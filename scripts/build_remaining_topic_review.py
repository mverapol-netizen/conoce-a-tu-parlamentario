from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "data" / "legislative" / "2026" / "topics"
SRC = TOPICS / "topic_review_queue_remaining.csv"
OUT = TOPICS / "topic_review_remaining_compact.csv"

# Cola compacta para revisión semántica humana/modelo de los casos pendientes.
def main() -> None:
    with SRC.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    fields = [
        "boletin", "titulo", "origen_iniciativa", "comision_origen_proxy",
        "comisiones_tramitacion", "topic_primary", "topic_secondary", "confidence",
        "review_reason", "evidence", "text_excerpt"
    ]
    compact = []
    for row in rows:
        excerpt = " ".join((row.get("text_excerpt") or "").split())[:900]
        compact.append({
            "boletin": row.get("boletin", ""),
            "titulo": row.get("titulo", ""),
            "origen_iniciativa": row.get("origen_iniciativa", ""),
            "comision_origen_proxy": row.get("comision_origen_proxy", ""),
            "comisiones_tramitacion": row.get("comisiones_tramitacion", ""),
            "topic_primary": row.get("topic_primary", ""),
            "topic_secondary": row.get("topic_secondary", ""),
            "confidence": row.get("confidence", ""),
            "review_reason": row.get("review_reason", ""),
            "evidence": row.get("evidence", ""),
            "text_excerpt": excerpt,
        })

    with OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(compact)

    print(f"remaining={len(compact)}")


if __name__ == "__main__":
    main()
