# Módulo D · Red de coautoría · v0.1

**Proyecto:** Conoce a tu parlamentario  
**Cámara:** Cámara de Diputadas y Diputados de Chile, período 2026–2030  
**Estado:** **CERRADO, IMPLEMENTADO Y DESPLEGADO**  
**Período observado:** desde el 11 de marzo de 2026  
**Corte de cierre:** 3 de septiembre de 2026

## 1. Pregunta pública

> **¿Con quién presenta proyectos?**

El módulo describe relaciones de coautoría formal entre diputadas y diputados en mociones originadas en la Cámara durante el período observado.

## 2. Definición de vínculo

Dos personas están conectadas cuando ambas figuran formalmente como autoras de una misma moción.

El peso de la relación es:

> **número de mociones distintas en que ambas personas aparecen juntas en la lista formal de autores.**

Por ejemplo, si A y B figuran juntos en cuatro boletines, el peso de su vínculo es 4.

## 3. Unidad relacional y advertencia de no aditividad

La unidad del módulo D es una **relación entre dos autores**, no una moción.

Una moción con diez autores genera 45 pares de coautoría y, desde la perspectiva de cada autor, nueve vínculos asociados a esa misma iniciativa.

Por ello:

> **no se debe sumar el peso de todas las relaciones de una persona para obtener su número de mociones.**

El número de mociones se informa en el Módulo C. El D responde quién aparece junto a quién y cuántas veces se repite cada pareja.

## 4. Universo

La red pública se reconstruye exclusivamente desde mociones que cumplen:

- origen parlamentario;
- tipo `Moción`;
- origen en Cámara de Diputados;
- ingreso desde el 11 de marzo de 2026;
- autores formales identificados como diputados.

En el corte de cierre:

- mociones de Cámara elegibles: **305**;
- nodos de diputados: **155**;
- aristas diputado–diputado: **3.346**;
- diputados sin ningún coautor: **0**.

## 5. Reconciliación con la red derivada

El constructor público reconstruye todas las parejas directamente desde `bill_authors.csv` y `projects.csv` y compara el resultado con `coauthorship_edges.csv`.

Corte de cierre:

- aristas reconstruidas: **3.346**;
- aristas esperadas: **3.346**;
- discrepancias de peso: **0**.

El workflow falla si la reconstrucción deja de coincidir con la capa derivada auditada.

## 6. Estructura observada y decisión de visualización

La red de coautoría es demasiado amplia para que una estrella de pocos nodos represente honestamente la estructura completa.

Número de coautores distintos por perfil:

- mínimo: **1**;
- mediana: **41**;
- percentil 90: **64,6**;
- máximo: **96**.

Para el perfil mediano, aproximadamente **60%** de los coautores aparecen en una única moción compartida.

La concentración de intensidad en los vínculos superiores es limitada:

- top 5: cobertura mediana **29,95%**;
- top 8: **42,59%**;
- top 10: **49,15%**;
- top 12: **54,55%**;
- top 15: **61,64%**.

La cobertura se calcula sobre la suma de pesos relacionales, no sobre mociones únicas.

### Decisión

No se presenta un gráfico de top 8/top 10 como si fuese “la red”.

La ficha contiene:

1. una síntesis titulada **Vínculos más repetidos**, con hasta 8 relaciones;
2. una advertencia explícita de que es una selección parcial;
3. acceso a **todos los coautores**;
4. evidencia por vínculo hasta los boletines concretos.

## 7. Resumen individual

La ficha muestra tres descriptivos:

- **Coautores distintos:** personas con al menos una moción compartida;
- **Vínculos recurrentes:** coautores con dos o más mociones compartidas;
- **Vínculos de una moción:** coautores que aparecen juntos una sola vez.

En el perfil mediano del corte:

- coautores distintos: **41**;
- recurrentes: **17**;
- de una sola moción: **26**.

Los dos últimos valores se calculan por perfil; no se interpretan normativamente.

## 8. Intensidad de vínculos

El vínculo diputado–diputado más fuerte en el corte tiene **17 mociones compartidas** y corresponde a Eduardo Durán Salinas y Ximena Ossandón Irarrázabal.

El máximo individual no se convierte en una puntuación de influencia, centralidad política ni cercanía ideológica.

## 9. Qué significa la coautoría

La afirmación autorizada es:

> **Estas dos personas figuran formalmente como autoras de una o más mociones comunes.**

La repetición permite describir que la relación formal aparece en más boletines.

## 10. Qué no significa

Una arista de coautoría no demuestra automáticamente:

- amistad;
- afinidad ideológica;
- pertenencia a una misma facción;
- cercanía personal;
- coordinación estable;
- disciplina;
- acuerdo general en votaciones;
- influencia causal de una persona sobre otra;
- igualdad en el trabajo de redacción.

Por esta razón, los vínculos no se colorean por ideología ni se transforman en un ranking de influencia.

## 11. Evidencia pública

Al abrir la red completa, cada coautor muestra:

- nombre;
- número de mociones compartidas;
- primera y última fecha de coautoría observada;
- enlace a su ficha cuando existe un perfil público vigente;
- botón para abrir las mociones concretas.

Cada moción compartida conserva:

- boletín;
- fecha;
- título;
- número total de autores formales;
- estado registrado;
- enlace a la tramitación oficial.

## 12. Arquitectura y rendimiento

La primera versión de los shards repetía el título y metadatos completos de una moción dentro de cada vínculo, generando un máximo cercano a 102 KB por perfil y aproximadamente 6,2 MB en total.

Antes de publicar, la estructura fue normalizada a:

- un catálogo de mociones por perfil;
- referencias `billIds` dentro de cada vínculo.

Resultado final:

- shards: **155**;
- tamaño mínimo: **650 bytes**;
- tamaño máximo: **31.456 bytes**;
- tamaño total: **1.949.636 bytes**.

La evidencia de un perfil se descarga solo cuando el usuario solicita la red completa.

## 13. Casos de control

### Cristian Contreras Radovic

Tiene un único coautor en el corte, Guillermo Valdés Carmona, sostenido por una sola moción: boletín 18586-11. El módulo representa una red mínima sin inventar vínculos adicionales.

### Patricio Briones Moller

Tiene **96 coautores distintos**, el máximo del corte. Este caso motivó no utilizar una estrella top-K como representación de la red completa.

## 14. Automatización

La capa pública se genera mediante:

`.github/workflows/build_public_coauthorship_module.yml`

La auditoría de densidad y cobertura top-K queda reproducible mediante:

`.github/workflows/audit_public_coauthorship_module.yml`

## 15. Estado final

- definición de arista: **CERRADA**;
- peso de vínculo: **CERRADO**;
- reconciliación con red derivada: **SUPERADA**;
- auditoría de densidad: **SUPERADA**;
- decisión top-K: **CERRADA COMO SÍNTESIS PARCIAL**;
- lista completa: **IMPLEMENTADA**;
- evidencia por boletín: **IMPLEMENTADA**;
- normalización de shards: **IMPLEMENTADA**;
- automatización: **ACTIVA**;
- despliegue público: **SUPERADO**.

## 16. Principio interpretativo final

> **La red muestra con qué otras personas una diputada o diputado comparte autoría formal de mociones y cuántas veces se repite cada pareja.**

No convierte la firma conjunta en una inferencia automática sobre ideología, amistad, influencia o coordinación política estable.
