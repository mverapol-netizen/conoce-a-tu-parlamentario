from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
AGGREGATE = OUT / "member_modal_agreement_loo.csv"
VOTES = OUT / "member_votes_enriched.csv"
GROUPS = OUT / "group_rollcall_behavior.csv"
PUBLIC_JS = ROOT / "assets" / "js" / "modal_agreement.js"
PUBLIC_DETAILS = ROOT / "assets" / "data" / "modal_agreement_details.json"
DIAGNOSTICS = OUT / "member_modal_agreement_public_diagnostics.json"

PUBLIC_SCOPE = "minority_ge_10"
PUBLIC_THRESHOLD = 0.10
MIN_PUBLIC_COMPARISONS = 20
SUBSTANTIVE = ("Afirmativo", "En Contra", "Abstención")
OPTION_CODES = {
    "Afirmativo": "A",
    "En Contra": "E",
    "Abstención": "B",
}


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def leave_one_out_mode(group: dict, member_option: str) -> str:
    counts = {
        "Afirmativo": int(group.get("n_affirmative") or 0),
        "En Contra": int(group.get("n_against") or 0),
        "Abstención": int(group.get("n_abstention") or 0),
    }
    if member_option not in counts or counts[member_option] <= 0:
        return ""
    counts[member_option] -= 1
    if sum(counts.values()) < 2:
        return ""
    top = max(counts.values())
    winners = [option for option, count in counts.items() if count == top and top > 0]
    return winners[0] if len(winners) == 1 else ""


def status_for(comparisons: int) -> str:
    if comparisons >= MIN_PUBLIC_COMPARISONS:
        return "available"
    if comparisons > 0:
        return "insufficient"
    return "unavailable"


def main() -> None:
    aggregate = read_csv(AGGREGATE)
    votes = read_csv(VOTES)
    groups = read_csv(GROUPS)

    public_rows = [row for row in aggregate if row.get("scope") == PUBLIC_SCOPE]
    if not public_rows:
        raise RuntimeError(f"No existen filas para scope público {PUBLIC_SCOPE}")

    summaries: dict[str, dict] = defaultdict(dict)
    names: dict[str, str] = {}
    status_counts = {"party": defaultdict(int), "caucus": defaultdict(int)}

    for row in public_rows:
        deputy_id = row["diputado_id"]
        group_type = row["group_type"]
        comparisons = int(row.get("comparisons") or 0)
        matches = int(row.get("matches") or 0)
        divergences = int(row.get("divergences") or 0)
        agreement = float(row["agreement_pct"]) if row.get("agreement_pct") else None
        group_names = [name for name in (row.get("group_names_observed") or "").split(";") if name]
        status = status_for(comparisons)
        status_counts[group_type][status] += 1
        names[deputy_id] = row["diputado_nombre"]
        summaries[deputy_id][group_type] = {
            "status": status,
            "comparisons": comparisons,
            "matches": matches,
            "divergences": divergences,
            "agreementPct": agreement,
            "groups": group_names,
        }

    group_lookup = {
        (row["vote_id"], row["group_type"], row["group_name"]): row
        for row in groups
    }
    if len(group_lookup) != len(groups):
        raise RuntimeError("group_rollcall_behavior.csv contiene claves duplicadas")

    details: dict[str, dict[str, list]] = defaultdict(lambda: {"party": [], "caucus": []})
    detail_counts = {"party": 0, "caucus": 0}
    lookup_missing = []

    for vote in votes:
        option = vote.get("opcion", "")
        if option not in SUBSTANTIVE:
            continue
        deputy_id = vote["diputado_id"]

        for group_type, field in (("party", "party_at_vote"), ("caucus", "caucus_at_vote")):
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
                continue
            if float(group.get("chamber_binary_minority_share") or 0.0) < PUBLIC_THRESHOLD:
                continue

            peer_modal = leave_one_out_mode(group, option)
            if not peer_modal:
                continue

            match = option == peer_modal
            details[deputy_id][group_type].append([
                vote["vote_id"],
                group_name,
                OPTION_CODES[option],
                OPTION_CODES[peer_modal],
                1 if match else 0,
            ])
            detail_counts[group_type] += 1

    if lookup_missing:
        raise RuntimeError(f"Faltan {len(lookup_missing)} relaciones voto × grupo en el activo público")

    for deputy_id, group_details in details.items():
        for group_type in ("party", "caucus"):
            group_details[group_type].sort(key=lambda row: int(row[0]))

    public_members = {}
    all_ids = sorted({row["diputado_id"] for row in public_rows}, key=int)
    for deputy_id in all_ids:
        public_members[deputy_id] = {
            "name": names.get(deputy_id, ""),
            "party": summaries.get(deputy_id, {}).get("party", {
                "status": "unavailable", "comparisons": 0, "matches": 0,
                "divergences": 0, "agreementPct": None, "groups": [],
            }),
            "caucus": summaries.get(deputy_id, {}).get("caucus", {
                "status": "unavailable", "comparisons": 0, "matches": 0,
                "divergences": 0, "agreementPct": None, "groups": [],
            }),
        }

    payload = {
        "meta": {
            "scope": PUBLIC_SCOPE,
            "chamberMinorityThreshold": PUBLIC_THRESHOLD,
            "minPublicComparisons": MIN_PUBLIC_COMPARISONS,
            "method": "leave-one-out modal agreement",
            "note": (
                "El voto de la persona se retira antes de calcular la moda de sus pares. "
                "Solo se comparan Afirmativo, En Contra y Abstención cuando hay al menos dos decisiones de pares y moda única."
            ),
        },
        "members": public_members,
    }

    PUBLIC_JS.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_JS.write_text(
        "window.LEGISLATIVE_MODAL_AGREEMENT = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )

    PUBLIC_DETAILS.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_DETAILS.write_text(
        json.dumps({"members": details}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    expected_party = sum(
        int(row["comparisons"])
        for row in public_rows
        if row["group_type"] == "party"
    )
    expected_caucus = sum(
        int(row["comparisons"])
        for row in public_rows
        if row["group_type"] == "caucus"
    )

    diagnostics = {
        "public_scope": PUBLIC_SCOPE,
        "public_threshold": PUBLIC_THRESHOLD,
        "min_public_comparisons": MIN_PUBLIC_COMPARISONS,
        "members": len(public_members),
        "summary_status_counts": {
            group_type: dict(status_counts[group_type])
            for group_type in ("party", "caucus")
        },
        "expected_detail_rows": {
            "party": expected_party,
            "caucus": expected_caucus,
        },
        "generated_detail_rows": detail_counts,
        "lookup_missing": 0,
        "method_note": (
            "Activo público del corte 10%; los porcentajes solo se muestran si hay al menos 20 comparaciones. "
            "Las filas de detalle conservan vote_id, grupo vigente, opción individual, moda leave-one-out y coincidencia/divergencia."
        ),
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if len(public_members) != len(all_ids):
        raise RuntimeError("El activo público perdió integrantes")
    if detail_counts["party"] != expected_party:
        raise RuntimeError(f"Detalle partido no reproduce agregados: {detail_counts['party']}/{expected_party}")
    if detail_counts["caucus"] != expected_caucus:
        raise RuntimeError(f"Detalle bancada no reproduce agregados: {detail_counts['caucus']}/{expected_caucus}")

    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
