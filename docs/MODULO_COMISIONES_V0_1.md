# Módulo de comisiones v0.1

**Estado:** implementación funcional en validación interna.  
**Corte inicial:** 3 de septiembre de 2026.  
**Ámbito:** Cámara de Diputadas y Diputados de Chile, período 2026–2030.

## 1. Pregunta pública

El módulo busca responder preguntas distintas de las que cubren las votaciones de Sala:

- ¿En qué comisiones participa actualmente una diputada o diputado?
- ¿Qué comisión estudia un determinado conjunto de asuntos?
- ¿Qué proyectos aparecen asociados institucionalmente a una comisión?
- ¿Cuándo se reunió o fue registrada una sesión de comisión?
- ¿Qué asuntos fueron citados para una sesión?
- ¿Qué resultados o acuerdos registró posteriormente la Cámara?
- ¿Qué oficios envió la comisión y a qué destinatarios?

La finalidad es reducir el sesgo de observabilidad hacia las votaciones nominales de Sala. El trabajo parlamentario también ocurre en instancias de comisión, mediante estudio de proyectos, audiencias, acuerdos, solicitudes de información, oficios y otras actuaciones.

## 2. Fuente institucional elegida

La primera implementación probó los servicios Open Data `WSComision.retornarComisionesVigentes` y `WSComision.retornarComisionesXPeriodo`, resolviendo previamente el período legislativo actual mediante `WSLegislativo.retornarPeriodoLegislativoActual`.

En septiembre de 2026 ambos caminos devolvieron un universo implausible de solo dos comisiones. El workflow incorporó un gate duro y abortó antes de publicar ese resultado.

Por ello, el directorio operativo se construye desde la página institucional server-rendered de **Comisiones Permanentes** de la Cámara y sus fichas por `prmID`. La fuente sigue siendo oficial; cambia el mecanismo de acceso.

El extractor conserva la distinción institucional entre:

1. las 27 comisiones legislativas temáticas numeradas; y
2. otras comisiones permanentes y subcomisiones que aparecen en el mismo directorio institucional.

No se mezclan automáticamente comisiones investigadoras, unidas, mixtas u otras familias de instancia.

## 3. Directorio y membresía

Archivo: `data/legislative/2026/commissions/commissions_snapshot.json`.

Contrato vigente: `commissions-web-v0.4`.

La corrida inicial validada recuperó:

- 34 instancias del directorio;
- 34 páginas con integrantes recuperados;
- 389 filas de membresía.

La membresía se extrae preferentemente desde la tabla de integrantes de cada ficha y no desde todos los enlaces a diputados presentes en la página. Esta decisión se adoptó después de detectar contaminación por enlaces de navegación o encabezado.

### Interpretación permitida

Una persona listada como integrante puede describirse como **integrante actual de esa comisión según el directorio institucional recuperado**.

### Interpretaciones no permitidas

La membresía no demuestra por sí sola:

- especialización técnica;
- asistencia efectiva a todas las sesiones;
- influencia en la agenda;
- liderazgo;
- productividad;
- posición sustantiva sobre los temas de la comisión.

## 4. Capas de actividad

Archivo: `data/legislative/2026/commissions/commission_activity_snapshot.json`.

Las capas se mantienen separadas porque responden preguntas diferentes.

### A. Sesiones

Describe filas del calendario/historial devuelto por la ficha institucional: número, día, inicio, término y estado cuando están disponibles.

No se utiliza el número de sesiones como ranking de productividad. Una comisión puede tener diferente carga, mandato, complejidad o calendario.

### B. Citaciones

Describe los asuntos que aparecen convocados para una sesión en la página de Citaciones.

Una citación representa **agenda prevista**. No permite afirmar que el asunto fue efectivamente discutido, votado, aprobado o rechazado.

### C. Resultados

Describe la información posterior que la Cámara registra en la página de Resultados: materias tratadas, acuerdos, avance de proyectos, invitados, asistencia, reemplazos u otras constancias según la fila institucional.

El texto institucional se conserva y se presenta separado de la citación.

### D. Proyectos de ley

Reproduce las iniciativas que la tabla de “Proyectos de Ley” de la comisión muestra para el período seleccionado por defecto, con ingreso, materia, estado y boletín.

