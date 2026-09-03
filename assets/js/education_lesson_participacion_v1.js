(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    camaraInfoCiudadana: {
      label: 'Información Ciudadana de la Cámara',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/informacion_ciudadana.aspx',
      note: 'Reúne mecanismos y recursos actuales de vínculo con la ciudadanía, incluido Congreso Virtual.'
    },
    camaraAudienciasPublicas: {
      label: 'Formación ciudadana · audiencias públicas',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://camara.cl/formacion_ciudadana/faq.aspx',
      note: 'Explica las audiencias públicas de comisiones permanentes y el procedimiento de inscripción de instituciones o entidades interesadas.'
    },
    camaraContactoCiudadano: {
      label: 'Formulario de contacto de la Cámara',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/formulario_contacto.aspx',
      note: 'Canal institucional de consultas a la Oficina de Información Ciudadana.'
    },
    senadoCiudadania: {
      label: 'Ciudadanía · Senado',
      publisher: 'Senado de la República de Chile',
      url: 'https://www.senado.cl/ciudadania',
      note: 'Reúne Congreso Virtual, consultas, transparencia, programas de educación cívica y otros recursos ciudadanos.'
    },
    senadoParticipacionReglamento: {
      label: 'Reglamento de Participación Ciudadana del Senado',
      publisher: 'Senado de la República de Chile',
      url: 'https://www.senado.cl/transparencia/transparencia-activa/reglamento-de-participacion-ciudadana-del-senado',
      note: 'Regula modalidades y procedimientos de participación antes, durante y después del proceso legislativo en el Senado.'
    },
    congresoVirtual: {
      label: 'Congreso Virtual',
      publisher: 'Congreso Nacional de Chile',
      url: 'https://congresovirtual.cl/',
      note: 'Plataforma digital de participación sobre proyectos y consultas legislativas; sus aportes sirven como insumo y no sustituyen la decisión parlamentaria.'
    },
    pnudParticipacionCongreso: {
      label: 'La participación de la sociedad civil en el proceso legislativo chileno',
      publisher: 'Programa de las Naciones Unidas para el Desarrollo',
      url: 'https://www.undp.org/es/chile/publicaciones/la-participacion-de-la-sociedad-civil-en-el-proceso-legislativo-chileno',
      note: 'Estudia audiencias públicas y otras formas de participación de sociedad civil en Cámara y Senado y formula recomendaciones para fortalecerlas.'
    },
    segoviaGamboa2019: {
      label: 'Neopluralismo “a la chilena”. Grupos de interés en el proceso legislativo',
      publisher: 'Revista de Ciencia Política',
      url: 'https://www.scielo.cl/scielo.php?pid=S0718-090X2019000100025&script=sci_arttext',
      note: 'Analiza participación de grupos de interés en comisiones entre 2006 y 2014 y encuentra participación plural pero desigual, especializada y de baja magnitud general.'
    },
    opazoComisiones2024: {
      label: 'Legislative science advice in Chile',
      publisher: 'The Journal of Legislative Studies',
      url: 'https://www.tandfonline.com/doi/full/10.1080/13572334.2023.2298123',
      note: 'Estudia participación de productores de conocimiento en comisiones ambientales y encuentra limitaciones de cantidad, género y localización geográfica.'
    }
  });

  data.lessons['participar'] = {
    title: '¿Cómo puede participar un ciudadano?',
    unit: 'participacion',
    status: 'ready',
    readingTime: '11–14 min',
    intro: 'Participar en el Congreso no significa tener un voto vinculante sobre cada proyecto. Existen distintos canales para informarse, contactar representantes, aportar antecedentes, solicitar ser oído y participar en consultas, cada uno con reglas y efectos diferentes.',
    keyPoints: [
      'El primer acto de participación informada puede ser seguir un proyecto, identificar su comisión, revisar sesiones, documentos y votaciones antes de intervenir.',
      'Los ciudadanos pueden contactar directamente a sus representantes y también utilizar canales institucionales de Cámara y Senado.',
      'Las comisiones pueden realizar audiencias públicas; en la Cámara los interesados pueden inscribirse ante la Secretaría de la comisión cuando se convoque una audiencia.',
      'Congreso Virtual permite opinar y votar sobre proyectos seleccionados, pero esa participación no reemplaza ni vincula jurídicamente el voto de diputadas y senadores.',
      'Participar no equivale a influir: el acceso a espacios legislativos puede ser desigual y la investigación chilena ha documentado sesgos en quiénes participan.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'Participar empieza por saber dónde está ocurriendo la decisión',
        paragraphs: [
          'Si una persona quiere influir o hacer oír una posición sobre un proyecto, escribir genéricamente “al Congreso” no siempre es la estrategia más útil. Primero conviene saber <strong>qué boletín es, en qué Cámara se encuentra, qué comisión lo estudia y qué etapa viene después</strong>.',
          'La arquitectura futura del sitio debe convertir esa información en una ruta práctica: proyecto → etapa → comisión → integrantes → próxima sesión → canales disponibles. La educación institucional termina así en capacidad de acción.'
        ],
        sourceIds: ['camaraInfoCiudadana', 'senadoCiudadania']
      },
      {
        type: 'institution',
        title: 'Contactar a un parlamentario es un canal legítimo, pero no convierte al representante en autoridad ejecutiva',
        paragraphs: [
          'Los representantes mantienen canales públicos de contacto y la función representativa incluye escuchar demandas territoriales y políticas. Un ciudadano puede enviar antecedentes, plantear una posición sobre una iniciativa o informar un problema que considere relevante para fiscalización o legislación.',
          'El límite estudiado en la lección anterior permanece: un diputado no puede ordenar por sí solo a un hospital, municipio, tribunal o ministerio que resuelva un caso. El contacto parlamentario puede <strong>representar, canalizar, preguntar o fiscalizar</strong>; no sustituye las competencias del órgano responsable.'
        ],
        sourceIds: ['camaraFuncionesParlamentarios', 'camaraContactoCiudadano', 'locArticulo9']
      },
      {
        type: 'institution',
        title: 'Audiencias públicas: participar en el lugar donde se estudia un proyecto',
        paragraphs: [
          'Las comisiones permanentes de la Cámara pueden celebrar <strong>audiencias públicas</strong> para escuchar instituciones o entidades interesadas en la materia de un proyecto de ley. La información institucional señala que quienes deseen participar deben inscribirse ante la Secretaría de la comisión cuando la audiencia es convocada.',
          'Esto no crea un derecho irrestricto a intervenir oralmente en toda sesión ni garantiza que una opinión sea incorporada al texto. La forma, selección, tiempo y organización de la audiencia dependen del procedimiento aplicable. Pero abre un canal institucional donde antecedentes ciudadanos pueden ingresar al proceso legislativo.'
        ],
        sourceIds: ['camaraAudienciasPublicas', 'locComisiones22']
      },
      {
        type: 'institution',
        title: 'Congreso Virtual: participación digital como insumo, no plebiscito',
        paragraphs: [
          'La Cámara y el Senado promueven actualmente <strong>Congreso Virtual</strong>, plataforma donde las personas pueden pronunciarse y formular comentarios sobre proyectos y consultas seleccionadas. Los resultados y aportes pueden llegar a las comisiones que analizan esas materias.',
          'La herramienta no transforma la tramitación en democracia directa. La decisión jurídica sigue correspondiendo a los órganos y representantes definidos por la Constitución. Por eso el sitio deberá decir siempre <strong>“opinión ciudadana no vinculante”</strong> cuando corresponda y evitar frases como “vota esta ley”.'
        ],
        sourceIds: ['camaraInfoCiudadana', 'senadoParticipacionReglamento', 'congresoVirtual']
      },
      {
        type: 'institution',
        title: 'Informarse y pedir información también son formas de participación',
        paragraphs: [
          'Cámara y Senado publican sesiones, citaciones de comisión, proyectos, documentos y resultados. El Senado ofrece además canales de consultas ciudadanas y solicitudes de acceso a información pública, y la Cámara mantiene una Oficina de Información Ciudadana y herramientas de transparencia.',
          'Esto importa porque participar no comienza necesariamente hablando. Poder reconstruir qué se está decidiendo, quién intervino y qué antecedentes existen reduce la dependencia de intermediarios y permite formular demandas mucho más específicas.'
        ],
        sourceIds: ['senadoCiudadania', 'camaraContactoCiudadano', 'camaraInfoCiudadana']
      },
      {
        type: 'case',
        title: 'Quiero opinar sobre un proyecto: la ruta que debería ofrecer el sitio',
        paragraphs: [
          '<strong>1.</strong> Busca el proyecto o su boletín. <strong>2.</strong> Revisa en qué etapa y cámara está. <strong>3.</strong> Identifica la comisión que lo estudia. <strong>4.</strong> Mira próximas sesiones y audiencias publicadas. <strong>5.</strong> Revisa quiénes integran esa comisión y los representantes de tu distrito. <strong>6.</strong> Elige un canal: contacto parlamentario, audiencia cuando corresponda, Congreso Virtual o consulta institucional.',
          'El sitio no enviará automáticamente comunicaciones ni fingirá que todos esos canales están siempre abiertos. Mostrará <strong>qué opción existe hoy para ese caso concreto</strong> y enlazará a la fuente oficial.'
        ],
        sourceIds: ['camaraAudienciasPublicas', 'camaraInfoCiudadana', 'senadoCiudadania']
      },
      {
        type: 'myth',
        title: 'Cuatro errores frecuentes sobre participación parlamentaria',
        bullets: [
          '<strong>“Si voto en Congreso Virtual, mi opción cuenta como un voto parlamentario”.</strong> No. Es participación consultiva y no reemplaza la decisión constitucional de las cámaras.',
          '<strong>“Tengo derecho a hablar en cualquier sesión de comisión”.</strong> No. Existen procedimientos, audiencias y decisiones de organización específicas.',
          '<strong>“Si una organización fue escuchada, entonces consiguió que se aprobara su posición”.</strong> Participación no demuestra influencia causal.',
          '<strong>“Si tengo un problema con el Estado, un diputado es siempre la autoridad correcta”.</strong> Depende del asunto. Muchas decisiones pertenecen a municipios, servicios públicos, tribunales u otros órganos.'
        ],
        sourceIds: ['senadoParticipacionReglamento', 'camaraAudienciasPublicas', 'segoviaGamboa2019', 'camaraFuncionesParlamentarios']
      },
      {
        type: 'evidence',
        title: 'Participar no garantiza igualdad de acceso ni de influencia',
        paragraphs: [
          'El estudio de Segovia y Gamboa sobre grupos de interés que participaron en el proceso legislativo entre 2006 y 2014 encontró presencia de distintos tipos de actores, pero también un desequilibrio favorable a intereses empresariales, una participación general relativamente baja y altos niveles de especialización.',
          'Investigaciones más recientes sobre productores de conocimiento en discusiones ambientales detectan además limitaciones de participación y sesgos de género y localización geográfica. Estos hallazgos advierten contra una conclusión automática: <strong>abrir una audiencia no garantiza por sí sola una representación equilibrada de la sociedad</strong>.'
        ],
        sourceIds: ['segoviaGamboa2019', 'opazoComisiones2024', 'pnudParticipacionCongreso']
      },
      {
        type: 'debate',
        title: '¿Cuánta participación debe existir dentro de una institución representativa?',
        paragraphs: [
          'Un Congreso existe precisamente para que representantes autorizados deliberen y decidan. Incorporar participación ciudadana puede mejorar información, pluralidad y responsiveness, pero no elimina la necesidad de reglas para ordenar acceso, tiempos y responsabilidad de la decisión final.',
          'La pregunta democrática no es simplemente “participación sí o no”. Es cómo diseñar mecanismos que amplíen voces sin permitir captura por actores con más recursos, sin borrar la responsabilidad de los representantes y sin convertir cada etapa legislativa en una competencia de movilización permanente.'
        ],
        sourceIds: ['pnudParticipacionCongreso', 'segoviaGamboa2019', 'senadoParticipacionReglamento']
      }
    ],
    sourceIds: ['camaraInfoCiudadana', 'camaraAudienciasPublicas', 'camaraContactoCiudadano', 'senadoCiudadania', 'senadoParticipacionReglamento', 'congresoVirtual', 'pnudParticipacionCongreso', 'segoviaGamboa2019', 'opazoComisiones2024', 'camaraFuncionesParlamentarios', 'locArticulo9', 'locComisiones22']
  };

  const question = data.featuredQuestions.find((item) => item.id === 'participar');
  if (question) {
    question.title = '¿Cómo puede participar un ciudadano?';
    question.summary = 'Cómo informarse, contactar, participar en audiencias o consultas y distinguir participación de influencia.';
    question.status = 'ready';
  }
})();
