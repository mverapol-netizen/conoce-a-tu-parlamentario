#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(pscl)
  library(wnominate)
  library(jsonlite)
})

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
out_dir <- file.path(wnom_dir, "temporal")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

matrix_path <- file.path(base_dir, "rollcall_matrix_binary.csv")
metadata_path <- file.path(base_dir, "rollcall_matrix_metadata.csv")
full_coord_path <- file.path(wnom_dir, "member_coordinates.csv")
if (!all(file.exists(c(matrix_path, metadata_path, full_coord_path)))) {
  stop("Faltan matriz, metadatos o coordenadas 1D completas")
}

matrix_df <- read.csv(
  matrix_path,
  check.names = FALSE,
  na.strings = c("", "NA"),
  stringsAsFactors = FALSE,
  fileEncoding = "UTF-8-BOM"
)
meta <- read.csv(
  metadata_path,
  check.names = FALSE,
  stringsAsFactors = FALSE,
  fileEncoding = "UTF-8-BOM"
)
full_coords <- read.csv(
  full_coord_path,
  check.names = FALSE,
  stringsAsFactors = FALSE,
  fileEncoding = "UTF-8-BOM"
)

member_ids <- as.character(matrix_df$diputado_id)
member_names <- as.character(matrix_df$diputado_nombre)
vote_ids <- setdiff(names(matrix_df), c("diputado_id", "diputado_nombre"))
votes <- as.matrix(matrix_df[, vote_ids, drop = FALSE])
storage.mode(votes) <- "numeric"
rownames(votes) <- paste(member_ids, member_names, sep = "|")
colnames(votes) <- vote_ids

meta$vote_id <- as.character(meta$vote_id)
meta$boletin <- as.character(meta$boletin)
meta$fecha <- as.character(meta$fecha)
meta$minority_count <- as.numeric(meta$minority_count)
meta$minority_share_binary <- as.numeric(meta$minority_share_binary)
meta$binary_participation_share <- as.numeric(meta$binary_participation_share)
meta <- meta[match(vote_ids, meta$vote_id), , drop = FALSE]
if (any(is.na(meta$vote_id))) stop("Hay columnas de matriz sin metadatos")

full_base <- full_coords[full_coords$spec_id == "raw_lop025", c("diputado_id", "diputado_nombre", "dimension_1_aligned")]
full_base$diputado_id <- as.character(full_base$diputado_id)
if (!nrow(full_base)) stop("No se encontró la especificación 1D raw_lop025")

eligible <- !is.na(meta$minority_count) & meta$minority_count > 0 &
  !is.na(meta$minority_share_binary) & meta$minority_share_binary >= 0.025
eligible_meta <- meta[eligible, , drop = FALSE]
eligible_meta$.date <- as.Date(eligible_meta$fecha)
eligible_meta$.vote_num <- suppressWarnings(as.numeric(eligible_meta$vote_id))
eligible_meta <- eligible_meta[order(eligible_meta$.date, eligible_meta$.vote_num, eligible_meta$vote_id, na.last = TRUE), , drop = FALSE]

if (nrow(eligible_meta) < 100) stop("Muy pocos roll calls elegibles para prueba temporal")
cut <- floor(nrow(eligible_meta) / 2)
early_ids <- eligible_meta$vote_id[seq_len(cut)]
late_ids <- eligible_meta$vote_id[(cut + 1):nrow(eligible_meta)]

cap_ids_by_bill <- function(ids, cap = 20) {
  sub <- meta[match(ids, meta$vote_id), , drop = FALSE]
  kept <- character(0)
  for (bill in unique(sub$boletin)) {
    rows <- sub[sub$boletin == bill, , drop = FALSE]
    rows <- rows[order(
      -rows$minority_share_binary,
      -rows$binary_participation_share,
      rows$fecha,
      suppressWarnings(as.numeric(rows$vote_id)),
      rows$vote_id,
      na.last = TRUE
    ), , drop = FALSE]
    kept <- c(kept, head(rows$vote_id, cap))
  }
  ids[ids %in% kept]
}

spec_ids <- list(
  early_raw = early_ids,
  late_raw = late_ids,
  early_cap20 = cap_ids_by_bill(early_ids, 20),
  late_cap20 = cap_ids_by_bill(late_ids, 20)
)

