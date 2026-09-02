from __future__ import annotations

import csv
import json
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026"


def read_csv(name: str) -> list[dict]:
    path = OUT / name
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def norm(value: str) -> str:
    text = unicodedata.normalize("NFD", str(value or "").lower())
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def duplicate_count(rows: list[dict], keys: tuple[str, ...]) -> int:
    seen = set()
    duplicates = 0
    for row in rows:
        key = tuple(row.get(k, "") for k in keys)
        if key in seen:
            duplicates += 1
        else:
            seen.add(key)
    return duplicates


def main() -> None:
    projects = read_csv("projects.csv")
    events = read_csv("project_events.csv")
    authors = read_csv("bill_authors.csv")
    rollcalls = read_csv("rollcalls.csv")
    member_votes = read_csv("member_votes.csv")

    failures: list[str] = []
    warnings: list[str] = []

    project_bills = {row.get("boletin", "") for row in projects if row.get("boletin")}
    parliamentary_bills = {
        row.get("boletin", "")
        for row in projects
        if row.get("boletin") and row.get("origen_iniciativa") == "parlamentario"
    }

    event_bills = {row.get("boletin", "") for row in events if row.get("boletin")}
    orphan_event_bills = sorted(event_bills - project_bills)
    event_coverage = len(event_bills & project_bills) / max(len(project_bills), 1)
    commission_events = [
        row
        for row in events
        if "comision" in norm(f"{row.get('etapa', '')} {row.get('subetapa', '')}")
    ]

    authors_by_bill: dict[str, list[dict]] = defaultdict(list)
    for row in authors:
        authors_by_bill[row.get("boletin", "")].append(row)
    authored_bills = {bill for bill, rows in authors_by_bill.items() if bill and rows}
    unresolved_motions = sorted(parliamentary_bills - authored_bills)
    author_counts = {bill: len(rows) for bill, rows in authors_by_bill.items() if bill}
    multi_author_bills = {bill: n for bill, n in author_counts.items() if n > 1}
    duplicate_authors_within_bill = 0
    duplicate_orders_within_bill = 0
    for bill, rows in authors_by_bill.items():
        ids = [row.get("author_id", "") for row in rows if row.get("author_id")]
        orders = [row.get("author_order", "") for row in rows if row.get("author_order")]
        duplicate_authors_within_bill += len(ids) - len(set(ids))
        duplicate_orders_within_bill += len(orders) - len(set(orders))

    member_counts = Counter(row.get("vote_id", "") for row in member_votes if row.get("vote_id"))
    rollcall_ids = {row.get("vote_id", "") for row in rollcalls if row.get("vote_id")}
    member_vote_ids = set(member_counts)
    orphan_member_vote_ids = sorted(member_vote_ids - rollcall_ids)
    incomplete_rollcalls = {
        vote_id: member_counts.get(vote_id, 0)
        for vote_id in sorted(rollcall_ids)
        if member_counts.get(vote_id, 0) < 150
    }
    vote_option_counts = Counter((row.get("opcion") or "<vacío>").strip() for row in member_votes)

    duplicates = {
        "projects_by_boletin": duplicate_count(projects, ("boletin",)),
        "project_events": duplicate_count(events, ("boletin", "fecha", "sesion", "etapa", "subetapa", "documento_url")),
        "author_relations": duplicate_count(authors, ("boletin", "author_chamber", "author_id", "author_order")),
        "rollcalls_by_vote_id": duplicate_count(rollcalls, ("vote_id",)),
        "member_votes": duplicate_count(member_votes, ("vote_id", "diputado_id")),
    }

    if not projects:
        failures.append("projects.csv está vacío")
    if not events:
        failures.append("project_events.csv está vacío")
    if projects and event_coverage < 0.80:
        failures.append(f"Cobertura de tramitación demasiado baja: {event_coverage:.1%}")
    elif projects and event_coverage < 0.95:
        warnings.append(f"Cobertura de tramitación inferior a 95%: {event_coverage:.1%}")
    if orphan_event_bills:
        failures.append(f"Hay {len(orphan_event_bills)} boletines huérfanos en project_events.csv")
    if events and not commission_events:
        failures.append("No se detectó ninguna mención de comisión en la tramitación")

    unresolved_limit = max(5, int(len(parliamentary_bills) * 0.03))
    if len(unresolved_motions) > unresolved_limit:
        failures.append(
            f"Demasiadas mociones sin autoría: {len(unresolved_motions)}/{len(parliamentary_bills)}"
        )
    if len(parliamentary_bills) >= 10 and not multi_author_bills:
        failures.append("No aparece ninguna moción con múltiples autores; posible pérdida de coautorías")
    if duplicate_authors_within_bill:
        failures.append(f"Hay {duplicate_authors_within_bill} autores duplicados dentro de un mismo boletín")
    if duplicate_orders_within_bill:
        warnings.append(f"Hay {duplicate_orders_within_bill} órdenes de autor repetidos dentro de un mismo boletín")

    if orphan_member_vote_ids:
        failures.append(f"Hay {len(orphan_member_vote_ids)} votaciones nominales sin roll call padre")
    if incomplete_rollcalls:
        failures.append(f"Hay {len(incomplete_rollcalls)} roll calls con menos de 150 registros nominales")

    for name, count in duplicates.items():
        if count:
            failures.append(f"Duplicados en {name}: {count}")

    report = {
        "generated_for": str(date.today()),
        "status": "pass" if not failures else "fail",
        "projects": {
            "count": len(projects),
            "events": len(events),
            "projects_with_events": len(event_bills & project_bills),
            "event_coverage_pct": round(event_coverage * 100, 2),
            "commission_events": len(commission_events),
            "orphan_event_bills": orphan_event_bills,
        },
        "authorship": {
            "parliamentary_bills": len(parliamentary_bills),
            "author_relations": len(authors),
            "bills_with_authors": len(authored_bills & parliamentary_bills),
            "unresolved_motions": unresolved_motions,
            "multi_author_bills": len(multi_author_bills),
            "max_authors_on_bill": max(author_counts.values(), default=0),
            "author_count_distribution": dict(sorted(Counter(author_counts.values()).items())),
        },
        "floor_votes": {
            "rollcalls": len(rollcalls),
            "member_vote_rows": len(member_votes),
            "min_member_rows_per_rollcall": min((member_counts.get(v, 0) for v in rollcall_ids), default=0),
            "max_member_rows_per_rollcall": max((member_counts.get(v, 0) for v in rollcall_ids), default=0),
            "incomplete_rollcalls": incomplete_rollcalls,
            "vote_option_counts": dict(vote_option_counts),
        },
        "duplicates": duplicates,
        "warnings": warnings,
        "failures": failures,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "audit_diagnostics.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    summary = [
        "# Auditoría de datos legislativos 2026",
        "",
        f"**Estado:** {'PASS' if not failures else 'FAIL'}",
        "",
        f"- Proyectos: {len(projects)}",
        f"- Eventos de tramitación: {len(events)} ({event_coverage:.1%} de proyectos con eventos)",
        f"- Eventos que mencionan comisión: {len(commission_events)}",
        f"- Mociones parlamentarias: {len(parliamentary_bills)}",
        f"- Relaciones de autoría: {len(authors)}",
        f"- Mociones con múltiples autores: {len(multi_author_bills)}",
        f"- Máximo de autores en una moción: {max(author_counts.values(), default=0)}",
        f"- Roll calls de Sala: {len(rollcalls)}",
        f"- Votos nominales: {len(member_votes)}",
        "",
    ]
    if warnings:
        summary.extend(["## Advertencias", ""] + [f"- {item}" for item in warnings] + [""])
    if failures:
        summary.extend(["## Fallas", ""] + [f"- {item}" for item in failures] + [""])
    (OUT / "AUDIT.md").write_text("\n".join(summary), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        raise RuntimeError("Auditoría legislativa fallida: " + " | ".join(failures))


if __name__ == "__main__":
    main()
