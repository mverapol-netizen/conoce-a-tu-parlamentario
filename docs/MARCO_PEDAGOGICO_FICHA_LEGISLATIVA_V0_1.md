# Marco pedagógico de la ficha legislativa · v0.1

**Proyecto:** Conoce a tu parlamentario  
**Cámara:** Cámara de Diputadas y Diputados de Chile, período 2026–2030  
**Período observado:** desde el 11 de marzo de 2026  
**Estado:** diseño editorial y metodológico para revisión antes de implementación pública  

Este documento define cómo traducir a lenguaje público las capas de comportamiento legislativo construidas por el proyecto. Su objetivo no es simplificar los resultados hasta convertirlos en puntajes, sino hacerlos comprensibles sin perder las distinciones metodológicas que permiten interpretarlos correctamente.

La regla general es:

> **Cada gráfico debe responder una pregunta concreta, formular una conclusión limitada y ofrecer al usuario la posibilidad de reconstruir cómo se llegó a ella.**

La ficha no debe presentar una esencia del parlamentario. Debe mostrar distintas dimensiones observables de su actividad: participación, decisiones de voto, relación descriptiva con sus grupos parlamentarios, iniciativa legislativa, colaboración en mociones y, cuando supere todos los gates metodológicos, ubicación relativa en el principal patrón espacial de votación de la Cámara.

---

# 1. Arquitectura narrativa de la ficha

La ficha debe organizarse como una secuencia de preguntas comprensibles para una persona sin formación en ciencia política:

1. **¿Cuánto participa en las votaciones de Sala?**
2. **¿Cómo se distribuyen sus decisiones cuando participa?**
3. **¿Con qué frecuencia vota igual que la posición predominante de su partido y de su bancada?**
4. **¿Qué proyectos ha presentado y cómo los presenta?**
5. **¿Con quién presenta proyectos?**
6. **¿En qué materias aparecen sus iniciativas?** — cuando la clasificación temática supere su validación externa.
7. **¿Dónde se ubica su patrón general de votación respecto del resto de la Cámara?** — únicamente cuando la estimación espacial supere los gates de publicación.
8. **¿Qué votaciones concretas ayudan a entender esa ubicación?** — como evidencia explicativa del modelo espacial.
9. **¿Cómo construimos estos datos y estas interpretaciones?**

No todas estas capas tienen actualmente el mismo estado de madurez. La ficha puede diseñarse completa desde ahora, pero cada módulo debe incorporar un `publication_status` explícito y no activarse públicamente antes de cumplir sus requisitos.

---

# 2. Una plantilla pedagógica común para todos los gráficos

Cada módulo gráfico debe tener cinco niveles de lectura.

## Nivel 1 — La frase principal

Una frase breve que responda directamente la pregunta del gráfico. Debe describir el resultado sin evaluación normativa.

Ejemplos válidos:

- “Participó con una decisión registrada en X% de las votaciones nominales de Sala del período observado.”
- “Coincidió con la posición más frecuente de su bancada en X de Y votaciones comparables.”
- “Ha presentado X mociones junto a Y coautores distintos.”

Ejemplos que deben evitarse:

- “Es uno de los diputados más trabajadores.”
- “Es disciplinado.”
- “Es rebelde.”
- “Es moderado.”
- “Es extremo.”

## Nivel 2 — Cómo leer este gráfico

Dos o tres frases visibles junto al gráfico que expliquen qué representa cada elemento visual y cuál es el denominador.

## Nivel 3 — Qué significa y qué no significa

Un desplegable debe distinguir explícitamente ambas cosas. La ausencia de esta sección vuelve demasiado fácil convertir una estadística descriptiva en un juicio sobre la persona.

## Nivel 4 — Cómo lo calculamos

Explicación metodológica resumida, con variables, universo y exclusiones principales.

## Nivel 5 — Ver evidencia y metodología

Enlace a:

- datos o votaciones que sostienen el indicador;
- fuente institucional pertinente;
- fecha de corte;
- versión del método;
- explicación completa del proyecto.