technical_anchor <- function(ids, minvotes = 20) {
  x <- votes[, ids, drop = FALSE]
  counts <- rowSums(!is.na(x))
  eligible_members <- counts >= minvotes
  if (sum(eligible_members) < 2) stop("No hay suficientes miembros para ancla técnica")
  means <- colMeans(x, na.rm = TRUE)
  z <- sweep(x, 2, means, FUN = "-")
  z[is.na(z)] <- 0
  z <- z[eligible_members, , drop = FALSE]
  sv <- svd(z, nu = 1, nv = 0)
  idx_eligible <- which(eligible_members)
  idx <- idx_eligible[which.max(abs(sv$u[, 1]))]
  list(index = idx, id = member_ids[idx], name = member_names[idx], n_votes = counts[idx])
}

zscore <- function(x) {
  good <- is.finite(x)
  out <- rep(NA_real_, length(x))
  if (sum(good) >= 2) {
    s <- sd(x[good])
    out[good] <- if (is.finite(s) && s > 0) (x[good] - mean(x[good])) / s else 0
  }
  out
}

rank_values <- function(x) {
  out <- rep(NA_integer_, length(x))
  good <- which(is.finite(x))
  if (length(good)) {
    ord <- good[order(x[good], member_ids[good])]
    out[ord] <- seq_along(ord)
  }
  out
}

run_spec <- function(spec_id, ids) {
  x <- votes[, ids, drop = FALSE]
  counts <- rowSums(!is.na(x))
  anchor <- technical_anchor(ids)

  rc <- pscl::rollcall(
    data = x,
    yea = 1,
    nay = 0,
    missing = NA,
    notInLegis = 9,
    legis.names = rownames(x),
    vote.names = ids,
    desc = paste("Cámara de Diputadas y Diputados de Chile 2026 · temporal", spec_id),
    source = "Conoce a tu parlamentario · Cámara de Diputadas y Diputados"
  )

  fit <- wnominate::wnominate(
    rc,
    dims = 1,
    minvotes = 20,
    lop = 0.025,
    polarity = anchor$index,
    trials = 1
  )

  coord <- as.numeric(fit$legislators$coord1D)
  comparison <- merge(
    data.frame(diputado_id = member_ids, coord = coord, stringsAsFactors = FALSE),
    full_base[, c("diputado_id", "dimension_1_aligned")],
    by = "diputado_id"
  )
  rho <- suppressWarnings(cor(comparison$coord, comparison$dimension_1_aligned, use = "complete.obs"))
  flipped <- is.finite(rho) && rho < 0
  aligned <- if (flipped) -coord else coord

  sub_meta <- meta[match(ids, meta$vote_id), , drop = FALSE]
  bill_tab <- sort(table(sub_meta$boletin), decreasing = TRUE)
  largest_bill_n <- if (length(bill_tab)) as.integer(bill_tab[1]) else 0L
  largest_bill_share <- if (length(ids)) largest_bill_n / length(ids) else NA_real_

  fits <- fit$fits
  fit_value <- function(name) {
    if (!is.null(names(fits)) && name %in% names(fits)) as.numeric(fits[[name]]) else NA_real_
  }

  member_out <- data.frame(
    spec_id = spec_id,
    diputado_id = member_ids,
    diputado_nombre = member_names,
    binary_votes_selected = counts,
    included_by_minvotes = counts >= 20,
    dimension_1_raw = coord,
    dimension_1_aligned_to_full = aligned,
    dimension_1_z = zscore(aligned),
    rank_aligned = rank_values(aligned),
    gmp = as.numeric(fit$legislators$GMP),
    correctly_classified = as.numeric(fit$legislators$CC),
    stringsAsFactors = FALSE
  )

  model_out <- data.frame(
    spec_id = spec_id,
    start_date = min(sub_meta$fecha),
    end_date = max(sub_meta$fecha),
    selected_rollcalls = length(ids),
    selected_bills = length(unique(sub_meta$boletin)),
    largest_bill_rollcalls = largest_bill_n,
    largest_bill_share = largest_bill_share,
    estimated_members = sum(is.finite(coord)),
    anchor_id = anchor$id,
    anchor_name = anchor$name,
    sign_flipped_to_full = flipped,
    correlation_raw_to_full_before_sign = rho,
    correlation_aligned_to_full = suppressWarnings(cor(aligned, full_base$dimension_1_aligned[match(member_ids, full_base$diputado_id)], use = "complete.obs")),
    correct_classification_1d = fit_value("correctclass1D"),
    apre_1d = fit_value("apre1D"),
    gmp_1d = fit_value("gmp1D"),
    eigenvalue_1 = if (length(fit$eigenvalues)) as.numeric(fit$eigenvalues[1]) else NA_real_,
    stringsAsFactors = FALSE
  )

  list(member = member_out, model = model_out)
}

