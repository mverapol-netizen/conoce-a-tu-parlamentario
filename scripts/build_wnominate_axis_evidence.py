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
R1 = WN / "research_1d"
D2 = WN / "two_dimensional"
TOPICS = DATA / "topics"
OUT = WN / "interpretation"
OUT.mkdir(parents=True, exist_ok=True)

P_COORD1 = R1 / "rollcall_coordinates_research.csv"
P_TOP2 = D2 / "top_dim2_rollcalls.csv"
P_RC = DATA / "rollcalls.csv"
P_PROJECTS = DATA / "projects.csv"
P_TOPICS = TOPICS / "rollcall_inherited_topic_final.csv"
P_VOTES = DATA / "member_votes_enriched.csv"

D1_DISPLAY_MULTIPLIER = -1.0
BASE_2D_SPEC = "raw_lop025_2d"
YES, NO = "Afirmativo", "En Contra"
BINARY = {YES, NO}

# Proyectos omnibus que no pueden interpretarse como una sola unidad sustantiva.
# Se auditan por separado, roll call por roll call, identificando articulo/indicacion exacta.
SPECIAL_OMNIBUS = {
    "18216-05": "Megareforma / proyecto omnibus del gobierno de Jose Antonio Kast",
}


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Falta archivo requerido: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def fnum(v, default=None):
    try:
        return default if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return default


def clean(v) -> str:
    return (v or "").strip()


def is_special_omnibus(row: dict) -> bool:
    return clean(row.get("boletin")) in SPECIAL_OMNIBUS


def cluster(row: dict) -> str:
    b = clean(row.get("boletin"))
    return f"bill:{b}" if b else f"vote:{row.get('vote_id', '')}"


def group_summary(rows: list[dict], field: str, minimum: int) -> tuple[str, float | None, int]:
    g: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        option = clean(r.get("opcion"))
        if option in BINARY:
            g[clean(r.get(field)) or "Sin dato"][option] += 1
    pieces, shares = [], []
    eligible = 0
    for name in sorted(g):
        y, n = g[name][YES], g[name][NO]
        den = y + n
        if den < minimum:
            continue
        eligible += 1
        share = y / den
        shares.append(share)
        pieces.append(f"{name}: {y}S/{n}N ({100*share:.1f}% S)")
    gap = max(shares) - min(shares) if len(shares) >= 2 else None
    return " | ".join(pieces), gap, eligible


def aggregate_vote(rows: list[dict]) -> dict:
    c = Counter(clean(r.get("opcion")) for r in rows)
    y, n = c[YES], c[NO]
    binary = y + n
    a, agap, na = group_summary(rows, "alignment_at_vote", 3)
    p, pgap, np = group_summary(rows, "party_at_vote", 2)
    k, kgap, nk = group_summary(rows, "caucus_at_vote", 2)
    return {
        "n_affirmative": y,
        "n_against": n,
        "n_abstention": c["Abstención"],
        "n_no_vote": c["No Vota"],
        "n_excused": c["Dispensado"],
        "n_binary": binary,
        "minority_share_binary_observed": round(min(y, n) / binary, 6) if binary else "",
        "alignment_binary_summary": a,
        "alignment_yes_share_gap": round(agap, 6) if agap is not None else "",
        "alignment_groups_binary_n3plus": na,
        "party_binary_summary": p,
        "party_yes_share_gap": round(pgap, 6) if pgap is not None else "",
        "party_groups_binary_n2plus": np,
        "caucus_binary_summary": k,
        "caucus_yes_share_gap": round(kgap, 6) if kgap is not None else "",
        "caucus_groups_binary_n2plus": nk,
    }


