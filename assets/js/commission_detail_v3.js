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

  const periodLabel = (layer) => {
    const options = layer?.page_period?.selected_options || [];
    const texts = options.map((item) => item.text).filter(Boolean);
    return texts.length ? texts.join(' · ') : 'vista devuelta por la fuente';
  };

  const activityText = (row) => {
    const excluded = new Set(['date_context', 'horario', 'sala']);
    const values = [];
    Object.entries(row || {}).forEach(([key, value]) => {
      if (excluded.has(key)) return;
      const text = String(value || '').trim();
      if (!text || values.includes(text)) return;
      values.push(text);
    });
    return values.join(' ');
  };

  const activityItem = (row, kind) => {
    const text = activityText(row);
    const preview = text.length > 420 ? `${text.slice(0, 417).trim()}…` : text;
    const meta = [row.date_context, row.horario, row.sala].filter(Boolean);
    const full = text.length > 420
      ? `<details class="commission-activity-details"><summary>Leer registro institucional completo</summary><p>${escapeHtml(text)}</p></details>`
      : '';
    return `<article class="commission-activity-item ${kind === 'result' ? 'is-result' : 'is-citation'}">
      <div class="commission-activity-meta">${meta.map((value) => `<span>${escapeHtml(value)}</span>`).join('')}</div>
      <p>${escapeHtml(preview || 'La fila institucional no contiene texto descriptivo recuperable.')}</p>
      ${full}
    </article>`;
  };

  const activityLayer = (title, explanation, layer, kind) => {
    const rows = Array.isArray(layer?.rows) ? layer.rows.slice(0, 3) : [];
    const official = safeUrl(layer?.url);
    return `<div class="commission-activity-card">
      <div class="commission-activity-head"><div><p class="eyebrow">${escapeHtml(periodLabel(layer))}</p><h3>${escapeHtml(title)}</h3></div>${official ? `<a href="${escapeHtml(official)}" target="_blank" rel="noopener noreferrer">Abrir fuente</a>` : ''}</div>
      <p class="commission-section-lead">${escapeHtml(explanation)}</p>
      ${rows.length ? `<div class="commission-activity-list">${rows.map((row) => activityItem(row, kind)).join('')}</div>` : `<div class="commission-empty">La vista recuperada no devolvió filas para este período. Esto no significa que la comisión no tenga actividad histórica.</div>`}
    </div>`;
  };

  const sessionItem = (row) => {
    const number = row.n || row.nº || row.numero || row.número || '—';
    const date = row['día'] || row.dia || 'Sin fecha recuperada';
    const start = row.inicio || '';
    const end = row['término'] || row.termino || '';
    const state = row.estado || 'Estado no recuperado';
    const time = start && end ? `${start}–${end}` : (start || end || 'Sin horario recuperado');
    return `<article class="commission-activity-item is-session">
      <div class="commission-activity-meta"><span>Sesión N° ${escapeHtml(number)}</span><span>${escapeHtml(date)}</span><span>${escapeHtml(time)}</span></div>
      <p><strong>${escapeHtml(state)}</strong>. Este estado proviene del registro institucional de sesiones y no se utiliza como medida de productividad.</p>
    </article>`;
  };

  const sessionLayer = (layer) => {
    const rows = Array.isArray(layer?.rows) ? layer.rows.slice(0, 5) : [];
    const official = safeUrl(layer?.url);
    return `<div class="commission-activity-card">
      <div class="commission-activity-head"><div><p class="eyebrow">${escapeHtml(periodLabel(layer))}</p><h3>Sesiones</h3></div>${official ? `<a href="${escapeHtml(official)}" target="_blank" rel="noopener noreferrer">Abrir fuente</a>` : ''}</div>
      <p class="commission-section-lead">Cuándo se reunió o fue registrada la comisión, con número de sesión, fecha, horario y estado. Esta capa describe calendario e historia institucional, no desempeño.</p>
      ${rows.length ? `<div class="commission-activity-list">${rows.map(sessionItem).join('')}</div>` : `<div class="commission-empty">La vista recuperada no devolvió sesiones para este período. No se interpreta como ausencia de actividad histórica.</div>`}
    </div>`;
  };

  const render = (snapshot, commission, activitySnapshot, activity) => {
    document.title = `${commission.name} · Comisión`;
    const number = Number.parseInt(commission.number, 10);
    const category = number >= 1 && number <= 27 ? 'Comisión legislativa permanente' : 'Otra comisión permanente o subcomisión';
    const members = Array.isArray(commission.members) ? commission.members : [];
    const official = safeUrl(commission.source_url || commission.members_url);
    const sessions = safeUrl(commission.sessions_url);
    const projects = safeUrl(commission.projects_url);
    const citations = safeUrl(commission.citations_url);
    const results = safeUrl(commission.results_url);
    const activityAvailable = activitySnapshot && activity && activitySnapshot.quality_gate?.passed === true;

    root.innerHTML = `
      <nav class="edu-breadcrumb" aria-label="Migas de pan"><a href="entender.html">Entiende el Congreso</a><span>›</span><a href="comisiones.html">Comisiones</a><span>›</span><strong>${escapeHtml(commission.name)}</strong></nav>
      <article class="commission-detail">
        <div class="commission-kicker"><span class="commission-pill">N° ${escapeHtml(commission.number || '—')}</span><span class="commission-pill">${escapeHtml(commission.type || 'Permanente')}</span></div>
        <h1>${escapeHtml(commission.name)}</h1>
        <p>${escapeHtml(category)}. Esta ficha conecta la explicación institucional de qué es una comisión con la instancia concreta que aparece en el directorio actual de la Cámara.</p>
        <div class="commission-facts">
          <div class="commission-fact"><span>Identificador institucional</span><strong>prmID ${escapeHtml(commission.id)}</strong></div>
          <div class="commission-fact"><span>Integrantes recuperados</span><strong>${members.length || 'No disponibles'}</strong></div>
          <div class="commission-fact"><span>Snapshot membresía</span><strong>${escapeHtml(formatStamp(snapshot.generated_at))}</strong></div>
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
        <h2>Actividad reciente recuperada</h2>
        <p class="commission-section-lead">Sesiones, citaciones y resultados responden preguntas distintas. La interfaz las mantiene separadas para no convertir calendario, agenda prevista y decisiones registradas en una sola medida de “actividad”.</p>
        ${activityAvailable ? `<div class="commission-activity-grid">
          ${sessionLayer(activity.sessions)}
          ${activityLayer('Citaciones', 'Qué asuntos aparecen convocados en la vista institucional recuperada. Una citación describe agenda prevista, no asegura que el asunto haya sido efectivamente tratado ni aprobado.', activity.citations, 'citation')}
          ${activityLayer('Resultados', 'Qué registra posteriormente la página de resultados de la comisión. El texto puede incluir acuerdos, avance de proyectos, invitados, asistencia y otras constancias de la sesión.', activity.results, 'result')}
        </div><p class="commission-caveat"><strong>Alcance:</strong> ${escapeHtml(activitySnapshot.scope_note || '')} Snapshot de actividad: ${escapeHtml(formatStamp(activitySnapshot.generated_at))}.</p>` : `<div class="commission-empty">La capa de actividad no está disponible o no superó su control de calidad. La ficha conserva membresía y enlaces oficiales sin inferir actividad.</div>`}
      </section>

      <section class="commission-section">
        <h2>Seguir en la fuente oficial</h2>
        <p class="commission-section-lead">Las páginas oficiales permiten profundizar en sesiones, proyectos, citaciones y resultados. Todavía no reconstruimos en nuestra base todas las actas, audiencias, oficios, informes ni el historial documental completo.</p>
        <div class="commission-links">
          ${sessions ? `<a href="${escapeHtml(sessions)}" target="_blank" rel="noopener noreferrer">Sesiones</a>` : ''}
          ${projects ? `<a href="${escapeHtml(projects)}" target="_blank" rel="noopener noreferrer">Proyectos de ley</a>` : ''}
          ${citations ? `<a href="${escapeHtml(citations)}" target="_blank" rel="noopener noreferrer">Citaciones</a>` : ''}
          ${results ? `<a href="${escapeHtml(results)}" target="_blank" rel="noopener noreferrer">Resultados</a>` : ''}
        </div>
        <p class="commission-caveat"><strong>Membresía:</strong> ${escapeHtml(snapshot.scope_note || '')}</p>
      </section>`;
  };

  const init = async () => {
    if (!commissionId) {
      root.innerHTML = '<div class="commission-error"><strong>Falta el identificador de comisión.</strong><br>Vuelve al directorio y selecciona una comisión.</div>';
      return;
    }
    root.innerHTML = '<div class="commission-loading">Cargando comisión y actividad institucional…</div>';
    try {
      const [directoryResponse, activityResponse] = await Promise.all([
        fetch('data/legislative/2026/commissions/commissions_snapshot.json', { cache: 'no-store' }),
        fetch('data/legislative/2026/commissions/commission_activity_snapshot.json', { cache: 'no-store' })
      ]);
      if (!directoryResponse.ok) throw new Error(`Directorio HTTP ${directoryResponse.status}`);
      const snapshot = await directoryResponse.json();
      if (!String(snapshot.schema_version || '').startsWith('commissions-web-v0.4') || snapshot.quality_gate?.passed !== true || (snapshot.counts?.commissions || 0) < 20) {
        throw new Error('El snapshot de membresía no supera el gate de calidad v0.4');
      }
      const commission = (snapshot.commissions || []).find((item) => item.id === commissionId);
      if (!commission) throw new Error(`No encontramos la comisión ${commissionId} en el directorio actual`);

      let activitySnapshot = null;
      let activity = null;
      if (activityResponse.ok) {
        const candidate = await activityResponse.json();
        if (String(candidate.schema_version || '').startsWith('commission-activity-web-v0.3') && candidate.quality_gate?.passed === true) {
          activitySnapshot = candidate;
          activity = (candidate.commissions || []).find((item) => item.id === commissionId) || null;
        }
      }
      render(snapshot, commission, activitySnapshot, activity);
    } catch (error) {
      root.innerHTML = `<div class="commission-error"><strong>No podemos mostrar esta comisión como actual.</strong><br>${escapeHtml(error.message)}.</div>`;
    }
  };

  init();
})();
