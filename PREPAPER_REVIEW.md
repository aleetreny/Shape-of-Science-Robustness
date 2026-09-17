# Revisión previa al manuscrito

17-09-2026. **La revisión técnica y el atlas de casos están terminados. El trabajo permite empezar una redacción con límites claros; todavía no está preparado para enviarse a una revista.** No se ha escrito el manuscrito ni publicado datos. El cierre anterior se conserva en `research/prepaper_2026-09-17/baseline_documents/`.

**Actualización posterior de disponibilidad:** el usuario ha autorizado commit y push de código, documentación, tablas y figuras. Las menciones a ausencia de publicación de esta revisión se referían al momento de su cierre. El corpus y los vectores siguen locales; el depósito permanente permanece pendiente. Versión documental anterior conservada en `research/github_release_2026-09-17/pre_release_documents/`.

La conclusión se mantiene: los modelos comparten parte de la organización científica, pero las relaciones locales dependen del modelo, del texto y de los candidatos disponibles. La revisión añade ejemplos comprobables y detecta errores de la fuente que debemos reconocer.

## Qué se revisó

| Etapa | Comprobación y evidencia | Alcance y límite |
| --- | --- | --- |
| Pregunta y antecedentes | [45 referencias verificadas](references/README.md), versiones publicadas y comparación con trabajos cercanos. | Revisión dirigida; no certifica haber encontrado toda la literatura ni prioridad absoluta. |
| Población y reparto | Protocolo de 400k base + 100k complemento; filtros, semillas, bloques aleatorios y reposición revisados en `sos_download/` y `sos_prepare/`. | Inglés, años 2000–2024, abstract disponible y reglas de OpenAlex. No representa toda la producción mundial. 500k es un presupuesto comprobado, no un óptimo universal. |
| Fuente e identidades | Los 500.000 IDs/huellas de texto coinciden entre corpus e índice; sus Fields/Subfields coinciden con el JSON original guardado. Los 30 registros de las ilustraciones coinciden también con las páginas crudas, incluidos los resúmenes. | Una copia fiel puede conservar errores de OpenAlex. No es validación semántica de 500.000 registros. |
| Limpieza | Reglas de idioma, abstract, duplicados, avisos y selección revisadas; nuevo diagnóstico de títulos genéricos en todo el corpus. | Hay avisos no detectados y etiquetas erróneas. El control de calidad anterior combina varios filtros. Ver hallazgo abajo. |
| Embeddings | Revisión de entrada, máscara, media/CLS/SEP, límites, adaptador proximity y versiones congeladas. Integridad previa completa, más lectura validada de las 500k filas de SPECTER, BERT y MiniLM en esta revisión. | Diez modelos elegidos por antecedentes; no son todos los encoders actuales ni diez observaciones independientes. Recorte y solapamiento de entrenamiento siguen siendo límites. |
| Forma | Seis CKA reales de dos Subfields y tres modelos reconstruidas con matrices entre artículos, por una vía distinta al cálculo publicado; coinciden a menos de 1e−10. | CKA corregida compara organización, no porcentaje de ciencia correcta. Procrustes/RSA son controles, no votos independientes. |
| Vecinos | 300 consultas reales reconstruidas mediante ordenación completa de todos sus candidatos; los primeros 50 coinciden. Atlas: otras 34.200 comprobaciones de intersecciones y relaciones. | Los vecinos dependen de k y del conjunto de búsqueda. No equivalen a citas ni a relevancia juzgada por expertos. |
| Tamaños y escalas | Sellos y fuentes de los 15 componentes vigentes verificados de nuevo. Se conservan los mismos grupos al comparar tamaños y los mismos artículos/fechas al comparar ámbitos. | En la comparación emparejada de ámbitos, 50/256 candidatos son consultas del mismo Subfield en ambos ámbitos. La búsqueda amplia está condicionada por ese diseño; no es una muestra completamente libre del Field. |
| Entrada, receta y estabilidad | 52k, tres entradas, piloto anidado, alternativas de receta y 100 selecciones. Conservadas las cinco alertas de entrada, las 50 originales y las de especialidades. | No se cruzaron todos los controles entre sí. Las selecciones son variación de un corpus fijo, no intervalos poblacionales. La pequeña diferencia modelo/título cambia de orden con la receta. |
| Tiempo y Medicina | Separación de consultas/candidatos y sensibilidad de composición revisadas. | El cambio temporal no es causal; las etiquetas y cobertura pueden cambiar. Menor acuerdo de Medicina no demuestra peor calidad de los modelos biomédicos. |
| Familias | Diseño, rango de las regresiones, permutación de etiquetas de modelos y omisiones revisados. | Objetivo, corpus, arquitectura y linaje se solapan. El ajuste de 45 pares no identifica efectos causales de diez modelos. |
| Presentación | README, índice, biblioteca central, atlas con IDs, dos figuras nuevas PDF/SVG/PNG de 300 dpi y guía de reproducción. | Las figuras anteriores siguen intactas; su adaptación final de tamaño y pies corresponde al manuscrito. Datos locales aún sin archivo público permanente. |

