from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

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
    "admisible", "estado_actual", "source_url", "updated_at",
]
EVENT_FIELDS = ["boletin", "fecha", "sesion", "etapa", "subetapa", "documento_url", "fuente"]
SUBJECT_FIELDS = ["boletin", "materia_id", "materia_oficial"]
MINISTRY_FIELDS = ["boletin", "ministerio_id", "ministerio"]
MAX_PAGE_WORKERS = 6


def refresh_existing(seed: dict, previous: dict) -> tuple[dict, list[dict]]:
    """Refresca solo la capa dinámica de un proyecto ya conocido.

    El detalle XML estructural se conserva del snapshot previo y se actualiza con
    la semilla anual. La página pública de tramitación sí se relee completa.
    """
    project = dict(previous)
    for key, value in seed.items():
        if value not in (None, ""):
            project[key] = value

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

    refreshed_projects: list[dict] = []
    new_subjects: list[dict] = []
    new_ministries: list[dict] = []
    new_events: list[dict] = []
    errors: list[dict] = []
    skipped_terminal = 0

    existing_to_refresh: list[tuple[dict, dict]] = []
    new_to_detail: list[dict] = []

    for seed in seeds:
        previous = existing_by_bill.get(seed["boletin"])
        if previous and is_terminal(previous.get("estado_actual", "")):
            skipped_terminal += 1
            continue
        if previous:
            existing_to_refresh.append((seed, previous))
        else:
            new_to_detail.append(seed)

    # La parte costosa de una corrida incremental es la página de tramitación.
    # Se consulta para TODOS los proyectos activos, pero con una concurrencia
    # pequeña para reducir tiempo sin castigar el sitio de la Cámara.
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
            except Exception as exc:  # noqa: BLE001
                errors.append({"boletin": seed["boletin"], "error": str(exc)})
                refreshed_projects.append(previous)
                # Si falla el refresco, conservamos los eventos previos de ese boletín.
                new_events.extend(x for x in events if x.get("boletin") == seed["boletin"])
            completed += 1
            if completed % 50 == 0:
                print(
                    f"Páginas activas {completed}/{len(existing_to_refresh)} "
                    f"· errores={len(errors)}"
                )

    # Los proyectos nuevos sí requieren la ficha XML completa una vez, porque
    # allí obtenemos metadatos estructurales, materias (si la fuente las ofrece)
    # y ministerios patrocinantes.
    for idx, seed in enumerate(new_to_detail, start=1):
        try:
            project, detail = project_detail(seed["boletin"], seed["origen_iniciativa"])
            page_meta, page_events = project_page(project["project_id"], project["boletin"])
            project.update(page_meta)
            refreshed_projects.append(project)
            new_subjects.extend(parse_subjects(detail, project["boletin"]))
            new_ministries.extend(parse_ministries(detail, project["boletin"]))
            new_events.extend(page_events)
        except Exception as exc:  # noqa: BLE001
            errors.append({"boletin": seed["boletin"], "error": str(exc)})
            fallback = dict(seed)
            fallback.update({"estado_actual": "", "source_url": "", "updated_at": ""})
            refreshed_projects.append(fallback)
        if idx % 25 == 0:
            print(f"Proyectos nuevos {idx}/{len(new_to_detail)} · errores={len(errors)}")

    projects = upsert(existing_projects, refreshed_projects, ("boletin",), ("fecha_ingreso", "boletin"))

    # Materias y ministerios son metadatos de ingreso: solo sustituimos la capa
    # de los boletines que acabamos de detallar por primera vez.
    detailed_bills = {x["boletin"] for x in new_to_detail}
    if detailed_bills:
        subjects = [x for x in subjects if x.get("boletin") not in detailed_bills]
        ministries = [x for x in ministries if x.get("boletin") not in detailed_bills]
    subjects = upsert(subjects, new_subjects, ("boletin", "materia_id", "materia_oficial"), ("boletin", "materia_id"))
    ministries = upsert(ministries, new_ministries, ("boletin", "ministerio_id", "ministerio"), ("boletin", "ministerio_id"))

    # Para proyectos refrescados, reemplazamos la tramitación por la fotografía
    # oficial actual. Así una corrección posterior de la Cámara no deja eventos
    # obsoletos acumulados para siempre.
    refreshed_bills = {x["boletin"] for x in refreshed_projects if x.get("boletin")}
    retained_events = [x for x in events if x.get("boletin") not in refreshed_bills]
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

    diagnostics = {
        "generated_for": str(date.today()),
        "initiatives_since_period_start": len(seeds),
        "projects_in_database": len(projects),
        "existing_active_pages_refreshed": len(existing_to_refresh),
        "new_projects_detailed": len(new_to_detail),
        "skipped_terminal": skipped_terminal,
        "page_workers": MAX_PAGE_WORKERS,
        "subjects": len(subjects),
        "ministries": len(ministries),
        "events": len(events),
        "errors": errors,
    }
    (OUT / "bills_diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if len(projects) < len(seeds):
        raise RuntimeError(f"Base incompleta: {len(projects)} proyectos para {len(seeds)} iniciativas")
    if errors and len(errors) / max(len(seeds), 1) > 0.05:
        raise RuntimeError(f"Demasiados errores de proyectos: {len(errors)}/{len(seeds)}")
    print(json.dumps({k: v for k, v in diagnostics.items() if k != "errors"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
