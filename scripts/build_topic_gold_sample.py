from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "data" / "legislative" / "2026" / "topics"
TEXTS = TOPICS / "project_texts.jsonl"
OUTPUT = TOPICS / "topic_gold_sample.csv"
N_PARLIAMENTARY = 50
N_EXECUTIVE = 30
EXCERPT_CHARS = 2600


def load_texts() -> list[dict]:
    rows = []
    with TEXTS.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def deterministic_sample(rows: list[dict], n: int) -> list[dict]:
    # Pseudoaleatoriedad reproducible: no depende del orden de descarga.
    scored = []
    for row in rows:
        digest = hashlib.sha256(row.get("boletin", "").encode("utf-8")).hexdigest()
        scored.append((digest, row))
    scored.sort(key=lambda item: item[0])
    return [row for _, row in scored[: min(n, len(scored))]]


def suffix(boletin: str) -> str:
    return boletin.rsplit("-", 1)[-1] if "-" in boletin else ""


def main() -> None:
    if not TEXTS.exists():
        raise RuntimeError("El corpus textual aún no existe")
    corpus = load_texts()
    usable = [r for r in corpus if r.get("text_quality") in {"rica", "utilizable"}]
    parliamentary = [r for r in usable if r.get("origen_iniciativa") == "parlamentario"]
    executive = [r for r in usable if r.get("origen_iniciativa") == "ejecutivo"]
    selected = deterministic_sample(parliamentary, N_PARLIAMENTARY) + deterministic_sample(executive, N_EXECUTIVE)
    selected.sort(key=lambda r: (r.get("fecha_ingreso", ""), r.get("boletin", "")))

    fields = [
        "boletin", "project_id", "fecha_ingreso", "origen_iniciativa", "boletin_suffix",
        "titulo", "document_type", "text_quality", "cleaned_chars", "text_excerpt",
        "topic_primary", "topic_secondary", "coder", "review_status", "notes",
    ]
    TOPICS.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in selected:
            writer.writerow({
                "boletin": row.get("boletin", ""),
                "project_id": row.get("project_id", ""),
                "fecha_ingreso": row.get("fecha_ingreso", ""),
                "origen_iniciativa": row.get("origen_iniciativa", ""),
                "boletin_suffix": suffix(row.get("boletin", "")),
                "titulo": row.get("titulo", ""),
                "document_type": row.get("document_type", ""),
                "text_quality": row.get("text_quality", ""),
                "cleaned_chars": row.get("cleaned_chars", ""),
                "text_excerpt": (row.get("cleaned_text") or "")[:EXCERPT_CHARS],
                "topic_primary": "",
                "topic_secondary": "",
                "coder": "",
                "review_status": "pending",
                "notes": "",
            })

    print(json.dumps({
        "corpus_rows": len(corpus),
        "usable_rows": len(usable),
        "sample_rows": len(selected),
        "parliamentary_sample": sum(r.get("origen_iniciativa") == "parlamentario" for r in selected),
        "executive_sample": sum(r.get("origen_iniciativa") == "ejecutivo" for r in selected),
        "output": str(OUTPUT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
