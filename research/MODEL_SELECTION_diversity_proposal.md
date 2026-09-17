> HISTORIAL: sustituido por el criterio posterior del usuario de priorizar uso en mapas científicos. No es la lista vigente. Véase ../MODEL_SELECTION.md.

# Qué modelos comparar: propuesta pendiente

**Actualización del 15-09-2026: el usuario quiere más de cuatro modelos. Propongo ocho; la lista sigue pendiente de elección.** Esto sustituye la recomendación inicial de cuatro, que el usuario no aceptó como tamaño. Su petición de más candidatos no aprueba nombres concretos, formatos ni el inicio de embeddings.

La idea es fotografiar los mismos objetos con cámaras distintas: necesitamos variedad entre las cámaras, manteniendo iguales los objetos. Ocho permiten 28 comparaciones por parejas; diez, 45. Esas parejas comparten modelos y artículos: no son 28 o 45 pruebas independientes. No hay un número que por sí solo haga publicable el trabajo.

## Propuesta ampliada: ocho

- **Científicos:** SPECTER2, SemCSE_cosine y SciNCL.
- **Generales:** all-mpnet-base-v2, Qwen3-Embedding-0.6B, e5-base-v2, BGE-M3 y EmbeddingGemma-300m.

Se recomienda añadir SciNCL para comparar herramientas científicas próximas; E5 como otra referencia general en inglés; BGE-M3 por su familia y entrenamiento multilingüe; EmbeddingGemma por otra familia compacta. Son motivos para estudiar diferencias, no predicciones de qué modelo ganará ni evidencia de independencia entre todos ellos. Tres científicos y cinco generales no justifican por sí solos conclusiones sobre esas categorías completas.

**Si se desean diez:** añadir GTE-ModernBERT-base y Jina Embeddings v5 text small. GTE aporta un codificador moderno para texto largo; Jina permite examinar una receta reciente orientada a tareas, emparentada con Qwen. Esta ampliación es opcional y requiere medir costes. No se propone escogerlos después de ver cuáles producen el resultado científico más llamativo.

## Candidatos adicionales comprobados

Todas las fuentes de esta tabla se consultaron el 15-09-2026. La descripción factual procede de la ficha o repositorio oficial; la prioridad es una recomendación para este proyecto.