La progresividad es importante: el usuario casual no necesita leer el método completo, pero el usuario que quiera auditar una afirmación debe poder hacerlo.

---

# 3. Módulo A — Participación en votaciones de Sala

## Pregunta pública

**¿Cuánto participa en las votaciones nominales de Sala?**

## Visualización recomendada

Una barra horizontal de composición con cinco estados separados:

- Afirmativo;
- En contra;
- Abstención;
- No vota;
- Dispensado.

Sobre la barra se muestra como cifra principal la **participación sustantiva**:

`(Afirmativo + En contra + Abstención) / oportunidades observadas de votación`.

Debe mostrarse también el número absoluto de oportunidades observadas.

## Texto público propuesto — En una frase

> **Participación en votaciones:** en el período observado, [Nombre] registró una decisión —a favor, en contra o abstención— en **[X]%** de las votaciones nominales de Sala en las que figura en nuestra base.

## Cómo leerlo

> La barra separa las distintas opciones que registra oficialmente la Cámara. Una abstención es una decisión parlamentaria registrada y se distingue de “No vota”. Las dispensas también aparecen por separado.

## Qué significa

Este indicador describe la participación observada **en votaciones nominales de Sala**. Permite saber en cuántas de esas oportunidades el parlamentario emitió una decisión sustantiva y cómo se distribuyeron esas decisiones.

## Qué no significa

- No es una medición completa de asistencia al Congreso.
- No mide trabajo en comisiones, territorio, fiscalización, elaboración de indicaciones ni otras actividades parlamentarias.
- `No vota` no significa automáticamente ausencia injustificada.
- `Abstención` no equivale a ausencia ni a voto en contra.
- Una mayor proporción de afirmativos no implica mayor apoyo al Gobierno ni mayor productividad.

## Cómo lo calculamos

El proyecto conserva los estados oficiales de cada votación nominal de Sala. Para este indicador se consideran decisiones sustantivas `Afirmativo`, `En Contra` y `Abstención`. `No Vota` y `Dispensado` permanecen visibles, pero no se recodifican como decisiones sustantivas.

## Estado

**APTO PARA IMPLEMENTACIÓN PÚBLICA**, sujeto a revisión final de denominadores para incorporaciones o salidas de la Cámara durante el período.

---

# 4. Módulo B — Cómo se distribuyen sus decisiones de voto

## Pregunta pública

**Cuando participa, ¿cómo vota?**

Este módulo puede integrarse visualmente con el anterior o aparecer inmediatamente debajo.

## Visualización recomendada

Barra de composición o pequeñas barras con:

- % afirmativo;
- % en contra;
- % abstención;

calculados únicamente sobre decisiones sustantivas.

## Texto público propuesto

> Entre las votaciones en que registró una decisión sustantiva, [Nombre] votó **a favor en [X]%**, **en contra en [Y]%** y **se abstuvo en [Z]%**.

## Interpretación permitida

Describe la distribución formal de sus decisiones. Puede utilizarse para contextualizar otros indicadores y abrir el listado de votaciones correspondiente.

## Interpretaciones prohibidas

No debe presentarse una alta proporción de afirmativos como “aprobador”, “oficialista” o “productivo”. La Cámara vota una mezcla de proyectos, artículos, indicaciones, enmiendas, vetos y decisiones procedimentales cuya orientación política no es constante.

## Estado

**APTO PARA IMPLEMENTACIÓN PÚBLICA.**

---

# 5. Módulo C — Coincidencia con partido y bancada

## Pregunta pública

**¿Con qué frecuencia vota igual que la posición predominante de su grupo?**

## Nombre público recomendado

**Coincidencia con su partido y bancada**

No usar como título principal:

- disciplina;
- lealtad;
- obediencia;
- rebeldía.

## Visualización recomendada

Dos barras o dos indicadores paralelos:

- **Partido**: X de Y votaciones comparables;
- **Bancada / Comité Parlamentario**: X de Y votaciones comparables.

La cifra porcentual nunca debe mostrarse sin el denominador `X de Y`.

