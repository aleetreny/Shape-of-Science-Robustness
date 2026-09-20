# Diez modelos elegidos

> **Estado, 17-09-2026: los diez modelos terminaron y fueron comprobados.** Ver `EMBEDDINGS_AUDIT.md`, `DATA_CATALOG.md` y `NEXT_STEPS.md`. Los comandos de cálculo se conservan como documentación; no hace falta relanzarlos.

**15-09-2026. Criterio pedido por el usuario:** más de cuatro modelos y prioridad a los que se utilizan para mapear la ciencia. La selección debe apoyarse en artículos, no en popularidad general o posiciones en pruebas de búsqueda de documentos.

**El usuario ha elegido los diez: los ocho de la tabla, más BioBERT y SimCSE.** Las revisiones exactas están fijadas en `config/embeddings_v1.json`; el programa y las pruebas se explican en `EMBEDDINGS.md`. La revisión de diez trabajos y sus límites está en [ACADEMIC_MODEL_USAGE.md](ACADEMIC_MODEL_USAGE.md). La propuesta anterior basada en diversificar modelos recientes queda [archivada](research/MODEL_SELECTION_diversity_proposal.md); nunca fue aprobada.

## Ocho del grupo inicial, ahora aceptados

| Modelo | Por qué incluirlo | Implementación aceptada; revisión fijada en configuración |
| --- | --- | --- |
| SPECTER original | Repetido en cinco de los diez antecedentes; referencia científica histórica. | `allenai/specter`, con una única receta y procedencia para todo el corpus. |
| SPECTER2 | Sucesor científico, referencia del TFM y comparación reciente de mapas. Aparece en uno de los diez. | `allenai/specter2_base` más adaptador de proximidad `allenai/specter2`, ambas revisiones fijadas. |
| SciNCL | Comparador científico en dos antecedentes; velocidad ya medida localmente. | `malteos/scincl`. |
| SciBERT | Repetido en cinco; permite examinar una representación científica anterior al ajuste de SPECTER/SciNCL. | `allenai/scibert_scivocab_uncased`; se guardan media, CLS y SEP. |
| BERT | Referencia general clásica, presente en tres; variante exacta confirmada en dos. | `google-bert/bert-base-uncased` ; se guardan media, CLS y SEP. |
| MPNet | Familia presente en tres: dos usan `all`, uno `paraphrase`. Uso en QSS y en comparación de mapas biomédicos. | `sentence-transformers/all-mpnet-base-v2`, que ya tiene prueba local. |
| MiniLM | Misma variante usada en tres antecedentes de temas y evolución científica. | `sentence-transformers/all-MiniLM-L6-v2`. |
| PubMedBERT | Modelo empleado para el mapa completo de biomedicina de González-Márquez et al.; un antecedente de la revisión. | Variante `abstract-fulltext`, hoy denominada `microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext`. Nombre actual del mismo modelo; revisión fijada. |

Los números cuentan uso en aplicaciones **o en sus comparaciones previas**, por modelo/familia, dentro de una revisión dirigida. No son porcentajes de la comunidad. SPECTER2 y PubMedBERT se añaden por su función concreta y sus antecedentes, aunque no sean los más repetidos de esta revisión.

La mezcla de generales y científicos está respaldada por los trabajos leídos. Es útil para comprobar si las conclusiones sobre ciencia se mantienen con herramientas de distinto propósito. Los modelos científicos comparten en parte antecesores/datos; no son diez familias independientes. “General” tampoco significa ausencia de textos científicos en su entrenamiento.

## Otros dos aceptados para llegar a diez

**BioBERT y SimCSE** también están aceptados: ambos se compararon en el estudio del mapa biomédico. BioBERT amplía el contraste dentro de biomedicina; SimCSE aporta una forma distinta de ajustar una representación general. Su presencia aquí procede de un solo trabajo, no de evidencia de uso extendido.

Otra opción es la variante `sentence-transformers/paraphrase-mpnet-base-v2`, usada por Constantino et al. en QSS. Añadirla reproduce un antecedente exacto y examina cambios dentro de MPNet; no añade una familia nueva. La variante paraphrase no se incorpora: el usuario eligió BioBERT y SimCSE para completar diez.

**Control propuesto aparte: TF-IDF**, que representa los artículos mediante sus palabras. Ya fue comparado con los modelos en el mapa biomédico. Ayudaría a interpretar qué se conserva respecto a una referencia sencilla. No se cuenta como uno de los diez modelos neuronales y no está aprobado todavía.

## Qué pasa con los candidatos anteriores

SemCSE, Qwen3, BGE-M3, EmbeddingGemma, GTE-ModernBERT y Jina siguen siendo candidatos posibles, con sus fichas en el documento archivado. La revisión actual no justifica presentarlos como habituales en mapas de ciencia. Esto no significa que no se usen o que sean peores. El criterio nuevo del usuario da prioridad a los antecedentes comprobados.

SemCSE-Multi se confirmó como artículo de ACL 2026, [DOI 10.18653/v1/2026.acl-long.1884](https://aclanthology.org/2026.acl-long.1884/), corrigiendo la descripción anterior solo como preprint. Se revisaron resumen y metadatos, no el cuerpo completo; no se usa para inflar las frecuencias de adopción de SemCSE.

## Preparación acordada

- Diez modelos sobre los mismos 500.000 artículos, con título y abstract y el formato habitual de cada modelo. El usuario acepta añadir una comprobación con fragmentos idénticos.
- Revisiones, separadores, límites de lectura y salidas: `config/embeddings_v1.json`. Recetas y justificación: `EMBEDDINGS.md`.
- SPECTER2 incluye el adaptador de proximidad. SimCSE no supervisado usa CLS antes de su capa de ajuste, según los autores.
- Los cuatro modelos de palabras (BERT, SciBERT, PubMedBERT y BioBERT) conservan media, CLS y SEP sin volver a pasar el texto por el modelo. La receta principal de análisis aún debe acordarse antes de comparar resultados. Son diez modelos, no dieciocho modelos independientes.
- Se guardan valores originales en float32. La normalización puede hacerse después; no se pierde la escala original. MPNet/MiniLM se pueden normalizar para reproducir su salida habitual.
- No se mezclan los 22.118 vectores antiguos de procedencia incompleta. Se recalcularán estos artículos con la versión identificada.
- La selección de diez modelos no fija las medidas finales ni garantiza novedad o aceptación. Las 45 parejas comparten modelos/artículos y no son 45 pruebas independientes.

## Ejecución

**El usuario pide lanzar él mismo el cálculo completo mediante un comando.** El asistente prepara pesos, programa y pruebas pequeñas; no inicia los cinco millones de representaciones principales.

Fuentes: [SPECTER](https://github.com/allenai/SPECTER), [SPECTER2](https://github.com/allenai/SPECTER2), [SciNCL](https://huggingface.co/malteos/scincl), [SciBERT](https://github.com/allenai/scibert), [MPNet](https://huggingface.co/sentence-transformers/all-mpnet-base-v2), [MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), [PubMedBERT/BiomedBERT](https://huggingface.co/microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext), [BioBERT](https://github.com/dmis-lab/biobert), [SimCSE](https://github.com/princeton-nlp/SimCSE). El uso académico, distinto de la ficha del modelo, está en `ACADEMIC_MODEL_USAGE.md`.
