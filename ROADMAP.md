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

## Clasificación temática de proyectos

- [x] Auditar una muestra estratificada de mensajes y mociones para comprobar disponibilidad de texto fuente.
- [x] Confirmar recuperación de iniciativas en **PDF y DOCX** desde enlaces oficiales de la Cámara.
- [x] Crear una taxonomía temática v0.1 versionada y explícitamente separada de las categorías oficiales.
- [x] Detectar el boilerplate administrativo de algunas mociones para evitar contaminar la clasificación.
- [ ] Construir el corpus textual incremental de todos los proyectos del período.
- [ ] Auditar cobertura y calidad del corpus completo por origen y formato.
- [ ] Crear una muestra de referencia humana (gold standard) estratificada.
- [ ] Revisar fronteras y solapamientos de la taxonomía v0.1 con el gold standard.
- [ ] Definir método de clasificación: reglas, modelo, enfoque híbrido y umbrales de confianza.
- [ ] Evaluar precisión por macroárea antes de clasificar masivamente.
- [ ] Generar `project_topics.csv` en formato largo con tema principal/secundarios, método, confianza y versión de taxonomía.
- [ ] Mantener la clasificación temática fuera de los datos primarios y permitir reclasificación sin repetir la recolección legislativa.

## Historia política y análisis derivados

- [ ] Construir historia temporal de partido y bancada por diputado (`fecha_desde` / `fecha_hasta`).
- [ ] Definir indicadores de disciplina, cohesión, participación y apoyo al Ejecutivo.
- [ ] Definir contrato metodológico para matrices roll-call y W-NOMINATE.
- [ ] Derivar redes de coautoría a partir de `bill_authors.csv` sin alterar la tabla primaria.
- [ ] Decidir qué indicadores finalmente se publicarán en las fichas legislativas del sitio.