La vista pública principal debería excluir votaciones casi unánimes. La opción candidata es usar, como default, votaciones donde al menos **10% de los votos binarios de la Cámara estuvieron en la posición minoritaria**. Antes de implementación pública este umbral debe quedar formalmente aprobado. El usuario puede disponer de una explicación o vista de sensibilidad con 5%, 10%, 20% y todas las votaciones comparables.

## Texto público propuesto

> En votaciones con una diferencia sustantiva de posiciones en la Cámara, [Nombre] coincidió con la opción más frecuente de su **partido en [X] de [Y] casos ([P]%)** y con la de su **bancada en [A] de [B] casos ([Q]%)**.

Si el parlamentario es independiente, debe omitirse la comparación partidaria cuando no exista un partido válido para la fecha del voto y privilegiarse la bancada/comité.

## Cómo leerlo

> Para cada votación comparamos la decisión del parlamentario con la opción más frecuente entre los integrantes de su grupo en esa misma votación. Solo hacemos la comparación cuando el grupo tiene una posición modal única y suficiente información para definirla.

## Qué significa

Mide **coincidencia descriptiva observada** entre las decisiones individuales y la posición más frecuente del grupo durante el período.

## Qué no significa

- No demuestra disciplina partidaria.
- No permite saber si existió una orden de partido.
- No permite distinguir convicción compartida, coordinación, negociación, estrategia o presión.
- Una divergencia no equivale automáticamente a una “rebelión”.
- `No Vota` y `Dispensado` no se cuentan como desacuerdo.
- El resultado puede cambiar según cuán competitivas sean las votaciones incluidas; por eso se mantiene análisis de sensibilidad.

## Decisión metodológica pendiente

Aprobar el umbral de competitividad pública. Los cálculos ya existen para 0%, 5%, 10% y 20% de minoría binaria de Cámara.

## Estado

**CASI APTO / CONDICIONADO A DECISIÓN DE UMBRAL Y COPY FINAL.**

---

# 6. Módulo D — Iniciativa legislativa

## Pregunta pública

**¿Qué proyectos ha presentado?**

## Visualización recomendada

Un bloque de cifras acompañado de una pequeña composición:

- mociones en las que figura como autor/a;
- mociones presentadas con otros autores;
- mociones presentadas en solitario;
- acceso al listado completo de boletines.

Puede agregarse una serie temporal acumulativa si con el avance de la legislatura aporta información útil.

## Texto público propuesto

> Desde el inicio del período observado, [Nombre] figura como autor/a de **[X] mociones**. De ellas, **[Y]** fueron presentadas junto a otros parlamentarios y **[Z]** en forma individual.

## Qué significa

Describe actividad de **iniciativa parlamentaria formal** registrada por la Cámara.

## Qué no significa

- Número de mociones no equivale a calidad legislativa.
- Número de mociones no equivale a leyes aprobadas.
- Ser coautor no permite inferir cuánto redactó o negoció cada persona.
- No incluye mensajes del Ejecutivo como si hubieran sido escritos por diputados.
- No debe construirse un ranking normativo de “mejor legislador” solo a partir de cantidad de mociones.

## Estado

**APTO PARA IMPLEMENTACIÓN PÚBLICA.**

---

# 7. Módulo E — Red de coautoría

## Pregunta pública

**¿Con quién presenta proyectos?**

## Visualización recomendada

Una red egocentrada alrededor del parlamentario seleccionado:

- centro: parlamentario de la ficha;
- nodos vecinos: coautores;
- grosor o intensidad de vínculo: número de mociones compartidas;
- filtro opcional por período o, después de validar temas, por materia.

Debe acompañarse de una lista accesible de los principales vínculos, porque la red por sí sola puede ser difícil de leer en celular y para lectores con necesidades de accesibilidad.

## Texto público propuesto

> Esta red conecta a [Nombre] con los parlamentarios que aparecen junto a él/ella como autores de una misma moción. Un vínculo más fuerte indica que han compartido autoría en más proyectos.

