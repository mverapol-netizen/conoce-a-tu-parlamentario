# Auditoría del núcleo P0 · Entiende el Congreso · v0.1

**Proyecto:** Conoce a tu parlamentario  
**Fecha:** 3 de septiembre de 2026  
**Alcance:** arquitectura y seis lecciones P0 de educación parlamentaria  
**Estado:** núcleo de contenido implementado en vista interna; **no habilitado todavía en la navegación pública**

## 1. Objeto de la auditoría

Esta auditoría comprueba que la primera capa de `Entiende el Congreso` mantenga coherencia jurídica, politológica, pedagógica y técnica antes de transformarse en una sección pública del sitio.

La regla de cierre continúa siendo:

> **La intuición inicial puede ser incompleta, pero no puede ser falsa. Cada nivel posterior debe aumentar precisión sin obligar a desmentir pedagógicamente el nivel anterior.**

La segunda regla es:

> **Una regla institucional, un hallazgo empírico y una controversia interpretativa no pueden presentarse como si tuvieran el mismo estatus epistemológico.**

---

## 2. Núcleo P0 implementado

Se encuentran estructuradas como lecciones completas:

1. **¿Para qué existe el Congreso?**
2. **¿Quién representa a quién?**
3. **Cámara y Senado: dos cámaras, un Congreso**
4. **¿Cómo se hace una ley?**
5. **¿Qué puede hacer realmente un diputado?**
6. **¿Cómo fiscaliza la Cámara al Gobierno?**

Cada una posee, cuando corresponde:

- intuición inicial;
- puntos esenciales;
- explicación institucional;
- distinciones negativas (`qué no significa`);
- historia;
- evidencia;
- debate;
- fuentes originales;
- vínculos conceptuales mediante glosario contextual.

---

## 3. Auditoría conceptual transversal

### 3.1 Congreso, Cámara y Senado

**Resultado: consistente.**

Las lecciones distinguen sistemáticamente:

- `Congreso Nacional` = Cámara + Senado;
- `Cámara de Diputadas y Diputados` = una de las ramas;
- `Senado` = segunda rama;
- ambas concurren a la formación de las leyes;
- no poseen idénticas atribuciones.

Se evita usar `Congreso` como sinónimo automático de `Cámara` al hablar de fiscalización.

### 3.2 Representación

**Resultado: consistente.**

Se evita definir representación como obediencia mecánica a preferencias electorales. Se distinguen:

- autorización electoral;
- accountability;
- representación territorial;
- mediación partidaria;
- juicio del representante;
- dimensiones descriptivas y sustantivas;
- actividad territorial.

La formulación pública preferida pasa a ser **“representantes elegidos por tu distrito”** y no la idea de que cada elector tenga un único diputado individual exclusivo.

### 3.3 Individuo versus institución colegiada

**Resultado: consistente y prioritario.**

La lección `¿Qué puede hacer realmente un diputado?` bloquea una confusión transversal:

- una persona puede presentar determinadas mociones, formular indicaciones, debatir, votar, participar en comisiones y utilizar herramientas de información bajo sus reglas;
- una persona no equivale a la Cámara;
- numerosas actuaciones requieren apoyos colectivos o decisiones de Sala;
- la Cámara tampoco sustituye al Ejecutivo, a tribunales, municipios o servicios públicos.

Esta distinción debe trasladarse posteriormente a fichas, tooltips y módulos de participación ciudadana.

### 3.4 Formación de la ley

**Resultado: consistente.**

Se evita la secuencia falsa `idea → votación → ley`. La arquitectura enseña:

- mensaje/moción;
- iniciativa exclusiva;
- cámara de origen;
- comisión;
- discusión general;
- indicaciones;
- discusión particular;
- cámara revisora;
- discrepancias y comisión mixta cuando corresponda;
- observaciones presidenciales;
- promulgación;
- publicación;
- control constitucional cuando proceda.

Se explicita que **“aprobado en general” no equivale a “texto final aprobado”** y que una votación debe interpretarse según su objeto y etapa.

### 3.5 Fiscalización

**Resultado: consistente con una precisión editorial importante.**

Se distingue:

- fiscalización ordinaria del artículo 52 N.º 1;
- solicitudes constitucionales de antecedentes;
- solicitudes de información bajo el artículo 9 de la LOC del Congreso;
- interpelación;
- comisión especial investigadora;
- acusación constitucional.

La acusación constitucional se ubica dentro del universo amplio del control político-constitucional, pero no se presenta como una etapa automática ni como una modalidad idéntica a las tres formas de fiscalización del artículo 52 N.º 1.

### 3.6 Presidencialismo

**Resultado: consistente.**

Se evita inferir que:

- interpelar a un ministro equivale a una moción de censura;
- fiscalizar equivale a gobernar;
- el Congreso monopoliza la formación de la ley;
- poder constitucional formal y peso empírico efectivo sean la misma cosa.

La literatura sobre cambios en la dominancia legislativa presidencial se presenta como `EVIDENCIA/DEBATE`, no como una modificación de las reglas constitucionales vigentes.

---

## 4. Auditoría epistemológica

