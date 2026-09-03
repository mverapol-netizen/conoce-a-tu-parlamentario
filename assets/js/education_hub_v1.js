(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  const els = {
    questions: document.getElementById('edu-questions'),
    units: document.getElementById('edu-units'),
    path: document.getElementById('edu-path'),
    search: document.getElementById('edu-search'),
    results: document.getElementById('edu-search-results'),
    epistemic: document.getElementById('edu-epistemic')
  };

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  const normalize = (value) => String(value || '')
    .toLocaleLowerCase('es-CL')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();

  const unitById = new Map(data.units.map((u) => [u.id, u]));
  const statusLabel = (status) => ({ research: 'Investigación abierta', planned: 'Planificada', design: 'En diseño', ready: 'Lista' }[status] || 'En preparación');

  const renderQuestions = () => {
    if (!els.questions) return;
    els.questions.innerHTML = data.featuredQuestions.map((q) => {
      const unit = unitById.get(q.unit);
      return `<a class="edu-question-card" href="aprender.html?id=${encodeURIComponent(q.id)}">
        <span class="edu-unit-pill">${escapeHtml(unit?.letter || '')} · ${escapeHtml(unit?.title || '')}</span>
        <h3>${escapeHtml(q.title)}</h3>
        <p>${escapeHtml(q.summary)}</p>
        <div class="edu-card-meta"><span></span><span class="edu-status-pill">${escapeHtml(statusLabel(q.status))}</span></div>
      </a>`;
    }).join('');
  };

  const renderUnits = () => {
    if (!els.units) return;
    els.units.innerHTML = data.units.map((unit) => `<article class="edu-unit-card">
      <span class="edu-unit-letter">${escapeHtml(unit.letter)}</span>
      <h3>${escapeHtml(unit.title)}</h3>
      <p>${escapeHtml(unit.summary)}</p>
    </article>`).join('');
  };

  const renderPath = () => {
    if (!els.path) return;
    els.path.innerHTML = data.learningPath.map((id, index) => {
      const lesson = data.lessons[id];
      if (!lesson) return '';
      return `<li><span class="edu-path-number">${index + 1}</span><a href="aprender.html?id=${encodeURIComponent(id)}">${escapeHtml(lesson.title)}</a></li>`;
    }).join('');
  };

  const renderEpistemic = () => {
    if (!els.epistemic) return;
    els.epistemic.innerHTML = Object.values(data.epistemicTypes).map((item) => `<article class="edu-epistemic-card">
      <span class="edu-epistemic-tag">${escapeHtml(item.label)}</span>
      <p>${escapeHtml(item.description)}</p>
    </article>`).join('');
  };

  const searchableRecords = [
    ...data.featuredQuestions.map((q) => ({ type: 'Pregunta', title: q.title, text: q.summary, href: `aprender.html?id=${q.id}` })),
    ...Object.entries(data.lessons).map(([id, lesson]) => ({ type: 'Lección', title: lesson.title, text: lesson.intro, href: `aprender.html?id=${id}` })),
    ...data.glossary.map((g) => ({ type: 'Concepto', title: g.term, text: g.short, href: `aprender.html?concepto=${g.slug}` }))
  ];

  const renderSearch = () => {
    if (!els.search || !els.results) return;
    const term = normalize(els.search.value);
    if (!term) {
      els.results.innerHTML = '<div class="edu-empty">Prueba con <strong>comisión mixta</strong>, <strong>urgencia</strong>, <strong>qué hace un diputado</strong> o <strong>bancada</strong>.</div>';
      return;
    }
    const matches = searchableRecords
      .map((item) => ({ ...item, haystack: normalize(`${item.title} ${item.text}`) }))
      .filter((item) => item.haystack.includes(term))
      .slice(0, 8);

    els.results.innerHTML = matches.length ? matches.map((item) => `<a class="edu-glossary-item" href="${escapeHtml(item.href)}">
      <strong>${escapeHtml(item.title)} <span class="edu-status-pill">${escapeHtml(item.type)}</span></strong>
      <p>${escapeHtml(item.text)}</p>
    </a>`).join('') : `<div class="edu-empty">Todavía no tenemos una entrada estructurada para <strong>${escapeHtml(els.search.value)}</strong>. La búsqueda crecerá a medida que cerremos el glosario y los dossiers.</div>`;
  };

  els.search?.addEventListener('input', renderSearch);
  renderQuestions();
  renderUnits();
  renderPath();
  renderEpistemic();
  renderSearch();
})();
