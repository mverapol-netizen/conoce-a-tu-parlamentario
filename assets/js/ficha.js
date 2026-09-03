(() => {
  const profiles = window.PROFILES || {};
  const participationPayload = window.LEGISLATIVE_PARTICIPATION || {};
  const participationMembers = participationPayload.members || {};
  const participationMeta = participationPayload.meta || {};
  const container = document.getElementById('legislative-profile');
  const shell = document.getElementById('legislative-shell');
  const participationModule = document.getElementById('participation-module');
  const error = document.getElementById('profile-error');

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

  const normalize = (value) => String(value || '')
    .toLocaleLowerCase('es-CL')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const numberFormat = new Intl.NumberFormat('es-CL');
  const percentFormat = new Intl.NumberFormat('es-CL', {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  });

  const formatDate = (value) => {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(String(value || ''))) return '';
    const [year, month, day] = value.split('-').map(Number);
    const date = new Date(Date.UTC(year, month - 1, day));
    return new Intl.DateTimeFormat('es-CL', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      timeZone: 'UTC',
    }).format(date);
  };

  const pct = (count, total) => total ? (100 * count / total) : 0;

  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  const requestedName = params.get('nombre');

  const entry = Object.entries(profiles).find(([name, profile]) => {
    if (id && String(profile.id) === String(id)) return true;
    if (requestedName && normalize(name) === normalize(requestedName)) return true;
    return false;
  });

  if (!entry) {
    container.hidden = true;
    shell.hidden = true;
    error.hidden = false;
    return;
  }

  const [name, profile] = entry;
  document.title = `${name} · Ficha legislativa`;

  const affiliation = profile.affiliationLabel || profile.party || 'Afiliación en actualización';
  const caucus = profile.caucus || 'Bancada por confirmar';
  const portrait = profile.photo
    ? `<img class="legislative-photo" src="${escapeHtml(profile.photo)}" alt="Fotografía de ${escapeHtml(name)}">`
    : `<div class="legislative-photo-fallback" aria-hidden="true"></div>`;

  container.innerHTML = `
    <div class="legislative-profile-grid">
      <div class="legislative-photo-frame">${portrait}</div>
      <div class="legislative-identity">
        <p class="eyebrow">Ficha legislativa</p>
        <h1>${escapeHtml(name)}</h1>
        <div class="legislative-tags">
          <span>Distrito ${escapeHtml(profile.district)}</span>
          <span>${escapeHtml(profile.region || '')}</span>
          <span>${escapeHtml(affiliation)}</span>
        </div>
        <p class="legislative-caucus">${escapeHtml(caucus)}</p>
        <div class="legislative-actions">
          ${profile.email ? `<a href="mailto:${escapeHtml(profile.email)}">Correo oficial</a>` : ''}
          ${profile.profileUrl ? `<a href="${escapeHtml(profile.profileUrl)}" target="_blank" rel="noopener">Ficha oficial de la Cámara</a>` : ''}
        </div>
      </div>
    </div>
  `;

  const image = container.querySelector('.legislative-photo');
  if (image) {
    image.addEventListener('error', () => {
      image.parentElement.innerHTML = '<div class="legislative-photo-fallback" aria-hidden="true"></div>';
    });
  }

  const participation = participationMembers[String(profile.id)];
  if (!participation) {
    participationModule.innerHTML = `
      <section class="participation-card participation-card-unavailable">
        <p class="eyebrow">Comportamiento legislativo</p>
        <h2>Participación en votaciones de Sala</h2>
        <p>Este indicador todavía no está disponible para esta ficha. No imputamos una cifra cuando la fuente nominal no permite construirla.</p>
      </section>
    `;
    shell.hidden = false;
    return;
  }

  const opportunities = Number(participation.opportunities || 0);
  const substantive = Number(participation.substantive || 0);
  const states = [
    { key: 'affirmative', label: 'A favor', count: Number(participation.affirmative || 0), className: 'vote-affirmative' },
    { key: 'against', label: 'En contra', count: Number(participation.against || 0), className: 'vote-against' },
    { key: 'abstention', label: 'Abstención', count: Number(participation.abstention || 0), className: 'vote-abstention' },
    { key: 'noVote', label: 'No vota', count: Number(participation.noVote || 0), className: 'vote-no-vote' },
    { key: 'excused', label: 'Dispensado', count: Number(participation.excused || 0), className: 'vote-excused' },
  ].map((state) => ({ ...state, share: pct(state.count, opportunities) }));

  const barLabel = states
    .map((state) => `${state.label}: ${numberFormat.format(state.count)} (${percentFormat.format(state.share)}%)`)
    .join('; ');

  const barSegments = states
    .filter((state) => state.count > 0)
    .map((state) => `
      <span
        class="vote-segment ${state.className}"
        style="width:${state.share.toFixed(6)}%"
        title="${escapeHtml(state.label)}: ${numberFormat.format(state.count)} (${percentFormat.format(state.share)}%)"
        aria-hidden="true"
      ></span>
    `)
    .join('');

  const legend = states
    .map((state) => `
      <li class="vote-legend-item">
        <span class="vote-legend-label">
          <span class="vote-legend-dot ${state.className}" aria-hidden="true"></span>
          ${escapeHtml(state.label)}
        </span>
        <span class="vote-legend-value">
          <strong>${numberFormat.format(state.count)}</strong>
          <span>${percentFormat.format(state.share)}%</span>
        </span>
      </li>
    `)
    .join('');

  const firstDate = formatDate(participation.firstOpportunityDate);
  const lastDate = formatDate(participation.lastOpportunityDate || participationMeta.dataCut);
  const dataCut = formatDate(participationMeta.dataCut);
  const dateRange = firstDate && lastDate ? `${firstDate}–${lastDate}` : '';
  const substantivePct = Number(participation.substantiveParticipationPct || 0);

  participationModule.innerHTML = `
    <section class="participation-card" aria-labelledby="participation-title">
      <div class="participation-heading">
        <div>
          <p class="eyebrow">Comportamiento legislativo</p>
          <h2 id="participation-title">Participación en votaciones de Sala</h2>
        </div>
        ${dateRange ? `<p class="participation-period">Período observado<br><strong>${escapeHtml(dateRange)}</strong></p>` : ''}
      </div>

      <div class="participation-summary">
        <div class="participation-kpi" aria-label="Participación sustantiva ${percentFormat.format(substantivePct)} por ciento">
          <strong>${percentFormat.format(substantivePct)}%</strong>
          <span>participación en votaciones</span>
        </div>
        <p class="participation-lead">
          <strong>${escapeHtml(name)}</strong> registró una decisión —a favor, en contra o abstención— en
          <strong>${numberFormat.format(substantive)} de ${numberFormat.format(opportunities)}</strong>
          votaciones nominales de Sala en las que tuvo una oportunidad registrada de votar.
        </p>
      </div>

      <div class="vote-distribution">
        <div class="vote-distribution-header">
          <h3>Cómo se distribuyen sus registros de voto</h3>
          <span>${numberFormat.format(opportunities)} oportunidades</span>
        </div>
        <div class="vote-bar" role="img" aria-label="${escapeHtml(barLabel)}">${barSegments}</div>
        <ul class="vote-legend" aria-label="Detalle de registros de voto">${legend}</ul>
      </div>

      <div class="participation-explainers">
        <details>
          <summary>¿Cómo leer este gráfico?</summary>
          <div class="explainer-body">
            <p>La cifra principal cuenta como participación una decisión registrada <strong>a favor, en contra o como abstención</strong>. La barra conserva además por separado los estados oficiales <strong>No vota</strong> y <strong>Dispensado</strong>.</p>
            <p>El largo de cada segmento representa su proporción real dentro de las oportunidades de votación de esta persona; la leyenda muestra los números absolutos y porcentajes exactos.</p>
          </div>
        </details>

        <details>
          <summary>¿Qué significa y qué no significa?</summary>
          <div class="explainer-body">
            <p>Describe participación observada exclusivamente en <strong>votaciones nominales de Sala</strong>. Permite distinguir si una persona emitió una decisión y qué tipo de registro dejó la fuente oficial.</p>
            <p>No mide asistencia general al Congreso, trabajo en comisiones, calidad del desempeño ni productividad legislativa. “No vota” tampoco se interpreta automáticamente como ausencia física, y una abstención no se trata como falta de participación.</p>
          </div>
        </details>

        <details>
          <summary>¿Cómo lo calculamos?</summary>
          <div class="explainer-body">
            <p><strong>Participación = (A favor + En contra + Abstención) / oportunidades efectivas de votación.</strong></p>
            <p>Cada registro nominal oficial que vincula una votación con esta diputada o diputado cuenta como una oportunidad. Si una persona todavía no integraba la Cámara o ya había dejado el cargo y su ID no aparece en el detalle nominal oficial, esa votación no entra en su denominador.</p>
            <p>Las categorías “No vota” y “Dispensado” se conservan sin recodificarlas. Los datos primarios provienen de los detalles nominales de votación publicados por la Cámara de Diputadas y Diputados.</p>
          </div>
        </details>
      </div>

      <p class="participation-source">
        Fuente: Cámara de Diputadas y Diputados de Chile · ${dataCut ? `Datos hasta el ${escapeHtml(dataCut)}` : 'corte de datos vigente'} · Indicador descriptivo, no evaluación de desempeño.
      </p>
    </section>
  `;

  shell.hidden = false;
})();
