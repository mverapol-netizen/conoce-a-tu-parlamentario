# Auditoría histórico-política transversal de D1 — Bloque 01

> Documento interno de investigación. No usar todavía como etiqueta pública de D1. Corte de datos: 2 de septiembre de 2026. Se excluye deliberadamente el boletín 18216-05 (Megareforma), que tiene protocolo y subcorpus propios.

## Objetivo

Auditar los primeros cinco casos de la muestra `d1_top30_non_omnibus_bill_diverse.csv`. La pregunta no es solo si las votaciones separan matemáticamente a los diputados, sino **qué conflicto político concreto producen y qué hipótesis sobre D1 apoyan o debilitan**.

Para evitar sobreinterpretación, cada caso se clasifica además por forma del clivaje observado:

- **A — bipolar/de bloques:** dos coaliciones amplias y contrapuestas;
- **B — gradiente/intra-bloque:** el conflicto sigue una dirección reconocible pero rompe alguno de los grandes bloques;
- **C — actor específico:** la capacidad discriminante proviene en gran medida de una fuerza o subgrupo particular;
- **D — contenido exacto pendiente:** el patrón de votos está identificado, pero falta recuperar el texto exacto sometido a votación para asignarle significado sustantivo.

## Caso 1 — votación 89937 / boletín 15295-07 / 1 septiembre 2026

**Proyecto:** modifica el DL 321 para restringir requisitos de acceso a libertad condicional.

**Patrón observado:** 102 afirmativos, 12 en contra, 30 abstenciones y 11 no votos. En la codificación temporal: oficialismo 62/0 a favor; no alineados 13/0; oposición 27/12. Frente Amplio concentra el rechazo (0/11 en las observaciones binarias del archivo), mientras PS y DC apoyan mayoritariamente.

**Contexto sustantivo recuperado:** el proyecto busca elevar la fracción de pena efectivamente cumplida exigida para optar a libertad condicional, con umbrales especialmente altos para ciertos delitos contra funcionarios públicos, e incorpora participación de víctimas y obligaciones de información. El debate público contrapone una lógica de mayor cumplimiento efectivo de penas con objeciones sobre reinserción, evidencia de reincidencia y sobrepoblación penal.

**Estado de fuente:** el contenido general del proyecto y el resultado del roll call están corroborados; la página primaria de detalle de la votación 89937 no respondió durante esta auditoría. Antes de cerrar la interpretación debe confirmarse si 89937 corresponde a votación general o a un objeto específico del articulado.

**Tipo:** **B + D** — gradiente sobre penalidad/garantías, con objeto exacto de la votación aún pendiente.

**Lectura provisional:** apoya con fuerza que **orden, penalidad y garantías** forman parte de D1, pero no reproduce una dicotomía completa oficialismo/oposición ni una izquierda/derecha binaria: sectores de centroizquierda acompañan la posición punitiva y FA aparece como el principal polo contrario.

## Caso 2 — votación 89113 / boletín 15936-18 / 10 junio 2026

**Proyecto:** prohibición/restricción de porte y tenencia de armas para personas vinculadas a violencia intrafamiliar.

**Objeto exacto recuperado:** en tercer trámite se votó separadamente la nueva disposición incorporada por el Senado (artículo 5). La norma modifica la legislación de violencia contra las mujeres y refuerza medidas cautelares relativas a armas de fuego cuando existe riesgo para la víctima; también contempla actuación frente a armas no registradas.

**Patrón observado:** 106 afirmativos, 5 en contra, 32 abstenciones y 12 no votos. En votos binarios, oficialismo 31/0 y oposición 60/0 apoyan. La anomalía principal es el PNL: 1 a favor y 5 en contra. El resto de los partidos relevantes vota binariamente a favor.

**Tipo:** **C — actor específico.**

