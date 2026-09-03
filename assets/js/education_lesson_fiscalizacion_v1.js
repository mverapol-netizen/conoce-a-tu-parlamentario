(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    constitucionFiscalizacion: {
      label: 'Constitución Política · artículo 52, N.º 1',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=242302&idParte=8563521',
      note: 'Regula las modalidades de fiscalización de los actos del Gobierno: acuerdos u observaciones, citación de ministros y comisiones especiales investigadoras.'
    },
    camaraCEI: {
      label: 'Comisiones Especiales Investigadoras',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://camara.cl/fiscalizacion/comisiones_investigadoras/comisiones_investigadoras.aspx',
      note: 'Registro público de CEI y explicación institucional: se crean con al menos 2/5 de los diputados en ejercicio para reunir información sobre determinados actos del Gobierno.'
    },
    camaraAcusaciones: {
      label: 'Acusaciones Constitucionales',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/fiscalizacion/acusaciones_constitucionales.aspx',
      note: 'Registro público del procedimiento y de las acusaciones presentadas; la Cámara decide procedencia y, si corresponde, el asunto pasa al Senado.'
    },
    ferrada2002: {
      label: 'La Reforma Constitucional a la Fiscalización Parlamentaria en la Constitución de 1980',
      publisher: 'Ius et Praxis',
      url: 'https://www.scielo.cl/scielo.php?pid=S0718-00122002000100025&script=sci_arttext',
      note: 'Analiza la fiscalización en el contexto del régimen presidencial chileno y la diferencia entre control parlamentario y responsabilidad política del gabinete.'
    },
    garciaFiscalizacion2011: {
      label: 'Fiscalización parlamentaria de los actos de gobierno',
      publisher: 'Revista de Derecho Público · Universidad de Chile',
      url: 'https://revistaderechopublico.uchile.cl/index.php/RDPU/article/view/36632',
      note: 'Estudia la evolución normativa y las tres modalidades de fiscalización configuradas tras la reforma constitucional de 2005.'
    },
    garciaCEI2012: {
      label: 'Comisiones especiales investigadoras de la Cámara de Diputados',
      publisher: 'Revista de Derecho Público · Universidad de Chile',
      url: 'https://revistaderechopublico.uchile.cl/index.php/RDPU/article/view/35377',
      note: 'Analiza finalidad, atribuciones, competencia y límites de las comisiones investigadoras después de su constitucionalización en 2005.'
    },
    zunigaInterpelacion2007: {
      label: 'Interpelaciones en la reforma constitucional',
      publisher: 'Revista de Derecho Público · Universidad de Chile',
      url: 'https://www.revistaderechopublico.uchile.cl/index.php/RDPU/article/view/40210',
      note: 'Examina la incorporación de la interpelación y su regulación dentro del presidencialismo chileno después de la reforma constitucional de 2005.'
    },
    constitucionAcusacion: {
      label: 'Constitución Política · artículo 52, N.º 2 y artículo 53',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=242302&idParte=8563521',
      note: 'Regula la acusación constitucional como atribución distinta: la Cámara declara si ha lugar y el Senado conoce la acusación como jurado.'
    }
  });

  data.lessons['fiscalizacion'] = {
    title: '¿Cómo fiscaliza la Cámara al Gobierno?',
    unit: 'fiscalizacion',
    status: 'ready',
    readingTime: '11–14 min',
    intro: 'Fiscalizar significa someter actos del Gobierno a examen político e institucional mediante herramientas para obtener información, exigir respuestas e investigar. No significa que la Cámara gobierne, remueva ministros por pérdida de confianza o actúe como tribunal penal.',
    keyPoints: [
      'Fiscalizar los actos del Gobierno es una atribución exclusiva de la Cámara de Diputadas y Diputados, no del Senado.',
      'La Constitución contempla acuerdos u observaciones, citación de ministros y comisiones especiales investigadoras como modalidades de fiscalización.',
      'Los acuerdos y observaciones no afectan por sí mismos la responsabilidad política de los ministros; Chile sigue siendo un régimen presidencial.',
      'Una comisión investigadora reúne información sobre determinados actos del Gobierno; no es un tribunal ni puede imponer penas.',
      'La acusación constitucional pertenece al sistema de control constitucional, pero el artículo 52 la regula separadamente de las modalidades ordinarias de fiscalización.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'La intuición: controlar también significa obligar al poder a explicar',
        paragraphs: [
          'El Ejecutivo administra servicios, ejecuta políticas y dispone de gran cantidad de información que no está automáticamente en manos de los representantes. Una función de la fiscalización parlamentaria es reducir esa asimetría: <strong>preguntar, obtener antecedentes, investigar y hacer públicamente examinables determinadas decisiones del Gobierno</strong>.',
          'El valor del control no depende únicamente de que termine en una sanción. Una respuesta oficial, un documento antes desconocido o una investigación pública también pueden producir accountability al obligar a una autoridad a dar cuenta de su actuación.'
        ],
        sourceIds: ['constitucionFiscalizacion', 'garciaFiscalizacion2011']
      },
      {
        type: 'institution',
        title: 'Primera precisión: fiscaliza la Cámara, no el Congreso completo',
        paragraphs: [
          'El artículo 52 de la Constitución define como atribución exclusiva de la Cámara de Diputadas y Diputados <strong>fiscalizar los actos del Gobierno</strong>. El Senado posee importantes atribuciones de control institucional, pero no esta misma potestad general.',
          'La distinción importa porque “Congreso”, “Cámara” y “Senado” no son términos intercambiables. Una noticia que diga genéricamente que “el Congreso interpelará a un ministro” está simplificando una facultad que corresponde específicamente a la Cámara.'
        ],
        sourceIds: ['constitucionFiscalizacion', 'senadoAtribuciones']
      },
      {
        type: 'institution',
        title: 'Acuerdos, observaciones y solicitudes de antecedentes',
        paragraphs: [
          'La Cámara puede adoptar acuerdos o sugerir observaciones respecto de actos del Gobierno con el voto de la mayoría de los diputados presentes. Estos se transmiten al Presidente de la República, quien debe responder fundadamente por medio del ministro correspondiente dentro del plazo constitucional.',
          'La Constitución permite además que un diputado, con el apoyo de un tercio de los miembros presentes, solicite determinados antecedentes al Gobierno. Separadamente, el artículo 9 de la Ley Orgánica del Congreso permite a comisiones o parlamentarios debidamente individualizados solicitar informes y antecedentes específicos a determinados organismos y entidades bajo reglas propias. <strong>No toda petición de información es idéntica a la modalidad constitucional de fiscalización.</strong>'
        ],
        sourceIds: ['constitucionFiscalizacion', 'locArticulo9']
      },
      {
        type: 'institution',
        title: 'Interpelación: el ministro debe comparecer, pero no depende de la confianza de la Cámara',
        paragraphs: [
          'A petición de al menos un tercio de los diputados en ejercicio, la Cámara puede citar a un ministro de Estado para formularle preguntas relacionadas con materias vinculadas al ejercicio de su cargo. La asistencia es obligatoria y el ministro debe responder las preguntas y consultas que motivaron la citación.',
          'Esto se denomina habitualmente <strong>interpelación</strong>. Pero Chile no se transforma por ello en un régimen parlamentario: una interpelación no equivale a una moción de censura y no provoca automáticamente la salida del ministro. La relación de confianza política del gabinete sigue estructurada en torno al Presidente de la República.'
        ],
        sourceIds: ['constitucionFiscalizacion', 'zunigaInterpelacion2007', 'ferrada2002']
      },
      {
        type: 'institution',
        title: 'Comisiones investigadoras: información sobre un objeto delimitado',
        paragraphs: [
          'La Cámara puede crear una Comisión Especial Investigadora a petición de al menos <strong>dos quintos de los diputados en ejercicio</strong> para reunir información relativa a determinados actos del Gobierno. La Cámara informa actualmente que estas comisiones están integradas por 13 diputadas y diputados y funcionan durante un plazo definido que puede prorrogarse.',
          'La comisión posee herramientas para solicitar antecedentes y citar autoridades conforme a las reglas constitucionales. Pero su mandato está delimitado: investiga políticamente un objeto determinado. No reemplaza al Ministerio Público, a Contraloría, a los tribunales ni a otros organismos de control.'
        ],
        sourceIds: ['constitucionFiscalizacion', 'camaraCEI', 'garciaCEI2012']
      },
      {
        type: 'case',
        title: 'La diferencia entre investigar políticamente y juzgar',
        paragraphs: [
          'Una comisión investigadora puede reconstruir hechos, recibir testimonios, obtener antecedentes y formular conclusiones o recomendaciones. Esas conclusiones pueden tener gran importancia política y aportar información a otras instituciones.',
          'Pero una CEI no dicta una sentencia penal. Si los antecedentes sugieren posibles delitos, responsabilidades administrativas u otras infracciones, su persecución corresponde a las instituciones que el ordenamiento jurídico haya hecho competentes. <strong>Fiscalización parlamentaria y jurisdicción son funciones distintas.</strong>'
        ],
        sourceIds: ['camaraCEI', 'garciaCEI2012']
      },
      {
        type: 'institution',
        title: 'Fiscalizar no significa gobernar',
        paragraphs: [
          'La Constitución establece expresamente que los acuerdos, observaciones y solicitudes de antecedentes de esta modalidad de fiscalización no afectan la responsabilidad política de los ministros. Esa frase refleja una característica estructural del presidencialismo chileno: el Gobierno no necesita conservar la confianza cotidiana de una mayoría parlamentaria para permanecer en funciones.',
          'La Cámara puede examinar, criticar, investigar y generar costos políticos. No posee por esa sola facultad un poder general para anular actos administrativos, ejecutar una política alternativa o sustituir al Presidente y sus ministros en la conducción del Gobierno.'
        ],
        sourceIds: ['constitucionFiscalizacion', 'ferrada2002']
      },
      {
        type: 'history',
        title: '2005 cambió la arquitectura del control parlamentario',
        paragraphs: [
          'La reforma constitucional de 2005 fortaleció y explicitó herramientas de fiscalización de la Cámara. La literatura jurídica identifica especialmente la incorporación constitucional de la interpelación y de las comisiones especiales investigadoras como parte de esa nueva arquitectura.',
          'La comparación histórica importa porque la pregunta “¿qué puede hacer la Cámara para controlar al Gobierno?” no ha tenido siempre la misma respuesta jurídica. Las capacidades de oversight también son instituciones sujetas a reforma.'
        ],
        sourceIds: ['garciaFiscalizacion2011', 'garciaCEI2012', 'zunigaInterpelacion2007']
      },
      {
        type: 'institution',
        title: 'Acusación constitucional: relacionada con el control, pero jurídicamente distinta',
        paragraphs: [
          'El mismo artículo 52 regula, en un numeral separado, la facultad de la Cámara de declarar si ha lugar determinadas <strong>acusaciones constitucionales</strong> formuladas por no menos de diez ni más de veinte diputados contra autoridades específicamente enumeradas y por causales constitucionalmente determinadas.',
          'Si la Cámara declara que ha lugar, el procedimiento pasa al Senado, que resuelve como jurado conforme al artículo 53. Por eso la acusación no debe enseñarse como si fuera simplemente una interpelación “más fuerte” o el desenlace necesario de una comisión investigadora. Es un procedimiento constitucional distinto, con sujetos, causales, quórums y efectos propios.'
        ],
        sourceIds: ['constitucionAcusacion', 'camaraAcusaciones']
      },
      {
        type: 'myth',
        title: 'Cinco confusiones frecuentes sobre fiscalización',
        bullets: [
          '<strong>“El Senado también fiscaliza al Gobierno”.</strong> No posee la atribución general de fiscalización que el artículo 52 reserva a la Cámara.',
          '<strong>“Interpelar a un ministro significa censurarlo”.</strong> No. Debe comparecer y responder, pero su continuidad no depende automáticamente de una votación de confianza parlamentaria.',
          '<strong>“Una comisión investigadora puede condenar a alguien”.</strong> No. Reúne información y formula conclusiones políticas; no es un tribunal penal.',
          '<strong>“Mandar un oficio obliga al servicio a hacer lo que pide el diputado”.</strong> Pedir información o antecedentes no equivale a impartir una orden administrativa.',
          '<strong>“Una acusación constitucional es la etapa final de toda fiscalización”.</strong> No. Es una atribución constitucional diferente que solo procede respecto de autoridades y causales específicas.'
        ],
        sourceIds: ['constitucionFiscalizacion', 'locArticulo9', 'constitucionAcusacion']
      },
      {
        type: 'debate',
        title: '¿Cómo sabemos si la fiscalización es efectiva?',
        paragraphs: [
          'Contar oficios, interpelaciones o comisiones investigadoras solo mide activación de herramientas. No demuestra cuánto nuevo conocimiento produjeron, si las autoridades respondieron sustantivamente, si hubo seguimiento o si una práctica pública cambió.',
          'Una futura capa de datos debería separar al menos actividad, respuesta, tiempos y seguimiento. Incluso entonces sería imprudente colapsar todo en un “puntaje de fiscalización”: cada instrumento persigue objetivos diferentes y la efectividad política es multidimensional.'
        ],
        sourceIds: ['garciaFiscalizacion2011', 'garciaCEI2012']
      }
    ],
    sourceIds: ['constitucionFiscalizacion', 'locArticulo9', 'camaraCEI', 'camaraAcusaciones', 'constitucionAcusacion', 'ferrada2002', 'garciaFiscalizacion2011', 'garciaCEI2012', 'zunigaInterpelacion2007', 'senadoAtribuciones']
  };

  const question = data.featuredQuestions.find((item) => item.id === 'fiscalizacion');
  if (question) question.status = 'ready';
})();
