# Contrato metodológico W-NOMINATE v0.1

Este documento fija las reglas para construir estimaciones espaciales a partir de las votaciones nominales de Sala de la Cámara de Diputadas y Diputados dentro de **Conoce a tu parlamentario**. La estimación es una **capa analítica derivada**: no modifica ni reemplaza los datos legislativos primarios.

## 1. Objeto

El objetivo es estimar posiciones relativas de votación entre integrantes de la Cámara a partir de decisiones binarias observadas en Sala. El resultado describe estructura espacial del comportamiento de voto; **no debe etiquetarse automáticamente como ideología, izquierda/derecha, oficialismo/oposición o posición programática**.

La interpretación política de una dimensión requiere una etapa posterior de validación sustantiva con partidos, bancadas, materias, votaciones discriminantes y conocimiento contextual.

## 2. Universo temporal e institucional

- Cámara de Diputadas y Diputados de Chile.
- Inicio del período observado: **11 de marzo de 2026**.
- Se usan exclusivamente votaciones nominales verificadas como votaciones de **Sala**.
- Se incluyen votaciones realizadas desde esa fecha aunque el proyecto de ley haya ingresado antes del inicio del período.
- Los votos de comisión quedan fuera de esta estimación.

## 3. Fuente y separación de capas

La fuente inmediata del modelo es la matriz neutral generada desde `member_votes_enriched.csv` y `rollcalls.csv`.

Archivos de preparación:

- `rollcall_matrix_binary.csv`: matriz diputado × roll call.
- `rollcall_matrix_metadata.csv`: metadatos y criterios de elegibilidad por votación.
- `rollcall_member_metadata.csv`: participación binaria y criterios de elegibilidad por diputado.
- `rollcall_matrix_diagnostics.json`: auditoría de la transformación.

Los archivos primarios `member_votes.csv` y `rollcalls.csv` permanecen intactos. Las afiliaciones temporales, temas, redes y estimaciones espaciales son capas derivadas independientes.

## 4. Codificación de votos

Para el modelo espacial binario:

- `Afirmativo` → `1`.
- `En Contra` / equivalente negativo oficial → `0`.
- `Abstención` → missing para W-NOMINATE.
- `No Vota` → missing para W-NOMINATE.
- `Dispensado` → missing para W-NOMINATE.

Estas categorías no binarias **no se recodifican como 0**. Permanecen disponibles en los datos originales y en las capas descriptivas para análisis de participación, abstención y comportamiento legislativo.

## 5. Criterio base de escalabilidad

La especificación principal seguirá los criterios convencionales de W-NOMINATE documentados por Voteview:

- `lop = 0.025`: una votación debe tener al menos 2,5% de los votos binarios en el lado minoritario.
- `minvotes = 20`: un legislador debe registrar al menos 20 votos binarios entre las votaciones retenidas para ser escalado.

La matriz neutral marca explícitamente estas condiciones antes de la estimación. El futuro ejecutor W-NOMINATE deberá además registrar las exclusiones efectivamente realizadas por el paquete y comprobar que concuerden con la preparación.

## 6. Análisis de sensibilidad

No se tratará 2,5% como una verdad sustantiva. Se conservarán como mínimo tres especificaciones:

- principal: `lop = 0.025`;
- sensibilidad 1: `lop = 0.05`;
- sensibilidad 2: `lop = 0.10`.

En todas se mantendrá inicialmente `minvotes = 20`. Se compararán cobertura, ordenamiento relativo, correlación de coordenadas y estabilidad de los resultados.

## 7. Dimensionalidad

### Modelo principal: una dimensión

La primera estimación será **1D**. Es la especificación más parsimoniosa y evita atribuir significado a una segunda dimensión antes de demostrar que aporta información sistemática.

### Segunda dimensión: prueba diagnóstica

Se estimará un modelo **2D** únicamente como análisis de sensibilidad y ajuste. No se publicará ni interpretará una segunda dimensión por el solo hecho de que el algoritmo pueda estimarla.

Para justificar 2D deberá observarse una mejora relevante de ajuste y una estructura sustantiva interpretable y estable.

## 8. Polaridad e identificación

El signo de una coordenada espacial es arbitrario. W-NOMINATE requiere fijar polaridad para identificar la orientación de las dimensiones.

Reglas:

1. El ancla de polaridad debe quedar registrada de forma explícita y versionada.
2. La elección del ancla no transforma por sí sola la dimensión en izquierda/derecha.
3. Los resultados iniciales se nombrarán `dimension_1_raw` y, cuando corresponda, `dimension_2_raw`.
4. Cualquier inversión posterior de signo deberá ser una transformación reproducible, documentada y separada del resultado bruto.
5. Antes de seleccionar el ancla definitiva se verificará que el legislador elegido tenga participación suficiente y se ubique de forma estable en uno de los extremos del espacio preliminar.

Por ahora, **la selección del ancla queda pendiente**. No se ejecutará una estimación que luego pueda parecer semánticamente identificada sin dejar constancia de esta decisión.

## 9. Diagnósticos mínimos de cada corrida

Toda ejecución deberá guardar, como mínimo:

- número de roll calls leídos, aceptados y excluidos;
- número de legisladores leídos, aceptados y excluidos;
- criterio `lop` y `minvotes` utilizado;
- porcentaje correctamente clasificado;
- APRE cuando esté disponible;
- probabilidad geométrica media u otras medidas de ajuste que entregue el paquete;
- parámetros estimados del modelo;
- polaridad utilizada;
- fecha y versión del contrato metodológico;
- lista o tabla de coordenadas brutas;
- metadatos necesarios para enlazar cada coordenada con `diputado_id`.

## 10. Comparaciones y estabilidad

Antes de utilizar públicamente los puntos ideales se compararán:

- 1D con `lop` 2,5%, 5% y 10%;
- 1D versus 2D;
- posición individual y posición agregada por partido/bancada;
- sensibilidad a ausencias y participación;
- estabilidad temporal cuando exista suficiente longitud del período para ventanas o cortes sucesivos.

Una posición que dependa fuertemente de un umbral, de pocas votaciones o de alta ausencia deberá ser marcada como menos estable.

## 11. Interpretación sustantiva

La orientación semántica de una dimensión se estudiará **después** de la estimación mediante:

- distribución por partido y bancada en la fecha de cada votación;
- votaciones con alta capacidad discriminante;
- materias legislativas de esas votaciones;
- origen Ejecutivo/parlamentario;
- contraste con patrones políticamente conocidos sin utilizarlos para alterar los datos originales.

No se inferirá que una dimensión es izquierda/derecha solamente porque partidos conocidos aparezcan ordenados de determinada manera en una corrida inicial.

## 12. Uso público

Hasta completar la validación sustantiva:

- no mostrar una cifra como “ideología del diputado”;
- no llamar automáticamente “moderado”, “extremo”, “rebelde” o equivalentes a una coordenada;
- no convertir distancia espacial en evaluación normativa;
- conservar intervalos, advertencias o medidas de estabilidad cuando corresponda.

La ficha pública podrá incorporar posteriormente una visualización espacial si la metodología supera estas validaciones.

## 13. Automatización

La secuencia objetivo es:

`datos primarios → afiliaciones temporales → matriz neutral → filtros auditables → W-NOMINATE → diagnósticos → interpretación sustantiva → eventual publicación`.

El estimador debe poder regenerarse sin volver a extraer datos de la Cámara y sin modificar las tablas primarias.

## 14. Referencias metodológicas de base

- Voteview, **W-NOMINATE Program Page**: documentación del corte habitual de 2,5% para el lado minoritario y mínimo de 20 votos por legislador: https://legacy.voteview.com/w-nominate.htm
- Poole, Keith T. y Howard Rosenthal. *Congress: A Political-Economic History of Roll Call Voting*. Oxford University Press.
- Poole, Keith T. *Spatial Models of Parliamentary Voting*. Cambridge University Press.
- W-NOMINATE para R, documentación y ejemplos históricos de Voteview: https://legacy.voteview.com/pdf/wnominate.pdf

## 15. Decisiones pendientes para v0.2

- Seleccionar y justificar el ancla de polaridad de la primera dimensión.
- Ejecutar y auditar la primera corrida 1D.
- Comparar sensibilidad 2,5% / 5% / 10%.
- Ejecutar 2D únicamente como prueba diagnóstica.
- Definir criterios de estabilidad para una eventual publicación.
- Decidir, solo después de validación, si la dimensión puede recibir una interpretación política sustantiva.
