from __future__ import annotations

import csv
import json
import math
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

from derive_topic_signals import COMMISSION_TOPIC, TRANSVERSAL

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "legislative" / "2026"
TOPICS = DATA / "topics"

# La clasificación se apoya primero en señales institucionales. El léxico solo
# interviene cuando la comisión de destinación es transversal o la trayectoria
# exige desambiguación. No usa partido, bancada ni autores.
TOPIC_LEXICON: dict[str, list[str]] = {
    "Seguridad": [
        "seguridad publica", "seguridad ciudadana", "crimen organizado", "narcotrafico",
        "armas", "homicidio", "secuestro", "delitos graves", "orden publico", "carabineros",
        "policia", "incautacion", "prision preventiva", "persecucion penal", "control de identidad",
        "trafico ilicito", "terrorismo",
    ],
    "Constitución y justicia": [
        "constitucion", "carta fundamental", "codigo procesal", "procedimiento judicial",
        "tribunal", "tribunales", "corte suprema", "ministerio publico", "fiscalia", "jueces",
        "recurso judicial", "indulto", "codigo penal", "sancion penal", "justicia",
    ],
    "Educación": [
        "educacion", "educacional", "escuela", "escolar", "colegio", "liceo", "docente",
        "profesor", "estudiante", "universidad", "aula", "apoderado", "convivencia escolar",
        "comunidad educativa",
    ],
    "Salud": [
        "salud", "sanitario", "sanitaria", "hospital", "medicamento", "vacuna", "inmunizacion",
        "paciente", "cancer", "enfermedad", "fonasa", "isapre", "medico", "farmaco",
        "atencion primaria",
    ],
    "Economía y hacienda": [
        "impuesto", "tributario", "tributaria", "presupuesto", "deuda publica", "politica fiscal",
        "gasto fiscal", "ingresos fiscales", "hacienda", "finanzas publicas", "exencion tributaria",
    ],
    "Economía, comercio y consumidores": [
        "consumidor", "consumidores", "comercio", "empresa", "empresas", "pyme", "mipyme",
        "competencia", "mercado", "turismo", "industria", "emprendimiento",
    ],
    "Trabajo y seguridad social": [
        "trabajo", "laboral", "trabajador", "trabajadores", "sindicato", "negociacion colectiva",
        "remuneracion", "fuero laboral", "jornada laboral", "contrato de trabajo", "cotizacion",
        "prevision", "pension", "pensiones",
    ],
    "Vivienda y territorio": [
        "vivienda", "habitacional", "urbanismo", "urbanistico", "construccion", "loteo",
        "copropiedad", "suelo urbano", "regularizacion de viviendas", "bienes nacionales",
    ],
    "Medio ambiente": [
        "medio ambiente", "ambiental", "biodiversidad", "contaminacion", "residuos", "reciclaje",
        "cambio climatico", "ecosistema", "conservacion", "evaluacion ambiental",
    ],
    "Minería y energía": [
        "mineria", "minero", "litio", "cobre", "energia", "electrico", "electricidad", "combustible",
        "kerosene", "petroleo", "gas natural", "hidrocarburo", "generacion electrica",
    ],
    "Agua y recursos hídricos": [
        "recursos hidricos", "recurso hidrico", "derechos de aprovechamiento de aguas", "codigo de aguas",
        "sequía", "sequia", "desertificacion", "agua potable", "cuenca", "acuifero",
    ],
    "Agricultura y mundo rural": [
        "agricultura", "agricola", "ganaderia", "ganadero", "silvicultura", "forestal", "mundo rural",
        "riego", "campesino",
    ],
    "Pesca y acuicultura": [
        "pesca", "pesquero", "acuicultura", "acuicola", "recursos hidrobiologicos", "caleta",
    ],
    "Transportes y telecomunicaciones": [
        "transporte", "transito", "vehiculo", "conductor", "licencia de conducir", "telecomunicaciones",
        "telefonia", "internet", "aeronautica", "aviacion", "ferrocarril",
    ],
    "Infraestructura y obras públicas": [
        "obras publicas", "infraestructura", "carretera", "camino publico", "puente", "concesion vial",
        "puerto", "embalse",
    ],
    "Cultura y comunicaciones": [
        "cultura", "cultural", "patrimonio", "arte", "artes", "television", "radiodifusion",
        "medios de comunicacion", "monumento", "biblioteca", "museo",
    ],
    "Deportes": [
        "deporte", "deportivo", "deportista", "estadio", "federacion deportiva", "actividad fisica",
    ],
    "Desarrollo social": [
        "pobreza", "vulnerabilidad", "proteccion social", "beneficio social", "subsidio social",
        "cuidados", "inclusion social", "registro social de hogares",
    ],
    "Personas mayores y discapacidad": [
        "discapacidad", "persona mayor", "personas mayores", "sindrome de down", "dependencia severa",
        "accesibilidad universal",
    ],
    "Familia, infancia y adolescencia": [
        "nino", "nina", "adolescente", "infancia", "familia", "adopcion", "cuidado personal",
        "proteccion de la ninez", "responsabilidad penal adolescente", "pension de alimentos",
    ],
    "Mujeres y género": [
        "mujer", "mujeres", "genero", "violencia de genero", "femicidio", "equidad de genero",
        "violencia intrafamiliar", "acoso sexual",
    ],
    "Derechos humanos": [
        "derechos humanos", "pueblos originarios", "pueblo indigena", "indigena", "libertad de culto",
        "discriminacion", "derechos fundamentales", "tortura", "memoria historica",
    ],
    "Ciencia y tecnología": [
        "inteligencia artificial", "ciberseguridad", "datos personales", "proteccion de datos", "tecnologia",
        "innovacion", "ciencia", "cientifico", "algoritmo", "plataforma digital", "firma electronica",
    ],
    "Relaciones exteriores": [
        "tratado internacional", "relaciones exteriores", "cooperacion internacional", "frontera",
        "migracion", "migrante", "extranjero", "refugiado", "consular", "integracion latinoamericana",
    ],
    "Gobierno interior y descentralización": [
        "municipalidad", "municipal", "gobierno regional", "regionalizacion", "descentralizacion",
        "administracion del estado", "probidad administrativa", "funcionario publico", "alcalde",
        "gobernador regional", "nacionalidad", "ciudadania",
    ],
    "Defensa": [
        "defensa nacional", "fuerzas armadas", "ejercito", "armada", "fuerza aerea", "militar",
        "estado mayor conjunto", "servicio militar",
    ],
    "Territorio y zonas extremas": [
        "zona extrema", "zonas extremas", "antartica", "isla de pascua", "territorio especial",
        "aislamiento territorial",
    ],
}

