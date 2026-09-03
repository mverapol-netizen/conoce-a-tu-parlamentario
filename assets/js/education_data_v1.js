(() => {
  window.CONGRESS_EDUCATION = {
    version: '0.1',
    updatedAt: '2026-09-03',
    status: 'internal-preview',
    epistemicTypes: {
      institution: { label: 'Institución', description: 'Regla, atribución o estructura respaldada por fuentes normativas o institucionales.' },
      evidence: { label: 'Evidencia', description: 'Hallazgo empírico proveniente de datos o investigación académica.' },
      debate: { label: 'Debate', description: 'Pregunta interpretativa, causal o normativa con posiciones o evidencia no concluyente.' },
      history: { label: 'Historia', description: 'Origen, cambio o antecedente histórico de una institución.' },
      myth: { label: 'Mito frecuente', description: 'Confusión habitual que conviene corregir de manera precisa.' }
    },
    sources: {
      constitucion46: {
        label: 'Constitución Política de la República · artículo 46 y capítulo V',
        publisher: 'Biblioteca del Congreso Nacional de Chile',
        url: 'https://www.bcn.cl/leychile/navegar?idNorma=242302&idParte=8563521',
        note: 'Fuente normativa para composición bicameral y atribuciones constitucionales del Congreso.'
      },
      constitucion52: {
        label: 'Constitución Política · artículo 52',
        publisher: 'Biblioteca del Congreso Nacional de Chile',
        url: 'https://www.bcn.cl/leychile/navegar?idNorma=242302&idParte=8563528&idVersion=2021-10-25',
        note: 'Fuente normativa para la atribución exclusiva de la Cámara de fiscalizar los actos del Gobierno.'
      },
      camaraFunciones: {
        label: 'Formación ciudadana · preguntas frecuentes de la Cámara',
        publisher: 'Cámara de Diputadas y Diputados de Chile',
        url: 'https://www.camara.cl/formacion_ciudadana/faq.aspx',
        note: 'Fuente institucional que presenta las funciones de legislar, fiscalizar y representar y distingue otras funciones parlamentarias.'
      },
      senadoFunciones: {
        label: 'Funciones y atribuciones del Senado',
        publisher: 'Senado de la República de Chile',
        url: 'https://www.senado.cl/acerca-del-senado/funciones-del-senado',
        note: 'Fuente institucional sobre participación legislativa, tratados y atribuciones del Senado.'
      },
      senadoAtribuciones: {
        label: 'Atribuciones del Senado',
        publisher: 'Senado de la República de Chile',
        url: 'https://www.senado.cl/acerca-del-senado/funciones-del-senado/atribuciones-del-senado',
        note: 'Detalla atribuciones exclusivas y señala expresamente que el Senado no fiscaliza los actos del Gobierno.'
      },
      parliamentaryFunctions2025: {
        label: 'A conceptual framework for understanding parliamentary skills and competences',
        publisher: 'Parliamentary Affairs · Oxford Academic',
        url: 'https://academic.oup.com/pa/article/78/4/835/8170052',
        note: 'Revisión comparada reciente: representación, legislación y oversight como núcleo, junto a deliberación, presupuesto y otras funciones según cada sistema.'
      },
      urbinatiWarren2008: {
        label: 'The Concept of Representation in Contemporary Democratic Theory',
        publisher: 'Annual Review of Political Science',
        url: 'https://www.annualreviews.org/content/journals/10.1146/annurev.polisci.11.053006.190533',
        note: 'Revisión de teoría democrática sobre representación, constituency, juicio, participación y accountability.'
      },
      sepRepresentation2026: {
        label: 'Political Representation',
        publisher: 'Stanford Encyclopedia of Philosophy',
        url: 'https://plato.stanford.edu/entries/political-representation/',
        note: 'Síntesis conceptual revisada en 2026 sobre los múltiples sentidos de la representación política.'
      }
    },
    units: [
      { id: 'representacion', letter: 'A', title: 'Democracia y representación', summary: 'Para qué existe el Congreso, quién representa a quién y cómo se conectan ciudadanía, territorio y partidos.' },
      { id: 'camaras', letter: 'B', title: 'Cámara y Senado', summary: 'Bicameralismo, composición y atribuciones comunes y exclusivas.' },
      { id: 'ley', letter: 'C', title: 'Cómo se hace una ley', summary: 'Del mensaje o moción a comisiones, trámites, votaciones y promulgación.' },
      { id: 'organizacion', letter: 'D', title: 'Cómo se organiza el Congreso', summary: 'Mesa, comisiones, bancadas, comités, tabla y agenda.' },
      { id: 'fiscalizacion', letter: 'E', title: 'Fiscalización y control', summary: 'Oficios, interpelaciones, investigaciones y límites del control parlamentario.' },
      { id: 'partidos', letter: 'F', title: 'Partidos y poder político', summary: 'Partidos, bancadas, coaliciones, cohesión, disciplina, mayorías y fragmentación.' },
      { id: 'historia', letter: 'G', title: 'Historia del Congreso', summary: 'Una historia de problemas políticos e institucionales desde 1811 hasta hoy.' },
      { id: 'participacion', letter: 'H', title: 'Participación ciudadana', summary: 'Qué puede pedir un ciudadano, cómo seguir un proyecto y a qué institución acudir.' }
    ],
    featuredQuestions: [
      { id: 'para-que-existe', unit: 'representacion', title: '¿Para qué existe el Congreso?', summary: 'Representación, decisiones colectivas, deliberación y control del poder.', status: 'ready' },
      { id: 'quien-me-representa', unit: 'representacion', title: '¿Quién me representa?', summary: 'Distritos, elecciones, partidos y las distintas dimensiones de la representación.', status: 'research' },
      { id: 'como-se-hace-una-ley', unit: 'ley', title: '¿Cómo se convierte una idea en ley?', summary: 'Iniciativa, comisiones, Sala, Senado, modificaciones y promulgación.', status: 'research' },
      { id: 'fiscalizacion', unit: 'fiscalizacion', title: '¿Cómo controla la Cámara al Gobierno?', summary: 'Solicitudes de antecedentes, oficios, interpelaciones y comisiones investigadoras.', status: 'research' },
      { id: 'organizacion-politica', unit: 'organizacion', title: '¿Quién organiza realmente la Cámara?', summary: 'Mesa, partidos, bancadas, comités y comisiones.', status: 'research' },
      { id: 'agenda', unit: 'organizacion', title: '¿Quién decide qué se vota?', summary: 'Tabla, urgencias, prioridades, tiempos y reglas de agenda.', status: 'research' },
      { id: 'historia-congreso', unit: 'historia', title: '¿Cómo llegamos al Congreso actual?', summary: 'Los principales quiebres y transformaciones institucionales de 1811 a 2026.', status: 'research' },
      { id: 'participar', unit: 'participacion', title: '¿Qué puedo hacer como ciudadano?', summary: 'Contactar, seguir proyectos, encontrar comisiones y usar los canales institucionales correctos.', status: 'design' }
    ],
    learningPath: [
      'para-que-existe', 'quien-me-representa', 'camara-y-senado', 'como-se-eligen',
      'como-se-hace-una-ley', 'comisiones', 'fiscalizacion', 'organizacion-politica',
      'agenda', 'mayorias', 'que-puede-hacer-un-diputado', 'participar'
    ],
    lessons: {
      'para-que-existe': {
        title: '¿Para qué existe el Congreso?',
        unit: 'representacion',
        status: 'ready',
        readingTime: '7–9 min',
        intro: 'El Congreso no es solo un lugar donde se votan leyes. En una democracia representativa organiza diferencias políticas, participa en decisiones colectivas y crea formas institucionales de control y rendición de cuentas.',
        keyPoints: [
          'Chile tiene un Congreso bicameral: Cámara de Diputadas y Diputados y Senado.',
          'Ambas cámaras participan en la formación de las leyes, pero no poseen idénticas atribuciones.',
          'Representación, legislación y control forman el núcleo clásico de las funciones parlamentarias; otras funciones dependen del diseño institucional de cada país.',
          'La función política de representar no debe confundirse con una atribución jurídica singular enumerada del mismo modo que fiscalizar.',
          'El Congreso no produce por sí solo todas las leyes: en Chile el Presidente de la República también interviene en su formación.'
        ],
        blocks: [
          {
            type: 'intuition',
            title: 'La intuición: decidir juntos cuando no pensamos igual',
            paragraphs: [
              'Una sociedad democrática contiene desacuerdos reales sobre impuestos, seguridad, derechos, educación, pensiones, medio ambiente y muchas otras materias. El Congreso es una de las instituciones que permite que esas diferencias estén representadas y sean procesadas mediante procedimientos públicos en vez de depender de una sola voluntad.',
              'La idea inicial puede formularse así: <strong>un Congreso democrático representa diferencias, las transforma en decisiones colectivas y distribuye parte del ejercicio del poder</strong>. Esta frase es deliberadamente amplia porque reducir el Congreso a una “fábrica de leyes” dejaría fuera una parte sustantiva de lo que hace.'
            ],
            sourceIds: ['parliamentaryFunctions2025']
          },
          {
            type: 'institution',
            title: 'El punto de partida institucional en Chile',
            paragraphs: [
              'El artículo 46 de la Constitución establece que el Congreso Nacional se compone de dos ramas: la Cámara de Diputadas y Diputados y el Senado. Ambas concurren a la formación de las leyes y poseen además las otras atribuciones que la propia Constitución establece.',
              'Esto obliga a distinguir desde el comienzo entre <strong>Congreso</strong> y <strong>Cámara</strong>. La Cámara es una de las dos ramas del Congreso. El Senado es la otra. Comparten parte de la función legislativa, pero tienen atribuciones exclusivas diferentes.'
            ],
            sourceIds: ['constitucion46', 'senadoFunciones']
          },
          {
            type: 'institution',
            title: 'Las dos cámaras no hacen exactamente lo mismo',
            paragraphs: [
              'La Cámara presenta pedagógicamente la labor de sus integrantes mediante las funciones de legislar, fiscalizar los actos del Gobierno y representar a la ciudadanía. La Constitución, a su vez, reserva a la Cámara la atribución de fiscalizar los actos del Gobierno.',
              'El Senado participa en la formación de las leyes y la aprobación de tratados y posee atribuciones exclusivas propias, entre ellas intervenir en determinadas acusaciones constitucionales y nombramientos. La propia institución señala expresamente que <strong>el Senado no fiscaliza los actos del Gobierno</strong> en el sentido constitucional reservado a la Cámara.'
            ],
            sourceIds: ['camaraFunciones', 'constitucion52', 'senadoAtribuciones']
          },
          {
            type: 'evidence',
            title: 'Una taxonomía analítica más amplia',
            paragraphs: [
              'La literatura comparada suele reconocer tres funciones parlamentarias nucleares: <strong>representación, legislación y oversight o control</strong>. Pero no existe una lista universal que describa del mismo modo a todos los parlamentos. Según el régimen y la constitución, también pueden distinguirse deliberación, presupuesto, formación o control de gobiernos, resolución de reclamos y funciones constitucionales o electorales.',
              'Por eso este sitio utilizará una taxonomía analítica de varias familias —representación, legislación, deliberación y negociación, control, integración institucional y decisiones presupuestarias o de recursos cuando corresponda— sin fingir que todas tienen exactamente el mismo estatus jurídico.'
            ],
            sourceIds: ['parliamentaryFunctions2025']
          },
          {
            type: 'evidence',
            title: 'Representar es más complejo que “hacer lo que quiere el votante”',
            paragraphs: [
              'La teoría democrática contemporánea trata la representación como una relación compleja que involucra elecciones, accountability, definición de quiénes son los representados, juicio político y distintas formas de hacer presentes voces e intereses en la decisión pública.',
              'Por eso la palabra <strong>representar</strong> describe una función democrática fundamental, pero no debe entenderse como una instrucción automática para reproducir cada preferencia individual. Ese problema se desarrolla en la siguiente lección del recorrido.'
            ],
            sourceIds: ['urbinatiWarren2008', 'sepRepresentation2026']
          },
          {
            type: 'myth',
            title: 'Tres confusiones que conviene evitar desde el comienzo',
            bullets: [
              '<strong>“El Congreso hace las leyes solo”.</strong> No. En Chile la formación de la ley implica también al Presidente de la República y, ordinariamente, la interacción entre ambas cámaras.',
              '<strong>“Cámara y Senado son duplicados”.</strong> No. Comparten funciones legislativas, pero su composición y varias atribuciones exclusivas son diferentes.',
              '<strong>“Si una actividad no termina en una ley, no es trabajo parlamentario”.</strong> No. Representación, fiscalización, deliberación, comisiones y otras actuaciones forman parte del funcionamiento parlamentario.'
            ],
            sourceIds: ['constitucion46', 'camaraFunciones', 'senadoAtribuciones']
          },
          {
            type: 'history',
            title: '¿Siempre significó lo mismo ser Congreso?',
            paragraphs: [
              'No. El Congreso chileno ha cambiado de composición, reglas, equilibrio con el Ejecutivo y formas de representación a lo largo de su historia. Por eso las instituciones siempre se explicarán con fecha: el Congreso de 1811, el de 1891, el de 1990 y el actual comparten una genealogía, pero no son institucionalmente idénticos.',
              'La sección histórica reconstruirá esos cambios como problemas políticos —quién representa, cómo se distribuye el poder y cómo se controla al Ejecutivo— y no como una simple lista de efemérides.'
            ],
            sourceIds: []
          },
          {
            type: 'debate',
            title: 'Lo que la definición no resuelve',
            paragraphs: [
              'Saber qué atribuciones tiene el Congreso no resuelve por sí solo preguntas como: ¿cuánto debe pesar el juicio propio de un representante frente a las preferencias de sus electores?, ¿cuánto poder efectivo tiene el Congreso frente al Ejecutivo?, ¿dos cámaras mejoran la representación y la revisión o dificultan innecesariamente las decisiones?, ¿cuánto del trabajo parlamentario ocurre realmente en la deliberación pública?',
              'Estas preguntas no se presentarán como errores que deban corregirse. Son <strong>debates genuinos</strong> de teoría democrática, derecho constitucional y ciencia política que requieren evidencia y argumentos rivales.'
            ],
            sourceIds: ['urbinatiWarren2008', 'parliamentaryFunctions2025']
          }
        ],
        sourceIds: ['constitucion46', 'constitucion52', 'camaraFunciones', 'senadoFunciones', 'senadoAtribuciones', 'parliamentaryFunctions2025', 'urbinatiWarren2008', 'sepRepresentation2026']
      },
      'quien-me-representa': { title: '¿Quién representa a quién?', unit: 'representacion', status: 'research', intro: 'Ser representante no significa reproducir mecánicamente cada preferencia individual: territorio, partidos, autorización, juicio y rendición de cuentas se superponen.' },
      'camara-y-senado': { title: 'Cámara y Senado', unit: 'camaras', status: 'research', intro: 'Chile tiene un Congreso bicameral: ambas cámaras participan en la legislación, pero no tienen idéntica composición ni las mismas atribuciones.' },
      'como-se-eligen': { title: '¿Cómo se eligen los parlamentarios?', unit: 'representacion', status: 'planned', intro: 'El voto por una candidatura opera dentro de distritos, listas y una fórmula proporcional de asignación de escaños.' },
      'como-se-hace-una-ley': { title: '¿Cómo se hace una ley?', unit: 'ley', status: 'research', intro: 'Legislar es un proceso: una propuesta puede ser estudiada, modificada, aprobada o rechazada en distintas etapas antes de llegar eventualmente a ser ley.' },
      'comisiones': { title: '¿Qué hacen las comisiones?', unit: 'organizacion', status: 'research', intro: 'Las comisiones permiten estudiar asuntos en grupos más pequeños, pero también son espacios de especialización, negociación, organización partidaria y representación territorial.' },
      'fiscalizacion': { title: '¿Cómo fiscaliza la Cámara?', unit: 'fiscalizacion', status: 'research', intro: 'Fiscalizar significa examinar actos del Gobierno, obtener información y exigir explicaciones; no equivale a gobernar ni a juzgar.' },
      'organizacion-politica': { title: 'Partidos, bancadas y comités', unit: 'partidos', status: 'research', intro: 'Partido, bancada, comité parlamentario, coalición y oficialismo u oposición son capas distintas de organización política e institucional.' },
      'agenda': { title: 'Agenda y tabla', unit: 'organizacion', status: 'research', intro: 'El poder parlamentario no consiste solo en votar: decidir qué asuntos llegan a discusión, cuándo y en qué orden también importa.' },
      'mayorias': { title: 'Mayorías y quórums', unit: 'organizacion', status: 'planned', intro: 'No todas las decisiones parlamentarias requieren la misma clase de mayoría ni se calculan sobre el mismo universo de integrantes.' },
      'que-puede-hacer-un-diputado': { title: '¿Qué puede hacer realmente un diputado?', unit: 'participacion', status: 'planned', intro: 'Un diputado participa en decisiones colegiadas y dispone de herramientas propias, pero no administra servicios públicos ni reemplaza a otras autoridades.' },
      'participar': { title: '¿Cómo puede participar un ciudadano?', unit: 'participacion', status: 'planned', intro: 'Comprender el Congreso debe terminar en capacidad de acción: saber a quién contactar, cómo seguir un proyecto y qué canales institucionales existen.' }
    },
    glossary: [
      { term: 'Bancada', slug: 'bancada', unit: 'partidos', short: 'Expresión parlamentaria colectiva asociada a un partido. No debe confundirse automáticamente con un comité parlamentario.' },
      { term: 'Comité parlamentario', slug: 'comite-parlamentario', unit: 'partidos', short: 'Unidad reglamentaria mediante la cual diputados se organizan y se relacionan con la Mesa; puede reunir partidos pequeños o independientes.' },
      { term: 'Comisión', slug: 'comision', unit: 'organizacion', short: 'Grupo más pequeño de parlamentarios que estudia determinadas materias o cumple una función específica dentro del Congreso.' },
      { term: 'Comisión mixta', slug: 'comision-mixta', unit: 'ley', short: 'Instancia integrada por diputados y senadores que interviene en ciertos desacuerdos entre ambas cámaras u otras funciones bicamerales específicas.' },
      { term: 'Indicación', slug: 'indicacion', unit: 'ley', short: 'Propuesta para agregar, suprimir o modificar parte de un proyecto durante su tramitación, dentro de las reglas constitucionales y reglamentarias aplicables.' },
      { term: 'Mensaje', slug: 'mensaje', unit: 'ley', short: 'Proyecto de ley iniciado por el Presidente de la República.' },
      { term: 'Moción', slug: 'mocion', unit: 'ley', short: 'Proyecto de ley iniciado por parlamentarios dentro de las materias en que tienen iniciativa.' },
      { term: 'Quórum', slug: 'quorum', unit: 'organizacion', short: 'Regla que determina cuántos apoyos o integrantes se requieren para adoptar válidamente una decisión.' },
      { term: 'Tabla', slug: 'tabla', unit: 'organizacion', short: 'Agenda formal de asuntos que serán tratados en una sesión según las reglas y prioridades aplicables.' },
      { term: 'Tercer trámite', slug: 'tercer-tramite', unit: 'ley', short: 'Etapa en que la cámara de origen se pronuncia sobre modificaciones introducidas por la cámara revisora.' },
      { term: 'Urgencia', slug: 'urgencia', unit: 'ley', short: 'Facultad presidencial que da prioridad temporal a la tramitación de un proyecto; no equivale a su aprobación.' }
    ]
  };
})();
