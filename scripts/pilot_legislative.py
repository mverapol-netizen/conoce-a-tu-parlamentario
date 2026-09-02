from __future__ import annotations

import csv
import html
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

import requests

from congress_api import child, child_text, descendants, enum_value, get_xml, local_name, person

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/legislative/pilot"
PERIOD_START = date(2026, 3, 11)
YEAR = 2026
CANDIDATES_PER_ORIGIN = 50
TARGET_PER_ORIGIN = 5
SALA_DETAIL = "https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={}"
HTTP = requests.Session()
HTTP.headers.update({"User-Agent": "Mozilla/5.0 conoce-a-tu-parlamentario/legislative-pilot", "Accept-Language": "es-CL,es;q=0.9"})


def iso_date(value: str) -> str:
    return (value or "").strip().split("T", 1)[0]


def date_ok(value: str) -> bool:
    try:
        return date.fromisoformat(iso_date(value)) >= PERIOD_START
    except Exception:
        return False


def nested(node, container: str, names: set[str]) -> list:
    parent = child(node, container)
    if parent is None:
        return []
    return [x for x in parent.iter() if local_name(x.tag) in names]


def projects_in(root) -> list:
    return [root] if local_name(root.tag) == "ProyectoLey" else descendants(root, "ProyectoLey")


def parse_project(node, origin: str) -> dict:
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


def initiatives(method: str, origin: str) -> list[dict]:
    root = get_xml("WSLegislativo", method, {"prmAnno": YEAR})
    rows = [parse_project(node, origin) for node in projects_in(root)]
    return sorted([x for x in rows if x["boletin"] and date_ok(x["fecha_ingreso"])], key=lambda x: (x["fecha_ingreso"], x["boletin"]))


def annual_votes() -> tuple[dict[str, object], dict]:
    root = get_xml("WSLegislativo", "retornarVotacionesXAnno", {"prmAnno": YEAR})
    nodes = descendants(root, "Votacion")
    index = {
        child_text(v, "Id"): v
        for v in nodes
        if child_text(v, "Id") and date_ok(child_text(v, "Fecha"))
    }
    diagnostic = {
        "root_tag": local_name(root.tag),
        "votes_returned": len(nodes),
        "votes_since_period_start": len(index),
        "tags": Counter(local_name(x.tag) for x in root.iter()).most_common(15),
    }
    if not index:
        raise RuntimeError(f"retornarVotacionesXAnno devolvió 0 votos desde el inicio: {diagnostic}")
    return index, diagnostic


def session_summary_index() -> dict[tuple[str, str], str]:
    root = get_xml("WSSala", "retornarSesionesXAnno", {"prmAnno": YEAR})
    result = {}
    for session in descendants(root, "Sesion") + descendants(root, "SesionSala"):
        day = iso_date(child_text(session, "FechaInicio"))
        number = child_text(session, "Numero")
        sid = child_text(session, "Id")
        if day and number and sid:
            result[(day, number)] = sid
    return result


def project_detail(boletin: str, origin: str) -> tuple[dict, object]:
    root = get_xml("WSLegislativo", "retornarProyectoLey", {"prmNumeroBoletin": boletin})
    nodes = projects_in(root)
    if not nodes:
        raise RuntimeError(f"Sin detalle de proyecto: {boletin}")
    return parse_project(nodes[0], origin), nodes[0]


def project_vote_object(boletin: str) -> object:
    root = get_xml("WSLegislativo", "retornarVotacionesXProyectoLey", {"prmNumeroBoletin": boletin})
    nodes = projects_in(root)
    if not nodes:
        raise RuntimeError(f"Sin votaciones para proyecto: {boletin}")
    return nodes[0]


def project_votes(node) -> list:
    return nested(node, "Votaciones", {"VotacionProyectoLey", "Votacion"})


def parse_subjects(node, boletin: str) -> list[dict]:
    return [{"boletin": boletin, "materia_id": child_text(x, "Id"), "materia_oficial": child_text(x, "Nombre")} for x in nested(node, "Materias", {"Materia"}) if child_text(x, "Id") or child_text(x, "Nombre")]


def parse_ministries(node, boletin: str) -> list[dict]:
    return [{"boletin": boletin, "ministerio_id": child_text(x, "Id"), "ministerio": child_text(x, "Nombre")} for x in nested(node, "MinisteriosPatrocinantes", {"Ministerio"}) if child_text(x, "Id") or child_text(x, "Nombre")]


