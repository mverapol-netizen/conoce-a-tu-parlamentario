#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(pscl)
  library(wnominate)
  library(jsonlite)
})

options(stringsAsFactors = FALSE)

args_full <- commandArgs(trailingOnly = FALSE)
file_arg <- sub("^--file=", "", args_full[grep("^--file=", args_full)])
root <- normalizePath(file.path(dirname(file_arg), ".."), mustWork = TRUE)

base_dir <- file.path(root, "data", "legislative", "2026")
out_dir <- file.path(base_dir, "wnominate", "research_1d")
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
meta$boletin <- trimws(as.character(meta$boletin))
meta$fecha <- as.character(meta$fecha)
meta$minority_count <- as.numeric(meta$minority_count)
meta$minority_share_binary <- as.numeric(meta$minority_share_binary)
meta$binary_participation_share <- as.numeric(meta$binary_participation_share)
meta <- meta[match(vote_ids, meta$vote_id), , drop = FALSE]

if (any(is.na(meta$vote_id))) stop("Hay columnas de la matriz sin metadatos")
if (!all(votes[!is.na(votes)] %in% c(0, 1))) stop("La matriz contiene códigos distintos de 0/1/NA")

BASE_LOP <- 0.025
ABS_MINVOTES <- 20
RELATIVE_REFERENCE <- 0.10
RELATIVE_SENSITIVITIES <- c(0.10, 0.20, 0.30)
WNOMINATE_TRIALS <- 501
CLUSTER_BOOTSTRAP_REPS <- 200
SEED_WNOMINATE <- 20260902L
SEED_CLUSTER_BOOTSTRAP <- 20260903L

eligible_vote_ids <- function(lop = BASE_LOP) {
  keep <- !is.na(meta$minority_count) &
    meta$minority_count > 0 &
    !is.na(meta$minority_share_binary) &
    meta$minority_share_binary >= lop
  meta$vote_id[keep]
}

base_ids <- eligible_vote_ids(BASE_LOP)
if (length(base_ids) < 20) stop("Muy pocos roll calls elegibles para la corrida research")

# En el snapshot actual cada roll call tiene una observación para los 155 integrantes.
# Por ello la oportunidad analítica de referencia es el número de roll calls elegibles.
# Si en el futuro aparecen reemplazos/altas/bajas legislativas, esta regla deberá usar
# explícitamente intervalos de pertenencia antes de ejecutar la corrida research.
opportunities <- rep(length(base_ids), length(member_ids))
binary_counts <- rowSums(!is.na(votes[, base_ids, drop = FALSE]))

eligibility <- data.frame(
  diputado_id = member_ids,
  diputado_nombre = member_names,
  opportunities = opportunities,
  binary_votes = binary_counts,
  participation_share = ifelse(opportunities > 0, binary_counts / opportunities, NA_real_),
  stringsAsFactors = FALSE
)

for (rate in RELATIVE_SENSITIVITIES) {
  suffix <- sprintf("%02d", as.integer(round(rate * 100)))
  threshold <- pmax(ABS_MINVOTES, ceiling(opportunities * rate))
  eligibility[[paste0("required_votes_", suffix, "pct")]] <- threshold
  eligibility[[paste0("eligible_", suffix, "pct")]] <- binary_counts >= threshold
}

reference_col <- "eligible_10pct"
eligible_members <- eligibility[[reference_col]]
if (sum(eligible_members) < 2) stop("No hay suficientes integrantes elegibles con regla relativa 10% + min 20")

