from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from congress_api import child, child_text, children, descendants, enum_value, get_xml, person

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026" / "commissions" / "commissions_snapshot.json"
TZ = ZoneInfo("America/Santiago")


def parse_dt(value: str) -> str:
    raw = (value or "").strip()
    if not raw:
        return ""
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return raw
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=TZ)
    return parsed.astimezone(TZ).isoformat()


def member_rows(node) -> list[dict]:
    container = child(node, "Integrantes")
    if container is None:
        return []
    rows = []
    for wrapper in descendants(container, "DiputadoIntegrante"):
        p = person(child(wrapper, "Diputado"))
        if not (p["id"] or p["name"]):
            continue
        rows.append({
            "id": p["id"],
            "name": p["name"],
            "start": parse_dt(child_text(wrapper, "FechaInicio")),
            "end": parse_dt(child_text(wrapper, "FechaTermino")),
        })
    return rows


def session_rows(node) -> list[dict]:
    container = child(node, "Sesiones")
    if container is None:
        return []
    rows = []
    for session in descendants(container, "SesionComision"):
        state, state_code = enum_value(child(session, "Estado"))
        session_type, type_code = enum_value(child(session, "Tipo"))
        rows.append({
            "id": child_text(session, "Id"),
            "number": child_text(session, "Numero"),
            "start": parse_dt(child_text(session, "FechaInicio")),
            "end": parse_dt(child_text(session, "FechaTermino")),
            "state": state,
            "state_code": state_code,
            "type": session_type,
            "type_code": type_code,
        })
    return sorted(rows, key=lambda row: row["start"] or "")


def commission_row(node) -> dict:
    state, state_code = enum_value(child(node, "Estado"))
    commission_type, type_code = enum_value(child(node, "Tipo"))
    president = person(child(node, "Presidente"))
    return {
        "id": child_text(node, "Id"),
        "number": child_text(node, "Numero"),
        "name": child_text(node, "Nombre"),
        "web_name": child_text(node, "NombreWeb"),
        "alias": child_text(node, "Alias"),
        "email": child_text(node, "Correo"),
        "phone": child_text(node, "Telefono"),
        "start": parse_dt(child_text(node, "FechaInicio")),
        "constitution_date": parse_dt(child_text(node, "FechaConstitucion")),
        "end": parse_dt(child_text(node, "FechaTermino")),
        "state": state,
        "state_code": state_code,
        "type": commission_type,
        "type_code": type_code,
        "president": president if (president["id"] or president["name"]) else None,
        "members": member_rows(node),
        "sessions": session_rows(node),
    }


def main() -> None:
    now = datetime.now(TZ)
    root = get_xml("WSComision", "retornarComisionesVigentes")
    nodes = descendants(root, "Comision")
    commissions = [commission_row(node) for node in nodes]
    commissions = [row for row in commissions if row["id"] and row["name"]]
    commissions.sort(key=lambda row: (row["type"], row["name"]))

    payload = {
        "schema_version": "commissions-v0.1",
        "generated_at": now.isoformat(),
        "timezone": "America/Santiago",
        "source": {
            "name": "Cámara de Diputadas y Diputados de Chile · Open Data",
            "service": "WSComision.retornarComisionesVigentes",
            "url": "https://opendata.camara.cl/camaradiputados/pages/comision/retornarComisionesVigentes.aspx",
        },
        "counts": {
            "commissions": len(commissions),
            "with_members": sum(bool(row["members"]) for row in commissions),
            "with_president": sum(bool(row["president"]) for row in commissions),
            "with_sessions_embedded": sum(bool(row["sessions"]) for row in commissions),
        },
        "commissions": commissions,
        "scope_note": (
            "La ficha reproduce campos entregados por el servicio oficial de comisiones vigentes. "
            "Una colección vacía significa que el método consultado no devolvió esos elementos; no se interpreta como ausencia sustantiva."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Comisiones vigentes: {len(commissions)} | con integrantes={payload['counts']['with_members']}")


if __name__ == "__main__":
    main()
