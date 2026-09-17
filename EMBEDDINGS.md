# Calcular los diez modelos

> **Estado, 17-09-2026: los diez modelos terminaron y fueron comprobados.** Ver `EMBEDDINGS_AUDIT.md`, `DATA_CATALOG.md` y `NEXT_STEPS.md`. Los comandos de cálculo se conservan como documentación; no hace falta relanzarlos.

El usuario ha elegido los diez y pide iniciar él mismo el cálculo desde la terminal. **El cálculo completo no se ha arrancado desde este chat.** La prueba técnica usa 1.300 artículos ya descargados: diez de cada una de las 130 combinaciones de área y período. No añade artículos al corpus.

## Un comando para empezar

Desde la carpeta de este repositorio:

```sh
./start_embeddings.sh
```

Mantener el Mac enchufado y con la tapa abierta. El comando usa `caffeinate` para evitar la suspensión por inactividad y conserva mensajes/errores en `data/embeddings_run.log`. Los modelos se ejecutan uno detrás de otro. Los pesos ya están descargados y comprobados; **el cálculo funciona sin internet**.

Para parar: `Ctrl+C`. Para continuar: repetir exactamente el mismo comando. Solo se repite el bloque que estaba a medias; los bloques completos se comprueban y se conservan. Cada bloque contiene hasta 1.024 artículos. No abrir dos cálculos a la vez; el programa bloquea ejecuciones simultáneas sobre la misma salida.

Consultar lo guardado, desde otra terminal:

```sh
./embed.sh status --scope full
```

El estado es el último punto guardado; por sí solo no demuestra que el proceso siga vivo. Comprobación completa de archivos y correspondencia con los artículos:

```sh
./embed.sh verify --scope full
```

## Tiempo estimado

**25–35 horas en total.** La prueba real de los diez modelos da unas 24,1 horas al extrapolar su velocidad; se añade margen para una ejecución larga. No incluye los análisis científicos posteriores. Detalle por modelo y límites en `research/embedding_setup_2026-09-15/RESULTS.md`.

## Qué queda guardado

- Entrada: `data/corpus_clean_v1/embedding_input.parquet`, intacta, con 500.000 artículos. Se conserva la distinción entre 400.000 base y 100.000 complemento.
- Configuración exacta: `config/embeddings_v1.json`. No se usan versiones flotantes como `main` al descargar.
- Pesos: `.benchmark-models/`, aprovechando la caché anterior de SciNCL y MPNet. Once repositorios: diez modelos y el adaptador de SPECTER2. `data/embedding_assets_v1.json` fija las huellas de cada archivo, contrastadas con el editor del modelo.
- Resultados completos: `data/embeddings_v1/<modelo>/shards/`. Cada bloque tiene los vectores, `rows.parquet` y `commit.json` con sus huellas. La misma posición sigue correspondiendo al mismo artículo.
- Prueba técnica: `data/embedding_pilot_v1/`. Control técnico con texto común: `data/embedding_control_pilot_v1/`. Estos resultados no se mezclan con los completos.
- Programa y dependencias: `sos_embed/`, `embed.sh`, `requirements-embeddings.txt`, `.venv-embed/`. Cada salida conserva una copia del programa y su configuración en el manifiesto.
- Evidencia y tiempos: `research/embedding_setup_2026-09-15/RESULTS.md`.

Cada fila de resultados conserva ID, posición, huella del texto, área, año y grupo base/complemento. Añade cuántas piezas de texto había, cuántas leyó realmente el modelo y si tuvo que recortar. Las marcas de calidad originales se recuperan por ID/posición desde la tabla maestra.

## Recetas fijadas antes de comparar resultados

La columna «límite» se refiere a las pequeñas piezas en que cada modelo divide el texto, incluidos sus marcadores. No equivale al mismo número de palabras ni garantiza el mismo fragmento leído.

| Modelo | Fuente exacta | Límite | Salidas conservadas |
| --- | --- | ---: | --- |
| SPECTER | `allenai/specter` | 512 | CLS |
| SPECTER2 | `allenai/specter2_base` + `allenai/specter2` | 512 | CLS con adaptador de proximidad activo |
| SciNCL | `malteos/scincl` | 512 | CLS |
| SciBERT | `allenai/scibert_scivocab_uncased` | 512 | Media, CLS y SEP |
| BERT | `google-bert/bert-base-uncased` | 512 | Media, CLS y SEP |
| MPNet | `sentence-transformers/all-mpnet-base-v2` | 384 | Media |
| MiniLM | `sentence-transformers/all-MiniLM-L6-v2` | 256 | Media |
| PubMedBERT/BiomedBERT | `microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext` | 512 | Media, CLS y SEP |
| BioBERT | `dmis-lab/biobert-v1.1` | 512 | Media, CLS y SEP |
| SimCSE | `princeton-nlp/unsup-simcse-bert-base-uncased` | 512 | CLS antes de la capa de ajuste |

