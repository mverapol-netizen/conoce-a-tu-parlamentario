# Auditoría de sensibilidad interpretativa D1 — `lop=.05` y `lop=.10`

> Documento interno de investigación. No usar todavía como etiqueta pública definitiva de D1 ni como autorización para publicar coordenadas individuales.
>
> Corte empírico: 2 de septiembre de 2026. Este ciclo continúa `BALANCE_HIPOTESIS_D1_30_NO_OMNIBUS.md` y `BALANCE_FINAL_OMNIBUS_18216_05.md`.

## 1. Pregunta del ciclo

El gate anterior dejó una pregunta precisa: ¿la interpretación de D1 como continuo político-ideológico amplio fuertemente asociado a izquierda–derecha depende de roll calls con minorías apenas superiores al umbral base de 2,5%?

La preocupación es sustantiva, no solo estadística. En las auditorías transversal y omnibus se comprobó que W-NOMINATE puede asignar un `abs(spread_1d)` muy alto a votaciones en que tres, seis, diez o catorce parlamentarios se separan de una mayoría enorme. Esas votaciones pueden ser excelentes para localizar individuos o subgrupos, pero pobres para nombrar el conflicto principal de la Cámara.

Por eso se comparan tres especificaciones idénticas salvo por el umbral de minoría binaria:

- `raw_lop025`: minoría mínima 2,5%;
- `raw_lop050`: minoría mínima 5%;
- `raw_lop100`: minoría mínima 10%.

La prueba tiene dos niveles:

1. **estabilidad geométrica:** verificar si cambian sustantivamente las coordenadas, el ajuste y la composición general del corpus;
2. **estabilidad interpretativa:** verificar si las familias y los casos de mayor peso sustantivo sobreviven mientras desaparecen preferentemente minorías delgadas.

---

## 2. Resultado estadístico general

La modificación del umbral elimina relativamente pocas votaciones:

| Especificación | `lop` | Roll calls | Proyectos | Mayor proyecto | Participación del mayor proyecto |
|---|---:|---:|---:|---:|---:|
| `raw_lop025` | 0,025 | 276 | 55 | 116 | 42,03% |
| `raw_lop050` | 0,050 | 269 | 54 | 114 | 42,38% |
| `raw_lop100` | 0,100 | 258 | 53 | 109 | 42,25% |

La Megareforma continúa representando algo más de 42% del corpus en las tres especificaciones. Por tanto, elevar `lop` **no resuelve ni pretende resolver** la dependencia por proyecto; esa dependencia sigue tratándose mediante el protocolo omnibus, caps, deduplicación y bootstrap agrupado.

Los tres modelos estiman 154 diputados. El ajuste permanece prácticamente constante:

| Especificación | Correctamente clasificado | APRE | GMP |
|---|---:|---:|---:|
| `raw_lop025` | 95,694% | 0,8823 | 0,8901 |
| `raw_lop050` | 95,639% | 0,8832 | 0,8923 |
| `raw_lop100` | 95,711% | 0,8889 | 0,8972 |

No existe deterioro del desempeño al excluir minorías pequeñas. En APRE y GMP la especificación `lop=.10` incluso mejora ligeramente, sin que esto deba interpretarse como una razón autónoma para escogerla como modelo principal.

---

## 3. Estabilidad de las coordenadas individuales

La prueba más fuerte es la comparación de las posiciones estimadas para los mismos 154 diputados.

### `raw_lop025` versus `raw_lop050`

- Pearson: **0,99958**
- Spearman: **0,99832**

### `raw_lop025` versus `raw_lop100`

- Pearson: **0,99702**
- Spearman: **0,98681**

### `raw_lop050` versus `raw_lop100`

- Pearson: **0,99757**
- Spearman: **0,99058**

La conclusión es inequívoca: la geometría de D1 no depende de conservar roll calls con minorías entre 2,5% y 10%. Incluso al exigir una minoría mínima de 10%, la posición relativa de los legisladores permanece extraordinariamente parecida.

Esto no significa que ninguna persona cambie algunos lugares en el ranking. Spearman menor que 1 indica movimientos locales. Significa que no aparece una reorganización sustantiva del espacio ni un eje alternativo.

---

## 4. Estabilidad del orden partidario

La estructura agregada por partido también permanece reconocible.

En `raw_lop025`, con la orientación interna ya alineada, aparecen en el polo positivo PC, FA y PS; luego PPD, liberales, radicales y DC; PDG se ubica cerca del centro; RN, UDI, PNL y Republicanos ocupan el polo negativo.

Con `raw_lop100` la misma secuencia general sobrevive. Medias aproximadas:

