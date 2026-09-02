from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
TOPICS = OUT / "topics"

ROLLCALL_META = OUT / "rollcall_matrix_metadata.csv"
MEMBER_VOTES = OUT / "member_votes_enriched.csv"
TOPIC_MAP = TOPICS / "rollcall_topic_map.csv"
PERIOD_PROJECTS = TOPICS / "project_topic_final.csv"
INHERITED_PROJECTS = TOPICS / "rollcall_inherited_topic_final.csv"

ROLLCALL_OUTPUT = OUT / "rollcall_model_eligibility.csv"
SENSITIVITY_OUTPUT = OUT / "rollcall_model_sensitivity.csv"
TOPIC_OUTPUT = OUT / "rollcall_model_sensitivity_by_topic.csv"
ORIGIN_OUTPUT = OUT / "rollcall_model_sensitivity_by_origin.csv"
DIAGNOSTICS = OUT / "rollcall_model_eligibility_diagnostics.json"

MINORITY_THRESHOLDS = (0.0, 0.025, 0.05, 0.10)
ROLLCALL_PARTICIPATION_FLOORS = (0.50, 0.75, 0.90)
MEMBER_PARTICIPATION_FLOORS = (0.50, 0.75, 0.90)
EXPECTED_MEMBERS = 155

ROLLCALL_FIELDS = [
    "vote_id", "fecha", "boletin", "topic_primary", "origin_initiative", "topic_source_layer",
    "vote_stage", "result", "binary_votes", "missing_for_spatial_model", "minority_count",
    "minority_share_binary", "binary_participation_share", "unanimous_binary",
]

SENSITIVITY_FIELDS = [
    "spec_id", "minority_share_floor", "rollcall_binary_participation_floor",
    "eligible_rollcalls", "eligible_share_of_all_rollcalls", "eligible_share_of_nonunanimous_rollcalls",
    "binary_observations", "missing_observations", "mean_rollcall_binary_participation",
    "min_member_binary_participation", "median_member_binary_participation", "max_member_binary_participation",
    "members_participation_gte_050", "members_participation_gte_075", "members_participation_gte_090",
    "topics_represented", "origins_represented",
]

BREAKDOWN_FIELDS = [
    "spec_id", "minority_share_floor", "rollcall_binary_participation_floor",
    "dimension_value", "all_rollcalls", "nonunanimous_rollcalls", "eligible_rollcalls",
    "retention_vs_all", "retention_vs_nonunanimous",
]

