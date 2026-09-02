# Método temático institucional v0.2

La clasificación temática de **Conoce a tu parlamentario** se apoyará primero en señales institucionales producidas por la propia tramitación legislativa y solo después en inferencia semántica. Esto reemplaza como diseño principal la idea de comenzar por una taxonomía abstracta de veinte macroáreas.

## Jerarquía de señales

1. **Comisión de origen del proyecto.** Se identifica cuando la página oficial registra una subetapa del tipo `Cuenta de proyecto. Pasa a Comisión de ...`. Es el proxy temático institucional de mayor peso.
2. **Trayectoria de comisiones.** Se conservan, en orden, las comisiones por las que el proyecto ha pasado o a las que ha sido remitido. Esta señal permite reconocer proyectos multidimensionales y distinguir una comisión inicial transversal de una comisión sustantiva posterior.
3. **Materia oficial.** Se conservan tanto las materias estructuradas del servicio legislativo como el campo `Materia:` de la página pública, cuando la Cámara lo completa.
4. **Ministerios patrocinantes.** Se usan como señal adicional en mensajes del Ejecutivo, nunca como sustituto automático del tema.
5. **Título y texto de la iniciativa.** Funcionan como evidencia semántica para resolver ambigüedades, no como primera fuente cuando existen señales institucionales más directas.

Partido, bancada, autor y bloque político quedan excluidos como señales temáticas.

## Por qué no basta una sola comisión

Las comisiones son un proxy fuerte, pero no equivalen automáticamente a una etiqueta temática final. Hay comisiones que cumplen frecuentemente funciones transversales. Dos casos importantes son:

- **Hacienda:** muchos proyectos pasan por ella debido a efectos fiscales aunque su objeto principal sea salud, educación, vivienda u otra política sectorial.
- **Constitución, Legislación, Justicia y Reglamento:** puede ser la materia sustantiva de una reforma institucional, pero también puede actuar como primera revisión jurídica de un proyecto cuyo objeto principal es seguridad, derechos, migración u otra área.

Por eso el sistema guarda dos variables distintas: `comision_origen_proxy` y `comisiones_tramitacion`.

## Unidad de clasificación

La etiqueta pública futura será deliberadamente simple. En vez de imponer desde el inicio una ontología extensa, el sistema producirá una **familia temática** apoyada por las señales institucionales. Ejemplos:

- Seguridad Ciudadana → Seguridad
- Salud → Salud
- Educación → Educación
- Trabajo y Seguridad Social → Trabajo y seguridad social
- Medio Ambiente y Recursos Naturales → Medio ambiente
- Minería y Energía → Minería y energía
- Transportes y Telecomunicaciones → Transportes y telecomunicaciones
- Relaciones Exteriores → Relaciones exteriores

La correspondencia comisión → familia es un proxy y se almacena separada de la futura clasificación final.

## Papel del modelo de lenguaje

Un modelo de lenguaje no deberá clasificar un proyecto partiendo de cero. Recibirá una ficha estructurada con:

- comisión de origen;
- secuencia de comisiones;
- materia oficial, si existe;
- ministerios patrocinantes, si existen;
- título;
- extracto del texto de ingreso.

Su tarea será seleccionar una familia temática sencilla, justificar brevemente la selección y señalar si existe un segundo tema relevante. Los casos donde las señales institucionales entren en tensión se enviarán a revisión humana.

## Datos derivados

`project_commissions.csv` contiene una fila por proyecto × comisión detectada, con secuencia, fecha, evidencia institucional y marca de comisión de origen.

`project_topic_signals.csv` resume por proyecto las señales que recibirá posteriormente el clasificador: comisión de origen, trayectoria, materias, ministerios y calidad del texto.

`topic_signal_diagnostics.json` audita la cobertura de estas señales.

## Regla metodológica

Las señales institucionales se conservan como datos y la clasificación final como inferencia. Nunca se sustituye la trayectoria oficial por una categoría generada por el modelo. Así podremos volver a clasificar todos los proyectos en el futuro sin tener que recolectar nuevamente la historia legislativa.

**Estado:** v0.2 en validación. Puede usarse para preparar y auditar señales, pero todavía no para publicar estadísticas temáticas definitivas.
