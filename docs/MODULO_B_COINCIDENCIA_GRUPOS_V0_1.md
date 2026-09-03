# Módulo B · Coincidencia con partido y bancada/comité · v0.1

**Proyecto:** Conoce a tu parlamentario  
**Cámara:** Cámara de Diputadas y Diputados de Chile, período 2026–2030  
**Estado:** diseño editorial y regla metodológica **CERRADOS**; implementación pública en curso  
**Corte auditado:** 364 votaciones nominales de Sala y 56.420 registros nominales, hasta el 1 de septiembre de 2026

Este módulo responde una pregunta descriptiva:

> **Cuando existe una posición predominante entre los demás integrantes de su grupo, ¿con qué frecuencia esta diputada o diputado vota de la misma manera?**

Se muestran por separado dos relaciones institucionales:

1. **Partido político** vigente en la fecha de cada votación.
2. **Bancada / Comité Parlamentario** vigente en la fecha de cada votación.

La separación es sustantiva. Una persona independiente puede no tener comparación partidaria y sí pertenecer a una bancada/comité comparable. Del mismo modo, pertenecer a un comité no la convierte en militante de los partidos que lo integran.

---

## 1. Nombre público

### Título del módulo

**Coincidencia con sus grupos parlamentarios**

### Nombres de las dos tarjetas

- **Con su partido**
- **Con su bancada o comité**

No se utilizarán como etiquetas principales:

- disciplina;
- indisciplina;
- rebelión;
- lealtad;
- obediencia.

Esas palabras implican mecanismos causales o evaluaciones que el indicador descriptivo no identifica.

---

## 2. Regla metodológica pública

La versión pública utiliza tres filtros simultáneos.

### 2.1 Leave-one-out: el voto de la persona no define su propio comparador

Para cada votación:

1. se identifica el partido o bancada/comité de la persona **en la fecha de ese voto**;
2. se elimina su propia decisión de los conteos del grupo;
3. se observan las decisiones de los demás integrantes del grupo;
4. se exige que existan al menos **dos decisiones sustantivas de pares**;
5. se exige una **posición modal única** entre esos pares;
6. recién entonces se compara la opción de la persona con esa posición predominante.

Esta regla evita circularidad. En particular, una persona de un partido compuesto por solo dos integrantes no puede definir junto a su único par una supuesta “posición predominante de los demás”.

### 2.2 Solo decisiones sustantivas de la persona

Son comparables:

- Afirmativo;
- En Contra;
- Abstención.

No se contabilizan como coincidencia ni divergencia:

- No Vota;
- Dispensado.

### 2.3 Votaciones con al menos 10% de minoría binaria en la Cámara

La vista pública utiliza como universo principal las votaciones donde el lado minoritario entre **Afirmativo y En Contra** representa al menos **10% de los votos binarios de la Cámara**.

El filtro no afirma que el 10% tenga un significado normativo. Su función es evitar que el indicador sea inflado por votaciones casi unánimes en las que coincidir con el grupo aporta poca información sobre diferencias políticas o institucionales.

Sensibilidades internas se conservan en:

- 0%;
- 5%;
- 10%;
- 20%.

---

## 3. Por qué 10% es el corte público

La auditoría leave-one-out muestra que con 10% todavía existe un universo amplio:

### Partido

- integrantes con al menos una comparación: **121**;
- comparaciones acumuladas: **29.147**;
- coincidencias: **27.922**;
- coincidencia ponderada: **95,80%**;
- mediana de comparaciones por integrante comparable: **251**;
- percentil 10 de comparaciones: **216**;
- integrantes comparables con menos de 20 observaciones: **0**.

### Bancada/comité

- integrantes con al menos una comparación: **152**;
- comparaciones acumuladas: **36.440**;
- coincidencias: **34.662**;
- coincidencia ponderada: **95,12%**;
- mediana de comparaciones por integrante comparable: **249**;
- percentil 10 de comparaciones: **219,2**;
- dos casos tienen menos de 20 observaciones y no mostrarán porcentaje público.

### Sensibilidad 5% → 10%

El cambio individual es muy pequeño para la gran mayoría:

