# Material preparado: embeddings terminados y revisados

**17-09-2026: diez modelos completos sobre 500.000 artículos; auditoría final aprobada.** Resultado en [EMBEDDINGS_AUDIT.md](EMBEDDINGS_AUDIT.md), acceso en [DATA_CATALOG.md](DATA_CATALOG.md) y continuación en [NEXT_STEPS.md](NEXT_STEPS.md). Esta guía conserva las reglas del corpus y la preparación ya realizada; no repetir descarga o cálculo.

**Corpus de 500.000 filas, 400.000 base + 100.000 complemento, preparado y verificado el 15-09-2026.** El usuario realizó después el cálculo completo de los diez modelos; todos están comprobados.

## Archivos que se usarán

- `data/corpus_clean_v1/embedding_input.parquet`: misma lista de IDs, títulos y abstracts para todos los modelos. Cada fila tiene `row_index`, empezando por cero.
- `data/corpus_clean_v1/corpus.parquet`: información completa de clasificación, año, base/complemento, calidad y procedencia.
- `data/corpus_clean_v1/embedding_manifest.json`: huellas de los archivos y del orden de IDs/textos.
- `CLEANING.md`: reglas, descartes y límites. `research/cleaning_2026-09-15/`: comprobaciones y recuentos.

Comprobación antes de empezar, desde esta carpeta:

```sh
./prepare.sh preflight
```

Este comando comprueba que los archivos no han cambiado. No descarga nada ni calcula embeddings.

## Columnas de la entrada común

| Columna | Significado |
| --- | --- |
| `row_index`, `work_id` | Posición fija, desde cero, e ID de OpenAlex. |
| `title`, `abstract` | Textos recibidos, conservados por separado. |
| `text_sha256` | Huella de título + dos saltos de línea + abstract, exactamente como se guardaron. No impone ese separador como entrada de todos los modelos. |
| `cohort` | `base` para los 400.000 generales; `extra` para los 100.000 de refuerzo. |
| `field_id`, `publication_year`, `period_start` | Área principal, año exacto e inicio del período de cinco años. |
| Marcas de calidad y duplicados | Permiten apartar casos en comprobaciones posteriores sin perder la correspondencia de filas. |

La tabla maestra añade DOI, Subfield, temas secundarios, fechas de descarga, longitud, diagnóstico de idioma y página de procedencia. El esquema completo puede consultarse leyendo el propio Parquet, un archivo de tabla pensado para muchos registros. Los datos grandes están fuera de Git.

## Lo que deben respetar todos los modelos

1. Misma fila = mismo paper y mismo texto de origen. Conservar `work_id`, `row_index` y `text_sha256` junto a cada vector.
2. Elegir y registrar versión exacta de modelo, adaptación si la hay, herramienta que divide el texto y reglas de entrada. El texto original está separado en título y abstract; el formato y el recorte deben quedar explícitos para cada modelo.
3. Procesar por bloques y guardar progreso, errores y huellas. Poder pausar y continuar sin mezclar versiones ni perder el orden.
4. Comprobar número de filas, IDs, dimensiones y valores válidos. No dar un cálculo por terminado solo porque exista el archivo.
5. Mantener base y complemento separados al interpretar resultados. Las marcas de idioma dudoso, contenido revisable y duplicados permiten controles posteriores sin volver a descargar ni calcular todo.

## Decisiones que siguen perteneciendo al siguiente paso

El usuario ya eligió los diez y aceptó uso habitual + control de fragmento común. Versiones fijadas en `config/embeddings_v1.json` y recetas en `EMBEDDINGS.md`. Siguen abiertos los análisis y el tamaño definitivo del control; no confundirlos con la prueba técnica.

Hay **22.118 vectores SPECTER2 antiguos candidatos** con ID y texto exactos coincidentes. Se localizaron y comprobaron numéricamente en los 119 archivos originales; el índice actualizado es `research/cleaning_2026-09-15/legacy_embedding_candidates.parquet`. Esos candidatos no se incorporaron al cálculo actual. SPECTER2 se calculó de nuevo para los 500.000 artículos con la versión y preparación fijadas. El índice antiguo se conserva como referencia, no como entrada del análisis.

## Conservación y reanudación

Los originales siguen en `data/corpus_500k/`. La tabla nueva está en `data/corpus_clean_v1/`; conservar ambas carpetas, porque las páginas originales se referencian mediante enlaces relativos. Los recorridos con sufijos `initial_pass`, `second_pass` y `third_pass` son evidencia provisional y no deben usarse como entrada.

Para consultar la preparación: `./prepare.sh status`. Para reanudarla si se hubiera interrumpido: `./prepare.sh prepare`; conserva lo guardado y rechaza cambios en reglas o programa. Una vez validada, no hace falta reconstruirla para empezar los modelos. El modo `--offline` impide consultas API; la última reconstrucción se hizo así, reutilizando incluso la página adicional.

Estado comprobado: [readiness.json](research/cleaning_2026-09-15/readiness.json). El manifiesto `data/corpus_clean_v1/embedding_manifest.json` identifica los archivos finales y el orden de IDs/textos. La copia del programa usado está en `data/corpus_clean_v1/source_snapshot/`. `./prepare.sh preflight` ya pasó sobre esta versión final.
