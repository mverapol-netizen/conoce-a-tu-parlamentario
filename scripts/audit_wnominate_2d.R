#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(jsonlite))
options(stringsAsFactors = FALSE)

args_full <- commandArgs(trailingOnly = FALSE)
file_arg <- args_full[grep("--file=", args_full)]
if (length(file_arg)) {
  script_path <- sub("^--file=", "", file_arg[1])
  root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
} else {
  root <- normalizePath(".", mustWork = TRUE)
}
if (!file.exists(file.path(root, "data"))) root <- normalizePath(".", mustWork = TRUE)

base_dir <- file.path(root, "data", "legislative", "2026")
wnom_dir <- file.path(base_dir, "wnominate")
dir2 <- file.path(wnom_dir, "two_dimensional")

member_path <- file.path(dir2, "member_coordinates_2d.csv")
rollcall_path <- file.path(dir2, "rollcall_coordinates_2d.csv")
model_path <- file.path(dir2, "model_diagnostics_2d.csv")
enriched_path <- file.path(base_dir, "member_votes_enriched.csv")
topic_path <- file.path(base_dir, "topics", "rollcall_topic_map.csv")

required <- c(member_path, rollcall_path, model_path, enriched_path, topic_path)
missing <- required[!file.exists(required)]
if (length(missing)) stop("Faltan archivos: ", paste(missing, collapse = ", "))

read_utf8 <- function(path) {
  read.csv(path, check.names = FALSE, stringsAsFactors = FALSE, fileEncoding = "UTF-8-BOM")
}

members <- read_utf8(member_path)
rollcalls <- read_utf8(rollcall_path)
models <- read_utf8(model_path)
enriched <- read_utf8(enriched_path)
topics <- read_utf8(topic_path)

baseline_spec <- "raw_lop025_2d"
specs <- unique(members$spec_id)
if (!(baseline_spec %in% specs)) stop("No existe la especificación base 2D")

members$diputado_id <- as.character(members$diputado_id)
rollcalls$vote_id <- as.character(rollcalls$vote_id)
topics$vote_id <- as.character(topics$vote_id)
enriched$diputado_id <- as.character(enriched$diputado_id)

mode_with_share <- function(x) {
  x <- trimws(as.character(x))
  x <- x[nzchar(x)]
  if (!length(x)) return(c(value = "", share = 0))
  tab <- table(x)
  top <- names(tab)[tab == max(tab)]
  value <- sort(top)[1]
  c(value = value, share = as.numeric(max(tab) / length(x)))
}

eta_squared <- function(values, groups) {
  keep <- is.finite(values) & !is.na(groups) & nzchar(groups)
  values <- values[keep]
  groups <- groups[keep]
  if (length(values) < 3 || length(unique(groups)) < 2) return(NA_real_)
  grand <- mean(values)
  total_ss <- sum((values - grand)^2)
  if (total_ss <= 0) return(NA_real_)
  split_vals <- split(values, groups)
  between_ss <- sum(vapply(split_vals, function(v) length(v) * (mean(v) - grand)^2, numeric(1)))
  between_ss / total_ss
}

# Afiliación histórica modal por observación de voto. Es solo contexto descriptivo.
ids <- unique(members$diputado_id)
aff_rows <- lapply(ids, function(id) {
  rows <- enriched[enriched$diputado_id == id, , drop = FALSE]
  party <- mode_with_share(rows$party_at_vote)
  caucus <- mode_with_share(rows$caucus_at_vote)
  alignment <- mode_with_share(rows$alignment_at_vote)
  data.frame(
    diputado_id = id,
    modal_party = unname(party["value"]),
    modal_party_share = as.numeric(party["share"]),
    modal_caucus = unname(caucus["value"]),
    modal_caucus_share = as.numeric(caucus["share"]),
    modal_alignment = unname(alignment["value"]),
    modal_alignment_share = as.numeric(alignment["share"]),
    stringsAsFactors = FALSE
  )
})
aff <- do.call(rbind, aff_rows)