- partido: diferencia absoluta mediana **0,16 puntos porcentuales**, p90 **0,56**;
- bancada/comité: diferencia absoluta mediana **0,23 puntos porcentuales**, p90 **0,60**.

Por tanto, el 10% elimina más consensos triviales sin alterar materialmente el indicador respecto de un filtro de 5%.

### Sensibilidad 10% → 20%

La diferencia mediana sigue siendo pequeña, pero el 20% reduce más el denominador y vuelve particularmente inestables algunos casos con historia breve en una bancada. No ofrece una ventaja interpretativa suficiente para desplazar al 10% como vista principal.

---

## 4. Efecto de retirar el propio voto

La versión anterior interna calculaba la moda incluyendo la decisión de la propia persona. La nueva versión pública utiliza leave-one-out.

En el umbral del 10%:

### Partido

Entre quienes siguen siendo comparables, la diferencia mediana respecto del cálculo inclusivo es apenas **−0,043 puntos porcentuales**. Sin embargo, cuatro integrantes pierden comparabilidad partidaria porque pertenecen a partidos con solo dos integrantes: al retirar su voto queda un solo par, insuficiente para hablar de posición predominante de un grupo.

### Bancada/comité

La diferencia mediana es **−0,011 puntos porcentuales** y nadie pierde comparabilidad por leave-one-out.

La conclusión es importante: leave-one-out no cambia artificialmente el panorama general, pero corrige justamente los casos donde la definición inclusiva era conceptualmente circular.

---

## 5. Umbral mínimo de evidencia individual

Para mostrar un porcentaje público se exigirán **al menos 20 votaciones comparables** dentro del universo principal del 10%.

### Si `comparisons >= 20`

Mostrar porcentaje y fracción absoluta:

> **Coincidió en X de Y votaciones comparables (Z%).**

### Si `1 <= comparisons < 20`

No mostrar porcentaje como resultado principal. Mostrar:

> **Evidencia todavía insuficiente.** Esta comparación se basa en solo Y votaciones desde que existe un grupo comparable.

La cifra puede permanecer disponible dentro de la metodología/evidencia, pero no se presenta como resumen estable.

### Si `comparisons = 0`

No mostrar 0%.

Para partido:

- si figura como independiente: **Sin comparación partidaria disponible.**
- si pertenece a un partido sin suficientes pares comparables: **Su partido no tiene suficientes pares comparables para construir este indicador.**

Para bancada/comité:

- **Sin bancada/comité comparable en las votaciones observadas.**

---

## 6. Visualización recomendada

Dos tarjetas paralelas o apiladas según ancho de pantalla.

### Tarjeta A — Partido

- nombre del grupo o grupos observados;
- porcentaje grande, cuando `Y >= 20`;
- fracción `X de Y`;
- pequeña barra `coincidió / divergió`;
- botón **Ver coincidencias**;
- botón **Ver divergencias**.

### Tarjeta B — Bancada/comité

Misma estructura, conservando la denominación institucional del comité.

No se usará un ranking de parlamentarios ni categorías como “alta/baja disciplina”.

---

## 7. Texto público principal

Cuando existe evidencia suficiente:

> **En votaciones donde al menos 10% de la Cámara estuvo en el lado minoritario, [Nombre] coincidió con la posición más frecuente de los demás integrantes de [grupo] en [X] de [Y] votaciones comparables ([Z]%).**

Cuando hubo cambios de grupo durante el período:

> **La comparación sigue el partido o bancada/comité que la persona tenía en la fecha de cada votación. El período incluye más de una afiliación.**

---

## 8. Cómo leer el gráfico

> Comparamos la decisión de esta persona con la opción más frecuente entre los demás integrantes de su partido o bancada en la misma votación. Para no hacer circular la comparación, su propio voto se retira antes de identificar la posición predominante del grupo.

> Solo incluimos votaciones suficientemente disputadas en la Cámara y casos en que los pares del grupo permiten identificar una posición predominante única.

---

## 9. Qué significa

El indicador describe **similitud observada de voto respecto de un grupo institucional** en un conjunto definido de votaciones comparables.

Permite responder, de manera descriptiva:

- con qué frecuencia la persona vota igual que la posición predominante de sus pares;
- si la relación con partido y bancada es similar o distinta;
- en qué votaciones concretas coincide o diverge.

