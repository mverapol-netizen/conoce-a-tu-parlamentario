from __future__ import annotations

import csv
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "assets" / "js" / "profiles.js"
OUT = ROOT / "data" / "legislative" / "2026" / "affiliations"
ELECTORAL = OUT / "election_baseline_2025.csv"
VERIFIED = OUT / "party_term_start_verified.csv"
BASELINE = OUT / "party_term_start_baseline.csv"
DIAGNOSTICS = OUT / "party_term_start_baseline_diagnostics.json"
TERM_START = "2026-03-11"

FIELDS = [
    "deputy_id", "deputy_name", "term_start", "party_at_term_start",
    "electoral_party_slot", "electoral_pact", "basis", "confidence",
    "source_url_primary", "source_url_secondary", "source_note", "frozen_on",
]

ALIASES = {
    "evolucion politica": "evopoli",
    "federacion regionalista verde social": "frvs",
    "frente amplio": "frente amplio",
    "independientes": "independiente",
    "independiente": "independiente",
    "partido accion humanista": "accion humanista",
    "partido comunista de chile": "partido comunista",
    "partido comunista": "partido comunista",
    "partido de la gente": "pdg",
    "partido democrata cristiano": "dc",
    "partido democratas chile": "democratas",
    "partido liberal de chile": "liberal",
    "partido nacional libertario": "pnl",
    "partido por la democracia": "ppd",
    "partido radical de chile": "radical",
    "partido republicano de chile": "republicano",
    "partido republicano": "republicano",
    "partido social cristiano": "psc",
    "partido cristiano de chile": "partido cristiano",
    "partido socialista de chile": "ps",
    "partido socialista": "ps",
    "renovacion nacional": "rn",
    "union democrata independiente": "udi",
}


def norm(value: str) -> str:
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text).lower()
    return re.sub(r"\s+", " ", text).strip()


def canonical(value: str) -> str:
    n = norm(value)
    return ALIASES.get(n, n)


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_profiles() -> dict[str, dict]:
    text = PROFILES.read_text(encoding="utf-8")
    match = re.search(r"window\.PROFILES\s*=\s*(\{.*\})\s*;\s*$", text, re.S)
    if not match:
        raise RuntimeError("No se pudo leer window.PROFILES")
    data = json.loads(match.group(1))
    return {str(v.get("id")): {"name": v.get("officialName") or k, **v} for k, v in data.items()}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    electoral = {x["deputy_id"]: x for x in read_csv(ELECTORAL)}
    verified = {x["deputy_id"]: x for x in read_csv(VERIFIED)}
    existing = {x["deputy_id"]: x for x in read_csv(BASELINE)}
    profiles = load_profiles()

    if len(electoral) != 155 or len(profiles) != 155:
        raise RuntimeError(f"Cobertura inválida: electoral={len(electoral)}, profiles={len(profiles)}")

    rows = []
    frozen_new = 0
    upgraded_verified = 0
    for deputy_id in sorted(profiles, key=int):
        profile = profiles[deputy_id]
        election = electoral[deputy_id]
        direct = verified.get(deputy_id)
        old = existing.get(deputy_id)

        if direct:
            row = {
                "deputy_id": deputy_id,
                "deputy_name": profile["name"],
                "term_start": TERM_START,
                "party_at_term_start": direct["party_at_term_start"],
                "electoral_party_slot": election.get("electoral_party", ""),
                "electoral_pact": election.get("electoral_pact", ""),
                "basis": direct.get("source_type") or "historical_direct_verification",
                "confidence": direct.get("confidence") or "high",
                "source_url_primary": direct.get("source_url", ""),
                "source_url_secondary": election.get("source_url", ""),
                "source_note": direct.get("note", ""),
                "frozen_on": old.get("frozen_on") if old else date.today().isoformat(),
            }
            if old and old.get("confidence") != "high":
                upgraded_verified += 1
        elif old:
            # Una vez congelado el estado de marzo, no se recalcula con un snapshot futuro.
            row = dict(old)
            row["deputy_name"] = profile["name"]
            row["electoral_party_slot"] = election.get("electoral_party", row.get("electoral_party_slot", ""))
            row["electoral_pact"] = election.get("electoral_pact", row.get("electoral_pact", ""))
        else:
            slot = election.get("electoral_party", "")
            current = profile.get("party", "")
            if canonical(slot) != canonical(current):
                raise RuntimeError(
                    f"No se puede congelar {profile['name']}: cupo Servel={slot!r}, Cámara actual={current!r}; requiere verificación directa"
                )
            row = {
                "deputy_id": deputy_id,
                "deputy_name": profile["name"],
                "term_start": TERM_START,
                "party_at_term_start": current,
                "electoral_party_slot": slot,
                "electoral_pact": election.get("electoral_pact", ""),
                "basis": "servel_slot_camara_snapshot_concordance",
                "confidence": "medium",
                "source_url_primary": election.get("source_url", ""),
                "source_url_secondary": profile.get("profileUrl", ""),
                "source_note": "Cupo electoral Servel 2025 y partido reportado por la Cámara el 02-09-2026 coinciden. Estado de inicio congelado con confianza media hasta verificación biográfica directa.",
                "frozen_on": date.today().isoformat(),
            }
            frozen_new += 1
        rows.append(row)

    with BASELINE.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    diagnostics = {
        "generated_for": date.today().isoformat(),
        "deputies": len(rows),
        "high_confidence": sum(x["confidence"] == "high" for x in rows),
        "medium_confidence": sum(x["confidence"] == "medium" for x in rows),
        "direct_verified": sum(x["basis"] != "servel_slot_camara_snapshot_concordance" for x in rows),
        "servel_camara_concordance": sum(x["basis"] == "servel_slot_camara_snapshot_concordance" for x in rows),
        "newly_frozen_this_run": frozen_new,
        "upgraded_to_direct_verification": upgraded_verified,
        "term_start": TERM_START,
        "warning": "electoral_party_slot es cupo electoral y no se interpreta como militancia. party_at_term_start es la variable analítica de afiliación partidaria.",
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))

    if len(rows) != 155:
        raise RuntimeError(f"La línea base partidaria no cubre 155 diputados: {len(rows)}")


if __name__ == "__main__":
    main()
