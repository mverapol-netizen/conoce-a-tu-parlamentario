from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"

VOTES_FILE = OUT / "member_votes_enriched.csv"
ROLLCALLS_FILE = OUT / "rollcalls.csv"
MATRIX_FILE = OUT / "rollcall_matrix_binary.csv"
ROLLCALL_META_FILE = OUT / "rollcall_matrix_metadata.csv"
MEMBER_META_FILE = OUT / "rollcall_member_metadata.csv"
DIAGNOSTICS_FILE = OUT / "rollcall_matrix_diagnostics.json"

YES_OPTIONS = {"afirmativo", "si", "sí"}
NO_OPTIONS = {"en contra", "negativo", "no"}
ABSTAIN_OPTIONS = {"abstencion", "abstención"}
NO_VOTE_OPTIONS = {"no vota"}
DISPENSED_OPTIONS = {"dispensado"}
EXPECTED_MEMBERS = 155
SENSITIVITY_THRESHOLDS = (0.0, 0.025, 0.05, 0.10)

ROLLCALL_META_FIELDS = [
    "vote_id",
    "fecha",
    "boletin",
    "descripcion",
    "affirmative",
    "against",
    "abstention",
    "no_vote",
    "dispensed",
    "other_missing",
    "binary_votes",
    "missing_for_spatial_model",
    "minority_count",
    "minority_share_binary",
    "binary_participation_share",
    "unanimous_binary",
]

