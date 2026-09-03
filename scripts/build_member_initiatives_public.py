from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"

AUTHORS = OUT / "bill_authors.csv"
PROJECTS = OUT / "projects.csv"
NODES = OUT / "coauthorship_nodes.csv"
PROFILES_JS = ROOT / "assets" / "js" / "profiles.js"
PUBLIC_JS = ROOT / "assets" / "js" / "initiatives.js"
DETAIL_DIR = ROOT / "assets" / "data" / "initiatives"
DIAGNOSTICS = OUT / "member_initiatives_public_diagnostics.json"
SUMMARY_CSV = OUT / "member_initiatives_summary.csv"

TERM_START = "2026-03-11"
SUMMARY_FIELDS = [
    "diputado_id",
    "diputado_nombre",
    "authored_motions",
    "coauthored_motions",
    "solo_motions",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_profiles() -> dict[str, dict]:
    if not PROFILES_JS.exists():
        raise RuntimeError("Falta assets/js/profiles.js")
    text = PROFILES_JS.read_text(encoding="utf-8")
    marker = "window.PROFILES = "
    if marker not in text:
        raise RuntimeError("No se reconoce el formato de profiles.js")
    raw = text.split(marker, 1)[1].strip()
    if raw.endswith(";"):
        raw = raw[:-1]
    profiles = json.loads(raw)
    if not isinstance(profiles, dict) or not profiles:
        raise RuntimeError("profiles.js no contiene perfiles")
    return profiles


def clean(value: object) -> str:
    return str(value or "").strip()


def main() -> None:
    authors = read_csv(AUTHORS)
    projects = read_csv(PROJECTS)
    nodes = read_csv(NODES)
    profiles = read_profiles()

    profile_by_id: dict[str, dict] = {}
    for display_name, profile in profiles.items():
        deputy_id = clean(profile.get("id"))
        if not deputy_id:
            raise RuntimeError(f"Perfil sin id: {display_name}")
        if deputy_id in profile_by_id:
            raise RuntimeError(f"ID de perfil duplicado: {deputy_id}")
        profile_by_id[deputy_id] = {
            "name": clean(profile.get("officialName")) or display_name,
            "display_name": display_name,
        }

    project_lookup: dict[str, dict] = {}
    duplicate_projects = []
    for row in projects:
        bill = clean(row.get("boletin"))
        if not bill:
            continue
        if bill in project_lookup:
            duplicate_projects.append(bill)
        project_lookup[bill] = row
    if duplicate_projects:
        raise RuntimeError(f"Boletines duplicados en projects.csv: {duplicate_projects[:10]}")

    # Deduplica relaciones autor-boletín. La tabla primaria debería ser 1:1 en
    # esa clave, pero el constructor no permite que una repetición infle cifras.
    relation_lookup: dict[tuple[str, str, str], dict] = {}
    duplicated_author_relations = []
    authors_by_bill: dict[str, dict[tuple[str, str], dict]] = defaultdict(dict)
    for row in authors:
        bill = clean(row.get("boletin"))
        chamber = clean(row.get("author_chamber")) or "Sin cámara"
        author_id = clean(row.get("author_id"))
        author_name = clean(row.get("author_name"))
        if not bill or not author_name:
            continue
        person_id = author_id or f"name:{author_name}"
        relation_key = (bill, chamber, person_id)
        if relation_key in relation_lookup:
            duplicated_author_relations.append(relation_key)
        relation_lookup[relation_key] = row
        authors_by_bill[bill][(chamber, person_id)] = row

    if duplicated_author_relations:
        raise RuntimeError(
            f"Relaciones autor-boletín duplicadas: {duplicated_author_relations[:10]}"
        )

    current_rows_by_member: dict[str, list[dict]] = defaultdict(list)
    historical_deputy_author_ids = set()
    missing_projects = []
    invalid_current_relations = []

    for (bill, chamber, person_id), row in relation_lookup.items():
        if chamber != "Diputado":
            continue
        author_id = clean(row.get("author_id"))
        if author_id:
            historical_deputy_author_ids.add(author_id)
        if author_id not in profile_by_id:
            continue

        project = project_lookup.get(bill)
        if project is None:
            missing_projects.append({"boletin": bill, "author_id": author_id})
            continue

        checks = {
            "origen_iniciativa": clean(project.get("origen_iniciativa")) == "parlamentario",
            "tipo_iniciativa": clean(project.get("tipo_iniciativa")) == "Moción",
            "camara_origen": clean(project.get("camara_origen")) == "Cámara de Diputados",
            "fecha_periodo": clean(project.get("fecha_ingreso")) >= TERM_START,
        }
        if not all(checks.values()):
            invalid_current_relations.append(
                {
                    "boletin": bill,
                    "author_id": author_id,
                    "checks": checks,
                    "project": {
                        "fecha_ingreso": project.get("fecha_ingreso"),
                        "origen_iniciativa": project.get("origen_iniciativa"),
                        "tipo_iniciativa": project.get("tipo_iniciativa"),
                        "camara_origen": project.get("camara_origen"),
                    },
                }
            )
            continue

        current_rows_by_member[author_id].append(row)

    if missing_projects:
        raise RuntimeError(f"Autorías de diputados sin proyecto: {missing_projects[:10]}")
    if invalid_current_relations:
        raise RuntimeError(
            "Autorías actuales fuera del contrato de mociones de Cámara/período: "
            + json.dumps(invalid_current_relations[:10], ensure_ascii=False)
        )

    node_lookup = {
        clean(row.get("author_id")): row
        for row in nodes
        if clean(row.get("author_chamber")) == "Diputado" and clean(row.get("author_id"))
    }

    summaries = {}
    details = {}
    summary_rows = []
    node_mismatches = []
    project_author_count_distribution = Counter()

    for deputy_id in sorted(profile_by_id, key=int):
        profile = profile_by_id[deputy_id]
        member_rows = current_rows_by_member.get(deputy_id, [])
        member_bills = sorted({clean(row.get("boletin")) for row in member_rows})

        member_details = []
        solo = 0
        coauthored = 0
        for bill in member_bills:
            project = project_lookup[bill]
            formal_author_count = len(authors_by_bill.get(bill, {}))
            if formal_author_count < 1:
                raise RuntimeError(f"Moción {bill} sin autores formales")
            project_author_count_distribution[formal_author_count] += 1
            is_solo = formal_author_count == 1
            if is_solo:
                solo += 1
            else:
                coauthored += 1
            member_details.append(
                {
                    "boletin": bill,
                    "title": clean(project.get("titulo")),
                    "date": clean(project.get("fecha_ingreso")),
                    "state": clean(project.get("estado_actual")),
                    "url": clean(project.get("source_url")),
                    "formalAuthorCount": formal_author_count,
                    "authorship": "individual" if is_solo else "shared",
                }
            )

        member_details.sort(key=lambda row: (row["date"], row["boletin"]), reverse=True)
        total = len(member_details)
        if total != solo + coauthored:
            raise RuntimeError(f"Identidad de autoría rota para {deputy_id}")

        node = node_lookup.get(deputy_id)
        if node:
            expected = (
                int(node.get("authored_bills") or 0),
                int(node.get("coauthored_bills") or 0),
                int(node.get("solo_bills") or 0),
            )
            observed = (total, coauthored, solo)
            if expected != observed:
                node_mismatches.append(
                    {
                        "diputado_id": deputy_id,
                        "name": profile["name"],
                        "coauthorship_nodes": expected,
                        "public_builder": observed,
                    }
                )
        elif total:
            node_mismatches.append(
                {
                    "diputado_id": deputy_id,
                    "name": profile["name"],
                    "coauthorship_nodes": None,
                    "public_builder": (total, coauthored, solo),
                }
            )

        summaries[deputy_id] = {
            "name": profile["name"],
            "motions": total,
            "shared": coauthored,
            "individual": solo,
        }
        details[deputy_id] = {
            "id": deputy_id,
            "name": profile["name"],
            "motions": member_details,
        }
        summary_rows.append(
            {
                "diputado_id": deputy_id,
                "diputado_nombre": profile["name"],
                "authored_motions": total,
                "coauthored_motions": coauthored,
                "solo_motions": solo,
            }
        )

    if node_mismatches:
        raise RuntimeError(
            "El resumen público no coincide con coauthorship_nodes.csv: "
            + json.dumps(node_mismatches[:10], ensure_ascii=False)
        )

    with SUMMARY_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(summary_rows)

    PUBLIC_JS.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "meta": {
            "termStart": TERM_START,
            "generatedFor": str(date.today()),
            "detailPathTemplate": "assets/data/initiatives/{id}.json",
            "unit": "mociones en que la persona figura como autor/a formal",
        },
        "members": summaries,
    }
    PUBLIC_JS.write_text(
        "window.LEGISLATIVE_INITIATIVES = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )

    DETAIL_DIR.mkdir(parents=True, exist_ok=True)
    expected_files = {f"{deputy_id}.json" for deputy_id in profile_by_id}
    for stale in DETAIL_DIR.glob("*.json"):
        if stale.name not in expected_files:
            stale.unlink()
    sizes = []
    for deputy_id, detail in details.items():
        path = DETAIL_DIR / f"{deputy_id}.json"
        path.write_text(
            json.dumps(detail, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        sizes.append(path.stat().st_size)

    totals = {
        "member_motion_relations": sum(row["authored_motions"] for row in summary_rows),
        "shared_relations": sum(row["coauthored_motions"] for row in summary_rows),
        "individual_relations": sum(row["solo_motions"] for row in summary_rows),
    }
    motion_counts = [row["authored_motions"] for row in summary_rows]
    diagnostics = {
        "generated_for": str(date.today()),
        "term_start": TERM_START,
        "current_profiles": len(profile_by_id),
        "historical_deputy_author_ids_in_primary_data": len(historical_deputy_author_ids),
        "current_members_with_motions": sum(value > 0 for value in motion_counts),
        "current_members_with_zero_motions": sum(value == 0 for value in motion_counts),
        "current_member_motion_relations": totals["member_motion_relations"],
        "current_member_shared_relations": totals["shared_relations"],
        "current_member_individual_relations": totals["individual_relations"],
        "unique_current_chamber_motions": len(
            {
                clean(row.get("boletin"))
                for member_rows in current_rows_by_member.values()
                for row in member_rows
            }
        ),
        "max_motions_by_member": max(motion_counts, default=0),
        "detail_files": len(details),
        "detail_file_size_bytes": {
            "min": min(sizes, default=0),
            "max": max(sizes, default=0),
            "total": sum(sizes),
        },
        "duplicate_author_relations": 0,
        "missing_projects": 0,
        "invalid_current_relations": 0,
        "coauthorship_node_mismatches": 0,
        "method_note": (
            "Una moción cuenta una sola vez por diputado y boletín. Autoría individual significa que la lista formal del boletín contiene una sola persona; autoría compartida, dos o más. "
            "El indicador describe autoría formal registrada y no atribuye redacción, esfuerzo, calidad, éxito ni impacto."
        ),
    }
    DIAGNOSTICS.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if len(details) != len(profile_by_id):
        raise RuntimeError("No se generó un shard por perfil actual")
    if totals["member_motion_relations"] != totals["shared_relations"] + totals["individual_relations"]:
        raise RuntimeError("Los totales públicos no cierran")

    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
