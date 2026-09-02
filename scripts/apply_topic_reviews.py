from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "data" / "legislative" / "2026" / "topics"
AUTO = TOPICS / "project_topic_classification.csv"
AUTO_LONG = TOPICS / "project_topics.csv"
AUTO_QUEUE = TOPICS / "topic_review_queue.csv"
OVERRIDES = TOPICS / "topic_model_overrides.csv"


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_pipe(value: str) -> list[str]:
    return [x.strip() for x in str(value or "").split("|") if x.strip()]


def main() -> None:
    automatic = read_csv(AUTO)
    queue = read_csv(AUTO_QUEUE)
    overrides = [x for x in read_csv(OVERRIDES) if (x.get("status") or "").lower() == "aprobado"]
    by_override = {x["boletin"]: x for x in overrides if x.get("boletin")}

    if not automatic:
        raise RuntimeError("No existe la clasificación automática")

    final_rows = []
    long_rows = []
    applied = 0

    for row in automatic:
        out = dict(row)
        override = by_override.get(row.get("boletin", ""))
        if override:
            applied += 1
            out["auto_topic_primary"] = row.get("topic_primary", "")
            out["auto_topic_secondary"] = row.get("topic_secondary", "")
            out["topic_primary"] = override.get("topic_primary", "")
            out["topic_secondary"] = override.get("topic_secondary", "")
            out["method"] = override.get("method", "revision_semantica")
            out["confidence"] = override.get("confidence", "")
            out["needs_review"] = "0"
            out["review_reason"] = ""
            out["reviewer"] = override.get("reviewer", "")
            out["review_rationale"] = override.get("rationale", "")
            out["reviewed_at"] = override.get("reviewed_at", "")
        else:
            out["auto_topic_primary"] = row.get("topic_primary", "")
            out["auto_topic_secondary"] = row.get("topic_secondary", "")
            out["reviewer"] = ""
            out["review_rationale"] = ""
            out["reviewed_at"] = ""
        final_rows.append(out)

        long_rows.append({
            "boletin": out.get("boletin", ""),
            "topic": out.get("topic_primary", ""),
            "role": "principal",
            "method": out.get("method", ""),
            "confidence": out.get("confidence", ""),
            "needs_review": out.get("needs_review", ""),
            "reviewer": out.get("reviewer", ""),
            "taxonomy_version": out.get("taxonomy_version", ""),
        })
        for secondary in split_pipe(out.get("topic_secondary", "")):
            if secondary == out.get("topic_primary", ""):
                continue
            long_rows.append({
                "boletin": out.get("boletin", ""),
                "topic": secondary,
                "role": "secundario",
                "method": out.get("method", ""),
                "confidence": out.get("confidence", ""),
                "needs_review": out.get("needs_review", ""),
                "reviewer": out.get("reviewer", ""),
                "taxonomy_version": out.get("taxonomy_version", ""),
            })

    remaining_queue = [x for x in queue if x.get("boletin", "") not in by_override]

    fields = [
        "boletin", "titulo", "origen_iniciativa", "comision_origen_proxy", "comisiones_tramitacion",
        "topic_primary", "topic_secondary", "method", "confidence", "needs_review", "review_reason",
        "evidence", "taxonomy_version", "auto_topic_primary", "auto_topic_secondary", "reviewer",
        "review_rationale", "reviewed_at",
    ]
    with (TOPICS / "project_topic_final.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(final_rows)

    long_fields = [
        "boletin", "topic", "role", "method", "confidence", "needs_review", "reviewer", "taxonomy_version"
    ]
    with (TOPICS / "project_topics_final.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=long_fields)
        writer.writeheader()
        writer.writerows(long_rows)

    queue_fields = list(queue[0].keys()) if queue else []
    with (TOPICS / "topic_review_queue_remaining.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        if queue_fields:
            writer = csv.DictWriter(handle, fieldnames=queue_fields)
            writer.writeheader()
            writer.writerows(remaining_queue)

    by_final_topic: dict[str, int] = defaultdict(int)
    for row in final_rows:
        by_final_topic[row.get("topic_primary", "")] += 1

    diagnostics = {
        "projects": len(final_rows),
        "automatic_review_queue_before": len(queue),
        "approved_model_overrides_available": len(overrides),
        "model_overrides_applied": applied,
        "final_accepted": sum(x.get("needs_review") == "0" for x in final_rows),
        "remaining_review_queue": len(remaining_queue),
        "remaining_review_rate": round(len(remaining_queue) / max(len(final_rows), 1), 4),
        "primary_topics_after_reviews": dict(sorted(by_final_topic.items(), key=lambda kv: (-kv[1], kv[0]))),
    }
    (TOPICS / "topic_final_diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
