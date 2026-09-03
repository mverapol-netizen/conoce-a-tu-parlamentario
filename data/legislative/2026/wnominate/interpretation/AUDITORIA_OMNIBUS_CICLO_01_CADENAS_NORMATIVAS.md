# Auditoría omnibus 18216-05 — Ciclo 01: cadenas normativas

> Documento interno de investigación. No usar todavía como texto público ni como etiqueta definitiva de D1.
>
> Corte: 2 de septiembre de 2026. Este documento complementa `PROTOCOLO_OMNIBUS_18216_05.md` y `MAPA_FAMILIAS_OMNIBUS_18216_05_V0_1.md`.

## 1. Hallazgo metodológico

La auditoría de las primeras votaciones prioritarias demuestra que dentro de un proyecto omnibus existen al menos **tres niveles distintos de dependencia**:

1. **boletín/proyecto:** todas las votaciones pertenecen al 18216-05;
2. **familia sustantiva:** varias disposiciones pueden pertenecer a crédito, tributación, trabajo, ambiente, etc.;
3. **cadena normativa:** una misma norma o conflicto de política puede ser votado varias veces a lo largo de distintos trámites.

Para la estimación W-NOMINATE la unidad observada sigue siendo el roll call. Para la **interpretación sustantiva**, en cambio, varias votaciones pertenecientes a una misma cadena normativa **no constituyen evidencia independiente**.

Esto resuelve un problema que el agrupamiento por proyecto no podía resolver: `bill=18216-05` es demasiado grueso, mientras `vote_id` es demasiado fino.

---

## 2. Cadena 1 — Prohibición del anatocismo

### Etapa A: incorporación de la norma

**Vote ID 88948 — 20 mayo 2026.**

Indicación renovada del diputado Raúl Soto para reemplazar el artículo 9 de la Ley 18.010 y prohibir estipular intereses sobre intereses o capitalizarlos. Resultado: **79 sí / 57 no / 17 abstenciones**.

Coalición temporal en nuestra base: oposición 64/0 a favor, oficialismo 1/50, no alineados 14/7.

### Etapa B: veto presidencial

**Vote ID 89668 — 10 agosto 2026.**

Observación presidencial N°1 para suprimir el artículo 32 incorporado durante la tramitación. El Senado identifica expresamente esta observación como el veto a la **prohibición absoluta del anatocismo**. En Cámara: **75 sí / 59 no / 12 abstenciones** para el veto supresivo.

### Decisión de auditoría

Ambos roll calls expresan la **misma disputa sustantiva** en etapas distintas. Se codifican como:

`ANATOCISM_POLICY_CHAIN`

La cadena puede aportar evidencia sobre `protección del deudor/regulación financiera ↔ mayor libertad contractual`, pero **88948 y 89668 no se suman como dos confirmaciones independientes**.

Fuentes:
- VotoPublico, ficha del boletín 18216-05: https://www.votopublico.cl/cl/leyes/18216
- Senado, agenda de vetos: https://www.senado.cl/comunicaciones/noticias/semana-legislativa-estara-marcada-por-los-vetos-megarreforma-y-el-proyecto
- Senado, aprobación de vetos: https://www.senado.cl/comunicaciones/noticias/proyecto-de-reconstruccion-con-aprobacion-de-vetos-supresivos-camara-alta

---

## 3. Cadena 2 — Derecho al olvido financiero

### Etapa A: intento de incorporación

**Vote ID 88955 — 20 mayo 2026.**

Reclamación contra la declaración de inadmisibilidad de una indicación que establecía un derecho al olvido financiero. La propuesta obligaba, entre otras cosas, a eliminar registros de información financiera de ciertas deudas impagas o extinguidas con más de cinco años y prohibía usar deudas extinguidas, prescritas o pagadas como criterio para denegar crédito. Resultado: **74 sí / 78 no / 1 abstención**.

En la base D1: oposición 62/2 a favor; oficialismo 0/67; no alineados 12/9.

El rechazo de esta reclamación no agotó el conflicto: una norma de derecho al olvido financiero fue incorporada posteriormente durante la tramitación y llegó a la fase de veto.

### Etapa B: veto presidencial

**Vote ID 89669 — 10 agosto 2026.**

Segunda observación presidencial supresiva, identificada oficialmente por el Senado como referida al **derecho al olvido financiero**. Resultado en Cámara: **75 sí / 58 no / 13 abstenciones**.

En la base D1: oficialismo 66/0 a favor del veto; oposición 1/58; no alineados 8/0.

### Decisión de auditoría

Se codifican dentro de:

`RIGHT_TO_FORGOTTEN_POLICY_CHAIN`

No se presupone que el texto inicial y el artículo finalmente vetado sean literalmente idénticos. La dependencia aquí es de **conflicto de política pública**, no necesariamente de identidad textual. Antes de producir una narrativa pública se recuperará también la genealogía del texto que finalmente se convirtió en el artículo 39.

