# Contrato prospectivo de modelos roll-call v0.2

**Proyecto:** Conoce a tu parlamentario  
**Cámara:** Cámara de Diputadas y Diputados de Chile, período 2026–2030  
**Inicio del universo observado:** 11 de marzo de 2026  
**Estado:** diseño prospectivo de investigación; resultados internos y no publicables  
**Versión:** 0.2

Este documento amplía `CONTRATO_WNOMINATE_V0_1.md`. La versión 0.1 y las
estimaciones producidas hasta el 2 de septiembre de 2026 conservan valor como
exploración, pero no constituyen una validación confirmatoria. La versión 0.2
fija las decisiones que se aplicarán a las nuevas corridas y actualizaciones.

## 1. Objeto y estimandos

El análisis persigue cuatro objetos distintos, que no deben confundirse:

1. **Posición espacial latente:** eje empírico que resume decisiones binarias de
   Sala. Se estimará principalmente en una dimensión.
2. **Incertidumbre de la posición:** variación compatible con la información
   observada, la dependencia entre votaciones y las decisiones de diseño.
3. **Variabilidad del comportamiento:** dispersión de las decisiones de un
   parlamentario alrededor de un patrón común. B-Call será un diagnóstico de
   este objeto, no un sustituto automático del modelo espacial.
4. **Estabilidad temporal:** persistencia o cambio de la posición espacial en
   el tiempo, distinguiendo cambio individual de cambio en la agenda sometida a
   votación.

Ninguno de estos estimandos se denominará automáticamente ideología,
izquierda–derecha, moderación, extremismo, disciplina o apoyo al Gobierno.

## 2. Cortafuego entre legislaturas

La Cámara 2022–2026 se utiliza únicamente como antecedente metodológico. Sus
votos, coordenadas, etiquetas, coaliciones, anclas y parámetros estimados no
entran en los modelos de la Cámara 2026–2030 y no se usarán como *priors*
informativos.

Sí se conservan aprendizajes generales: separar tipos de ausencia, estimar
incertidumbre válida, auditar participación y votos desbalanceados, estudiar
concentración por proyecto, comprobar dimensionalidad y evitar interpretar una
coordenada como disciplina partidaria.

Una eventual comparación entre legislaturas será un producto separado y
exigirá un diseño de enlace o un modelo dinámico común. No se compararán
directamente coordenadas obtenidas en estimaciones independientes.

## 3. Universo y separación de capas

- Solo votaciones nominales verificadas como votaciones de Sala desde el 11 de
  marzo de 2026.
- Se incluyen proyectos ingresados antes de esa fecha cuando la votación de
  Sala ocurre dentro del período.
- Se excluyen votaciones de comisión.
- Los datos primarios `rollcalls.csv` y `member_votes.csv` permanecen intactos.
- Toda matriz, filtro, estimación, etiqueta temática y asociación política es
  una capa derivada regenerable.
- Cada corrida debe registrar SHA del commit, fecha de corte, hash de los
  insumos, versiones de R/Python y paquetes, semilla y parámetros.

## 4. Estados de voto y matrices

### 4.1 Matriz espacial binaria

- `Afirmativo` = 1.
- `En Contra` = 0.
- `Abstención`, `No Vota` y `Dispensado` = missing observado.
- No pertenecer aún o ya no pertenecer a la legislatura = missing estructural.

Los estados no binarios nunca se recodifican como voto negativo en la
especificación principal. Una recodificación alternativa de abstenciones podrá
usarse solo como prueba extrema de sensibilidad, con una etiqueta inequívoca.

### 4.2 Matriz B-Call

- `Afirmativo` = 1.
- `Abstención` = 0.
- `En Contra` = -1.
- `No Vota`, `Dispensado` y missing estructural permanecen ausentes.

La matriz B-Call se almacenará separadamente para impedir que su cero
sustantivo se confunda con el cero binario de W-NOMINATE/IRT.

## 5. Elegibilidad y composición de la evidencia

### 5.1 Votaciones

La especificación de referencia usa `lop = 0.025`. Se estimarán sensibilidades
con `lop = 0.01`, `0.05` y `0.10`. En cada corrida se informarán el número y la
proporción de roll calls excluidos, no solo el ajuste entre los retenidos.

### 5.2 Parlamentarios

La elegibilidad analítica se determinará sobre las oportunidades que cada
integrante tuvo mientras pertenecía a la Cámara:

- referencia: al menos 10% de decisiones binarias y un mínimo absoluto de 20;
- sensibilidades: 20% y 30%;
- reporte continuo de cobertura, sin convertir el umbral en una afirmación
  sustantiva sobre la persona excluida.

Cuando el software solo acepte un `minvotes` global, el filtro relativo se
aplicará y documentará antes de construir el objeto de estimación; `minvotes`
quedará además como salvaguarda interna.

