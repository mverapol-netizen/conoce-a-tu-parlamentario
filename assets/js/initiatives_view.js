(() => {
  const profiles = window.PROFILES || {};
  const payload = window.LEGISLATIVE_INITIATIVES || {};
  const members = payload.members || {};
  const meta = payload.meta || {};
  const container = document.getElementById('initiatives-module');
  if (!container) return;

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
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  const requestedName = params.get('nombre');
  const entry = Object.entries(profiles).find(([name, profile]) => {
    if (id && String(profile.id) === String(id)) return true;
    if (requestedName && normalize(name) === normalize(requestedName)) return true;
    return false;
  });
  if (!entry) return;

  const [, profile] = entry;
  const member = members[String(profile.id)] || {
    name: profile.officialName || '', motions: 0, shared: 0, individual: 0,
  };

  const total = Number(member.motions || 0);
  const shared = Number(member.shared || 0);
  const individual = Number(member.individual || 0);
  const sharedPct = total ? 100 * shared / total : 0;
  const individualPct = total ? 100 * individual / total : 0;
  const termStart = meta.termStart || '2026-03-11';

  const summaryMarkup = total ? `
    <div class="initiatives-summary">
      <article class="initiative-stat initiative-stat-main">
        <p class="initiative-stat-label">Mociones con autoría registrada</p>
        <strong class="initiative-stat-value">${numberFormat.format(total)}</strong>
        <p class="initiative-stat-copy">Proyectos en los que figura como autor/a formal desde el inicio del período observado.</p>
      </article>
      <article class="initiative-stat">
        <p class="initiative-stat-label">Autoría compartida</p>
        <strong class="initiative-stat-value">${numberFormat.format(shared)}</strong>
        <p class="initiative-stat-copy">Mociones cuya lista formal contiene dos o más autores.</p>
      </article>
      <article class="initiative-stat">
        <p class="initiative-stat-label">Autoría individual</p>
        <strong class="initiative-stat-value">${numberFormat.format(individual)}</strong>
        <p class="initiative-stat-copy">Mociones con una sola persona en la lista formal de autores.</p>
      </article>
    </div>
    <div class="initiatives-composition" role="img" aria-label="${numberFormat.format(shared)} mociones con autoría compartida y ${numberFormat.format(individual)} con autoría individual">
      <span class="initiatives-shared" style="width:${sharedPct.toFixed(6)}%"></span>
      <span class="initiatives-individual" style="width:${individualPct.toFixed(6)}%"></span>
    </div>
    <div class="initiatives-legend">
      <span><i class="initiatives-dot initiatives-dot-shared" aria-hidden="true"></i>${numberFormat.format(shared)} compartidas</span>
      <span><i class="initiatives-dot initiatives-dot-individual" aria-hidden="true"></i>${numberFormat.format(individual)} individuales</span>
    </div>
    <div class="initiatives-actions">
      <button type="button" data-open-initiatives>Ver ${numberFormat.format(total)} ${total === 1 ? 'moción' : 'mociones'}</button>
    </div>
  ` : `
    <div class="initiatives-empty">
      <strong>No registra mociones en el período observado.</strong>
      <p>Esto significa que no encontramos proyectos de origen parlamentario en los que figure como autor/a formal desde ${escapeHtml(termStart)}. No equivale a ausencia de trabajo legislativo.</p>
    </div>
  `;

  container.innerHTML = `
    <section class="initiatives-section" aria-labelledby="initiatives-title">
      <div class="initiatives-heading">
        <div>
          <p class="eyebrow">Iniciativa legislativa</p>
          <h2 id="initiatives-title">¿Qué proyectos ha presentado?</h2>
        </div>
        <p class="initiatives-period">Período observado<br><strong>desde ${escapeHtml(termStart)}</strong></p>
      </div>
      <p class="initiatives-intro">Contamos las <strong>mociones</strong> en las que esta persona figura en la lista formal de autores de la Cámara. Separamos las que tienen autoría compartida de aquellas con una sola persona registrada como autora.</p>

      ${summaryMarkup}

      <section id="initiatives-detail" class="initiatives-detail" aria-live="polite" hidden></section>

      <div class="initiatives-explainers">
        <details>
          <summary>¿Qué significa este indicador?</summary>
          <div class="initiatives-explainer-body">
            <p>Describe actividad de iniciativa parlamentaria formal: proyectos ingresados como mociones en los que la Cámara registra a esta persona entre sus autores.</p>
            <p>Una moción se cuenta una sola vez por boletín, aunque el proyecto tenga varios autores.</p>
          </div>
        </details>
        <details>
          <summary>¿Qué no significa?</summary>
          <div class="initiatives-explainer-body">
            <p>La cantidad de mociones no mide por sí sola calidad, impacto, esfuerzo, productividad ni éxito legislativo. Ser coautor tampoco permite saber cuánto redactó, negoció o impulsó cada firmante.</p>
            <p>No incluimos mensajes del Ejecutivo como si fueran iniciativas de diputados, ni usamos esta cifra para construir un ranking.</p>
          </div>
        </details>
        <details>
          <summary>¿Cómo distinguimos autoría compartida e individual?</summary>
          <div class="initiatives-explainer-body">
            <p>Miramos la lista formal de autores del boletín. Si contiene una sola persona, clasificamos la moción como autoría individual registrada. Si contiene dos o más, la clasificamos como autoría compartida.</p>
            <p>Esta distinción describe la firma formal del proyecto; no atribuye la redacción material del texto.</p>
          </div>
        </details>
      </div>

      <p class="initiatives-source">Fuente: Cámara de Diputadas y Diputados · Unidad de conteo: moción × autor/a formal · Datos actualizados automáticamente.</p>
    </section>
  `;

  if (!total) return;

  let detailsPromise = null;
  const loadDetails = () => {
    if (!detailsPromise) {
      const template = String(meta.detailPathTemplate || 'assets/data/initiatives/{id}.json');
      const detailPath = template.replace('{id}', encodeURIComponent(String(profile.id)));
      detailsPromise = fetch(detailPath)
        .then((response) => {
          if (!response.ok) throw new Error('No se pudo cargar el listado de mociones de esta persona.');
          return response.json();
        })
        .then((details) => {
          if (String(details.id || '') !== String(profile.id)) {
            throw new Error('El archivo de iniciativas no corresponde a esta ficha.');
          }
          return details;
        });
    }
    return detailsPromise;
  };

  const detailContainer = document.getElementById('initiatives-detail');

  const renderDetails = async () => {
    detailContainer.hidden = false;
    detailContainer.innerHTML = `
      <div class="initiatives-detail-heading">
        <div><p class="eyebrow">Evidencia</p><h3>Mociones registradas</h3></div>
        <button type="button" data-close-initiatives>Cerrar</button>
      </div>
      <p>Cargando proyectos…</p>
    `;

    try {
      const details = await loadDetails();
      const rows = Array.isArray(details.motions) ? details.motions : [];
      const items = rows.map((row) => {
        const individualAuthorship = row.authorship === 'individual';
        const authorshipLabel = individualAuthorship
          ? 'Autoría individual registrada'
          : `${numberFormat.format(Number(row.formalAuthorCount || 0))} autores registrados`;
        return `
          <article class="initiative-item">
            <div class="initiative-item-meta">
              <span>${escapeHtml(row.date || '')}</span>
              <span>Boletín ${escapeHtml(row.boletin || '')}</span>
              <span class="initiative-authorship-badge ${individualAuthorship ? 'is-individual' : ''}">${escapeHtml(authorshipLabel)}</span>
            </div>
            <h4>${escapeHtml(row.title || `Moción boletín ${row.boletin || ''}`)}</h4>
            <div class="initiative-item-footer">
              <span>${row.state ? `Estado registrado: <strong>${escapeHtml(row.state)}</strong>` : ''}</span>
              ${row.url ? `<a href="${escapeHtml(row.url)}" target="_blank" rel="noopener">Ver tramitación oficial ↗</a>` : ''}
            </div>
          </article>
        `;
      }).join('');

      detailContainer.innerHTML = `
        <div class="initiatives-detail-heading">
          <div>
            <p class="eyebrow">Evidencia</p>
            <h3>Mociones registradas</h3>
            <p>${numberFormat.format(rows.length)} ${rows.length === 1 ? 'moción' : 'mociones'}, de la más reciente a la más antigua.</p>
          </div>
          <button type="button" data-close-initiatives>Cerrar</button>
        </div>
        <div class="initiatives-list">${items || '<p>No hay mociones en este conjunto.</p>'}</div>
      `;
      detailContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
      detailContainer.innerHTML = `
        <div class="initiatives-detail-heading">
          <div><p class="eyebrow">Evidencia</p><h3>No pudimos cargar el listado</h3></div>
          <button type="button" data-close-initiatives>Cerrar</button>
        </div>
        <p>${escapeHtml(error?.message || 'El detalle no está disponible en este momento.')}</p>
      `;
    }
  };

  container.addEventListener('click', (event) => {
    if (event.target.closest('[data-close-initiatives]')) {
      detailContainer.hidden = true;
      detailContainer.innerHTML = '';
      return;
    }
    if (event.target.closest('[data-open-initiatives]')) renderDetails();
  });
})();
