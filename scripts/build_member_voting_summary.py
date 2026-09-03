from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
VOTES = OUT / "member_votes_enriched.csv"
GROUPS = OUT / "group_rollcall_behavior.csv"
AGREEMENT_OUT = OUT / "member_modal_agreement.csv"
DIAGNOSTICS = OUT / "member_voting_summary_diagnostics.json"

SUBSTANTIVE = {"Afirmativo", "En Contra", "Abstención"}
SCOPES = (
    ("all", 0.00),
    ("minority_ge_05", 0.05),
    ("minority_ge_10", 0.10),
    ("minority_ge_20", 0.20),
)

AGREEMENT_FIELDS = [
    "diputado_id", "diputado_nombre", "group_type", "scope", "min_chamber_binary_minority_share",
    "comparisons", "matches", "divergences", "agreement_pct", "group_names_observed",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(num: int, den: int) -> str:
    return f"{100 * num / den:.4f}" if den else ""


def main() -> None:
    votes = read_csv(VOTES)
    groups = read_csv(GROUPS)
    if not votes or not groups:
        raise RuntimeError("Las tablas de entrada están vacías")

    group_lookup = {
        (x["vote_id"], x["group_type"], x["group_name"]): x
        for x in groups
    }
    if len(group_lookup) != len(groups):
        raise RuntimeError("group_rollcall_behavior.csv contiene claves duplicadas")

    by_member: dict[str, list[dict]] = defaultdict(list)
    for row in votes:
        by_member[row["diputado_id"]].append(row)

    agreement_rows = []
    lookup_missing = []

    for deputy_id, member_votes in sorted(by_member.items(), key=lambda item: int(item[0])):
        member_votes.sort(key=lambda x: (x["fecha"], x["vote_id"]))
        name = member_votes[0]["diputado_nombre"]

        for group_type, field in (("party", "party_at_vote"), ("caucus", "caucus_at_vote")):
            observed_names = sorted({x[field] for x in member_votes if x.get(field)})
            for scope, threshold in SCOPES:
                comparisons = 0
                matches = 0
                divergences = 0
                for vote in member_votes:
                    if vote["opcion"] not in SUBSTANTIVE:
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
                    if group.get("modal_eligible") != "1" or not group.get("modal_position"):
                        continue
                    minority = float(group.get("chamber_binary_minority_share") or 0.0)
                    if minority < threshold:
                        continue
                    comparisons += 1
                    if vote["opcion"] == group["modal_position"]:
                        matches += 1
                    else:
                        divergences += 1

                agreement_rows.append({
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

    agreement_rows.sort(key=lambda x: (int(x["diputado_id"]), x["group_type"], x["min_chamber_binary_minority_share"]))
    with AGREEMENT_OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AGREEMENT_FIELDS)
        writer.writeheader()
        writer.writerows(agreement_rows)

    scope_diagnostics = {}
    for group_type in ("party", "caucus"):
        for scope, _ in SCOPES:
            subset = [x for x in agreement_rows if x["group_type"] == group_type and x["scope"] == scope]
            eligible_members = [x for x in subset if int(x["comparisons"]) > 0]
            weighted_matches = sum(int(x["matches"]) for x in eligible_members)
            weighted_comparisons = sum(int(x["comparisons"]) for x in eligible_members)
            scope_diagnostics[f"{group_type}:{scope}"] = {
                "members_with_comparisons": len(eligible_members),
                "comparisons": weighted_comparisons,
                "matches": weighted_matches,
                "weighted_agreement_pct": round(100 * weighted_matches / weighted_comparisons, 4) if weighted_comparisons else None,
            }

    diagnostics = {
        "input_enriched_vote_rows": len(votes),
        "historical_members_with_enriched_votes": len(by_member),
        "modal_agreement_rows": len(agreement_rows),
        "lookup_missing": len(lookup_missing),
        "scope_diagnostics": scope_diagnostics,
        "method_note": (
            "Coincidencia modal es descriptiva, no una medida causal de disciplina. Solo compara Afirmativo/En Contra/Abstención "
            "cuando el grupo formal tiene al menos dos votos sustantivos y una moda única. No Vota y Dispensado no cuentan como "
            "divergencia. Los scopes 5/10/20% permiten sensibilidad a cuán dividida estaba la Cámara. La participación individual "
            "se calcula ahora en un pipeline independiente desde member_votes.csv."
        ),
        "errors": {"lookup_missing_examples": lookup_missing[:20]},
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in diagnostics.items() if k != "errors"}, ensure_ascii=False, indent=2))

    if lookup_missing:
        raise RuntimeError(f"Faltan {len(lookup_missing)} relaciones voto×grupo en la tabla de primitivas")
    expected_rows = len(by_member) * 2 * len(SCOPES)
    if len(agreement_rows) != expected_rows:
        raise RuntimeError(f"Resumen modal incompleto: {len(agreement_rows)}/{expected_rows} filas")


if __name__ == "__main__":
    main()
