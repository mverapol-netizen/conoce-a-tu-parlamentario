# Conoce a tu parlamentario

Herramienta cívica para conectar a una persona con sus representantes en la Cámara de Diputadas y Diputados de Chile.

## Qué hace esta versión

1. La persona selecciona su **región**.
2. El sitio limita automáticamente el segundo filtro a las **comunas de esa región**.
3. La persona selecciona su **comuna**.
4. El sitio identifica automáticamente su **distrito electoral**.
5. Muestra las **diputadas y diputados del distrito** con fotografía, partido y número de distrito.
6. Al elegir una persona, abre una ficha resumida con **correo oficial** y enlace directo a su **ficha de la Cámara**.

La aplicación funciona 100% en el navegador: no requiere servidor, base de datos externa, instalación ni claves API para ser consultada. Por eso puede publicarse directamente con **GitHub Pages** y funciona también en dispositivos móviles.

## Cobertura actual

- 16 regiones.
- 28 distritos electorales.
- 346 comunas de Chile.
- 155 integrantes de la Cámara para el período 2026–2030.
- 155 fotografías oficiales almacenadas localmente en el repositorio.
- 155 correos institucionales extraídos desde las fichas oficiales de la Cámara.
- Partido, distrito, región, ID parlamentario y vínculo a la ficha oficial para cada integrante.

La Cámara no muestra un teléfono individual utilizable en las fichas revisadas, por lo que el sitio no inventa ni rellena ese dato: cuando no existe una vía telefónica personal publicada, se muestra correo + ficha oficial.

## Fuentes

La base territorial y parlamentaria se construye y contrasta con fuentes públicas oficiales:

- Servicio Electoral de Chile (Servel), para territorios electorales.
- Biblioteca del Congreso Nacional (BCN), para reportes distritales y antecedentes parlamentarios.
- Cámara de Diputadas y Diputados de Chile, para integración vigente, fichas, partidos, fotografías y correos institucionales.
- Portal de Datos Abiertos del Congreso, para IDs e integración vigente de la Cámara.

## Actualización automática

El repositorio incluye sincronización mediante **GitHub Actions**.

- `.github/workflows/sync_profiles.yml` ejecuta la sincronización completa de perfiles.
- `scripts/sync_profiles.py` empareja los 155 nombres de la base territorial con los IDs oficiales, actualiza partidos y descarga las fotografías oficiales.
- `scripts/sync_contacts.py` recupera los correos institucionales, incluyendo los correos protegidos en el HTML de la Cámara.
- `.github/workflows/sync_contacts_only.yml` permite actualizar solo contactos sin volver a descargar todas las fotografías.
- La sincronización completa está programada semanalmente y también puede ejecutarse manualmente desde GitHub Actions.

Después de cada actualización, GitHub Pages vuelve a desplegar automáticamente el sitio.

## Estructura principal

```text
conoce-a-tu-parlamentario/
├── index.html
├── README.md
├── .nojekyll
├── .github/
│   └── workflows/
│       ├── sync_profiles.yml
│       └── sync_contacts_only.yml
├── scripts/
│   ├── sync_profiles.py
│   └── sync_contacts.py
└── assets/
    ├── css/
    │   ├── styles.css
    │   └── profiles.css
    ├── js/
    │   ├── data.js
    │   ├── profiles.js
    │   └── app.js
    └── photos/
        └── 155 fotografías
```

## Diseño de los datos

`assets/js/data.js` conserva la relación territorial:

**región → comuna → distrito → representantes**

`assets/js/profiles.js` agrega la capa individual:

**representante → partido → foto → correo → ficha oficial**

Separar ambas capas permite mantener estable el mapa electoral y actualizar con mayor frecuencia los datos personales de quienes integran la Cámara.

## Próximas capas posibles

La siguiente etapa natural es convertir la selección de un parlamentario en una ficha de desempeño más completa. Entre otras cosas, se pueden agregar:

- bancada parlamentaria;
- reseña biográfica resumida;
- asistencia a Sala;
- votaciones;
- mociones y proyectos patrocinados;
- comisiones permanentes y especiales;
- oficios y actividad fiscalizadora;
- comparación con los demás representantes del distrito;
- series históricas y visualizaciones.

El objetivo es que una persona pueda pasar de **“¿quién me representa?”** a **“¿qué hace mi representante?”** sin tener que conocer de antemano cómo navegar las distintas bases del Congreso.
