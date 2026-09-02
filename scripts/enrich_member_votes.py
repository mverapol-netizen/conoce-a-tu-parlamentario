from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
AFF = OUT / "affiliations"
MEMBER_VOTES = OUT / "member_votes.csv"
ROLLCALLS = OUT / "rollcalls.csv"
HISTORY = AFF / "affiliation_history.csv"
DETECTED_EVENTS = AFF / "affiliation_detected_events.csv"
OUTPUT = OUT / "member_votes_enriched.csv"
DIAGNOSTICS = OUT / "member_votes_enriched_diagnostics.json"
EXPECTED_MEMBERS_PER_ROLLCALL = 155

FIELDS = [
    "vote_id", "fecha", "boletin", "diputado_id", "diputado_nombre", "opcion", "opcion_codigo",
    "party_at_vote", "caucus_at_vote", "alignment_at_vote",
    "party_confidence", "caucus_confidence", "affiliation_confidence",
    "party_basis", "caucus_basis", "affiliation_interval_from", "affiliation_interval_to",
    "affiliation_uncertain", "uncertain_fields", "uncertainty_window_start", "uncertainty_window_end",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_day(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def in_interval(day, row: dict) -> bool:
    start = parse_day(row["valid_from"])
    end = parse_day(row["valid_to"]) if row.get("valid_to") else None
    return day >= start and (end is None or day <= end)


def uncertainty_for(day, deputy_id: str, detected_by_id: dict[str, list[dict]]) -> dict:
    matches = []
    for event in detected_by_id.get(deputy_id, []):
        if not event.get("window_start") or not event.get("window_end"):
            continue
        if parse_day(event["window_start"]) <= day <= parse_day(event["window_end"]):
            matches.append(event)
    if not matches:
        return {
            "affiliation_uncertain": "0",
            "uncertain_fields": "",
            "uncertainty_window_start": "",
            "uncertainty_window_end": "",
        }

    fields = set()
    starts = []
    ends = []
    for event in matches:
        if event.get("party_before") or event.get("party_after"):
            fields.add("party")
        if event.get("caucus_before") or event.get("caucus_after"):
            fields.add("caucus")
        starts.append(event["window_start"])
        ends.append(event["window_end"])
    return {
        "affiliation_uncertain": "1",
        "uncertain_fields": ";".join(sorted(fields)),
        "uncertainty_window_start": min(starts),
        "uncertainty_window_end": max(ends),
    }


def main() -> None:
    member_votes = read_csv(MEMBER_VOTES)
    rollcalls = read_csv(ROLLCALLS)
    history = read_csv(HISTORY)
    detected = read_csv(DETECTED_EVENTS) if DETECTED_EVENTS.exists() else []

    rollcall_by_id = {x["vote_id"]: x for x in rollcalls}
    if len(rollcall_by_id) != len(rollcalls):
        raise RuntimeError("rollcalls.csv contiene vote_id duplicados")

    input_keys = [(x["vote_id"], x["diputado_id"]) for x in member_votes]
    if len(set(input_keys)) != len(input_keys):
        raise RuntimeError("member_votes.csv contiene pares vote_id × diputado_id duplicados")

    input_counts = Counter(x["vote_id"] for x in member_votes)
    bad_input_rollcalls = {vote_id: n for vote_id, n in input_counts.items() if n != EXPECTED_MEMBERS_PER_ROLLCALL}
    if bad_input_rollcalls:
        raise RuntimeError(f"La matriz nominal de entrada no tiene 155 filas en todos los roll calls: {bad_input_rollcalls}")

    history_by_id: dict[str, list[dict]] = defaultdict(list)
    for row in history:
        history_by_id[row["deputy_id"]].append(row)
    for rows in history_by_id.values():
        rows.sort(key=lambda x: x["valid_from"])
    if len(history_by_id) != 155:
        raise RuntimeError(f"El historial temporal no cubre 155 diputados: {len(history_by_id)}")

    detected_by_id: dict[str, list[dict]] = defaultdict(list)
    for row in detected:
        detected_by_id[row["deputy_id"]].append(row)

    enriched = []
    missing_rollcalls = []
    missing_history = []
    ambiguous_history = []

    for vote in member_votes:
        vote_id = vote["vote_id"]
        deputy_id = vote["diputado_id"]
        rollcall = rollcall_by_id.get(vote_id)
        if not rollcall or not rollcall.get("fecha"):
            missing_rollcalls.append({"vote_id": vote_id, "diputado_id": deputy_id})
            continue
        day = parse_day(rollcall["fecha"])
        matches = [row for row in history_by_id.get(deputy_id, []) if in_interval(day, row)]
        if not matches:
            missing_history.append({"vote_id": vote_id, "fecha": rollcall["fecha"], "diputado_id": deputy_id})
            continue
        if len(matches) != 1:
            ambiguous_history.append({
                "vote_id": vote_id,
                "fecha": rollcall["fecha"],
                "diputado_id": deputy_id,
                "intervals": [f"{x['valid_from']}..{x.get('valid_to', '')}" for x in matches],
            })
            continue

        aff = matches[0]
        uncertain = uncertainty_for(day, deputy_id, detected_by_id)
        enriched.append({
            "vote_id": vote_id,
            "fecha": rollcall["fecha"],
            "boletin": rollcall.get("boletin", ""),
            "diputado_id": deputy_id,
            "diputado_nombre": vote.get("diputado_nombre", ""),
            "opcion": vote.get("opcion", ""),
            "opcion_codigo": vote.get("opcion_codigo", ""),
            "party_at_vote": aff.get("party", ""),
            "caucus_at_vote": aff.get("caucus", ""),
            "alignment_at_vote": aff.get("alignment", ""),
            "party_confidence": aff.get("party_confidence", ""),
            "caucus_confidence": aff.get("caucus_confidence", ""),
            "affiliation_confidence": aff.get("confidence", ""),
            "party_basis": aff.get("party_basis", ""),
            "caucus_basis": aff.get("caucus_basis", ""),
            "affiliation_interval_from": aff.get("valid_from", ""),
            "affiliation_interval_to": aff.get("valid_to", ""),
            **uncertain,
        })

    enriched.sort(key=lambda x: (
        x["fecha"],
        int(x["vote_id"]) if x["vote_id"].isdigit() else x["vote_id"],
        int(x["diputado_id"]),
    ))
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(enriched)

    enriched_counts = Counter(x["vote_id"] for x in enriched)
    bad_enriched_rollcalls = {
        vote_id: n for vote_id, n in enriched_counts.items() if n != EXPECTED_MEMBERS_PER_ROLLCALL
    }
    provisional_rows = sum(
        x["party_confidence"] == "provisional" or x["caucus_confidence"] == "provisional"
        for x in enriched
    )

    diagnostics = {
        "member_vote_rows_input": len(member_votes),
        "member_vote_rows_enriched": len(enriched),
        "rollcalls": len(rollcalls),
        "rollcalls_with_155_input_rows": sum(n == EXPECTED_MEMBERS_PER_ROLLCALL for n in input_counts.values()),
        "rollcalls_with_155_enriched_rows": sum(n == EXPECTED_MEMBERS_PER_ROLLCALL for n in enriched_counts.values()),
        "deputies_in_history": len(history_by_id),
        "missing_rollcall_rows": len(missing_rollcalls),
        "missing_history_rows": len(missing_history),
        "ambiguous_history_rows": len(ambiguous_history),
        "provisional_affiliation_rows": provisional_rows,
        "uncertain_affiliation_rows": sum(x["affiliation_uncertain"] == "1" for x in enriched),
        "party_confidence_counts": dict(Counter(x["party_confidence"] for x in enriched)),
        "caucus_confidence_counts": dict(Counter(x["caucus_confidence"] for x in enriched)),
        "overall_affiliation_confidence_counts": dict(Counter(x["affiliation_confidence"] for x in enriched)),
        "vote_option_counts": dict(Counter(x["opcion"] for x in enriched)),
        "errors": {
            "bad_input_rollcalls": bad_input_rollcalls,
            "bad_enriched_rollcalls": bad_enriched_rollcalls,
            "missing_rollcall_examples": missing_rollcalls[:20],
            "missing_history_examples": missing_history[:20],
            "ambiguous_history_examples": ambiguous_history[:20],
        },
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in diagnostics.items() if k != "errors"}, ensure_ascii=False, indent=2))

    if missing_rollcalls or missing_history or ambiguous_history:
        raise RuntimeError(
            "La unión temporal no es 1:1 para todas las filas: "
            f"missing_rollcall={len(missing_rollcalls)}, missing_history={len(missing_history)}, "
            f"ambiguous={len(ambiguous_history)}"
        )
    if len(enriched) != len(member_votes):
        raise RuntimeError(f"Cobertura incompleta: {len(enriched)}/{len(member_votes)}")
    if bad_enriched_rollcalls:
        raise RuntimeError(f"La matriz enriquecida no conserva 155 filas por roll call: {bad_enriched_rollcalls}")
    if provisional_rows:
        raise RuntimeError(f"La matriz enriquecida contiene {provisional_rows} filas con afiliación provisional")


if __name__ == "__main__":
    main()
