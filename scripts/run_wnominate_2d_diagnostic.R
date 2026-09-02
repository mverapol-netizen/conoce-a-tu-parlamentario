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
out_dir <- file.path(base_dir, "wnominate", "two_dimensional")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

matrix_df <- read.csv(
  file.path(base_dir, "rollcall_matrix_binary.csv"),
  check.names = FALSE,
  na.strings = c("", "NA"),
  stringsAsFactors = FALSE,
  fileEncoding = "UTF-8-BOM"
)
meta <- read.csv(
  file.path(base_dir, "rollcall_matrix_metadata.csv"),
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
if (any(is.na(meta$vote_id))) stop("Hay votos sin metadatos")

specs <- data.frame(
  spec_id = c("raw_lop025_2d", "raw_lop050_2d", "cap20_balanced_lop025_2d"),
  lop = c(0.025, 0.050, 0.025),
  bill_cap = c(NA, NA, 20),
  stringsAsFactors = FALSE
)

eligible_ids <- function(lop) {
  keep <- meta$minority_count > 0 & meta$minority_share_binary >= lop
  meta$vote_id[keep]
}

cap_ids_by_bill <- function(ids, cap) {
  if (is.na(cap)) return(ids)
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

select_ids <- function(lop, cap) {
  ids <- eligible_ids(lop)
  cap_ids_by_bill(ids, cap)
}

technical_anchors_2d <- function(ids, minvotes = 20) {
  x <- votes[, ids, drop = FALSE]
  counts <- rowSums(!is.na(x))
  eligible <- counts >= minvotes
  if (sum(eligible) < 3) stop("No hay suficientes diputados elegibles para 2D")

  means <- colMeans(x, na.rm = TRUE)
  z <- sweep(x, 2, means, FUN = "-")
  z[is.na(z)] <- 0
  z_e <- z[eligible, , drop = FALSE]
  sv <- svd(z_e, nu = 2, nv = 0)
  eligible_idx <- which(eligible)

  anchor1_local <- which.max(abs(sv$u[, 1]))
  anchor1 <- eligible_idx[anchor1_local]

  candidates <- seq_len(nrow(sv$u))
  candidates <- candidates[candidates != anchor1_local]
  anchor2_local <- candidates[which.max(abs(sv$u[candidates, 2]))]
  anchor2 <- eligible_idx[anchor2_local]

  list(
    indices = c(anchor1, anchor2),
    ids = c(member_ids[anchor1], member_ids[anchor2]),
    names = c(member_names[anchor1], member_names[anchor2]),
    binary_votes = c(counts[anchor1], counts[anchor2])
  )
}

fit_value <- function(fits, name) {
  if (!is.null(names(fits)) && name %in% names(fits)) return(as.numeric(fits[[name]]))
  NA_real_
}

member_rows <- list()
model_rows <- list()
rollcall_rows <- list()
errors <- list()

for (i in seq_len(nrow(specs))) {
  spec <- specs[i, , drop = FALSE]
  spec_id <- spec$spec_id
  message(sprintf("[2D] Ejecutando %s", spec_id))

  result <- tryCatch({
    ids <- select_ids(spec$lop, spec$bill_cap)
    anchors <- technical_anchors_2d(ids)
    x <- votes[, ids, drop = FALSE]
    counts <- rowSums(!is.na(x))

    rc <- pscl::rollcall(
      data = x,
      yea = 1,
      nay = 0,
      missing = NA,
      notInLegis = 9,
      legis.names = rownames(x),
      vote.names = ids,
      desc = paste("Cámara de Diputadas y Diputados de Chile 2026 · diagnóstico 2D", spec_id),
      source = "Conoce a tu parlamentario · Cámara de Diputadas y Diputados"
    )

    fit <- wnominate::wnominate(
      rc,
      dims = 2,
      minvotes = 20,
      lop = spec$lop,
      polarity = anchors$indices,
      trials = 1
    )

    leg <- fit$legislators
    rcf <- fit$rollcalls

    members <- data.frame(
      spec_id = spec_id,
      diputado_id = member_ids,
      diputado_nombre = member_names,
      binary_votes_selected = counts,
      dimension_1_raw = as.numeric(leg$coord1D),
      dimension_2_raw = as.numeric(leg$coord2D),
      se_1d = as.numeric(leg$se1D),
      se_2d = as.numeric(leg$se2D),
      gmp = as.numeric(leg$GMP),
      correctly_classified = as.numeric(leg$CC),
      stringsAsFactors = FALSE
    )

    rollcalls <- data.frame(
      spec_id = spec_id,
      vote_id = ids,
      boletin = meta$boletin[match(ids, meta$vote_id)],
      fecha = meta$fecha[match(ids, meta$vote_id)],
      spread_1d = as.numeric(rcf$spread1D),
      spread_2d = as.numeric(rcf$spread2D),
      midpoint_1d = as.numeric(rcf$midpoint1D),
      midpoint_2d = as.numeric(rcf$midpoint2D),
      gmp = as.numeric(rcf$GMP),
      apre = as.numeric(rcf$PRE),
      stringsAsFactors = FALSE
    )

    fits <- fit$fits
    model <- data.frame(
      spec_id = spec_id,
      lop = spec$lop,
      bill_cap = spec$bill_cap,
      selected_rollcalls = length(ids),
      estimated_rollcalls = sum(!is.na(rcf$GMP)),
      estimated_members = sum(!is.na(leg$coord1D)),
      anchor1_id = anchors$ids[1],
      anchor1_name = anchors$names[1],
      anchor2_id = anchors$ids[2],
      anchor2_name = anchors$names[2],
      correct_classification_1d = fit_value(fits, "correctclass1D"),
      correct_classification_2d = fit_value(fits, "correctclass2D"),
      delta_correct_classification = fit_value(fits, "correctclass2D") - fit_value(fits, "correctclass1D"),
      apre_1d = fit_value(fits, "apre1D"),
      apre_2d = fit_value(fits, "apre2D"),
      delta_apre = fit_value(fits, "apre2D") - fit_value(fits, "apre1D"),
      gmp_1d = fit_value(fits, "gmp1D"),
      gmp_2d = fit_value(fits, "gmp2D"),
      delta_gmp = fit_value(fits, "gmp2D") - fit_value(fits, "gmp1D"),
      eigenvalue_1 = if (length(fit$eigenvalues) >= 1) as.numeric(fit$eigenvalues[1]) else NA_real_,
      eigenvalue_2 = if (length(fit$eigenvalues) >= 2) as.numeric(fit$eigenvalues[2]) else NA_real_,
      beta = if (length(fit$beta)) as.numeric(fit$beta[1]) else NA_real_,
      weight_1 = if (length(fit$weights) >= 1) as.numeric(fit$weights[1]) else NA_real_,
      weight_2 = if (length(fit$weights) >= 2) as.numeric(fit$weights[2]) else NA_real_,
      stringsAsFactors = FALSE
    )

    list(members = members, rollcalls = rollcalls, model = model)
  }, error = function(e) e)

  if (inherits(result, "error")) {
    errors[[spec_id]] <- conditionMessage(result)
    message(sprintf("[2D] ERROR %s: %s", spec_id, conditionMessage(result)))
  } else {
    member_rows[[spec_id]] <- result$members
    rollcall_rows[[spec_id]] <- result$rollcalls
    model_rows[[spec_id]] <- result$model
  }
}

if (length(model_rows) < 2 || !("raw_lop025_2d" %in% names(model_rows))) {
  stop(sprintf("Diagnóstico 2D insuficiente. Errores: %s", paste(names(errors), unlist(errors), collapse = " | ")))
}

members_all <- do.call(rbind, member_rows)
rollcalls_all <- do.call(rbind, rollcall_rows)
models_all <- do.call(rbind, model_rows)
rownames(members_all) <- NULL
rownames(rollcalls_all) <- NULL
rownames(models_all) <- NULL

write.csv(members_all, file.path(out_dir, "member_coordinates_2d.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(rollcalls_all, file.path(out_dir, "rollcall_coordinates_2d.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(models_all, file.path(out_dir, "model_diagnostics_2d.csv"), row.names = FALSE, fileEncoding = "UTF-8")

summary <- list(
  generated_for = as.character(Sys.Date()),
  status = if (length(errors)) "PARTIAL" else "PASS",
  completed_specs = names(model_rows),
  failed_specs = errors,
  package_versions = list(
    R = R.version.string,
    pscl = as.character(packageVersion("pscl")),
    wnominate = as.character(packageVersion("wnominate"))
  ),
  anchor_rule = "Dos anclas técnicas elegidas como extremos absolutos de los dos primeros vectores singulares de la matriz centrada de cada especificación. No tienen significado político sustantivo.",
  interpretation_rule = "La segunda dimensión solo se considerará sustantivamente útil si mejora el ajuste de forma relevante y muestra estructura estable e interpretable. Su mera estimabilidad no justifica publicarla.",
  warnings = c(
    "Diagnóstico experimental, no público.",
    "La orientación y rotación de un espacio multidimensional dependen de restricciones de identificación.",
    "No denominar las dimensiones izquierda/derecha u otra categoría sustantiva sin validación posterior."
  )
)
write_json(summary, file.path(out_dir, "diagnostics_2d.json"), pretty = TRUE, auto_unbox = TRUE, na = "null")

message(sprintf("Diagnóstico W-NOMINATE 2D completado: %d/%d especificaciones", length(model_rows), nrow(specs)))
