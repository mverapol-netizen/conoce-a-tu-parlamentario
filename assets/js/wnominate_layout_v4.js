(() => {
  const card = document.querySelector('.wn-chart-card');
  const wrap = document.getElementById('wn-chart-wrap');
  const svg = document.getElementById('wn-chart');
  const view1 = document.getElementById('wn-view-1d');
  const view2 = document.getElementById('wn-view-2d');
  if (!card || !wrap || !svg || !view1 || !view2) return;

  const head = card.querySelector('.wn-chart-head');
  const stats = card.querySelector('.wn-chart-stats');
  let fullscreenButton = document.getElementById('wn-fullscreen');

  if (!fullscreenButton && head && stats) {
    const tools = document.createElement('div');
    tools.className = 'wn-chart-head-tools';
    stats.replaceWith(tools);
    tools.appendChild(stats);
    fullscreenButton = document.createElement('button');
    fullscreenButton.id = 'wn-fullscreen';
    fullscreenButton.className = 'wn-secondary-button wn-fullscreen-button';
    fullscreenButton.type = 'button';
    fullscreenButton.setAttribute('aria-pressed', 'false');
    fullscreenButton.textContent = 'Pantalla completa';
    tools.appendChild(fullscreenButton);
  }

  const nativeFullscreenElement = () => document.fullscreenElement || document.webkitFullscreenElement || null;
  const fallbackActive = () => card.classList.contains('wn-fullscreen-fallback');
  const fullscreenActive = () => nativeFullscreenElement() === card || fallbackActive();

  const updateFullscreenUi = () => {
    if (!fullscreenButton) return;
    const active = fullscreenActive();
    fullscreenButton.setAttribute('aria-pressed', String(active));
    fullscreenButton.textContent = active ? 'Salir de pantalla completa' : 'Pantalla completa';
    document.body.classList.toggle('wn-fullscreen-lock', active);
  };

  let syncScheduled = false;
  const syncLayout = () => {
    syncScheduled = false;
    const is2d = view2.getAttribute('aria-pressed') === 'true' || view2.classList.contains('is-active');
    wrap.classList.toggle('wn-mode-1d', !is2d);
    wrap.classList.toggle('wn-mode-2d', is2d);

    if (is2d) {
      svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
      const targetHeight = fullscreenActive()
        ? Math.max(460, Math.floor(wrap.clientHeight || window.innerHeight - 210))
        : 590;
      svg.style.setProperty('height', `${targetHeight}px`, 'important');
      svg.style.setProperty('min-height', fullscreenActive() ? '0px' : `${targetHeight}px`, 'important');
    } else {
      svg.setAttribute('preserveAspectRatio', 'xMinYMin meet');
      svg.style.setProperty('height', 'auto', 'important');
      svg.style.setProperty('min-height', '0px', 'important');
    }
    updateFullscreenUi();
  };

  const scheduleSync = () => {
    if (syncScheduled) return;
    syncScheduled = true;
    requestAnimationFrame(() => requestAnimationFrame(syncLayout));
  };

  const enterFallback = () => {
    card.classList.add('wn-fullscreen-fallback');
    updateFullscreenUi();
    scheduleSync();
  };

  const exitFallback = () => {
    card.classList.remove('wn-fullscreen-fallback');
    updateFullscreenUi();
    scheduleSync();
    fullscreenButton?.focus();
  };

  const toggleFullscreen = async () => {
    if (fallbackActive()) {
      exitFallback();
      return;
    }

    if (nativeFullscreenElement() === card) {
      const exit = document.exitFullscreen || document.webkitExitFullscreen;
      if (exit) {
        try { await exit.call(document); } catch (_) { exitFallback(); }
      }
      return;
    }

    const request = card.requestFullscreen || card.webkitRequestFullscreen;
    if (request) {
      try {
        await request.call(card);
        return;
      } catch (_) {
        enterFallback();
        return;
      }
    }
    enterFallback();
  };

  fullscreenButton?.addEventListener('click', toggleFullscreen);
  view1.addEventListener('click', scheduleSync);
  view2.addEventListener('click', scheduleSync);
  window.addEventListener('resize', scheduleSync);

  document.addEventListener('fullscreenchange', () => {
    updateFullscreenUi();
    setTimeout(scheduleSync, 40);
  });
  document.addEventListener('webkitfullscreenchange', () => {
    updateFullscreenUi();
    setTimeout(scheduleSync, 40);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && fallbackActive()) exitFallback();
  });

  const observer = new MutationObserver((mutations) => {
    if (mutations.some((mutation) => mutation.type === 'childList')) scheduleSync();
  });
  observer.observe(svg, { childList: true, subtree: false });

  scheduleSync();
})();
