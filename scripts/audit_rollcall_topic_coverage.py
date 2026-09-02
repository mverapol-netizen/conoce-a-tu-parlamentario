from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
ROLLCALLS = OUT / "rollcalls.csv"
TOPICS = OUT / "topics" / "project_topics_final.csv"
MISSING = OUT / "topics" / "rollcall_topic_missing.csv"
DIAGNOSTICS = OUT / "topics" / "rollcall_topic_coverage_diagnostics.json"


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    rollcalls = read_csv(ROLLCALLS)
    topics = read_csv(TOPICS)

    principal_by_bill: dict[str, str] = {}
    duplicate_principal: dict[str, list[str]] = defaultdict(list)
    for row in topics:
        if row.get("role") != "principal":
            continue
        bill = (row.get("boletin") or "").strip()
        topic = (row.get("topic") or "").strip()
        if not bill:
            continue
        if bill in principal_by_bill and principal_by_bill[bill] != topic:
            duplicate_principal[bill].extend([principal_by_bill[bill], topic])
        else:
            principal_by_bill[bill] = topic

    bill_rollcalls = Counter()
    blank_bill_rollcalls = 0
    covered_rollcalls = 0
    topic_rollcalls = Counter()
    for row in rollcalls:
        bill = (row.get("boletin") or "").strip()
        if not bill:
            blank_bill_rollcalls += 1
            continue
        bill_rollcalls[bill] += 1
        topic = principal_by_bill.get(bill)
        if topic:
            covered_rollcalls += 1
            topic_rollcalls[topic] += 1

    missing_rows = []
    for bill, n in sorted(bill_rollcalls.items(), key=lambda kv: (-kv[1], kv[0])):
        if bill in principal_by_bill:
            continue
        sample = next((r for r in rollcalls if (r.get("boletin") or "").strip() == bill), {})
        missing_rows.append({
            "boletin": bill,
            "rollcalls": n,
            "first_vote_date": min(
                (r.get("fecha", "") for r in rollcalls if (r.get("boletin") or "").strip() == bill),
                default="",
            ),
            "sample_description": sample.get("descripcion", ""),
            "sample_verification_url": sample.get("verification_url", ""),
        })

    with MISSING.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["boletin", "rollcalls", "first_vote_date", "sample_description", "sample_verification_url"],
        )
        writer.writeheader()
        writer.writerows(missing_rows)

    unique_rollcall_bills = len(bill_rollcalls)
    covered_bills = sum(bill in principal_by_bill for bill in bill_rollcalls)
    diagnostics = {
        "rollcalls": len(rollcalls),
        "rollcalls_with_boletin": len(rollcalls) - blank_bill_rollcalls,
        "rollcalls_without_boletin": blank_bill_rollcalls,
        "unique_rollcall_bills": unique_rollcall_bills,
        "unique_rollcall_bills_with_topic": covered_bills,
        "unique_rollcall_bills_missing_topic": len(missing_rows),
        "rollcalls_with_topic": covered_rollcalls,
        "rollcalls_missing_topic": (len(rollcalls) - blank_bill_rollcalls) - covered_rollcalls,
        "rollcall_topic_coverage_pct": round(100 * covered_rollcalls / max(1, len(rollcalls) - blank_bill_rollcalls), 4),
        "bill_topic_coverage_pct": round(100 * covered_bills / max(1, unique_rollcall_bills), 4),
        "duplicate_principal_topics": {k: sorted(set(v)) for k, v in duplicate_principal.items()},
        "rollcalls_by_covered_topic": dict(topic_rollcalls.most_common()),
        "largest_missing_bills": missing_rows[:25],
        "method_note": "Cobertura medida contra el tema principal final. No se calculan estadísticas diputado×tema hasta cubrir los boletines heredados votados durante la legislatura.",
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))

    if duplicate_principal:
        raise RuntimeError(f"Hay boletines con más de un tema principal: {dict(duplicate_principal)}")


if __name__ == "__main__":
    main()
