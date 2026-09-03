from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from congress_api import child, child_text, descendants, enum_value, get_xml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026" / "agenda" / "sala_snapshot.json"
TZ = ZoneInfo("America/Santiago")


def parse_dt(value: str) -> datetime | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=TZ)
    return parsed.astimezone(TZ)


def session_row(node) -> dict:
    start_raw = child_text(node, "FechaInicio")
    end_raw = child_text(node, "FechaTermino")
    start = parse_dt(start_raw)
    end = parse_dt(end_raw)
    state, state_code = enum_value(child(node, "Estado"))
    session_type, type_code = enum_value(child(node, "Tipo"))
    return {
        "session_id": child_text(node, "Id"),
        "number": child_text(node, "Numero"),
        "start": start.isoformat() if start else start_raw,
        "end": end.isoformat() if end else end_raw,
        "local_date": start.date().isoformat() if start else "",
        "state": state,
        "state_code": state_code,
        "type": session_type,
        "type_code": type_code,
    }


def main() -> None:
    now = datetime.now(TZ)
    today = now.date()
    root = get_xml("WSSala", "retornarSesionesXAnno", {"prmAnno": today.year})
    sessions = [session_row(node) for node in descendants(root, "SesionSala")]
    sessions = [row for row in sessions if row["session_id"] and row["local_date"]]
    sessions.sort(key=lambda row: (row["start"], int(row["number"] or 0)))

    window_start = today - timedelta(days=2)
    window_end = today + timedelta(days=14)
    window = [
        row
        for row in sessions
        if window_start.isoformat() <= row["local_date"] <= window_end.isoformat()
    ]
    today_rows = [row for row in sessions if row["local_date"] == today.isoformat()]
    upcoming = [row for row in sessions if row["local_date"] > today.isoformat()][:8]
    recent = [row for row in sessions if row["local_date"] < today.isoformat()][-4:]

    payload = {
        "schema_version": "sala-agenda-v0.1",
        "source": {
            "name": "Cámara de Diputadas y Diputados de Chile · Open Data",
            "service": "WSSala.retornarSesionesXAnno",
            "url": "https://opendata.camara.cl/camaradiputados/pages/sala/retornarSesionesXAnno.aspx",
        },
        "generated_at": now.isoformat(),
        "timezone": "America/Santiago",
        "local_date": today.isoformat(),
        "year": today.year,
        "counts": {
            "sessions_returned_year": len(sessions),
            "today": len(today_rows),
            "upcoming_shown": len(upcoming),
            "recent_shown": len(recent),
        },
        "today": today_rows,
        "upcoming": upcoming,
        "recent": recent,
        "window": window,
        "scope_note": (
            "Este snapshot describe sesiones de Sala registradas por el servicio oficial. "
            "No equivale a la tabla del Orden del Día ni afirma qué asuntos serán efectivamente votados."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Snapshot Sala: {OUT} | hoy={len(today_rows)} | próximas={len(upcoming)}")


if __name__ == "__main__":
    main()
