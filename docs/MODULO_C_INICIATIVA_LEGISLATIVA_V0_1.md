# Módulo C · Iniciativa legislativa · v0.1

**Proyecto:** Conoce a tu parlamentario  
**Cámara:** Cámara de Diputadas y Diputados de Chile, período 2026–2030  
**Estado:** **CERRADO, IMPLEMENTADO Y DESPLEGADO**  
**Período observado:** desde el 11 de marzo de 2026  
**Corte de cierre:** datos generados el 3 de septiembre de 2026

## 1. Pregunta pública

> **¿Qué proyectos ha presentado?**

El módulo describe las **mociones** en las que una diputada o diputado figura formalmente en la lista de autores registrada por la Cámara de Diputadas y Diputados.

No cuenta mensajes del Ejecutivo como si fueran iniciativas parlamentarias ni atribuye a una persona proyectos en los que no aparece formalmente como autora.

## 2. Unidad de análisis

La unidad pública es:

> **una moción × un diputado/a formalmente registrado como autor/a.**

Una misma moción puede, por tanto, contribuir a la cifra de varias personas cuando tiene coautoría. Para cada diputado, cada boletín se cuenta una sola vez.

El número total de relaciones diputado–moción no debe confundirse con el número de mociones únicas presentadas por la Cámara.

## 3. Universo público

Para ingresar al indicador deben cumplirse simultáneamente estas condiciones:

1. `origen_iniciativa = parlamentario`;
2. `tipo_iniciativa = Moción`;
3. `camara_origen = Cámara de Diputados`;
4. `fecha_ingreso >= 2026-03-11`;
5. la persona figura en `bill_authors.csv` como `author_chamber = Diputado`;
6. el ID corresponde a un perfil vigente en la ficha pública.

La base primaria conserva también autorías senatoriales y autorías históricas. Esas relaciones no se borran, pero no contaminan el contador público de una ficha de diputado.

## 4. Distinción entre autoría compartida e individual

### Autoría individual registrada

Una moción se clasifica como **autoría individual** cuando, después de deduplicar la lista formal de autores del boletín, existe una sola persona registrada como autora.

### Autoría compartida

Una moción se clasifica como **autoría compartida** cuando la lista formal contiene dos o más personas distintas.

La identidad que debe cumplirse para cada perfil es:

`mociones totales = autorías compartidas + autorías individuales`.

## 5. Qué significa la autoría formal

El indicador permite afirmar:

> **La Cámara registra a esta persona como autora o coautora formal de estas mociones.**

Esto describe una relación institucional verificable entre una persona y un boletín.

## 6. Qué no significa

La autoría formal no permite inferir por sí sola:

- quién redactó materialmente el texto;
- cuánto aportó cada coautor;
- quién negoció la iniciativa;
- quién tuvo la idea original;
- cuánto trabajo requirió;
- calidad normativa;
- importancia política;
- impacto;
- probabilidad de convertirse en ley;
- productividad legislativa global.

Por eso el módulo no construye rankings ni denomina a una persona “más productiva” por presentar más mociones.

## 7. Universo auditado en el corte de cierre

El corpus parlamentario general contiene **452 iniciativas parlamentarias** y **2.579 relaciones de autoría** entre Cámara y Senado.

Al aplicar el contrato público específico para fichas de diputados, el universo queda en:

- **155 perfiles actuales**;
- **305 mociones únicas originadas en la Cámara de Diputados**;
- **1.975 relaciones diputado–moción**;
- **1.937 relaciones correspondientes a mociones de autoría compartida**;
- **38 relaciones correspondientes a autorías individuales**;
- **155 perfiles con al menos una moción en el corte actual**;
- máximo observado: **39 mociones** para un perfil.

Las 452 iniciativas del corpus bicameral no deben utilizarse como denominador de la ficha de diputados.

## 8. Controles de integridad

El constructor público falla si detecta:

