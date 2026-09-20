# Revisión de la introducción y los antecedentes

18-09-2026. Primer borrador solicitado por el autor. Texto en `manuscript/main.tex`, páginas 3–5 del PDF principal. La petición de empezar por estos bloques sustituye el orden anterior de métodos/resultados; no autoriza escribir el resto del paper.

## Extensión y voz

367 palabras de introducción y 627 de antecedentes/preguntas: **994 palabras de prosa**, sin títulos ni expansiones de citas. El presupuesto inicial era 1.550; se ha reducido sin rellenar los párrafos hasta una longitud uniforme. El recuento y su regla se conservan en `word_count.json`.

Se aplica `AUTHOR_VOICE.md`: problema concreto antes de técnicas, explicación del mecanismo, verbos directos y límites ligados a la afirmación. Se conservan los tres subtítulos aceptados y las preguntas, pero no se impone una longitud fija a los párrafos. No hay historia ficticia de descubrimiento, autoelogio, promesa de novedad absoluta, detector de autoría ni plural de autores supuesto. La voz inglesa sigue pendiente de la revisión personal del autor.

## Fuentes de las afirmaciones externas

| Afirmación incluida | Fuente primaria y comprobación | Límite mantenido |
| --- | --- | --- |
| La relación entre estructura temática y método tiene antecedentes. | [Gläser et al., 2017](https://doi.org/10.1007/s11192-017-2296-z): resumen editorial consultado de nuevo. | No se le atribuyen experimentos con transformers. |
| Puntuaciones agregadas parecidas pueden coexistir con distintas pertenencias a grupos. | [Boyack y Klavans, 2020](https://doi.org/10.1162/qss_a_00085): resumen e introducción del texto editorial guardado en `data/qss_structure_review_v1/publisher_texts/qss_a_00085.txt`. | Son agrupaciones de texto/citas/híbridos, no nuestros diez encoders. Acceso web directo fallido; se reutiliza la copia previamente verificada. |
| Comparación de texto/grafo y entradas frente a la clasificación de Física. | [Constantino et al., 2025](https://doi.org/10.1162/qss_a_00349): resumen, datos, evaluación y límites de la copia consultada en `data/qss_structure_review_v1/publisher_texts/qss_a_00349.txt`. | Se cita la edición de QSS; no se traslada su evaluación con PACS como validación de OpenAlex. Acceso directo actual fallido. |
| Modelos y pooling comparados antes de construir el mapa biomédico; evaluación con etiquetas de los vecinos. | [González-Márquez et al., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11240179/): resultados y procedimientos del texto abierto. | Sus etiquetas proceden de títulos de revistas; el borrador habla de etiquetas de áreas, sin suponer validación individual por expertos. |
| Las consultas cortas y perturbaciones del texto afectan a la recuperación. | [Singh y Singh, 2022](https://aclanthology.org/2022.findings-acl.249/): resumen editorial y metadatos oficiales consultados de nuevo. | No se atribuye a este trabajo nuestro cruce exacto de tres entradas. |
| Comparación conjunta de geometría y vecinos recuperados. | [Caspari et al., 2024](https://arxiv.org/abs/2407.08275): resumen de autores y registro v1 consultados de nuevo. | Se mantiene como preprint; no se presenta la combinación de medidas como nueva. |
| Densidad/asimetría en varias representaciones y disciplinas, relacionadas con citas. | [Imel y Hafen, 2025](https://arxiv.org/abs/2506.23366): resumen y registro v1 consultados de nuevo. | Se mantiene como preprint y no se equiparan sus medidas a las nuestras. |
| Interpretar agrupaciones exige atender al significado de las relaciones entre artículos. | [Held y Velden, 2022](https://doi.org/10.1162/qss_a_00194): resumen y secciones de validación del texto editorial guardado en `data/qss_structure_review_v1/publisher_texts/qss_a_00194.txt`. | Estudio de invasión biológica basado en citas y contexto cualitativo; no valida directamente nuestros embeddings. |

La selección desarrolla los antecedentes próximos del plano; no pretende revisar exhaustivamente toda la literatura en estos dos bloques. Las definiciones de acuerdo, estabilidad y alcance geométrico son operativas de este estudio; no se atribuyen como taxonomía literal a Held y Velden.

## Afirmaciones sobre nuestro estudio

- Corpus, fechas, idioma y 26 Fields: `CORPUS_PROTOCOL.md`, `CLEANING.md` y tabla principal de paneles. Se mencionan subconjuntos para cambios de entrada/representación, sin extender esos cálculos a los 500.000.
- Acuerdo amplio y variación local: `ANALYSIS_RESULTS.md` y los controles de `ROBUSTNESS_RESULTS.md`. No se afirma un descenso universal de acuerdo con la escala.
- Direcciones opuestas persistentes y necesidad de mirar magnitudes: `FIELD_PAIR_RESULTS.md`. No se afirma que todos los modelos discrepen ni que todas las diferencias sean grandes. El efecto del procesamiento queda señalado.
- Forma: espacio de embeddings antes de proyección bidimensional. Apertura y dimensión son propiedades geométricas; no diversidad temática o número de temas.
- RQ3 permanece explícitamente exploratoria y posterior. OpenAlex organiza la comparación, conserva errores y no sirve como verdad externa. No se elige un modelo ganador ni se afirma representatividad mundial.

## Citas y composición

Ocho referencias únicas en la apertura; 17 al incluir las nueve de la tabla de modelos. `citation_validation.json` comprueba las 17 contra el texto con sus tablas incluidas: cero errores, avisos, duplicados o citas sin resolver. Es validación de metadatos/consistencia; la revisión de las afirmaciones es la tabla anterior.

Se reutiliza la biblioteca canónica de 54 entradas sin modificarla. La copia tipográfica `manuscript/references.bib` escapa únicamente el guion largo del título de Gläser mediante `---`: conserva su significado y corrige un glifo ausente. `context_references.bib` incorpora exactamente la entrada de Held y Velden de la biblioteca QSS, sin duplicados. La compilación final no presenta glifos ausentes, referencias indefinidas o texto desbordado. Se evita una primera línea de párrafo aislada al final de página.

El validador no pudo ejecutarse con el Python de documentos por falta de `requests`; se usó el entorno de auditoría ya existente, sin instalar paquetes ni cambiar entornos. No se alteraron datos, tablas, figuras, fórmulas o criterios científicos.
