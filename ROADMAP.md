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
- [x] Definir el marco pedagógico general de la ficha: pregunta pública, lectura, significado, límites, método y evidencia para cada gráfico.
- [x] Cerrar el diseño editorial y metodológico del **Módulo A: Participación y distribución de decisiones de voto** en `docs/MODULO_A_PARTICIPACION_VOTACIONES_V0_1.md`.
- [x] Adaptar el resumen de participación para usar **oportunidades efectivas durante la pertenencia a la Cámara** como denominador público y distinguir missing estructural de `No vota`.
- [x] Implementar y auditar el Módulo A, incluyendo barra de cinco estados y drill-down hasta la votación oficial.
- [x] Cerrar, implementar y desplegar el **Módulo B: Coincidencia con partido y bancada/comité**, con leave-one-out, umbral público de 10%, mínimo de 20 comparaciones y evidencia fragmentada por parlamentario. Contrato de cierre: `docs/MODULO_B_COINCIDENCIA_GRUPOS_V0_2.md`.
- [x] Cerrar, implementar y desplegar el **Módulo C: Iniciativa legislativa**, restringido a mociones originadas en la Cámara durante el período, distinguiendo autoría formal compartida e individual y conservando evidencia por boletín. Contrato de cierre: `docs/MODULO_C_INICIATIVA_LEGISLATIVA_V0_1.md`.
- [x] Cerrar, implementar y desplegar el **Módulo D: Red de coautoría**, con definición relacional explícita, síntesis de vínculos más repetidos, lista completa y evidencia por boletín. Contrato de cierre: `docs/MODULO_D_COAUTORIA_V0_1.md`.
- [x] Publicar una pestaña separada **Patrones de voto** como **laboratorio W-NOMINATE experimental**, sin convertir todavía la coordenada espacial en indicador cerrado de las fichas.
- [x] Añadir al laboratorio advertencia de estatus experimental, cobertura 154/155, concentración del omnibus, límites de agenda, contexto temático provisional, versionado visible y D2 como laboratorio exploratorio.
- [x] Incorporar a la ficha individual un bloque descriptivo de **Comisiones actuales**, enlazado por identificador institucional y sin convertir número de membresías en indicador de desempeño.
- [ ] Cerrar el módulo de materias antes de integrarlo a las fichas individuales.
- [ ] Cerrar los gates multimétodo/temporales antes de decidir si la posición espacial se incorpora como módulo individual definitivo.
- [ ] Auditar el diseño definitivo de la ficha una vez que se cierre el contenido de todos los módulos publicables.

## Educación ciudadana y actividad de comisiones

- [x] Construir la arquitectura interna **Entiende el Congreso** con explicación institucional progresiva, herramientas cívicas y glosario.
- [x] Implementar **Hoy en la Cámara** con snapshot diario de sesiones de Sala y bloqueo explícito ante datos desactualizados.
- [x] Implementar **Sigue un proyecto** y **¿Qué se votó realmente?**, conectando proyecto, tramitación, objeto exacto de votación y fuente nominal oficial.
- [x] Construir un directorio actual de comisiones desde la página institucional de la Cámara, después de descartar el endpoint Open Data que devolvía un universo implausible.
- [x] Validar `commissions-web-v0.4`: 34 instancias del directorio, 34 fichas con integrantes y extracción de membresía desde la tabla pertinente.
- [x] Separar las 27 comisiones legislativas permanentes de otras comisiones permanentes y subcomisiones para no atribuirles funciones idénticas.
- [x] Incorporar **Sesiones**, **Citaciones** y **Resultados** como capas distintas, evitando convertir agenda prevista en decisión adoptada.
- [x] Incorporar **Proyectos de ley asociados** por comisión y enlazar cada boletín con `proyecto.html?boletin=...`.
- [x] Incorporar **Oficios enviados** con número, sesión, destino y referencia, preservando enlaces oficiales de documento y respuesta cuando existen.
- [x] Documentar el contrato del módulo en `docs/MODULO_COMISIONES_V0_1.md` y mantener un gate mínimo de 80% de cobertura por capa antes de aceptar un snapshot.
- [ ] Evaluar **Actas** como fuente documental y no como simple contador.
- [ ] Diseñar un contrato específico para **Audiencias Públicas**, invitados y comparecencias.
- [ ] Reconstruir **asistencia a sesiones de comisión** con membresía al momento, reemplazos y denominadores temporales correctos.
- [ ] Identificar **presidencias y otros roles de comisión** con historia temporal fiable.
- [ ] Evaluar **Informes de comisión** y su unión con `project_events.csv` evitando duplicar eventos.
- [ ] Incorporar comisiones investigadoras, unidas, mixtas u otras familias solo mediante capas metodológicas separadas.
- [ ] Auditar escritorio/móvil y decidir cuándo promover las páginas de comisión desde vista interna a navegación pública principal.

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
- [x] Mantener la clasificación temática fuera de los datos primarios y permitir reclasificación sin repetir la recolección legislativa.
- [x] En la página W-NOMINATE rotular el filtro como **contexto temático del proyecto**, no como materia oficial ni tema exacto de cada objeto votado.
- [ ] Realizar una validación externa/formal de precisión por macroárea antes de presentar la clasificación como métrica validada de investigación.
- [ ] Refinar, para usos analíticos por roll call, la clasificación de artículos/indicaciones/objetos exactos y `policy_chains`, especialmente dentro de proyectos omnibus.