- relaciones autor–boletín duplicadas;
- una autoría de diputado sin proyecto correspondiente;
- una relación pública cuyo proyecto no sea una moción parlamentaria;
- una moción pública con cámara de origen distinta de Cámara de Diputados;
- un proyecto anterior al inicio del período;
- una inconsistencia `total != compartidas + individuales`;
- una diferencia entre el resumen público y `coauthorship_nodes.csv`.

En el corte de cierre:

- duplicados: **0**;
- proyectos faltantes: **0**;
- relaciones fuera del contrato: **0**;
- discrepancias con la capa de coautoría: **0**.

## 9. Tratamiento de reemplazos y perfiles con cero mociones

La salida pública parte del universo de perfiles actuales de `profiles.js`, no solo de quienes aparecen en `bill_authors.csv`.

Esto permite que un futuro diputado reemplazante que todavía no haya presentado mociones aparezca correctamente con **0 mociones** en vez de desaparecer del módulo.

En este indicador, a diferencia de una comparación partidaria inexistente, cero es un valor interpretable cuando el universo fue observado correctamente.

La interfaz acompaña el cero con una advertencia: no registrar mociones no equivale a ausencia de trabajo legislativo.

## 10. Diseño público

La ficha muestra tres cifras:

1. **Mociones con autoría registrada**;
2. **Autoría compartida**;
3. **Autoría individual**.

Una barra de composición representa compartidas frente a individuales. No representa calidad, éxito ni peso político.

El botón **Ver mociones** abre el listado de evidencia.

## 11. Drill-down de evidencia

Cada moción muestra:

- fecha de ingreso;
- boletín;
- título oficial;
- número de autores formales;
- clasificación compartida/individual;
- estado de tramitación registrado en el corte;
- enlace a la tramitación oficial.

El estado del proyecto se presenta como metadato documental, no como indicador de éxito de la persona.

## 12. Arquitectura pública y rendimiento

Los datos agregados se cargan en `assets/js/initiatives.js`.

La evidencia se fragmenta en **155 archivos**, uno por perfil:

`assets/data/initiatives/{id}.json`

El navegador descarga el detalle de la persona solo cuando el usuario abre el listado. En el corte de cierre:

- archivo mínimo: **478 bytes**;
- archivo máximo: **15.242 bytes**;
- suma de shards: **786.705 bytes**.

El frontend verifica que el `id` del archivo descargado coincida con la ficha abierta.

## 13. Automatización

La construcción está automatizada mediante:

`.github/workflows/build_member_initiatives_public.yml`

Se activa cuando cambian:

- `bill_authors.csv`;
- `projects.csv`;
- `coauthorship_nodes.csv`;
- `profiles.js`;
- el propio constructor o workflow.

Las salidas se regeneran desde las capas auditadas y no requieren copia manual.

## 14. Casos de control

### Cristian Contreras Radovic

En el corte de cierre registra **12 mociones**:

- **1** compartida;
- **11** de autoría individual registrada.

El detalle reproduce cada boletín y su número formal de autores.

### Patricio Briones Moller

Registra **39 mociones**, el máximo del corte actual:

- **37** compartidas;
- **2** individuales.

Este caso prueba que el módulo soporta listados extensos sin cargar evidencia de otros perfiles.

## 15. Estado final

- definición de universo: **CERRADA**;
- unidad de conteo: **CERRADA**;
- compartida/individual: **CERRADA**;
- reconciliación con coautoría: **SUPERADA**;
- tratamiento de reemplazos: **IMPLEMENTADO**;
- drill-down: **IMPLEMENTADO**;
- evidencia fragmentada: **IMPLEMENTADA**;
- automatización: **ACTIVA**;
- despliegue público: **SUPERADO**.

## 16. Principio interpretativo final

> **El módulo muestra cuántas mociones registran formalmente a una persona como autora durante el período observado y distingue si esa firma aparece sola o junto a otros autores.**

No convierte el número de firmas en un juicio sobre productividad, calidad, influencia o éxito legislativo.