def parse_authors(node, boletin: str) -> list[dict]:
    rows = []
    for wrapper in nested(node, "Autores", {"ParlamentarioAutor"}):
        target = child(wrapper, "Diputado")
        if target is None:
            target = child(wrapper, "Senador")
        p = person(target)
        if p["id"] or p["name"]:
            rows.append({"boletin": boletin, "author_order": child_text(wrapper, "Orden"), "author_id": p["id"], "author_name": p["name"], "author_chamber": p["chamber"]})
    return rows


def plain_text(raw: str) -> str:
    raw = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw)).strip()


def verify_sala_page(vote_id: str, boletin: str, expected_date: str) -> dict:
    url = SALA_DETAIL.format(vote_id)
    response = HTTP.get(url, timeout=35)
    response.raise_for_status()
    text = plain_text(response.text)
    if "Sala de Sesiones" not in text or "Detalle de Votación" not in text:
        raise RuntimeError(f"ID {vote_id}: página oficial no se identifica como Detalle de Votación de Sala")
    normalized_bill = boletin.replace(" ", "")
    if normalized_bill and normalized_bill not in text.replace(" ", ""):
        raise RuntimeError(f"ID {vote_id}: la página de Sala no contiene el boletín {boletin}")
    session_match = re.search(r"Sesión\s*n[°º]?\s*(\d+)", text, re.I)
    if not session_match:
        session_match = re.search(r"Sesión\s+(\d+)", text, re.I)
    date_match = re.search(r"Fecha:\s*(\d{1,2})\s+([A-Za-záéíóúñ]+)\s+(\d{4})", text, re.I)
    months = {"enero":"01","febrero":"02","marzo":"03","abril":"04","mayo":"05","junio":"06","julio":"07","agosto":"08","septiembre":"09","octubre":"10","noviembre":"11","diciembre":"12"}
    page_date = ""
    if date_match:
        month = months.get(date_match.group(2).lower())
        if month:
            page_date = f"{date_match.group(3)}-{month}-{int(date_match.group(1)):02d}"
    if page_date and expected_date and page_date != expected_date:
        raise RuntimeError(f"ID {vote_id}: fecha API {expected_date} != fecha página Sala {page_date}")
    return {"url": url, "session_number": session_match.group(1) if session_match else "", "page_date": page_date}


def pick(primary, fallback, field: str) -> str:
    return child_text(primary, field) or child_text(fallback, field)


def individual_votes(node, vote_id: str) -> list[dict]:
    rows = []
    for vote in nested(node, "Votos", {"Voto"}):
        p = person(child(vote, "Diputado"))
        option, option_code = enum_value(child(vote, "OpcionVoto"))
        if p["id"] or p["name"]:
            rows.append({"vote_id": vote_id, "diputado_id": p["id"], "diputado_nombre": p["name"], "opcion": option, "opcion_codigo": option_code})
    return rows


def rollcall(project_vote, base_vote, boletin: str, page: dict, session_ids: dict) -> tuple[dict, list[dict]]:
    vote_id = pick(project_vote, base_vote, "Id")
    vote_date = iso_date(pick(project_vote, base_vote, "Fecha"))
    t, tc = enum_value(child(project_vote, "Tipo") or child(base_vote, "Tipo"))
    result, result_code = enum_value(child(project_vote, "Resultado") or child(base_vote, "Resultado"))
    quorum, quorum_code = enum_value(child(project_vote, "Quorum") or child(base_vote, "Quorum"))
    ptype, ptype_code = enum_value(child(project_vote, "TipoVotacionProyectoLey"))
    constitutional, constitutional_code = enum_value(child(project_vote, "TramiteConstitucional"))
    regulatory, regulatory_code = enum_value(child(project_vote, "TramiteReglamentario"))
    session_number = page["session_number"]
    session_id = session_ids.get((page["page_date"] or vote_date, session_number), "") if session_number else ""
    row = {
        "vote_id": vote_id, "boletin": boletin, "fecha": vote_date, "sesion_id": session_id, "sesion_numero": session_number,
        "descripcion": pick(project_vote, base_vote, "Descripcion"), "articulo": child_text(project_vote, "Articulo"),
        "total_si": pick(project_vote, base_vote, "TotalSi"), "total_no": pick(project_vote, base_vote, "TotalNo"),
        "total_abstencion": pick(project_vote, base_vote, "TotalAbstencion"), "total_dispensado": pick(project_vote, base_vote, "TotalDispensado"),
        "tipo_votacion": t, "tipo_votacion_codigo": tc, "resultado": result, "resultado_codigo": result_code,
        "quorum": quorum, "quorum_codigo": quorum_code, "tipo_votacion_proyecto": ptype, "tipo_votacion_proyecto_codigo": ptype_code,
        "tramite_constitucional": constitutional, "tramite_constitucional_codigo": constitutional_code,
        "tramite_reglamentario": regulatory, "tramite_reglamentario_codigo": regulatory_code,
        "verificado_sala": "1", "verification_url": page["url"],
    }
    votes = individual_votes(base_vote, vote_id) or individual_votes(project_vote, vote_id)
    return row, votes