YES = "Afirmativo"
NO = "En Contra"
BINARY_OPTIONS = {YES, NO}


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def safe_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def safe_int(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def pct(num: int | float, den: int | float) -> str:
    return f"{num / den:.6f}" if den else ""


def spec_id(minority_floor: float, participation_floor: float) -> str:
    return f"m{int(round(minority_floor * 1000)):03d}_p{int(round(participation_floor * 100)):03d}"


def origin_map() -> dict[str, str]:
    mapping = {}
    for path in (PERIOD_PROJECTS, INHERITED_PROJECTS):
        for row in read_csv(path):
            bill = (row.get("boletin") or "").strip()
            origin = (row.get("origen_iniciativa") or "").strip()
            if not bill:
                continue
            previous = mapping.get(bill)
            if previous and origin and previous != origin:
                raise RuntimeError(f"Origen inconsistente para boletín {bill}: {previous} vs {origin}")
            if origin:
                mapping[bill] = origin
    return mapping


def member_binary_participation(selected_ids: set[str], votes: list[dict]) -> dict[str, float]:
    if not selected_ids:
        return {}
    binary = Counter()
    members = set()
    for row in votes:
        member_id = (row.get("diputado_id") or "").strip()
        if not member_id:
            continue
        members.add(member_id)
        if row.get("vote_id") in selected_ids and row.get("opcion") in BINARY_OPTIONS:
            binary[member_id] += 1
    if len(members) != EXPECTED_MEMBERS:
        raise RuntimeError(f"Se esperaban {EXPECTED_MEMBERS} diputados; aparecen {len(members)}")
    denominator = len(selected_ids)
    return {member_id: binary[member_id] / denominator for member_id in members}


def breakdown_rows(
    dimension: str,
    values_by_vote: dict[str, str],
    all_vote_ids: set[str],
    nonunanimous_ids: set[str],
    specs: list[tuple[str, float, float, set[str]]],
) -> list[dict]:
    universe_values = sorted({values_by_vote.get(vote_id, "") or "Sin información" for vote_id in all_vote_ids})
    rows = []
    for sid, minority_floor, participation_floor, selected in specs:
        for value in universe_values:
            all_count = sum((values_by_vote.get(vote_id, "") or "Sin información") == value for vote_id in all_vote_ids)
            nonunanimous_count = sum(
                (values_by_vote.get(vote_id, "") or "Sin información") == value
                for vote_id in nonunanimous_ids
            )
            eligible_count = sum(
                (values_by_vote.get(vote_id, "") or "Sin información") == value
                for vote_id in selected
            )
            rows.append({
                "spec_id": sid,
                "minority_share_floor": f"{minority_floor:.3f}",
                "rollcall_binary_participation_floor": f"{participation_floor:.2f}",
                "dimension_value": value,
                "all_rollcalls": all_count,
                "nonunanimous_rollcalls": nonunanimous_count,
                "eligible_rollcalls": eligible_count,
                "retention_vs_all": pct(eligible_count, all_count),
                "retention_vs_nonunanimous": pct(eligible_count, nonunanimous_count),
            })
    return rows


def main() -> None:
    rollcalls = read_csv(ROLLCALL_META)
    votes = read_csv(MEMBER_VOTES)
    topics = read_csv(TOPIC_MAP)
    origins = origin_map()

    rollcall_by_id = {row["vote_id"]: row for row in rollcalls}
    if len(rollcall_by_id) != len(rollcalls):
        raise RuntimeError("rollcall_matrix_metadata.csv contiene vote_id duplicados")
    topic_by_id = {row["vote_id"]: row for row in topics}
    if len(topic_by_id) != len(topics):
        raise RuntimeError("rollcall_topic_map.csv contiene vote_id duplicados")
    if set(rollcall_by_id) != set(topic_by_id):
        missing_topics = sorted(set(rollcall_by_id) - set(topic_by_id))[:20]
        extra_topics = sorted(set(topic_by_id) - set(rollcall_by_id))[:20]
        raise RuntimeError(f"Cobertura temática no 1:1. missing={missing_topics}; extra={extra_topics}")

    enriched_rollcalls = []
    topic_value = {}
    origin_value = {}
    missing_origin_bills = set()

    for vote_id, meta in rollcall_by_id.items():
        topic = topic_by_id[vote_id]
        bill = (meta.get("boletin") or topic.get("boletin") or "").strip()
        origin = origins.get(bill, "")
        if bill and not origin:
            missing_origin_bills.add(bill)
        topic_primary = (topic.get("topic_primary") or "").strip()
        topic_value[vote_id] = topic_primary or "Sin tema"
        origin_value[vote_id] = origin or "Sin información"
        enriched_rollcalls.append({
            "vote_id": vote_id,
            "fecha": meta.get("fecha", ""),
            "boletin": bill,
            "topic_primary": topic_primary,
            "origin_initiative": origin,
            "topic_source_layer": topic.get("topic_source_layer", ""),
            "vote_stage": topic.get("tipo_votacion_proyecto", ""),
            "result": topic.get("resultado", ""),
            "binary_votes": meta.get("binary_votes", ""),
            "missing_for_spatial_model": meta.get("missing_for_spatial_model", ""),
            "minority_count": meta.get("minority_count", ""),
            "minority_share_binary": meta.get("minority_share_binary", ""),
            "binary_participation_share": meta.get("binary_participation_share", ""),
            "unanimous_binary": meta.get("unanimous_binary", ""),
        })

    if missing_origin_bills:
        raise RuntimeError(f"Falta origen de iniciativa para {len(missing_origin_bills)} boletines: {sorted(missing_origin_bills)[:20]}")

    enriched_rollcalls.sort(key=lambda row: (row["fecha"], int(row["vote_id"]) if row["vote_id"].isdigit() else row["vote_id"]))
    write_csv(ROLLCALL_OUTPUT, enriched_rollcalls, ROLLCALL_FIELDS)

    all_vote_ids = set(rollcall_by_id)
    nonunanimous_ids = {
        vote_id for vote_id, row in rollcall_by_id.items()
        if safe_int(row.get("minority_count", "")) > 0
    }

    specs: list[tuple[str, float, float, set[str]]] = []
    sensitivity = []
    for minority_floor in MINORITY_THRESHOLDS:
        for participation_floor in ROLLCALL_PARTICIPATION_FLOORS:
            sid = spec_id(minority_floor, participation_floor)
            selected = {
                vote_id for vote_id, row in rollcall_by_id.items()
                if safe_int(row.get("minority_count", "")) > 0
                and safe_float(row.get("minority_share_binary", "")) >= minority_floor
                and safe_float(row.get("binary_participation_share", "")) >= participation_floor
            }
            specs.append((sid, minority_floor, participation_floor, selected))

            member_participation = member_binary_participation(selected, votes)
            member_values = sorted(member_participation.values())
            binary_observations = sum(safe_int(rollcall_by_id[vote_id].get("binary_votes", "")) for vote_id in selected)
            missing_observations = sum(
                safe_int(rollcall_by_id[vote_id].get("missing_for_spatial_model", "")) for vote_id in selected
            )
            mean_rc_participation = (
                sum(safe_float(rollcall_by_id[vote_id].get("binary_participation_share", "")) for vote_id in selected)
                / len(selected)
                if selected else 0.0
            )
            sensitivity.append({
                "spec_id": sid,
                "minority_share_floor": f"{minority_floor:.3f}",
                "rollcall_binary_participation_floor": f"{participation_floor:.2f}",
                "eligible_rollcalls": len(selected),
                "eligible_share_of_all_rollcalls": pct(len(selected), len(all_vote_ids)),
                "eligible_share_of_nonunanimous_rollcalls": pct(len(selected), len(nonunanimous_ids)),
                "binary_observations": binary_observations,
                "missing_observations": missing_observations,
                "mean_rollcall_binary_participation": f"{mean_rc_participation:.6f}",
                "min_member_binary_participation": f"{member_values[0]:.6f}" if member_values else "",
                "median_member_binary_participation": f"{median(member_values):.6f}" if member_values else "",
                "max_member_binary_participation": f"{member_values[-1]:.6f}" if member_values else "",
                "members_participation_gte_050": sum(value >= 0.50 for value in member_values),
                "members_participation_gte_075": sum(value >= 0.75 for value in member_values),
                "members_participation_gte_090": sum(value >= 0.90 for value in member_values),
                "topics_represented": len({topic_value[vote_id] for vote_id in selected}),
                "origins_represented": len({origin_value[vote_id] for vote_id in selected}),
            })

    write_csv(SENSITIVITY_OUTPUT, sensitivity, SENSITIVITY_FIELDS)
    topic_rows = breakdown_rows("topic", topic_value, all_vote_ids, nonunanimous_ids, specs)
    origin_rows = breakdown_rows("origin", origin_value, all_vote_ids, nonunanimous_ids, specs)
    write_csv(TOPIC_OUTPUT, topic_rows, BREAKDOWN_FIELDS)
    write_csv(ORIGIN_OUTPUT, origin_rows, BREAKDOWN_FIELDS)

    diagnostics = {
        "generated_for": str(date.today()),
        "rollcalls": len(all_vote_ids),
        "nonunanimous_rollcalls": len(nonunanimous_ids),
        "members": EXPECTED_MEMBERS,
        "topics": len(set(topic_value.values())),
        "origins": dict(Counter(origin_value.values())),
        "minority_share_thresholds": list(MINORITY_THRESHOLDS),
        "rollcall_binary_participation_floors": list(ROLLCALL_PARTICIPATION_FLOORS),
        "member_participation_reporting_floors": list(MEMBER_PARTICIPATION_FLOORS),
        "specifications_tested": len(specs),
        "recommended_spec": None,
        "method_note": (
            "Auditoría de sensibilidad previa a cualquier estimación espacial. Cada especificación exige una minoría "
            "binaria no nula, un piso de proporción minoritaria y un piso de participación binaria de la Cámara. "
            "Se reporta retención por tema/origen y participación de legisladores. No se selecciona una especificación, "
            "no se estiman puntos ideales y no se orienta ningún eje ideológico."
        ),
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))

    if len(all_vote_ids) != 364:
        raise RuntimeError(f"Se esperaban 364 roll calls; hay {len(all_vote_ids)}")
    if len(votes) != 56420:
        raise RuntimeError(f"Se esperaban 56.420 votos nominales; hay {len(votes)}")
    if not sensitivity:
        raise RuntimeError("No se generaron especificaciones de sensibilidad")


if __name__ == "__main__":
    main()