### Institución

Se reserva para:

- Constitución;
- Ley Orgánica Constitucional del Congreso;
- reglamentos;
- reglas electorales;
- información institucional competente.

### Evidencia

Se utiliza para resultados provenientes de:

- literatura académica;
- datos comparados;
- estudios empíricos sobre Chile.

### Debate

Se utiliza para cuestiones como:

- delegate/trustee;
- justificación del bicameralismo;
- balance Ejecutivo–Legislativo;
- evaluación de efectividad de fiscalización;
- interpretación de actividad territorial.

### Historia

La historia no se usa para naturalizar la institución actual. Su propósito es mostrar que las reglas presentes son históricamente contingentes y han cambiado.

### Mito frecuente

Se usa para bloquear inferencias previsibles antes de que sean trasladadas a los datos.

**Resultado general:** la clasificación es conceptualmente sostenible y debe conservarse como contrato editorial.

---

## 5. Auditoría de fuentes

La jerarquía adoptada es:

1. Constitución vigente y legislación;
2. reglamentos;
3. Cámara, Senado, BCN y Servel según competencia;
4. literatura académica especializada;
5. datos del propio proyecto, claramente identificados como tales.

Las lecciones P0 incluyen enlaces a fuentes originales. Antes del paso a producción debe ejecutarse una verificación sistemática de:

- URL accesible;
- vigencia de la versión jurídica enlazada;
- concordancia exacta entre afirmación y fuente;
- ausencia de enlaces históricos presentados como derecho vigente;
- fecha de última revisión.

---

## 6. Auditoría técnica

### Implementado

- `entender.html` como hub interno;
- `aprender.html` como plantilla única de lección;
- `education_data_v1.js` como contrato de contenidos base;
- módulos separados para lecciones P0;
- buscador local de preguntas, lecciones y conceptos;
- glosario contextual reutilizable;
- navegación progresiva entre lecciones;
- estilos responsivos propios;
- `robots=noindex` mientras la sección esté en construcción;
- no se ha añadido todavía el enlace a `Entiende el Congreso` en las páginas públicas principales.

### Integración

El build/deploy de GitHub Pages correspondiente al núcleo P0 cargado en el hub terminó exitosamente. Después se añadieron mejoras de búsqueda y navegación progresiva, por lo que cada commit posterior debe continuar verificándose mediante Actions.

### Limitación de la auditoría actual

Se intentó descargar los scripts desde `raw.githubusercontent.com` hacia un runtime local para ejecutar `node --check`, pero el entorno de validación no pudo resolver ese dominio. Por tanto, **no se registra falsamente una prueba local de sintaxis**. La integración estática se comprueba mediante el build de GitHub Pages y queda pendiente una comprobación de navegador real.

---

## 7. Gate antes de publicación

La sección **no debe incorporarse todavía a la navegación pública principal** hasta completar:

- [ ] revisión visual en escritorio;
- [ ] revisión visual en móvil;
- [ ] prueba de buscador y navegación de teclado;
- [ ] prueba de popovers/glosario con teclado y lector de pantalla en lo razonablemente verificable;
- [ ] revisión sistemática de todos los enlaces fuente;
- [ ] comprobación de las seis lecciones P0 en navegador después del deploy final;
- [ ] reemplazar o esconder en modo público las lecciones que continúen solo como `planned`/`research` si pudieran confundirse con contenido final;
- [ ] añadir conexiones reales mínimas entre concepto e instancia del sitio;
- [ ] decidir el primer conjunto de tooltips que se infiltrará en `ficha.html`, proyectos y votaciones;
- [ ] retirar `noindex` únicamente al momento de publicación deliberada;
- [ ] añadir `Entiende el Congreso` a la navegación superior de todas las páginas en un único ciclo consistente.

---

## 8. Conexiones mínimas exigidas para el gate público

Antes de publicar, al menos estas conexiones deben funcionar:

- `distrito` → distrito real seleccionado por el usuario;
- `moción` → una moción real;
- `mensaje` → un mensaje real;
- `comisión` → una comisión actual;
- `primer/segundo/tercer trámite` → proyecto real que ejemplifique la etapa;
- `votación` → objeto de votación real;
- `fiscalización` → al menos un registro público de CEI/oficio/interpelación cuando la fuente lo permita;
- `partido/bancada/comité` → instancia actual de la Cámara.

El objetivo es cumplir el segundo principio de arquitectura:

> **todo concepto importante debe poder observarse funcionando y todo dato importante debe poder devolver al concepto que lo explica.**

---

## 9. Prioridad posterior al gate P0

Una vez superado el gate, el siguiente bloque de contenidos debe cerrar:

1. **Comisiones**;
2. **Partidos, bancadas y comités**;
3. **Agenda y tabla**;
4. **Mayorías y quórums**;
5. **Cómo se eligen los parlamentarios / D’Hondt**;
6. **Historia institucional completa 1811–2026**;
7. **Participación ciudadana y “¿a quién debo contactar?”**.

No se recomienda abrir nuevas familias analíticas complejas antes de consolidar estas funciones institucionales.
