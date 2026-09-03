from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "legislative" / "2026"
WN = DATA / "wnominate"
RESEARCH_1D = WN / "research_1d"
TWO_D = WN / "two_dimensional"
TOPICS = DATA / "topics"
OUT = WN / "interpretation"
OUT.mkdir(parents=True, exist_ok=True)

ROLLCALL_COORD_1D = RESEARCH_1D / "rollcall_coordinates_research.csv"
TOP_DIM2 = TWO_D / "top_dim2_rollcalls.csv"
ROLLCALLS = DATA / "rollcalls.csv"
PROJECTS = DATA / "projects.csv"
TOPIC_FINAL = TOPICS / "rollcall_inherited_topic_final.csv"
MEMBER_VOTES = DATA / "member_votes_enriched.csv"

DISPLAY_MULTIPLIER_D1 = -1.0
BASE_2D_SPEC = "raw_lop025_2d"
YES = "Afirmativo"
NO = "En Contra"
BINARY = {YES, NO}


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def as_float(value, default=None):
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value, default=0):
    try:
        if value in (None, ""):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def norm(value: str | None) -> str:
    return (value or "").strip()


def cluster_id(row: dict) -> str:
    boletin = norm(row.get("boletin"))
    return f"bill:{boletin}" if boletin else f"vote:{row.get('vote_id', '')}"


def group_binary_summary(rows: list[dict], field: str, min_binary: int = 1) -> tuple[str, float | None, int]:
    groups: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        option = norm(row.get("opcion"))
        if option not in BINARY:
            continue
        name = norm(row.get(field)) or "Sin dato"
        groups[name][option] += 1

    pieces = []
    shares = []
    eligible_groups = 0
    for name in sorted(groups):
        yes = groups[name][YES]
        no = groups[name][NO]
        n = yes + no
        if n < min_binary:
            continue
        eligible_groups += 1
        share = yes / n if n else math.nan
        shares.append(share)
        pieces.append(f"{name}: {yes}S/{no}N ({100*share:.1f}% S)")

    gap = max(shares) - min(shares) if len(shares) >= 2 else None
    return " | ".join(pieces), gap, eligible_groups


def vote_aggregate(rows: list[dict]) -> dict:
    counts = Counter(norm(r.get("opcion")) for r in rows)
    yes = counts[YES]
    no = counts[NO]
    binary = yes + no
    minority = min(yes, no) / binary if binary else None

    alignment_summary, alignment_gap, n_align = group_binary_summary(rows, "alignment_at_vote", min_binary=3)
    party_summary, party_gap, n_party = group_binary_summary(rows, "party_at_vote", min_binary=2)
    caucus_summary, caucus_gap, n_caucus = group_binary_summary(rows, "caucus_at_vote", min_binary=2)

    return {
        "n_affirmative": yes,
        "n_against": no,
        "n_abstention": counts["Abstención"],
        "n_no_vote": counts["No Vota"],
        "n_excused": counts["Dispensado"],
        "n_binary": binary,
        "minority_share_binary_observed": round(minority, 6) if minority is not None else "",
        "alignment_binary_summary": alignment_summary,
        "alignment_yes_share_gap": round(alignment_gap, 6) if alignment_gap is not None else "",
        "alignment_groups_binary_n3plus": n_align,
        "party_binary_summary": party_summary,
        "party_yes_share_gap": round(party_gap, 6) if party_gap is not None else "",
        "party_groups_binary_n2plus": n_party,
        "caucus_binary_summary": caucus_summary,
        "caucus_yes_share_gap": round(caucus_gap, 6) if caucus_gap is not None else "",
        "caucus_groups_binary_n2plus": n_caucus,
    }


def join_metadata(base: dict, rc_by_id: dict[str, dict], proj_by_bill: dict[str, dict], topic_by_bill: dict[str, dict]) -> dict:
    vote_id = str(base.get("vote_id", ""))
    rc = rc_by_id.get(vote_id, {})
    boletin = norm(rc.get("boletin") or base.get("boletin"))
    project = proj_by_bill.get(boletin, {}) if boletin else {}
    topic = topic_by_bill.get(boletin, {}) if boletin else {}

    return {
        **base,
        "fecha": rc.get("fecha", base.get("fecha", "")),
        "boletin": boletin,
        "cluster_id": f"bill:{boletin}" if boletin else f"vote:{vote_id}",
        "resultado": rc.get("resultado", base.get("resultado", "")),
        "descripcion": rc.get("descripcion", base.get("descripcion", "")),
        "url_original": rc.get("url_original", base.get("url_original", "")),
        "project_title": project.get("titulo", base.get("project_title", topic.get("titulo", ""))),
        "project_initiative": project.get("iniciativa", ""),
        "project_origin_chamber": project.get("camara_origen", ""),
        "project_stage": project.get("etapa", ""),
        "topic_primary_internal": topic.get("topic_primary", base.get("topic_primary", "")),
        "topic_secondary_internal": topic.get("topic_secondary", ""),
        "topic_confidence_internal": topic.get("confidence", base.get("topic_confidence", "")),
        "topic_validation_status": "internal_not_external_validated",
    }


