# Dónde está cada cosa

**Entrega pública preparada, 20-09-2026:** [paquete y comprobaciones](PUBLIC_RELEASE.md), [diccionario de archivos](reproducibility/DATA_DICTIONARY.md). Los 19 ZIP numéricos están verificados en `output/zenodo/`; su borrador aún no tiene archivos públicos. El catálogo histórico siguiente conserva las rutas originales.

**Cierre vigente, 20-09-2026:** controles finales terminados y congelados; [informe para el autor](ROBUSTNESS_CLOSURE_REPORT.md) y [cambios del manuscrito](ROBUSTNESS_MANUSCRIPT_CHANGELOG.md). El tono claro está aceptado. La revisión personal del contenido sigue pendiente.

El cierre anterior de parejas se conserva como historial. Para la cobertura completa de centrado y alternativas, usar las rutas nuevas al final.

**Último cierre, 18-09-2026:** [resumen de parejas](FIELD_PAIR_RESULTS.md), [métodos](METHODS_FIELD_PAIRS.md), `reports/field_pair_summary_v1/` (doce tablas y dos figuras) y `data/field_pair_summary_v1/` (manifiesto, contrastes guardados y auditorías). Son derivados de medidas existentes; no nuevos embeddings. Los cierres previos permanecen conservados.

**Revisión previa al manuscrito, 17-09-2026:** [PREPAPER_REVIEW.md](PREPAPER_REVIEW.md), [atlas de casos](CASE_ATLAS.md), [biblioteca verificada](references/README.md) y `reports/prepaper_v1/` son la nueva entrada de revisión. Los cálculos científicos anteriores permanecen en sus rutas. [Índice de documentos](docs/INDEX.md) · [Cómo reproducir](docs/REPRODUCING.md) · [Disponibilidad todavía local](docs/DATA_RELEASE.md).

**Material vigente, 17-09-2026:** corpus original de 500.000, entradas ampliadas a 52.000 y resultados de especialidades en `data/robustness_v2/`. Consultar el cierre en [NEXT_STEPS.md](NEXT_STEPS.md), la interpretación en [ROBUSTNESS_RESULTS.md](ROBUSTNESS_RESULTS.md) y las rutas nuevas al final de este catálogo. Se conservan todas las rutas originales; no se mueven ni duplican archivos grandes para ordenarlos.

**Historial conservado:** diez modelos y comparación original sobre 500.000; después, tres entradas sobre 26.000 y comparaciones de tiempo, disciplinas y familias. [CHECKLIST_RESULTS.md](CHECKLIST_RESULTS.md) describe ese piloto, ampliado posteriormente a 52.000; sus cifras y sus 31 alertas no deben confundirse con la ampliación.

| Material | Ruta desde este repositorio | Uso |
| --- | --- | --- |
| Descarga original | `data/corpus_500k/` | Evidencia de origen; conservar. |
| Corpus limpio completo | `data/corpus_clean_v1/corpus.parquet` | Textos, clasificación, procedencia y marcas de calidad. |
| Entrada congelada de los modelos | `data/corpus_clean_v1/embedding_input.parquet` | Mismos 500.000 IDs y textos, con orden fijo. |
| Resultados principales | `data/embeddings_v1/<modelo>/shards/` | Vectores originales; 489 bloques por modelo. |
| Procedencia de cada modelo | `data/embeddings_v1/<modelo>/manifest.json` | Versión, entrada, programa, entorno y receta usada. |
| Programa guardado con los resultados | `data/embeddings_v1/source_snapshot/` | Copia de la implementación usada. |
| Prueba técnica habitual | `data/embedding_pilot_v1/` | 1.300 artículos; no usar como muestra final. |
| Prueba técnica con fragmento común | `data/embedding_control_pilot_v1/` | Los mismos 1.300 artículos con texto común. |
| Índice ligero nuevo | `data/analysis_ready_v1/metadata.parquet` | 500.000 filas; áreas, años, base/complemento y calidad. Unos 45 MB. |
| Catálogo para programas | [catalog.json](research/embedding_final_audit_2026-09-17/catalog.json) | Rutas y huellas de cada bloque/variante, dimensiones y versiones. |
| Inventario de bloques | [shard_inventory.csv](research/embedding_final_audit_2026-09-17/shard_inventory.csv) | 4.890 carpetas, con posiciones y archivos. |
| Informe final | [EMBEDDINGS_AUDIT.md](EMBEDDINGS_AUDIT.md) | Resultado de las comprobaciones y límites. |
| Acceso para análisis | [sos_analysis/reader.py](sos_analysis/reader.py) | Lectura comprobada, por bloques, sin cambiar los datos. |

