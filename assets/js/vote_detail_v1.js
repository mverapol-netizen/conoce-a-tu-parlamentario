(() => {
  const root = document.getElementById('vote-detail-root');
  if (!root || !window.CSV_UTILS) return;

  const { fetchCsv, escapeHtml, formatDate } = window.CSV_UTILS;
  const voteId = new URLSearchParams(window.location.search).get('id')?.trim();
  const safeUrl = (value) => /^https:\/\//i.test(String(value || '')) ? String(value) : '';
  const asNumber = (value) => Number.parseInt(value, 10) || 0;
  const lower = (value) => String(value || '').toLocaleLowerCase('es-CL');

  const explainType = (vote) => {
    const type = lower(vote.tipo_votacion_proyecto);
    if (type.includes('general')) return 'Esta decisión se refiere al proyecto en general o a la idea de legislar. No significa que cada artículo haya quedado aprobado en su versión definitiva.';
    if (type.includes('particular')) return 'Esta decisión recae sobre una parte específica del texto —por ejemplo, un artículo, numeral, indicación o disposición— y no debe traducirse automáticamente como apoyo o rechazo al proyecto completo.';
    return 'La base no clasifica esta decisión inequívocamente como general o particular. Por eso conservamos la descripción oficial y evitamos inferir más de lo registrado.';
  };

  const explainStage = (vote) => {
    const stage = lower(vote.tramite_constitucional);
    if (stage.includes('primer')) return 'Ocurrió durante el primer trámite constitucional, es decir, mientras la cámara de origen conocía el proyecto.';
    if (stage.includes('segundo')) return 'Ocurrió durante el segundo trámite constitucional, cuando la cámara revisora conocía el proyecto.';
    if (stage.includes('tercer')) return 'Ocurrió durante el tercer trámite, cuando la cámara de origen examinaba modificaciones de la cámara revisora.';
    return '';
  };

  const explainQuorum = (vote) => {
    const quorum = lower(vote.quorum);
    if (quorum.includes('simple')) return 'La fuente registra esta votación como de quórum simple. El resultado debe leerse junto con las reglas de asistencia y decisión aplicables a la sesión.';
    if (quorum.includes('mayoría absoluta') || quorum.includes('mayoria absoluta')) return 'La fuente registra un quórum calculado sobre la mayoría absoluta de los miembros en ejercicio, no solamente sobre quienes emitieron un voto.';
    if (quorum.includes('tres quintos') || quorum.includes('3/5')) return 'La fuente registra un quórum reforzado de tres quintos; no basta una mayoría simple de quienes votan.';
    if (quorum.includes('dos tercios') || quorum.includes('2/3')) return 'La fuente registra un quórum reforzado de dos tercios; no basta una mayoría simple de quienes votan.';
    return 'El quórum aparece con la etiqueta de la fuente. Para interpretar su umbral jurídico exacto, consulta la lección de mayorías y quórums.';
  };

  const render = (vote, project) => {
    const object = vote.articulo || vote.descripcion || `Boletín ${vote.boletin || 'sin identificar'}`;
    const official = safeUrl(vote.verification_url);
    const projectUrl = vote.boletin ? `proyecto.html?boletin=${encodeURIComponent(vote.boletin)}` : '';
    document.title = `Votación ${vote.vote_id} · ¿Qué se votó realmente?`;
    root.innerHTML = `
      <nav class="edu-breadcrumb" aria-label="Migas de pan"><a href="entender.html">Entiende el Congreso</a><span>›</span><a href="votaciones.html">Explorar votaciones</a><span>›</span><strong>ID ${escapeHtml(vote.vote_id)}</strong></nav>
      <article class="vote-detail">
        <div class="project-kicker"><span class="vote-pill">Votación ${escapeHtml(vote.vote_id)}</span><span class="vote-pill">${escapeHtml(vote.resultado || 'Resultado no informado')}</span></div>
        <h1>${escapeHtml(project?.titulo || `Boletín ${vote.boletin || 'sin identificar'}`)}</h1>
        <p class="vote-project-title">La ficha separa el proyecto general del <strong>objeto exacto sometido a decisión</strong>. Una votación puede referirse a una parte muy específica del texto.</p>
        <div class="vote-facts">
          <div class="vote-fact"><span>Fecha</span><strong>${escapeHtml(formatDate(vote.fecha))}</strong></div>
          <div class="vote-fact"><span>Tipo</span><strong>${escapeHtml(vote.tipo_votacion_proyecto || vote.tipo_votacion || 'No informado')}</strong></div>
          <div class="vote-fact"><span>Trámite</span><strong>${escapeHtml(vote.tramite_constitucional || 'No informado')}</strong></div>
          <div class="vote-fact"><span>Quórum</span><strong>${escapeHtml(vote.quorum || 'No informado')}</strong></div>
        </div>
        <section class="vote-object"><h2>¿Qué se votó?</h2><p>${escapeHtml(object)}</p><div class="vote-explain"><strong>Cómo leer esta decisión:</strong> ${escapeHtml(explainType(vote))}</div>${explainStage(vote) ? `<div class="vote-explain"><strong>Dónde ocurrió en el proceso:</strong> ${escapeHtml(explainStage(vote))}</div>` : ''}<div class="vote-explain"><strong>Sobre el quórum:</strong> ${escapeHtml(explainQuorum(vote))}</div></section>
        <div class="vote-counts">
          <div class="vote-count"><strong>${asNumber(vote.total_si)}</strong><span>A favor</span></div>
          <div class="vote-count"><strong>${asNumber(vote.total_no)}</strong><span>En contra</span></div>
          <div class="vote-count"><strong>${asNumber(vote.total_abstencion)}</strong><span>Abstenciones</span></div>
          <div class="vote-count"><strong>${asNumber(vote.total_dispensado)}</strong><span>Dispensados</span></div>
        </div>
        <div class="vote-actions">
          ${official ? `<a class="vote-primary" href="${escapeHtml(official)}" target="_blank" rel="noopener noreferrer">Ver detalle nominal oficial</a>` : ''}
          ${projectUrl ? `<a class="vote-secondary" href="${escapeHtml(projectUrl)}">Ver historia completa del proyecto</a>` : ''}
          <a class="vote-secondary" href="aprender.html?id=mayorias-y-quorums">Entender mayorías y quórums</a>
          <a class="vote-secondary" href="aprender.html?id=como-se-hace-una-ley">Entender el proceso legislativo</a>
        </div>
      </article>
      <aside class="vote-note"><strong>Qué no concluimos automáticamente:</strong> que votar “A favor” en esta decisión equivalga a apoyar todo el proyecto; que una abstención sea idéntica a ausencia; o que esta votación, por sí sola, describa la posición general del parlamentario sobre la materia. El objeto, la etapa y el tipo de votación importan.</aside>`;
  };

  const init = async () => {
    if (!voteId) {
      root.innerHTML = '<div class="vote-error"><strong>Falta el identificador de votación.</strong><br>Vuelve al explorador y selecciona una votación.</div>';
      return;
    }
    root.innerHTML = '<div class="vote-loading">Reconstruyendo la votación…</div>';
    try {
      const [votes, projects] = await Promise.all([
        fetchCsv('data/legislative/2026/rollcalls.csv'),
        fetchCsv('data/legislative/2026/projects.csv')
      ]);
      const vote = votes.find((item) => item.vote_id === voteId);
      if (!vote) {
        root.innerHTML = `<div class="vote-error"><strong>No encontramos la votación ${escapeHtml(voteId)}.</strong><br>Esta vista utiliza las votaciones nominales incluidas en la base legislativa actual.</div>`;
        return;
      }
      const project = projects.find((item) => item.boletin === vote.boletin);
      render(vote, project);
    } catch (error) {
      root.innerHTML = `<div class="vote-error"><strong>No pudimos reconstruir la votación.</strong><br>${escapeHtml(error.message)}</div>`;
    }
  };

  init();
})();
