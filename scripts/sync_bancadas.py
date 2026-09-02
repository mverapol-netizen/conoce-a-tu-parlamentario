from __future__ import annotations

import json
import re
import time
import unicodedata
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PROFILES_FILE = ROOT / "assets/js/profiles.js"
PREFIX = "// Generado automáticamente desde fuentes oficiales de la Cámara.\nwindow.PROFILES = "

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 conoce-a-tu-parlamentario/bancadas-1.0",
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.7",
})


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", value.lower()).strip()


def load_profiles() -> dict[str, dict]:
    source = PROFILES_FILE.read_text(encoding="utf-8")
    if not source.startswith(PREFIX) or not source.rstrip().endswith(";"):
        raise RuntimeError("Formato inesperado en assets/js/profiles.js")
    payload = source[len(PREFIX):].rstrip()[:-1]
    profiles = json.loads(payload)
    if len(profiles) != 155:
        raise RuntimeError(f"Se esperaban 155 perfiles; se encontraron {len(profiles)}")
    return profiles


def save_profiles(profiles: dict[str, dict]) -> None:
    PROFILES_FILE.write_text(
        PREFIX + json.dumps(profiles, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def extract_label(soup: BeautifulSoup, label: str) -> str | None:
    wanted = normalize(label).rstrip(":")
    strings = list(soup.stripped_strings)
    for i, value in enumerate(strings):
        norm = normalize(value)
        if norm == wanted or norm == wanted + ":":
            if i + 1 < len(strings):
                candidate = strings[i + 1].strip()
                if candidate and len(candidate) < 180:
                    return candidate
        if norm.startswith(wanted + ":"):
            candidate = value.split(":", 1)[1].strip()
            if candidate:
                return candidate
    return None


def main() -> None:
    profiles = load_profiles()
    caucuses = 0
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
            caucus = extract_label(soup, "Bancada") or "Por definir"
            profile["caucus"] = caucus
            is_independent = normalize(profile.get("party", "")).startswith("independ")
            profile["independent"] = is_independent
            if is_independent and caucus != "Por definir":
                profile["affiliationLabel"] = f"Independiente en {caucus}"
            elif is_independent:
                profile["affiliationLabel"] = "Independiente · bancada por definir"
            else:
                profile["affiliationLabel"] = profile.get("party") or "Sin información partidaria"
            caucuses += 1
            print(f"[{index:03d}/155] {name} — {caucus}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            profile.setdefault("caucus", "Por definir")
            profile["independent"] = normalize(profile.get("party", "")).startswith("independ")
            print(f"[bancada] {name}: {exc}")
        time.sleep(0.03)

    save_profiles(profiles)
    print(f"Bancadas: {caucuses}/155 | errores={failures}")
    if caucuses < 150:
        raise RuntimeError("Demasiadas fichas sin bancada; no se actualiza silenciosamente")


if __name__ == "__main__":
    main()
