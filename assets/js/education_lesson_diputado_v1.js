(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    camaraFuncionesParlamentarios: {
      label: '¿Cuáles son las funciones que cumplen las y los parlamentarios?',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://camara.cl/formacion_ciudadana/faq.aspx',
      note: 'La Cámara distingue función legislativa, control del Gobierno, fiscalización exclusiva de diputados, designaciones y representación territorial.'
    },
    camaraGlosarioFunciones: {
      label: 'Glosario legislativo · fiscalización y distrito',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/formacion_Ciudadana/glosario.aspx',
      note: 'Fuente institucional sobre distrito, fiscalización y conceptos parlamentarios relacionados.'
    },
    locArticulo9: {
      label: 'Ley Orgánica Constitucional del Congreso · artículo 9',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=30289&idParte=8535743&idVersion=2016-01-05',
      note: 'Permite que comisiones o parlamentarios debidamente individualizados soliciten informes y antecedentes específicos a determinados organismos y entidades, con límites legales.'
    },
    trabajoDistritalReglamento: {
      label: 'Reglamento de la Cámara · trabajo distrital',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/doc/leyes_normas/reglamento.pdf',
      note: 'El Reglamento reserva periódicamente tiempo para trabajo distrital, mostrando que la función representativa no se reduce al trabajo de Sala.'
    }
  });

  data.lessons['que-puede-hacer-un-diputado'] = {
    title: '¿Qué puede hacer realmente un diputado?',
    unit: 'participacion',
    status: 'ready',
    readingTime: '9–12 min',
    intro: 'Un diputado participa en una institución colegiada: puede proponer, deliberar, votar, solicitar antecedentes y representar territorialmente, pero muchas decisiones requieren a la Cámara completa y otras pertenecen al Ejecutivo, los tribunales, municipios u organismos administrativos.',
    keyPoints: [
      'Un diputado puede participar en la elaboración de leyes mediante debate, voto, determinadas mociones e indicaciones, dentro de los límites constitucionales.',
      'Puede integrar comisiones y participar en el estudio detallado de proyectos y otros asuntos parlamentarios.',
      'Puede solicitar determinados informes y antecedentes a organismos públicos bajo las reglas de la Ley Orgánica del Congreso.',
      'La representación incluye contacto y trabajo territorial; la Cámara reserva tiempo institucional para trabajo distrital.',
      'Muchas facultades de fiscalización y decisión son colectivas: un diputado individual no equivale a la Cámara de Diputadas y Diputados.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'La intuición: un diputado tiene herramientas, no un poder general sobre el Estado',
        paragraphs: [
          'Un diputado no es un pequeño gobierno de su distrito. No administra hospitales, municipios o ministerios; no dicta sentencias y no puede transformar por sí solo una propuesta en ley. Su poder opera dentro de una <strong>institución colegiada</strong> y mediante herramientas constitucionales, legales y reglamentarias determinadas.',
          'Eso no significa que el cargo sea impotente. Puede intervenir en legislación, representación, obtención de información, fiscalización y organización parlamentaria. La clave es distinguir qué puede hacer <strong>personalmente</strong>, qué necesita apoyo de otros parlamentarios y qué simplemente pertenece a otra institución.'
        ],
        sourceIds: ['camaraFuncionesParlamentarios', 'constitucion46']
      },
      {
        type: 'institution',
        title: 'Puede legislar, pero no hacer una ley individualmente',
        paragraphs: [
          'Un diputado puede debatir y votar proyectos, presentar una <span data-edu-term="mocion">moción</span> dentro de las materias en que existe iniciativa parlamentaria y formular <span data-edu-term="indicacion">indicaciones</span> bajo las reglas correspondientes. La Constitución limita, sin embargo, qué materias pueden ser iniciadas o modificadas por parlamentarios.',
          'La aprobación de una ley es una decisión institucional que involucra comisiones, Sala, la otra cámara y al Presidente de la República según el procedimiento aplicable. Por eso “el diputado X hizo esta ley” puede ser una forma coloquial de atribuir protagonismo, pero no describe literalmente cómo funciona la potestad legislativa.'
        ],
        sourceIds: ['constitucion65', 'reglamentoDiscusiones', 'bcnProcesoLey']
      },
      {
        type: 'institution',
        title: 'Puede trabajar en comisión y modificar el proceso antes de la Sala',
        paragraphs: [
          'Los diputados integran comisiones donde se estudian proyectos, se reciben antecedentes, se escuchan actores y se adoptan decisiones previas a muchas votaciones de Sala. Una parte importante de la actividad legislativa ocurre por tanto fuera del hemiciclo.',
          'Integrar una comisión tampoco convierte al parlamentario en autoridad ejecutiva sobre el sector que estudia. La Comisión de Salud puede examinar legislación sanitaria y recibir información; no administra el sistema de salud.'
        ],
        sourceIds: ['locCongresoLey', 'reglamentoDiscusiones']
      },
      {
        type: 'institution',
        title: 'Puede pedir información al Estado bajo reglas específicas',
        paragraphs: [
          'El artículo 9 de la Ley Orgánica Constitucional del Congreso obliga a determinados organismos y entidades a proporcionar informes y antecedentes específicos solicitados por comisiones o por parlamentarios debidamente individualizados en sesión de Sala o de comisión, dentro de los límites y reservas que establece la ley.',
          'Esta herramienta es relevante para representación y control: un problema planteado por ciudadanos puede llevar a un parlamentario a pedir antecedentes y hacer visible una situación. Pero <strong>pedir información no equivale a ordenar una solución</strong> ni transforma al diputado en superior jerárquico del servicio requerido.'
        ],
        sourceIds: ['locArticulo9']
      },
      {
        type: 'institution',
        title: 'Puede representar territorialmente y mantener contacto con la ciudadanía',
        paragraphs: [
          'La propia Cámara incluye la representación de ciudadanos de distritos entre las funciones parlamentarias y menciona reuniones con ciudadanía y autoridades locales, regionales y nacionales. El Reglamento reserva además períodos para trabajo distrital.',
          'Esta dimensión explica por qué recibir organizaciones, visitar el territorio o canalizar información hacia organismos públicos puede formar parte legítima del trabajo representativo. Sin embargo, la existencia de actividad territorial no permite inferir automáticamente su calidad ni sus efectos.'
        ],
        sourceIds: ['camaraFuncionesParlamentarios', 'trabajoDistritalReglamento', 'camaraRepresentacion']
      },
      {
        type: 'institution',
        title: 'Fiscalizar es una función de la Cámara: el diputado activa herramientas dentro de reglas colectivas',
        paragraphs: [
          'La Constitución entrega a la <strong>Cámara</strong> la atribución exclusiva de fiscalizar los actos del Gobierno. Un diputado puede promover o participar en esas actuaciones, pero varios instrumentos exigen apoyos adicionales. Por ejemplo, una solicitud constitucional de antecedentes al Gobierno requiere el apoyo de un tercio de los miembros presentes de la Cámara.',
          'La diferencia es importante: decir que “un diputado puede fiscalizar” es pedagógicamente útil si entendemos que actúa dentro de herramientas institucionales; sería incorrecto imaginar que cada diputado posee individualmente todas las potestades de la Cámara.'
        ],
        sourceIds: ['constitucion52', 'camaraGlosarioFunciones']
      },
      {
        type: 'case',
        title: 'Cuando una persona lleva un problema a su diputado',
        paragraphs: [
          'Supongamos que vecinos denuncian meses de retraso en una obra pública. El diputado puede escuchar, reunir antecedentes, solicitar información por los canales parlamentarios correspondientes, plantear el asunto en espacios institucionales o promover acciones de fiscalización cuando existan fundamentos y apoyos suficientes.',
          'Lo que normalmente no puede hacer es ordenar al organismo ejecutor que termine la obra el martes, reasignar unilateralmente su presupuesto o sancionar administrativamente a un funcionario. El valor de la representación puede estar en <strong>abrir información, activar control y elevar políticamente un problema</strong>, no necesariamente en sustituir al órgano competente.'
        ],
        sourceIds: ['locArticulo9', 'constitucion52']
      },
      {
        type: 'myth',
        title: 'Qué no puede prometer razonablemente un diputado',
        bullets: [
          '<strong>“Yo voy a construir este hospital”.</strong> Un parlamentario puede impulsar legislación, presupuesto o fiscalización según corresponda, pero no ejecuta directamente una obra pública.',
          '<strong>“Voy a ordenar que te den este beneficio”.</strong> Los beneficios administrativos se rigen por autoridades, requisitos y procedimientos propios; el diputado no reemplaza al servicio competente.',
          '<strong>“Voy a resolver tu causa judicial”.</strong> Un parlamentario no puede decidir una controversia que corresponde a los tribunales.',
          '<strong>“Voy a presentar una ley sobre cualquier materia”.</strong> La Constitución reserva materias a la iniciativa exclusiva del Presidente.',
          '<strong>“Yo aprobé esta ley”.</strong> Puede haber tenido una intervención importante, pero la aprobación es resultado de decisiones colectivas e interinstitucionales.'
        ],
        sourceIds: ['constitucion65', 'bcnProcesoLey', 'camaraFuncionesParlamentarios']
      },
      {
        type: 'evidence',
        title: 'Por qué no conviene reducir el trabajo parlamentario a una sola cifra',
        paragraphs: [
          'Las distintas herramientas cumplen funciones diferentes. Presentar mociones, votar, intervenir en comisión, representar territorialmente o solicitar información no son unidades intercambiables de “productividad”. Sumarlas en un índice único obligaría a decidir normativamente cuánto vale cada una.',
          'Por eso este sitio mostrará dimensiones separadas y evidencia reconstruible. Una persona puede evaluar qué considera más importante sin que la plataforma invente una medida universal de “mejor diputado”.'
        ],
        sourceIds: ['parliamentaryFunctions2025']
      },
      {
        type: 'debate',
        title: 'La frontera entre representación, intermediación y particularismo',
        paragraphs: [
          'Atender problemas ciudadanos puede ser una forma legítima de constituency service y de conexión representativa. Pero la teoría y la evidencia comparada también preguntan cuándo la intermediación se vuelve excesivamente particularista, desigual o electoralista.',
          'La existencia de esa discusión es otra razón para no premiar automáticamente el volumen de gestiones territoriales. Para evaluar esa dimensión necesitamos saber qué se hizo, para qué, mediante qué instrumento y con qué resultado.'
        ],
        sourceIds: ['chileConstituencyService2023']
      }
    ],
    sourceIds: ['camaraFuncionesParlamentarios', 'camaraGlosarioFunciones', 'constitucion65', 'reglamentoDiscusiones', 'bcnProcesoLey', 'locCongresoLey', 'locArticulo9', 'trabajoDistritalReglamento', 'camaraRepresentacion', 'constitucion52', 'parliamentaryFunctions2025', 'chileConstituencyService2023']
  };

  if (!data.featuredQuestions.some((item) => item.id === 'que-puede-hacer-un-diputado')) {
    data.featuredQuestions.push({
      id: 'que-puede-hacer-un-diputado',
      unit: 'participacion',
      title: '¿Qué puede hacer realmente un diputado?',
      summary: 'Qué herramientas tiene, qué decisiones requieren a la Cámara y qué asuntos corresponden a otras autoridades.',
      status: 'ready'
    });
  }
})();
