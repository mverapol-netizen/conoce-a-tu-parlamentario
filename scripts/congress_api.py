from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

import requests

OPEN_DATA_HOSTS = (
    "https://opendata.congreso.cl/camaradiputados",
    "https://opendata.camara.cl/camaradiputados",
)

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "Mozilla/5.0 conoce-a-tu-parlamentario/legislative-pilot",
        "Accept-Language": "es-CL,es;q=0.9,en;q=0.7",
    }
)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def children(node: ET.Element, wanted: str) -> list[ET.Element]:
    return [child for child in list(node) if local_name(child.tag) == wanted]


def child(node: ET.Element | None, wanted: str) -> ET.Element | None:
    if node is None:
        return None
    for item in list(node):
        if local_name(item.tag) == wanted:
            return item
    return None


def child_text(node: ET.Element | None, wanted: str, default: str = "") -> str:
    item = child(node, wanted)
    if item is None:
        return default
    return (item.text or "").strip()


def descendants(node: ET.Element, wanted: str) -> list[ET.Element]:
    return [item for item in node.iter() if local_name(item.tag) == wanted]


def enum_value(node: ET.Element | None) -> tuple[str, str]:
    """Devuelve (etiqueta, codigo) de los tipos del servicio, tolerando serializaciones distintas."""
    if node is None:
        return "", ""
    code = str(node.attrib.get("Valor", "") or node.attrib.get("valor", "")).strip()
    text = (node.text or "").strip()
    if not text:
        for wanted in ("Nombre", "Descripcion", "Glosa", "Valor"):
            candidate = child_text(node, wanted)
            if candidate:
                text = candidate
                break
    return text, code


def person(node: ET.Element | None) -> dict:
    if node is None:
        return {"id": "", "name": "", "chamber": ""}
    chamber = local_name(node.tag)
    pieces = [
        child_text(node, "Nombre"),
        child_text(node, "Nombre2"),
        child_text(node, "ApellidoPaterno"),
        child_text(node, "ApellidoMaterno"),
    ]
    return {
        "id": child_text(node, "Id"),
        "name": " ".join(piece for piece in pieces if piece).strip(),
        "chamber": chamber,
    }


def get_xml(service: str, method: str, params: dict | None = None, *, timeout: int = 60, tries: int = 3) -> ET.Element:
    query = f"?{urlencode(params or {})}" if params else ""
    errors: list[str] = []
    for host in OPEN_DATA_HOSTS:
        url = f"{host}/WServices/{service}.asmx/{method}{query}"
        for attempt in range(tries):
            try:
                response = SESSION.get(url, timeout=timeout, allow_redirects=True)
                response.raise_for_status()
                content = response.content.lstrip()
                if not content.startswith(b"<"):
                    raise RuntimeError("respuesta no XML")
                return ET.fromstring(response.content)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{url} intento {attempt + 1}: {exc}")
                time.sleep(0.7 * (attempt + 1))
    raise RuntimeError(" | ".join(errors[-8:]))
