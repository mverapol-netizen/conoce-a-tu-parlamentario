from __future__ import annotations

import csv
import html
import re
import time
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

import requests
from bs4 import BeautifulSoup

from congress_api import child, child_text, descendants, enum_value, get_xml, local_name, person

ROOT = Path(__file__).resolve().parents[1]
YEAR = 2026
PERIOD_START = date(2026, 3, 11)
OUT = ROOT / "data" / "legislative" / str(YEAR)
PROJECT_URL = "https://www.camara.cl/legislacion/ProyectosDeLey/tramitacion.aspx?prmID={project_id}&prmBOLETIN={boletin}"
SALA_URL = "https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={vote_id}"
HTTP = requests.Session()
HTTP.headers.update({"User-Agent": "Mozilla/5.0 conoce-a-tu-parlamentario/legislative-sync", "Accept-Language": "es-CL,es;q=0.9"})

MONTHS = {
    "ene": 1, "enero": 1, "feb": 2, "febrero": 2, "mar": 3, "marzo": 3,
    "abr": 4, "abril": 4, "may": 5, "mayo": 5, "jun": 6, "junio": 6,
    "jul": 7, "julio": 7, "ago": 8, "agosto": 8, "sep": 9, "sept": 9, "septiembre": 9,
    "oct": 10, "octubre": 10, "nov": 11, "noviembre": 11, "dic": 12, "diciembre": 12,
}

TERMINAL_HINTS = ("publicado", "archivado", "retirado", "rechazado", "promulgado")
RETRYABLE_HTTP = {429, 500, 502, 503, 504}


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


def initiatives() -> list[dict]:
    rows: list[dict] = []
    for method, origin in (("retornarMocionesXAnno", "parlamentario"), ("retornarMensajesXAnno", "ejecutivo")):
        root = get_xml("WSLegislativo", method, {"prmAnno": YEAR})
        rows.extend(parse_project(node, origin) for node in projects_in(root))
    rows = [x for x in rows if x["boletin"] and date_ok(x["fecha_ingreso"])]
    return sorted(rows, key=lambda x: (x["fecha_ingreso"], x["boletin"]))


def project_detail(boletin: str, origin: str) -> tuple[dict, object]:
    root = get_xml("WSLegislativo", "retornarProyectoLey", {"prmNumeroBoletin": boletin})
    nodes = projects_in(root)
    if not nodes:
        raise RuntimeError(f"Sin detalle oficial para boletín {boletin}")
    return parse_project(nodes[0], origin), nodes[0]


def parse_subjects(node, boletin: str) -> list[dict]:
    return [
        {"boletin": boletin, "materia_id": child_text(x, "Id"), "materia_oficial": child_text(x, "Nombre")}
        for x in nested(node, "Materias", {"Materia"})
        if child_text(x, "Id") or child_text(x, "Nombre")
    ]


def parse_ministries(node, boletin: str) -> list[dict]:
    return [
        {"boletin": boletin, "ministerio_id": child_text(x, "Id"), "ministerio": child_text(x, "Nombre")}
        for x in nested(node, "MinisteriosPatrocinantes", {"Ministerio"})
        if child_text(x, "Id") or child_text(x, "Nombre")
    ]


def parse_authors(node, boletin: str) -> list[dict]:
    rows = []
    for wrapper in nested(node, "Autores", {"ParlamentarioAutor"}):
        target = child(wrapper, "Diputado")
        if target is None:
            target = child(wrapper, "Senador")
        p = person(target)
        if p["id"] or p["name"]:
            rows.append({
                "boletin": boletin,
                "author_order": child_text(wrapper, "Orden"),
                "author_id": p["id"],
                "author_name": p["name"],
                "author_chamber": p["chamber"],
            })
    return rows


