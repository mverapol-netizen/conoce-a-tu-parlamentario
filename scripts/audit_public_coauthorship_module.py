from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
EDGES = OUT / "coauthorship_edges.csv"
NODES = OUT / "coauthorship_nodes.csv"
DIAGNOSTICS = OUT / "public_coauthorship_module_diagnostics.json"

TOP_K = (5, 8, 10, 12, 15)


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    frac = pos - lo
    return ordered[lo] * (1 - frac) + ordered[hi] * frac


def main() -> None:
    edges = read_csv(EDGES)
    nodes = read_csv(NODES)

    deputy_nodes = {
        row["author_id"]: row
        for row in nodes
        if row.get("author_chamber") == "Diputado" and row.get("author_id")
    }
    deputy_edges = [
        row for row in edges
        if row.get("source_chamber") == "Diputado" and row.get("target_chamber") == "Diputado"
    ]

    incident: dict[str, list[dict]] = defaultdict(list)
    duplicate_pairs = []
    seen_pairs = set()
    for row in deputy_edges:
        a, b = row["source_id"], row["target_id"]
        pair = tuple(sorted((a, b), key=int))
        if pair in seen_pairs:
            duplicate_pairs.append(pair)
        seen_pairs.add(pair)
        w = int(row.get("shared_bills") or 0)
        incident[a].append({"other": b, "weight": w})
        incident[b].append({"other": a, "weight": w})

    if duplicate_pairs:
        raise RuntimeError(f"Aristas duplicadas: {duplicate_pairs[:10]}")

    unique_counts = []
    weighted_degrees = []
    max_ties = []
    one_off_shares = []
    isolated = []
    coverage_by_k: dict[int, list[float]] = {k: [] for k in TOP_K}
    visible_nodes_by_k: dict[int, list[int]] = {k: [] for k in TOP_K}
    member_rows = []

    for deputy_id, node in deputy_nodes.items():
        ties = sorted(incident.get(deputy_id, []), key=lambda row: (-row["weight"], int(row["other"])))
        unique = len(ties)
        weighted = sum(row["weight"] for row in ties)
        max_tie = max((row["weight"] for row in ties), default=0)
        one_off = sum(row["weight"] == 1 for row in ties)
        if not ties:
            isolated.append(deputy_id)

        unique_counts.append(unique)
        weighted_degrees.append(weighted)
        max_ties.append(max_tie)
        one_off_shares.append(100 * one_off / unique if unique else 0.0)

        coverages = {}
        for k in TOP_K:
            visible = min(k, unique)
            visible_nodes_by_k[k].append(visible)
            top_weight = sum(row["weight"] for row in ties[:k])
            coverage = 100 * top_weight / weighted if weighted else 100.0
            coverage_by_k[k].append(coverage)
            coverages[str(k)] = round(coverage, 2)

        member_rows.append({
            "diputado_id": deputy_id,
            "diputado_nombre": node.get("author_name", ""),
            "unique_coauthors": unique,
            "weighted_degree": weighted,
            "max_shared_bills_with_one_coauthor": max_tie,
            "one_off_coauthors": one_off,
            "one_off_coauthor_share_pct": round(100 * one_off / unique, 2) if unique else 0.0,
            "top_k_weight_coverage_pct": coverages,
        })

    member_rows.sort(key=lambda row: (-row["unique_coauthors"], -row["weighted_degree"], row["diputado_nombre"]))

    top_edge = max(deputy_edges, key=lambda row: int(row.get("shared_bills") or 0), default=None)
    diagnostics = {
        "deputy_nodes": len(deputy_nodes),
        "deputy_edges": len(deputy_edges),
        "isolated_deputies": len(isolated),
        "isolated_ids": isolated,
        "unique_coauthors": {
            "min": min(unique_counts, default=0),
            "p10": round(quantile(unique_counts, .10) or 0, 2),
            "median": round(median(unique_counts), 2) if unique_counts else 0,
            "p90": round(quantile(unique_counts, .90) or 0, 2),
            "max": max(unique_counts, default=0),
        },
        "weighted_degree": {
            "min": min(weighted_degrees, default=0),
            "median": round(median(weighted_degrees), 2) if weighted_degrees else 0,
            "p90": round(quantile(weighted_degrees, .90) or 0, 2),
            "max": max(weighted_degrees, default=0),
        },
        "max_tie_strength_per_member": {
            "median": round(median(max_ties), 2) if max_ties else 0,
            "p90": round(quantile(max_ties, .90) or 0, 2),
            "max": max(max_ties, default=0),
        },
        "one_off_coauthor_share_pct": {
            "median": round(median(one_off_shares), 2) if one_off_shares else 0,
            "p90": round(quantile(one_off_shares, .90) or 0, 2),
        },
        "top_k_weight_coverage_pct": {
            str(k): {
                "median": round(median(coverage_by_k[k]), 2),
                "p10": round(quantile(coverage_by_k[k], .10) or 0, 2),
                "p90": round(quantile(coverage_by_k[k], .90) or 0, 2),
                "members_below_50pct": sum(v < 50 for v in coverage_by_k[k]),
                "members_below_70pct": sum(v < 70 for v in coverage_by_k[k]),
            }
            for k in TOP_K
        },
        "strongest_deputy_edge": {
            "source_id": top_edge.get("source_id") if top_edge else None,
            "source_name": top_edge.get("source_name") if top_edge else None,
            "target_id": top_edge.get("target_id") if top_edge else None,
            "target_name": top_edge.get("target_name") if top_edge else None,
            "shared_bills": int(top_edge.get("shared_bills") or 0) if top_edge else 0,
        },
        "highest_unique_coauthor_profiles": member_rows[:10],
        "method_note": (
            "La cobertura top-k se calcula sobre weighted_degree, es decir, la suma de mociones compartidas a través de todos los vínculos de coautoría de la persona. "
            "No es proporción de mociones únicas: una moción con varios coautores contribuye a varios vínculos."
        ),
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if len(deputy_nodes) != 155:
        raise RuntimeError(f"Se esperaban 155 nodos de diputados y hay {len(deputy_nodes)}")
    if any(int(row["unique_coauthors"]) != len(incident.get(row["diputado_id"], [])) for row in member_rows):
        raise RuntimeError("La reconstrucción de grados no coincide")

    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
