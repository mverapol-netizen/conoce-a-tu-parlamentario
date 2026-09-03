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
      { id: 'para-que-existe', unit: 'representacion', title: '¿Para qué existe el Congreso?', summary: 'Representación, decisiones colectivas, deliberación y control del poder.', status: 'research' },
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
      'para-que-existe': { title: '¿Para qué existe el Congreso?', unit: 'representacion', status: 'research', intro: 'Una democracia necesita instituciones que representen diferencias, permitan tomar decisiones colectivas y distribuyan el ejercicio del poder.' },
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
