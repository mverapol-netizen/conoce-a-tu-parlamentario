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


def normalize_header(value: str) -> str:
    text = clean(value).lower()
    text = re.sub(r"[^a-záéíóúüñ0-9]+", "_", text, flags=re.IGNORECASE)
    return text.strip("_")


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


def top_level_rows(table: Tag) -> list[Tag]:
    rows: list[Tag] = []
    for section in table.find_all(["thead", "tbody", "tfoot"], recursive=False):
        rows.extend(section.find_all("tr", recursive=False))
    if not rows:
        rows = table.find_all("tr", recursive=False)
    return rows


def direct_cells(row: Tag, names: tuple[str, ...] = ("th", "td")) -> list[Tag]:
    return row.find_all(list(names), recursive=False)


def row_to_dict(cells: list[str], headers: list[str], date_context: str) -> dict:
    row = {"date_context": date_context}
    for index, value in enumerate(cells):
        key = headers[index] if index < len(headers) and headers[index] else f"col_{index + 1}"
        row[key] = value
    return row


def header_matches(layer: str, header_text: str) -> bool:
    if layer == "citations":
        return "citaci" in header_text or "invit" in header_text
    if layer == "results":
        return "resultado" in header_text or "materia_tratada" in header_text or "acuerdos" in header_text
    if layer == "sessions":
        return "inicio" in header_text and "estado" in header_text and ("dia" in header_text or "día" in header_text or "termino" in header_text or "término" in header_text)
    return False


def parse_tables(soup: BeautifulSoup, layer: str) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    seen_signatures: set[str] = set()
    diagnostics = {
        "top_level_tables_examined": 0,
        "matching_tables": 0,
        "nested_tables_skipped": 0,
        "wide_rows_skipped": 0,
        "duplicate_rows_skipped": 0,
    }

    for table in soup.find_all("table"):
        if table.find_parent("table") is not None:
            diagnostics["nested_tables_skipped"] += 1
            continue
        diagnostics["top_level_tables_examined"] += 1
        tr_list = top_level_rows(table)
        if len(tr_list) < 2:
            continue

        header_row_index = None
        headers: list[str] = []
        for idx, tr in enumerate(tr_list[:3]):
            cells = direct_cells(tr)
            candidate = [normalize_header(cell.get_text(" ", strip=True)) for cell in cells]
            header_text = " ".join(candidate)
            if header_matches(layer, header_text):
                header_row_index = idx
                headers = candidate
                break
        if header_row_index is None:
            continue

        diagnostics["matching_tables"] += 1
        date_context = "" if layer == "sessions" else nearest_date(table)
        for tr in tr_list[header_row_index + 1:]:
            cell_tags = direct_cells(tr, ("td",))
            cells = [clean(cell.get_text(" ", strip=True)) for cell in cell_tags]
            if not cells or not any(cells):
                continue
            if len(cells) > max(14 if layer == "sessions" else 6, len(headers) + 1):
                diagnostics["wide_rows_skipped"] += 1
                continue
            substantive_text = clean(" ".join(cells))
            if len(substantive_text) < 8:
                continue
            signature = f"{date_context}|{substantive_text}"
            if signature in seen_signatures:
                diagnostics["duplicate_rows_skipped"] += 1
                continue
            seen_signatures.add(signature)
            rows.append(row_to_dict(cells, headers, date_context))

    return rows[:MAX_ROWS_PER_LAYER], diagnostics


def parse_layer(session: requests.Session, url: str, layer: str) -> dict:
    try:
        soup = fetch(session, url)
    except requests.RequestException as exc:
        return {
            "status": f"unavailable:{type(exc).__name__}",
            "url": url,
            "rows": [],
            "page_period": {},
            "diagnostics": {},
        }
    rows, diagnostics = parse_tables(soup, layer)
    return {
        "status": "retrieved",
        "url": url,
        "rows": rows,
        "page_period": selected_period(soup),
        "diagnostics": diagnostics,
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
    sessions_ok = 0
    citation_rows = 0
    result_rows = 0
    session_rows = 0

    for commission in commissions:
        citations = parse_layer(session, commission.get("citations_url", ""), "citations")
        results = parse_layer(session, commission.get("results_url", ""), "results")
        sessions = parse_layer(session, commission.get("sessions_url", ""), "sessions")
        citations_ok += citations["status"] == "retrieved"
        results_ok += results["status"] == "retrieved"
        sessions_ok += sessions["status"] == "retrieved"
        citation_rows += len(citations["rows"])
        result_rows += len(results["rows"])
        session_rows += len(sessions["rows"])
        activity.append({
            "id": commission.get("id", ""),
            "number": commission.get("number", ""),
            "name": commission.get("name", ""),
            "sessions": sessions,
            "citations": citations,
            "results": results,
        })

    n = len(activity)
    citation_coverage = citations_ok / n if n else 0
    result_coverage = results_ok / n if n else 0
    session_coverage = sessions_ok / n if n else 0
    passed = min(citation_coverage, result_coverage, session_coverage) >= MIN_PAGE_COVERAGE
    if not passed:
        raise RuntimeError(
            f"Cobertura insuficiente: sesiones={session_coverage:.1%}, citaciones={citation_coverage:.1%}, resultados={result_coverage:.1%}"
        )

    now = datetime.now(TZ)
    payload = {
        "schema_version": "commission-activity-web-v0.3",
        "generated_at": now.isoformat(),
        "timezone": "America/Santiago",
        "directory_schema": directory.get("schema_version"),
        "source": {
            "name": "Cámara de Diputadas y Diputados de Chile · fichas institucionales de comisión",
            "layers": ["Sesiones", "Citaciones", "Resultados"],
            "method": "HTML institucional de cada prmID; solo tablas principales, excluyendo subtablas anidadas",
        },
        "counts": {
            "commissions": n,
            "sessions_pages_retrieved": sessions_ok,
            "citations_pages_retrieved": citations_ok,
            "results_pages_retrieved": results_ok,
            "session_rows_retained": session_rows,
            "citation_rows_retained": citation_rows,
            "result_rows_retained": result_rows,
        },
        "quality_gate": {
            "minimum_page_coverage": MIN_PAGE_COVERAGE,
            "sessions_coverage": session_coverage,
            "citations_coverage": citation_coverage,
            "results_coverage": result_coverage,
            "passed": True,
            "content_rule": "Una fila retenida corresponde a una fila principal de la tabla institucional; las subtablas no se convierten en eventos independientes.",
        },
        "commissions": activity,
        "scope_note": (
            "Sesiones registra filas del calendario/historial que devuelve la ficha; Citaciones describe asuntos convocados; Resultados describe materias tratadas o acuerdos registrados. "
            "Las tres capas se mantienen separadas. Este snapshot conserva solo las primeras filas principales que devuelve cada ficha institucional y no pretende todavía reconstruir "
            "todo el historial documental de la comisión. Una lista vacía significa que esa vista no devolvió filas, no ausencia sustantiva de actividad."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Actividad comisiones={n} | sesiones {sessions_ok}/{n}, filas={session_rows} | "
        f"citaciones {citations_ok}/{n}, filas={citation_rows} | resultados {results_ok}/{n}, filas={result_rows}"
    )


if __name__ == "__main__":
    main()
