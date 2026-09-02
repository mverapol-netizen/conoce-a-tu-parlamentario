from __future__ import annotations

import difflib
import html
import json
import re
import shutil
import time
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "assets/js/data.js"
OUT_FILE = ROOT / "assets/js/profiles.js"
PHOTO_DIR = ROOT / "assets/photos"

OPEN_DATA_CURRENT = (
    "https://opendata.camara.cl/camaradiputados/WServices/"
    "WSDiputado.asmx/retornarDiputadosPeriodoActual"
)
OPEN_DATA_DETAIL = (
    "https://opendata.camara.cl/camaradiputados/WServices/"
    "WSDiputado.asmx/retornarDiputado?prmDiputadoId={}"
)
PROFILE_URL = "https://www.camara.cl/diputados/detalle/biografia.aspx?prmId={}"
NS = {"c": "http://opendata.camara.cl/camaradiputados/v1"}

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "Chrome/130 Safari/537.36 conoce-a-tu-parlamentario/1.0"
        ),
        "Accept-Language": "es-CL,es;q=0.9,en;q=0.7",
    }
)


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.lower().replace("ñ", "n")
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def slug(value: str) -> str:
    return normalize(value).replace(" ", "-")


def get(url: str, *, timeout: int = 30, tries: int = 3) -> requests.Response:
    last = None
    for attempt in range(tries):
        try:
            response = SESSION.get(url, timeout=timeout)
            if response.status_code == 200:
                return response
            last = RuntimeError(f"HTTP {response.status_code} for {url}")
        except Exception as exc:  # noqa: BLE001
            last = exc
        time.sleep(0.6 * (attempt + 1))
    raise RuntimeError(str(last) if last else f"No se pudo descargar {url}")


def load_targets() -> list[dict]:
    source = DATA_FILE.read_text(encoding="utf-8")
    pattern = re.compile(
        r"\{id:(\d+),region:\"([^\"]+)\",comunas:\[(.*?)\],parlamentarios:\[(.*?)\]\}",
        re.S,
    )
    targets: list[dict] = []
    for district_id, region, _communes, reps in pattern.findall(source):
        for name in re.findall(r'\"([^\"]+)\"', reps):
            targets.append(
                {
                    "name": name,
                    "district": int(district_id),
                    "region": region,
                    "norm": normalize(name),
                }
            )
    if len(targets) != 155:
        raise RuntimeError(f"Se esperaban 155 parlamentarios; se encontraron {len(targets)}")
    return targets


def open_data_current() -> list[dict]:
    xml = get(OPEN_DATA_CURRENT).content
    root = ET.fromstring(xml)
    rows: list[dict] = []
    for node in root.findall("c:DiputadoPeriodo", NS):
        dep = node.find("c:Diputado", NS)
        district = node.find("c:Distrito/c:Numero", NS)
        if dep is None or district is None:
            continue
        dep_id = dep.findtext("c:Id", default="", namespaces=NS)
        pieces = [
            dep.findtext("c:Nombre", default="", namespaces=NS),
            dep.findtext("c:Nombre2", default="", namespaces=NS),
            dep.findtext("c:ApellidoPaterno", default="", namespaces=NS),
            dep.findtext("c:ApellidoMaterno", default="", namespaces=NS),
        ]
        name = " ".join(piece.strip() for piece in pieces if piece and piece.strip())
        if dep_id and name:
            rows.append(
                {
                    "id": int(dep_id),
                    "name": name,
                    "norm": normalize(name),
                    "district": int(district.text or 0),
                }
            )
    if len(rows) < 150:
        raise RuntimeError(f"Open Data devolvió solo {len(rows)} diputados vigentes")
    return rows


def score_name(target: dict, candidate: dict) -> float:
    if target["district"] != candidate["district"]:
        return -1
    a, b = target["norm"], candidate["norm"]
    if a == b:
        return 10
    a_tokens, b_tokens = set(a.split()), set(b.split())
    overlap = len(a_tokens & b_tokens) / max(1, len(a_tokens | b_tokens))
    seq = difflib.SequenceMatcher(None, a, b).ratio()
    containment = 0.25 if a in b or b in a else 0
    return overlap * 0.65 + seq * 0.35 + containment


