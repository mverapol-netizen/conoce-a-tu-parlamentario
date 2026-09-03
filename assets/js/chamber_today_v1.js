(() => {
  const root = document.getElementById('chamber-today-root');
  if (!root) return;

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  const chileDate = () => {
    const parts = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'America/Santiago', year: 'numeric', month: '2-digit', day: '2-digit'
    }).formatToParts(new Date());
    const values = Object.fromEntries(parts.map((part) => [part.type, part.value]));
    return `${values.year}-${values.month}-${values.day}`;
  };

  const formatDate = (iso) => {
    if (!iso) return 'Fecha no informada';
    const date = new Date(`${String(iso).slice(0, 10)}T12:00:00-04:00`);
    if (Number.isNaN(date.getTime())) return iso;
    return new Intl.DateTimeFormat('es-CL', { timeZone: 'America/Santiago', weekday: 'long', day: 'numeric', month: 'long' }).format(date);
  };

  const formatTime = (iso) => {
    if (!iso) return '—';
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) return '—';
    return new Intl.DateTimeFormat('es-CL', { timeZone: 'America/Santiago', hour: '2-digit', minute: '2-digit', hour12: false }).format(date);
  };

  const formatStamp = (iso) => {
    if (!iso) return 'Sin hora de actualización';
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) return iso;
    return new Intl.DateTimeFormat('es-CL', {
      timeZone: 'America/Santiago', dateStyle: 'medium', timeStyle: 'short'
    }).format(date);
  };

  const renderSession = (session, showDate = false) => {
    const start = formatTime(session.start);
    const end = formatTime(session.end);
    const dateText = showDate ? formatDate(session.local_date) : '';
    return `<article class="today-session"><div class="today-time">${escapeHtml(start)}<small>${end !== '—' ? `– ${escapeHtml(end)}` : 'hora Chile'}</small></div><div><h3>${escapeHtml(session.type || 'Sesión de Sala')} ${session.number ? `N° ${escapeHtml(session.number)}` : ''}</h3><p>${showDate ? `${escapeHtml(dateText)} · ` : ''}Registro oficial de sesión de Sala · ID ${escapeHtml(session.session_id)}</p></div><div class="today-pills">${session.state ? `<span class="today-pill">${escapeHtml(session.state)}</span>` : ''}<span class="today-pill">Sala</span></div></article>`;
  };

  const render = (data) => {
    const actualChileDate = chileDate();
    const fresh = data.local_date === actualChileDate;
    const todayRows = fresh ? (data.today || []) : [];
    const upcoming = data.upcoming || [];
    const recent = data.recent || [];
    const sourceUrl = data.source?.url || 'https://opendata.camara.cl/camaradiputados/pages/sala/retornarSesionesXAnno.aspx';

    root.innerHTML = `
      <nav class="edu-breadcrumb" aria-label="Migas de pan"><a href="entender.html">Entiende el Congreso</a><span>›</span><strong>Hoy en la Cámara</strong></nav>
      <div class="today-hero">
        <article class="today-card">
          <p class="eyebrow">Agenda institucional · Sala</p>
          <h1>Hoy en la Cámara</h1>
          <p>Una vista diaria de las sesiones de Sala registradas por el servicio oficial de datos abiertos. Esta primera versión muestra <strong>cuándo sesiona la Sala</strong>; no confunde ese calendario con la tabla de asuntos que eventualmente serán discutidos o votados.</p>
          <div class="today-actions"><a class="today-primary" href="aprender.html?id=agenda-y-tabla">¿Cómo se organiza la agenda?</a><a class="today-secondary" href="votaciones.html">Ver votaciones nominales</a></div>
        </article>
        <aside class="today-status">
          <span class="today-status-label">Snapshot oficial consultado</span>
          <strong>${escapeHtml(formatStamp(data.generated_at))}</strong>
          <small>Zona horaria: Chile continental · fuente: Cámara de Diputadas y Diputados, Open Data.</small>
          <span class="${fresh ? 'today-fresh' : 'today-stale'}">${fresh ? 'Actualizado para hoy' : `Snapshot del ${escapeHtml(data.local_date || 'día no informado')}`}</span>
        </aside>
      </div>

      <section class="today-section">
        <div class="today-section-head"><div><p class="eyebrow">Sala</p><h2>${fresh ? `Hoy, ${escapeHtml(formatDate(actualChileDate))}` : 'La información de hoy todavía no está confirmada'}</h2></div><p>${fresh ? 'Sesiones cuyo inicio está registrado para la fecha de hoy en el servicio oficial.' : 'El snapshot disponible no corresponde al día chileno actual. Para evitar presentar información atrasada como “hoy”, ocultamos deliberadamente las sesiones antiguas de esta sección.'}</p></div>
        ${fresh ? (todayRows.length ? `<div class="today-sessions">${todayRows.map((row) => renderSession(row)).join('')}</div>` : '<div class="today-empty"><strong>No hay sesiones de Sala registradas para hoy en este snapshot.</strong><br>Esto no significa que no exista actividad parlamentaria: pueden realizarse comisiones, trabajo territorial u otras actuaciones fuera de Sala.</div>') : '<div class="today-empty"><strong>Snapshot desactualizado.</strong><br>Consulta la fuente oficial si necesitas confirmar una sesión antes de la próxima actualización automática.</div>'}
      </section>

      <section class="today-section">
        <div class="today-section-head"><div><p class="eyebrow">Próximamente</p><h2>Próximas sesiones registradas</h2></div><p>Hasta ocho sesiones posteriores incluidas por la API anual. Una programación futura puede cambiar; el estado oficial debe revisarse nuevamente cerca de la fecha.</p></div>
        ${upcoming.length ? `<div class="today-sessions">${upcoming.map((row) => renderSession(row, true)).join('')}</div>` : '<div class="today-empty">El servicio no devolvió próximas sesiones dentro de la ventana mostrada.</div>'}
      </section>

      ${recent.length ? `<section class="today-section"><div class="today-section-head"><div><p class="eyebrow">Contexto</p><h2>Sesiones recientes</h2></div><p>Las últimas sesiones anteriores registradas en el año. Para conocer decisiones concretas, usa el explorador de votaciones.</p></div><div class="today-sessions">${recent.map((row) => renderSession(row, true)).join('')}</div></section>` : ''}

      <div class="today-caveat"><strong>Qué muestra y qué no muestra:</strong> ${escapeHtml(data.scope_note || 'Este snapshot corresponde al calendario de sesiones de Sala.')} La tabla del Orden del Día, las citaciones de comisiones y otras actividades requieren fuentes adicionales y se incorporarán como capas distintas. <a href="${escapeHtml(sourceUrl)}" target="_blank" rel="noopener noreferrer">Abrir documentación oficial del servicio</a>.</div>`;
  };

  const init = async () => {
    root.innerHTML = '<div class="today-loading">Cargando snapshot oficial de Sala…</div>';
    try {
      const response = await fetch('data/legislative/2026/agenda/sala_snapshot.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      render(await response.json());
    } catch (error) {
      root.innerHTML = `<div class="today-error"><strong>La agenda diaria todavía no está disponible.</strong><br>El snapshot oficial no pudo cargarse (${escapeHtml(error.message)}). Esta vista no usará datos antiguos como sustituto silencioso.</div>`;
    }
  };

  init();
})();
