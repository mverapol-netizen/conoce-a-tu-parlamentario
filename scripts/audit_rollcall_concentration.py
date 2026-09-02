from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
INPUT = OUT / "rollcall_model_eligibility.csv"
PROJECTS = OUT / "projects.csv"
INHERITED = OUT / "topics" / "rollcall_inherited_topic_final.csv"
OUTPUT = OUT / "rollcall_concentration_by_bill.csv"
DIAGNOSTICS = OUT / "rollcall_concentration_diagnostics.json"

THRESHOLDS = (0.025, 0.05, 0.10)

FIELDS = [
    "boletin", "titulo", "origin_initiative", "topic_primary", "topic_source_layer",
    "all_rollcalls", "nonunanimous_rollcalls",
    "eligible_lop_0025", "eligible_lop_0050", "eligible_lop_0100",
    "share_lop_0025", "share_lop_0050", "share_lop_0100",
    "general_rollcalls", "particular_rollcalls", "other_stage_rollcalls",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def suffix(threshold: float) -> str:
    return f"{int(round(threshold * 1000)):04d}"


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


def project_titles() -> dict[str, str]:
    result = {}
    for path in (PROJECTS, INHERITED):
        for row in read_csv(path):
            bill = (row.get("boletin") or "").strip()
            title = (row.get("titulo") or "").strip()
            if bill and title:
                result[bill] = title
    return result


def concentration_stats(counts: list[int]) -> dict:
    total = sum(counts)
    if not counts or not total:
        return {
            "bills": 0,
            "rollcalls": 0,
            "max_rollcalls_one_bill": 0,
            "median_rollcalls_per_bill": 0,
            "top1_share": 0,
            "top5_share": 0,
            "top10_share": 0,
            "hhi_bill_share": 0,
        }
    ordered = sorted(counts, reverse=True)
    shares = [count / total for count in ordered]
    return {
        "bills": len(counts),
        "rollcalls": total,
        "max_rollcalls_one_bill": ordered[0],
        "median_rollcalls_per_bill": median(ordered),
        "top1_share": round(sum(shares[:1]), 6),
        "top5_share": round(sum(shares[:5]), 6),
        "top10_share": round(sum(shares[:10]), 6),
        "hhi_bill_share": round(sum(share * share for share in shares), 6),
    }


def stage_bucket(value: str) -> str:
    text = (value or "").strip().lower()
    if text == "general":
        return "general"
    if text == "particular":
        return "particular"
    return "other"


def main() -> None:
    rows = read_csv(INPUT)
    if not rows:
        raise RuntimeError("rollcall_model_eligibility.csv está vacío")

    titles = project_titles()
    by_bill: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        bill = (row.get("boletin") or "").strip()
        if not bill:
            raise RuntimeError(f"Roll call {row.get('vote_id')} sin boletín")
        by_bill[bill].append(row)

    eligible_total = {
        threshold: sum(
            safe_int(row.get("minority_count", "")) > 0
            and safe_float(row.get("minority_share_binary", "")) >= threshold
            for row in rows
        )
        for threshold in THRESHOLDS
    }

    output = []
    for bill, bill_rows in by_bill.items():
        first = bill_rows[0]
        stages = Counter(stage_bucket(row.get("vote_stage", "")) for row in bill_rows)
        record = {
            "boletin": bill,
            "titulo": titles.get(bill, ""),
            "origin_initiative": first.get("origin_initiative", ""),
            "topic_primary": first.get("topic_primary", ""),
            "topic_source_layer": first.get("topic_source_layer", ""),
            "all_rollcalls": len(bill_rows),
            "nonunanimous_rollcalls": sum(safe_int(row.get("minority_count", "")) > 0 for row in bill_rows),
            "general_rollcalls": stages["general"],
            "particular_rollcalls": stages["particular"],
            "other_stage_rollcalls": stages["other"],
        }
        for threshold in THRESHOLDS:
            count = sum(
                safe_int(row.get("minority_count", "")) > 0
                and safe_float(row.get("minority_share_binary", "")) >= threshold
                for row in bill_rows
            )
            tag = suffix(threshold)
            record[f"eligible_lop_{tag}"] = count
            record[f"share_lop_{tag}"] = f"{count / eligible_total[threshold]:.6f}" if eligible_total[threshold] else ""
        output.append(record)

    output.sort(key=lambda row: (-safe_int(row["eligible_lop_0025"]), -safe_int(row["all_rollcalls"]), row["boletin"]))
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output)

    stage_counts_all = Counter(stage_bucket(row.get("vote_stage", "")) for row in rows)
    diagnostics = {
        "generated_for": str(date.today()),
        "all": concentration_stats([len(v) for v in by_bill.values()]),
        "nonunanimous": concentration_stats([
            sum(safe_int(row.get("minority_count", "")) > 0 for row in bill_rows)
            for bill_rows in by_bill.values()
            if any(safe_int(row.get("minority_count", "")) > 0 for row in bill_rows)
        ]),
        "lop": {},
        "stage_counts_all": dict(stage_counts_all),
        "top_bills_lop_0025": [],
        "method_note": (
            "Diagnóstico de dependencia potencial por repetición de roll calls dentro de un mismo boletín. "
            "No descarta ni pondera votaciones. Sirve para decidir pruebas de robustez posteriores a la estimación base."
        ),
    }

    for threshold in THRESHOLDS:
        tag = suffix(threshold)
        counts = [
            safe_int(row[f"eligible_lop_{tag}"])
            for row in output
            if safe_int(row[f"eligible_lop_{tag}"]) > 0
        ]
        diagnostics["lop"][f"{threshold:.3f}"] = concentration_stats(counts)

    diagnostics["top_bills_lop_0025"] = [
        {
            "boletin": row["boletin"],
            "titulo": row["titulo"],
            "topic_primary": row["topic_primary"],
            "origin_initiative": row["origin_initiative"],
            "eligible_rollcalls": safe_int(row["eligible_lop_0025"]),
            "share": safe_float(row["share_lop_0025"]),
        }
        for row in output[:10]
        if safe_int(row["eligible_lop_0025"]) > 0
    ]

    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))

    if len(rows) != 364:
        raise RuntimeError(f"Se esperaban 364 roll calls; hay {len(rows)}")
    if len(by_bill) != 89:
        raise RuntimeError(f"Se esperaban 89 boletines con roll calls; hay {len(by_bill)}")


if __name__ == "__main__":
    main()