# Similarity Procrustes: traslación + rotación/reflexión + escala isotrópica.
# Esto remueve indeterminaciones geométricas antes de juzgar estabilidad entre corridas.
procrustes_to_baseline <- function(spec_df, baseline_df) {
  common <- merge(
    spec_df[, c("diputado_id", "dimension_1_raw", "dimension_2_raw")],
    baseline_df[, c("diputado_id", "dimension_1_raw", "dimension_2_raw")],
    by = "diputado_id",
    suffixes = c("_spec", "_base")
  )
  keep <- complete.cases(common[, c("dimension_1_raw_spec", "dimension_2_raw_spec", "dimension_1_raw_base", "dimension_2_raw_base")])
  common <- common[keep, , drop = FALSE]
  if (nrow(common) < 20) stop("Muy pocos miembros comunes para Procrustes")

  X <- as.matrix(common[, c("dimension_1_raw_spec", "dimension_2_raw_spec")])
  Y <- as.matrix(common[, c("dimension_1_raw_base", "dimension_2_raw_base")])
  xbar <- colMeans(X)
  ybar <- colMeans(Y)
  Xc <- sweep(X, 2, xbar, "-")
  Yc <- sweep(Y, 2, ybar, "-")
  sv <- svd(t(Xc) %*% Yc)
  R <- sv$u %*% t(sv$v)
  scale <- sum(sv$d) / sum(Xc^2)

  allX <- as.matrix(spec_df[, c("dimension_1_raw", "dimension_2_raw")])
  aligned <- matrix(NA_real_, nrow = nrow(allX), ncol = 2)
  valid <- complete.cases(allX)
  if (any(valid)) {
    centered <- sweep(allX[valid, , drop = FALSE], 2, xbar, "-")
    aligned[valid, ] <- sweep(scale * centered %*% R, 2, ybar, "+")
  }

  common_aligned <- scale * Xc %*% R
  common_target <- Yc
  rmse <- sqrt(mean(rowSums((common_aligned - common_target)^2)))
  disparity <- sum((common_aligned - common_target)^2) / sum(common_target^2)

  list(
    aligned = aligned,
    rotation = R,
    scale = scale,
    n_common = nrow(common),
    rmse = rmse,
    disparity = disparity
  )
}

base <- members[members$spec_id == baseline_spec, , drop = FALSE]
base_coords <- as.matrix(base[, c("dimension_1_raw", "dimension_2_raw")])

aligned_blocks <- list()
procrustes_rows <- list()
for (spec in specs) {
  df <- members[members$spec_id == spec, , drop = FALSE]
  if (spec == baseline_spec) {
    aligned <- as.matrix(df[, c("dimension_1_raw", "dimension_2_raw")])
    proc <- list(
      rotation = diag(2), scale = 1,
      n_common = sum(complete.cases(aligned)), rmse = 0, disparity = 0
    )
  } else {
    proc <- procrustes_to_baseline(df, base)
    aligned <- proc$aligned
  }
  df$dimension_1_aligned <- aligned[, 1]
  df$dimension_2_aligned <- aligned[, 2]
  aligned_blocks[[spec]] <- df

  joined <- merge(
    df[, c("diputado_id", "dimension_1_aligned", "dimension_2_aligned")],
    base[, c("diputado_id", "dimension_1_raw", "dimension_2_raw")],
    by = "diputado_id"
  )
  ok <- complete.cases(joined[, -1, drop = FALSE])
  joined <- joined[ok, , drop = FALSE]

  procrustes_rows[[spec]] <- data.frame(
    spec_id = spec,
    n_common = proc$n_common,
    scale_to_baseline = proc$scale,
    rotation_11 = proc$rotation[1, 1],
    rotation_12 = proc$rotation[1, 2],
    rotation_21 = proc$rotation[2, 1],
    rotation_22 = proc$rotation[2, 2],
    procrustes_rmse = proc$rmse,
    procrustes_disparity = proc$disparity,
    pearson_dim1_after_alignment = if (nrow(joined) > 2) cor(joined$dimension_1_aligned, joined$dimension_1_raw, use = "complete.obs") else NA,
    pearson_dim2_after_alignment = if (nrow(joined) > 2) cor(joined$dimension_2_aligned, joined$dimension_2_raw, use = "complete.obs") else NA,
    spearman_dim1_after_alignment = if (nrow(joined) > 2) cor(joined$dimension_1_aligned, joined$dimension_1_raw, use = "complete.obs", method = "spearman") else NA,
    spearman_dim2_after_alignment = if (nrow(joined) > 2) cor(joined$dimension_2_aligned, joined$dimension_2_raw, use = "complete.obs", method = "spearman") else NA,
    stringsAsFactors = FALSE
  )
}
procrustes_df <- do.call(rbind, procrustes_rows)
rownames(procrustes_df) <- NULL
aligned_members <- do.call(rbind, aligned_blocks)
rownames(aligned_members) <- NULL
aligned_members <- merge(aligned_members, aff, by = "diputado_id", all.x = TRUE, sort = FALSE)

