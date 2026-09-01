(() => {
  const districts = window.DISTRICTS || [];

  const form = document.getElementById('location-form');
  const regionInput = document.getElementById('region-input');
  const communeInput = document.getElementById('commune-input');
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

  const REGION_ORDER = [
    { code: 'I', name: 'Tarapacá', aliases: ['primera region', 'region de tarapaca', '1'] },
    { code: 'II', name: 'Antofagasta', aliases: ['segunda region', 'region de antofagasta', '2'] },
    { code: 'III', name: 'Atacama', aliases: ['tercera region', 'region de atacama', '3'] },
    { code: 'IV', name: 'Coquimbo', aliases: ['cuarta region', 'region de coquimbo', '4'] },
    { code: 'V', name: 'Valparaíso', aliases: ['quinta region', 'region de valparaiso', '5'] },
    { code: 'VI', name: "O'Higgins", aliases: ['sexta region', 'region de ohiggins', 'ohiggins', '6'] },
    { code: 'VII', name: 'Maule', aliases: ['septima region', 'region del maule', '7'] },
    { code: 'VIII', name: 'Biobío', aliases: ['octava region', 'region del biobio', 'biobio', '8'] },
    { code: 'IX', name: 'La Araucanía', aliases: ['novena region', 'region de la araucania', 'araucania', '9'] },
    { code: 'X', name: 'Los Lagos', aliases: ['decima region', 'region de los lagos', '10'] },
    { code: 'XI', name: 'Aysén', aliases: ['undecima region', 'region de aysen', 'aysen', '11'] },
    { code: 'XII', name: 'Magallanes y de la Antártica Chilena', aliases: ['duodecima region', 'magallanes', 'antartica', '12'] },
    { code: 'RM', name: 'Metropolitana de Santiago', aliases: ['region metropolitana', 'metropolitana', 'rm', 'santiago', '13'] },
    { code: 'XIV', name: 'Los Ríos', aliases: ['region de los rios', 'los rios', '14'] },
    { code: 'XV', name: 'Arica y Parinacota', aliases: ['region de arica y parinacota', 'arica', 'parinacota', '15'] },
    { code: 'XVI', name: 'Ñuble', aliases: ['region de nuble', 'nuble', '16'] }
  ];

  const availableRegionNames = new Set(districts.map((district) => district.region));
  const regionEntries = REGION_ORDER
    .filter((region) => availableRegionNames.has(region.name))
    .map((region) => {
      const regionDistricts = districts.filter((district) => district.region === region.name);
      const communes = [...new Set(regionDistricts.flatMap((district) => district.comunas))]
        .sort((a, b) => a.localeCompare(b, 'es'));
      const searchTerms = [region.name, region.code, ...region.aliases].map(normalize);
      return { ...region, districts: regionDistricts, communes, searchTerms };
    });

  const communeGlobalIndex = new Map();
  districts.forEach((district) => {
    district.comunas.forEach((commune) => {
      communeGlobalIndex.set(normalize(commune), { district, commune });
    });
  });

  let selectedRegion = null;
  let selectedCommune = null;
  let regionMatches = [];
  let communeMatches = [];
  let regionActive = -1;
  let communeActive = -1;

  const closeMenu = (input, menu) => {
    menu.hidden = true;
    input.setAttribute('aria-expanded', 'false');
    input.removeAttribute('aria-activedescendant');
  };

  const openMenu = (input, menu) => {
    menu.hidden = false;
    input.setAttribute('aria-expanded', 'true');
  };

  const updateSearchButton = () => {
    searchButton.disabled = !(selectedRegion && selectedCommune);
  };

  const resetResults = () => {
    results.hidden = true;
    selectionPanel.hidden = true;
    selectionPanel.innerHTML = '';
  };

  const initials = (name) => {
    const ignore = new Set(['de', 'del', 'la', 'las', 'los', 'y']);
    const words = name.split(/\s+/).filter((word) => !ignore.has(word.toLocaleLowerCase('es-CL')));
    return `${words[0]?.[0] || ''}${words[1]?.[0] || ''}`.toUpperCase();
  };

  const renderDistrict = (district, commune) => {
    const plural = district.parlamentarios.length === 1 ? 'representante' : 'representantes';
    districtSummary.innerHTML = `
      <div>
        <p class="eyebrow">Resultado para ${commune}</p>
        <h2>Tu comuna pertenece al Distrito ${district.id}</h2>
        <p>Región ${district.region}. En este distrito hay ${district.parlamentarios.length} ${plural} en la Cámara.</p>
      </div>
      <div class="district-number" aria-label="Distrito ${district.id}">
        <span>Distrito</span>
        <strong>${district.id}</strong>
      </div>
    `;

    count.textContent = `${district.parlamentarios.length} ${plural}`;
    grid.innerHTML = '';
    selectionPanel.hidden = true;
    selectionPanel.innerHTML = '';

    district.parlamentarios.forEach((name) => {
      const card = document.createElement('article');
      card.className = 'representative-card';
      card.dataset.name = name;
      card.innerHTML = `
        <div class="avatar" aria-hidden="true">${initials(name)}</div>
        <h3>${name}</h3>
        <p class="role">Diputada/o · Distrito ${district.id}</p>
        <button class="choose-btn" type="button">Elegir</button>
      `;

      card.querySelector('button').addEventListener('click', () => {
        grid.querySelectorAll('.representative-card').forEach((item) => item.classList.remove('is-selected'));
        card.classList.add('is-selected');
        localStorage.setItem('cap-selected', JSON.stringify({ name, district: district.id, commune }));
        selectionPanel.innerHTML = `
          <strong>Elegiste a ${name}</strong>
          <p>Distrito ${district.id} · ${commune}. La siguiente etapa del proyecto puede abrir aquí su ficha parlamentaria completa.</p>
        `;
        selectionPanel.hidden = false;
        selectionPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });

      grid.appendChild(card);
    });

    results.hidden = false;
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const regionLabel = (region) => `${region.code} · ${region.name}`;

  const regionMatchesQuery = (query) => {
    if (!query) return regionEntries;
    return regionEntries.filter((region) => region.searchTerms.some((term) => term.includes(query)));
  };

  const communeMatchesQuery = (query) => {
    if (!selectedRegion) return [];
    if (!query) return selectedRegion.communes;
    return selectedRegion.communes
      .filter((commune) => normalize(commune).includes(query))
      .sort((a, b) => {
        const aStarts = normalize(a).startsWith(query) ? 0 : 1;
        const bStarts = normalize(b).startsWith(query) ? 0 : 1;
        return aStarts - bStarts || a.localeCompare(b, 'es');
      });
  };

  const renderRegionMenu = (query = normalize(regionInput.value)) => {
    regionMatches = regionMatchesQuery(query);
    regionActive = -1;
    regionMenu.innerHTML = '';

    if (!regionMatches.length) {
      regionMenu.innerHTML = '<div class="autocomplete-empty">No encontramos una región con ese texto.</div>';
      openMenu(regionInput, regionMenu);
      return;
    }

    regionMatches.forEach((region, index) => {
      const option = document.createElement('button');
      option.type = 'button';
      option.className = 'autocomplete-option region-option';
      option.id = `region-option-${index}`;
      option.setAttribute('role', 'option');
      option.innerHTML = `<span class="region-code">${region.code}</span><span>${region.name}</span>`;
      option.addEventListener('click', () => selectRegion(region));
      regionMenu.appendChild(option);
    });

    openMenu(regionInput, regionMenu);
  };

  const renderCommuneMenu = (query = normalize(communeInput.value)) => {
    communeMatches = communeMatchesQuery(query);
    communeActive = -1;
    communeMenu.innerHTML = '';

    if (!communeMatches.length) {
      communeMenu.innerHTML = '<div class="autocomplete-empty">No hay comunas que coincidan dentro de esta región.</div>';
      openMenu(communeInput, communeMenu);
      return;
    }

    communeMatches.forEach((commune, index) => {
      const option = document.createElement('button');
      option.type = 'button';
      option.className = 'autocomplete-option';
      option.id = `commune-option-${index}`;
      option.setAttribute('role', 'option');
      option.textContent = commune;
      option.addEventListener('click', () => selectCommune(commune));
      communeMenu.appendChild(option);
    });

    openMenu(communeInput, communeMenu);
  };

  const selectRegion = (region, { focusCommune = true } = {}) => {
    selectedRegion = region;
    selectedCommune = null;
    regionInput.value = regionLabel(region);
    regionInput.setAttribute('aria-invalid', 'false');
    closeMenu(regionInput, regionMenu);

    communeInput.disabled = false;
    communeInput.value = '';
    communeInput.placeholder = 'Ej.: Macul, Maipú, Santiago…';
    communeInput.setAttribute('aria-invalid', 'false');
    communeHelp.textContent = `${region.communes.length} comunas disponibles en ${region.name}.`;
    message.textContent = '';
    resetResults();
    updateSearchButton();

    if (focusCommune) {
      communeInput.focus();
      renderCommuneMenu('');
    }
  };

  const selectCommune = (commune) => {
    selectedCommune = commune;
    communeInput.value = commune;
    communeInput.setAttribute('aria-invalid', 'false');
    closeMenu(communeInput, communeMenu);
    message.textContent = '';
    resetResults();
    updateSearchButton();
  };

  const findExactRegion = (value) => {
    const query = normalize(value);
    if (!query) return null;
    return regionEntries.find((region) => region.searchTerms.includes(query) || normalize(regionLabel(region)) === query) || null;
  };

  const findExactCommune = (value) => {
    if (!selectedRegion) return null;
    const query = normalize(value);
    return selectedRegion.communes.find((commune) => normalize(commune) === query) || null;
  };

  const setActiveOption = (type, nextIndex) => {
    const isRegion = type === 'region';
    const menu = isRegion ? regionMenu : communeMenu;
    const input = isRegion ? regionInput : communeInput;
    const matches = isRegion ? regionMatches : communeMatches;
    if (!matches.length) return;

    const max = matches.length - 1;
    const index = Math.max(0, Math.min(nextIndex, max));
    const buttons = [...menu.querySelectorAll('.autocomplete-option')];
    buttons.forEach((button) => button.classList.remove('is-active'));
    const activeButton = buttons[index];
    if (activeButton) {
      activeButton.classList.add('is-active');
      activeButton.scrollIntoView({ block: 'nearest' });
      input.setAttribute('aria-activedescendant', activeButton.id);
    }

    if (isRegion) regionActive = index;
    else communeActive = index;
  };

  const handleComboKeydown = (event, type) => {
    const isRegion = type === 'region';
    const input = isRegion ? regionInput : communeInput;
    const menu = isRegion ? regionMenu : communeMenu;
    const matches = isRegion ? regionMatches : communeMatches;
    const active = isRegion ? regionActive : communeActive;
    const renderMenu = isRegion ? renderRegionMenu : renderCommuneMenu;

    if (event.key === 'ArrowDown') {
      event.preventDefault();
      if (menu.hidden) renderMenu(normalize(input.value));
      setActiveOption(type, active < 0 ? 0 : active + 1);
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      if (menu.hidden) renderMenu(normalize(input.value));
      setActiveOption(type, active < 0 ? matches.length - 1 : active - 1);
    } else if (event.key === 'Enter' && !menu.hidden && active >= 0) {
      event.preventDefault();
      if (isRegion) selectRegion(matches[active]);
      else selectCommune(matches[active]);
    } else if (event.key === 'Escape') {
      closeMenu(input, menu);
    }
  };

  regionInput.addEventListener('focus', () => renderRegionMenu(normalize(regionInput.value)));
  regionInput.addEventListener('input', () => {
    const exact = findExactRegion(regionInput.value);

    if (exact) {
      selectRegion(exact, { focusCommune: false });
      return;
    }

    selectedRegion = null;
    selectedCommune = null;
    communeInput.value = '';
    communeInput.disabled = true;
    communeInput.placeholder = 'Primero selecciona tu región';
    communeHelp.textContent = 'Las comunas se filtrarán según tu región.';
    resetResults();
    updateSearchButton();
    renderRegionMenu(normalize(regionInput.value));
  });
  regionInput.addEventListener('keydown', (event) => handleComboKeydown(event, 'region'));

  communeInput.addEventListener('focus', () => {
    if (selectedRegion) renderCommuneMenu(normalize(communeInput.value));
  });
  communeInput.addEventListener('input', () => {
    const exact = findExactCommune(communeInput.value);
    selectedCommune = exact || null;
    resetResults();
    updateSearchButton();
    renderCommuneMenu(normalize(communeInput.value));
  });
  communeInput.addEventListener('keydown', (event) => handleComboKeydown(event, 'commune'));

  document.addEventListener('click', (event) => {
    if (!event.target.closest('.filter-field')) {
      closeMenu(regionInput, regionMenu);
      closeMenu(communeInput, communeMenu);
    }
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    message.textContent = '';

    const exactRegion = selectedRegion || findExactRegion(regionInput.value);
    if (!exactRegion) {
      regionInput.setAttribute('aria-invalid', 'true');
      message.textContent = 'Selecciona una región válida para continuar.';
      regionInput.focus();
      renderRegionMenu(normalize(regionInput.value));
      return;
    }

    if (!selectedRegion) selectRegion(exactRegion, { focusCommune: false });

    const exactCommune = selectedCommune || findExactCommune(communeInput.value);
    if (!exactCommune) {
      communeInput.setAttribute('aria-invalid', 'true');
      message.textContent = 'Selecciona una comuna de la región elegida.';
      communeInput.focus();
      renderCommuneMenu(normalize(communeInput.value));
      return;
    }

    selectCommune(exactCommune);
    const match = communeGlobalIndex.get(normalize(exactCommune));
    if (!match || match.district.region !== selectedRegion.name) {
      message.textContent = 'No pudimos asociar esa comuna a un distrito. Intenta nuevamente.';
      return;
    }

    renderDistrict(match.district, match.commune);
  });

  const params = new URLSearchParams(window.location.search);
  const presetCommune = params.get('comuna');
  const presetRegion = params.get('region');

  if (presetCommune) {
    const globalMatch = communeGlobalIndex.get(normalize(presetCommune));
    if (globalMatch) {
      const region = regionEntries.find((entry) => entry.name === globalMatch.district.region);
      if (region) {
        selectRegion(region, { focusCommune: false });
        selectCommune(globalMatch.commune);
        renderDistrict(globalMatch.district, globalMatch.commune);
      }
    }
  } else if (presetRegion) {
    const region = findExactRegion(presetRegion) || regionMatchesQuery(normalize(presetRegion))[0];
    if (region) selectRegion(region, { focusCommune: false });
  }
})();