Aparecer en esta tabla significa **asociación institucional con la comisión en esa vista oficial**. No significa necesariamente:

- aprobación de la iniciativa;
- que la comisión sea la única instancia competente;
- que el proyecto permanezca actualmente radicado allí;
- que la tabla reconstruya toda su historia legislativa.

Cada boletín se enlaza con `proyecto.html?boletin=...`, que reconstruye la tramitación desde la base legislativa principal del proyecto.

### E. Oficios enviados

Capa en validación al momento de abrir este contrato. La página institucional expone, cuando existen filas, número, sesión, destino, referencia, documento y respuestas.

Un oficio debe interpretarse como **una comunicación institucional emitida por la comisión**. No demuestra por sí solo fiscalización efectiva, influencia, cumplimiento del destinatario, suficiencia de la respuesta o éxito político.

## 5. Unidad de análisis y tablas anidadas

Las páginas de Citaciones y Resultados pueden contener subtablas dentro de una fila principal para detallar varios asuntos de una misma sesión.

La primera prueba del extractor convirtió accidentalmente esas subtablas en filas independientes. Esa salida fue descartada antes de publicación.

Desde `commission-activity-web-v0.2`, la regla es:

> una fila retenida corresponde a una fila principal de la tabla institucional; una subtabla anidada nunca se convierte automáticamente en un evento independiente.

Cuando una fila principal contiene varios asuntos, el texto puede permanecer concatenado. Separar esos asuntos requerirá una segunda etapa de normalización documental con trazabilidad al bloque de origen.

## 6. Gates de calidad

### Directorio

El workflow falla antes de persistir si el directorio devuelve menos de 20 comisiones con identificador `prmID` y nombre recuperable.

### Actividad

Cada capa nueva debe alcanzar al menos 80% de cobertura de páginas recuperadas sobre el universo del directorio antes de que el snapshot se considere válido.

La cobertura de página no sustituye la auditoría de contenido: antes de activar una nueva capa en la interfaz se revisan manualmente filas concretas para detectar tablas anidadas, encabezados ambiguos o contaminación de navegación.

Una lista de filas vacía significa **“la vista recuperada no devolvió filas”**. Nunca se transforma automáticamente en “la comisión no tuvo actividad”.

## 7. Actualización

El workflow `.github/workflows/sync_commissions.yml` se ejecuta semanalmente y puede activarse manualmente.

El flujo previsto es:

1. reconstruir y validar el directorio actual;
2. reconstruir las capas de actividad desde las fichas institucionales;
3. abortar ante cobertura implausible;
4. persistir snapshots solo después de superar gates;
5. permitir que las páginas consuman únicamente versiones de schema explícitamente aceptadas.

## 8. Uso en la ficha parlamentaria

La ficha individual incorpora un bloque **Comisiones actuales** alimentado por el mismo snapshot del directorio.

La conexión se hace por identificador institucional de diputado. Cada membresía enlaza a `comision.html?id=<prmID>`.

Este bloque es descriptivo y no se agrega a Participación, Coincidencia, Iniciativa o Coautoría en un índice compuesto.

## 9. Pendientes

Antes de considerar cerrado el módulo de actividad en comisión quedan, al menos:

- validar y activar Oficios enviados;
- estudiar recuperación de enlaces directos a documentos y respuestas;
- evaluar Actas como fuente documental y no como simple contador;
- evaluar Audiencias Públicas e invitados con un contrato específico;
- reconstruir asistencia a sesiones con denominadores temporales correctos, membresía al momento y reemplazos;
- identificar presidencias y otros roles con temporalidad fiable;
- decidir si Informes puede conectarse de manera estable con `project_events.csv` sin duplicar eventos;
- incorporar comisiones investigadoras y otras familias solo mediante módulos separados;
- realizar una auditoría móvil/escritorio antes de promover las páginas de comisión desde vista interna a navegación pública principal.

## 10. Regla editorial

El módulo no produce un ranking de “mejores” o “peores” parlamentarios ni un puntaje de productividad de comisión.

Su función es reconstruir **qué instancia existe, quién la integra y qué actuaciones institucionales deja registradas la fuente oficial**, conservando visibles las diferencias entre calendario, agenda, decisión, proyecto y comunicación institucional.
