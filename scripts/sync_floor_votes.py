from __future__ import annotations

import json
from collections import Counter
from datetime import date

from congress_api import child, child_text, enum_value, get_xml
from legislative_common import (
    OUT,
    annual_votes,
    date_ok,
    individual_votes,
    iso_date,
    nested,
    read_csv,
    upsert,
    verify_sala,
    vote_detail,
    write_csv,
)

ROLLCALL_FIELDS = [
    "vote_id", "boletin", "fecha", "sesion_id", "sesion_numero", "descripcion", "articulo",
    "total_si", "total_no", "total_abstencion", "total_dispensado", "tipo_votacion",
    "tipo_votacion_codigo", "resultado", "resultado_codigo", "quorum", "quorum_codigo",
    "tipo_votacion_proyecto", "tipo_votacion_proyecto_codigo", "tramite_constitucional",
    "tramite_constitucional_codigo", "tramite_reglamentario", "tramite_reglamentario_codigo",
    "verificado_sala", "verification_url",
]
MEMBER_FIELDS = ["vote_id", "diputado_id", "diputado_nombre", "opcion", "opcion_codigo"]
STATE_PATH = OUT / "floor_vote_state.json"


def project_vote_map(boletin: str) -> dict[str, object]:
    root = get_xml("WSLegislativo", "retornarVotacionesXProyectoLey", {"prmNumeroBoletin": boletin})
    projects = [root] if root.tag.endswith("ProyectoLey") else [x for x in root.iter() if x.tag.endswith("ProyectoLey")]
    if not projects:
        return {}
    return {child_text(v, "Id"): v for v in nested(projects[0], "Votaciones", {"VotacionProyectoLey", "Votacion"}) if child_text(v, "Id")}


def session_index() -> dict[tuple[str, str], str]:
    root = get_xml("WSSala", "retornarSesionesXAnno", {"prmAnno": 2026})
    result = {}
    for session in [x for x in root.iter() if x.tag.endswith("Sesion") or x.tag.endswith("SesionSala")]:
        day = iso_date(child_text(session, "FechaInicio"))
        number = child_text(session, "Numero")
        sid = child_text(session, "Id")
        if day and number and sid:
            result[(day, number)] = sid
    return result


def pick(primary, fallback, field: str) -> str:
    return child_text(primary, field) or child_text(fallback, field)


def first_element(primary, fallback, field: str):
    value = child(primary, field)
    return value if value is not None else child(fallback, field)