def match_targets(targets: list[dict], current: list[dict]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    used: set[int] = set()
    for target in targets:
        candidates = [row for row in current if row["id"] not in used]
        ranked = sorted(candidates, key=lambda row: score_name(target, row), reverse=True)
        if not ranked or score_name(target, ranked[0]) < 0.47:
            raise RuntimeError(f"No se pudo emparejar: {target['name']}")
        chosen = ranked[0]
        used.add(chosen["id"])
        result[target["name"]] = chosen
    return result


def strings_after_label(soup: BeautifulSoup, label: str) -> str | None:
    strings = list(soup.stripped_strings)
    target = normalize(label)
    for i, value in enumerate(strings):
        norm = normalize(value)
        if norm == target or norm == target.rstrip(":"):
            if i + 1 < len(strings):
                nxt = strings[i + 1].strip()
                if nxt and len(nxt) < 180:
                    return nxt
        if norm.startswith(target + " "):
            raw = value.split(":", 1)
            if len(raw) == 2 and raw[1].strip():
                return raw[1].strip()
    return None


def current_party_from_open_data(dep_id: int) -> str | None:
    try:
        root = ET.fromstring(get(OPEN_DATA_DETAIL.format(dep_id)).content)
    except Exception:
        return None
    memberships = []
    for node in root.findall(".//c:Militancia", NS):
        party = node.find("c:Partido", NS)
        if party is None:
            continue
        name = party.findtext("c:Nombre", default="", namespaces=NS).strip()
        start = node.findtext("c:FechaInicio", default="", namespaces=NS)
        end = node.findtext("c:FechaTermino", default="", namespaces=NS)
        if name:
            memberships.append((not bool(end), start, name))
    if not memberships:
        return None
    memberships.sort(reverse=True)
    return memberships[0][2]


def candidate_photo(soup: BeautifulSoup, person_name: str, base_url: str) -> str | None:
    person_tokens = normalize(person_name).split()
    first = person_tokens[0] if person_tokens else ""
    last = person_tokens[-2:] if len(person_tokens) >= 2 else person_tokens
    best: tuple[int, str] | None = None
    for img in soup.find_all("img"):
        src = (img.get("src") or "").strip()
        if not src or src.startswith("data:"):
            continue
        alt = normalize(img.get("alt") or "")
        src_norm = normalize(src)
        score = 0
        if "diputad" in alt:
            score += 6
        if first and first in alt:
            score += 3
        score += sum(2 for token in last if token and token in alt)
        if any(term in src_norm for term in ("diput", "parlament", "foto")):
            score += 2
        if any(term in src_norm for term in ("logo", "icon", "banner", "redes", "flecha")):
            score -= 7
        absolute = urljoin(base_url, html.unescape(src))
        if best is None or score > best[0]:
            best = (score, absolute)
    if best and best[0] >= 5:
        return best[1]
    return None


def extract_profile(dep_id: int, fallback_name: str, target_district: int) -> dict:
    url = PROFILE_URL.format(dep_id)
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text("\n", strip=True)

    title_match = re.search(r"Diputad[oa]\s+([^\n]+)", page_text, re.I)
    official_name = title_match.group(1).strip() if title_match else fallback_name

    party = strings_after_label(soup, "Partido:")
    if not party or normalize(party) in {"contacto", "telefono", "email"}:
        party = current_party_from_open_data(dep_id)
    party = party or "Independiente / sin información partidaria"

    district_text = strings_after_label(soup, "Distrito:") or ""
    district_match = re.search(r"(\d+)", district_text)
    district = int(district_match.group(1)) if district_match else target_district

    email_value = None
    mail_links = soup.select('a[href^="mailto:"]')
    if mail_links:
        email_value = mail_links[0].get("href", "").replace("mailto:", "").strip()
    if not email_value:
        emails = re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", response.text, re.I)
        emails = [e for e in emails if "example" not in e.lower()]
        email_value = emails[0] if emails else None

    phone_value = None
    phone_links = soup.select('a[href^="tel:"]')
    if phone_links:
        phone_value = phone_links[0].get("href", "").replace("tel:", "").strip()
    if not phone_value:
        maybe_phone = strings_after_label(soup, "Teléfono") or strings_after_label(soup, "Teléfono:")
        if maybe_phone and any(ch.isdigit() for ch in maybe_phone):
            phone_value = maybe_phone

    photo_url = candidate_photo(soup, official_name, url)
    return {
        "officialName": official_name,
        "party": party,
        "district": district,
        "profileUrl": url,
        "contactUrl": url,
        "email": email_value,
        "phone": phone_value,
        "photoUrl": photo_url,
    }


def save_photo(name: str, photo_url: str | None) -> str | None:
    if not photo_url:
        return None
    try:
        response = get(photo_url, timeout=40, tries=2)
    except Exception as exc:  # noqa: BLE001
        print(f"[foto] {name}: {exc}")
        return None
    content_type = response.headers.get("content-type", "").lower()
    if "image" not in content_type or len(response.content) < 2000:
        print(f"[foto] {name}: respuesta no parece imagen ({content_type}, {len(response.content)} bytes)")
        return None
    ext = ".jpg"
    if "png" in content_type:
        ext = ".png"
    elif "webp" in content_type:
        ext = ".webp"
    filename = f"{slug(name)}{ext}"
    path = PHOTO_DIR / filename
    path.write_bytes(response.content)
    return f"assets/photos/{filename}"


def main() -> None:
    targets = load_targets()
    current = open_data_current()
    matches = match_targets(targets, current)

    if PHOTO_DIR.exists():
        shutil.rmtree(PHOTO_DIR)
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)

    profiles: dict[str, dict] = {}
    failures = []
    photos = 0

    for i, target in enumerate(targets, 1):
        name = target["name"]
        current_row = matches[name]
        try:
            profile = extract_profile(current_row["id"], current_row["name"], target["district"])
        except Exception as exc:  # noqa: BLE001
            print(f"[perfil] {name}: {exc}")
            profile = {
                "officialName": current_row["name"],
                "party": current_party_from_open_data(current_row["id"]) or "Sin información",
                "district": target["district"],
                "profileUrl": PROFILE_URL.format(current_row["id"]),
                "contactUrl": PROFILE_URL.format(current_row["id"]),
                "email": None,
                "phone": None,
                "photoUrl": None,
            }
            failures.append(name)

        local_photo = save_photo(name, profile.pop("photoUrl", None))
        if local_photo:
            photos += 1
        profile["photo"] = local_photo
        profile["id"] = current_row["id"]
        profile["region"] = target["region"]
        profiles[name] = profile
        print(f"[{i:03d}/155] {name} — {profile['party']} — foto={'sí' if local_photo else 'no'}")
        time.sleep(0.05)

    OUT_FILE.write_text(
        "// Generado automáticamente desde fuentes oficiales de la Cámara.\n"
        "window.PROFILES = " + json.dumps(profiles, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    print(f"Perfiles: {len(profiles)} | Fotos locales: {photos} | Errores de ficha: {len(failures)}")
    if len(profiles) != 155:
        raise RuntimeError("La salida no contiene los 155 perfiles esperados")


if __name__ == "__main__":
    main()