def diversify(rows: list[dict], n: int, max_per_cluster: int = 1) -> list[dict]:
    used = Counter()
    out = []
    for row in rows:
        cid = cluster_id(row)
        if used[cid] >= max_per_cluster:
            continue
        out.append(row)
        used[cid] += 1
        if len(out) >= n:
            break
    return out


def write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise RuntimeError(f"No hay filas para escribir en {path}")
    fields = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    coord1 = read_csv(ROLLCALL_COORD_1D)
    top2 = read_csv(TOP_DIM2)
    rollcalls = read_csv(ROLLCALLS)
    projects = read_csv(PROJECTS)
    topics = read_csv(TOPIC_FINAL)
    member_votes = read_csv(MEMBER_VOTES)

    rc_by_id = {str(r["vote_id"]): r for r in rollcalls}
    proj_by_bill = {norm(r.get("boletin")): r for r in projects if norm(r.get("boletin"))}
    topic_by_bill = {norm(r.get("boletin")): r for r in topics if norm(r.get("boletin"))}

    votes_by_id: dict[str, list[dict]] = defaultdict(list)
    for row in member_votes:
        votes_by_id[str(row.get("vote_id", ""))].append(row)

    if len(rc_by_id) != len(rollcalls):
        raise RuntimeError("rollcalls.csv contiene vote_id duplicados")
    if any(len(rows) != 155 for rows in votes_by_id.values()):
        bad = {k: len(v) for k, v in votes_by_id.items() if len(v) != 155}
        raise RuntimeError(f"member_votes_enriched no conserva 155 observaciones por roll call: {bad}")

    # ----- D1: universo completo de la corrida research -----
    d1 = []
    for row in coord1:
        vote_id = str(row["vote_id"])
        spread_model = as_float(row.get("spread_1d"))
        midpoint_model = as_float(row.get("midpoint_1d"))
        enriched = join_metadata(dict(row), rc_by_id, proj_by_bill, topic_by_bill)
        enriched.update(vote_aggregate(votes_by_id.get(vote_id, [])))
        enriched["abs_spread_1d"] = abs(spread_model) if spread_model is not None else ""
        enriched["spread_1d_display"] = DISPLAY_MULTIPLIER_D1 * spread_model if spread_model is not None else ""
        enriched["midpoint_1d_display"] = DISPLAY_MULTIPLIER_D1 * midpoint_model if midpoint_model is not None else ""
        enriched["d1_display_multiplier"] = DISPLAY_MULTIPLIER_D1
        d1.append(enriched)

    d1.sort(key=lambda r: as_float(r.get("abs_spread_1d"), -1), reverse=True)
    for i, row in enumerate(d1, start=1):
        row["rank_abs_spread_1d"] = i

    d1_top30_raw = d1[:30]
    d1_top30_diverse = diversify(d1, n=30, max_per_cluster=1)
    for i, row in enumerate(d1_top30_diverse, start=1):
        row["rank_bill_diverse_d1"] = i

    # ----- D2: candidatos de la auditoría 2D existente -----
    d2_base = [dict(r) for r in top2 if norm(r.get("spec_id")) == BASE_2D_SPEC]
    d2 = []
    for row in d2_base:
        vote_id = str(row["vote_id"])
        enriched = join_metadata(row, rc_by_id, proj_by_bill, topic_by_bill)
        enriched.update(vote_aggregate(votes_by_id.get(vote_id, [])))
        # D1 se refleja solo para presentación; D2 permanece intacta.
        m1 = as_float(enriched.get("midpoint_1_aligned"))
        s1 = as_float(enriched.get("spread_1_aligned"))
        enriched["midpoint_1_display"] = DISPLAY_MULTIPLIER_D1 * m1 if m1 is not None else ""
        enriched["spread_1_display"] = DISPLAY_MULTIPLIER_D1 * s1 if s1 is not None else ""
        enriched["d1_display_multiplier"] = DISPLAY_MULTIPLIER_D1
        d2.append(enriched)

    d2.sort(key=lambda r: as_float(r.get("relative_dim2_loading"), -1), reverse=True)
    for i, row in enumerate(d2, start=1):
        row["rank_relative_dim2_loading"] = i

    d2_top25_raw = d2[:25]
    d2_top25_diverse = diversify(d2, n=min(25, len(d2)), max_per_cluster=1)
    for i, row in enumerate(d2_top25_diverse, start=1):
        row["rank_bill_diverse_d2"] = i

    write_rows(OUT / "d1_rollcall_evidence_full.csv", d1)
    write_rows(OUT / "d1_top30_raw.csv", d1_top30_raw)
    write_rows(OUT / "d1_top30_bill_diverse.csv", d1_top30_diverse)
    write_rows(OUT / "d2_candidate_evidence.csv", d2)
    write_rows(OUT / "d2_top25_raw.csv", d2_top25_raw)
    write_rows(OUT / "d2_top25_bill_diverse.csv", d2_top25_diverse)

    def concentration(rows: list[dict]) -> dict:
        c = Counter(cluster_id(r) for r in rows)
        top = c.most_common(5)
        total = len(rows)
        return {
            "n_rows": total,
            "unique_clusters": len(c),
            "top_clusters": [{"cluster": k, "n": v, "share": round(v / total, 4)} for k, v in top] if total else [],
        }

    diagnostics = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "d1_display_multiplier": DISPLAY_MULTIPLIER_D1,
        "d1_rollcalls": len(d1),
        "d1_top30_raw_concentration": concentration(d1_top30_raw),
        "d1_top30_bill_diverse_concentration": concentration(d1_top30_diverse),
        "d2_base_spec": BASE_2D_SPEC,
        "d2_candidates_available": len(d2),
        "d2_top25_raw_concentration": concentration(d2_top25_raw),
        "d2_top25_bill_diverse_concentration": concentration(d2_top25_diverse),
        "member_vote_rows": len(member_votes),
        "rollcalls_with_member_votes": len(votes_by_id),
        "method": {
            "d1_identifying_strength": "abs(spread_1d) from 501-trial research fit; no composite score is invented",
            "d1_diversification": "greedy descending abs(spread_1d), maximum one roll call per bill/cluster",
            "d2_identifying_strength": "relative_dim2_loading already produced by the 2D diagnostic",
            "d2_diversification": "greedy descending relative_dim2_loading, maximum one roll call per bill/cluster",
            "coalitions": "actual temporal party/caucus/alignment from member_votes_enriched at each vote date",
            "topics": "internal thematic classification only; not externally validated and never sufficient by itself to name an axis",
        },
        "warnings": [
            "D1 sign is arbitrary. Display orientation is a reflection only.",
            "D2 remains exploratory and small relative to D1.",
            "High identifying strength does not by itself provide a substantive axis label.",
            "Interpretation must compare multiple bills, actual coalitions, external political context and competing hypotheses.",
        ],
    }
    (OUT / "diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    readme = """# Evidencia para interpretar los ejes W-NOMINATE 2026\n\n"
    readme += "Esta carpeta es una capa interna de investigación. No nombra D1 ni D2.\n\n"
    readme += "## D1\n- `d1_rollcall_evidence_full.csv`: las 276 votaciones de la corrida research.\n"
    readme += "- `d1_top30_raw.csv`: 30 mayores |spread|, sin corregir concentración por proyecto.\n"
    readme += "- `d1_top30_bill_diverse.csv`: selección descendente con máximo una votación por proyecto/cluster.\n\n"
    readme += "## D2\n- `d2_candidate_evidence.csv`: candidatos de la auditoría 2D para la especificación base.\n"
    readme += "- `d2_top25_raw.csv`: mayores cargas relativas D2.\n"
    readme += "- `d2_top25_bill_diverse.csv`: máximo una votación por proyecto/cluster.\n\n"
    readme += "## Coaliciones\nCada fila incluye resúmenes temporales reales por alineamiento, partido y comité, calculados con la afiliación vigente el día de la votación.\n\n"
    readme += "## Regla de interpretación\nUna votación fuerte matemáticamente es un **caso a investigar**, no una etiqueta sustantiva. Para nombrar un eje se requiere recurrencia entre proyectos, coaliciones coherentes, contraste con fuentes externas y descarte de hipótesis alternativas.\n"
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
