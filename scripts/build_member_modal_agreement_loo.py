from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
VOTES = OUT / "member_votes_enriched.csv"
GROUPS = OUT / "group_rollcall_behavior.csv"
INCLUSIVE = OUT / "member_modal_agreement.csv"
OUTPUT = OUT / "member_modal_agreement_loo.csv"
DIAGNOSTICS = OUT / "member_modal_agreement_loo_diagnostics.json"

SUBSTANTIVE = ("Afirmativo", "En Contra", "Abstención")
SCOPES = (
    ("all", 0.00),
    ("minority_ge_05", 0.05),
    ("minority_ge_10", 0.10),
    ("minority_ge_20", 0.20),
)

FIELDS = [
    "diputado_id",
    "diputado_nombre",
    "group_type",
    "scope",
    "min_chamber_binary_minority_share",
    "comparisons",
    "matches",
    "divergences",
    "agreement_pct",
    "group_names_observed",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(num: int, den: int) -> str:
    return f"{100 * num / den:.4f}" if den else ""


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - pos) + ordered[hi] * (pos - lo)


def leave_one_out_mode(group: dict, member_option: str) -> tuple[str, str]:
    counts = {
        "Afirmativo": int(group.get("n_affirmative") or 0),
        "En Contra": int(group.get("n_against") or 0),
        "Abstención": int(group.get("n_abstention") or 0),
    }
    if member_option not in counts or counts[member_option] <= 0:
        return "", "member_not_in_group_counts"

    counts[member_option] -= 1
    peer_substantive = sum(counts.values())
    if peer_substantive < 2:
        return "", "fewer_than_two_peer_decisions"

    top = max(counts.values())
    winners = [option for option, count in counts.items() if count == top and top > 0]
    if len(winners) != 1:
        return "", "peer_modal_tie"
    return winners[0], "eligible"


