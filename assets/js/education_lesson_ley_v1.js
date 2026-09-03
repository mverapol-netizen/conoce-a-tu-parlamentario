(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    bcnProcesoLey: {
      label: 'El Poder Legislativo · proceso de formación de la ley',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/formacioncivica/detalle_guia?h=10221.3%2F45763',
      note: 'Guía institucional detallada sobre iniciativa, trámites constitucionales, comisiones mixtas, veto, promulgación, publicación y urgencias.'
    },
    camaraProcesoLey: {
      label: 'Formación de la Ley · información ciudadana',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/informacion_ciudadana.aspx',
      note: 'Material institucional sobre etapas del proceso y conceptos como mensaje, moción, cámara de origen, discusión general y particular, veto y promulgación.'
    },
    reglamentoDiscusiones: {
      label: 'Reglamento de la Cámara · discusiones e indicaciones',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/doc/leyes_normas/reglamento.pdf',
      note: 'Regula discusión general y particular, indicaciones y retorno a comisión para segundo informe.'
    },
    locCongresoLey: {
      label: 'Ley Orgánica Constitucional del Congreso Nacional · artículos 23 a 25',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/doc/leyes_normas/loc_12-16.pdf',
      note: 'Define discusión general y particular y fija reglas de admisibilidad de indicaciones.'
    },
    constitucion65: {
      label: 'Constitución Política · iniciativa de ley e iniciativa exclusiva',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=242302&idVersion=2023-01-17',
      note: 'Regula mensaje, moción, cámaras de origen reservadas e iniciativa exclusiva del Presidente en determinadas materias.'
    },
    constitucion74: {
      label: 'Constitución Política · urgencias legislativas',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=242302&idParte=8563557&idVersion=2024-01-19',
      note: 'Faculta al Presidente para hacer presente urgencia en uno o todos los trámites de un proyecto.'
    },
    ejemplo18216: {
      label: 'Boletín 18.216-05 · historial de tramitación',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/legislacion/ProyectosDeLey/tramitacion.aspx?prmBOLETIN=18216-05&prmID=18872',
      note: 'Ejemplo real de un proyecto con primer y segundo trámite, discusión general, indicaciones, informes y paso por Hacienda.'
    },
    mimicaNavia2024: {
      label: 'Where did Hyper-Presidentialism Go? The Origin of Bills and Laws Passed in Chile, 1990–2022',
      publisher: 'Journal of Politics in Latin America',
      url: 'https://journals.sagepub.com/doi/10.1177/1866802X241245727',
      note: 'Analiza 13.358 proyectos y 2.603 leyes entre 1990 y 2022 y documenta cambios en la participación relativa de iniciativas presidenciales y parlamentarias.'
    },
    mimicaEtAl2023: {
      label: 'Changes in the Rules of the Lawmaking Process and the Success of Presidential Bills: Chile, 1990–2018',
      publisher: 'Legislative Studies Quarterly',
      url: 'https://onlinelibrary.wiley.com/doi/10.1111/lsq.12375',
      note: 'Estudia cómo reglas del proceso y urgencias presidenciales se relacionan con el éxito de proyectos del Ejecutivo.'
    }
  });

  data.lessons['como-se-hace-una-ley'] = {
    title: '¿Cómo se hace una ley?',
    unit: 'ley',
    status: 'ready',
    readingTime: '12–15 min',
    intro: 'Una ley no nace de una sola votación. Es el resultado eventual de un proceso en que una propuesta puede ser estudiada, modificada, aprobada, rechazada y revisada por distintos actores e instituciones.',
    keyPoints: [
      'Una iniciativa puede comenzar como mensaje presidencial o como moción parlamentaria, pero la Constitución reserva determinadas materias a la iniciativa exclusiva del Presidente.',
      'Primer trámite es el proceso en la cámara de origen; segundo trámite ocurre en la cámara revisora.',
      'Aprobar en general significa aceptar la idea de legislar; la discusión particular examina el proyecto en detalle y por artículos.',
      'La cámara revisora puede aprobar, modificar o rechazar; las diferencias pueden llevar a una comisión mixta.',
      'Aprobación en el Congreso no equivale todavía, en todos los casos, a una ley publicada: pueden intervenir observaciones presidenciales, promulgación, publicación y controles constitucionales cuando correspondan.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'La intuición: una ley es un recorrido, no un momento',
        paragraphs: [
          'Cuando una noticia dice que “la Cámara aprobó un proyecto”, todavía falta saber <strong>qué aprobó, en qué etapa y con qué efecto</strong>. Una votación puede referirse a la idea general de legislar, a un artículo, a una indicación, a cambios del Senado o a otra decisión procedimental.',
          'Por eso la unidad básica para entender una ley no es una votación aislada, sino su <strong>tramitación</strong>: la secuencia documentada de decisiones mediante la cual un texto cambia y eventualmente llega —o no llega— a convertirse en ley.'
        ],
        sourceIds: ['bcnProcesoLey', 'camaraProcesoLey']
      },
      {
        type: 'institution',
        title: 'Primero tiene que existir una iniciativa: mensaje o moción',
        paragraphs: [
          'La Constitución permite que los proyectos se originen mediante un <span data-edu-term="mensaje">mensaje</span> del Presidente de la República o una <span data-edu-term="mocion">moción</span> de parlamentarios. La iniciativa puede comenzar en Cámara o Senado, salvo materias para las cuales la propia Constitución reserva una cámara de origen determinada.',
          'Sin embargo, Presidente y parlamentarios no poseen la misma capacidad de iniciativa. Determinadas materias —especialmente varias de carácter tributario, presupuestario, administrativo, remuneracional y de seguridad social— están reservadas a la <strong>iniciativa exclusiva presidencial</strong>. Por eso “un diputado puede presentar cualquier proyecto” es una afirmación incorrecta.'
        ],
        sourceIds: ['constitucion65', 'bcnProcesoLey']
      },
      {
        type: 'institution',
        title: 'Primer trámite: la cámara de origen estudia la propuesta',
        paragraphs: [
          'El <strong>primer trámite constitucional</strong> ocurre en la cámara donde el proyecto inició. Habitualmente la propuesta es enviada a una o más comisiones, que la estudian y elaboran informes antes de las decisiones de Sala.',
          'La <strong>discusión general</strong> se concentra en las ideas matrices o fundamentales y decide si se admite o desecha el proyecto en su totalidad. Si se aprueba en general y existen indicaciones, la discusión puede volver a comisión para su examen detallado antes de la discusión particular.'
        ],
        sourceIds: ['bcnProcesoLey', 'reglamentoDiscusiones', 'locCongresoLey']
      },
      {
        type: 'institution',
        title: 'Aprobar en general no significa aprobar el texto final',
        paragraphs: [
          'La <strong>discusión particular</strong> examina el proyecto en sus detalles y por artículos. Allí adquieren especial importancia las <span data-edu-term="indicacion">indicaciones</span>, es decir, propuestas destinadas a agregar, suprimir o modificar partes del texto dentro de los límites constitucionales y reglamentarios.',
          'Esta distinción explica por qué un parlamentario puede votar a favor de la idea de legislar y después votar en contra de artículos concretos, o viceversa. Resumir ambas decisiones como “votó a favor del proyecto” puede ocultar información decisiva.'
        ],
        sourceIds: ['reglamentoDiscusiones', 'locCongresoLey', 'camaraProcesoLey']
      },
      {
        type: 'institution',
        title: 'Segundo trámite: la otra cámara no es un sello automático',
        paragraphs: [
          'Una vez aprobado en la cámara de origen, el proyecto pasa a la <strong>cámara revisora</strong>, donde vuelve a ser estudiado en comisión y Sala. La cámara revisora puede aprobar el texto tal como llegó, modificarlo o rechazarlo.',
          'Si introduce cambios, la cámara de origen debe pronunciarse sobre ellos. Cuando existen determinadas discrepancias entre ambas cámaras puede constituirse una <span data-edu-term="comision-mixta">comisión mixta</span> para proponer una fórmula de solución. El proceso bicameral es por tanto una negociación institucional sobre el texto, no una simple repetición de la primera votación.'
        ],
        sourceIds: ['bcnProcesoLey', 'constitucion46']
      },
      {
        type: 'institution',
        title: 'El Presidente sigue interviniendo después del Congreso',
        paragraphs: [
          'Cuando ambas cámaras aprueban el proyecto en términos compatibles, este se remite al Presidente de la República. Si lo aprueba, dispone su promulgación. La Constitución también regula las observaciones presidenciales —habitualmente llamadas veto— y los procedimientos mediante los cuales el Congreso puede pronunciarse sobre ellas.',
          'La <strong>promulgación</strong> reconoce formalmente la existencia de la ley y ordena su cumplimiento. Luego viene la <strong>publicación</strong> en el Diario Oficial. Como regla general, desde la publicación la ley es obligatoria, aunque el propio texto puede establecer una entrada en vigencia posterior.'
        ],
        sourceIds: ['bcnProcesoLey', 'camaraProcesoLey']
      },
      {
        type: 'institution',
        title: 'Las urgencias ordenan tiempo; no deciden el resultado',
        paragraphs: [
          'El Presidente puede hacer presente la <span data-edu-term="urgencia">urgencia</span> para el despacho de un proyecto. La guía de formación cívica de la BCN distingue simple urgencia, suma urgencia y discusión inmediata, con plazos ordinarios de 30, 15 y 6 días respectivamente para la cámara correspondiente.',
          'La urgencia es una herramienta importante de <strong>agenda</strong>: altera prioridad y tiempo de tramitación. Pero no transforma un proyecto en ley ni obliga a los parlamentarios a aprobarlo. Poder acelerar una decisión y poder determinar su contenido son formas distintas de poder.'
        ],
        sourceIds: ['constitucion74', 'bcnProcesoLey']
      },
      {
        type: 'case',
        title: 'Caso real: un proyecto puede acumular muchas decisiones antes de terminar',
        paragraphs: [
          'El historial oficial del boletín <strong>18.216-05</strong> muestra una trayectoria con primer trámite en la Cámara, informes de comisión, envío a la cámara revisora, discusión general en el Senado, plazo de indicaciones, nuevos informes y paso por Hacienda. Es un buen ejemplo de por qué una etiqueta como “proyecto aprobado” resulta demasiado ambigua si no se especifica la etapa.',
          'La futura página de cada proyecto debe reconstruir justamente esta secuencia y permitir abrir cada hito, documento y votación sin exigir al usuario interpretar por sí solo un historial administrativo extenso.'
        ],
        sourceIds: ['ejemplo18216']
      },
      {
        type: 'evidence',
        title: 'Quién inicia las leyes también ha cambiado históricamente',
        paragraphs: [
          'Chile ha sido descrito tradicionalmente como un presidencialismo con fuertes poderes legislativos del Ejecutivo. Sin embargo, la distribución efectiva de iniciativas y leyes no ha permanecido constante. Mimica y Navia examinan 13.358 proyectos y 2.603 leyes entre 1990 y 2022 y encuentran una disminución sostenida de la participación relativa de mensajes presidenciales entre los proyectos ingresados y las leyes promulgadas.',
          'Ese hallazgo no elimina los poderes constitucionales del Presidente —iniciativa exclusiva, urgencias y veto, entre otros—. Sí obliga a distinguir entre <strong>facultades institucionales</strong> y <strong>peso empírico efectivo</strong> en diferentes períodos.'
        ],
        sourceIds: ['mimicaNavia2024', 'constitucion65', 'constitucion74']
      },
      {
        type: 'evidence',
        title: 'Las reglas procedimentales también distribuyen poder',
        paragraphs: [
          'La investigación sobre Chile muestra que las reglas del proceso legislativo modifican las oportunidades de negociación entre Ejecutivo y Congreso. Incluso herramientas aparentemente procedimentales, como las urgencias, se relacionan con las probabilidades de avance de proyectos presidenciales.',
          'Esto revela una dimensión menos visible del Congreso: no solo importa quién vota qué, sino también quién puede iniciar, priorizar, modificar, retrasar y devolver un asunto dentro del procedimiento.'
        ],
        sourceIds: ['mimicaEtAl2023']
      },
      {
        type: 'myth',
        title: 'Cinco frases periodísticas que necesitan contexto',
        bullets: [
          '<strong>“La Cámara aprobó la ley”.</strong> Puede haber aprobado solo una etapa de un proyecto que todavía debe continuar su tramitación.',
          '<strong>“Se aprobó en general”.</strong> Significa aceptar la idea de legislar, no cerrar el texto artículo por artículo.',
          '<strong>“El Senado rechazó la ley”.</strong> Hay que precisar si rechazó el proyecto completo, una modificación o una decisión específica.',
          '<strong>“El Gobierno puso urgencia, así que se aprobará pronto”.</strong> La urgencia afecta plazos y prioridad, no garantiza aprobación.',
          '<strong>“Esta es la ley de una sola persona”.</strong> El texto final puede haber sido modificado por comisiones, parlamentarios, ambas cámaras y el Ejecutivo.'
        ],
        sourceIds: ['bcnProcesoLey', 'reglamentoDiscusiones', 'constitucion74']
      },
      {
        type: 'debate',
        title: 'Legislar es también decidir quién puede cambiar el texto y controlar el tiempo',
        paragraphs: [
          'La descripción formal del procedimiento no agota la ciencia política del lawmaking. Quedan preguntas sobre poder de agenda, negociación, control del contenido, especialización de comisiones y capacidad relativa de Ejecutivo, partidos y legisladores.',
          'Por eso el sitio separará cuidadosamente <strong>la ruta jurídica de una ley</strong> de <strong>la explicación política de por qué avanzó, cambió o se detuvo</strong>. La primera puede reconstruirse con fuentes institucionales; la segunda exige evidencia adicional y muchas veces admite explicaciones rivales.'
        ],
        sourceIds: ['mimicaNavia2024', 'mimicaEtAl2023']
      }
    ],
    sourceIds: ['bcnProcesoLey', 'camaraProcesoLey', 'reglamentoDiscusiones', 'locCongresoLey', 'constitucion65', 'constitucion74', 'ejemplo18216', 'mimicaNavia2024', 'mimicaEtAl2023']
  };

  const question = data.featuredQuestions.find((item) => item.id === 'como-se-hace-una-ley');
  if (question) question.status = 'ready';
})();
