from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

from congress_api import child, child_text, descendants, enum_value, get_xml, local_name, person

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/legislative/pilot"
PERIOD_START = date(2026, 3, 11)
YEAR = 2026
CANDIDATES_PER_ORIGIN = 30
TARGET_PER_ORIGIN = 5


def iso_date(value: str) -> str:
    return (value or "").strip().split("T", 1)[0]


def date_ok(value: str) -> bool:
    try:
        return date.fromisoformat(iso_date(value)) >= PERIOD_START
    except Exception:  # noqa: BLE001
        return False


def nested_named(node, container_name: str, item_name: str):
    container = child(node, container_name)
    if container is None:
        return []
    return [item for item in container.iter() if local_name(item.tag) == item_name]


def parse_project(node, declared_origin: str | None = None) -> dict:
    initiative_label, initiative_code = enum_value(child(node, "TipoIniciativa"))
    chamber_label, chamber_code = enum_value(child(node, "CamaraOrigen"))
    admissible = child_text(node, "Admisible") or child_text(node, "Adminisible")
    return {
        "project_id": child_text(node, "Id"),
        "boletin": child_text(node, "NumeroBoletin"),
        "titulo": child_text(node, "Nombre"),
        "fecha_ingreso": iso_date(child_text(node, "FechaIngreso")),
        "origen_iniciativa": declared_origin or "",
        "tipo_iniciativa": initiative_label,
        "tipo_iniciativa_codigo": initiative_code,
        "camara_origen": chamber_label,
        "camara_origen_codigo": chamber_code,
        "admisible": admissible,
    }


def parse_subjects(node, boletin: str) -> list[dict]:
    return [
        {"boletin": boletin, "materia_id": child_text(item, "Id"), "materia_oficial": child_text(item, "Nombre")}
        for item in nested_named(node, "Materias", "Materia")
        if child_text(item, "Id") or child_text(item, "Nombre")
    ]


def parse_ministries(node, boletin: str) -> list[dict]:
    return [
        {"boletin": boletin, "ministerio_id": child_text(item, "Id"), "ministerio": child_text(item, "Nombre")}
        for item in nested_named(node, "MinisteriosPatrocinantes", "Ministerio")
        if child_text(item, "Id") or child_text(item, "Nombre")
    ]


def parse_authors(node, boletin: str) -> list[dict]:
    rows = []
    for author in nested_named(node, "Autores", "ParlamentarioAutor"):
        dep = child(author, "Diputado")
        sen = child(author, "Senador")
        parsed = person(dep if dep is not None else sen)
        if not parsed["name"] and not parsed["id"]:
            continue
        rows.append({
            "boletin": boletin,
            "author_order": child_text(author, "Orden"),
            "author_id": parsed["id"],
            "author_name": parsed["name"],
            "author_chamber": parsed["chamber"],
        })
    return rows


def parse_member_votes(vote_node, vote_id: str) -> list[dict]:
    rows = []
    for vote in nested_named(vote_node, "Votos", "Voto"):
        parsed = person(child(vote, "Diputado"))
        option_label, option_code = enum_value(child(vote, "OpcionVoto"))
        if not parsed["id"] and not parsed["name"]:
            continue
        rows.append({
            "vote_id": vote_id,
            "diputado_id": parsed["id"],
            "diputado_nombre": parsed["name"],
            "opcion": option_label,
            "opcion_codigo": option_code,
        })
    return rows


