# Auditoría final del corpus — 15-09-2026

> Informe de la **descarga original**. Después, el usuario autorizó limpiar y completar una copia aparte. El resultado actualizado está en [CLEANING.md](CLEANING.md). Las 166 alertas de contenido de este informe fueron un primer hallazgo; la revisión posterior amplió esa lista.

**La descarga ha terminado y se ha guardado correctamente. Los datos sirven como base del estudio, pero necesitan una limpieza adicional antes de calcular los embeddings.**

## Qué tenemos

| Comprobación | Resultado |
| --- | --- |
| Trabajos distintos | **500.000 IDs únicos**: 400.000 base general + 100.000 complemento. |
| Cobertura | **26 Fields y 130 combinaciones de área/período**, con los años exactos guardados. También hay 252 Subfields y 4.477 temas principales distintos. |
| Tamaño mínimo por área/período | **2.163 trabajos**. El reparto coincide con la regla acordada; no se agotó ninguna celda. |
| Descarga original | **6.138 páginas, 613.800 candidatos recibidos**. Terminó a las 12:30:35 UTC, unas 2 h 17 min después de arrancar. |
| Guardado y selección | Comprobados todos los archivos de páginas, todos los trabajos seleccionados y las 500.000 filas de la tabla final. Sin discrepancias. |
| Reutilización | 27.562 IDs coinciden con el TFM; **22.118 también conservan exactamente título y abstract**. |

La revisión reprodujo la selección con las semillas y el orden guardados, comprobó los descartes y calculó el reparto con otra implementación. También contrastó cada fila final con la respuesta original de OpenAlex. Los 22 fallos temporales registrados se recuperaron: 17 de conexión y cinco respuestas HTTP 504.

Recuento completo por área: [field_summary.csv](research/corpus_audit_2026-09-15/field_summary.csv). [Mapa de área y período](research/corpus_audit_2026-09-15/field_period_coverage.png).

## Qué falta limpiar o resolver

| Hallazgo | Alcance y límite |
| --- | --- |
| Posible idioma distinto del inglés | **8.544 abstracts señalados (1,71 %)** por un detector adicional. 5.122 tienen puntuación ≥0,9; eso no es una probabilidad garantizada de acierto ni un umbral de descarte aprobado. Se confirmaron ejemplos en coreano, español, ruso y otros idiomas leyendo el texto. |
| Contenido ajeno al resumen | **166 registros señalados** por mensajes de error DOI, descripciones de revistas, bibliotecas o catálogos. Son familias observadas; no se afirma haber encontrado todos los errores posibles. |
| Posibles avisos de retirada o corrección | **12 títulos** requieren comprobar el tipo real de documento. No se han eliminado automáticamente. |
| IDs distintos con texto idéntico | **80 grupos, 173 registros** comparten exactamente título y abstract. Hay además siete grupos de DOI repetido, con 18 registros. Las listas pueden solaparse: no sumar sus cantidades como descartes. |
| Abstracts entre 50 y 79 palabras | **43.482**. Cumplen la regla aprobada; se mantienen marcados para la comprobación futura con ≥80. |
| Abstracts muy largos | **246 superan 2.000 palabras**. Pueden incluir más contenido que el resumen; longitud por sí sola no justifica borrarlos. |

El idioma no afecta a todas las áreas por igual: el detector señala un 5,20 % en Artes y Humanidades y un 4,37 % en Ciencias Sociales, frente al 1,21 % en Medicina. Son alertas, no tasas de error confirmadas. **No basta con decir que los casos problemáticos son pocos en el total.**

OpenAlex explica que el idioma se estima automáticamente sobre metadatos y que algunos abstracts pueden incluir texto adicional de las páginas de origen. [Referencia oficial](https://help.openalex.org/data/works/attributes/). La comprobación adicional usa el modelo oficial fastText lid.176, identificado mediante su huella; sus puntuaciones se usan como diagnóstico. [Documentación del modelo](https://fasttext.cc/docs/en/language-identification.html).

## Cómo aprovechar lo que ya está descargado

- Hay **6.531 candidatos globales adicionales** del último bloque de la base, válidos según los filtros actuales y no incluidos en sus 400.000. 6.419 tienen primera etiqueta de idioma inglés. Son posibles reservas; no se han elegido como reemplazos.
- Los **22.118 vectores antiguos candidatos** están localizados en sus 119 archivos. Todos los vectores correspondientes son finitos, no nulos y tienen IDs alineados con sus metadatos. Falta resolver la versión exacta del modelo y su entrada antes de usarlos en el paper. No se copiaron ni recalcularon vectores.
- Si se aprueba excluir trabajos, hay que completar primero la base aleatoria global y después recalcular el complemento. No rellenar la base por área ni añadir el corpus antiguo por conveniencia.

## Dónde continuar

**Recomendación: acordar una limpieza común y completar los huecos antes de elegir y ejecutar los modelos.** Opciones y material preparado en [NEXT_STEPS.md](NEXT_STEPS.md). Esa decisión sigue pendiente; el corpus original se conserva íntegro.

- Tabla original: `data/corpus_500k/corpus.parquet`.
- Evidencia técnica: [final_validation.json](research/corpus_audit_2026-09-15/final_validation.json).
- Huellas de la tabla y del orden de IDs/textos: [corpus_manifest.json](research/corpus_audit_2026-09-15/corpus_manifest.json).
- Listas de revisión, idiomas, duplicados, reservas y vectores localizados: `research/corpus_audit_2026-09-15/`.
- Scripts reproducibles de auditoría: `scripts/audit_corpus.py`, `audit_language.py`, `audit_content_flags.py`, `audit_legacy_embeddings.py` y `audit_figures.py`.

El paso de guardar y comprobar la descarga está cerrado. Esto no demuestra por sí solo la calidad de todos los metadatos, la ausencia de versiones duplicadas o la estabilidad de las futuras conclusiones científicas.