write.csv(
  eligibility,
  file.path(out_dir, "member_eligibility.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

technical_anchor <- function(x, ids, names, minvotes = ABS_MINVOTES) {
  counts <- rowSums(!is.na(x))
  eligible <- counts >= minvotes
  if (sum(eligible) < 2) stop("No hay suficientes legisladores para seleccionar ancla técnica")
  means <- colMeans(x, na.rm = TRUE)
  z <- sweep(x, 2, means, FUN = "-")
  z[is.na(z)] <- 0
  z <- z[eligible, , drop = FALSE]
  s <- svd(z, nu = 1, nv = 0)
  score <- s$u[, 1]
  eligible_indices <- which(eligible)
  idx <- eligible_indices[which.max(abs(score))]
  list(index = idx, id = ids[idx], name = names[idx], binary_votes = counts[idx])
}

x_base <- votes[eligible_members, base_ids, drop = FALSE]
ids_base_members <- member_ids[eligible_members]
names_base_members <- member_names[eligible_members]
anchor <- technical_anchor(x_base, ids_base_members, names_base_members)

rc_base <- pscl::rollcall(
  data = x_base,
  yea = 1,
  nay = 0,
  missing = NA,
  notInLegis = 9,
  legis.names = rownames(x_base),
  vote.names = base_ids,
  desc = "Cámara de Diputadas y Diputados de Chile 2026 · W-NOMINATE 1D research",
  source = "Conoce a tu parlamentario · Cámara de Diputadas y Diputados"
)

message(sprintf(
  "[research-1D] Base: %d integrantes · %d roll calls · trials=%d",
  nrow(x_base), ncol(x_base), WNOMINATE_TRIALS
))
set.seed(SEED_WNOMINATE)
fit_base <- wnominate::wnominate(
  rc_base,
  dims = 1,
  minvotes = ABS_MINVOTES,
  lop = BASE_LOP,
  polarity = anchor$index,
  trials = WNOMINATE_TRIALS
)
saveRDS(fit_base, file.path(out_dir, "wnominate_1d_research_fit.rds"))

leg <- fit_base$legislators
rcfit <- fit_base$rollcalls
base_coordinates <- data.frame(
  diputado_id = ids_base_members,
  diputado_nombre = names_base_members,
  opportunities = eligibility$opportunities[eligible_members],
  binary_votes = eligibility$binary_votes[eligible_members],
  participation_share = eligibility$participation_share[eligible_members],
  dimension_1_raw = as.numeric(leg$coord1D),
  se_wnominate_501 = as.numeric(leg$se1D),
  gmp = as.numeric(leg$GMP),
  correctly_classified = as.numeric(leg$CC),
  stringsAsFactors = FALSE
)
write.csv(
  base_coordinates,
  file.path(out_dir, "member_coordinates_research.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

rollcall_coordinates <- data.frame(
  vote_id = base_ids,
  boletin = meta$boletin[match(base_ids, meta$vote_id)],
  fecha = meta$fecha[match(base_ids, meta$vote_id)],
  minority_share_binary = meta$minority_share_binary[match(base_ids, meta$vote_id)],
  binary_participation_share = meta$binary_participation_share[match(base_ids, meta$vote_id)],
  spread_1d = as.numeric(rcfit$spread1D),
  midpoint_1d = as.numeric(rcfit$midpoint1D),
  gmp = as.numeric(rcfit$GMP),
  apre = as.numeric(rcfit$PRE),
  stringsAsFactors = FALSE
)
write.csv(
  rollcall_coordinates,
  file.path(out_dir, "rollcall_coordinates_research.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

# Bootstrap agrupado por boletín/proyecto. Votaciones sin boletín se tratan como
# clusters unitarios para no crear un falso mega-cluster de registros vacíos.
cluster_id <- meta$boletin[match(base_ids, meta$vote_id)]
blank_cluster <- is.na(cluster_id) | cluster_id == ""
cluster_id[blank_cluster] <- paste0("__vote_", base_ids[blank_cluster])
clusters <- split(base_ids, cluster_id)
cluster_names <- names(clusters)

baseline_coord <- setNames(base_coordinates$dimension_1_raw, base_coordinates$diputado_id)
baseline_anchor_row <- match(anchor$id, ids_base_members)

bootstrap_rows <- vector("list", CLUSTER_BOOTSTRAP_REPS)
bootstrap_diag <- vector("list", CLUSTER_BOOTSTRAP_REPS)
set.seed(SEED_CLUSTER_BOOTSTRAP)

for (b in seq_len(CLUSTER_BOOTSTRAP_REPS)) {
  sampled_clusters <- sample(cluster_names, length(cluster_names), replace = TRUE)
  sampled_ids <- unlist(clusters[sampled_clusters], use.names = FALSE)
  x_rep <- x_base[, sampled_ids, drop = FALSE]
  colnames(x_rep) <- paste0(sampled_ids, "__boot", sprintf("%03d", b), "__", seq_along(sampled_ids))

  counts_rep <- rowSums(!is.na(x_rep))
  rep_anchor <- baseline_anchor_row
  if (is.na(rep_anchor) || counts_rep[rep_anchor] < ABS_MINVOTES) {
    alt <- technical_anchor(x_rep, ids_base_members, names_base_members)
    rep_anchor <- alt$index
  }

  rc_rep <- pscl::rollcall(
    data = x_rep,
    yea = 1,
    nay = 0,
    missing = NA,
    notInLegis = 9,
    legis.names = rownames(x_rep),
    vote.names = colnames(x_rep),
    desc = paste("Cluster bootstrap by bill", b),
    source = "Conoce a tu parlamentario"
  )

  result <- tryCatch(
    wnominate::wnominate(
      rc_rep,
      dims = 1,
      minvotes = ABS_MINVOTES,
      lop = BASE_LOP,
      polarity = rep_anchor,
      trials = 1
    ),
    error = function(e) e
  )

  if (inherits(result, "error")) {
    bootstrap_diag[[b]] <- data.frame(
      replicate = b,
      status = "ERROR",
      sampled_clusters = length(sampled_clusters),
      unique_clusters = length(unique(sampled_clusters)),
      sampled_rollcalls = length(sampled_ids),
      estimated_members = 0,
      sign_flipped = NA,
      correlation_to_baseline = NA_real_,
      error = conditionMessage(result),
      stringsAsFactors = FALSE
    )
    next
  }

  coord <- as.numeric(result$legislators$coord1D)
  names(coord) <- ids_base_members
  common <- intersect(names(coord)[!is.na(coord)], names(baseline_coord)[!is.na(baseline_coord)])
  rho <- if (length(common) >= 3) {
    suppressWarnings(cor(coord[common], baseline_coord[common], use = "complete.obs"))
  } else {
    NA_real_
  }
  flip <- !is.na(rho) && rho < 0
  if (flip) coord <- -coord

  bootstrap_rows[[b]] <- data.frame(
    replicate = b,
    diputado_id = ids_base_members,
    dimension_1_aligned = as.numeric(coord[ids_base_members]),
    stringsAsFactors = FALSE
  )
  bootstrap_diag[[b]] <- data.frame(
    replicate = b,
    status = "PASS",
    sampled_clusters = length(sampled_clusters),
    unique_clusters = length(unique(sampled_clusters)),
    sampled_rollcalls = length(sampled_ids),
    estimated_members = sum(!is.na(coord)),
    sign_flipped = flip,
    correlation_to_baseline = if (flip && !is.na(rho)) -rho else rho,
    error = "",
    stringsAsFactors = FALSE
  )

  if (b %% 20 == 0) message(sprintf("[research-1D] Bootstrap %d/%d", b, CLUSTER_BOOTSTRAP_REPS))
}

bootstrap_rep <- do.call(rbind, bootstrap_rows[!vapply(bootstrap_rows, is.null, logical(1))])
bootstrap_diag_df <- do.call(rbind, bootstrap_diag[!vapply(bootstrap_diag, is.null, logical(1))])
if (is.null(bootstrap_rep) || nrow(bootstrap_rep) == 0) stop("Fallaron todas las réplicas del bootstrap agrupado")

write.csv(
  bootstrap_rep,
  file.path(out_dir, "cluster_bootstrap_replicates.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
write.csv(
  bootstrap_diag_df,
  file.path(out_dir, "cluster_bootstrap_diagnostics.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

member_boot <- lapply(ids_base_members, function(id) {
  z <- bootstrap_rep$dimension_1_aligned[bootstrap_rep$diputado_id == id]
  z <- z[!is.na(z)]
  base_value <- baseline_coord[[id]]
  if (!length(z)) {
    return(data.frame(
      diputado_id = id, n_success = 0, baseline_coord = base_value,
      bootstrap_mean = NA_real_, bootstrap_sd = NA_real_, q025 = NA_real_, q975 = NA_real_,
      interval_width = NA_real_, stringsAsFactors = FALSE
    ))
  }
  qs <- quantile(z, probs = c(0.025, 0.975), na.rm = TRUE, names = FALSE, type = 7)
  data.frame(
    diputado_id = id,
    n_success = length(z),
    baseline_coord = base_value,
    bootstrap_mean = mean(z),
    bootstrap_sd = if (length(z) > 1) sd(z) else NA_real_,
    q025 = qs[1],
    q975 = qs[2],
    interval_width = qs[2] - qs[1],
    stringsAsFactors = FALSE
  )
})
member_boot <- do.call(rbind, member_boot)
member_boot$diputado_nombre <- names_base_members[match(member_boot$diputado_id, ids_base_members)]
member_boot <- member_boot[, c(
  "diputado_id", "diputado_nombre", "n_success", "baseline_coord", "bootstrap_mean",
  "bootstrap_sd", "q025", "q975", "interval_width"
)]
write.csv(
  member_boot,
  file.path(out_dir, "cluster_bootstrap_member_summary.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

fits <- fit_base$fits
get_fit <- function(name) {
  if (!is.null(names(fits)) && name %in% names(fits)) return(as.numeric(fits[[name]]))
  NA_real_
}

successful_bootstrap <- sum(bootstrap_diag_df$status == "PASS")
median_boot_corr <- median(bootstrap_diag_df$correlation_to_baseline[bootstrap_diag_df$status == "PASS"], na.rm = TRUE)
min_success_member <- min(member_boot$n_success, na.rm = TRUE)

input_md5 <- as.list(tools::md5sum(c(matrix_path, metadata_path)))
names(input_md5) <- c("rollcall_matrix_binary", "rollcall_matrix_metadata")

summary_json <- list(
  generated_for = as.character(Sys.Date()),
  status = if (successful_bootstrap >= ceiling(CLUSTER_BOOTSTRAP_REPS * 0.90)) "PASS" else "PARTIAL",
  mode = "research",
  git_sha = Sys.getenv("GITHUB_SHA", unset = NA_character_),
  package_versions = list(
    R = R.version.string,
    pscl = as.character(packageVersion("pscl")),
    wnominate = as.character(packageVersion("wnominate")),
    jsonlite = as.character(packageVersion("jsonlite"))
  ),
  input_md5 = input_md5,
  universe = list(
    members_total = length(member_ids),
    rollcalls_total = length(vote_ids),
    base_lop = BASE_LOP,
    rollcalls_selected = length(base_ids),
    clusters_selected = length(cluster_names)
  ),
  participation_rule = list(
    reference_relative_rate = RELATIVE_REFERENCE,
    absolute_minimum = ABS_MINVOTES,
    members_eligible_reference = sum(eligible_members),
    sensitivities = RELATIVE_SENSITIVITIES,
    note = "En este snapshot cada roll call tiene una observación para los 155 integrantes; oportunidad = roll calls elegibles. Futuras altas/bajas requieren intervalos explícitos de pertenencia."
  ),
  baseline = list(
    wnominate_trials = WNOMINATE_TRIALS,
    seed = SEED_WNOMINATE,
    anchor_diputado_id = anchor$id,
    anchor_diputado_nombre = anchor$name,
    correct_classification_1d = get_fit("correctclass1D"),
    apre_1d = get_fit("apre1D"),
    gmp_1d = get_fit("gmp1D")
  ),
  cluster_bootstrap = list(
    grouping = "boletin/proyecto; roll calls sin boletin como cluster unitario",
    requested_replicates = CLUSTER_BOOTSTRAP_REPS,
    successful_replicates = successful_bootstrap,
    seed = SEED_CLUSTER_BOOTSTRAP,
    median_correlation_to_baseline = median_boot_corr,
    minimum_successful_replicates_for_any_member = min_success_member,
    interpretation = "Intervalos de sensibilidad a composición/dependencia por proyecto; no sustituyen el bootstrap paramétrico interno de W-NOMINATE."
  ),
  methodological_warnings = c(
    "Resultado interno de investigación; no publicar todavía en fichas.",
    "El signo de D1 es arbitrario; el bootstrap solo se alinea por reflexión respecto de la corrida base.",
    "Los errores estándar se obtienen con 501 trials en la corrida base; las 200 réplicas agrupadas por boletín estiman sensibilidad adicional a dependencia/composición por proyecto.",
    "No denominar D1 izquierda/derecha, oficialismo/oposición o ideología sin validación sustantiva posterior."
  )
)
write_json(
  summary_json,
  file.path(out_dir, "diagnostics.json"),
  pretty = TRUE,
  auto_unbox = TRUE,
  na = "null"
)

message(sprintf(
  "[research-1D] Completado: base trials=%d · bootstrap agrupado %d/%d · salida %s",
  WNOMINATE_TRIALS, successful_bootstrap, CLUSTER_BOOTSTRAP_REPS, out_dir
))