## Qué significa

Muestra **colaboración legislativa formal en la presentación de mociones**.

## Qué no significa

- No representa amistad personal.
- No equivale a coalición electoral.
- No prueba cercanía ideológica.
- No mide similitud de voto.
- No significa que todos los coautores estén de acuerdo con cada detalle posterior de la tramitación.
- No implica que una relación con muchos proyectos sea más importante políticamente que otra con pocos.

## Fuente y construcción

La red se deriva exclusivamente de `bill_authors.csv`. Una pareja se conecta cuando ambos aparecen como autores de la misma moción. Una relación repetida dentro del mismo boletín se cuenta una sola vez para ese proyecto. La red no modifica los datos primarios.

## Estado

**APTO PARA IMPLEMENTACIÓN PÚBLICA**, con revisión UX de densidad y del tratamiento de coautorías intercámara.

---

# 8. Módulo F — Perfil temático de las iniciativas

## Pregunta pública

**¿Sobre qué materias ha presentado proyectos?**

## Visualización recomendada

Barras horizontales con el número de mociones del parlamentario por **familia temática**, mostrando también el total utilizado como denominador.

No mezclar en un mismo gráfico:

- temas de proyectos que el parlamentario presenta;
- temas de proyectos sobre los que simplemente vota.

Son dos universos distintos y deben comunicarse separadamente si ambos llegan a publicarse.

## Texto público propuesto

> Esta distribución muestra las materias principales de las mociones en las que [Nombre] figura como autor/a durante el período observado.

## Qué significa

Permite describir la **composición temática de su producción de iniciativas**.

## Qué no significa

- No permite afirmar que estos sean necesariamente sus únicos intereses o prioridades políticas.
- Una iniciativa puede ser multidimensional.
- El número de proyectos no mide importancia, esfuerzo, impacto ni éxito.
- Las familias temáticas son una clasificación analítica del proyecto y no deben presentarse como si fueran una etiqueta oficial de la Cámara.

## Transparencia metodológica obligatoria

La clasificación utiliza primero señales institucionales —destinación, comisión de origen, trayectoria de comisiones, materias oficiales y ministerios— y después texto y revisión semántica. Partido, bancada y autor no se utilizan para decidir el tema.

## Estado

**DISEÑAR AHORA, NO PUBLICAR COMO MÉTRICA VALIDADA HASTA CERRAR LA VALIDACIÓN EXTERNA/FORMAL DE LA TAXONOMÍA.**

---

# 9. Módulo G — Patrón general de votación de la Cámara (D1)

## Pregunta pública

**¿Dónde se ubica su patrón de votación respecto del resto de la Cámara?**

## Nombre recomendado del módulo

Mientras el gate final no esté cerrado:

**Patrón general de votación — diseño en validación**

Si los gates finales confirman la interpretación sustantiva, la presentación pública puede usar:

**Ubicación relativa en el principal eje de votación de la Cámara**

con una explicación visible:

> El eje se obtiene de las votaciones nominales y resume el principal patrón de diferencias entre parlamentarios. Nuestra auditoría encuentra que este patrón está fuertemente asociado a la distinción política izquierda–derecha, pero no equivale mecánicamente a partido, Gobierno/oposición ni a una sola materia legislativa.

## Visualización pública recomendada

No publicar una tabla ordenada tipo ranking “1 al 154”.

Preferir una **franja horizontal de la Cámara**:

- distribución de todas las posiciones estimadas;
- punto destacado del parlamentario;
- intervalo o banda de incertidumbre/sensibilidad;
- opcionalmente distribuciones resumidas de partidos o bancadas como contexto, no como variables que determinen el modelo.

Si finalmente se usan rótulos `izquierda ↔ derecha`, la transformación del signo debe estar registrada y separada de la coordenada cruda.

## Texto público propuesto — versión final condicionada

> A partir de muchas votaciones nominales de Sala, estimamos qué parlamentarios tienden a tomar decisiones semejantes y cuáles se separan de ese patrón. La posición de [Nombre] aparece aquí **relativa al resto de esta Cámara y durante este período**, no como una puntuación ideológica absoluta.

