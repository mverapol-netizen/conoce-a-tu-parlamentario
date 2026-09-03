(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    reglamentoAgenda107108: {
      label: 'Reglamento de la Cámara · Orden del Día y formación de la tabla',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/doc/leyes_normas/reglamento.pdf',
      note: 'Los artículos 107 y 108 regulan el Orden del Día y establecen que su tabla se forma semanalmente por la Mesa y la unanimidad de los Comités Parlamentarios sobre una propuesta de la Mesa.'
    },
    camaraGlosarioTabla: {
      label: 'Glosario de formación ciudadana · Tabla',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/formacion_Ciudadana/glosario.aspx',
      note: 'Define la tabla como el conjunto de asuntos que una cámara o comisión puede tratar en una sesión y distingue Despacho Inmediato, Fácil Despacho y Orden del Día.'
    },
    bcnUrgencias: {
      label: 'Formación cívica · urgencias legislativas',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/formacioncivica/detalle_guia?h=10221.3%2F45763',
      note: 'Explica simple urgencia, suma urgencia y discusión inmediata y su efecto sobre la prioridad temporal de la tramitación.'
    },
    locUrgencias26: {
      label: 'Ley Orgánica Constitucional del Congreso · artículos 26 y 27',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=30289',
      note: 'Regula la facultad presidencial de hacer presente urgencia y fija plazos de 30, 15 y 6 días según su calificación.'
    },
    aninatAgendaChile: {
      label: 'Political Institutions, Policymaking Processes and Policy Outcomes in Chile',
      publisher: 'Banco Interamericano de Desarrollo',
      url: 'https://publications.iadb.org/en/political-institutions-policymaking-processes-and-policy-outcomes-chile',
      note: 'Trabajo clásico que caracterizó al Ejecutivo chileno de la transición como un actor muy poderoso y con fuerte control de agenda dentro de un sistema de múltiples puntos de veto.'
    },
    mimicaNaviaDominance2024: {
      label: 'Where did Hyper-Presidentialism Go? The Origin of Bills and Laws Passed in Chile, 1990–2022',
      publisher: 'Journal of Politics in Latin America',
      url: 'https://journals.sagepub.com/doi/10.1177/1866802X241245727',
      note: 'Muestra cambios históricos en la dominancia legislativa presidencial y cuestiona trasladar sin matices el diagnóstico de hiperpresidencialismo de comienzos de la transición al Congreso contemporáneo.'
    }
  });

  data.lessons['agenda'] = {
    title: 'Agenda y tabla: ¿quién decide qué se discute?',
    unit: 'organizacion',
    status: 'ready',
    readingTime: '10–13 min',
    intro: 'El poder parlamentario no consiste solamente en ganar una votación. Antes hay otra decisión fundamental: qué asuntos llegan a ser discutidos, cuándo y en qué orden.',
    keyPoints: [
      'La tabla es la agenda formal de asuntos que pueden ser tratados en una sesión; no es una simple lista de todos los proyectos existentes.',
      'El Reglamento vigente establece que la tabla del Orden del Día se forma semanalmente por la Mesa y la unanimidad de los Comités Parlamentarios, sobre una propuesta de la Mesa.',
      'Existen además reglas de prioridad y distintos tipos de tabla, por lo que la agenda está estructurada por procedimientos y no solo por negociación política.',
      'El Presidente puede hacer presente urgencias legislativas que introducen plazos y prioridades temporales, pero eso no equivale a aprobar el proyecto ni a controlar unilateralmente cada decisión de la Cámara.',
      'No llegar a votación también importa políticamente: el poder de agenda determina qué conflictos reciben tiempo institucional para transformarse en decisiones.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'Antes de preguntar quién ganó, hay que preguntar por qué se votó ese asunto',
        paragraphs: [
          'Una Cámara dispone de tiempo limitado y puede tener cientos de proyectos pendientes. Por eso no basta observar el resultado final de una votación. Decidir qué proyecto se discute esta semana y cuál permanece esperando también distribuye poder político.',
          'La <span data-edu-term="tabla">tabla</span> convierte esa selección en una agenda formal. Lo que no entra a la agenda puede seguir existiendo jurídicamente, pero no avanza por el solo hecho de haber sido presentado.'
        ],
        sourceIds: ['camaraGlosarioTabla', 'reglamentoAgenda107108']
      },
      {
        type: 'institution',
        title: 'Qué es exactamente la tabla del Orden del Día',
        paragraphs: [
          'El Reglamento destina una parte de las sesiones ordinarias al <strong>Orden del Día</strong>, durante el cual se tratan exclusivamente los asuntos que figuran en su tabla. La regulación actual fija además un tiempo mínimo para esta parte de la sesión.',
          'La Cámara distingue tablas de Despacho Inmediato, Fácil Despacho y Orden del Día. Cada una responde a reglas y finalidades diferentes; por eso “estar en tabla” debe interpretarse siempre identificando la clase de tabla y la sesión correspondiente.'
        ],
        sourceIds: ['reglamentoAgenda107108', 'camaraGlosarioTabla']
      },
      {
        type: 'institution',
        title: 'Mesa y Comités Parlamentarios comparten una función de organización de agenda',
        paragraphs: [
          'El artículo 108 del Reglamento vigente establece que la tabla del Orden del Día se forma <strong>semanalmente</strong> por la Mesa y la unanimidad de los Comités Parlamentarios. La Mesa formula una propuesta que sirve de base para esa formación.',
          'Esto explica por qué las jefaturas de comité poseen importancia institucional más allá de comunicar posiciones partidarias. Participan en una arquitectura que organiza el tiempo de Sala y la secuencia de asuntos que la corporación tratará.'
        ],
        sourceIds: ['reglamentoAgenda107108', 'camaraComitesActual']
      },
      {
        type: 'institution',
        title: 'La agenda también contiene prioridades regladas',
        paragraphs: [
          'Cuando no opera un acuerdo que altere la tabla, el Reglamento establece órdenes de preferencia entre distintos tipos de asuntos. Acusaciones constitucionales, Presupuesto, proyectos con diferentes grados de urgencia, informes de comisiones mixtas, observaciones presidenciales y asuntos devueltos por el Senado ocupan posiciones específicas dentro de esa arquitectura.',
          'Por eso no sería correcto explicar la agenda como si cada semana los actores comenzaran desde cero una negociación completamente libre. Hay negociación, pero dentro de un procedimiento institucional previo.'
        ],
        sourceIds: ['reglamentoAgenda107108']
      },
      {
        type: 'institution',
        title: 'Las urgencias presidenciales introducen poder de agenda desde el Ejecutivo',
        paragraphs: [
          'El Presidente de la República puede hacer presente <span data-edu-term="urgencia">urgencia</span> para el despacho de un proyecto. La Ley Orgánica reconoce tres calificaciones: simple, suma y discusión inmediata, con plazos de 30, 15 y 6 días para terminar la discusión y votación en la Cámara requerida.',
          'La urgencia altera prioridad y tiempo de tramitación. <strong>No significa que el proyecto esté aprobado</strong>, que la Cámara deba aprobarlo ni que desaparezca la necesidad de construir las mayorías exigidas para cada decisión.'
        ],
        sourceIds: ['locUrgencias26', 'bcnUrgencias']
      },
      {
        type: 'myth',
        title: '“El Presidente decide lo que vota el Congreso” es demasiado fuerte',
        paragraphs: [
          'El Ejecutivo chileno posee herramientas legislativas importantes, entre ellas iniciativa exclusiva en ciertas materias y urgencias. La literatura clásica describió por ello una fuerte capacidad presidencial de agenda.',
          'Pero la agenda efectiva también depende de reglas de cada cámara, Mesa, comités, comisiones, etapas legislativas y construcción de mayorías. La expresión correcta es que existe una <strong>estructura compartida y asimétrica de agenda</strong>, no un control unilateral simple.'
        ],
        sourceIds: ['aninatAgendaChile', 'reglamentoAgenda107108', 'locUrgencias26']
      },
      {
        type: 'evidence',
        title: 'La relación Ejecutivo–Congreso ha cambiado históricamente',
        paragraphs: [
          'La descripción del Ejecutivo chileno como extraordinariamente dominante en el proceso legislativo fue especialmente influyente para los primeros años posteriores a 1990. Trabajos recientes muestran, sin embargo, cambios importantes en el peso relativo de mensajes y mociones y asocian parte de esa transformación a las reformas constitucionales de 2005 y electorales de 2015.',
          'Esto no elimina los poderes constitucionales del Presidente. Sí obliga a distinguir entre <strong>facultades formales de agenda</strong> y <strong>dominancia empírica sobre el conjunto del proceso legislativo</strong>, que puede variar históricamente.'
        ],
        sourceIds: ['aninatAgendaChile', 'mimicaNaviaDominance2024']
      },
      {
        type: 'case',
        title: 'Cómo debería leerse una agenda real en este sitio',
        paragraphs: [
          'La futura sección “Hoy en la Cámara” no debería copiar una tabla oficial sin contexto. Cada asunto debería mostrar <strong>qué es, en qué etapa está, qué podría decidirse ese día y qué ocurriría después</strong>. Si existe una urgencia, debe explicar su tipo y efecto procedimental.',
          'Por ejemplo: “Discusión general” debería aclarar que se debate la idea de legislar; “tercer trámite”, que se examinan modificaciones de la cámara revisora; “veto”, que se consideran observaciones presidenciales. La agenda puede así convertirse en educación institucional en tiempo real.'
        ],
        sourceIds: ['camaraGlosarioTabla', 'bcnUrgencias']
      },
      {
        type: 'debate',
        title: 'Poder de agenda y poder de decisión no son lo mismo',
        paragraphs: [
          'Un actor puede tener capacidad para priorizar un asunto y aun así perder la votación. Otro puede carecer de control sobre cuándo llega un proyecto a Sala, pero ser indispensable para formar la mayoría cuando finalmente se vota.',
          'Por eso una cartografía rigurosa del poder parlamentario debería distinguir al menos iniciativa, agenda, modificación del texto, información y decisión. Contar solamente quién ganó más votaciones deja fuera una parte importante de cómo funciona una legislatura.'
        ],
        sourceIds: ['aninatAgendaChile', 'mimicaNaviaDominance2024']
      }
    ],
    sourceIds: ['reglamentoAgenda107108', 'camaraGlosarioTabla', 'bcnUrgencias', 'locUrgencias26', 'aninatAgendaChile', 'mimicaNaviaDominance2024']
  };

  const question = data.featuredQuestions.find((item) => item.id === 'agenda');
  if (question) {
    question.title = '¿Quién decide qué se discute?';
    question.summary = 'Tabla, Mesa, comités, urgencias y la diferencia entre poder de agenda y poder de decisión.';
    question.status = 'ready';
  }
})();
