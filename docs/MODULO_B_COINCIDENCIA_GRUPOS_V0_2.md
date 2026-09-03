# Módulo B · Coincidencia con partido y bancada/comité · v0.2

**Proyecto:** Conoce a tu parlamentario  
**Cámara:** Cámara de Diputadas y Diputados de Chile, período 2026–2030  
**Estado:** **CERRADO, IMPLEMENTADO Y DESPLEGADO**  
**Corte auditado:** 364 votaciones nominales de Sala y 56.420 registros nominales, hasta el 1 de septiembre de 2026  
**Supersede:** `MODULO_B_COINCIDENCIA_GRUPOS_V0_1.md`

## 1. Pregunta pública

> **Cuando existe una posición predominante entre los demás integrantes de su grupo, ¿con qué frecuencia esta diputada o diputado vota de la misma manera?**

La ficha muestra por separado:

- **Con su partido**;
- **Con su bancada o comité**.

La separación es sustantiva. Partido y comité parlamentario son objetos institucionales distintos y se determinan según la afiliación vigente **en la fecha de cada votación**.

## 2. Regla metodológica definitiva

La versión pública adopta simultáneamente cuatro reglas.

### 2.1 Leave-one-out

El voto de la persona se retira antes de construir el comparador. Para cada votación:

1. se identifica su partido o bancada/comité vigente en esa fecha;
2. se elimina su propia decisión de los conteos del grupo;
3. se requieren al menos **dos decisiones sustantivas de pares**;
4. se exige una **moda única** entre esos pares;
5. solo entonces se compara la decisión individual con la posición predominante.

Esto evita que la decisión de la propia persona ayude a definir aquello con lo que luego se la compara. En partidos de solo dos integrantes, retirar el propio voto deja un único par y, por diseño, no se presenta ese caso como una “posición predominante del partido”.

### 2.2 Decisiones sustantivas

Se comparan:

- Afirmativo;
- En Contra;
- Abstención.

No se convierten en coincidencia ni divergencia:

- No Vota;
- Dispensado.

### 2.3 Umbral público de competitividad

La vista principal utiliza votaciones donde el lado minoritario entre **Afirmativo y En Contra** representa al menos **10% de los votos binarios de la Cámara**.

El 10% no es un umbral normativo. Es un filtro descriptivo destinado a evitar que votaciones casi unánimes inflen mecánicamente la coincidencia.

Las sensibilidades 0%, 5%, 10% y 20% permanecen disponibles internamente.

### 2.4 Mínimo de evidencia individual

- `comparisons >= 20`: se publica porcentaje y fracción absoluta;
- `1–19`: se muestra **Evidencia todavía insuficiente**, sin porcentaje principal;
- `0`: se muestra **Sin comparación disponible**, nunca 0%.

## 3. Auditoría del umbral 10%

### Partido

- integrantes con al menos una comparación: **121**;
- comparaciones: **29.147**;
- coincidencias: **27.922**;
- coincidencia ponderada: **95,80%**;
- mediana de comparaciones: **251**;
- percentil 10: **216**;
- integrantes con menos de 20 comparaciones: **0**.

### Bancada/comité

- integrantes con al menos una comparación: **152**;
- comparaciones: **36.440**;
- coincidencias: **34.662**;
- coincidencia ponderada: **95,12%**;
- mediana de comparaciones: **249**;
- percentil 10: **219,2**;
- integrantes con menos de 20 comparaciones: **2**.

## 4. Sensibilidad

### 5% → 10%

El cambio individual es pequeño:

- partido: diferencia absoluta mediana **0,16 pp**, p90 **0,56 pp**;
- bancada/comité: diferencia absoluta mediana **0,23 pp**, p90 **0,60 pp**.

Por tanto, 10% elimina más consensos triviales sin alterar materialmente la lectura respecto de 5%.

### 10% → 20%

La diferencia mediana continúa siendo pequeña, pero 20% reduce denominadores y vuelve frágiles algunos casos con trayectorias breves en un comité. No ofrece una ventaja suficiente para reemplazar el 10% como vista pública.

## 5. Efecto de leave-one-out

Frente al cálculo inclusivo anterior, en el corte del 10%:

- partido: diferencia mediana LOO − inclusivo **−0,043 pp**;
- bancada/comité: diferencia mediana **−0,011 pp**.

El patrón agregado prácticamente no cambia, pero se corrigen los casos conceptualmente circulares. Cuatro integrantes dejan de tener comparación partidaria porque, una vez retirado su voto, no queda un conjunto suficiente de pares.

## 6. Lenguaje autorizado

La expresión pública es:

> **Coincidencia con la posición predominante de sus pares.**