MEMBER_META_FIELDS = [
    "diputado_id",
    "diputado_nombre",
    "binary_votes",
    "affirmative",
    "against",
    "missing_for_spatial_model",
    "binary_participation_share",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_option(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


def spatial_code(option: str) -> str:
    norm = normalize_option(option)
    if norm in YES_OPTIONS:
        return "1"
    if norm in NO_OPTIONS:
        return "0"
    return ""


def option_bucket(option: str) -> str:
    norm = normalize_option(option)
    if norm in YES_OPTIONS:
        return "affirmative"
    if norm in NO_OPTIONS:
        return "against"
    if norm in ABSTAIN_OPTIONS:
        return "abstention"
    if norm in NO_VOTE_OPTIONS:
        return "no_vote"
    if norm in DISPENSED_OPTIONS:
        return "dispensed"
    return "other_missing"


def vote_sort_key(vote_id: str):
    return (0, int(vote_id)) if vote_id.isdigit() else (1, vote_id)


def member_sort_key(member_id: str):
    return (0, int(member_id)) if member_id.isdigit() else (1, member_id)


def main() -> None:
    votes = read_csv(VOTES_FILE)
    rollcalls = read_csv(ROLLCALLS_FILE)
    rollcall_by_id = {row["vote_id"]: row for row in rollcalls}

    if len(rollcall_by_id) != len(rollcalls):
        raise RuntimeError("rollcalls.csv contiene vote_id duplicados")

    pair_keys = [(row["vote_id"], row["diputado_id"]) for row in votes]
    if len(pair_keys) != len(set(pair_keys)):
        raise RuntimeError("member_votes_enriched.csv contiene pares vote_id × diputado_id duplicados")

    by_vote: dict[str, list[dict]] = defaultdict(list)
    by_member: dict[str, list[dict]] = defaultdict(list)
    member_names: dict[str, str] = {}
    for row in votes:
        vote_id = (row.get("vote_id") or "").strip()
        member_id = (row.get("diputado_id") or "").strip()
        if not vote_id or not member_id:
            raise RuntimeError("Fila sin vote_id o diputado_id en member_votes_enriched.csv")
        if vote_id not in rollcall_by_id:
            raise RuntimeError(f"Voto nominal refiere a roll call inexistente: {vote_id}")
        by_vote[vote_id].append(row)
        by_member[member_id].append(row)
        member_names[member_id] = (row.get("diputado_nombre") or "").strip()

    if len(by_member) != EXPECTED_MEMBERS:
        raise RuntimeError(f"Se esperaban {EXPECTED_MEMBERS} diputados; aparecen {len(by_member)}")

    bad_rollcall_sizes = {vote_id: len(rows) for vote_id, rows in by_vote.items() if len(rows) != EXPECTED_MEMBERS}
    if bad_rollcall_sizes:
        raise RuntimeError(f"Roll calls sin {EXPECTED_MEMBERS} observaciones: {bad_rollcall_sizes}")

    ordered_vote_ids = sorted(rollcall_by_id, key=lambda vid: (
        rollcall_by_id[vid].get("fecha", ""),
        vote_sort_key(vid),
    ))
    ordered_member_ids = sorted(by_member, key=member_sort_key)

    # Matriz puramente binaria. Las categorías no binarias quedan vacías para que
    # ningún estimador posterior confunda abstención/no-voto con una posición 0.
    cell: dict[tuple[str, str], str] = {}
    rollcall_meta = []
    unknown_options = Counter()

    for vote_id in ordered_vote_ids:
        rows = by_vote.get(vote_id, [])
        counts = Counter()
        for row in rows:
            member_id = row["diputado_id"]
            code = spatial_code(row.get("opcion", ""))
            cell[(member_id, vote_id)] = code
            bucket = option_bucket(row.get("opcion", ""))
            counts[bucket] += 1
            if bucket == "other_missing":
                unknown_options[row.get("opcion", "")] += 1

        yes = counts["affirmative"]
        no = counts["against"]
        binary = yes + no
        missing = EXPECTED_MEMBERS - binary
        minority = min(yes, no) if binary else 0
        minority_share = minority / binary if binary else 0.0
        participation = binary / EXPECTED_MEMBERS
        rc = rollcall_by_id[vote_id]
        rollcall_meta.append({
            "vote_id": vote_id,
            "fecha": rc.get("fecha", ""),
            "boletin": rc.get("boletin", ""),
            "descripcion": rc.get("descripcion", ""),
            "affirmative": yes,
            "against": no,
            "abstention": counts["abstention"],
            "no_vote": counts["no_vote"],
            "dispensed": counts["dispensed"],
            "other_missing": counts["other_missing"],
            "binary_votes": binary,
            "missing_for_spatial_model": missing,
            "minority_count": minority,
            "minority_share_binary": f"{minority_share:.6f}",
            "binary_participation_share": f"{participation:.6f}",
            "unanimous_binary": "1" if binary > 0 and minority == 0 else "0",
        })

    with MATRIX_FILE.open("w", encoding="utf-8-sig", newline="") as handle:
        fields = ["diputado_id", "diputado_nombre", *ordered_vote_ids]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for member_id in ordered_member_ids:
            row = {
                "diputado_id": member_id,
                "diputado_nombre": member_names[member_id],
            }
            for vote_id in ordered_vote_ids:
                row[vote_id] = cell.get((member_id, vote_id), "")
            writer.writerow(row)

    with ROLLCALL_META_FILE.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ROLLCALL_META_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rollcall_meta)

    member_meta = []
    total_rollcalls = len(ordered_vote_ids)
    for member_id in ordered_member_ids:
        counts = Counter(option_bucket(row.get("opcion", "")) for row in by_member[member_id])
        binary = counts["affirmative"] + counts["against"]
        member_meta.append({
            "diputado_id": member_id,
            "diputado_nombre": member_names[member_id],
            "binary_votes": binary,
            "affirmative": counts["affirmative"],
            "against": counts["against"],
            "missing_for_spatial_model": total_rollcalls - binary,
            "binary_participation_share": f"{(binary / total_rollcalls if total_rollcalls else 0):.6f}",
        })

    with MEMBER_META_FILE.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MEMBER_META_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(member_meta)

    sensitivity = {}
    for threshold in SENSITIVITY_THRESHOLDS:
        eligible = [
            row for row in rollcall_meta
            if int(row["binary_votes"]) > 0
            and float(row["minority_share_binary"]) >= threshold
            and int(row["minority_count"]) > 0
        ]
        sensitivity[f"minority_share_gte_{threshold:.3f}"] = len(eligible)

    diagnostics = {
        "generated_for": str(date.today()),
        "source_member_vote_rows": len(votes),
        "members": len(ordered_member_ids),
        "rollcalls": len(ordered_vote_ids),
        "matrix_cells": len(ordered_member_ids) * len(ordered_vote_ids),
        "binary_cells": sum(1 for value in cell.values() if value in {"0", "1"}),
        "missing_cells_for_spatial_model": sum(1 for value in cell.values() if value == ""),
        "unanimous_binary_rollcalls": sum(row["unanimous_binary"] == "1" for row in rollcall_meta),
        "sensitivity_rollcalls_by_minority_share": sensitivity,
        "unknown_vote_options": dict(unknown_options),
        "coding": {
            "1": "Afirmativo",
            "0": "En Contra",
            "missing": "Abstención / No Vota / Dispensado / otra categoría no binaria",
        },
        "method_note": (
            "Esta salida prepara una matriz neutral. No selecciona aún un umbral de competitividad, "
            "no estima puntos ideales y no fija la orientación ideológica de futuras dimensiones."
        ),
    }
    DIAGNOSTICS_FILE.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if unknown_options:
        raise RuntimeError(f"Aparecieron opciones de voto no previstas: {dict(unknown_options)}")
    if len(cell) != len(votes):
        raise RuntimeError(f"La matriz no conserva todas las observaciones: {len(cell)}/{len(votes)}")

    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
