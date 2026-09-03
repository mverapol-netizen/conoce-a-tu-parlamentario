(() => {
  const root = document.getElementById('project-results');
  const input = document.getElementById('project-search');
  const count = document.getElementById('project-count');
  if (!root || !input || !window.CSV_UTILS) return;

  const { fetchCsv, normalize, escapeHtml, formatDate } = window.CSV_UTILS;
  let projects = [];

  const rankProject = (project, term) => {
    if (!term) return 0;
    const bulletin = normalize(project.boletin);
    const title = normalize(project.titulo);
    if (bulletin === term) return 100;
    if (bulletin.startsWith(term)) return 90;
    if (title.startsWith(term)) return 70;
    if (title.includes(term)) return 50;
    return 0;
  };

  const render = () => {
    const term = normalize(input.value);
    let rows;
    if (!term) {
      rows = [...projects]
        .sort((a, b) => String(b.fecha_ingreso).localeCompare(String(a.fecha_ingreso)) || String(b.project_id).localeCompare(String(a.project_id)))
        .slice(0, 18);
    } else {
      rows = projects
        .map((project) => ({ project, score: rankProject(project, term) }))
        .filter((item) => item.score > 0)
        .sort((a, b) => b.score - a.score || String(b.project.fecha_ingreso).localeCompare(String(a.project.fecha_ingreso)))
        .slice(0, 30)
        .map((item) => item.project);
    }

    if (count) count.textContent = term ? `${rows.length} coincidencia${rows.length === 1 ? '' : 's'}` : `${projects.length} proyectos en la base · mostrando los más recientes`;
    if (!rows.length) {
      root.innerHTML = `<div class="project-empty">No encontramos proyectos que coincidan con <strong>${escapeHtml(input.value)}</strong>. Prueba con el boletín sin puntos o con palabras del título.</div>`;
      return;
    }

    root.innerHTML = rows.map((project) => `
      <a class="project-result" href="proyecto.html?boletin=${encodeURIComponent(project.boletin)}">
        <div>
          <h2>${escapeHtml(project.titulo)}</h2>
          <p>Boletín ${escapeHtml(project.boletin)} · ingreso ${escapeHtml(formatDate(project.fecha_ingreso))}</p>
        </div>
        <div class="project-result-side">
          <span class="project-pill">${escapeHtml(project.tipo_iniciativa || project.origen_iniciativa || 'Iniciativa')}</span>
          <span class="project-pill">${escapeHtml(project.estado_actual || 'Estado no informado')}</span>
        </div>
      </a>`).join('');
  };

  const init = async () => {
    root.innerHTML = '<div class="project-loading">Cargando proyectos del período 2026–2030…</div>';
    try {
      projects = await fetchCsv('data/legislative/2026/projects.csv');
      input.disabled = false;
      render();
    } catch (error) {
      root.innerHTML = `<div class="project-error"><strong>No pudimos cargar la base de proyectos.</strong><br>${escapeHtml(error.message)}</div>`;
    }
  };

  input.disabled = true;
  input.addEventListener('input', render);
  init();
})();
