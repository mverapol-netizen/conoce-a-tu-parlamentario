from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "data" / "legislative" / "2026" / "topics"
SOURCE = TOPICS / "topic_review_queue.csv"
OUT = TOPICS / "topic_review_pilot_20.csv"


def read_rows() -> list[dict]:
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    rows = read_rows()
    if not rows:
        raise RuntimeError("La cola de revisión está vacía")

    chosen = rows[:10]
    remaining = rows[10:]
    if remaining:
        n = min(10, len(remaining))
        if n == 1:
            idxs = [0]
        else:
            idxs = [round(i * (len(remaining) - 1) / (n - 1)) for i in range(n)]
        chosen.extend(remaining[i] for i in idxs)

    seen = set()
    unique = []
    for row in chosen:
        bill = row.get("boletin", "")
        if bill and bill not in seen:
            seen.add(bill)
            row = dict(row)
            row["text_excerpt"] = (row.get("text_excerpt") or "")[:900]
            unique.append(row)

    fields = [
        "boletin", "titulo", "origen_iniciativa", "comision_origen_proxy", "comisiones_tramitacion",
        "topic_primary", "topic_secondary", "confidence", "review_reason", "evidence", "top_scores",
        "text_excerpt",
    ]
    with OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(unique)

    print(f"Muestra de revisión: {len(unique)} casos de {len(rows)} pendientes")


if __name__ == "__main__":
    main()