def parse_rollcall(vote_node, boletin: str, session: dict) -> tuple[dict, list[dict]]:
    vote_id = child_text(vote_node, "Id")
    type_label, type_code = enum_value(child(vote_node, "Tipo"))
    result_label, result_code = enum_value(child(vote_node, "Resultado"))
    quorum_label, quorum_code = enum_value(child(vote_node, "Quorum"))
    project_vote_label, project_vote_code = enum_value(child(vote_node, "TipoVotacionProyectoLey"))
    constitutional_label, constitutional_code = enum_value(child(vote_node, "TramiteConstitucional"))
    regulatory_label, regulatory_code = enum_value(child(vote_node, "TramiteReglamentario"))
    row = {
        "vote_id": vote_id,
        "boletin": boletin,
        "fecha": iso_date(child_text(vote_node, "Fecha")),
        "sesion_id": session.get("sesion_id", ""),
        "sesion_numero": session.get("sesion_numero", ""),
        "descripcion": child_text(vote_node, "Descripcion"),
        "articulo": child_text(vote_node, "Articulo"),
        "total_si": child_text(vote_node, "TotalSi"),
        "total_no": child_text(vote_node, "TotalNo"),
        "total_abstencion": child_text(vote_node, "TotalAbstencion"),
        "total_dispensado": child_text(vote_node, "TotalDispensado"),
        "tipo_votacion": type_label,
        "tipo_votacion_codigo": type_code,
        "resultado": result_label,
        "resultado_codigo": result_code,
        "quorum": quorum_label,
        "quorum_codigo": quorum_code,
        "tipo_votacion_proyecto": project_vote_label,
        "tipo_votacion_proyecto_codigo": project_vote_code,
        "tramite_constitucional": constitutional_label,
        "tramite_constitucional_codigo": constitutional_code,
        "tramite_reglamentario": regulatory_label,
        "tramite_reglamentario_codigo": regulatory_code,
        "verificado_sala": "1",
    }
    return row, parse_member_votes(vote_node, vote_id)


def project_nodes(root) -> list:
    if local_name(root.tag) == "ProyectoLey":
        return [root]
    return descendants(root, "ProyectoLey")


def vote_nodes(project_node) -> list:
    return nested_named(project_node, "Votaciones", "VotacionProyectoLey")


def fetch_origin(method: str, origin: str) -> list[dict]:
    root = get_xml("WSLegislativo", method, {"prmAnno": YEAR})
    result = []
    for node in project_nodes(root):
        row = parse_project(node, origin)
        if row["boletin"] and date_ok(row["fecha_ingreso"]):
            result.append(row)
    return sorted(result, key=lambda row: (row["fecha_ingreso"], row["boletin"]))


def fetch_sessions() -> tuple[dict[str, dict], dict]:
    root = get_xml("WSSala", "retornarSesionesXAnno", {"prmAnno": YEAR})
    session_nodes = descendants(root, "Sesion") + descendants(root, "SesionSala")
    unique_sessions = []
    seen_ids = set()
    for session in session_nodes:
        sid = child_text(session, "Id") or child_text(session, "ID")
        if sid and sid not in seen_ids:
            seen_ids.add(sid)
            unique_sessions.append(session)

    vote_to_session: dict[str, dict] = {}
    kept_sessions = 0
    detail_errors = []
    for index, session in enumerate(unique_sessions, 1):
        session_date = iso_date(child_text(session, "FechaInicio") or child_text(session, "Fecha"))
        if not date_ok(session_date):
            continue
        kept_sessions += 1
        session_id = child_text(session, "Id") or child_text(session, "ID")
        info = {
            "sesion_id": session_id,
            "sesion_numero": child_text(session, "Numero"),
            "sesion_fecha": session_date,
        }
        try:
            detail_root = get_xml("WSSala", "retornarSesionAsistencia", {"prmSesionId": session_id})
            detail_nodes = []
            if local_name(detail_root.tag) in {"Sesion", "SesionSala"}:
                detail_nodes = [detail_root]
            else:
                detail_nodes = descendants(detail_root, "Sesion") + descendants(detail_root, "SesionSala")
            detail = detail_nodes[0] if detail_nodes else detail_root
            vote_container = child(detail, "Votaciones")
            if vote_container is not None:
                for vote in vote_container.iter():
                    if local_name(vote.tag) not in {"Votacion", "VotacionProyectoLey"}:
                        continue
                    vote_id = child_text(vote, "Id") or child_text(vote, "ID")
                    if vote_id:
                        vote_to_session[vote_id] = info
        except Exception as exc:  # noqa: BLE001
            detail_errors.append({"sesion_id": session_id, "error": str(exc)})
        if index % 15 == 0:
            print(f"  Sesiones auditadas: {index}/{len(unique_sessions)} · votos Sala acumulados={len(vote_to_session)}")

    tags = Counter(local_name(node.tag) for node in root.iter())
    debug = {
        "root_tag": local_name(root.tag),
        "session_nodes_detected": len(unique_sessions),
        "sessions_since_start": kept_sessions,
        "session_detail_errors": len(detail_errors),
        "session_detail_error_sample": detail_errors[:3],
        "most_common_tags": tags.most_common(20),
    }
    if not vote_to_session:
        raise RuntimeError(f"WSSala no produjo IDs de votación de Sala tras consultar detalle de sesiones. Diagnóstico: {debug}")
    return vote_to_session, debug