## Cómo se relacionan los archivos

La fila `row_index` identifica la misma posición en todos los modelos. `work_id` identifica el artículo de OpenAlex. `text_sha256` comprueba que se usó el mismo texto de origen. Cada bloque contiene una tabla `rows.parquet`, sus archivos de vectores y `commit.json`, que registra sus huellas. Los rangos son inicio incluido y final excluido.

La tabla ligera conserva `cohort`: **400.000 `base` y 100.000 `extra`**. También conserva Field, Subfield, año, período, DOI, tipo, longitudes y marcas de idioma/contenido/duplicados. Los textos y la procedencia detallada siguen en el corpus completo. No se han eliminado casos nuevos.

Los vectores ocupan **26,88 GB decimales / 25,04 GiB**, sin contar tablas, pesos ni pruebas. Todos son números de 32 bits (`float32`), sin normalización. Esta elección de almacenamiento conserva la información. La transformación de análisis se fijó después en `ANALYSIS_PROTOCOL.md`: longitud igual como principal, originales como control. El almacenamiento original no se cambia.

## Revisión previa y atlas de casos

| Material nuevo | Ruta | Contenido |
| --- | --- | --- |
| Diseño y selección | [CASE_ATLAS_PROTOCOL.md](CASE_ATLAS_PROTOCOL.md), `config/case_atlas_v1.json` | Criterios anteriores a la lectura de títulos; seguimiento exploratorio posterior a los resultados generales. |
| Atlas completo local | `data/prepaper_v1/case_atlas/` | 217 especialidades, 10.850 consultas, 531.650 relaciones dirigidas y 23.436 parejas de centros; manifiesto y auditoría. |
| Entrega legible | [CASES.md](reports/prepaper_v1/CASES.md), `reports/prepaper_v1/` | Doce artículos y sus relaciones, tablas, dos figuras en tres formatos y catálogo de huellas. |
| Verificación de la fuente | `data/prepaper_v1/source_quality/` | Identidades/etiquetas de 500k; 30 registros comparados con respuestas originales; diagnóstico posterior de 82 títulos genéricos. |
| Comprobación numérica independiente | [numerical_audit.json](research/prepaper_2026-09-17/numerical_audit.json) | Seis comparaciones de forma y 300 consultas reconstruidas por otra vía; 15 componentes sellados verificados. |
| Literatura y referencias | [references/README.md](references/README.md) | Biblioteca canónica de 45 entradas, correcciones, fuentes y límites de lectura. |
| Evidencia de esta revisión | `research/prepaper_2026-09-17/` | Pruebas, inventario, registros de acceso, auditoría final y copia de los 23 documentos del cierre anterior. |

`case_texts_local.json` contiene textos completos para revisar ejemplos; queda en `data/`, fuera de Git. Los originales no se han movido. Estas rutas son **locales**, no un depósito público: [plan de disponibilidad](docs/DATA_RELEASE.md).

## Variantes originales por modelo

