# Qué estructura encaja con nuestro estudio en QSS

**Revisión del 18-09-2026. Propuesta para discutir; no es el manuscrito.**

Recomiendo presentar el trabajo como un estudio de **qué conclusiones sobre los mapas de ciencia se mantienen al cambiar la forma de representar los mismos artículos**. El hilo debe ir de la imagen general a las relaciones concretas y, finalmente, a las comparaciones entre disciplinas. Los modelos y las medidas son las herramientas que permiten responder esa pregunta.

Es una recomendación basada en las fuentes y en nuestro diseño. No existe una estructura demostrablemente óptima para cualquier revisor. La organización aplicada, con preguntas, extensión, figuras y resultados concretos, está en [PAPER_OUTLINE.md](PAPER_OUTLINE.md).

## 1. Qué se revisó realmente

Se recuperaron **465 registros** del catálogo Crossref de QSS, ISSN 2641-3337, publicados hasta el 18-09-2026: dos páginas, 465 esperados y 465 recuperados. Incluye editoriales y otros tipos. Ese número describe el marco bibliográfico, **no artículos leídos**. De ahí se seleccionaron **34 trabajos de 2020–2026** por cercanía a mapas de ciencia, comparación de representaciones, clasificación, medición, interpretación y calidad de fuentes. Un trabajo sobre la estructura de los artículos aporta contexto para esta revisión editorial.

El cribado fue dirigido, apoyado en títulos/resúmenes y búsquedas por tema; no una evaluación manual exhaustiva de cada registro ni una selección aleatoria. Se buscó variedad de enfoques y de fechas. No es una revisión sistemática de efectos ni permite estimar qué porcentaje de toda QSS usa una estructura.

| Cobertura | Resultado |
| --- | --- |
| Trabajos seleccionados | 34: nueve de 2020, cinco de 2021, cinco de 2022, dos de 2023, uno de 2024, ocho de 2025 y cuatro de 2026 |
| Textos disponibles y lectura estructural | 33: resumen, secuencia de secciones y pasajes de introducción, método/resultados y cierre |
| Lectura focal adicional | 11 de esos 33, centrada en comparación, validez, interpretación y límites |
| Acceso parcial | Donner y Henneken (2025), Q25: resumen e inicio; excluido de conclusiones sobre estructura |
| Versiones consultadas | 20 editoriales identificadas, dos publicaciones anticipadas, nueve manuscritos de autor —uno aceptado— y dos cuerpos de texto cuya versión tipográfica no se certificó |
| Qué no se hizo | Lectura íntegra de todos los párrafos/suplementos, repetición de sus análisis, medición automática del estilo o estimación de aceptación editorial |

Los manuscritos de autor sirven para estudiar el argumento; no certifican la maquetación final. En particular, el preprint Q34 sitúa métodos al final: **no se utiliza como evidencia de una excepción editorial**. La extracción de algunos PDF pierde encabezados o coloca pies en medio del texto. Las notas describen funciones y declaran esas pérdidas; no se han convertido los encabezados extraídos automáticamente en recuentos de normas.

Una recuperación para Q25 devolvió su ficha acompañada del cuerpo de un artículo distinto. Se rechazó. Las copias largas quedan en `data/qss_structure_review_v1/`, fuera de Git. Se conserva la fecha, fuente y huella de cada copia usada.

Material verificable:

- [Notas de los 34 artículos](research/qss_structure_2026-09-18/READING_NOTES.md), con DOI, copia consultada, versión y límite.
- [Matriz CSV](research/qss_structure_2026-09-18/article_matrix.csv), [cobertura](research/qss_structure_2026-09-18/coverage.json) y [catálogo de 465 registros](research/qss_structure_2026-09-18/journal_inventory.json).
- [Bibliografía de la revisión](research/qss_structure_2026-09-18/qss_review.bib): metadatos Crossref, 34 entradas, cero errores de formato/duplicados; un aviso por volumen ausente en Q34. No se inventó ese volumen. No sustituye ni se suma sin deduplicar a la biblioteca científica de 54 referencias.

## 2. Qué pide QSS y qué estamos recomendando nosotros