def fetch_project_votes(boletin: str, origin: str) -> tuple[dict, object]:
    root = get_xml("WSLegislativo", "retornarVotacionesXProyectoLey", {"prmNumeroBoletin": boletin})
    nodes = project_nodes(root)
    if not nodes:
        raise RuntimeError(f"No se encontró ProyectoLey/votaciones para boletín {boletin}")
    return parse_project(nodes[0], origin), nodes[0]


def fetch_project_detail(boletin: str, origin: str) -> tuple[dict, object]:
    root = get_xml("WSLegislativo", "retornarProyectoLey", {"prmNumeroBoletin": boletin})
    nodes = project_nodes(root)
    if not nodes:
        raise RuntimeError(f"No se encontró detalle ProyectoLey para boletín {boletin}")
    return parse_project(nodes[0], origin), nodes[0]


def write_csv(name: str, rows: list[dict], fields: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("[1/5] Descargando mociones y mensajes 2026...")
    motions = fetch_origin("retornarMocionesXAnno", "parlamentario")
    messages = fetch_origin("retornarMensajesXAnno", "ejecutivo")
    print(f"Mociones desde {PERIOD_START}: {len(motions)} | Mensajes: {len(messages)}")

    print("[2/5] Construyendo universo verificable de votaciones de Sala...")
    sessions, session_debug = fetch_sessions()
    print(f"IDs de votación vinculados a sesiones de Sala desde {PERIOD_START}: {len(sessions)}")

    pools = {
        "parlamentario": motions[:CANDIDATES_PER_ORIGIN],
        "ejecutivo": messages[:CANDIDATES_PER_ORIGIN],
    }
    enriched: dict[str, list[dict]] = {"parlamentario": [], "ejecutivo": []}
    vote_details: dict[str, object] = {}

    print("[3/5] Auditando candidatos y sus votaciones...")
    for origin, candidates in pools.items():
        for i, candidate in enumerate(candidates, 1):
            boletin = candidate["boletin"]
            try:
                row, vote_node = fetch_project_votes(boletin, origin)
                floor_ids = {
                    child_text(vote, "Id")
                    for vote in vote_nodes(vote_node)
                    if child_text(vote, "Id") in sessions and date_ok(child_text(vote, "Fecha"))
                }
                row["floor_vote_count"] = len(floor_ids)
                enriched[origin].append(row)
                vote_details[boletin] = vote_node
                print(f"  {origin} {i:02d}/{len(candidates)} · {boletin} · Sala={row['floor_vote_count']}")
            except Exception as exc:  # noqa: BLE001
                print(f"  ERROR {boletin}: {exc}")

    selected = []
    for origin in ("parlamentario", "ejecutivo"):
        ranked = sorted(
            enriched[origin],
            key=lambda row: (-int(row.get("floor_vote_count", 0)), row["fecha_ingreso"], row["boletin"]),
        )
        selected.extend(ranked[:TARGET_PER_ORIGIN])
    if len(selected) < 10:
        leftovers = [row for rows in enriched.values() for row in rows if row not in selected]
        leftovers.sort(key=lambda row: (-int(row.get("floor_vote_count", 0)), row["fecha_ingreso"]))
        selected.extend(leftovers[: 10 - len(selected)])
    if len(selected) != 10:
        raise RuntimeError(f"Piloto incompleto: se seleccionaron {len(selected)} proyectos")

    project_rows = []
    subject_rows = []
    ministry_rows = []
    author_rows = []
    rollcall_rows = []
    member_vote_rows = []
    event_rows = []

    print("[4/5] Materializando contrato del piloto...")
    for selected_row in sorted(selected, key=lambda row: (row["fecha_ingreso"], row["boletin"])):
        boletin = selected_row["boletin"]
        detail_row, detail_node = fetch_project_detail(boletin, selected_row["origen_iniciativa"])
        vote_node = vote_details[boletin]
        project_rows.append(detail_row)
        subject_rows.extend(parse_subjects(detail_node, boletin))
        ministry_rows.extend(parse_ministries(detail_node, boletin))
        author_rows.extend(parse_authors(detail_node, boletin))
        for vote in vote_nodes(vote_node):
            vote_id = child_text(vote, "Id")
            session = sessions.get(vote_id)
            if not session or not date_ok(child_text(vote, "Fecha")):
                continue
            rollcall, individual = parse_rollcall(vote, boletin, session)
            rollcall_rows.append(rollcall)
            member_vote_rows.extend(individual)
            event_rows.append({
                "boletin": boletin,
                "fecha": rollcall["fecha"],
                "evento_tipo": "votacion_sala",
                "sesion_id": rollcall["sesion_id"],
                "vote_id": vote_id,
                "tramite_constitucional": rollcall["tramite_constitucional"],
                "tramite_reglamentario": rollcall["tramite_reglamentario"],
                "comision": "",
                "fuente": "Open Data Cámara / WSLegislativo + WSSala",
            })

    rollcall_rows = list({row["vote_id"]: row for row in rollcall_rows}.values())
    member_vote_rows = list({(row["vote_id"], row["diputado_id"]): row for row in member_vote_rows}.values())
    author_rows = list({(row["boletin"], row["author_chamber"], row["author_id"], row["author_order"]): row for row in author_rows}.values())
    subject_rows = list({(row["boletin"], row["materia_id"], row["materia_oficial"]): row for row in subject_rows}.values())
    ministry_rows = list({(row["boletin"], row["ministerio_id"], row["ministerio"]): row for row in ministry_rows}.values())

    if not subject_rows:
        raise RuntimeError("El piloto no recuperó materias oficiales; revisar contrato del detalle de ProyectoLey")
    if not rollcall_rows:
        raise RuntimeError("El piloto no recuperó ninguna votación de Sala para los proyectos seleccionados")
    valid_vote_ids = {row["vote_id"] for row in rollcall_rows}
    if any(row["vote_id"] not in valid_vote_ids for row in member_vote_rows):
        raise RuntimeError("member_votes contiene votos sin rollcall correspondiente")

    write_csv("projects.csv", project_rows, ["project_id", "boletin", "titulo", "fecha_ingreso", "origen_iniciativa", "tipo_iniciativa", "tipo_iniciativa_codigo", "camara_origen", "camara_origen_codigo", "admisible"])
    write_csv("project_subjects.csv", subject_rows, ["boletin", "materia_id", "materia_oficial"])
    write_csv("project_ministries.csv", ministry_rows, ["boletin", "ministerio_id", "ministerio"])
    write_csv("bill_authors.csv", author_rows, ["boletin", "author_order", "author_id", "author_name", "author_chamber"])
    write_csv("rollcalls.csv", rollcall_rows, ["vote_id", "boletin", "fecha", "sesion_id", "sesion_numero", "descripcion", "articulo", "total_si", "total_no", "total_abstencion", "total_dispensado", "tipo_votacion", "tipo_votacion_codigo", "resultado", "resultado_codigo", "quorum", "quorum_codigo", "tipo_votacion_proyecto", "tipo_votacion_proyecto_codigo", "tramite_constitucional", "tramite_constitucional_codigo", "tramite_reglamentario", "tramite_reglamentario_codigo", "verificado_sala"])
    write_csv("member_votes.csv", member_vote_rows, ["vote_id", "diputado_id", "diputado_nombre", "opcion", "opcion_codigo"])
    write_csv("project_events.csv", event_rows, ["boletin", "fecha", "evento_tipo", "sesion_id", "vote_id", "tramite_constitucional", "tramite_reglamentario", "comision", "fuente"])

    diagnostics = {
        "generated_for": str(date.today()),
        "period_start": str(PERIOD_START),
        "year": YEAR,
        "universe": {
            "motions_since_period_start": len(motions),
            "messages_since_period_start": len(messages),
            "verified_floor_vote_ids_since_period_start": len(sessions),
            "session_parser": session_debug,
        },
        "pilot": {
            "projects": len(project_rows),
            "origins": dict(Counter(row["origen_iniciativa"] for row in project_rows)),
            "subjects": len(subject_rows),
            "ministries": len(ministry_rows),
            "authors": len(author_rows),
            "verified_floor_rollcalls": len(rollcall_rows),
            "individual_votes": len(member_vote_rows),
            "floor_events": len(event_rows),
        },
        "selected_bills": [row["boletin"] for row in project_rows],
        "contract_findings": {
            "floor_verification": "Solo se incluye una votación si su ID aparece dentro de Votaciones del detalle de una sesión de WSSala.",
            "full_legislative_course": "ProyectoLey no contiene una secuencia completa comisión por comisión; project_events conserva por ahora los trámites asociados a votaciones de Sala.",
            "themes": "Se preserva Materia oficial sin macroclasificación editorial.",
            "authorship": "Formato largo proyecto × autor, conservando orden e identificación Cámara/Senado.",
        },
    }
    (OUT / "diagnostics.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = [
        "# Piloto legislativo 2026", "", f"Generado: {date.today().isoformat()}", f"Período observado: desde {PERIOD_START.isoformat()}.", "",
        "## Resultado", "",
        f"- Proyectos piloto: **{len(project_rows)}**.",
        f"- Mociones: **{diagnostics['pilot']['origins'].get('parlamentario', 0)}**; mensajes: **{diagnostics['pilot']['origins'].get('ejecutivo', 0)}**.",
        f"- Materias oficiales: **{len(subject_rows)}** relaciones proyecto–materia.",
        f"- Autorías: **{len(author_rows)}** relaciones proyecto–autor.",
        f"- Votaciones verificadas de Sala: **{len(rollcall_rows)}**.",
        f"- Votos individuales: **{len(member_vote_rows)}**.", "",
        "## Criterio de Sala", "", "Una votación entra en `rollcalls.csv` únicamente si su ID aparece dentro del detalle de una sesión retornada por `WSSala.retornarSesionAsistencia`.", "",
        "## Hallazgo sobre tramitación", "", "`ProyectoLey` entrega iniciativa, Cámara de origen, autores, ministerios, materias y votaciones. Las votaciones agregan trámite constitucional y reglamentario. La cronología completa comisión por comisión requiere una capa adicional.", "",
        "## Boletines del piloto", "",
    ]
    report.extend([f"- {row['boletin']} · {row['origen_iniciativa']} · {row['titulo']}" for row in project_rows])
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print("[5/5] Piloto validado.")
    print(json.dumps(diagnostics["pilot"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