def metadata(base: dict, rc_by_id: dict, proj_by_bill: dict, topic_by_bill: dict) -> dict:
    vote_id = str(base.get("vote_id", ""))
    rc = rc_by_id.get(vote_id, {})
    boletin = clean(rc.get("boletin") or base.get("boletin"))
    pr = proj_by_bill.get(boletin, {}) if boletin else {}
    tp = topic_by_bill.get(boletin, {}) if boletin else {}
    omnibus = boletin in SPECIAL_OMNIBUS
    return {
        **base,
        "fecha": rc.get("fecha", base.get("fecha", "")),
        "boletin": boletin,
        "cluster_id": f"bill:{boletin}" if boletin else f"vote:{vote_id}",
        "resultado": rc.get("resultado", base.get("resultado", "")),
        "descripcion": rc.get("descripcion", base.get("descripcion", "")),
        "url_original": rc.get("url_original", base.get("url_original", "")),
        "project_title": pr.get("titulo", base.get("project_title", tp.get("titulo", ""))),
        "project_initiative": pr.get("iniciativa", ""),
        "project_origin_chamber": pr.get("camara_origen", ""),
        "project_stage": pr.get("etapa", ""),
        "topic_primary_internal": tp.get("topic_primary", base.get("topic_primary", "")),
        "topic_secondary_internal": tp.get("topic_secondary", ""),
        "topic_confidence_internal": tp.get("confidence", base.get("topic_confidence", "")),
        "topic_validation_status": (
            "project_level_not_sufficient_for_omnibus_rollcall"
            if omnibus else "internal_not_external_validated"
        ),
        "special_omnibus": "1" if omnibus else "0",
        "special_omnibus_label": SPECIAL_OMNIBUS.get(boletin, ""),
        "interpretation_unit": "exact_rollcall_item" if omnibus else "rollcall_with_project_context",
        "omnibus_audit_required": "1" if omnibus else "0",
    }


def diversify(rows: list[dict], n: int) -> list[dict]:
    used, out = Counter(), []
    for row in rows:
        cid = cluster(row)
        if used[cid]:
            continue
        used[cid] += 1
        out.append(row)
        if len(out) >= n:
            break
    return out


def diversify_non_omnibus(rows: list[dict], n: int) -> list[dict]:
    """Muestra transversal entre proyectos ordinarios; los omnibus se auditan aparte."""
    return diversify([r for r in rows if not is_special_omnibus(r)], n)


def write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise RuntimeError(f"No hay filas para {path}")
    fields, seen = [], set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def concentration(rows: list[dict]) -> dict:
    c = Counter(cluster(r) for r in rows)
    total = len(rows)
    return {
        "n_rows": total,
        "unique_clusters": len(c),
        "top_clusters": [
            {"cluster": k, "n": v, "share": round(v / total, 4)} for k, v in c.most_common(5)
        ] if total else [],
    }


