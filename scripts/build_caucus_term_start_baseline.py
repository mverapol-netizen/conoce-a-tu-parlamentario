from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026" / "affiliations"
ELECTION = OUT / "election_baseline_2025.csv"
PARTY_BASELINE = OUT / "party_term_start_baseline.csv"
SNAPSHOTS = OUT / "affiliation_snapshots.csv"
MANUAL_EVENTS = OUT / "affiliation_manual_events.csv"
OUTPUT = OUT / "caucus_term_start_baseline.csv"
DIAGNOSTICS = OUT / "caucus_term_start_baseline_diagnostics.json"
TERM_START = "2026-03-11"

SESSION_SOURCE = "https://www.bcn.cl/laborparlamentaria/participacion?idParticipacion=2610607"
CAMARA_TABLE_SOURCE = "https://www.camara.cl/verDoc.aspx?prmid=4771&prmtipo=DOCUMENTOTABLA"

FIELDS = [
    "deputy_id", "deputy_name", "caucus_at_term_start", "basis", "confidence",
    "source_url_primary", "source_url_validation", "source_note",
    "electoral_party_slot", "party_at_term_start", "validation_bucket",
]

# Composición reconstruida para el inicio de la 374a legislatura. Los tamaños de los
# comités que aparecen en Incidentes se obtienen de la distribución proporcional de
# minutos de Sala: 12:00=31, 6:58=18, 6:12=16, 5:48=15, 5:25=14,
# 4:39=12, 3:52=10 y 3:06=8. Los tres PSC no integraban comité parlamentario.
EXPECTED_COUNTS = {
    "Comité Partido Republicano": 31,
    "Frente Amplio": 18,
    "Unión Demócrata Independiente": 18,
    "Renovación Nacional, Evopoli e Independientes": 16,
    "Socialista, Liberal, Radical e Independientes": 15,
    "Comité Partido de la Gente": 14,
    "Comité Comunista e Independientes": 12,
    "Comité Democracia Cristiana, Federación Regionalista Verde Social e Independientes": 10,
    "Partido Por la Democracia e Independientes": 10,
    "Comité Partido Nacional Libertarios": 8,
    "Sin comité parlamentario / por definir": 3,
}

PARTY_TO_CAUCUS = {
    "Partido Republicano": "Comité Partido Republicano",
    "Frente Amplio": "Frente Amplio",
    "Unión Demócrata Independiente": "Unión Demócrata Independiente",
    "Renovación Nacional": "Renovación Nacional, Evopoli e Independientes",
    "Evolución Política": "Renovación Nacional, Evopoli e Independientes",
    "Partido Demócratas Chile": "Renovación Nacional, Evopoli e Independientes",
    "Partido Socialista": "Socialista, Liberal, Radical e Independientes",
    "Partido Liberal de Chile": "Socialista, Liberal, Radical e Independientes",
    "Partido Radical de Chile": "Socialista, Liberal, Radical e Independientes",
    "Partido Por la Democracia": "Partido Por la Democracia e Independientes",
    "Partido Demócrata Cristiano": "Comité Democracia Cristiana, Federación Regionalista Verde Social e Independientes",
    "Federación Regionalista Verde Social": "Comité Democracia Cristiana, Federación Regionalista Verde Social e Independientes",
    "Partido Comunista": "Comité Comunista e Independientes",
    "Partido Acción Humanista": "Comité Comunista e Independientes",
    "Partido de la Gente": "Comité Partido de la Gente",
    "Partido Nacional Libertario": "Comité Partido Nacional Libertarios",
    "Partido Social Cristiano": "Sin comité parlamentario / por definir",
}

SLOT_TO_CAUCUS = {
    "PARTIDO REPUBLICANO DE CHILE": "Comité Partido Republicano",
    "FRENTE AMPLIO": "Frente Amplio",
    "UNION DEMOCRATA INDEPENDIENTE": "Unión Demócrata Independiente",
    "RENOVACION NACIONAL": "Renovación Nacional, Evopoli e Independientes",
    "EVOLUCION POLITICA": "Renovación Nacional, Evopoli e Independientes",
    "PARTIDO DEMOCRATAS CHILE": "Renovación Nacional, Evopoli e Independientes",
    "PARTIDO SOCIALISTA DE CHILE": "Socialista, Liberal, Radical e Independientes",
    "PARTIDO LIBERAL DE CHILE": "Socialista, Liberal, Radical e Independientes",
    "PARTIDO RADICAL DE CHILE": "Socialista, Liberal, Radical e Independientes",
    "PARTIDO POR LA DEMOCRACIA": "Partido Por la Democracia e Independientes",
    "PARTIDO DEMOCRATA CRISTIANO": "Comité Democracia Cristiana, Federación Regionalista Verde Social e Independientes",
    "FEDERACION REGIONALISTA VERDE SOCIAL": "Comité Democracia Cristiana, Federación Regionalista Verde Social e Independientes",
    "PARTIDO COMUNISTA DE CHILE": "Comité Comunista e Independientes",
    "PARTIDO ACCIÓN HUMANISTA": "Comité Comunista e Independientes",
    "PARTIDO DE LA GENTE": "Comité Partido de la Gente",
    "PARTIDO NACIONAL LIBERTARIO": "Comité Partido Nacional Libertarios",
    "PARTIDO SOCIAL CRISTIANO": "Sin comité parlamentario / por definir",
}

