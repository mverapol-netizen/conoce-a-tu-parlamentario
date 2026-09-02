from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "data" / "legislative" / "2026" / "topics"
TEXTS = TOPICS / "project_texts.jsonl"
OUTPUT = TOPICS / "topic_gold_sample.csv"
MANIFEST = TOPICS / "topic_gold_sample_manifest.json"
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


def suffix(boletin: str) -> str:
    return boletin.rsplit("-", 1)[-1] if "-" in boletin else ""


def score(row: dict) -> str:
    # Pseudoaleatoriedad reproducible: no depende del orden de descarga.
    return hashlib.sha256(row.get("boletin", "").encode("utf-8")).hexdigest()


def stratified_round_robin(rows: list[dict], n: int) -> list[dict]:
    """Distribuye la muestra entre sufijos de boletín sin usar el sufijo como etiqueta.

    El sufijo solo sirve para que la muestra de validación cubra distintos tipos de
    proyectos. Dentro de cada estrato la selección es determinística por hash.
    """
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[suffix(row.get("boletin", "")) or "NA"].append(row)
    for key in groups:
        groups[key].sort(key=score)

    # Primero recorremos todos los estratos disponibles. Después volvemos a
    # empezar, tomando el segundo, tercer, etc. caso de cada estrato.
    keys = sorted(groups, key=lambda key: (-len(groups[key]), key))
    selected: list[dict] = []
    depth = 0
    seen = set()
    while len(selected) < min(n, len(rows)):
        added = 0
        for key in keys:
            bucket = groups[key]
            if depth >= len(bucket):
                continue
            row = bucket[depth]
            bill = row.get("boletin", "")
            if bill and bill not in seen:
                selected.append(row)
                seen.add(bill)
                added += 1
                if len(selected) >= min(n, len(rows)):
                    break
        if not added:
            break
        depth += 1
    return selected


def main() -> None:
    if not TEXTS.exists():
        raise RuntimeError("El corpus textual aún no existe")
    corpus = load_texts()
    usable = [r for r in corpus if r.get("text_quality") in {"rica", "utilizable"}]
    parliamentary = [r for r in usable if r.get("origen_iniciativa") == "parlamentario"]
    executive = [r for r in usable if r.get("origen_iniciativa") == "ejecutivo"]

    selected_parliamentary = stratified_round_robin(parliamentary, N_PARLIAMENTARY)
    selected_executive = stratified_round_robin(executive, N_EXECUTIVE)
    selected = selected_parliamentary + selected_executive
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

    manifest = {
        "corpus_rows": len(corpus),
        "usable_rows": len(usable),
        "sample_rows": len(selected),
        "parliamentary_sample": len(selected_parliamentary),
        "executive_sample": len(selected_executive),
        "selection_method": "deterministic_round_robin_by_origin_and_boletin_suffix",
        "suffix_is_sampling_only_not_label_signal": True,
        "sample_suffix_distribution": dict(sorted(Counter(suffix(r.get("boletin", "")) or "NA" for r in selected).items())),
        "parliamentary_suffix_distribution": dict(sorted(Counter(suffix(r.get("boletin", "")) or "NA" for r in selected_parliamentary).items())),
        "executive_suffix_distribution": dict(sorted(Counter(suffix(r.get("boletin", "")) or "NA" for r in selected_executive).items())),
        "output": str(OUTPUT.relative_to(ROOT)),
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

    if len(selected_parliamentary) < min(N_PARLIAMENTARY, len(parliamentary)):
        raise RuntimeError("No se pudo construir la muestra parlamentaria objetivo")
    if len(selected_executive) < min(N_EXECUTIVE, len(executive)):
        raise RuntimeError("No se pudo construir la muestra ejecutiva objetivo")


if __name__ == "__main__":
    main()
