from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
ELIGIBILITY = OUT / "rollcall_model_eligibility.csv"
VOTES = OUT / "member_votes_enriched.csv"
OUTPUT = OUT / "rollcall_redundancy_by_bill.csv"
DIAGNOSTICS = OUT / "rollcall_redundancy_diagnostics.json"

LOP = 0.025

FIELDS = [
    "boletin", "topic_primary", "origin_initiative", "eligible_rollcalls",
    "unique_binary_patterns", "duplicate_rollcalls", "duplicate_share",
    "largest_pattern_multiplicity", "largest_pattern_share",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def safe_int(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def model_code(option: str) -> str:
    if option == "Afirmativo":
        return "1"
    if option in {"En Contra", "Negativo"}:
        return "0"
    return "."


def main() -> None:
    eligibility = read_csv(ELIGIBILITY)
    votes = read_csv(VOTES)

    eligible_meta = {
        row["vote_id"]: row
        for row in eligibility
        if safe_int(row.get("minority_count", "")) > 0
        and safe_float(row.get("minority_share_binary", "")) >= LOP
    }
    if len(eligible_meta) != 276:
        raise RuntimeError(f"Se esperaban 276 roll calls con lop=0.025; hay {len(eligible_meta)}")

    members = sorted({row["diputado_id"] for row in votes}, key=lambda x: int(x) if x.isdigit() else x)
    if len(members) != 155:
        raise RuntimeError(f"Se esperaban 155 diputados; hay {len(members)}")
    member_pos = {member_id: idx for idx, member_id in enumerate(members)}

    vectors: dict[str, list[str]] = {vote_id: ["."] * len(members) for vote_id in eligible_meta}
    seen_pairs = set()
    for row in votes:
        vote_id = row.get("vote_id", "")
        if vote_id not in eligible_meta:
            continue
        member_id = row.get("diputado_id", "")
        key = (vote_id, member_id)
        if key in seen_pairs:
            raise RuntimeError(f"Par duplicado vote_id × diputado_id: {key}")
        seen_pairs.add(key)
        vectors[vote_id][member_pos[member_id]] = model_code(row.get("opcion", ""))

    expected_pairs = len(eligible_meta) * len(members)
    if len(seen_pairs) != expected_pairs:
        raise RuntimeError(f"Matriz elegible incompleta: {len(seen_pairs)}/{expected_pairs}")

    by_bill: dict[str, list[str]] = defaultdict(list)
    for vote_id, meta in eligible_meta.items():
        bill = (meta.get("boletin") or "").strip()
        if not bill:
            raise RuntimeError(f"Roll call {vote_id} sin boletín")
        by_bill[bill].append(vote_id)

    output = []
    total_unique_bill_patterns = 0
    total_duplicate_rollcalls = 0
    cross_bill_pattern_bills: dict[str, set[str]] = defaultdict(set)
    all_pattern_counts = Counter()

    for bill, vote_ids in by_bill.items():
        pattern_counts = Counter()
        for vote_id in vote_ids:
            pattern = "".join(vectors[vote_id])
            digest = hashlib.sha256(pattern.encode("ascii")).hexdigest()
            pattern_counts[digest] += 1
            all_pattern_counts[digest] += 1
            cross_bill_pattern_bills[digest].add(bill)

        unique = len(pattern_counts)
        total = len(vote_ids)
        duplicates = total - unique
        largest = max(pattern_counts.values()) if pattern_counts else 0
        total_unique_bill_patterns += unique
        total_duplicate_rollcalls += duplicates
        first = eligible_meta[vote_ids[0]]
        output.append({
            "boletin": bill,
            "topic_primary": first.get("topic_primary", ""),
            "origin_initiative": first.get("origin_initiative", ""),
            "eligible_rollcalls": total,
            "unique_binary_patterns": unique,
            "duplicate_rollcalls": duplicates,
            "duplicate_share": f"{duplicates / total:.6f}" if total else "",
            "largest_pattern_multiplicity": largest,
            "largest_pattern_share": f"{largest / total:.6f}" if total else "",
        })

    output.sort(key=lambda row: (-safe_int(row["eligible_rollcalls"]), row["boletin"]))
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output)

    global_unique_patterns = len(all_pattern_counts)
    patterns_shared_across_bills = sum(len(bills) > 1 for bills in cross_bill_pattern_bills.values())
    top = output[:10]
    diagnostics = {
        "generated_for": str(date.today()),
        "lop": LOP,
        "eligible_rollcalls": len(eligible_meta),
        "eligible_bills": len(by_bill),
        "unique_patterns_within_bill_total": total_unique_bill_patterns,
        "exact_duplicates_within_bill": total_duplicate_rollcalls,
        "duplicate_share_within_bill": round(total_duplicate_rollcalls / len(eligible_meta), 6),
        "globally_unique_binary_patterns": global_unique_patterns,
        "globally_repeated_rollcalls": len(eligible_meta) - global_unique_patterns,
        "patterns_occurring_in_multiple_bills": patterns_shared_across_bills,
        "top_bills": [
            {
                "boletin": row["boletin"],
                "eligible_rollcalls": safe_int(row["eligible_rollcalls"]),
                "unique_binary_patterns": safe_int(row["unique_binary_patterns"]),
                "duplicate_rollcalls": safe_int(row["duplicate_rollcalls"]),
                "largest_pattern_multiplicity": safe_int(row["largest_pattern_multiplicity"]),
            }
            for row in top
        ],
        "method_note": (
            "Dos roll calls se consideran redundantes dentro de un boletín solo cuando la matriz usada por el modelo "
            "es exactamente idéntica para los 155 diputados después de codificar Afirmativo=1, En Contra=0 y las "
            "demás opciones como missing. Este diagnóstico no elimina observaciones."
        ),
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
