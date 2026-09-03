(() => {
  const profiles = window.PROFILES || {};
  const payload = window.LEGISLATIVE_MODAL_AGREEMENT || {};
  const members = payload.members || {};
  const meta = payload.meta || {};
  const container = document.getElementById('modal-agreement-module');
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
  const percentFormat = new Intl.NumberFormat('es-CL', {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  });

  const optionLabels = { A: 'A favor', E: 'En contra', B: 'Abstención' };
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  const requestedName = params.get('nombre');
  const entry = Object.entries(profiles).find(([name, profile]) => {
    if (id && String(profile.id) === String(id)) return true;
    if (requestedName && normalize(name) === normalize(requestedName)) return true;
    return false;
  });
  if (!entry) return;

  const [name, profile] = entry;
  const member = members[String(profile.id)];
  if (!member) {
    container.innerHTML = `
      <section class="agreement-section agreement-unavailable">
        <p class="eyebrow">Relación con sus grupos</p>
        <h2>Coincidencia con sus grupos parlamentarios</h2>
        <p>Este indicador todavía no está disponible para esta ficha. No imputamos una comparación cuando la información temporal de partido o bancada no permite construirla.</p>
      </section>
    `;
    return;
  }

  const groupLabel = (type) => type === 'party' ? 'Con su partido' : 'Con su bancada o comité';
  const groupNoun = (type) => type === 'party' ? 'partido' : 'bancada o comité';

  const groupNamesMarkup = (group) => {
    const groups = group.groups || [];
    if (!groups.length) return '<p class="agreement-group-name">Sin grupo registrado</p>';
    if (groups.length === 1) return `<p class="agreement-group-name">${escapeHtml(groups[0])}</p>`;
    return `
      <p class="agreement-group-name">Más de un grupo durante el período</p>
      <p class="agreement-group-history">${groups.map(escapeHtml).join(' · ')}</p>
    `;
  };

  const unavailableText = (type, group) => {
    const groups = group.groups || [];
    if (type === 'party') {
      if (groups.some((value) => normalize(value) === 'independientes')) {
        return 'Sin comparación partidaria disponible: figura como independiente en las votaciones observadas.';
      }
      if (groups.length) {
        return 'No hay suficientes pares partidarios para identificar una posición predominante sin usar el propio voto de esta persona.';
      }
      return 'No existe un partido formal comparable en las votaciones observadas.';
    }
    if (groups.some((value) => ['por definir', 'fuera del comite partido de la gente'].includes(normalize(value)))) {
      return 'No existe una bancada o comité formal comparable en suficientes votaciones del período observado.';
    }
    return 'No hay decisiones comparables suficientes para construir esta relación con bancada o comité.';
  };

  const renderCard = (type, group) => {
    const label = groupLabel(type);
    const noun = groupNoun(type);
    const comparisons = Number(group.comparisons || 0);
    const matches = Number(group.matches || 0);
    const divergences = Number(group.divergences || 0);
    const agreement = Number(group.agreementPct || 0);

    if (group.status === 'available') {
      const divergencePct = comparisons ? 100 * divergences / comparisons : 0;
      return `
        <article class="agreement-card" data-group-card="${type}">
          <div class="agreement-card-head">
            <div>
              <p class="agreement-card-label">${escapeHtml(label)}</p>
              ${groupNamesMarkup(group)}
            </div>
            <span class="agreement-sample">${numberFormat.format(comparisons)} comparables</span>
          </div>
          <div class="agreement-kpi-row">
            <strong class="agreement-kpi">${percentFormat.format(agreement)}%</strong>
            <p>Coincidió con la posición más frecuente de los <strong>demás integrantes</strong> de su ${escapeHtml(noun)} en <strong>${numberFormat.format(matches)} de ${numberFormat.format(comparisons)}</strong> votaciones comparables.</p>
          </div>
          <div class="agreement-bar" role="img" aria-label="Coincidencias ${numberFormat.format(matches)}, divergencias ${numberFormat.format(divergences)}">
            <span class="agreement-bar-match" style="width:${agreement.toFixed(6)}%"></span>
            <span class="agreement-bar-diverge" style="width:${divergencePct.toFixed(6)}%"></span>
          </div>
          <div class="agreement-legend">
            <span><i class="agreement-dot agreement-dot-match" aria-hidden="true"></i>${numberFormat.format(matches)} coincidencias</span>
            <span><i class="agreement-dot agreement-dot-diverge" aria-hidden="true"></i>${numberFormat.format(divergences)} divergencias</span>
          </div>
          <div class="agreement-actions">
            <button type="button" data-agreement-detail="${type}:match">Ver coincidencias</button>
            <button type="button" data-agreement-detail="${type}:diverge">Ver divergencias</button>
          </div>
        </article>
      `;
    }

    if (group.status === 'insufficient') {
      return `
        <article class="agreement-card agreement-card-warning" data-group-card="${type}">
          <div class="agreement-card-head">
            <div>
              <p class="agreement-card-label">${escapeHtml(label)}</p>
              ${groupNamesMarkup(group)}
            </div>
            <span class="agreement-sample">${numberFormat.format(comparisons)} comparables</span>
          </div>
          <div class="agreement-state-copy">
            <strong>Evidencia todavía insuficiente</strong>
            <p>Solo encontramos ${numberFormat.format(comparisons)} votaciones comparables. Para mostrar un porcentaje público exigimos al menos ${numberFormat.format(meta.minPublicComparisons || 20)}.</p>
          </div>
          <div class="agreement-actions">
            <button type="button" data-agreement-detail="${type}:all">Revisar las ${numberFormat.format(comparisons)} comparaciones</button>
          </div>
        </article>
      `;
    }

    return `
      <article class="agreement-card agreement-card-empty" data-group-card="${type}">
        <div class="agreement-card-head">
          <div>
            <p class="agreement-card-label">${escapeHtml(label)}</p>
            ${groupNamesMarkup(group)}
          </div>
        </div>
        <div class="agreement-state-copy">
          <strong>Sin comparación disponible</strong>
          <p>${escapeHtml(unavailableText(type, group))}</p>
        </div>
      </article>
    `;
  };

  container.innerHTML = `
    <section class="agreement-section" aria-labelledby="agreement-title">
      <div class="agreement-heading">
        <div>
          <p class="eyebrow">Relación con sus grupos</p>
          <h2 id="agreement-title">Coincidencia con sus grupos parlamentarios</h2>
        </div>
        <p class="agreement-threshold">Vista principal<br><strong>votaciones con minoría ≥ 10%</strong></p>
      </div>

      <p class="agreement-intro">Comparamos cada decisión con la opción más frecuente entre los <strong>demás integrantes</strong> del partido o bancada que la persona tenía en esa fecha. Su propio voto se retira antes de definir la posición predominante.</p>

      <div class="agreement-grid">
        ${renderCard('party', member.party || {})}
        ${renderCard('caucus', member.caucus || {})}
      </div>

      <section id="agreement-detail" class="agreement-detail" aria-live="polite" hidden></section>

      <div class="agreement-explainers">
        <details>
          <summary>¿Cómo leer estas cifras?</summary>
          <div class="agreement-explainer-body">
            <p>Una coincidencia significa que la persona eligió la misma opción —A favor, En contra o Abstención— que la posición más frecuente entre los demás integrantes de su grupo en esa votación.</p>
            <p>Partido y bancada/comité se muestran por separado porque son instituciones distintas. La comparación sigue el grupo que la persona tenía en la fecha de cada voto, no su afiliación actual aplicada retrospectivamente.</p>
          </div>
        </details>
        <details>
          <summary>¿Por qué usamos votaciones con minoría de al menos 10%?</summary>
          <div class="agreement-explainer-body">
            <p>Las votaciones casi unánimes hacen muy fácil coincidir con cualquier grupo y pueden inflar el porcentaje sin aportar mucha información. Por eso la vista principal exige que el lado minoritario entre A favor y En contra reúna al menos 10% de los votos binarios de la Cámara.</p>
            <p>La auditoría también probó cortes de 5% y 20%. El 10% conserva cientos de comparaciones para la gran mayoría de los casos comparables y produce resultados muy similares al 5%, pero excluye más consensos triviales.</p>
          </div>
        </details>
        <details>
          <summary>¿Qué significa y qué no significa?</summary>
          <div class="agreement-explainer-body">
            <p>El indicador describe <strong>similitud observada de voto</strong> con un grupo institucional. No identifica por qué existe esa similitud.</p>
            <p>Una coincidencia alta puede ser compatible con preferencias compartidas, coordinación, selección partidaria, deliberación o disciplina, entre otros mecanismos. Una divergencia tampoco equivale automáticamente a rebelión, indisciplina o voto de conciencia.</p>
          </div>
        </details>
        <details>
          <summary>¿Cómo lo calculamos?</summary>
          <div class="agreement-explainer-body">
            <p>Para cada votación retiramos primero el voto de la persona. Luego exigimos al menos dos decisiones sustantivas de sus pares y una única opción predominante. Solo entonces comparamos su voto con esa moda.</p>
            <p>“No vota” y “Dispensado” no cuentan como coincidencias ni divergencias. Además, para mostrar un porcentaje público exigimos al menos ${numberFormat.format(meta.minPublicComparisons || 20)} comparaciones acumuladas.</p>
          </div>
        </details>
      </div>

      <p class="agreement-source">Indicador descriptivo · Método leave-one-out · Umbral público de minoría de Cámara: ${percentFormat.format(100 * Number(meta.chamberMinorityThreshold || 0.10))}%.</p>
    </section>
  `;

  let detailsPromise = null;
  const loadDetails = () => {
    if (!detailsPromise) {
      const template = String(meta.detailPathTemplate || 'assets/data/modal_agreement/{id}.json');
      const detailPath = template.replace('{id}', encodeURIComponent(String(profile.id)));
      detailsPromise = Promise.all([
        fetch(detailPath).then((response) => {
          if (!response.ok) throw new Error('No se pudo cargar el detalle de coincidencias de esta persona.');
          return response.json();
        }),
        fetch('assets/data/participation_rollcalls.json').then((response) => {
          if (!response.ok) throw new Error('No se pudo cargar el catálogo de votaciones.');
          return response.json();
        }),
      ]).then(([details, rollcalls]) => {
        if (String(details.id || '') !== String(profile.id)) {
          throw new Error('El archivo de evidencia no corresponde a esta ficha.');
        }
        return {
          member: details,
          rollcalls: rollcalls.rollcalls || {},
        };
      });
    }
    return detailsPromise;
  };

  const detailContainer = document.getElementById('agreement-detail');

  const renderDetail = async (type, mode) => {
    const label = groupLabel(type);
    const modeLabel = mode === 'match' ? 'Coincidencias' : mode === 'diverge' ? 'Divergencias' : 'Comparaciones disponibles';
    detailContainer.hidden = false;
    detailContainer.innerHTML = `
      <div class="agreement-detail-heading">
        <div><p class="eyebrow">Evidencia</p><h3>${escapeHtml(modeLabel)} · ${escapeHtml(label)}</h3></div>
        <button type="button" data-close-agreement-detail>Cerrar</button>
      </div>
      <p class="agreement-detail-status">Cargando votaciones…</p>
    `;

    try {
      const data = await loadDetails();
      const rows = (data.member?.[type] || [])
        .filter((row) => mode === 'all' || (mode === 'match' ? Number(row[4]) === 1 : Number(row[4]) === 0))
        .map((row) => ({
          voteId: String(row[0]),
          groupName: row[1],
          memberOption: row[2],
          peerOption: row[3],
          match: Number(row[4]) === 1,
          rollcall: data.rollcalls[String(row[0])] || {},
        }))
        .sort((a, b) => String(b.rollcall.date || '').localeCompare(String(a.rollcall.date || '')) || Number(b.voteId) - Number(a.voteId));

      const items = rows.map((row) => {
        const date = row.rollcall.date || '';
        const object = row.rollcall.object && row.rollcall.object !== 'Votación del proyecto' ? row.rollcall.object : '';
        return `
          <article class="agreement-detail-item">
            <div class="agreement-detail-meta">
              <span>${escapeHtml(date)}</span>
              ${row.rollcall.bulletin ? `<span>Boletín ${escapeHtml(row.rollcall.bulletin)}</span>` : ''}
              <span class="agreement-result-badge ${row.match ? 'is-match' : 'is-divergence'}">${row.match ? 'Coincidió' : 'Divergió'}</span>
            </div>
            <h4>${escapeHtml(row.rollcall.title || `Votación ${row.voteId}`)}</h4>
            ${object ? `<p class="agreement-object">${escapeHtml(object)}</p>` : ''}
            <dl class="agreement-comparison-pair">
              <div><dt>Su voto</dt><dd>${escapeHtml(optionLabels[row.memberOption] || row.memberOption)}</dd></div>
              <div><dt>Posición predominante de sus pares</dt><dd>${escapeHtml(optionLabels[row.peerOption] || row.peerOption)}</dd></div>
            </dl>
            <p class="agreement-group-used">Grupo usado en esa fecha: <strong>${escapeHtml(row.groupName)}</strong></p>
            <div class="agreement-detail-footer">
              ${row.rollcall.result ? `<span>Resultado general: <strong>${escapeHtml(row.rollcall.result)}</strong></span>` : '<span></span>'}
              ${row.rollcall.url ? `<a href="${escapeHtml(row.rollcall.url)}" target="_blank" rel="noopener">Ver votación oficial ↗</a>` : ''}
            </div>
          </article>
        `;
      }).join('');

      detailContainer.innerHTML = `
        <div class="agreement-detail-heading">
          <div>
            <p class="eyebrow">Evidencia</p>
            <h3>${escapeHtml(modeLabel)} · ${escapeHtml(label)}</h3>
            <p>${numberFormat.format(rows.length)} ${rows.length === 1 ? 'votación' : 'votaciones'}, de la más reciente a la más antigua.</p>
          </div>
          <button type="button" data-close-agreement-detail>Cerrar</button>
        </div>
        <div class="agreement-detail-list">${items || '<p class="agreement-detail-status">No hay votaciones en este conjunto.</p>'}</div>
      `;
      detailContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (detailError) {
      detailContainer.innerHTML = `
        <div class="agreement-detail-heading">
          <div><p class="eyebrow">Evidencia</p><h3>No pudimos cargar el detalle</h3></div>
          <button type="button" data-close-agreement-detail>Cerrar</button>
        </div>
        <p class="agreement-detail-status">${escapeHtml(detailError?.message || 'El detalle no está disponible en este momento.')}</p>
      `;
    }
  };

  container.addEventListener('click', (event) => {
    const close = event.target.closest('[data-close-agreement-detail]');
    if (close) {
      detailContainer.hidden = true;
      detailContainer.innerHTML = '';
      return;
    }

    const trigger = event.target.closest('[data-agreement-detail]');
    if (!trigger) return;
    const [type, mode] = String(trigger.dataset.agreementDetail || '').split(':');
    if (!['party', 'caucus'].includes(type) || !['match', 'diverge', 'all'].includes(mode)) return;
    renderDetail(type, mode);
  });
})();