# Pendientes y revisión global

## Fotografías de parlamentarios

- [ ] Revisar **todos los perfiles y tarjetas** para asegurar que ninguna fotografía quede tapada por las iniciales de respaldo.
- [ ] El fallback con iniciales debe mostrarse **solo si la imagen no existe o falla al cargar**, nunca superpuesto sobre una foto válida.
- [ ] Auditar encuadre y `object-position` para que el rostro quede visible tanto en tarjetas como en la ficha del representante seleccionado, en escritorio y celular.

## Hemiciclo

- [ ] Revisar la primera versión completa del Hemiciclo después de probarla en escritorio y celular: legibilidad, colores, orden, tamaño de escaños, leyendas y experiencia de selección.
- [ ] Mantener la distinción explícita entre militancia partidaria y pertenencia a bancada/comité parlamentario.
- [ ] Para independientes, mostrar la fórmula: **“Independiente en [bancada/comité]”**.
- [ ] Revisar mensualmente la clasificación editorial de fuerzas como oficialismo, oposición o no alineadas.
- [ ] Dejar claro que el gráfico representa **distribución de fuerzas**, no ubicación física exacta de cada escaño en la Sala.

## Fichas legislativas

- [x] Habilitar una página interna y una URL estable para cada integrante de la Cámara.
- [x] Conectar la selección por distrito y el Hemiciclo con esa ficha interna.
- [ ] Definir posteriormente qué dimensiones, indicadores y documentos deberá contener la ficha legislativa.
- [ ] Auditar el diseño definitivo de la ficha una vez que se defina su contenido.

## Base legislativa 2026–2030

- [x] Diseñar el contrato de datos primarios.
- [x] Ejecutar un piloto real con 10 proyectos (5 mociones y 5 mensajes).
- [x] Validar el enlace **proyecto → votación de Sala → voto nominal de cada diputado**.
- [x] Confirmar `retornarVotacionDetalle` como fuente de votos individuales.
- [x] Registrar que `WSSala` no serializa en 2026 la colección de votaciones declarada en su esquema.
- [x] Tratar la ausencia de materias oficiales asociadas como missingness de la fuente, no como error del extractor.
- [x] Convertir el piloto en un recolector incremental de proyectos y tramitación.
- [x] Crear el recolector incremental de votaciones exclusivamente de Sala.
- [x] Crear el recolector incremental de autorías/coautorías de mociones.
- [x] Reconstruir el historial completo por boletín: ingreso, cuenta, comisiones, informes, Hacienda, indicaciones, urgencias, oficios y demás eventos.
- [x] Realizar el backfill inicial desde el **11 de marzo de 2026**.
- [x] Configurar actualización automática semanal los **viernes**.
- [x] Generar controles de integridad y un reporte de auditoría por ejecución.
- [x] Conciliar todas las capas de una corrida con un mismo snapshot de proyectos.
- [x] Mantener separadas las capas de datos primarios, clasificación temática, indicadores derivados y modelos como W-NOMINATE/redes.
- [x] Revalidar semanalmente una **ventana móvil de 35 días** de autorías y votaciones para absorber correcciones retroactivas de la fuente oficial sin repetir el backfill completo.
- [x] Escalonar la revisión de historiales de proyectos: actividad reciente cada semana y proyectos antiguos no terminales en cuatro grupos rotativos, con concurrencia reducida y backoff ante saturación del portal.

## Clasificación temática de proyectos

- [x] Auditar una muestra estratificada de mensajes y mociones para comprobar disponibilidad de texto fuente.
- [x] Confirmar recuperación de iniciativas en **PDF y DOCX** desde enlaces oficiales de la Cámara.
- [x] Crear una taxonomía temática v0.1 versionada y explícitamente separada de las categorías oficiales.
- [x] Detectar el boilerplate administrativo de algunas mociones para evitar contaminar la clasificación.
- [x] Construir el corpus textual incremental de todos los proyectos del período.
- [x] Auditar cobertura y calidad del corpus completo por origen y formato.
- [x] Crear una muestra de referencia humana estratificada.
- [x] Revisar fronteras y solapamientos de la taxonomía con casos ambiguos.
- [x] Definir un método híbrido: señal institucional de comisión/destinación + trayectoria + texto + revisión semántica.
- [x] Completar la primera clasificación temática de todos los proyectos disponibles, con trazabilidad de revisiones y cero casos pendientes.
- [ ] Realizar una validación externa/formal de precisión por macroárea antes de presentar la clasificación como métrica validada de investigación.
- [ ] Mantener la clasificación temática fuera de los datos primarios y permitir reclasificación sin repetir la recolección legislativa.

