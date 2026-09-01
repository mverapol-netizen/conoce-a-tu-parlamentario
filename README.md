# Conoce a tu parlamentario

Primera versión funcional de un proyecto cívico para conectar a una persona con sus representantes en la Cámara de Diputadas y Diputados de Chile.

## Qué hace esta versión

1. La persona escribe su **comuna**.
2. El sitio identifica automáticamente su **distrito electoral**.
3. Muestra las **diputadas y diputados del distrito**.
4. Permite **elegir uno** para continuar, en futuras versiones, hacia una ficha parlamentaria detallada.

La aplicación funciona 100% en el navegador: no requiere servidor, base de datos, instalación ni claves API. Por eso puede publicarse directamente con **GitHub Pages**.

## Estructura

```text
conoce-a-tu-parlamentario/
├── index.html
├── README.md
├── .nojekyll
└── assets/
    ├── css/
    │   └── styles.css
    └── js/
        ├── data.js
        └── app.js
```

## Datos incluidos

- 28 distritos electorales.
- 346 comunas de Chile.
- 155 integrantes de la Cámara para el período 2026–2030.
- Corte de actualización: **1 de septiembre de 2026**.

Fuentes de referencia utilizadas para construir la base:

- Servicio Electoral de Chile (Servel), Territorios Electorales.
- Biblioteca del Congreso Nacional (BCN), Reportes Distritales.
- Cámara de Diputadas y Diputados de Chile, listado y fichas parlamentarias.

> Nota: este repositorio guarda una fotografía de los datos. Si cambia la integración de la Cámara (reemplazos, renuncias, etc.), habrá que actualizar `assets/js/data.js` o, en una etapa posterior, automatizar la actualización desde una fuente oficial.

## Cómo probarlo en tu computador

Haz doble clic en `index.html`. La búsqueda funciona incluso sin instalar nada.

También puedes probar enlaces directos, por ejemplo:

```text
index.html?comuna=Maipu
```

## Cómo subirlo a GitHub y publicarlo

1. Crea un repositorio llamado `conoce-a-tu-parlamentario`.
2. Sube **todo el contenido de esta carpeta**, manteniendo la estructura.
3. En GitHub entra a **Settings → Pages**.
4. En **Build and deployment**, selecciona **Deploy from a branch**.
5. Elige la rama `main` y la carpeta `/ (root)`.
6. Guarda. GitHub entregará una dirección pública para el sitio.

## Próximas capas posibles

La arquitectura ya deja un punto claro para ampliar la ficha del parlamentario elegido. Entre otras cosas, se pueden agregar:

- partido y bancada;
- fotografía y datos biográficos;
- asistencia;
- votaciones en Sala;
- mociones y proyectos patrocinados;
- comisiones;
- temas de especialización;
- oficinas y vías de contacto;
- comparaciones con otros representantes del mismo distrito;
- series históricas y visualizaciones.