| Modelo: nombre de carpeta | Salidas disponibles | Números por artículo |
| --- | --- | ---: |
| `specter` | `cls` | 768 |
| `specter2` | `cls` | 768 |
| `scincl` | `cls` | 768 |
| `scibert` | `mean`, `cls`, `sep` | 768 |
| `bert` | `mean`, `cls`, `sep` | 768 |
| `mpnet` | `mean` | 768 |
| `minilm` | `mean` | 384 |
| `pubmedbert` | `mean`, `cls`, `sep` | 768 |
| `biobert` | `mean`, `cls`, `sep` | 768 |
| `simcse` | `cls` | 768 |

`mean`, `cls` y `sep` son tres maneras ya guardadas de resumir la salida de un modelo; están explicadas en [EMBEDDINGS.md](EMBEDDINGS.md). Hay **diez modelos y dieciocho variantes**, no dieciocho modelos independientes. Las revisiones exactas, incluido el adaptador de SPECTER2, están en [config/embeddings_v1.json](config/embeddings_v1.json) y en el catálogo.

## Leer las representaciones originales

Ejecutar con `.venv-embed/bin/python` desde la raíz del repositorio. Ejemplo de acceso, **sin calcular nuevas comparaciones**. La receta principal de análisis de los cuatro BERT ya está fijada en el protocolo:

```python
import json
from pathlib import Path
from sos_analysis import EmbeddingCorpus

audit = json.loads(Path("research/embedding_final_audit_2026-09-17/audit_summary.json").read_text())
corpus = EmbeddingCorpus(Path.cwd(), catalog_sha256=audit["catalog_sha256"])
for metadata, vectors in corpus.iter_aligned(
    {"specter": "cls", "minilm": "mean"}, cohorts=["base"]
):
    # vectors["specter"][i] y vectors["minilm"][i] pertenecen al mismo artículo.
    # Procesar este bloque y descartarlo antes de pasar al siguiente.
    pass
```

También admite `field_ids=[...]` y `periods=[...]`, con valores existentes en los datos. Cada modelo requiere una salida explícita. El lector comprueba huellas, procedencia, orden, IDs, textos, dimensiones y valores antes de entregar cada bloque seleccionado. Un filtro puede saltar bloques ajenos a la selección; no significa que vuelva a auditar todo el repositorio. No aplica normalización, pesos ni exclusiones de calidad. Las matrices se abren solo para lectura; acumular todos los bloques en una lista eliminaría el ahorro de memoria.

Comprobación completa del lector, sin ejecutar modelos:

```sh
.venv-embed/bin/python research/embedding_final_audit_2026-09-17/verify_reader.py
```

La pasada real leyó las 18 variantes, con un máximo de unos 0,72 GB de memoria del proceso. Resultado: [reader_verification.json](research/embedding_final_audit_2026-09-17/reader_verification.json). Las pruebas de errores artificiales están en [reader_tests.txt](research/embedding_final_audit_2026-09-17/reader_tests.txt).

## Conservación

Las carpetas grandes están excluidas de Git: el repositorio remoto no es una copia de seguridad de estos datos. No se han borrado originales ni recorridos provisionales. Los SPECTER2 antiguos del TFM no se incorporaron: los resultados actuales se calcularon con la versión fijada. El lector depende de las rutas actuales; cualquier traslado futuro requiere actualizar y comprobar un catálogo nuevo.

## Comparación terminada, 17-09-2026

