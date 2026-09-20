# Qué cambia al mirar áreas, especialidades y artículos

Resultados del cierre ampliado del 17-09-2026. **El dibujo general se parece bastante entre modelos, pero no existe una regla de que cada aumento de detalle empeore siempre el acuerdo.** Los controles de tamaño permiten precisar dónde sucede.

## Cobertura

Hay 252 Subfields en el corpus de 500.000 artículos. No sustituyen a las 26 áreas como unidad principal. Una especialidad solo tiene tres artículos: no permite CKA corregida. Con 50 vecinos, 243 especialidades y 499.750 artículos permiten una comparación informativa. Los demás IDs permanecen en las tablas con valor no disponible, no con cero o acuerdo perfecto.

| Control | Especialidades elegibles | Qué permite |
| --- | ---: | --- |
| 128 artículos por grupo | 232 | Comparación de grupos de tamaño igual |
| 256 artículos, principal | 217 | Incluye grupos que contienen 495.828 artículos del corpus |
| 512 artículos | 183 | Control de tamaño sobre estas mismas 183 en los tres tamaños |
| 128 en cada uno de los cinco períodos | 125 | Comparación temporal sin cambiar el conjunto de especialidades |

Todas las coberturas y exclusiones están en `data/robustness_v2/subfield_controls/coverage.csv` y `period_coverage.csv`. La elegibilidad del control no elimina artículos del corpus.

## Tres miradas diferentes

**Centros de grupos.** Con 256 artículos por centro, CKA media es aproximadamente 0,939 entre los centros de 26 áreas y 0,911 entre los de 217 especialidades. Los repartos aleatorios, conservando tamaños y fechas, dan aproximadamente 0,631 y 0,639. Un control con 26 centros de especialidades, una por área, da aproximadamente 0,903. Por tanto, el número de centros por sí solo no explica todo el patrón. Son comparaciones de relaciones entre centros, no una validación externa de temas ni porcentajes de ciencia correcta.

**Dentro de grupos.** Sobre las mismas 183 especialidades elegibles, CKA media queda en torno a 0,636 con 128, 256 o 512 artículos. En las 26 áreas queda en torno a 0,629–0,632. No aparece una caída general de CKA al pasar del interior de áreas al interior de especialidades. Los grupos y ponderaciones difieren: no interpretar esa pequeña diferencia como un efecto causal del nivel jerárquico.

**Vecinos de los mismos artículos.** Control más directo: 50 consultas fijas por cada una de 217 especialidades, diez selecciones de 256 candidatos y la misma composición de fechas. Una búsqueda usa candidatos de la especialidad; otra, del área que la contiene.

| Vecinos que pedimos | Coincidencia buscando en el área | Buscando en la especialidad | Especialidades donde baja |
| --- | ---: | ---: | ---: |
| 10 | 38,65% | 36,92% | 145/217 |
| 25, principal | 46,69% | 45,34% | 127/217 |
| 50 | 54,49% | 53,70% | 109/217 |

La bajada media existe y se mantiene en las diez selecciones, pero es pequeña y heterogénea. Con 50 vecinos la dirección se reparte casi por mitad. Estos porcentajes usan solo 256 candidatos: no compararlos directamente con el 30,3% de la búsqueda principal, cuyo universo es mayor.

## Estabilidad por artículo y especialidad

`data/robustness_v2/regions_native/paper_agreement.parquet` conserva los 500.000 IDs, las coincidencias para 10/25/50 vecinos y cuánto varían al omitir modelos o familias. `paired_neighbor_scales/paper_agreement.parquet` añade el rango entre diez selecciones para las 10.850 consultas controladas. No todas las 500.000 tienen este segundo control de selección. Los ejemplos conservan IDs; no se han escogido para ilustrar solo el resultado esperado.

