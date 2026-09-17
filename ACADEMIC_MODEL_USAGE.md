# Qué modelos usan trabajos cercanos al nuestro

**Actualización posterior: el usuario eligió los diez (ocho + BioBERT y SimCSE).** La revisión siguiente conserva su evidencia y sus límites; selección vigente en `MODEL_SELECTION.md`.

Revisión dirigida del **15-09-2026**. El usuario pide priorizar los modelos utilizados para mapear la ciencia. Este criterio sustituye la propuesta centrada en diversificar familias recientes.

**Resultado:** SPECTER, SciBERT y la familia general Sentence-BERT aparecen repetidamente en los trabajos revisados. Dentro de Sentence-BERT encontramos MPNet y MiniLM. Los modelos generales sí tienen antecedentes claros en esta tarea.

## Qué cuenta esta revisión

Se contrastaron **diez trabajos** sobre mapas de publicaciones, estructura disciplinar, relaciones bibliométricas o evolución temática. Incluye aplicaciones y comparaciones metodológicas; algunos mapean un campo concreto y otros abarcan varias disciplinas. No es un censo de publicaciones ni una muestra aleatoria de toda la literatura.

Se buscaron tanto términos generales (`science mapping embeddings models comparison`, `mapping scientific literature sentence-transformers`) como modelos concretos, y se siguieron antecedentes ya localizados. Esto favorece encontrar familias conocidas. **Las frecuencias solo describen estos diez estudios; no estiman qué porcentaje de toda la comunidad usa cada modelo.** No llamarlos “los ocho más usados del mundo”.

Reglas: contar un modelo una vez por estudio si se usó en un análisis pertinente; distinguir aplicaciones de pruebas comparativas; no contar una mera cita, el modelo antecesor de otro, la biblioteca que lo ejecuta o dos versiones del mismo artículo. Tampoco sumar una prueba de recuperación de documentos separada como si fuera un mapa científico.

## Evidencia por trabajo

