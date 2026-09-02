from __future__ import annotations

import json
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta

from legislative_common import (
    OUT,
    initiatives,
    is_terminal,
    parse_ministries,
    parse_subjects,
    project_detail,
    project_page,
    read_csv,
    upsert,
    write_csv,
)

PROJECT_FIELDS = [
    "project_id", "boletin", "titulo", "fecha_ingreso", "origen_iniciativa",
    "tipo_iniciativa", "tipo_iniciativa_codigo", "camara_origen", "camara_origen_codigo",
    "admisible", "materia_pagina", "estado_actual", "source_url", "updated_at",
]
EVENT_FIELDS = ["boletin", "fecha", "sesion", "etapa", "subetapa", "documento_url", "fuente"]
SUBJECT_FIELDS = ["boletin", "materia_id", "materia_oficial"]
MINISTRY_FIELDS = ["boletin", "ministerio_id", "ministerio"]

# Los proyectos con actividad reciente se revisan todas las semanas. Los demás
# proyectos no terminales se reparten en cuatro grupos estables: cada viernes se
# consulta un grupo distinto, de modo que todos vuelven a comprobarse al menos
# una vez cada cuatro semanas sin descargar los ~500 historiales a la vez.
RECENT_ACTIVITY_DAYS = 35
OLDER_REFRESH_SHARDS = 4
MAX_PAGE_WORKERS = 3


def safe_date(value: str) -> date | None:
    raw = (value or "").strip().split("T", 1)[0]
    try:
        return date.fromisoformat(raw)
    except Exception:
        return None


def latest_event_by_bill(events: list[dict]) -> dict[str, date]:
    latest: dict[str, date] = {}
    for row in events:
        bill = (row.get("boletin") or "").strip()
        day = safe_date(row.get("fecha", ""))
        if not bill or day is None:
            continue
        if bill not in latest or day > latest[bill]:
            latest[bill] = day
    return latest


def merge_seed(previous: dict, seed: dict) -> dict:
    project = dict(previous)
    for key, value in seed.items():
        if value not in (None, ""):
            project[key] = value
    return project


def recently_checked(previous: dict) -> bool:
    """Evita repetir cientos de páginas si el workflow se relanza el mismo día."""
    checked = safe_date(previous.get("updated_at", ""))
    return checked == date.today()


def has_recent_activity(seed: dict, latest_event: date | None, cutoff: date) -> bool:
    entered = safe_date(seed.get("fecha_ingreso", ""))
    return bool((entered and entered >= cutoff) or (latest_event and latest_event >= cutoff))


def stable_shard(boletin: str) -> int:
    return zlib.crc32(boletin.encode("utf-8")) % OLDER_REFRESH_SHARDS


