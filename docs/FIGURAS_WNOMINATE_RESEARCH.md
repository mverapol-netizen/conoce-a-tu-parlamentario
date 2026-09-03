# Galería de figuras W-NOMINATE — investigación 2026

> **Uso interno de investigación.** D1 mantiene signo arbitrario y no se interpreta todavía como izquierda/derecha, oficialismo/oposición o ideología. D2 sigue siendo exploratoria. Ninguna de estas figuras está marcada como lista para publicación pública.

Esta página reúne las visualizaciones generadas automáticamente por `scripts/plot_wnominate_research.R` a partir de la corrida de investigación W-NOMINATE 2026.

## 1. D1 ordenada por partido

![W-NOMINATE D1 ordenada por partido](../data/legislative/2026/wnominate/figures/wnominate_1d_ranked_party.png)

Versión ordenada de los parlamentarios sobre D1. El color representa partido vigente en el snapshot de afiliaciones usado para la corrida.

## 2. D1 con incertidumbre — Cámara completa

![W-NOMINATE D1 con incertidumbre completa](../data/legislative/2026/wnominate/figures/wnominate_1d_uncertainty_full.png)

Punto base W-NOMINATE más intervalo de sensibilidad obtenido mediante bootstrap agrupado por proyecto/boletín.

## 3. D1 con incertidumbre — 30 casos más sensibles

![W-NOMINATE D1 con incertidumbre top 30](../data/legislative/2026/wnominate/figures/wnominate_1d_uncertainty_top30.png)

Detalle de los 30 parlamentarios con intervalos más amplios en el bootstrap por proyecto. Sirve para ver dónde la ubicación individual depende más de la composición de la agenda legislativa.

## 4. D1 × D2 por partido — exploratorio

![W-NOMINATE 2D por partido](../data/legislative/2026/wnominate/figures/wnominate_2d_party_exploratory.png)

Solución bidimensional exploratoria. D2 no se eleva todavía a dimensión sustantiva ni recibe etiqueta temática.

## 5. D1 × D2 por alineamiento — exploratorio

![W-NOMINATE 2D por alineamiento](../data/legislative/2026/wnominate/figures/wnominate_2d_alignment_exploratory.png)

La misma geometría 2D, coloreada por alineamiento vigente. El color es descriptivo y no define el significado matemático de los ejes.

---

### Archivos vectoriales

Cada figura también se guarda en PDF en `data/legislative/2026/wnominate/figures/` para uso en papers, presentaciones o revisión de alta resolución.
