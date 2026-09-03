(() => {
  const svg = document.getElementById('wn-chart');
  const view2 = document.getElementById('wn-view-2d');
  const visibleCount = document.getElementById('wn-visible-count');
  const showAll = document.getElementById('wn-show-all');
  const chartCard = document.querySelector('.wn-chart-card');
  const chartDescription = document.getElementById('wn-chart-description');

  const mainNav = document.querySelector('.site-tabs');
  if (mainNav && !mainNav.querySelector('a[href="entender.html"]')) {
    const educationLink = document.createElement('a');
    educationLink.className = 'site-tab';
    educationLink.href = 'entender.html';
    educationLink.textContent = 'Entiende el Congreso';
    mainNav.appendChild(educationLink);
  }

  if (!svg || !view2 || !visibleCount || !showAll || !chartCard) return;

  const densityNote = document.createElement('p');
  densityNote.className = 'wn-density-note';
  densityNote.textContent = 'Para evitar una nube ilegible, cuando se muestran muchos casos en 2D los nombres se consultan mediante hover o clic en lugar de rotular todos los puntos simultáneamente.';
  chartDescription?.insertAdjacentElement('afterend', densityNote);

  const normalizeShowAllLabel = () => {
    const text = showAll.textContent || '';
    if (/^Ver los \d+ estimados$/i.test(text.trim())) {
      const count = text.match(/\d+/)?.[0] || '154';
      showAll.textContent = `Ver lista completa (${count})`;
      showAll.setAttribute('aria-label', `Ver lista completa de ${count} integrantes estimados; no representa un ranking de desempeño`);
    } else if (/^Volver a selección$/i.test(text.trim())) {
      showAll.setAttribute('aria-label', 'Volver a la selección resumida del gráfico');
    }
  };

  const apply2dDensityRule = () => {
    const is2d = view2.getAttribute('aria-pressed') === 'true';
    const nVisible = Number(visibleCount.textContent || '0');
    const dense = is2d && nVisible > 25;
    chartCard.dataset.dense2d = dense ? 'true' : 'false';

    svg.querySelectorAll('.wn-point-label').forEach((label) => {
      label.classList.toggle('wn-auto-hidden', dense);
    });
  };

  const refresh = () => {
    normalizeShowAllLabel();
    apply2dDensityRule();
  };

  const observer = new MutationObserver(() => {
    window.requestAnimationFrame(refresh);
  });

  observer.observe(svg, { childList: true, subtree: true });
  observer.observe(visibleCount, { childList: true, characterData: true, subtree: true });
  observer.observe(showAll, { childList: true, characterData: true, subtree: true });
  observer.observe(view2, { attributes: true, attributeFilter: ['aria-pressed'] });

  window.addEventListener('resize', apply2dDensityRule);
  refresh();
})();