### 5.3 Dependencia por proyecto

Las siguientes especificaciones son obligatorias:

- universo elegible completo;
- deduplicación de patrones idénticos dentro de boletín;
- límites deterministas de 20 y 10 roll calls por boletín;
- exclusión sucesiva de boletines dominantes;
- resumen de concentración y número efectivo de proyectos.

Los límites por boletín son pruebas de sensibilidad y no representan que una
votación tenga menos valor por pertenecer a un proyecto con tramitación extensa.

## 6. Jerarquía de modelos

### 6.1 W-NOMINATE 1D: benchmark

W-NOMINATE se conserva por su tradición comparada y capacidad descriptiva. La
corrida de investigación utilizará 501 ensayos en la especificación base. Las
corridas de humo podrán usar menos ensayos, pero sus errores estándar no se
guardarán ni presentarán como resultados de investigación.

Los errores estándar iguales a cero producidos con `trials = 1` se consideran
no estimados, no evidencia de ausencia de incertidumbre.

### 6.2 IRT bayesiano 2PL 1D: modelo inferencial principal

Se estimará un modelo de respuesta al ítem con un punto ideal por legislador y
parámetros de dificultad y discriminación por roll call. Tendrá al menos cuatro
cadenas independientes, semillas registradas y diagnósticos de convergencia.

Requisitos mínimos para aceptar una corrida:

- \(\hat R < 1{,}01\) para los parámetros de interés;
- tamaños muestrales efectivos adecuados, con objetivo de al menos 1.000 para
  los puntos ideales individuales;
- trazas sin mezcla deficiente;
- ausencia de divergencias si el motor utilizado las define;
- estabilidad frente a inicializaciones e identificación alternativas.

La duración se ampliará hasta satisfacer diagnósticos; no se considerará que
un número fijo de iteraciones garantiza convergencia.

### 6.3 Optimal Classification: robustez no paramétrica

Optimal Classification comprobará si el orden unidimensional depende de la
función probabilística de W-NOMINATE/IRT. Se compararán clasificación, errores y
ordenamiento, después de alinear técnicamente el signo.

### 6.4 B-Call: diagnóstico complementario

B-Call se implementará de manera fiel a su artículo y código de replicación:
estandarización dentro de cada votación, orientación mediante dos grupos,
promedio individual como D1 y desviación estándar individual como D2.

Se documentará cómo se obtuvieron los dos grupos y cuál fue el pivote. Si los
grupos proceden de W-NOMINATE, B-Call no se presentará como validación
independiente de W-NOMINATE. También se ejecutará sensibilidad al algoritmo de
agrupamiento, pivote, participación y exclusión de proyectos dominantes.

B-Call D2 se denominará **variabilidad B-Call**. No equivale por construcción a
cohesión partidaria, disciplina ni cambio temporal, y actualmente no ofrece el
mismo modelo de incertidumbre que el IRT bayesiano.

## 7. Identificación y orientación

- El signo es arbitrario y se conservarán coordenadas brutas.
- Un ancla técnica debe tener alta participación y estabilidad entre
  especificaciones; su elección no confiere significado político al eje.
- Las soluciones se alinearán por reflexión en 1D y mediante Procrustes en 2D.
- La orientación sustantiva, si se justifica, será una transformación posterior
  registrada y nunca reemplazará el resultado bruto.
- Los partidos, bancadas y bloques históricos se usarán para validación e
  interpretación, no para modificar votos ni forzar resultados.

## 8. Dimensionalidad

Una dimensión es la especificación principal. La segunda dimensión permanece
diagnóstica y debe superar conjuntamente:

- ganancia de clasificación, APRE y desempeño predictivo;
- estabilidad frente a `lop`, deduplicación y balanceo por boletín;
- estabilidad geométrica después de Procrustes;
- interpretación común de las votaciones que más la identifican;
- prueba de efecto arco.

La prueba de arco estimará la asociación de D2 con D1 y \(D1^2\), reportará la
varianza explicada por la curvatura y volverá a estudiar los residuos. Una D2
principalmente cuadrática respecto de D1 no se interpretará como un cleavage
independiente.

## 9. Incertidumbre y validación predictiva

Además de la incertidumbre interna de cada modelo, se aplicará remuestreo por
boletín/proyecto para respetar la dependencia entre roll calls. El modo piloto
usará 200 réplicas y la corrida destinada a investigación, 1.000.

Se reportarán:

- intervalos individuales y su anchura;
- Pearson, Spearman y RMSE estandarizado entre métodos y especificaciones;
- cambio de percentil y estabilidad de bandas, no solo cambio de ranking;
- clasificación correcta, APRE y probabilidad geométrica media cuando
  correspondan;
- validación cruzada o predicción fuera de muestra a nivel de proyecto;
- chequeos predictivos posteriores del modelo bayesiano.

