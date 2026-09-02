from __future__ import annotations

import json
from datetime import date

from legislative_common import OUT, parse_authors, project_detail, read_csv, upsert, write_csv

FIELDS = ["boletin", "author_order", "author_id", "author_name", "author_chamber"]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # El universo de autorías debe ser exactamente el mismo snapshot que acaba
    # de producir sync_bills.py. No volvemos a consultar la lista anual aquí,
    # porque una iniciativa nueva publicada entre ambas etapas produciría dos
    # poblaciones temporalmente distintas dentro de una misma sincronización.
    projects = read_csv("projects.csv")
    motions = [x for x in projects if x.get("origen_iniciativa") == "parlamentario" and x.get("boletin")]
    motion_bills = {x["boletin"] for x in motions}

    # Podamos relaciones antiguas que ya no pertenezcan al snapshot vigente.
    existing_all = read_csv("bill_authors.csv")
    existing = [x for x in existing_all if x.get("boletin") in motion_bills]
    pruned_relations = len(existing_all) - len(existing)

    covered = {x["boletin"] for x in existing}
    pending = [x for x in motions if x["boletin"] not in covered]

    incoming = []
    errors = []
    empty = []
    for idx, seed in enumerate(pending, start=1):
        try:
            _, detail = project_detail(seed["boletin"], "parlamentario")
            rows = parse_authors(detail, seed["boletin"])
            if rows:
                incoming.extend(rows)
            else:
                empty.append(seed["boletin"])
        except Exception as exc:  # noqa: BLE001
            errors.append({"boletin": seed["boletin"], "error": str(exc)})
        if idx % 50 == 0:
            print(f"Autorías {idx}/{len(pending)} · errores={len(errors)}")

    rows = upsert(
        existing,
        incoming,
        ("boletin", "author_chamber", "author_id", "author_order"),
        ("boletin", "author_order", "author_id"),
    )
    write_csv("bill_authors.csv", rows, FIELDS)

    covered_after = {x["boletin"] for x in rows}
    diagnostics = {
        "generated_for": str(date.today()),
        "parliamentary_initiatives": len(motions),
        "new_bills_checked": len(pending),
        "author_relations": len(rows),
        "bills_with_authors": len(covered_after),
        "pruned_stale_author_relations": pruned_relations,
        "empty_author_lists": empty,
        "errors": errors,
    }
    (OUT / "authorship_diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    unresolved = len(motion_bills - covered_after)
    if unresolved > max(5, int(len(motions) * 0.03)):
        raise RuntimeError(f"Demasiadas mociones sin autoría resuelta: {unresolved}/{len(motions)}")
    print(json.dumps({k: v for k, v in diagnostics.items() if k not in {"errors", "empty_author_lists"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