MINISTRY_TOPIC = {
    "ministerio de educacion": "Educación",
    "ministerio de salud": "Salud",
    "ministerio de seguridad publica": "Seguridad",
    "ministerio de justicia y de derechos humanos": "Constitución y justicia",
    "ministerio de hacienda": "Economía y hacienda",
    "ministerio del trabajo y prevision social": "Trabajo y seguridad social",
    "ministerio de vivienda y urbanismo": "Vivienda y territorio",
    "ministerio del medio ambiente": "Medio ambiente",
    "ministerio de mineria": "Minería y energía",
    "ministerio de energia": "Minería y energía",
    "ministerio de agricultura": "Agricultura y mundo rural",
    "ministerio de transportes y telecomunicaciones": "Transportes y telecomunicaciones",
    "ministerio de obras publicas": "Infraestructura y obras públicas",
    "ministerio de desarrollo social y familia": "Desarrollo social",
    "ministerio de la mujer y la equidad de genero": "Mujeres y género",
    "ministerio de relaciones exteriores": "Relaciones exteriores",
    "ministerio de defensa nacional": "Defensa",
}


def norm(value: str) -> str:
    text = unicodedata.normalize("NFD", str(value or "").lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9ñ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_texts() -> dict[str, str]:
    path = TOPICS / "project_texts.jsonl"
    result: dict[str, str] = {}
    if not path.exists():
        return result
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            bill = str(row.get("boletin", "")).strip()
            text = row.get("cleaned_text") or row.get("text") or row.get("raw_text") or ""
            if bill:
                result[bill] = str(text)
    return result


def split_pipe(value: str) -> list[str]:
    return [x.strip() for x in str(value or "").split("|") if x.strip()]


def term_count(text: str, term: str) -> int:
    phrase = norm(term)
    if not phrase:
        return 0
    # Las frases son suficientemente específicas; limitamos la contribución de
    # repeticiones para evitar que un documento largo domine por reiteración.
    return min(text.count(phrase), 4)


def lexical_scores(title: str, body: str, ministries: str) -> dict[str, float]:
    title_n = norm(title)
    body_n = norm(body[:45000])
    ministry_n = norm(ministries)
    scores: dict[str, float] = defaultdict(float)

    for topic, terms in TOPIC_LEXICON.items():
        for term in terms:
            scores[topic] += 5.0 * term_count(title_n, term)
            scores[topic] += 0.75 * term_count(body_n, term)

    for ministry, topic in MINISTRY_TOPIC.items():
        if ministry in ministry_n:
            scores[topic] += 7.0
    return dict(scores)


def confidence(top: float, second: float, institutional_bonus: float = 0.0) -> float:
    if top <= 0:
        return 0.5
    margin = max(top - second, 0.0)
    raw = 0.56 + min(0.22, top * 0.018) + min(0.14, margin * 0.018) + institutional_bonus
    return round(min(raw, 0.98), 3)


def classify(row: dict, body: str) -> dict:
    origin_commission = row.get("comision_origen_proxy", "")
    origin_topic = row.get("tema_proxy_origen", "")
    trajectory_topics = split_pipe(row.get("temas_proxy_trayectoria", ""))
    substantive_commissions = split_pipe(row.get("comisiones_sustantivas", ""))
    substantive_topics = []
    for commission in substantive_commissions:
        topic = COMMISSION_TOPIC.get(commission, "")
        if topic and topic not in substantive_topics:
            substantive_topics.append(topic)

    secondary: list[str] = []
    evidence: list[str] = []
    needs_review = False
    review_reason = []

    # Caso institucional fuerte: la comisión inicial es sustantiva. No hace
    # falta que un modelo redescubra lo que el Congreso ya clasificó.
    if origin_commission and origin_commission not in TRANSVERSAL and origin_topic:
        primary = origin_topic
        method = "institucional_destinacion"
        conf = 0.97
        evidence.append(f"comision_origen={origin_commission}")
        for topic in trajectory_topics:
            if topic and topic != primary and topic not in secondary:
                secondary.append(topic)
        return {
            "primary": primary,
            "secondary": secondary,
            "method": method,
            "confidence": conf,
            "needs_review": needs_review,
            "review_reason": review_reason,
            "evidence": evidence,
            "scores": {},
        }

    # Si la destinación inicial es transversal pero luego existe una única
    # comisión claramente sustantiva, esa trayectoria tiene prioridad.
    if origin_commission in TRANSVERSAL and len(substantive_topics) == 1:
        primary = substantive_topics[0]
        method = "institucional_trayectoria"
        conf = 0.94
        evidence.extend([f"comision_origen_transversal={origin_commission}", f"comision_sustantiva={substantive_commissions[0]}"])
        if origin_topic and origin_topic != primary:
            secondary.append(origin_topic)
        return {
            "primary": primary,
            "secondary": secondary,
            "method": method,
            "confidence": conf,
            "needs_review": False,
            "review_reason": [],
            "evidence": evidence,
            "scores": {},
        }

    scores = lexical_scores(row.get("titulo", ""), body, row.get("ministerios", ""))

    # La trayectoria institucional suma evidencia, pero no deja que Hacienda o
    # Constitución ganen automáticamente por ser filtros transversales.
    for topic in substantive_topics:
        scores[topic] = scores.get(topic, 0.0) + 8.0
    if origin_topic:
        scores[origin_topic] = scores.get(origin_topic, 0.0) + (1.0 if origin_commission in TRANSVERSAL else 4.0)

    ordered = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    top_topic, top_score = ordered[0] if ordered else (origin_topic or "Sin clasificar", 0.0)
    second_topic, second_score = ordered[1] if len(ordered) > 1 else ("", 0.0)

    if top_score <= 0 and origin_topic:
        top_topic = origin_topic
        top_score = 1.0
        method = "institucional_transversal_sin_resolucion"
        needs_review = True
        review_reason.append("sin_evidencia_semantica_suficiente")
    else:
        method = "hibrido_institucional_texto"

    margin = top_score - second_score
    conf = confidence(top_score, second_score, 0.02 if substantive_topics else 0.0)

    # Umbral deliberadamente conservador. El sistema puede resolver bastante,
    # pero un empate real debe llegar a revisión humana/modelo.
    if top_score < 7.0:
        needs_review = True
        review_reason.append("evidencia_semantica_debil")
    if second_score > 0 and margin < 3.0:
        needs_review = True
        review_reason.append("empate_tematico")
    if origin_commission in TRANSVERSAL and top_topic == origin_topic and not substantive_topics and top_score < 10:
        needs_review = True
        review_reason.append("solo_comision_transversal")

    if second_topic and second_score >= max(5.0, top_score * 0.55) and second_topic != top_topic:
        secondary.append(second_topic)
    if origin_topic and origin_topic != top_topic and origin_commission in TRANSVERSAL and origin_topic not in secondary:
        secondary.append(origin_topic)

    evidence.append(f"origen={origin_commission or 'sin_comision'}")
    if substantive_commissions:
        evidence.append("trayectoria=" + " | ".join(substantive_commissions))
    evidence.append(f"score_1={top_topic}:{top_score:.2f}")
    if second_topic:
        evidence.append(f"score_2={second_topic}:{second_score:.2f}")

    return {
        "primary": top_topic,
        "secondary": secondary,
        "method": method,
        "confidence": conf,
        "needs_review": needs_review,
        "review_reason": review_reason,
        "evidence": evidence,
        "scores": dict(ordered[:6]),
    }


def main() -> None:
    rows = read_csv(TOPICS / "project_topic_signals.csv")
    texts = load_texts()
    if not rows:
        raise RuntimeError("No existe project_topic_signals.csv")

    classifications = []
    long_rows = []
    review_rows = []

    for row in rows:
        bill = row.get("boletin", "")
        result = classify(row, texts.get(bill, ""))
        secondary = [x for x in result["secondary"] if x and x != result["primary"]]
        secondary = list(dict.fromkeys(secondary))
        classification = {
            "boletin": bill,
            "titulo": row.get("titulo", ""),
            "origen_iniciativa": row.get("origen_iniciativa", ""),
            "comision_origen_proxy": row.get("comision_origen_proxy", ""),
            "comisiones_tramitacion": row.get("comisiones_tramitacion", ""),
            "topic_primary": result["primary"],
            "topic_secondary": " | ".join(secondary),
            "method": result["method"],
            "confidence": result["confidence"],
            "needs_review": "1" if result["needs_review"] else "0",
            "review_reason": " | ".join(result["review_reason"]),
            "evidence": " || ".join(result["evidence"]),
            "taxonomy_version": "institutional-hybrid-v0.3",
        }
        classifications.append(classification)
        long_rows.append({
            "boletin": bill,
            "topic": result["primary"],
            "role": "principal",
            "method": result["method"],
            "confidence": result["confidence"],
            "needs_review": classification["needs_review"],
            "taxonomy_version": classification["taxonomy_version"],
        })
        for topic in secondary:
            long_rows.append({
                "boletin": bill,
                "topic": topic,
                "role": "secundario",
                "method": result["method"],
                "confidence": result["confidence"],
                "needs_review": classification["needs_review"],
                "taxonomy_version": classification["taxonomy_version"],
            })

        if result["needs_review"]:
            review_rows.append({
                **classification,
                "text_excerpt": re.sub(r"\s+", " ", texts.get(bill, ""))[:3500],
                "top_scores": json.dumps(result["scores"], ensure_ascii=False),
            })

    TOPICS.mkdir(parents=True, exist_ok=True)
    class_fields = [
        "boletin", "titulo", "origen_iniciativa", "comision_origen_proxy", "comisiones_tramitacion",
        "topic_primary", "topic_secondary", "method", "confidence", "needs_review", "review_reason",
        "evidence", "taxonomy_version",
    ]
    with (TOPICS / "project_topic_classification.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=class_fields)
        writer.writeheader()
        writer.writerows(classifications)

    long_fields = ["boletin", "topic", "role", "method", "confidence", "needs_review", "taxonomy_version"]
    with (TOPICS / "project_topics.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=long_fields)
        writer.writeheader()
        writer.writerows(long_rows)

    review_fields = class_fields + ["text_excerpt", "top_scores"]
    review_rows.sort(key=lambda x: (float(x["confidence"]), x["boletin"]))
    with (TOPICS / "topic_review_queue.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=review_fields)
        writer.writeheader()
        writer.writerows(review_rows)

    by_method: dict[str, int] = defaultdict(int)
    by_topic: dict[str, int] = defaultdict(int)
    for row in classifications:
        by_method[row["method"]] += 1
        by_topic[row["topic_primary"]] += 1

    diagnostics = {
        "projects": len(classifications),
        "classified": sum(x["topic_primary"] != "Sin clasificar" for x in classifications),
        "auto_accepted": sum(x["needs_review"] == "0" for x in classifications),
        "review_queue": len(review_rows),
        "review_rate": round(len(review_rows) / max(len(classifications), 1), 4),
        "mean_confidence": round(sum(float(x["confidence"]) for x in classifications) / max(len(classifications), 1), 4),
        "methods": dict(sorted(by_method.items())),
        "primary_topics": dict(sorted(by_topic.items(), key=lambda kv: (-kv[1], kv[0]))),
    }
    (TOPICS / "topic_classifier_diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
