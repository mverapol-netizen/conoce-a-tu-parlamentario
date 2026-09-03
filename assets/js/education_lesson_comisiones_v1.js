(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    camaraComisionesActual: {
      label: 'Comisiones de la Cámara de Diputadas y Diputados',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/legislacion/comisiones/comisiones_permanentes.aspx',
      note: 'Portal institucional actual de comisiones, con integración, sesiones, proyectos, citaciones, resultados, documentos, audiencias públicas, oficios e informes.'
    },
    camaraFaqComisiones: {
      label: 'Formación ciudadana · comisiones permanentes',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/formacion_ciudadana/faq.aspx',
      note: 'Explica que las comisiones permanentes legislativas estudian y tramitan proyectos por áreas temáticas y que cada una está integrada por 13 diputadas y diputados.'
    },
    locComisiones22: {
      label: 'Ley Orgánica Constitucional del Congreso · trabajo de las comisiones',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=30289',
      note: 'Regula el informe de proyectos por comisiones y faculta a estas para reunir antecedentes, requerir comparecencias, asesorarse por especialistas, solicitar informes y oír instituciones o personas.'
    },
    reglamentoComisiones: {
      label: 'Reglamento de la Cámara · integración de comisiones',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/doc/leyes_normas/reglamento.pdf',
      note: 'Regula integración y funcionamiento; los partidos están representados proporcionalmente y la Cámara elige integrantes a propuesta de la Mesa conforme a las reglas internas.'
    },
    mimicaNaviaComisiones2022: {
      label: 'Who Gets What Committee? Committee Assignments in the Chilean Chamber of Deputies, 1990–2018',
      publisher: 'Revista de Ciencia Política',
      url: 'https://www.scielo.cl/scielo.php?pid=S0718-090X2022005000107&script=sci_arttext',
      note: 'Encuentra que especialización profesional, características económicas del distrito e issue ownership partidario ayudan a explicar asignaciones a comisiones en Chile.'
    },
    camaraComisionSalud: {
      label: 'Comisión de Salud · actividad institucional',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/legislacion/comisiones/comisiones_permanentes.aspx',
      note: 'El portal de comisiones permite abrir cada comisión y consultar integrantes, sesiones, proyectos, audiencias, documentos, oficios e informes como ejemplo de actividad real.'
    }
  });

  data.lessons['comisiones'] = {
    title: '¿Qué hacen las comisiones?',
    unit: 'organizacion',
    status: 'ready',
    readingTime: '10–13 min',
    intro: 'Gran parte del trabajo parlamentario ocurre antes de la Sala. Las comisiones permiten estudiar asuntos en grupos más pequeños, reunir información, escuchar actores y preparar decisiones, pero también reflejan especialización, intereses territoriales y organización partidaria.',
    keyPoints: [
      'Las comisiones legislativas permanentes de la Cámara están formadas por 13 diputadas y diputados y estudian materias temáticas determinadas.',
      'Pueden reunir antecedentes, solicitar comparecencias e informes, asesorarse por especialistas y oír a instituciones y personas.',
      'Su integración no es una selección puramente técnica: los partidos tienen representación proporcional y operan reglas de asignación institucional.',
      'Comisión permanente, comisión investigadora y comisión mixta son instituciones distintas, con propósitos y reglas diferentes.',
      'La evidencia chilena sugiere que especialización profesional, intereses del distrito y prioridades partidarias pueden influir simultáneamente en quién integra qué comisión.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'La intuición: el Congreso no ocurre solo en la Sala',
        paragraphs: [
          'La imagen más visible del Congreso es el hemiciclo lleno de parlamentarios votando. Pero muchas decisiones llegan a esa instancia después de un trabajo previo de estudio, discusión y modificación en grupos más pequeños. Las <span data-edu-term="comision">comisiones</span> existen, entre otras razones, para permitir esa división del trabajo.',
          'Una comisión legislativa puede revisar antecedentes, escuchar a autoridades y especialistas, examinar artículos y preparar un informe. Por eso mirar solamente las votaciones de Sala entrega una imagen real pero incompleta de la actividad parlamentaria.'
        ],
        sourceIds: ['camaraFaqComisiones', 'locComisiones22']
      },
      {
        type: 'institution',
        title: 'Comisiones permanentes: especialización temática dentro de la Cámara',
        paragraphs: [
          'La Cámara organiza comisiones permanentes que estudian y tramitan proyectos y otros asuntos según áreas temáticas. Las comisiones legislativas están integradas por <strong>13 diputadas y diputados</strong>. Existen áreas como Salud, Educación, Hacienda, Constitución, Seguridad y otras materias del trabajo legislativo.',
          'Conviene ser cuidadosos con el número total: la información institucional distingue las comisiones legislativas temáticas de otras comisiones permanentes, internas o subcomisiones que también aparecen en el portal. Por eso el sitio no reducirá toda la arquitectura a una cifra única sin especificar la categoría que está contando.'
        ],
        sourceIds: ['camaraFaqComisiones', 'camaraComisionesActual']
      },
      {
        type: 'institution',
        title: 'Qué puede hacer una comisión para estudiar un asunto',
        paragraphs: [
          'La Ley Orgánica Constitucional del Congreso permite que las comisiones reúnan los antecedentes que estimen necesarios para informar un proyecto. También pueden solicitar la comparecencia de determinados funcionarios que puedan ilustrar el debate, pedir informes, asesorarse por especialistas y oír a instituciones o personas cuya opinión consideren conveniente.',
          'Esto convierte a la comisión en un punto institucional de entrada de información hacia el Congreso. Una sesión puede reunir conocimiento administrativo, técnico, académico, sectorial y ciudadano. <strong>Escuchar a un actor, sin embargo, no significa que ese actor controle la decisión final.</strong>'
        ],
        sourceIds: ['locComisiones22']
      },
      {
        type: 'institution',
        title: 'La composición también es política',
        paragraphs: [
          'Las comisiones no son paneles de expertos seleccionados únicamente por sus credenciales profesionales. El Reglamento organiza su integración dentro de la representación política de la Cámara: los partidos representados participan proporcionalmente y la elección de integrantes opera mediante procedimientos institucionales en los que intervienen la Mesa y las estructuras parlamentarias correspondientes.',
          'Eso tiene sentido democrático: las comisiones preparan decisiones políticas y deben reflejar la pluralidad de la corporación. Pero significa también que su composición no puede entenderse únicamente como una división tecnocrática del conocimiento.'
        ],
        sourceIds: ['reglamentoComisiones']
      },
      {
        type: 'evidence',
        title: 'Especialización, territorio y partido pueden operar al mismo tiempo',
        paragraphs: [
          'La investigación de Mimica y Navia sobre asignaciones de comisión en la Cámara chilena entre 1990 y 2018 encuentra evidencia para varias explicaciones simultáneas. La profesión de los legisladores ayuda a predecir algunas asignaciones: por ejemplo, determinados perfiles profesionales aparecen con mayor probabilidad en comisiones relacionadas con su expertise.',
          'También importan características de los distritos: la relevancia territorial de actividades como minería, agricultura o pesca se relaciona con la presencia en las comisiones correspondientes. Y en algunas materias aparecen patrones compatibles con <em>issue ownership</em> partidario. Por eso no deberíamos elegir artificialmente entre una lógica “técnica”, “territorial” o “partidaria”: pueden coexistir.'
        ],
        sourceIds: ['mimicaNaviaComisiones2022']
      },
      {
        type: 'institution',
        title: 'No todas las comisiones son la misma institución',
        paragraphs: [
          'Una <strong>comisión permanente</strong> estudia de manera estable determinadas áreas de legislación y otros asuntos. Una <strong>Comisión Especial Investigadora</strong>, en cambio, se crea temporalmente para reunir información sobre determinados actos del Gobierno dentro de la función fiscalizadora de la Cámara.',
          'Una <span data-edu-term="comision-mixta">comisión mixta</span> reúne diputados y senadores para determinadas funciones bicamerales, entre ellas resolver ciertos desacuerdos entre ambas cámaras. La Comisión Especial Mixta de Presupuestos posee, a su vez, una función específica en el examen presupuestario. Compartir la palabra “comisión” no vuelve equivalentes a estas instituciones.'
        ],
        sourceIds: ['locComisiones22', 'camaraCEI', 'bcnProcesoLey']
      },
      {
        type: 'institution',
        title: 'Hacienda muestra por qué comisión no equivale a tema',
        paragraphs: [
          'La Comisión de Hacienda cumple una función transversal respecto de proyectos con incidencia presupuestaria o financiera. Un proyecto de salud, vivienda o educación puede pasar por Hacienda porque genera consecuencias fiscales.',
          'Por eso sería un error clasificar automáticamente como “economía” todo proyecto que haya pasado por esa comisión. La trayectoria institucional de un proyecto entrega señales valiosas, pero no reemplaza el análisis de su contenido.'
        ],
        sourceIds: ['locComisiones22']
      },
      {
        type: 'case',
        title: 'Míralo funcionando: una comisión deja un rastro público',
        paragraphs: [
          'El portal actual de la Cámara permite entrar a una comisión concreta y consultar integrantes, sesiones, proyectos de ley, citaciones, resultados, documentos, audiencias públicas, oficios enviados e informes. Esa estructura muestra que el trabajo de comisión es mucho más que una lista de miembros.',
          'La futura página de cada comisión en este sitio debería reutilizar ese rastro para responder preguntas ciudadanas: <strong>qué estudia, quiénes la integran, quién la preside, qué proyectos tiene, cuándo sesiona, a quién ha escuchado y qué decisiones ha adoptado</strong>.'
        ],
        sourceIds: ['camaraComisionesActual', 'camaraComisionSalud']
      },
      {
        type: 'myth',
        title: 'Cuatro confusiones frecuentes sobre comisiones',
        bullets: [
          '<strong>“La comisión es un grupo neutral de expertos”.</strong> No. Puede existir especialización, pero sus integrantes son representantes políticos y su composición también refleja partidos y reglas institucionales.',
          '<strong>“Si un proyecto pasó por Hacienda, entonces su tema es economía”.</strong> No. Hacienda cumple además una función transversal sobre incidencia financiera y presupuestaria.',
          '<strong>“Si una organización fue escuchada, entonces influyó en el resultado”.</strong> La audiencia prueba acceso y participación en una instancia, no causalidad sobre el texto final.',
          '<strong>“El trabajo importante ocurre cuando llega a Sala”.</strong> La Sala es decisiva, pero una gran parte del estudio, modificación y producción de información ocurre previamente en comisión.'
        ],
        sourceIds: ['locComisiones22', 'reglamentoComisiones', 'mimicaNaviaComisiones2022']
      },
      {
        type: 'debate',
        title: '¿Para qué sirven políticamente las comisiones?',
        paragraphs: [
          'La ciencia política ha desarrollado distintas familias de explicación. Una perspectiva <strong>informacional</strong> destaca especialización y producción de conocimiento. Una perspectiva <strong>distributiva</strong> observa incentivos para ocupar espacios relacionados con intereses de los distritos. Una perspectiva <strong>partidaria</strong> analiza cómo los partidos organizan posiciones y prioridades dentro de la legislatura.',
          'La evidencia chilena no obliga a elegir una sola explicación. Precisamente porque distintos mecanismos aparecen simultáneamente, el sitio presentará las comisiones como instituciones de información, representación y organización política, evitando reducirlas a una única función.'
        ],
        sourceIds: ['mimicaNaviaComisiones2022']
      }
    ],
    sourceIds: ['camaraComisionesActual', 'camaraFaqComisiones', 'locComisiones22', 'reglamentoComisiones', 'mimicaNaviaComisiones2022', 'camaraCEI', 'bcnProcesoLey']
  };

  if (!data.featuredQuestions.some((item) => item.id === 'comisiones')) {
    const fiscalIndex = data.featuredQuestions.findIndex((item) => item.id === 'fiscalizacion');
    const at = fiscalIndex >= 0 ? fiscalIndex : data.featuredQuestions.length;
    data.featuredQuestions.splice(at, 0, {
      id: 'comisiones',
      unit: 'organizacion',
      title: '¿Qué hacen las comisiones?',
      summary: 'Dónde se estudia en detalle gran parte del trabajo parlamentario y cómo se cruzan información, territorio y partidos.',
      status: 'ready'
    });
  }
})();
