# Módulo A · Participación y distribución de decisiones de voto · v0.1

**Proyecto:** Conoce a tu parlamentario  
**Cámara:** Cámara de Diputadas y Diputados de Chile, período 2026–2030  
**Estado:** **CERRADO E IMPLEMENTADO** en su núcleo público; comparación contextual de Cámara queda como extensión opcional posterior  
**Corte auditado:** 364 votaciones nominales de Sala y 56.420 registros nominales, hasta el 1 de septiembre de 2026  

Este documento convierte la primera capa de comportamiento legislativo en una pieza pública interpretable y auditable. El módulo responde dos preguntas distintas pero relacionadas:

1. **¿Cuánto participa esta persona en las votaciones nominales de Sala?**
2. **¿Cómo se distribuyen las decisiones que registra la Cámara cuando esa persona tiene una oportunidad de votar?**

La pieza no mide asistencia general, trabajo parlamentario, productividad ni calidad del desempeño. Tampoco infiere motivos a partir de las categorías oficiales de voto.

---

## 1. Idea pública central

La primera información sustantiva de la ficha es un dato observable y comprensible antes de entrar a relaciones partidarias o modelos espaciales.

### Título visible

**Participación en votaciones de Sala**

### Cifra principal

**[X]%**

### Texto dinámico

> **[Nombre] registró una decisión —a favor, en contra o abstención— en [n] de [N] votaciones nominales de Sala en las que tuvo una oportunidad registrada de votar.**

El porcentaje principal es:

`participación sustantiva = (Afirmativo + En contra + Abstención) / oportunidades efectivas de votación`

La denominación pública es **participación en votaciones**, nunca `asistencia`.

---

## 2. Denominador público: regla cerrada

### Regla definitiva

El denominador `N` no se obtiene suponiendo que toda persona histórica deba estar presente en todas las votaciones de la legislatura. Se deriva directamente del detalle nominal oficial:

> **Cada fila oficial `vote_id × diputado_id` en `member_votes.csv` cuenta como una oportunidad efectiva de votación para esa persona.**

Si el ID de una persona no aparece en el detalle nominal de una votación —por ejemplo porque todavía no integraba la Cámara o porque ya dejó el cargo— esa votación no entra en su denominador.

### Por qué esta solución es mejor que una ventana imputada

Inicialmente se consideró reconstruir el denominador mediante una tabla separada de fechas de ingreso y salida. La auditoría mostró que no es necesario para este indicador: la propia fuente nominal define quién tiene un registro asociado a cada roll call.

Esto evita convertir en `No vota` una votación en la que la persona no tenía una oportunidad institucional de participar.

### Auditoría del corte actual

En el corte vigente:

- 364 roll calls verificados de Sala;
- 155 registros nominales en cada roll call;
- 56.420 pares únicos `vote_id × diputado_id`;
- 155 integrantes históricos observados hasta ahora;
- 155 filas en el resumen público;
- suma de oportunidades individuales: 56.420;
- cero roll calls con cardinalidad distinta de 155;
- cero opciones de voto desconocidas;
- cero votos nominales sin roll call asociado.

Actualmente todos los integrantes observados tienen 364 oportunidades porque todavía no se ha producido un reemplazo dentro del universo acumulado. El pipeline, sin embargo, ya no exige que la historia completa contenga exactamente 155 IDs únicos y está preparado para que ese número crezca durante la legislatura.

---

## 3. Visualización principal

### Forma

Una **barra horizontal apilada al 100%**, construida sobre las oportunidades efectivas `N`.

Segmentos:

1. **A favor**
2. **En contra**
3. **Abstención**
4. **No vota**
5. **Dispensado**

`No vota` y `Dispensado` permanecen separados porque son categorías oficiales diferentes.

### Encima de la barra

La ficha muestra:

- **[X]% participación en votaciones**;
- `[n] decisiones registradas de [N] oportunidades`;
- período entre la primera y la última oportunidad observada de la persona.

### Debajo de la barra

La leyenda informa para cada estado:

- número absoluto;
- porcentaje sobre las oportunidades efectivas.

