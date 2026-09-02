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
EVENTS = OUT / "affiliation_manual_events.csv"
HISTORY = OUT / "affiliation_history.csv"
DIAGNOSTICS = OUT / "affiliation_diagnostics.json"
TERM_START = date(2026, 3, 11)

SNAPSHOT_FIELDS = [
    "observed_date", "deputy_id", "deputy_name", "party_reported", "caucus_reported",
    "alignment_reported", "profile_url", "source_type",
]

EVENT_FIELDS = [
    "effective_date", "deputy_id", "deputy_name", "party_before", "party_after",
    "caucus_before", "caucus_after", "source_url", "source_type", "confidence",
    "date_precision", "note",
]

HISTORY_FIELDS = [
    "deputy_id", "deputy_name", "valid_from", "valid_to", "party", "caucus",
    "alignment", "basis", "confidence", "date_precision", "source_url", "source_note",
    "official_snapshot_conflict",
]


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
    # Una reejecución del mismo día reemplaza el snapshot de ese día, no lo duplica.
    kept = [row for row in old if row.get("observed_date") != observed.isoformat()]
    merged = kept + rows
    merged.sort(key=lambda x: (x["observed_date"], int(x["deputy_id"])))
    write_csv(SNAPSHOTS, merged, SNAPSHOT_FIELDS)
    return merged


def state_from_snapshot(row: dict) -> dict:
    return {
        "party": row.get("party_reported") or "Sin información",
        "caucus": row.get("caucus_reported") or "Bancada por confirmar",
    }


def make_interval(deputy_id: str, name: str, start: date, end: date | None, state: dict,
                  basis: str, confidence: str, precision: str, source_url: str, note: str,
                  conflict: str = "0") -> dict:
    return {
        "deputy_id": deputy_id,
        "deputy_name": name,
        "valid_from": start.isoformat(),
        "valid_to": end.isoformat() if end else "",
        "party": state.get("party") or "Sin información",
        "caucus": state.get("caucus") or "Bancada por confirmar",
        "alignment": classify(state.get("party"), state.get("caucus")),
        "basis": basis,
        "confidence": confidence,
        "date_precision": precision,
        "source_url": source_url,
        "source_note": note,
        "official_snapshot_conflict": conflict,
    }


def build_history(snapshots: list[dict], events: list[dict]) -> tuple[list[dict], list[dict]]:
    latest_date = max(parse_day(x["observed_date"]) for x in snapshots)
    latest_by_id: dict[str, dict] = {}
    for row in snapshots:
        if parse_day(row["observed_date"]) == latest_date:
            latest_by_id[row["deputy_id"]] = row

    events_by_id: dict[str, list[dict]] = defaultdict(list)
    for event in events:
        if not event.get("deputy_id") or not event.get("effective_date"):
            continue
        events_by_id[event["deputy_id"]].append(event)
    for rows in events_by_id.values():
        rows.sort(key=lambda x: x["effective_date"])

    history: list[dict] = []
    conflicts: list[dict] = []

    for deputy_id, snap in sorted(latest_by_id.items(), key=lambda kv: int(kv[0])):
        name = snap["deputy_name"]
        official = state_from_snapshot(snap)
        deputy_events = [e for e in events_by_id.get(deputy_id, []) if parse_day(e["effective_date"]) <= latest_date]

        if not deputy_events:
            history.append(make_interval(
                deputy_id, name, TERM_START, None, official,
                "current_snapshot_assumed_stable", "provisional", "term_assumption",
                snap.get("profile_url", ""),
                "Sin cambio 2026 documentado todavía; se validará contra afiliación electoral de 2025.",
            ))
            continue

        first = deputy_events[0]
        state = {
            "party": first.get("party_before") or official["party"],
            "caucus": first.get("caucus_before") or official["caucus"],
        }
        start = TERM_START
        previous_source = first.get("source_url", "")
        previous_note = "Estado anterior reconstruido a partir del primer cambio documentado."

        for event in deputy_events:
            event_day = parse_day(event["effective_date"])
            if event_day < TERM_START:
                continue
            if event_day > start:
                history.append(make_interval(
                    deputy_id, name, start, event_day - timedelta(days=1), state,
                    "documented_event_chain", event.get("confidence") or "high",
                    event.get("date_precision") or "day", previous_source, previous_note,
                ))
            if event.get("party_after"):
                state["party"] = event["party_after"]
            if event.get("caucus_after"):
                state["caucus"] = event["caucus_after"]
            start = event_day
            previous_source = event.get("source_url", "")
            previous_note = event.get("note", "")

        mismatch = []
        if official["party"] != state["party"]:
            mismatch.append(f"party: Cámara={official['party']} / evidencia={state['party']}")
        if official["caucus"] != state["caucus"]:
            mismatch.append(f"caucus: Cámara={official['caucus']} / evidencia={state['caucus']}")
        conflict = "1" if mismatch else "0"
        if mismatch:
            conflicts.append({"deputy_id": deputy_id, "deputy_name": name, "detail": " | ".join(mismatch)})

        history.append(make_interval(
            deputy_id, name, start, None, state,
            "documented_event_chain", deputy_events[-1].get("confidence") or "high",
            deputy_events[-1].get("date_precision") or "day", previous_source,
            previous_note + ((" | Conflicto con snapshot oficial: " + " | ".join(mismatch)) if mismatch else ""),
            conflict,
        ))

    history.sort(key=lambda x: (int(x["deputy_id"]), x["valid_from"]))
    return history, conflicts


def audit_history(history: list[dict], snapshot_count: int, conflicts: list[dict]) -> dict:
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

    basis_counts = Counter(x["basis"] for x in history)
    confidence_counts = Counter(x["confidence"] for x in history)
    return {
        "generated_for": date.today().isoformat(),
        "deputies": len(by_id),
        "history_intervals": len(history),
        "documented_manual_events": len(read_csv(EVENTS)),
        "basis_counts": dict(basis_counts),
        "confidence_counts": dict(confidence_counts),
        "official_snapshot_conflicts": conflicts,
        "provisional_deputies": sum(1 for rows in by_id.values() if all(x["basis"] == "current_snapshot_assumed_stable" for x in rows)),
        "verified_event_chain_deputies": sum(1 for rows in by_id.values() if any(x["basis"] == "documented_event_chain" for x in rows)),
        "term_start": TERM_START.isoformat(),
        "warning": "Los diputados sin cambio documentado usan provisionalmente el snapshot actual hacia atrás hasta validar la afiliación electoral 2025. No usar esos intervalos como historia definitiva sin considerar confidence/basis.",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    profiles = load_profiles()
    if len(profiles) != 155:
        raise RuntimeError(f"Se esperaban 155 perfiles; hay {len(profiles)}")

    observed = snapshot_date(profiles)
    current = current_snapshot_rows(profiles, observed)
    snapshots = persist_snapshot(current, observed)
    events = read_csv(EVENTS)
    history, conflicts = build_history(snapshots, events)
    write_csv(HISTORY, history, HISTORY_FIELDS)

    diagnostics = audit_history(history, len(current), conflicts)
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
