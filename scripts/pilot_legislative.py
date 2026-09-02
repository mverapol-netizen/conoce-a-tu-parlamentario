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
CANDIDATES_PER_ORIGIN = 40
TARGET_PER_ORIGIN = 5


def iso_date(value: str) -> str:
    return (value or "").strip().split("T", 1)[0]


def date_ok(value: str) -> bool:
    try:
        return date.fromisoformat(iso_date(value)) >= PERIOD_START
    except Exception:
        return False


def nested(node, container_name: str, item_names: set[str]) -> list:
    container = child(node, container_name)
    if container is None:
        return []
    return [x for x in container.iter() if local_name(x.tag) in item_names]


def project_nodes(root) -> list:
    return [root] if local_name(root.tag) == "ProyectoLey" else descendants(root, "ProyectoLey")


def project_row(node, origin: str) -> dict:
    initiative, initiative_code = enum_value(child(node, "TipoIniciativa"))
    chamber, chamber_code = enum_value(child(node, "CamaraOrigen"))
    return {
        "project_id": child_text(node, "Id"),
        "boletin": child_text(node, "NumeroBoletin"),
        "titulo": child_text(node, "Nombre"),
        "fecha_ingreso": iso_date(child_text(node, "FechaIngreso")),
        "origen_iniciativa": origin,
        "tipo_iniciativa": initiative,
        "tipo_iniciativa_codigo": initiative_code,
        "camara_origen": chamber,
        "camara_origen_codigo": chamber_code,
        "admisible": child_text(node, "Admisible") or child_text(node, "Adminisible"),
    }


def get_origins(method: str, origin: str) -> list[dict]:
    root = get_xml("WSLegislativo", method, {"prmAnno": YEAR})
    rows = [project_row(node, origin) for node in project_nodes(root)]
    return sorted(
        [row for row in rows if row["boletin"] and date_ok(row["fecha_ingreso"])],
        key=lambda row: (row["fecha_ingreso"], row["boletin"]),
    )


def current_legislature() -> dict:
    root = get_xml("WSLegislativo", "retornarLegislaturaActual")
    node = root if local_name(root.tag) == "Legislatura" else (descendants(root, "Legislatura") or [root])[0]
    result = {
        "id": child_text(node, "Id"),
        "numero": child_text(node, "Numero"),
        "inicio": iso_date(child_text(node, "FechaInicio")),
        "termino": iso_date(child_text(node, "FechaTermino")),
    }
    if not result["id"]:
        raise RuntimeError(f"No se pudo identificar legislatura actual; raíz={local_name(root.tag)}")
    return result


def sala_vote_index() -> tuple[dict[str, dict], dict]:
    legislature = current_legislature()
    root = get_xml("WSSala", "retornarSesionesXLegislatura", {"prmLegislaturaId": legislature["id"]})
    sessions = descendants(root, "Sesion") + descendants(root, "SesionSala")
    index: dict[str, dict] = {}
    sessions_kept = 0
    for session in sessions:
        session_date = iso_date(child_text(session, "FechaInicio"))
        if not date_ok(session_date):
            continue
        sessions_kept += 1
        info = {
            "sesion_id": child_text(session, "Id"),
            "sesion_numero": child_text(session, "Numero"),
            "sesion_fecha": session_date,
        }
        for vote in nested(session, "Votaciones", {"Votacion", "VotacionProyectoLey"}):
            vote_id = child_text(vote, "Id")
            if vote_id:
                index[vote_id] = info
    tags = Counter(local_name(x.tag) for x in root.iter())
    diagnostic = {
        "legislature": legislature,
        "root_tag": local_name(root.tag),
        "sessions_detected": len(sessions),
        "sessions_since_period_start": sessions_kept,
        "sala_vote_ids": len(index),
        "most_common_tags": tags.most_common(20),
    }
    if not index:
        raise RuntimeError(f"retornarSesionesXLegislatura no entregó votaciones: {diagnostic}")
    return index, diagnostic


