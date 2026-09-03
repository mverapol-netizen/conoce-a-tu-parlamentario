(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  const bySlug = new Map(data.glossary.map((item) => [item.slug, item]));
  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  let popover = null;
  let activeTrigger = null;

  const close = () => {
    if (!popover) return;
    popover.remove();
    popover = null;
    if (activeTrigger) activeTrigger.setAttribute('aria-expanded', 'false');
    activeTrigger = null;
  };

  const open = (trigger, concept) => {
    close();
    activeTrigger = trigger;
    trigger.setAttribute('aria-expanded', 'true');
    popover = document.createElement('div');
    popover.className = 'edu-term-popover';
    popover.setAttribute('role', 'dialog');
    popover.setAttribute('aria-label', `Definición de ${concept.term}`);
    popover.innerHTML = `<button type="button" class="edu-term-close" aria-label="Cerrar definición">×</button>
      <strong>${escapeHtml(concept.term)}</strong>
      <p>${escapeHtml(concept.short)}</p>
      <a href="aprender.html?concepto=${encodeURIComponent(concept.slug)}">Entender en profundidad</a>`;
    document.body.appendChild(popover);
    const rect = trigger.getBoundingClientRect();
    const width = Math.min(330, window.innerWidth - 24);
    popover.style.width = `${width}px`;
    const left = Math.min(Math.max(12, rect.left), window.innerWidth - width - 12);
    const top = Math.min(window.scrollY + rect.bottom + 8, window.scrollY + window.innerHeight - popover.offsetHeight - 12);
    popover.style.left = `${left}px`;
    popover.style.top = `${Math.max(window.scrollY + 12, top)}px`;
    popover.querySelector('.edu-term-close')?.addEventListener('click', close);
  };

  const enhance = (root = document) => {
    root.querySelectorAll('[data-edu-term]').forEach((node) => {
      if (node.dataset.eduEnhanced === 'true') return;
      const slug = node.dataset.eduTerm;
      const concept = bySlug.get(slug);
      if (!concept) return;
      node.dataset.eduEnhanced = 'true';
      node.classList.add('edu-term');
      node.setAttribute('tabindex', '0');
      node.setAttribute('role', 'button');
      node.setAttribute('aria-expanded', 'false');
      node.setAttribute('aria-label', `${node.textContent.trim()}. Ver definición`);
      const handler = (event) => { event.preventDefault(); event.stopPropagation(); open(node, concept); };
      node.addEventListener('click', handler);
      node.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') handler(event);
        if (event.key === 'Escape') close();
      });
    });
  };

  document.addEventListener('click', (event) => {
    if (popover && !popover.contains(event.target) && event.target !== activeTrigger) close();
  });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') close(); });
  window.addEventListener('resize', close);
  window.addEventListener('scroll', close, { passive: true });

  window.EDUCATION_GLOSSARY = { enhance, close };
  enhance();
})();