## Historia política y análisis derivados

- [x] Construir historia temporal de partido por diputado desde el 11 de marzo de 2026.
- [x] Reconstruir y congelar la bancada/comité al inicio del período para los 155 integrantes.
- [x] Mantener snapshots semanales de partido y bancada y registrar cambios con fecha exacta o ventana de observación según la evidencia disponible.
- [x] Enriquecer los votos nominales con `party_at_vote` y `caucus_at_vote`, conservando confianza, procedencia y banderas de incertidumbre.
- [x] Auditar una unión temporal 1:1 para las 56.420 observaciones nominales y 364 roll calls, sin afiliaciones provisionales.
- [x] Generar primitivas por grupo y votación: participación, Rice, posición modal, abstenciones y elegibilidad metodológica.
- [x] Generar resúmenes individuales de participación y coincidencia modal con partido/bancada, con análisis de sensibilidad según competitividad de la votación.
- [ ] Decidir qué umbral o conjunto de umbrales de competitividad usar para los indicadores públicos, evitando confundir votaciones casi unánimes con disciplina.
- [ ] Definir cuándo corresponde hablar de **cohesión**, **coincidencia modal** o **disciplina**; no etiquetar automáticamente toda divergencia como rebelión.
- [ ] Diseñar un indicador de apoyo al Ejecutivo que incorpore posición gubernamental en cada votación y no asuma que votar “Sí” a todo proyecto de origen Ejecutivo equivale a apoyar al Gobierno.
- [x] Definir y documentar el contrato metodológico para la matriz roll-call y W-NOMINATE.
- [x] Construir la matriz neutral 155 × 364 preservando abstención, no voto y dispensado como missing para estimación espacial.
- [x] Auditar elegibilidad bajo distintos umbrales de minoría y participación sin fijar prematuramente un único filtro público.
- [x] Auditar concentración por boletín y redundancia exacta de patrones de voto.
- [x] Estimar W-NOMINATE 1D bajo seis especificaciones de sensibilidad (`lop`, deduplicación y límites por boletín).
- [x] Comprobar alta estabilidad global de la dimensión 1 frente a cambios de umbral y balanceo por proyecto.
- [x] Auditar estabilidad individual, exclusiones y asociación descriptiva de D1 con partido, bancada y bloques históricos.
- [x] Estimar un diagnóstico W-NOMINATE 2D y comparar su ganancia de ajuste frente a 1D.
- [x] Alinear espacios 2D mediante Procrustes y comprobar que D2 es estable al cambiar `lop`, pero bastante más sensible al balanceo por boletín.
- [x] Adoptar provisionalmente **1D como modelo espacial principal parsimonioso** y mantener D2 únicamente como diagnóstico exploratorio secundario.
- [x] Documentar resultados experimentales en `docs/RESULTADOS_WNOMINATE_V0_1.md` y mantenerlos fuera de la ficha pública.
- [ ] Auditar **estabilidad temporal** de D1 en subperíodos comparables antes de cualquier uso público.
- [ ] Validar sustantivamente la orientación e interpretación de D1; no denominar automáticamente el signo izquierda/derecha, gobierno/oposición o ideología.
- [ ] Decidir la forma pública eventual de la posición espacial: coordenada, percentil, banda robusta, visualización sin ranking o ninguna.
- [x] Derivar redes de coautoría a partir de `bill_authors.csv` sin alterar la tabla primaria y actualizarlas semanalmente después del sync legislativo.
- [ ] Decidir qué indicadores finalmente se publicarán en las fichas legislativas del sitio.
