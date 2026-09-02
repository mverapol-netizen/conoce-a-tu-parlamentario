from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

from classify_topics_hybrid import classify
from derive_topic_signals import (
    COMMISSION_TOPIC,
    DESTINATION_CODE_TO_COMMISSION,
    TRANSVERSAL,
    bulletin_destination_code,
    canonical_commissions,
    origin_commission_from_event,
)
from legislative_common import parse_ministries, project_detail, project_page
from sync_project_texts import document_priority, fetch_document

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "legislative" / "2026"
TOPICS = DATA / "topics"
MISSING = TOPICS / "rollcall_topic_missing.csv"
CLASSIFICATION = TOPICS / "rollcall_inherited_topic_classification.csv"
REVIEW = TOPICS / "rollcall_inherited_topic_review_queue.csv"
DIAGNOSTICS = TOPICS / "rollcall_inherited_topic_diagnostics.json"
TAXONOMY_VERSION = "institutional-hybrid-v0.3"


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def unique(values: list[str]) -> list[str]:
    out = []
    seen = set()
    for value in values:
        value = (value or "").strip()
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def pipe(values: list[str]) -> str:
    return " | ".join(unique(values))


def infer_origin(tipo: str) -> str:
    value = (tipo or "").lower()
    if "moción" in value or "mocion" in value:
        return "parlamentario"
    if "mensaje" in value:
        return "ejecutivo"
    return "historico"


def build_signal(project: dict, events: list[dict], ministries: list[dict]) -> dict:
    bill = project.get("boletin", "")
    code = bulletin_destination_code(bill)
    suffix_origin = DESTINATION_CODE_TO_COMMISSION.get(code, "")

    explicit_origin = ""
    commission_names: list[str] = []
    for event in sorted(events, key=lambda x: (x.get("fecha", ""), x.get("subetapa", ""))):
        substage = event.get("subetapa", "")
        candidate = origin_commission_from_event(substage)
        if candidate and not explicit_origin:
            explicit_origin = candidate
        commission_names.extend(canonical_commissions(substage))
        if candidate:
            commission_names.append(candidate)

    commission_names = unique(([suffix_origin] if suffix_origin else []) + commission_names)
    origin_proxy = explicit_origin or suffix_origin
    trajectory_topics = unique([COMMISSION_TOPIC.get(x, "") for x in commission_names])
    substantive = [x for x in commission_names if x not in TRANSVERSAL]

    return {
        "boletin": bill,
        "titulo": project.get("titulo", ""),
        "origen_iniciativa": infer_origin(project.get("tipo_iniciativa", "")),
        "camara_origen": project.get("camara_origen", ""),
        "codigo_destinacion": code,
        "comision_destino_sufijo": suffix_origin,
        "comision_origen_evento": explicit_origin,
        "comision_origen_proxy": origin_proxy,
        "tema_proxy_origen": COMMISSION_TOPIC.get(origin_proxy, ""),
        "comisiones_tramitacion": pipe(commission_names),
        "temas_proxy_trayectoria": pipe(trajectory_topics),
        "comisiones_sustantivas": pipe(substantive),
        "ministerios": pipe([x.get("ministerio", "") for x in ministries]),
    }


def document_text(events: list[dict]) -> tuple[str, str, str]:
    candidates = sorted(events, key=document_priority)
    candidate = next((x for x in candidates if document_priority(x) < 50), None)
    if not candidate:
        return "", "", "sin_documento_candidato"
    url = candidate.get("documento_url", "")
    try:
        extracted = fetch_document(url)
        return extracted.get("cleaned_text", ""), url, extracted.get("text_quality", "")
    except Exception as exc:  # noqa: BLE001
        return "", url, f"error:{exc}"