| Trabajo | Uso comprobado relevante | Qué se pudo leer |
| --- | --- | --- |
| [Lamers et al., ISSI 2021](https://cris.unibo.it/handle/11585/948699) | Compara BERT, SciBERT y SPECTER en relaciones entre publicaciones. | Registro institucional y resumen que enumera los modelos usados. PDF no recuperado; versiones exactas pendientes. |
| [González-Márquez et al., Patterns 2024](https://doi.org/10.1016/j.patter.2024.100968) | Mapa con PubMedBERT; prueba previa de BERT, SciBERT, BioBERT, MPNet, SPECTER, SimCSE y SciNCL, además de PubMedBERT. Control TF-IDF. | Texto completo y lista exacta de modelos, reutilizando el XML local. No se atribuye el mapa completo a los ocho modelos. |
| [Constantino et al., QSS 2025](https://arxiv.org/html/2308.15706v2) | SciBERT, MPNet en su variante `paraphrase` y Doc2Vec para estructura de Física. | Métodos de la versión completa de autores, sección 2.2.2. |
| [Huang et al., QSS 2025](https://direct.mit.edu/qss/article/doi/10.1162/qss_a_00344/125737/A-framework-for-demonstrating-forecasting-and) | MiniLM, MPNet y BERT para evolución de temas. | Fragmentos editoriales de métodos/resultados y [código de los autores](https://github.com/WannaLearning/Demonstrating-Forecasting-and-Explaining-Topic-Evolution). Representaciones de tema/contexto ligado a artículos; no idéntico a nuestro protocolo. |
| [Imel y Hafen, preprint 2025](https://arxiv.org/html/2506.23366v1) | SciBERT, SBERT, GPT-2, Word2Vec y bolsa de palabras para geometría y mapas de nueve disciplinas. | Métodos completos. Variante concreta de SBERT no identificada en lo leído; no se atribuye a MPNet o MiniLM. |
| [Liang et al., IP&M 2026](https://arxiv.org/pdf/2512.13054) | SciBERT, SPECTER, SPECTER2 y SciNCL en la comparación de mapas de PubMed. | PDF de autores, apartados 4.1.2 y 4.2. E5, Ada, BERT y otros pertenecen a otra evaluación: no se suman como modelos del mapa. DOI editorial confirmado: 10.1016/j.ipm.2025.104557. |
| [The Knowledge Cosmos, VISAP 2025](https://www.theknowledgecosmos.com/VISAP.pdf) | Mapa con SPECTER. | PDF completo del sitio del proyecto, con un título anterior al editorial. SciBERT se menciona como antecesor de SPECTER; no se cuenta como otro modelo utilizado. |
| [Identifying interdisciplinary emergence…, 2024](https://www.nature.com/articles/s41599-024-03044-y) | MiniLM dentro de BERTopic para estudiar temas en ciencia de la ciencia. | Métodos del HTML editorial. MPNet se menciona, pero no se ejecuta: no se cuenta. |
| [Evolution of Characterization Methods in Nanoscience, 2025](https://doi.org/10.1007/s40820-025-01807-z) | MiniLM dentro de BERTopic para temas y evolución de métodos. | XML completo de Europe PMC; métodos leídos. |
| [Bascur et al., versión evaluada en MetaROR 2026](https://metaror.org/article/use-of-diverse-data-sources-to-control-which-topics-emerge-in-a-science-map-2/) | SPECTER para redes de semejanza textual y mapas biomédicos. | Métodos del HTML completo. Su red llamada “BERT” usa realmente `allenai-specter`. Versiones agrupadas como un solo trabajo. |

## Cuáles se repiten

| Modelo o familia | Estudios de estos diez | Precisión necesaria |
| --- | ---: | --- |
| SPECTER original | 5 | Separado de SPECTER2. |
| SciBERT | 5 | Las recetas para obtener el vector no son iguales en todos los artículos. |
| BERT | 3 | Dos identifican `bert-base-uncased`; la variante de Lamers no está confirmada. |
| MPNet | 3 | Dos usan `all-mpnet-base-v2`; uno, `paraphrase-mpnet-base-v2`. |
| MiniLM | 3 | Los tres identifican `all-MiniLM-L6-v2`. |
| SciNCL | 2 | Comparaciones de representaciones para mapas. |
| SPECTER2 | 1 | Antecedente reciente de mapeo; no se presenta como uno de los más repetidos. |
| PubMedBERT | 1 | Modelo del mapa completo de biomedicina de González-Márquez et al. |
| BioBERT | 1 | Comparación previa del mismo trabajo biomédico. |
| SimCSE | 1 | Comparación previa del mismo trabajo biomédico. |
| GPT-2 | 1 | Comparación de Imel y Hafen. |
| SBERT sin variante identificada | 1 | No sumar a MPNet/MiniLM por suposición. |

La unión de MPNet, MiniLM y SBERT sin identificar aparece en **seis estudios**, contando una sola vez el trabajo de Huang, que usa ambos primeros. Este grupo general no incluye SPECTER/SciNCL simplemente porque puedan ejecutarse con la biblioteca Sentence-Transformers.

Son frecuencias de **uso como aplicación o comparación**, no solo de modelos elegidos para el mapa final. Un estudio que compara ocho modelos aporta más apariciones que uno con un único modelo. Diferentes estudios pueden compartir datos o equipos; no constituyen votos independientes sobre qué representación es mejor.

## Propuesta que se deriva de la revisión

Recomiendo como grupo de trabajo **ocho candidatos**: SPECTER, SPECTER2, SciNCL, SciBERT, BERT, MPNet, MiniLM y PubMedBERT. Los seis con más repetición forman el núcleo. SPECTER2 añade una versión científica posterior y la referencia del TFM; PubMedBERT añade el modelo usado en un mapa biomédico a gran escala. Esas dos incorporaciones se justifican por su papel, no por fingir una frecuencia alta.

Para diez, BioBERT y SimCSE permitirían cubrir también dos comparadores del estudio biomédico. Otra ampliación posible es `paraphrase-mpnet-base-v2`, para repetir la referencia exacta de Constantino. No es una familia nueva. No recomendaría incluir todos por defecto: el usuario aún debe elegir el conjunto concreto.

**TF-IDF**, una representación basada en las palabras de los artículos, queda propuesto como control adicional. Permitiría comprobar qué cambia respecto a una referencia sencilla. No es uno de los ocho modelos neuronales ni se ha autorizado su ejecución.

Qwen, BGE-M3, EmbeddingGemma, GTE y Jina quedan como alternativas de una futura ampliación: esta revisión no aporta evidencia suficiente para presentarlos como habituales en mapas científicos. Eso no demuestra que nadie los use. SemCSE es un antecedente científico reciente, pero todavía no se ha acreditado un uso extendido que lo sitúe por delante del núcleo anterior.

El uso previo apoya la relevancia de la selección para los lectores del paper. La aportación propuesta sigue siendo averiguar qué conclusiones resisten cambiar la representación en los mismos artículos, áreas y períodos; no se demuestra novedad contando modelos. Detalle vigente en [MODEL_SELECTION.md](MODEL_SELECTION.md).

## Comprobaciones y límites de acceso

- [Estudios y decisiones de conteo](research/model_review_2026-09-15/academic_sources/studies.json), [frecuencias](research/model_review_2026-09-15/academic_sources/model_occurrences.csv) y [huellas de la evidencia local](research/model_review_2026-09-15/academic_sources/evidence_manifest.json).
- Se corrigió una referencia del borrador: `10.1162/qss_a_00168` no pertenece a Lamers; Crossref lo identifica como otro artículo sobre Twitter/opioides. Se conserva la respuesta y se enlaza Lamers mediante su registro ISSI.
- No se contó [Which topics are best represented by science maps?](https://link.springer.com/article/10.1007/s11192-024-05218-6) como uso de SPECTER: ese trabajo de Bascur usa BM25. Tampoco se contó [Xie y Waltman](https://link.springer.com/article/10.1007/s11192-025-05324-z): mencionan embeddings, pero su comparación central es LDA frente a citas.
- Los accesos editoriales de QSS fallaron; Huang se verificó con fragmentos editoriales y código. Lamers solo está confirmado al nivel del resumen institucional. El PDF de Cosmos excedía el tamaño del lector web y se leyó localmente; Nanoscience se obtuvo mediante Europe PMC ante la comprobación de navegador de PMC. No se confundieron estos niveles de acceso.
- Una URL arXiv introducida por error resolvió a un artículo de física estadística; se descartó por título y se recuperó el identificador correcto de Liang, `2512.13054`. No influyó en las frecuencias.
- Se reutilizó la guía **paper-lookup**, ya citada en los informes del proyecto: [Kassis et al. (2026)](https://doi.org/10.48550/arXiv.2609.00065), versión vigente consultada durante esta revisión. Es procedencia de herramientas, no respaldo de la selección.

Esta consulta no cambió datos, cuotas ni filtros, y no descargó pesos ni inició embeddings. La elección de ocho o diez y sus recetas queda pendiente; el criterio de priorizar antecedentes académicos sí procede directamente del usuario.
