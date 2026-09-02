from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"
INPUT = OUT / "member_votes_enriched.csv"
OUTPUT = OUT / "group_rollcall_behavior.csv"
DIAGNOSTICS = OUT / "group_rollcall_behavior_diagnostics.json"

YES = "Afirmativo"
NO = "En Contra"
ABSTAIN = "Abstención"
NO_VOTE = "No Vota"
EXCUSED = "Dispensado"
SUBSTANTIVE = (YES, NO, ABSTAIN)

FIELDS = [
    "vote_id", "fecha", "boletin", "group_type", "group_name", "group_size",
    "n_affirmative", "n_against", "n_abstention", "n_no_vote", "n_excused",
    "n_substantive", "n_binary", "participation_substantive_pct",
    "yes_share_binary", "minority_share_binary", "rice_index",
    "modal_position", "modal_count", "modal_agreement_pct", "modal_tie",
    "formal_group", "rice_eligible", "modal_eligible",
    "chamber_affirmative", "chamber_against", "chamber_abstention", "chamber_no_vote",
    "chamber_excused", "chamber_binary_minority_share",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(num: int, den: int) -> str:
    return f"{100 * num / den:.4f}" if den else ""


def ratio(num: int, den: int) -> str:
    return f"{num / den:.6f}" if den else ""


def is_formal_group(group_type: str, name: str, group_size: int) -> bool:
    if group_size < 2:
        return False
    normalized = (name or "").strip().lower()
    if group_type == "party":
        return normalized not in {"independiente", "independientes", "sin información", "sin informacion", ""}
    return not (
        normalized in {"por definir", "bancada por confirmar", ""}
        or normalized.startswith("fuera del ")
    )


def modal_position(counts: Counter) -> tuple[str, int, bool]:
    values = {option: counts.get(option, 0) for option in SUBSTANTIVE}
    top = max(values.values()) if values else 0
    if top == 0:
        return "", 0, False
    winners = [option for option, count in values.items() if count == top]
    return (winners[0] if len(winners) == 1 else "", top, len(winners) > 1)


def main() -> None:
    rows = read_csv(INPUT)
    if not rows:
        raise RuntimeError("member_votes_enriched.csv está vacío")

    by_vote: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_vote[row["vote_id"]].append(row)

    output = []
    bad_rollcalls = {}
    unknown_options = Counter()

    for vote_id, members in by_vote.items():
        if len(members) != 155:
            bad_rollcalls[vote_id] = len(members)
            continue

        first = members[0]
        chamber = Counter(x["opcion"] for x in members)
        for option in chamber:
            if option not in {YES, NO, ABSTAIN, NO_VOTE, EXCUSED}:
                unknown_options[option] += chamber[option]
        chamber_binary = chamber[YES] + chamber[NO]
        chamber_minority = min(chamber[YES], chamber[NO]) / chamber_binary if chamber_binary else None

        for group_type, field in (("party", "party_at_vote"), ("caucus", "caucus_at_vote")):
            grouped: dict[str, list[dict]] = defaultdict(list)
            for member in members:
                grouped[member.get(field, "")].append(member)

            for group_name, group_members in sorted(grouped.items()):
                votes = Counter(x["opcion"] for x in group_members)
                group_size = len(group_members)
                n_yes = votes[YES]
                n_no = votes[NO]
                n_abstain = votes[ABSTAIN]
                n_no_vote = votes[NO_VOTE]
                n_excused = votes[EXCUSED]
                n_substantive = n_yes + n_no + n_abstain
                n_binary = n_yes + n_no
                modal, modal_count, modal_tie = modal_position(votes)
                formal = is_formal_group(group_type, group_name, group_size)
                rice_eligible = formal and n_binary >= 2
                modal_eligible = formal and n_substantive >= 2 and not modal_tie
                rice = abs(n_yes - n_no) / n_binary if n_binary else None

                output.append({
                    "vote_id": vote_id,
                    "fecha": first["fecha"],
                    "boletin": first.get("boletin", ""),
                    "group_type": group_type,
                    "group_name": group_name,
                    "group_size": group_size,
                    "n_affirmative": n_yes,
                    "n_against": n_no,
                    "n_abstention": n_abstain,
                    "n_no_vote": n_no_vote,
                    "n_excused": n_excused,
                    "n_substantive": n_substantive,
                    "n_binary": n_binary,
                    "participation_substantive_pct": pct(n_substantive, group_size),
                    "yes_share_binary": ratio(n_yes, n_binary),
                    "minority_share_binary": ratio(min(n_yes, n_no), n_binary),
                    "rice_index": f"{rice:.6f}" if rice is not None else "",
                    "modal_position": modal,
                    "modal_count": modal_count,
                    "modal_agreement_pct": pct(modal_count, n_substantive),
                    "modal_tie": "1" if modal_tie else "0",
                    "formal_group": "1" if formal else "0",
                    "rice_eligible": "1" if rice_eligible else "0",
                    "modal_eligible": "1" if modal_eligible else "0",
                    "chamber_affirmative": chamber[YES],
                    "chamber_against": chamber[NO],
                    "chamber_abstention": chamber[ABSTAIN],
                    "chamber_no_vote": chamber[NO_VOTE],
                    "chamber_excused": chamber[EXCUSED],
                    "chamber_binary_minority_share": f"{chamber_minority:.6f}" if chamber_minority is not None else "",
                })

    output.sort(key=lambda x: (
        x["fecha"],
        int(x["vote_id"]) if x["vote_id"].isdigit() else x["vote_id"],
        x["group_type"],
        x["group_name"],
    ))
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output)

    rice_values = [float(x["rice_index"]) for x in output if x["rice_eligible"] == "1" and x["rice_index"]]
    modal_values = [float(x["modal_agreement_pct"]) for x in output if x["modal_eligible"] == "1" and x["modal_agreement_pct"]]
    diagnostics = {
        "input_member_rows": len(rows),
        "rollcalls": len(by_vote),
        "output_group_rollcall_rows": len(output),
        "party_group_rollcall_rows": sum(x["group_type"] == "party" for x in output),
        "caucus_group_rollcall_rows": sum(x["group_type"] == "caucus" for x in output),
        "formal_group_rows": sum(x["formal_group"] == "1" for x in output),
        "rice_eligible_rows": len(rice_values),
        "modal_eligible_rows": len(modal_values),
        "mean_rice_eligible": round(sum(rice_values) / len(rice_values), 6) if rice_values else None,
        "mean_modal_agreement_pct_eligible": round(sum(modal_values) / len(modal_values), 4) if modal_values else None,
        "bad_rollcalls": bad_rollcalls,
        "unknown_vote_options": dict(unknown_options),
        "method_note": "Rice usa solo Afirmativo/En Contra. Abstenciones se conservan en modal_position. No Vota y Dispensado se excluyen de ambas medidas. Independientes como pseudo-partido, Por definir y Fuera de comité no son grupos formales para cohesión.",
    }
    DIAGNOSTICS.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))

    if bad_rollcalls:
        raise RuntimeError(f"Roll calls sin 155 filas: {bad_rollcalls}")
    if unknown_options:
        raise RuntimeError(f"Opciones de voto desconocidas: {dict(unknown_options)}")
    if len(by_vote) != 364:
        raise RuntimeError(f"Se esperaban 364 roll calls; hay {len(by_vote)}")


if __name__ == "__main__":
    main()
