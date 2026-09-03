# Conoce a tu parlamentario

Herramienta cívica y politológica para conectar a una persona con sus representantes en la Cámara de Diputadas y Diputados de Chile y explorar, con evidencia auditable, distintas dimensiones de su actividad legislativa y del comportamiento de la Cámara.

## Qué ofrece la versión pública

### Tu distrito

1. La persona selecciona su **región** y **comuna**.
2. El sitio identifica automáticamente su **distrito electoral**.
3. Muestra las diputadas y diputados que representan ese territorio.
4. Desde cada representante se puede abrir una ficha legislativa estable.

### Hemiciclo

`hemiciclo.html` presenta los **155 escaños** como un mapa interactivo de fuerzas. Distingue deliberadamente:

- partido;
- bancada o Comité Parlamentario;
- independientes adscritos a una bancada, sin presentarlos como militantes;
- clasificación editorial entre oficialismo, oposición y no alineados.

El gráfico representa **distribución de fuerzas**, no la ubicación física exacta de los escaños en la Sala.

### Fichas legislativas

Las fichas públicas incluyen actualmente cuatro módulos metodológicamente cerrados:

- **A · Participación y decisiones de voto:** oportunidades efectivas de votación, con Afirmativo, En Contra, Abstención, No Vota y Dispensado preservados por separado y drill-down a la evidencia oficial.
- **B · Coincidencia con partido y bancada/comité:** comparación leave-one-out con la posición predominante de pares, umbral público de minoría binaria ≥10% y mínimo de 20 comparaciones para publicar porcentaje.
- **C · Iniciativa legislativa:** mociones originadas en Cámara en las que la persona figura formalmente como autor/a, distinguiendo autoría individual y compartida.
- **D · Coautoría:** relaciones formales entre autores de una misma moción, con acceso a los boletines que sostienen cada vínculo.

Estos módulos describen comportamiento observable. No se transforman en un puntaje general de desempeño.

### Patrones de voto · laboratorio W-NOMINATE

`wnominate.html` es un **laboratorio público experimental**, separado de las fichas cerradas. Permite explorar:

- W-NOMINATE 1D como patrón espacial principal de trabajo;
- una vista 2D explícitamente exploratoria;
- filtros territoriales, partidarios y por parlamentario;
- contexto temático del proyecto asociado a cada votación;
- bootstrap por proyectos como diagnóstico de robustez;
- descarga PNG y modo pantalla completa.

La estimación base usa `lop = 2.5%` y `minvotes = 20`, con 276 votaciones elegibles y 154 de 155 integrantes estimados.

La visualización pública invierte el signo técnico de D1 para mantener la convención izquierda → derecha (`D1 visual = -D1 técnico`). La lectura izquierda–derecha está fuertemente respaldada por la auditoría sustantiva interna, pero sigue siendo **provisional** hasta cerrar los gates multimétodo y temporales pendientes.

La segunda dimensión permanece sin etiqueta política sustantiva.

## Principios metodológicos

El proyecto mantiene separadas cuatro capas:

1. **datos primarios oficiales**;
2. **clasificaciones analíticas derivadas**;
3. **indicadores descriptivos**;
4. **modelos estadísticos e interpretaciones politológicas**.

Una capa derivada nunca reemplaza silenciosamente la fuente primaria.

Regla editorial general:

> Cada gráfico debe responder una pregunta concreta, formular una conclusión limitada y permitir reconstruir la evidencia y el método que la sostienen.

## Cobertura actual

- 16 regiones.
- 28 distritos electorales.
- 346 comunas.
- 155 integrantes de la Cámara 2026–2030.
- 155 fotografías oficiales almacenadas localmente.
- perfiles, partido, bancada/comité, distrito, región y contacto institucional.
- base legislativa incremental desde el 11 de marzo de 2026.
- votaciones nominales de Sala, proyectos, autorías, tramitación, afiliaciones históricas y capas derivadas.

## Fuentes

La base se construye y contrasta con fuentes públicas oficiales:

- Servicio Electoral de Chile (Servel);
- Biblioteca del Congreso Nacional (BCN);
- Cámara de Diputadas y Diputados de Chile;
- Portal de Datos Abiertos del Congreso.

## Actualización

El repositorio utiliza GitHub Actions para sincronización de perfiles y actualización legislativa. Los hechos institucionales pueden actualizarse automáticamente cuando la fuente lo permite; clasificaciones editoriales como oficialismo/oposición/no alineado requieren revisión pública separada.

## Estado científico del laboratorio espacial

W-NOMINATE 1D es actualmente el benchmark descriptivo espacial del proyecto. Antes de convertir su coordenada en un indicador individual cerrado dentro de las fichas todavía deben completarse, entre otros:

- IRT bayesiano 2PL 1D;
- Optimal Classification;
- estabilidad temporal con ventanas comparables;
- contrato final de incertidumbre/robustez;
- cierre formal de la interpretación pública de D1.

La taxonomía temática también mantiene pendiente una validación externa/formal por macroárea. Por eso el filtro de la página se presenta como **contexto temático del proyecto**, no como materia oficial ni clasificación exacta de cada roll call.

## Próximas capas

La expansión natural del proyecto incluye:

- materias de iniciativas, una vez validada la taxonomía;
- comisiones y roles institucionales;
- estado de tramitación de mociones;
- actividad fiscalizadora;
- indicaciones/enmiendas cuando exista atribución individual fiable;
- apoyo al Ejecutivo solo después de reconstruir su posición en cada votación;
- validación multimétodo y temporal del modelo espacial.

El objetivo es pasar de **“¿quién me representa?”** a **“¿qué hace mi representante?”**, y además ofrecer una lectura transparente de **cómo se estructura empíricamente el comportamiento legislativo de la Cámara**.