## Qué significa políticamente según la auditoría sustantiva actual

La evidencia acumulada indica que D1 sintetiza un **continuo político-ideológico multidominio fuertemente asociado con izquierda–derecha**. Esta conclusión no surge solamente de observar los nombres de los partidos. Se obtiene porque una dirección semejante reaparece en conflictos legislativos materialmente distintos:

- regulación económica, laboral y ambiental;
- protección social y obligaciones regulatorias;
- educación, selección y autonomía de establecimientos;
- seguridad, penalidad, control y garantías;
- migración;
- tributación, inversión y contratación;
- determinadas controversias simbólicas y de memoria política.

También aparecen gradientes y fracturas internas: centroizquierda puede acompañar a la derecha en materias de seguridad o regulación; RN/UDI pueden separarse de Republicanos/PNL; y fuerzas no alineadas pueden converger con distintos polos según la materia.

Por eso el eje no debe explicarse como dos bloques perfectamente homogéneos.

## Qué alternativas auditamos

### “Es solo Gobierno contra oposición”

**Insuficiente.** Esa lógica estructura muchas votaciones —especialmente partes de la agenda prioritaria del Ejecutivo y secuencias del tercer trámite—, pero no explica los múltiples casos en que partidos fuera del Gobierno convergen con su mismo polo ideológico, ni las fracturas dentro de Gobierno y oposición.

### “Es solamente mercado contra Estado”

**Componente importante, pero demasiado estrecho.** Explica buena parte de los conflictos regulatorios, tributarios, ambientales y laborales, pero no seguridad, migración, educación, garantías ni memoria política.

### “Son simplemente dos bloques partidarios rígidos”

**Rechazado por la evidencia.** Existen demasiadas divergencias dentro de ambos espacios para tratar la coordenada como una codificación de partido.

### “La dimensión aparece por unas pocas votaciones extremas”

**Fuertemente debilitado.** La geometría permanece casi intacta al elevar el umbral mínimo del lado minoritario de 2,5% a 5% y 10%; además, al usar 10% desaparecen preferentemente votaciones de minorías muy delgadas mientras sobreviven los principales conflictos sustantivos.

### “La Megareforma 18216-05 produce artificialmente todo el eje”

**Fuertemente debilitado.** Ese proyecto concentra una proporción muy alta de roll calls y por eso recibió un protocolo especial. Después de agrupar cadenas normativas y descontar serialidad, los mismos tipos de conflicto reaparecen en numerosos proyectos independientes.

## Qué no significa la ubicación individual

- No es “porcentaje de izquierdismo” o “porcentaje de derechismo”.
- No es una medida moral.
- No equivale a moderación o extremismo normativo.
- No describe todas las posiciones programáticas de la persona.
- No permite inferir motivos internos detrás de cada voto.
- No debe compararse directamente con una coordenada de otra legislatura estimada separadamente.
- No es necesariamente fija durante todo el mandato.
- Un punto muy cercano a otro indica similitud relativa de comportamiento en las votaciones utilizadas, no identidad política completa.

## Incertidumbre

La banda alrededor de cada posición debe explicarse en lenguaje sencillo:

> **La franja muestra cuánto puede moverse la ubicación estimada cuando cambia la composición de proyectos utilizada para reconstruir el patrón general de votación. Una franja más amplia indica que tenemos menos precisión para ubicar a esa persona en un punto exacto.**

El diseño debe evitar que un punto estimado visualmente tape su incertidumbre.

## Estado

**DISEÑO PEDAGÓGICO APROBABLE; PUBLICACIÓN DE LA COORDENADA Y DEL RÓTULO SUSTANTIVO CONDICIONADA A LOS GATES RESTANTES DEL CONTRATO MULTIMÉTODO.**

---

# 10. Módulo H — Votaciones que ayudan a entender la ubicación espacial

