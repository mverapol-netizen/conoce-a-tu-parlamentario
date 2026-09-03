from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from congress_api import child, child_text, descendants, enum_value, get_xml, person

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026" / "commissions" / "commissions_snapshot.json"
TZ = ZoneInfo("America/Santiago")
MIN_EXPECTED_COMMISSION_COUNT = 10


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


def current_period() -> dict:
    root = get_xml("WSLegislativo", "retornarPeriodoLegislativoActual")
    period_id = child_text(root, "Id")
    if not period_id:
        raise RuntimeError("retornarPeriodoLegislativoActual no devolvió Id")
    return {
        "id": period_id,
        "name": child_text(root, "Nombre"),
        "start": parse_dt(child_text(root, "FechaInicio")),
        "end": parse_dt(child_text(root, "FechaTermino")),
    }


def main() -> None:
    now = datetime.now(TZ)
    period = current_period()
    root = get_xml("WSComision", "retornarComisionesXPeriodo", {"prmPeriodoId": period["id"]})
    nodes = descendants(root, "Comision")
    commissions = [commission_row(node) for node in nodes]
    commissions = [row for row in commissions if row["id"] and row["name"]]
    commissions.sort(key=lambda row: (row["type"], row["name"]))

    if len(commissions) < MIN_EXPECTED_COMMISSION_COUNT:
        raise RuntimeError(
            f"Universo de comisiones no plausible para período {period['id']}: "
            f"{len(commissions)} < {MIN_EXPECTED_COMMISSION_COUNT}"
        )

    payload = {
        "schema_version": "commissions-v0.2",
        "generated_at": now.isoformat(),
        "timezone": "America/Santiago",
        "period": period,
        "source": {
            "name": "Cámara de Diputadas y Diputados de Chile · Open Data",
            "services": [
                "WSLegislativo.retornarPeriodoLegislativoActual",
                "WSComision.retornarComisionesXPeriodo",
            ],
            "url": "https://opendata.camara.cl/camaradiputados/WServices/WSComision.asmx?op=retornarComisionesXPeriodo",
        },
        "counts": {
            "commissions": len(commissions),
            "with_members": sum(bool(row["members"]) for row in commissions),
            "with_president": sum(bool(row["president"]) for row in commissions),
            "with_sessions_embedded": sum(bool(row["sessions"]) for row in commissions),
        },
        "commissions": commissions,
        "scope_note": (
            "El universo se obtiene para el período legislativo actual resuelto por el servicio oficial. "
            "Una colección vacía de integrantes o sesiones significa que el método consultado no devolvió esos elementos; "
            "no se interpreta como ausencia sustantiva."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Periodo {period['id']} {period['name']} | comisiones={len(commissions)} "
        f"| con integrantes={payload['counts']['with_members']} "
        f"| con sesiones={payload['counts']['with_sessions_embedded']}"
    )


if __name__ == "__main__":
    main()
