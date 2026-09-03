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

  const optionLabels = {
    A: 'A favor',
    E: 'En contra',
    B: 'Abstención',
    N: 'No vota',
    D: 'Dispensado',
  };

  const optionClasses = {
    A: 'vote-affirmative',
    E: 'vote-against',
    B: 'vote-abstention',
    N: 'vote-no-vote',
    D: 'vote-excused',
  };

  const filterCodes = {
    affirmative: 'A',
    against: 'E',
    abstention: 'B',
    noVote: 'N',
    excused: 'D',
  };

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

  let voteDetailDataPromise = null;
  const loadVoteDetailData = () => {
    if (!voteDetailDataPromise) {
      voteDetailDataPromise = Promise.all([
        fetch('assets/data/participation_rollcalls.json').then((response) => {
          if (!response.ok) throw new Error('No se pudo cargar el detalle de votaciones.');
          return response.json();
        }),
        fetch('assets/data/participation_member_votes.json').then((response) => {
          if (!response.ok) throw new Error('No se pudo cargar el historial individual de votos.');
          return response.json();
        }),
      ]).then(([rollcalls, memberVotes]) => ({
        rollcalls: rollcalls.rollcalls || {},
        members: memberVotes.members || {},
      }));
    }
    return voteDetailDataPromise;
  };

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
    { key: 'affirmative', code: 'A', label: 'A favor', count: Number(participation.affirmative || 0), className: 'vote-affirmative' },
    { key: 'against', code: 'E', label: 'En contra', count: Number(participation.against || 0), className: 'vote-against' },
    { key: 'abstention', code: 'B', label: 'Abstención', count: Number(participation.abstention || 0), className: 'vote-abstention' },
    { key: 'noVote', code: 'N', label: 'No vota', count: Number(participation.noVote || 0), className: 'vote-no-vote' },
    { key: 'excused', code: 'D', label: 'Dispensado', count: Number(participation.excused || 0), className: 'vote-excused' },
  ].map((state) => ({ ...state, share: pct(state.count, opportunities) }));

  const barLabel = states
    .map((state) => `${state.label}: ${numberFormat.format(state.count)} (${percentFormat.format(state.share)}%)`)
    .join('; ');

  const barSegments = states
    .filter((state) => state.count > 0)
    .map((state) => `
      <button
        type="button"
        class="vote-segment ${state.className}"
        style="width:${state.share.toFixed(6)}%"
        title="${escapeHtml(state.label)}: ${numberFormat.format(state.count)} (${percentFormat.format(state.share)}%)"
        aria-label="Ver ${numberFormat.format(state.count)} votaciones registradas como ${escapeHtml(state.label)}"
        data-vote-filter="${state.key}"
      ></button>
    `)
    .join('');

  const legend = states
    .map((state) => `
      <li>
        <button
          type="button"
          class="vote-legend-item"
          data-vote-filter="${state.key}"
          ${state.count === 0 ? 'disabled' : ''}
          aria-label="${state.count === 0 ? 'Sin registros' : 'Ver votaciones'}: ${escapeHtml(state.label)}, ${numberFormat.format(state.count)}, ${percentFormat.format(state.share)} por ciento"
        >
          <span class="vote-legend-label">
            <span class="vote-legend-dot ${state.className}" aria-hidden="true"></span>
            ${escapeHtml(state.label)}
          </span>
          <span class="vote-legend-value">
            <strong>${numberFormat.format(state.count)}</strong>
            <span>${percentFormat.format(state.share)}%</span>
          </span>
        </button>
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
          <div>
            <h3>Cómo se distribuyen sus registros de voto</h3>
            <p>Selecciona un segmento o una categoría para revisar las votaciones que contiene.</p>
          </div>
          <button type="button" class="view-all-votes" data-vote-filter="all">Ver las ${numberFormat.format(opportunities)} votaciones</button>
        </div>
        <div class="vote-bar" role="group" aria-label="Distribución de registros de voto. ${escapeHtml(barLabel)}">${barSegments}</div>
        <ul class="vote-legend" aria-label="Detalle de registros de voto">${legend}</ul>
      </div>

      <section id="vote-detail" class="vote-detail" aria-live="polite" hidden></section>

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

  const voteDetail = document.getElementById('vote-detail');

  const renderVoteDetailError = (message) => {
    voteDetail.hidden = false;
    voteDetail.innerHTML = `
      <div class="vote-detail-heading">
        <div><p class="eyebrow">Evidencia</p><h3>No pudimos cargar el detalle</h3></div>
        <button type="button" class="vote-detail-close" data-close-votes aria-label="Cerrar detalle de votaciones">Cerrar</button>
      </div>
      <p class="vote-detail-status">${escapeHtml(message)}</p>
    `;
  };

  const renderVoteDetails = async (filterKey) => {
    const code = filterKey === 'all' ? null : filterCodes[filterKey];
    const state = states.find((item) => item.key === filterKey);
    const label = filterKey === 'all' ? 'Todas las oportunidades de votación' : state?.label || 'Votaciones';

    voteDetail.hidden = false;
    voteDetail.innerHTML = `
      <div class="vote-detail-heading">
        <div><p class="eyebrow">Evidencia</p><h3>${escapeHtml(label)}</h3></div>
        <button type="button" class="vote-detail-close" data-close-votes aria-label="Cerrar detalle de votaciones">Cerrar</button>
      </div>
      <p class="vote-detail-status">Cargando votaciones…</p>
    `;

    try {
      const data = await loadVoteDetailData();
      const memberRows = data.members[String(profile.id)] || [];
      const selected = memberRows
        .filter(([, optionCode]) => !code || optionCode === code)
        .map(([voteId, optionCode]) => ({
          voteId: String(voteId),
          optionCode,
          rollcall: data.rollcalls[String(voteId)] || {},
        }))
        .sort((a, b) => String(b.rollcall.date || '').localeCompare(String(a.rollcall.date || '')) || Number(b.voteId) - Number(a.voteId));

      const items = selected.map(({ voteId, optionCode, rollcall }) => {
        const date = formatDate(rollcall.date);
        const optionLabel = optionLabels[optionCode] || optionCode;
        const optionClass = optionClasses[optionCode] || '';
        const object = rollcall.object && rollcall.object !== 'Votación del proyecto' ? rollcall.object : '';
        return `
          <article class="vote-detail-item">
            <div class="vote-detail-meta">
              <span>${escapeHtml(date || rollcall.date || '')}</span>
              ${rollcall.bulletin ? `<span>Boletín ${escapeHtml(rollcall.bulletin)}</span>` : ''}
              <span class="vote-option-badge ${optionClass}">${escapeHtml(optionLabel)}</span>
            </div>
            <h4>${escapeHtml(rollcall.title || `Votación ${voteId}`)}</h4>
            ${object ? `<p>${escapeHtml(object)}</p>` : ''}
            <div class="vote-detail-footer">
              ${rollcall.result ? `<span>Resultado general: <strong>${escapeHtml(rollcall.result)}</strong></span>` : '<span></span>'}
              ${rollcall.url ? `<a href="${escapeHtml(rollcall.url)}" target="_blank" rel="noopener">Ver votación oficial ↗</a>` : ''}
            </div>
          </article>
        `;
      }).join('');

      voteDetail.innerHTML = `
        <div class="vote-detail-heading">
          <div>
            <p class="eyebrow">Evidencia</p>
            <h3>${escapeHtml(label)}</h3>
            <p>${numberFormat.format(selected.length)} ${selected.length === 1 ? 'votación' : 'votaciones'}, de la más reciente a la más antigua.</p>
          </div>
          <button type="button" class="vote-detail-close" data-close-votes aria-label="Cerrar detalle de votaciones">Cerrar</button>
        </div>
        <div class="vote-detail-list">${items || '<p class="vote-detail-status">No hay registros en esta categoría.</p>'}</div>
      `;
      voteDetail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (detailError) {
      renderVoteDetailError(detailError?.message || 'El detalle no está disponible en este momento.');
    }
  };

  participationModule.addEventListener('click', (event) => {
    const close = event.target.closest('[data-close-votes]');
    if (close) {
      voteDetail.hidden = true;
      voteDetail.innerHTML = '';
      return;
    }

    const trigger = event.target.closest('[data-vote-filter]');
    if (!trigger || trigger.disabled) return;
    renderVoteDetails(trigger.dataset.voteFilter);
  });

  shell.hidden = false;
})();
