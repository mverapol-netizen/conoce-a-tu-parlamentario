# Módulo A · Participación y distribución de decisiones de voto · v0.1

**Proyecto:** Conoce a tu parlamentario  
**Cámara:** Cámara de Diputadas y Diputados de Chile, período 2026–2030  
**Estado:** especificación editorial, pedagógica y de interacción cerrada; pendiente adaptación del denominador técnico a oportunidades efectivas de pertenencia antes de activación pública  

Este documento convierte la primera capa de comportamiento legislativo en una pieza pública interpretable y auditable. El módulo responde dos preguntas distintas pero relacionadas:

1. **¿Cuánto participa esta persona en las votaciones nominales de Sala?**
2. **¿Cómo se distribuyen las decisiones que registra la Cámara cuando esa persona tiene una oportunidad de votar?**

La pieza no mide asistencia general, trabajo parlamentario, productividad ni calidad del desempeño. Tampoco infiere motivos a partir de las categorías oficiales de voto.

---

## 1. Idea pública central

La primera información sustantiva de la ficha debe ser un dato observable y fácil de comprender antes de entrar a relaciones partidarias o modelos espaciales.

### Título visible

**Participación en votaciones de Sala**

### Cifra principal

**[X]%**

### Texto principal dinámico

> **[Nombre] registró una decisión —a favor, en contra o abstención— en [n] de [N] votaciones nominales de Sala que ocurrieron mientras integraba la Cámara durante el período observado.**

El porcentaje principal es:

`participación sustantiva = (Afirmativo + En contra + Abstención) / oportunidades efectivas de votación`

La denominación pública será **participación en votaciones**, nunca `asistencia`.

---

## 2. Denominador público correcto

### Regla definitiva

El denominador `N` debe corresponder únicamente a las votaciones nominales de Sala celebradas **mientras la persona tenía una oportunidad institucional de participar como integrante de la Cámara**.

Esto exige distinguir:

- votaciones ocurridas durante su pertenencia efectiva a la legislatura;
- votaciones anteriores a su ingreso;
- votaciones posteriores a una eventual salida;
- estados oficiales registrados durante las oportunidades efectivas.

### Razón pedagógica y metodológica

Una persona que ingresa a mitad del período no puede ser tratada como si hubiera dejado de votar en las sesiones anteriores a su ingreso. Esa diferencia debe representarse como **missing estructural / fuera del período de pertenencia**, no como `No vota`.

### Pendiente técnico detectado

La tabla actual `member_participation_summary.csv` resume las 364 filas observadas para cada integrante del snapshot actual. Antes de activar este módulo públicamente, el constructor debe utilizar las ventanas de pertenencia a la Cámara y producir `eligible_rollcalls` u otra variable equivalente. Esta modificación no altera los datos primarios y debe permanecer como transformación derivada.

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

No se agruparán `No vota` y `Dispensado`, porque son categorías oficiales diferentes.

### Encima de la barra

A la izquierda:

**[X]% participación en votaciones**

Debajo, en texto menor:

**[n] decisiones registradas de [N] oportunidades**

A la derecha, cuando exista espacio:

**Período: [fecha de inicio individual]–[fecha de corte]**

### Debajo de la barra

Una leyenda con número y porcentaje de cada estado:

- A favor: `[n] · [x%]`
- En contra: `[n] · [x%]`
- Abstención: `[n] · [x%]`
- No vota: `[n] · [x%]`
- Dispensado: `[n] · [x%]`

Los porcentajes de esta leyenda usan como denominador las oportunidades efectivas `N`, de modo que la barra completa suma 100%.

---

## 4. Por qué la abstención cuenta como participación

La abstención es una opción de voto registrada por la Cámara. Por ello se incluye en la **participación sustantiva** del módulo descriptivo.

Esto no contradice el tratamiento del modelo espacial. W-NOMINATE e IRT utilizan principalmente la decisión binaria `Afirmativo / En contra`, y por tanto la abstención se trata allí como observación no binaria. Las dos decisiones responden a preguntas diferentes:

- este gráfico pregunta **si hubo una decisión parlamentaria registrada**;
- el modelo espacial pregunta **cómo se ordenan las decisiones binarias entre alternativas enfrentadas**.

La ficha debe explicar esta diferencia cuando el usuario llegue posteriormente al módulo espacial.

