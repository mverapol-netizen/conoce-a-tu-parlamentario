from __future__ import annotations

import json
import re
import time
import unicodedata
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PROFILES_FILE = ROOT / "assets/js/profiles.js"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 conoce-a-tu-parlamentario/2.0",
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.7",
})

# Esta capa es editorial y fechada. Partido y bancada provienen de la Cámara;
# la posición oficialismo/oposición/no alineado se revisa separadamente.
OFFICIALISM = (
    "partido republicano",
    "renovacion nacional",
    "union democrata independiente",
    "evolucion politica",
    "partido democratas chile",
    "democratas chile",
    "partido cristiano",
    "partido social cristiano",
)

OPPOSITION = (
    "frente amplio",
    "partido comunista",
    "comite comunista",
    "partido socialista",
    "socialista liberal radical",
    "partido por la democracia",
    "partido liberal",
    "partido democrata cristiano",
    "democracia cristiana",
    "federacion regionalista verde social",
    "partido accion humanista",
    "partido radical",
)

AUTONOMOUS = (
    "partido de la gente",
    "partido nacional libertario",
)


def normalize(value: str | None) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.lower()
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def load_profiles() -> dict:
    text = PROFILES_FILE.read_text(encoding="utf-8")
    match = re.search(r"window\.PROFILES\s*=\s*(\{.*\})\s*;\s*$", text, re.S)
    if not match:
        raise RuntimeError("No se pudo leer window.PROFILES")
    return json.loads(match.group(1))


def save_profiles(profiles: dict) -> None:
    PROFILES_FILE.write_text(
        "// Generado automáticamente desde fuentes oficiales de la Cámara.\n"
        "window.PROFILES = " + json.dumps(profiles, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def after_label(soup: BeautifulSoup, label: str) -> str | None:
    target = normalize(label)
    values = list(soup.stripped_strings)
    for i, value in enumerate(values):
        norm = normalize(value)
        if norm == target:
            if i + 1 < len(values):
                nxt = values[i + 1].strip()
                if nxt and len(nxt) < 220:
                    return nxt
        if norm.startswith(target + " "):
            parts = value.split(":", 1)
            if len(parts) == 2 and parts[1].strip():
                return parts[1].strip()
    return None


def classify_by_text(value: str | None) -> str | None:
    text = normalize(value)
    if not text:
        return None
    if any(term in text for term in OFFICIALISM):
        return "oficialismo"
    if any(term in text for term in OPPOSITION):
        return "oposicion"
    if any(term in text for term in AUTONOMOUS):
        return "no_alineado"
    return None


def classify(party: str | None, caucus: str | None) -> str:
    party_norm = normalize(party)
    is_independent = party_norm in {"independiente", "independientes", "sin partido"}

    # Para militantes o miembros de un partido, prima la posición pública del partido.
    if not is_independent:
        by_party = classify_by_text(party)
        if by_party:
            return by_party

    # Para independientes, la bancada/comité define su ubicación parlamentaria.
    by_caucus = classify_by_text(caucus)
    if by_caucus:
        return by_caucus

    return "no_alineado"


def affiliation_label(party: str | None, caucus: str | None) -> str:
    party_text = (party or "Sin información partidaria").strip()
    if normalize(party_text) in {"independiente", "independientes", "sin partido"}:
        return f"Independiente en {caucus}" if caucus else "Independiente"
    return party_text


def main() -> None:
    profiles = load_profiles()
    if len(profiles) != 155:
        raise RuntimeError(f"Se esperaban 155 perfiles; hay {len(profiles)}")

    caucuses: dict[str, int] = {}
    alignments: dict[str, int] = {"oficialismo": 0, "oposicion": 0, "no_alineado": 0}
    failures: list[str] = []

    for i, (name, profile) in enumerate(profiles.items(), 1):
        url = profile.get("profileUrl")
        party = profile.get("party")
        caucus = profile.get("caucus")
        if url:
            try:
                response = SESSION.get(url, timeout=25)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                current_party = after_label(soup, "Partido:")
                current_caucus = after_label(soup, "Bancada:")
                if current_party and normalize(current_party) not in {"bancada", "contacto"}:
                    party = current_party
                if current_caucus and normalize(current_caucus) not in {"contacto", "telefono", "email"}:
                    caucus = current_caucus
            except Exception as exc:  # noqa: BLE001
                print(f"[politica] {name}: {exc}")
                failures.append(name)

        alignment = classify(party, caucus)
        profile["party"] = party or "Sin información"
        profile["caucus"] = caucus or "Bancada por confirmar"
        profile["alignment"] = alignment
        profile["affiliationLabel"] = affiliation_label(profile["party"], profile["caucus"])
        profile["politicalUpdated"] = date.today().isoformat()

        caucuses[profile["caucus"]] = caucuses.get(profile["caucus"], 0) + 1
        alignments[alignment] += 1
        print(
            f"[{i:03d}/155] {name} — {profile['party']} — {profile['caucus']} — {alignment}"
        )
        time.sleep(0.03)

    if sum(alignments.values()) != 155:
        raise RuntimeError(f"La clasificación política no cierra en 155: {alignments}")

    save_profiles(profiles)

    print("\nBancadas/comités:")
    for caucus, n in sorted(caucuses.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {n:>2}  {caucus}")
    print(f"Bloques: {alignments}")
    print(f"Errores: {len(failures)}")


if __name__ == "__main__":
    main()
