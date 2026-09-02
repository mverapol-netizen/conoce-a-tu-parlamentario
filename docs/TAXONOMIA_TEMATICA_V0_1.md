# Taxonomía temática legislativa v0.1 · BORRADOR

Esta taxonomía es una capa **analítica derivada** y no reemplaza ninguna categoría oficial de la Cámara. La versión 0.1 se crea antes de clasificar masivamente los proyectos para poder auditar cobertura, fronteras conceptuales y casos difíciles.

## Principios

1. **Clasificación múltiple:** un proyecto puede pertenecer a más de una macroárea.
2. **Tema principal + temas secundarios:** cuando corresponda se conservará un tema principal y cero o más secundarios.
3. **Fuente separada de inferencia:** título, texto de iniciativa, ministerios, comisiones y otros metadatos se conservarán como señales independientes.
4. **No usar partido, autor o bloque político como señal temática.**
5. **No confundir instrumento con materia:** por ejemplo, una reforma constitucional puede tratar principalmente seguridad, educación o pensiones.
6. **Versionado:** toda clasificación debe registrar la versión de taxonomía con la que fue producida.
7. **Trazabilidad:** una etiqueta automática debe conservar método, confianza y evidencia utilizada.
8. **Revisión humana:** los casos de baja confianza o verdaderamente multidimensionales podrán marcarse para revisión.

## Macroáreas candidatas

| Código | Macroárea | Alcance orientativo |
|---|---|---|
| EST | Estado, Constitución y sistema político | Constitución, órganos del Estado, sistema electoral, partidos, probidad, transparencia, administración pública |
| SEG | Seguridad pública, crimen y defensa | Policía, crimen organizado, armas, orden público, inteligencia, defensa nacional |
| JUS | Justicia y derechos fundamentales | Procesos judiciales, derecho penal/procesal, acceso a justicia, derechos civiles y garantías |
| ECO | Economía, Hacienda y sistema financiero | Presupuesto, impuestos, deuda, banca, mercado financiero, política fiscal y macroeconómica |
| TRA | Trabajo, empleo y relaciones laborales | Código del Trabajo, empleo, negociación, condiciones laborales, remuneraciones |
| SPS | Pensiones y seguridad social | Pensiones, cotizaciones, seguros sociales, prestaciones previsionales |
| SAL | Salud | Sistema sanitario, medicamentos, salud pública, prestadores, prevención y enfermedades |
| EDU | Educación | Educación escolar, superior, técnico-profesional, convivencia educativa, docentes |
| SOC | Desarrollo social, pobreza y cuidados | Transferencias, vulnerabilidad, discapacidad, cuidados, inclusión y protección social |
| FAM | Niñez, familia, género y diversidad | Infancia, adolescencia, familia, violencia de género, igualdad y diversidad |
| VIV | Vivienda, urbanismo y territorio | Vivienda, suelo, planificación urbana, construcción, propiedad urbana y emergencias habitacionales |
| AMB | Medio ambiente, agua y cambio climático | Protección ambiental, biodiversidad, aguas, emisiones, residuos, cambio climático |
| ENM | Energía, minería y recursos naturales | Energía, combustibles, minería, concesiones y recursos naturales no agrícolas |
| AGR | Agricultura, pesca y mundo rural | Agricultura, ganadería, pesca, acuicultura, silvicultura y desarrollo rural |
| INF | Transporte, obras públicas e infraestructura | Transporte terrestre/aéreo/marítimo, carreteras, puertos, obras públicas e infraestructura |
| CTD | Ciencia, tecnología y digitalización | Innovación, IA, datos, ciberseguridad, firma electrónica, telecomunicaciones y plataformas digitales |
| CUL | Cultura, patrimonio, deporte y medios | Cultura, patrimonio, artes, deporte, medios públicos y comunicación cultural |
| COM | Comercio, industria, consumidores y competencia | Empresas, comercio, permisos económicos, protección al consumidor, libre competencia |
| INT | Relaciones exteriores, migración y fronteras | Tratados, cooperación internacional, migración, extranjería, fronteras y diáspora |
| REG | Gobiernos subnacionales y descentralización | Municipios, gobiernos regionales, competencias territoriales y financiamiento subnacional |

## Regla para proyectos constitucionales

`EST` no se asigna automáticamente por el solo hecho de modificar la Constitución. Si una reforma constitucional busca, por ejemplo, reconocer un derecho sanitario, su tema sustantivo puede ser `SAL` y eventualmente `EST` como secundario si el diseño institucional es central al proyecto.

## Regla para proyectos penales

`JUS` y `SEG` se distinguen. Un cambio procesal o de garantías puede ser principalmente `JUS`; una reforma centrada en persecución del crimen organizado, armas u orden público puede ser `SEG`, con `JUS` como tema secundario cuando corresponda.

## Regla para proyectos económicos sectoriales

No todo proyecto con impacto fiscal es `ECO`. Un proyecto de educación con informe financiero sigue siendo principalmente `EDU`. `ECO` se usa cuando la política fiscal, tributaria, presupuestaria o financiera es sustantiva y no solo instrumental.

## Esquema de salida previsto

La futura tabla `project_topics.csv` tendrá formato largo:

```text
boletin
topic_code
topic_label
role                 # principal / secundario
method               # humano / reglas / modelo / híbrido
confidence           # 0-1 cuando exista
source_text_type      # título / iniciativa / mensaje / etc.
taxonomy_version     # v0.1, v0.2...
review_status         # pendiente / revisado
classified_at
```

## Qué falta antes de usar esta taxonomía

- Auditar disponibilidad del texto completo o parcial de las iniciativas.
- Revisar una muestra estratificada de mensajes y mociones.
- Identificar temas que la lista actual separe demasiado o mezcle indebidamente.
- Construir un pequeño gold standard humano antes de evaluar clasificación automática.
- Definir reglas para proyectos refundidos y proyectos con múltiples objetos.

**Estado:** borrador metodológico; no usar aún para estadísticas públicas del sitio.