def fetch_project(boletin: str, origin: str) -> tuple[dict, object]:
    root = get_xml("WSLegislativo", "retornarProyectoLey", {"prmNumeroBoletin": boletin})
    nodes = project_nodes(root)
    if not nodes:
        raise RuntimeError(f"Sin detalle para {boletin}")
    return project_row(nodes[0], origin), nodes[0]


def fetch_project_votes(boletin: str) -> object:
    root = get_xml("WSLegislativo", "retornarVotacionesXProyectoLey", {"prmNumeroBoletin": boletin})
    nodes = project_nodes(root)
    if not nodes:
        raise RuntimeError(f"Sin objeto de votaciones para {boletin}")
    return nodes[0]


def project_votes(node) -> list:
    return nested(node, "Votaciones", {"VotacionProyectoLey", "Votacion"})


def subjects(node, boletin: str) -> list[dict]:
    return [
        {"boletin": boletin, "materia_id": child_text(x, "Id"), "materia_oficial": child_text(x, "Nombre")}
        for x in nested(node, "Materias", {"Materia"})
        if child_text(x, "Id") or child_text(x, "Nombre")
    ]


def ministries(node, boletin: str) -> list[dict]:
    return [
        {"boletin": boletin, "ministerio_id": child_text(x, "Id"), "ministerio": child_text(x, "Nombre")}
        for x in nested(node, "MinisteriosPatrocinantes", {"Ministerio"})
        if child_text(x, "Id") or child_text(x, "Nombre")
    ]


def authors(node, boletin: str) -> list[dict]:
    rows = []
    for wrapper in nested(node, "Autores", {"ParlamentarioAutor"}):
        person_node = child(wrapper, "Diputado") or child(wrapper, "Senador")
        parsed = person(person_node)
        if parsed["id"] or parsed["name"]:
            rows.append({
                "boletin": boletin,
                "author_order": child_text(wrapper, "Orden"),
                "author_id": parsed["id"],
                "author_name": parsed["name"],
                "author_chamber": parsed["chamber"],
            })
    return rows


def individual_votes(vote_node, vote_id: str) -> list[dict]:
    rows = []
    for vote in nested(vote_node, "Votos", {"Voto"}):
        parsed = person(child(vote, "Diputado"))
        option, option_code = enum_value(child(vote, "OpcionVoto"))
        if parsed["id"] or parsed["name"]:
            rows.append({
                "vote_id": vote_id,
                "diputado_id": parsed["id"],
                "diputado_nombre": parsed["name"],
                "opcion": option,
                "opcion_codigo": option_code,
            })
    return rows


def rollcall(vote, boletin: str, session: dict) -> tuple[dict, list[dict]]:
    vote_id = child_text(vote, "Id")
    type_label, type_code = enum_value(child(vote, "Tipo"))
    result_label, result_code = enum_value(child(vote, "Resultado"))
    quorum_label, quorum_code = enum_value(child(vote, "Quorum"))
    project_type, project_type_code = enum_value(child(vote, "TipoVotacionProyectoLey"))
    constitutional, constitutional_code = enum_value(child(vote, "TramiteConstitucional"))
    regulatory, regulatory_code = enum_value(child(vote, "TramiteReglamentario"))
    row = {
        "vote_id": vote_id,
        "boletin": boletin,
        "fecha": iso_date(child_text(vote, "Fecha")),
        "sesion_id": session["sesion_id"],
        "sesion_numero": session["sesion_numero"],
        "descripcion": child_text(vote, "Descripcion"),
        "articulo": child_text(vote, "Articulo"),
        "total_si": child_text(vote, "TotalSi"),
        "total_no": child_text(vote, "TotalNo"),
        "total_abstencion": child_text(vote, "TotalAbstencion"),
        "total_dispensado": child_text(vote, "TotalDispensado"),
        "tipo_votacion": type_label,
        "tipo_votacion_codigo": type_code,
        "resultado": result_label,
        "resultado_codigo": result_code,
        "quorum": quorum_label,
        "quorum_codigo": quorum_code,
        "tipo_votacion_proyecto": project_type,
        "tipo_votacion_proyecto_codigo": project_type_code,
        "tramite_constitucional": constitutional,
        "tramite_constitucional_codigo": constitutional_code,
        "tramite_reglamentario": regulatory,
        "tramite_reglamentario_codigo": regulatory_code,
        "verificado_sala": "1",
    }
    return row, individual_votes(vote, vote_id)


