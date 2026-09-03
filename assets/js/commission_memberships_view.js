(() => {
  const root = document.getElementById('commission-memberships-module');
  if (!root) return;

  const memberId = new URLSearchParams(window.location.search).get('id')?.trim();
  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  const formatStamp = (value) => {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value || 'sin fecha';
    return new Intl.DateTimeFormat('es-CL', {
      timeZone: 'America/Santiago',
      day: 'numeric', month: 'long', year: 'numeric'
    }).format(date);
  };

  const render = (snapshot, memberships) => {
    const legislative = memberships.filter((item) => {
      const n = Number.parseInt(item.number, 10);
      return n >= 1 && n <= 27;
    });
    const other = memberships.filter((item) => !legislative.includes(item));

    const cards = (rows) => rows.map((commission) => `
      <a class="member-commission-card" href="comision.html?id=${encodeURIComponent(commission.id)}">
        <span class="member-commission-number">${commission.number ? `N° ${escapeHtml(commission.number)}` : 'Otra'}</span>
        <strong>${escapeHtml(commission.name)}</strong>
        <small>${escapeHtml(commission.type || 'Permanente')} · Ver comisión</small>
      </a>
    `).join('');

    root.innerHTML = `
      <section class="member-commissions-card" aria-labelledby="member-commissions-title">
        <div class="member-commissions-heading">
          <div>
            <p class="eyebrow">Organización parlamentaria</p>
            <h2 id="member-commissions-title">Comisiones actuales</h2>
          </div>
          <a href="comisiones.html">Explorar todas</a>
        </div>
        <p class="member-commissions-lead">Membresías recuperadas desde el directorio institucional actual de la Cámara. Integrar una comisión describe una función organizativa: no demuestra por sí solo especialización, influencia, asistencia ni desempeño.</p>
        ${memberships.length ? `
          ${legislative.length ? `<div class="member-commission-group"><h3>Comisiones legislativas</h3><div class="member-commission-grid">${cards(legislative)}</div></div>` : ''}
          ${other.length ? `<div class="member-commission-group"><h3>Otras comisiones o subcomisiones</h3><div class="member-commission-grid">${cards(other)}</div></div>` : ''}
        ` : `<div class="member-commission-empty">El snapshot actual no vinculó esta ficha con una comisión. Esto no se interpreta como ausencia definitiva: puede reflejar actualización institucional o diferencias de identificación.</div>`}
        <p class="member-commission-source">Directorio actualizado: ${escapeHtml(formatStamp(snapshot.generated_at))}. Fuente: Cámara de Diputadas y Diputados de Chile.</p>
      </section>`;
  };

  const init = async () => {
    if (!memberId) return;
    try {
      const response = await fetch('data/legislative/2026/commissions/commissions_snapshot.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const snapshot = await response.json();
      if (!String(snapshot.schema_version || '').startsWith('commissions-web-v0.4') || snapshot.quality_gate?.passed !== true || (snapshot.counts?.commissions || 0) < 20) {
        throw new Error('snapshot no validado');
      }
      const memberships = (snapshot.commissions || []).filter((commission) =>
        (commission.members || []).some((member) => String(member.id) === String(memberId))
      );
      memberships.sort((a, b) => {
        const na = Number.parseInt(a.number, 10);
        const nb = Number.parseInt(b.number, 10);
        if (Number.isFinite(na) && Number.isFinite(nb)) return na - nb;
        if (Number.isFinite(na)) return -1;
        if (Number.isFinite(nb)) return 1;
        return String(a.name || '').localeCompare(String(b.name || ''), 'es');
      });
      render(snapshot, memberships);
    } catch (error) {
      root.innerHTML = `
        <section class="member-commissions-card is-unavailable">
          <p class="eyebrow">Organización parlamentaria</p>
          <h2>Comisiones actuales</h2>
          <p>No mostramos membresías cuando el directorio institucional no supera sus controles de actualización y cobertura.</p>
        </section>`;
    }
  };

  init();
})();
