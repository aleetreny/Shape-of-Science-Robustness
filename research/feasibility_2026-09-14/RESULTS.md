# Qué se midió para decidir 500.000 papers

14-09-2026. Pruebas autorizadas por el usuario, en el Mac real: M5 Pro, 48 GiB. No son los resultados del futuro paper. Protocolo decidido en [CORPUS_PROTOCOL.md](../../CORPUS_PROTOCOL.md).

## Extracción y limpieza

- **67.202.824 candidatos**: catálogo principal, 2000–2024, artículos/revisiones/congresos en inglés con abstract y Field conocido, sin retractados/paratext. Ver `proposed_population_fields.json` y `proposed_population_field_years.json`; 26 Fields y 650 celdas reconciliadas.
- Se revisaron 700 candidatos con texto: 400 aleatorios generales y 100 adicionales de Veterinaria, Artes e Informática. Solo la selección general estima la aceptación general.
- Pasan título no vacío y abstract ≥50 palabras: **357/400 = 89,25 %** en la prueba general. Con ≥80: 315/400. Son estimaciones exploratorias; no porcentajes exactos del conjunto completo.
- Páginas de 100 trabajos: mediana 0,82 s, rango 0,68–1,25 s. Dos páginas adicionales de una muestra configurada con 10.000 trabajos tardaron 1,07 y 1,28 s, sin IDs repetidos entre ellas. Total de esta fase: **36 consultas API**, de ellas 27 de recuentos y 9 páginas con un máximo de 900 registros descargados para pruebas.
- En los 400 candidatos generales, 4 IDs ya estaban en el corpus local. No suponer que mantener sus 2,38 millones permite evitar la extracción de la nueva muestra.

La proyección para 500.000 válidos es de unas dos horas ideales de peticiones secuenciales al ritmo medido, incluida una pausa de 0,2 s y el descarte observado. El presupuesto práctico reserva 3–6 horas, con posible ampliación por incidencias. No se han medido horas de uso continuo de la API.

## Procesamiento real de textos

| Modelo usado para medir | Textos | Velocidad | Proyección simple para 500.000 |
| --- | ---: | ---: | ---: |
| SciNCL | 512 | 50,53 papers/s | 2,75 horas |
| MPNet | 512 | 64,65 papers/s | 2,15 horas |
| SciNCL, prueba más larga | 15.780 | 50,54 papers/s | 2,75 horas |

GPU MPS, 32 bits, longitudes máximas respectivas 512/384, lotes medidos 8/16/32. Versiones exactas en `benchmark_model_revisions.json`, paquetes en `requirements-benchmark.txt`. Las matrices se comprobaron finitas y de 768 columnas. Son modelos de prueba, no una decisión sobre el conjunto final.

El presupuesto de 3–6 horas por modelo comparable añade margen a la extrapolación. No certifica tiempos de otros modelos más grandes, otras entradas ni condiciones térmicas de muchas horas. Los registros de memoria GPU del ensayo de embeddings son lecturas al final de cada prueba, no una medida exhaustiva del máximo del proceso.

## Comprobación pequeña del tamaño

Se compararon SPECTER2 heredado y SciNCL, sobre los mismos textos/IDs, en cuatro casos. La medida fue CKA lineal con corrección de muestra finita, calculada con HSIC insesgado, sobre vectores normalizados. Su implementación se contrastó con la fórmula de matrices completas en CPU de 64 bits y con GPU en una selección pequeña. Referencia conceptual: [Kornblith et al.](https://proceedings.mlr.press/v97/kornblith19a.html).

Se hicieron 20 selecciones sin reemplazo para cada tamaño: 256, 512, 1.024 y 2.048. Antes del cálculo se fijaron tolerancias de cambio de mediana ≤0,02 entre los dos tamaños mayores y amplitud del rango empírico central del 95 % ≤0,04 para 2.048. No se escogieron según los resultados.

| Área y período | Papers en la base de prueba | Rango central del 95 % a 2.048, amplitud | Criba |
| --- | ---: | ---: | --- |
| Medicina, 2000–2004 | 4.096 | 0,0046 | Pasa |
| Medicina, 2020–2024 | 4.096 | 0,0051 | Pasa |
| Veterinaria, 2000–2004 | 3.588 | 0,0070 | Pasa |
| Veterinaria, 2020–2024 | 4.000 | 0,0056 | Pasa |

Los cambios de mediana entre 1.024 y 2.048 fueron menores de 0,002. **Estos rangos se refieren a las pequeñas bases históricas de prueba**, cuyo muestreo anterior y metadatos de SPECTER2 tienen las limitaciones del inventario. Las selecciones comparten papers y 2.048 supone una fracción grande de esas bases: no interpretar los rangos como intervalos de confianza sobre toda la población. Tampoco se han comprobado los otros 24 Fields ni otros pares de modelos. El resultado apoya el orden de magnitud; no demuestra suficiencia universal.

## Memoria y cálculos posteriores

Se cargaron **500.000 vectores reales** del análisis antiguo en GPU y se buscaron vecinos exactos para 256 consultas, en lotes de 32. Tardó 0,27 s tras calentamiento; máximo observado de memoria asignada por el controlador MPS durante esos lotes: 2,94 GiB. Es una prueba de tiempo sobre las primeras filas, no un muestreo científico ni el estudio completo de vecinos.

Una matriz de 500.000 × 768 en 32 bits ocupa 1,43 GiB. Evitar una tabla completa de todas las distancias, que ocuparía aproximadamente 931 GiB. Trabajar por bloques y definir las consultas necesarias al cerrar las medidas finales. Los tiempos de la prueba no incluyen todos los controles, repeticiones ni comparaciones futuras.

## Archivos y reproducibilidad

Scripts: `probe_openalex.py`, `benchmark_embeddings.py`, `probe_sample_size.py`, `benchmark_analysis.py`. Resultados: JSON del mismo nombre descriptivo; costes comparados en `budget_scenarios.csv`. Las proyecciones por grupo y Field están en `allocation_projection.csv` y `field_allocation_projection.csv`; aún no son cuotas realizadas.

Los textos, respuestas con abstracts, pesos de modelos y vectores de prueba quedan fuera de Git. Mapping-Science se mantuvo en lectura. La prueba de 512 textos se obtuvo por prioridades aleatorias uniformes, semilla 20260914; la prueba por área usa semilla 20260916. Los IDs seleccionados y versiones de modelos se conservan en los resultados.

Las pruebas no prometen aceptación editorial. Como precedente de escala y diseño se consultaron los [métodos abiertos del trabajo de Constantino et al., publicado en QSS](https://arxiv.org/html/2308.15706v2); el acceso editorial directo devolvió 403. No se atribuye a QSS una exigencia de tamaño o una política que no se haya podido verificar.