La guía oficial consultada **no impone una estructura única**. Admite la organización de introducción, métodos, resultados y discusión, y pide que los métodos aparezcan en la primera parte. Señala resumen de hasta 200 palabras, hasta seis palabras clave y normalmente 5.000–8.000 palabras para investigación original; esta última cifra es orientación, no un máximo rígido. El primer envío permite formato flexible. Para la preparación final indica secciones numeradas y referencias de autor/año, con formato APA. Incluye declaraciones de contribución, intereses y disponibilidad; pide depositar datos esenciales con identificador persistente, con excepciones justificadas, y recomienda compartir código. [Guía oficial](https://direct.mit.edu/qss/pages/submission-guidelines).

**Límite de esta comprobación:** el acceso directo devolvió 403. Se leyó la versión indexada de la página oficial, con rastreo antiguo —el buscador indicaba aproximadamente 1,3 años—. No se certifica que cada detalle siga vigente hoy. Antes del envío hay que consultar la guía en directo. Esto no impide estudiar artículos ya publicados ni preparar un esquema.

El alcance editorial exige una aportación al conocimiento sobre la ciencia. Para nosotros, eso favorece explicar las consecuencias de elegir una representación, además de describir su funcionamiento. Es nuestra aplicación del alcance al proyecto, no una exigencia de usar determinadas medidas. [Alcance de QSS](https://direct.mit.edu/qss).

| Tipo de afirmación | Ejemplo | Cómo se usa |
| --- | --- | --- |
| Indicación editorial consultada | Resumen de hasta 200 palabras; métodos en la primera parte | Se sigue y se vuelve a verificar antes del envío |
| Práctica observada | Separar antecedentes; unir o separar discusión y conclusiones | Muestra opciones publicadas, no obligaciones |
| Propuesta para este estudio | Seis secciones, tres preguntas, cuatro figuras principales | Elección de organización pendiente de conversar con el usuario |
| Afirmación que no podemos hacer | “Esta estructura evitará objeciones de los revisores” | No hay evidencia para prometerlo |

## 3. Las formas de artículo que aparecen en la muestra

No todos los trabajos cercanos pertenecen al mismo tipo de artículo. Copiar el más largo o el más técnico puede desviar nuestro mensaje.

| Forma de artículo | Ejemplos de QSS | Lo que organiza el texto | Encaje con nosotros |
| --- | --- | --- | --- |
| Comparación y consecuencias de una elección | [Boyack y Klavans, 2020](https://doi.org/10.1162/qss_a_00085); [Armitage et al., 2020](https://doi.org/10.1162/qss_a_00071); [Sīle et al., 2021](https://doi.org/10.1162/qss_a_00110) | Comparación → diferencias relevantes → implicaciones de uso | **Encaje principal** |
| Concepto y validez de la herramienta | [Held, 2022](https://doi.org/10.1162/qss_a_00217); [Held y Velden, 2022](https://doi.org/10.1162/qss_a_00194) | Qué se pretende representar → qué hace la herramienta → qué interpretación permite | Fundamenta nuestras distinciones y límites |
| Propuesta técnica y evaluación | [Ahlgren et al., 2020](https://doi.org/10.1162/qss_a_00027); [Rao et al., 2025](https://doi.org/10.1162/qss.a.2) | Método → prueba → rendimiento/aplicación | Útil como referencia, pero no hemos creado un encoder ganador |
| Mapa aplicado a una pregunta sobre ciencia | [Gargiulo et al., 2023](https://doi.org/10.1162/qss_a_00267); [Plazas et al., 2026](https://doi.org/10.1162/qss.a.489) | Mapa general → fenómenos o usos concretos → significado | Inspira pasar del promedio a consecuencias y casos |
| Recurso, software o revisión | [Färber y Ao, 2022](https://doi.org/10.1162/qss_a_00183); [Gates y Barabási, 2023](https://doi.org/10.1162/qss_a_00260); [Salatino et al., 2025](https://doi.org/10.1162/qss_a_00363) | Componentes, funciones o dimensiones de una revisión | Nuestro repositorio sostiene el paper, pero no debe organizarlo |

Hay resultados y discusión unidos —Q16, Q28, Q31—, discusión y conclusiones unidas —Q02, Q04, Q05, Q23—, y cierres separados —Q10, Q17, Q18, Q22—. Algunas secciones de resultados llevan el nombre de la pregunta o del objeto. La lista no pretende fijar frecuencias de toda la revista.

Nathan et al. estudian precisamente la diferencia entre nombres y funciones de secciones. Su trabajo ayuda a evitar una lectura mecánica de los títulos, pero su corpus de varios editores no demuestra una norma específica de QSS. [Nathan et al., 2021](https://doi.org/10.1162/qss_a_00135).

## 4. Los antecedentes que más orientan nuestro argumento

Esta tabla resume lo que conviene aprender de los textos, no reproduce sus conclusiones como si fueran resultados nuestros.

| Trabajo | Lección pertinente | Aplicación y diferencia de nuestro estudio |
| --- | --- | --- |
| [Wang y Schneider, 2020](https://doi.org/10.1162/qss_a_00011) | Medidas muy relacionadas globalmente pueden cambiar comparaciones concretas entre áreas | Dar peso a las 325 parejas, además de las correlaciones generales. Nosotros estudiamos descripciones geométricas, no validez de indicadores de interdisciplinariedad |
| [Huang et al., 2020](https://doi.org/10.1162/qss_a_00031) | Las diferencias entre fuentes importan por sus consecuencias en rankings | Mostrar qué conclusión cambia y de cuánto es la diferencia; mantener fuente y artículos comunes en cada comparación |
| [Waltman et al., 2020](https://doi.org/10.1162/qss_a_00035) | La interpretación como precisión necesita un criterio de evaluación defendible | Nuestra comparación mide acuerdo. No convertir la coincidencia de encoders en exactitud temática |
| [Armitage et al., 2020](https://doi.org/10.1162/qss_a_00071) | Elecciones razonables de delimitación pueden producir resultados muy diferentes | Terminar cada bloque con su consecuencia práctica, dejando claro el universo comparado |
| [Boyack y Klavans, 2020](https://doi.org/10.1162/qss_a_00085) | Rendimientos agregados parecidos pueden coexistir con agrupaciones distintas | Reconocer ese antecedente y precisar qué añade nuestro cruce de encoder, entrada, escala y conclusiones entre áreas |
| [Sīle et al., 2021](https://doi.org/10.1162/qss_a_00110) | La semejanza del perfil general no garantiza semejanza en otras cantidades; las categorías tienen contexto | Separar objetos de comparación y no tratar Field/Subfield como límites naturales e infalibles |
| [Held y Velden, 2022](https://doi.org/10.1162/qss_a_00194) | Interpretar un mapa exige atender a qué perspectiva produce y cómo se valida | Usar los ejemplos para explicar el resultado, no para fingir validación temática experta |
| [Held, 2022](https://doi.org/10.1162/qss_a_00217) | Una propiedad matemática necesita una relación explícita con lo que se quiere estudiar | Definir apertura y reparto entre direcciones; evitar llamarlos diversidad, número de temas o fragmentación |
| [Constantino et al., 2025](https://doi.org/10.1162/qss_a_00349) | Compara representaciones de texto/red en Física y explicita los límites de etiquetas y texto disponible | Es uno de los vecinos más próximos. Nuestro objetivo es estabilidad entre representaciones textuales en 26 áreas, no clasificar mejor según PACS |
| [Cunningham et al., 2025](https://doi.org/10.1162/qss.a.9) | El valor de una representación depende del uso y del tipo de recomendación que se evalúa | No llamar “malos vecinos” a vecinos diferentes: nuestro acuerdo no evalúa relevancia para un usuario |
| [Plazas et al., 2026](https://doi.org/10.1162/qss.a.489) | Un mapa de grants pasa de estructura general a usos institucionales y territoriales; explicita límites de cobertura | Ayuda a dar sentido a la estabilidad de mapas. No pretendemos haber probado consecuencias reales de política científica |

La discusión debe reconocer también antecedentes próximos fuera de QSS: Caspari, González-Márquez, Bascur, Singh y otros ya recogidos en [RELATED_WORK.md](references/RELATED_WORK.md). Que esta revisión busque modelos de escritura de QSS **no justifica omitir literatura de otras revistas**.

El hueco propuesto es la **comparación controlada de la persistencia de conclusiones a varias escalas**, incluyendo el contenido de entrada y la dirección de comparaciones geométricas entre áreas. La combinación concreta debe explicarse frente a esos trabajos. “Diez modelos”, “500.000 artículos” o “forma y vecinos juntos” no bastan como afirmación de novedad.

## 5. Cómo argumentan estos trabajos y cómo aplicarlo

Las siguientes pautas son una síntesis interpretativa de los ejemplos, no un análisis estadístico de la prosa de QSS ni instrucciones recibidas de sus editores.

### Resumen: problema, diseño, resultados y consecuencia

Conviene que permita entender qué decisión está en juego, qué comparación se hizo y qué se aprendió. Para nuestro resumen propongo cuatro funciones, dentro de 180–200 palabras: problema; diseño y tamaños bien delimitados; dos resultados principales; consecuencia y límite. No una lista de modelos, siglas o controles. Los tamaños de las submuestras deben impedir que el lector crea que las tres entradas se calcularon en 500.000 artículos.

### Introducción: importancia sin exageración

Una entrada eficaz conecta mapas y estudios sobre organización de la ciencia. Después explica qué sabemos ya sobre dependencia de métodos, qué falta en esa evidencia y qué pregunta concreta respondemos. Cerrar con la aportación y un adelanto breve de los resultados.

No abrir con una historia general de la inteligencia artificial ni con una lista de arquitecturas. Tampoco afirmar que nadie ha comparado representaciones antes. Los ejemplos Q02, Q09, Q21, Q24 y Q28 ofrecen distintas maneras de enlazar el instrumento con su uso científico; no una fórmula que haya que copiar.

### Antecedentes: una comparación razonada

Necesitamos una sección breve propia porque el término “forma” es ambiguo y hay antecedentes próximos. Debe separar: coincidencia entre representaciones; evaluación con referencias externas; interpretación temática. Después ubicar nuestros tres niveles: estructura general, vecinos y comparaciones geométricas entre disciplinas.

La literatura se organiza por preguntas y diferencias, no con un párrafo aislado por cada paper. La tabla de antecedentes del suplemento puede contener más detalle que el texto principal.

### Métodos: justificar las comparaciones

Cada decisión importante debe responder a “¿qué confusión evita?”. Por ejemplo: mismos artículos evita comparar contenidos distintos; candidatos iguales ayuda a separar cambios de búsqueda; alternativas de medida muestran dependencia de la descripción elegida. También hay que explicar lo que esos controles **no** resuelven.

El cuerpo necesita las definiciones operativas mínimas y las reglas que determinan las conclusiones. Fórmulas extensas, versiones completas y tablas exhaustivas pueden ir al suplemento. Las reglas principales no deben quedar ocultas allí. Los análisis posteriores a resultados anteriores deben declararse como tales, sin fabricar un registro previo.

### Resultados: una afirmación, su magnitud y su límite

Para cada bloque, este orden:

1. Qué pregunta responde.
2. Qué se observa y en qué conjunto.
3. Cuánto cambia y cómo se reparte, no solo si cambia.
4. Qué comprobación sostiene o limita esa lectura.
5. Qué significa para interpretar el mapa.

La explicación de por qué pudo ocurrir —entrenamiento, dominio, composición— pertenece a discusión y debe mantener su carácter de hipótesis si no se identificó una causa. El propio resultado puede llevar una interpretación breve que ayude a leerlo.

### Discusión: volver a la pregunta científica

Primero responder las tres preguntas sin repetir todas las cifras. Después confrontar los antecedentes cercanos, explicar consecuencias de uso y exponer los límites que cambian la interpretación. Terminar con una continuación acotada. El formato de discusión separado nos conviene porque distingue con claridad la evidencia de sus posibles explicaciones.

Los artículos publicados contienen grados distintos de contundencia. No debemos imitar una afirmación fuerte solo porque fue publicada. La fuerza de nuestra frase debe ajustarse a nuestra evidencia.

### Vocabulario que necesitamos mantener constante

| Término del manuscrito | Significado en este estudio | Uso que se debe evitar |
| --- | --- | --- |
| *Agreement* | Coincidencia entre resultados de modelos | Exactitud temática |
| *Stability under resampling* | Persistencia al cambiar selecciones dentro de este corpus | Certeza sobre toda la población científica |
| *Encoder dependence* | Dependencia observada entre los modelos/recetas estudiados | Causa aislada del corpus de entrenamiento |
| *Geometric descriptor* | Descripción numérica de los vectores | Diversidad de ideas o número real de temas |
| *Persistent reversal* | Dos modelos sostienen direcciones opuestas en las selecciones definidas | Los diez modelos discrepan entre sí, o una diferencia es estadísticamente significativa |
| *Exploratory analysis* | Ampliación hecha después de conocer fases previas | Hipótesis confirmatoria fijada antes de todo el estudio |

Para observaciones, verbos directos como *we observed* o *we found* son adecuados si el conjunto y la comparación quedan claros. Para una explicación no demostrada, *may reflect* o *is consistent with* dejan visible ese límite. Son orientaciones propias de escritura, no frases copiadas ni un borrador del manuscrito.

## 6. Aplicación propuesta al paper

**Pregunta central:** ¿qué conclusiones sobre los mapas de ciencia se mantienen cuando cambiamos el modelo que representa los mismos artículos?

| Sección | Función para nuestro estudio |
| --- | --- |
| 1. Introduction | Presentar el problema, el hueco concreto y la aportación |
| 2. Background and research questions | Definir qué llamamos forma; separar acuerdo y validez; formular tres preguntas |
| 3. Data and comparative design | Explicar corpus, modelos, entradas, medidas, comparaciones y controles |
| 4. Results | Estructura general → vecinos → texto frente a modelo → comparaciones entre áreas |
| 5. Discussion | Interpretación, relación con antecedentes, consecuencias de uso y limitaciones |
| 6. Conclusion | Responder de forma breve qué aprendimos y qué no se puede inferir |

Propongo unas **6.750 palabras de cuerpo** como presupuesto de trabajo, cuatro figuras principales y dos tablas principales. No son límites de QSS ni un objetivo científico. El detalle está en [el esquema aplicado](PAPER_OUTLINE.md).

Las dos tablas deben aclarar el diseño y los modelos. Las cuatro figuras ya existen: escalas, vecinos comparables, efecto de entrada y conclusiones entre las 325 parejas. No hace falta producir un dibujo 2D atractivo para sostener una afirmación geométrica en los espacios originales.

Los resultados de tiempo, Medicina y familias ayudan a matizar el argumento, pero dar a cada uno una historia principal convertiría el paper en varios artículos superpuestos. Recomiendo conservarlos en suplemento, con las excepciones importantes mencionadas en resultados/discusión. El atlas añade ejemplos breves, expresamente exploratorios.

La conexión de grafos **no queda validada como fragmentación general**. Sus controles y contraejemplos se conservan en el suplemento; el texto principal debe reconocer que no se sostiene esa interpretación. No se elimina evidencia incómoda ni se presenta el descarte posterior como una decisión previa.

## 7. Qué debe verse incluso en una versión corta

- Los errores y avisos encontrados en OpenAlex; su diagnóstico limitado no estima todos los errores de clasificación.
- Los tamaños de cada análisis y la diferencia entre las dos selecciones de 52.000.
- Las alertas de estabilidad conservadas, con sus denominadores separados.
- La ausencia de una caída universal de acuerdo al pasar a Subfield y la dependencia temporal del número de candidatos.
- La cercanía de medias de entrada/modelo sin afirmar equivalencia ni una separación causal pura.
- La magnitud de las inversiones entre áreas, los casos no resueltos y la sensibilidad al centrado/receta.
- La naturaleza posterior de la ampliación geométrica y de varios controles.
- Que consenso no es verdad, las parejas no son independientes y no se elige un ganador.

Esos puntos delimitan la afirmación principal. Los cálculos completos pueden ir al suplemento, pero los límites que cambian el mensaje no pueden esconderse allí.

## 8. Estado de la propuesta

La revisión y la propuesta están terminadas. **No se ha empezado el manuscrito, cambiado un resultado científico ni publicado esta entrega.** La organización final queda para conversar con el usuario. La biblioteca de 34 artículos es material de consulta: no hay que citar todos en el paper por haberlos leído para estudiar su estructura.

Antes de redactar, basta con acordar este hilo y la jerarquía de resultados. No aparece una necesidad de otro experimento por motivos de estructura. Antes de enviar siguen pendientes las tareas reales de [QSS_CHECK.md](docs/QSS_CHECK.md), incluidos manuscrito revisado por autores, disponibilidad permanente y declaraciones veraces.

