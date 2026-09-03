(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    constitucionArt66Actual: {
      label: 'Constitución Política · artículo 66 vigente',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=242302',
      note: 'Distingue los quórums para normas interpretativas de la Constitución, leyes orgánicas constitucionales y de quórum calificado, y leyes ordinarias.'
    },
    reforma21535Quorums: {
      label: 'Ley N° 21.535 · reforma a los quórums del artículo 66',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?i=1188344',
      note: 'Desde 2023, las leyes orgánicas constitucionales y de quórum calificado requieren mayoría absoluta de diputados y senadores en ejercicio.'
    },
    reforma21481Constitucion: {
      label: 'Ley N° 21.481 · quórum de reformas constitucionales',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/Navegar/imprimir?idNorma=1180303&idVersion=2022-08-23',
      note: 'Estableció el quórum de cuatro séptimos de los miembros en ejercicio de cada Cámara para reformas constitucionales.'
    },
    camaraGlosarioQuorum: {
      label: 'Glosario de formación ciudadana · Quórum',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/formacion_Ciudadana/glosario.aspx',
      note: 'Presenta la idea general de quórum como cantidad mínima relevante para sesionar, votar o adoptar acuerdos.'
    },
    reglamentoVotaciones145: {
      label: 'Reglamento de la Cámara · votaciones',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/camara/doc/leyes_normas/reglamento.pdf',
      note: 'Regula clases de votación, registro de votos afirmativos, negativos, abstenciones e inhabilidades y la proclamación de resultados.'
    },
    camaraVotaciones2026: {
      label: 'Votaciones de Sala 2026',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/legislacion/sala_sesiones/votaciones.aspx',
      note: 'La base oficial muestra para cada votación resultado, votos y, cuando corresponde, el quórum especial aplicable.'
    }
  });

  data.lessons['mayorias'] = {
    title: 'Mayorías y quórums: ¿cuántos votos se necesitan?',
    unit: 'organizacion',
    status: 'ready',
    readingTime: '9–12 min',
    intro: '“Aprobado por mayoría” no siempre significa lo mismo. La regla puede calcularse sobre quienes están presentes, sobre todos los miembros en ejercicio o mediante un umbral especial fijado por la Constitución.',
    keyPoints: [
      'Quórum puede referirse tanto al mínimo necesario para funcionar válidamente como al número de votos requerido para adoptar una decisión; siempre hay que identificar qué regla se está usando.',
      'Las leyes ordinarias requieren, como regla general, la mayoría de los miembros presentes de cada Cámara.',
      'Las leyes orgánicas constitucionales y las leyes de quórum calificado requieren actualmente mayoría absoluta de los diputados y senadores en ejercicio.',
      'Las normas legales que interpretan preceptos constitucionales requieren cuatro séptimos de los miembros en ejercicio, y las reformas constitucionales también se rigen actualmente por un quórum de cuatro séptimos.',
      'Una abstención no es lo mismo que una ausencia: cuando la regla se calcula sobre miembros presentes, seguir presente sin votar afirmativamente puede afectar la posibilidad de alcanzar la mayoría exigida.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'La pregunta correcta no es solo “¿cuántos votaron Sí?”',
        paragraphs: [
          'Para saber si una decisión fue aprobada necesitamos conocer el <strong>denominador</strong>. ¿La regla exige mayoría de quienes están presentes? ¿Mayoría absoluta de todos los miembros en ejercicio? ¿Un porcentaje especial?',
          'Dos votaciones con exactamente 78 votos afirmativos pueden tener significados jurídicos diferentes según la norma que se esté decidiendo y el universo sobre el cual se calcula el <span data-edu-term="quorum">quórum</span>.'
        ],
        sourceIds: ['constitucionArt66Actual', 'camaraGlosarioQuorum']
      },
      {
        type: 'institution',
        title: 'Ley ordinaria: mayoría de los miembros presentes',
        paragraphs: [
          'El artículo 66 de la Constitución establece como regla general que las demás normas legales —aquellas sin un quórum especial— requieren la <strong>mayoría de los miembros presentes</strong> de cada Cámara, sin perjuicio de reglas particulares previstas en otras etapas del procedimiento legislativo.',
          'Esto significa que el número necesario puede variar según la asistencia efectiva a la votación. Por eso un portal riguroso debe mostrar no solo los votos afirmativos y negativos, sino también qué regla se aplicó.'
        ],
        sourceIds: ['constitucionArt66Actual', 'camaraVotaciones2026']
      },
      {
        type: 'institution',
        title: 'Leyes orgánicas constitucionales y de quórum calificado: mayoría absoluta en ejercicio',
        paragraphs: [
          'Desde la reforma constitucional publicada en enero de 2023, tanto las normas a las que la Constitución confiere carácter de <strong>ley orgánica constitucional</strong> como las <strong>leyes de quórum calificado</strong> se establecen, modifican o derogan por la mayoría absoluta de los diputados y senadores en ejercicio.',
          'En una Cámara de 155 integrantes, mientras todos estén jurídicamente en ejercicio, esa mayoría absoluta corresponde a <strong>78 votos afirmativos</strong>. A diferencia de una mayoría calculada sobre presentes, una ausencia no reduce por sí sola ese umbral.'
        ],
        sourceIds: ['constitucionArt66Actual', 'reforma21535Quorums', 'camaraVotaciones2026']
      },
      {
        type: 'institution',
        title: 'Existen umbrales todavía diferentes para otras decisiones',
        paragraphs: [
          'Las normas legales que interpretan preceptos constitucionales requieren actualmente <strong>cuatro séptimos</strong> de los diputados y senadores en ejercicio. Las reformas a la Constitución también requieren cuatro séptimos en cada Cámara conforme a la reforma de 2022.',
          'Además existen decisiones constitucionales específicas con reglas propias. Por eso el sitio no usará una tabla simplificada de “quórum alto” y “quórum bajo”: cada votación deberá identificar la fuente normativa exacta del umbral que aplica.'
        ],
        sourceIds: ['constitucionArt66Actual', 'reforma21481Constitucion']
      },
      {
        type: 'myth',
        title: 'Abstenerse no es desaparecer de la votación',
        paragraphs: [
          'Una abstención es una decisión registrada distinta de votar afirmativamente, votar negativamente o no participar. Cuando una norma exige mayoría de los miembros presentes, quien permanece presente pero se abstiene sigue formando parte del universo relevante para determinar esa mayoría.',
          'Por eso, en determinadas reglas, una abstención puede dificultar alcanzar el umbral aun cuando no sea jurídicamente un “voto en contra”. El sitio no debe traducirla simplemente como rechazo: debe mostrar el estado original y explicar el efecto del denominador.'
        ],
        sourceIds: ['reglamentoVotaciones145', 'constitucionArt66Actual']
      },
      {
        type: 'case',
        title: 'Un ejemplo contemporáneo: 78 votos requeridos',
        paragraphs: [
          'La base oficial de votaciones de 2026 contiene decisiones en que la propia Cámara advierte que una norma requiere <strong>78 votos favorables</strong> por tratarse de una disposición orgánica constitucional o de quórum calificado. Esto permite mostrar al usuario el umbral junto al resultado real.',
          'La futura tarjeta de votación debería decir, por ejemplo: <strong>“78 necesarios · 82 obtenidos”</strong>. Esa información es pedagógicamente más útil que un simple sello “Aprobado”.'
        ],
        sourceIds: ['camaraVotaciones2026', 'reforma21535Quorums']
      },
      {
        type: 'history',
        title: 'Los quórums cambian: una definición antigua puede quedar obsoleta',
        paragraphs: [
          'Las reglas chilenas de quórum han sido reformadas varias veces. En 2022 se redujo el quórum general de reforma constitucional a cuatro séptimos y en 2023 se modificó el artículo 66 para que las leyes orgánicas constitucionales requirieran mayoría absoluta, en lugar del antiguo cuatro séptimos.',
          'Este cambio revela una regla metodológica para el sitio: <strong>cuando una explicación pedagógica institucional contradiga una norma vigente más reciente, prevalece la fuente normativa actual</strong>. Toda página deberá tener fecha de revisión.'
        ],
        sourceIds: ['reforma21481Constitucion', 'reforma21535Quorums', 'constitucionArt66Actual']
      },
      {
        type: 'debate',
        title: '¿Por qué exigir mayorías especiales?',
        paragraphs: [
          'Los quórums reforzados pueden justificarse como mecanismos que exigen acuerdos más amplios para modificar reglas especialmente importantes y dificultan cambios abruptos por mayorías circunstanciales.',
          'Pero también pueden entregar poder de veto a minorías y dificultar que una mayoría electoral implemente decisiones. Por eso la discusión sobre quórums no es puramente matemática: enfrenta valores de estabilidad, protección de minorías, capacidad de decisión y regla mayoritaria.'
        ],
        sourceIds: ['reforma21481Constitucion', 'reforma21535Quorums']
      }
    ],
    sourceIds: ['constitucionArt66Actual', 'reforma21535Quorums', 'reforma21481Constitucion', 'camaraGlosarioQuorum', 'reglamentoVotaciones145', 'camaraVotaciones2026']
  };
})();
