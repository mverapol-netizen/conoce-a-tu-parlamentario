(() => {
  const profiles = window.PROFILES || {};
  const config = window.POLITICAL_CONFIG || { parties: {}, blocks: {}, caucusKeywords: [], majority: 78 };
  const svg = document.getElementById('hemicycle-svg');
  const tooltip = document.getElementById('hemicycle-tooltip');
  const panel = document.getElementById('member-panel');
  const legend = document.getElementById('party-legend');
  const caucusBody = document.getElementById('caucus-body');

  const normalize = (value) => String(value || '')
    .toLocaleLowerCase('es-CL')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

  const legislativeUrl = (member) => member.id
    ? `ficha.html?id=${encodeURIComponent(member.id)}`
    : `ficha.html?nombre=${encodeURIComponent(member.name)}`;

  const isIndependent = (profile) => normalize(profile.party).startsWith('independ');

  const partyFromCaucus = (caucus) => {
    const text = normalize(caucus);
    for (const [needle, party] of config.caucusKeywords || []) {
      if (text.includes(normalize(needle))) return party;
    }
    return null;
  };

  const partyMeta = (party) => config.parties?.[party] || config.parties?.['Sin información'] || {
    short: 'S/I', color: '#aab2bb', order: 999, alignment: 'no_alineado'
  };

  const effectiveParty = (profile) => {
    if (!isIndependent(profile)) return profile.party || 'Sin información';
    return partyFromCaucus(profile.caucus) || 'Independientes';
  };

  const alignmentFor = (profile) => {
    if (profile.alignment && config.blocks?.[profile.alignment]) return profile.alignment;
    const party = effectiveParty(profile);
    return partyMeta(party).alignment || 'no_alineado';
  };

  const memberFromEntry = ([name, profile]) => {
    const effective = effectiveParty(profile);
    const meta = partyMeta(effective);
    const alignment = alignmentFor(profile);
    return {
      name,
      ...profile,
      effectiveParty: effective,
      color: meta.color,
      partyShort: meta.short,
      partyOrder: meta.order,
      alignment,
      independent: isIndependent(profile),
      affiliation: profile.affiliationLabel || (isIndependent(profile)
        ? `Independiente en ${profile.caucus || 'bancada por confirmar'}`
        : profile.party)
    };
  };

  const members = Object.entries(profiles).map(memberFromEntry);
  const blockOrder = (alignment) => config.blocks?.[alignment]?.order ?? 1;
  members.sort((a, b) =>
    blockOrder(a.alignment) - blockOrder(b.alignment) ||
    a.partyOrder - b.partyOrder ||
    a.name.localeCompare(b.name, 'es')
  );

  const blockCounts = members.reduce((acc, member) => {
    acc[member.alignment] = (acc[member.alignment] || 0) + 1;
    return acc;
  }, {});

  document.getElementById('total-seats').textContent = members.length;
  document.getElementById('majority-seats').textContent = config.majority || 78;
  document.getElementById('opposition-seats').textContent = blockCounts.oposicion || 0;
  document.getElementById('autonomous-seats').textContent = blockCounts.no_alineado || 0;
  document.getElementById('government-seats').textContent = blockCounts.oficialismo || 0;

  const rows = [21, 27, 33, 35, 39];
  const radii = [135, 180, 225, 270, 315];
  const positions = [];
  const cx = 400;
  const cy = 390;
  const start = Math.PI + 0.08;
  const end = Math.PI * 2 - 0.08;

  rows.forEach((count, rowIndex) => {
    const radius = radii[rowIndex];
    for (let i = 0; i < count; i += 1) {
      const angle = count === 1 ? (start + end) / 2 : start + (end - start) * (i / (count - 1));
      positions.push({
        angle,
        radius,
        x: cx + Math.cos(angle) * radius,
        y: cy + Math.sin(angle) * radius
      });
    }
  });

  positions.sort((a, b) => a.angle - b.angle || b.radius - a.radius);

  const svgNs = 'http://www.w3.org/2000/svg';
  const backgroundArc = document.createElementNS(svgNs, 'path');
  backgroundArc.setAttribute('d', 'M 56 390 A 344 344 0 0 1 744 390');
  backgroundArc.setAttribute('fill', 'none');
  backgroundArc.setAttribute('stroke', '#dfe7ee');
  backgroundArc.setAttribute('stroke-width', '1.5');
  svg.appendChild(backgroundArc);

  const selectedSeat = { node: null };

  const showTooltip = (member, event) => {
    tooltip.innerHTML = `
      <strong>${escapeHtml(member.name)}</strong>
      <span>${escapeHtml(member.affiliation || member.party)}</span>
      <span>Distrito ${escapeHtml(member.district)} · ${escapeHtml(member.caucus || 'Bancada por confirmar')}</span>
    `;
    const stage = svg.parentElement;
    const rect = stage.getBoundingClientRect();
    const clientX = event.clientX ?? (rect.left + rect.width / 2);
    const clientY = event.clientY ?? (rect.top + rect.height / 2);
    tooltip.style.left = `${Math.max(8, Math.min(rect.width - 250, clientX - rect.left))}px`;
    tooltip.style.top = `${Math.max(70, clientY - rect.top)}px`;
    tooltip.hidden = false;
  };

  const hideTooltip = () => { tooltip.hidden = true; };

  const selectMember = (member, node) => {
    if (selectedSeat.node) selectedSeat.node.classList.remove('is-selected');
    selectedSeat.node = node;
    node.classList.add('is-selected');
    const blockLabel = config.blocks?.[member.alignment]?.label || 'No alineado';
    const photo = member.photo
      ? `<img src="${escapeHtml(member.photo)}" alt="Fotografía de ${escapeHtml(member.name)}">`
      : `<div class="member-photo-fallback" aria-hidden="true"></div>`;
    panel.innerHTML = `
      <div class="member-panel-grid">
        ${photo}
        <div>
          <h3>${escapeHtml(member.name)}</h3>
          <p>${escapeHtml(member.affiliation || member.party)}</p>
          <p>${escapeHtml(member.caucus || 'Bancada por confirmar')} · Distrito ${escapeHtml(member.district)} · ${escapeHtml(blockLabel)}</p>
        </div>
        <a href="${escapeHtml(legislativeUrl(member))}">Ficha legislativa</a>
      </div>
    `;
    panel.hidden = false;
  };

  members.forEach((member, index) => {
    const pos = positions[index];
    const circle = document.createElementNS(svgNs, 'circle');
    circle.setAttribute('cx', pos.x.toFixed(2));
    circle.setAttribute('cy', pos.y.toFixed(2));
    circle.setAttribute('r', '7.2');
    circle.setAttribute('fill', member.color);
    circle.setAttribute('tabindex', '0');
    circle.setAttribute('role', 'button');
    circle.setAttribute('aria-label', `${member.name}, ${member.affiliation}, distrito ${member.district}`);
    circle.classList.add('seat');
    if (member.independent) circle.classList.add('is-independent');
    circle.dataset.alignment = member.alignment;
    circle.dataset.party = member.effectiveParty;
    circle.addEventListener('mouseenter', (event) => showTooltip(member, event));
    circle.addEventListener('mousemove', (event) => showTooltip(member, event));
    circle.addEventListener('mouseleave', hideTooltip);
    circle.addEventListener('focus', (event) => showTooltip(member, event));
    circle.addEventListener('blur', hideTooltip);
    circle.addEventListener('click', () => selectMember(member, circle));
    circle.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        selectMember(member, circle);
      }
    });
    svg.appendChild(circle);
  });

  const partyCounts = new Map();
  members.forEach((member) => {
    const key = member.independent ? member.effectiveParty : member.party;
    const item = partyCounts.get(key) || { count: 0, independents: 0 };
    item.count += 1;
    if (member.independent) item.independents += 1;
    partyCounts.set(key, item);
  });

  [...partyCounts.entries()]
    .sort((a, b) => partyMeta(a[0]).order - partyMeta(b[0]).order)
    .forEach(([party, data]) => {
      const meta = partyMeta(party);
      const row = document.createElement('div');
      row.className = 'party-row';
      row.dataset.party = party;
      row.innerHTML = `
        <span class="party-dot" style="background:${escapeHtml(meta.color)}"></span>
        <div><strong>${escapeHtml(meta.short)} · ${escapeHtml(party)}</strong>${data.independents ? `<small>Incluye ${data.independents} independiente${data.independents > 1 ? 's' : ''} adscrito${data.independents > 1 ? 's' : ''}</small>` : ''}</div>
        <span class="party-count">${data.count}</span>
      `;
      row.addEventListener('mouseenter', () => {
        svg.querySelectorAll('.seat').forEach((seat) => seat.classList.toggle('is-muted', seat.dataset.party !== party));
      });
      row.addEventListener('mouseleave', () => svg.querySelectorAll('.seat').forEach((seat) => seat.classList.remove('is-muted')));
      legend.appendChild(row);
    });

  const caucuses = new Map();
  members.forEach((member) => {
    const caucus = member.caucus || 'Bancada por confirmar';
    const item = caucuses.get(caucus) || { count: 0, blocks: {} };
    item.count += 1;
    item.blocks[member.alignment] = (item.blocks[member.alignment] || 0) + 1;
    caucuses.set(caucus, item);
  });

  const dominantBlock = (blocks) => Object.entries(blocks).sort((a, b) => b[1] - a[1])[0]?.[0] || 'no_alineado';
  [...caucuses.entries()]
    .sort((a, b) => b[1].count - a[1].count || a[0].localeCompare(b[0], 'es'))
    .forEach(([caucus, data]) => {
      const block = dominantBlock(data.blocks);
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${escapeHtml(caucus)}</td>
        <td><span class="block-pill ${escapeHtml(block)}">${escapeHtml(config.blocks?.[block]?.label || 'No alineado')}</span></td>
        <td>${data.count}</td>
      `;
      caucusBody.appendChild(row);
    });

  document.querySelectorAll('[data-filter-block]').forEach((button) => {
    button.addEventListener('click', () => {
      const block = button.dataset.filterBlock;
      const active = button.classList.toggle('is-active');
      document.querySelectorAll('[data-filter-block]').forEach((other) => { if (other !== button) other.classList.remove('is-active'); });
      svg.querySelectorAll('.seat').forEach((seat) => {
        seat.classList.toggle('is-muted', active && seat.dataset.alignment !== block);
      });
    });
  });

  document.getElementById('political-reviewed').textContent = config.reviewed || 'sin fecha';
})();