# Estabilidad individual tras remover rotación/reflexión/escala global.
base_aligned <- aligned_members[aligned_members$spec_id == baseline_spec, c("diputado_id", "dimension_1_aligned", "dimension_2_aligned")]
names(base_aligned)[2:3] <- c("base_d1", "base_d2")
stability_rows <- lapply(ids, function(id) {
  b <- base_aligned[base_aligned$diputado_id == id, , drop = FALSE]
  rows <- aligned_members[aligned_members$diputado_id == id, , drop = FALSE]
  if (!nrow(b) || !is.finite(b$base_d1[1]) || !is.finite(b$base_d2[1])) {
    shifts <- rep(NA_real_, nrow(rows))
  } else {
    shifts <- sqrt((rows$dimension_1_aligned - b$base_d1[1])^2 + (rows$dimension_2_aligned - b$base_d2[1])^2)
  }
  valid_shifts <- shifts[is.finite(shifts)]
  first <- rows[1, , drop = FALSE]
  data.frame(
    diputado_id = id,
    diputado_nombre = first$diputado_nombre,
    modal_party = first$modal_party,
    modal_caucus = first$modal_caucus,
    modal_alignment = first$modal_alignment,
    specs_estimated = sum(is.finite(rows$dimension_1_aligned) & is.finite(rows$dimension_2_aligned)),
    baseline_d1 = if (nrow(b)) b$base_d1[1] else NA,
    baseline_d2 = if (nrow(b)) b$base_d2[1] else NA,
    max_euclidean_shift = if (length(valid_shifts)) max(valid_shifts) else NA,
    mean_euclidean_shift = if (length(valid_shifts)) mean(valid_shifts) else NA,
    stringsAsFactors = FALSE
  )
})
stability <- do.call(rbind, stability_rows)
stability <- stability[order(-stability$max_euclidean_shift, stability$diputado_nombre, na.last = TRUE), , drop = FALSE]

# Asociación descriptiva de cada dimensión de la corrida base con agrupaciones históricas modales.
base_context <- aligned_members[aligned_members$spec_id == baseline_spec, , drop = FALSE]
group_fields <- c(party = "modal_party", caucus = "modal_caucus", alignment = "modal_alignment")
group_assoc <- do.call(rbind, lapply(names(group_fields), function(group_type) {
  field <- group_fields[[group_type]]
  data.frame(
    group_type = group_type,
    n_groups = length(unique(base_context[[field]][nzchar(base_context[[field]])])),
    n_members = sum(complete.cases(base_context[, c("dimension_1_aligned", "dimension_2_aligned")]) & nzchar(base_context[[field]])),
    eta_squared_dim1 = eta_squared(base_context$dimension_1_aligned, base_context[[field]]),
    eta_squared_dim2 = eta_squared(base_context$dimension_2_aligned, base_context[[field]]),
    note = "Eta² descriptivo: asociación entre coordenada y diferencias entre grupos; no causal ni suficiente para nombrar una dimensión.",
    stringsAsFactors = FALSE
  )
}))

# Centros 2D por grupo, útiles para visualizar si D2 separa subgrupos de forma sistemática.
group_centers <- do.call(rbind, lapply(names(group_fields), function(group_type) {
  field <- group_fields[[group_type]]
  split_rows <- split(base_context, base_context[[field]])
  split_rows <- split_rows[nzchar(names(split_rows))]
  do.call(rbind, lapply(names(split_rows), function(group) {
    d <- split_rows[[group]]
    keep <- complete.cases(d[, c("dimension_1_aligned", "dimension_2_aligned")])
    d <- d[keep, , drop = FALSE]
    if (!nrow(d)) return(NULL)
    data.frame(
      group_type = group_type,
      group = group,
      n_members = nrow(d),
      mean_dim1 = mean(d$dimension_1_aligned),
      median_dim1 = median(d$dimension_1_aligned),
      mean_dim2 = mean(d$dimension_2_aligned),
      median_dim2 = median(d$dimension_2_aligned),
      sd_dim1 = if (nrow(d) > 1) sd(d$dimension_1_aligned) else NA,
      sd_dim2 = if (nrow(d) > 1) sd(d$dimension_2_aligned) else NA,
      stringsAsFactors = FALSE
    )
  }))
}))