| Material nuevo | Ruta | Contenido |
| --- | --- | --- |
| Informe comprensible | [ANALYSIS_RESULTS.md](ANALYSIS_RESULTS.md) | Hallazgos, controles, áreas, alertas y límites. |
| Entrega para el paper | `reports/analysis_v1/final/` | 33 CSV, ocho figuras en tres formatos, resumen JSON, auditoría y catálogo con huellas. |
| Resumen por artículo | `reports/analysis_v1/final/article_neighbor_stability.parquet` | 500.000 filas con `row_index`, `work_id`, Field, período, base/refuerzo y media/extremos de coincidencia de vecinos. |
| Forma y selección | `data/analysis_v1/shape/` | 130 celdas, base general, centros, recetas, calidad, 20 selecciones por tamaño y referencias mezcladas. |
| Listas exactas de vecinos | `data/analysis_v1/neighbors/` | Todos los 500.000 dentro de área/período; 13.000 consultas globales sobre base de 400.000; coincidencias por artículo. Los IDs de vecinos son posiciones globales `row_index`. |
| MiniLM ampliado | `data/analysis_v1/controls/minilm_512/` | 500.000 filas, variante de 512; original de 256 intacto. |
| Control de contenido común | `data/analysis_v1/controls/common_text_52k/` | 52.000 IDs compartidos por diez modelos, 400 por área/período; entrada, fuentes y salidas guardadas. |
| Comparaciones de control | `data/analysis_v1/robustness_controls/` | MiniLM, contenido común, tres recetas y 2.048 candidatos idénticos por celda; listas y resúmenes. |
| Seguimiento entre centros | `data/analysis_v1/macro_controls/` | Receta, calidad, longitud del vector y texto común sobre 52.000 emparejados. |
| Referencia de grupos aleatorios | `data/analysis_v1/centroid_random_groups/` | 20 repartos de 26 grupos de 2.000, con 400 artículos de cada período por grupo. |
| Nuevas auditorías de vectores | `research/analysis_2026-09-17/extra_output_audit/` | Once controles completos, reutilización exacta, textos, IDs, recortes, versiones y huellas. |
| Fuentes y bibliografía | `research/analysis_2026-09-17/` | Revisión de medidas, ocho referencias verificadas, fuentes primarias, registros de ejecución y comprobaciones. |

El índice global `row_index` sigue identificando el corpus original también en las selecciones. No usar el número de fila local de un control como si fuera ese índice. Los manifiestos y archivos de selección guardan la correspondencia. Ninguna carpeta se ha movido.

Los nuevos programas usan `.venv-analysis/`, fijado en `requirements-analysis.txt`. La inferencia adicional usó el entorno original sin modificarlo. La entrega se puede reconstruir con el comando de [NEXT_STEPS.md](NEXT_STEPS.md), sin volver a calcular los modelos ni los vecinos. El archivo por artículo y las carpetas grandes siguen siendo locales; preparar su distribución es una tarea posterior.

## Checklist adicional terminada, 17-09-2026

| Material | Ruta | Contenido |
| --- | --- | --- |
| Informe de los seis puntos | [CHECKLIST_RESULTS.md](CHECKLIST_RESULTS.md) | Resultados, decisiones, alertas y límites. |
| Entrega adicional | `reports/checklist_v1/final/` | 33 CSV, siete figuras PDF/SVG/PNG, resumen, auditoría, catálogo de huellas y copia del exportador. |
| Selección y textos del piloto | `data/checklist_v1/inputs/native_input.parquet`, `title_input.parquet`, `abstract_input.parquet` | Los mismos 26.000 IDs; 200 por Field/período, ordenados por `row_index` original. Manifiesto `input_manifest.json`. |
| Tres entradas por modelo | `data/checklist_v1/inputs/<title,abstract,title_abstract>/<modelo>/` | Veinte condiciones nuevas y diez reutilizadas exactamente; bloques, vectores, tokens, textos, versiones y huellas. Cuatro BERT con sus tres recetas. |
| Comparación principal del piloto | `data/checklist_v1/input_comparisons/` | 26 áreas de 1.000 artículos; CKA, rangos, vecinos 10/25/50, efectos y 20 selecciones por área. Listas por área en `fields/`. |
| Cruce de entrada y receta | `data/checklist_v1/input_recipes/` | Mean reproducida y CLS/SEP; efectos por modelo/área, auditoría, vecinos alternativos y fuente congelada. |
| Tiempo, disciplinas y familias | `data/checklist_v1/existing_v2/` | Resúmenes de datos anteriores, 20 resultados/controles, trayectorias, regresión descriptiva y referencias por permutación/omisión. |
| Consultas temporales idénticas | `data/checklist_v1/candidate_check/` | 266.240 consultas compartidas contra todos los candidatos y contra 2.048; diagnóstico posterior, sin volver a buscar vecinos. |
| Perfil de textos | `data/checklist_v1/text_profile/` | Repeticiones y longitudes por área/condición, sin excluir artículos después de seleccionarlos. |
| Alertas del piloto | `reports/checklist_v1/final/tables/input_stability_alerts.csv` | 31 contrastes individuales de forma; la tabla `input_stability.csv` conserva también los que pasan. |
| Auditoría de todas las entradas | `research/checklist_2026-09-17/input_audit/` | Identidades, texto/tokens, todas las recetas, valores finitos, huellas y reutilización bit a bit. |
| Fuentes y pruebas | `research/checklist_2026-09-17/` | Procedencia de modelos, antecedentes de entradas, pruebas reales, siete pruebas matemáticas/de flujo, registros y cierre. |
| Programas y protocolo | `sos_followup/`, `CHECKLIST_PROTOCOL.md`, `METHODS_CHECKLIST.md` | Las implementaciones científicas tienen copia y huellas en sus salidas. Configuraciones `checklist_v1.json` y `checklist_input_recipes_v1.json`. |