Este módulo es indispensable si D1 llega a publicarse. Una coordenada sin evidencia concreta corre el riesgo de parecer una etiqueta opaca producida por un algoritmo.

## Pregunta pública

**¿Qué decisiones legislativas ayudan a explicar esta ubicación?**

## Diseño recomendado

Entre tres y seis tarjetas de votaciones, seleccionadas mediante reglas deterministas y auditables.

Cada tarjeta debe mostrar:

- fecha;
- proyecto y boletín;
- objeto exacto sometido a votación —artículo, indicación, enmienda, veto u otra unidad—;
- voto del parlamentario;
- resultado de la Cámara;
- breve explicación de qué estaba en disputa;
- por qué esa votación es informativa para el eje;
- enlace a la fuente oficial.

## Regla de selección pública

Para evitar *cherry-picking*, una votación pedagógica debe cumplir preferentemente:

1. el parlamentario emitió un voto binario observable;
2. contenido normativo exacto cerrado;
3. evidencia sustantiva Nivel I o II;
4. diversidad temática respecto de las demás tarjetas;
5. máximo una tarjeta por `policy_chain` o conflicto sustantivo repetido;
6. capacidad discriminante relevante en el modelo;
7. evitar como ejemplos principales votaciones cuyo poder estadístico proviene solamente de una minoría minúscula;
8. evitar como ejemplos principales decisiones puramente procedimentales o de fiscalización si no se explica expresamente ese carácter.

## Texto introductorio propuesto

> Ninguna votación por sí sola determina la ubicación de un parlamentario. Estas decisiones se muestran porque, tomadas junto con muchas otras, ayudan a entender los conflictos que organizan el principal patrón de votación de la Cámara.

## Lección de la auditoría

El `spread` de W-NOMINATE no debe convertirse automáticamente en un ranking de “votaciones más ideológicas”. Durante la auditoría encontramos al menos cuatro mecanismos capaces de producir alta discriminación matemática:

1. división sustantiva amplia;
2. gradiente político dentro de uno o ambos bloques;
3. minoría pequeña y concentrada;
4. votación procedimental o de fiscalización con fuerte lógica Gobierno–oposición.

Solo los dos primeros, y ciertos casos complementarios cuidadosamente auditados, deben ocupar el centro de la explicación pública del eje.

## Estado

**DISEÑAR AHORA; ACTIVAR JUNTO CON D1.**

---

# 11. Módulos que NO deben publicarse todavía

## Segunda dimensión W-NOMINATE (D2)

No publicar. Su estabilidad es claramente menor frente al balanceo por proyecto y todavía no existe una interpretación sustantiva común suficientemente robusta. El hecho de que un modelo 2D mejore el ajuste no basta para convertir D2 en una dimensión política pública.

## “Disciplina partidaria”

No publicar con ese nombre a partir de la coincidencia modal. El indicador actual solo establece coincidencia descriptiva.

## “Rebeldía”

No inferirla de una divergencia individual frente a partido o bancada.

## “Apoyo al Gobierno”

No construirlo contando votos afirmativos en proyectos originados por el Ejecutivo. Un indicador válido necesitará identificar la posición gubernamental sobre cada unidad concreta sometida a votación.

## B-Call D2 como “disciplina”

No. Si posteriormente se implementa y valida, debe describirse inicialmente como **variabilidad del comportamiento B-Call**.

## Rankings normativos

No producir un índice agregado que mezcle participación, coincidencia, posición espacial, mociones y coautoría para declarar quién es “mejor”, “peor”, “más trabajador”, “más independiente”, “más moderado” o equivalentes.

---

# 12. “Más sobre este proyecto” — explicación pública paso a paso

La metodología debe tener una página o panel propio escrito como una cadena transparente y comprensible.

## Paso 1 — Identificamos quién integra la Cámara

Partimos de fuentes oficiales para identificar a los 155 integrantes de la Cámara, sus distritos, partidos, bancadas/comités y datos institucionales.

## Paso 2 — Seguimos las votaciones nominales de Sala