## Historia política y análisis derivados

- [x] Construir historia temporal de partido por diputado desde el 11 de marzo de 2026.
- [x] Reconstruir y congelar la bancada/comité al inicio del período para los 155 integrantes.
- [x] Mantener snapshots semanales de partido y bancada y registrar cambios con fecha exacta o ventana de observación según la evidencia disponible.
- [x] Enriquecer los votos nominales con `party_at_vote` y `caucus_at_vote`, conservando confianza, procedencia y banderas de incertidumbre.
- [x] Auditar una unión temporal 1:1 para las 56.420 observaciones nominales y 364 roll calls, sin afiliaciones provisionales.
- [x] Generar primitivas por grupo y votación: participación, Rice, posición modal, abstenciones y elegibilidad metodológica.
- [x] Generar resúmenes individuales de participación y coincidencia modal con partido/bancada, con análisis de sensibilidad según competitividad de la votación.
- [x] Decidir el umbral de competitividad para el indicador público de coincidencia: **minoría binaria de Cámara ≥10%**, conservando 5% y 20% como sensibilidades internas.
- [x] Definir cuándo corresponde hablar de **cohesión**, **coincidencia modal** o **disciplina**: el indicador público se denomina coincidencia descriptiva y no etiqueta automáticamente divergencias como rebelión o indisciplina.
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
- [x] Documentar resultados experimentales en `docs/RESULTADOS_WNOMINATE_V0_1.md`.
- [x] Publicar esos resultados en una **pestaña experimental separada** con advertencias visibles, sin integrarlos todavía como indicador cerrado de la ficha individual.
- [x] Ejecutar una primera prueba exploratoria de mitades temporales; conservarla como evidencia descriptiva porque usa `trials = 1` y las agendas no están balanceadas.
- [x] Auditar literatura y experiencia previa y fijar el contrato prospectivo multimétodo en `docs/CONTRATO_MODELOS_ROLLCALL_V0_2.md`.
- [x] Reestimar W-NOMINATE 1D con incertidumbre válida y cerrar la corrida de investigación correspondiente.
- [ ] Estimar IRT bayesiano 2PL 1D como modelo inferencial principal y comprobar convergencia de cadenas.
- [ ] Estimar Optimal Classification como robustez no paramétrica.
- [x] Implementar B-Call como diagnóstico separado de posición y variabilidad, sin denominar D2 disciplina partidaria.
- [x] Auditar efecto arco de D2 mediante la relación cuadrática entre D1 y D2 y estudiar los residuos; no hay evidencia fuerte de que D2 sea meramente un artefacto cuadrático, pero permanece exploratorio y sin etiqueta sustantiva pública.
- [ ] Separar fiabilidad por partición, ventanas cronológicas balanceadas y un modelo dinámico conjunto para cerrar la **estabilidad temporal** de D1.
- [ ] Cerrar formalmente la validación sustantiva de D1 y decidir el lenguaje público definitivo: izquierda–derecha, continuo político-ideológico o formulación más prudente.
- [ ] Decidir la forma pública eventual de la posición espacial dentro de las fichas: coordenada, percentil, banda robusta, visualización sin ranking o ninguna.
- [x] Derivar redes de coautoría a partir de `bill_authors.csv` sin alterar la tabla primaria y actualizarlas semanalmente después del sync legislativo.
- [ ] Decidir qué indicadores adicionales finalmente se publicarán en las fichas legislativas del sitio.