# Auditoría omnibus 18216-05 — Ciclo 04: trabajo, empleo, Sala Cuna y función pública

> Documento interno de investigación. No usar todavía como etiqueta pública de D1 ni incorporar coordenadas espaciales a perfiles públicos.
>
> Corte: 2 de septiembre de 2026. Continúa los ciclos 01–03 de auditoría interna del boletín 18216-05.

## 1. Pregunta del ciclo

Este ciclo pregunta si las votaciones laborales de la Megareforma aportan evidencia sustantiva independiente para interpretar D1 o si su fuerza matemática puede explicarse mejor por procedimiento, disciplina gobierno-oposición o minorías pequeñas.

La auditoría distingue cuatro objetos que no deben confundirse:

1. **política social-laboral sustantiva**, especialmente Sala Cuna Universal;
2. **arquitectura de capacitación y empleo**, especialmente SENCE, franquicia tributaria y certificación de competencias;
3. **administración y beneficios del empleo público**, como retiro voluntario;
4. **probidad y disciplina funcionaria**, como el uso de licencias médicas.

La distinción es importante porque `abs(spread_1d)` mide capacidad de una votación para ordenar posiciones en el espacio estimado, no la importancia sustantiva o amplitud política del conflicto.

D1 conserva signo arbitrario. El análisis que sigue valida contenido de roll calls; no asigna por sí solo sentido político al signo numérico.

---

## 2. Cadena Sala Cuna Universal

La reconstrucción de esta cadena permite separar con claridad procedimiento y fondo.

### 2.1. Vote ID 88910 — admisibilidad, no política sustantiva directa

**Fecha:** 20 de mayo de 2026.

**Objeto formal:** reclamación de la declaración de inadmisibilidad efectuada por la Comisión de Hacienda respecto de la indicación del diputado Jorge Brito que modificaba el Código del Trabajo para establecer Sala Cuna Universal.

La propia ficha oficial de la Cámara identifica expresamente que el objeto era la **inadmisibilidad** de la indicación.

**Resultado en nuestra base:** 80 sí / 65 no / 9 abstenciones.

**Coalición:** oposición 64/0 a favor de revertir la inadmisibilidad; oficialismo 4/55; no alineados 12/10.

**Clasificación:** `F5_labor_employment_public_service / sala_cuna_universal`.

**Proceso:** `inadmissibility_reconsideration`.

**Nivel de evidencia:** **III — contextual/procedimental**.

**Regla interpretativa:** no puede presentarse como “voto a favor de Sala Cuna Universal”. El contenido de la indicación es sustantivo, pero el objeto formal de este roll call es si la indicación podía ser discutida.

Fuente oficial: https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion=88910

### 2.2. Vote ID 88911 — incorporación sustantiva de Sala Cuna Universal

**Objeto formal:** indicación renovada del diputado Jorge Brito, páginas 603–620 del informe de Hacienda.

Una vez superada la discusión de admisibilidad, la Cámara votó directamente la indicación que incorporaba un sistema de Sala Cuna Universal mediante modificaciones al Código del Trabajo.

**Resultado:** 82 sí / 48 no / 24 abstenciones.

**Coalición:** oposición 64/0 a favor; oficialismo 5/39; no alineados 13/9.

Entre partidos, FA, PC, DC, PL, PPD y PS votaron prácticamente o completamente a favor; Republicanos, PNL y buena parte de la derecha gubernamental se concentraron en contra, mientras PDG apoyó mayoritariamente.

**`abs(spread_1d)`:** 0.7853.

**Clasificación:** `F5 / sala_cuna_universal`.

**Nivel de evidencia:** **I — sustantiva principal**.

Este es el roll call correcto para hablar de la posición de la Cámara ante la incorporación de Sala Cuna Universal en este proyecto.

Fuente oficial: https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion=88911

### 2.3. Vote ID 89485 — supresión posterior de Sala Cuna Universal

**Fecha:** 21 de julio de 2026.

**Objeto formal:** enmienda del Senado que suprime el artículo 31, disposición que contenía el sistema de Sala Cuna Universal.

**Resultado:** 75 sí / 70 no.

**Coalición:** oficialismo 67/0 a favor de la supresión; oposición 0/58; no alineados 8/12.

