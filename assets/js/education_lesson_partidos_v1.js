(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    camaraComitesActual: {
      label: 'Comités Parlamentarios actuales',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/diputados/bancadas_parlamentarias.aspx',
      note: 'Define los Comités Parlamentarios, explica el rol de sus jefaturas y publica su composición actual.'
    },
    reglamentoComites56: {
      label: 'Reglamento de la Cámara · artículo 56',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/doc/leyes_normas/reglamento.pdf',
      note: 'Establece la formación de comités, el umbral de siete representantes, la obligación de adscripción y las reglas para partidos pequeños e independientes.'
    },
    camaraFaqBancada: {
      label: 'Formación ciudadana · Jefe de Bancada y Mesa Directiva',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/formacion_ciudadana/faq.aspx',
      note: 'Explica que el jefe de bancada representa un Comité Parlamentario o el conjunto de comités de un mismo partido y describe la Mesa Directiva.'
    },
    toroUnidad2007: {
      label: 'Conducta legislativa ante las iniciativas del Ejecutivo: unidad de los bloques políticos en Chile',
      publisher: 'Revista de Ciencia Política',
      url: 'https://www.scielo.cl/scielo.php?pid=S0718-090X2007000200002&script=sci_arttext',
      note: 'Analiza unidad de partidos y coaliciones ante iniciativas del Ejecutivo y permite distinguir patrones observados de sus posibles mecanismos causales.'
    },
    careyChile1990s: {
      label: 'Parties, Coalitions, and the Chilean Congress in the 1990s',
      publisher: 'Cambridge University Press',
      url: 'https://www.cambridge.org/core/books/abs/legislative-politics-in-latin-america/parties-coalitions-and-the-chilean-congress-in-the-1990s/ADFF472F96C390133DDBA3432B49C2FB',
      note: 'Reconstruye la centralidad histórica de partidos y coaliciones para organizar el comportamiento legislativo chileno.'
    },
    bunkerFragmentacion2017: {
      label: 'La elección de 2017 y el fraccionamiento del sistema de partidos en Chile',
      publisher: 'Revista Chilena de Derecho y Ciencia Política',
      url: 'https://jonraf.uct.cl/index.php/RDCP/es/article/view/1296',
      note: 'Examina el aumento de fragmentación partidaria tras la reforma electoral y sus posibles consecuencias para la coordinación legislativa.'
    }
  });

  data.lessons['organizacion-politica'] = {
    title: 'Partidos, bancadas y comités: ¿son lo mismo?',
    unit: 'partidos',
    status: 'ready',
    readingTime: '11–14 min',
    intro: 'Una Cámara con 155 integrantes no funciona como 155 individuos aislados. Pero partido, bancada, comité parlamentario, coalición y oficialismo u oposición describen relaciones distintas y no deben usarse como sinónimos.',
    keyPoints: [
      'El partido político es una organización que existe más allá del Congreso; su presencia parlamentaria es solo una parte de su actividad.',
      'La bancada expresa políticamente a un grupo dentro de la Cámara, mientras el Comité Parlamentario es una unidad formal del Reglamento para organizar la vida interna de la corporación.',
      'Cada partido integra un comité por cada siete representantes; partidos con menos de siete pueden asociarse y todo diputado debe pertenecer a un comité.',
      'Un independiente puede integrarse a un comité sin convertirse por eso en militante del partido que domina ese comité.',
      'Cohesión describe un patrón de voto conjunto; disciplina supone un mecanismo que induce ese comportamiento. Una no demuestra automáticamente la otra.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'En la papeleta eliges personas; dentro de la Cámara esas personas se organizan colectivamente',
        paragraphs: [
          'Los ciudadanos votan por candidaturas, pero los representantes elegidos no ingresan a una institución vacía. Llegan vinculados a partidos, listas y alianzas, y luego deben organizarse dentro de la Cámara mediante estructuras parlamentarias.',
          'Esas capas ayudan a coordinar cientos de decisiones, distribuir tiempos, negociar procedimientos y construir mayorías. El error aparece cuando se supone que todas ellas significan exactamente lo mismo.'
        ],
        sourceIds: ['camaraComitesActual', 'careyChile1990s']
      },
      {
        type: 'institution',
        title: 'Partido, bancada y comité responden preguntas diferentes',
        paragraphs: [
          '<strong>Partido</strong> es una organización política que compite electoralmente, desarrolla programas y existe fuera del Congreso. <strong>Bancada</strong> es una expresión parlamentaria utilizada para agrupar y coordinar representantes. El <span data-edu-term="comite-parlamentario">Comité Parlamentario</span>, en cambio, es una unidad reglamentaria formal de organización interna.',
          'La propia Cámara explica que los comités permiten la relación entre sus integrantes y la Mesa y denomina jefe de bancada a quien representa a un comité —o al conjunto de comités de un mismo partido—. Esto muestra por qué el lenguaje cotidiano puede superponer términos sin volverlos jurídicamente idénticos.'
        ],
        sourceIds: ['camaraComitesActual', 'camaraFaqBancada']
      },
      {
        type: 'institution',
        title: 'El Reglamento obliga a organizarse en comités',
        paragraphs: [
          'El artículo 56 del Reglamento establece que cada partido político integra un comité por cada <strong>siete representantes</strong> que tenga en la Cámara. Dos o más partidos con menos de siete pueden juntarse para alcanzar ese umbral.',
          'Todo diputado debe pertenecer a un comité. Los independientes pueden juntarse y formar uno o ingresar a los comités de otros partidos. Por eso un representante puede ser independiente en términos partidarios y, al mismo tiempo, estar adscrito institucionalmente a un comité compartido.'
        ],
        sourceIds: ['reglamentoComites56']
      },
      {
        type: 'myth',
        title: '“Independiente en Comité X” no significa “militante de X”',
        paragraphs: [
          'La militancia y la adscripción parlamentaria responden a instituciones diferentes. Integrarse a un comité puede ser necesario para ejercer derechos y participar de la organización reglamentaria de la Cámara, sin que ello produzca por sí solo afiliación partidaria.',
          'Por eso este sitio mantendrá separadas las variables de <strong>partido</strong> y <strong>bancada/comité</strong> y, cuando corresponda, usará fórmulas como “Independiente en [comité]”.'
        ],
        sourceIds: ['reglamentoComites56', 'camaraComitesActual']
      },
      {
        type: 'institution',
        title: 'Coalición y oficialismo/oposición son otras dos capas',
        paragraphs: [
          'Una <strong>coalición</strong> es una alianza política entre partidos. Puede tener dimensión electoral, gubernamental o legislativa. No es una unidad reglamentaria de la Cámara y sus partidos conservan identidades propias.',
          '<strong>Oficialismo</strong> y <strong>oposición</strong> describen una relación política con el Gobierno de turno. No son atributos permanentes de un partido: pueden cambiar cuando cambia el Gobierno, una coalición o la posición de una fuerza política. Tampoco todas las organizaciones encajan siempre limpiamente en ese binomio.'
        ],
        sourceIds: ['careyChile1990s']
      },
      {
        type: 'evidence',
        title: 'Los partidos y coaliciones han estructurado fuertemente el Congreso chileno',
        paragraphs: [
          'La literatura sobre Chile ha destacado históricamente partidos nacionales relativamente fuertes y un papel importante de las coaliciones en la organización del comportamiento legislativo. Carey mostró que, durante los años noventa, comprender el Congreso requería observar no solo individuos sino partidos y coaliciones.',
          'Trabajos posteriores, como el de Sergio Toro para 2002–2006, encuentran altos niveles de unidad en bloques políticos frente a iniciativas del Ejecutivo. Esos resultados describen regularidades agregadas en períodos concretos; no constituyen una regla según la cual todo integrante votará siempre como su grupo.'
        ],
        sourceIds: ['careyChile1990s', 'toroUnidad2007']
      },
      {
        type: 'myth',
        title: 'Cohesión no demuestra disciplina',
        paragraphs: [
          'Si nueve de diez integrantes de un partido votan igual, podemos observar una alta <strong>cohesión</strong> o unidad en esa decisión. No sabemos todavía por qué ocurrió.',
          'Podrían compartir preferencias, haber deliberado, coordinar estratégicamente o responder a incentivos de la organización. Hablar de <strong>disciplina</strong> exige evidencia sobre mecanismos que inducen el comportamiento. Por eso el sitio puede medir coincidencia o cohesión sin llamar automáticamente “rebelde” a quien diverge ni “obediente” a quien coincide.'
        ],
        sourceIds: ['toroUnidad2007']
      },
      {
        type: 'history',
        title: 'El Congreso de 2026 no tiene la misma estructura partidaria que el de la transición',
        paragraphs: [
          'Gran parte de la literatura clásica sobre el Congreso posterior a 1990 estudió un sistema organizado por el binominal y dos grandes coaliciones. La reforma electoral de 2015 modificó ese entorno y la elección de 2017 mostró un incremento marcado de la fragmentación partidaria.',
          'Más fragmentación puede ampliar la diversidad de fuerzas representadas, pero también eleva los costos de construir mayorías y coordinar procedimientos. Por eso no es correcto trasladar sin revisión conclusiones de la Cámara de 1990 a la de 2026.'
        ],
        sourceIds: ['bunkerFragmentacion2017', 'careyChile1990s']
      },
      {
        type: 'case',
        title: 'Míralo funcionando: cinco etiquetas pueden describir a una misma persona',
        paragraphs: [
          'Una diputada puede pertenecer al Partido A, integrar la bancada de ese partido, compartir un Comité Parlamentario con Partido B e independientes, formar parte de una coalición gubernamental y ser clasificada como oficialista en una fecha determinada. No hay contradicción: cada etiqueta responde a una pregunta distinta.',
          'La futura ficha política debe mostrar estas capas separadamente y con fecha. Para actuaciones históricas, la pregunta correcta no es “¿cuál es su partido hoy?”, sino “¿qué partido y comité tenía cuando ocurrió este hecho?”.'
        ],
        sourceIds: ['camaraComitesActual', 'reglamentoComites56']
      },
      {
        type: 'debate',
        title: 'La tensión entre representación individual y organización partidaria no tiene una solución simple',
        paragraphs: [
          'Los partidos permiten ofrecer programas, reducir costos de información y coordinar mayorías. Al mismo tiempo, un representante posee vínculos territoriales, preferencias personales y responsabilidades hacia electores que pueden entrar en tensión con la posición colectiva.',
          'La discusión democrática no consiste en elegir entre “partidos” o “personas” como si solo uno fuera legítimo. La pregunta relevante es cómo se distribuyen autorización, autonomía, coordinación y rendición de cuentas entre ambas dimensiones.'
        ],
        sourceIds: ['careyChile1990s', 'bunkerFragmentacion2017']
      }
    ],
    sourceIds: ['camaraComitesActual', 'reglamentoComites56', 'camaraFaqBancada', 'toroUnidad2007', 'careyChile1990s', 'bunkerFragmentacion2017']
  };

  const question = data.featuredQuestions.find((item) => item.id === 'organizacion-politica');
  if (question) {
    question.title = 'Partidos, bancadas y comités: ¿son lo mismo?';
    question.summary = 'Cómo se organizan políticamente los representantes y por qué partido, comité, coalición y oficialismo no son sinónimos.';
    question.status = 'ready';
  }
})();
