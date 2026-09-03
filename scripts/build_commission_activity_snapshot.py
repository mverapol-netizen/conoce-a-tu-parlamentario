from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
COMMISSIONS_PATH = ROOT / "data" / "legislative" / "2026" / "commissions" / "commissions_snapshot.json"
OUT = ROOT / "data" / "legislative" / "2026" / "commissions" / "commission_activity_snapshot.json"
TZ = ZoneInfo("America/Santiago")
MIN_PAGE_COVERAGE = 0.80
MAX_ROWS_PER_LAYER = 8

DATE_RE = re.compile(
    r"\b(?:lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo)\s+"
    r"\d{1,2}\s+(?:de\s+)?(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+"
    r"(?:de\s+)?\d{4}\b",
    re.IGNORECASE,
)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def fetch(session: requests.Session, url: str) -> BeautifulSoup:
    response = session.get(url, timeout=(10, 35))
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def selected_period(soup: BeautifulSoup) -> dict:
    selected = []
    for select in soup.find_all("select"):
        option = select.find("option", selected=True) or select.find("option")
        if option:
            text = clean(option.get_text(" ", strip=True))
            value = clean(option.get("value", ""))
            if text:
                selected.append({"text": text, "value": value})
    return {"selected_options": selected[:4]}


def nearest_date(table: Tag) -> str:
    # Search nearby previous elements, because the institutional page places
    # a human-readable weekday/date heading immediately before each block.
    seen = 0
    for node in table.previous_elements:
        if not isinstance(node, Tag):
            continue
        if node.name not in {"h2", "h3", "h4", "h5", "strong", "div", "span", "p"}:
            continue
        text = clean(node.get_text(" ", strip=True))
        match = DATE_RE.search(text)
        if match:
            return clean(match.group(0))
        seen += 1
        if seen >= 80:
            break
    return ""


def row_to_dict(cells: list[str], headers: list[str], date_context: str) -> dict:
    row = {"date_context": date_context}
    for index, value in enumerate(cells):
        key = headers[index] if index < len(headers) and headers[index] else f"col_{index + 1}"
        row[key] = value
    return row


def parse_tables(soup: BeautifulSoup, layer: str) -> list[dict]:
    rows: list[dict] = []
    for table in soup.find_all("table"):
        tr_list = table.find_all("tr")
        if len(tr_list) < 2:
            continue
        first_cells = tr_list[0].find_all(["th", "td"])
        headers = [clean(cell.get_text(" ", strip=True)).lower().replace(" ", "_") for cell in first_cells]
        header_text = " ".join(headers)
        if layer == "citations" and not ("citaci" in header_text or "invit" in header_text):
            continue
        if layer == "results" and not ("resultado" in header_text or "materia_tratada" in header_text or "acuerdos" in header_text):
            continue

        date_context = nearest_date(table)
        for tr in tr_list[1:]:
            cells = [clean(cell.get_text(" ", strip=True)) for cell in tr.find_all("td")]
            if not cells or not any(cells):
                continue
            row = row_to_dict(cells, headers, date_context)
            # Avoid navigation/filter rows accidentally captured as data.
            substantive_text = clean(" ".join(cells))
            if len(substantive_text) < 12:
                continue
            rows.append(row)
    return rows[:MAX_ROWS_PER_LAYER]


def parse_layer(session: requests.Session, url: str, layer: str) -> dict:
    try:
        soup = fetch(session, url)
    except requests.RequestException as exc:
        return {
            "status": f"unavailable:{type(exc).__name__}",
            "url": url,
            "rows": [],
            "page_period": {},
        }
    return {
        "status": "retrieved",
        "url": url,
        "rows": parse_tables(soup, layer),
        "page_period": selected_period(soup),
    }


def main() -> None:
    if not COMMISSIONS_PATH.exists():
        raise RuntimeError("Falta commissions_snapshot.json")
    directory = json.loads(COMMISSIONS_PATH.read_text(encoding="utf-8"))
    if not str(directory.get("schema_version", "")).startswith("commissions-web-v0.4"):
        raise RuntimeError("El directorio de comisiones no supera el gate v0.4")
    commissions = directory.get("commissions") or []
    if len(commissions) < 20:
        raise RuntimeError(f"Directorio de comisiones no plausible: {len(commissions)}")

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; ConoceATuParlamentario/1.0; civic-research)",
        "Accept-Language": "es-CL,es;q=0.9,en;q=0.5",
    })

    activity = []
    citations_ok = 0
    results_ok = 0
    citation_rows = 0
    result_rows = 0

    for commission in commissions:
        citations = parse_layer(session, commission.get("citations_url", ""), "citations")
        results = parse_layer(session, commission.get("results_url", ""), "results")
        citations_ok += citations["status"] == "retrieved"
        results_ok += results["status"] == "retrieved"
        citation_rows += len(citations["rows"])
        result_rows += len(results["rows"])
        activity.append({
            "id": commission.get("id", ""),
            "number": commission.get("number", ""),
            "name": commission.get("name", ""),
            "citations": citations,
            "results": results,
        })

    n = len(activity)
    citation_coverage = citations_ok / n if n else 0
    result_coverage = results_ok / n if n else 0
    passed = citation_coverage >= MIN_PAGE_COVERAGE and result_coverage >= MIN_PAGE_COVERAGE
    if not passed:
        raise RuntimeError(
            f"Cobertura insuficiente: citaciones={citation_coverage:.1%}, resultados={result_coverage:.1%}"
        )

    now = datetime.now(TZ)
    payload = {
        "schema_version": "commission-activity-web-v0.1",
        "generated_at": now.isoformat(),
        "timezone": "America/Santiago",
        "directory_schema": directory.get("schema_version"),
        "source": {
            "name": "Cámara de Diputadas y Diputados de Chile · fichas institucionales de comisión",
            "layers": ["Citaciones", "Resultados"],
            "method": "HTML institucional de cada prmID; vista devuelta por defecto al momento de extracción",
        },
        "counts": {
            "commissions": n,
            "citations_pages_retrieved": citations_ok,
            "results_pages_retrieved": results_ok,
            "citation_rows_retained": citation_rows,
            "result_rows_retained": result_rows,
        },
        "quality_gate": {
            "minimum_page_coverage": MIN_PAGE_COVERAGE,
            "citations_coverage": citation_coverage,
            "results_coverage": result_coverage,
            "passed": True,
        },
        "commissions": activity,
        "scope_note": (
            "Citaciones describe asuntos convocados; Resultados describe materias tratadas o acuerdos registrados. "
            "No se tratan como equivalentes. Este snapshot conserva solo las primeras filas que devuelve por defecto cada ficha institucional "
            "y no pretende reconstruir todavía el historial completo de sesiones de la comisión. Una lista vacía significa que esa vista no devolvió filas, "
            "no que la comisión carezca de actividad."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Actividad comisiones={n} | citaciones {citations_ok}/{n}, filas={citation_rows} | "
        f"resultados {results_ok}/{n}, filas={result_rows}"
    )


if __name__ == "__main__":
    main()
