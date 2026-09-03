from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"

AUTHORS = OUT / "bill_authors.csv"
PROJECTS = OUT / "projects.csv"
EDGES = OUT / "coauthorship_edges.csv"
PROFILES_JS = ROOT / "assets" / "js" / "profiles.js"
PUBLIC_JS = ROOT / "assets" / "js" / "coauthorship.js"
DETAIL_DIR = ROOT / "assets" / "data" / "coauthorship"
DIAGNOSTICS = OUT / "public_coauthorship_diagnostics.json"
SUMMARY_CSV = OUT / "member_coauthorship_summary.csv"

TERM_START = "2026-03-11"
TOP_VISIBLE = 8
SUMMARY_FIELDS = [
    "diputado_id",
    "diputado_nombre",
    "unique_coauthors",
    "recurrent_coauthors",
    "one_off_coauthors",
    "strongest_tie_shared_motions",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_profiles() -> dict[str, dict]:
    text = PROFILES_JS.read_text(encoding="utf-8")
    marker = "window.PROFILES = "
    if marker not in text:
        raise RuntimeError("No se reconoce profiles.js")
    raw = text.split(marker, 1)[1].strip()
    if raw.endswith(";"):
        raw = raw[:-1]
    return json.loads(raw)


def clean(value: object) -> str:
    return str(value or "").strip()


def pair_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b), key=int))


