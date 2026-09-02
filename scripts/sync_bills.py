from __future__ import annotations

import json
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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    seeds = initiatives()
    existing_projects = read_csv("projects.csv")
    existing_by_bill = {x["boletin"]: x for x in existing_projects}
    subjects = read_csv("project_subjects.csv")
    ministries = read_csv("project_ministries.csv")
    events = read_csv("project_events.csv")

    refreshed_projects = []
    new_subjects = []
    new_ministries = []
    new_events = []
    errors = []
    refreshed = 0
    skipped_terminal = 0

    for idx, seed in enumerate(seeds, start=1):
        previous = existing_by_bill.get(seed["boletin"])
        if previous and is_terminal(previous.get("estado_actual", "")):
            skipped_terminal += 1
            continue
        try:
            project, detail = project_detail(seed["boletin"], seed["origen_iniciativa"])
            page_meta, page_events = project_page(project["project_id"], project["boletin"])
            project.update(page_meta)
            refreshed_projects.append(project)
            new_subjects.extend(parse_subjects(detail, project["boletin"]))
            new_ministries.extend(parse_ministries(detail, project["boletin"]))
            new_events.extend(page_events)
            refreshed += 1
        except Exception as exc:  # noqa: BLE001
            errors.append({"boletin": seed["boletin"], "error": str(exc)})
            if previous:
                refreshed_projects.append(previous)
            else:
                fallback = dict(seed)
                fallback.update({"estado_actual": "", "source_url": "", "updated_at": ""})
                refreshed_projects.append(fallback)
        if idx % 50 == 0:
            print(f"Procesados {idx}/{len(seeds)} · errores={len(errors)}")

    projects = upsert(existing_projects, refreshed_projects, ("boletin",), ("fecha_ingreso", "boletin"))
    subjects = upsert(subjects, new_subjects, ("boletin", "materia_id", "materia_oficial"), ("boletin", "materia_id"))
    ministries = upsert(ministries, new_ministries, ("boletin", "ministerio_id", "ministerio"), ("boletin", "ministerio_id"))
    events = upsert(events, new_events, ("boletin", "fecha", "sesion", "etapa", "subetapa", "documento_url"), ("boletin", "fecha", "etapa", "subetapa"))

    write_csv("projects.csv", projects, PROJECT_FIELDS)
    write_csv("project_subjects.csv", subjects, SUBJECT_FIELDS)
    write_csv("project_ministries.csv", ministries, MINISTRY_FIELDS)
    write_csv("project_events.csv", events, EVENT_FIELDS)

    diagnostics = {
        "generated_for": str(date.today()),
        "initiatives_since_period_start": len(seeds),
        "projects_in_database": len(projects),
        "refreshed_this_run": refreshed,
        "skipped_terminal": skipped_terminal,
        "subjects": len(subjects),
        "ministries": len(ministries),
        "events": len(events),
        "errors": errors,
    }
    (OUT / "bills_diagnostics.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if len(projects) < len(seeds):
        raise RuntimeError(f"Base incompleta: {len(projects)} proyectos para {len(seeds)} iniciativas")
    if errors and len(errors) / max(len(seeds), 1) > 0.05:
        raise RuntimeError(f"Demasiados errores de proyectos: {len(errors)}/{len(seeds)}")
    print(json.dumps({k: v for k, v in diagnostics.items() if k != "errors"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
