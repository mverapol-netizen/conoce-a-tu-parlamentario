from __future__ import annotations

import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PROFILES_FILE = ROOT / "assets/js/profiles.js"
PREFIX = "// Generado automáticamente desde fuentes oficiales de la Cámara.\nwindow.PROFILES = "

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "Chrome/130 Safari/537.36 conoce-a-tu-parlamentario/contacts-1.0"
        ),
        "Accept-Language": "es-CL,es;q=0.9,en;q=0.7",
    }
)


def decode_cfemail(encoded: str) -> str | None:
    """Decodifica el formato estándar de Cloudflare Email Protection."""
    encoded = (encoded or "").strip()
    if len(encoded) < 4 or len(encoded) % 2:
        return None
    try:
        key = int(encoded[:2], 16)
        chars = [chr(int(encoded[i : i + 2], 16) ^ key) for i in range(2, len(encoded), 2)]
        value = "".join(chars).strip()
    except (ValueError, UnicodeError):
        return None
    return value if "@" in value else None


def clean_email(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().replace("mailto:", "").split("?", 1)[0].strip()
    if re.fullmatch(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", value, re.I):
        return value
    return None


def extract_email(soup: BeautifulSoup, raw_html: str) -> str | None:
    # 1) mailto visible.
    for link in soup.select('a[href^="mailto:"]'):
        value = clean_email(link.get("href"))
        if value:
            return value

    # 2) Cloudflare: data-cfemail.
    for node in soup.select("[data-cfemail]"):
        value = decode_cfemail(node.get("data-cfemail", ""))
        if value:
            return value

    # 3) Cloudflare: /cdn-cgi/l/email-protection#<hex>.
    for link in soup.select('a[href*="/cdn-cgi/l/email-protection"]'):
        href = link.get("href", "")
        if "#" in href:
            value = decode_cfemail(href.rsplit("#", 1)[-1])
            if value:
                return value

    # 4) Texto sin protección, por si el sitio cambia.
    emails = re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", raw_html, re.I)
    for value in emails:
        if "example" not in value.lower():
            return value
    return None


def extract_phone(soup: BeautifulSoup) -> str | None:
    for link in soup.select('a[href^="tel:"]'):
        value = link.get("href", "").replace("tel:", "").strip()
        if any(ch.isdigit() for ch in value):
            return value
    return None


def load_profiles() -> dict[str, dict]:
    source = PROFILES_FILE.read_text(encoding="utf-8")
    if not source.startswith(PREFIX) or not source.rstrip().endswith(";"):
        raise RuntimeError("Formato inesperado en assets/js/profiles.js")
    payload = source[len(PREFIX) :].rstrip()
    payload = payload[:-1]
    profiles = json.loads(payload)
    if len(profiles) != 155:
        raise RuntimeError(f"Se esperaban 155 perfiles; se encontraron {len(profiles)}")
    return profiles


def save_profiles(profiles: dict[str, dict]) -> None:
    PROFILES_FILE.write_text(
        PREFIX + json.dumps(profiles, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    profiles = load_profiles()
    emails = 0
    phones = 0
    failures = 0

    for index, (name, profile) in enumerate(profiles.items(), 1):
        url = profile.get("profileUrl") or profile.get("contactUrl")
        if not url:
            failures += 1
            continue
        try:
            response = SESSION.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            email = extract_email(soup, response.text)
            phone = extract_phone(soup)
            if email:
                profile["email"] = email
                emails += 1
            if phone:
                profile["phone"] = phone
                phones += 1
            print(
                f"[{index:03d}/155] {name} — "
                f"email={'sí' if email else 'no'} — teléfono={'sí' if phone else 'no'}"
            )
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"[contacto] {name}: {exc}")
        time.sleep(0.03)

    save_profiles(profiles)
    print(f"Contactos: emails={emails} | teléfonos={phones} | errores={failures}")


if __name__ == "__main__":
    main()
