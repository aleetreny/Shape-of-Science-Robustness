# Pruebas de preparación de los diez modelos

Verificado el 2026-09-15 17:08 UTC. **El cálculo completo no está iniciado.** El usuario lo arrancará con `./start_embeddings.sh`.

## Tiempo previsto

**Reservar 25–35 horas para los diez modelos y los 500.000 artículos.** La extrapolación directa de la prueba da 24.14 horas. El margen es de planificación, no un intervalo estadístico: la prueba es corta, reparte igual entre áreas/períodos y no mide un día entero de temperatura, ahorro energético o uso simultáneo del Mac.

Se midió el programa real, con MPS (aceleración del chip Apple), float32, grupos de 16 y bloques de 1.024. Cada modelo procesó los mismos 1.300 artículos; se excluyeron su carga inicial y ocho artículos de calentamiento. Se incluyen preparación de texto, división en piezas, inferencia, obtención de salidas y copia de los resultados a memoria. La escritura y validación de archivos añaden tiempo fuera de esta medida.

| Modelo | Artículos/s medidos | Horas extrapoladas para 500.000 | Textos recortados en la prueba |
| --- | ---: | ---: | ---: |
| SPECTER | 52.9 | 2.63 | 64/1.300 (4.9 %) |
| SPECTER2 | 50.1 | 2.77 | 55/1.300 (4.2 %) |
| SciNCL | 53.3 | 2.60 | 55/1.300 (4.2 %) |
| SciBERT | 53.3 | 2.61 | 55/1.300 (4.2 %) |
| BERT | 52.4 | 2.65 | 75/1.300 (5.8 %) |
| MPNet | 65.0 | 2.14 | 235/1.300 (18.1 %) |
| MiniLM | 394.6 | 0.35 | 622/1.300 (47.8 %) |
| PubMedBERT / BiomedBERT | 51.3 | 2.70 | 53/1.300 (4.1 %) |
| BioBERT | 46.7 | 2.97 | 94/1.300 (7.2 %) |
| SimCSE | 51.3 | 2.71 | 75/1.300 (5.8 %) |

Estos porcentajes describen la prueba técnica, no los 500.000 artículos. Las cifras finales de recorte quedarán guardadas por artículo durante el cálculo completo. La normalización y las comparaciones científicas posteriores no están incluidas en las horas estimadas.

## Qué se comprobó

- Diez revisiones oficiales fijadas, con base y adaptador separados para SPECTER2. Once repositorios verificados contra sus identificadores publicados; pesos y archivos pequeños completos. Copia compartible de las huellas: `assets_manifest.json`.
- Los diez modelos cargan sin parámetros faltantes. Los avisos por cabezas de preentrenamiento no utilizadas quedan en los registros; no se usa una cabeza aleatoria para obtener el vector.
- Primera comprobación con ocho artículos/modelo: resultados finitos y coherentes al cambiar el tamaño de los grupos de 8 a 2. `model_smoke.json`.
- Prueba nativa: 1.300 filas/modelo, sin duplicar IDs, 26 áreas y 130 combinaciones área/período. Cada variante conserva dimensiones correctas y valores finitos no nulos.
- Parada real de SPECTER después de un bloque: al continuar se conservan exactamente las huellas de los tres archivos del bloque completado. `before_resume_hashes.json`, `pilot_pause.log`, `pilot_run.log`.
- Diecisiete pruebas automáticas: orden e identidad, cambio de receta/entrada, corrupción, bloques parciales, cierre brusco de proceso, exclusión mutua, formas de resumir vectores, fragmento común y lanzador de terminal. `tests_all.txt`.
- El lanzador se probó con un comando de sustitución mínimo en una carpeta temporal: conserva salida y errores y devuelve el fallo verdadero. **No se lanzó el cálculo completo para probarlo.**
- Control técnico: 1.300 artículos/modelo con las mismas porciones originales de título/abstract. Hubo 622 recortes de abstract y ningún título recortado. Ningún modelo volvió a truncar esos fragmentos.
- Para los 678 artículos cuyo texto no cambia, las salidas nativas y de control coinciden dentro de la tolerancia numérica fijada (absoluta 0,0002; relativa 0,0001). No es un umbral de estabilidad científica.
- Auditoría adicional independiente de los archivos, sus huellas y sus vínculos con la entrada: `verify_setup.py` y `verification.json`. Las huellas del corpus original y de la entrada congelada siguen coincidiendo.
- Cálculo completo ausente: `full_not_started.json`; no hay bloques completos en `data/embeddings_v1/`.

## Espacio y memoria

Las salidas numéricas completas ocupan 26,880,000,000 bytes: 25.03 GiB, más índices y registros. Son 18 salidas guardadas de diez modelos, porque cuatro modelos conservan tres formas de resumir el texto. No se repite la parte costosa para producirlas. Se recomienda reservar 35 GB libres.

La ejecución carga un modelo cada vez. Las medidas de memoria del proceso y del controlador gráfico están separadas en `verification.json`; pueden solaparse en memoria unificada y no deben sumarse como un pico exacto. No se construyen matrices de todas las parejas de 500.000 artículos.

## Lo que esta prueba no decide

- No demuestra estabilidad científica ni que 1.300 artículos sean suficientes para el control definitivo. Son diez por celda solo para comprobar cobertura/funcionamiento.
- No selecciona métricas, normalización, receta principal de BERT/SciBERT/PubMedBERT/BioBERT ni umbrales mirando resultados de mapas.
- No demuestra uso mayoritario mundial ni diez familias independientes. Los antecedentes y sus límites están en `../../ACADEMIC_MODEL_USAGE.md`.
- No inicia la extracción de más artículos ni cambia los 500.000 ya preparados. El manifiesto de limpieza mantiene su estado histórico; los cálculos posteriores se registran aparte.

## Continuación

El usuario ejecuta `./start_embeddings.sh` desde el repositorio. La guía completa está en `../../EMBEDDINGS.md`. Antes de analizar la salida final: `./embed.sh verify --scope full`. Después deben cerrarse las decisiones científicas pendientes registradas en `../../DECISIONS.md`.