def main() -> None:
    authors = read_csv(AUTHORS)
    projects = read_csv(PROJECTS)
    edges = read_csv(EDGES)
    profiles = read_profiles()

    profile_by_id = {}
    for display_name, profile in profiles.items():
        deputy_id = clean(profile.get("id"))
        if not deputy_id:
            raise RuntimeError(f"Perfil sin ID: {display_name}")
        profile_by_id[deputy_id] = {
            "name": clean(profile.get("officialName")) or display_name,
        }

    project_lookup = {
        clean(row.get("boletin")): row
        for row in projects
        if clean(row.get("boletin"))
    }

    authors_by_bill: dict[str, dict[str, str]] = defaultdict(dict)
    for row in authors:
        if clean(row.get("author_chamber")) != "Diputado":
            continue
        bill = clean(row.get("boletin"))
        deputy_id = clean(row.get("author_id"))
        name = clean(row.get("author_name"))
        if bill and deputy_id and name:
            authors_by_bill[bill][deputy_id] = name

    pair_bills: dict[tuple[str, str], list[dict]] = defaultdict(list)
    person_names: dict[str, str] = {}
    eligible_bills = 0
    invalid_bills = []

    for bill, people in authors_by_bill.items():
        project = project_lookup.get(bill)
        if project is None:
            raise RuntimeError(f"Falta proyecto para boletín con autorías de diputados: {bill}")
        checks = (
            clean(project.get("origen_iniciativa")) == "parlamentario",
            clean(project.get("tipo_iniciativa")) == "Moción",
            clean(project.get("camara_origen")) == "Cámara de Diputados",
            clean(project.get("fecha_ingreso")) >= TERM_START,
        )
        if not all(checks):
            # bill_authors también contiene mociones originadas en Senado. Esas
            # no pertenecen al universo de coautoría de diputados de la ficha.
            continue
        eligible_bills += 1
        for deputy_id, name in people.items():
            person_names[deputy_id] = name
        if len(people) < 2:
            continue
        bill_meta = {
            "boletin": bill,
            "title": clean(project.get("titulo")),
            "date": clean(project.get("fecha_ingreso")),
            "state": clean(project.get("estado_actual")),
            "url": clean(project.get("source_url")),
            "formalAuthorCount": len(people),
        }
        for a, b in combinations(sorted(people, key=int), 2):
            pair_bills[pair_key(a, b)].append(bill_meta)

    # Reconciliación con la red derivada ya existente.
    expected_edges = {}
    for row in edges:
        if row.get("source_chamber") != "Diputado" or row.get("target_chamber") != "Diputado":
            continue
        key = pair_key(clean(row.get("source_id")), clean(row.get("target_id")))
        if key in expected_edges:
            raise RuntimeError(f"Arista duplicada en coauthorship_edges.csv: {key}")
        expected_edges[key] = int(row.get("shared_bills") or 0)

    observed_edges = {key: len(bills) for key, bills in pair_bills.items()}
    missing_edges = sorted(set(expected_edges) - set(observed_edges))
    extra_edges = sorted(set(observed_edges) - set(expected_edges))
    weight_mismatches = [
        {"pair": key, "expected": expected_edges[key], "observed": observed_edges[key]}
        for key in set(expected_edges) & set(observed_edges)
        if expected_edges[key] != observed_edges[key]
    ]
    if missing_edges or extra_edges or weight_mismatches:
        raise RuntimeError(
            "La reconstrucción de coautoría no coincide con coauthorship_edges.csv: "
            + json.dumps({
                "missing": missing_edges[:10],
                "extra": extra_edges[:10],
                "weights": weight_mismatches[:10],
            }, ensure_ascii=False)
        )

    incident: dict[str, list[dict]] = defaultdict(list)
    for (a, b), bills in pair_bills.items():
        sorted_bills = sorted(bills, key=lambda row: (row["date"], row["boletin"]), reverse=True)
        for central, other in ((a, b), (b, a)):
            incident[central].append({
                "id": other,
                "name": person_names.get(other, ""),
                "sharedMotions": len(sorted_bills),
                "firstSharedDate": min((row["date"] for row in sorted_bills), default=""),
                "lastSharedDate": max((row["date"] for row in sorted_bills), default=""),
                "profileAvailable": other in profile_by_id,
                "motions": sorted_bills,
            })

    summaries = {}
    details = {}
    summary_rows = []
    all_unique_counts = []
    all_recurrent_counts = []
    all_one_off_counts = []
    all_strongest = []

    for deputy_id in sorted(profile_by_id, key=int):
        name = profile_by_id[deputy_id]["name"]
        coauthors = sorted(
            incident.get(deputy_id, []),
            key=lambda row: (-row["sharedMotions"], row["name"], int(row["id"])),
        )
        unique_count = len(coauthors)
        recurrent = sum(row["sharedMotions"] >= 2 for row in coauthors)
        one_off = sum(row["sharedMotions"] == 1 for row in coauthors)
        strongest = max((row["sharedMotions"] for row in coauthors), default=0)

        if unique_count != recurrent + one_off:
            raise RuntimeError(f"Clasificación de vínculos rota para {deputy_id}")

        top = [
            {
                "id": row["id"],
                "name": row["name"],
                "sharedMotions": row["sharedMotions"],
                "profileAvailable": row["profileAvailable"],
            }
            for row in coauthors[:TOP_VISIBLE]
        ]
        summaries[deputy_id] = {
            "name": name,
            "uniqueCoauthors": unique_count,
            "recurrentCoauthors": recurrent,
            "oneOffCoauthors": one_off,
            "strongestTie": strongest,
            "topVisible": top,
        }
        details[deputy_id] = {
            "id": deputy_id,
            "name": name,
            "coauthors": coauthors,
        }
        summary_rows.append({
            "diputado_id": deputy_id,
            "diputado_nombre": name,
            "unique_coauthors": unique_count,
            "recurrent_coauthors": recurrent,
            "one_off_coauthors": one_off,
            "strongest_tie_shared_motions": strongest,
        })
        all_unique_counts.append(unique_count)
        all_recurrent_counts.append(recurrent)
        all_one_off_counts.append(one_off)
        all_strongest.append(strongest)

    with SUMMARY_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(summary_rows)

    payload = {
        "meta": {
            "termStart": TERM_START,
            "generatedFor": str(date.today()),
            "topVisible": TOP_VISIBLE,
            "detailPathTemplate": "assets/data/coauthorship/{id}.json",
            "edgeWeight": "número de mociones en que ambas personas figuran como autoras formales",
            "note": "Los vínculos visibles son solo los más repetidos; la lista completa permanece disponible en el shard individual.",
        },
        "members": summaries,
    }
    PUBLIC_JS.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_JS.write_text(
        "window.LEGISLATIVE_COAUTHORSHIP = "
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
        path.write_text(json.dumps(detail, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        sizes.append(path.stat().st_size)

    diagnostics = {
        "generated_for": str(date.today()),
        "term_start": TERM_START,
        "current_profiles": len(profile_by_id),
        "eligible_chamber_motions": eligible_bills,
        "reconstructed_deputy_edges": len(observed_edges),
        "expected_deputy_edges": len(expected_edges),
        "edge_weight_mismatches": 0,
        "current_profiles_without_coauthors": sum(v == 0 for v in all_unique_counts),
        "unique_coauthors": {
            "min": min(all_unique_counts, default=0),
            "median": sorted(all_unique_counts)[len(all_unique_counts)//2] if all_unique_counts else 0,
            "max": max(all_unique_counts, default=0),
        },
        "recurrent_coauthors": {
            "min": min(all_recurrent_counts, default=0),
            "median": sorted(all_recurrent_counts)[len(all_recurrent_counts)//2] if all_recurrent_counts else 0,
            "max": max(all_recurrent_counts, default=0),
        },
        "one_off_coauthors": {
            "min": min(all_one_off_counts, default=0),
            "median": sorted(all_one_off_counts)[len(all_one_off_counts)//2] if all_one_off_counts else 0,
            "max": max(all_one_off_counts, default=0),
        },
        "strongest_tie": {
            "max": max(all_strongest, default=0),
        },
        "detail_files": len(details),
        "detail_file_size_bytes": {
            "min": min(sizes, default=0),
            "max": max(sizes, default=0),
            "total": sum(sizes),
        },
        "public_top_visible": TOP_VISIBLE,
        "method_note": (
            "Dos personas están conectadas si figuran formalmente como autoras de la misma moción de origen Cámara durante el período. "
            "El peso es el número de mociones compartidas. La coautoría no se interpreta automáticamente como afinidad ideológica, amistad, coordinación estable ni intensidad causal de colaboración."
        ),
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if len(profile_by_id) != 155:
        raise RuntimeError(f"Se esperaban 155 perfiles y hay {len(profile_by_id)}")
    if len(details) != len(profile_by_id):
        raise RuntimeError("No se produjo un shard por perfil")

    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
