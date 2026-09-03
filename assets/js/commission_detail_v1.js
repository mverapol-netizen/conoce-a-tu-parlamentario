(() => {
  const root = document.getElementById('commission-detail-root');
  if (!root) return;

  const commissionId = new URLSearchParams(window.location.search).get('id')?.trim();
  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const safeUrl = (value) => /^https:\/\//i.test(String(value || '')) ? String(value) : '';
  const cleanName = (value) => String(value || '').replace(/^(Sr\.|Sra\.)\s*/i, '').trim();

  const formatStamp = (value) => {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value || 'Sin fecha';
    return new Intl.DateTimeFormat('es-CL', { timeZone: 'America/Santiago', dateStyle: 'medium', timeStyle: 'short' }).format(date);
  };

  const memberCard = (member) => {
    const name = cleanName(member.name);
    const local = member.id ? `ficha.html?id=${encodeURIComponent(member.id)}` : '';
    const official = safeUrl(member.profile_url);
    if (local) return `<a class="commission-member" href="${escapeHtml(local)}">${escapeHtml(name)}<small>Ver ficha parlamentaria</small></a>`;
    if (official) return `<a class="commission-member" href="${escapeHtml(official)}" target="_blank" rel="noopener noreferrer">${escapeHtml(name)}<small>Ver perfil oficial</small></a>`;
    return `<div class="commission-member">${escapeHtml(name)}<small>Identificador local no disponible</small></div>`;
  };

  const render = (snapshot, commission) => {
    document.title = `${commission.name} · Comisión`;
    const number = Number.parseInt(commission.number, 10);
    const category = number >= 1 && number <= 27 ? 'Comisión legislativa permanente' : 'Otra comisión permanente o subcomisión';
    const members = Array.isArray(commission.members) ? commission.members : [];
    const official = safeUrl(commission.source_url || commission.members_url);
    const sessions = safeUrl(commission.sessions_url);
    const projects = safeUrl(commission.projects_url);
    const citations = safeUrl(commission.citations_url);
    const results = safeUrl(commission.results_url);

    root.innerHTML = `
      <nav class="edu-breadcrumb" aria-label="Migas de pan"><a href="entender.html">Entiende el Congreso</a><span>›</span><a href="comisiones.html">Comisiones</a><span>›</span><strong>${escapeHtml(commission.name)}</strong></nav>
      <article class="commission-detail">
        <div class="commission-kicker"><span class="commission-pill">N° ${escapeHtml(commission.number || '—')}</span><span class="commission-pill">${escapeHtml(commission.type || 'Permanente')}</span></div>
        <h1>${escapeHtml(commission.name)}</h1>
        <p>${escapeHtml(category)}. Esta ficha conecta la explicación institucional de qué es una comisión con la instancia concreta que aparece en el directorio actual de la Cámara.</p>
        <div class="commission-facts">
          <div class="commission-fact"><span>Identificador institucional</span><strong>prmID ${escapeHtml(commission.id)}</strong></div>
          <div class="commission-fact"><span>Integrantes recuperados</span><strong>${members.length || 'No disponibles'}</strong></div>
          <div class="commission-fact"><span>Snapshot</span><strong>${escapeHtml(formatStamp(snapshot.generated_at))}</strong></div>
        </div>
        <div class="commission-links">
          ${official ? `<a href="${escapeHtml(official)}" target="_blank" rel="noopener noreferrer">Abrir ficha oficial</a>` : ''}
          <a href="aprender.html?id=comisiones">¿Qué hace una comisión?</a>
        </div>
      </article>

      <section class="commission-section">
        <h2>Integrantes</h2>
        <p class="commission-section-lead">Personas recuperadas desde la sección “Integrantes” de la ficha institucional. La pertenencia a una comisión no significa por sí sola especialización técnica ni determina cómo votará cada integrante.</p>
        ${members.length ? `<div class="commission-members">${members.map(memberCard).join('')}</div>` : '<div class="commission-empty">La fuente utilizada no devolvió integrantes para esta ficha. No se interpreta como una comisión sin miembros.</div>'}
      </section>

      <section class="commission-section">
        <h2>Seguir su actividad en la fuente oficial</h2>
        <p class="commission-section-lead">La Cámara separa sesiones, proyectos, citaciones y resultados. Mantener esas capas distintas evita tratar una citación como si fuera una decisión ya adoptada.</p>
        <div class="commission-links">
          ${sessions ? `<a href="${escapeHtml(sessions)}" target="_blank" rel="noopener noreferrer">Sesiones</a>` : ''}
          ${projects ? `<a href="${escapeHtml(projects)}" target="_blank" rel="noopener noreferrer">Proyectos de ley</a>` : ''}
          ${citations ? `<a href="${escapeHtml(citations)}" target="_blank" rel="noopener noreferrer">Citaciones</a>` : ''}
          ${results ? `<a href="${escapeHtml(results)}" target="_blank" rel="noopener noreferrer">Resultados</a>` : ''}
        </div>
        <p class="commission-caveat"><strong>Alcance de esta versión:</strong> todavía no copiamos todas las sesiones, audiencias, oficios e informes a nuestra propia base. Los enlaces anteriores llevan al registro institucional vivo. ${escapeHtml(snapshot.scope_note || '')}</p>
      </section>`;
  };

  const init = async () => {
    if (!commissionId) {
      root.innerHTML = '<div class="commission-error"><strong>Falta el identificador de comisión.</strong><br>Vuelve al directorio y selecciona una comisión.</div>';
      return;
    }
    root.innerHTML = '<div class="commission-loading">Cargando comisión desde el snapshot institucional…</div>';
    try {
      const response = await fetch('data/legislative/2026/commissions/commissions_snapshot.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const snapshot = await response.json();
      if (!String(snapshot.schema_version || '').startsWith('commissions-web-v0.4') || snapshot.quality_gate?.passed !== true || (snapshot.counts?.commissions || 0) < 20) {
        throw new Error('El snapshot disponible no supera el gate de calidad v0.4');
      }
      const commission = (snapshot.commissions || []).find((item) => item.id === commissionId);
      if (!commission) throw new Error(`No encontramos la comisión ${commissionId} en el directorio actual`);
      render(snapshot, commission);
    } catch (error) {
      root.innerHTML = `<div class="commission-error"><strong>No podemos mostrar esta comisión como actual.</strong><br>${escapeHtml(error.message)}.</div>`;
    }
  };

  init();
})();