**Lectura provisional:** este caso es muy útil precisamente porque **no** confirma un clivaje de bloques. Su alta fuerza discriminante parece derivar de una resistencia muy concentrada en el PNL frente a la restricción de armas, mientras el resto de la Cámara converge. Debe incorporarse como caso de control contra una lectura demasiado automática de `abs(spread_1d)`: una votación muy informativa para la estimación no necesariamente es una gran batalla izquierda–derecha de 70 contra 70.

**Implicación:** puede reflejar una posición libertaria/civil sobre propiedad y armas dentro de la derecha, pero esa interpretación requiere recurrencia en otros casos PNL antes de elevarla a componente sustantivo.

## Caso 3 — votación 88870 / boletín 18155-25 / 13 mayo 2026

**Proyecto:** nuevas agravantes para delitos cometidos contra la comunidad educativa o en recintos educacionales.

**Contexto:** mensaje del Ejecutivo ingresado en abril de 2026, tramitado con urgencia y discutido junto con autoridades de Seguridad/Justicia, Defensoría de la Niñez, defensa penal y especialistas. La finalidad general es endurecer consecuencias penales por ataques a integrantes de comunidades educativas y determinados delitos en establecimientos.

**Patrón observado:** 104 afirmativos, 16 en contra, 22 abstenciones y 13 no votos. Oficialismo 62/0; no alineados 19/0; oposición 23/16. PC registra 0/8; el resto de la centroizquierda muestra apoyo o división.

**Estado del objeto:** el registro de la Cámara consultado no identifica un artículo separado para 88870, mientras la votación siguiente sí registra un numeral separado. La evidencia disponible es compatible con que 88870 sea la votación general, aunque debe conservarse esa calificación con cautela hasta cerrar la ficha primaria completa.

**Tipo:** **B — gradiente/intra-bloque.**

**Lectura provisional:** refuerza la familia **orden/penalidad**, pero vuelve a mostrar que D1 no es simplemente oficialismo contra oposición. El rechazo se concentra en el PC y parte de la izquierda, mientras DC y otros sectores opositores acompañan el proyecto. Es compatible con una dimensión izquierda–derecha amplia entendida como gradiente, no como dos bloques sin excepciones.

## Caso 4 — votación 88647 / boletín 17522-12 / 15 abril 2026

**Proyecto:** aumenta sanciones por incineración ilegal de basura e incorpora medidas de educación ambiental y manejo de residuos.

**Objeto:** votación general del proyecto en Sala, corroborada con la ficha oficial de la Cámara.

**Contenido:** el proyecto persigue la quema ilegal de basura en espacios urbanos, naturales y protegidos, eleva consecuencias administrativas/penales en determinados casos y contempla responsabilidades y educación municipal sobre residuos y reciclaje.

**Patrón observado:** 77 afirmativos, 49 en contra, 12 abstenciones, 15 no votos y 2 dispensados. Oposición 61/0 a favor; oficialismo 4/42; no alineados 12/7. FA, PC, PS, DC y PPD apoyan; PNL, Republicanos y UDI concentran el rechazo; PDG apoya.

**Tipo:** **A — bipolar/de bloques**, con actores intermedios que no siguen mecánicamente el alineamiento gubernamental.

**Lectura provisional:** es hasta ahora el caso más limpio del bloque para una interpretación de D1 como dimensión político-ideológica amplia. Activa una oposición sobre **regulación ambiental e intervención estatal**, que coincide ampliamente con izquierda/derecha, pero no se agota en gobierno/oposición: PDG acompaña la regulación y el PNL se ubica con los partidos de derecha pese a no integrar formalmente el Gobierno.

## Caso 5 — votación 89389 / boletín 16836-06 / 13 julio 2026

**Proyecto:** reforma de la Ley 21.325 para perfeccionar el procedimiento de expulsión administrativa.

**Objeto exacto identificado:** en tercer trámite se votó una enmienda del Senado que eliminaba la letra a) del número 6, que pasó a ser número 8, del artículo 1. La votación separada fue solicitada por el diputado Benjamín Moreno. Resultado oficial: 51 a favor, 69 en contra y 19 abstenciones; la enmienda fue rechazada.

