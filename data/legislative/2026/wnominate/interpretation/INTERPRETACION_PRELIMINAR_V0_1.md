# Interpretación preliminar de los ejes W-NOMINATE 2026 — v0.1

> **Documento interno de investigación. No usar todavía como texto público ni como etiqueta de ejes.**
>
> Corte de datos: 2 de septiembre de 2026. D1 se presenta con la orientación visual invertida (`D1_display = -D1_model`), sin alterar la estimación subyacente. D2 continúa siendo exploratoria.

## 1. Pregunta

¿Qué estructura política sustantiva resume la primera dimensión de W-NOMINATE y existe evidencia suficiente para asignar un significado coherente a la segunda dimensión?

La regla de interpretación es deliberadamente exigente: una votación con alta capacidad de discriminar posiciones es un **caso a investigar**, no una etiqueta automática. El significado del eje debe reaparecer en varios proyectos, materias y momentos, debe ser compatible con las coaliciones efectivamente observadas y debe poder distinguirse de hipótesis alternativas como gobierno/oposición, mercado/Estado, orden/garantías o comportamiento transaccional.

## 2. Procedimiento

Se utilizan dos rankings complementarios.

1. **D1:** fuerza identificadora medida por `abs(spread_1d)` en la corrida research de 501 trials. Se construye además una selección diversificada con máximo una votación por boletín/proyecto.
2. **D2:** carga relativa ya calculada por la auditoría bidimensional (`relative_dim2_loading`), también diversificada por proyecto.

Cada roll call se cruza con partido, comité y alineamiento vigentes en la **fecha exacta de la votación**, no con la afiliación actual. La clasificación temática interna solo se usa como pista; no ha cerrado todavía su validación externa y no puede justificar por sí sola el nombre de un eje.

## 3. Resultado metodológico previo

El ranking bruto de las 30 votaciones más identificadoras de D1 contiene 21 proyectos distintos; el boletín 18216-05 aporta cinco. La versión diversificada fuerza 30 proyectos distintos y conserva casos altamente identificadores. Por tanto, la lectura sustantiva de D1 no necesita descansar en un único megaproyecto.

En D2 la dependencia por proyecto es mayor: los 25 primeros casos brutos contienen solo 15 clusters y los 40 candidatos disponibles abarcan apenas 20 proyectos únicos. Esta concentración se suma a la debilidad espectral y a la sensibilidad ya documentada de D2.

## 4. Hipótesis líder para D1 — todavía provisional

La evidencia revisada hasta ahora favorece que D1 represente una **dimensión político-ideológica amplia que se aproxima al clivaje izquierda–derecha del comportamiento legislativo**, antes que una simple dimensión gobierno–oposición.

La formulación es intencionalmente cauta. No se sostiene todavía que D1 sea una medida exhaustiva de “ideología” ni que cada valor individual pueda interpretarse como una posición ideológica esencial. Se sostiene que las votaciones que más ayudan a ordenar a la Cámara reaparecen en conflictos reconocibles entre posiciones de izquierda/progresistas y de derecha/conservadoras o pro-mercado/orden, a través de materias distintas.

### 4.1 Casos que separan regulación social/económica y derecha de mercado

- **Boletín 17381-03 — subcontratación de teleoperadores fuera de Chile (5 mayo).** Votación general: 76 a favor, 68 en contra. Oposición: 62/0 a favor; oficialismo: 0/60; PNL: 0/8; Republicanos: 0/27; RN: 0/10; UDI: 0/13; PDG: 14/0. Es un conflicto económico-laboral de alta nitidez.
- **Boletín 16487-12 — prohibición temporal de importación de ciertos plásticos de un solo uso (24 marzo).** 75/71. Oposición: 61/0; oficialismo: 0/63; PNL 0/8; Republicanos 0/27; RN 0/10; UDI 0/11; PDG 14/0. Combina regulación ambiental y económica con una coalición izquierda/derecha muy clara.
- **Boletín 17872-33 — estándar mínimo de reducción de aguas no facturadas (5 mayo).** 73/66. Oposición: 59/0; oficialismo: 0/58; PNL 0/8; Republicanos 0/27; RN 0/8; UDI 0/13; PDG 14/0.
- **Boletín 17837-13 — salud y seguridad laboral (17 agosto).** 79/45. La oposición vota 52/0 a favor mientras el oficialismo lo hace 16/38; la materia incluye mayores obligaciones empresariales, sanciones y protección sindical.
- **Boletín 18216-05, votación 88948 — indicación de Raúl Soto contra el cobro de intereses sobre intereses (20 mayo).** 79/57/17. La indicación buscaba impedir estipular y capitalizar intereses sobre intereses. En nuestros datos temporales: oposición 64/0 a favor, oficialismo 1/50, no alineados 14/7. Este caso confirma que no debe interpretarse el título general de la “megarreforma”; el contenido discriminante es una indicación concreta de regulación crediticia.

