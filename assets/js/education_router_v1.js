(() => {
  const root = document.getElementById('civic-router-root');
  if (!root) return;

  const scenarios = [
    {
      id: 'proyecto', mark: '01', title: 'Quiero opinar sobre un proyecto de ley', hint: 'Aportar una posición, antecedente o experiencia sobre una iniciativa en trámite.', status: 'yes', statusLabel: 'Sí: el Congreso es relevante', heading: 'Busca primero dónde está el proyecto',
      text: 'Este es un asunto directamente parlamentario. La forma más útil de participar depende de la etapa: puede convenir contactar representantes, identificar la comisión que estudia el proyecto, revisar si existe una audiencia pública o utilizar una consulta habilitada en Congreso Virtual.',
      steps: ['Identifica el número de boletín o el nombre exacto del proyecto.', 'Revisa en qué Cámara y etapa se encuentra.', 'Ubica la comisión competente y sus próximas sesiones.', 'Si existe audiencia pública o consulta abierta, revisa sus reglas antes de participar.', 'Si escribes a un parlamentario, identifica el proyecto y formula una solicitud concreta.'],
      links: [
        ['Cámara · proyectos de ley', 'https://www.camara.cl/legislacion/ProyectosDeLey/proyectos_ley.aspx'],
        ['Senado · proyectos y ley fácil', 'https://www.senado.cl/actividad-legislativa/proyectos-de-ley'],
        ['Congreso Virtual', 'https://congresovirtual.cl/']
      ]
    },
    {
      id: 'seguir', mark: '02', title: 'Quiero saber qué pasó con una ley o votación', hint: 'Seguir el trámite, revisar una etapa o saber cómo votaron representantes.', status: 'yes', statusLabel: 'Sí: información parlamentaria', heading: 'La pregunta se puede reconstruir con fuentes del Congreso',
      text: 'Aquí el Congreso es la fuente principal. Conviene distinguir proyecto, ley y votación: una iniciativa puede haber tenido muchas votaciones distintas antes de convertirse —o no— en ley.',
      steps: ['Busca el boletín o ley.', 'Abre su historial de tramitación.', 'Identifica el objeto exacto de la votación que te interesa.', 'Revisa resultado y votos individuales cuando exista registro nominal.', 'No traduzcas automáticamente una votación parcial como apoyo o rechazo a todo el proyecto.'],
      links: [['Cámara · legislación', 'https://www.camara.cl/legislacion/'], ['Senado · actividad legislativa', 'https://www.senado.cl/actividad-legislativa']]
    },
    {
      id: 'servicio', mark: '03', title: 'Tengo un problema con un servicio público nacional', hint: 'Por ejemplo, una respuesta administrativa, una obra o la ejecución de una política.', status: 'mixed', statusLabel: 'Puede ayudar, pero no resuelve directamente', heading: 'La autoridad competente sigue siendo el organismo responsable',
      text: 'Un diputado puede recibir antecedentes, hacer visible un problema y utilizar herramientas parlamentarias para solicitar información o promover fiscalización. Pero no se transforma por eso en superior jerárquico del servicio ni puede ordenar unilateralmente una solución administrativa.',
      steps: ['Usa primero el canal formal del servicio responsable cuando exista.', 'Conserva folios, fechas, respuestas y documentos.', 'Si contactas a un parlamentario, explica qué organismo interviene y qué gestión formal ya realizaste.', 'Pide una acción parlamentaria posible —por ejemplo, solicitar antecedentes— en lugar de exigir que el diputado dicte la resolución administrativa.'],
      links: [['Encuentra a tus representantes', 'index.html'], ['ChileAtiende · instituciones y trámites', 'https://www.chileatiende.gob.cl/']]
    },
    {
      id: 'municipal', mark: '04', title: 'Tengo un problema que corresponde a mi municipio', hint: 'Permisos municipales, servicios locales, ordenanzas u otras competencias comunales.', status: 'mixed', statusLabel: 'Congreso no es la autoridad resolutiva', heading: 'El municipio es normalmente la primera institución competente',
      text: 'Un diputado puede escuchar una demanda territorial, visibilizarla o relacionarla con un problema de política nacional. Pero no dirige al alcalde ni a las unidades municipales y no puede sustituir sus procedimientos administrativos.',
      steps: ['Identifica la unidad municipal competente y utiliza su canal formal.', 'Si el problema revela una falla más amplia de legislación o política pública, puede ser razonable informar también a tus representantes.', 'Distingue siempre entre pedir representación política y pedir una resolución administrativa.'],
      links: [['Encuentra a tus representantes', 'index.html']]
    },
    {
      id: 'judicial', mark: '05', title: 'Tengo una causa judicial o necesito que alguien resuelva un conflicto', hint: 'Juicios, decisiones de tribunales, conflictos civiles o una resolución judicial pendiente.', status: 'no', statusLabel: 'No: el Congreso no decide causas', heading: 'Un parlamentario no puede resolver ni dirigir una causa judicial',
      text: 'La función legislativa no autoriza a diputadas o senadores a decidir controversias sometidas a tribunales. Si necesitas orientación jurídica o representación, debes acudir a los canales judiciales o de asistencia legal que correspondan.',
      steps: ['No pidas a un parlamentario que ordene a un juez fallar de determinada manera.', 'Busca orientación jurídica profesional o los servicios públicos de asistencia que correspondan a tu situación.', 'El Congreso puede cambiar reglas generales mediante leyes, pero no reemplaza la decisión del tribunal en un caso concreto.'],
      links: [['Corporación de Asistencia Judicial', 'https://www.cajmetro.cl/'], ['Poder Judicial', 'https://www.pjud.cl/']]
    },
    {
      id: 'delito', mark: '06', title: 'Quiero denunciar un posible delito o una emergencia', hint: 'Hechos que podrían requerir investigación penal o respuesta inmediata.', status: 'no', statusLabel: 'No: usa el canal competente', heading: 'El Congreso no recibe denuncias penales como órgano investigador',
      text: 'Un parlamentario puede discutir legislación de seguridad o fiscalizar políticas públicas, pero no reemplaza a las policías, el Ministerio Público ni los servicios de emergencia. Una denuncia o emergencia debe dirigirse al organismo competente.',
      steps: ['Si existe una emergencia actual, utiliza el servicio de emergencia correspondiente.', 'Para denuncias penales, utiliza los canales oficiales de policías o Ministerio Público.', 'Puedes informar después a representantes sobre un patrón o problema de política pública, pero eso no sustituye la denuncia formal.'],
      links: [['Fiscalía de Chile', 'https://www.fiscaliadechile.cl/'], ['Carabineros de Chile', 'https://www.carabineros.cl/']]
    },
    {
      id: 'electoral', mark: '07', title: 'Tengo una duda sobre elecciones, padrón o local de votación', hint: 'Inscripción electoral, datos electorales, candidaturas o resultados oficiales.', status: 'no', statusLabel: 'No: la fuente es Servel', heading: 'Servel administra y publica la información electoral oficial',
      text: 'El Congreso define parte de las reglas electorales mediante leyes, pero la administración de elecciones y la información oficial de padrón, locales, candidaturas y resultados corresponde al Servicio Electoral dentro de sus competencias.',
      steps: ['Consulta primero Servel.', 'Si tu interés es cambiar una regla electoral, entonces sí puede ser pertinente seguir proyectos de ley y contactar parlamentarios.'],
      links: [['Servicio Electoral de Chile', 'https://www.servel.cl/']]
    },
    {
      id: 'transparencia', mark: '08', title: 'Quiero pedir información pública al Congreso', hint: 'Documentos, antecedentes administrativos o información de las propias corporaciones.', status: 'yes', statusLabel: 'Sí: usa transparencia de la corporación', heading: 'Cámara y Senado tienen canales institucionales de información y transparencia',
      text: 'Si la información solicitada corresponde a la Cámara o al Senado, utiliza los mecanismos oficiales de información o transparencia de la corporación respectiva. Si el antecedente pertenece a otro organismo, la solicitud debe dirigirse a ese órgano.',
      steps: ['Identifica quién posee el documento.', 'Busca primero si ya está publicado en transparencia activa.', 'Si no está disponible, utiliza el canal formal de solicitud correspondiente.', 'Conserva el número de seguimiento o comprobante.'],
      links: [['Cámara · transparencia', 'https://www.camara.cl/transparencia/'], ['Senado · ciudadanía y transparencia', 'https://www.senado.cl/ciudadania']]
    }
  ];

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  const renderOptions = () => {
    root.innerHTML = `<div class="civic-options">${scenarios.map((item) => `<button class="civic-option" type="button" data-civic-id="${escapeHtml(item.id)}"><span class="civic-option-mark">${escapeHtml(item.mark)}</span><span><strong>${escapeHtml(item.title)}</strong><small>${escapeHtml(item.hint)}</small></span></button>`).join('')}</div><div id="civic-result" class="civic-result" hidden aria-live="polite"></div>`;
  };

  const show = (id) => {
    const item = scenarios.find((scenario) => scenario.id === id);
    const result = document.getElementById('civic-result');
    if (!item || !result) return;
    result.hidden = false;
    result.innerHTML = `<div class="civic-result-head"><span class="civic-result-status ${escapeHtml(item.status)}">${escapeHtml(item.statusLabel)}</span><h2>${escapeHtml(item.heading)}</h2></div><p>${escapeHtml(item.text)}</p><ol class="civic-steps">${item.steps.map((step) => `<li>${escapeHtml(step)}</li>`).join('')}</ol><div class="civic-links">${item.links.map(([label, href]) => `<a href="${escapeHtml(href)}" ${/^https?:/.test(href) ? 'target="_blank" rel="noopener noreferrer"' : ''}>${escapeHtml(label)}</a>`).join('')}</div><button class="civic-reset" type="button">Elegir otra situación</button>`;
    result.querySelector('.civic-reset')?.addEventListener('click', () => {
      result.hidden = true;
      result.innerHTML = '';
      root.querySelector('.civic-option')?.focus();
    });
    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  };

  renderOptions();
  root.addEventListener('click', (event) => {
    const button = event.target.closest('[data-civic-id]');
    if (button) show(button.dataset.civicId);
  });
})();