---

## 10. Qué no significa

Una coincidencia alta no permite distinguir por sí sola entre:

- preferencias políticas compartidas;
- selección ideológica de quienes integran un partido;
- deliberación;
- coordinación estratégica;
- disciplina formal;
- instrucciones de bancada;
- cálculo electoral;
- acuerdos legislativos.

Una divergencia tampoco es automáticamente:

- rebelión;
- indisciplina;
- ruptura política;
- voto de conciencia.

El indicador observa el resultado del voto, no la causa de ese resultado.

---

## 11. Por qué partido y bancada pueden diferir

El partido y la bancada/comité son objetos institucionales distintos.

- Una bancada puede reunir integrantes de varios partidos e independientes.
- Un independiente puede carecer de partido comparable y sí tener comité comparable.
- Una persona puede cambiar de partido o bancada durante la legislatura.

Por eso ambas cifras se calculan separadamente y utilizando `party_at_vote` y `caucus_at_vote`, nunca la afiliación actual aplicada retrospectivamente a toda la serie.

---

## 12. Drill-down de evidencia

Cada tarjeta debe permitir abrir dos conjuntos:

### Coincidencias

Listado de votaciones donde:

- la persona registró Afirmativo, En Contra o Abstención;
- sus pares tenían una moda única después de retirar su voto;
- el lado minoritario de la Cámara alcanzó al menos 10%;
- su opción fue igual a la moda de sus pares.

### Divergencias

Mismo universo, pero la opción de la persona fue distinta de la moda de sus pares.

Cada registro debe mostrar:

- fecha;
- boletín;
- título del proyecto;
- objeto votado cuando esté disponible;
- opción de la persona;
- posición predominante de los pares;
- grupo usado en esa fecha;
- resultado general de la votación;
- enlace a la votación oficial.

La interfaz utilizará el mismo catálogo público de roll calls del Módulo A para evitar duplicar metadatos legislativos.

---

## 13. Casos especialmente informativos detectados por la auditoría

### Cristian Contreras Radovic

Su comparación partidaria en el corte del 10% dispone de 254 observaciones y arroja 62,60%. En cambio, su comparación con comité dispone de solo 11 observaciones debido a su trayectoria entre `Comité Partido de la Gente` y `Fuera del Comité Partido de la Gente`. La regla pública mostrará el dato partidario, pero marcará el de bancada como **evidencia insuficiente**.

### Roberto Arroyo Muñoz

La comparación partidaria dispone de 144 observaciones; la comparación con comité solo de 16 debido a su trayectoria entre `Comité Partido de la Gente` y `Por definir`. De nuevo, la tarjeta partidaria puede publicarse y la de bancada no debe resumirse en un porcentaje.

### Independientes

Un independiente no recibe 0% de partido. La tarjeta explica que no existe grupo partidario formal comparable y puede mostrar su relación con la bancada/comité cuando sí sea estimable.

### Partidos de dos integrantes

Leave-one-out vuelve no comparable la relación partidaria porque, una vez retirado el voto de la persona, queda un solo par. Esto es deliberado: coincidencia con una sola persona no se presenta como posición predominante de un partido.

---

## 14. Estado de publicación

### Regla conceptual

**CERRADA.**

### Leave-one-out

**AUDITADO Y SUPERADO.**

### Umbral principal 10%

**AUDITADO Y ADOPTADO PARA LA VISTA PÚBLICA.**

### Mínimo de 20 comparaciones

**ADOPTADO.**

### Lenguaje autorizado

**Coincidencia con la posición predominante de sus pares / partido / bancada.**

### Lenguaje no autorizado

**Disciplina, rebelión, lealtad, obediencia** como equivalentes directos del indicador.

---

## 15. Principio interpretativo final

La afirmación autorizada es:

> **En un conjunto explícito de votaciones suficientemente disputadas, podemos observar con qué frecuencia una persona tomó la misma decisión que la posición más frecuente de los demás integrantes de su partido o bancada/comité.**

La afirmación no identifica por qué votaron de esa manera y no convierte la similitud observada en una explicación causal de disciplina partidaria.
