# Arquitectura de educación parlamentaria · v0.1

**Proyecto:** Conoce a tu parlamentario  
**Sección pública futura:** `Entiende el Congreso`  
**Estado:** contrato editorial, pedagógico y técnico para implementación incremental  
**Fecha:** 3 de septiembre de 2026

## 1. Propósito

Esta arquitectura define cómo incorporar al sitio una capa de **educación parlamentaria rigurosa y progresiva**. El objetivo no es producir una enciclopedia paralela ni una colección de preguntas frecuentes aisladas. La nueva sección debe permitir que una persona pase desde una intuición elemental hasta una comprensión institucional, histórica y politológica suficientemente precisa, sin que la pedagogía sacrifique rigurosidad.

La regla central es:

> **La intuición inicial nunca debe ser falsa. Puede ser incompleta, pero cada nivel posterior debe precisar, corregir y problematizar lo anterior sin contradecirlo artificialmente.**

La segunda regla es:

> **Cada concepto institucional debe conectarse con una instancia real del Congreso y cada dato real debe poder devolver al usuario a la explicación del concepto que está observando.**

Por tanto, esta capa educativa no será un apéndice del sitio. Debe atravesar fichas, proyectos, votaciones, comisiones, partidos, distritos y futuras páginas de actividad parlamentaria.

---

# 2. Nueva puerta principal del sitio

Se crea una nueva sección principal:

## `Entiende el Congreso`

La navegación superior futura queda conceptualmente así:

- **Tu distrito**
- **Hemiciclo**
- **Patrones de voto**
- **Entiende el Congreso**

`Entiende el Congreso` será un **hub**, no una única página larga. Debe permitir tres formas de entrada simultáneas:

1. **Entrada por pregunta:** “¿Qué quieres entender?”
2. **Entrada por búsqueda conceptual:** buscar `comisión mixta`, `urgencia`, `qué hace un diputado`, etc.
3. **Entrada por recorrido guiado:** “Aprender desde el comienzo”.

---

# 3. Taxonomía principal de contenidos

La sección se organiza en ocho unidades mayores.

## A. Democracia y representación

Preguntas principales:

- ¿Para qué existe el Congreso?
- ¿Qué significa representar?
- ¿A quién representa una diputada o diputado?
- ¿Qué es un distrito?
- ¿Por qué un distrito elige varios representantes?
- ¿Qué papel cumplen los partidos en la representación?
- ¿Qué significa accountability electoral?
- ¿Qué diferencia hay entre autorización, representación descriptiva y representación sustantiva?

## B. Cámara y Senado

Preguntas principales:

- ¿Por qué Chile tiene dos cámaras?
- ¿Qué comparten Cámara y Senado?
- ¿Qué atribuciones son exclusivas de cada una?
- ¿Por qué tienen distinto número de integrantes y duración de mandato?
- ¿Cómo ha cambiado históricamente el bicameralismo chileno?
- ¿Qué ventajas y costos atribuye la literatura al bicameralismo?

## C. Cómo se hace una ley

Conceptos principales:

- mensaje;
- moción;
- iniciativa exclusiva;
- admisibilidad;
- cuenta;
- comisión;
- discusión general;
- discusión particular;
- indicación;
- informe;
- cámara de origen;
- cámara revisora;
- primer, segundo y tercer trámite;
- comisión mixta;
- urgencias;
- observaciones o veto;
- promulgación;
- publicación.

Pregunta rectora:

> **¿Cómo pasa una propuesta desde una idea o iniciativa hasta convertirse —eventualmente— en ley?**

## D. Cómo se organiza el Congreso

Conceptos principales:

- Mesa;
- Presidencia;
- Secretaría;
- comisiones permanentes;
- comisiones especiales;
- comisiones investigadoras;
- comisiones mixtas;
- bancadas;
- comités parlamentarios;
- jefaturas de comité;
- tabla;
- Orden del Día;
- tiempos de debate;
- agenda legislativa.

## E. Fiscalización y control

Conceptos principales:

- acuerdos y observaciones;
- solicitudes de antecedentes;
- oficios;
- interpelaciones;
- comisiones especiales investigadoras;
- acusación constitucional;
- control político;
- accountability;
- límites de competencia;
- diferencia entre fiscalizar, gobernar y juzgar.

## F. Partidos y poder político

Conceptos principales:

- partido;
- bancada;
- comité parlamentario;
- coalición;
- oficialismo;
- oposición;
- no alineados;
- cohesión;
- coincidencia;
- disciplina;
- mayorías;
- fragmentación;
- transfuguismo;
- voto personal y organización partidaria.

## G. Historia del Congreso

La historia tendrá una página propia, pero también será transversal a todas las unidades.

Hitos mínimos:

- 1811 — primer Congreso;
- 1812 — primer Senado;
- 1828 — consolidación del bicameralismo;
- 1833 — nuevo orden constitucional;
- 1891 — quiebre y predominio parlamentario;
- 1925 — reconfiguración presidencial y fiscalización;
- 1973 — disolución del Congreso;
- 1990 — reapertura democrática;
- 2005–2006 — fin de senadores designados y vitalicios y reformas de control;
- 2015 — reforma electoral;
- 2026 — Cámara y Senado actuales.

La historia no se presenta como una secuencia de efemérides. Cada hito debe responder una pregunta política.

Ejemplos:

- **1811:** ¿Quién podía hablar en nombre del país?
- **1828:** ¿Por qué dividir el Congreso en dos cámaras?
- **1891:** ¿Qué ocurre cuando Ejecutivo y Congreso disputan el poder?
- **1925:** ¿Cómo distinguir fiscalización de gobierno parlamentario?
- **1973:** ¿Puede existir legislación sin parlamento democrático?
- **1990:** ¿Qué significa restaurar el Congreso después de una ruptura autoritaria?

## H. Participación ciudadana

Esta unidad convierte comprensión institucional en capacidad de acción.

Preguntas principales:

- ¿Qué puede y qué no puede hacer un diputado por una persona?
- ¿Cuándo conviene contactar a un parlamentario?
- ¿Cuándo corresponde acudir a un municipio, ministerio, tribunal u otro órgano?
- ¿Cómo seguir un proyecto?
- ¿Cómo saber qué comisión estudia un tema?
- ¿Cómo contactar a representantes y comisiones?
- ¿Cómo interpretar una agenda legislativa?
- ¿Qué mecanismos institucionales de participación existen cuando corresponda?

---

# 4. Portada de `Entiende el Congreso`

La portada debe comenzar con la pregunta:

> **¿Qué quieres entender?**

No debe mostrar inmediatamente una lista exhaustiva de artículos.

## Puertas iniciales sugeridas

### ¿Para qué existe el Congreso?
Representación, decisiones colectivas, deliberación y control del poder.

### ¿Quién me representa?
Distritos, elecciones, partidos y representación política.

### ¿Cómo se convierte una idea en ley?
Iniciativas, comisiones, trámites, votaciones y promulgación.

### ¿Cómo controla la Cámara al Gobierno?
Oficios, interpelaciones, investigaciones y responsabilidad constitucional.

### ¿Quién organiza realmente la Cámara?
Mesa, comités, bancadas, comisiones y agenda.

### ¿Quién decide qué se vota?
Tabla, urgencias, prioridades, agenda y mayorías.

### ¿Cómo llegamos al Congreso actual?
Historia institucional de 1811 a 2026.

### ¿Qué puedo hacer como ciudadano?
Contacto, seguimiento de proyectos, comisiones y canales institucionales.

---

# 5. Recorrido guiado

La portada incluirá un botón:

> **Aprender desde el comienzo**

Recorrido recomendado v0.1:

1. ¿Para qué existe el Congreso?
2. ¿Quién representa a quién?
3. Cámara y Senado
4. ¿Cómo se eligen los parlamentarios?
5. ¿Cómo se hace una ley?
6. ¿Qué hacen las comisiones?
7. ¿Cómo fiscaliza la Cámara?
8. Partidos, bancadas y comités
9. Agenda y tabla
10. Mayorías y quórums
11. ¿Qué puede hacer realmente un diputado?
12. ¿Cómo puede participar un ciudadano?

El recorrido es recomendado, nunca obligatorio. Todas las páginas también deben ser navegables directamente.

---

# 6. Plantilla cognitiva común para cada página

Cada página educativa usará la misma arquitectura progresiva.

## Nivel 1 — La intuición

Una pregunta clara y una respuesta de dos o tres frases.

Ejemplo:

> **¿Qué es una comisión?**  
> Es un grupo más pequeño de parlamentarios que estudia determinadas materias con mayor detalle. Muchas decisiones legislativas son examinadas primero allí antes de llegar a la Sala.