def read_csv(name: str) -> list[dict]:
    path = OUT / name
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(name: str, rows: list[dict], fields: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def upsert(existing: Iterable[dict], incoming: Iterable[dict], keys: tuple[str, ...], sort_keys: tuple[str, ...] = ()) -> list[dict]:
    index = {tuple(row.get(k, "") for k in keys): dict(row) for row in existing}
    for row in incoming:
        index[tuple(row.get(k, "") for k in keys)] = dict(row)
    rows = list(index.values())
    if sort_keys:
        rows.sort(key=lambda r: tuple(r.get(k, "") for k in sort_keys))
    return rows


def spanish_date(value: str) -> str:
    text = re.sub(r"[.,]", "", (value or "").strip().lower())
    match = re.search(r"(\d{1,2})\s+([a-záéíóúñ]+)\s+(\d{4})", text)
    if not match:
        return ""
    month = MONTHS.get(match.group(2)[:3], MONTHS.get(match.group(2)))
    if not month:
        return ""
    return date(int(match.group(3)), month, int(match.group(1))).isoformat()


def get_html(url: str, *, timeout: int = 45, tries: int = 4) -> requests.Response:
    """Consulta HTML con backoff conservador para no castigar el portal público.

    La Cámara puede responder 429/5xx después de ráfagas de solicitudes. Reintentar
    unas pocas veces y respetar Retry-After hace la sincronización más estable sin
    ocultar una caída persistente de la fuente.
    """
    last: Exception | None = None
    for attempt in range(tries):
        try:
            response = HTTP.get(url, timeout=timeout, allow_redirects=True)
            if response.status_code == 200:
                return response
            if response.status_code not in RETRYABLE_HTTP:
                response.raise_for_status()
            retry_after = response.headers.get("Retry-After", "").strip()
            try:
                delay = float(retry_after) if retry_after else 1.5 * (2 ** attempt)
            except ValueError:
                delay = 1.5 * (2 ** attempt)
            last = RuntimeError(f"HTTP {response.status_code} para {url}")
        except requests.RequestException as exc:
            last = exc
            delay = 1.5 * (2 ** attempt)
        if attempt < tries - 1:
            time.sleep(min(delay, 12.0))
    raise RuntimeError(str(last) if last else f"No se pudo descargar {url}")


def project_page(project_id: str, boletin: str) -> tuple[dict, list[dict]]:
    url = PROJECT_URL.format(project_id=project_id, boletin=boletin)
    response = get_html(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    status_match = re.search(r"Estado\s+(.*?)\s+Numero de bolet[ií]n", text, re.I)
    status = status_match.group(1).strip() if status_match else ""
    matter_match = re.search(r"Materia:\s*(.*?)\s+Iniciativa:", text, re.I)
    matter = matter_match.group(1).strip() if matter_match else ""
    if matter in {"-", "—", "–"}:
        matter = ""
    events = []
    for table in soup.find_all("table"):
        headers = [re.sub(r"\s+", " ", th.get_text(" ", strip=True)) for th in table.find_all("th")]
        norm = [h.lower() for h in headers]
        if not ({"fecha", "etapa"} <= set(norm)) or not any("sub-etapa" in h or "subetapa" in h for h in norm):
            continue
        for tr in table.find_all("tr"):
            cells = [re.sub(r"\s+", " ", td.get_text(" ", strip=True)) for td in tr.find_all("td")]
            if len(cells) < 4:
                continue
            document_link = ""
            link = tr.find("a", href=True)
            if link:
                href = link.get("href", "")
                document_link = requests.compat.urljoin(url, href)
            events.append({
                "boletin": boletin,
                "fecha": spanish_date(cells[0]),
                "sesion": cells[1],
                "etapa": cells[2],
                "subetapa": cells[3],
                "documento_url": document_link,
                "fuente": url,
            })
        break
    return {
        "estado_actual": status,
        "materia_pagina": matter,
        "source_url": url,
        "updated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }, events


def is_terminal(status: str) -> bool:
    text = (status or "").lower()
    return any(hint in text for hint in TERMINAL_HINTS)


def annual_votes() -> dict[str, object]:
    root = get_xml("WSLegislativo", "retornarVotacionesXAnno", {"prmAnno": YEAR})
    return {
        child_text(v, "Id"): v
        for v in descendants(root, "Votacion")
        if child_text(v, "Id") and date_ok(child_text(v, "Fecha"))
    }


def vote_detail(vote_id: str):
    root = get_xml("WSLegislativo", "retornarVotacionDetalle", {"prmVotacionId": vote_id})
    nodes = descendants(root, "Votacion")
    node = root if local_name(root.tag) == "Votacion" else (nodes[0] if nodes else None)
    if node is None:
        raise RuntimeError(f"Sin detalle de votación {vote_id}")
    return node


def individual_votes(node, vote_id: str) -> list[dict]:
    rows = []
    for vote in nested(node, "Votos", {"Voto"}):
        p = person(child(vote, "Diputado"))
        option, option_code = enum_value(child(vote, "OpcionVoto"))
        if p["id"] or p["name"]:
            rows.append({"vote_id": vote_id, "diputado_id": p["id"], "diputado_nombre": p["name"], "opcion": option, "opcion_codigo": option_code})
    return rows


def verify_sala(vote_id: str, expected_date: str = "") -> dict:
    url = SALA_URL.format(vote_id=vote_id)
    response = get_html(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = re.sub(r"\s+", " ", html.unescape(soup.get_text(" ", strip=True)))
    if "Detalle de Votación" not in text or "Sala de Sesiones" not in text:
        raise RuntimeError(f"{vote_id} no resuelve a Detalle de Votación de Sala")
    bill_match = re.search(r"Proyecto De Ley:\s*([0-9]+-[0-9]+)", text, re.I)
    date_match = re.search(r"Fecha:\s*(\d{1,2})\s+([A-Za-záéíóúñ]+)\s+(\d{4})", text, re.I)
    session_match = re.search(r"Sesión\s*n[°º]?\s*(\d+)", text, re.I)
    page_date = ""
    if date_match:
        page_date = spanish_date(" ".join(date_match.groups()))
    if expected_date and page_date and expected_date != page_date:
        raise RuntimeError(f"Fecha inconsistente en voto {vote_id}: API={expected_date} Sala={page_date}")
    return {
        "boletin": bill_match.group(1) if bill_match else "",
        "fecha": page_date or expected_date,
        "sesion_numero": session_match.group(1) if session_match else "",
        "verification_url": url,
    }
