(() => {
  const SVG_NS = 'http://www.w3.org/2000/svg';
  const profiles = window.PROFILES || {};
  const districts = window.DISTRICTS || [];
  const political = window.POLITICAL_CONFIG || { parties: {}, blocks: {} };

  const els = {
    status: document.getElementById('wn-status'), app: document.getElementById('wn-app'),
    svg: document.getElementById('wn-chart'), tooltip: document.getElementById('wn-tooltip'),
    card: document.getElementById('wn-member-card'), view1: document.getElementById('wn-view-1d'),
    view2: document.getElementById('wn-view-2d'), uncertainty: document.getElementById('wn-uncertainty'),
    context: document.getElementById('wn-context'), showAll: document.getElementById('wn-show-all'),
    download: document.getElementById('wn-download'), reset: document.getElementById('wn-reset'),
    resetZoom: document.getElementById('wn-reset-zoom'), commune: document.getElementById('wn-commune'),
    topic: document.getElementById('wn-topic'), region: document.getElementById('wn-region'),
    district: document.getElementById('wn-district'), partyList: document.getElementById('wn-party-list'),
    alignmentList: document.getElementById('wn-alignment-list'), memberSearch: document.getElementById('wn-member-search'),
    memberList: document.getElementById('wn-member-list'), chartEyebrow: document.getElementById('wn-chart-eyebrow'),
    chartTitle: document.getElementById('wn-chart-title'), chartDescription: document.getElementById('wn-chart-description'),
    chartFootnote: document.getElementById('wn-chart-footnote'), axisCaption: document.getElementById('wn-axis-caption'),
    topicBanner: document.getElementById('wn-topic-banner'), visibleCount: document.getElementById('wn-visible-count'),
    modelCount: document.getElementById('wn-model-count'), legend: document.getElementById('wn-legend')
  };

  const state = {
    view: '1d', uncertainty: false, showContext: false, showAll: false,
    topic: '', region: '', district: '', commune: '', parties: new Set(),
    alignments: new Set(), members: new Set(), activeId: null, zoom2d: null
  };

  let modelMembers = [];
  let bootstrapById = new Map();
  let topicVotes = new Map();
  let memberVotes = {};
  let topicMeta = new Map();
  let initialSelection = new Set();
  const themeStatsCache = new Map();

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  const normalize = (value) => String(value || '').toLocaleLowerCase('es-CL')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ').trim();

  const partyColor = (party) => political.parties?.[party]?.color || '#8995a2';
  const partyShort = (party) => political.parties?.[party]?.short || party || 'S/I';
  const alignmentLabel = (alignment) => political.blocks?.[alignment]?.label || ({
    oposicion: 'Oposición', oficialismo: 'Oficialismo', no_alineado: 'No alineados'
  }[alignment] || 'Sin clasificación');

  const parseCSV = (text) => {
    const src = String(text || '').replace(/^\uFEFF/, '');
    const rows = []; let row = []; let field = ''; let quoted = false;
    for (let i = 0; i < src.length; i += 1) {
      const char = src[i];
      if (quoted) {
        if (char === '"' && src[i + 1] === '"') { field += '"'; i += 1; }
        else if (char === '"') quoted = false;
        else field += char;
      } else if (char === '"') quoted = true;
      else if (char === ',') { row.push(field); field = ''; }
      else if (char === '\n') { row.push(field.replace(/\r$/, '')); rows.push(row); row = []; field = ''; }
      else field += char;
    }
    if (field.length || row.length) { row.push(field.replace(/\r$/, '')); rows.push(row); }
    if (!rows.length) return [];
    const headers = rows.shift().map((h) => h.trim());
    return rows.filter((r) => r.some((v) => String(v).trim() !== '')).map((r) => {
      const obj = {}; headers.forEach((h, idx) => { obj[h] = r[idx] ?? ''; }); return obj;
    });
  };

  const fetchText = async (url) => {
    const response = await fetch(url, { cache: 'no-store' });
    if (!response.ok) throw new Error(`No se pudo cargar ${url}`);
    return response.text();
  };

  const fetchJson = async (url) => {
    const response = await fetch(url, { cache: 'no-store' });
    if (!response.ok) throw new Error(`No se pudo cargar ${url}`);
    return response.json();
  };

  const profileById = new Map(Object.entries(profiles).map(([key, profile]) => [String(profile.id), { key, ...profile }]));

  const makeSvg = (tag, attrs = {}, text = '') => {
    const node = document.createElementNS(SVG_NS, tag);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, String(value)));
    if (text !== '') node.textContent = text;
    return node;
  };

  const quantileSelection = (members, n = 20) => {
    const ordered = [...members].filter((m) => Number.isFinite(m.d1)).sort((a, b) => a.d1 - b.d1);
    if (ordered.length <= n) return new Set(ordered.map((m) => m.id));
    const ids = new Set();
    for (let i = 0; i < n; i += 1) {
      const idx = Math.round(i * (ordered.length - 1) / (n - 1)); ids.add(ordered[idx].id);
    }
    return ids;
  };

  const districtSelection = (members, districtId, n = 20) => {
    const anchors = members.filter((m) => Number(m.profile?.district) === Number(districtId));
    const selected = new Set(anchors.map((m) => m.id));
    if (!anchors.length) return quantileSelection(members, n);
    const candidates = members.filter((m) => !selected.has(m.id));
    while (selected.size < Math.min(n, members.length) && candidates.length) {
      let bestIndex = -1; let bestDistance = Infinity;
      candidates.forEach((candidate, idx) => {
        const distance = Math.min(...anchors.map((anchor) => Math.abs(anchor.d1 - candidate.d1)));
        if (distance < bestDistance) { bestDistance = distance; bestIndex = idx; }
      });
      if (bestIndex < 0) break;
      selected.add(candidates[bestIndex].id); candidates.splice(bestIndex, 1);
    }
    return selected;
  };

  const buildFilters = () => {
    [...new Set(modelMembers.map((m) => m.profile?.region).filter(Boolean))]
      .sort((a, b) => a.localeCompare(b, 'es'))
      .forEach((region) => els.region.insertAdjacentHTML('beforeend', `<option value="${escapeHtml(region)}">${escapeHtml(region)}</option>`));

    [...new Set(modelMembers.map((m) => Number(m.profile?.district)).filter(Number.isFinite))]
      .sort((a, b) => a - b)
      .forEach((d) => els.district.insertAdjacentHTML('beforeend', `<option value="${d}">Distrito ${d}</option>`));

    const communeRecords = [];
    districts.forEach((district) => (district.comunas || []).forEach((commune) => communeRecords.push({ commune, district: district.id, region: district.region })));
    communeRecords.sort((a, b) => a.commune.localeCompare(b.commune, 'es')).forEach((item) => {
      const option = document.createElement('option'); option.value = item.commune;
      option.textContent = `${item.commune} · D${item.district}`; option.dataset.district = item.district; option.dataset.region = item.region;
      els.commune.appendChild(option);
    });

    [...topicVotes.keys()].sort((a, b) => a.localeCompare(b, 'es')).forEach((topic) => {
      els.topic.insertAdjacentHTML('beforeend', `<option value="${escapeHtml(topic)}">${escapeHtml(topic)} (${topicVotes.get(topic).size})</option>`);
    });

    const parties = [...new Set(modelMembers.map((m) => m.profile?.party || 'Sin información'))]
      .sort((a, b) => (political.parties?.[a]?.order ?? 999) - (political.parties?.[b]?.order ?? 999));
    els.partyList.innerHTML = parties.map((party) => {
      const count = modelMembers.filter((m) => (m.profile?.party || 'Sin información') === party).length;
      return `<label class="wn-check-item"><input type="checkbox" data-party="${escapeHtml(party)}"><span><b>${escapeHtml(partyShort(party))}</b> · ${escapeHtml(party)} <small>${count} con coordenada</small></span></label>`;
    }).join('');

    const alignmentOrder = ['oposicion', 'no_alineado', 'oficialismo'];
    els.alignmentList.innerHTML = alignmentOrder.map((alignment) => {
      const count = modelMembers.filter((m) => m.profile?.alignment === alignment).length;
      return `<label class="wn-check-item"><input type="checkbox" data-alignment="${alignment}"><span>${escapeHtml(alignmentLabel(alignment))}<small>${count} con coordenada</small></span></label>`;
    }).join('');
    renderMemberChecklist(); renderLegend();
  };

  const renderMemberChecklist = () => {
    const term = normalize(els.memberSearch.value);
    const visible = modelMembers.filter((m) => !term || normalize(m.name).includes(term)).sort((a, b) => a.name.localeCompare(b.name, 'es'));
    els.memberList.innerHTML = visible.map((m) => `<label class="wn-check-item"><input type="checkbox" data-member="${m.id}" ${state.members.has(m.id) ? 'checked' : ''}><span>${escapeHtml(m.name)}<small>${escapeHtml(partyShort(m.profile?.party))} · D${escapeHtml(m.profile?.district)}</small></span></label>`).join('');
  };

  const renderLegend = () => {
    const parties = [...new Set(modelMembers.map((m) => m.profile?.party || 'Sin información'))]
      .sort((a, b) => (political.parties?.[a]?.order ?? 999) - (political.parties?.[b]?.order ?? 999));
    els.legend.innerHTML = parties.map((party) => `<span class="wn-legend-item"><span class="wn-legend-dot" style="background:${partyColor(party)}"></span>${escapeHtml(partyShort(party))}</span>`).join('');
  };

  const filteredUniverse = () => modelMembers.filter((m) => {
    if (state.region && m.profile?.region !== state.region) return false;
    if (state.district && Number(m.profile?.district) !== Number(state.district)) return false;
    if (state.parties.size && !state.parties.has(m.profile?.party || 'Sin información')) return false;
    if (state.alignments.size && !state.alignments.has(m.profile?.alignment || 'no_alineado')) return false;
    return true;
  });

  const selectionForCurrentState = (universe) => {
    if (state.showAll) return new Set(universe.map((m) => m.id));
    if (state.members.size) return new Set(universe.filter((m) => state.members.has(m.id)).map((m) => m.id));
    if (state.district) return districtSelection(universe, state.district, 20);
    const initialInUniverse = [...initialSelection].filter((id) => universe.some((m) => m.id === id));
    if (initialInUniverse.length >= Math.min(8, universe.length)) return new Set(initialInUniverse);
    return quantileSelection(universe, 20);
  };

  const visibleSets = () => {
    const universe = filteredUniverse(); const selected = selectionForCurrentState(universe);
    const visible = state.showContext && !state.showAll ? new Set(universe.map((m) => m.id)) : selected;
    return { universe, selected, visible };
  };

  const themeStats = (id) => {
    if (!state.topic) return null;
    const key = `${state.topic}|${id}`; if (themeStatsCache.has(key)) return themeStatsCache.get(key);
    const ids = topicVotes.get(state.topic) || new Set();
    const stats = { totalRollcalls: ids.size, affirmative: 0, against: 0, abstention: 0, noVote: 0, excused: 0, observed: 0 };
    (memberVotes[String(id)] || []).forEach(([voteId, code]) => {
      if (!ids.has(String(voteId))) return;
      if (code === 'A') stats.affirmative += 1; else if (code === 'E') stats.against += 1;
      else if (code === 'B') stats.abstention += 1; else if (code === 'N') stats.noVote += 1; else if (code === 'D') stats.excused += 1;
      stats.observed += 1;
    });
    themeStatsCache.set(key, stats); return stats;
  };

  const updateTopicBanner = () => {
    if (!state.topic) { els.topicBanner.hidden = true; els.topicBanner.innerHTML = ''; return; }
    const set = topicVotes.get(state.topic) || new Set(); const meta = topicMeta.get(state.topic) || {};
    els.topicBanner.hidden = false;
    els.topicBanner.innerHTML = `<strong>${escapeHtml(state.topic)}</strong> · ${set.size} votaciones del universo W-NOMINATE base clasificadas con este tema principal. Las coordenadas globales permanecen fijas; el filtro solo añade contexto sobre las decisiones registradas. <span>Taxonomía: ${escapeHtml(meta.taxonomy || 'institucional-híbrida')}</span>`;
  };

  const showTooltip = (event, member) => {
    const stats = themeStats(member.id);
    els.tooltip.innerHTML = `<strong>${escapeHtml(member.name)}</strong>${escapeHtml(member.profile?.party || '')}<br><span class="muted">D${escapeHtml(member.profile?.district)} · ${escapeHtml(member.profile?.region || '')}</span>${stats ? `<br><b>${escapeHtml(state.topic)}:</b> ${stats.affirmative} a favor · ${stats.against} en contra · ${stats.abstention} abst.` : ''}<br><span class="muted">Clic para abrir detalle</span>`;
    const wrap = document.getElementById('wn-chart-wrap').getBoundingClientRect();
    const x = Math.min(event.clientX - wrap.left + 12, wrap.width - 292); const y = Math.max(8, event.clientY - wrap.top - 20);
    els.tooltip.style.left = `${Math.max(8, x)}px`; els.tooltip.style.top = `${y}px`; els.tooltip.hidden = false;
  };
  const hideTooltip = () => { els.tooltip.hidden = true; };

  const openMemberCard = (member) => {
    state.activeId = member.id; const stats = themeStats(member.id);
    const photo = member.profile?.photo ? `<img class="wn-member-photo" src="${escapeHtml(member.profile.photo)}" alt="Fotografía de ${escapeHtml(member.name)}">` : '<div class="wn-member-photo"></div>';
    els.card.hidden = false;
    els.card.innerHTML = `<div class="wn-member-grid">${photo}<div><h3>${escapeHtml(member.name)}</h3><p class="wn-member-meta">${escapeHtml(member.profile?.party || '')} · Distrito ${escapeHtml(member.profile?.district)} · ${escapeHtml(member.profile?.region || '')} · ${escapeHtml(alignmentLabel(member.profile?.alignment))}</p><div class="wn-member-coords"><span>D1: ${member.d1.toFixed(3)}</span>${Number.isFinite(member.d2) ? `<span>D2: ${member.d2.toFixed(3)}</span>` : ''}</div>${stats ? `<div class="wn-theme-votes"><div><strong>${stats.affirmative}</strong><small>A favor</small></div><div><strong>${stats.against}</strong><small>En contra</small></div><div><strong>${stats.abstention}</strong><small>Abstención</small></div><div><strong>${stats.noVote}</strong><small>No vota</small></div></div>` : ''}</div><div class="wn-member-actions"><a href="ficha.html?id=${encodeURIComponent(member.id)}">Ver ficha completa</a></div></div>`;
    render();
  };

  const domain1d = () => {
    const vals = modelMembers.map((m) => m.d1).filter(Number.isFinite); const min = Math.min(-1, ...vals); const max = Math.max(1, ...vals); const pad = (max - min) * 0.045;
    return [min - pad, max + pad];
  };

  const baseDomain2d = () => {
    const xs = modelMembers.map((m) => m.d1_2d).filter(Number.isFinite); const ys = modelMembers.map((m) => m.d2).filter(Number.isFinite);
    const xmin = Math.min(...xs), xmax = Math.max(...xs), ymin = Math.min(...ys), ymax = Math.max(...ys);
    return { xMin: xmin - 0.12, xMax: xmax + 0.12, yMin: ymin - 0.12, yMax: ymax + 0.12 };
  };

  const render1d = (sets) => {
    els.svg.innerHTML = ''; els.svg.setAttribute('viewBox', '0 0 1000 590');
    const W = 1000, left = 65, right = 55, midY = 300; const [xmin, xmax] = domain1d();
    const xScale = (v) => left + (v - xmin) / (xmax - xmin) * (W - left - right);
    [-1, -0.5, 0, 0.5, 1].forEach((tick) => {
      const x = xScale(tick); els.svg.appendChild(makeSvg('line', { x1: x, y1: 70, x2: x, y2: 515, class: tick === 0 ? 'wn-zero-line' : 'wn-grid-line' }));
      els.svg.appendChild(makeSvg('text', { x, y: 540, 'text-anchor': 'middle', class: 'wn-axis-text' }, tick.toFixed(tick === 0 ? 0 : 1)));
    });
    els.svg.appendChild(makeSvg('line', { x1: left, y1: midY, x2: W - right, y2: midY, stroke: '#b9c6d2', 'stroke-width': 1.2 }));

    const selectedMembers = modelMembers.filter((m) => sets.selected.has(m.id)).sort((a, b) => a.d1 - b.d1);
    const selectedY = new Map(); selectedMembers.forEach((m, i) => selectedY.set(m.id, midY + ((i % 7) - 3) * 38));

    if (state.uncertainty) selectedMembers.forEach((m) => {
      const b = bootstrapById.get(m.id); if (!b) return; const y = selectedY.get(m.id); const x1 = xScale(b.q025), x2 = xScale(b.q975);
      els.svg.appendChild(makeSvg('line', { x1, y1: y, x2, y2: y, class: 'wn-whisker' }));
      els.svg.appendChild(makeSvg('line', { x1, y1: y - 5, x2: x1, y2: y + 5, class: 'wn-whisker-cap' }));
      els.svg.appendChild(makeSvg('line', { x1: x2, y1: y - 5, x2, y2: y + 5, class: 'wn-whisker-cap' }));
    });

    modelMembers.filter((m) => sets.visible.has(m.id)).forEach((m) => {
      const selected = sets.selected.has(m.id); const y = selected ? selectedY.get(m.id) : midY;
      const circle = makeSvg('circle', { cx: xScale(m.d1), cy: y, r: selected ? 7 : 4.4, fill: partyColor(m.profile?.party), stroke: '#fff', 'stroke-width': 1.5, class: `wn-point ${selected ? 'wn-selected' : 'wn-muted'}`, 'data-id': m.id, tabindex: 0, 'aria-label': `${m.name}, dimensión 1 ${m.d1.toFixed(3)}` });
      circle.addEventListener('mouseenter', (e) => showTooltip(e, m)); circle.addEventListener('mousemove', (e) => showTooltip(e, m)); circle.addEventListener('mouseleave', hideTooltip); circle.addEventListener('click', () => openMemberCard(m));
      circle.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openMemberCard(m); } }); els.svg.appendChild(circle);
      if (selected) {
        if (state.activeId === m.id) els.svg.appendChild(makeSvg('circle', { cx: xScale(m.d1), cy: y, r: 11, class: 'wn-ring' }));
        const anchor = xScale(m.d1) > W * 0.7 ? 'end' : (xScale(m.d1) < W * 0.3 ? 'start' : 'middle');
        const tx = xScale(m.d1) + (anchor === 'start' ? 10 : anchor === 'end' ? -10 : 0);
        els.svg.appendChild(makeSvg('text', { x: tx, y: y - 11, 'text-anchor': anchor, class: 'wn-point-label' }, m.name.split(' ').slice(0, 2).join(' ')));
      }
    });
  };

  const render2d = (sets) => {
    els.svg.innerHTML = ''; els.svg.setAttribute('viewBox', '0 0 1000 590');
    const W = 1000, H = 590, left = 65, right = 45, top = 35, bottom = 55; const d = state.zoom2d || baseDomain2d();
    const xScale = (v) => left + (v - d.xMin) / (d.xMax - d.xMin) * (W - left - right);
    const yScale = (v) => H - bottom - (v - d.yMin) / (d.yMax - d.yMin) * (H - top - bottom);
    [-1, -0.5, 0, 0.5, 1].forEach((tick) => {
      if (tick >= d.xMin && tick <= d.xMax) { const x = xScale(tick); els.svg.appendChild(makeSvg('line', { x1: x, y1: top, x2: x, y2: H - bottom, class: tick === 0 ? 'wn-zero-line' : 'wn-grid-line' })); els.svg.appendChild(makeSvg('text', { x, y: H - 28, 'text-anchor': 'middle', class: 'wn-axis-text' }, tick.toFixed(tick === 0 ? 0 : 1))); }
      if (tick >= d.yMin && tick <= d.yMax) { const y = yScale(tick); els.svg.appendChild(makeSvg('line', { x1: left, y1: y, x2: W - right, y2: y, class: tick === 0 ? 'wn-zero-line' : 'wn-grid-line' })); els.svg.appendChild(makeSvg('text', { x: 42, y: y + 4, 'text-anchor': 'middle', class: 'wn-axis-text' }, tick.toFixed(tick === 0 ? 0 : 1))); }
    });
    els.svg.appendChild(makeSvg('text', { x: (left + W - right) / 2, y: H - 7, 'text-anchor': 'middle', class: 'wn-axis-text' }, 'Dimensión 1 · patrón principal'));
    els.svg.appendChild(makeSvg('text', { x: 15, y: (top + H - bottom) / 2, 'text-anchor': 'middle', class: 'wn-axis-text', transform: `rotate(-90 15 ${(top + H - bottom) / 2})` }, 'Dimensión 2 · exploratoria'));

    modelMembers.filter((m) => sets.visible.has(m.id) && Number.isFinite(m.d1_2d) && Number.isFinite(m.d2)).forEach((m) => {
      const selected = sets.selected.has(m.id); const cx = xScale(m.d1_2d), cy = yScale(m.d2);
      const circle = makeSvg('circle', { cx, cy, r: selected ? 7 : 4.5, fill: partyColor(m.profile?.party), stroke: '#fff', 'stroke-width': 1.5, class: `wn-point ${selected ? 'wn-selected' : 'wn-muted'}`, 'data-id': m.id, tabindex: 0, 'aria-label': `${m.name}, dimensión 1 ${m.d1_2d.toFixed(3)}, dimensión 2 ${m.d2.toFixed(3)}` });
      circle.addEventListener('mouseenter', (e) => showTooltip(e, m)); circle.addEventListener('mousemove', (e) => showTooltip(e, m)); circle.addEventListener('mouseleave', hideTooltip); circle.addEventListener('click', () => openMemberCard(m));
      circle.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openMemberCard(m); } }); els.svg.appendChild(circle);
      if (selected) { if (state.activeId === m.id) els.svg.appendChild(makeSvg('circle', { cx, cy, r: 11, class: 'wn-ring' })); const rightSide = cx > W * 0.68; els.svg.appendChild(makeSvg('text', { x: cx + (rightSide ? -9 : 9), y: cy - 8, 'text-anchor': rightSide ? 'end' : 'start', class: 'wn-point-label' }, m.name.split(' ').slice(0, 2).join(' '))); }
    });
  };

  const render = () => {
    const sets = visibleSets(); els.visibleCount.textContent = sets.visible.size; els.modelCount.textContent = modelMembers.length; updateTopicBanner();
    els.uncertainty.hidden = state.view !== '1d'; els.resetZoom.hidden = state.view !== '2d';
    els.view1.classList.toggle('is-active', state.view === '1d'); els.view1.setAttribute('aria-pressed', String(state.view === '1d'));
    els.view2.classList.toggle('is-active', state.view === '2d'); els.view2.setAttribute('aria-pressed', String(state.view === '2d'));
    els.context.setAttribute('aria-pressed', String(state.showContext)); els.uncertainty.setAttribute('aria-pressed', String(state.uncertainty));
    els.showAll.textContent = state.showAll ? 'Volver a selección' : 'Ver los 155';
    if (state.view === '1d') {
      els.chartEyebrow.textContent = 'W-NOMINATE · una dimensión'; els.chartTitle.textContent = 'Principal patrón de votación';
      els.chartDescription.textContent = 'Ordena a los parlamentarios según el principal patrón de semejanza y diferencia observado en sus votos nominales de Sala.';
      els.chartFootnote.textContent = 'El signo del eje es una orientación matemática. Una posición más cercana a cero no equivale automáticamente a mayor moderación. El rango opcional proviene de bootstrap por proyectos.';
      els.axisCaption.innerHTML = '<span>Valores negativos</span><span>Dimensión 1</span><span>Valores positivos</span>'; render1d(sets);
    } else {
      els.chartEyebrow.textContent = 'W-NOMINATE · dos dimensiones'; els.chartTitle.textContent = 'Mapa bidimensional exploratorio';
      els.chartDescription.textContent = 'La primera dimensión conserva el patrón principal; la segunda captura diferencias residuales y permanece deliberadamente sin una etiqueta política sustantiva.';
      els.chartFootnote.textContent = 'Usa la rueda o gesto de desplazamiento sobre el gráfico para acercar/alejar y arrastra para recorrer el plano. La segunda dimensión es exploratoria.';
      els.axisCaption.innerHTML = '<span>Arrastra para mover</span><span>Rueda para zoom</span><span>D2 sin etiqueta sustantiva</span>'; render2d(sets);
    }
  };

  const resetState = () => {
    state.view = '1d'; state.uncertainty = false; state.showContext = false; state.showAll = false; state.topic = ''; state.region = ''; state.district = ''; state.commune = '';
    state.parties.clear(); state.alignments.clear(); state.members.clear(); state.activeId = null; state.zoom2d = baseDomain2d(); themeStatsCache.clear();
    els.commune.value = ''; els.topic.value = ''; els.region.value = ''; els.district.value = ''; els.memberSearch.value = '';
    document.querySelectorAll('#wn-party-list input,#wn-alignment-list input').forEach((input) => { input.checked = false; }); renderMemberChecklist(); els.card.hidden = true; render();
  };

  const downloadPng = () => {
    const clone = els.svg.cloneNode(true); clone.setAttribute('xmlns', SVG_NS); const bg = document.createElementNS(SVG_NS, 'rect');
    bg.setAttribute('x', '0'); bg.setAttribute('y', '0'); bg.setAttribute('width', '100%'); bg.setAttribute('height', '100%'); bg.setAttribute('fill', '#ffffff'); clone.insertBefore(bg, clone.firstChild);
    const xml = new XMLSerializer().serializeToString(clone); const blob = new Blob([xml], { type: 'image/svg+xml;charset=utf-8' }); const url = URL.createObjectURL(blob); const img = new Image();
    img.onload = () => { const canvas = document.createElement('canvas'); canvas.width = 2000; canvas.height = 1180; const ctx = canvas.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, canvas.width, canvas.height); ctx.drawImage(img, 0, 0, canvas.width, canvas.height); URL.revokeObjectURL(url); const link = document.createElement('a'); link.download = `wnominate-${state.view}-${state.topic ? normalize(state.topic).replace(/\s+/g, '-') : 'todos'}-2026.png`; link.href = canvas.toDataURL('image/png'); link.click(); };
    img.src = url;
  };

  const bindEvents = () => {
    els.view1.addEventListener('click', () => { state.view = '1d'; render(); });
    els.view2.addEventListener('click', () => { state.view = '2d'; state.uncertainty = false; if (!state.zoom2d) state.zoom2d = baseDomain2d(); render(); });
    els.uncertainty.addEventListener('click', () => { state.uncertainty = !state.uncertainty; render(); });
    els.context.addEventListener('click', () => { state.showContext = !state.showContext; render(); });
    els.showAll.addEventListener('click', () => { state.showAll = !state.showAll; state.showContext = false; render(); });
    els.reset.addEventListener('click', resetState); els.resetZoom.addEventListener('click', () => { state.zoom2d = baseDomain2d(); render(); });
    els.topic.addEventListener('change', () => { state.topic = els.topic.value; themeStatsCache.clear(); render(); if (state.activeId) { const m = modelMembers.find((x) => x.id === state.activeId); if (m) openMemberCard(m); } });
    els.region.addEventListener('change', () => { state.region = els.region.value; state.district = ''; state.commune = ''; els.district.value = ''; els.commune.value = ''; state.showAll = false; render(); });
    els.district.addEventListener('change', () => { state.district = els.district.value; state.commune = ''; els.commune.value = ''; state.showAll = false; render(); });
    els.commune.addEventListener('change', () => { state.commune = els.commune.value; state.showAll = false; if (!state.commune) { state.district = ''; state.region = ''; els.district.value = ''; els.region.value = ''; render(); return; } const option = els.commune.selectedOptions[0]; state.district = option?.dataset?.district || ''; state.region = option?.dataset?.region || ''; els.district.value = state.district; els.region.value = state.region; render(); });
    els.partyList.addEventListener('change', (e) => { const party = e.target?.dataset?.party; if (!party) return; e.target.checked ? state.parties.add(party) : state.parties.delete(party); state.showAll = false; render(); });
    els.alignmentList.addEventListener('change', (e) => { const alignment = e.target?.dataset?.alignment; if (!alignment) return; e.target.checked ? state.alignments.add(alignment) : state.alignments.delete(alignment); state.showAll = false; render(); });
    els.memberList.addEventListener('change', (e) => { const id = e.target?.dataset?.member; if (!id) return; e.target.checked ? state.members.add(id) : state.members.delete(id); state.showAll = false; render(); });
    els.memberSearch.addEventListener('input', renderMemberChecklist);
    els.memberSearch.addEventListener('keydown', (e) => { if (e.key !== 'Enter') return; e.preventDefault(); const term = normalize(els.memberSearch.value); const match = modelMembers.find((m) => normalize(m.name).includes(term)); if (match) { state.members.add(match.id); renderMemberChecklist(); render(); openMemberCard(match); } });
    els.download.addEventListener('click', downloadPng);

    let drag = null;
    els.svg.addEventListener('wheel', (e) => {
      if (state.view !== '2d') return; e.preventDefault(); const rect = els.svg.getBoundingClientRect(); const d = state.zoom2d || baseDomain2d();
      const px = (e.clientX - rect.left) / rect.width; const py = (e.clientY - rect.top) / rect.height; const x = d.xMin + px * (d.xMax - d.xMin); const y = d.yMax - py * (d.yMax - d.yMin);
      const factor = e.deltaY < 0 ? 0.84 : 1.19; const nx = (d.xMax - d.xMin) * factor; const ny = (d.yMax - d.yMin) * factor;
      state.zoom2d = { xMin: x - px * nx, xMax: x + (1 - px) * nx, yMin: y - (1 - py) * ny, yMax: y + py * ny }; render();
    }, { passive: false });
    els.svg.addEventListener('pointerdown', (e) => { if (state.view !== '2d') return; els.svg.setPointerCapture(e.pointerId); drag = { x: e.clientX, y: e.clientY, d: { ...(state.zoom2d || baseDomain2d()) } }; });
    els.svg.addEventListener('pointermove', (e) => { if (!drag || state.view !== '2d') return; const rect = els.svg.getBoundingClientRect(); const dx = (e.clientX - drag.x) / rect.width * (drag.d.xMax - drag.d.xMin); const dy = (e.clientY - drag.y) / rect.height * (drag.d.yMax - drag.d.yMin); state.zoom2d = { xMin: drag.d.xMin - dx, xMax: drag.d.xMax - dx, yMin: drag.d.yMin + dy, yMax: drag.d.yMax + dy }; render(); });
    els.svg.addEventListener('pointerup', () => { drag = null; }); els.svg.addEventListener('pointercancel', () => { drag = null; });
  };

  const init = async () => {
    try {
      const [oneText, bootText, twoText, topicText, modelRollcallsText, votesPayload] = await Promise.all([
        fetchText('data/legislative/2026/wnominate/research_1d/member_coordinates_research.csv'),
        fetchText('data/legislative/2026/wnominate/research_1d/cluster_bootstrap_member_summary.csv'),
        fetchText('data/legislative/2026/wnominate/two_dimensional/member_coordinates_2d_aligned.csv'),
        fetchText('data/legislative/2026/topics/rollcall_topic_map.csv'),
        fetchText('data/legislative/2026/wnominate/research_1d/rollcall_coordinates_research.csv'),
        fetchJson('assets/data/participation_member_votes.json')
      ]);
      const one = parseCSV(oneText), boot = parseCSV(bootText), two = parseCSV(twoText), topics = parseCSV(topicText), modelRollcalls = parseCSV(modelRollcallsText);
      const modelVoteIds = new Set(modelRollcalls.map((r) => String(r.vote_id)));
      const twoById = new Map(two.filter((r) => r.spec_id === 'raw_lop025_2d').map((r) => [String(r.diputado_id), r]));
      modelMembers = one.map((r) => {
        const id = String(r.diputado_id), p = profileById.get(id) || {}, r2 = twoById.get(id) || {};
        return { id, name: r.diputado_nombre || p.key || `ID ${id}`, d1: Number(r.dimension_1_raw), d1_2d: Number(r2.dimension_1_aligned), d2: Number(r2.dimension_2_aligned), binaryVotes: Number(r.binary_votes), profile: p };
      }).filter((m) => Number.isFinite(m.d1));
      bootstrapById = new Map(boot.map((r) => [String(r.diputado_id), { q025: Number(r.q025), q975: Number(r.q975), width: Number(r.interval_width) }]));
      topics.forEach((r) => {
        const topic = String(r.topic_primary || '').trim(), voteId = String(r.vote_id || '').trim(); if (!topic || !voteId || !modelVoteIds.has(voteId)) return;
        if (!topicVotes.has(topic)) topicVotes.set(topic, new Set()); topicVotes.get(topic).add(voteId);
        if (!topicMeta.has(topic)) topicMeta.set(topic, { taxonomy: r.taxonomy_version, method: r.topic_method });
      });
      memberVotes = votesPayload.members || {}; initialSelection = quantileSelection(modelMembers, 20); state.zoom2d = baseDomain2d();
      buildFilters(); bindEvents(); els.status.hidden = true; els.app.hidden = false; render();
    } catch (error) {
      console.error(error); els.status.className = 'wn-loading-error'; els.status.textContent = 'No pudimos cargar el explorador W-NOMINATE. La ficha y el hemiciclo siguen disponibles mientras revisamos esta capa.';
    }
  };

  init();
})();
