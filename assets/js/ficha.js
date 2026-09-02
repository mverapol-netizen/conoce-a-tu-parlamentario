(() => {
  const profiles = window.PROFILES || {};
  const container = document.getElementById('legislative-profile');
  const shell = document.getElementById('legislative-shell');
  const error = document.getElementById('profile-error');

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

  const normalize = (value) => String(value || '')
    .toLocaleLowerCase('es-CL')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  const requestedName = params.get('nombre');

  const entry = Object.entries(profiles).find(([name, profile]) => {
    if (id && String(profile.id) === String(id)) return true;
    if (requestedName && normalize(name) === normalize(requestedName)) return true;
    return false;
  });

  if (!entry) {
    container.hidden = true;
    shell.hidden = true;
    error.hidden = false;
    return;
  }

  const [name, profile] = entry;
  document.title = `${name} · Ficha legislativa`;

  const affiliation = profile.affiliationLabel || profile.party || 'Afiliación en actualización';
  const caucus = profile.caucus || 'Bancada por confirmar';
  const portrait = profile.photo
    ? `<img class="legislative-photo" src="${escapeHtml(profile.photo)}" alt="Fotografía de ${escapeHtml(name)}">`
    : `<div class="legislative-photo-fallback" aria-hidden="true"></div>`;

  container.innerHTML = `
    <div class="legislative-profile-grid">
      <div class="legislative-photo-frame">${portrait}</div>
      <div class="legislative-identity">
        <p class="eyebrow">Ficha legislativa</p>
        <h1>${escapeHtml(name)}</h1>
        <div class="legislative-tags">
          <span>Distrito ${escapeHtml(profile.district)}</span>
          <span>${escapeHtml(profile.region || '')}</span>
          <span>${escapeHtml(affiliation)}</span>
        </div>
        <p class="legislative-caucus">${escapeHtml(caucus)}</p>
        <div class="legislative-actions">
          ${profile.email ? `<a href="mailto:${escapeHtml(profile.email)}">Correo oficial</a>` : ''}
          ${profile.profileUrl ? `<a href="${escapeHtml(profile.profileUrl)}" target="_blank" rel="noopener">Ficha oficial de la Cámara</a>` : ''}
        </div>
      </div>
    </div>
  `;

  const image = container.querySelector('.legislative-photo');
  if (image) {
    image.addEventListener('error', () => {
      image.parentElement.innerHTML = '<div class="legislative-photo-fallback" aria-hidden="true"></div>';
    });
  }

  shell.hidden = false;
})();