El indicador describe **similitud observada de voto**.

No se usarán como equivalentes automáticos:

- disciplina;
- indisciplina;
- rebelión;
- lealtad;
- obediencia.

Una coincidencia alta puede ser compatible con preferencias compartidas, selección partidaria, deliberación, coordinación, disciplina, acuerdos u otros mecanismos. El indicador no identifica la causa.

## 7. Tratamiento de casos especiales

### Independientes

No reciben 0% de coincidencia partidaria. Si no existe partido formal comparable, la ficha lo explica y puede mostrar de manera independiente la relación con su bancada/comité.

### Cambios de afiliación

La comparación utiliza `party_at_vote` y `caucus_at_vote`. Nunca aplica retroactivamente la afiliación actual a toda la serie histórica.

### Evidencia escasa

Los casos con menos de 20 comparaciones conservan su evidencia auditable, pero no reciben un porcentaje público principal.

## 8. Implementación pública

La ficha contiene dos tarjetas paralelas:

- **Con su partido**;
- **Con su bancada o comité**.

Cuando existe evidencia suficiente, cada tarjeta muestra:

- porcentaje;
- `X de Y` comparaciones;
- barra coincidencia/divergencia;
- botón **Ver coincidencias**;
- botón **Ver divergencias**.

Cada registro del drill-down muestra:

- fecha;
- boletín;
- título del proyecto;
- objeto votado cuando existe;
- opción individual;
- posición predominante leave-one-out;
- grupo vigente usado en la comparación;
- resultado general;
- enlace a la votación oficial.

El catálogo de roll calls se comparte con el Módulo A para no duplicar metadatos.

## 9. Arquitectura de evidencia y rendimiento

La primera implementación usaba un único archivo de detalle de aproximadamente 3,4 MB. Esa arquitectura fue reemplazada antes del cierre.

La versión definitiva genera:

- **155 archivos de evidencia**, uno por integrante histórico observado en el corte;
- ruta pública: `assets/data/modal_agreement/{id}.json`;
- archivo máximo en el corte auditado: **40.488 bytes**;
- archivo monolítico antiguo: **eliminado**.

El navegador descarga el detalle de una persona **solo cuando el usuario abre la evidencia**. Además, el frontend verifica que el `id` contenido en el shard corresponda a la ficha abierta.

La generación está automatizada por `.github/workflows/build_modal_agreement_public.yml`. El workflow persiste altas, modificaciones y eliminaciones de shards y vuelve a generar los diagnósticos públicos.

## 10. Auditoría de integridad de los activos públicos

Corte de cierre:

- perfiles: **155**;
- detalle esperado partido: **29.147** filas;
- detalle generado partido: **29.147**;
- detalle esperado bancada/comité: **36.440**;
- detalle generado bancada/comité: **36.440**;
- relaciones de lookup faltantes: **0**;
- archivos de detalle: **155**;
- monolito legado eliminado: **sí**.

Estados públicos:

### Partido

- disponibles: **121**;
- no disponibles: **34**.

### Bancada/comité

- disponibles: **150**;
- evidencia insuficiente: **2**;
- no disponibles: **3**.

## 11. Casos de control

### René Alinco Bustos

No tiene comparación partidaria válida como independiente, pero sí conserva comparación con su comité. El shard público contiene `party: []` y evidencia de bancada/comité.

### Roberto Arroyo Muñoz

Tiene **144** comparaciones partidarias y solo **16** de comité en el corte del 10%. La primera tarjeta puede publicar porcentaje; la segunda debe mostrar **Evidencia todavía insuficiente**.

### Boris Barrera Moreno

El shard individual conserva el universo de evidencia de partido y comité y permite inspeccionar las comparaciones sin descargar los datos de los otros 154 perfiles.

## 12. Estado final

- Regla conceptual: **CERRADA**.
- Leave-one-out: **AUDITADO Y SUPERADO**.
- Umbral 10%: **ADOPTADO**.
- Mínimo 20 comparaciones: **ADOPTADO**.
- Casos límite: **AUDITADOS**.
- Drill-down: **IMPLEMENTADO**.
- Evidencia fragmentada por parlamentario: **IMPLEMENTADA**.
- Automatización: **ACTIVA**.
- Despliegue público: **SUPERADO**.

## 13. Principio interpretativo final

> **En un conjunto explícito de votaciones suficientemente disputadas, podemos observar con qué frecuencia una persona tomó la misma decisión que la posición más frecuente de los demás integrantes de su partido o bancada/comité.**

La afirmación no identifica por qué votaron de esa manera y no convierte la similitud observada en una explicación causal de disciplina partidaria.
