(() => {
  const data = window.CONGRESS_EDUCATION;
  if (!data) return;

  Object.assign(data.sources, {
    camaraActual: {
      label: 'Formación ciudadana · Cámara de Diputadas y Diputados',
      publisher: 'Cámara de Diputadas y Diputados de Chile',
      url: 'https://www.camara.cl/formacion_ciudadana/faq.aspx',
      note: 'Fuente institucional sobre composición de la Cámara: 155 integrantes elegidos directamente en 28 distritos por cuatro años.'
    },
    senadoActual: {
      label: 'Senadoras y senadores',
      publisher: 'Senado de la República de Chile',
      url: 'https://www.senado.cl/senadoras-y-senadores',
      note: 'Fuente institucional actual: 50 integrantes elegidos directamente en 16 circunscripciones senatoriales por ocho años.'
    },
    constitucion49: {
      label: 'Constitución Política · artículo 49',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=242302',
      note: 'Regula la elección del Senado por circunscripciones senatoriales en consideración a las regiones, mandatos de ocho años y renovación alternada.'
    },
    senadoElectoralVigente: {
      label: 'Ley electoral · artículo 190',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=1108229&idParte=9836522&idVersion=2021-10-21',
      note: 'Establece un Senado de 50 miembros y una circunscripción por región; las regiones eligen cantidades diferentes de senadores.'
    },
    historia1828: {
      label: 'Períodos legislativos e historia del Congreso Nacional',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/corporaciones/periodos_legislativos_index',
      note: 'Identifica la Constitución de 1828 como punto de inflexión que establece el bicameralismo con Cámara de Senadores y Cámara de Diputados y da continuidad a los períodos legislativos.'
    },
    historiaBicameral1829: {
      label: 'Elecciones parlamentarias de 1829',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/elecciones/detalle_eleccion?handle=10221.1%2F62591&periodo=1823-1833',
      note: 'Registra la elección del primer Congreso bicameral bajo las normas de la Constitución de 1828.'
    },
    finDesignados2006: {
      label: 'Derogación de senadores designados y vitalicios',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/historiapolitica/hitos_periodo/detalle_periodo.html?K=1&filtros=1%2C2%2C3%2C4%2C5%2C6&pagina=5&per=1990-2022',
      note: 'Desde el 11 de marzo de 2006 el Senado quedó integrado únicamente por miembros elegidos, tras la reforma constitucional de 2005.'
    },
    reformaSenado2015: {
      label: 'Ley N.º 20.840 · nueva composición del Senado',
      publisher: 'Biblioteca del Congreso Nacional de Chile',
      url: 'https://www.bcn.cl/leychile/navegar?idNorma=1077039&idParte=9593345&idVersion=2015-05-05',
      note: 'Estableció la estructura de 50 senadores y circunscripciones regionales con magnitudes diferenciadas.'
    },
    uhrBicameralism: {
      label: 'Bicameralism',
      publisher: 'The Oxford Handbook of Political Institutions · Oxford Academic',
      url: 'https://academic.oup.com/edited-volume/34346/chapter-abstract/291404607',
      note: 'Revisión comparada que sostiene que no existe un único modelo ni una única teoría explicativa del bicameralismo.'
    },
    hellerBranduse2014: {
      label: 'The Politics of Bicameralism',
      publisher: 'The Oxford Handbook of Legislative Studies · Oxford Academic',
      url: 'https://academic.oup.com/edited-volume/35475/chapter-abstract/303832623',
      note: 'Subraya que la existencia de dos cámaras dice poco por sí sola: importan sus poderes relativos y la negociación intercameral.'
    },
    testa2019: {
      label: 'Bicameralism',
      publisher: 'The Oxford Handbook of Public Choice · Oxford Academic',
      url: 'https://academic.oup.com/edited-volume/34674/chapter-abstract/295449058',
      note: 'Revisa posibles beneficios del bicameralismo —representación de intereses heterogéneos, estabilidad, accountability y revisión— y sus costos, incluida mayor complejidad y riesgo de bloqueo.'
    },
    waldron2012: {
      label: 'Bicameralism and the Separation of Powers',
      publisher: 'Current Legal Problems · Oxford Academic',
      url: 'https://academic.oup.com/clp/article/65/1/31/356923',
      note: 'Argumenta que la justificación del bicameralismo depende crucialmente de qué diferencias institucionales existan entre una cámara y otra.'
    }
  });

  data.lessons['camara-y-senado'] = {
    title: 'Cámara y Senado: dos cámaras, un Congreso',
    unit: 'camaras',
    status: 'ready',
    readingTime: '8–10 min',
    intro: 'Chile tiene un Congreso bicameral. Cámara y Senado participan en la formación de las leyes, pero no son duplicados: representan territorios mediante reglas diferentes, tienen mandatos distintos y poseen atribuciones exclusivas propias.',
    keyPoints: [
      'El Congreso Nacional se compone de la Cámara de Diputadas y Diputados y el Senado; ambas ramas concurren a la formación de las leyes.',
      'La Cámara tiene 155 integrantes elegidos en 28 distritos por cuatro años.',
      'El Senado tiene 50 integrantes elegidos en 16 circunscripciones regionales por ocho años y se renueva de manera alternada.',
      'Las regiones no tienen representación senatorial igual: la ley asigna entre 2 y 5 escaños según la circunscripción.',
      'Fiscalizar los actos del Gobierno es atribución exclusiva de la Cámara; el Senado posee otras atribuciones exclusivas, por lo que no son instituciones intercambiables.'
    ],
    blocks: [
      {
        type: 'intuition',
        title: 'La intuición: dos decisiones institucionales, no una votación repetida',
        paragraphs: [
          'La explicación escolar suele decir que existe una segunda cámara “para revisar” lo que hace la primera. La revisión es parte del bicameralismo, pero esa frase es demasiado pobre. En Chile muchas decisiones legislativas deben atravesar <strong>dos cuerpos representativos distintos</strong>, cada uno con su propia composición, mandato, organización y atribuciones.',
          'Eso obliga a construir acuerdos en dos arenas institucionales. A veces la segunda cámara confirma el texto; otras veces lo modifica, lo rechaza o genera una discrepancia que debe resolverse mediante los procedimientos constitucionales correspondientes.'
        ],
        sourceIds: ['constitucion46', 'hellerBranduse2014']
      },
      {
        type: 'institution',
        title: 'La Cámara: representación distrital y mandato de cuatro años',
        paragraphs: [
          'La Cámara de Diputadas y Diputados tiene actualmente <strong>155 integrantes</strong> elegidos directamente en <strong>28 distritos</strong>. Sus mandatos duran cuatro años. Los distritos agrupan comunas y eligen varios representantes, de modo que la Cámara combina proporcionalidad electoral y representación territorial subregional.',
          'Además de participar en la formación de la ley, la Constitución entrega a la Cámara atribuciones exclusivas. Entre ellas se encuentra la <strong>fiscalización de los actos del Gobierno</strong>, que se ejerce mediante mecanismos constitucionales específicos.'
        ],
        sourceIds: ['camaraActual', 'constitucion52']
      },
      {
        type: 'institution',
        title: 'El Senado: circunscripciones regionales, ocho años y renovación alternada',
        paragraphs: [
          'El Senado está integrado actualmente por <strong>50 senadoras y senadores</strong> elegidos directamente en <strong>16 circunscripciones senatoriales</strong>, una por cada región. Sus integrantes permanecen ocho años en el cargo y la Constitución dispone una renovación alternada cada cuatro años.',
          'Que las circunscripciones correspondan a regiones no significa que todas tengan el mismo número de escaños. La legislación electoral asigna magnitudes diferentes: algunas regiones eligen dos senadores y otras tres o cinco. Por eso sería impreciso describir al Senado chileno como una cámara de igualdad territorial entre regiones.'
        ],
        sourceIds: ['senadoActual', 'constitucion49', 'senadoElectoralVigente']
      },
      {
        type: 'institution',
        title: 'Simetría legislativa y asimetría de atribuciones',
        paragraphs: [
          'En gran parte del proceso legislativo ambas cámaras poseen una posición fuerte: un proyecto normalmente necesita atravesar Cámara y Senado y las discrepancias entre ellas deben resolverse mediante procedimientos constitucionales. En ese sentido, no estamos ante una segunda cámara meramente consultiva.',
          'Pero esa fuerza legislativa no vuelve idénticas a las corporaciones. La Cámara fiscaliza los actos del Gobierno y declara si ha lugar determinadas acusaciones constitucionales; el Senado conoce esas acusaciones y posee, además, competencias propias respecto de ciertos nombramientos y actos presidenciales. La distribución de funciones es deliberadamente diferenciada.'
        ],
        sourceIds: ['constitucion46', 'constitucion52', 'senadoAtribuciones']
      },
      {
        type: 'evidence',
        title: 'El bicameralismo no es una institución única',
        paragraphs: [
          'La literatura comparada advierte que decir simplemente “este país tiene dos cámaras” entrega muy poca información. Los sistemas bicamerales difieren en cómo se seleccionan sus integrantes, qué territorios o intereses representan, cuánto duran sus mandatos y, sobre todo, cuánto poder tiene cada cámara frente a la otra.',
          'Por eso se estudia tanto la <strong>diferencia entre las cámaras</strong> como su existencia. Una segunda cámara puede ser muy poderosa o relativamente débil; puede representar territorios en pie de igualdad o con magnitudes distintas; puede ser elegida, designada o combinar mecanismos. Chile constituye una configuración específica dentro de ese universo.'
        ],
        sourceIds: ['uhrBicameralism', 'hellerBranduse2014', 'waldron2012']
      },
      {
        type: 'evidence',
        title: '¿Qué puede aportar una segunda cámara y qué puede costar?',
        paragraphs: [
          'Entre las justificaciones comparadas del bicameralismo aparecen la representación de intereses o territorios heterogéneos, una instancia adicional de revisión, mayor estabilidad de las decisiones y mecanismos adicionales de accountability. Sin embargo, esos efectos dependen del diseño concreto y no son consecuencias automáticas de tener dos cámaras.',
          'También existen costos potenciales: más pasos procedimentales, negociación adicional, menor claridad sobre quién es responsable de una decisión y posibilidad de bloqueo cuando ambas cámaras discrepan. Una pedagogía rigurosa no debe presentar al bicameralismo como sinónimo de “leyes mejores”, sino como una arquitectura con ventajas y costos posibles.'
        ],
        sourceIds: ['testa2019', 'uhrBicameralism']
      },
      {
        type: 'history',
        title: 'El bicameralismo chileno también cambió profundamente',
        paragraphs: [
          'Chile experimentó tempranamente con distintos cuerpos legislativos. La Constitución de 1828 marca el punto de inflexión que la historia institucional de la BCN utiliza para identificar el establecimiento de un Congreso bicameral con Cámara de Senadores y Cámara de Diputados y el inicio de los períodos legislativos que se numeran hasta hoy. El primer Congreso elegido bajo esas reglas funcionó desde 1829.',
          'Pero el Senado de entonces no era el Senado actual. Su composición y forma de selección cambiaron repetidamente. Bajo la Constitución de 1980, por ejemplo, el Senado democrático reabierto en 1990 coexistió con senadores designados y vitalicios. Esas figuras fueron eliminadas por la reforma constitucional de 2005 y dejaron definitivamente la corporación el 11 de marzo de 2006. La reforma electoral de 2015 estableció posteriormente la estructura de 50 senadores y circunscripciones regionales que organiza el Senado contemporáneo.'
        ],
        sourceIds: ['historia1828', 'historiaBicameral1829', 'finDesignados2006', 'reformaSenado2015']
      },
      {
        type: 'myth',
        title: 'Cuatro ideas que conviene corregir',
        bullets: [
          '<strong>“El Senado simplemente vuelve a votar lo mismo”.</strong> No. Puede aprobar, rechazar o modificar textos y tiene además atribuciones exclusivas propias.',
          '<strong>“La Cámara es la única cámara realmente democrática y el Senado es solo una cámara técnica”.</strong> No. Actualmente ambas corporaciones se integran mediante elección directa; su diferencia no puede reducirse a una oposición entre política y técnica.',
          '<strong>“El Senado representa a todas las regiones por igual”.</strong> No. Cada región constituye una circunscripción, pero la cantidad de senadores varía entre ellas.',
          '<strong>“Dos cámaras garantizan mejores leyes”.</strong> No existe tal garantía. La investigación identifica beneficios posibles y también costos de complejidad y bloqueo.'
        ],
        sourceIds: ['senadoActual', 'senadoElectoralVigente', 'testa2019']
      },
      {
        type: 'debate',
        title: 'La pregunta normativa permanece abierta: ¿por qué dos cámaras?',
        paragraphs: [
          'La descripción institucional permite explicar cómo funciona el sistema chileno, pero no demuestra que sea el diseño óptimo. La teoría del bicameralismo pregunta qué diferencias justifican mantener una segunda cámara, qué intereses debe representar, cuánto poder debe poseer y si la revisión adicional compensa los costos decisorios.',
          'Ese debate no se resuelve diciendo que “Chile siempre ha sido bicameral”. La historia explica cómo llegamos aquí; la justificación normativa exige argumentos propios sobre representación, control, calidad legislativa, estabilidad y capacidad de decisión.'
        ],
        sourceIds: ['waldron2012', 'uhrBicameralism', 'testa2019']
      }
    ],
    sourceIds: ['constitucion46', 'constitucion52', 'camaraActual', 'senadoActual', 'constitucion49', 'senadoElectoralVigente', 'senadoAtribuciones', 'historia1828', 'historiaBicameral1829', 'finDesignados2006', 'reformaSenado2015', 'uhrBicameralism', 'hellerBranduse2014', 'testa2019', 'waldron2012']
  };

  if (!data.featuredQuestions.some((item) => item.id === 'camara-y-senado')) {
    const index = Math.max(0, data.featuredQuestions.findIndex((item) => item.id === 'quien-me-representa') + 1);
    data.featuredQuestions.splice(index, 0, {
      id: 'camara-y-senado',
      unit: 'camaras',
      title: '¿Por qué Chile tiene Cámara y Senado?',
      summary: 'Dos cámaras participan en la legislación, pero difieren en composición, mandato, representación territorial y atribuciones exclusivas.',
      status: 'ready'
    });
  }
})();