results <- list()
errors <- list()
for (spec in names(spec_ids)) {
  message(sprintf("[Temporal] Ejecutando %s (%d roll calls)", spec, length(spec_ids[[spec]])))
  result <- tryCatch(run_spec(spec, spec_ids[[spec]]), error = function(e) e)
  if (inherits(result, "error")) {
    errors[[spec]] <- conditionMessage(result)
    message(sprintf("[Temporal] ERROR %s: %s", spec, conditionMessage(result)))
  } else {
    results[[spec]] <- result
  }
}

if (!all(c("early_raw", "late_raw") %in% names(results))) {
  stop("No se pudieron estimar las dos mitades temporales crudas")
}
if (length(results) < 3) stop("Demasiadas especificaciones temporales fallaron")

member_all <- do.call(rbind, lapply(results, `[[`, "member"))
model_all <- do.call(rbind, lapply(results, `[[`, "model"))
rownames(member_all) <- NULL
rownames(model_all) <- NULL

pair_specs <- list(
  c("early_raw", "late_raw"),
  c("early_cap20", "late_cap20"),
  c("early_raw", "early_cap20"),
  c("late_raw", "late_cap20")
)
pair_rows <- list()
for (pair in pair_specs) {
  if (!all(pair %in% names(results))) next
  a <- results[[pair[1]]]$member
  b <- results[[pair[2]]]$member
  z <- merge(
    a[, c("diputado_id", "dimension_1_aligned_to_full", "dimension_1_z", "rank_aligned")],
    b[, c("diputado_id", "dimension_1_aligned_to_full", "dimension_1_z", "rank_aligned")],
    by = "diputado_id",
    suffixes = c("_a", "_b")
  )
  good_raw <- complete.cases(z[, c("dimension_1_aligned_to_full_a", "dimension_1_aligned_to_full_b")])
  good_z <- complete.cases(z[, c("dimension_1_z_a", "dimension_1_z_b")])
  pair_rows[[paste(pair, collapse = "__")]] <- data.frame(
    spec_a = pair[1],
    spec_b = pair[2],
    n_common = sum(good_raw),
    pearson = cor(z$dimension_1_aligned_to_full_a, z$dimension_1_aligned_to_full_b, use = "complete.obs"),
    spearman = cor(z$dimension_1_aligned_to_full_a, z$dimension_1_aligned_to_full_b, use = "complete.obs", method = "spearman"),
    standardized_rmse = if (any(good_z)) sqrt(mean((z$dimension_1_z_a[good_z] - z$dimension_1_z_b[good_z])^2)) else NA_real_,
    median_abs_rank_change = median(abs(z$rank_aligned_a - z$rank_aligned_b), na.rm = TRUE),
    max_abs_rank_change = max(abs(z$rank_aligned_a - z$rank_aligned_b), na.rm = TRUE),
    stringsAsFactors = FALSE
  )
}
pair_df <- do.call(rbind, pair_rows)
rownames(pair_df) <- NULL

make_shifts <- function(a_spec, b_spec, label) {
  if (!all(c(a_spec, b_spec) %in% names(results))) return(NULL)
  a <- results[[a_spec]]$member
  b <- results[[b_spec]]$member
  z <- merge(
    a[, c("diputado_id", "diputado_nombre", "dimension_1_z", "rank_aligned", "binary_votes_selected")],
    b[, c("diputado_id", "dimension_1_z", "rank_aligned", "binary_votes_selected")],
    by = "diputado_id",
    suffixes = c("_early", "_late")
  )
  z$comparison <- label
  z$delta_z_late_minus_early <- z$dimension_1_z_late - z$dimension_1_z_early
  z$abs_delta_z <- abs(z$delta_z_late_minus_early)
  z$rank_change_late_minus_early <- z$rank_aligned_late - z$rank_aligned_early
  z$abs_rank_change <- abs(z$rank_change_late_minus_early)
  z <- z[order(-z$abs_delta_z, -z$abs_rank_change, z$diputado_nombre, na.last = TRUE), ]
  z
}

shifts_raw <- make_shifts("early_raw", "late_raw", "raw_halves")
shifts_cap20 <- make_shifts("early_cap20", "late_cap20", "cap20_halves")
shift_all <- do.call(rbind, Filter(Negate(is.null), list(shifts_raw, shifts_cap20)))
rownames(shift_all) <- NULL

