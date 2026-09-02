# Contrato de matriz roll-call · Cámara 2026–2030

Este documento fija la transformación **neutral y reproducible** entre los votos nominales de Sala y futuros modelos espaciales como W-NOMINATE. No estima posiciones ideológicas y no decide todavía qué votaciones deben entrar al modelo final.

## Fuente

La matriz se deriva de `data/legislative/2026/member_votes_enriched.csv`, que conserva una fila por `vote_id × diputado_id`, y de `rollcalls.csv` para los metadatos de cada votación.

La transformación nunca modifica los archivos primarios.

## Unidad y universo

- Filas de la matriz: diputados/as.
- Columnas: roll calls de Sala verificados desde el 11 de marzo de 2026.
- Cada celda representa la opción emitida por un diputado en una votación determinada.
- El universo puede incorporar votaciones sobre proyectos ingresados antes del inicio del período, siempre que la votación de Sala haya ocurrido durante el período 2026–2030.

## Codificación neutral

Para una futura estimación espacial binaria:

- `Afirmativo` → `1`.
- `En Contra` / `Negativo` → `0`.
- `Abstención` → missing.
- `No Vota` → missing.
- `Dispensado` → missing.

El missing no significa oposición, abstención ni ausencia por sí mismo: esas categorías continúan disponibles por separado en los datos fuente y en los metadatos de la matriz.

Esta regla evita forzar opciones no binarias dentro de una dimensión Sí/No.

## No se fija todavía un umbral de competitividad

Las votaciones prácticamente unánimes contienen muy poca información para ubicar legisladores en un espacio político. Sin embargo, excluirlas durante la recolección sería irreversible y metodológicamente prematuro.

Por ello `build_rollcall_matrix.py` conserva todas las votaciones y calcula, para cada una:

- votos afirmativos;
- votos en contra;
- abstenciones;
- `No Vota`;
- dispensados;
- número de votos binarios;
- número de observaciones missing para el modelo;
- tamaño de la minoría binaria;
- proporción de la minoría entre votos binarios;
- participación binaria sobre los 155 integrantes;
- indicador de unanimidad binaria.

Los diagnósticos reportan cuántos roll calls sobrevivirían a diferentes umbrales de proporción minoritaria —0%, 2,5%, 5% y 10%— sin seleccionar ninguno como regla oficial.

## Salidas

### `rollcall_matrix_binary.csv`

Matriz ancha `diputado × votación`.

Las únicas celdas no vacías son `1` y `0`. Está diseñada como artefacto intermedio reproducible, no como formato específico de un paquete estadístico.

### `rollcall_matrix_metadata.csv`

Una fila por roll call con sus conteos y métricas de información/competitividad. Esta tabla permitirá definir y auditar posteriormente la muestra usada por W-NOMINATE.

### `rollcall_member_metadata.csv`

Una fila por diputado con número de votos binarios, afirmativos, negativos, missing y tasa de participación binaria.

### `rollcall_matrix_diagnostics.json`

Control de integridad de la transformación y análisis de sensibilidad preliminar.

## Decisiones que quedan pendientes antes de estimar W-NOMINATE

1. Umbral de competitividad o conjunto de especificaciones de sensibilidad.
2. Requisito mínimo de participación por legislador.
3. Número de dimensiones a estimar y criterio para comparar una y dos dimensiones.
4. Regla de identificación/orientación de los ejes para evitar que el signo de una dimensión se interprete arbitrariamente como izquierda/derecha.
5. Tratamiento de cambios de partido o bancada: los puntos ideales pertenecen al legislador, mientras las afiliaciones son atributos temporales para interpretar los resultados, no códigos dentro de la matriz de votos.
6. Evaluación de votaciones procedimentales frente a votaciones sustantivas.
7. Pruebas de robustez por período temporal y por subconjuntos temáticos cuando exista suficiente información.

## Principio metodológico

**Preparar no es estimar.** La matriz debe poder reconstruirse automáticamente cada vez que cambien los votos nominales, mientras que la especificación de W-NOMINATE se mantiene como una decisión analítica versionada y auditable.