Solo incorporamos una votación al universo principal cuando verificamos institucionalmente que corresponde a Sala y podemos enlazarla con su proyecto y con el detalle nominal de cada parlamentario.

## Paso 3 — Conservamos la decisión original

No transformamos los datos primarios para que encajen en una interpretación. `Afirmativo`, `En Contra`, `Abstención`, `No Vota` y `Dispensado` permanecen separados.

## Paso 4 — Reconstruimos el contexto político en la fecha del voto

El partido o bancada actual no se usa retroactivamente para toda la serie. Cuando existen cambios de afiliación, las votaciones se enlazan con la pertenencia correspondiente al momento de la decisión.

## Paso 5 — Vinculamos proyectos, autorías y trayectoria legislativa

La base permite seguir `proyecto → autoría → tramitación → votación de Sala → voto nominal` sin reemplazar la información oficial por indicadores derivados.

## Paso 6 — Construimos indicadores descriptivos

A partir de esas capas calculamos participación, distribución de votos, coincidencia modal y redes de coautoría. Cada indicador tiene su propio universo y no se interpreta como una medida de otra cosa.

## Paso 7 — Para el modelo espacial usamos solamente Sí/No

W-NOMINATE y los modelos espaciales principales utilizan únicamente `Afirmativo` y `En Contra`. Abstenciones, no votos y dispensas se consideran información ausente para esa estimación, no votos negativos.

## Paso 8 — Exigimos que una votación tenga desacuerdo suficiente

La especificación base conserva votaciones cuyo lado minoritario representa al menos 2,5% de los votos binarios y realiza pruebas más exigentes con 5% y 10%. La interpretación D1 permanece extraordinariamente estable bajo esos cambios.

## Paso 9 — Evitamos que un solo proyecto defina la historia

Auditamos concentración por boletín, deduplicación y especificaciones que limitan la cantidad de roll calls aportados por un proyecto. La Megareforma 18216-05 recibió tratamiento especial porque concentra muchas decisiones.

## Paso 10 — En proyectos ómnibus seguimos conflictos, no solo IDs de votación

Una misma política puede votarse como indicación, artículo, enmienda y veto. Para interpretar el eje agrupamos esas etapas en `policy chains` y no contamos cada roll call como una confirmación política independiente.

## Paso 11 — Auditamos proyectos distintos y buscamos contraejemplos

Seleccionamos una muestra transversal de treinta proyectos no ómnibus y revisamos qué se votó realmente. La búsqueda fue falsacionista: además de casos compatibles con la hipótesis principal, registramos fracturas internas, minorías específicas y votaciones donde Gobierno/oposición explicaba mejor el patrón.

## Paso 12 — Auditamos la Megareforma por familias sustantivas

Separamos crédito, impuestos, inversión, contratación, ambiente, trabajo, capacitación, protección social y otras familias, distinguiendo contenido sustantivo, procedimiento, serialidad y minorías delgadas.

## Paso 13 — Comparamos interpretaciones alternativas

La hipótesis de una dimensión político-ideológica amplia asociada a izquierda–derecha sobrevivió mejor que alternativas más estrechas como Gobierno/oposición, mercado/Estado o dos bloques rígidos. Estas alternativas explican partes del comportamiento, pero no el conjunto de dominios observados.

## Paso 14 — Medimos incertidumbre y robustez

La ubicación no se considera un punto perfectamente conocido. Utilizamos sensibilidad a decisiones de diseño y remuestreo agrupado por proyecto para estudiar cuánto puede cambiar cada posición.

## Paso 15 — Comparamos métodos antes de publicar

El contrato del proyecto exige contrastar W-NOMINATE con un IRT bayesiano 2PL y Optimal Classification, además de cerrar la estabilidad temporal. El rótulo público final de D1 debe depender de esa convergencia y no de un solo estimador.

## Paso 16 — Versionamos y fechamos los resultados

Cada gráfico debe mostrar claramente el período observado y la fecha de corte. Las cifras son una fotografía acumulativa del comportamiento legislativo hasta esa fecha y cambiarán con nuevas votaciones.

---