El piloto reúne cinco períodos por área, con 1.000 candidatos; no confundirlo con los 2.048 candidatos **por área/período** del control anterior. Hay 780.000 filas modelo–artículo–entrada, pero solo 26.000 artículos distintos. `title_abstract` reutiliza 260.000 filas modelo–artículo; 520.000 son inferencia nueva. Las alternativas de receta no se cuentan como modelos independientes.

El intento parcial `data/checklist_v1/existing/` se conserva como historial y no se usa en la entrega. La versión completa declara la omisión SEP sin SimCSE no identificable. Las carpetas `preview/` tampoco son la entrega final. Todo permanece en salidas separadas y se reconstruye con el exportador de [NEXT_STEPS.md](NEXT_STEPS.md).

## Ampliación a 52k y controles de especialidades

Todas las rutas siguientes pertenecen al proyecto nuevo. Las auditorías científicas están en cada componente; la comprobación conjunta está en `data/robustness_v2/final_audit/`. El estado de presentación se registra aparte en `reports/robustness_v2/final/audit.json`.

| Material | Ruta | Contenido y alcance |
| --- | --- | --- |
| Informe principal de la ampliación | [ROBUSTNESS_RESULTS.md](ROBUSTNESS_RESULTS.md) | Resultados, límites y decisiones; no es el manuscrito. |
| Métodos nuevos | [METHODS_ROBUSTNESS.md](METHODS_ROBUSTNESS.md) | Definiciones, muestras, controles, versiones y reproducción. |
| Presentación integrada | `reports/robustness_v2/final/` | Tablas resumidas, siete figuras PDF/SVG/PNG, resumen, catálogo y exportador. |
| Entradas nuevas | `data/robustness_v2/inputs/` | Tres Parquet de los mismos 52.000 IDs, 400 por área/período. Contienen exactamente el piloto de 26k; manifiesto y 30 condiciones de modelo/entrada. |
| Auditoría independiente de entradas | `research/robustness_2026-09-17/input_audit/` | Texto, tokens, orden, reutilización exacta y todas las recetas. 1.560.000 combinaciones modelo–artículo–entrada. |
| Forma y vecinos por entrada | `data/robustness_v2/input_comparisons/` | 26 grupos de 2.000; tres entradas, k=10/25/50, efectos y selección. |
| Cruce de recetas | `data/robustness_v2/input_recipes/` | Mean/CLS/SEP sobre las tres entradas; mean reproducida, comparación por modelo/área/entrada. |
| Cien selecciones en ambos tamaños | `data/robustness_v2/input_stability100/` | IDs y valores brutos de 26k/52k, primeras 20 reproducidas, 31 claves originales y transiciones de alertas. |
| Resumen integrado de entradas | `data/robustness_v2/input_review/` | Efectos globales/por modelo/por área, cambios de receta/signo y seguimiento de alertas. |
| Especialidades completas | `data/robustness_v2/subfields_native/` | 252 Subfields, cobertura de 500.000 IDs, CKA/rangos/Procrustes y vecinos; grupos no informativos identificados. |
| Tamaños y selección por especialidad | `data/robustness_v2/subfield_controls/` | 128/256/512; 183 grupos comunes; 20 selecciones; 125 grupos con cinco períodos a 128; recetas. |
| Vecinos con mismas consultas/fechas | `data/robustness_v2/paired_neighbor_scales/` | 10.850 consultas, 217 especialidades, diez selecciones de 256 candidatos. IDs, listas exactas y dos Parquet de resultados por artículo/par. |
| Puntuación por cada artículo | `data/robustness_v2/regions_native/paper_agreement.parquet` | Los 500.000 IDs; vecinos por Field/período y Subfield, k, omisiones de modelos/familias y marcas de casos triviales. |
| Localización de regiones y ejemplos | `data/robustness_v2/regions_native/regions.csv` y `paper_examples.csv` | Distribuciones por grupo y ejemplos seleccionados con reglas explícitas. No etiquetas universales de calidad. |
| Centros y grupos aleatorios | `data/robustness_v2/centroid_scales/` | Centros nativos/igualados, selecciones, veinte referencias aleatorias y archivos NPZ con huellas propias. |
| Tiempo y candidatos | `data/robustness_v2/temporal_review/` | 23.400 trayectorias; heterogeneidad y separación exacta del efecto de consultas/candidatos. |
| Composición de Medicina y otras áreas | `data/robustness_v2/medicine_composition/` | 2.048 por área, fechas iguales, observado/equilibrado, diez selecciones, cobertura y grupos de modelos. |
| Rasgos de los diez modelos | `data/robustness_v2/family_traits/` | Configuración real, fuentes, linaje/corpus/objetivo/dominio/receta, asociaciones, 5.000 permutaciones y omisiones. |
| Revisión vigente de controles | `data/robustness_v2/control_review_v2/` | 50 alertas originales reconstruidas; medidas, calidad, MiniLM y texto común. Separa MiniLM consigo mismo de su acuerdo con otros. |
| Resumen estructural vigente | `data/robustness_v2/structural_review_v3/` | Escalas, regiones, Medicina y familias; tablas derivadas y padres verificados. |
| Procedencia original comprobada | `data/robustness_v2/provenance/` | Inventario de 6.139 respuestas únicas OpenAlex y versiones; corpus, 4.890 bloques y 8.802 archivos de vectores originales verificados. |
| Literatura ampliada | [RELATED_WORK_UPDATE.md](research/robustness_2026-09-17/RELATED_WORK_UPDATE.md) | Cinco antecedentes pedidos, trabajos próximos de 2025–26, fuentes primarias y límites de acceso. |
| Ejecución, pruebas y cierre | `research/robustness_2026-09-17/` | Registros, configuración de ejecutores, auditorías y pruebas de ambos entornos. |

