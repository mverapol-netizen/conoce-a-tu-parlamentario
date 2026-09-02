from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "assets" / "js" / "profiles.js"
AFF = ROOT / "data" / "legislative" / "2026" / "affiliations"
BASELINE = AFF / "election_baseline_2025.csv"
EVENTS = AFF / "affiliation_manual_events.csv"
OUT = AFF / "party_baseline_audit.csv"
DIAGNOSTICS = AFF / "party_baseline_audit_diagnostics.json"

FIELDS = [
    "deputy_id", "deputy_name", "district", "electoral_party_slot", "electoral_pact",
    "current_party_camara", "current_caucus_camara", "comparison_status",
    "has_documented_2026_event", "event_dates", "baseline_action", "review_priority",
]


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", str(value or ""))
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


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
    baseline = read_csv(BASELINE)
    profiles = load_profiles()
    events = read_csv(EVENTS)
    event_dates: dict[str, list[str]] = {}
    for event in events:
        event_dates.setdefault(event.get("deputy_id", ""), []).append(event.get("effective_date", ""))

    if len(baseline) != 155 or len(profiles) != 155:
        raise RuntimeError(f"Cobertura inválida: baseline={len(baseline)}, profiles={len(profiles)}")

    rows = []
    for electoral in baseline:
        deputy_id = electoral["deputy_id"]
        profile = profiles.get(deputy_id)
        if not profile:
            raise RuntimeError(f"No existe perfil para ID {deputy_id}")
        slot = electoral.get("electoral_party", "")
        current = profile.get("party", "")
        has_event = bool(event_dates.get(deputy_id))

        if canonical(slot) == canonical(current):
            status = "slot_coincide_partido_actual"
            action = "validar_partido_desde_inicio_sujeto_a_estatus_juridico"
            priority = "baja"
        elif canonical(current) == "independiente" and canonical(slot) != "independiente":
            status = "actual_independiente_en_cupo_partidario"
            action = "verificar_independencia_en_eleccion_o_fecha_de_salida"
            priority = "alta"
        elif canonical(slot) == "independiente" and canonical(current) != "independiente":
            status = "electo_independiente_hoy_partidario"
            action = "buscar_fecha_de_afiliacion"
            priority = "alta"
        else:
            status = "cambio_de_etiqueta_o_partido"
            action = "reconstruir_transicion"
            priority = "media" if has_event else "alta"

        rows.append({
            "deputy_id": deputy_id,
            "deputy_name": electoral.get("deputy_name", ""),
            "district": electoral.get("district", ""),
            "electoral_party_slot": slot,
            "electoral_pact": electoral.get("electoral_pact", ""),
            "current_party_camara": current,
            "current_caucus_camara": profile.get("caucus", ""),
            "comparison_status": status,
            "has_documented_2026_event": "1" if has_event else "0",
            "event_dates": " | ".join(sorted(event_dates.get(deputy_id, []))),
            "baseline_action": action,
            "review_priority": priority,
        })

    rows.sort(key=lambda x: (0 if x["review_priority"] == "alta" else 1 if x["review_priority"] == "media" else 2, int(x["deputy_id"])))
    with OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    diagnostics = {
        "deputies": len(rows),
        "status_counts": dict(Counter(x["comparison_status"] for x in rows)),
        "priority_counts": dict(Counter(x["review_priority"] for x in rows)),
        "high_priority_cases": [
            {
                "deputy_id": x["deputy_id"],
                "deputy_name": x["deputy_name"],
                "district": x["district"],
                "electoral_party_slot": x["electoral_party_slot"],
                "current_party_camara": x["current_party_camara"],
                "has_documented_2026_event": x["has_documented_2026_event"],
            }
            for x in rows if x["review_priority"] == "alta"
        ],
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