La suma de los cinco estados reproduce exactamente `N`.

---

## 4. Por qué la abstención cuenta como participación

La abstención es una opción expresamente registrada por la Cámara y por eso se incluye en la **participación sustantiva** de este módulo descriptivo.

Esto no contradice el tratamiento del modelo espacial:

- este gráfico pregunta **si hubo una decisión parlamentaria registrada**;
- W-NOMINATE/IRT preguntan **cómo se ordenan las decisiones binarias entre alternativas enfrentadas** y tratan la abstención como observación no binaria.

La misma categoría puede, por tanto, recibir tratamientos diferentes cuando las preguntas analíticas son distintas.

---

## 5. Significado preciso de las categorías

### A favor

La Cámara registra una opción afirmativa.

**No significa por sí sola:** apoyo al Gobierno, apoyo al proyecto completo, posición ideológica ni aprobación general de una política. El objeto puede ser un proyecto completo, artículo, numeral, indicación, insistencia, observación presidencial u otra proposición.

### En contra

La Cámara registra una opción negativa.

**No significa por sí sola:** oposición al Gobierno ni rechazo del proyecto completo. Se interpreta respecto del objeto exacto sometido a votación.

### Abstención

La Cámara registra expresamente una abstención. Cuenta como participación sustantiva en este módulo y no se presenta como ausencia ni como voto en contra.

### No vota

La fuente oficial registra `No Vota`. El proyecto conserva esa categoría y **no infiere automáticamente ausencia física, inasistencia, negligencia ni rechazo**.

### Dispensado

La fuente oficial registra una dispensa. Se mantiene separada de `No vota` y no se transforma en una evaluación del parlamentario.

---

## 6. Interacción y trazabilidad pública

La barra y la leyenda son interactivas.

### Al seleccionar un segmento

La ficha carga bajo demanda las votaciones que forman esa categoría y muestra, de la más reciente a la más antigua:

- fecha;
- boletín;
- título del proyecto;
- objeto exacto de la votación cuando la fuente lo entrega;
- opción registrada de la persona;
- resultado general;
- enlace directo al detalle oficial de la Cámara.

También existe el control **Ver las [N] votaciones**, que abre todas las oportunidades de la persona y conserva su opción en cada una.

### Títulos de proyectos heredados

Algunas votaciones del período corresponden a proyectos ingresados antes del 11 de marzo de 2026. `projects.csv` no contiene necesariamente todos esos proyectos. Para evitar títulos incompletos, el activo público complementa exclusivamente el **título documental** desde `topics/rollcall_inherited_topic_final.csv`.

Este uso no publica ni utiliza todavía la clasificación temática de esa tabla. Solo recupera un dato factual ya reconstruido.

En la auditoría final del módulo:

- roll calls públicos: **364/364**;
- relaciones individuales públicas: **56.420/56.420**;
- roll calls sin título de proyecto: **0**.

---

## 7. Texto `¿Cómo leer este gráfico?`

La versión implementada explica:

> La cifra principal cuenta como participación una decisión registrada a favor, en contra o como abstención. La barra conserva además por separado los estados oficiales No vota y Dispensado. El largo de cada segmento representa su proporción real dentro de las oportunidades de votación de esta persona.

---

## 8. Texto `¿Qué significa y qué no significa?`

La ficha explica explícitamente que el indicador describe participación observada en **votaciones nominales de Sala**.

No mide:

- asistencia general al Congreso;
- trabajo en comisiones;
- productividad legislativa;
- calidad del desempeño;
- apoyo u oposición al Gobierno.

Tampoco convierte `No vota` en inasistencia ni una abstención en falta de participación.

---

## 9. Texto `¿Cómo lo calculamos?`

Versión pública implementada:

> **Participación = (A favor + En contra + Abstención) / oportunidades efectivas de votación.** Cada registro nominal oficial que vincula una votación con esta diputada o diputado cuenta como una oportunidad. Si una persona todavía no integraba la Cámara o ya había dejado el cargo y su ID no aparece en el detalle nominal oficial, esa votación no entra en su denominador. Las categorías No vota y Dispensado se conservan sin recodificarlas.

