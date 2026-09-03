#!/usr/bin/env Rscript

# Visualizaciones internas y reproducibles de los modelos espaciales 2026.
#
# IMPORTANTE:
# - D1 mantiene signo matemáticamente arbitrario y NO se interpreta aquí como
#   izquierda/derecha, oficialismo/oposición o ideología.
# - Para presentación usamos una convención fija de orientación: D1_display = -D1_model.
#   Esto refleja horizontalmente el eje, sin alterar distancias, ajuste ni orden relativo.
# - D2 sigue siendo exploratoria y no se invierte en esta convención.
# - Estas figuras viven en la capa de investigación y no se publican
#   automáticamente en las fichas públicas.

suppressPackageStartupMessages({
  library(ggplot2)
})

options(stringsAsFactors = FALSE)

D1_DISPLAY_MULTIPLIER <- -1

root <- normalizePath(".", mustWork = TRUE)
research_dir <- file.path(root, "data", "legislative", "2026", "wnominate", "research_1d")
two_d_dir <- file.path(root, "data", "legislative", "2026", "wnominate", "two_dimensional")
aff_dir <- file.path(root, "data", "legislative", "2026", "affiliations")
out_dir <- file.path(root, "data", "legislative", "2026", "wnominate", "figures")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

coord_path <- file.path(research_dir, "member_coordinates_research.csv")
boot_path <- file.path(research_dir, "cluster_bootstrap_member_summary.csv")
aff_path <- file.path(aff_dir, "affiliation_snapshots.csv")
coord2_path <- file.path(two_d_dir, "member_coordinates_2d_aligned.csv")

required <- c(coord_path, boot_path, aff_path, coord2_path)
missing <- required[!file.exists(required)]
if (length(missing) > 0L) {
  stop("Faltan insumos requeridos:\n", paste(missing, collapse = "\n"))
}

read_utf8 <- function(path) {
  read.csv(path, fileEncoding = "UTF-8-BOM", check.names = FALSE, stringsAsFactors = FALSE)
}

coord <- read_utf8(coord_path)
boot <- read_utf8(boot_path)
aff <- read_utf8(aff_path)
coord2 <- read_utf8(coord2_path)

coord$diputado_id <- as.character(coord$diputado_id)
boot$diputado_id <- as.character(boot$diputado_id)
aff$deputy_id <- as.character(aff$deputy_id)
coord2$diputado_id <- as.character(coord2$diputado_id)

# Snapshot vigente más reciente disponible.
aff$observed_date <- as.Date(aff$observed_date)
latest_snapshot <- max(aff$observed_date, na.rm = TRUE)
aff_now <- aff[aff$observed_date == latest_snapshot, , drop = FALSE]
aff_now <- aff_now[!duplicated(aff_now$deputy_id), , drop = FALSE]

# Join 1D research + bootstrap + afiliación vigente.
idx_b <- match(coord$diputado_id, boot$diputado_id)
idx_a <- match(coord$diputado_id, aff_now$deputy_id)

p1 <- coord
p1$q025_model <- boot$q025[idx_b]
p1$q975_model <- boot$q975[idx_b]
p1$interval_width <- boot$interval_width[idx_b]
p1$n_success <- boot$n_success[idx_b]
p1$party <- aff_now$party_reported[idx_a]
p1$caucus <- aff_now$caucus_reported[idx_a]
p1$alignment <- aff_now$alignment_reported[idx_a]

p1$party[is.na(p1$party) | p1$party == ""] <- "Sin dato"
p1$alignment[is.na(p1$alignment) | p1$alignment == ""] <- "Sin dato"

# Convención visual solicitada: reflejar D1 respecto de cero.
# El intervalo [q025, q975] se transforma en [-q975, -q025].
p1$dimension_1_display <- D1_DISPLAY_MULTIPLIER * p1$dimension_1_raw
if (D1_DISPLAY_MULTIPLIER == -1) {
  p1$q025_display <- -p1$q975_model
  p1$q975_display <- -p1$q025_model
} else {
  p1$q025_display <- p1$q025_model
  p1$q975_display <- p1$q975_model
}

# Orden espacial según la orientación de presentación.
p1 <- p1[order(p1$dimension_1_display), , drop = FALSE]
p1$rank_d1 <- seq_len(nrow(p1))
p1$name_order <- factor(p1$diputado_nombre, levels = rev(p1$diputado_nombre))

# Selección reproducible de etiquetas para figuras compactas:
# extremos D1 y observaciones con mayor sensibilidad por proyecto.
extreme_idx <- unique(c(head(seq_len(nrow(p1)), 6L), tail(seq_len(nrow(p1)), 6L)))
wide_idx <- order(p1$interval_width, decreasing = TRUE, na.last = NA)
wide_idx <- head(wide_idx, 8L)
label_idx <- sort(unique(c(extreme_idx, wide_idx)))
p1$label <- ""
p1$label[label_idx] <- p1$diputado_nombre[label_idx]