write.csv(member_all, file.path(out_dir, "temporal_member_coordinates.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(model_all, file.path(out_dir, "temporal_model_diagnostics.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(pair_df, file.path(out_dir, "temporal_stability_pairs.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(shift_all, file.path(out_dir, "temporal_member_shifts.csv"), row.names = FALSE, fileEncoding = "UTF-8")

raw_pair <- pair_df[pair_df$spec_a == "early_raw" & pair_df$spec_b == "late_raw", , drop = FALSE]
cap_pair <- pair_df[pair_df$spec_a == "early_cap20" & pair_df$spec_b == "late_cap20", , drop = FALSE]
raw_pearson <- if (nrow(raw_pair)) raw_pair$pearson[1] else NA_real_
cap_pearson <- if (nrow(cap_pair)) cap_pair$pearson[1] else NA_real_
raw_spearman <- if (nrow(raw_pair)) raw_pair$spearman[1] else NA_real_
cap_spearman <- if (nrow(cap_pair)) cap_pair$spearman[1] else NA_real_

if (is.finite(raw_pearson) && is.finite(cap_pearson) && raw_pearson >= 0.90 && cap_pearson >= 0.90) {
  conclusion <- "Alta estabilidad temporal agregada: las dos mitades producen un eje 1D muy semejante tanto en bruto como al limitar la concentración por boletín. Aun así, deben auditarse desplazamientos individuales antes de uso público."
} else if (is.finite(raw_pearson) && raw_pearson >= 0.75 && (!is.finite(cap_pearson) || cap_pearson >= 0.75)) {
  conclusion <- "Estabilidad temporal moderada: la estructura 1D persiste, pero existe variación suficiente para mantener las coordenadas como experimentales y evitar rankings públicos estáticos."
} else {
  conclusion <- "Estabilidad temporal insuficiente para un indicador público estático con el corte actual. Conviene acumular más período y tratar la posición como dinámica."
}

top_raw_shifts <- if (!is.null(shifts_raw)) head(shifts_raw[is.finite(shifts_raw$abs_delta_z), c("diputado_id", "diputado_nombre", "delta_z_late_minus_early", "abs_rank_change")], 20) else data.frame()
top_cap_shifts <- if (!is.null(shifts_cap20)) head(shifts_cap20[is.finite(shifts_cap20$abs_delta_z), c("diputado_id", "diputado_nombre", "delta_z_late_minus_early", "abs_rank_change")], 20) else data.frame()

split_info <- list(
  eligible_rollcalls = nrow(eligible_meta),
  early_rollcalls_raw = length(early_ids),
  late_rollcalls_raw = length(late_ids),
  early_start = min(meta$fecha[match(early_ids, meta$vote_id)]),
  early_end = max(meta$fecha[match(early_ids, meta$vote_id)]),
  late_start = min(meta$fecha[match(late_ids, meta$vote_id)]),
  late_end = max(meta$fecha[match(late_ids, meta$vote_id)]),
  split_rule = "Orden cronológico de los roll calls elegibles con lop >= 0.025; primera mitad vs segunda mitad por número de votaciones, evitando elegir una fecha de corte sustantiva ad hoc."
)

diagnostics <- list(
  generated_for = as.character(Sys.Date()),
  status = if (length(errors)) "PARTIAL" else "PASS",
  completed_specs = names(results),
  failed_specs = errors,
  split = split_info,
  raw_halves = list(pearson = raw_pearson, spearman = raw_spearman),
  cap20_halves = list(pearson = cap_pearson, spearman = cap_spearman),
  model_diagnostics = model_all,
  most_shifted_raw = top_raw_shifts,
  most_shifted_cap20 = top_cap_shifts,
  methodological_conclusion_provisional = conclusion,
  warnings = c(
    "La estabilidad temporal agregada no implica estabilidad individual.",
    "Las submuestras temporales reducen el número de roll calls y pueden excluir miembros con baja participación binaria.",
    "El signo de cada corrida se alinea técnicamente contra la estimación completa; esta alineación no confiere significado político al signo.",
    "No integrar todavía resultados temporales ni coordenadas W-NOMINATE en fichas públicas."
  )
)
write_json(diagnostics, file.path(out_dir, "temporal_diagnostics.json"), pretty = TRUE, auto_unbox = TRUE, na = "null")

if (nrow(raw_pair) != 1) stop("No se produjo comparación early_raw vs late_raw")
if (raw_pair$n_common[1] < 140) warning("Menos de 140 miembros comunes en comparación temporal cruda")

cat(jsonlite::toJSON(list(
  early_window = paste(split_info$early_start, split_info$early_end, sep = " -> "),
  late_window = paste(split_info$late_start, split_info$late_end, sep = " -> "),
  raw_pearson = raw_pearson,
  raw_spearman = raw_spearman,
  cap20_pearson = cap_pearson,
  cap20_spearman = cap_spearman,
  conclusion = conclusion
), pretty = TRUE, auto_unbox = TRUE), "\n")
