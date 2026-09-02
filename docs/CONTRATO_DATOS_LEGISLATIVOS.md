# Contrato de datos legislativos · Cámara 2026–2030

Este documento fija el contrato de datos primarios para la capa legislativa de **Conoce a tu parlamentario**. Se cerró después de un piloto real ejecutado el 2 de septiembre de 2026 sobre fuentes oficiales de la Cámara de Diputadas y Diputados.

## Período

- Inicio del comportamiento parlamentario observado: **11 de marzo de 2026**.
- Producción legislativa del período: proyectos ingresados desde esa fecha.
- Comportamiento de votación del período: cualquier votación de Sala celebrada desde esa fecha, aunque el proyecto haya ingresado antes.
- La base debe conservar la fecha original de ingreso del proyecto para poder distinguir ambos universos.

## Principios

1. **No inferir Sala por texto o por una sola fuente.** Una votación entra en la base de roll calls cuando: (a) su ID aparece en `WSLegislativo.retornarVotacionesXAnno`; (b) el mismo ID aparece asociado al boletín en `retornarVotacionesXProyectoLey`; y (c) el ID resuelve a la página institucional `Sala de Sesiones > Detalle de Votación`, donde coinciden boletín y fecha.
2. **Los votos nominales se obtienen desde el detalle oficial.** Para cada roll call validado se consulta `WSLegislativo.retornarVotacionDetalle(prmVotacionId)`, que entrega `Votos/Voto`, `Diputado` y `OpcionVoto`.
3. **No borrar la fuente original.** Tipos, trámites, opciones de voto, resultados, materias y demás categorías oficiales se conservan tal como las entrega la Cámara.
4. **Separar origen e institución de origen.** `origen_iniciativa` distingue Ejecutivo/parlamentario; `camara_origen` distingue Cámara/Senado.
5. **Formato largo.** Autorías y votos individuales se almacenan una fila por relación, facilitando redes, matrices roll-call y análisis reproducibles.
6. **No calcular ideología en la recolección.** Disciplina, cohesión, apoyo al Gobierno, W-NOMINATE, redes y clasificaciones temáticas son capas analíticas posteriores.
7. **La ausencia de un campo oficial se registra como ausencia.** No se imputan materias, comisiones ni estados que la fuente no haya entregado.
8. **La recolección y el análisis permanecen separados.** Los datos primarios pueden regenerarse sin depender de categorías políticas o modelos posteriores.

## Hallazgos de compatibilidad de las fuentes

### Votaciones de Sala

Los endpoints `WSSala.retornarSesionesXAnno` y `retornarSesionesXLegislatura` devuelven en 2026 el resumen de las sesiones, pero **no serializan la colección `Votaciones` que figura en el esquema publicado**. Por ello no se usa esa colección ausente como criterio de integridad.

La validación de Sala se realiza mediante el cruce triple descrito arriba. El número e ID de sesión se recuperan, cuando es posible, combinando la página pública de detalle de votación con el índice anual de sesiones.

### Votos individuales

`retornarVotacionesXAnno` funciona como índice de roll calls, pero en la respuesta observada de 2026 no incorpora los votos nominales. Los votos individuales sí aparecen en `retornarVotacionDetalle`.

En el piloto, **6 roll calls produjeron 930 filas nominales: exactamente 155 registros por votación**. La fuente distingue opciones como `Afirmativo`, `Negativo`, `Abstención`, `Dispensado` y `No Vota`. Por tanto, `No Vota` no debe confundirse con abstención.

### Materias

La Cámara expone un catálogo oficial de materias —8.494 entradas observadas en el piloto—, pero la asociación concreta `ProyectoLey/Materias` vino vacía para los diez proyectos seleccionados. Las páginas públicas también pueden mostrar `Materia: -`.

Consecuencia: `project_subjects.csv` conserva el esquema oficial, incluso si queda vacío. Las macroáreas propias —seguridad, economía, medio ambiente, etc.— se construirán posteriormente en una **tabla derivada separada**, sin sustituir la fuente original.

### Tramitación y comisiones

La página pública de cada boletín expone un historial cronológico con fecha, sesión, etapa, subetapa y documentos. Allí aparecen hitos como ingreso, cuenta, paso a comisión, informes, paso a Hacienda, indicaciones, urgencias, oficios y otros eventos.

La reconstrucción completa del curso legislativo se hará en una capa específica por boletín. `project_events.csv` del piloto contiene por ahora solo eventos de votación de Sala y **no debe interpretarse como la tramitación completa**.

## Tablas primarias

### `projects.csv`

Una fila por proyecto.

Clave: `boletin`.

Campos principales: ID oficial, boletín, título, fecha de ingreso, origen de iniciativa, tipo de iniciativa, Cámara de origen y admisibilidad.

### `project_subjects.csv`

Una fila por proyecto × materia oficial, cuando la fuente entregue esa asociación.

Clave prevista: `boletin + materia_id`.

### `project_ministries.csv`

Una fila por proyecto × ministerio patrocinante.

Especialmente relevante para mensajes del Ejecutivo.

### `bill_authors.csv`

Una fila por proyecto × autor.

Conserva orden de autoría, ID, nombre y cámara del autor. Esta tabla será la fuente primaria de futuras redes de coautoría.

### `rollcalls.csv`

Una fila por votación de proyecto verificada como **votación de Sala**.

Incluye ID, boletín, fecha, sesión, descripción, artículo, totales, tipo, resultado, quórum, trámite constitucional, trámite reglamentario y URL institucional de verificación.

### `member_votes.csv`

Una fila por votación × diputado.

Clave prevista: `vote_id + diputado_id`.

Conserva también `No Vota` y `Dispensado`; esas categorías solo se transformarán en la etapa analítica y nunca en la extracción.

Esta tabla es la fuente para disciplina partidaria, similitud de voto y futuras estimaciones espaciales como W-NOMINATE.

### `project_events.csv`

Una fila por evento legislativo normalizado.

En el piloto contiene exclusivamente votaciones de Sala. La versión de producción incorporará la cronología del boletín y las comisiones.

## Resultado del piloto cerrado

Ejecución exitosa del 2 de septiembre de 2026:

- Universo desde el inicio del período: **449 mociones**, **44 mensajes del Ejecutivo** y **599 votaciones**.
- Proyectos piloto: **10** (5 mociones + 5 mensajes).
- Roll calls de Sala verificados: **6**.
- Votos individuales recuperados: **930**.
- Ministerios patrocinantes recuperados: **5**.
- Autorías parlamentarias recuperadas: **5** en los cinco proyectos parlamentarios del piloto.
- Materias oficiales asociadas: **0**, tratado como ausencia de la fuente y no como error del extractor.

El workflow terminó con éxito y comprometió automáticamente sus salidas al repositorio.

## Salidas del piloto

El workflow genera en `data/legislative/pilot/`:

- `projects.csv`
- `project_subjects.csv`
- `project_ministries.csv`
- `bill_authors.csv`
- `rollcalls.csv`
- `member_votes.csv`
- `project_events.csv`
- `diagnostics.json`
- `REPORT.md`

## Criterio para pasar a producción

El piloto se considera aprobado porque demostró de punta a punta que podemos enlazar:

**proyecto → origen/autoría → roll call de Sala → voto nominal de cada diputado**.

La siguiente fase debe transformar esta prueba en tres recolectores incrementales de producción —proyectos/tramitación, votaciones de Sala y autorías— con actualización semanal y sin volver a descargar innecesariamente toda la historia.