def main() -> None:
    votes = read_csv(VOTES)
    groups = read_csv(GROUPS)
    inclusive_rows = read_csv(INCLUSIVE)
    if not votes or not groups:
        raise RuntimeError("Las tablas de entrada están vacías")

    group_lookup = {
        (row["vote_id"], row["group_type"], row["group_name"]): row
        for row in groups
    }
    if len(group_lookup) != len(groups):
        raise RuntimeError("group_rollcall_behavior.csv contiene claves duplicadas")

    by_member: dict[str, list[dict]] = defaultdict(list)
    for row in votes:
        by_member[row["diputado_id"]].append(row)

    rows_out = []
    exclusion_reasons = Counter()
    lookup_missing = []

    for deputy_id, member_votes in sorted(by_member.items(), key=lambda item: int(item[0])):
        member_votes.sort(key=lambda row: (row["fecha"], row["vote_id"]))
        name = member_votes[0]["diputado_nombre"]

        for group_type, field in (("party", "party_at_vote"), ("caucus", "caucus_at_vote")):
            observed_names = sorted({row.get(field, "") for row in member_votes if row.get(field, "")})

            for scope, threshold in SCOPES:
                comparisons = 0
                matches = 0
                divergences = 0

                for vote in member_votes:
                    option = vote.get("opcion", "")
                    if option not in SUBSTANTIVE:
                        exclusion_reasons["member_non_substantive"] += 1
                        continue

                    group_name = vote.get(field, "")
                    group = group_lookup.get((vote["vote_id"], group_type, group_name))
                    if group is None:
                        lookup_missing.append({
                            "vote_id": vote["vote_id"],
                            "diputado_id": deputy_id,
                            "group_type": group_type,
                            "group_name": group_name,
                        })
                        continue

                    if group.get("formal_group") != "1":
                        exclusion_reasons[f"{group_type}:not_formal_group"] += 1
                        continue

                    chamber_minority = float(group.get("chamber_binary_minority_share") or 0.0)
                    if chamber_minority < threshold:
                        exclusion_reasons[f"{group_type}:{scope}:below_chamber_threshold"] += 1
                        continue

                    peer_modal, reason = leave_one_out_mode(group, option)
                    if reason != "eligible":
                        exclusion_reasons[f"{group_type}:{reason}"] += 1
                        continue

                    comparisons += 1
                    if option == peer_modal:
                        matches += 1
                    else:
                        divergences += 1

                rows_out.append({
                    "diputado_id": deputy_id,
                    "diputado_nombre": name,
                    "group_type": group_type,
                    "scope": scope,
                    "min_chamber_binary_minority_share": f"{threshold:.2f}",
                    "comparisons": comparisons,
                    "matches": matches,
                    "divergences": divergences,
                    "agreement_pct": pct(matches, comparisons),
                    "group_names_observed": ";".join(observed_names),
                })

    rows_out.sort(key=lambda row: (
        int(row["diputado_id"]),
        row["group_type"],
        float(row["min_chamber_binary_minority_share"]),
    ))
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows_out)

    lookup = {
        (row["diputado_id"], row["group_type"], row["scope"]): row
        for row in rows_out
    }
    inclusive_lookup = {
        (row["diputado_id"], row["group_type"], row["scope"]): row
        for row in inclusive_rows
    }

    scope_diagnostics = {}
    for group_type in ("party", "caucus"):
        for scope, threshold in SCOPES:
            subset = [row for row in rows_out if row["group_type"] == group_type and row["scope"] == scope]
            eligible = [row for row in subset if int(row["comparisons"]) > 0]
            total_comparisons = sum(int(row["comparisons"]) for row in eligible)
            total_matches = sum(int(row["matches"]) for row in eligible)
            comparison_counts = [int(row["comparisons"]) for row in eligible]
            agreement_values = [float(row["agreement_pct"]) for row in eligible if row["agreement_pct"]]
            scope_diagnostics[f"{group_type}:{scope}"] = {
                "threshold": threshold,
                "members_with_comparisons": len(eligible),
                "comparisons": total_comparisons,
                "matches": total_matches,
                "weighted_agreement_pct": round(100 * total_matches / total_comparisons, 4) if total_comparisons else None,
                "median_member_comparisons": median(comparison_counts) if comparison_counts else None,
                "p10_member_comparisons": round(quantile(comparison_counts, 0.10), 2) if comparison_counts else None,
                "median_member_agreement_pct": round(median(agreement_values), 4) if agreement_values else None,
                "members_lt_20_comparisons": sum(value < 20 for value in comparison_counts),
            }

    sensitivity = {}
    pairs = (
        ("all", "minority_ge_10"),
        ("minority_ge_05", "minority_ge_10"),
        ("minority_ge_10", "minority_ge_20"),
    )
    for group_type in ("party", "caucus"):
        for left_scope, right_scope in pairs:
            diffs = []
            largest = []
            for deputy_id in by_member:
                left = lookup.get((deputy_id, group_type, left_scope))
                right = lookup.get((deputy_id, group_type, right_scope))
                if not left or not right or not left["agreement_pct"] or not right["agreement_pct"]:
                    continue
                diff = float(right["agreement_pct"]) - float(left["agreement_pct"])
                diffs.append(abs(diff))
                largest.append({
                    "diputado_id": deputy_id,
                    "diputado_nombre": left["diputado_nombre"],
                    "left_pct": float(left["agreement_pct"]),
                    "right_pct": float(right["agreement_pct"]),
                    "difference_pp": round(diff, 4),
                    "left_comparisons": int(left["comparisons"]),
                    "right_comparisons": int(right["comparisons"]),
                })
            largest.sort(key=lambda row: abs(row["difference_pp"]), reverse=True)
            sensitivity[f"{group_type}:{left_scope}_vs_{right_scope}"] = {
                "members_compared": len(diffs),
                "median_abs_difference_pp": round(median(diffs), 4) if diffs else None,
                "p90_abs_difference_pp": round(quantile(diffs, 0.90), 4) if diffs else None,
                "max_abs_difference_pp": round(max(diffs), 4) if diffs else None,
                "largest_changes": largest[:10],
            }

    loo_effect = {}
    for group_type in ("party", "caucus"):
        for scope, _threshold in SCOPES:
            diffs = []
            abs_diffs = []
            lost_comparability = []
            for deputy_id in by_member:
                loo = lookup.get((deputy_id, group_type, scope))
                inclusive = inclusive_lookup.get((deputy_id, group_type, scope))
                if not loo or not inclusive:
                    continue
                if inclusive.get("agreement_pct") and not loo.get("agreement_pct"):
                    lost_comparability.append({
                        "diputado_id": deputy_id,
                        "diputado_nombre": inclusive["diputado_nombre"],
                        "inclusive_comparisons": int(inclusive["comparisons"]),
                    })
                    continue
                if not loo.get("agreement_pct") or not inclusive.get("agreement_pct"):
                    continue
                diff = float(loo["agreement_pct"]) - float(inclusive["agreement_pct"])
                diffs.append(diff)
                abs_diffs.append(abs(diff))
            loo_effect[f"{group_type}:{scope}"] = {
                "members_compared": len(diffs),
                "median_difference_pp_loo_minus_inclusive": round(median(diffs), 4) if diffs else None,
                "median_abs_difference_pp": round(median(abs_diffs), 4) if abs_diffs else None,
                "p90_abs_difference_pp": round(quantile(abs_diffs, 0.90), 4) if abs_diffs else None,
                "max_abs_difference_pp": round(max(abs_diffs), 4) if abs_diffs else None,
                "members_losing_comparability": len(lost_comparability),
                "lost_comparability_examples": lost_comparability[:20],
            }

    diagnostics = {
        "input_enriched_vote_rows": len(votes),
        "historical_members_observed": len(by_member),
        "output_rows": len(rows_out),
        "lookup_missing": len(lookup_missing),
        "scope_diagnostics": scope_diagnostics,
        "threshold_sensitivity": sensitivity,
        "leave_one_out_effect_vs_inclusive": loo_effect,
        "exclusion_reasons": dict(sorted(exclusion_reasons.items())),
        "method_note": (
            "Coincidencia modal leave-one-out: el voto de la persona se elimina antes de calcular la posición más frecuente de su grupo. "
            "Se requieren al menos dos decisiones sustantivas de pares y una moda única. No Vota y Dispensado no se comparan. "
            "Los scopes filtran según la proporción minoritaria Afirmativo/En Contra de toda la Cámara, no según la división interna del grupo."
        ),
        "errors": {"lookup_missing_examples": lookup_missing[:20]},
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in diagnostics.items() if key not in {"errors", "exclusion_reasons"}}, ensure_ascii=False, indent=2))

    if lookup_missing:
        raise RuntimeError(f"Faltan {len(lookup_missing)} relaciones voto × grupo")
    expected_rows = len(by_member) * 2 * len(SCOPES)
    if len(rows_out) != expected_rows:
        raise RuntimeError(f"Salida incompleta: {len(rows_out)}/{expected_rows} filas")


if __name__ == "__main__":
    main()
