(() => {
  const profiles = window.PROFILES || {};
  const payload = window.LEGISLATIVE_COAUTHORSHIP || {};
  const members = payload.members || {};
  const meta = payload.meta || {};
  const container = document.getElementById('coauthorship-module');
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
  const member = members[String(profile.id)];
  if (!member) {
    container.innerHTML = `
      <section class="coauthorship-section">
        <p class="eyebrow">Red de coautoría</p>
        <h2>¿Con quién presenta proyectos?</h2>
        <p>No pudimos construir todavía la red de coautoría para esta ficha.</p>
      </section>
    `;
    return;
  }

  const unique = Number(member.uniqueCoauthors || 0);
  const recurrent = Number(member.recurrentCoauthors || 0);
  const oneOff = Number(member.oneOffCoauthors || 0);
  const strongest = Number(member.strongestTie || 0);
  const topVisible = Array.isArray(member.topVisible) ? member.topVisible : [];
  const termStart = meta.termStart || '2026-03-11';

  const profileLink = (person) => person.profileAvailable
    ? `<a href="ficha.html?id=${encodeURIComponent(String(person.id))}">${escapeHtml(person.name)}</a>`
    : escapeHtml(person.name);

  const topMarkup = topVisible.length ? topVisible.map((person) => {
    const count = Number(person.sharedMotions || 0);
    const width = strongest ? 100 * count / strongest : 0;
    return `
      <div class="coauthorship-tie">
        <div class="coauthorship-tie-name">${profileLink(person)}</div>
        <div class="coauthorship-tie-track" aria-hidden="true"><span class="coauthorship-tie-fill" style="width:${width.toFixed(6)}%"></span></div>
        <div class="coauthorship-tie-count">${numberFormat.format(count)} ${count === 1 ? 'moción compartida' : 'mociones compartidas'}</div>
      </div>
    `;
  }).join('') : '<p class="coauthorship-note">No registra coautorías en el período observado.</p>';

  container.innerHTML = `
    <section class="coauthorship-section" aria-labelledby="coauthorship-title">
      <div class="coauthorship-heading">
        <div>
          <p class="eyebrow">Red de coautoría</p>
          <h2 id="coauthorship-title">¿Con quién presenta proyectos?</h2>
        </div>
        <p class="coauthorship-period">Período observado<br><strong>desde ${escapeHtml(termStart)}</strong></p>
      </div>

      <p class="coauthorship-intro">Conectamos a dos diputadas o diputados cuando ambos figuran formalmente como autores de una misma moción. El vínculo se hace más fuerte cuando esa coincidencia se repite en más de un proyecto.</p>

      <div class="coauthorship-stats">
        <article class="coauthorship-stat">
          <p class="coauthorship-stat-label">Coautores distintos</p>
          <strong class="coauthorship-stat-value">${numberFormat.format(unique)}</strong>
          <p>Personas con las que comparte al menos una moción.</p>
        </article>
        <article class="coauthorship-stat">
          <p class="coauthorship-stat-label">Vínculos recurrentes</p>
          <strong class="coauthorship-stat-value">${numberFormat.format(recurrent)}</strong>
          <p>Coautores con dos o más mociones compartidas.</p>
        </article>
        <article class="coauthorship-stat">
          <p class="coauthorship-stat-label">Vínculos de una moción</p>
          <strong class="coauthorship-stat-value">${numberFormat.format(oneOff)}</strong>
          <p>Coautores que aparecen junto a esta persona una sola vez.</p>
        </article>
      </div>

      <section class="coauthorship-top" aria-labelledby="coauthorship-top-title">
        <div class="coauthorship-top-head">
          <div>
            <h3 id="coauthorship-top-title">Vínculos más repetidos</h3>
            <p>Mostramos hasta ${numberFormat.format(Number(meta.topVisible || 8))} relaciones con mayor número de mociones compartidas. Esta selección <strong>no representa la red completa</strong>.</p>
          </div>
        </div>
        <div class="coauthorship-tie-list">${topMarkup}</div>
        ${unique ? `<div class="coauthorship-actions"><button type="button" data-open-coauthors>Ver los ${numberFormat.format(unique)} coautores y sus proyectos</button></div>` : ''}
      </section>

      <section id="coauthorship-detail" class="coauthorship-detail" aria-live="polite" hidden></section>

      <div class="coauthorship-explainers">
        <details>
          <summary>¿Qué representa un vínculo?</summary>
          <div class="coauthorship-explainer-body">
            <p>Existe un vínculo cuando ambas personas figuran en la lista formal de autores de la misma moción. Su peso es el número de mociones distintas que comparten.</p>
            <p>La unidad es relacional: una moción con varios autores genera varios vínculos. Por eso <strong>no debe sumarse el peso de todas las relaciones para obtener el número de mociones</strong>; ese total se muestra por separado en el módulo de iniciativa legislativa.</p>
          </div>
        </details>
        <details>
          <summary>¿Por qué no mostramos solo una red de 8 o 10 personas?</summary>
          <div class="coauthorship-explainer-body">
            <p>Las redes observadas son amplias. Para muchos perfiles, sus vínculos más repetidos representan solo una parte de toda la actividad relacional. Por eso la síntesis superior está rotulada como una selección de vínculos frecuentes y la lista completa permanece disponible.</p>
          </div>
        </details>
        <details>
          <summary>¿Qué no significa coautoría?</summary>
          <div class="coauthorship-explainer-body">
            <p>Compartir una firma formal no demuestra amistad, afinidad ideológica, cercanía personal, coordinación estable ni acuerdo general entre dos parlamentarios. Tampoco permite repartir cuánto aportó cada autor al texto.</p>
            <p>Los vínculos no se colorean por ideología ni se convierten en un ranking de influencia.</p>
          </div>
        </details>
      </div>

      <p class="coauthorship-source">Fuente: Cámara de Diputadas y Diputados · Peso del vínculo: mociones compartidas como autores formales · Evidencia disponible por boletín.</p>
    </section>
  `;

  if (!unique) return;

  let detailsPromise = null;
  const loadDetails = () => {
    if (!detailsPromise) {
      const template = String(meta.detailPathTemplate || 'assets/data/coauthorship/{id}.json');
      const detailPath = template.replace('{id}', encodeURIComponent(String(profile.id)));
      detailsPromise = fetch(detailPath)
        .then((response) => {
          if (!response.ok) throw new Error('No se pudo cargar la red completa de esta persona.');
          return response.json();
        })
        .then((details) => {
          if (String(details.id || '') !== String(profile.id)) {
            throw new Error('El archivo de coautoría no corresponde a esta ficha.');
          }
          return details;
        });
    }
    return detailsPromise;
  };

  const detailContainer = document.getElementById('coauthorship-detail');

  const billMarkup = (billId, catalog) => {
    const bill = catalog[billId] || {};
    return `
      <article class="coauthor-bill">
        <div class="coauthor-bill-meta">
          <span>${escapeHtml(bill.date || '')}</span>
          <span>Boletín ${escapeHtml(billId)}</span>
          ${bill.formalAuthorCount ? `<span>${numberFormat.format(Number(bill.formalAuthorCount))} autores formales</span>` : ''}
        </div>
        <h4>${escapeHtml(bill.title || `Moción boletín ${billId}`)}</h4>
        <div class="coauthor-bill-footer">
          <span>${bill.state ? `Estado registrado: <strong>${escapeHtml(bill.state)}</strong>` : ''}</span>
          ${bill.url ? `<a href="${escapeHtml(bill.url)}" target="_blank" rel="noopener">Ver tramitación oficial ↗</a>` : ''}
        </div>
      </article>
    `;
  };

  const renderFullList = async () => {
    detailContainer.hidden = false;
    detailContainer.innerHTML = `
      <div class="coauthorship-detail-head">
        <div><p class="eyebrow">Evidencia</p><h3>Red completa de coautoría</h3></div>
        <button type="button" data-close-coauthors>Cerrar</button>
      </div>
      <p>Cargando coautores…</p>
    `;

    try {
      const details = await loadDetails();
      const catalog = details.motions || {};
      const coauthors = Array.isArray(details.coauthors) ? details.coauthors : [];
      const rows = coauthors.map((person, index) => {
        const count = Number(person.sharedMotions || 0);
        const dates = person.firstSharedDate && person.lastSharedDate
          ? (person.firstSharedDate === person.lastSharedDate ? person.firstSharedDate : `${person.firstSharedDate} → ${person.lastSharedDate}`)
          : '';
        const buttonLabel = count === 1 ? 'Ver moción compartida' : `Ver ${numberFormat.format(count)} mociones compartidas`;
        return `
          <article class="coauthor-row" data-coauthor-row="${index}">
            <div class="coauthor-row-main">
              <div class="coauthor-person">
                <strong>${profileLink(person)}</strong>
                ${dates ? `<div class="coauthor-dates">Registro compartido: ${escapeHtml(dates)}</div>` : ''}
              </div>
              <span class="coauthor-count">${numberFormat.format(count)} ${count === 1 ? 'moción' : 'mociones'}</span>
              <button type="button" data-toggle-coauthor-bills="${index}">${escapeHtml(buttonLabel)}</button>
            </div>
            <div class="coauthor-bills" data-coauthor-bills="${index}" hidden></div>
          </article>
        `;
      }).join('');

      detailContainer.innerHTML = `
        <div class="coauthorship-detail-head">
          <div>
            <p class="eyebrow">Evidencia</p>
            <h3>Todos los coautores</h3>
            <p>${numberFormat.format(coauthors.length)} personas, ordenadas por número de mociones compartidas.</p>
          </div>
          <button type="button" data-close-coauthors>Cerrar</button>
        </div>
        <div class="coauthor-full-list">${rows || '<p>No hay vínculos en este conjunto.</p>'}</div>
      `;

      detailContainer.dataset.loaded = '1';
      detailContainer._coauthorshipData = { coauthors, catalog };
      detailContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
      detailContainer.innerHTML = `
        <div class="coauthorship-detail-head">
          <div><p class="eyebrow">Evidencia</p><h3>No pudimos cargar la red completa</h3></div>
          <button type="button" data-close-coauthors>Cerrar</button>
        </div>
        <p>${escapeHtml(error?.message || 'La evidencia no está disponible en este momento.')}</p>
      `;
    }
  };

  container.addEventListener('click', (event) => {
    if (event.target.closest('[data-close-coauthors]')) {
      detailContainer.hidden = true;
      detailContainer.innerHTML = '';
      delete detailContainer.dataset.loaded;
      detailContainer._coauthorshipData = null;
      return;
    }

    if (event.target.closest('[data-open-coauthors]')) {
      renderFullList();
      return;
    }

    const toggle = event.target.closest('[data-toggle-coauthor-bills]');
    if (!toggle || !detailContainer._coauthorshipData) return;
    const index = Number(toggle.dataset.toggleCoauthorBills);
    const person = detailContainer._coauthorshipData.coauthors[index];
    const target = detailContainer.querySelector(`[data-coauthor-bills="${index}"]`);
    if (!person || !target) return;

    if (!target.hidden) {
      target.hidden = true;
      return;
    }

    if (!target.dataset.rendered) {
      const billIds = Array.isArray(person.billIds) ? person.billIds : [];
      target.innerHTML = `<div class="coauthor-bill-list">${billIds.map((billId) => billMarkup(billId, detailContainer._coauthorshipData.catalog)).join('')}</div>`;
      target.dataset.rendered = '1';
    }
    target.hidden = false;
  });
})();
