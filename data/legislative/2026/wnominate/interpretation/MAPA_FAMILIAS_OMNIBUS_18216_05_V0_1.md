# Mapa de familias internas — Megareforma 18216-05 v0.1

> Documento interno de investigación. No usar todavía como texto público ni como evidencia definitiva para nombrar D1 o D2.
>
> Corte: 2 de septiembre de 2026. El boletín 18216-05 es un proyecto omnibus del gobierno de José Antonio Kast. De las 276 votaciones seleccionadas en la corrida research de D1, 116 pertenecen a este boletín. La ficha pública del proyecto registra un universo de votaciones de Cámara algo mayor; esta diferencia no se interpreta aquí sin auditar exactamente las reglas de selección de W-NOMINATE y las votaciones excluidas.

## 1. Problema que resuelve este mapa

El proyecto reúne medidas tributarias, fiscales, regulatorias, laborales, ambientales, de reconstrucción, vivienda, inversión, administración pública y otras materias. Por eso una clasificación exclusiva por `boletín` es sustantivamente inútil, pero contar cada roll call como una pieza independiente sobreponderaría una sola iniciativa.

La solución v0.1 es clasificar cada votación en **dos dimensiones simultáneas**:

1. **familia sustantiva**: qué problema o política pública contiene la disposición;
2. **tipo de trámite**: cómo llegó esa disposición a la votación de Sala.

Una misma fila puede ser, por ejemplo, `crédito y deuda de hogares` en contenido y `indicación renovada` en procedimiento. El tipo de trámite nunca reemplaza el contenido sustantivo.

## 2. Familias sustantivas provisionales

### F1 — Reconstrucción, emergencia y vivienda

Incluye fondos de emergencia, alivios por catástrofe, deudas municipales, reconexión de servicios, medidas de vivienda y beneficios transitorios asociados a reconstrucción.

**Pregunta interpretativa:** ¿la coalición responde a distribución de costos de reconstrucción, alivio social, gasto público o a detalles instrumentales?

### F2 — Tributación, recaudación y distribución

Incluye impuesto corporativo, repatriación o regularización de capitales, FUT/FUR, contribuciones, beneficios tributarios, propuestas de IVA compensatorio y otras reglas distributivas.

**Pregunta:** ¿aparece una oposición redistribución/progresividad ↔ reducción o estabilidad tributaria?

### F3 — Inversión, certeza jurídica y facilitación regulatoria

Incluye invariabilidad tributaria, depreciación, reglas orientadas a inversión, plazos administrativos y mecanismos de aceleración de permisos.

**Pregunta:** ¿reproduce el componente regulación/intervención ↔ inversión/mercado ya encontrado fuera de la Megareforma?

### F4 — Medio ambiente, territorio y regulación sectorial

Incluye SEIA/RCA, acuicultura, energía, medidas cautelares ambientales, SBAP, patrimonio/monumentos y otras reformas sectoriales vinculadas a permisos y control ambiental.

**Pregunta:** ¿la coalición vuelve a ordenar izquierda/centroizquierda versus derecha, o aparecen fracturas regulatorias internas?

### F5 — Trabajo, empleo, capacitación y función pública

Incluye incentivos a formalización, capacitación, SENCE/ChileValora, reglas laborales, sala cuna y medidas sobre funcionarios públicos/licencias médicas.

**Pregunta:** distinguir protección laboral/distribución de medidas de probidad o disciplina administrativa.

### F6 — Crédito, deuda de hogares y protección financiera

Incluye anatocismo/intereses sobre intereses, reprogramación de deudas, condonaciones, información financiera y propuestas de protección al deudor/consumidor.

**Pregunta:** ¿reaparece la oposición regulación/protección ↔ libertad contractual/mercado financiero?

### F7 — Gestión pública, datos, probidad y fiscalización

Incluye intercambio de datos públicos, evaluación ex post, controles sobre beneficios a autoridades, información al Congreso, eficiencia presupuestaria y otras normas de accountability.