base_theme <- theme_minimal(base_size = 12) +
  theme(
    panel.grid.minor = element_blank(),
    legend.position = "bottom",
    plot.title.position = "plot",
    plot.caption = element_text(hjust = 0, size = 9),
    plot.subtitle = element_text(size = 10)
  )

caption_common <- paste0(
  "Fuente: Cámara de Diputadas y Diputados de Chile; elaboración propia. ",
  "Snapshot de afiliación: ", latest_snapshot, ". ",
  "Orientación de presentación: D1 = -D1 de la salida del modelo. ",
  "El signo sigue siendo una convención; uso interno de investigación."
)

# 1. D1 ordenada por parlamentario, similar a un gráfico NOMINATE clásico.
g_rank <- ggplot(p1, aes(x = rank_d1, y = dimension_1_display, colour = party)) +
  geom_hline(yintercept = 0, linewidth = 0.35, linetype = 2) +
  geom_line(aes(group = 1), colour = "grey75", linewidth = 0.45) +
  geom_point(size = 2.2, alpha = 0.9) +
  geom_text(
    data = p1[p1$label != "", , drop = FALSE],
    aes(label = label),
    colour = "black",
    size = 2.7,
    vjust = -0.7,
    check_overlap = TRUE,
    show.legend = FALSE
  ) +
  labs(
    title = "W-NOMINATE 2026: dimensión principal ordenada",
    subtitle = "154 parlamentarios elegibles; orientación visual reflejada; color = partido vigente",
    x = "Orden según D1",
    y = "Coordenada D1 (convención de presentación)",
    colour = "Partido",
    caption = caption_common
  ) +
  base_theme +
  theme(axis.text.x = element_blank(), axis.ticks.x = element_blank())

# 2. Forest plot completo con sensibilidad bootstrap por proyecto.
g_forest_full <- ggplot(p1, aes(y = name_order, x = dimension_1_display, colour = party)) +
  geom_vline(xintercept = 0, linewidth = 0.35, linetype = 2) +
  geom_errorbarh(aes(xmin = q025_display, xmax = q975_display), height = 0, linewidth = 0.45, alpha = 0.65) +
  geom_point(size = 1.8) +
  labs(
    title = "W-NOMINATE 2026: posición estimada y sensibilidad por proyecto",
    subtitle = "Punto = D1 reflejada; barra = percentiles 2,5–97,5 del bootstrap agrupado por boletín (200 réplicas)",
    x = "Coordenada D1 (convención de presentación)",
    y = NULL,
    colour = "Partido",
    caption = caption_common
  ) +
  base_theme +
  theme(
    axis.text.y = element_text(size = 5.7),
    panel.grid.major.y = element_line(linewidth = 0.18)
  )

# 3. Versión legible: 30 intervalos más anchos.
wide30 <- p1[order(p1$interval_width, decreasing = TRUE, na.last = NA), , drop = FALSE]
wide30 <- head(wide30, 30L)
wide30 <- wide30[order(wide30$dimension_1_display), , drop = FALSE]
wide30$name_order <- factor(wide30$diputado_nombre, levels = rev(wide30$diputado_nombre))

g_forest_30 <- ggplot(wide30, aes(y = name_order, x = dimension_1_display, colour = party)) +
  geom_vline(xintercept = 0, linewidth = 0.35, linetype = 2) +
  geom_errorbarh(aes(xmin = q025_display, xmax = q975_display), height = 0, linewidth = 0.75, alpha = 0.75) +
  geom_point(size = 2.4) +
  labs(
    title = "W-NOMINATE 2026: parlamentarios más sensibles a la composición de proyectos",
    subtitle = "Los 30 intervalos bootstrap más anchos; no equivale a 'moderación' ni a cambio ideológico",
    x = "Coordenada D1 (convención de presentación)",
    y = NULL,
    colour = "Partido",
    caption = caption_common
  ) +
  base_theme +
  theme(axis.text.y = element_text(size = 8))

# 4. D1–D2 exploratoria: especificación base 2D.
p2 <- coord2[coord2$spec_id == "raw_lop025_2d", , drop = FALSE]
if (nrow(p2) == 0L) stop("No existe spec_id raw_lop025_2d en member_coordinates_2d_aligned.csv")

# Preferimos snapshot vigente para color; conservamos modal_* solo como respaldo.
idx_a2 <- match(p2$diputado_id, aff_now$deputy_id)
p2$party_current <- aff_now$party_reported[idx_a2]
p2$alignment_current <- aff_now$alignment_reported[idx_a2]
p2$party_current[is.na(p2$party_current) | p2$party_current == ""] <- p2$modal_party[is.na(p2$party_current) | p2$party_current == ""]
p2$alignment_current[is.na(p2$alignment_current) | p2$alignment_current == ""] <- p2$modal_alignment[is.na(p2$alignment_current) | p2$alignment_current == ""]
p2$party_current[is.na(p2$party_current) | p2$party_current == ""] <- "Sin dato"
p2$alignment_current[is.na(p2$alignment_current) | p2$alignment_current == ""] <- "Sin dato"