**`abs(spread_1d)`:** 1.5806, cuarto roll call más identificador del omnibus.

**Nivel:** **II**. Es una decisión sustantiva directa, pero ocurre en un tercer trámite caracterizado por serialidad muy fuerte de la coalición gobierno-oposición.

### 2.4. Unidad interpretativa

Los votos 88910, 88911 y 89485 se registran bajo:

`SALA_CUNA_UNIVERSAL_POLICY_CHAIN`

No constituyen tres pruebas independientes.

- 88910 explica el **filtro de admisibilidad**;
- 88911 registra la **decisión sustantiva de incorporación**;
- 89485 registra la **decisión sustantiva posterior de supresión**.

La cadena es especialmente valiosa porque demuestra que una misma disputa puede aparecer primero como procedimiento y después como política pública directa. Para interpretar D1 se privilegian 88911 y, complementariamente, 89485; 88910 se mantiene como contexto.

---

## 3. Cadena de reforma del sistema de capacitación, SENCE y certificación

Esta familia es distinta de Sala Cuna. También produce una división ideológica fuerte, pero se refiere a la arquitectura institucional y financiera de la capacitación laboral.

### 3.1. Vote ID 88932 — artículo 26 del mensaje

**Objeto:** artículo 26 del mensaje original, respecto del cual las comisiones propusieron rechazo.

El artículo forma parte de la reforma a la ley 19.518 y de la reorganización de la arquitectura de capacitación y empleo, incluyendo reglas vinculadas al financiamiento mediante franquicia tributaria SENCE.

**Resultado:** 60 sí / 91 no / 1 abstención.

**Coalición:** oposición casi completamente en contra; oficialismo mayoritariamente a favor, aunque con disidencias; no alineados mayoritariamente en contra.

**`abs(spread_1d)`:** 0.4844.

**Nivel:** **II** porque el artículo es amplio y compuesto. Su contenido laboral está identificado, pero no debe tratarse como una única proposición elemental.

### 3.2. Vote ID 88933 — financiamiento de certificación de competencias

**Objeto:** artículo 27 del mensaje original.

La disposición modifica la ley 20.267 en materia de financiamiento de la certificación de competencias laborales: sustituye el mecanismo previo por financiamiento con recursos de la empresa y deroga reglas operativas vinculadas al uso o imputación de la franquicia tributaria SENCE.

**Resultado:** 58 sí / 94 no.

**Coalición:** oposición 0/63 a favor; oficialismo 50/17; no alineados 8/14.

**`abs(spread_1d)`:** **1.5840**, tercer roll call más identificador del omnibus.

**Nivel:** **I — sustantiva principal**.

Este caso tiene especial valor para D1: combina contenido laboral-económico preciso, oposición amplia entre posiciones reconocibles y capacidad estadística muy alta para ordenar la dimensión.

Fuente de votación: https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion=88933

### 3.3. Vote ID 89486 — reglas posteriores sobre qué constituye capacitación

**Fecha:** 21 de julio de 2026.

**Objeto:** enmienda del Senado que agrega un artículo 33 nuevo y modifica la ley 19.518.

La reconstrucción del informe del Senado permite cerrar la familia sustantiva: entre otras reglas, la modificación precisa actividades que no constituyen capacitación y agrega requisitos y controles aplicables al sistema de cursos. El artículo es compuesto y por eso no se fuerza todavía una exégesis numeral por numeral.

**Resultado:** 75 sí / 70 no.

**Coalición:** idéntica a 89485: oficialismo/derecha a favor, oposición en contra.

**Nivel:** **II**, por dos razones simultáneas: es contenido laboral directo, pero el artículo es compuesto y aparece en una secuencia de tercer trámite con coalición serial.

### 3.4. Unidad interpretativa

88932, 88933 y 89486 se agrupan como:

`TRAINING_SYSTEM_REFORM_CHAIN`

No se cuentan como tres validaciones independientes de D1. La evidencia principal es 88933; 88932 establece el marco de reforma y 89486 muestra que el conflicto reaparece en una etapa posterior del mismo sistema normativo.

---

## 4. Retiro voluntario en el empleo público: evidencia de consenso, no clivaje principal

### 4.1. Vote ID 88934 — ampliación de cupos