**Pregunta:** separar cuidadosamente conflicto ideológico de una lógica contingente gobierno–oposición.

### F8 — Seguridad, aduanas y administración miscelánea

Incluye disposiciones de seguridad, transporte, aduanas, contrabando u otras materias que no correspondan a las familias anteriores.

**Pregunta:** comprobar si estas disposiciones reactivan orden/garantías o si son acuerdos amplios/actor-específicos.

## 3. Tipos de trámite

Cada roll call debe recibir además uno de estos valores en `process_type`:

- `general` — votación general del proyecto o capítulo;
- `article_original` — artículo del mensaje/proyecto original;
- `commission_text` — texto propuesto por una comisión;
- `separate_vote` — disposición solicitada a votación separada;
- `renewed_amendment` — indicación renovada en Sala;
- `inadmissibility_reconsideration` — reconsideración de inadmisibilidad;
- `senate_amendment` — modificación introducida por el Senado en tercer trámite;
- `presidential_veto` — observación/veto del Presidente;
- `quorum_or_constitutional` — decisión ligada a quórum, constitucionalidad o reserva;
- `procedural_other` — otra decisión procedimental;
- `pending_exact` — todavía no recuperado.

Un `process_type` procedimental no vuelve “no sustantiva” a una indicación: se conserva además su `substantive_family` cuando el texto de fondo es conocido.

## 4. Primeras votaciones prioritarias del subcorpus

### 88948 — prioridad máxima

- **Rango omnibus D1:** 1.
- **Resultado:** 79 sí / 57 no / 17 abstenciones.
- **Coalición temporal:** oposición 64/0 a favor; oficialismo 1/50; no alineados 14/7.
- **Objeto exacto:** indicación renovada de Raúl Soto para impedir estipular/capitalizar intereses sobre intereses.
- **Familia:** `F6 crédito/deuda/protección financiera`.
- **Proceso:** `renewed_amendment`.
- **Lectura inicial:** candidato Nivel I. Es sustantivamente interpretable y reproduce un conflicto regulación/protección financiera ↔ mayor libertad contractual. Debe contrastarse con casos externos al omnibus antes de usarlo como evidencia independiente del eje.

### 88936 — alta fuerza matemática, bajo peso narrativo inicial

- **Rango:** 6.
- **Resultado:** 127 sí / 6 no / 19 abstenciones.
- **Objeto:** artículo 26, texto de Trabajo; asociado a sanciones para funcionarios públicos por incumplimientos vinculados a licencias médicas.
- **Familia:** `F5 función pública/probidad laboral`.
- **Proceso:** `commission_text`.
- **Lectura:** probablemente Nivel III/IV para nombrar D1: seis votos negativos pueden ser muy útiles para localizar individuos pero no representan una gran división de Cámara.

### 88933 — prioridad alta, contenido todavía por cerrar

- **Rango:** 3.
- **Resultado:** 58 sí / 94 no.
- **Objeto formal:** artículo 27 del mensaje original, respecto del cual Hacienda/Trabajo propusieron rechazo.
- **Familia:** `pending_exact`.
- **Proceso:** `article_original`.
- **Lectura:** coalición fuerte, pero queda fuera de conclusión sustantiva hasta recuperar el efecto normativo exacto.

### 89485 y 89486 — no asumir independencia

- **Rangos:** 4 y 5 aproximadamente entre los líderes del subcorpus.
- **Fecha:** 21 julio.
- **Resultado idéntico:** 75 sí / 70 no.
- **Coalición:** derecha/oficialismo a favor, oposición en contra.
- **89485:** modificación del Senado que suprime el artículo 31.
- **89486:** objeto exacto todavía debe cerrarse.
- **Proceso:** `senate_amendment`.
- **Regla:** se marcan provisionalmente como `possible_duplicate_group=JUL21_75_70_A` hasta comprobar si son decisiones normativamente distintas o una repetición/encadenamiento técnico. No cuentan como dos evidencias independientes por ahora.