La selección de entradas de 52k **no es** la del control de fragmento común de 52k. Se unen por `row_index`/`work_id`, nunca por la posición local suponiendo que coincidan. La auditoría conserva ambas selecciones por separado.

`control_review/` es un resumen anterior: no usar su promedio MiniLM que mezcla comparación consigo mismo y con otros. `structural_review/` y `structural_review_v2/` son intentos incompletos conservados; el vigente es `structural_review_v3/`. Las carpetas de vista provisional no sustituyen la entrega final.

Los archivos grandes permanecen locales y fuera de Git. La copia de respuestas OpenAlex se recogió a lo largo del 15-09-2026; no es una instantánea global simultánea de la base. Reconstruir la presentación con el comando de [NEXT_STEPS.md](NEXT_STEPS.md) no repite inferencia ni búsqueda de vecinos.


## Piloto separado de morfología, 18-09-2026

| Material | Ruta | Contenido |
| --- | --- | --- |
| Diseño anterior a resultados | `MORPHOLOGY_PROTOCOL.md`, `config/morphology_pilot_v1.json` | Apertura, espectro y conexión; alternativas y controles. |
| Selecciones | `data/morphology_pilot_v1/selections.npz`, `selection_audit.json` | 1.406 arrays emparejados; 52k principal y selecciones derivadas del mismo corpus. |
| Cálculo completo | `data/morphology_pilot_v1/metrics.parquet`, `parts/` | 16.884 conjuntos, treinta bloques; no inferencia nueva. |
| Auditorías | `data/morphology_pilot_v1/audit.json`, `independent_audit.json`, `synthetic/` | Completitud, fórmulas independientes y contraejemplos. |
| Entrega | `reports/morphology_pilot_v1/` | Veinte tablas, cinco figuras en tres formatos, resumen y catálogo. |
| Lectura | [MORPHOLOGY_RESULTS.md](MORPHOLOGY_RESULTS.md), [METHODS_MORPHOLOGY.md](METHODS_MORPHOLOGY.md) | Conclusiones condicionales, cuatro alertas PR y 51 de conexión conservadas. |