### 4.2 Casos que separan orden, control y penalidad

- **Boletín 15258-25 — control preventivo de identidad en zonas fronterizas e instalaciones estratégicas (13 mayo).** Oficialismo 62/0 a favor; PC 0/8; el resto de la centroizquierda es mucho más favorable. El conflicto no reproduce una oposición homogénea, sino una gradación compatible con posiciones sobre control y garantías.
- **Boletín 15347-07 — agravantes en la legislación de drogas (23 marzo).** Oficialismo 65/0 y PNL 7/0; PC 0/8; FA y gran parte del centro/centroizquierda votan a favor. Nuevamente existe gradación dentro del polo izquierdo.
- **Boletín 18155-25 — agravantes por delitos contra la comunidad educativa (13 mayo).** Oficialismo 62/0; PC 0/8; FA dividido en la observación binaria disponible; PS y DC mayoritariamente a favor.
- **Boletín 15295-07 — requisitos para libertad condicional (1 septiembre).** Oficialismo 62/0 y no alineados 13/0; FA 0/11; PS y DC votan a favor. Muestra que el eje no equivale a una dicotomía mecánica de bloques, sino que ordena diferencias internas en cuestiones penales.
- **Boletín 17354-37 — monumento a Sebastián Piñera (14 abril).** Republicanos, PNL, RN, UDI, DC, PPD y PDG apoyan; FA 0/9 y PC 0/7. La dimensión también aparece en una disputa simbólico-política que no es reducible a economía.

## 5. Por qué “gobierno–oposición” parece insuficiente como explicación de D1

La hipótesis gobierno/oposición tiene poder descriptivo porque el gobierno de José Antonio Kast está compuesto principalmente por partidos ubicados en uno de los polos y la oposición de izquierda/centroizquierda en el otro. Sin embargo, existen casos discriminantes que rompen esa equivalencia.

El **Partido Nacional Libertario no integra el gobierno** y se ha declarado oposición/autonomía respecto del Ejecutivo. Pese a ello, en varias de las votaciones más identificadoras se alinea sistemáticamente con Republicanos, UDI y RN: contra la restricción a la subcontratación internacional de teleoperadores, contra regulaciones ambientales y sanitarias y a favor de medidas penales o de control. Esto es evidencia especialmente valiosa: su localización no puede explicarse simplemente por pertenencia al gobierno.

El **PDG** muestra el patrón inverso de utilidad analítica: en varias regulaciones económico-laborales y ambientales vota con la izquierda/centroizquierda, mientras en distintas materias de seguridad acompaña posiciones de derecha o coaliciones amplias. Su comportamiento es más transaccional y de materia, lo que ayuda a producir posiciones intermedias sin convertir el eje en una mera variable de bloque.

Por tanto, la hipótesis que debe intentar falsarse en la siguiente etapa es: **D1 recoge una estructura izquierda–derecha amplia, mientras gobierno/oposición es una correlación política importante pero no su definición.**

## 6. Caso de control: no confundir el proyecto con la votación

El boletín 18216-05 muestra por qué es imprescindible auditar el artículo o indicación exacta. La votación 88948 no era un voto genérico “a favor o en contra de la megarreforma”: correspondía a una indicación renovada del diputado Raúl Soto que prohibía cobrar intereses sobre intereses. El patrón oposición a favor / oficialismo en contra tiene un significado sustantivo coherente con regulación crediticia, no con apoyo general al proyecto del Ejecutivo.