**CLS** es la representación del marcador inicial. **SEP** es la del marcador final real, nunca la de una posición vacía usada para igualar longitudes. **Media** promedia las representaciones de la última capa de las posiciones leídas, incluidos los marcadores y excluido el relleno. Los cuatro modelos de palabras conservan las tres sin repetir la parte costosa. La receta principal de su análisis aún debe acordarse, antes de mirar los resultados científicos. Guardarlas no las convierte en 18 modelos independientes.

SPECTER, SPECTER2 y SciNCL reciben título + separador del modelo + abstract, siguiendo sus ejemplos oficiales. Los demás reciben título + dos saltos de línea + abstract. No se traduce, reescribe ni completa texto. BioBERT conserva mayúsculas según su propio tokenizador. El límite de uso de MiniLM es 256 aunque su arquitectura admita 512; no se amplía en silencio.

Se conservan vectores **sin normalizar, en float32**, para mantener toda la información original. Normalizar después es reversible si se conservan estos originales. Para reproducir la salida habitual normalizada de MPNet/MiniLM se divide cada vector por su longitud. Esta elección de almacenamiento no decide todavía cómo se calcularán distancias u otras medidas.

Las 22.118 coincidencias con vectores SPECTER2 antiguos se recalcularán: su revisión exacta sigue sin identificarse y mezclarla con la nueva impediría saber si una diferencia viene del modelo o de la versión. El proyecto antiguo sigue en lectura.

## Comprobación con exactamente el mismo fragmento

Aceptada por el usuario como complemento del uso habitual. La prueba técnica toma los mismos 1.300 artículos y conserva, para todos los modelos, el mismo título y el mismo comienzo del abstract que cabe en todos. Solo se recortan extremos; se conservan caracteres originales y finales de palabras. Si un título no cupiera, la regla recortaría también su extremo, por igual para todos.

Cada modelo mantiene sus separadores propios. «Texto idéntico» significa las mismas porciones de título y abstract; los marcadores y la división en piezas siguen siendo propios del modelo. Se verifica que ninguno vuelve a recortar el fragmento. Se conserva también la huella del texto original.

Esta muestra de 1.300 es una **prueba de funcionamiento**, no una justificación del tamaño de un análisis científico definitivo. El tamaño final del control y las medidas de comparación quedan pendientes. El comando completo de arriba calcula la entrada habitual sobre los 500.000; no decide esas cuestiones por su cuenta.

Para reproducir las pruebas pequeñas:

```sh
./embed.sh run --scope pilot
./embed.sh run --scope control
```

## Espacio y continuidad

Los vectores completos ocuparán aproximadamente **25 GiB** (26,9 GB), más los índices y registros. Reservar **35 GB libres** para resultados da margen. La memoria no necesita contener todos los artículos ni los diez modelos a la vez. No se construye una tabla de todas las parejas de artículos.

No editar `sos_embed/`, las dependencias ni la configuración durante una ejecución. Al reanudar, el programa rechaza cambios de modelo, entrada, programa, entorno o forma de cálculo para evitar mezclas. No borrar corpus, pesos o bloques completados. Los directorios `.partial-*` son restos de un bloque interrumpido y nunca cuentan como trabajo terminado.

Si hubiera que reconstruir el entorno, están fijadas las versiones:

```sh
uv venv --python 3.12 .venv-embed
uv pip install --python .venv-embed/bin/python -r requirements-embeddings.txt
./embed.sh download
./embed.sh preflight
```

Un entorno nuevo que difiera del usado en bloques existentes requiere revisar la compatibilidad; no se fuerza la reanudación. La instalación ya está hecha en este Mac.

## Fuentes de las recetas

[SPECTER](https://github.com/allenai/SPECTER) documenta separador, CLS y las diferencias entre su versión de Hugging Face y otras salidas. Aquí se fija únicamente la de Hugging Face. [SPECTER2](https://github.com/allenai/SPECTER2) distingue la base, el adaptador de proximidad y la variante de actualización; se usa la combinación de referencia. [SciNCL](https://huggingface.co/malteos/scincl) da su preparación para artículos.

[MPNet](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) y [MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) documentan media y normalización; sus archivos `sentence_bert_config.json` fijan 384 y 256. [SimCSE](https://github.com/princeton-nlp/SimCSE#evaluation) pide explícitamente CLS antes de la capa de ajuste en la variante no supervisada.

[Landscape 2024](https://doi.org/10.1016/j.patter.2024.100968) compara media, CLS y SEP y usa SEP para su mapa con PubMedBERT. Aquí no se presupone que una receta elegida en biomedicina sea la mejor para las 26 áreas; se conservan las tres. El nombre actual de [PubMedBERT/BiomedBERT](https://huggingface.co/microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext) procede de su ficha oficial. Los antecedentes de adopción y sus límites están en `ACADEMIC_MODEL_USAGE.md`.