**Patrón observado:** separación excepcionalmente nítida: oposición 51/0 a favor; oficialismo 0/63; no alineados 0/6. FA, PC, DC, PPD y PS votan afirmativamente en las observaciones binarias; Republicanos, PNL, RN, UDI y otras fuerzas del polo contrario votan en contra.

**Estado sustantivo:** todavía falta recuperar la página 26 del texto comparado para determinar **qué efecto normativo concreto tenía la letra a) eliminada**. Sin ese texto no debe afirmarse si votar a favor de la enmienda significaba ampliar expulsiones, introducir garantías, restringir facultades u otra cosa.

**Tipo:** **A + D** — clivaje de bloques extremadamente claro, dirección sustantiva pendiente del comparado.

**Lectura provisional:** fuerte evidencia de que D1 captura una separación política estructural en materia migratoria, pero el caso queda deliberadamente abierto para nombrar el contenido de los polos hasta recuperar el texto comparado.

## Balance del bloque 01

Los cinco casos muestran una primera lección metodológica: **`abs(spread_1d)` identifica votaciones que ayudan a ordenar el espacio, pero no todas tienen la misma anatomía política**.

| Caso | Forma del clivaje | Izq.–der. amplia | Gob.–opos. | Orden–garantías | Regulación–mercado | Estado de contenido |
|---|---|---|---|---|---|---|
| 15295-07 | B + D | compatible/gradiente | débil | fuerte | baja | objeto exacto pendiente |
| 15936-18 | C | complicación/control | muy débil | parcial | baja | exacto recuperado |
| 18155-25 | B | compatible/gradiente | débil | fuerte | baja | casi cerrado |
| 17522-12 | A | fuerte | fuerte pero insuficiente | baja | fuerte | cerrado |
| 16836-06 | A + D | fuerte en coalición | fuerte | por determinar | baja | efecto normativo pendiente |

### Hallazgo provisional

Este bloque **no falsifica** la hipótesis de que D1 se aproxima a una izquierda–derecha amplia, pero obliga a formularla como una estructura multidominio y gradual. Dos de los cinco casos son conflictos de orden/penalidad donde la centroizquierda se separa de la izquierda más dura; uno es una excepción casi específica del PNL; uno produce un clivaje regulatorio-ambiental clásico; y uno produce una división de bloques casi perfecta en migración, aunque falta recuperar el contenido normativo preciso.

Por tanto, después de cinco casos sería prematuro decir que D1 “es izquierda–derecha”. Sí podemos decir que la hipótesis sigue viva y que **gobierno–oposición por sí solo ya encuentra problemas importantes**, sobre todo en los casos gradientes y en el actor-específico.

## Regla nueva para los bloques siguientes

La auditoría de cada roll call identificador deberá registrar además la **forma del clivaje (A/B/C/D)**. Esto evitará que el futuro motor pedagógico explique como “la Cámara se dividió en dos grandes sectores” una votación cuya información proviene en realidad de un partido pequeño, una abstención estratégica o una subdivisión interna de uno de los polos.

## Pendientes antes de cerrar definitivamente estos cinco expedientes

1. **89937 / 15295-07:** recuperar la ficha primaria exacta del roll call y confirmar si es general o particular.
2. **89389 / 16836-06:** recuperar el comparado de tercer trámite, página 26, y reconstruir el efecto normativo de la letra a) eliminada.
3. Mantener 15936-18 como caso de control actor-específico y buscar recurrencias del PNL antes de interpretarlo sustantivamente.

## Estado

**Bloque 01 cerrado como auditoría preliminar, con 3 expedientes sustantivamente suficientes y 2 expedientes explícitamente abiertos por contenido primario pendiente.** No se modifica todavía el nombre público de D1.