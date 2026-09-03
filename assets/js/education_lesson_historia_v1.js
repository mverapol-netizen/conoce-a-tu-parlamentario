(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    bcnHistoria1811: {
      label: 'Historia del Congreso · 1811–1823',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/congreso_nacional/historia/index.html?periodo=1811-1823',
      note: 'Reconstruye el primer Congreso Nacional, su carácter unicameral y su papel en los primeros ensayos institucionales.'
    },
    senadoHistoria: {
      label: 'Historia del Senado',
      publisher: 'Senado de la República de Chile',
      url: 'https://www.senado.cl/acerca-del-senado/antecedentes-historicos/historia-del-senado',
      note: 'Documenta el Congreso de 1811, los primeros Senados y el proceso que conduce a la consolidación del bicameralismo.'
    },
    bcnPeriodos1828: {
      label: 'Períodos legislativos y Diarios de Sesiones',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/corporaciones/periodos_legislativos_index',
      note: 'Identifica la Constitución de 1828 como punto de inflexión en la consolidación del bicameralismo y origen de la numeración continua de períodos legislativos.'
    },
    obandoComisionesHistoria: {
      label: 'The Congressional Committee System of the Chilean Legislature, 1834–1924',
      publisher: 'Historia',
      url: 'https://www.scielo.cl/scielo.php?pid=S0717-71942011000100005&script=sci_arttext',
      note: 'Muestra la temprana institucionalización de un sistema especializado de comisiones en el Congreso chileno durante el siglo XIX.'
    },
    bcnParlamentario1891: {
      label: 'Historia del Congreso · 1891–1925',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/congreso_nacional/historia/index.html?periodo=1891-1925',
      note: 'Describe la preeminencia política del Congreso durante el régimen parlamentario y su término con la Constitución de 1925.'
    },
    memoriaParlamentaria: {
      label: 'La república parlamentaria (1891–1925)',
      publisher: 'Memoria Chilena · Biblioteca Nacional de Chile',
      url: 'https://www.memoriachilena.gob.cl/602/w3-article-3537.html',
      note: 'Explica que el parlamentarismo chileno operó mediante prácticas e interpretación de la Constitución de 1833 y presenta tanto sus deficiencias como sus continuidades institucionales.'
    },
    bcnConstitucion1925: {
      label: 'Historia y vigencia de la Constitución de 1925',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/constitucion1925/historia.html',
      note: 'Reconstruye el reemplazo del régimen parlamentario por un sistema presidencialista y la reapertura del Congreso en 1926.'
    },
    bcnHistoria1925: {
      label: 'Historia del Congreso · 1925–1973',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/congreso_nacional/historia/index.html?periodo=1925-1973',
      note: 'Revisa la trayectoria del Congreso bajo la Constitución de 1925, la expansión de la ciudadanía y las interrupciones autoritarias del período.'
    },
    dl27Congreso: {
      label: 'Decreto Ley N° 27 · disuelve el Congreso Nacional',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=209763',
      note: 'Norma de septiembre de 1973 que disolvió el Congreso y cesó las funciones de los parlamentarios.'
    },
    bcnHistoriaDictadura: {
      label: 'Historia del Congreso · 1973–1990',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/congreso_nacional/historia/index.html?periodo=1973-1990',
      note: 'Describe la ruptura democrática, la concentración de funciones en la Junta Militar y la ausencia del Congreso electivo hasta 1990.'
    },
    bcnReapertura1990: {
      label: 'Reapertura del Congreso Nacional · 11 de marzo de 1990',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/hitos_periodo/detalle_periodo.html?K=1&filtros=1%2C2%2C3%2C4%2C5%2C6&pagina=1&per=1990-2022',
      note: 'Registra la reapertura democrática: Cámara de 120 electos y Senado con 38 electos y 9 designados.'
    },
    bcnReforma2005: {
      label: 'Ley N° 20.050 · reformas constitucionales de 2005',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/elecciones/detalle_eleccion?handle=10221.1%2F63215&periodo=1990-2022',
      note: 'Eliminó senadores designados y vitalicios, reforzó mecanismos de control parlamentario y modificó otras instituciones heredadas del texto de 1980.'
    },
    bcnReforma2015: {
      label: 'Ley N° 20.840 · reforma electoral de 2015',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/elecciones/detalle_eleccion?handle=10221.1%2F63227&periodo=1990-2022',
      note: 'Reemplazó el sistema binominal por una estructura proporcional inclusiva, redujo los distritos a 28 y elevó la Cámara a 155 integrantes.'
    }
  });

  data.lessons['historia-congreso'] = {
    title: 'El Congreso no siempre fue así: una historia de problemas políticos',
    unit: 'historia',
    status: 'ready',
    readingTime: '15–19 min',
    intro: 'Chile posee una larga continuidad parlamentaria, pero no ha existido un único Congreso inmutable. Su composición, reglas electorales, relación con el Presidente y grado de legitimidad democrática han cambiado profundamente desde 1811.',
    keyPoints: [
      'El primer Congreso de 1811 fue unicameral y nació mientras todavía se discutían cuestiones básicas sobre soberanía, territorio y organización política.',
      'La Constitución de 1828 consolidó una estructura bicameral cuya continuidad nominal llega hasta hoy, aunque las dos cámaras han cambiado repetidamente.',
      'El régimen de 1891–1925 no fue una copia del parlamentarismo británico: operó mediante prácticas políticas dentro de la Constitución de 1833.',
      'La Constitución de 1925 reconfiguró el equilibrio hacia un presidencialismo más definido, sin convertir al Congreso en una institución irrelevante.',
      'En 1973 el Congreso fue disuelto y la producción legislativa pasó a un régimen autoritario: una demostración histórica de que producir normas no basta para definir un parlamento democrático.',
      'La reapertura de 1990 restauró la representación parlamentaria, pero el Senado todavía incluía miembros no electos; las reformas de 2005 y 2015 volvieron a modificar sustantivamente la institución.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'La continuidad del nombre puede esconder instituciones muy diferentes',
        paragraphs: [
          'Hablamos del “Congreso Nacional” como si fuera una institución única que hubiera permanecido intacta durante dos siglos. Existe una continuidad histórica real, pero esa continuidad convive con cambios profundos: quién puede votar, cómo se eligen los representantes, cuánto duran sus mandatos, cómo se relacionan las cámaras y qué poder tiene el Presidente.',
          'La historia sirve entonces para desnaturalizar las reglas actuales. <strong>Lo que hoy parece obvio fue alguna vez una decisión política entre alternativas posibles.</strong>'
        ],
        sourceIds: ['bcnPeriodos1828', 'bcnHistoria1811']
      },
      {
        type: 'history',
        title: '1811 — ¿Quién podía hablar en nombre del país?',
        paragraphs: [
          'El primer Congreso Nacional se constituyó el <strong>4 de julio de 1811</strong>. Era unicameral y tuvo una existencia de pocos meses antes de ser disuelto en diciembre. Su creación ocurrió cuando todavía estaban abiertas preguntas fundamentales sobre soberanía, autoridad, relación con la monarquía y representación de las provincias.',
          'Las tensiones entre capital y provincias estuvieron presentes desde el inicio. Por eso el nacimiento parlamentario chileno no debe contarse solo como una fecha fundacional: es también el comienzo de una disputa sobre <strong>quién puede representar políticamente a territorios distintos dentro de una comunidad en formación</strong>.'
        ],
        sourceIds: ['senadoHistoria', 'bcnHistoria1811']
      },
      {
        type: 'history',
        title: '1828 — ¿Por qué dividir el Congreso en dos cámaras?',
        paragraphs: [
          'Entre 1811 y la década de 1820 hubo diversos congresos, senados y ensayos constitucionales. El bicameralismo no estaba predeterminado. La Constitución de <strong>1828</strong> marca el punto de inflexión en que el Poder Legislativo queda organizado en Cámara de Senadores y Cámara de Diputados de una manera que abre una continuidad institucional posterior.',
          'La BCN utiliza precisamente 1828 como inicio de la numeración correlativa de períodos legislativos que continúa hasta la actualidad. La lección histórica es importante: <strong>tener dos cámaras fue una solución construida, no una característica natural del Estado chileno</strong>.'
        ],
        sourceIds: ['bcnPeriodos1828', 'senadoHistoria']
      },
      {
        type: 'evidence',
        title: 'Siglo XIX — el Congreso se institucionalizó mucho antes de la política contemporánea',
        paragraphs: [
          'La historia parlamentaria no fue solo una sucesión de constituciones. El trabajo de Iván Obando muestra que entre 1834 y 1924 el Congreso desarrolló tempranamente un sistema especializado de comisiones, mediante experimentación institucional, y que estas llegaron a operar como agencias relativamente especializadas incluso antes de la consolidación de los partidos modernos.',
          'Eso muestra que procedimientos hoy poco visibles —comisiones, personal, reglas internas, informes— forman parte de una acumulación institucional de larga duración.'
        ],
        sourceIds: ['obandoComisionesHistoria']
      },
      {
        type: 'history',
        title: '1891 — ¿qué ocurre cuando Congreso y Presidente disputan el poder?',
        paragraphs: [
          'La Guerra Civil de 1891 terminó con la derrota del presidente José Manuel Balmaceda y abrió un período de fuerte predominio parlamentario. Pero no se aprobó entonces una constitución británica ni apareció un primer ministro: el nuevo equilibrio operó mediante reformas previas e interpretación parlamentaria de la <strong>Constitución de 1833</strong>.',
          'Las prácticas de censura y la dependencia política de los gabinetes respecto de mayorías cambiantes produjeron una intensa rotación ministerial. Al mismo tiempo, el período mantuvo regularidad institucional y electoral y vio una ampliación gradual del sistema de partidos y de los grupos que ingresaban a la política.'
        ],
        sourceIds: ['bcnParlamentario1891', 'memoriaParlamentaria']
      },
      {
        type: 'debate',
        title: '1891–1925 — evitar una historia en que “demasiado Congreso” explica todo',
        paragraphs: [
          'Una tradición historiográfica subraya inmovilismo, rotativa ministerial, participación electoral restringida, oligarquización y debilidad ejecutiva. Esos rasgos cuentan con abundante evidencia y forman parte de la crítica histórica al período.',
          'Pero una narración que reduzca toda la etapa a fracaso parlamentario es demasiado simple. También existieron estabilidad relativa, continuidad constitucional, desarrollo organizacional y ampliación progresiva de actores políticos. El sitio presentará el período como una experiencia discutida, no como demostración automática de que un Congreso fuerte sea bueno o malo.'
        ],
        sourceIds: ['memoriaParlamentaria', 'bcnParlamentario1891']
      },
      {
        type: 'history',
        title: '1925 — ¿cómo fiscalizar sin que el gabinete dependa de la Cámara?',
        paragraphs: [
          'La Constitución de 1925 buscó terminar con las prácticas parlamentarias y reinstalar un sistema presidencialista más definido. El Congreso continuó siendo bicameral, pero el Gobierno dejó de depender políticamente de la confianza parlamentaria en la forma desarrollada durante el período anterior.',
          'El nuevo orden no produjo estabilidad inmediata: hubo autoritarismo, un Congreso designado durante Ibáñez y nuevas interrupciones hasta 1932. Desde entonces y hasta 1973, sin embargo, el Congreso operó durante décadas dentro de un sistema de partidos competitivo y de expansión de la ciudadanía.'
        ],
        sourceIds: ['bcnConstitucion1925', 'bcnHistoria1925']
      },
      {
        type: 'history',
        title: '1973 — ¿puede haber legislación sin un parlamento democrático?',
        paragraphs: [
          'Tras el golpe de Estado de septiembre de 1973, el Decreto Ley N° 27 disolvió el Congreso Nacional y puso fin a las funciones de sus parlamentarios. Durante el régimen militar la Junta asumió funciones legislativas y constituyentes dentro de una ruptura radical de la institucionalidad democrática.',
          'Chile continuó produciendo normas generales. Pero desaparecieron el Congreso electivo, la representación plural, la oposición parlamentaria y los procedimientos ordinarios de competencia democrática. Esta diferencia permite enseñar algo esencial: <strong>producir legislación no basta para definir un parlamento democrático</strong>.'
        ],
        sourceIds: ['dl27Congreso', 'bcnHistoriaDictadura']
      },
      {
        type: 'history',
        title: '1990 — restaurar el Congreso no significó volver exactamente a 1973',
        paragraphs: [
          'Las elecciones parlamentarias de diciembre de 1989 hicieron posible la reapertura del Congreso el <strong>11 de marzo de 1990</strong>. Volvieron la Cámara y el Senado electivos como centros de representación, legislación y oposición democrática.',
          'Pero la arquitectura no era la anterior a 1973. La Cámara tenía 120 integrantes electos y el Senado combinaba <strong>38 senadores electos y 9 designados</strong>, dentro del orden constitucional de 1980. La transición restauró competencia democrática y representación parlamentaria sin borrar de inmediato todas las instituciones heredadas.'
        ],
        sourceIds: ['bcnReapertura1990']
      },
      {
        type: 'history',
        title: '2005–2006 — ¿qué cambia cuando todos los senadores pasan a ser electos?',
        paragraphs: [
          'La reforma constitucional de 2005 eliminó las figuras de senadores designados y vitalicios, reforzó instrumentos de fiscalización de la Cámara e introdujo otras modificaciones relevantes. Desde el <strong>11 de marzo de 2006</strong>, el Senado quedó compuesto enteramente por miembros elegidos mediante sufragio.',
          'La continuidad del nombre “Senado” escondía así una transformación democrática importante: dejó de existir una categoría de integrantes que accedían al cargo por mecanismos distintos de una elección popular.'
        ],
        sourceIds: ['bcnReforma2005']
      },
      {
        type: 'history',
        title: '2015 — ¿qué cambia cuando cambia la regla electoral?',
        paragraphs: [
          'La Ley N° 20.840 reemplazó el sistema binominal por una estructura proporcional inclusiva, reorganizó los territorios electorales y aumentó la Cámara de 120 a <strong>155 integrantes distribuidos en 28 distritos</strong>. El Senado avanzó gradualmente hacia su composición actual de 50 escaños.',
          'El cambio no fue meramente administrativo. Alterar cuántas personas se eligen en cada territorio modifica las condiciones de competencia, la proporcionalidad y los incentivos para partidos y candidatos. Por eso una reforma electoral puede transformar también la forma en que después funciona el Congreso.'
        ],
        sourceIds: ['bcnReforma2015']
      },
      {
        type: 'myth',
        title: 'Cuatro formas de contar mal la historia del Congreso',
        bullets: [
          '<strong>“Chile siempre tuvo el mismo Congreso bicameral”.</strong> No. Hubo experimentación inicial y la estructura, composición y elección de las cámaras cambió repetidamente.',
          '<strong>“La República Parlamentaria fue igual al parlamentarismo británico”.</strong> No. Funcionó mediante prácticas propias dentro de la Constitución de 1833.',
          '<strong>“Entre 1973 y 1990 no hubo leyes, porque no había Congreso”.</strong> Sí hubo producción normativa; lo que faltó fue un parlamento democrático electivo y plural.',
          '<strong>“En 1990 simplemente volvió el Congreso anterior”.</strong> No. La institución reabrió bajo reglas constitucionales y electorales diferentes y con senadores no electos.'
        ],
        sourceIds: ['bcnPeriodos1828', 'memoriaParlamentaria', 'bcnHistoriaDictadura', 'bcnReapertura1990']
      },
      {
        type: 'case',
        title: 'La futura línea de tiempo no será una galería de fechas',
        paragraphs: [
          'Cada hito del sitio debería abrir una pregunta: <strong>1811, quién representa; 1828, por qué dos cámaras; 1891, cómo se distribuye el poder; 1925, cómo se reconstruye el presidencialismo; 1973, qué distingue legislación de parlamento democrático; 1990, qué significa restaurar; 2005, quién puede integrar legítimamente el Senado; 2015, cómo las reglas electorales cambian la representación</strong>.',
          'La cronología permitirá además saltar desde el pasado hacia la institución actual correspondiente. Historia y funcionamiento contemporáneo serán dos formas de mirar el mismo objeto, no dos secciones desconectadas.'
        ],
        sourceIds: ['bcnHistoria1811', 'bcnPeriodos1828', 'bcnParlamentario1891', 'bcnConstitucion1925', 'dl27Congreso', 'bcnReapertura1990', 'bcnReforma2005', 'bcnReforma2015']
      }
    ],
    sourceIds: ['bcnHistoria1811', 'senadoHistoria', 'bcnPeriodos1828', 'obandoComisionesHistoria', 'bcnParlamentario1891', 'memoriaParlamentaria', 'bcnConstitucion1925', 'bcnHistoria1925', 'dl27Congreso', 'bcnHistoriaDictadura', 'bcnReapertura1990', 'bcnReforma2005', 'bcnReforma2015']
  };

  const question = data.featuredQuestions.find((item) => item.id === 'historia-congreso');
  if (question) {
    question.title = '¿Cómo llegamos al Congreso actual?';
    question.summary = 'Una historia de representación, bicameralismo, presidencialismo, quiebres democráticos y reformas desde 1811.';
    question.status = 'ready';
  }
})();
