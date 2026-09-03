(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    camaraRepresentacion: {
      label: 'Formación ciudadana · distrito, semana distrital y representación',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/formacion_ciudadana/faq.aspx',
      note: 'Define distrito, señala que la Cámara tiene 155 integrantes elegidos en 28 distritos y explica la semana distrital como parte de la función representativa.'
    },
    servelDhondt: {
      label: 'Método D’Hondt y distribución de escaños',
      publisher: 'Servicio Electoral de Chile',
      url: 'https://www.servel.cl/metodo-dhondt/',
      note: 'Explica cómo los votos se convierten en escaños mediante representación proporcional y listas o pactos electorales.'
    },
    ley20840: {
      label: 'Ley N.º 20.840 · reforma electoral de 2015',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=1077039',
      note: 'Sustituyó el sistema binominal, reorganizó los distritos y estableció 28 distritos que eligen entre 3 y 8 diputados dentro de un total de 155 escaños.'
    },
    mansbridge2003: {
      label: 'Rethinking Representation',
      publisher: 'American Political Science Review · Cambridge University Press',
      url: 'https://www.cambridge.org/core/journals/american-political-science-review/article/abs/rethinking-representation/608152BA9E3A0D9B0EC01CE4063B9FB3',
      note: 'Distingue representación promissory, anticipatory, gyroscopic y surrogate y muestra que la representación democrática no se agota en una sola relación electoral.'
    },
    rehfeld2009: {
      label: 'Representation Rethought: On Trustees, Delegates, and Gyroscopes',
      publisher: 'American Political Science Review · Cambridge University Press',
      url: 'https://www.cambridge.org/core/journals/american-political-science-review/article/abs/representation-rethought-on-trustees-delegates-and-gyroscopes-in-the-study-of-political-representation-and-democracy/A6D5583CFF57FC81D5E0C7D38245C14D',
      note: 'Cuestiona la oposición binaria delegate/trustee y separa fines, fuente del juicio y responsiveness.'
    },
    chileConstituencyService2023: {
      label: 'Constituency Service and Representation: The Effects of Remoteness and Social Deprivation',
      publisher: 'Representation · Taylor & Francis',
      url: 'https://www.tandfonline.com/doi/full/10.1080/00344893.2023.2237028',
      note: 'Estudia reuniones de diputados chilenos y encuentra más atención relativa a asuntos locales o personales en distritos más remotos y socioeconómicamente desfavorecidos.'
    },
    fossen2019: {
      label: 'Constructivism and the Logic of Political Representation',
      publisher: 'American Political Science Review · Cambridge University Press',
      url: 'https://www.cambridge.org/core/journals/american-political-science-review/article/constructivism-and-the-logic-of-political-representation/7CD1163445B3D2C46A682E40D8EC3E72',
      note: 'Refina el enfoque constructivista y distingue actuar por otros de representar o caracterizar políticamente a una constituency.'
    }
  });

  data.lessons['quien-me-representa'] = {
    title: '¿Quién representa a quién?',
    unit: 'representacion',
    status: 'ready',
    readingTime: '9–12 min',
    intro: 'En Chile no tienes un único diputado personal. Tu comuna pertenece a un distrito que elige varios representantes, y cada uno actúa además dentro de partidos, bancadas y una institución nacional. Representar es una relación política más compleja que obedecer instrucciones.',
    keyPoints: [
      'La Cámara tiene 155 integrantes elegidos directamente en 28 distritos; cada distrito elige varios diputados.',
      'Institucionalmente, los diputados electos por un distrito representan ese distrito aunque una persona haya votado por otra candidatura o por ninguna.',
      'El voto por una candidatura también opera dentro de listas o pactos: la representación electoral combina una dimensión personal y otra colectiva.',
      'La teoría democrática distingue autorización, accountability, juicio propio, responsiveness y distintas formas de representación; no existe una regla simple según la cual representar sea obedecer siempre a una mayoría inmediata.',
      'La representación territorial no termina el día de la elección: la Cámara institucionaliza tiempo de trabajo distrital y la evidencia chilena muestra que las características territoriales afectan el tipo de servicio representativo.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'La intuición: no tienes un solo diputado',
        paragraphs: [
          'Si vives en una comuna chilena, esa comuna pertenece a un <strong>distrito electoral</strong>. El distrito no elige una sola persona: el sistema vigente distribuye varios escaños. Por eso es más preciso hablar de <strong>los representantes elegidos por tu distrito</strong> que de “tu diputado” en singular.',
          'Puedes sentir mayor cercanía con la persona por la que votaste, pero el cargo parlamentario no se convierte por eso en una relación privada entre candidato y votante. Quienes resultan electos ejercen una función representativa respecto del distrito completo.'
        ],
        sourceIds: ['camaraRepresentacion', 'ley20840']
      },
      {
        type: 'institution',
        title: 'Cómo se construye la representación electoral en Chile',
        paragraphs: [
          'La Cámara está integrada por 155 diputadas y diputados elegidos directamente en 28 distritos. La propia Cámara define un distrito como una comuna o agrupación de comunas cuyos ciudadanos eligen a quienes los representan durante el período correspondiente.',
          'La elección no funciona como una suma de competencias individuales aisladas. El método D’Hondt asigna primero escaños según la votación de listas o pactos y luego determina qué candidaturas ocupan esos escaños conforme a las reglas electorales. El voto posee, por tanto, una dimensión personal y una dimensión colectiva.'
        ],
        sourceIds: ['camaraRepresentacion', 'servelDhondt', 'ley20840']
      },
      {
        type: 'history',
        title: 'El distrito actual también tiene historia',
        paragraphs: [
          'La arquitectura territorial vigente no es natural ni inmutable. La reforma electoral de 2015 redujo los distritos de diputados de 60 a 28, aumentó la Cámara de 120 a 155 escaños y reemplazó la lógica binominal por una fórmula proporcional más amplia. Los distritos actuales eligen entre 3 y 8 diputados.',
          'Esto importa porque la pregunta “¿quién me representa?” depende también de reglas electorales que pueden cambiar históricamente. La constituency es una institución construida jurídicamente, no una frontera política dada de una vez para siempre.'
        ],
        sourceIds: ['ley20840']
      },
      {
        type: 'evidence',
        title: 'Autorización y rendición de cuentas: la relación no termina con el voto',
        paragraphs: [
          'Las elecciones hacen dos cosas distintas. Primero, autorizan a determinadas personas a ocupar cargos representativos. Después permiten que la ciudadanía observe su actuación y, en elecciones futuras, pueda premiar, castigar o reemplazar. La teoría democrática trata esta relación mediante conceptos como autorización, responsiveness y accountability.',
          'Por eso conocer lo que ocurre entre elecciones es democráticamente importante. Un sitio parlamentario puede reducir el costo de observar votos, iniciativas, afiliaciones, comisiones y otras actuaciones, pero esa información no determina por sí sola si una persona “representó bien”: esa evaluación requiere criterios normativos adicionales.'
        ],
        sourceIds: ['urbinatiWarren2008', 'sepRepresentation2026']
      },
      {
        type: 'debate',
        title: '¿Debe un diputado hacer lo que quiere la mayoría de su distrito?',
        paragraphs: [
          'La oposición clásica entre <strong>delegate</strong> y <strong>trustee</strong> pregunta cuánto debe seguir un representante las preferencias de sus electores y cuánto debe ejercer juicio propio. Pero la literatura contemporánea advierte que esta oposición es demasiado simple: mezcla qué fines debe perseguir, de dónde obtiene su juicio y cuán responsive debe ser ante los representados.',
          'Por eso esta página no adopta como regla que un buen diputado deba obedecer siempre una mayoría inmediata, ni la regla contraria de que pueda ignorarla libremente. Ambas son posiciones normativas que necesitan argumentos.'
        ],
        sourceIds: ['rehfeld2009', 'mansbridge2003']
      },
      {
        type: 'evidence',
        title: 'Representar también puede significar escuchar y atender el territorio',
        paragraphs: [
          'La Cámara reserva tiempo para trabajo distrital, precisamente para que sus integrantes puedan mantener contacto con los territorios y conocer problemas locales. Eso muestra que la representación no se agota en emitir votos dentro de la Sala.',
          'La evidencia chilena sobre reuniones entre legisladores, ciudadanos y organizaciones encuentra que los diputados de distritos más remotos y de condiciones socioeconómicas más desfavorables dedican una proporción mayor de sus reuniones a asuntos locales o personales. El territorio, por tanto, ayuda a moldear la práctica representativa.'
        ],
        sourceIds: ['camaraRepresentacion', 'chileConstituencyService2023']
      },
      {
        type: 'evidence',
        title: 'Los representantes también participan en definir qué significa “representar” a un grupo',
        paragraphs: [
          'Enfoques constructivistas recuerdan que los representantes no reciben necesariamente intereses perfectamente formados y transparentes. Cuando un actor dice “represento a las regiones”, “a la clase media” o “a los trabajadores”, también está proponiendo una manera de caracterizar ese colectivo y sus intereses.',
          'Esto no elimina la necesidad de responsiveness. Significa que la representación es una relación dinámica: puede ser reconocida, discutida y rechazada incluso cuando la autorización electoral formal sigue vigente.'
        ],
        sourceIds: ['fossen2019', 'sepRepresentation2026']
      },
      {
        type: 'myth',
        title: 'Cuatro confusiones frecuentes',
        bullets: [
          '<strong>“Solo me representa la persona por la que voté”.</strong> Institucionalmente, el distrito elige varios representantes; no existe un vínculo exclusivo entre cada elector y una sola diputación.',
          '<strong>“Representar significa votar siempre como quiere la mayoría”.</strong> Esa es una concepción normativa posible, no una definición neutral de representación democrática.',
          '<strong>“Partido y territorio compiten, así que el diputado debe elegir uno”.</strong> La representación contemporánea está mediada simultáneamente por territorio, partidos, bancadas, programas, electores y juicio individual.',
          '<strong>“Más reuniones locales significan automáticamente mejor representación”.</strong> La actividad territorial puede ser relevante, pero su cantidad por sí sola no permite evaluar su calidad, su propósito ni sus efectos.'
        ],
        sourceIds: ['camaraRepresentacion', 'rehfeld2009', 'chileConstituencyService2023']
      },
      {
        type: 'debate',
        title: 'Lo que podremos observar y lo que no debemos inventar',
        paragraphs: [
          'Podemos observar distrito, afiliación, bancada, votaciones, mociones, coautorías, comisiones y otras actuaciones registradas. Con mejores datos podremos mostrar además distintas formas de actividad territorial y de contacto institucional.',
          'No podemos inferir automáticamente a partir de esos registros motivaciones internas como obediencia, convicción, presión partidaria o intención representativa. La arquitectura del sitio debe mantener esa frontera entre comportamiento observado y explicación causal.'
        ],
        sourceIds: []
      }
    ],
    sourceIds: ['camaraRepresentacion', 'servelDhondt', 'ley20840', 'urbinatiWarren2008', 'sepRepresentation2026', 'mansbridge2003', 'rehfeld2009', 'chileConstituencyService2023', 'fossen2019']
  };

  const question = data.featuredQuestions.find((item) => item.id === 'quien-me-representa');
  if (question) question.status = 'ready';
})();