**Objeto:** artículo 24 del texto de Hacienda, correspondiente al artículo 28 del mensaje.

Aumenta de 2.200 a 6.000 el cupo de beneficiarios del bono de incentivo al retiro regulado por la ley 20.948.

**Resultado:** 122 sí / 30 no.

**Coalición:** oficialismo 67/0 a favor; oposición dividida 39/24; no alineados 16/6.

**`abs(spread_1d)`:** 0.2831.

**Nivel:** **III**. Es una política pública directa, pero con apoyo amplio y una estructura que no representa una oposición bipolar general de la Cámara.

### 4.2. Vote ID 88935 — asignación de cupos adicionales

**Objeto:** artículo 25 del texto de Hacienda, correspondiente al artículo 29 del mensaje.

Implementa durante 2026 la distribución de cupos adicionales generados por la ampliación legal.

**Resultado:** 138 sí / 14 no.

**Patrón:** oficialismo y no alineados votan a favor; la oposición también lo hace mayoritariamente. El rechazo está concentrado en un subconjunto pequeño, especialmente el PC.

**`abs(spread_1d)`:** **1.5718**, séptimo roll call más identificador del omnibus.

**Nivel:** **IV — localización individual/minoría específica**.

Este caso es metodológicamente decisivo: su `abs(spread_1d)` es casi tan grande como el de Sala Cuna 89485 y capacitación 88933, pero políticamente la votación es 138–14. Por lo tanto, **la fuerza discriminante del roll call no equivale a la amplitud del desacuerdo sustantivo**.

88934 y 88935 se agrupan como:

`PUBLIC_SERVICE_RETIREMENT_BONUS_CHAIN`

---

## 5. Licencias médicas de funcionarios: segundo “falso amigo” de alta discriminación

### Vote ID 88936

**Objeto:** artículo 26 en el texto de la Comisión de Trabajo.

Regula contravenciones de funcionarios públicos a las condiciones de reposo establecidas por una licencia médica y contempla sanciones disciplinarias que pueden llegar a la destitución.

**Resultado:** 127 sí / 6 no / 19 abstenciones.

**Coalición:** no alineados 22/0 a favor; oficialismo 66/0; oposición 39/6.

**`abs(spread_1d)`:** **1.5763**, sexto roll call más identificador del omnibus.

**Nivel:** **IV**.

El caso tiene un valor estadístico muy alto porque los seis votos negativos se encuentran políticamente concentrados. Pero no representa una fractura amplia de la Cámara sobre el principio general de sancionar abusos de licencias médicas. Es evidencia útil para localizar ciertos parlamentarios, no para nombrar el eje.

Fuente de votación: https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion=88936

---

## 6. El hallazgo metodológico más importante del ciclo

La comparación de tres roll calls consecutivos en el ranking del omnibus produce una prueba muy limpia:

| Vote ID | Contenido | Resultado | abs(spread D1) | Peso interpretativo |
|---|---|---:|---:|---|
| 88933 | reforma de financiamiento/certificación laboral | 58–94 | 1.5840 | I — conflicto sustantivo amplio |
| 88936 | licencias médicas y disciplina funcionaria | 127–6–19 | 1.5763 | IV — minoría delgada |
| 88935 | asignación de cupos de retiro | 138–14 | 1.5718 | IV — minoría delgada |

Los tres son casi igualmente fuertes para el algoritmo, pero **no son igualmente informativos para una interpretación política de D1**.

Esto confirma, dentro del propio omnibus, la regla desarrollada en la auditoría no-omnibus: un roll call puede tener gran capacidad de discriminación por al menos tres mecanismos distintos —división amplia, gradiente o minoría concentrada— y solo el primero o un gradiente sustantivamente coherente debe recibir alto peso narrativo para nombrar la dimensión.

La jerarquía I–IV, por tanto, no es decorativa: evita que la explicación pública de W-NOMINATE se convierta en una lista de las votaciones con mayor parámetro de discriminación.

---

## 7. Qué aporta F5 a la interpretación de D1

El ciclo laboral fortalece la lectura ya emergente de D1 como **continuo político-ideológico amplio asociado a izquierda–derecha**, pero aporta una razón diferente de F2/F3/F4.

