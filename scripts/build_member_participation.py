from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
MEMBER_VOTES = OUT / "member_votes.csv"
ROLLCALLS = OUT / "rollcalls.csv"
PROJECTS = OUT / "projects.csv"
INHERITED_PROJECTS = OUT / "topics" / "rollcall_inherited_topic_final.csv"
OUTPUT = OUT / "member_participation_summary.csv"
DIAGNOSTICS = OUT / "member_participation_diagnostics.json"
PUBLIC_OUTPUT = ROOT / "assets" / "js" / "participation.js"
PUBLIC_DATA = ROOT / "assets" / "data"
PUBLIC_ROLLCALLS = PUBLIC_DATA / "participation_rollcalls.json"
PUBLIC_MEMBER_VOTES = PUBLIC_DATA / "participation_member_votes.json"

EXPECTED_SEATS_PER_ROLLCALL = 155
SUBSTANTIVE = {"Afirmativo", "En Contra", "Abstención"}
KNOWN_OPTIONS = SUBSTANTIVE | {"No Vota", "Dispensado"}
OPTION_CODES = {
    "Afirmativo": "A",
    "En Contra": "E",
    "Abstención": "B",
    "No Vota": "N",
    "Dispensado": "D",
}

FIELDS = [
    "diputado_id",
    "diputado_nombre",
    "opportunity_rollcalls",
    "rollcalls_total",
    "first_opportunity_date",
    "last_opportunity_date",
    "n_affirmative",
    "n_against",
    "n_abstention",
    "n_no_vote",
    "n_excused",
    "n_substantive",
    "substantive_participation_pct",
    "n_binary",
    "binary_participation_pct",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(num: int, den: int) -> str:
    return f"{100 * num / den:.4f}" if den else ""


def public_record(row: dict) -> dict:
    return {
        "id": str(row["diputado_id"]),
        "name": row["diputado_nombre"],
        "opportunities": int(row["opportunity_rollcalls"]),
        "firstOpportunityDate": row["first_opportunity_date"],
        "lastOpportunityDate": row["last_opportunity_date"],
        "affirmative": int(row["n_affirmative"]),
        "against": int(row["n_against"]),
        "abstention": int(row["n_abstention"]),
        "noVote": int(row["n_no_vote"]),
        "excused": int(row["n_excused"]),
        "substantive": int(row["n_substantive"]),
        "substantiveParticipationPct": float(row["substantive_participation_pct"]),
        "binary": int(row["n_binary"]),
        "binaryParticipationPct": float(row["binary_participation_pct"]),
    }


def clean_object(row: dict) -> str:
    article = (row.get("articulo") or "").strip()
    description = (row.get("descripcion") or "").strip()
    bulletin = (row.get("boletin") or "").strip()
    generic_descriptions = {
        f"Boletín N°{bulletin}",
        f"Boletin N°{bulletin}",
        f"Boletín Nº{bulletin}",
    }
    if article:
        return article
    if description and description not in generic_descriptions:
        return description
    return "Votación del proyecto"


def main() -> None:
    votes = read_csv(MEMBER_VOTES)
    rollcalls = read_csv(ROLLCALLS)
    projects = read_csv(PROJECTS)
    inherited_projects = read_csv(INHERITED_PROJECTS)
    if not votes or not rollcalls:
        raise RuntimeError("Las tablas de entrada están vacías")

    rollcall_by_id = {row["vote_id"]: row for row in rollcalls if row.get("vote_id")}
    if len(rollcall_by_id) != len(rollcalls):
        raise RuntimeError("rollcalls.csv contiene vote_id duplicados o vacíos")

    project_title_by_bill = {
        (row.get("boletin") or "").strip(): (row.get("titulo") or "").strip()
        for row in projects
        if (row.get("boletin") or "").strip() and (row.get("titulo") or "").strip()
    }
    for row in inherited_projects:
        bulletin = (row.get("boletin") or "").strip()
        title = (row.get("titulo") or "").strip()
        if bulletin and title:
            project_title_by_bill.setdefault(bulletin, title)

    keys = [(row.get("vote_id", ""), row.get("diputado_id", "")) for row in votes]
    if any(not vote_id or not deputy_id for vote_id, deputy_id in keys):
        raise RuntimeError("member_votes.csv contiene claves vote_id × diputado_id incompletas")
    if len(set(keys)) != len(keys):
        raise RuntimeError("member_votes.csv contiene pares vote_id × diputado_id duplicados")

    missing_rollcall_ids = sorted({row["vote_id"] for row in votes if row["vote_id"] not in rollcall_by_id})
    if missing_rollcall_ids:
        raise RuntimeError(f"Hay votos nominales sin roll call asociado: {missing_rollcall_ids[:20]}")

    counts_by_rollcall = Counter(row["vote_id"] for row in votes)
    bad_rollcalls = {
        vote_id: count
        for vote_id, count in counts_by_rollcall.items()
        if count != EXPECTED_SEATS_PER_ROLLCALL
    }
    if bad_rollcalls:
        raise RuntimeError(
            "No todas las votaciones tienen 155 registros nominales; no es seguro construir el denominador público: "
            f"{bad_rollcalls}"
        )

    unknown_options = Counter(
        row.get("opcion", "") for row in votes if row.get("opcion", "") not in KNOWN_OPTIONS
    )
    if unknown_options:
        raise RuntimeError(f"Aparecieron opciones de voto no contempladas: {dict(unknown_options)}")

    by_member: dict[str, list[dict]] = defaultdict(list)
    for row in votes:
        enriched = dict(row)
        enriched["fecha"] = rollcall_by_id[row["vote_id"]].get("fecha", "")
        by_member[row["diputado_id"]].append(enriched)

    output_rows = []
    for deputy_id, member_votes in sorted(by_member.items(), key=lambda item: int(item[0])):
        member_votes.sort(key=lambda row: (row.get("fecha", ""), row["vote_id"]))
        names = [row.get("diputado_nombre", "").strip() for row in member_votes if row.get("diputado_nombre", "").strip()]
        name = Counter(names).most_common(1)[0][0] if names else ""
        counts = Counter(row["opcion"] for row in member_votes)

        opportunities = len(member_votes)
        n_substantive = sum(counts[option] for option in SUBSTANTIVE)
        n_binary = counts["Afirmativo"] + counts["En Contra"]
        dates = [row.get("fecha", "") for row in member_votes if row.get("fecha", "")]

        output_rows.append({
            "diputado_id": deputy_id,
            "diputado_nombre": name,
            "opportunity_rollcalls": opportunities,
            # Alias conservado por compatibilidad. Desde v0.2 significa oportunidades
            # observadas para esa persona, no total de roll calls de la legislatura.
            "rollcalls_total": opportunities,
            "first_opportunity_date": min(dates) if dates else "",
            "last_opportunity_date": max(dates) if dates else "",
            "n_affirmative": counts["Afirmativo"],
            "n_against": counts["En Contra"],
            "n_abstention": counts["Abstención"],
            "n_no_vote": counts["No Vota"],
            "n_excused": counts["Dispensado"],
            "n_substantive": n_substantive,
            "substantive_participation_pct": pct(n_substantive, opportunities),
            "n_binary": n_binary,
            "binary_participation_pct": pct(n_binary, opportunities),
        })

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output_rows)

    public_payload = {
        "meta": {
            "source": "Cámara de Diputadas y Diputados de Chile",
            "periodStart": min((row.get("fecha", "") for row in rollcalls if row.get("fecha", "")), default=""),
            "dataCut": max((row.get("fecha", "") for row in rollcalls if row.get("fecha", "")), default=""),
            "rollcalls": len(rollcalls),
            "denominator": "Cada registro nominal oficial vote_id × diputado_id cuenta como una oportunidad efectiva.",
        },
        "members": {row["diputado_id"]: public_record(row) for row in output_rows},
    }
    PUBLIC_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUTPUT.write_text(
        "window.LEGISLATIVE_PARTICIPATION = "
        + json.dumps(public_payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )

    public_rollcalls = {}
    missing_project_titles = []
    for vote_id, row in sorted(rollcall_by_id.items(), key=lambda item: (item[1].get("fecha", ""), int(item[0]))):
        bulletin = (row.get("boletin") or "").strip()
        title = project_title_by_bill.get(bulletin, "")
        if not title:
            missing_project_titles.append({"vote_id": vote_id, "boletin": bulletin})
            title = f"Proyecto boletín {bulletin}" if bulletin else "Votación de Sala"
        public_rollcalls[vote_id] = {
            "bulletin": bulletin,
            "date": row.get("fecha", ""),
            "title": title,
            "object": clean_object(row),
            "result": row.get("resultado", ""),
            "url": row.get("verification_url", ""),
        }

    public_member_votes = {
        deputy_id: [
            [row["vote_id"], OPTION_CODES[row["opcion"]]]
            for row in sorted(member_votes, key=lambda x: (x.get("fecha", ""), int(x["vote_id"])))
        ]
        for deputy_id, member_votes in sorted(by_member.items(), key=lambda item: int(item[0]))
    }

    PUBLIC_DATA.mkdir(parents=True, exist_ok=True)
    PUBLIC_ROLLCALLS.write_text(
        json.dumps({"rollcalls": public_rollcalls}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    PUBLIC_MEMBER_VOTES.write_text(
        json.dumps({"members": public_member_votes}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    opportunity_counts = [int(row["opportunity_rollcalls"]) for row in output_rows]
    full_rollcall_count = len(rollcalls)
    diagnostics = {
        "input_vote_rows": len(votes),
        "rollcalls": full_rollcall_count,
        "rollcalls_with_155_rows": sum(
            count == EXPECTED_SEATS_PER_ROLLCALL for count in counts_by_rollcall.values()
        ),
        "historical_members_observed": len(by_member),
        "participation_rows": len(output_rows),
        "public_asset_members": len(public_payload["members"]),
        "public_rollcalls": len(public_rollcalls),
        "public_member_vote_rows": sum(len(rows) for rows in public_member_votes.values()),
        "public_rollcalls_without_project_title": len(missing_project_titles),
        "members_with_all_current_rollcalls_as_opportunities": sum(
            count == full_rollcall_count for count in opportunity_counts
        ),
        "min_opportunity_rollcalls": min(opportunity_counts) if opportunity_counts else 0,
        "max_opportunity_rollcalls": max(opportunity_counts) if opportunity_counts else 0,
        "sum_member_opportunities": sum(opportunity_counts),
        "vote_option_counts": dict(Counter(row["opcion"] for row in votes)),
        "denominator_rule": (
            "Cada fila oficial vote_id × diputado_id en member_votes.csv cuenta como una oportunidad efectiva de votación. "
            "La persona no recibe oportunidades por roll calls en los que su ID no aparece en el detalle nominal oficial."
        ),
        "public_method_note": (
            "Participación sustantiva = (Afirmativo + En Contra + Abstención) / oportunidades efectivas. "
            "No Vota y Dispensado se muestran por separado. Este indicador no es asistencia general al Congreso."
        ),
        "errors": {
            "bad_rollcalls": bad_rollcalls,
            "unknown_options": dict(unknown_options),
            "missing_rollcall_ids": missing_rollcall_ids[:20],
            "missing_project_title_examples": missing_project_titles[:20],
        },
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in diagnostics.items() if key != "errors"}, ensure_ascii=False, indent=2))

    if sum(opportunity_counts) != len(votes):
        raise RuntimeError("La suma de oportunidades individuales no reproduce las filas nominales de entrada")
    if len(output_rows) != len(by_member):
        raise RuntimeError("El resumen individual perdió integrantes observados")
    if len(public_payload["members"]) != len(output_rows):
        raise RuntimeError("El activo público perdió integrantes del resumen auditado")
    if len(public_rollcalls) != len(rollcalls):
        raise RuntimeError("La trazabilidad pública perdió votaciones")
    if sum(len(rows) for rows in public_member_votes.values()) != len(votes):
        raise RuntimeError("La trazabilidad pública perdió votos nominales")


if __name__ == "__main__":
    main()
