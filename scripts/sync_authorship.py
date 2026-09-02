from __future__ import annotations

import json
from datetime import date

from legislative_common import OUT, initiatives, parse_authors, project_detail, read_csv, upsert, write_csv

FIELDS = ["boletin", "author_order", "author_id", "author_name", "author_chamber"]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    motions = [x for x in initiatives() if x["origen_iniciativa"] == "parlamentario"]
    existing = read_csv("bill_authors.csv")
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

    rows = upsert(existing, incoming, ("boletin", "author_chamber", "author_id", "author_order"), ("boletin", "author_order", "author_id"))
    write_csv("bill_authors.csv", rows, FIELDS)

    covered_after = {x["boletin"] for x in rows}
    diagnostics = {
        "generated_for": str(date.today()),
        "parliamentary_initiatives": len(motions),
        "new_bills_checked": len(pending),
        "author_relations": len(rows),
        "bills_with_authors": len(covered_after),
        "empty_author_lists": empty,
        "errors": errors,
    }
    (OUT / "authorship_diagnostics.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unresolved = len(motions) - len(covered_after)
    if unresolved > max(5, int(len(motions) * 0.03)):
        raise RuntimeError(f"Demasiadas mociones sin autoría resuelta: {unresolved}/{len(motions)}")
    print(json.dumps({k: v for k, v in diagnostics.items() if k not in {"errors", "empty_author_lists"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
