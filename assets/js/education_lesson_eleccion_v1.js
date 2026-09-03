(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    servelDhondt: {
      label: 'Método D’Hondt · elecciones parlamentarias',
      publisher: 'Servicio Electoral de Chile',
      url: 'https://www.servel.cl/metodo-dhondt/',
      note: 'Explica paso a paso cómo los votos se convierten en escaños por lista o pacto y luego en candidaturas electas.'
    },
    ley18700Dhondt: {
      label: 'Ley N° 18.700 · reglas de proclamación parlamentaria',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=30082',
      note: 'Regula legalmente el coeficiente D’Hondt y la asignación de escaños en elecciones de diputados y senadores.'
    },
    servelTerritorios: {
      label: 'Territorios electorales',
      publisher: 'Servicio Electoral de Chile',
      url: 'https://www.servel.cl/sistema-electoral/territorios-electorales/',
      note: 'Relaciona comunas, distritos y circunscripciones senatoriales vigentes.'
    },
    camaraDistritos155: {
      label: 'Cámara de Diputadas y Diputados · composición y distritos',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/formacion_ciudadana/faq.aspx',
      note: 'La Cámara actual posee 155 integrantes elegidos directamente en 28 distritos electorales.'
    },
    senado50Actual: {
      label: 'Senadoras y senadores',
      publisher: 'Senado de la República de Chile',
      url: 'https://www.senado.cl/senadoras-y-senadores',
      note: 'El Senado actual está formado por 50 integrantes elegidos directamente en 16 circunscripciones senatoriales, con mandatos de ocho años.'
    },
    senadoCircunscripciones: {
      label: 'Glosario legislativo · circunscripción senatorial',
      publisher: 'Senado de la República de Chile',
      url: 'https://www.senado.cl/ciudadania/glosario-legislativo',
      note: 'Cada región constituye una circunscripción senatorial y elige entre dos y cinco senadores según su población.'
    }
  });

  data.lessons['como-se-eligen'] = {
    title: '¿Cómo se eligen los parlamentarios?',
    unit: 'representacion',
    status: 'ready',
    readingTime: '10–13 min',
    intro: 'En Chile el voto por una candidatura no se convierte directamente en un escaño individual. Primero contribuye a una lista o pacto; luego D’Hondt distribuye los cargos y finalmente se determina qué personas resultan electas.',
    keyPoints: [
      'La Cámara tiene 155 integrantes elegidos en 28 distritos; cada distrito elige varios diputados, no uno solo.',
      'El Senado tiene 50 integrantes elegidos en 16 circunscripciones regionales y sus mandatos duran ocho años.',
      'D’Hondt asigna primero los escaños a listas o pactos según su votación agregada.',
      'Si existe un pacto, los escaños obtenidos se distribuyen nuevamente entre sus partidos conforme a las reglas legales; después resultan electas las candidaturas con mayores votaciones personales dentro del grupo que obtuvo los cupos.',
      'Por eso votar por una persona también contribuye electoralmente a la lista o pacto en que esa candidatura compite.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'Tu voto elige una persona dentro de una competencia colectiva',
        paragraphs: [
          'La papeleta muestra candidaturas individuales, pero la regla de asignación de escaños considera también la votación total de las listas y pactos. El camino real no es simplemente “la persona con más votos gana”.',
          'La secuencia básica es: <strong>voto por candidatura → suma de votos de la lista o pacto → asignación de escaños → determinación de las candidaturas electas</strong>. Esta arquitectura explica por qué una candidatura puede obtener muchos votos personales y no resultar electa, mientras otra con menos votos sí lo hace dentro de una lista que obtiene más cupos.'
        ],
        sourceIds: ['servelDhondt', 'ley18700Dhondt']
      },
      {
        type: 'institution',
        title: 'Cámara: representación plurinominal en 28 distritos',
        paragraphs: [
          'Los 155 integrantes de la Cámara son elegidos por votación directa en <strong>28 distritos electorales</strong>. Cada distrito agrupa una o más comunas y elige varios representantes.',
          'Esto significa que una persona no tiene un único “diputado propio”. Todos quienes resultan electos por el distrito ocupan institucionalmente la representación de ese territorio, aunque el elector haya votado solo por una candidatura o por ninguna de las finalmente electas.'
        ],
        sourceIds: ['camaraDistritos155', 'servelTerritorios']
      },
      {
        type: 'institution',
        title: 'Senado: circunscripciones regionales y mandatos más largos',
        paragraphs: [
          'El Senado posee <strong>50 integrantes</strong> elegidos directamente en 16 circunscripciones senatoriales, correspondientes a las regiones. Cada circunscripción elige entre dos y cinco senadores según la configuración vigente.',
          'Las senadoras y senadores permanecen ocho años en el cargo. Por ello, la elección senatorial no renueva los 50 escaños simultáneamente: en una elección parlamentaria solo corresponde elegir los cargos de las circunscripciones cuyo período termina.'
        ],
        sourceIds: ['senado50Actual', 'senadoCircunscripciones', 'servelDhondt']
      },
      {
        type: 'institution',
        title: 'Paso 1: D’Hondt distribuye escaños entre listas o pactos',
        paragraphs: [
          'La votación total de cada lista se divide sucesivamente por 1, 2, 3 y así hasta el número de cargos que corresponda elegir. Los cocientes resultantes se ordenan de mayor a menor y los escaños se atribuyen a las cifras más altas hasta completar todos los cargos disponibles.',
          'Los votos nulos y blancos no se consideran para este cálculo. Lo relevante en esta etapa es la votación agregada de cada lista o pacto, no todavía qué candidatura específica ocupará cada escaño.'
        ],
        sourceIds: ['servelDhondt', 'ley18700Dhondt']
      },
      {
        type: 'institution',
        title: 'Paso 2: dentro del grupo que obtuvo escaños se determina quién entra',
        paragraphs: [
          'En una lista de un solo partido, resultan electas las candidaturas con las mayores votaciones personales dentro de esa lista, hasta completar los escaños que le fueron asignados.',
          'Cuando existe un pacto de varios partidos, los cargos del pacto se distribuyen nuevamente entre sus componentes conforme a D’Hondt y las reglas legales aplicables. Una vez definido cuántos escaños recibe cada partido o conjunto, las mayores votaciones personales determinan qué candidaturas ocupan esos cupos.'
        ],
        sourceIds: ['servelDhondt', 'ley18700Dhondt']
      },
      {
        type: 'myth',
        title: '“Salen los candidatos más votados del distrito” es falso como regla general',
        paragraphs: [
          'El orden general de votación individual de todo el distrito no basta para determinar los electos. La distribución depende primero de cuántos cargos consigue cada lista o pacto.',
          'Por eso puede ocurrir que una candidatura individualmente muy votada quede fuera si su lista no obtiene suficientes escaños, mientras una candidatura con menos votos personales resulte electa dentro de una lista que sí consiguió un cupo adicional. No es una excepción al sistema: es consecuencia de su diseño proporcional por listas.'
        ],
        sourceIds: ['servelDhondt', 'ley18700Dhondt']
      },
      {
        type: 'case',
        title: 'Así se eligieron tus representantes: una futura función del sitio',
        paragraphs: [
          'Después de seleccionar una comuna, el sitio ya identifica el distrito correspondiente. La próxima capa puede utilizar los resultados oficiales para reconstruir, paso a paso, la elección de ese distrito: votos por candidatura, suma por lista o pacto, tabla D’Hondt, escaños adjudicados y candidaturas finalmente electas.',
          'La visualización no debería pedir al ciudadano que acepte una fórmula como una caja negra. Podrá mostrar los cocientes concretos y destacar exactamente qué cifra adjudicó cada escaño.'
        ],
        sourceIds: ['servelDhondt', 'servelTerritorios']
      },
      {
        type: 'history',
        title: 'La reforma de 2015 cambió mucho más que el número de diputados',
        paragraphs: [
          'La reforma electoral de 2015 reemplazó la estructura binominal por distritos de mayor magnitud, elevó la Cámara de 120 a 155 integrantes y estableció la actual configuración territorial y proporcional.',
          'Una precisión histórica importante es que D’Hondt no nació con esa reforma. Lo que cambió decisivamente fue, entre otras cosas, la magnitud de los distritos y la estructura de competencia. La misma familia de fórmula puede producir efectos representativos distintos cuando cambia cuántos escaños se reparten en cada territorio.'
        ],
        sourceIds: ['ley18700Dhondt', 'camaraDistritos155']
      },
      {
        type: 'debate',
        title: 'Representación proporcional implica elegir entre valores que pueden tensionarse',
        paragraphs: [
          'Distritos más grandes y mayor proporcionalidad pueden facilitar que más fuerzas políticas obtengan representación y reducir la distancia entre votos y escaños. Al mismo tiempo pueden ampliar el número de partidos relevantes y hacer más compleja la coordinación legislativa.',
          'El diseño electoral no resuelve una única pregunta técnica. Distribuye pesos entre proporcionalidad, representación territorial, vínculo personal con candidaturas, gobernabilidad y pluralismo. La elección entre esos objetivos es también política y normativa.'
        ],
        sourceIds: ['servelDhondt', 'ley18700Dhondt']
      }
    ],
    sourceIds: ['servelDhondt', 'ley18700Dhondt', 'servelTerritorios', 'camaraDistritos155', 'senado50Actual', 'senadoCircunscripciones']
  };
})();
