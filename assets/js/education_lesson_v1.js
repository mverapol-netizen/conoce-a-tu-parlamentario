(() => {
  const data = window.CONGRESS_EDUCATION;
  const root = document.getElementById('edu-lesson-root');
  if (!data || !root) return;

  const params = new URLSearchParams(window.location.search);
  const lessonId = params.get('id');
  const conceptSlug = params.get('concepto');
  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const unitById = new Map(data.units.map((u) => [u.id, u]));
  const statusLabel = (status) => ({ research: 'Investigación en curso', planned: 'Planificada', design: 'En diseño', ready: 'Lista para revisión editorial' }[status] || 'En preparación');
  const typeLabel = (type) => ({
    intuition: 'Intuición', institution: 'Institución', evidence: 'Evidencia', debate: 'Debate', history: 'Historia', myth: 'Mito frecuente'
  }[type] || type || 'Contenido');

  const renderSourceRefs = (ids = []) => {
    const valid = ids.map((id) => data.sources?.[id]).filter(Boolean);
    if (!valid.length) return '';
    return `<div class="edu-source-list">${valid.map((source) => `<a class="edu-source" href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer"><strong>${escapeHtml(source.label)}</strong><small>${escapeHtml(source.publisher)}</small></a>`).join('')}</div>`;
  };

  const renderBlock = (block) => {
    const paragraphs = (block.paragraphs || []).map((text) => `<p>${text}</p>`).join('');
    const bullets = (block.bullets || []).length ? `<ul>${block.bullets.map((item) => `<li>${item}</li>`).join('')}</ul>` : '';
    return `<section class="edu-block">
      <span class="edu-epistemic-tag">${escapeHtml(typeLabel(block.type))}</span>
      <h2>${escapeHtml(block.title)}</h2>
      ${paragraphs}${bullets}${renderSourceRefs(block.sourceIds)}
    </section>`;
  };

  const renderSources = (ids = []) => {
    const valid = ids.map((id) => data.sources?.[id]).filter(Boolean);
    if (!valid.length) return '';
    return `<section class="edu-block">
      <h2>Fuentes y profundización</h2>
      <p>La página distingue entre fuentes normativas, institucionales y académicas. Los enlaces abren la fuente original para que la explicación sea auditable.</p>
      <div class="edu-source-list">${valid.map((source) => `<a class="edu-source" href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer"><strong>${escapeHtml(source.label)}</strong><small>${escapeHtml(source.publisher)} · ${escapeHtml(source.note || '')}</small></a>`).join('')}</div>
    </section>`;
  };

  const renderPlaceholderStack = () => `
    <div class="edu-content-stack">
      <section class="edu-block edu-placeholder"><span class="edu-epistemic-tag">Intuición</span><h2>La puerta de entrada</h2><p>Este bloque alojará una explicación breve que sea correcta desde el primer nivel y que pueda precisarse después sin tener que desmentirla.</p></section>
      <section class="edu-block edu-placeholder"><span class="edu-epistemic-tag">Institución</span><h2>Cómo funciona realmente en Chile</h2><p>Constitución, Ley Orgánica, reglamentos, procedimientos, excepciones y diferencias institucionales relevantes.</p></section>
      <section class="edu-block edu-placeholder"><span class="edu-epistemic-tag">Caso real</span><h2>Míralo funcionando</h2><p>La explicación se conectará con una comisión, proyecto, votación, distrito, bancada u otra instancia real de los datos del sitio cuando corresponda.</p></section>
      <section class="edu-block edu-placeholder"><span class="edu-epistemic-tag">Mito frecuente</span><h2>Qué significa y qué no significa</h2><p>Aquí se bloquearán las inferencias intuitivas más frecuentes antes de que el usuario avance a interpretaciones más complejas.</p></section>
      <section class="edu-block edu-placeholder"><span class="edu-epistemic-tag">Historia</span><h2>¿Siempre funcionó así?</h2><p>La institución se situará históricamente y enlazará con la cronología general del Congreso.</p></section>
      <section class="edu-block edu-placeholder"><span class="edu-epistemic-tag">Evidencia</span><h2>Qué sabemos empíricamente</h2><p>Resultados relevantes de ciencia política, derecho, historia o datos legislativos, distinguidos de la descripción institucional.</p></section>
      <section class="edu-block edu-placeholder"><span class="edu-epistemic-tag">Debate</span><h2>Qué discuten los especialistas</h2><p>Consensos, hipótesis rivales y controversias que no deben presentarse como hechos institucionales cerrados.</p></section>
      <section class="edu-block edu-placeholder"><h2>Fuentes y profundización</h2><p>La versión publicable incluirá fuentes normativas, institucionales y académicas, fecha de revisión y trazabilidad editorial.</p></section>
    </div>`;

  const renderLesson = (id) => {
    const lesson = data.lessons[id];
    if (!lesson) return false;
    const unit = unitById.get(lesson.unit);
    document.title = `${lesson.title} · Entiende el Congreso`;

    const keyPoints = lesson.keyPoints?.length ? `<section class="edu-block"><h2>En pocas palabras</h2><div class="edu-key-points">${lesson.keyPoints.map((item) => `<div class="edu-key-point">${item}</div>`).join('')}</div></section>` : '';
    const richContent = lesson.blocks?.length
      ? `<div class="edu-content-stack">${keyPoints}${lesson.blocks.map(renderBlock).join('')}${renderSources(lesson.sourceIds)}</div>`
      : renderPlaceholderStack();

    root.innerHTML = `
      <nav class="edu-breadcrumb" aria-label="Migas de pan">
        <a href="entender.html">Entiende el Congreso</a><span>›</span><span>${escapeHtml(unit?.title || '')}</span><span>›</span><strong>${escapeHtml(lesson.title)}</strong>
      </nav>
      <article class="edu-lesson-hero">
        <div class="edu-lesson-meta">
          <span class="edu-unit-pill">${escapeHtml(unit?.letter || '')} · ${escapeHtml(unit?.title || '')}</span>
          <span class="edu-status-pill">${escapeHtml(statusLabel(lesson.status))}</span>
          ${lesson.readingTime ? `<span class="edu-reading-time">Lectura orientativa: ${escapeHtml(lesson.readingTime)}</span>` : ''}
        </div>
        <h1>${escapeHtml(lesson.title)}</h1>
        <p class="edu-lesson-intro">${escapeHtml(lesson.intro)}</p>
      </article>
      ${richContent}`;

    window.EDUCATION_GLOSSARY?.enhance(root);
    return true;
  };

  const renderConcept = (slug) => {
    const concept = data.glossary.find((item) => item.slug === slug);
    if (!concept) return false;
    const unit = unitById.get(concept.unit);
    document.title = `${concept.term} · Entiende el Congreso`;
    root.innerHTML = `
      <nav class="edu-breadcrumb" aria-label="Migas de pan">
        <a href="entender.html">Entiende el Congreso</a><span>›</span><span>Glosario contextual</span><span>›</span><strong>${escapeHtml(concept.term)}</strong>
      </nav>
      <article class="edu-lesson-hero">
        <div class="edu-lesson-meta"><span class="edu-unit-pill">${escapeHtml(unit?.letter || '')} · ${escapeHtml(unit?.title || '')}</span><span class="edu-status-pill">Definición v0.1</span></div>
        <h1>${escapeHtml(concept.term)}</h1>
        <p class="edu-lesson-intro">${escapeHtml(concept.short)}</p>
      </article>
      <div class="edu-content-stack">
        <section class="edu-block edu-placeholder"><h2>Qué es</h2><p>Esta definición breve será ampliada con la regla institucional precisa y el contexto en que aparece en el trabajo parlamentario.</p></section>
        <section class="edu-block edu-placeholder"><span class="edu-epistemic-tag">Mito frecuente</span><h2>Qué no significa</h2><p>La versión cerrada identificará las confusiones más frecuentes asociadas a este término.</p></section>
        <section class="edu-block edu-placeholder"><h2>Ver un ejemplo real</h2><p>Cuando exista una instancia disponible en la base pública, este bloque llevará directamente a ella.</p></section>
      </div>`;
    return true;
  };

  const rendered = conceptSlug ? renderConcept(conceptSlug) : renderLesson(lessonId || 'para-que-existe');
  if (!rendered) {
    root.innerHTML = '<div class="edu-empty"><strong>No encontramos esa entrada.</strong><br>Vuelve al hub de Entiende el Congreso para explorar las lecciones disponibles.</div>';
  }
})();