La intuición debe ser correcta, aunque todavía incompleta.

## Nivel 2 — En pocas palabras

Tres a cinco hechos esenciales:

- para qué sirve;
- quién participa;
- qué puede hacer;
- qué no puede hacer;
- cuándo importa para un ciudadano.

## Nivel 3 — Cómo funciona realmente en Chile

Aquí entra la precisión normativa e institucional:

- Constitución;
- Ley Orgánica Constitucional del Congreso;
- Reglamento de la Cámara;
- Reglamento del Senado;
- procedimientos;
- quórums;
- excepciones;
- diferencias entre cámaras;
- cambios históricos relevantes.

## Nivel 4 — Míralo funcionando

Cada concepto debe enlazarse con datos reales del sitio cuando exista una instancia pública disponible.

Ejemplos:

- comisión → una comisión actual;
- moción → una moción real;
- votación particular → una votación real;
- bancada → una bancada actual;
- distrito → el distrito del usuario;
- tercer trámite → un proyecto que se encuentre o haya pasado por esa etapa.

## Nivel 5 — Qué significa y qué no significa

Bloque obligatorio contra inferencias intuitivas incorrectas.

Ejemplos:

- aprobar en general ≠ convertir el proyecto en ley;
- abstenerse ≠ ausentarse;
- pertenecer a un comité ≠ militar en el partido dominante del comité;
- fiscalizar ≠ gobernar;
- comisión investigadora ≠ tribunal penal;
- muchas mociones ≠ mejor legislador.

## Nivel 6 — Historia

Cápsula breve que responda:

> **¿Siempre funcionó así?**

Debe explicar cuándo apareció o cambió la institución y enlazar con la línea de tiempo general.

## Nivel 7 — Qué sabemos por evidencia

Hallazgos empíricos relevantes de ciencia política, historia o investigación legislativa.

No se confunden con la descripción normativa.

## Nivel 8 — Qué discuten los especialistas

Mapa de consensos, hipótesis y controversias.

La página no debe convertir una controversia académica en una verdad institucional.

## Nivel 9 — Fuentes y profundización

Debe incluir:

- fuentes normativas;
- fuentes institucionales;
- bibliografía académica;
- fecha de última revisión;
- responsable o versión editorial cuando corresponda.

---

# 7. Tipos epistemológicos visibles

La interfaz utilizará etiquetas consistentes para indicar qué tipo de afirmación está leyendo el usuario.

## `INSTITUCIÓN`

Regla, atribución o estructura respaldada directamente por Constitución, ley, reglamento o fuente institucional competente.

## `EVIDENCIA`

Hallazgo empírico proveniente de datos o investigación académica.

## `DEBATE`

Pregunta interpretativa, causal o normativa respecto de la cual existen posiciones diferentes o evidencia no concluyente.

## `HISTORIA`

Genealogía, cambio o antecedente histórico de una institución.

## `MITO FRECUENTE`

Confusión habitual que puede ser corregida de manera precisa.

### Regla editorial

Una afirmación `DEBATE` nunca debe presentarse visualmente como `INSTITUCIÓN`. Una inferencia propia del proyecto tampoco debe presentarse como si fuera una categoría oficial de la Cámara.

---

# 8. Glosario contextual

No se prioriza un glosario tradicional con cientos de entradas aisladas. Se implementa un **glosario contextual reutilizable**.

Conceptos como:

- moción;
- mensaje;
- indicación;
- bancada;
- comité parlamentario;
- comisión mixta;
- urgencia;
- quórum;
- tercer trámite;
- admisibilidad;

pueden aparecer acompañados por un indicador contextual `ⓘ`.

La interacción tendrá tres profundidades:

1. **Tooltip / popover:** definición de una o dos frases.
2. **Explicación breve:** panel con `qué es`, `qué no es`, `ejemplo`.
3. **Página completa:** acceso al dossier o sección pertinente.

Una definición se redacta una sola vez en la fuente de contenidos y se reutiliza donde corresponda.

---

# 9. Arquitectura de contenidos reutilizables

Los contenidos educativos no deben codificarse repetidamente dentro de múltiples páginas HTML.

Cada concepto debe tener un identificador estable y una estructura reutilizable.

Esquema conceptual mínimo:

```yaml
id: comite-parlamentario
titulo: ¿Qué es un Comité Parlamentario?
unidad: organizacion
resumen: ...
intuicion: ...
hechos_clave:
  - ...
como_funciona: ...
no_significa:
  - ...
historia: ...
evidencia:
  - ...
debates:
  - ...
fuentes:
  - ...
relaciones:
  - bancada
  - partido
  - mesa
  - tabla
instancias_reales:
  - ...
```

La implementación técnica puede usar JSON, JS u otra estructura estática compatible con GitHub Pages. La elección concreta se definirá en la fase de implementación, pero la separación contenido/interfaz es obligatoria.

---

# 10. Grafo conceptual

Cada concepto debe declarar relaciones con otros conceptos.

Ejemplos:

## Comisión

Conecta con:

- proyecto;
- indicación;
- informe;
- Sala;
- Hacienda;
- comisión mixta;
- especialización;
- partidos.

## Partido

Conecta con:

- elección;
- lista;
- bancada;
- comité;
- coalición;
- oficialismo/oposición;
- cohesión;
- disciplina.

## Fiscalización

Conecta con:

- oficio;
- solicitud de antecedentes;
- interpelación;
- comisión investigadora;
- Gobierno;
- acusación constitucional.

Al final de cada página aparecerá:

> **Sigue aprendiendo**

con dos a cuatro conceptos relacionados de manera substantiva, no enlaces genéricos.

---

# 11. Conexión bidireccional entre educación y datos

La nueva arquitectura separa dos tipos de página que deben enlazarse constantemente.

## Página educativa

Explica **qué es** una institución o procedimiento.

Ejemplo futuro:

`aprende/comisiones.html`

## Página de instancia real

Muestra **qué está haciendo hoy** un objeto concreto.

Ejemplo futuro:

`comision.html?id=salud`

Regla:

> **La página educativa explica el objeto; la página de datos muestra la instancia.**

Y debe funcionar en ambos sentidos.

Ejemplos:

- desde `comision.html?id=salud` → `¿Qué es una comisión?`;
- desde `aprende/comisiones.html` → `Ver Comisión de Salud hoy`;
- desde una votación de tercer trámite → `¿Qué significa tercer trámite?`;
- desde la explicación de tercer trámite → `Ver un caso real`.

---

# 12. Nuevos objetos navegables del sitio

El sitio ya no debe organizarse únicamente alrededor del parlamentario.

La arquitectura de largo plazo debe admitir como entidades navegables:

- **Parlamentario**
- **Distrito**
- **Partido**
- **Bancada / Comité**
- **Comisión**
- **Proyecto**
- **Votación**
- **Tema**
- **Concepto institucional**

Cada entidad puede enlazar con las demás.

Ejemplo:

`Tema Educación` → Comisión de Educación → proyectos → votaciones → parlamentarios → conceptos institucionales relevantes.

---

# 13. Separación de tres capas públicas

El proyecto tendrá tres familias de páginas que no deben confundirse.

## `Entiende el Congreso`

Explica **cómo funciona la institución**.

## Páginas de datos y exploración

Muestran **qué está ocurriendo o qué ocurrió** en el Congreso.

## `Datos y metodología`

Explica **cómo construimos, limpiamos, clasificamos y analizamos nuestros datos**.

Regla:

> explicar qué es una comisión no es lo mismo que explicar cómo el proyecto clasificó temáticamente un proyecto o recolectó una votación.

---

# 14. Historia transversal

Aunque exista una página general de historia, cada concepto debe incluir una cápsula:

> **¿Siempre fue así?**

Ejemplos:

- bicameralismo → 1828, 2005, 2015;
- fiscalización → 1925 y reforma de 2005;
- Senado → designados/vitalicios y reforma 2005–2006;
- sistema electoral → binominal y reforma 2015;
- trabajo distrital → evolución histórica correspondiente;
- comisiones → desarrollo histórico de especialización parlamentaria.

La historia debe ayudar a comprender la institución actual, no quedar aislada en un museo cronológico.

---

# 15. Búsqueda conceptual

La portada incluirá en una fase posterior un buscador:

> **Busca algo que quieras entender**

Ejemplos de consulta:

- `comisión mixta`
- `qué hace un diputado`
- `urgencia`
- `por qué hay Senado`
- `acusación constitucional`
- `aprobado en general`

El resultado debe priorizar:

1. respuesta breve;
2. conceptos relacionados;
3. botón **Profundizar**;
4. ejemplos reales cuando existan.

No se requiere IA generativa para la primera versión. El contenido puede ser un índice estructurado local y determinista.

---

# 16. Traducción contextual del lenguaje parlamentario

La capa educativa debe actuar como traductor institucional del sitio.

Ejemplo:

> **“Proyecto aprobado en general”**

Debe poder desplegar:

> La Cámara aprobó la idea de legislar. Esto no significa todavía que el proyecto sea ley ni que todos sus artículos hayan quedado aprobados.

Ejemplo:

> **“Suma urgencia”**

Debe explicar:

> Es una prioridad procedimental asignada por el Ejecutivo dentro de las reglas constitucionales; no significa que el proyecto esté aprobado.

Esta traducción contextual debe integrarse en proyectos, votaciones y agenda futura.

---

# 17. Diseño de lectura progresiva

Las páginas no deben ser muros de texto académicos.

Contenido visible inicialmente:

- pregunta;
- intuición;
- hechos clave;
- ejemplo real.

Contenido expandible:

- cómo funciona exactamente;
- qué no significa;
- historia;
- evidencia;
- debates;
- fuentes.

La progresividad no altera el contenido: **reduce carga cognitiva, no rigor**.

---

# 18. Usuarios y niveles de profundidad

No se implementarán modos artificiales tipo “niño”, “adulto” o “experto”.

La misma página permite tres comportamientos:

## Usuario casual

Lee:

- título;
- intuición;
- tres hechos clave.

## Ciudadano interesado

Lee además:

- funcionamiento institucional;
- ejemplos;
- límites.

## Estudiante, periodista o especialista

Puede llegar a:

- historia;
- evidencia;
- controversias;
- fuentes completas.

El sitio no produce versiones epistemológicamente distintas del mismo concepto.

---

# 19. URLs y estructura técnica preliminar

Propuesta inicial, sujeta a implementación:

```text
entiende.html

aprende/
├── para-que-existe-el-congreso.html
├── representacion.html
├── camara-y-senado.html
├── elecciones-y-distritos.html
├── como-se-hace-una-ley.html
├── comisiones.html
├── fiscalizacion.html
├── partidos-bancadas-comites.html
├── agenda-y-tabla.html
├── mayorias-y-quorums.html
├── historia-del-congreso.html
└── participacion-ciudadana.html
```

Entidades reales futuras:

```text
comision.html?id=...
proyecto.html?boletin=...
votacion.html?id=...
partido.html?id=...
comite.html?id=...
distrito.html?id=...
```

La estructura definitiva debe preservar URLs estables y enlaces profundos.

---

# 20. Fases de implementación

## Fase 1 — Esqueleto editorial y técnico

Crear:

- pestaña `Entiende el Congreso`;
- hub inicial;
- plantilla común de páginas;
- estilos epistemológicos `Institución / Evidencia / Debate / Historia / Mito frecuente`;
- estructura de contenidos reutilizable;
- glosario contextual mínimo;
- navegación `Sigue aprendiendo`.

## Fase 2 — Núcleo P0

Publicar las primeras seis páginas completas:

1. ¿Para qué existe el Congreso?
2. Cámara y Senado
3. ¿Quién te representa?
4. ¿Cómo se hace una ley?
5. ¿Qué puede hacer realmente un diputado?
6. ¿Cómo fiscaliza la Cámara?

Estas páginas deben contener fuentes normativas e investigación académica revisada.

## Fase 3 — Organización interna

Publicar:

- comisiones;
- partidos, bancadas y comités;
- agenda y tabla;
- mayorías y quórums.

## Fase 4 — Historia integrada

Implementar:

- timeline 1811–2026;
- cápsulas históricas en páginas conceptuales;
- vínculos entre hitos históricos y reglas actuales.

## Fase 5 — Navegación ciudadana

Implementar:

- ¿A quién debo contactar?;
- sigue un proyecto;
- hoy en la Cámara;
- seguimiento de comisiones;
- canales institucionales de participación;
- orientación sobre competencias de distintas instituciones.

## Fase 6 — Entidades parlamentarias completas

Desarrollar páginas propias para:

- comisiones;
- proyectos;
- votaciones;
- partidos;
- comités;
- distritos.

La capa educativa deberá estar integrada en todas ellas.