def main() -> None:
    missing = read_csv(MISSING)
    if not missing:
        raise RuntimeError("No hay boletines heredados pendientes en rollcall_topic_missing.csv")

    rows = []
    review_rows = []
    errors = []
    text_fetches = 0
    text_success = 0

    for idx, item in enumerate(missing, start=1):
        bill = item.get("boletin", "").strip()
        try:
            project, detail = project_detail(bill, "historico")
            project["origen_iniciativa"] = infer_origin(project.get("tipo_iniciativa", ""))
            page_meta, events = project_page(project["project_id"], bill)
            project.update(page_meta)
            ministries = parse_ministries(detail, bill)
            signal = build_signal(project, events, ministries)

            initial = classify(signal, "")
            body = ""
            doc_url = ""
            text_quality = "no_requerido"
            result = initial
            if initial["needs_review"]:
                text_fetches += 1
                body, doc_url, text_quality = document_text(events)
                if body:
                    text_success += 1
                result = classify(signal, body)

            secondary = unique([x for x in result["secondary"] if x and x != result["primary"]])
            row = {
                "boletin": bill,
                "rollcalls": item.get("rollcalls", ""),
                "titulo": project.get("titulo", ""),
                "fecha_ingreso": project.get("fecha_ingreso", ""),
                "origen_iniciativa": project.get("origen_iniciativa", ""),
                "tipo_iniciativa": project.get("tipo_iniciativa", ""),
                "camara_origen": project.get("camara_origen", ""),
                "codigo_destinacion": signal.get("codigo_destinacion", ""),
                "comision_origen_proxy": signal.get("comision_origen_proxy", ""),
                "comisiones_tramitacion": signal.get("comisiones_tramitacion", ""),
                "topic_primary": result["primary"],
                "topic_secondary": pipe(secondary),
                "method": result["method"],
                "confidence": result["confidence"],
                "needs_review": "1" if result["needs_review"] else "0",
                "review_reason": pipe(result["review_reason"]),
                "evidence": " || ".join(result["evidence"]),
                "document_url": doc_url,
                "text_quality": text_quality,
                "source_url": project.get("source_url", ""),
                "taxonomy_version": TAXONOMY_VERSION,
            }
            rows.append(row)
            if result["needs_review"]:
                review_rows.append({
                    **row,
                    "text_excerpt": re.sub(r"\s+", " ", body)[:1800],
                    "top_scores": json.dumps(result["scores"], ensure_ascii=False),
                })
        except Exception as exc:  # noqa: BLE001
            errors.append({"boletin": bill, "error": str(exc)})

        if idx % 10 == 0:
            print(f"Heredados {idx}/{len(missing)} · revisión={len(review_rows)} · errores={len(errors)}")

    fields = [
        "boletin", "rollcalls", "titulo", "fecha_ingreso", "origen_iniciativa", "tipo_iniciativa",
        "camara_origen", "codigo_destinacion", "comision_origen_proxy", "comisiones_tramitacion",
        "topic_primary", "topic_secondary", "method", "confidence", "needs_review", "review_reason",
        "evidence", "document_url", "text_quality", "source_url", "taxonomy_version",
    ]
    with CLASSIFICATION.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    review_fields = fields + ["text_excerpt", "top_scores"]
    review_rows.sort(key=lambda x: (float(x["confidence"]), -int(x.get("rollcalls") or 0), x["boletin"]))
    with REVIEW.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=review_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(review_rows)

    diagnostics = {
        "missing_rollcall_bills_input": len(missing),
        "classified": len(rows),
        "auto_accepted": sum(x["needs_review"] == "0" for x in rows),
        "review_queue": len(review_rows),
        "errors": errors,
        "text_fetches": text_fetches,
        "text_success": text_success,
        "methods": dict(Counter(x["method"] for x in rows)),
        "primary_topics": dict(Counter(x["topic_primary"] for x in rows).most_common()),
        "review_rollcalls": sum(int(x.get("rollcalls") or 0) for x in review_rows),
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))

    if errors:
        raise RuntimeError(f"Falló detalle oficial en {len(errors)} boletines heredados")
    if len(rows) != len(missing):
        raise RuntimeError(f"Cobertura heredada incompleta: {len(rows)}/{len(missing)}")


if __name__ == "__main__":
    main()
