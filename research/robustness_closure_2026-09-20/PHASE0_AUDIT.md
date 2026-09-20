# Auditoría antes de las nuevas comparaciones

## Procedencia

- Figura 1: `manuscript/scripts/build_figures.py`; centros en `sos_deep/centroid_scales.py` y `data/robustness_v2/centroid_scales/`; forma interna en `sos_deep/subfield_controls.py` y tabla `structure_matched_size_agreement.csv` de `reports/robustness_v2/final/tables/`.
- Vecinos originales: `sos_analysis/run_neighbors.py`, `neighbors.py`, `config/neighbors_v1.json`, `data/analysis_v1/neighbors/`.
- Entradas de 52.000: `sos_deep/input_analysis52.py`, `input_recipes52.py`, `config/input52_v1.json`, `data/robustness_v2/inputs/` y comparaciones derivadas.
- Forma: `sos_morphology/run.py`, `metrics.py`, `config/morphology_pilot_v1.json`, `data/morphology_pilot_v1/metrics.parquet` y `selections.npz`.
- Parejas de áreas: `sos_pair_summary/analyze.py`, `config/field_pairs_v1.json`, `data/field_pair_summary_v1/` y `reports/field_pair_summary_v1/`.
- Calidad: `sos_analysis/run_shape.py::strict_quality`; siete indicadores de `config/analysis_v1.json` y un representante (menor índice) por componente conectado de DOI/texto normalizado idéntico. No identifica todas las versiones casi idénticas ni certifica contenido.
- Texto actual: `manuscript/{main,supplement}.tex` y equivalentes en `manuscript_es/`. Copia anterior y huellas en esta carpeta. Catálogo de vectores: `research/embedding_final_audit_2026-09-17/catalog.json`; lectura e identidad en `sos_analysis/reader.py`.

## Lo comprobado

Cada artículo se normaliza a longitud uno. Para centros se calcula la media y se normaliza **también el centro** antes de formar productos coseno y aplicar CKA corregida. Así consta en la configuración congelada; conviene explicitar el segundo paso en el artículo. No es un cambio de receta.

La fórmula de CKA aplicada a matrices de similitud y la fórmula independiente con momentos de los vectores coinciden en la prueba numérica. Se reproducen los valores guardados de los centros y se comprueban las huellas de los análisis padre; detalles en `phase0_audit.json`. El lector de vectores verifica índices, IDs OpenAlex, huellas de texto, archivos y correspondencia entre modelos. Los vecinos usan coseno en doble precisión, redondeo a doce decimales, exclusión del propio artículo y desempate por índice global.

Los centros originales usan un orden por hash y sus primeros 256 artículos; **no** fuerzan períodos iguales. Los grupos aleatorios usan exactamente esos artículos, con permutaciones dentro de cada período: conservan el tamaño y el número de artículos de cada fecha en cada grupo. Ya hay veinte asignaciones aleatorias, no una.

Las veinte selecciones de «26 subáreas» eligen una subárea elegible por área. Sus centros proceden de los mismos 256 artículos originales: cambia la subárea, **no** los artículos dentro de ella. El 0,902 es la media de veinte selecciones y 45 parejas de modelos. Falta medir por separado la variación de artículos, que cubre el nuevo diseño.

El filtro de calidad conserva 448.886 filas. El mínimo por área/período baja a 1.375; no se puede prometer un análisis de 2.048 candidatos en todas las celdas. El panel de entradas conserva al menos 235 artículos limpios de los 400 por celda, suficiente para un control de 200 limpios por celda sin nueva inferencia.

La tabla vigente confirma 2.628 alertas entre 8.235 comparaciones de 183 subáreas con más de 512 artículos. El grupo distinto de 68 subáreas tiene 213 alertas entre 3.060 comparaciones y usa todo el grupo al tamaño mayor. No se mezclan esos denominadores.

No se ha encontrado un error científico en las implementaciones revisadas. Los errores de dos intentos del programa nuevo de auditoría eran de lectura del formato guardado (asignaciones expresadas como índices globales y función que devuelve dos objetos); se corrigieron antes de producir evidencia y sin tocar resultados anteriores.

## Aclaración adicional de la referencia restringida

La afirmación de «los mismos artículos» de la auditoría anterior corresponde a los grupos completos de 26 áreas y 217 subáreas, que fueron los verificados explícitamente. En la comparación antigua restringida a 26 subáreas, los centros aleatorios se tomaban de una reasignación de las **217** subáreas. Conservaban tamaño, fechas y correspondencia entre modelos, pero no exactamente el conjunto de artículos de las 26 subáreas observadas. `phase0_restricted_reference_addendum.json` conserva el recuento comprobado. El nuevo protocolo ya exige permutar solo los artículos de cada conjunto observado y su implementación lo cumple. Esta diferencia de procedencia se declarará; no se atribuye al nuevo control el valor de la referencia antigua. No se ha alterado una salida original.