En Sala Cuna y capacitación aparecen conflictos sobre:

- provisión e institucionalización de derechos o beneficios asociados al trabajo;
- quién financia y bajo qué arquitectura se organiza la capacitación y certificación laboral;
- alcance de la intervención pública y de obligaciones vinculadas al empleo.

Esos conflictos producen ordenamientos partidarios compatibles con los observados en otros dominios —regulación económica, ambiente, educación y seguridad— fuera de la Megareforma.

Esto debilita la hipótesis de que D1 sea únicamente:

- una dimensión de apoyo al Gobierno;
- una dimensión exclusivamente económica mercado–Estado;
- o un artefacto producido por un solo proyecto omnibus.

Al mismo tiempo, el tercer trámite de 21 de julio recuerda que **gobierno-oposición sí es un mecanismo real de estructuración**. 89485 y 89486, objetos normativos distintos, generan exactamente 75–70 y la misma coalición. Esa serialidad debe descontarse antes de hablar de evidencia sustantiva independiente.

---

## 8. Balance de hipótesis del ciclo 04

### H1 — D1 es puramente Gobierno versus oposición

**Se debilita como definición suficiente.**

88911 y 88933 son conflictos laborales sustantivos y tienen contenido interpretable. Sin embargo, 89485 y 89486 muestran que la condición de iniciativa prioritaria del Gobierno refuerza y serializa las coaliciones en tercer trámite.

### H2 — D1 refleja un continuo político-ideológico amplio asociado a izquierda–derecha

**Se fortalece.**

El dominio laboral reproduce una ordenación compatible con la encontrada en múltiples materias no-omnibus y añade casos de política social y capacitación a la convergencia multidominio.

### H3 — D1 es principalmente mercado versus Estado

**Recibe apoyo parcial, pero sigue siendo demasiado estrecha.**

Capacitación y Sala Cuna contienen componentes de regulación, financiamiento y obligaciones laborales, pero D1 también organiza conflictos de seguridad, educación, garantías, migración y memoria política que no pueden reducirse a esta dicotomía.

### H4 — la Megareforma crea artificialmente D1

**Se debilita nuevamente, aunque no se elimina el problema de dependencia.**

El omnibus contiene conflictos laborales reales y reconocibles, pero repite muchas veces las mismas coaliciones. La respuesta metodológica correcta es trabajar por cadenas normativas, no eliminar el proyecto entero ni contar todos sus roll calls por separado.

---

## 9. Regla de conteo derivada

Para la síntesis sustantiva de F5 se usarán tres tipos de unidades:

1. **`SALA_CUNA_UNIVERSAL_POLICY_CHAIN`** — una sola cadena, con 88911 como evidencia directa principal; 88910 procedimental y 89485 etapa posterior.
2. **`TRAINING_SYSTEM_REFORM_CHAIN`** — una sola familia de reforma del sistema de capacitación; 88933 como caso principal, 88932 y 89486 como contexto sustantivo complementario.
3. **Controles de consenso/minoría** — `PUBLIC_SERVICE_RETIREMENT_BONUS_CHAIN` y 88936 no se cuentan como confirmaciones de un clivaje laboral amplio; se conservan para explicar por qué discriminación matemática y importancia sustantiva son conceptos distintos.

---

## 10. Estado del ciclo

**Ciclo 04 — trabajo, empleo, Sala Cuna y función pública: CERRADO.**

### Hallazgo central

F5 contiene al menos dos conflictos laborales sustantivos de alta calidad —Sala Cuna Universal y reforma del sistema de capacitación— que fortalecen la interpretación multidominio de D1. Al mismo tiempo, retiro voluntario y licencias médicas demuestran que algunos de los roll calls más discriminantes del modelo pueden provenir de minorías muy pequeñas y no deben dominar la narrativa sustantiva.

### Siguiente ciclo lógico

**Ciclo 05 — residuales de alta discriminación y cierre del omnibus.**

El objetivo será recuperar los objetos todavía pendientes de mayor prioridad —especialmente 88938 y 88900—, revisar cualquier cadena incompleta de las familias ya abiertas, cuantificar cuánto del top identificador queda efectivamente explicado y producir un balance final del boletín 18216-05 antes de volver al gate general de interpretación de D1.
