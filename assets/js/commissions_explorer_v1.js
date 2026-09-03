(() => {
  const root = document.getElementById('commissions-root');
  if (!root) return;

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const normalize = (value) => String(value ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('es-CL');
  let snapshot = null;

  const card = (commission) => {
    const href = `comision.html?id=${encodeURIComponent(commission.id)}`;
    const memberCount = Array.isArray(commission.members) ? commission.members.length : 0;
    return `<a class="commission-card" href="${escapeHtml(href)}"><span class="commission-number">${escapeHtml(commission.number || '—')}</span><div><h3>${escapeHtml(commission.name)}</h3><p>${memberCount ? `${memberCount} integrantes recuperados de la ficha institucional` : 'Integrantes no recuperados por el snapshot'}</p></div><span class="commission-pill">${escapeHtml(commission.type || 'Permanente')}</span></a>`;
  };

  const render = (query = '') => {
    const q = normalize(query.trim());
    const all = snapshot.commissions || [];
    const filtered = q ? all.filter((commission) => normalize(`${commission.number} ${commission.name} ${commission.type}`).includes(q)) : all;
    const legislative = filtered.filter((commission) => Number.parseInt(commission.number, 10) >= 1 && Number.parseInt(commission.number, 10) <= 27);
    const other = filtered.filter((commission) => !(Number.parseInt(commission.number, 10) >= 1 && Number.parseInt(commission.number, 10) <= 27));

    if (!filtered.length) {
      root.innerHTML = `<div class="commission-empty">No encontramos una comisión para <strong>${escapeHtml(query)}</strong>.</div>`;
      return;
    }

    root.innerHTML = `
      ${legislative.length ? `<section class="commission-group"><div class="commission-group-head"><div><p class="eyebrow">1–27</p><h2>Comisiones legislativas permanentes</h2></div><p>La Cámara informa actualmente 27 comisiones permanentes encargadas del estudio y despacho de proyectos u otros asuntos asignados por la Sala.</p></div><div class="commission-grid">${legislative.map(card).join('')}</div></section>` : ''}
      ${other.length ? `<section class="commission-group"><div class="commission-group-head"><div><p class="eyebrow">Organización interna y funciones especiales</p><h2>Otras comisiones permanentes y subcomisiones</h2></div><p>Se muestran separadas para no confundirlas con las 27 comisiones legislativas temáticas. Sus competencias y composiciones pueden ser distintas.</p></div><div class="commission-grid">${other.map(card).join('')}</div></section>` : ''}
      <p class="commission-caveat"><strong>Fuente y alcance:</strong> ${escapeHtml(snapshot.scope_note || '')} Actualizado: ${escapeHtml(new Intl.DateTimeFormat('es-CL', { timeZone: 'America/Santiago', dateStyle: 'medium', timeStyle: 'short' }).format(new Date(snapshot.generated_at)))}.</p>`;
  };

  const init = async () => {
    root.innerHTML = '<div class="commission-loading">Cargando directorio institucional de comisiones…</div>';
    try {
      const response = await fetch('data/legislative/2026/commissions/commissions_snapshot.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      snapshot = await response.json();
      if (!String(snapshot.schema_version || '').startsWith('commissions-web-v0.4') || snapshot.quality_gate?.passed !== true || (snapshot.counts?.commissions || 0) < 20) {
        throw new Error('El snapshot disponible no supera el gate de calidad v0.4');
      }
      render('');
      const search = document.getElementById('commission-search');
      search?.addEventListener('input', () => render(search.value));
    } catch (error) {
      root.innerHTML = `<div class="commission-error"><strong>El directorio actual no está disponible.</strong><br>${escapeHtml(error.message)}. La vista se bloquea para evitar mostrar como actuales datos de comisiones que no hayan superado el control de fuente.</div>`;
    }
  };

  init();
})();
