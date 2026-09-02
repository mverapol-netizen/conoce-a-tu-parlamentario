# Contrato de datos legislativos · piloto 2026

Este documento fija la separación entre datos primarios, variables derivadas y análisis futuros para la capa legislativa de **Conoce a tu parlamentario**.

## Período

- Inicio del comportamiento parlamentario observado: **11 de marzo de 2026**.
- Producción legislativa del período: proyectos ingresados desde esa fecha.
- Comportamiento de votación del período: cualquier votación de Sala celebrada desde esa fecha, aunque el proyecto haya ingresado antes.

## Principios

1. **No inferir Sala por texto.** Una votación se considera de Sala únicamente si su ID está contenido en una `Sesion` retornada por `WSSala.retornarSesionesXAnno`.
2. **No borrar la fuente original.** Materias, tipos, trámites, opciones de voto y demás categorías oficiales se conservan tal como las entrega la Cámara.
3. **Separar origen e institución de origen.** `origen_iniciativa` distingue Ejecutivo/parlamentario; `camara_origen` distingue Cámara/Senado.
4. **Formato largo.** Autorías y votos individuales se almacenan una fila por relación, facilitando redes y matrices roll-call.
5. **No calcular ideología en la recolección.** Disciplina, cohesión, apoyo al Gobierno, W-NOMINATE y redes son capas analíticas posteriores.

## Tablas piloto

### `projects.csv`

Una fila por proyecto.

Clave esperada: `boletin`.

Campos principales: ID oficial, boletín, título, fecha de ingreso, origen de iniciativa, tipo de iniciativa, Cámara de origen y admisibilidad.

### `project_subjects.csv`

Una fila por proyecto × materia oficial.

Clave compuesta: `boletin + materia_id`.

Las macroáreas propias —seguridad, economía, medio ambiente, etc.— se agregarán en otra tabla de clasificación sin sustituir la materia original.

### `project_ministries.csv`

Una fila por proyecto × ministerio patrocinante.

Especialmente relevante para mensajes del Ejecutivo.

### `bill_authors.csv`

Una fila por proyecto × autor.

Conserva orden de autoría, ID, nombre y cámara del autor. Esta tabla será la fuente primaria de futuras redes de coautoría.

### `rollcalls.csv`

Una fila por votación de proyecto **verificada como votación de Sala**.

Incluye ID, boletín, fecha, sesión, descripción, artículo, totales, tipo, resultado, quórum, trámite constitucional y trámite reglamentario.

### `member_votes.csv`

Una fila por votación × diputado.

Clave compuesta prevista: `vote_id + diputado_id`.

Esta es la matriz fuente para disciplina partidaria, similitud de voto y estimaciones espaciales como W-NOMINATE.

### `project_events.csv`

Tabla de eventos legislativos.

En el piloto solo registra eventos verificables de votación de Sala y sus trámites asociados. **No debe interpretarse todavía como reconstrucción completa del curso legislativo.**

## Hallazgo que debe probar el piloto

El tipo oficial `ProyectoLey` expone proyecto, iniciativa, Cámara de origen, autores, ministerios, materias y votaciones. Las votaciones contienen trámite constitucional y reglamentario. La reconstrucción completa de pasos por comisión probablemente requerirá una fuente adicional o una combinación con páginas de tramitación. Esto se resolverá después del piloto y antes del backfill completo.

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

El piloto utiliza **10 proyectos** y busca mantener una composición equilibrada de cinco mociones parlamentarias y cinco mensajes del Ejecutivo, privilegiando dentro de cada grupo aquellos que ya tengan votaciones verificadas de Sala.