# La convención visual refleja solo D1; D2 permanece exactamente como estaba.
p2$dimension_1_display <- D1_DISPLAY_MULTIPLIER * p2$dimension_1_aligned
p2$dimension_2_display <- p2$dimension_2_aligned

# Etiquetar extremos geométricos para evitar una nube ilegible de 154 nombres.
score_extreme <- pmax(abs(p2$dimension_1_display), abs(p2$dimension_2_display), na.rm = TRUE)
lab2 <- order(score_extreme, decreasing = TRUE)
lab2 <- head(lab2, 22L)
p2$label <- ""
p2$label[lab2] <- p2$diputado_nombre[lab2]

caption_2d <- paste0(
  "Fuente: Cámara de Diputadas y Diputados de Chile; elaboración propia. ",
  "D1 se refleja solo para presentación (D1 = -D1 del modelo); D2 no se altera. ",
  "D2 es exploratoria y no tiene interpretación sustantiva validada. Snapshot: ", latest_snapshot, "."
)

g_2d_party <- ggplot(p2, aes(x = dimension_1_display, y = dimension_2_display, colour = party_current)) +
  geom_hline(yintercept = 0, linewidth = 0.3, colour = "grey75") +
  geom_vline(xintercept = 0, linewidth = 0.3, colour = "grey75") +
  geom_point(size = 2.2, alpha = 0.82) +
  geom_text(
    data = p2[p2$label != "", , drop = FALSE],
    aes(label = label),
    colour = "black",
    size = 2.5,
    vjust = -0.65,
    check_overlap = TRUE,
    show.legend = FALSE
  ) +
  coord_equal(xlim = c(-1.05, 1.05), ylim = c(-1.05, 1.05)) +
  labs(
    title = "W-NOMINATE 2026: solución bidimensional exploratoria",
    subtitle = "Especificación raw_lop025_2d; D1 reflejada para presentación; color = partido vigente",
    x = "D1 (convención de presentación)",
    y = "D2 alineada (exploratoria)",
    colour = "Partido",
    caption = caption_2d
  ) +
  base_theme

g_2d_alignment <- ggplot(p2, aes(x = dimension_1_display, y = dimension_2_display, colour = alignment_current)) +
  geom_hline(yintercept = 0, linewidth = 0.3, colour = "grey75") +
  geom_vline(xintercept = 0, linewidth = 0.3, colour = "grey75") +
  geom_point(size = 2.5, alpha = 0.86) +
  geom_text(
    data = p2[p2$label != "", , drop = FALSE],
    aes(label = label),
    colour = "black",
    size = 2.5,
    vjust = -0.65,
    check_overlap = TRUE,
    show.legend = FALSE
  ) +
  coord_equal(xlim = c(-1.05, 1.05), ylim = c(-1.05, 1.05)) +
  labs(
    title = "W-NOMINATE 2026: D1 y D2 por alineamiento actual",
    subtitle = "D1 reflejada para presentación; D2 sigue exploratoria",
    x = "D1 (convención de presentación)",
    y = "D2 alineada (exploratoria)",
    colour = "Alineamiento",
    caption = caption_2d
  ) +
  base_theme

save_pair <- function(plot, stem, width, height, dpi = 180) {
  png_path <- file.path(out_dir, paste0(stem, ".png"))
  pdf_path <- file.path(out_dir, paste0(stem, ".pdf"))
  ggsave(png_path, plot = plot, width = width, height = height, units = "in", dpi = dpi, bg = "white", limitsize = FALSE)
  ggsave(pdf_path, plot = plot, width = width, height = height, units = "in", bg = "white", limitsize = FALSE)
  c(png_path, pdf_path)
}

outputs <- character()
outputs <- c(outputs, save_pair(g_rank, "wnominate_1d_ranked_party", 15, 8))
outputs <- c(outputs, save_pair(g_forest_full, "wnominate_1d_uncertainty_full", 13, 32, dpi = 160))
outputs <- c(outputs, save_pair(g_forest_30, "wnominate_1d_uncertainty_top30", 12, 11))
outputs <- c(outputs, save_pair(g_2d_party, "wnominate_2d_party_exploratory", 13, 10))
outputs <- c(outputs, save_pair(g_2d_alignment, "wnominate_2d_alignment_exploratory", 12, 10))

manifest <- data.frame(
  file = basename(outputs),
  generated_at_utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
  snapshot_affiliation = as.character(latest_snapshot),
  d1_display_multiplier = D1_DISPLAY_MULTIPLIER,
  public_ready = FALSE,
  stringsAsFactors = FALSE
)
write.csv(manifest, file.path(out_dir, "figure_manifest.csv"), row.names = FALSE, fileEncoding = "UTF-8")

cat("Figuras generadas:\n")
cat(paste0(" - ", outputs, collapse = "\n"), "\n")
cat("Orientación visual D1: multiplicador ", D1_DISPLAY_MULTIPLIER, "\n", sep = "")
cat("Manifest: ", file.path(out_dir, "figure_manifest.csv"), "\n", sep = "")