def main() -> None:
    coord1, top2 = read_csv(P_COORD1), read_csv(P_TOP2)
    rollcalls, projects = read_csv(P_RC), read_csv(P_PROJECTS)
    topics, member_votes = read_csv(P_TOPICS), read_csv(P_VOTES)

    rc_by_id = {str(r["vote_id"]): r for r in rollcalls}
    proj_by_bill = {clean(r.get("boletin")): r for r in projects if clean(r.get("boletin"))}
    topic_by_bill = {clean(r.get("boletin")): r for r in topics if clean(r.get("boletin"))}
    votes_by_id: dict[str, list[dict]] = defaultdict(list)
    for r in member_votes:
        votes_by_id[str(r.get("vote_id", ""))].append(r)

    if len(rc_by_id) != len(rollcalls):
        raise RuntimeError("rollcalls.csv contiene vote_id duplicados")
    bad = {k: len(v) for k, v in votes_by_id.items() if len(v) != 155}
    if bad:
        raise RuntimeError(f"member_votes_enriched no conserva 155 filas por roll call: {bad}")

    d1 = []
    for row in coord1:
        vote_id = str(row["vote_id"])
        spread, midpoint = fnum(row.get("spread_1d")), fnum(row.get("midpoint_1d"))
        x = metadata(dict(row), rc_by_id, proj_by_bill, topic_by_bill)
        x.update(aggregate_vote(votes_by_id.get(vote_id, [])))
        x["abs_spread_1d"] = abs(spread) if spread is not None else ""
        x["spread_1d_display"] = D1_DISPLAY_MULTIPLIER * spread if spread is not None else ""
        x["midpoint_1d_display"] = D1_DISPLAY_MULTIPLIER * midpoint if midpoint is not None else ""
        x["d1_display_multiplier"] = D1_DISPLAY_MULTIPLIER
        d1.append(x)
    d1.sort(key=lambda r: fnum(r.get("abs_spread_1d"), -1), reverse=True)
    for i, r in enumerate(d1, 1):
        r["rank_abs_spread_1d"] = i
    d1_raw = d1[:30]
    d1_div = diversify(d1, 30)
    d1_non_omnibus_div = diversify_non_omnibus(d1, 30)
    d1_omnibus = [r for r in d1 if is_special_omnibus(r)]
    for i, r in enumerate(d1_div, 1):
        r["rank_bill_diverse_d1"] = i
    for i, r in enumerate(d1_non_omnibus_div, 1):
        r["rank_non_omnibus_bill_diverse_d1"] = i
    for i, r in enumerate(d1_omnibus, 1):
        r["rank_within_omnibus_d1"] = i

    d2 = []
    for row in top2:
        if clean(row.get("spec_id")) != BASE_2D_SPEC:
            continue
        vote_id = str(row["vote_id"])
        x = metadata(dict(row), rc_by_id, proj_by_bill, topic_by_bill)
        x.update(aggregate_vote(votes_by_id.get(vote_id, [])))
        m1, s1 = fnum(x.get("midpoint_1_aligned")), fnum(x.get("spread_1_aligned"))
        x["midpoint_1_display"] = D1_DISPLAY_MULTIPLIER * m1 if m1 is not None else ""
        x["spread_1_display"] = D1_DISPLAY_MULTIPLIER * s1 if s1 is not None else ""
        x["d1_display_multiplier"] = D1_DISPLAY_MULTIPLIER
        d2.append(x)
    d2.sort(key=lambda r: fnum(r.get("relative_dim2_loading"), -1), reverse=True)
    for i, r in enumerate(d2, 1):
        r["rank_relative_dim2_loading"] = i
    d2_raw = d2[:25]
    d2_div = diversify(d2, min(25, len(d2)))
    d2_non_omnibus_div = diversify_non_omnibus(d2, min(25, len(d2)))
    d2_omnibus = [r for r in d2 if is_special_omnibus(r)]
    for i, r in enumerate(d2_div, 1):
        r["rank_bill_diverse_d2"] = i
    for i, r in enumerate(d2_non_omnibus_div, 1):
        r["rank_non_omnibus_bill_diverse_d2"] = i
    for i, r in enumerate(d2_omnibus, 1):
        r["rank_within_omnibus_d2"] = i

    outputs = {
        "d1_rollcall_evidence_full.csv": d1,
        "d1_top30_raw.csv": d1_raw,
        "d1_top30_bill_diverse.csv": d1_div,
        "d1_top30_non_omnibus_bill_diverse.csv": d1_non_omnibus_div,
        "d1_omnibus_18216_05.csv": d1_omnibus,
        "d2_candidate_evidence.csv": d2,
        "d2_top25_raw.csv": d2_raw,
        "d2_top25_bill_diverse.csv": d2_div,
        "d2_top25_non_omnibus_bill_diverse.csv": d2_non_omnibus_div,
        "d2_omnibus_18216_05.csv": d2_omnibus,
    }
    for name, rows in outputs.items():
        write_rows(OUT / name, rows)

    diagnostics = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "d1_display_multiplier": D1_DISPLAY_MULTIPLIER,
        "d1_rollcalls": len(d1),
        "d1_top30_raw_concentration": concentration(d1_raw),
        "d1_top30_bill_diverse_concentration": concentration(d1_div),
        "d1_non_omnibus_diverse_concentration": concentration(d1_non_omnibus_div),
        "d1_special_omnibus_rollcalls": {b: sum(clean(r.get("boletin")) == b for r in d1) for b in SPECIAL_OMNIBUS},
        "d2_base_spec": BASE_2D_SPEC,
        "d2_candidates_available": len(d2),
        "d2_top25_raw_concentration": concentration(d2_raw),
        "d2_top25_bill_diverse_concentration": concentration(d2_div),
        "d2_non_omnibus_diverse_concentration": concentration(d2_non_omnibus_div),
        "d2_special_omnibus_candidates": {b: sum(clean(r.get("boletin")) == b for r in d2) for b in SPECIAL_OMNIBUS},
        "member_vote_rows": len(member_votes),
        "rollcalls_with_member_votes": len(votes_by_id),
        "special_omnibus": SPECIAL_OMNIBUS,
        "method": {
            "d1_identifying_strength": "abs(spread_1d) from 501-trial research fit; no composite score",
            "ordinary_bill_diversification": "descending identifying strength, max one roll call per ordinary bill/cluster",
            "omnibus_treatment": "special omnibus bills are excluded from the ordinary diversified audit and audited separately at exact roll-call/article/indication level before contributing substantive evidence",
            "d2_identifying_strength": "relative_dim2_loading from existing 2D diagnostic",
            "coalitions": "temporal party/caucus/alignment at each vote date from member_votes_enriched",
            "topics": "project-level topic classification is never sufficient for an omnibus roll call; exact voted content must be recovered",
        },
        "warnings": [
            "D1 sign is arbitrary; display orientation is only a reflection.",
            "D2 remains exploratory and small relative to D1.",
            "Identifying strength alone does not supply substantive meaning.",
            "The omnibus bill 18216-05 contains heterogeneous substantive items and must not be interpreted from its project title or counted as either one homogeneous item or many independent projects.",
            "Axis interpretation requires recurring evidence across ordinary bills plus separately audited omnibus subitems, actual coalitions, external context and alternative-hypothesis tests.",
        ],
    }
    (OUT / "diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    readme = (
        "# Evidencia para interpretar los ejes W-NOMINATE 2026\n\n"
        "Capa interna de investigación: estos archivos **no nombran** D1 ni D2.\n\n"
        "## D1\n"
        "- `d1_rollcall_evidence_full.csv`: universo completo de la corrida research.\n"
        "- `d1_top30_raw.csv`: 30 mayores valores de |spread| sin corregir concentración.\n"
        "- `d1_top30_bill_diverse.csv`: ranking histórico con máximo una votación por boletín.\n"
        "- `d1_top30_non_omnibus_bill_diverse.csv`: muestra transversal recomendada para auditoría histórico-política; excluye proyectos omnibus.\n"
        "- `d1_omnibus_18216_05.csv`: todas las votaciones D1 de la Megareforma, para auditoría interna separada.\n\n"
        "## D2\n"
        "- `d2_candidate_evidence.csv`: candidatos de la auditoría 2D base.\n"
        "- `d2_top25_raw.csv`: mayores cargas relativas sobre D2.\n"
        "- `d2_top25_non_omnibus_bill_diverse.csv`: muestra transversal sin proyectos omnibus.\n"
        "- `d2_omnibus_18216_05.csv`: candidatos D2 internos de la Megareforma.\n\n"
        "## Regla especial: boletín 18216-05\n"
        "Es la Megareforma/proyecto omnibus y contiene materias heterogéneas. No puede tratarse como una unidad sustantiva homogénea, pero sus roll calls tampoco pueden contarse como proyectos independientes. Cada votación debe recuperar el artículo, numeral o indicación exacta, clasificarse por materia y compararse con otras votaciones de la misma familia antes de usarse para nombrar un eje.\n\n"
        "## Coaliciones\n"
        "Cada fila resume votos por alineamiento, partido y comité usando la afiliación vigente en la fecha exacta.\n\n"
        "## Regla de interpretación\n"
        "Una votación fuerte matemáticamente es un caso a investigar, no una etiqueta sustantiva. Nombrar un eje requiere recurrencia entre materias y proyectos, coaliciones coherentes, fuentes externas y descarte de hipótesis alternativas.\n"
    )
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
