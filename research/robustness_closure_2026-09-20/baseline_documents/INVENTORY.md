# Inventario de infraestructura y datos reutilizables

**Actualización del proyecto nuevo, 17-09-2026:** el inventario de resultados actuales está en [DATA_CATALOG.md](DATA_CATALOG.md): corpus propio de 500.000, diez modelos completos, tres entradas en 52.000 y controles de áreas/especialidades. Interpretación en [ROBUSTNESS_RESULTS.md](ROBUSTNESS_RESULTS.md), estado en [NEXT_STEPS.md](NEXT_STEPS.md). El inventario del TFM que sigue es histórico y se conserva como referencia; sus SPECTER2 no se mezclaron con los nuevos.

Revisión local: **14 de septiembre de 2026**. Proyecto de referencia: [Mapping-Science](https://github.com/aleetreny/Mapping-Science), commit `4ed7127c50fc08e27eeb18b2f02ab9fa50ceacaf`. Inspección en lectura; no se ejecutaron extracciones ni experimentos.

**Conclusión: ya tenemos el corpus limpio y SPECTER2 para sus 2.378.036 papers. No hace falta volver a descargar OpenAlex ni recalcular esos embeddings para empezar a preparar el nuevo estudio.**

> Actualización de diseño, 14-09-2026: este inventario describe lo que existe. La preparación ahora decidida es una muestra nueva de 500.000, con selección probabilística y filtros propios, según `CORPUS_PROTOCOL.md`. La reutilización del TFM sirve para código, comprobaciones e IDs coincidentes; su reparto anterior no sustituye la muestra representativa decidida.

## 1. Dónde está lo importante

La copia completa está en **`/Users/alejandrotreny/Workspace/Mapping-Science`**. Todas las rutas siguientes parten de esta carpeta; `E` abrevia `embeddings/specter2_v1_2000_2024_400py/`.

La ruta facilitada, `/Users/alejandrotreny/Library/Mobile Documents/com~apple~CloudDocs/Github/Localizate`, corresponde a otro proyecto. La copia en `/Users/alejandrotreny/Library/Mobile Documents/com~apple~CloudDocs/Github/TFM/sources/Mapping-Science` conserva el mismo commit y código, pero sus directorios de datos contienen solo marcadores. Los archivos grandes están excluidos de Git.

| Recurso disponible | Ubicación | Contenido y utilidad |
| --- | --- | --- |
| Corpus limpio | `data/processed/works_text_2000_2024_400py.parquet` | **2.378.036 IDs únicos**, 2000–2024, 26 Fields, **252 Subfields**, 4 Domains; 3,88 GiB. Fuente principal reutilizable. |
| Taxonomía | `data/interim/{domains,fields,subfields}.parquet` | IDs, nombres y relaciones jerárquicas; 4/26/252 filas. |
| Conteos y muestreo | `data/interim/{domain,field,subfield}_year_counts_2000_2024_400py.parquet`; `corpus_plan_2000_2024_400py.parquet` y `sample_plan_2000_2024_400py.parquet` en ese mismo directorio | Cobertura y plan histórico; 6.300 celdas Subfield×año, semillas y cupos. |
| Registro de extracción | `data/interim/download_manifest_2000_2024_400py.parquet`; `outputs/01_corpus_construction/` | Resultados por celda, semillas, descartes, déficits y reportes de validación. |
| SPECTER2 completo | `E/shard_0000_*` hasta `E/shard_0118_*` | **119 triples**: `*_embeddings.npy`, `*_metadata.parquet`, `*_summary.json`. Total **2.378.036 × 768**, `float16`; matrices originales: 3,40 GiB. |
| Índice completo de vectores | `data/processed/embedding_index.parquet` | `work_id → embedding_shard_file + embedding_row_in_shard`, con etiquetas y año. Cubre todo el corpus. |
| Matriz del análisis del TFM | `E/analysis/main_embeddings.float16.npy`; `E/analysis/main_work_ids.parquet`; `data/processed/analysis_embedding_index.parquet` | **2.344.927 × 768**, `float16`, 3,35 GiB; 241 Subfields y 26 Fields. `analysis_row_id` identifica la fila de la matriz. |
| Base DuckDB | `warehouse/tfm_openalex.duckdb` | 36,59 GiB; abre correctamente en modo lectura. Contiene corpus, índices, taxonomía, planes y manifiestos, con tablas versionadas y sin sufijo. El Parquet permite reutilizar el corpus sin copiar toda esta base. |
| Análisis ya calculados | `data/processed/subfield_embedding_space_metrics.{parquet,csv}`; `data/processed/temporal/`; `outputs/03_embedding_metrics/`, `outputs/04_reduced_metric_core/`, `outputs/05_static_comparison/` | Métricas de 241 Subfields, centroides, trayectorias y comparaciones previas. `outputs/08_visualization/` contiene las proyecciones. Útiles como referencia y para comprobar futuras adaptaciones. |

## 2. Estructura del corpus y correspondencia con embeddings

El Parquet contiene una fila por paper y conserva:

- **Identidad y texto:** `work_id` (cadena `W…`), `doi` opcional, `title`, `abstract`, `text_for_embedding`.
- **Tiempo y selección:** `publication_year`, `publication_date`, `type`, `language`, `downloaded_at`.
- **Clasificación:** `field_id`, `subfield_id`, `domain_id`, sus respectivos `*_display_name`, `primary_topic_id`, `primary_topic_display_name` y `topics_json`. Field/Subfield son cadenas numéricas y proceden del **primary topic**.
- **Información adicional:** `title_token_count`, `abstract_token_count`, `text_token_count`, `cited_by_count`, `referenced_works_count`. Estos últimos son conteos, no un grafo de citas.

Se mantienen **título y abstract separados**, suficientes para preparar después distintas entradas. `text_for_embedding` concatena título, dos saltos de línea y abstract; los conteos de limpieza son palabras por regex, no tokens del modelo. Los metadatos de los shards no incluyen el texto: hay que unirlos al corpus por `work_id`.

El corpus se descargó entre el **10 y el 12 de mayo de 2026**. Contiene 2.276.707 artículos y 101.329 preprints, todos etiquetados como inglés. Se verificaron cero IDs duplicados y cero títulos, abstracts, años o IDs de Field/Subfield ausentes.

## 3. Código que merece reaprovecharse

- **Extracción completa:** `scripts/00_fetch_taxonomy.py` a `scripts/06_build_analysis_subfields.py`; cliente, filtros, paginación y reintentos en `src/openalex.py`; reconstrucción del índice invertido en `src/abstracts.py`; limpieza/esquema en `src/works.py`; semillas y reanudación en `src/sampling.py` y `src/download_state.py`.
- **Embeddings e índices:** `scripts/embed_specter2_kaggle.py`, `src/embeddings.py`, `src/analysis_matrix.py` y scripts `07_validate_embeddings.py` / `08_prepare_analysis_matrix.py`. La receta archivada utiliza título + separador del tokenizador + abstract.
- **Muestreo y análisis local:** `sample_subfield_rows` en `src/per_subfield_umap_maps.py`, `src/temporal_common.py`, `src/embedding_space_metrics.py` y `src/reduced_interpretable_embedding_core.py`: selección reproducible, ventanas temporales, dispersión, kNN, hubness y espectro PCA.
- **Verificación e infraestructura:** `tests/test_{sample_plan,embeddings,analysis_matrix,embedding_space_metrics}.py`. El entorno `.venv/bin/python` existente permite leer NumPy, Parquet y DuckDB; se utilizó para esta auditoría.

## 4. Problemas e incompatibilidades

1. **Corpus filtrado y equilibrado por Subfield×año.** Hasta 400 papers por celda; inglés, artículos/preprints, título ≥5 palabras y abstract ≥80; filtros de retractados/paratext según configuración y reporte histórico. Hay 805 celdas con menos de 400 papers y 2 vacías. No representa los volúmenes naturales de publicación ni incluye conferencias como tipo separado. `data/raw/` está vacío: no se conservaron las respuestas originales de OpenAlex.
2. **241 Subfields es una selección del TFM, no toda la extracción.** La matriz compacta aplica elegibilidad temporal (≥5.000 papers y ≥20 años). Los **33.109 papers restantes también tienen SPECTER2** en los shards. Los flags heredados, incluidos nombres con sufijos `2500`/`500`, no deben decidir automáticamente la muestra nueva.
3. **Procedencia de SPECTER2 incompleta.** `E/embedding_config.json` registra `allenai/specter2_base` + adaptador `allenai/specter2`, CLS, longitud máxima 512 y `float16`, pero no las revisiones exactas de modelo/tokenizador/adaptador. Además, declara procesamiento por grupos Parquet sin ordenación global; el script archivado sí ordena globalmente. Falta localizar la versión exacta ejecutada. **Usar los índices reales, nunca inferir el orden de los vectores.**
4. **Registros y defaults antiguos.** `E/embedding_run_manifest.csv` solo recoge shards 60–118, aunque están los 119 triples completos. Algunos documentos, el descargador desde Drive y la validación todavía esperan 37 shards. `requirements.txt` no fija versiones ni incluye todas las dependencias del generador GPU.
5. **Normalización y adaptación entre modelos.** Los vectores guardados no tienen norma unitaria; las métricas antiguas convierten a `float32` y normalizan L2. Las funciones matemáticas son aprovechables, pero rutas, dimensiones y selección están acopladas a SPECTER2. Comparar dimensionalidades distintas requiere revisar métricas como el número de componentes PCA. Los scripts escriben dentro del proyecto antiguo: habrá que adaptar componentes en el repo nuevo antes de ejecutarlos.

## 5. Qué faltaba al realizar el inventario inicial

- Fijar una muestra común de `work_id`, sus textos, etiquetas y orden, con huellas de contenido. La extracción existente permite hacerlo sin nuevas consultas a OpenAlex.
- Completar la trazabilidad de SPECTER2 y decidir después si los vectores heredados cumplen el protocolo nuevo. No se localizaron embeddings de otros modelos para este corpus.
- Preparar posteriormente los otros modelos, variantes de entrada y comparaciones emparejadas. No se encontró implementación de CKA ni de kNN overlap entre modelos en el código activo revisado.

**Alcance de la verificación:** se inspeccionaron schemas y recuentos reales, los 119 triples y la base en lectura. Los IDs del corpus, índice completo y metadatos coinciden globalmente; también coincide la alineación del índice analítico con `main_work_ids`. Se cotejaron 357 vectores compactos contra sus shards sin diferencias y se revisaron 1.190 vectores originales, todos finitos y no nulos. La comprobación numérica fue muestral, no de todas las celdas. No se copiaron datasets, modificaron fuentes ni iniciaron experimentos.

## Actualización del nuevo proyecto, 15-09-2026

El repo nuevo ya contiene `data/corpus_500k/corpus.parquet`: 500.000 registros, 400.000 base y 100.000 complemento. Descarga y selección comprobadas por completo. `AUDIT.md` documenta errores de contenido de origen. El usuario autorizó después limpiarlos y completar una copia separada; resultado actualizado en `CLEANING.md`.

Hay 22.118 coincidencias exactas de título+abstract con vectores antiguos localizados y comprobados numéricamente. Índice listo: `research/corpus_audit_2026-09-15/legacy_embedding_candidates.parquet`. La falta de revisiones exactas del modelo antiguo sigue pendiente; no se autoriza reutilización final automáticamente.

### Material limpio ya preparado

La entrada que debe usarse ahora es **`data/corpus_clean_v1/embedding_input.parquet`**: 500.000 IDs con título y abstract separados, orden y huellas. La tabla maestra contigua conserva año, Field/Subfield, temas, base/complemento, calidad y procedencia. Reglas y resultados en `CLEANING.md`; continuación en `EMBEDDINGS_READY.md`.

Se reutilizaron las páginas originales para 499.990 de los registros finales; solo diez proceden de una página nueva. El índice actualizado de los 22.118 vectores históricos candidatos está en `research/cleaning_2026-09-15/legacy_embedding_candidates.parquet`. Sigue faltando identificar sus versiones exactas antes de aprobarlos. El TFM permanece intacto.
