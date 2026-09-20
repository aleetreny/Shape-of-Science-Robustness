# Cinco comentarios del autor resueltos

**Edición vigente, 20-09-2026:** [V2 elegida y explicación reescrita](MANUSCRIPT_CLARITY.md). Inglés: 3.989 palabras de cuerpo y resumen de 192, PDF de 19 páginas; español: 20 páginas. Suplementos: 34 y 36. El título, los resultados y las declaraciones se conservan. Las cifras de extensión y páginas que siguen pertenecen al registro histórico del 18-09; las rutas estables de PDF ahora abren la edición vigente.

## Registro histórico de esta revisión

18-09-2026. Cambios de presentación aplicados al inglés y al español. Se conservan resultados, criterios, referencias y límites. El artículo inglés sigue teniendo 19 páginas; el español, 21. Los suplementos tienen 33 y 35.

| Comentario | Cambio | Página nueva, inglés / español |
| --- | --- | --- |
| 1. PubMedBERT ocupa dos líneas | Las cinco columnas se alinean al centro vertical de cada celda. Las cifras quedan a mitad de las dos líneas del nombre y centradas en sus columnas. | 6 / 7 |
| 2. Cuesta separar las filas del corpus | Más espacio entre las seis filas completas, manteniendo juntas las líneas de cada fila. | 5 / 6 |
| 3. Recuperar un título más directo | **How much does the map of science depend on the embedding model?** En español: **¿Cuánto depende el mapa de la ciencia del modelo de embeddings?** | 1 / 1 |
| 4. Utilidad de la Figura 1B | Sustituidas las líneas casi superpuestas por medias identificadas y rangos descriptivos de las comparaciones. | 9 / 11 |
| 5. Acortar la declaración de IA | Dos frases que indican la ayuda real recibida y la responsabilidad del autor. | 17 / 19 |

El título recoge la pregunta propuesta por el autor con una construcción inglesa más natural. No implica que el estudio estime qué porcentaje del mapa es correcto.

## Qué aporta ahora la figura

El promedio cambia muy poco entre 128, 256 y 512 artículos por grupo. Ese resultado es útil, pero dos líneas planas ocultaban la variedad de comparaciones que hay detrás. Ahora cada tamaño muestra la media y los percentiles 2,5–97,5 de los resultados de grupo y pareja de modelos: 1.170 comparaciones de áreas y 8.235 de especialidades. Se utilizan los seis resúmenes ya guardados, sin calcular una nueva medida científica.

Se conserva la escala completa de 0 a 1. Las líneas muestran dispersión descriptiva, **no intervalos de confianza ni una prueba de estabilidad de cada comparación**. Las parejas de modelos comparten modelos y no son independientes. Esto queda explícito en el pie; las alertas anteriores permanecen. Los paneles A y B siguen comparando objetos diferentes.

## Declaración breve

> OpenAI Codex assisted with literature searches, software development and analysis, visualisation, and manuscript drafting and editing. The author is responsible for the content.

La política general de [MIT Press](https://mitpress.mit.edu/for-authors/), consultada el 18-09-2026, exige transparencia sobre la ayuda de IA y atribuye la responsabilidad al autor. No prescribe el párrafo largo anterior. El acceso directo a las [normas específicas de QSS](https://direct.mit.edu/qss/pages/submission-guidelines) volvió a fallar; no se presenta ese acceso como una comprobación satisfactoria. La versión indexada de las [normas para revistas](https://direct.mit.edu/journals/pages/authors) coincide, pero es antigua. Comprobar los requisitos finales al preparar el envío.

La declaración no dice que la intervención fuera solo una corrección lingüística, ni atribuye al autor una revisión personal ya terminada. Esa aprobación sigue pendiente.

## Comprobaciones y entrega

- [Artículo inglés](output/pdf/main.pdf) y [suplemento inglés](output/pdf/supplement.pdf).
- [Artículo español](output/pdf/es/main.pdf) y [suplemento español](output/pdf/es/supplement.pdf).
- Paquetes editables: [inglés](output/manuscript_source.zip) y [español](output/manuscript_source_es.zip).
- [Comprobación de cifras y cambios](research/manuscript_comments_2026-09-18/numeric_layout_audit.json), [revisión visual](research/manuscript_comments_2026-09-18/visual_review.json) y [cierre](research/manuscript_comments_2026-09-18/closure_audit.json).

Las copias anteriores se guardan en `data/manuscript_comments_v1/baseline/`; sus huellas están en `research/manuscript_comments_2026-09-18/baseline_manifest.json`. Los registros de las entregas anteriores conservan su estado histórico. No hubo nuevos experimentos, publicación o envío.