def refresh_existing(seed: dict, previous: dict) -> tuple[dict, list[dict]]:
    """Refresca la capa dinámica de un proyecto ya conocido."""
    project = merge_seed(previous, seed)

    # Si por alguna razón histórica falta el ID, recuperamos una vez el detalle.
    if not project.get("project_id"):
        project, _ = project_detail(seed["boletin"], seed["origen_iniciativa"])

    page_meta, page_events = project_page(project["project_id"], project["boletin"])
    project.update(page_meta)
    return project, page_events


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    seeds = initiatives()
    existing_projects = read_csv("projects.csv")
    existing_by_bill = {x["boletin"]: x for x in existing_projects}
    subjects = read_csv("project_subjects.csv")
    ministries = read_csv("project_ministries.csv")
    events = read_csv("project_events.csv")
    latest_events = latest_event_by_bill(events)

    refreshed_projects: list[dict] = []
    new_subjects: list[dict] = []
    new_ministries: list[dict] = []
    new_events: list[dict] = []
    errors: list[dict] = []
    page_refreshed_bills: set[str] = set()
    skipped_terminal = 0
    skipped_same_day = 0
    skipped_other_shard = 0
    selected_recent = 0
    selected_rotating = 0

    existing_to_refresh: list[tuple[dict, dict]] = []
    new_to_detail: list[dict] = []
    cutoff = date.today() - timedelta(days=RECENT_ACTIVITY_DAYS)
    week_number = date.today().isocalendar().week
    active_shard = week_number % OLDER_REFRESH_SHARDS

    for seed in seeds:
        previous = existing_by_bill.get(seed["boletin"])
        if previous is None:
            new_to_detail.append(seed)
            continue

        # La semilla anual es barata: aun cuando no releamos el HTML, permite
        # absorber correcciones estructurales del índice oficial.
        seed_merged = merge_seed(previous, seed)
        refreshed_projects.append(seed_merged)

        if is_terminal(previous.get("estado_actual", "")):
            skipped_terminal += 1
            continue
        if recently_checked(previous):
            skipped_same_day += 1
            continue

        recent = has_recent_activity(seed, latest_events.get(seed["boletin"]), cutoff)
        if recent:
            selected_recent += 1
            existing_to_refresh.append((seed, previous))
            continue

        if stable_shard(seed["boletin"]) == active_shard:
            selected_rotating += 1
            existing_to_refresh.append((seed, previous))
        else:
            skipped_other_shard += 1

    # Tres trabajadores, más backoff en legislative_common.get_html(), evita las
    # ráfagas que anteriormente provocaron decenas de errores al final del lote.
    with ThreadPoolExecutor(max_workers=MAX_PAGE_WORKERS) as executor:
        futures = {
            executor.submit(refresh_existing, seed, previous): (seed, previous)
            for seed, previous in existing_to_refresh
        }
        completed = 0
        for future in as_completed(futures):
            seed, previous = futures[future]
            try:
                project, page_events = future.result()
                refreshed_projects.append(project)
                new_events.extend(page_events)
                page_refreshed_bills.add(seed["boletin"])
            except Exception as exc:  # noqa: BLE001
                errors.append({"boletin": seed["boletin"], "error": str(exc)})
                # Conservamos exactamente el último snapshot dinámico válido.
                refreshed_projects.append(merge_seed(previous, seed))
            completed += 1
            if completed % 25 == 0:
                print(
                    f"Páginas seleccionadas {completed}/{len(existing_to_refresh)} "
                    f"· errores={len(errors)}"
                )

    successful_new_bills: set[str] = set()
    for idx, seed in enumerate(new_to_detail, start=1):
        try:
            project, detail = project_detail(seed["boletin"], seed["origen_iniciativa"])
            page_meta, page_events = project_page(project["project_id"], project["boletin"])
            project.update(page_meta)
            refreshed_projects.append(project)
            new_subjects.extend(parse_subjects(detail, project["boletin"]))
            new_ministries.extend(parse_ministries(detail, project["boletin"]))
            new_events.extend(page_events)
            page_refreshed_bills.add(project["boletin"])
            successful_new_bills.add(project["boletin"])
        except Exception as exc:  # noqa: BLE001
            errors.append({"boletin": seed["boletin"], "error": str(exc)})
            fallback = dict(seed)
            fallback.update({"materia_pagina": "", "estado_actual": "", "source_url": "", "updated_at": ""})
            refreshed_projects.append(fallback)
        if idx % 25 == 0:
            print(f"Proyectos nuevos {idx}/{len(new_to_detail)} · errores={len(errors)}")

    projects = upsert(existing_projects, refreshed_projects, ("boletin",), ("fecha_ingreso", "boletin"))

    # Solo reemplazamos relaciones estructurales para proyectos nuevos cuyo
    # detalle se obtuvo correctamente. Una falla transitoria nunca borra datos.
    if successful_new_bills:
        subjects = [x for x in subjects if x.get("boletin") not in successful_new_bills]
        ministries = [x for x in ministries if x.get("boletin") not in successful_new_bills]
    subjects = upsert(subjects, new_subjects, ("boletin", "materia_id", "materia_oficial"), ("boletin", "materia_id"))
    ministries = upsert(ministries, new_ministries, ("boletin", "ministerio_id", "ministerio"), ("boletin", "ministerio_id"))

    # El historial de un boletín se sustituye solo tras una descarga HTML exitosa.
    # Los proyectos no visitados esta semana y los que fallaron conservan su
    # cronología previa completa.
    retained_events = [x for x in events if x.get("boletin") not in page_refreshed_bills]
    events = upsert(
        retained_events,
        new_events,
        ("boletin", "fecha", "sesion", "etapa", "subetapa", "documento_url"),
        ("boletin", "fecha", "etapa", "subetapa"),
    )

    write_csv("projects.csv", projects, PROJECT_FIELDS)
    write_csv("project_subjects.csv", subjects, SUBJECT_FIELDS)
    write_csv("project_ministries.csv", ministries, MINISTRY_FIELDS)
    write_csv("project_events.csv", events, EVENT_FIELDS)

    attempted_pages = len(existing_to_refresh) + len(new_to_detail)
    diagnostics = {
        "generated_for": str(date.today()),
        "initiatives_since_period_start": len(seeds),
        "projects_in_database": len(projects),
        "recent_activity_days": RECENT_ACTIVITY_DAYS,
        "older_refresh_shards": OLDER_REFRESH_SHARDS,
        "active_shard_this_week": active_shard,
        "selected_recent_projects": selected_recent,
        "selected_rotating_projects": selected_rotating,
        "existing_pages_attempted": len(existing_to_refresh),
        "existing_pages_refreshed": len(page_refreshed_bills - successful_new_bills),
        "new_projects_detailed": len(successful_new_bills),
        "skipped_terminal": skipped_terminal,
        "skipped_same_day": skipped_same_day,
        "skipped_other_shard": skipped_other_shard,
        "page_workers": MAX_PAGE_WORKERS,
        "subjects": len(subjects),
        "ministries": len(ministries),
        "events": len(events),
        "projects_with_public_matter": sum(bool(x.get("materia_pagina")) for x in projects),
        "errors": errors,
    }
    (OUT / "bills_diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if len(projects) < len(seeds):
        raise RuntimeError(f"Base incompleta: {len(projects)} proyectos para {len(seeds)} iniciativas")
    error_limit = max(3, int(attempted_pages * 0.05))
    if len(errors) > error_limit:
        raise RuntimeError(
            f"Demasiados errores de proyectos: {len(errors)}/{attempted_pages} "
            f"(límite tolerado={error_limit})"
        )
    print(json.dumps({k: v for k, v in diagnostics.items() if k != "errors"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
