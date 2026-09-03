(() => {
  const data = window.CONGRESS_EDUCATION;
  const root = document.getElementById('edu-lesson-root');
  if (!data || !root) return;

  const params = new URLSearchParams(window.location.search);
  const currentId = params.get('id');
  if (!currentId || !data.lessons[currentId]) return;

  const path = data.learningPath.filter((id) => data.lessons[id]);
  const index = path.indexOf(currentId);
  if (index < 0) return;

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  const prevId = index > 0 ? path[index - 1] : null;
  const nextId = index < path.length - 1 ? path[index + 1] : null;
  const nav = document.createElement('nav');
  nav.className = 'edu-progress-nav';
  nav.setAttribute('aria-label', 'Recorrido de aprendizaje');

  const previous = prevId ? `<a class="edu-progress-link edu-progress-prev" href="aprender.html?id=${encodeURIComponent(prevId)}"><small>← Anterior</small><strong>${escapeHtml(data.lessons[prevId].title)}</strong></a>` : '<span></span>';
  const next = nextId ? `<a class="edu-progress-link edu-progress-next" href="aprender.html?id=${encodeURIComponent(nextId)}"><small>Siguiente →</small><strong>${escapeHtml(data.lessons[nextId].title)}</strong></a>` : '<a class="edu-progress-link edu-progress-next" href="entender.html"><small>Recorrido completado</small><strong>Volver a Entiende el Congreso</strong></a>';

  nav.innerHTML = `<div class="edu-progress-status"><span>Paso ${index + 1} de ${path.length}</span><div class="edu-progress-track" aria-hidden="true"><span style="width:${((index + 1) / path.length * 100).toFixed(1)}%"></span></div></div><div class="edu-progress-links">${previous}${next}</div>`;
  root.appendChild(nav);
})();