# 13. Jerarquía visual recomendada para una ficha individual

Una primera versión pública debería ordenar los módulos así:

### Capa 1 — actividad observable

1. Participación en votaciones.
2. Distribución de decisiones.
3. Mociones presentadas.

### Capa 2 — relaciones institucionales

4. Coincidencia con partido/bancada.
5. Red de coautorías.

### Capa 3 — contenido político

6. Temas de las iniciativas, cuando la taxonomía esté validada.
7. Patrón espacial D1, cuando supere los gates.
8. Votaciones que explican D1.

### Capa 4 — transparencia

9. Ver todas las votaciones.
10. Ver todas las mociones.
11. Fuentes y fecha de actualización.
12. Más sobre este proyecto / metodología completa.

Esta secuencia evita que la primera impresión de una ficha sea una etiqueta ideológica. Primero se muestra qué hizo la persona; luego con quién se relaciona; finalmente se ofrece una interpretación más compleja del comportamiento de voto.

---

# 14. Reglas editoriales transversales

1. **Denominadores visibles.** Un porcentaje sin `n` puede engañar.
2. **Fecha de corte visible.** Todo resultado es temporal.
3. **Comparaciones prudentes.** Si se compara con Cámara, partido o distrito, mostrar distribución y no categorías morales.
4. **Datos ausentes no se imputan silenciosamente.** Explicar cuando no existe información suficiente.
5. **Separar hecho e inferencia.** Partido, voto y autoría son hechos institucionales; tema y posición espacial son capas analíticas.
6. **No convertir correlación en causalidad.** Asociación con partido o bancada no prueba disciplina.
7. **No ocultar sensibilidad.** Cuando una conclusión depende del universo utilizado, debe decirse.
8. **Evitar rankings innecesarios.** Priorizar posición relativa y distribución.
9. **Toda explicación compleja debe poder aterrizar en evidencia concreta.** Especialmente D1.
10. **Las advertencias no deben estar escondidas solo en una página metodológica.** La principal limitación de cada gráfico debe aparecer junto al gráfico.

---

# 15. Estado de publicación por módulo

| Módulo | Diseño | Datos | Interpretación | Estado público |
|---|---|---|---|---|
| Participación de Sala | listo para diseñar | disponible | cerrada | **publicable** |
| Distribución A favor/En contra/Abstención | listo para diseñar | disponible | cerrada | **publicable** |
| Coincidencia partido/bancada | listo para diseñar | disponible | cerrada como coincidencia modal | **condicionado al umbral público** |
| Mociones / iniciativa legislativa | listo para diseñar | disponible | cerrada | **publicable** |
| Red de coautoría | listo para diseñar | disponible | cerrada | **publicable con revisión UX** |
| Perfil temático | listo para diseñar | disponible como clasificación derivada | método definido | **esperar validación externa** |
| D1 | diseño y copy definidos | disponible | sustantivamente muy avanzada | **esperar gates multimétodo/temporales** |
| Evidencia concreta de D1 | diseño definido | auditorías disponibles | jerarquía I–IV definida | **activar junto con D1** |
| D2 | no prioritario | experimental | no cerrada | **no publicar** |
| Disciplina/rebeldía | no | indicador causal no construido | no autorizada | **no publicar** |
| Apoyo al Gobierno | no | posición gubernamental por roll call pendiente | no autorizada | **no publicar** |

---

# 16. Principio editorial final

La promesa pública de la ficha no debe ser “decirte quién es ideológicamente un parlamentario” ni “ponerle una nota”. Debe ser más modesta y, por eso mismo, más defendible:

> **Mostrar qué decisiones ha tomado un representante, cómo se relacionan esas decisiones con otros actores de la Cámara y qué patrones podemos reconstruir a partir de ellas, dejando visible tanto la evidencia como los límites de la interpretación.**

Esa formulación permite que el proyecto sea pedagógico sin fingir una certeza que los datos no ofrecen y, al mismo tiempo, permite aprovechar la profundidad de la investigación acumulada detrás de cada visualización.