Ninguna métrica aislada decidirá la validez. Los umbrales de advertencia se
calibrarán mediante simulaciones y perturbaciones conocidas, no a partir de
elegir el corte que favorezca los resultados observados.

## 10. Estabilidad temporal

Se separan tres ejercicios:

1. **Fiabilidad de partición:** divisiones aleatorias estratificadas de la
   evidencia; no miden cambio temporal.
2. **Comparación cronológica descriptiva:** ventanas contiguas con cantidad de
   información semejante, auditando tema, origen, competitividad, proyectos y
   participación.
3. **Modelo dinámico conjunto:** puntos ideales relacionados entre períodos y
   estimados en una escala común.

La comparación cronológica se repetirá sobre una muestra emparejada o
ponderada de roll calls según tema, origen, competitividad y concentración por
proyecto. Se mostrarán tanto resultados sin balancear como balanceados.

La prueba exploratoria de mitades producida el 2 de septiembre de 2026 no cierra
esta etapa: utilizó `trials = 1`, la mitad inicial concentró 52,2% de sus roll
calls en un boletín y las submuestras con cap tuvieron 78 y 114 votaciones. Sus
correlaciones son evidencia descriptiva útil, pero mezclan tiempo y composición
de agenda.

## 11. Historia política y validación externa

Cada voto se asociará con `party_at_vote` y `caucus_at_vote`. Nunca se utilizará
el partido actual para explicar retrospectivamente toda la serie.

La interpretación de D1 considerará:

- partidos, bancadas y alineamiento vigentes en la fecha del voto;
- origen Ejecutivo/parlamentario;
- macroárea temática, una vez validada formalmente la taxonomía;
- roll calls con alta discriminación;
- hitos y cambios de afiliación documentados externamente.

La asociación con grupos no demuestra que el eje sea ideológico ni permite
distinguir preferencias sinceras, disciplina, selección o estrategia.

## 12. Reproducibilidad y modos de ejecución

Habrá dos modos separados:

- **smoke/pilot:** valida ambiente, formas de datos y finalización del código;
  nunca publica coordenadas ni incertidumbre.
- **research:** ejecuta toda la grilla aprobada, incertidumbre y diagnósticos;
  sus resultados permanecen internos hasta revisión metodológica.

Cada modelo guardará su objeto completo (`RDS` u homólogo), tablas derivadas,
manifiesto, logs diagnósticos y un resumen legible. Los workflows no modificarán
datos primarios ni el sitio público.

## 13. Puertas antes de cualquier publicación

Antes de incorporar una representación espacial a las fichas deben estar
cerradas y documentadas estas etapas:

1. convergencia e incertidumbre válidas;
2. estabilidad entre W-NOMINATE, IRT y OC;
3. robustez por participación, `lop`, proyecto y agenda;
4. auditoría temporal conjunta;
5. validación sustantiva de D1;
6. decisión explícita sobre formato público y lenguaje permitido.

Mientras alguna permanezca abierta, las coordenadas son resultados internos de
investigación.

## 14. Referencias metodológicas principales

- Poole, Keith T., Jeffrey B. Lewis, James Lo y Royce Carroll. 2011. “Scaling
  Roll Call Votes with W-NOMINATE in R”. *Journal of Statistical Software*
  42(14). https://www.jstatsoft.org/article/view/v042i14
- Clinton, Joshua, Simon Jackman y Douglas Rivers. 2004. “The Statistical
  Analysis of Roll Call Data”. *American Political Science Review* 98(2).
  https://doi.org/10.1017/S0003055404001194
- Lewis, Jeffrey B. y Keith T. Poole. 2004. “Measuring Bias and Uncertainty in
  Ideal Point Estimates via the Parametric Bootstrap”. *Political Analysis*
  12(2). https://doi.org/10.1093/pan/mph009
- Carroll, Royce, Jeffrey B. Lewis, James Lo, Keith T. Poole y Howard Rosenthal.
  2009. “Measuring Bias and Uncertainty in DW-NOMINATE Ideal Point Estimates via
  the Parametric Bootstrap”. *Political Analysis* 17(3).
  https://doi.org/10.1093/pan/mpp005
- Imai, Kosuke, James Lo y Jonathan Olmsted. 2016. “Fast Estimation of Ideal
  Points with Massive Data”. *American Political Science Review* 110(4).
  https://doi.org/10.1017/S000305541600037X
- Toro-Maureira, Sergio, Juan Reutter, Lucas Valenzuela, Daniel Alcatruz y
  Macarena Valenzuela. 2025. “B-Call: Integrating Ideological Position and
  Voting Cohesion in Legislative Behavior”. *Frontiers in Political Science* 7.
  https://doi.org/10.3389/fpos.2025.1670089