def write_csv(name: str, rows: list[dict], fields: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("[1/5] Universo de iniciativas...")
    motions = initiatives("retornarMocionesXAnno", "parlamentario")
    messages = initiatives("retornarMensajesXAnno", "ejecutivo")
    print(f"Mociones={len(motions)} | Mensajes={len(messages)} desde {PERIOD_START}")

    print("[2/5] Universo central de votaciones 2026...")
    annual, annual_diag = annual_votes()
    session_ids = session_summary_index()
    print(f"Votaciones API desde inicio={len(annual)} | sesiones resumen={len(session_ids)}")

    print("[3/5] Selección de 10 proyectos...")
    selected = []
    project_vote_cache = {}
    for origin, candidates in (("parlamentario", motions[:CANDIDATES_PER_ORIGIN]), ("ejecutivo", messages[:CANDIDATES_PER_ORIGIN])):
        ranked = []
        for candidate in candidates:
            try:
                node = project_vote_object(candidate["boletin"])
                ids = {child_text(v, "Id") for v in project_votes(node) if child_text(v, "Id") in annual and date_ok(child_text(v, "Fecha"))}
                ranked.append((len(ids), candidate)); project_vote_cache[candidate["boletin"]] = node
            except Exception as exc:
                print(f"  ERROR {candidate['boletin']}: {exc}")
        ranked.sort(key=lambda x: (-x[0], x[1]["fecha_ingreso"], x[1]["boletin"]))
        chosen = ranked[:TARGET_PER_ORIGIN]
        selected.extend([x[1] for x in chosen])
        print(f"  {origin}: " + ", ".join(f"{x[1]['boletin']}({x[0]})" for x in chosen))
    if len(selected) != 10:
        raise RuntimeError(f"Solo {len(selected)} proyectos seleccionados")

    projects=[]; subject_rows=[]; ministry_rows=[]; author_rows=[]; rollcalls=[]; member_votes=[]; events=[]
    print("[4/5] Contrato y triple validación de roll calls...")
    for seed in sorted(selected, key=lambda x:(x["fecha_ingreso"],x["boletin"])):
        boletin=seed["boletin"]
        prow, detail=project_detail(boletin, seed["origen_iniciativa"])
        projects.append(prow); subject_rows.extend(parse_subjects(detail,boletin)); ministry_rows.extend(parse_ministries(detail,boletin)); author_rows.extend(parse_authors(detail,boletin))
        for pv in project_votes(project_vote_cache[boletin]):
            vid=child_text(pv,"Id"); base=annual.get(vid)
            if base is None or not date_ok(pick(pv,base,"Fecha")): continue
            page=verify_sala_page(vid,boletin,iso_date(pick(pv,base,"Fecha")))
            rc, indiv=rollcall(pv,base,boletin,page,session_ids)
            rollcalls.append(rc); member_votes.extend(indiv)
            events.append({"boletin":boletin,"fecha":rc["fecha"],"evento_tipo":"votacion_sala","sesion_id":rc["sesion_id"],"vote_id":vid,"tramite_constitucional":rc["tramite_constitucional"],"tramite_reglamentario":rc["tramite_reglamentario"],"comision":"","fuente":rc["verification_url"]})

    subject_rows=list({(x["boletin"],x["materia_id"],x["materia_oficial"]):x for x in subject_rows}.values())
    ministry_rows=list({(x["boletin"],x["ministerio_id"],x["ministerio"]):x for x in ministry_rows}.values())
    author_rows=list({(x["boletin"],x["author_chamber"],x["author_id"],x["author_order"]):x for x in author_rows}.values())
    rollcalls=list({x["vote_id"]:x for x in rollcalls}.values())
    member_votes=list({(x["vote_id"],x["diputado_id"]):x for x in member_votes}.values())
    if not subject_rows: raise RuntimeError("0 materias oficiales")
    if not rollcalls: raise RuntimeError("0 roll calls validados como Sala")
    if not member_votes: raise RuntimeError("0 votos individuales")

    write_csv("projects.csv",projects,["project_id","boletin","titulo","fecha_ingreso","origen_iniciativa","tipo_iniciativa","tipo_iniciativa_codigo","camara_origen","camara_origen_codigo","admisible"])
    write_csv("project_subjects.csv",subject_rows,["boletin","materia_id","materia_oficial"])
    write_csv("project_ministries.csv",ministry_rows,["boletin","ministerio_id","ministerio"])
    write_csv("bill_authors.csv",author_rows,["boletin","author_order","author_id","author_name","author_chamber"])
    write_csv("rollcalls.csv",rollcalls,["vote_id","boletin","fecha","sesion_id","sesion_numero","descripcion","articulo","total_si","total_no","total_abstencion","total_dispensado","tipo_votacion","tipo_votacion_codigo","resultado","resultado_codigo","quorum","quorum_codigo","tipo_votacion_proyecto","tipo_votacion_proyecto_codigo","tramite_constitucional","tramite_constitucional_codigo","tramite_reglamentario","tramite_reglamentario_codigo","verificado_sala","verification_url"])
    write_csv("member_votes.csv",member_votes,["vote_id","diputado_id","diputado_nombre","opcion","opcion_codigo"])
    write_csv("project_events.csv",events,["boletin","fecha","evento_tipo","sesion_id","vote_id","tramite_constitucional","tramite_reglamentario","comision","fuente"])

    diag={"generated_for":str(date.today()),"period_start":str(PERIOD_START),"universe":{"motions":len(motions),"messages":len(messages),"annual_votes":annual_diag,"session_summaries":len(session_ids)},"pilot":{"projects":len(projects),"origins":dict(Counter(x["origen_iniciativa"] for x in projects)),"subjects":len(subject_rows),"ministries":len(ministry_rows),"authors":len(author_rows),"verified_floor_rollcalls":len(rollcalls),"individual_votes":len(member_votes),"floor_events":len(events)},"selected_bills":[x["boletin"] for x in projects],"contract_findings":{"floor_verification":"Triple criterio: ID en retornarVotacionesXAnno + ID asociado al proyecto + página oficial camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx validada.","session_api_2026":"Los endpoints WSSala de 2026 omiten actualmente la colección Votaciones aunque el esquema publicado la declare; se conserva como hallazgo de compatibilidad.","themes":"Se conserva Materia oficial sin recodificar.","full_legislative_course":"Comisiones y cronología completa siguen pendientes de una capa específica."}}
    (OUT/"diagnostics.json").write_text(json.dumps(diag,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report=["# Piloto legislativo 2026","",f"Generado: {date.today()}","","## Resultado","",f"- 10 proyectos: {diag['pilot']['origins']}",f"- Materias oficiales: **{len(subject_rows)}**",f"- Autorías: **{len(author_rows)}**",f"- Votaciones de Sala triple-validadas: **{len(rollcalls)}**",f"- Votos individuales: **{len(member_votes)}**","","## Criterio de Sala","","Cada roll call debe aparecer en la API anual, estar asociado al proyecto y resolver a una página institucional `Sala de Sesiones > Detalle de Votación` del mismo boletín y fecha.","","## Hallazgo de compatibilidad","","Los endpoints WSSala 2026 devuelven resúmenes de sesión sin la colección Votaciones que figura en el esquema. No se usa ese campo ausente como condición de integridad.","","## Pendiente","","Reconstruir el curso comisión por comisión como capa separada.",""]+[f"- {x['boletin']} · {x['origen_iniciativa']} · {x['titulo']}" for x in projects]
    (OUT/"REPORT.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    print("[5/5] PILOTO VALIDADO"); print(json.dumps(diag["pilot"],ensure_ascii=False,indent=2))


if __name__ == "__main__": main()
