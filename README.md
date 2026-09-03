# Conoce a tu parlamentario

Herramienta cívica y politológica para conectar a una persona con sus representantes en la Cámara de Diputadas y Diputados de Chile y explorar, con evidencia auditable, distintas dimensiones de su actividad legislativa, su organización parlamentaria y el comportamiento de la Cámara.

## Qué ofrece la versión pública

### Tu distrito

1. La persona selecciona su **región** y **comuna**.
2. El sitio identifica automáticamente su **distrito electoral**.
3. Muestra las diputadas y diputados que representan ese territorio.
4. Desde cada representante se puede abrir una ficha legislativa estable.

### Hemiciclo

`hemiciclo.html` presenta los **155 escaños** como un mapa interactivo de fuerzas. Distingue deliberadamente:

- partido;
- bancada o Comité Parlamentario;
- independientes adscritos a una bancada, sin presentarlos como militantes;
- clasificación editorial entre oficialismo, oposición y no alineados.

El gráfico representa **distribución de fuerzas**, no la ubicación física exacta de los escaños en la Sala.

### Fichas legislativas

Las fichas públicas mantienen cuatro módulos analíticos metodológicamente cerrados:

- **A · Participación y decisiones de voto:** oportunidades efectivas de votación, con Afirmativo, En Contra, Abstención, No Vota y Dispensado preservados por separado y drill-down a la evidencia oficial.
- **B · Coincidencia con partido y bancada/comité:** comparación leave-one-out con la posición predominante de pares, umbral público de minoría binaria ≥10% y mínimo de 20 comparaciones para publicar porcentaje.
- **C · Iniciativa legislativa:** mociones originadas en Cámara en las que la persona figura formalmente como autor/a, distinguiendo autoría individual y compartida.
- **D · Coautoría:** relaciones formales entre autores de una misma moción, con acceso a los boletines que sostienen cada vínculo.

A esos módulos se suma una capa de **contexto organizacional**: la ficha puede mostrar las comisiones actuales en las que la persona aparece como integrante según el directorio institucional de la Cámara. Esta membresía no se incorpora a un puntaje y no se interpreta por sí sola como especialización, asistencia, influencia o desempeño.

Los módulos describen comportamiento o posición institucional observable. No se transforman en un puntaje general de desempeño.

### Patrones de voto · laboratorio W-NOMINATE

`wnominate.html` es un **laboratorio público experimental**, separado de las fichas cerradas. Permite explorar:

- W-NOMINATE 1D como patrón espacial principal de trabajo;
- una vista 2D explícitamente exploratoria;
- filtros territoriales, partidarios y por parlamentario;
- contexto temático del proyecto asociado a cada votación;
- bootstrap por proyectos como diagnóstico de robustez;
- descarga PNG y modo pantalla completa.

La estimación base usa `lop = 2.5%` y `minvotes = 20`, con 276 votaciones elegibles y 154 de 155 integrantes estimados.

La visualización pública invierte el signo técnico de D1 para mantener la convención izquierda → derecha (`D1 visual = -D1 técnico`). La lectura izquierda–derecha está fuertemente respaldada por la auditoría sustantiva interna, pero sigue siendo **provisional** hasta cerrar los gates multimétodo y temporales pendientes.

La segunda dimensión permanece sin etiqueta política sustantiva.

## Entiende el Congreso · entorno interno

`entender.html` es una arquitectura educativa en desarrollo y todavía no forma parte de la navegación pública principal. Combina lecciones institucionales con herramientas construidas sobre datos reales.

Actualmente incluye, entre otras piezas:

- **Sigue un proyecto** (`proyectos.html` / `proyecto.html?boletin=...`): estado, tramitación, autoría y votaciones nominales vinculadas.
- **¿Qué se votó realmente?** (`votaciones.html` / ficha de votación): separa proyecto general y objeto exacto sometido a decisión.
- **Hoy en la Cámara** (`hoy.html`): sesiones de Sala registradas para el día y próximas sesiones citadas, con control de frescura y actualización diaria.
- **Explora las comisiones** (`comisiones.html` / `comision.html?id=...`): directorio actual, integrantes, proyectos asociados, sesiones, citaciones y resultados recuperados de las fichas institucionales.
- **¿A quién debo contactar?** (`orientar.html`): prototipo para distinguir representación política de competencia administrativa, judicial o electoral.

Las páginas internas usan `noindex` mientras se completan auditorías de contenido, fuentes, diseño y experiencia móvil.

## Comisiones y trabajo fuera de Sala

El módulo de comisiones busca reducir el sesgo de observabilidad que aparece cuando toda la actividad parlamentaria se representa únicamente mediante votaciones nominales de Sala.

La primera prueba con los servicios Open Data de comisiones devolvió un universo implausible de solo dos instancias incluso al resolver el período legislativo actual. El workflow fue diseñado para **fallar antes de publicar** ante ese resultado.

