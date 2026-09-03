(() => {
  const SVG_NS = 'http://www.w3.org/2000/svg';
  const button = document.getElementById('wn-download');
  const svg = document.getElementById('wn-chart');
  if (!button || !svg) return;

  // Reemplaza el botón para eliminar el listener de exportación anterior sin
  // interferir con el resto de la lógica del explorador.
  const cleanButton = button.cloneNode(true);
  button.replaceWith(cleanButton);

  const normalize = (value) => String(value || '')
    .toLocaleLowerCase('es-CL')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const styleProps = [
    'fill', 'fill-opacity', 'stroke', 'stroke-opacity', 'stroke-width',
    'stroke-dasharray', 'stroke-linecap', 'stroke-linejoin', 'opacity',
    'font-family', 'font-size', 'font-weight', 'font-style', 'letter-spacing',
    'text-anchor', 'dominant-baseline', 'paint-order', 'visibility'
  ];

  const inlineComputedStyles = (sourceRoot, targetRoot) => {
    const sourceNodes = [sourceRoot, ...sourceRoot.querySelectorAll('*')];
    const targetNodes = [targetRoot, ...targetRoot.querySelectorAll('*')];

    sourceNodes.forEach((source, index) => {
      const target = targetNodes[index];
      if (!target) return;
      const computed = window.getComputedStyle(source);
      styleProps.forEach((prop) => {
        const value = computed.getPropertyValue(prop);
        if (value) target.style.setProperty(prop, value);
      });
    });
  };

  const exportPng = () => {
    const clone = svg.cloneNode(true);
    clone.setAttribute('xmlns', SVG_NS);
    clone.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');

    // El SVG interactivo depende de CSS externo. Para una imagen autónoma,
    // copiamos todos los estilos computados antes de serializarlo.
    inlineComputedStyles(svg, clone);

    // Salvaguarda específica del 1D: sin CSS, un <rect> SVG tiene fill negro
    // por defecto. Forzamos el color editorial de las bandas alternadas.
    clone.querySelectorAll('.wn-row-band').forEach((band) => {
      band.setAttribute('fill', '#f7f9fb');
      band.style.setProperty('fill', '#f7f9fb');
      band.removeAttribute('stroke');
      band.style.setProperty('stroke', 'none');
    });

    const viewBox = svg.viewBox.baseVal;
    const width = Math.max(1, viewBox.width || 1000);
    const height = Math.max(1, viewBox.height || 590);
    const scale = 2;

    clone.setAttribute('width', String(width));
    clone.setAttribute('height', String(height));
    clone.setAttribute(
      'preserveAspectRatio',
      svg.getAttribute('preserveAspectRatio') || 'xMinYMin meet'
    );

    const bg = document.createElementNS(SVG_NS, 'rect');
    bg.setAttribute('x', '0');
    bg.setAttribute('y', '0');
    bg.setAttribute('width', String(width));
    bg.setAttribute('height', String(height));
    bg.setAttribute('fill', '#ffffff');
    bg.setAttribute('stroke', 'none');
    clone.insertBefore(bg, clone.firstChild);

    const xml = new XMLSerializer().serializeToString(clone);
    const blob = new Blob([xml], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const image = new Image();

    image.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = Math.round(width * scale);
      canvas.height = Math.round(height * scale);
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
      URL.revokeObjectURL(url);

      const topic = document.getElementById('wn-topic')?.value || '';
      const view = document.getElementById('wn-view-2d')?.getAttribute('aria-pressed') === 'true' ? '2d' : '1d';
      const link = document.createElement('a');
      link.download = `wnominate-${view}-${topic ? normalize(topic).replace(/\s+/g, '-') : 'todos'}-2026.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    };

    image.onerror = () => {
      URL.revokeObjectURL(url);
      console.error('No se pudo rasterizar el SVG W-NOMINATE para exportarlo como PNG.');
    };

    image.src = url;
  };

  cleanButton.addEventListener('click', exportPng);
})();
