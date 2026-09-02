from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

from sync_political import classify

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "assets" / "js" / "profiles.js"
OUT = ROOT / "data" / "legislative" / "2026" / "affiliations"
SNAPSHOTS = OUT / "affiliation_snapshots.csv"
MANUAL_EVENTS = OUT / "affiliation_manual_events.csv"
DETECTED_EVENTS = OUT / "affiliation_detected_events.csv"
PARTY_BASELINE = OUT / "party_term_start_baseline.csv"
CAUCUS_BASELINE = OUT / "caucus_term_start_baseline.csv"
HISTORY = OUT / "affiliation_history.csv"
DIAGNOSTICS = OUT / "affiliation_diagnostics.json"
TERM_START = date(2026, 3, 11)

SNAPSHOT_FIELDS = [
    "observed_date", "deputy_id", "deputy_name", "party_reported", "caucus_reported",
    "alignment_reported", "profile_url", "source_type",
]

DETECTED_FIELDS = [
    "effective_date", "window_start", "window_end", "deputy_id", "deputy_name",
    "party_before", "party_after", "caucus_before", "caucus_after", "source_url",
    "source_type", "confidence", "date_precision", "note",
]

HISTORY_FIELDS = [
    "deputy_id", "deputy_name", "valid_from", "valid_to", "party", "caucus", "alignment",
    "party_basis", "party_confidence", "party_source_url", "party_source_note",
    "caucus_basis", "caucus_confidence", "caucus_source_url", "caucus_source_note",
    "electoral_party_slot", "electoral_pact",
    "basis", "confidence", "date_precision", "source_url", "source_note",
    "official_snapshot_conflict",
]

CONFIDENCE_ORDER = {"provisional": 0, "low": 1, "medium": 2, "high": 3}


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_profiles() -> dict:
    text = PROFILES.read_text(encoding="utf-8")
    match = re.search(r"window\.PROFILES\s*=\s*(\{.*\})\s*;\s*$", text, re.S)
    if not match:
        raise RuntimeError("No se pudo leer window.PROFILES")
    return json.loads(match.group(1))


