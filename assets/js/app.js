(() => {
  const districts = window.DISTRICTS || [];
  const profiles = window.PROFILES || {};

  const form = document.getElementById('location-form');
  const regionTrigger = document.getElementById('region-trigger');
  const communeTrigger = document.getElementById('commune-trigger');
  const regionValue = document.getElementById('region-value');
  const communeValue = document.getElementById('commune-value');
  const regionMenu = document.getElementById('region-options');
  const communeMenu = document.getElementById('commune-options');
  const communeHelp = document.getElementById('commune-help');
  const message = document.getElementById('search-message');
  const searchButton = document.getElementById('search-button');
  const results = document.getElementById('results');
  const districtSummary = document.getElementById('district-summary');
  const grid = document.getElementById('representatives-grid');
  const count = document.getElementById('representative-count');
  const selectionPanel = document.getElementById('selection-panel');

  const normalize = (value) => String(value || '')
    .toLocaleLowerCase('es-CL')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, '')
    .replace(/\s+/g, ' ')
    .trim();

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

  const REGION_ORDER = [
    { code: 'I', name: 'Tarapacá' },
    { code: 'II', name: 'Antofagasta' },
    { code: 'III', name: 'Atacama' },
    { code: 'IV', name: 'Coquimbo' },
    { code: 'V', name: 'Valparaíso' },
    { code: 'VI', name: "O'Higgins" },
    { code: 'VII', name: 'Maule' },
    { code: 'VIII', name: 'Biobío' },
    { code: 'IX', name: 'La Araucanía' },
    { code: 'X', name: 'Los Lagos' },
    { code: 'XI', name: 'Aysén' },
    { code: 'XII', name: 'Magallanes y de la Antártica Chilena' },
    { code: 'RM', name: 'Metropolitana de Santiago' },
    { code: 'XIV', name: 'Los Ríos' },
    { code: 'XV', name: 'Arica y Parinacota' },
    { code: 'XVI', name: 'Ñuble' }
  ];

  const availableRegions = new Set(districts.map((district) => district.region));
  const regions = REGION_ORDER
    .filter((region) => availableRegions.has(region.name))
    .map((region) => {
      const regionDistricts = districts.filter((district) => district.region === region.name);
      const communes = [...new Set(regionDistricts.flatMap((district) => district.comunas))]
        .sort((a, b) => a.localeCompare(b, 'es'));
      return { ...region, districts: regionDistricts, communes };
    });

  const communeIndex = new Map();
  districts.forEach((district) => {
    district.comunas.forEach((commune) => {
      communeIndex.set(normalize(commune), { district, commune });
    });
  });

  let selectedRegion = null;
  let selectedCommune = null;

  const closeMenu = (trigger, menu) => {
    menu.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
  };

  const openMenu = (trigger, menu) => {
    menu.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
  };

  const closeAllMenus = () => {
    closeMenu(regionTrigger, regionMenu);
    closeMenu(communeTrigger, communeMenu);
  };

  const resetResults = () => {
    results.hidden = true;
    selectionPanel.hidden = true;
    selectionPanel.innerHTML = '';
  };

  const updateSearchButton = () => {
    searchButton.disabled = !(selectedRegion && selectedCommune);
  };

  const initials = (name) => {
    const ignore = new Set(['de', 'del', 'la', 'las', 'los', 'y']);
    const words = name.split(/\s+/).filter((word) => !ignore.has(word.toLocaleLowerCase('es-CL')));
    return `${words[0]?.[0] || ''}${words[1]?.[0] || ''}`.toUpperCase();
  };

  const profileFor = (name, district) => {
    const profile = profiles[name] || {};
    return {
      ...profile,
      district: profile.district || district.id,
      region: profile.region || district.region,
      party: profile.party || 'Información partidaria en actualización'
    };
  };

  const legislativeUrl = (name, profile) => profile.id
    ? `ficha.html?id=${encodeURIComponent(profile.id)}`
    : `ficha.html?nombre=${encodeURIComponent(name)}`;

  const renderPortrait = (name, profile) => {
    const fallback = `<div class="avatar representative-fallback" aria-hidden="true">${escapeHtml(initials(name))}</div>`;
    if (!profile.photo) return fallback;
    return `
      <div class="representative-photo-wrap">
        <img class="representative-photo" src="${escapeHtml(profile.photo)}" alt="Fotografía de ${escapeHtml(name)}" loading="lazy">
        <div class="avatar representative-photo-fallback" aria-hidden="true">${escapeHtml(initials(name))}</div>
      </div>
    `;
  };

  const renderContact = (name, profile, commune) => {
    const actions = [];
    actions.push(`<a class="profile-contact-link is-primary" href="${escapeHtml(legislativeUrl(name, profile))}">Ver ficha legislativa</a>`);
    if (profile.email) {
      actions.push(`<a class="profile-contact-link" href="mailto:${escapeHtml(profile.email)}">Correo electrónico</a>`);
    }
    if (profile.phone) {
      actions.push(`<a class="profile-contact-link" href="tel:${escapeHtml(profile.phone)}">${escapeHtml(profile.phone)}</a>`);
    }
    if (profile.contactUrl || profile.profileUrl) {
      actions.push(`<a class="profile-contact-link" href="${escapeHtml(profile.contactUrl || profile.profileUrl)}" target="_blank" rel="noopener">Ver ficha oficial</a>`);
    }

    const contactText = actions.length
      ? `<div class="profile-contact-actions">${actions.join('')}</div>`
      : '<p class="profile-contact-note">El contacto oficial está siendo sincronizado desde la Cámara.</p>';

    return `
      <div class="selected-profile-head">
        ${renderPortrait(name, profile)}
        <div>
          <p class="eyebrow">Representante seleccionado</p>
          <strong>${escapeHtml(name)}</strong>
          <div class="selected-profile-meta">
            <span>Distrito ${escapeHtml(profile.district)}</span>
            <span>${escapeHtml(profile.region)}</span>
            <span>${escapeHtml(profile.party)}</span>
          </div>
        </div>
      </div>
      <div class="selected-profile-contact">
        <h3>Contacto oficial</h3>
        ${contactText}
        <p class="source-note">${escapeHtml(commune)} · Datos oficiales de la Cámara de Diputadas y Diputados.</p>
      </div>
    `;
  };

  const renderDistrict = (district, commune) => {
    const plural = district.parlamentarios.length === 1 ? 'representante' : 'representantes';
    districtSummary.innerHTML = `
      <div>
        <p class="eyebrow">Resultado para ${escapeHtml(commune)}</p>
        <h2>Tu comuna pertenece al Distrito ${escapeHtml(district.id)}</h2>
        <p>Región ${escapeHtml(district.region)}. En este distrito hay ${district.parlamentarios.length} ${plural} en la Cámara.</p>
      </div>
      <div class="district-number" aria-label="Distrito ${escapeHtml(district.id)}">
        <span>Distrito</span>
        <strong>${escapeHtml(district.id)}</strong>
      </div>
    `;

    count.textContent = `${district.parlamentarios.length} ${plural}`;
    grid.innerHTML = '';
    selectionPanel.hidden = true;
    selectionPanel.innerHTML = '';

    district.parlamentarios.forEach((name) => {
      const profile = profileFor(name, district);
      const card = document.createElement('article');
      card.className = 'representative-card';
      card.dataset.name = name;
      card.innerHTML = `
        ${renderPortrait(name, profile)}
        <div class="representative-card-body">
          <h3>${escapeHtml(name)}</h3>
          <div class="representative-meta">
            <span class="district-tag">Distrito ${escapeHtml(profile.district)}</span>
            <span class="party-badge">${escapeHtml(profile.party)}</span>
          </div>
          <button class="choose-btn" type="button">Elegir</button>
        </div>
      `;

      const image = card.querySelector('.representative-photo');
      if (image) {
        image.addEventListener('load', () => card.classList.add('photo-loaded'));
        image.addEventListener('error', () => {
          image.remove();
          card.classList.remove('photo-loaded');
        });
      }

      card.querySelector('.choose-btn').addEventListener('click', () => {
        grid.querySelectorAll('.representative-card').forEach((item) => item.classList.remove('is-selected'));
        card.classList.add('is-selected');
        localStorage.setItem('cap-selected', JSON.stringify({ name, district: district.id, commune }));
        selectionPanel.innerHTML = renderContact(name, profile, commune);
        selectionPanel.hidden = false;
        selectionPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });

      grid.appendChild(card);
    });

    results.hidden = false;
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const renderRegionMenu = () => {
    regionMenu.innerHTML = '';
    regions.forEach((region) => {
      const option = document.createElement('button');
      option.type = 'button';
      option.className = `selector-option${selectedRegion?.name === region.name ? ' is-selected' : ''}`;
      option.setAttribute('role', 'option');
      option.setAttribute('aria-selected', selectedRegion?.name === region.name ? 'true' : 'false');
      option.innerHTML = `<span class="region-code">${escapeHtml(region.code)}</span><span>${escapeHtml(region.name)}</span>`;
      option.addEventListener('click', () => selectRegion(region));
      regionMenu.appendChild(option);
    });
  };

  const renderCommuneMenu = () => {
    communeMenu.innerHTML = '';
    if (!selectedRegion) return;
    selectedRegion.communes.forEach((commune) => {
      const option = document.createElement('button');
      option.type = 'button';
      option.className = `selector-option${selectedCommune === commune ? ' is-selected' : ''}`;
      option.setAttribute('role', 'option');
      option.setAttribute('aria-selected', selectedCommune === commune ? 'true' : 'false');
      option.textContent = commune;
      option.addEventListener('click', () => selectCommune(commune));
      communeMenu.appendChild(option);
    });
  };

  const selectRegion = (region) => {
    selectedRegion = region;
    selectedCommune = null;
    regionValue.textContent = `${region.code} · ${region.name}`;
    regionValue.classList.remove('is-placeholder');
    communeTrigger.disabled = false;
    communeValue.textContent = 'Selecciona tu comuna';
    communeValue.classList.add('is-placeholder');
    communeHelp.textContent = `${region.communes.length} comunas disponibles en ${region.name}.`;
    message.textContent = '';
    resetResults();
    updateSearchButton();
    renderRegionMenu();
    renderCommuneMenu();
    closeAllMenus();
  };

  const selectCommune = (commune) => {
    selectedCommune = commune;
    communeValue.textContent = commune;
    communeValue.classList.remove('is-placeholder');
    message.textContent = '';
    resetResults();
    updateSearchButton();
    renderCommuneMenu();
    closeMenu(communeTrigger, communeMenu);
  };

  regionTrigger.addEventListener('click', () => {
    const isOpen = !regionMenu.hidden;
    closeAllMenus();
    if (!isOpen) {
      renderRegionMenu();
      openMenu(regionTrigger, regionMenu);
    }
  });

  communeTrigger.addEventListener('click', () => {
    if (!selectedRegion) return;
    const isOpen = !communeMenu.hidden;
    closeAllMenus();
    if (!isOpen) {
      renderCommuneMenu();
      openMenu(communeTrigger, communeMenu);
    }
  });

  document.addEventListener('click', (event) => {
    if (!event.target.closest('.selector-wrap')) closeAllMenus();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeAllMenus();
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    message.textContent = '';
    if (!selectedRegion) {
      message.textContent = 'Selecciona primero tu región.';
      renderRegionMenu();
      openMenu(regionTrigger, regionMenu);
      return;
    }
    if (!selectedCommune) {
      message.textContent = 'Selecciona tu comuna.';
      renderCommuneMenu();
      openMenu(communeTrigger, communeMenu);
      return;
    }
    const match = communeIndex.get(normalize(selectedCommune));
    if (!match || match.district.region !== selectedRegion.name) {
      message.textContent = 'No pudimos asociar esa comuna a un distrito.';
      return;
    }
    renderDistrict(match.district, match.commune);
  });

  const params = new URLSearchParams(window.location.search);
  const presetCommune = params.get('comuna');
  const presetRegion = params.get('region');
  if (presetCommune) {
    const match = communeIndex.get(normalize(presetCommune));
    if (match) {
      const region = regions.find((item) => item.name === match.district.region);
      if (region) {
        selectRegion(region);
        selectCommune(match.commune);
        renderDistrict(match.district, match.commune);
      }
    }
  } else if (presetRegion) {
    const query = normalize(presetRegion);
    const region = regions.find((item) => normalize(item.name) === query || normalize(item.code) === query);
    if (region) selectRegion(region);
  }

  renderRegionMenu();
  updateSearchButton();
})();