Se leen los originales de 500k, las tres entradas 52k, el control de fragmento común y MiniLM512. No se mezclan las dos selecciones 52k ni se genera ningún embedding nuevo. Los IDs de las referencias gaussianas identifican la muestra de origen usada para ajustarlas; sus puntos sintéticos no son artículos representados. Los datos anteriores mantienen sus rutas.
## Revisión de estructura y argumentación de QSS, 18-09-2026

Material bibliográfico; no añade ni modifica datos del experimento.

| Material | Ruta | Alcance |
| --- | --- | --- |
| Síntesis y propuesta | [QSS_STRUCTURE_REVIEW.md](QSS_STRUCTURE_REVIEW.md), [PAPER_OUTLINE.md](PAPER_OUTLINE.md) | Normas consultadas, prácticas y propuesta propia separadas |
| Marco y selección | `research/qss_structure_2026-09-18/journal_inventory.json`, `article_matrix.csv` | 465 registros Crossref y 34 artículos seleccionados |
| Notas y bibliografía | [READING_NOTES.md](research/qss_structure_2026-09-18/READING_NOTES.md), `qss_review.bib` | 33 lecturas estructurales, once con foco adicional; una parcial; versiones explícitas |
| Evidencia local | `data/qss_structure_review_v1/` | Respuestas originales, copias de consulta y huellas; textos completos de terceros excluidos de Git |
| Cierre y conservación | `research/qss_structure_2026-09-18/closure_audit.json`, `baseline_documents/` | Verificación de metadatos, enlaces, copias previas y fuentes científicas |


## Cierre final de robustez, 20-09-2026

| Material | Ruta | Contenido |
| --- | --- | --- |
| Resultados completos | `data/robustness_closure_v1/{centres,headline,morphology,quality}/` | Selecciones, índices, vectores de centros, búsquedas y resultados por condición; fuentes/configuración y huellas. |
| Congelación de ramas | `data/robustness_closure_v1/summary/` | Manifiesto que enlaza las ramas completas; auditoría. |
| Entrega ligera | `reports/robustness_closure_v1/` | 25 CSV, `summary.json` y catálogo de huellas. |
| Semillas y entorno | `research/robustness_closure_2026-09-20/random_seeds.csv`, `execution_environment.json` | 190.884 pares de etiqueta y semilla; versiones y plataforma. |
| Revisión numérica y editorial | `research/robustness_closure_2026-09-20/` | Auditoría previa, once afirmaciones, controles independientes, PDF y paquetes. |

No se movieron corpus o embeddings. Las fuentes y los resultados nuevos están congelados; las figuras y tablas tipográficas son derivados separados de presentación. El ZIP del manuscrito reproduce los documentos, no todos los experimentos.
