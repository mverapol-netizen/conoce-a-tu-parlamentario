from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean, median, pstdev

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "legislative" / "2026"
WNOM = BASE / "wnominate"
COORDS = WNOM / "member_coordinates.csv"
ENRICHED = BASE / "member_votes_enriched.csv"

STABILITY_OUT = WNOM / "member_stability_audit.csv"
EXCLUSIONS_OUT = WNOM / "member_exclusions.csv"
GROUP_OUT = WNOM / "group_position_summary.csv"
ASSOCIATION_OUT = WNOM / "group_association_diagnostics.csv"
DIAGNOSTICS_OUT = WNOM / "stability_audit_diagnostics.json"

BASELINE = "raw_lop025"


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def number(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper() in {"NA", "NAN", "NULL"}:
        return None
    try:
        x = float(text)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def mode_with_share(values: list[str]) -> tuple[str, float]:
    cleaned = [str(x).strip() for x in values if str(x).strip()]
    if not cleaned:
        return "", 0.0
    counts = Counter(cleaned)
    top_n = max(counts.values())
    top = sorted(k for k, v in counts.items() if v == top_n)[0]
    return top, top_n / len(cleaned)


def quantile(values: list[float], p: float) -> float | None:
    values = sorted(values)
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    pos = (len(values) - 1) * p
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return values[lo]
    frac = pos - lo
    return values[lo] * (1 - frac) + values[hi] * frac


def zscores(values_by_id: dict[str, float | None]) -> dict[str, float | None]:
    present = [x for x in values_by_id.values() if x is not None]
    if len(present) < 2:
        return {k: None for k in values_by_id}
    mu = mean(present)
    sd = pstdev(present)
    if sd == 0:
        return {k: (0.0 if v is not None else None) for k, v in values_by_id.items()}
    return {k: ((v - mu) / sd if v is not None else None) for k, v in values_by_id.items()}


def ranks(values_by_id: dict[str, float | None]) -> dict[str, int | None]:
    present = sorted(
        ((member_id, value) for member_id, value in values_by_id.items() if value is not None),
        key=lambda x: (x[1], x[0]),
    )
    return {**{member_id: None for member_id in values_by_id}, **{member_id: idx for idx, (member_id, _) in enumerate(present, 1)}}


def eta_squared(values: dict[str, float | None], groups: dict[str, str]) -> tuple[float | None, int, int]:
    rows = [(member_id, value, groups.get(member_id, "")) for member_id, value in values.items()]
    rows = [(i, v, g) for i, v, g in rows if v is not None and g]
    if len(rows) < 3:
        return None, len(rows), 0
    grand = mean(v for _, v, _ in rows)
    by_group: dict[str, list[float]] = defaultdict(list)
    for _, value, group in rows:
        by_group[group].append(value)
    total_ss = sum((v - grand) ** 2 for _, v, _ in rows)
    between_ss = sum(len(vals) * (mean(vals) - grand) ** 2 for vals in by_group.values())
    eta = between_ss / total_ss if total_ss > 0 else None
    return eta, len(rows), len(by_group)


def main() -> None:
    coords = read_csv(COORDS)
    enriched = read_csv(ENRICHED)

    specs = list(dict.fromkeys(row["spec_id"] for row in coords))
    if BASELINE not in specs:
        raise RuntimeError(f"No existe especificación base {BASELINE}")

    names: dict[str, str] = {}
    coord_by_spec: dict[str, dict[str, float | None]] = {spec: {} for spec in specs}
    binary_votes_by_spec: dict[str, dict[str, int]] = {spec: {} for spec in specs}

    for row in coords:
        member_id = row["diputado_id"].strip()
        names[member_id] = row["diputado_nombre"].strip()
        coord_by_spec[row["spec_id"]][member_id] = number(row.get("dimension_1_aligned"))
        try:
            binary_votes_by_spec[row["spec_id"]][member_id] = int(float(row.get("binary_votes_selected", "0") or 0))
        except ValueError:
            binary_votes_by_spec[row["spec_id"]][member_id] = 0

    member_ids = sorted(names, key=lambda x: int(x) if x.isdigit() else x)
    for spec in specs:
        for member_id in member_ids:
            coord_by_spec[spec].setdefault(member_id, None)
            binary_votes_by_spec[spec].setdefault(member_id, 0)

    # Afiliación histórica modal por roll call. Conservamos la proporción modal
    # para detectar casos en que un diputado cambió de partido/bancada durante el período.
    party_values: dict[str, list[str]] = defaultdict(list)
    caucus_values: dict[str, list[str]] = defaultdict(list)
    alignment_values: dict[str, list[str]] = defaultdict(list)
    for row in enriched:
        member_id = row["diputado_id"].strip()
        party_values[member_id].append(row.get("party_at_vote", ""))
        caucus_values[member_id].append(row.get("caucus_at_vote", ""))
        alignment_values[member_id].append(row.get("alignment_at_vote", ""))

    affiliations: dict[str, dict] = {}
    for member_id in member_ids:
        party, party_share = mode_with_share(party_values.get(member_id, []))
        caucus, caucus_share = mode_with_share(caucus_values.get(member_id, []))
        alignment, alignment_share = mode_with_share(alignment_values.get(member_id, []))
        affiliations[member_id] = {
            "modal_party": party,
            "modal_party_share": party_share,
            "modal_caucus": caucus,
            "modal_caucus_share": caucus_share,
            "modal_alignment": alignment,
            "modal_alignment_share": alignment_share,
        }

    z_by_spec = {spec: zscores(coord_by_spec[spec]) for spec in specs}
    rank_by_spec = {spec: ranks(coord_by_spec[spec]) for spec in specs}

    stability_rows = []
    for member_id in member_ids:
        present_specs = [spec for spec in specs if z_by_spec[spec][member_id] is not None]
        zvals = [z_by_spec[spec][member_id] for spec in present_specs]
        rvals = [rank_by_spec[spec][member_id] for spec in present_specs]
        baseline_coord = coord_by_spec[BASELINE][member_id]
        baseline_z = z_by_spec[BASELINE][member_id]
        max_abs_z_shift = None
        if baseline_z is not None:
            comparisons = [abs(z_by_spec[spec][member_id] - baseline_z) for spec in present_specs]
            max_abs_z_shift = max(comparisons) if comparisons else 0.0

        row = {
            "diputado_id": member_id,
            "diputado_nombre": names[member_id],
            **affiliations[member_id],
            "specs_estimated": len(present_specs),
            "baseline_coord_aligned": baseline_coord,
            "baseline_z": baseline_z,
            "baseline_binary_votes": binary_votes_by_spec[BASELINE][member_id],
            "max_abs_z_shift_from_baseline": max_abs_z_shift,
            "sd_z_across_specs": pstdev(zvals) if len(zvals) >= 2 else None,
            "min_rank": min(rvals) if rvals else None,
            "max_rank": max(rvals) if rvals else None,
            "rank_range": (max(rvals) - min(rvals)) if rvals else None,
        }
        for spec in specs:
            row[f"coord_{spec}"] = coord_by_spec[spec][member_id]
            row[f"z_{spec}"] = z_by_spec[spec][member_id]
            row[f"rank_{spec}"] = rank_by_spec[spec][member_id]
        stability_rows.append(row)

    stability_rows.sort(
        key=lambda row: (
            -(row["max_abs_z_shift_from_baseline"] if row["max_abs_z_shift_from_baseline"] is not None else -1),
            row["diputado_nombre"],
        )
    )

    stability_fields = [
        "diputado_id", "diputado_nombre",
        "modal_party", "modal_party_share", "modal_caucus", "modal_caucus_share",
        "modal_alignment", "modal_alignment_share",
        "specs_estimated", "baseline_coord_aligned", "baseline_z", "baseline_binary_votes",
        "max_abs_z_shift_from_baseline", "sd_z_across_specs", "min_rank", "max_rank", "rank_range",
    ]
    for spec in specs:
        stability_fields.extend([f"coord_{spec}", f"z_{spec}", f"rank_{spec}"])
    write_csv(STABILITY_OUT, stability_rows, stability_fields)

    exclusions = []
    for spec in specs:
        for member_id in member_ids:
            if coord_by_spec[spec][member_id] is None:
                exclusions.append({
                    "spec_id": spec,
                    "diputado_id": member_id,
                    "diputado_nombre": names[member_id],
                    "binary_votes_selected": binary_votes_by_spec[spec][member_id],
                    "reason": "Menos de minvotes=20 votos binarios en la especificación" if binary_votes_by_spec[spec][member_id] < 20 else "Excluido/no estimado por W-NOMINATE",
                })
    write_csv(
        EXCLUSIONS_OUT,
        exclusions,
        ["spec_id", "diputado_id", "diputado_nombre", "binary_votes_selected", "reason"],
    )

    group_rows = []
    association_rows = []
    group_fields_map = {
        "party": "modal_party",
        "caucus": "modal_caucus",
        "alignment": "modal_alignment",
    }

    for spec in specs:
        values = coord_by_spec[spec]
        zvalues = z_by_spec[spec]
        for group_type, field in group_fields_map.items():
            groups = {member_id: affiliations[member_id][field] for member_id in member_ids}
            by_group: dict[str, list[float]] = defaultdict(list)
            by_group_z: dict[str, list[float]] = defaultdict(list)
            for member_id in member_ids:
                value = values[member_id]
                zvalue = zvalues[member_id]
                group = groups.get(member_id, "")
                if value is not None and group:
                    by_group[group].append(value)
                    by_group_z[group].append(zvalue)

            for group, vals in sorted(by_group.items()):
                zvals_group = by_group_z[group]
                group_rows.append({
                    "spec_id": spec,
                    "group_type": group_type,
                    "group": group,
                    "n_members": len(vals),
                    "mean_coord": mean(vals),
                    "median_coord": median(vals),
                    "q25_coord": quantile(vals, 0.25),
                    "q75_coord": quantile(vals, 0.75),
                    "min_coord": min(vals),
                    "max_coord": max(vals),
                    "mean_z": mean(zvals_group),
                })

            eta, n_members, n_groups = eta_squared(zvalues, groups)
            association_rows.append({
                "spec_id": spec,
                "group_type": group_type,
                "n_members": n_members,
                "n_groups": n_groups,
                "eta_squared_descriptive": eta,
                "interpretation": "Fracción descriptiva de varianza de la coordenada 1D asociada a diferencias entre grupos; no implica causalidad ni valida por sí sola una etiqueta ideológica.",
            })

    write_csv(
        GROUP_OUT,
        group_rows,
        [
            "spec_id", "group_type", "group", "n_members", "mean_coord", "median_coord",
            "q25_coord", "q75_coord", "min_coord", "max_coord", "mean_z",
        ],
    )
    write_csv(
        ASSOCIATION_OUT,
        association_rows,
        ["spec_id", "group_type", "n_members", "n_groups", "eta_squared_descriptive", "interpretation"],
    )

    unstable = [row for row in stability_rows if row["max_abs_z_shift_from_baseline"] is not None]
    rank_unstable = sorted(
        (row for row in stability_rows if row["rank_range"] is not None),
        key=lambda row: (-row["rank_range"], row["diputado_nombre"]),
    )
    changed_party = [
        row for row in stability_rows
        if row["modal_party_share"] < 0.999 and row["modal_party"]
    ]
    changed_caucus = [
        row for row in stability_rows
        if row["modal_caucus_share"] < 0.999 and row["modal_caucus"]
    ]

    baseline_groups = {
        row["group_type"]: row["eta_squared_descriptive"]
        for row in association_rows if row["spec_id"] == BASELINE
    }

    diagnostics = {
        "generated_for": str(date.today()),
        "status": "PASS",
        "specifications": specs,
        "members": len(member_ids),
        "members_estimated_baseline": sum(coord_by_spec[BASELINE][x] is not None for x in member_ids),
        "exclusion_rows_across_specs": len(exclusions),
        "baseline_excluded_members": [
            {
                "diputado_id": row["diputado_id"],
                "diputado_nombre": row["diputado_nombre"],
                "binary_votes_selected": row["binary_votes_selected"],
            }
            for row in exclusions if row["spec_id"] == BASELINE
        ],
        "most_sensitive_by_standardized_coordinate": [
            {
                "diputado_id": row["diputado_id"],
                "diputado_nombre": row["diputado_nombre"],
                "max_abs_z_shift": round(row["max_abs_z_shift_from_baseline"], 6),
                "rank_range": row["rank_range"],
            }
            for row in unstable[:15]
        ],
        "largest_rank_ranges": [
            {
                "diputado_id": row["diputado_id"],
                "diputado_nombre": row["diputado_nombre"],
                "rank_range": row["rank_range"],
                "max_abs_z_shift": round(row["max_abs_z_shift_from_baseline"], 6) if row["max_abs_z_shift_from_baseline"] is not None else None,
            }
            for row in rank_unstable[:15]
        ],
        "members_with_party_variation_over_rollcalls": len(changed_party),
        "members_with_caucus_variation_over_rollcalls": len(changed_caucus),
        "baseline_eta_squared_descriptive": baseline_groups,
        "method_note": (
            "La auditoría estandariza cada especificación antes de medir desplazamientos individuales, "
            "porque la escala absoluta de W-NOMINATE puede cambiar entre corridas. Partido, bancada y "
            "alineamiento son modales históricos por roll call; sus shares permiten detectar cambios. "
            "Eta² se usa solo como asociación descriptiva, no como interpretación causal ni etiqueta del eje."
        ),
    }
    DIAGNOSTICS_OUT.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if len(member_ids) != 155:
        raise RuntimeError(f"Esperábamos 155 diputados en coordenadas: {len(member_ids)}")
    if diagnostics["members_estimated_baseline"] < 150:
        raise RuntimeError("La especificación base estima menos de 150 diputados")

    print(json.dumps({
        "members": diagnostics["members"],
        "members_estimated_baseline": diagnostics["members_estimated_baseline"],
        "exclusion_rows_across_specs": diagnostics["exclusion_rows_across_specs"],
        "members_with_party_variation_over_rollcalls": diagnostics["members_with_party_variation_over_rollcalls"],
        "members_with_caucus_variation_over_rollcalls": diagnostics["members_with_caucus_variation_over_rollcalls"],
        "baseline_eta_squared_descriptive": diagnostics["baseline_eta_squared_descriptive"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
