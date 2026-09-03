# Resultados experimentales W-NOMINATE · v0.1

**Proyecto:** Conoce a tu parlamentario  
**Período observado:** 11 de marzo de 2026 en adelante  
**Fecha del corte:** 2 de septiembre de 2026  
**Estado:** experimental; **apto para laboratorio público con advertencias, no cerrado todavía como indicador ideológico individual de las fichas**.

Este documento registra los resultados de la primera estimación espacial de las votaciones nominales de Sala de la Cámara de Diputadas y Diputados. Complementa el contrato metodológico `CONTRATO_WNOMINATE_V0_1.md`; no modifica los datos primarios ni convierte las coordenadas en categorías políticas sustantivas definitivas.

La pestaña pública `wnominate.html` debe entenderse como un **laboratorio de exploración metodológica**. Su publicación no equivale al cierre de los gates multimétodo, temporales o interpretativos requeridos para integrar la coordenada como indicador individual definitivo dentro de las fichas legislativas.

## 1. Insumo y codificación

La matriz de origen contiene **155 integrantes × 364 votaciones de Sala**. Para el modelo espacial se conserva únicamente la elección binaria:

- `Afirmativo = 1`
- `En Contra = 0`
- `Abstención`, `No Vota` y `Dispensado = missing`

La matriz contiene 50.552 observaciones binarias y 5.868 missing para la estimación espacial. Sesenta y cuatro roll calls son unánimes en la submatriz binaria y 300 son no unánimes.

La especificación base usa `lop = 0.025` y `minvotes = 20`. Se estiman sensibilidades a `lop = 0.05` y `lop = 0.10`, además de pruebas que eliminan duplicados exactos dentro de boletín y limitan el número de roll calls aportados por un mismo boletín.

## 2. Resultado unidimensional

Se estimaron correctamente seis especificaciones 1D:

| Especificación | Roll calls | Diputados estimados | Clasificación correcta | APRE |
|---|---:|---:|---:|---:|
| `raw_lop025` | 276 | 154 | 95,80% | 0,884 |
| `raw_lop050` | 269 | 154 | 95,90% | 0,887 |
| `raw_lop100` | 258 | 154 | 95,97% | 0,889 |
| `dedup_lop025` | 269 | 154 | 95,79% | 0,884 |
| `cap20_balanced_lop025` | 180 | 154 | 95,66% | 0,880 |
| `cap10_balanced_lop025` | 136 | 153 | 95,66% | 0,875 |

La orientación matemática del eje es arbitraria. Las corridas se alinean técnicamente entre sí para estudiar estabilidad. La visualización pública invierte el signo técnico (`D1 visual = -D1 técnico`) para mantener la convención izquierda → derecha. Esa lectura se apoya en una auditoría sustantiva posterior, pero permanece provisional hasta el cierre final del contrato de publicación.

## 3. Robustez frente a umbral y concentración por boletín

La concentración por proyecto era una preocupación real: en la especificación `lop >= 0.025`, un solo boletín aporta 116 de 276 roll calls elegibles. Por eso se ejecutaron sensibilidades que limitan cada boletín a 20 o 10 votaciones seleccionadas de manera determinista.

Las coordenadas 1D resultaron muy estables:

- base vs. `lop = 0.05`: Pearson ≈ **0,9998**;
- base vs. `lop = 0.10`: Pearson ≈ **0,9992**;
- base vs. deduplicación exacta: Pearson ≈ **0,99998**;
- base vs. cap 20: Pearson ≈ **0,9951**;
- base vs. cap 10: Pearson ≈ **0,9941**.

La conclusión es importante: la sobrerrepresentación de un boletín aumenta el peso de ese proyecto en la muestra, pero **no parece determinar el orden espacial unidimensional de la Cámara**.

## 4. Cobertura y exclusiones

La especificación base estima 154 de 155 integrantes.

- **María Francisca Bello Campos** no tiene votos binarios utilizables en el universo observado y queda fuera de todas las especificaciones. No se imputa una posición.
- En el recorte extremo `cap10`, **Javiera Morales Alvarado** conserva solo 12 observaciones binarias y queda bajo `minvotes = 20`; sí es estimable en las demás especificaciones.

Las exclusiones permanecen explícitas en `member_exclusions.csv` y deben permanecer visibles en cualquier presentación pública del modelo.

## 5. Estabilidad individual y relación con agrupaciones políticas

