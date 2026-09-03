(() => {
  const root = document.getElementById('project-detail-root');
  if (!root || !window.CSV_UTILS) return;

  const { fetchCsv, escapeHtml, formatDate } = window.CSV_UTILS;
  const bulletin = new URLSearchParams(window.location.search).get('boletin')?.trim();

  const safeUrl = (value) => /^https:\/\//i.test(String(value || '')) ? String(value) : '';
  const asNumber = (value) => Number.parseInt(value, 10) || 0;

  const renderAuthors = (authors, project) => {
    if (authors.length) {
      return `<section class="project-section"><h2>Autoría formal</h2><p class="project-section-lead">Autores registrados para esta iniciativa. La autoría formal no resume todas las intervenciones posteriores sobre el texto.</p><div class="project-authors">${authors.map((author) => `<span class="project-author">${escapeHtml(author.author_name)} · ${escapeHtml(author.author_chamber)}</span>`).join('')}</div></section>`;
    }
    if (String(project.tipo_iniciativa).toLocaleLowerCase('es-CL').includes('mensaje') || String(project.origen_iniciativa).toLocaleLowerCase('es-CL').includes('ejecut')) {
      return `<section class="project-section"><h2>Origen de la iniciativa</h2><p class="project-section-lead">Este proyecto figura como iniciativa del Ejecutivo. La base de autores parlamentarios se usa para mociones y no debe inventar una autoría individual donde la fuente no la registra.</p></section>`;
    }
    return '';
  };

  const renderEvents = (events) => {
    if (!events.length) return '<div class="project-empty">No hay eventos de tramitación recolectados para este boletín en la base actual.</div>';
    return `<div class="project-timeline">${events.map((event) => {
      const doc = safeUrl(event.documento_url);
      return `<article class="project-event"><div class="project-event-date">${escapeHtml(formatDate(event.fecha))}</div><span class="project-event-dot" aria-hidden="true"></span><div class="project-event-body"><strong>${escapeHtml(event.subetapa || 'Evento de tramitación')}</strong><small>${escapeHtml(event.etapa || 'Etapa no informada')}${event.sesion ? ` · Sesión ${escapeHtml(event.sesion)}` : ''}</small>${doc ? `<a href="${escapeHtml(doc)}" target="_blank" rel="noopener noreferrer">Abrir documento oficial</a>` : ''}</div></article>`;
    }).join('')}</div>`;
  };

  const renderVotes = (votes) => {
    if (!votes.length) return '<div class="project-empty">No hay votaciones nominales de Sala vinculadas a este boletín en la base actual.</div>';
    return `<div class="project-votes">${votes.map((vote) => {
      const exactObject = vote.articulo || vote.descripcion || `Boletín ${vote.boletin}`;
      const source = safeUrl(vote.verification_url);
      return `<article class="project-vote"><div class="project-vote-head"><div><h3>${escapeHtml(formatDate(vote.fecha))} · ${escapeHtml(vote.tipo_votacion_proyecto || vote.tipo_votacion || 'Votación')}</h3><span class="project-pill">${escapeHtml(vote.resultado || 'Resultado no informado')}</span></div><span class="project-pill">${escapeHtml(vote.quorum || 'Quórum no informado')}</span></div><p class="project-vote-object"><strong>Objeto registrado:</strong> ${escapeHtml(exactObject)}</p><div class="project-vote-meta"><span class="project-pill">${escapeHtml(vote.tramite_constitucional || 'Trámite no informado')}</span>${vote.tramite_reglamentario ? `<span class="project-pill">${escapeHtml(vote.tramite_reglamentario)}</span>` : ''}${vote.sesion_numero ? `<span class="project-pill">Sesión ${escapeHtml(vote.sesion_numero)}</span>` : ''}</div><div class="project-counts"><span class="project-count">A favor ${asNumber(vote.total_si)}</span><span class="project-count">En contra ${asNumber(vote.total_no)}</span><span class="project-count">Abstención ${asNumber(vote.total_abstencion)}</span>${asNumber(vote.total_dispensado) ? `<span class="project-count">Dispensado ${asNumber(vote.total_dispensado)}</span>` : ''}</div>${source ? `<a href="${escapeHtml(source)}" target="_blank" rel="noopener noreferrer">Ver votación oficial y detalle nominal</a>` : ''}</article>`;
    }).join('')}</div>`;
  };

  const render = (project, events, votes, authors) => {
    document.title = `Boletín ${project.boletin} · Sigue un proyecto`;
    const official = safeUrl(project.source_url);
    root.innerHTML = `
      <nav class="edu-breadcrumb" aria-label="Migas de pan"><a href="entender.html">Entiende el Congreso</a><span>›</span><a href="proyectos.html">Explorar proyectos</a><span>›</span><strong>Boletín ${escapeHtml(project.boletin)}</strong></nav>
      <div class="project-detail-grid">
        <article class="project-detail-card">
          <div class="project-kicker"><span class="project-pill">Boletín ${escapeHtml(project.boletin)}</span><span class="project-pill">${escapeHtml(project.tipo_iniciativa || project.origen_iniciativa || 'Iniciativa')}</span></div>
          <h1>${escapeHtml(project.titulo)}</h1>
          <div class="project-facts">
            <div class="project-fact"><span>Ingreso</span><strong>${escapeHtml(formatDate(project.fecha_ingreso))}</strong></div>
            <div class="project-fact"><span>Estado informado</span><strong>${escapeHtml(project.estado_actual || 'Sin estado')}</strong></div>
            <div class="project-fact"><span>Cámara de origen</span><strong>${escapeHtml(project.camara_origen || 'No informada')}</strong></div>
            <div class="project-fact"><span>Admisibilidad registrada</span><strong>${project.admisible === 'true' ? 'Sí' : project.admisible === 'false' ? 'No' : 'Sin dato'}</strong></div>
          </div>
          ${official ? `<a class="project-official-link" href="${escapeHtml(official)}" target="_blank" rel="noopener noreferrer">Abrir tramitación oficial</a>` : ''}
        </article>
        <aside class="project-detail-card">
          <p class="eyebrow">Cómo leer esta ficha</p>
          <h2 style="font-size:26px">Una historia, no un semáforo</h2>
          <p style="color:var(--muted)">El estado actual resume dónde está el proyecto. La línea de tiempo muestra cómo llegó allí. Las votaciones se presentan por separado porque una iniciativa puede tener decisiones generales, particulares, indicaciones u otros objetos distintos.</p>
          <a class="project-official-link" href="aprender.html?id=como-se-hace-una-ley">Entender el proceso legislativo</a>
        </aside>
      </div>
      ${renderAuthors(authors, project)}
      <section class="project-section"><h2>Historia de tramitación</h2><p class="project-section-lead">Eventos recolectados desde la ficha oficial de la Cámara. Se muestra la descripción institucional registrada, sin inventar una etapa intermedia cuando la fuente no la informa.</p>${renderEvents(events)}</section>
      <section class="project-section"><h2>Votaciones nominales de Sala vinculadas</h2><p class="project-section-lead">Cada tarjeta representa una decisión distinta. El objeto exacto importa: votar una disposición particular no equivale necesariamente a apoyar o rechazar todo el proyecto.</p>${renderVotes(votes)}<p class="project-caveat"><strong>Límite:</strong> esta primera vista conecta la base de la Cámara disponible en el proyecto. No pretende reconstruir todavía todas las actuaciones del Senado ni atribuir una “posición global” a cada parlamentario a partir de decisiones parciales.</p></section>`;
  };

  const init = async () => {
    if (!bulletin) {
      root.innerHTML = '<div class="project-error"><strong>Falta el boletín.</strong><br>Vuelve al explorador y selecciona un proyecto.</div>';
      return;
    }
    root.innerHTML = '<div class="project-loading">Reconstruyendo el proyecto desde la base legislativa…</div>';
    try {
      const [projects, allEvents, allVotes, allAuthors] = await Promise.all([
        fetchCsv('data/legislative/2026/projects.csv'),
        fetchCsv('data/legislative/2026/project_events.csv'),
        fetchCsv('data/legislative/2026/rollcalls.csv'),
        fetchCsv('data/legislative/2026/bill_authors.csv')
      ]);
      const project = projects.find((item) => item.boletin === bulletin);
      if (!project) {
        root.innerHTML = `<div class="project-error"><strong>No encontramos el boletín ${escapeHtml(bulletin)}.</strong><br>La vista interna contiene proyectos presentes en la base legislativa 2026–2030.</div>`;
        return;
      }
      const events = allEvents.filter((item) => item.boletin === bulletin).map((item, index) => ({ ...item, _index: index })).sort((a, b) => String(a.fecha).localeCompare(String(b.fecha)) || a._index - b._index);
      const votes = allVotes.filter((item) => item.boletin === bulletin).sort((a, b) => String(a.fecha).localeCompare(String(b.fecha)) || asNumber(a.vote_id) - asNumber(b.vote_id));
      const authors = allAuthors.filter((item) => item.boletin === bulletin).sort((a, b) => asNumber(a.author_order) - asNumber(b.author_order));
      render(project, events, votes, authors);
    } catch (error) {
      root.innerHTML = `<div class="project-error"><strong>No pudimos reconstruir el proyecto.</strong><br>${escapeHtml(error.message)}</div>`;
    }
  };

  init();
})();
