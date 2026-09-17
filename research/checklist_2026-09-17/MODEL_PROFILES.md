# De dónde vienen las familias comparadas

Fuentes primarias consultadas el 17-09-2026. Las revisiones exactas utilizadas siguen en `config/embeddings_v1.json`; no se cambia ningún modelo. Los grupos numéricos se fijaron en `config/checklist_v1.json` antes de su regresión.

| Modelo | Objetivo final y origen que importa | Fuente |
| --- | --- | --- |
| SPECTER | Representación científica con señales de citas; entrada título y resumen. | [Modelo oficial](https://huggingface.co/allenai/specter) |
| SPECTER2 | Base procedente de SciBERT, ajuste con citas y adaptador de proximidad con tareas de SciRepEval. | [Modelo oficial](https://huggingface.co/allenai/specter2) |
| SciNCL | Inicializa desde SciBERT; crea ejemplos de contraste a partir del vecindario del grafo de citas S2ORC. | [Modelo oficial](https://huggingface.co/malteos/scincl) |
| SciBERT | Modelo de palabras entrenado sobre textos científicos; no es por sí solo un modelo ajustado para proximidad documental. | [Artículo](https://aclanthology.org/D19-1371/), [repositorio](https://github.com/allenai/scibert) |
| BERT | Modelo de palabras de propósito general; la revisión elegida es base uncased. | [Artículo original](https://aclanthology.org/N19-1423/), configuración local fijada |
| MPNet | Ajuste para frases/fragmentos mediante contraste sobre una mezcla de más de mil millones de parejas. Incluye datos científicos S2ORC y ejemplos de SPECTER. | [Modelo oficial](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) |
| MiniLM | Ajuste de frases de la misma iniciativa de parejas masivas, con arquitectura de menor tamaño; tampoco está libre de textos científicos. | [Modelo oficial](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| PubMedBERT/BiomedBERT | La versión abstract-fulltext se entrena desde cero con resúmenes PubMed y textos PMC. | [Modelo oficial](https://huggingface.co/microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext) |
| BioBERT | v1.1 parte de BERT-base-cased y añade entrenamiento PubMed. No tiene el mismo origen ni vocabulario que PubMedBERT. «PubMed 1M» en la versión se refiere a su configuración de entrenamiento, no a que nuestro corpus tenga un millón de artículos. | [Repositorio oficial, versiones](https://github.com/dmis-lab/biobert) |
| SimCSE | La versión no supervisada usa frases de Wikipedia con dos pasadas alteradas por dropout; parte de BERT. No es el mismo ajuste de MPNet/MiniLM. | [Ficha oficial](https://huggingface.co/princeton-nlp/unsup-simcse-bert-base-uncased), [artículo](https://aclanthology.org/2021.emnlp-main.552/) |

## Cómo se traducen a variables

- **Objetivo:** citas/documentos (3), palabras en contexto (4), contraste de frases (3). Son grupos amplios; SPECTER2 incluye tareas adicionales y SimCSE difiere de los otros dos.

La columna llamada `same_objective` significa aquí pertenecer a ese grupo amplio de entrenamiento final. No significa tener idéntica función matemática de pérdida: los modelos con citas también emplean contrastes. Los grupos combinan señales/tareas de entrenamiento y unidad textual; no son factores causales puros. No cambiar la asignación después de observar parecidos.
- **Dominio amplio:** especialización científica (4), biomédica (2), sin especialización exclusiva de dominio (4). No mide el solapamiento real de artículos de entrenamiento. «Sin especialización exclusiva» puede incluir ciencia.
- **Receta principal:** media o primera posición, tal como estaba fijado. Se incluye porque puede confundirse con el objetivo del modelo. Se repite la descripción con recetas alternativas de los cuatro BERT.

Las 45 parejas comparten modelos. La regresión es descriptiva, y se acompaña de permutaciones simultáneas de filas/columnas y de quitar un modelo cada vez; no usa errores estándar que finjan 45 observaciones independientes. El contraste de dominios tiene solo una pareja exclusivamente biomédica: no permite atribuir causalmente el patrón al corpus o a la arquitectura. Explicaremos asociaciones y excepciones, no un mecanismo demostrado.