# Único electo estrictamente como independiente en Servel. Su pertenencia actual al
# comité PPD+Ind y el cierre exacto de tamaños institucionales permiten reconstruirlo.
SPECIAL_CAUCUS = {
    "1172": "Partido Por la Democracia e Independientes",  # se reemplaza dinámicamente si el ID no corresponde
}


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def latest_snapshot(rows: list[dict]) -> dict[str, dict]:
    latest = max(x["observed_date"] for x in rows)
    return {x["deputy_id"]: x for x in rows if x["observed_date"] == latest}


def first_events(rows: list[dict]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for row in sorted(rows, key=lambda x: x.get("effective_date", "")):
        if row.get("deputy_id") and row.get("effective_date", "") >= TERM_START:
            result.setdefault(row["deputy_id"], row)
    return result


def main() -> None:
    election = {x["deputy_id"]: x for x in read_csv(ELECTION)}
    party = {x["deputy_id"]: x for x in read_csv(PARTY_BASELINE)}
    current = latest_snapshot(read_csv(SNAPSHOTS))
    events = first_events(read_csv(MANUAL_EVENTS))

    if not (len(election) == len(party) == len(current) == 155):
        raise RuntimeError(f"Cobertura insuficiente: election={len(election)} party={len(party)} current={len(current)}")

    rows = []
    unresolved = []
    for deputy_id in sorted(party, key=int):
        p = party[deputy_id]
        e = election[deputy_id]
        cur = current[deputy_id]
        name = p.get("deputy_name") or cur.get("deputy_name", "")
        party_start = p.get("party_at_term_start", "")
        slot = e.get("electoral_party", "")

        caucus = ""
        basis = ""
        confidence = "medium"
        note = ""

        # Un evento documentado durante 2026 puede revelar directamente la bancada previa.
        first = events.get(deputy_id)
        if first and first.get("caucus_before"):
            caucus = first["caucus_before"]
            basis = "documented_pre_event_state"
            confidence = first.get("confidence") or "high"
            note = "Bancada inicial reconstruida directamente desde el estado previo al primer cambio documentado del período."
        elif party_start != "Independientes" and party_start in PARTY_TO_CAUCUS:
            caucus = PARTY_TO_CAUCUS[party_start]
            basis = "party_to_caucus_plus_official_structure"
            confidence = "high"
            note = "Partido de inicio determina el comité; estructura y tamaño validados con documentos de Sala de marzo de 2026."
        elif party_start == "Independientes" and slot in SLOT_TO_CAUCUS:
            caucus = SLOT_TO_CAUCUS[slot]
            basis = "independent_electoral_slot_plus_current_caucus_plus_size_closure"
            confidence = "medium"
            note = "Independiente: cupo electoral, bancada actual y cierre exacto de tamaños institucionales apuntan al mismo comité inicial."
        elif slot == "INDEPENDIENTES":
            # Carlos Bianchi: el único electo sin cupo partidario. En el snapshot oficial actual integra PPD+Ind;
            # esa asignación es además necesaria para reproducir el tamaño oficial de 10 integrantes en marzo.
            if cur.get("caucus_reported") == "Partido Por la Democracia e Independientes":
                caucus = "Partido Por la Democracia e Independientes"
                basis = "current_caucus_plus_official_size_closure"
                confidence = "medium"
                note = "Electo independiente sin cupo partidario; bancada actual y tamaño oficial de marzo reproducen PPD+Ind=10."
        
        if not caucus:
            unresolved.append({"deputy_id": deputy_id, "deputy_name": name, "party": party_start, "slot": slot})
            continue

        rows.append({
            "deputy_id": deputy_id,
            "deputy_name": name,
            "caucus_at_term_start": caucus,
            "basis": basis,
            "confidence": confidence,
            "source_url_primary": first.get("source_url", "") if first and first.get("caucus_before") else SESSION_SOURCE,
            "source_url_validation": CAMARA_TABLE_SOURCE,
            "source_note": note,
            "electoral_party_slot": slot,
            "party_at_term_start": party_start,
            "validation_bucket": "documented_event" if basis == "documented_pre_event_state" else "institutional_reconstruction",
        })

    counts = Counter(x["caucus_at_term_start"] for x in rows)
    mismatches = {
        caucus: {"expected": expected, "observed": counts.get(caucus, 0)}
        for caucus, expected in EXPECTED_COUNTS.items()
        if counts.get(caucus, 0) != expected
    }
    extras = {k: v for k, v in counts.items() if k not in EXPECTED_COUNTS}

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    diagnostics = {
        "term_start": TERM_START,
        "deputies": len(rows),
        "high_confidence": sum(x["confidence"] == "high" for x in rows),
        "medium_confidence": sum(x["confidence"] == "medium" for x in rows),
        "unresolved": unresolved,
        "caucus_counts": dict(counts),
        "expected_counts": EXPECTED_COUNTS,
        "count_mismatches": mismatches,
        "unexpected_caucuses": extras,
        "method": "Reconstrucción por partido/cupo electoral, estados previos documentados y cierre con tamaños oficiales de comités de marzo de 2026. PSC se conserva como sin comité/por definir, no se fuerza a una bancada inexistente.",
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))

    if unresolved or len(rows) != 155 or mismatches or extras:
        raise RuntimeError(
            f"Línea base de bancadas no cierra: rows={len(rows)} unresolved={len(unresolved)} mismatches={mismatches} extras={extras}"
        )


if __name__ == "__main__":
    main()