Evidencia nueva: [auditoría numérica](research/prepaper_2026-09-17/numerical_audit.json), `data/prepaper_v1/source_quality/summary.json`, `data/prepaper_v1/case_atlas/audit.json`. Las pruebas pasan en sus entornos: **32 de análisis y 20 de embeddings/preparación de entradas**. No se ejecutó inferencia nueva.

[Auditoría de cierre](research/prepaper_2026-09-17/closure_audit.json): copias históricas y entrega anterior intactas, fuentes científicas congeladas comprobadas, atlas y figuras actuales verificados, enlaces locales válidos y revisión de posibles claves en archivos versionables sin hallazgos. Esta última es una búsqueda por patrones, no una garantía universal de detección.

## El hallazgo que impide decir «todo está perfecto»

La selección automática de ejemplos encontró:

- `W7045581866`: descripción de un libro sobre brujería, clasificada como física nuclear. La fuente le daba un score de tema de 0,9158: un score alto tampoco garantiza una etiqueta correcta.
- `W2011180849`: resumen sobre invasión bacteriana clasificado en política internacional.
- `W4234898602`: `Announcement`, con texto de reseña de un atlas clínico, marcado por la fuente como artículo y no paratexto.

Se comprobaron contra las respuestas originales del 15 de septiembre. No son cruces de filas de nuestro código. Se mantienen en el atlas con notas, sin cambiar a mano el corpus ni sustituir ejemplos después de conocerlos.

Un diagnóstico nuevo, conservador, encontró **82 títulos genéricos de 500.000 (0,0164%)**, 67 fuera de las marcas estrictas previas. Cinco están entre las 10.850 consultas controladas. Excluir esas cinco consultas deja el acuerdo medio en **45,349% frente a 45,344%**: un cambio de **0,0048 puntos porcentuales**. Los candidatos se mantienen; es una comprobación parcial. **No estima cuántas etiquetas temáticas están equivocadas ni descarta su influencia.**

Decisión de esta revisión: describir resultados condicionados a la clasificación OpenAlex y conservar estos casos como diagnóstico. No afirmar que las especialidades observadas son grupos temáticos validados. Si el manuscrito necesita afirmar precisión temática o explicar causas disciplinares, antes necesitará una validación externa específica. No se ha inventado esa validación.

## Qué aporta el atlas

[CASE_ATLAS.md](CASE_ATLAS.md) resume 217 especialidades, 10.850 artículos con candidatos repetidos, **531.650 relaciones dirigidas** entre artículos siempre elegibles y **23.436 parejas** de centros de especialidades. Incluye tablas completas locales y una entrega legible con IDs.

La selección de ejemplos se fijó antes de leer sus títulos, pero después de los resultados generales: es exploratoria. «Alto» y «bajo» son posiciones relativas entre estos modelos y condiciones. No son sellos de verdad científica.

## Preparado para redactar; pendiente antes de enviar

La [comparación con antecedentes](references/RELATED_WORK.md) delimita la aportación. El [esquema](PAPER_OUTLINE.md) prioriza una pregunta, cuatro figuras y ejemplos concretos. [QSS_CHECK.md](docs/QSS_CHECK.md) distingue requisitos localizados de las tareas pendientes.

Antes de enviar faltan el manuscrito, revisión humana de afirmaciones y casos, datos/código esenciales archivados con identificador persistente, y declaraciones reales de autoría, financiación, intereses y uso de herramientas. Las licencias y disponibilidad se describirán según lo efectivamente compartido. El plan de archivo está preparado en [DATA_RELEASE.md](docs/DATA_RELEASE.md); no se ha hecho un depósito permanente del material científico.
