from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "legislative" / "2026"
TOPICS = DATA / "topics"
AUTO = TOPICS / "rollcall_inherited_topic_classification.csv"
REVIEWS = TOPICS / "rollcall_inherited_topic_reviews.csv"
PROJECT_FINAL = TOPICS / "project_topic_final.csv"
ROLLCALLS = DATA / "rollcalls.csv"
INHERITED_FINAL = TOPICS / "rollcall_inherited_topic_final.csv"
ROLLCALL_MAP = TOPICS / "rollcall_topic_map.csv"
DIAGNOSTICS = TOPICS / "rollcall_topic_map_diagnostics.json"


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    auto = read_csv(AUTO)
    reviews = {x["boletin"]: x for x in read_csv(REVIEWS) if x.get("boletin")}
    project_final = read_csv(PROJECT_FINAL)
    rollcalls = read_csv(ROLLCALLS)

    inherited_final = []
    unresolved = []
    for row in auto:
        out = dict(row)
        review = reviews.get(row["boletin"])
        if row.get("needs_review") == "1":
            if not review:
                unresolved.append(row["boletin"])
                continue
            out["auto_topic_primary"] = row.get("topic_primary", "")
            out["auto_topic_secondary"] = row.get("topic_secondary", "")
            out["topic_primary"] = review.get("topic_primary", "")
            out["topic_secondary"] = review.get("topic_secondary", "")
            out["confidence"] = review.get("confidence", "") or "0.95"
            out["method"] = "revision_semantica"
            out["needs_review"] = "0"
            out["reviewer"] = review.get("reviewer", "")
            out["review_rationale"] = review.get("review_rationale", "")
            out["reviewed_at"] = review.get("reviewed_at", "")
        else:
            out["auto_topic_primary"] = row.get("topic_primary", "")
            out["auto_topic_secondary"] = row.get("topic_secondary", "")
            out["reviewer"] = ""
            out["review_rationale"] = ""
            out["reviewed_at"] = ""
        inherited_final.append(out)

    if unresolved:
        raise RuntimeError(f"Quedan {len(unresolved)} boletines heredados sin revisión: {unresolved}")

    final_fields = [
        "boletin", "rollcalls", "titulo", "fecha_ingreso", "origen_iniciativa", "tipo_iniciativa",
        "camara_origen", "codigo_destinacion", "comision_origen_proxy", "comisiones_tramitacion",
        "topic_primary", "topic_secondary", "method", "confidence", "needs_review", "review_reason",
        "evidence", "document_url", "text_quality", "source_url", "taxonomy_version",
        "auto_topic_primary", "auto_topic_secondary", "reviewer", "review_rationale", "reviewed_at",
    ]
    inherited_final.sort(key=lambda x: x["boletin"])
    write_csv(INHERITED_FINAL, inherited_final, final_fields)

    project_by_bill = {x["boletin"]: x for x in project_final if x.get("boletin")}
    inherited_by_bill = {x["boletin"]: x for x in inherited_final if x.get("boletin")}

    map_rows = []
    missing = []
    for rc in rollcalls:
        bill = rc.get("boletin", "")
        topic_row = project_by_bill.get(bill) or inherited_by_bill.get(bill)
        if not topic_row:
            missing.append({"vote_id": rc.get("vote_id", ""), "boletin": bill})
            continue
        source_layer = "period_project" if bill in project_by_bill else "inherited_rollcall_project"
        map_rows.append({
            "vote_id": rc.get("vote_id", ""),
            "boletin": bill,
            "fecha": rc.get("fecha", ""),
            "topic_primary": topic_row.get("topic_primary", ""),
            "topic_secondary": topic_row.get("topic_secondary", ""),
            "topic_method": topic_row.get("method", ""),
            "topic_confidence": topic_row.get("confidence", ""),
            "topic_source_layer": source_layer,
            "taxonomy_version": topic_row.get("taxonomy_version", ""),
            "tipo_votacion_proyecto": rc.get("tipo_votacion_proyecto", ""),
            "resultado": rc.get("resultado", ""),
        })

    map_fields = [
        "vote_id", "boletin", "fecha", "topic_primary", "topic_secondary", "topic_method",
        "topic_confidence", "topic_source_layer", "taxonomy_version", "tipo_votacion_proyecto", "resultado",
    ]
    write_csv(ROLLCALL_MAP, map_rows, map_fields)

    diagnostics = {
        "rollcalls": len(rollcalls),
        "rollcall_topic_map_rows": len(map_rows),
        "missing_rollcalls": len(missing),
        "unique_rollcall_bills": len({x.get("boletin", "") for x in rollcalls}),
        "period_project_bills_used": len({x["boletin"] for x in map_rows if x["topic_source_layer"] == "period_project"}),
        "inherited_bills_used": len({x["boletin"] for x in map_rows if x["topic_source_layer"] == "inherited_rollcall_project"}),
        "topics": dict(Counter(x["topic_primary"] for x in map_rows).most_common()),
        "topic_source_layers": dict(Counter(x["topic_source_layer"] for x in map_rows)),
        "missing_examples": missing[:20],
        "method_note": "Cada roll call hereda el tema principal del proyecto/boletín. Se conservan por separado proyectos ingresados en el período y proyectos heredados votados durante el período.",
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))

    if missing or len(map_rows) != len(rollcalls):
        raise RuntimeError(f"Mapa temático incompleto: {len(map_rows)}/{len(rollcalls)}")


if __name__ == "__main__":
    main()