---

## 5. Significado preciso de cada categoría

### A favor

La Cámara registra una opción afirmativa en esa votación.

**No significa:** apoyo al Gobierno, apoyo al proyecto completo, posición ideológica progresista/conservadora ni aprobación general de una política. El objeto sometido a votación puede ser un proyecto completo, un artículo, una indicación, una insistencia, una observación presidencial u otra proposición.

### En contra

La Cámara registra una opción negativa en esa votación.

**No significa:** oposición al Gobierno ni rechazo del proyecto completo. Debe interpretarse respecto del objeto exacto sometido a votación.

### Abstención

La Cámara registra expresamente una abstención.

**Sí cuenta como participación sustantiva** en este módulo.

**No debe presentarse** como ausencia ni como equivalente a votar en contra.

### No vota

La fuente oficial registra `No Vota`.

**No debe traducirse automáticamente como ausencia física**, inasistencia, negligencia ni rechazo. El proyecto conserva la categoría oficial y no infiere el motivo cuando la fuente no lo establece.

### Dispensado

La fuente oficial registra una dispensa.

Se mantiene separada de `No vota` y no se transforma en una evaluación del parlamentario.

---

## 6. Interacción del gráfico

Cada segmento de la barra debe ser seleccionable.

### Al seleccionar un segmento

Se abre una lista de las votaciones que componen ese segmento, con:

- fecha;
- boletín;
- título abreviado del proyecto;
- objeto exacto de la votación cuando esté disponible;
- opción registrada del parlamentario;
- resultado general de la votación;
- enlace a la votación oficial de la Cámara.

### Ejemplo de interacción

Si el usuario selecciona **Abstención · 14**, no recibe solamente el número 14: puede abrir esas 14 votaciones y comprobar en qué asuntos se abstuvo.

La lista debe poder ordenarse por fecha y, una vez validada la taxonomía temática, filtrarse por materia.

---

## 7. Caja `Cómo leer este gráfico`

Texto visible recomendado:

> **La barra muestra qué registró oficialmente la Cámara en cada votación nominal de Sala durante el período en que esta persona integró la corporación. A favor, en contra y abstención cuentan como decisiones registradas. “No vota” y “Dispensado” se muestran por separado y no se interpretan automáticamente como inasistencia.**

---

## 8. Desplegable `¿Qué significa?`

> Este indicador permite observar con qué frecuencia una diputada o diputado registra una decisión en las votaciones nominales de Sala y cómo se distribuyen esas decisiones. Es una descripción de comportamiento en votaciones, no una evaluación general de desempeño.

---

## 9. Desplegable `¿Qué no significa?`

Texto recomendado:

> **No es un indicador de asistencia al Congreso.** Una parlamentaria o parlamentario puede desarrollar actividad legislativa fuera de una votación nominal de Sala, y la categoría “No vota” no permite inferir por sí sola si estaba o no presente en la sesión.
>
> **No mide productividad ni calidad.** Participar en más votaciones no permite concluir, por sí solo, que una persona trabaja más o mejor que otra.
>
> **No mide apoyo u oposición política.** La cantidad de votos afirmativos y negativos no puede interpretarse sin conocer qué se estaba votando en cada caso.

---

## 10. Desplegable `¿Cómo lo calculamos?`

Versión pública breve:

> Usamos exclusivamente votaciones nominales verificadas como votaciones de Sala de la Cámara de Diputadas y Diputados desde el 11 de marzo de 2026. Para cada integrante conservamos por separado las categorías oficiales Afirmativo, En contra, Abstención, No vota y Dispensado. El porcentaje de participación cuenta Afirmativo, En contra y Abstención como decisiones registradas y utiliza como denominador solo las votaciones ocurridas mientras la persona integraba la Cámara.

### Versión técnica enlazada

Debe explicar además:

- fuente oficial de cada roll call;
- fuente de los votos nominales;
- reconstrucción temporal de pertenencia;
- fecha de corte;
- SHA/versión del pipeline;
- definición exacta de `substantive_participation_pct`;
- tratamiento de missing estructural;
- relación con `member_votes.csv`, `member_votes_enriched.csv` y la tabla derivada de participación.

---

## 11. Contexto comparativo de Cámara

### Decisión editorial

La comparación con otros parlamentarios debe ser **secundaria**, no el centro del gráfico.