El directorio operativo se reconstruye por ello desde las páginas institucionales oficiales server-rendered de la Cámara, usando `prmID` como identificador de instancia.

Contrato vigente de directorio: `commissions-web-v0.4`.

La corrida inicial validada recuperó:

- 34 instancias del directorio permanente;
- 34 fichas con integrantes recuperados;
- 389 filas de membresía.

La interfaz distingue las 27 comisiones legislativas temáticas de otras comisiones permanentes y subcomisiones. No mezcla automáticamente comisiones investigadoras, unidas, mixtas u otras familias.

La actividad de comisión se mantiene en capas conceptualmente diferentes:

- **Sesiones:** calendario/historial registrado;
- **Citaciones:** agenda convocada;
- **Resultados:** materias tratadas o acuerdos registrados;
- **Proyectos de ley:** iniciativas asociadas institucionalmente a la comisión en la vista oficial;
- **Oficios enviados:** capa en proceso de validación al momento de este corte.

Estas capas no se suman en un indicador de productividad. El contrato metodológico completo está en `docs/MODULO_COMISIONES_V0_1.md`.

## Principios metodológicos

El proyecto mantiene separadas cuatro capas:

1. **datos primarios oficiales**;
2. **clasificaciones analíticas derivadas**;
3. **indicadores descriptivos**;
4. **modelos estadísticos e interpretaciones politológicas**.

Una capa derivada nunca reemplaza silenciosamente la fuente primaria.

Regla editorial general:

> Cada gráfico debe responder una pregunta concreta, formular una conclusión limitada y permitir reconstruir la evidencia y el método que la sostienen.

## Cobertura actual

- 16 regiones.
- 28 distritos electorales.
- 346 comunas.
- 155 integrantes de la Cámara 2026–2030.
- 155 fotografías oficiales almacenadas localmente.
- perfiles, partido, bancada/comité, distrito, región y contacto institucional.
- base legislativa incremental desde el 11 de marzo de 2026.
- votaciones nominales de Sala, proyectos, autorías, tramitación, afiliaciones históricas y capas derivadas.
- directorio institucional de comisiones y membresías actuales con gate de plausibilidad.
- snapshots separados de agenda de Sala y actividad reciente de comisiones.

## Fuentes

La base se construye y contrasta con fuentes públicas oficiales:

- Servicio Electoral de Chile (Servel);
- Biblioteca del Congreso Nacional (BCN);
- Cámara de Diputadas y Diputados de Chile;
- Portal de Datos Abiertos del Congreso.

Cuando un servicio Open Data no representa adecuadamente el universo institucional, el proyecto puede utilizar otra página oficial de la misma institución, siempre con fuente, método y control de calidad explícitos.

## Actualización

El repositorio utiliza GitHub Actions para sincronización automática:

- la base legislativa principal se actualiza semanalmente;
- perfiles y afiliaciones mantienen sus propios controles de actualización;
- la agenda liviana de Sala se actualiza diariamente;
- el directorio y las capas de comisión se actualizan semanalmente y pueden ejecutarse manualmente.

Los hechos institucionales pueden actualizarse automáticamente cuando la fuente lo permite; clasificaciones editoriales como oficialismo/oposición/no alineado requieren revisión pública separada.

## Estado científico del laboratorio espacial

W-NOMINATE 1D es actualmente el benchmark descriptivo espacial del proyecto. Antes de convertir su coordenada en un indicador individual cerrado dentro de las fichas todavía deben completarse, entre otros:

- IRT bayesiano 2PL 1D;
- Optimal Classification;
- estabilidad temporal con ventanas comparables;
- contrato final de incertidumbre/robustez;
- cierre formal de la interpretación pública de D1.

La taxonomía temática también mantiene pendiente una validación externa/formal por macroárea. Por eso el filtro de la página se presenta como **contexto temático del proyecto**, no como materia oficial ni clasificación exacta de cada roll call.

## Próximas capas

La expansión natural del proyecto incluye:

- cerrar la validación de la capa de oficios de comisión y estudiar enlaces a documentos/respuestas;
- asistencia a comisiones con denominadores temporales correctos y tratamiento de reemplazos;
- presidencias y otros roles institucionales con temporalidad fiable;
- audiencias públicas, actas e informes como capas documentales separadas;
- materias de iniciativas, una vez validada externamente la taxonomía;
- actividad fiscalizadora más allá de comisiones cuando exista una fuente auditable;
- indicaciones/enmiendas cuando exista atribución individual fiable;
- apoyo al Ejecutivo solo después de reconstruir su posición en cada votación;
- validación multimétodo y temporal del modelo espacial.

El objetivo es pasar de **“¿quién me representa?”** a **“¿qué hace mi representante y en qué instituciones parlamentarias lo hace?”**, y además ofrecer una lectura transparente de **cómo se estructura empíricamente el comportamiento legislativo de la Cámara**.