Fuentes:
- VotoPublico, texto y recuento de la indicación inicial: https://www.votopublico.cl/cl/leyes/18216
- Senado, identificación oficial de los tres vetos: https://www.senado.cl/comunicaciones/noticias/semana-legislativa-estara-marcada-por-los-vetos-megarreforma-y-el-proyecto

---

## 4. Cadena 3 — Plazos de pago a pymes

**Vote ID 89670 — 10 agosto 2026.**

Tercera observación presidencial supresiva. El Senado identifica el conflicto como **pago a las pymes**; la norma vetada restringía la posibilidad de pactar plazos de pago superiores a treinta días. La Cámara aprobó el veto por **74 sí / 50 no / 22 abstenciones**.

Se abre:

`PAYMENT_TERMS_PYMES_POLICY_CHAIN`

El origen legislativo de la disposición todavía debe ser identificado dentro de las votaciones anteriores del 18216-05. Hasta entonces, 89670 queda como una etapa cerrada de una cadena aún incompleta y no se cuenta como una familia independiente adicional.

---

## 5. Igualdad de recuentos no significa identidad normativa

Los **vote ID 89485 y 89486**, ambos del 21 de julio, tienen exactamente el mismo resultado `75 sí / 70 no` y la misma coalición observable. Sin embargo, la auditoría formal muestra que corresponden a objetos distintos:

- 89485: modificación del Senado que suprime el artículo 31;
- 89486: modificación del Senado que incorpora un artículo 33 nuevo.

Por tanto, **no se deduplican por similitud de patrón de votos**. Permanecen en un grupo provisional mientras se recupera el contenido sustantivo de ambos artículos.

Regla:

> mismo recuento + misma coalición ≠ misma norma.

La dependencia debe probarse por genealogía normativa, no por correlación de votos.

---

## 6. Resultado legislativo y voto binario tampoco son equivalentes

**Vote ID 89488** ilustra otro problema. El nuevo artículo 35 del Senado recibió **76 votos a favor y 69 en contra**, pero fue rechazado porque requería un quórum de **78 votos** al tratarse de una norma orgánica constitucional.

Para W-NOMINATE, los 76 `Sí` y 69 `No` siguen siendo decisiones individuales válidas para estimar posiciones. Para interpretar el proceso legislativo, sin embargo, debemos registrar que la disposición **no fue aprobada**.

Regla:

> `mayoría de votos Sí` no implica necesariamente `norma aprobada` cuando existe un quórum especial.

El motor público deberá separar siempre `cómo votaron los parlamentarios` de `qué ocurrió jurídicamente con la disposición`.

---

## 7. Nueva unidad de independencia interpretativa

A partir de este ciclo, cada roll call omnibus debe poder asociarse a:

- `substantive_family` — familia temática;
- `process_type` — etapa o mecanismo legislativo;
- `policy_chain` — norma/conflicto sustantivo a través del tiempo;
- `vote_id` — observación concreta empleada por el modelo.

Jerarquía:

`familia sustantiva → cadena normativa → roll call`

Para describir D1 públicamente, la evidencia repetida dentro de una misma `policy_chain` se resumirá como **un solo conflicto sustantivo**, aunque pueda contener múltiples roll calls informativos para la estimación.

---

## 8. Implicación para el peso aparente de la Megareforma

Sabemos que 116 de las 276 votaciones seleccionadas por D1 pertenecen al 18216-05. Este número **no equivale a 116 conflictos políticos independientes**.

La aparición temprana de al menos dos cadenas normativas demostradas —anatocismo y derecho al olvido financiero— confirma que una fracción desconocida de esas 116 observaciones corresponde a distintas etapas de conflictos repetidos, artículos conexos, reconsideraciones, enmiendas y vetos.

Por ello, la concentración bruta de roll calls sobrestima necesariamente el número de unidades sustantivas independientes, aunque no sabemos todavía en qué magnitud.

Esto **no invalida la estimación W-NOMINATE**. Sí modifica la manera correcta de usar la Megareforma para interpretar qué representa D1.

---

## 9. Estado del ciclo

**Ciclo 01 de cadenas normativas: CERRADO.**

Cadenas identificadas:

1. `ANATOCISM_POLICY_CHAIN` — 88948 ↔ 89668.
2. `RIGHT_TO_FORGOTTEN_POLICY_CHAIN` — 88955 ↔ 89669.
3. `PAYMENT_TERMS_PYMES_POLICY_CHAIN` — 89670, origen previo pendiente.

Casos metodológicos de control:

- 89485/89486: misma coalición no basta para deduplicar;
- 89488: mayoría binaria no basta para determinar aprobación cuando existe quórum especial.

**Siguiente ciclo:** ampliar la auditoría en la familia financiera/tributaria para identificar el origen del artículo 40, cerrar artículos 4/25/27/28/31/33/35 y empezar a convertir los 116 roll calls en un número menor y justificable de cadenas normativas independientes.