### 89668 y 89670 — veto como envoltorio procedimental

- **89668:** observación presidencial N°1 para suprimir artículo 32, 75–59–12.
- **89670:** observación presidencial N°3 para suprimir artículo 40, 74–50–22.
- **Proceso:** `presidential_veto`.
- **Familia:** pendiente de recuperar contenido exacto de los artículos 32 y 40.
- **Regla:** no interpretar “veto” como familia sustantiva. Primero debe saberse qué política se estaba suprimiendo.

### 89488 — disposición nueva del Senado con quórum especial

- **Resultado:** 76–69.
- **Objeto formal:** incorporación de nuevo artículo 35, sometido a quórum especial.
- **Proceso:** `senate_amendment` + `quorum_or_constitutional`.
- **Familia:** pendiente.
- **Regla:** prioridad alta para recuperar texto, pero todavía no pesa en interpretación.

### 88900 — empate perfecto, artículo original

- **Resultado:** 77–77.
- **Objeto:** artículo 4 del mensaje original, respecto del cual Hacienda propuso rechazo.
- **Proceso:** `article_original`.
- **Familia:** pendiente exacta.
- **Lectura:** matemáticamente muy informativa, pero el empate no dice qué conflicto es hasta recuperar el artículo.

### 88938 — mayoría transversal con disidencia concentrada

- **Resultado:** 142–10.
- **Objeto formal:** artículo 28.
- **Familia:** pendiente exacta.
- **Lectura:** candidato actor-específico/gradiente; no debe confundirse con un clivaje amplio pese a su alto `spread`.

## 5. Hallazgo metodológico v0.1

La primera inspección confirma por qué el tratamiento especial era necesario. Entre las votaciones más identificadoras del mismo boletín conviven:

- una regulación crediticia sustantiva claramente interpretable;
- sanciones administrativas con apenas seis votos negativos;
- enmiendas del Senado con coaliciones idénticas;
- observaciones presidenciales;
- artículos originales que las comisiones propusieron rechazar;
- decisiones de quórum/constitucionalidad.

Por tanto, **la concentración de 116 roll calls del 18216-05 puede amplificar simultáneamente conflictos ideológicos sustantivos, gobierno–oposición y dependencia serial/procedimental**. Sin esta auditoría, cualquiera de esas fuentes podría confundirse con “el significado” de D1.

## 6. Relación con la auditoría transversal

Hasta este mapa v0.1 **no aparece evidencia que obligue a abandonar** la conclusión transversal de D1 como continuo político-ideológico amplio asociado a izquierda–derecha. Sin embargo, todavía sería incorrecto afirmar que la Megareforma la confirma: falta clasificar sus familias y reducir la dependencia interna.

La prueba correcta será:

1. identificar familias sustantivas;
2. colapsar repeticiones/duplicaciones dentro de cada familia;
3. seleccionar uno o pocos casos representativos por familia;
4. comparar sus coaliciones con proyectos externos equivalentes;
5. medir cuánto de la polarización del omnibus es ideológica y cuánto es gobierno–oposición/procedimiento.

## 7. Salida de trabajo asociada

`omnibus_18216_05_audit_worklist.csv` contiene el esquema de auditoría y los primeros diez casos prioritarios. La tabla se irá completando hasta cubrir los 116 roll calls seleccionados en D1.

## 8. Estado

**Mapa de familias v0.1: CERRADO.**

No se han contado todavía frecuencias por familia porque clasificar automáticamente las 116 votaciones desde el título del proyecto sería precisamente el error que este protocolo busca evitar.

**Siguiente ciclo:** recuperar y codificar el contenido exacto de las votaciones prioritarias y después expandir la clasificación por familias en lotes, empezando por tributación/crédito y por los artículos/vetos de mayor `abs(spread`.