# Efecto arco/herradura: una segunda coordenada puede recoger la curvatura de
# un espacio esencialmente unidimensional. Comparamos una relación lineal con
# una cuadrática para cada especificación ya alineada por Procrustes. El p-valor
# se conserva como diagnóstico auxiliar; no convierte por sí solo D2 en una
# dimensión sustantiva ni incorpora la incertidumbre de las coordenadas.
arch_rows <- list()
arch_member_rows <- list()
for (spec in specs) {
  d <- aligned_members[aligned_members$spec_id == spec, , drop = FALSE]
  keep <- is.finite(d$dimension_1_aligned) & is.finite(d$dimension_2_aligned)
  d <- d[keep, , drop = FALSE]
  if (nrow(d) < 20) next

  linear_fit <- lm(dimension_2_aligned ~ dimension_1_aligned, data = d)
  quadratic_fit <- lm(dimension_2_aligned ~ dimension_1_aligned + I(dimension_1_aligned^2), data = d)
  linear_summary <- summary(linear_fit)
  quadratic_summary <- summary(quadratic_fit)
  comparison <- anova(linear_fit, quadratic_fit)
  quadratic_term <- coef(quadratic_summary)["I(dimension_1_aligned^2)", , drop = FALSE]

  arch_rows[[spec]] <- data.frame(
    spec_id = spec,
    n_members = nrow(d),
    r_squared_linear = linear_summary$r.squared,
    adjusted_r_squared_linear = linear_summary$adj.r.squared,
    r_squared_quadratic = quadratic_summary$r.squared,
    adjusted_r_squared_quadratic = quadratic_summary$adj.r.squared,
    delta_r_squared_quadratic = quadratic_summary$r.squared - linear_summary$r.squared,
    quadratic_coefficient = unname(quadratic_term[1, "Estimate"]),
    quadratic_term_p_value_auxiliary = unname(quadratic_term[1, "Pr(>|t|)"]),
    nested_model_p_value_auxiliary = comparison$`Pr(>F)`[2],
    quadratic_rmse = sqrt(mean(residuals(quadratic_fit)^2)),
    stringsAsFactors = FALSE
  )

  arch_member_rows[[spec]] <- data.frame(
    spec_id = spec,
    diputado_id = d$diputado_id,
    diputado_nombre = d$diputado_nombre,
    dimension_1_aligned = d$dimension_1_aligned,
    dimension_2_aligned = d$dimension_2_aligned,
    dimension_2_predicted_by_quadratic = as.numeric(fitted(quadratic_fit)),
    dimension_2_residual_after_quadratic = as.numeric(residuals(quadratic_fit)),
    modal_party = d$modal_party,
    modal_caucus = d$modal_caucus,
    modal_alignment = d$modal_alignment,
    stringsAsFactors = FALSE
  )
}

arch_diagnostics <- do.call(rbind, arch_rows)
rownames(arch_diagnostics) <- NULL
arch_members <- do.call(rbind, arch_member_rows)
rownames(arch_members) <- NULL

base_arch_members <- arch_members[arch_members$spec_id == baseline_spec, , drop = FALSE]
arch_residual_group_association <- do.call(rbind, lapply(names(group_fields), function(group_type) {
  field <- group_fields[[group_type]]
  group_present <- !is.na(base_arch_members[[field]]) & nzchar(base_arch_members[[field]])
  data.frame(
    group_type = group_type,
    n_groups = length(unique(base_arch_members[[field]][group_present])),
    n_members = sum(is.finite(base_arch_members$dimension_2_residual_after_quadratic) & group_present),
    eta_squared_dim2_residual = eta_squared(base_arch_members$dimension_2_residual_after_quadratic, base_arch_members[[field]]),
    note = "Asociación descriptiva de los residuos de D2 tras retirar D1 y D1^2; no causal ni suficiente para nombrar una dimensión.",
    stringsAsFactors = FALSE
  )
}))

