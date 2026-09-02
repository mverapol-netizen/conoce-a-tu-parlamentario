#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(pscl)
  library(wnominate)
  library(jsonlite)
})

options(stringsAsFactors = FALSE)

root <- normalizePath(file.path(dirname(commandArgs(trailingOnly = FALSE)[grep("--file=", commandArgs(trailingOnly = FALSE))]), ".."), mustWork = FALSE)
if (!dir.exists(root) || !file.exists(file.path(root, "data"))) {
  root <- normalizePath(".", mustWork = TRUE)
}

base_dir <- file.path(root, "data", "legislative", "2026")
out_dir <- file.path(base_dir, "wnominate")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

matrix_path <- file.path(base_dir, "rollcall_matrix_binary.csv")
metadata_path <- file.path(base_dir, "rollcall_matrix_metadata.csv")

if (!file.exists(matrix_path) || !file.exists(metadata_path)) {
  stop("Faltan rollcall_matrix_binary.csv o rollcall_matrix_metadata.csv")
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

required_matrix <- c("diputado_id", "diputado_nombre")
required_meta <- c(
  "vote_id", "fecha", "boletin", "minority_count", "minority_share_binary",
  "binary_participation_share"
)
if (!all(required_matrix %in% names(matrix_df))) {
  stop("La matriz no contiene las columnas de identificación esperadas")
}
if (!all(required_meta %in% names(meta))) {
  stop("Los metadatos no contienen las columnas esperadas")
}

member_ids <- as.character(matrix_df$diputado_id)
member_names <- as.character(matrix_df$diputado_nombre)
vote_ids <- setdiff(names(matrix_df), required_matrix)

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

if (any(is.na(meta$vote_id))) {
  stop("Hay columnas de la matriz sin metadatos de roll call")
}
if (!all(votes[!is.na(votes)] %in% c(0, 1))) {
  stop("La matriz contiene códigos distintos de 0/1/NA")
}

specs <- data.frame(
  spec_id = c(
    "raw_lop025", "raw_lop050", "raw_lop100",
    "dedup_lop025", "cap20_balanced_lop025", "cap10_balanced_lop025"
  ),
  lop = c(0.025, 0.050, 0.100, 0.025, 0.025, 0.025),
  deduplicate_within_bill = c(FALSE, FALSE, FALSE, TRUE, FALSE, FALSE),
  bill_cap = c(NA, NA, NA, NA, 20, 10),
  stringsAsFactors = FALSE
)

eligible_vote_ids <- function(lop) {
  keep <- !is.na(meta$minority_count) &
    meta$minority_count > 0 &
    !is.na(meta$minority_share_binary) &
    meta$minority_share_binary >= lop
  meta$vote_id[keep]
}

vote_signature <- function(x) {
  paste(ifelse(is.na(x), "M", as.character(as.integer(x))), collapse = "")
}

deduplicate_ids <- function(ids) {
  if (length(ids) <= 1) return(ids)
  sub_meta <- meta[match(ids, meta$vote_id), , drop = FALSE]
  signatures <- vapply(ids, function(id) vote_signature(votes[, id]), character(1))
  keys <- paste(sub_meta$boletin, signatures, sep = "::")
  ids[!duplicated(keys)]
}

cap_ids_by_bill <- function(ids, cap) {
  if (is.na(cap) || length(ids) <= 1) return(ids)
  sub_meta <- meta[match(ids, meta$vote_id), , drop = FALSE]
  sub_meta$.original_order <- seq_len(nrow(sub_meta))
  bills <- unique(sub_meta$boletin)
  kept <- character(0)

  for (bill in bills) {
    rows <- sub_meta[sub_meta$boletin == bill, , drop = FALSE]
    # Para la sensibilidad de concentración retenemos, de manera determinista,
    # las votaciones más discriminantes de cada boletín: mayor proporción del
    # lado minoritario, luego mayor participación binaria y finalmente fecha/ID.
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

  # Reponemos el orden cronológico/original de la matriz para reproducibilidad.
  ids[ids %in% kept]
}

select_ids_for_spec <- function(spec_row) {
  ids <- eligible_vote_ids(spec_row$lop)
  if (isTRUE(spec_row$deduplicate_within_bill)) {
    ids <- deduplicate_ids(ids)
  }
  if (!is.na(spec_row$bill_cap)) {
    ids <- cap_ids_by_bill(ids, spec_row$bill_cap)
  }
  ids
}

technical_anchor <- function(ids, minvotes = 20) {
  x <- votes[, ids, drop = FALSE]
  counts <- rowSums(!is.na(x))
  eligible <- counts >= minvotes
  if (sum(eligible) < 2) stop("No hay suficientes legisladores elegibles para seleccionar ancla")

  means <- colMeans(x, na.rm = TRUE)
  z <- sweep(x, 2, means, FUN = "-")
  z[is.na(z)] <- 0
  z <- z[eligible, , drop = FALSE]
  s <- svd(z, nu = 1, nv = 0)
  score <- s$u[, 1]
  eligible_indices <- which(eligible)
  idx <- eligible_indices[which.max(abs(score))]
  list(index = idx, id = member_ids[idx], name = member_names[idx], binary_votes = counts[idx])
}

baseline_ids <- select_ids_for_spec(specs[specs$spec_id == "raw_lop025", , drop = FALSE])
baseline_anchor <- technical_anchor(baseline_ids)

all_member_rows <- list()
all_rollcall_rows <- list()
model_rows <- list()
manifest_rows <- list()
results_by_spec <- list()
errors <- list()

run_one <- function(spec_row) {
  spec_id <- spec_row$spec_id
  ids <- select_ids_for_spec(spec_row)
  if (length(ids) < 20) stop(sprintf("%s retiene solo %d roll calls", spec_id, length(ids)))

  x <- votes[, ids, drop = FALSE]
  counts <- rowSums(!is.na(x))
  anchor <- baseline_anchor
  if (counts[anchor$index] < 20) {
    anchor <- technical_anchor(ids)
  } else {
    anchor$binary_votes <- counts[anchor$index]
  }

  rc <- pscl::rollcall(
    data = x,
    yea = 1,
    nay = 0,
    missing = NA,
    notInLegis = 9,
    legis.names = rownames(x),
    vote.names = ids,
    desc = paste("Cámara de Diputadas y Diputados de Chile 2026", spec_id),
    source = "Conoce a tu parlamentario · Cámara de Diputadas y Diputados"
  )

  fit <- wnominate::wnominate(
    rc,
    dims = 1,
    minvotes = 20,
    lop = spec_row$lop,
    polarity = anchor$index,
    trials = 1
  )

  leg <- fit$legislators
  rcfit <- fit$rollcalls

  member_out <- data.frame(
    spec_id = spec_id,
    diputado_id = member_ids,
    diputado_nombre = member_names,
    binary_votes_selected = counts,
    included_by_minvotes = counts >= 20,
    dimension_1_raw = as.numeric(leg$coord1D),
    se_1d = as.numeric(leg$se1D),
    gmp = as.numeric(leg$GMP),
    correctly_classified = as.numeric(leg$CC),
    stringsAsFactors = FALSE
  )

  rollcall_out <- data.frame(
    spec_id = spec_id,
    vote_id = ids,
    boletin = meta$boletin[match(ids, meta$vote_id)],
    fecha = meta$fecha[match(ids, meta$vote_id)],
    minority_share_binary = meta$minority_share_binary[match(ids, meta$vote_id)],
    binary_participation_share = meta$binary_participation_share[match(ids, meta$vote_id)],
    spread_1d = as.numeric(rcfit$spread1D),
    midpoint_1d = as.numeric(rcfit$midpoint1D),
    gmp = as.numeric(rcfit$GMP),
    apre = as.numeric(rcfit$PRE),
    stringsAsFactors = FALSE
  )

  fits <- fit$fits
  get_fit <- function(name) {
    if (!is.null(names(fits)) && name %in% names(fits)) return(as.numeric(fits[[name]]))
    NA_real_
  }

  model_out <- data.frame(
    spec_id = spec_id,
    lop = spec_row$lop,
    minvotes = 20,
    deduplicate_within_bill = spec_row$deduplicate_within_bill,
    bill_cap = spec_row$bill_cap,
    selected_rollcalls_before_package = length(ids),
    estimated_rollcalls = sum(!is.na(rcfit$GMP)),
    estimated_members = sum(!is.na(leg$coord1D)),
    anchor_diputado_id = anchor$id,
    anchor_diputado_nombre = anchor$name,
    anchor_binary_votes = anchor$binary_votes,
    correct_classification_1d = get_fit("correctclass1D"),
    apre_1d = get_fit("apre1D"),
    gmp_1d = get_fit("gmp1D"),
    beta = if (length(fit$beta)) as.numeric(fit$beta[1]) else NA_real_,
    weight_1d = if (length(fit$weights)) as.numeric(fit$weights[1]) else NA_real_,
    stringsAsFactors = FALSE
  )

  manifest_out <- data.frame(
    spec_id = spec_id,
    lop = spec_row$lop,
    deduplicate_within_bill = spec_row$deduplicate_within_bill,
    bill_cap = spec_row$bill_cap,
    selected_rollcalls = length(ids),
    selected_bills = length(unique(meta$boletin[match(ids, meta$vote_id)])),
    largest_bill_rollcalls = max(table(meta$boletin[match(ids, meta$vote_id)])),
    largest_bill_share = max(table(meta$boletin[match(ids, meta$vote_id)])) / length(ids),
    stringsAsFactors = FALSE
  )

  list(
    fit = fit,
    members = member_out,
    rollcalls = rollcall_out,
    model = model_out,
    manifest = manifest_out
  )
}

for (i in seq_len(nrow(specs))) {
  spec_row <- specs[i, , drop = FALSE]
  spec_id <- spec_row$spec_id
  message(sprintf("[W-NOMINATE] Ejecutando %s", spec_id))
  result <- tryCatch(
    run_one(spec_row),
    error = function(e) e
  )
  if (inherits(result, "error")) {
    errors[[spec_id]] <- conditionMessage(result)
    message(sprintf("[W-NOMINATE] ERROR %s: %s", spec_id, conditionMessage(result)))
  } else {
    results_by_spec[[spec_id]] <- result
    all_member_rows[[spec_id]] <- result$members
    all_rollcall_rows[[spec_id]] <- result$rollcalls
    model_rows[[spec_id]] <- result$model
    manifest_rows[[spec_id]] <- result$manifest
  }
}

if (!("raw_lop025" %in% names(results_by_spec))) {
  stop(sprintf("Falló la especificación base raw_lop025: %s", errors[["raw_lop025"]]))
}
if (length(results_by_spec) < 4) {
  stop(sprintf("Solo %d especificaciones terminaron correctamente", length(results_by_spec)))
}

members_all <- do.call(rbind, all_member_rows)
rownames(members_all) <- NULL
rollcalls_all <- do.call(rbind, all_rollcall_rows)
rownames(rollcalls_all) <- NULL
models_all <- do.call(rbind, model_rows)
rownames(models_all) <- NULL
manifest_all <- do.call(rbind, manifest_rows)
rownames(manifest_all) <- NULL

# Alineación puramente técnica de signo respecto de la corrida base. Esto NO
# añade significado izquierda/derecha; solo permite comparar coordenadas entre
# especificaciones cuyo signo es matemáticamente arbitrario.
baseline <- members_all[members_all$spec_id == "raw_lop025", c("diputado_id", "dimension_1_raw")]
names(baseline)[2] <- "baseline_coord"
members_all$dimension_1_aligned <- members_all$dimension_1_raw
models_all$sign_flipped_to_baseline <- FALSE

for (spec_id in unique(members_all$spec_id)) {
  idx <- members_all$spec_id == spec_id
  temp <- merge(
    members_all[idx, c("diputado_id", "dimension_1_raw")],
    baseline,
    by = "diputado_id",
    all.x = TRUE,
    sort = FALSE
  )
  rho <- suppressWarnings(cor(temp$dimension_1_raw, temp$baseline_coord, use = "complete.obs"))
  flip <- !is.na(rho) && rho < 0
  if (flip) members_all$dimension_1_aligned[idx] <- -members_all$dimension_1_raw[idx]
  models_all$sign_flipped_to_baseline[models_all$spec_id == spec_id] <- flip
}

spec_ids <- unique(members_all$spec_id)
stability <- data.frame()
if (length(spec_ids) >= 2) {
  pairs <- combn(spec_ids, 2, simplify = FALSE)
  stability <- do.call(rbind, lapply(pairs, function(pair) {
    a <- members_all[members_all$spec_id == pair[1], c("diputado_id", "dimension_1_aligned")]
    b <- members_all[members_all$spec_id == pair[2], c("diputado_id", "dimension_1_aligned")]
    names(a)[2] <- "a"
    names(b)[2] <- "b"
    z <- merge(a, b, by = "diputado_id")
    data.frame(
      spec_a = pair[1],
      spec_b = pair[2],
      n_common = sum(complete.cases(z$a, z$b)),
      pearson = suppressWarnings(cor(z$a, z$b, use = "complete.obs", method = "pearson")),
      spearman = suppressWarnings(cor(z$a, z$b, use = "complete.obs", method = "spearman")),
      stringsAsFactors = FALSE
    )
  }))
}

write.csv(members_all, file.path(out_dir, "member_coordinates.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(rollcalls_all, file.path(out_dir, "rollcall_coordinates.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(models_all, file.path(out_dir, "model_diagnostics.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(manifest_all, file.path(out_dir, "spec_manifest.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(stability, file.path(out_dir, "stability_correlations.csv"), row.names = FALSE, fileEncoding = "UTF-8")

summary_json <- list(
  generated_for = as.character(Sys.Date()),
  status = if (length(errors)) "PARTIAL" else "PASS",
  package_versions = list(
    R = R.version.string,
    pscl = as.character(packageVersion("pscl")),
    wnominate = as.character(packageVersion("wnominate")),
    jsonlite = as.character(packageVersion("jsonlite"))
  ),
  source = list(
    members = nrow(votes),
    rollcalls = ncol(votes),
    binary_observations = sum(!is.na(votes))
  ),
  baseline_technical_anchor = list(
    diputado_id = baseline_anchor$id,
    diputado_nombre = baseline_anchor$name,
    selection_rule = "Mayor valor absoluto del primer vector singular de la matriz base centrada, con missing imputado a la media de cada roll call y minvotes >= 20. El signo no tiene interpretación política."
  ),
  completed_specs = names(results_by_spec),
  failed_specs = errors,
  methodological_warnings = c(
    "Resultados experimentales: no integrar todavía en la ficha pública.",
    "El signo de la dimensión es arbitrario y la alineación entre especificaciones es técnica.",
    "La concentración de múltiples roll calls en un mismo boletín se evalúa mediante deduplicación y caps de sensibilidad; los caps no constituyen una especificación sustantivamente preferida.",
    "No denominar la dimensión izquierda/derecha, oficialismo/oposición o ideología sin validación sustantiva posterior."
  )
)
write_json(summary_json, file.path(out_dir, "diagnostics.json"), pretty = TRUE, auto_unbox = TRUE, na = "null")

message(sprintf(
  "W-NOMINATE experimental completado: %d/%d especificaciones · salida %s",
  length(results_by_spec), nrow(specs), out_dir
))