La puntuación de un artículo depende también de la biblioteca donde buscamos sus vecinos. En la búsqueda controlada dentro de especialidades, el rango mediano entre diez selecciones es de 9,33 puntos porcentuales con k25. Por eso no usamos un único decimal para dar una etiqueta definitiva de «estable» a cada artículo.

Las regiones varían incluso dentro de la misma disciplina. Con 256 artículos, Algebra and Number Theory obtiene CKA media 0,491 y Modeling and Simulation 0,812, ambas dentro de Matemáticas. Classics obtiene 0,465; Ecological Modeling 0,815. Esas cifras miden acuerdo entre modelos, no la calidad científica de las áreas ni la exactitud de sus etiquetas.

En el control por artículo con 25 vecinos, Artes y Humanidades conserva alrededor del 40,3%, Medicina 45,3%, Física 47,5% y Ciencias Ambientales 48,9%. Son promedios de consultas equilibradas por especialidad, no estimaciones ponderadas de toda la producción de cada área. Las tablas incluyen todas las áreas, fechas, especialidades y marcas de calidad.

Las muestras pequeñas no siempre estabilizan las diferencias finas. Entre los 183 Subfields donde 512 aún es una parte del grupo, 2.628 de 8.235 comparaciones no superan la regla operativa de selección. En otros 68 grupos, la selección grande ya es el grupo entero: su amplitud nula no es una prueba de precisión poblacional; 213 de 3.060 comparaciones cambian demasiado frente a la selección reducida. Se conservan todas las alertas. Para conclusiones sobre diferencias pequeñas, usar las cifras completas, su sensibilidad y cobertura; no inventar un orden preciso de todos los grupos.

## Qué explica y qué no explica el caso de Medicina

Se compararon dos selecciones de 2.048 artículos por área con las mismas cuotas de fechas: mezcla observada de especialidades elegibles y reparto igual entre ellas. Diez repeticiones, mismas condiciones para todos los modelos. Medicina conserva 39 de sus 42 especialidades en este control; las excluidas no desaparecen del análisis original.

| Área | Forma, mezcla observada | Forma, mezcla equilibrada | Vecinos 25, observada | Vecinos 25, equilibrada |
| --- | ---: | ---: | ---: | ---: |
| Medicina | 0,546 | 0,543 | 29,05% | 29,21% |
| Energía | 0,772 | 0,772 | 33,24% | 33,24% |
| Matemáticas | 0,671 | 0,644 | 29,44% | 28,76% |
| Física | 0,663 | 0,674 | 33,00% | 34,13% |

Energía tiene un solo Subfield elegible en este control; sus dos condiciones son iguales por construcción. No es evidencia de que reequilibrar nunca influya en Energía. La comparación observada/equilibrada cambia pesos de especialidades, no iguala los temas reales de diferentes áreas.

En Medicina, retirar BioBERT y PubMedBERT aumenta CKA observada de 0,546 a 0,564 y vecinos de 29,05% a 29,53%. El cambio es parcial. Los dos biomédicos **entre sí** sí coinciden bastante: CKA 0,829 y vecinos 53,93%. No son simplemente dos modelos defectuosos.

Dentro de especialidades de Medicina, con 256 artículos y igual peso por especialidad, CKA media es 0,611; sube a 0,626 sin los biomédicos. Es mayor que el promedio del área mezclada, aunque esos diseños no aíslan una causa única. La diversidad de especialidades se asocia descriptivamente con menor acuerdo entre las 26 áreas, pero también cambian vocabulario, cobertura, textos y clasificación. **No queda demostrado que la diversidad sea la causa del caso de Medicina.** Tampoco Medicina es siempre peor que Matemáticas al mirar vecinos controlados.

Tablas completas: `data/robustness_v2/structural_review_v3/`. Programas, selecciones y huellas: carpetas originales de cada control y `ROBUSTNESS_PROTOCOL.md`. Las etiquetas de OpenAlex sirven para organizar la comparación; no son una evaluación temática independiente.