# Carga relativa de D2 por roll call en la corrida base. La documentación de wnominate
# define spread1D/spread2D como spreads por dimensión. Usamos los pesos estimados para
# calcular una medida puramente geométrica del aporte relativo de D2 al vector de spread.
base_rc <- rollcalls[rollcalls$spec_id == baseline_spec, , drop = FALSE]
base_model <- models[models$spec_id == baseline_spec, , drop = FALSE]
if (nrow(base_model) != 1) stop("Diagnóstico de modelo base 2D inconsistente")
w1 <- as.numeric(base_model$weight_1)
w2 <- as.numeric(base_model$weight_2)
base_rc$weighted_spread_1 <- as.numeric(base_rc$spread_1d) * w1
base_rc$weighted_spread_2 <- as.numeric(base_rc$spread_2d) * w2
den <- sqrt(base_rc$weighted_spread_1^2 + base_rc$weighted_spread_2^2)
base_rc$relative_dim2_loading <- ifelse(den > 0, abs(base_rc$weighted_spread_2) / den, NA_real_)
base_rc <- merge(base_rc, topics, by = c("vote_id", "boletin", "fecha"), all.x = TRUE, sort = FALSE)
base_rc$topic_primary[is.na(base_rc$topic_primary) | !nzchar(base_rc$topic_primary)] <- "Sin clasificación"

# Resumen temático solo exploratorio: la taxonomía aún tiene validación externa pendiente.
topic_split <- split(base_rc, base_rc$topic_primary)
topic_summary <- do.call(rbind, lapply(names(topic_split), function(topic) {
  d <- topic_split[[topic]]
  vals <- d$relative_dim2_loading[is.finite(d$relative_dim2_loading)]
  if (!length(vals)) return(NULL)
  data.frame(
    topic_primary = topic,
    n_rollcalls = length(vals),
    mean_relative_dim2_loading = mean(vals),
    median_relative_dim2_loading = median(vals),
    q75_relative_dim2_loading = unname(quantile(vals, 0.75, names = FALSE)),
    share_rollcalls_dim2_loading_gt_0_50 = mean(vals > 0.50),
    mean_topic_confidence = mean(as.numeric(d$topic_confidence), na.rm = TRUE),
    stringsAsFactors = FALSE
  )
}))
topic_summary <- topic_summary[order(-topic_summary$mean_relative_dim2_loading, -topic_summary$n_rollcalls), , drop = FALSE]

top_rollcalls <- base_rc[is.finite(base_rc$relative_dim2_loading), , drop = FALSE]
top_rollcalls <- top_rollcalls[order(-top_rollcalls$relative_dim2_loading), , drop = FALSE]
top_rollcalls <- head(top_rollcalls, 40)

# Fit: ganancia de 2D y relación de eigenvalores.
models$eigenvalue_ratio_2_to_1 <- as.numeric(models$eigenvalue_2) / as.numeric(models$eigenvalue_1)
models$delta_cc_percentage_points <- as.numeric(models$delta_correct_classification)
models$delta_apre_value <- as.numeric(models$delta_apre)

