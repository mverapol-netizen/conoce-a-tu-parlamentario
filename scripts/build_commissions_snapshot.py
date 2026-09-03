from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026" / "commissions" / "commissions_snapshot.json"
TZ = ZoneInfo("America/Santiago")
LIST_URL = "https://www.camara.cl/legislacion/comisiones/comisiones_permanentes.aspx"
DETAIL_BASE = "https://www.camara.cl/legislacion/comisiones/"
MIN_EXPECTED_COMMISSION_COUNT = 20
GENERIC_LINK_TEXT = {
    "integrantes", "sesiones", "proyectos de ley", "citaciones", "resultados",
    "documentos", "jornadas temáticas", "oficios enviados", "informes",
    "audiencias públicas", "ver", "volver",
}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def commission_id_from_href(href: str) -> str:
    if not href:
        return ""
    parsed = urlparse(urljoin(DETAIL_BASE, href))
    query = parse_qs(parsed.query)
    for key, values in query.items():
        if key.lower() == "prmid" and values:
            return clean(values[0])
    return ""


def fetch(session: requests.Session, url: str) -> BeautifulSoup:
    response = session.get(url, timeout=(10, 35))
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def list_commissions(session: requests.Session) -> list[dict]:
    soup = fetch(session, LIST_URL)
    found: dict[str, dict] = {}

    for row in soup.find_all("tr"):
        cells = row.find_all(["td", "th"])
        if len(cells) < 2:
            continue
        candidates = []
        for anchor in row.find_all("a", href=True):
            cid = commission_id_from_href(anchor.get("href", ""))
            text = clean(anchor.get_text(" ", strip=True))
            if cid and text and text.lower() not in GENERIC_LINK_TEXT:
                candidates.append((cid, text, anchor.get("href", "")))
        if not candidates:
            continue
        cid, anchor_text, href = max(candidates, key=lambda item: len(item[1]))
        number = clean(cells[0].get_text(" ", strip=True))
        name = clean(cells[1].get_text(" ", strip=True)) or anchor_text
        if not name or len(name) < 4:
            continue
        found[cid] = {
            "id": cid,
            "number": number if number.isdigit() else "",
            "name": name,
            "type": "Permanente",
            "source_url": urljoin(DETAIL_BASE, href),
            "members_url": f"{DETAIL_BASE}integrantes.aspx?prmID={cid}",
            "sessions_url": f"{DETAIL_BASE}sesiones.aspx?prmID={cid}",
            "projects_url": f"{DETAIL_BASE}proyecto_ley.aspx?prmID={cid}",
            "citations_url": f"{DETAIL_BASE}citaciones.aspx?prmID={cid}",
            "results_url": f"{DETAIL_BASE}resultados.aspx?prmID={cid}",
        }

    if len(found) < MIN_EXPECTED_COMMISSION_COUNT:
        for anchor in soup.find_all("a", href=True):
            cid = commission_id_from_href(anchor.get("href", ""))
            text = clean(anchor.get_text(" ", strip=True))
            if not cid or not text or text.lower() in GENERIC_LINK_TEXT or len(text) < 4:
                continue
            href = anchor.get("href", "")
            if "/legislacion/comisiones/" not in urljoin(DETAIL_BASE, href).lower():
                continue
            found.setdefault(cid, {
                "id": cid,
                "number": "",
                "name": text,
                "type": "Permanente",
                "source_url": urljoin(DETAIL_BASE, href),
                "members_url": f"{DETAIL_BASE}integrantes.aspx?prmID={cid}",
                "sessions_url": f"{DETAIL_BASE}sesiones.aspx?prmID={cid}",
                "projects_url": f"{DETAIL_BASE}proyecto_ley.aspx?prmID={cid}",
                "citations_url": f"{DETAIL_BASE}citaciones.aspx?prmID={cid}",
                "results_url": f"{DETAIL_BASE}resultados.aspx?prmID={cid}",
            })

    commissions = list(found.values())
    commissions.sort(key=lambda row: (int(row["number"]) if row["number"].isdigit() else 999, row["name"]))
    return commissions


def parse_member_id(href: str) -> str:
    parsed = urlparse(urljoin("https://www.camara.cl", href or ""))
    query = parse_qs(parsed.query)
    for key, values in query.items():
        if key.lower() in {"prmid", "prmidiputado"} and values:
            return clean(values[0])
    return ""