No se mostrará un ranking `1 de 155` ni etiquetas como `alto/bajo desempeño`.

### Forma recomendada

Debajo del gráfico puede existir un pequeño bloque opcional:

**Contexto de la Cámara**

> `Mediana de participación en votaciones: [M]%`

Y, si el espacio visual lo permite, un mini-distribución horizontal con:

- todos los parlamentarios como marcas neutras;
- mediana de Cámara;
- parlamentario seleccionado destacado.

### Regla

La comparación solo se activa cuando todos los integrantes comparados utilizan el mismo criterio de oportunidades efectivas. Si existen cohortes con ventanas de pertenencia demasiado distintas, debe informarse explícitamente y evitar un ranking ordinal.

---

## 12. Casos límite

### Integrante sin oportunidades observadas

Mostrar:

**Sin período comparable todavía**

No calcular porcentaje.

### Integrante con muy pocas oportunidades

Mostrar el porcentaje, pero acompañado por:

> **Basado en solo [N] votaciones desde su incorporación.**

No comparar ordinalmente con toda la Cámara si el denominador es demasiado pequeño.

### Cambios de pertenencia durante el período

La ventana pública se construye sobre las fechas de pertenencia, no sobre el snapshot partidario actual.

### Datos oficiales corregidos posteriormente

El módulo se regenera en cada actualización. La fecha de corte debe estar visible y las correcciones retroactivas de la fuente deben propagarse al resumen.

---

## 13. Accesibilidad

La barra no puede depender exclusivamente del color.

Cada segmento debe tener:

- etiqueta textual;
- valor numérico;
- porcentaje;
- `aria-label` descriptivo;
- navegación por teclado.

En móvil, la leyenda numérica sustituye cualquier información que no quepa dentro de los segmentos pequeños.

---

## 14. Orden visual dentro de la ficha

El módulo aparece inmediatamente después del encabezado biográfico básico.

Secuencia:

1. título `Participación en votaciones de Sala`;
2. cifra principal;
3. frase interpretativa;
4. barra apilada;
5. leyenda numérica;
6. botón `Ver votaciones`;
7. bloque opcional `Contexto de la Cámara`;
8. desplegables `Cómo leerlo`, `Qué significa`, `Qué no significa`, `Cómo lo calculamos`.

No deben aparecer términos como `score`, `nota`, `desempeño`, `ranking`, `asistencia` o `cumplimiento`.

---

## 15. Contrato de datos para implementación

La capa web deberá recibir por parlamentario al menos:

- `member_id`
- `period_start`
- `period_end_or_cutoff`
- `eligible_rollcalls`
- `n_affirmative`
- `n_against`
- `n_abstention`
- `n_no_vote`
- `n_excused`
- `n_substantive`
- `substantive_participation_pct`
- `data_cutoff`
- `method_version`

Invariante obligatorio:

`eligible_rollcalls = n_affirmative + n_against + n_abstention + n_no_vote + n_excused`

Y:

`n_substantive = n_affirmative + n_against + n_abstention`

Las observaciones fuera de la ventana de pertenencia no entran en ninguna de esas cinco categorías.

---

## 16. Gate de publicación del módulo A

### Editorial/pedagógico

**CERRADO.**

Quedan fijados:

- pregunta pública;
- vocabulario permitido;
- vocabulario prohibido;
- gráfico principal;
- interpretación;
- interacción;
- trazabilidad;
- manejo de casos límite.

### Técnico

**PENDIENTE DE UNA CORRECCIÓN ACOTADA:** adaptar el resumen de participación a oportunidades efectivas según ventana de pertenencia antes de conectarlo con la ficha pública.

Una vez corregido y auditado ese denominador, este módulo puede publicarse sin depender de W-NOMINATE, IRT, OC, clasificación temática ni interpretación ideológica.

---

## 17. Principio interpretativo final

La afirmación que este gráfico autoriza es deliberadamente limitada:

> **Sabemos qué opción registró oficialmente la Cámara para esta persona en cada votación nominal de Sala y podemos describir cuántas veces emitió una decisión durante sus oportunidades efectivas de participación.**

No autoriza, por sí solo, ninguna afirmación sobre las razones de una no votación, la calidad del trabajo parlamentario, la ideología del representante ni su apoyo al Gobierno.