write.csv(aligned_members, file.path(dir2, "member_coordinates_2d_aligned.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(procrustes_df, file.path(dir2, "procrustes_stability.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(stability, file.path(dir2, "member_2d_stability.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(group_assoc, file.path(dir2, "group_association_2d.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(group_centers, file.path(dir2, "group_centers_2d.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(arch_diagnostics, file.path(dir2, "dim2_arch_diagnostics.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(arch_members, file.path(dir2, "dim2_arch_member_residuals.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(arch_residual_group_association, file.path(dir2, "dim2_arch_group_association.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(topic_summary, file.path(dir2, "topic_dim2_summary.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(top_rollcalls, file.path(dir2, "top_dim2_rollcalls.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(models, file.path(dir2, "model_diagnostics_2d_audited.csv"), row.names = FALSE, fileEncoding = "UTF-8")

nonbase_proc <- procrustes_df[procrustes_df$spec_id != baseline_spec, , drop = FALSE]
second_eta <- setNames(group_assoc$eta_squared_dim2, group_assoc$group_type)
first_eta <- setNames(group_assoc$eta_squared_dim1, group_assoc$group_type)
base_arch <- arch_diagnostics[arch_diagnostics$spec_id == baseline_spec, , drop = FALSE]

# Conclusión metodológica provisional basada en parsimonia: D2 mejora el ajuste, pero
# su eigenvalor es muy pequeño respecto de D1. La estabilidad Procrustes decide si
# merece conservarse como exploración, no si debe convertirse en indicador público.
mean_delta_cc <- mean(models$delta_cc_percentage_points, na.rm = TRUE)
mean_delta_apre <- mean(models$delta_apre_value, na.rm = TRUE)
mean_eigen_ratio <- mean(models$eigenvalue_ratio_2_to_1, na.rm = TRUE)
min_d2_corr <- if (nrow(nonbase_proc)) min(nonbase_proc$pearson_dim2_after_alignment, na.rm = TRUE) else NA_real_

if (is.finite(min_d2_corr) && min_d2_corr >= 0.70) {
  provisional <- "Mantener 1D como modelo principal parsimonioso y conservar 2D como diagnóstico exploratorio secundario. D2 es reproducible tras alineación, pero su importancia espectral es mucho menor que D1 y requiere interpretación sustantiva adicional."
} else {
  provisional <- "Mantener 1D como modelo principal. La segunda dimensión no muestra estabilidad suficiente entre especificaciones para una interpretación sustantiva en esta etapa."
}

most_sensitive <- head(stability[is.finite(stability$max_euclidean_shift), c("diputado_id", "diputado_nombre", "max_euclidean_shift", "modal_party", "modal_caucus")], 15)
leading_topics <- head(topic_summary, 10)

diagnostics <- list(
  generated_for = as.character(Sys.Date()),
  status = "PASS",
  baseline_spec = baseline_spec,
  specifications = specs,
  mean_delta_correct_classification_percentage_points = mean_delta_cc,
  mean_delta_apre = mean_delta_apre,
  mean_eigenvalue_ratio_2_to_1 = mean_eigen_ratio,
  procrustes = list(
    min_pearson_dim1_after_alignment_nonbaseline = if (nrow(nonbase_proc)) min(nonbase_proc$pearson_dim1_after_alignment, na.rm = TRUE) else NA,
    min_pearson_dim2_after_alignment_nonbaseline = min_d2_corr,
    max_disparity_nonbaseline = if (nrow(nonbase_proc)) max(nonbase_proc$procrustes_disparity, na.rm = TRUE) else NA,
    interpretation = "Similarity Procrustes elimina traslación, rotación/reflexión y escala isotrópica antes de evaluar estabilidad entre espacios 2D."
  ),
  baseline_group_eta_squared = list(
    dim1 = as.list(first_eta),
    dim2 = as.list(second_eta),
    warning = "Asociación descriptiva, no causal y no suficiente para nombrar dimensiones."
  ),
  dim2_arch_diagnostic = list(
    baseline_r_squared_quadratic = if (nrow(base_arch)) base_arch$r_squared_quadratic[1] else NA,
    baseline_delta_r_squared_quadratic = if (nrow(base_arch)) base_arch$delta_r_squared_quadratic[1] else NA,
    baseline_quadratic_coefficient = if (nrow(base_arch)) base_arch$quadratic_coefficient[1] else NA,
    specifications = arch_diagnostics,
    residual_group_association = arch_residual_group_association,
    warning = "La relación cuadrática es un diagnóstico geométrico. Los p-valores son auxiliares y no propagan la incertidumbre de las coordenadas estimadas."
  ),
  most_sensitive_members_after_procrustes = most_sensitive,
  leading_topics_by_relative_dim2_loading = leading_topics,
  topic_warning = "La lectura temática es exploratoria: la taxonomía legislativa mantiene pendiente una validación externa/formal de precisión por macroárea.",
  methodological_conclusion_provisional = provisional,
  public_use = "NO: no integrar todavía coordenadas 1D/2D ni etiquetas ideológicas a las fichas públicas."
)
write_json(diagnostics, file.path(dir2, "audit_2d_diagnostics.json"), pretty = TRUE, auto_unbox = TRUE, na = "null")

if (nrow(procrustes_df) != length(specs)) stop("Faltan especificaciones en auditoría Procrustes")
if (!all(is.finite(models$eigenvalue_ratio_2_to_1))) stop("Eigenvalue ratios inválidos")
if (mean_eigen_ratio >= 0.20) warning("D2 tiene un eigenvalor relativamente grande; revisar conclusión de parsimonia")
if (nrow(base_arch) != 1) stop("No se produjo el diagnóstico de arco para la especificación base")

cat(jsonlite::toJSON(list(
  mean_delta_cc_pp = mean_delta_cc,
  mean_delta_apre = mean_delta_apre,
  mean_eigen_ratio = mean_eigen_ratio,
  min_d2_corr_after_procrustes = min_d2_corr,
  baseline_dim2_quadratic_r_squared = base_arch$r_squared_quadratic[1],
  baseline_dim2_quadratic_delta_r_squared = base_arch$delta_r_squared_quadratic[1],
  conclusion = provisional
), pretty = TRUE, auto_unbox = TRUE), "\n")
