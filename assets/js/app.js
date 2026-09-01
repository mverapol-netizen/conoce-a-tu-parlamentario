(() => {
  const districts = window.DISTRICTS || [];
  const form = document.getElementById('commune-form');
  const input = document.getElementById('commune-input');
  const dataList = document.getElementById('communes-list');
  const message = document.getElementById('search-message');
  const results = document.getElementById('results');
  const districtSummary = document.getElementById('district-summary');
  const grid = document.getElementById('representatives-grid');
  const count = document.getElementById('representative-count');
  const selectionPanel = document.getElementById('selection-panel');

  const normalize = (value) => value
    .toLocaleLowerCase('es-CL')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s'-]/g, '')
    .replace(/\s+/g, ' ')
    .trim();

  const communeIndex = new Map();
  const communeNames = [];

  districts.forEach((district) => {
    district.comunas.forEach((commune) => {
      communeIndex.set(normalize(commune), { district, commune });
      communeNames.push(commune);
    });
  });

  communeNames
    .sort((a, b) => a.localeCompare(b, 'es'))
    .forEach((commune) => {
      const option = document.createElement('option');
      option.value = commune;
      dataList.appendChild(option);
    });

  const initials = (name) => {
    const ignore = new Set(['de', 'del', 'la', 'las', 'los', 'y']);
    const words = name.split(/\s+/).filter((word) => !ignore.has(word.toLocaleLowerCase('es-CL')));
    return `${words[0]?.[0] || ''}${words[1]?.[0] || ''}`.toUpperCase();
  };

  const distance = (a, b) => {
    const matrix = Array.from({ length: b.length + 1 }, (_, i) => [i]);
    for (let j = 0; j <= a.length; j += 1) matrix[0][j] = j;
    for (let i = 1; i <= b.length; i += 1) {
      for (let j = 1; j <= a.length; j += 1) {
        matrix[i][j] = b[i - 1] === a[j - 1]
          ? matrix[i - 1][j - 1]
          : Math.min(matrix[i - 1][j - 1] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j] + 1);
      }
    }
    return matrix[b.length][a.length];
  };

  const suggest = (query) => {
    if (!query) return [];
    return communeNames
      .map((name) => ({ name, score: distance(normalize(name), query) }))
      .sort((a, b) => a.score - b.score || a.name.localeCompare(b.name, 'es'))
      .slice(0, 3)
      .filter((item) => item.score <= Math.max(3, Math.ceil(query.length * 0.35)))
      .map((item) => item.name);
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

  const search = () => {
    const query = normalize(input.value);
    message.textContent = '';
    if (!query) {
      message.textContent = 'Escribe una comuna para continuar.';
      input.focus();
      return;
    }

    const match = communeIndex.get(query);
    if (!match) {
      const options = suggest(query);
      message.textContent = options.length
        ? `No encontramos esa comuna. ¿Quisiste decir: ${options.join(', ')}?`
        : 'No encontramos esa comuna. Revisa la escritura e inténtalo nuevamente.';
      results.hidden = true;
      return;
    }

    input.value = match.commune;
    renderDistrict(match.district, match.commune);
  };

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    search();
  });

  // Permite abrir el sitio ya enfocado en una comuna: ?comuna=Maipu
  const params = new URLSearchParams(window.location.search);
  const preset = params.get('comuna');
  if (preset) {
    input.value = preset;
    search();
  }
})();