---

# 21. Orden de investigación antes de publicación

Cada página debe superar un pequeño contrato de investigación.

## Paso 1 — Norma

Revisar:

- Constitución;
- LOC del Congreso;
- Reglamento de Cámara;
- Reglamento del Senado;
- normativa complementaria pertinente.

## Paso 2 — Institución

Contrastar:

- Cámara;
- Senado;
- BCN;
- Servel cuando corresponda;
- documentos técnicos públicos.

## Paso 3 — Historia

Reconstruir cambios relevantes y evitar anacronismos.

## Paso 4 — Ciencia política y derecho

Mapear:

- consenso;
- explicaciones alternativas;
- controversias;
- evidencia empírica chilena;
- literatura comparada cuando ayude a entender el caso.

## Paso 5 — Traducción pedagógica

Redactar de:

> intuición → precisión → funcionamiento → límites → evidencia → debate.

No al revés.

## Paso 6 — Auditoría editorial

Comprobar que:

- ninguna simplificación sea falsa;
- no se atribuyan causalidades no demostradas;
- no se confundan funciones políticas con atribuciones jurídicas;
- se distingan Cámara y Congreso;
- se distingan hechos institucionales e inferencias;
- las fuentes permitan reconstruir la afirmación.

---

# 22. Principios editoriales obligatorios

1. **Pedagogía sin pérdida de precisión.**
2. **No presentar una controversia como hecho.**
3. **No presentar una práctica histórica como regla actual.**
4. **No usar “Congreso” cuando la atribución corresponde solo a la Cámara o solo al Senado.**
5. **No tratar partido, bancada, comité, coalición y alineamiento como sinónimos.**
6. **No reducir legislar a presentar proyectos o votar.**
7. **No reducir fiscalizar a sancionar.**
8. **No reducir representación a obedecer preferencias inmediatas.**
9. **No convertir actividad en calidad mediante rankings normativos.**
10. **Toda clasificación analítica propia debe distinguirse de categorías oficiales.**
11. **Los ejemplos reales deben indicar fecha y estado del procedimiento.**
12. **Los conceptos deben permanecer versionados y reutilizables.**

---

# 23. Funcionalidades P0 derivadas de esta arquitectura

Sin incluir nuevos modelos estadísticos, la arquitectura identifica como próximas funcionalidades de mayor valor ciudadano:

1. **Hub `Entiende el Congreso`.**
2. **Glosario contextual transversal.**
3. **¿Qué puede y qué no puede hacer un diputado?**
4. **Cómo se hace una ley, con proceso interactivo.**
5. **Sigue un proyecto mediante timeline.**
6. **¿Qué se votó realmente?**
7. **Cámara y Senado comparados.**
8. **Cómo fiscaliza la Cámara.**
9. **Páginas de comisiones.**
10. **Traductor de agenda y estados legislativos.**
11. **¿A quién debo contactar?**
12. **Historia del Congreso como problemas políticos, no solo fechas.**

---

# 24. Criterio de éxito

La nueva sección habrá cumplido su función si una persona puede:

1. entrar con una pregunta sencilla;
2. recibir inmediatamente una respuesta correcta;
3. profundizar hasta el nivel jurídico e histórico que desee;
4. distinguir hechos, evidencia y debates;
5. observar una instancia real del concepto funcionando;
6. volver desde los datos a la explicación institucional;
7. comprender qué puede hacer con esa información como ciudadano.

La arquitectura no busca que toda persona lea todo. Busca que **nadie tenga que elegir entre una explicación comprensible y una explicación rigurosa**.

---

# 25. Estado de cierre v0.1

- Nombre de sección: **Entiende el Congreso**.
- Arquitectura por preguntas: **ADOPTADA**.
- Lectura progresiva: **ADOPTADA**.
- Tipos epistemológicos: **ADOPTADOS**.
- Historia transversal: **ADOPTADA**.
- Conexión bidireccional educación ↔ datos: **ADOPTADA**.
- Separación educación / datos / metodología: **ADOPTADA**.
- Taxonomía temática A–H: **ADOPTADA COMO V0.1**.
- Orden de implementación por fases: **ADOPTADO**.

**Siguiente ciclo:** implementar el esqueleto de la Fase 1 sin publicar todavía contenido incompleto como definitivo, y continuar la investigación sustantiva de las páginas P0 siguiendo este contrato.