def extract_member_links(scope) -> dict[str, dict]:
    members: dict[str, dict] = {}
    for anchor in scope.find_all("a", href=True):
        href = anchor.get("href", "")
        full = urljoin("https://www.camara.cl", href)
        if "/diputados/detalle/" not in full.lower():
            continue
        name = clean(anchor.get_text(" ", strip=True))
        if not name or len(name) < 4:
            continue
        member_id = parse_member_id(href)
        key = member_id or name.lower()
        members[key] = {
            "id": member_id,
            "name": name,
            "profile_url": full,
        }
    return members


def enrich_members(session: requests.Session, commission: dict) -> dict:
    try:
        soup = fetch(session, commission["members_url"])
    except requests.RequestException as exc:
        commission["members_status"] = f"unavailable:{type(exc).__name__}"
        commission["members"] = []
        return commission

    page_text = clean(soup.get_text(" ", strip=True))
    type_match = re.search(r"Tipo de Comisión:\s*([^|]+?)(?:Integrantes|Sesiones|Proyectos de Ley|$)", page_text, re.IGNORECASE)
    if type_match:
        commission["type"] = clean(type_match.group(1))[:120]

    # Global headers may contain links to deputies who are not commission members.
    # Therefore choose the table with the densest cluster of deputy-profile links.
    table_candidates: list[tuple[int, dict[str, dict]]] = []
    for table in soup.find_all("table"):
        members = extract_member_links(table)
        if members:
            table_candidates.append((len(members), members))

    if table_candidates:
        _, members = max(table_candidates, key=lambda item: item[0])
        extraction_method = "member_table"
    else:
        broad = extract_member_links(soup)
        # Fallback removes navigation/header links by preferring the honorific format
        # used by the institutional integrantes list when it is present.
        honorific = {
            key: value for key, value in broad.items()
            if re.match(r"^(Sr\.|Sra\.)\s", value["name"])
        }
        members = honorific or broad
        extraction_method = "page_fallback"

    commission["members"] = sorted(members.values(), key=lambda row: row["name"])
    commission["members_status"] = "retrieved" if members else "not_returned_by_page"
    commission["members_extraction"] = extraction_method
    return commission


def main() -> None:
    now = datetime.now(TZ)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; ConoceATuParlamentario/1.0; civic-research)",
        "Accept-Language": "es-CL,es;q=0.9,en;q=0.5",
    })

    commissions = list_commissions(session)
    if len(commissions) < MIN_EXPECTED_COMMISSION_COUNT:
        raise RuntimeError(
            f"Directorio oficial no plausible: {len(commissions)} comisiones con prmID "
            f"(< {MIN_EXPECTED_COMMISSION_COUNT})"
        )

    enriched = [enrich_members(session, commission) for commission in commissions]
    payload = {
        "schema_version": "commissions-web-v0.4",
        "generated_at": now.isoformat(),
        "timezone": "America/Santiago",
        "source": {
            "name": "Cámara de Diputadas y Diputados de Chile · Directorio institucional de comisiones permanentes",
            "url": LIST_URL,
            "method": "HTML institucional server-rendered; prmID como identificador de instancia",
        },
        "counts": {
            "commissions": len(enriched),
            "with_members_retrieved": sum(bool(row.get("members")) for row in enriched),
            "member_rows": sum(len(row.get("members", [])) for row in enriched),
            "member_table_method": sum(row.get("members_extraction") == "member_table" for row in enriched),
        },
        "commissions": enriched,
        "quality_gate": {
            "minimum_expected_commissions": MIN_EXPECTED_COMMISSION_COUNT,
            "passed": True,
            "note": "El workflow falla antes de persistir si el directorio devuelve un universo implausiblemente pequeño.",
        },
        "scope_note": (
            "El directorio describe comisiones permanentes visibles en la página institucional actual. "
            "Los integrantes se recuperan desde la tabla de la ficha oficial cuando está disponible; una lista vacía no se interpreta como ausencia sustantiva. "
            "Comisiones investigadoras, unidas, mixtas u otras familias requieren capas separadas."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Directorio institucional: comisiones={len(enriched)} | "
        f"con integrantes={payload['counts']['with_members_retrieved']} | "
        f"filas integrantes={payload['counts']['member_rows']} | "
        f"tabla={payload['counts']['member_table_method']}"
    )


if __name__ == "__main__":
    main()
