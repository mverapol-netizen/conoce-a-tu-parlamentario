# Conoce a tu parlamentario

Herramienta cívica para conectar a una persona con sus representantes en la Cámara de Diputadas y Diputados de Chile y ofrecer una vista comprensible de la composición de la Cámara.

## Qué hace esta versión

### Tu distrito

1. La persona selecciona su **región**.
2. El sitio limita automáticamente el segundo selector a las **comunas de esa región**.
3. La persona selecciona su **comuna**.
4. El sitio identifica automáticamente su **distrito electoral**.
5. Muestra las **diputadas y diputados del distrito** con fotografía, partido y número de distrito.
6. Al elegir una persona, abre una ficha resumida con **correo oficial** y enlace directo a su **ficha de la Cámara**.

### Hemiciclo

La pestaña `hemiciclo.html` muestra los **155 escaños** como un mapa interactivo de fuerzas. Permite ver:

- partido de cada diputada o diputado;
- bancada o Comité Parlamentario;
- independientes adscritos a una bancada, sin presentarlos como militantes del partido;
- distribución editorial entre **oficialismo, oposición y no alineados**;
- número de integrantes de cada partido y de cada bancada/comité;
- mayoría absoluta de 78 escaños;
- identificación individual de cada escaño al tocarlo o seleccionarlo.

El hemiciclo representa **distribución de fuerzas**, no la ubicación física exacta de cada parlamentario en la Sala.

## Cobertura actual

- 16 regiones.
- 28 distritos electorales.
- 346 comunas de Chile.
- 155 integrantes de la Cámara para el período 2026–2030.
- 155 fotografías oficiales almacenadas localmente en el repositorio.
- 155 correos institucionales extraídos desde las fichas oficiales de la Cámara.
- Partido, bancada/comité, distrito, región, ID parlamentario y vínculo a la ficha oficial.

La Cámara no muestra un teléfono individual utilizable en todas las fichas revisadas, por lo que el sitio no inventa ni rellena ese dato.

## Fuentes

La base territorial y parlamentaria se construye y contrasta con fuentes públicas oficiales:

- Servicio Electoral de Chile (Servel), para territorios electorales.
- Biblioteca del Congreso Nacional (BCN), para reportes distritales y antecedentes parlamentarios.
- Cámara de Diputadas y Diputados de Chile, para integración vigente, partidos, bancadas/comités, fotografías, fichas y correos institucionales.
- Portal de Datos Abiertos del Congreso, para IDs e integración vigente de la Cámara.

## Partido, bancada y bloque político

Estas dimensiones se mantienen separadas deliberadamente.

- **Partido:** militancia o pertenencia partidaria publicada por la Cámara.
- **Bancada / Comité Parlamentario:** organización parlamentaria publicada por la Cámara. Los independientes deben integrarse a un Comité Parlamentario.
- **Adscripción de independientes:** se muestra como `Independiente en [bancada/comité]`. Para los cálculos de fuerzas parlamentarias se ubica al independiente en la bancada a la que está adscrito, pero nunca se altera su condición de independiente.
- **Oficialismo / oposición / no alineado:** capa editorial independiente de los datos oficiales. Está fechada en `assets/js/political_config.js` y debe revisarse cuando cambie públicamente la posición de una colectividad respecto del Gobierno.

Esta separación evita transformar una pertenencia a bancada en una militancia partidaria ficticia.

## Actualización automática

El repositorio incluye sincronización mediante **GitHub Actions**.

- `.github/workflows/sync_profiles.yml` ejecuta la sincronización completa el **primer día de cada mes** y también puede ejecutarse manualmente.
- `scripts/sync_profiles.py` empareja los 155 nombres con los IDs oficiales, actualiza partidos y descarga fotografías.
- `scripts/sync_contacts.py` recupera los correos institucionales.
- `scripts/sync_political.py` actualiza bancada/comité y aplica la clasificación política vigente configurada para el proyecto.
- `.github/workflows/sync_contacts_only.yml` permite actualizar solo contactos sin volver a descargar todas las fotografías.

Después de cada actualización, GitHub Pages vuelve a desplegar automáticamente el sitio.

La pertenencia a partido y bancada puede sincronizarse automáticamente desde la Cámara. En cambio, un cambio político como “un partido deja de ser oficialista y pasa a la oposición” requiere una **revisión editorial de fuentes públicas**; no se infiere automáticamente a partir de una sola votación.

## Estructura principal

```text
conoce-a-tu-parlamentario/
├── index.html
├── hemiciclo.html
├── README.md
├── ROADMAP.md
├── .nojekyll
├── .github/
│   └── workflows/
│       ├── sync_profiles.yml
│       └── sync_contacts_only.yml
├── scripts/
│   ├── sync_profiles.py
│   ├── sync_contacts.py
│   └── sync_political.py
└── assets/
    ├── css/
    │   ├── styles.css
    │   ├── profiles.css
    │   └── hemicycle.css
    ├── js/
    │   ├── data.js
    │   ├── profiles.js
    │   ├── political_config.js
    │   ├── app.js
    │   └── hemicycle.js
    └── photos/
        └── 155 fotografías
```

## Diseño de los datos

`assets/js/data.js` conserva la relación territorial:

**región → comuna → distrito → representantes**

`assets/js/profiles.js` agrega la capa individual:

**representante → partido → bancada → foto → correo → ficha oficial**

`assets/js/political_config.js` contiene únicamente la capa interpretativa y visual del hemiciclo:

**partido/bancada → color → orden → bloque político**

Separar estas capas permite actualizar los hechos oficiales sin confundirlos con decisiones de clasificación editorial.

## Próximas capas

La siguiente etapa natural es convertir la selección de un parlamentario en una ficha de desempeño más completa. Entre otras cosas, se pueden agregar:

- reseña biográfica resumida;
- asistencia a Sala;
- votaciones;
- mociones y proyectos patrocinados;
- comisiones permanentes y especiales;
- oficios y actividad fiscalizadora;
- comparación con los demás representantes del distrito;
- series históricas y visualizaciones.

El objetivo es que una persona pueda pasar de **“¿quién me representa?”** a **“¿qué hace mi representante?”** y, al mismo tiempo, entender **cómo está compuesto el Congreso**.