def write_csv(name: str, rows: list[dict], fields: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("[1/5] Universo de iniciativas...")
    motions = get_origins("retornarMocionesXAnno", "parlamentario")
    messages = get_origins("retornarMensajesXAnno", "ejecutivo")
    print(f"Mociones desde {PERIOD_START}: {len(motions)} | Mensajes: {len(messages)}")

    print("[2/5] Índice oficial de votaciones de Sala por legislatura...")
    sala_ids, sala_diag = sala_vote_index()
    print(f"Legislatura {sala_diag['legislature']['numero']} (id={sala_diag['legislature']['id']}) · votos Sala={len(sala_ids)}")

    print("[3/5] Buscando 5 mociones y 5 mensajes con buen poder de prueba...")
    selected = []
    cached_votes = {}
    for origin, candidates in (("parlamentario", motions[:CANDIDATES_PER_ORIGIN]), ("ejecutivo", messages[:CANDIDATES_PER_ORIGIN])):
        ranked = []
        for i, candidate in enumerate(candidates, 1):
            try:
                node = fetch_project_votes(candidate["boletin"])
                count = len({child_text(v, "Id") for v in project_votes(node) if child_text(v, "Id") in sala_ids and date_ok(child_text(v, "Fecha"))})
                cached_votes[candidate["boletin"]] = node
                ranked.append((count, candidate))
                print(f"  {origin} {i:02d}/{len(candidates)} · {candidate['boletin']} · Sala={count}")
            except Exception as exc:
                print(f"  ERROR {candidate['boletin']}: {exc}")
        ranked.sort(key=lambda item: (-item[0], item[1]["fecha_ingreso"], item[1]["boletin"]))
        selected.extend([row for _, row in ranked[:TARGET_PER_ORIGIN]])
    if len(selected) != 10:
        raise RuntimeError(f"Piloto incompleto: {len(selected)} proyectos")

    projects = []
    project_subjects = []
    project_ministries = []
    bill_authors = []
    rollcalls = []
    member_votes = []
    events = []

    print("[4/5] Materializando las siete tablas...")
    for seed in sorted(selected, key=lambda x: (x["fecha_ingreso"], x["boletin"])):
        boletin = seed["boletin"]
        detail_row, detail = fetch_project(boletin, seed["origen_iniciativa"])
        projects.append(detail_row)
        project_subjects.extend(subjects(detail, boletin))
        project_ministries.extend(ministries(detail, boletin))
        bill_authors.extend(authors(detail, boletin))
        vote_object = cached_votes[boletin]
        for vote in project_votes(vote_object):
            vote_id = child_text(vote, "Id")
            session = sala_ids.get(vote_id)
            if not session or not date_ok(child_text(vote, "Fecha")):
                continue
            rc, iv = rollcall(vote, boletin, session)
            rollcalls.append(rc)
            member_votes.extend(iv)
            events.append({
                "boletin": boletin,
                "fecha": rc["fecha"],
                "evento_tipo": "votacion_sala",
                "sesion_id": rc["sesion_id"],
                "vote_id": rc["vote_id"],
                "tramite_constitucional": rc["tramite_constitucional"],
                "tramite_reglamentario": rc["tramite_reglamentario"],
                "comision": "",
                "fuente": "Open Data Cámara: WSLegislativo + WSSala/retornarSesionesXLegislatura",
            })

    project_subjects = list({(x["boletin"], x["materia_id"], x["materia_oficial"]): x for x in project_subjects}.values())
    project_ministries = list({(x["boletin"], x["ministerio_id"], x["ministerio"]): x for x in project_ministries}.values())
    bill_authors = list({(x["boletin"], x["author_chamber"], x["author_id"], x["author_order"]): x for x in bill_authors}.values())
    rollcalls = list({x["vote_id"]: x for x in rollcalls}.values())
    member_votes = list({(x["vote_id"], x["diputado_id"]): x for x in member_votes}.values())

    if not project_subjects:
        raise RuntimeError("0 materias: revisar contrato de retornarProyectoLey")
    if not rollcalls:
        raise RuntimeError("0 votaciones de Sala en los 10 casos seleccionados")
    if not member_votes:
        raise RuntimeError("0 votos individuales en las votaciones seleccionadas")

    write_csv("projects.csv", projects, ["project_id", "boletin", "titulo", "fecha_ingreso", "origen_iniciativa", "tipo_iniciativa", "tipo_iniciativa_codigo", "camara_origen", "camara_origen_codigo", "admisible"])
    write_csv("project_subjects.csv", project_subjects, ["boletin", "materia_id", "materia_oficial"])
    write_csv("project_ministries.csv", project_ministries, ["boletin", "ministerio_id", "ministerio"])
    write_csv("bill_authors.csv", bill_authors, ["boletin", "author_order", "author_id", "author_name", "author_chamber"])
    write_csv("rollcalls.csv", rollcalls, ["vote_id", "boletin", "fecha", "sesion_id", "sesion_numero", "descripcion", "articulo", "total_si", "total_no", "total_abstencion", "total_dispensado", "tipo_votacion", "tipo_votacion_codigo", "resultado", "resultado_codigo", "quorum", "quorum_codigo", "tipo_votacion_proyecto", "tipo_votacion_proyecto_codigo", "tramite_constitucional", "tramite_constitucional_codigo", "tramite_reglamentario", "tramite_reglamentario_codigo", "verificado_sala"])
    write_csv("member_votes.csv", member_votes, ["vote_id", "diputado_id", "diputado_nombre", "opcion", "opcion_codigo"])
    write_csv("project_events.csv", events, ["boletin", "fecha", "evento_tipo", "sesion_id", "vote_id", "tramite_constitucional", "tramite_reglamentario", "comision", "fuente"])

    result = {
        "generated_for": str(date.today()),
        "period_start": str(PERIOD_START),
        "universe": {
            "motions_since_period_start": len(motions),
            "messages_since_period_start": len(messages),
            "sala": sala_diag,
        },
        "pilot": {
            "projects": len(projects),
            "origins": dict(Counter(x["origen_iniciativa"] for x in projects)),
            "subjects": len(project_subjects),
            "ministries": len(project_ministries),
            "authors": len(bill_authors),
            "verified_floor_rollcalls": len(rollcalls),
            "individual_votes": len(member_votes),
            "floor_events": len(events),
        },
        "selected_bills": [x["boletin"] for x in projects],
        "contract_findings": {
            "floor_verification": "El ID de votación debe aparecer en una sesión de Sala retornada por WSSala.retornarSesionesXLegislatura.",
            "themes": "Materia oficial se conserva sin macroclasificación propia.",
            "authorship": "Formato largo proyecto × autor.",
            "full_legislative_course": "La cronología comisión por comisión sigue siendo una capa pendiente y no se presume a partir de estas tablas.",
        },
    }
    (OUT / "diagnostics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Piloto legislativo 2026", "", f"Generado: {date.today()}", f"Inicio del período: {PERIOD_START}.", "",
        "## Resultado", "",
        f"- Proyectos: **{len(projects)}** (5 mociones + 5 mensajes).",
        f"- Materias oficiales: **{len(project_subjects)}**.",
        f"- Autorías: **{len(bill_authors)}**.",
        f"- Votaciones verificadas de Sala: **{len(rollcalls)}**.",
        f"- Votos individuales: **{len(member_votes)}**.", "",
        "## Regla de Sala", "",
        "Una votación solo entra si su ID aparece en `WSSala.retornarSesionesXLegislatura` para la legislatura actual. No se infiere por descripción ni por tipo de proyecto.", "",
        "## Límite deliberado", "",
        "La secuencia completa de comisiones todavía no forma parte del contrato validado; se agregará como capa separada después de identificar su fuente oficial más estable.", "",
        "## Casos", "",
    ] + [f"- {x['boletin']} · {x['origen_iniciativa']} · {x['titulo']}" for x in projects]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("[5/5] PILOTO VALIDADO")
    print(json.dumps(result["pilot"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