Este principio debe implementarse en el motor de interpretación: **la unidad interpretativa es el roll call concreto, no solo el título del boletín.**

## 7. D2 — no hay todavía una interpretación sustantiva defendible

La evidencia inicial refuerza la decisión de mantener D2 como exploratoria.

Los principales casos son heterogéneos y muchas veces dependen de indicaciones particulares o pequeñas minorías:

- **17112-19, IA y derechos fundamentales:** 22 sí, 59 no y 67 abstenciones. El PNL aparece entre quienes apoyan mientras Republicanos, buena parte de UDI y PDG rechazan; gran parte de la izquierda se abstiene. Es un patrón transversal, pero no basta para definir un clivaje.
- **17471-07, robo/receptación de medidores de agua:** coalición singular con DC claramente favorable y muchos partidos tanto de derecha como de izquierda contrarios o divididos.
- **18216-05:** varias indicaciones particulares del megaproyecto generan altas cargas D2, lo que introduce dependencia por proyecto.
- **18189-14, equipos municipales para regularización gratuita de viviendas vulnerables:** izquierda y varios RN/PNL votan a favor, mientras Republicanos, UDI y PDG concentran buena parte del rechazo. Es una fractura transversal interesante, pero distinta de los casos anteriores.

Con solo 20 proyectos únicos entre los 40 candidatos D2 y con la inestabilidad geométrica ya observada bajo balanceo por proyecto, **no debe asignarse todavía un nombre a D2**.

## 8. Hipótesis a contrastar formalmente en la siguiente auditoría

| Hipótesis | Estado preliminar | Qué tendría que observarse |
|---|---|---|
| Izquierda–derecha amplia | **Hipótesis líder D1** | recurrencia a través de economía, regulación, seguridad y disputas simbólicas; PNL próximo a derecha pese a no ser gobierno |
| Gobierno–oposición | Parcial, pero insuficiente | debería explicar PNL y todas las divisiones internas opositoras; por ahora no lo hace |
| Estado/intervención–mercado | Componente importante de D1 | explica muy bien varios casos económicos/ambientales, pero no seguridad ni memoria simbólica |
| Orden/control–garantías | Componente importante de D1 | explica varias votaciones penales, pero no las económico-laborales |
| Tradicional–anti-establishment | Evidencia débil | debería reunir de manera consistente PNL/PDG contra partidos tradicionales; no aparece de forma estable |
| Transaccional/autonomía | Mejor como propiedad de actores que como eje | PDG y algunos independientes cambian de coalición según materia |
| Segundo clivaje coherente D2 | **No demostrado** | requiere recurrencia temática y coalicional entre proyectos, estabilidad geométrica y baja dependencia por boletín |

## 9. Arquitectura futura de comunicación pública

Cuando la interpretación supere la auditoría, la web debe separar tres capas:

### Qué encontramos
Una frase simple y sustantiva, sin jerga estadística.

### Por qué creemos que significa eso
Resumen de 3–5 patrones empíricos recurrentes, incluyendo casos que permiten distinguir izquierda/derecha de gobierno/oposición.

### ¿Cómo llegamos a esta conclusión?
Panel desplegable con el método completo: selección de roll calls identificadores, diversificación por proyecto, coaliciones temporales, contenido exacto de artículos/indicaciones, fuentes externas, hipótesis alternativas y límites de interpretación.

La comunicación debe incluir siempre que las coordenadas resumen **comportamiento de votación bajo la agenda legislativa observada**, no una esencia ideológica de cada persona.

## 10. Estado

**v0.1 = evidencia preliminar suficiente para formular una hipótesis líder sobre D1; insuficiente para cerrar el nombre del eje y claramente insuficiente para nombrar D2.**

La siguiente versión debe auditar fuentes primarias y prensa/especialistas para una muestra humana de casos, y después evaluar explícitamente las hipótesis competidoras.