La estabilidad global no implica que cada posición individual sea igualmente estable. La auditoría estandariza cada especificación y registra desplazamientos y cambios de rango por diputado. Algunos casos presentan variaciones relevantes de rango aun cuando las correlaciones agregadas sean muy altas; por eso **no se debe publicar un ranking lineal ingenuo de “más a menos ideológico”**.

En la especificación base, la coordenada 1D muestra una asociación descriptiva muy fuerte con las estructuras políticas históricas observadas durante las votaciones:

- partido: η² ≈ **0,848**;
- bancada/comité: η² ≈ **0,987**;
- bloque editorial oficialismo/oposición/no alineado: η² ≈ **0,893**.

Estos valores indican estructura, no causalidad. La dimensión se obtiene de los votos y no de las etiquetas de partido o bancada.

## 6. Diagnóstico bidimensional

Se estimaron tres especificaciones 2D: base `lop = 0.025`, `lop = 0.05` y una versión balanceada con máximo 20 roll calls por boletín. Las tres terminaron correctamente.

El paso de 1D a 2D mejora, en promedio:

- clasificación correcta: **+1,56 puntos porcentuales**;
- APRE: **+0,043**.

Sin embargo, el segundo eigenvalor es muy pequeño respecto del primero: la razón media `eigenvalue2 / eigenvalue1` es aproximadamente **0,027**.

Para no confundir cambios de orientación matemática con cambios reales se alinearon los espacios mediante **Similarity Procrustes**. La primera dimensión permanece extremadamente estable. La segunda dimensión presenta dos comportamientos distintos:

- base vs. cambio de `lop`: Pearson D2 ≈ **0,991**, Spearman ≈ **0,977**;
- base vs. cap 20 por boletín: Pearson D2 ≈ **0,723**, Spearman ≈ **0,347**.

Por tanto, D2 es reproducible frente a un cambio del umbral de minoría, pero **mucho más sensible a la composición de proyectos de la muestra** que D1.

## 7. Qué parece capturar D2

En la corrida base, la asociación descriptiva de D2 es:

- partido: η² ≈ **0,822**;
- bancada/comité: η² ≈ **0,926**;
- bloque oficialismo/oposición/no alineado: η² ≈ **0,153**.

Esto sugiere que D2 no reproduce principalmente la separación gobierno/oposición. Parece recoger diferencias internas entre partidos y bancadas, pero su interpretación sustantiva todavía no está cerrada.

Una exploración mediante los `spread` de W-NOMINATE muestra mayor carga relativa de D2 en algunos conjuntos temáticos, pero esta evidencia **no basta para nombrar la dimensión**, especialmente porque la taxonomía temática aún tiene pendiente una validación externa/formal y varios roll calls heredan el tema principal del proyecto asociado.

## 8. Decisión metodológica provisional

A este corte:

1. **1D será el modelo espacial principal y parsimonioso de trabajo.**
2. **2D se conserva como diagnóstico exploratorio secundario** y puede mostrarse únicamente como laboratorio explícitamente exploratorio, no como segundo eje político cerrado.
3. La lectura izquierda–derecha de D1 es la interpretación sustantiva líder y se muestra de manera provisional en el laboratorio, pero su nombre público definitivo sigue sujeto a los gates restantes.
4. No se imputarán posiciones a diputados sin información suficiente.
5. Las coordenadas **no se integrarán todavía como indicador cerrado de las fichas individuales**.
6. Los filtros temáticos públicos deben describirse como **contexto temático del proyecto**, no como clasificación oficial ni como codificación exacta del objeto de cada roll call.

## 9. Pruebas pendientes antes de uso individual cerrado

Antes de transformar las coordenadas en un indicador individual definitivo de las fichas se debe:

- evaluar **estabilidad temporal** del eje 1D mediante subperíodos comparables;
- realizar IRT bayesiano 2PL 1D;
- estimar Optimal Classification como robustez no paramétrica;
- cerrar el contrato final de incertidumbre/robustez individual;
- cerrar formalmente la interpretación y nombre público de D1;
- documentar explícitamente missingness y casos no estimables;
- mejorar la explicación sustantiva mediante votaciones concretas auditadas.

La regla mientras estas etapas estén abiertas es:

> **W-NOMINATE puede explorarse públicamente como laboratorio metodológico transparente, pero no debe presentarse todavía como un puntaje ideológico individual definitivo ni integrarse silenciosamente a las fichas cerradas.**