| Candidato | Qué permitiría estudiar | Prioridad propuesta |
| --- | --- | --- |
| [SciNCL](https://huggingface.co/malteos/scincl) | Otro científico entrenado con relaciones de citas; comparación próxima a SPECTER2. Ya se midió su velocidad en este Mac. | Añadir al grupo de ocho. |
| [E5-base-v2](https://huggingface.co/intfloat/e5-base-v2) | Otra referencia general en inglés, basada en BERT y entrenada para semejanza de textos. | Añadir al grupo de ocho. |
| [BGE-M3](https://huggingface.co/BAAI/bge-m3) | Otra familia multilingüe, basada en XLM-R y entrenada con varias formas de buscar documentos. | Añadir al grupo de ocho. |
| [EmbeddingGemma-300m](https://huggingface.co/google/embeddinggemma-300m) | Familia Gemma de Google, compacta y diseñada para ejecución local. | Añadir al grupo de ocho, sujeto a acceso y prueba local. |
| [GTE-ModernBERT-base](https://huggingface.co/Alibaba-NLP/gte-modernbert-base) | Un codificador moderno en inglés que admite textos largos. | Candidato para nueve/diez o alternativa si otro falla técnicamente. |
| [Jina Embeddings v5 text small](https://huggingface.co/jinaai/jina-embeddings-v5-text-small) | Modelo de 2026 con ajustes para comparar textos o agruparlos. Comparte base Qwen y aprende de Qwen3-Embedding-4B: útil para estudiar recetas próximas, no otra familia completamente independiente. | Candidato para diez. |
| [Qwen3-Embedding-4B](https://huggingface.co/Qwen/Qwen3-Embedding-4B) | Comparar tamaños dentro de Qwen junto al 0.6B. Cambian también otros detalles; no aislaría únicamente el número de parámetros. | Opcional si se prioriza esta pregunta y su coste resulta viable. |
| [SPECTER original](https://github.com/allenai/SPECTER) | Comparar generaciones de una herramienta científica. | Control histórico opcional; menor prioridad que ampliar familias. |

### Notas técnicas para preparar una prueba, no configuraciones aprobadas

- **E5:** ID `intfloat/e5-base-v2`, 768 dimensiones, máximo 512 tokens, media de representaciones y normalización, licencia MIT. La ficha recomienda el prefijo `query: ` para semejanza simétrica y agrupación. También documenta valores coseno concentrados entre 0,7 y 1: comparar sus valores absolutos con otros modelos sin control podría confundir entrenamiento con estructura científica.
- **BGE-M3:** ID `BAAI/bge-m3`, 1.024 dimensiones, hasta 8.192 tokens, licencia MIT. Para el espacio común, considerar su salida densa: un vector por artículo. Las salidas de palabras y múltiples vectores responden a otra comparación. No requiere las instrucciones de consulta de BGE anterior.
- **EmbeddingGemma:** ID `google/embeddinggemma-300m`, alrededor de 300 millones de parámetros, 768 dimensiones, 2.048 tokens. Licencia Gemma; Hugging Face exige aceptar sus condiciones para descargar. Su ficha indica `float32` o `bfloat16`, no `float16` para activaciones. Fijar los prefijos y la receta de comparación antes de ejecutar. Su diseño para dispositivos locales no sustituye una medición en este Mac.
- **GTE-ModernBERT:** ID `Alibaba-NLP/gte-modernbert-base`, 149 millones de parámetros, 768 dimensiones, 8.192 tokens, licencia Apache-2.0. La receta oficial extrae el primer token; requiere Transformers 4.48 o posterior. Flash Attention es opcional; no se ha comprobado aquí el funcionamiento con MPS.
- **Jina v5 small:** ID `jinaai/jina-embeddings-v5-text-small`, 677 millones de parámetros, 1.024 dimensiones, hasta 32.768 tokens, licencia CC BY-NC 4.0. Hay variantes de comparación de textos y agrupación: cerrar una por objetivo antes de analizar resultados, sin contar adaptadores como familias independientes. La ficha exige versiones recientes de Transformers/Torch y usa código propio. No se ha instalado ni ejecutado.
- **Qwen 4B:** ID `Qwen/Qwen3-Embedding-4B`, 4.000 millones de parámetros, hasta 2.560 dimensiones y 32K tokens, licencia Apache-2.0. Mayor almacenamiento de pesos que 0.6B; la velocidad no escala necesariamente de forma lineal con ese número. No estimar horas de 500.000 sin una prueba real ni cambiar precisión silenciosamente para hacerlo caber.
- **SPECTER original:** el repositorio advierte que los vectores de su API y los generados por su código pueden proceder de versiones diferentes y no se deben mezclar. Si se eligiera, fijar un único modelo y receta para todos los artículos.

Las dimensiones y longitudes máximas son capacidades de los modelos, no reglas ya elegidas para nuestro experimento. Un modelo multilingüe tampoco convierte nuestro corpus inglés en un estudio multilingüe. Estos candidatos no agotan el catálogo de modelos existente.

## Cuatro candidatos iniciales, incluidos en la propuesta ampliada

| Modelo | Papel en el estudio | Motivo y límite |
| --- | --- | --- |
| **SPECTER2** | Científico; referencia del TFM | Representación científica informada por citas. Identificar base y adaptador: la documentación recomienda proximidad para comparar artículos. Los vectores heredados no tienen todavía procedencia suficiente para aprobar su reutilización. |
| **SemCSE_cosine** | Científico; entrenamiento distinto | Aprende semejanza semántica mediante resúmenes generados durante su entrenamiento. Aporta una diferencia útil frente a modelos basados en citas. Variante publicada para similitud coseno; su ejecución y velocidad en el Mac están por probar. |
| **all-mpnet-base-v2** | Uso general; referencia ya probada localmente | Modelo de propósito amplio, con velocidad medida en este Mac. Su entrenamiento también contiene datos científicos y pares relacionados con citas: “general” no significa “nunca ha visto ciencia”. |
| **Qwen3-Embedding-0.6B** | Uso general; arquitectura diferente | Alternativa de 600 millones de parámetros y contexto más largo. Tamaño elegido como candidato por viabilidad, sin afirmar que sea el mejor ni el más reciente. Falta medir tiempo y memoria reales aquí. |

Fuentes oficiales: [SPECTER2, código y recetas](https://github.com/allenai/SPECTER2), [SemCSE_cosine](https://huggingface.co/CLAUSE-Bielefeld/SemCSE_cosine), [MPNet](https://huggingface.co/sentence-transformers/all-mpnet-base-v2), [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B).

**SciNCL pasa de quinto opcional a candidato del grupo de ocho.** SPECTER2 y SciNCL comparten parte de los datos de entrenamiento según el repositorio de SPECTER2; incluirlo amplía el control dentro de esa familia. SemCSE sigue aportando una diferencia de entrenamiento útil. Ninguno queda aceptado automáticamente por esta propuesta.

Dos representantes por grupo evitan que todo dependa de un único ejemplo, pero no permiten afirmar que todos los modelos científicos o generales se comportan igual. Cambian varias cosas a la vez: arquitectura, datos, objetivo de entrenamiento y tamaño. El estudio examinaría la dependencia respecto a modelos concretos; no aislaría por sí solo la causa de cada diferencia.

## ¿Por qué incluir modelos generales?

Solo científicos respondería una pregunta más estrecha: cuánto cambia la representación entre herramientas especializadas. Incluir generales permite comprobar si las conclusiones también resisten otra clase de herramientas que alguien podría usar para representar estos artículos. No presuponemos que el especializado sea mejor, ni que una puntuación alta en recuperación de documentos demuestre una forma “verdadera” de la ciencia.

Con la preferencia del usuario por más de cuatro, recomiendo el grupo mixto de ocho por variedad y una carga potencialmente manejable que debe medirse. Si prefiere solo especializados, habrá que concretar otra lista; pedir más modelos no cierra automáticamente esa elección.

## Qué sabemos del coste

Las [pruebas locales](feasibility_2026-09-14/RESULTS.md) midieron aproximadamente 50,5 artículos/s en SciNCL y 64,6 en MPNet. Para modelos comparables se había reservado un margen de 3–6 horas por 500.000 artículos. Es una previsión con límites, no una medición de cuatro ejecuciones completas.

**De los ocho propuestos, solo SciNCL y MPNet tienen medidas locales previas.** No se ha medido aquí SemCSE, Qwen3, E5, BGE-M3 ni EmbeddingGemma. Tampoco todos los formatos de entrada y controles futuros. Tras elegir los candidatos, conviene una prueba pequeña de compatibilidad, velocidad, memoria y longitud del texto antes de lanzar el conjunto. Ocho modelos no significa ocho multiplicado por un tiempo ya garantizado. No se han descargado pesos nuevos en esta revisión.

## Qué aportaría frente a trabajos existentes

La revisión es dirigida, no exhaustiva. No se ha demostrado prioridad ni se promete aceptación en QSS.

| Trabajo comprobado | Qué hace y cómo limita nuestra afirmación de novedad |
| --- | --- |
| **Imel y Hafen (2025), preprint**, [Density, asymmetry and citation dynamics in scientific literature](https://arxiv.org/html/2506.23366v1) | Examina unas 53.000 publicaciones de nueve disciplinas con cinco representaciones y relaciona geometría y citas. Su selección se expande por semejanza SciBERT y después exige estabilidad de vecinos. Ya existe comparación entre varias representaciones; “usar varios modelos” no basta como novedad. Métodos leídos. |
| **Brinner y Zarrieß (EMNLP 2025)**, [SemCSE](https://aclanthology.org/2025.emnlp-main.1662/) | Propone embeddings científicos con otro entrenamiento y compara modelos científicos y generales en tareas de evaluación. Apoya incluir variedad, pero es un estudio de desarrollo/evaluación de modelos, no una demostración de nuestra pregunta. Artículo completo leído. No atribuir todos los resultados del modelo principal a su variante coseno. |
| **Brinner y Zarrieß (ACL 2026)**, [SemCSE-Multi](https://aclanthology.org/2026.acl-long.1884/) | Presenta representaciones de distintos aspectos para mapas científicos interpretables. Solo se revisaron resumen y metadatos. La búsqueda ampliada confirmó publicación en julio de 2026, DOI 10.18653/v1/2026.acl-long.1884; sustituye la identificación anterior únicamente como preprint. No se ha leído todavía el artículo publicado completo. |

**Propuesta de aportación, todavía por concretar:** identificar qué conclusiones sobre las relaciones entre áreas y sus cambios en el tiempo sobreviven al cambiar de modelo, sobre una misma selección de artículos no guiada por ninguno de los modelos. Separar diferencias debidas al modelo, a qué artículos entran y a cuánto texto lee cada modelo. Los 26 Fields y cinco períodos dan cobertura para esa pregunta; aumentar el número de modelos sin una conclusión clara no la hace más original.

Antes de reclamar novedad en un manuscrito habría que ampliar la revisión específica de esa pregunta y cerrar una aportación principal medible. Las medidas globales, los vecinos y las conclusiones temporales siguen siendo propuestas del brief, no resultados ni protocolo final cerrado.

## Comparación justa: decisiones siguientes, aún abiertas

1. **Mismos IDs y textos de origen**, usando el archivo común ya preparado. No seleccionar artículos por semejanza bajo un modelo. Mantener separados los usos de la base general y el refuerzo.
2. **Versiones y recetas exactas.** SPECTER2 requiere distinguir base y adaptador; SemCSE principal usa distancia euclídea y la variante propuesta usa coseno. MPNet, SemCSE, SPECTER2 y Qwen no extraen el vector de la misma manera. Seguir y fijar cada receta oficial; no darles por defecto la de otro modelo.
3. **Cuánto texto ve cada uno.** MPNet trunca por defecto a 384 piezas de texto; SPECTER2 usa habitualmente 512; Qwen admite más. Un mismo número de piezas no garantiza el mismo contenido entre vocabularios. Acordar una comparación con contenido común y, si interesa, otra con la entrada propia de cada modelo. Registrar texto efectivamente leído y truncamientos. No se ha elegido ahora esa regla.
4. **Medidas compatibles.** Dimensiones distintas no impiden comparar relaciones entre artículos, pero no procede restar directamente sus vectores. Cerrar medidas globales/locales, normalización y tratamiento de distancias antes de mirar resultados.
5. **Comprobación del tamaño y la calidad.** Especial atención a Matemáticas/Humanidades antiguas y grupos pequeños. Acordar qué variación toleramos y qué controles haremos sin borrar automáticamente los textos señalados. Ver [CORPUS_BALANCE.md](../CORPUS_BALANCE.md).

No descargar más artículos ni iniciar cálculos masivos como efecto secundario de esta propuesta. Los 22.118 vectores antiguos con texto coincidente siguen siendo candidatos: coincidencia y validez numérica no resuelven su versión.

## Preguntas presentadas al usuario

1. ¿Prefiere mezclar modelos científicos y generales, como se recomienda, o limitar el estudio a científicos?
2. Tras pedir más de cuatro, ¿quiere el grupo ampliado de ocho o prefiere diez añadiendo GTE-ModernBERT y Jina v5? La cantidad exacta y los nombres siguen pendientes.

Después de su respuesta: concretar candidatos aceptados, versiones y formato; determinar el alcance de la prueba pequeña antes del cálculo completo. No registrar las recomendaciones como decisiones aceptadas.

## Trazabilidad de la búsqueda

Consultas del 15-09-2026, entre otras: `"science mapping" "embedding models" "robustness"`; `scientific document embedding space geometry robustness comparison general domain models science map SPECTER2 SciNCL 2025 2026`; `"Density, asymmetry and citation dynamics" publication`; `"SemCSE" huggingface model`. Se leyeron fuentes primarias; los resultados de buscador no leídos no sustentan conclusiones.

Ampliación tras la petición de más modelos: búsquedas dirigidas de `e5-base-v2`, `gte-modernbert-base`, `embeddinggemma-300m`, `jina-embeddings-v5-text-small`, `Qwen3-Embedding-4B` y modelos científicos recientes; lectura de las ocho fichas/repositorios enlazados en la tabla. También se consultó la [ficha oficial de Google](https://ai.google.dev/gemma/docs/embeddinggemma/model_card). No se compararon experimentalmente ni se hizo una búsqueda exhaustiva. Los tiempos locales siguen procediendo únicamente del informe de viabilidad existente.

Metadatos editoriales de SemCSE comprobados en Crossref, DOI **10.18653/v1/2025.emnlp-main.1662**. La búsqueda Crossref por título de Imel/Hafen devolvió tres títulos diferentes; no confirmó publicación editorial y tampoco demuestra que no exista. Respuestas reducidas y fechas en [research/model_review_2026-09-15/](model_review_2026-09-15/).

Guías de apoyo: paper-lookup y citation-management. Su procedencia metodológica es [Kassis et al. (2026), Scientific Agent Skills](https://doi.org/10.48550/arXiv.2609.00065), metadatos v2 comprobados en arXiv. Es una referencia de herramientas, no evidencia que justifique el tamaño o la originalidad del estudio.
