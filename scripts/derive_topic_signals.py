from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "legislative" / "2026"
OUT = DATA / "topics"


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def norm(value: str) -> str:
    text = unicodedata.normalize("NFD", str(value or "").lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", text).strip()


# El sufijo de los boletines corresponde al código institucional de DESTINACIÓN.
# Se conserva como señal separada de las remisiones observadas en la tramitación.
DESTINATION_CODE_TO_COMMISSION = {
    "01": "Agricultura, Silvicultura y Desarrollo Rural",
    "02": "Defensa Nacional",
    "03": "Economía, Fomento, MIPYMES, Consumidores y Turismo",
    "04": "Educación",
    "05": "Hacienda",
    "06": "Gobierno Interior, Nacionalidad, Ciudadanía y Regionalización",
    "07": "Constitución, Legislación, Justicia y Reglamento",
    "08": "Minería y Energía",
    "09": "Obras Públicas",
    "10": "Relaciones Exteriores",
    "11": "Salud",
    "12": "Medio Ambiente y Recursos Naturales",
    "13": "Trabajo y Seguridad Social",
    "14": "Vivienda, Desarrollo Urbano",
    "15": "Transportes y Telecomunicaciones",
    "16": "Régimen Interno y Administración",
    "17": "Derechos Humanos y Pueblos Originarios",
    "18": "Familia, Infancia y Adolescencia",
    "19": "Ciencia y Tecnología",
    "20": "Bienes Nacionales",
    "21": "Pesca, Acuicultura e Intereses Marítimos",
    "22": "Emergencias, Desastres y Bomberos",
    "24": "Cultura, Artes y Comunicaciones",
    "25": "Seguridad Ciudadana",
    "27": "Zonas Extremas y Antártica Chilena",
    "29": "Deportes y Recreación",
    "31": "Desarrollo Social",
    "33": "Recursos Hídricos y Desertificación",
    "34": "Mujeres y Equidad de Género",
    "35": "Personas Mayores y Discapacidad",
}

COMMISSION_ALIASES = {
    "Agricultura, Silvicultura y Desarrollo Rural": ["agricultura, silvicultura y desarrollo rural"],
    "Defensa Nacional": ["defensa nacional"],
    "Economía, Fomento, MIPYMES, Consumidores y Turismo": [
        "economia, fomento; micro, pequena y mediana empresa proteccion de los consumidores y turismo",
        "economia, fomento; micro, pequena y mediana empresa, proteccion de los consumidores y turismo",
        "economia, fomento, micro, pequena y mediana empresa, proteccion de los consumidores y turismo",
    ],
    "Educación": ["educacion"],
    "Hacienda": ["hacienda"],
    "Gobierno Interior, Nacionalidad, Ciudadanía y Regionalización": [
        "gobierno interior, nacionalidad, ciudadania y regionalizacion"
    ],
    "Constitución, Legislación, Justicia y Reglamento": [
        "constitucion, legislacion, justicia y reglamento"
    ],
    "Minería y Energía": ["mineria y energia"],
    "Obras Públicas": ["obras publicas"],
    "Relaciones Exteriores": [
        "relaciones exteriores, asuntos interparlamentarios e integracion latinoamericana",
        "relaciones exteriores",
    ],
    "Salud": ["salud"],
    "Medio Ambiente y Recursos Naturales": ["medio ambiente y recursos naturales"],
    "Trabajo y Seguridad Social": ["trabajo y seguridad social"],
    "Vivienda, Desarrollo Urbano": ["vivienda, desarrollo urbano"],
    "Transportes y Telecomunicaciones": [
        "transportes y telecomunicaciones",
        "obras publicas, transporte y telecomunicaciones",
        "obras publicas, transportes y telecomunicaciones",
    ],
    "Régimen Interno y Administración": ["regimen interno y administracion"],
    "Derechos Humanos y Pueblos Originarios": [
        "derechos humanos y pueblos originarios",
        "derechos humanos",
    ],
    "Familia, Infancia y Adolescencia": [
        "familia, infancia y adolescencia",
        "comision de la familia",
    ],
    "Ciencia y Tecnología": [
        "ciencia y tecnologia",
        "ciencias y tecnologia",
        "futuro, ciencias, tecnologia, conocimiento e innovacion",
        "desafios del futuro, ciencia, tecnologia e innovacion",
    ],
    "Bienes Nacionales": ["bienes nacionales"],
    "Pesca, Acuicultura e Intereses Marítimos": ["pesca, acuicultura e intereses maritimos"],
    "Emergencias, Desastres y Bomberos": [
        "emergencias, desastres y bomberos",
        "emergencia, desastres y bomberos",
    ],
    "Cultura, Artes y Comunicaciones": ["cultura, artes y comunicaciones"],
    "Seguridad Ciudadana": ["seguridad ciudadana"],
    "Zonas Extremas y Antártica Chilena": ["zonas extremas y antartica chilena"],
    "Deportes y Recreación": ["deportes y recreacion"],
    "Desarrollo Social": [
        "desarrollo social, superacion de la pobreza y planificacion",
        "desarrollo social",
    ],
    "Recursos Hídricos y Desertificación": ["recursos hidricos y desertificacion"],
    "Mujeres y Equidad de Género": ["mujeres y equidad de genero"],
    "Personas Mayores y Discapacidad": ["personas mayores y discapacidad"],
}

COMMISSION_TOPIC = {
    "Agricultura, Silvicultura y Desarrollo Rural": "Agricultura y mundo rural",
    "Defensa Nacional": "Defensa",
    "Economía, Fomento, MIPYMES, Consumidores y Turismo": "Economía, comercio y consumidores",
    "Educación": "Educación",
    "Hacienda": "Economía y hacienda",
    "Gobierno Interior, Nacionalidad, Ciudadanía y Regionalización": "Gobierno interior y descentralización",
    "Constitución, Legislación, Justicia y Reglamento": "Constitución y justicia",
    "Minería y Energía": "Minería y energía",
    "Obras Públicas": "Infraestructura y obras públicas",
    "Relaciones Exteriores": "Relaciones exteriores",
    "Salud": "Salud",
    "Medio Ambiente y Recursos Naturales": "Medio ambiente",
    "Trabajo y Seguridad Social": "Trabajo y seguridad social",
    "Vivienda, Desarrollo Urbano": "Vivienda y territorio",
    "Transportes y Telecomunicaciones": "Transportes y telecomunicaciones",
    "Régimen Interno y Administración": "Administración parlamentaria",
    "Derechos Humanos y Pueblos Originarios": "Derechos humanos",
    "Familia, Infancia y Adolescencia": "Familia, infancia y adolescencia",
    "Ciencia y Tecnología": "Ciencia y tecnología",
    "Bienes Nacionales": "Bienes nacionales y territorio",
    "Pesca, Acuicultura e Intereses Marítimos": "Pesca y acuicultura",
    "Emergencias, Desastres y Bomberos": "Emergencias y desastres",
    "Cultura, Artes y Comunicaciones": "Cultura y comunicaciones",
    "Seguridad Ciudadana": "Seguridad",
    "Zonas Extremas y Antártica Chilena": "Territorio y zonas extremas",
    "Deportes y Recreación": "Deportes",
    "Desarrollo Social": "Desarrollo social",
    "Recursos Hídricos y Desertificación": "Agua y recursos hídricos",
    "Mujeres y Equidad de Género": "Mujeres y género",
    "Personas Mayores y Discapacidad": "Personas mayores y discapacidad",
}

TRANSVERSAL = {
    "Hacienda",
    "Constitución, Legislación, Justicia y Reglamento",
    "Régimen Interno y Administración",
}


def bulletin_destination_code(boletin: str) -> str:
    if "-" not in (boletin or ""):
        return ""
    return boletin.rsplit("-", 1)[-1].zfill(2)


def canonical_commissions(text: str) -> list[str]:
    normalized = norm(text)
    hits = []
    for canonical, aliases in COMMISSION_ALIASES.items():
        if any(alias in normalized for alias in aliases):
            hits.append(canonical)
    return hits


def clean_raw_commission(value: str) -> str:
    text = re.sub(r"\s+", " ", value or "").strip(" .;,:")
    stops = [
        " el acuerdo", " que la ", " que el ", " con posterioridad", " una vez",
        " la asignación", " la asignacion", " para que", " a fin de", " mediante",
    ]
    lower = text.lower()
    positions = [lower.find(stop) for stop in stops if lower.find(stop) >= 0]
    if positions:
        text = text[: min(positions)].strip(" .;,:")
    return text


def origin_commission_from_event(substage: str) -> str:
    match = re.search(r"pasa\s+a\s+comisi[oó]n\s+de\s+(.+)$", substage or "", re.I)
    if not match:
        return ""
    raw = clean_raw_commission(match.group(1))
    canonical = canonical_commissions(raw)
    return canonical[0] if canonical else raw


def unique_join(values: list[str]) -> str:
    result = []
    seen = set()
    for value in values:
        value = (value or "").strip()
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return " | ".join(result)


def same_commission(a: str, b: str) -> bool:
    return bool(a and b and norm(a) == norm(b))


def main() -> None:
    projects = read_csv(DATA / "projects.csv")
    events = read_csv(DATA / "project_events.csv")
    subjects = read_csv(DATA / "project_subjects.csv")
    ministries = read_csv(DATA / "project_ministries.csv")
    text_index = read_csv(OUT / "project_text_index.csv")

    by_events: dict[str, list[dict]] = defaultdict(list)
    for idx, event in enumerate(events):
        event = dict(event)
        event["_order"] = idx
        by_events[event.get("boletin", "")].append(event)

    by_subjects: dict[str, list[str]] = defaultdict(list)
    for row in subjects:
        by_subjects[row.get("boletin", "")].append(row.get("materia_oficial", ""))

    by_ministries: dict[str, list[str]] = defaultdict(list)
    for row in ministries:
        by_ministries[row.get("boletin", "")].append(row.get("ministerio", ""))

    text_quality = {row.get("boletin", ""): row.get("text_quality", "") for row in text_index}

    commission_rows = []
    signal_rows = []
    unknown_codes: Counter[str] = Counter()
    mismatches = []

    for project in projects:
        bill = project.get("boletin", "")
        destination_code = bulletin_destination_code(bill)
        suffix_origin = DESTINATION_CODE_TO_COMMISSION.get(destination_code, "")
        if destination_code and not suffix_origin:
            unknown_codes[destination_code] += 1

        bill_events = sorted(
            by_events.get(bill, []),
            key=lambda x: (x.get("fecha", ""), int(x.get("_order", 0))),
        )

        explicit_origin = ""
        origin_evidence = ""
        discovered: list[dict] = []
        seen = set()

        for event in bill_events:
            substage = event.get("subetapa", "")
            candidate_origin = origin_commission_from_event(substage)
            if candidate_origin and not explicit_origin:
                explicit_origin = candidate_origin
                origin_evidence = substage

            commissions = canonical_commissions(substage)
            if candidate_origin and candidate_origin not in commissions:
                commissions.insert(0, candidate_origin)

            for commission in commissions:
                if commission in seen:
                    continue
                seen.add(commission)
                discovered.append({
                    "commission": commission,
                    "fecha": event.get("fecha", ""),
                    "etapa": event.get("etapa", ""),
                    "evidence": substage,
                    "source": event.get("fuente", ""),
                    "source_type": "evento_tramitacion",
                })

        mismatch = bool(explicit_origin and suffix_origin and not same_commission(explicit_origin, suffix_origin))
        if mismatch:
            mismatches.append({
                "boletin": bill,
                "destination_code": destination_code,
                "suffix_commission": suffix_origin,
                "explicit_event_commission": explicit_origin,
                "event": origin_evidence,
            })

        origin_proxy = explicit_origin or suffix_origin
        if explicit_origin and suffix_origin:
            origin_source = "evento_cuenta+sufijo" if not mismatch else "evento_cuenta_vs_sufijo"
        elif explicit_origin:
            origin_source = "evento_cuenta"
        elif suffix_origin:
            origin_source = "sufijo_boletin"
        else:
            origin_source = "sin_proxy"

        if suffix_origin and suffix_origin not in seen:
            discovered.insert(0, {
                "commission": suffix_origin,
                "fecha": project.get("fecha_ingreso", ""),
                "etapa": "destinación inicial",
                "evidence": f"Código de destinación del boletín: {destination_code}",
                "source": project.get("source_url", ""),
                "source_type": "sufijo_boletin",
            })
            seen.add(suffix_origin)

        if explicit_origin and explicit_origin not in seen:
            discovered.insert(0, {
                "commission": explicit_origin,
                "fecha": project.get("fecha_ingreso", ""),
                "etapa": "",
                "evidence": origin_evidence,
                "source": project.get("source_url", ""),
                "source_type": "evento_cuenta",
            })
            seen.add(explicit_origin)

        for seq, item in enumerate(discovered, start=1):
            commission_rows.append({
                "boletin": bill,
                "sequence": seq,
                "commission": item["commission"],
                "topic_proxy": COMMISSION_TOPIC.get(item["commission"], ""),
                "is_origin_proxy": "1" if same_commission(item["commission"], origin_proxy) else "0",
                "is_transversal": "1" if item["commission"] in TRANSVERSAL else "0",
                "source_type": item["source_type"],
                "first_seen_date": item["fecha"],
                "etapa": item["etapa"],
                "evidence_event": item["evidence"],
                "source_url": item["source"],
            })

        commission_names = [item["commission"] for item in discovered]
        trajectory_topics = [COMMISSION_TOPIC.get(name, "") for name in commission_names]
        substantive = [name for name in commission_names if name not in TRANSVERSAL]

        if origin_proxy and COMMISSION_TOPIC.get(origin_proxy):
            signal_strength = "media" if origin_proxy in TRANSVERSAL or mismatch else "alta"
        elif commission_names or project.get("materia_pagina") or by_subjects.get(bill):
            signal_strength = "media"
        else:
            signal_strength = "baja"

        review_reasons = []
        if mismatch:
            review_reasons.append("discrepancia_origen_evento_vs_sufijo")
        if destination_code and not suffix_origin:
            review_reasons.append("codigo_destinacion_no_mapeado")
        if not origin_proxy:
            review_reasons.append("sin_proxy_comision_origen")
        if origin_proxy in TRANSVERSAL and substantive:
            review_reasons.append("origen_transversal_con_comision_sustantiva")
        elif origin_proxy in TRANSVERSAL:
            review_reasons.append("origen_transversal")
        if len(set(x for x in trajectory_topics if x)) >= 2:
            review_reasons.append("trayectoria_multitematica")

        signal_rows.append({
            "boletin": bill,
            "titulo": project.get("titulo", ""),
            "origen_iniciativa": project.get("origen_iniciativa", ""),
            "codigo_destinacion": destination_code,
            "comision_destino_sufijo": suffix_origin,
            "comision_origen_evento": explicit_origin,
            "comision_origen_proxy": origin_proxy,
            "origin_proxy_source": origin_source,
            "origin_proxy_mismatch": "1" if mismatch else "0",
            "tema_proxy_origen": COMMISSION_TOPIC.get(origin_proxy, ""),
            "materia_pagina": project.get("materia_pagina", ""),
            "materias_oficiales": unique_join(by_subjects.get(bill, [])),
            "comisiones_tramitacion": unique_join(commission_names),
            "temas_proxy_trayectoria": unique_join(trajectory_topics),
            "comisiones_sustantivas": unique_join(substantive),
            "ministerios": unique_join(by_ministries.get(bill, [])),
            "text_quality": text_quality.get(bill, ""),
            "signal_strength": signal_strength,
            "review_reason": unique_join(review_reasons),
            "origin_evidence_event": origin_evidence,
        })

    OUT.mkdir(parents=True, exist_ok=True)
    commission_fields = [
        "boletin", "sequence", "commission", "topic_proxy", "is_origin_proxy",
        "is_transversal", "source_type", "first_seen_date", "etapa", "evidence_event", "source_url",
    ]
    with (OUT / "project_commissions.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=commission_fields)
        writer.writeheader()
        writer.writerows(commission_rows)

    signal_fields = [
        "boletin", "titulo", "origen_iniciativa", "codigo_destinacion",
        "comision_destino_sufijo", "comision_origen_evento", "comision_origen_proxy",
        "origin_proxy_source", "origin_proxy_mismatch", "tema_proxy_origen",
        "materia_pagina", "materias_oficiales", "comisiones_tramitacion",
        "temas_proxy_trayectoria", "comisiones_sustantivas", "ministerios", "text_quality",
        "signal_strength", "review_reason", "origin_evidence_event",
    ]
    with (OUT / "project_topic_signals.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=signal_fields)
        writer.writeheader()
        writer.writerows(signal_rows)

    diagnostics = {
        "projects": len(projects),
        "projects_with_suffix_destination_proxy": sum(bool(x["comision_destino_sufijo"]) for x in signal_rows),
        "projects_with_explicit_origin_event": sum(bool(x["comision_origen_evento"]) for x in signal_rows),
        "projects_with_origin_commission_proxy": sum(bool(x["comision_origen_proxy"]) for x in signal_rows),
        "projects_with_any_commission": sum(bool(x["comisiones_tramitacion"]) for x in signal_rows),
        "projects_with_public_matter": sum(bool(x["materia_pagina"]) for x in signal_rows),
        "projects_with_xml_subject": sum(bool(x["materias_oficiales"]) for x in signal_rows),
        "commission_relations": len(commission_rows),
        "origin_proxy_mismatches": len(mismatches),
        "unknown_destination_codes": dict(sorted(unknown_codes.items())),
        "high_signal": sum(x["signal_strength"] == "alta" for x in signal_rows),
        "medium_signal": sum(x["signal_strength"] == "media" for x in signal_rows),
        "low_signal": sum(x["signal_strength"] == "baja" for x in signal_rows),
        "mismatch_examples": mismatches[:20],
    }
    (OUT / "topic_signal_diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
