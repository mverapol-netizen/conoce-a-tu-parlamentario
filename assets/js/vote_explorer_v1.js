(() => {
  const root = document.getElementById('vote-explorer-root');
  if (!root || !window.CSV_UTILS) return;

  const { fetchCsv, normalize, escapeHtml, formatDate } = window.CSV_UTILS;
  const MAX_RESULTS = 80;
  let votes = [];
  let projectsByBulletin = new Map();

  const exactObject = (vote) => vote.articulo || vote.descripcion || `Boletín ${vote.boletin || 'sin identificar'}`;

  const renderResults = (items, query = '') => {
    if (!items.length) {
      root.innerHTML = `<div class="vote-empty">No encontramos votaciones para <strong>${escapeHtml(query)}</strong>. Prueba con un boletín, una palabra del proyecto o una expresión del objeto votado.</div>`;
      return;
    }
    root.innerHTML = `<div class="vote-results">${items.slice(0, MAX_RESULTS).map((vote) => {
      const project = projectsByBulletin.get(vote.boletin);
      const title = project?.titulo || `Boletín ${vote.boletin || 'sin identificar'}`;
      const object = exactObject(vote);
      const detail = new URL('votacion.html', window.location.href);
      detail.searchParams.set('id', vote.vote_id);
      return `<a class="vote-result" href="${escapeHtml(detail.pathname + detail.search)}"><div><h2>${escapeHtml(title)}</h2><p><strong>${escapeHtml(formatDate(vote.fecha))}</strong> · ${escapeHtml(vote.tipo_votacion_proyecto || vote.tipo_votacion || 'Votación')} · ${escapeHtml(object)}</p></div><div class="vote-side"><span class="vote-pill">ID ${escapeHtml(vote.vote_id)}</span><span class="vote-pill">${escapeHtml(vote.resultado || 'Sin resultado')}</span><span class="vote-pill">${escapeHtml(vote.quorum || 'Quórum no informado')}</span></div></a>`;
    }).join('')}</div>${items.length > MAX_RESULTS ? `<p class="vote-help">Mostramos los primeros ${MAX_RESULTS} resultados de ${items.length}. Refina la búsqueda para acotar.</p>` : ''}`;
  };

  const search = (query) => {
    const q = normalize(query);
    const sorted = [...votes].sort((a, b) => String(b.fecha).localeCompare(String(a.fecha)) || Number(b.vote_id || 0) - Number(a.vote_id || 0));
    if (!q) {
      renderResults(sorted.slice(0, 30));
      return;
    }
    const terms = q.split(' ').filter(Boolean);
    const matches = sorted.filter((vote) => {
      const project = projectsByBulletin.get(vote.boletin);
      const haystack = normalize([
        vote.vote_id,
        vote.boletin,
        vote.fecha,
        vote.tipo_votacion,
        vote.tipo_votacion_proyecto,
        vote.resultado,
        vote.quorum,
        vote.tramite_constitucional,
        vote.tramite_reglamentario,
        vote.descripcion,
        vote.articulo,
        project?.titulo
      ].filter(Boolean).join(' '));
      return terms.every((term) => haystack.includes(term));
    });
    renderResults(matches, query);
  };

  const init = async () => {
    root.innerHTML = '<div class="vote-loading">Cargando votaciones nominales…</div>';
    try {
      const [rawVotes, projects] = await Promise.all([
        fetchCsv('data/legislative/2026/rollcalls.csv'),
        fetchCsv('data/legislative/2026/projects.csv')
      ]);
      votes = rawVotes;
      projectsByBulletin = new Map(projects.map((project) => [project.boletin, project]));
      search('');
      const input = document.getElementById('vote-search');
      input?.addEventListener('input', () => search(input.value));
      input?.focus();
    } catch (error) {
      root.innerHTML = `<div class="vote-error"><strong>No pudimos cargar las votaciones.</strong><br>${escapeHtml(error.message)}</div>`;
    }
  };

  init();
})();