def rollcall_row(project_vote, base_vote, sala: dict, sessions: dict) -> dict:
    vote_id = pick(project_vote, base_vote, "Id")
    vote_date = iso_date(pick(project_vote, base_vote, "Fecha"))
    vote_type, vote_type_code = enum_value(first_element(project_vote, base_vote, "Tipo"))
    result, result_code = enum_value(first_element(project_vote, base_vote, "Resultado"))
    quorum, quorum_code = enum_value(first_element(project_vote, base_vote, "Quorum"))
    ptype, ptype_code = enum_value(child(project_vote, "TipoVotacionProyectoLey"))
    constitutional, constitutional_code = enum_value(child(project_vote, "TramiteConstitucional"))
    regulatory, regulatory_code = enum_value(child(project_vote, "TramiteReglamentario"))
    session_number = sala.get("sesion_numero", "")
    session_id = sessions.get((sala.get("fecha", "") or vote_date, session_number), "") if session_number else ""
    return {
        "vote_id": vote_id,
        "boletin": sala.get("boletin", ""),
        "fecha": vote_date,
        "sesion_id": session_id,
        "sesion_numero": session_number,
        "descripcion": pick(project_vote, base_vote, "Descripcion"),
        "articulo": child_text(project_vote, "Articulo"),
        "total_si": pick(project_vote, base_vote, "TotalSi"),
        "total_no": pick(project_vote, base_vote, "TotalNo"),
        "total_abstencion": pick(project_vote, base_vote, "TotalAbstencion"),
        "total_dispensado": pick(project_vote, base_vote, "TotalDispensado"),
        "tipo_votacion": vote_type,
        "tipo_votacion_codigo": vote_type_code,
        "resultado": result,
        "resultado_codigo": result_code,
        "quorum": quorum,
        "quorum_codigo": quorum_code,
        "tipo_votacion_proyecto": ptype,
        "tipo_votacion_proyecto_codigo": ptype_code,
        "tramite_constitucional": constitutional,
        "tramite_constitucional_codigo": constitutional_code,
        "tramite_reglamentario": regulatory,
        "tramite_reglamentario_codigo": regulatory_code,
        "verificado_sala": "1",
        "verification_url": sala.get("verification_url", ""),
    }


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"skipped_non_project": []}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"skipped_non_project": []}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    annual = annual_votes()
    existing_rollcalls = read_csv("rollcalls.csv")
    existing_members = read_csv("member_votes.csv")
    member_counts = Counter(x["vote_id"] for x in existing_members)
    complete_ids = {x["vote_id"] for x in existing_rollcalls if member_counts[x["vote_id"]] >= 150}
    state = load_state()
    skipped = set(state.get("skipped_non_project", []))
    pending = [vid for vid in annual if vid not in complete_ids and vid not in skipped]
    pending.sort(key=lambda vid: (iso_date(child_text(annual[vid], "Fecha")), int(vid) if vid.isdigit() else vid))

    sessions = session_index()
    project_cache: dict[str, dict[str, object]] = {}
    incoming_rollcalls = []
    incoming_members = []
    errors = []
    newly_skipped = []

    for idx, vote_id in enumerate(pending, start=1):
        base = annual[vote_id]
        expected_date = iso_date(child_text(base, "Fecha"))
        if not date_ok(expected_date):
            continue
        try:
            sala = verify_sala(vote_id, expected_date)
            boletin = sala.get("boletin", "")
            if not boletin:
                newly_skipped.append(vote_id)
                continue
            if boletin not in project_cache:
                project_cache[boletin] = project_vote_map(boletin)
            project_vote = project_cache[boletin].get(vote_id)
            if project_vote is None:
                raise RuntimeError(f"{vote_id}: página Sala indica boletín {boletin}, pero el ID no aparece en retornarVotacionesXProyectoLey")
            detail = vote_detail(vote_id)
            members = individual_votes(detail, vote_id)
            if len(members) < 150:
                raise RuntimeError(f"{vote_id}: solo {len(members)} registros nominales")
            incoming_rollcalls.append(rollcall_row(project_vote, base, sala, sessions))
            incoming_members.extend(members)
        except Exception as exc:  # noqa: BLE001
            errors.append({"vote_id": vote_id, "error": str(exc)})
        if idx % 50 == 0:
            print(f"Votaciones {idx}/{len(pending)} · nuevas={len(incoming_rollcalls)} · omitidas={len(newly_skipped)} · errores={len(errors)}")

    rollcalls = upsert(existing_rollcalls, incoming_rollcalls, ("vote_id",), ("fecha", "vote_id"))
    members = upsert(existing_members, incoming_members, ("vote_id", "diputado_id"), ("vote_id", "diputado_id"))
    write_csv("rollcalls.csv", rollcalls, ROLLCALL_FIELDS)
    write_csv("member_votes.csv", members, MEMBER_FIELDS)

    skipped.update(newly_skipped)
    state = {
        "updated_for": str(date.today()),
        "annual_votes_since_period_start": len(annual),
        "skipped_non_project": sorted(skipped, key=lambda x: int(x) if str(x).isdigit() else str(x)),
    }
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    diagnostics = {
        "generated_for": str(date.today()),
        "annual_votes_since_period_start": len(annual),
        "pending_this_run": len(pending),
        "new_project_floor_rollcalls": len(incoming_rollcalls),
        "new_member_vote_rows": len(incoming_members),
        "rollcalls_in_database": len(rollcalls),
        "member_vote_rows_in_database": len(members),
        "non_project_floor_votes_skipped": len(skipped),
        "errors": errors,
    }
    (OUT / "floor_votes_diagnostics.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errors and len(errors) / max(len(pending), 1) > 0.05:
        raise RuntimeError(f"Demasiados errores en votaciones: {len(errors)}/{len(pending)}")
    if rollcalls and len(members) < len(rollcalls) * 150:
        raise RuntimeError("La matriz nominal acumulada no alcanza 150 registros por roll call")
    print(json.dumps({k: v for k, v in diagnostics.items() if k != "errors"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
