from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"

AUTHOR_FILE = OUT / "bill_authors.csv"
PROJECT_FILE = OUT / "projects.csv"
NODE_FILE = OUT / "coauthorship_nodes.csv"
EDGE_FILE = OUT / "coauthorship_edges.csv"
DIAGNOSTICS_FILE = OUT / "coauthorship_diagnostics.json"

NODE_FIELDS = [
    "author_id",
    "author_name",
    "author_chamber",
    "authored_bills",
    "coauthored_bills",
    "solo_bills",
    "unique_coauthors",
    "weighted_degree",
]

EDGE_FIELDS = [
    "source_id",
    "source_name",
    "source_chamber",
    "target_id",
    "target_name",
    "target_chamber",
    "shared_bills",
    "first_shared_bill_date",
    "last_shared_bill_date",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"No existe {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def person_key(row: dict) -> tuple[str, str]:
    """Usa cámara + ID para impedir colisiones entre cámaras.

    El ID oficial es la clave principal. Si faltara excepcionalmente, usamos el
    nombre como respaldo explícito para no perder una autoría primaria.
    """
    chamber = (row.get("author_chamber") or "Sin cámara").strip()
    author_id = (row.get("author_id") or "").strip()
    if author_id:
        return chamber, author_id
    return chamber, f"name:{(row.get('author_name') or '').strip()}"


def canonical_pair(a: tuple[str, str], b: tuple[str, str]) -> tuple[tuple[str, str], tuple[str, str]]:
    return (a, b) if a <= b else (b, a)


def main() -> None:
    authors = read_csv(AUTHOR_FILE)
    projects = read_csv(PROJECT_FILE)

    project_dates = {
        (row.get("boletin") or "").strip(): (row.get("fecha_ingreso") or "").strip()
        for row in projects
        if (row.get("boletin") or "").strip()
    }

    by_bill: dict[str, dict[tuple[str, str], dict]] = defaultdict(dict)
    people: dict[tuple[str, str], dict] = {}

    for row in authors:
        bill = (row.get("boletin") or "").strip()
        name = (row.get("author_name") or "").strip()
        if not bill or not name:
            continue
        key = person_key(row)
        person = {
            "author_id": (row.get("author_id") or "").strip(),
            "author_name": name,
            "author_chamber": (row.get("author_chamber") or "Sin cámara").strip(),
        }
        # Una relación repetida dentro de un mismo boletín no debe duplicar aristas.
        by_bill[bill][key] = person
        people[key] = person

    authored_bills: Counter = Counter()
    coauthored_bills: Counter = Counter()
    solo_bills: Counter = Counter()
    coauthors: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    weighted_degree: Counter = Counter()
    edges: dict[tuple[tuple[str, str], tuple[str, str]], dict] = {}

    for bill, members_by_key in by_bill.items():
        members = sorted(members_by_key.items(), key=lambda item: item[0])
        for key, _person in members:
            authored_bills[key] += 1

        if len(members) == 1:
            solo_bills[members[0][0]] += 1
            continue

        for key, _person in members:
            coauthored_bills[key] += 1

        bill_date = project_dates.get(bill, "")
        for (key_a, person_a), (key_b, person_b) in combinations(members, 2):
            pair = canonical_pair(key_a, key_b)
            if pair not in edges:
                left = people[pair[0]]
                right = people[pair[1]]
                edges[pair] = {
                    "source_id": left["author_id"],
                    "source_name": left["author_name"],
                    "source_chamber": left["author_chamber"],
                    "target_id": right["author_id"],
                    "target_name": right["author_name"],
                    "target_chamber": right["author_chamber"],
                    "shared_bills": 0,
                    "first_shared_bill_date": "",
                    "last_shared_bill_date": "",
                }
            edge = edges[pair]
            edge["shared_bills"] += 1
            if bill_date:
                first = edge["first_shared_bill_date"]
                last = edge["last_shared_bill_date"]
                edge["first_shared_bill_date"] = bill_date if not first or bill_date < first else first
                edge["last_shared_bill_date"] = bill_date if not last or bill_date > last else last

            coauthors[key_a].add(key_b)
            coauthors[key_b].add(key_a)
            weighted_degree[key_a] += 1
            weighted_degree[key_b] += 1

    node_rows = []
    for key, person in sorted(people.items(), key=lambda item: (item[1]["author_chamber"], item[1]["author_name"])):
        node_rows.append(
            {
                **person,
                "authored_bills": authored_bills[key],
                "coauthored_bills": coauthored_bills[key],
                "solo_bills": solo_bills[key],
                "unique_coauthors": len(coauthors[key]),
                "weighted_degree": weighted_degree[key],
            }
        )

    edge_rows = sorted(
        edges.values(),
        key=lambda row: (-int(row["shared_bills"]), row["source_name"], row["target_name"]),
    )

    write_csv(NODE_FILE, node_rows, NODE_FIELDS)
    write_csv(EDGE_FILE, edge_rows, EDGE_FIELDS)

    chamber_nodes = Counter(row["author_chamber"] for row in node_rows)
    chamber_edges = Counter()
    for row in edge_rows:
        a = row["source_chamber"]
        b = row["target_chamber"]
        chamber_edges[a if a == b else "Intercámara"] += 1

    diagnostics = {
        "generated_for": str(date.today()),
        "primary_author_rows": len(authors),
        "motions_with_authors": len(by_bill),
        "nodes": len(node_rows),
        "edges": len(edge_rows),
        "nodes_by_chamber": dict(sorted(chamber_nodes.items())),
        "edges_by_scope": dict(sorted(chamber_edges.items())),
        "multi_author_motions": sum(len(members) > 1 for members in by_bill.values()),
        "solo_author_motions": sum(len(members) == 1 for members in by_bill.values()),
        "max_shared_bills_edge": max((int(row["shared_bills"]) for row in edge_rows), default=0),
        "note": "Red derivada de bill_authors.csv; los datos primarios no se modifican.",
    }
    DIAGNOSTICS_FILE.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if len(node_rows) < 100:
        raise RuntimeError(f"Red sospechosamente pequeña: {len(node_rows)} nodos")
    if not edge_rows:
        raise RuntimeError("La red no produjo aristas de coautoría")

    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
