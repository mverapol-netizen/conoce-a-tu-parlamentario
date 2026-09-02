from __future__ import annotations

import json
from datetime import date, timedelta

from legislative_common import OUT, parse_authors, project_detail, read_csv, upsert, write_csv

FIELDS = ["boletin", "author_order", "author_id", "author_name", "author_chamber"]
RECENT_RECHECK_DAYS = 35


def is_recent_motion(seed: dict, cutoff: date) -> bool:
    try:
        return date.fromisoformat((seed.get("fecha_ingreso") or "").split("T", 1)[0]) >= cutoff
    except Exception:
        return False


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
    cutoff = date.today() - timedelta(days=RECENT_RECHECK_DAYS)
    recent_bills = {x["boletin"] for x in motions if is_recent_motion(x, cutoff)}

    # Las mociones nunca vistas se consultan una vez; las recientes se vuelven a
    # validar durante una ventana móvil para capturar rectificaciones de autoría
    # hechas por la Cámara después de la publicación inicial.
    pending = [x for x in motions if x["boletin"] not in covered or x["boletin"] in recent_bills]

    incoming = []
    errors = []
    empty = []
    successful_bills: set[str] = set()
    for idx, seed in enumerate(pending, start=1):
        try:
            _, detail = project_detail(seed["boletin"], "parlamentario")
            rows = parse_authors(detail, seed["boletin"])
            if rows:
                incoming.extend(rows)
                successful_bills.add(seed["boletin"])
            else:
                # Una moción debería tener autoría. Si una revalidación reciente
                # llega vacía, no destruimos un snapshot previo válido: se deja
                # constancia en diagnósticos y se intentará de nuevo la próxima vez.
                empty.append(seed["boletin"])
        except Exception as exc:  # noqa: BLE001
            errors.append({"boletin": seed["boletin"], "error": str(exc)})
        if idx % 50 == 0:
            print(f"Autorías {idx}/{len(pending)} · válidas={len(successful_bills)} · errores={len(errors)}")

    # Reemplazo exacto por boletín solo cuando la revalidación fue exitosa. Así
    # también desaparecen relaciones antiguas si la fuente oficial corrigió la
    # lista de firmantes, sin dejar coautores residuales.
    retained_existing = [x for x in existing if x.get("boletin") not in successful_bills]
    rows = upsert(
        retained_existing,
        incoming,
        ("boletin", "author_chamber", "author_id", "author_order"),
        ("boletin", "author_order", "author_id"),
    )
    write_csv("bill_authors.csv", rows, FIELDS)

    covered_after = {x["boletin"] for x in rows}
    new_checked = {x["boletin"] for x in pending if x["boletin"] not in covered}
    rechecked_existing = {x["boletin"] for x in pending if x["boletin"] in covered}
    diagnostics = {
        "generated_for": str(date.today()),
        "parliamentary_initiatives": len(motions),
        "recent_recheck_days": RECENT_RECHECK_DAYS,
        "recent_recheck_cutoff": str(cutoff),
        "recent_motions_considered_for_recheck": len(recent_bills),
        "new_bills_checked": len(new_checked),
        "existing_bills_revalidated": len(rechecked_existing & successful_bills),
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