| Partido | D1 media `lop=.10` |
|---|---:|
| PC | +0,970 |
| Acción Humanista | +0,836 |
| FA | +0,750 |
| PS | +0,536 |
| PPD | +0,335 |
| Radical | +0,251 |
| Liberal | +0,221 |
| DC | +0,178 |
| PDG | −0,109 |
| RN | −0,718 |
| UDI | −0,827 |
| PNL | −0,858 |
| Republicanos | −0,993 |

La orientación del signo sigue siendo una convención de identificación; la evidencia relevante es la estabilidad del orden relativo.

La persistencia del gradiente resulta especialmente importante porque el aumento de `lop` elimina varias votaciones que localizaban pequeñas minorías en PC, FA, PNL u otros grupos. El orden partidario no colapsa cuando esas observaciones dejan de contribuir.

---

## 5. Cobertura temática con `lop=.10`

Al mantener el piso de participación binaria de 50%, `lop=.025` representa 17 temas y `lop=.10` representa 16. La pérdida temática es mínima.

Con `lop=.10` sobreviven, entre otros:

- Economía y hacienda: 112 roll calls;
- Educación: 48;
- Seguridad: 29;
- Minería y energía: 13;
- Gobierno interior y descentralización: 12;
- Trabajo y seguridad social: 8;
- Medio ambiente: 8;
- Vivienda y territorio: 6;
- Economía, comercio y consumidores: 5;
- Agua y recursos hídricos: 4.

Por tanto, la D1 de umbral alto sigue siendo claramente **multidominio**. No se transforma en una dimensión producida exclusivamente por economía, seguridad o la Megareforma.

La categoría `Familia, infancia y adolescencia` pierde su único roll call elegible del corpus base. Este hecho es interpretativamente coherente: el caso seleccionado de ese dominio, 89113/15936-18, era una votación 106–5 cuya capacidad discriminante provenía principalmente de cinco votos negativos concentrados en el PNL y ya había sido clasificada como actor-específico.

---

## 6. Qué ocurre con los 30 proyectos no omnibus

La muestra transversal priorizada permite una prueba interpretativa especialmente transparente.

### Con `lop=.05`

Sobreviven **27 de los 30** casos.

Caen:

1. **89113 / 15936-18** — 106–5; restricción de armas vinculada a VIF; clasificado **C — actor específico**.
2. **88489 / 18137-05** — 109–3; kerosene; clasificado **C/D — minoría delgada y contenido exacto pendiente**.
3. **89315 / 14767-03** — 97–3; propiedad intelectual; clasificado **C — minoría específica con abstención alta**.

### Con `lop=.10`

Sobreviven **25 de los 30** casos. A los tres anteriores se agregan:

4. **88613 / 17170-07** — 110–8; agravante penal/rural; clasificado **B/D**, pero con rechazo concentrado en un pequeño subconjunto del FA.
5. **88450 / 15347-07** — 130–12; agravantes en drogas; clasificado **C/B — subgrupo específico dentro de gradiente penal**.

El patrón de poda es sustantivamente revelador: **ninguno de los cinco casos eliminados era una de las evidencias bipolares principales utilizadas para nombrar D1**.

En cambio sobreviven:

- plásticos de un solo uso, 75–71;
- teleoperadores/offshoring, 76–68;
- expulsión administrativa, 51–69;
- seguridad y salud laboral, 79–45;
- aguas no facturadas, 73–66;
- jornada de trabajadores audiovisuales, 91–43;
- elección mutua en admisión escolar, 111–28;
- creación de establecimientos, 103–33;
- legítima defensa privilegiada, 114–26;
- control legislativo en cuidados, 66–67;
- protección tarifaria eléctrica, 66–65;
- subvención de reingreso, 67–72;
- indicación sobre endeudamiento, 72–74;
- y otros gradientes de regulación, seguridad y educación.

Así, el umbral alto **elimina desproporcionadamente evidencia de localización individual y conserva los conflictos amplios y gradientes sustantivos**.

---

## 7. Qué ocurre dentro de la Megareforma 18216-05

El resultado es aún más limpio.

La auditoría del top 20 del omnibus había identificado exactamente cuatro casos Nivel IV —roll calls matemáticamente muy discriminantes pero interpretativamente dominados por minorías pequeñas:

- **88938** — transporte de monedas: 142–10;
- **88936** — licencias médicas de funcionarios: 127–6–19;
- **88935** — asignación de cupos de retiro: 138–14;
- **88937** — residual: 139–12–1.

Los cuatro tienen minorías binarias inferiores a 10% y, por tanto, **los cuatro desaparecen en `raw_lop100`**.

El patrón por umbral es informativo:

- `88936` ya cae con `lop=.05`;
- `88938`, `88935` y `88937` sobreviven al 5% pero caen al 10%.

En cambio sobreviven los conflictos sustantivos principales:

- **88948 — anatocismo:** 79–57; Nivel I;
- **88933 — capacitación/certificación laboral:** 58–94; Nivel I;
- **88900 — contratación y concesiones:** 77–77; Nivel I;
- **88962 — gradualidad de rebaja del impuesto corporativo:** 77–76; Nivel I;
- **88911 — incorporación de Sala Cuna Universal:** 82–48–24; Nivel I;
- **89485 — supresión posterior de Sala Cuna:** 75–70; Nivel II por serialidad;
- **88946 — reconexión de servicios básicos en catástrofe:** 80–69–4; Nivel II.

Por tanto, `lop=.10` produce exactamente la poda que la auditoría sustantiva había recomendado de manera independiente: reduce el peso de minorías delgadas sin eliminar las cadenas normativas que sostienen la interpretación multidominio.

---

## 8. Qué hipótesis sobreviven después de la sensibilidad

### H1 — D1 es un artefacto de minorías pequeñas

**Rechazada.**

Las coordenadas son casi idénticas con `lop=.10`, el orden partidario permanece estable y los conflictos sustantivos principales continúan presentes.

### H2 — D1 es simplemente Gobierno versus oposición

**Sigue rechazada como definición suficiente.**

El aumento de `lop` conserva casos en que PNL acompaña a las derechas sin integrar el Gobierno, casos en que DC/PPD acompañan al Gobierno en seguridad o educación y casos en que RN/UDI se separan de Republicanos/PNL. La estabilidad no depende de pequeñas disidencias.

### H3 — D1 es principalmente mercado versus Estado

**Sigue siendo una familia fuerte, no el nombre global.**

Con `lop=.10` sobreviven regulación ambiental, trabajo, inversión, tributación y protección contractual, pero también seguridad, migración, educación, garantías e institucionalidad.

### H4 — D1 es un continuo político-ideológico amplio fuertemente asociado a izquierda–derecha

**Se fortalece.**

Es la hipótesis que mejor explica simultáneamente:

- estabilidad casi perfecta de coordenadas;
- persistencia del orden agregado de partidos;
- supervivencia de conflictos en varios dominios;
- conservación de gradientes intra-bloque;
- desaparición selectiva de falsos amigos de minoría delgada sin cambio de geometría.

### H5 — la interpretación dependía del omnibus

**Sigue fuertemente debilitada.**

El omnibus conserva una participación cercana al 42% en las tres especificaciones, por lo que `lop` no soluciona esa dependencia. Sin embargo, las especificaciones balanceadas por `bill_cap` ya habían mostrado correlaciones de aproximadamente 0,994 con la base y la auditoría externa identifica las mismas familias fuera del 18216-05. La sensibilidad de `lop` agrega una prueba distinta y consistente.

---

## 9. Veredicto del gate

**Sensibilidad interpretativa `lop=.05` y `lop=.10`: SUPERADA.**

La interpretación de D1 no depende de roll calls marginalmente competitivos. Al contrario, el umbral de 10% elimina preferentemente las observaciones que la auditoría histórico-política ya había clasificado como minorías delgadas o localización individual, mientras conserva la geometría, el orden partidario y los conflictos sustantivos multidominio.

La formulación interna puede reforzarse a:

> **D1 resume un continuo político-ideológico amplio del comportamiento legislativo de la Cámara, fuertemente asociado a izquierda–derecha. La estructura es robusta a excluir votaciones con minorías inferiores a 5% y 10%; no depende de unos pocos roll calls extremos, de una sola materia ni de pequeñas minorías altamente discriminantes. Gobierno–oposición y regulación–mercado son mecanismos importantes dentro del eje, pero no lo agotan.**

Esta conclusión sigue siendo **interna**. Superar el gate de `lop` no autoriza todavía el rótulo público definitivo.

---

## 10. Qué queda abierto

El orden de trabajo recomendado después de este cierre es:

1. revisar si entre las votaciones que adquieren mayor peso relativo en `raw_lop100` aparece algún caso sustantivamente anómalo no cubierto por las auditorías previas;
2. cerrar los pocos residuos primarios exactos que sigan siendo relevantes en las especificaciones `.05/.10`;
3. contrastar la interpretación con literatura politológica, análisis especializados y evidencia pública sobre la estructura de competencia de la Cámara 2026;
4. realizar validación multimétodo con IRT 2PL y Optimal Classification;
5. completar el contrato de incertidumbre/robustez antes de autorizar publicación de coordenadas y nombre público.

D2 permanece exploratoria y sin nombre sustantivo.

---

## 11. Estado

**Gate de sensibilidad `lop=.05/.10`: CERRADO Y SUPERADO.**

**Hipótesis líder D1:** continuo político-ideológico amplio fuertemente asociado a izquierda–derecha.

**Siguiente operación inmediata:** inspección de casos que ganan prioridad relativa bajo `raw_lop100` y cierre de residuos relevantes, antes del contraste externo y multimétodo.