---

## 10. Arquitectura de datos implementada

### Datos primarios

- `data/legislative/2026/member_votes.csv`
- `data/legislative/2026/rollcalls.csv`
- `data/legislative/2026/projects.csv`

### Complemento documental para proyectos heredados

- `data/legislative/2026/topics/rollcall_inherited_topic_final.csv` — solo título del proyecto en este módulo.

### Transformación derivada

- `scripts/build_member_participation.py`

### Salidas auditables

- `data/legislative/2026/member_participation_summary.csv`
- `data/legislative/2026/member_participation_diagnostics.json`

### Activos públicos

- `assets/js/participation.js` — resumen individual ligero cargado con la ficha;
- `assets/data/participation_rollcalls.json` — metadatos públicos de las votaciones;
- `assets/data/participation_member_votes.json` — pares compactos de votación y opción por integrante, cargados solo cuando el usuario pide evidencia.

La separación permite que la ficha inicial sea liviana y que el historial detallado se descargue únicamente al abrir una categoría.

---

## 11. Separación respecto de otros indicadores

La participación se calcula directamente desde los votos nominales primarios y **no depende de partido, bancada, clasificación temática ni W-NOMINATE**.

La coincidencia con partido/bancada sigue un pipeline separado (`build_member_voting_summary.py`) porque responde una pregunta distinta y necesita afiliaciones temporales y primitivas de grupo.

Esta separación impide que un problema de afiliación política invalide un indicador puramente descriptivo de voto.

---

## 12. Contexto comparativo de Cámara

La comparación con otros parlamentarios queda como **extensión secundaria**, no como parte necesaria del módulo A.

No se publica por ahora:

- ranking `1 de 155`;
- etiquetas `alto/bajo desempeño`;
- percentil normativo de participación.

Una futura vista de contexto podrá mostrar mediana y distribución de Cámara de forma descriptiva, siempre que las ventanas individuales sean comparables.

---

## 13. Casos límite

### Integrante sin oportunidades observadas

Mostrar: **Sin período comparable todavía**. No imputar porcentaje.

### Integrante con pocas oportunidades

Mostrar el porcentaje junto al denominador absoluto y una advertencia del tipo: **Basado en solo [N] votaciones desde su incorporación.**

### Reemplazos o salidas

El denominador se adapta automáticamente a las filas nominales asociadas al ID de cada persona. El total histórico de personas puede superar 155 sin romper el resumen.

### Correcciones posteriores de la fuente

El workflow regenera resumen y activos públicos cuando cambian `member_votes.csv`, `rollcalls.csv`, `projects.csv` o la fuente documental de proyectos heredados.

---

## 14. Accesibilidad

La barra no depende solo del color:

- cada segmento es un botón con `aria-label`;
- la leyenda contiene etiqueta, valor y porcentaje;
- las categorías con cero registros se muestran pero quedan deshabilitadas;
- existe foco visible para navegación por teclado;
- en móvil la leyenda conserva toda la información aunque un segmento sea demasiado pequeño para contener texto.

---

## 15. Gate de publicación del módulo A

### Editorial/pedagógico

**CERRADO.**

### Denominador y auditoría

**CERRADO.**

### Trazabilidad pública

**CERRADA.**

### Implementación web

**IMPLEMENTADA.**

La activación no depende de W-NOMINATE, IRT, OC ni de la validación temática. El único componente deliberadamente diferido es la comparación contextual de Cámara, que es una extensión y no modifica el significado del indicador.

---

## 16. Principio interpretativo final

La afirmación autorizada es deliberadamente limitada:

> **Sabemos qué opción registró oficialmente la Cámara para esta persona en cada votación nominal de Sala y podemos describir cuántas veces emitió una decisión durante sus oportunidades efectivas de participación.**

El usuario puede además bajar desde cada segmento del gráfico hasta las votaciones concretas que lo componen y abrir la fuente oficial correspondiente.

El módulo no autoriza, por sí solo, afirmaciones sobre las razones de una no votación, la calidad del trabajo parlamentario, la ideología del representante ni su apoyo al Gobierno.