def parse_day(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def snapshot_date(profiles: dict) -> date:
    dates = []
    for profile in profiles.values():
        value = str(profile.get("politicalUpdated") or "").strip()
        if value:
            try:
                dates.append(parse_day(value))
            except ValueError:
                pass
    return max(dates) if dates else date.today()


def current_snapshot_rows(profiles: dict, observed: date) -> list[dict]:
    rows = []
    for name, profile in profiles.items():
        deputy_id = str(profile.get("id") or "").strip()
        if not deputy_id:
            raise RuntimeError(f"Perfil sin ID: {name}")
        rows.append({
            "observed_date": observed.isoformat(),
            "deputy_id": deputy_id,
            "deputy_name": profile.get("officialName") or name,
            "party_reported": profile.get("party") or "Sin información",
            "caucus_reported": profile.get("caucus") or "Bancada por confirmar",
            "alignment_reported": profile.get("alignment") or classify(profile.get("party"), profile.get("caucus")),
            "profile_url": profile.get("profileUrl") or "",
            "source_type": "camara_snapshot",
        })
    rows.sort(key=lambda x: int(x["deputy_id"]))
    return rows


def persist_snapshot(rows: list[dict], observed: date) -> list[dict]:
    old = read_csv(SNAPSHOTS)
    kept = [row for row in old if row.get("observed_date") != observed.isoformat()]
    merged = kept + rows
    merged.sort(key=lambda x: (x["observed_date"], int(x["deputy_id"])))
    write_csv(SNAPSHOTS, merged, SNAPSHOT_FIELDS)
    return merged


def manual_event_covers_change(manual: list[dict], deputy_id: str, start: date, end: date,
                               field: str, before: str, after: str) -> bool:
    before_key = f"{field}_before"
    after_key = f"{field}_after"
    for event in manual:
        if event.get("deputy_id") != deputy_id or not event.get("effective_date"):
            continue
        day = parse_day(event["effective_date"])
        if not (start < day <= end):
            continue
        event_after = event.get(after_key, "")
        event_before = event.get(before_key, "")
        if event_after == after and (not event_before or event_before == before):
            return True
    return False


def derive_detected_events(snapshots: list[dict], manual: list[dict]) -> list[dict]:
    by_id: dict[str, list[dict]] = defaultdict(list)
    for row in snapshots:
        by_id[row["deputy_id"]].append(row)

    detected = []
    for deputy_id, rows in by_id.items():
        rows.sort(key=lambda x: x["observed_date"])
        for previous, current in zip(rows, rows[1:]):
            previous_day = parse_day(previous["observed_date"])
            current_day = parse_day(current["observed_date"])
            party_changed = previous.get("party_reported", "") != current.get("party_reported", "")
            caucus_changed = previous.get("caucus_reported", "") != current.get("caucus_reported", "")

            party_unexplained = party_changed and not manual_event_covers_change(
                manual, deputy_id, previous_day, current_day, "party",
                previous.get("party_reported", ""), current.get("party_reported", ""),
            )
            caucus_unexplained = caucus_changed and not manual_event_covers_change(
                manual, deputy_id, previous_day, current_day, "caucus",
                previous.get("caucus_reported", ""), current.get("caucus_reported", ""),
            )
            if not party_unexplained and not caucus_unexplained:
                continue

            window_start = previous_day + timedelta(days=1)
            note_bits = [
                f"Cambio detectado entre snapshots de Cámara {previous_day.isoformat()} y {current_day.isoformat()}; fecha exacta pendiente de corroboración."
            ]
            if party_unexplained:
                note_bits.append(
                    f"Partido: {previous.get('party_reported', '')} → {current.get('party_reported', '')}."
                )
            if caucus_unexplained:
                note_bits.append(
                    f"Bancada: {previous.get('caucus_reported', '')} → {current.get('caucus_reported', '')}."
                )
            detected.append({
                "effective_date": current_day.isoformat(),
                "window_start": window_start.isoformat(),
                "window_end": current_day.isoformat(),
                "deputy_id": deputy_id,
                "deputy_name": current.get("deputy_name", ""),
                "party_before": previous.get("party_reported", "") if party_unexplained else "",
                "party_after": current.get("party_reported", "") if party_unexplained else "",
                "caucus_before": previous.get("caucus_reported", "") if caucus_unexplained else "",
                "caucus_after": current.get("caucus_reported", "") if caucus_unexplained else "",
                "source_url": current.get("profile_url", ""),
                "source_type": "camara_weekly_snapshot_change",
                "confidence": "medium",
                "date_precision": "observation_window",
                "note": " ".join(note_bits),
            })

    detected.sort(key=lambda x: (x["effective_date"], int(x["deputy_id"])))
    write_csv(DETECTED_EVENTS, detected, DETECTED_FIELDS)
    return detected


def event_rows(manual: list[dict], detected: list[dict]) -> list[dict]:
    combined = []
    for row in manual:
        out = dict(row)
        out.setdefault("window_start", row.get("effective_date", ""))
        out.setdefault("window_end", row.get("effective_date", ""))
        combined.append(out)
    combined.extend(detected)
    combined.sort(key=lambda x: (x.get("effective_date", ""), 0 if x.get("source_type") != "camara_weekly_snapshot_change" else 1))
    return combined


def latest_snapshot(snapshots: list[dict]) -> tuple[date, dict[str, dict]]:
    latest_date = max(parse_day(x["observed_date"]) for x in snapshots)
    latest_by_id = {
        row["deputy_id"]: row
        for row in snapshots
        if parse_day(row["observed_date"]) == latest_date
    }
    return latest_date, latest_by_id


def weakest_confidence(party_conf: str, caucus_conf: str) -> str:
    return min((party_conf or "provisional", caucus_conf or "provisional"), key=lambda x: CONFIDENCE_ORDER.get(x, -1))


def state_note(state: dict) -> str:
    return f"Partido: {state.get('party_note', '')} | Bancada: {state.get('caucus_note', '')}".strip()


def make_interval(deputy_id: str, name: str, start: date, end: date | None, state: dict,
                  electoral: dict, conflict: str = "0") -> dict:
    party_basis = state.get("party_basis", "")
    caucus_basis = state.get("caucus_basis", "")
    party_conf = state.get("party_confidence", "provisional")
    caucus_conf = state.get("caucus_confidence", "provisional")
    basis = party_basis if party_basis == caucus_basis else f"party:{party_basis}|caucus:{caucus_basis}"
    confidence = weakest_confidence(party_conf, caucus_conf)
    precision = state.get("date_precision", "")
    source_url = state.get("party_source_url") or state.get("caucus_source_url") or ""
    return {
        "deputy_id": deputy_id,
        "deputy_name": name,
        "valid_from": start.isoformat(),
        "valid_to": end.isoformat() if end else "",
        "party": state.get("party") or "Sin información",
        "caucus": state.get("caucus") or "Bancada por confirmar",
        "alignment": classify(state.get("party"), state.get("caucus")),
        "party_basis": party_basis,
        "party_confidence": party_conf,
        "party_source_url": state.get("party_source_url", ""),
        "party_source_note": state.get("party_note", ""),
        "caucus_basis": caucus_basis,
        "caucus_confidence": caucus_conf,
        "caucus_source_url": state.get("caucus_source_url", ""),
        "caucus_source_note": state.get("caucus_note", ""),
        "electoral_party_slot": electoral.get("electoral_party_slot", ""),
        "electoral_pact": electoral.get("electoral_pact", ""),
        "basis": basis,
        "confidence": confidence,
        "date_precision": precision,
        "source_url": source_url,
        "source_note": state_note(state),
        "official_snapshot_conflict": conflict,
    }


def initial_state(deputy_id: str, party_baseline: dict, caucus_baseline: dict,
                  first_event: dict | None) -> dict:
    party = party_baseline.get("party_at_term_start", "")
    caucus = caucus_baseline.get("caucus_at_term_start", "")
    if not party:
        raise RuntimeError(f"Falta partido de inicio para diputado {deputy_id}")
    if not caucus:
        raise RuntimeError(f"Falta bancada de inicio para diputado {deputy_id}")

    state = {
        "party": party,
        "party_basis": party_baseline.get("basis", "party_term_start_baseline"),
        "party_confidence": party_baseline.get("confidence", "medium"),
        "party_source_url": party_baseline.get("source_url_primary", ""),
        "party_note": party_baseline.get("source_note", ""),
        "caucus": caucus,
        "caucus_basis": caucus_baseline.get("basis", "caucus_term_start_baseline"),
        "caucus_confidence": caucus_baseline.get("confidence", "medium"),
        "caucus_source_url": caucus_baseline.get("source_url_primary", ""),
        "caucus_note": caucus_baseline.get("source_note", ""),
        "date_precision": "term_start",
    }

    # Un primer evento documentado puede aportar evidencia directa del estado previo.
    if first_event:
        if first_event.get("party_before") and first_event["party_before"] != state["party"]:
            state["party_note"] += (
                f" | Primer evento documenta partido previo {first_event['party_before']}; "
                "revisar discrepancia con línea base."
            )
        if first_event.get("caucus_before"):
            event_conf = first_event.get("confidence") or "high"
            if CONFIDENCE_ORDER.get(event_conf, 0) >= CONFIDENCE_ORDER.get(state["caucus_confidence"], 0):
                state["caucus"] = first_event["caucus_before"]
                state["caucus_basis"] = "documented_pre_event_state"
                state["caucus_confidence"] = event_conf
                state["caucus_source_url"] = first_event.get("source_url", "")
                state["caucus_note"] = "Estado de bancada anterior reconstruido a partir del primer cambio documentado del período."
    return state


def apply_event_to_state(state: dict, event: dict) -> None:
    confidence = event.get("confidence") or "medium"
    source = event.get("source_url", "")
    note = event.get("note", "")
    source_type = event.get("source_type") or "documented_event"
    precision = event.get("date_precision") or "day"

    if event.get("party_after"):
        state["party"] = event["party_after"]
        state["party_basis"] = source_type
        state["party_confidence"] = confidence
        state["party_source_url"] = source
        state["party_note"] = note
    if event.get("caucus_after"):
        state["caucus"] = event["caucus_after"]
        state["caucus_basis"] = source_type
        state["caucus_confidence"] = confidence
        state["caucus_source_url"] = source
        state["caucus_note"] = note
    state["date_precision"] = precision


def build_history(snapshots: list[dict], events: list[dict], party_baselines: list[dict],
                  caucus_baselines: list[dict]) -> tuple[list[dict], list[dict]]:
    latest_date, latest_by_id = latest_snapshot(snapshots)
    party_by_id = {x["deputy_id"]: x for x in party_baselines}
    caucus_by_id = {x["deputy_id"]: x for x in caucus_baselines}
    if len(party_by_id) != 155:
        raise RuntimeError(f"La línea base partidaria debe contener 155 diputados; contiene {len(party_by_id)}")
    if len(caucus_by_id) != 155:
        raise RuntimeError(f"La línea base de bancadas debe contener 155 diputados; contiene {len(caucus_by_id)}")
    if set(party_by_id) != set(caucus_by_id):
        raise RuntimeError("Las líneas base de partido y bancada no cubren exactamente los mismos diputados")

    events_by_id: dict[str, list[dict]] = defaultdict(list)
    for event in events:
        if not event.get("deputy_id") or not event.get("effective_date"):
            continue
        if parse_day(event["effective_date"]) <= latest_date:
            events_by_id[event["deputy_id"]].append(event)
    for rows in events_by_id.values():
        rows.sort(key=lambda x: (x["effective_date"], 0 if x.get("source_type") != "camara_weekly_snapshot_change" else 1))

    history: list[dict] = []
    conflicts: list[dict] = []

    for deputy_id, snap in sorted(latest_by_id.items(), key=lambda kv: int(kv[0])):
        name = snap["deputy_name"]
        party_baseline = party_by_id[deputy_id]
        caucus_baseline = caucus_by_id[deputy_id]
        electoral = party_baseline
        deputy_events = events_by_id.get(deputy_id, [])
        first_event = deputy_events[0] if deputy_events else None
        state = initial_state(deputy_id, party_baseline, caucus_baseline, first_event)
        start = TERM_START

        for event in deputy_events:
            event_day = parse_day(event["effective_date"])
            if event_day < TERM_START:
                apply_event_to_state(state, event)
                continue
            if event_day > start:
                history.append(make_interval(deputy_id, name, start, event_day - timedelta(days=1), state, electoral))
            apply_event_to_state(state, event)
            start = max(event_day, TERM_START)

        mismatch = []
        official_party = snap.get("party_reported") or "Sin información"
        official_caucus = snap.get("caucus_reported") or "Bancada por confirmar"
        if official_party != state["party"]:
            mismatch.append(f"party: Cámara={official_party} / historial={state['party']}")
        if official_caucus != state["caucus"]:
            mismatch.append(f"caucus: Cámara={official_caucus} / historial={state['caucus']}")
        conflict = "1" if mismatch else "0"
        if mismatch:
            conflicts.append({"deputy_id": deputy_id, "deputy_name": name, "detail": " | ".join(mismatch)})
            state["party_note"] += (" | " if state.get("party_note") else "") + "Conflicto con snapshot oficial vigente registrado por auditoría."

        history.append(make_interval(deputy_id, name, start, None, state, electoral, conflict))

    history.sort(key=lambda x: (int(x["deputy_id"]), x["valid_from"]))
    return history, conflicts


def audit_history(history: list[dict], snapshot_count: int, conflicts: list[dict], detected: list[dict]) -> dict:
    by_id: dict[str, list[dict]] = defaultdict(list)
    for row in history:
        by_id[row["deputy_id"]].append(row)

    bad_starts = []
    overlaps = []
    for deputy_id, rows in by_id.items():
        rows.sort(key=lambda x: x["valid_from"])
        if rows[0]["valid_from"] != TERM_START.isoformat():
            bad_starts.append(deputy_id)
        for left, right in zip(rows, rows[1:]):
            if left["valid_to"] and parse_day(left["valid_to"]) >= parse_day(right["valid_from"]):
                overlaps.append(deputy_id)

    if snapshot_count != 155:
        raise RuntimeError(f"El snapshot actual no contiene 155 diputados: {snapshot_count}")
    if len(by_id) != 155:
        raise RuntimeError(f"El historial no cubre 155 diputados: {len(by_id)}")
    if bad_starts or overlaps:
        raise RuntimeError(f"Historial temporal inconsistente: bad_starts={bad_starts}, overlaps={overlaps}")

    term_start_rows = [sorted(rows, key=lambda x: x["valid_from"])[0] for rows in by_id.values()]
    party_provisional = sum(x["party_confidence"] == "provisional" for x in term_start_rows)
    caucus_provisional = sum(x["caucus_confidence"] == "provisional" for x in term_start_rows)
    if party_provisional or caucus_provisional:
        raise RuntimeError(
            f"La línea de base aún contiene valores provisionales: party={party_provisional}, caucus={caucus_provisional}"
        )

    return {
        "generated_for": date.today().isoformat(),
        "deputies": len(by_id),
        "history_intervals": len(history),
        "documented_manual_events": len(read_csv(MANUAL_EVENTS)),
        "detected_weekly_snapshot_events": len(detected),
        "party_term_start_high_confidence": sum(x["party_confidence"] == "high" for x in term_start_rows),
        "party_term_start_medium_confidence": sum(x["party_confidence"] == "medium" for x in term_start_rows),
        "party_term_start_provisional": party_provisional,
        "caucus_term_start_high_confidence": sum(x["caucus_confidence"] == "high" for x in term_start_rows),
        "caucus_term_start_medium_confidence": sum(x["caucus_confidence"] == "medium" for x in term_start_rows),
        "caucus_term_start_provisional": caucus_provisional,
        "party_interval_confidence_counts": dict(Counter(x["party_confidence"] for x in history)),
        "caucus_interval_confidence_counts": dict(Counter(x["caucus_confidence"] for x in history)),
        "overall_interval_confidence_counts": dict(Counter(x["confidence"] for x in history)),
        "official_snapshot_conflicts": conflicts,
        "term_start": TERM_START.isoformat(),
        "party_history_coverage": 155,
        "caucus_history_coverage": 155,
        "warning": "Las líneas base de partido y bancada cubren 155/155 sin valores provisionales. Los cambios detectados solo entre snapshots semanales conservan una ventana de incertidumbre en affiliation_detected_events.csv y deben tratarse como fecha aproximada hasta su corroboración documental.",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    profiles = load_profiles()
    if len(profiles) != 155:
        raise RuntimeError(f"Se esperaban 155 perfiles; hay {len(profiles)}")

    party_baselines = read_csv(PARTY_BASELINE)
    caucus_baselines = read_csv(CAUCUS_BASELINE)
    if len(party_baselines) != 155:
        raise RuntimeError(f"Falta línea base partidaria completa: {len(party_baselines)}/155")
    if len(caucus_baselines) != 155:
        raise RuntimeError(f"Falta línea base de bancadas completa: {len(caucus_baselines)}/155")

    observed = snapshot_date(profiles)
    current = current_snapshot_rows(profiles, observed)
    snapshots = persist_snapshot(current, observed)
    manual = read_csv(MANUAL_EVENTS)
    detected = derive_detected_events(snapshots, manual)
    combined = event_rows(manual, detected)
    history, conflicts = build_history(snapshots, combined, party_baselines, caucus_baselines)
    write_csv(HISTORY, history, HISTORY_FIELDS)

    diagnostics = audit_history(history, len(current), conflicts, detected)
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
