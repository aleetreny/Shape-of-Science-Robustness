# Novedad y entrega reproducible, 20-09-2026

Los tres párrafos propuestos ya están integrados en el artículo, en inglés y español. [GitHub está actualizado y comprobado](https://github.com/aleetreny/Shape-of-Science-Robustness/commit/cc61517dc2ea1e946c4fe391c4fcc80fa6e4819f). La versión de código archivada es `cc61517`; el paquete de Zenodo contiene **32 archivos y 51,41 GB**, incluido su ZIP de código. El depósito de Zenodo sigue siendo un **borrador sin archivos subidos**; el DOI reservado aún no acredita acceso público.

## Artículo actualizado

- [Inglés, 24 páginas](output/pdf/main.pdf) y [español, 25 páginas](output/pdf/es/main.pdf).
- [Fuentes inglesas](output/manuscript_source.zip) y [españolas](output/manuscript_source_es.zip).
- La introducción presenta la aportación; los antecedentes precisan la diferencia frente a trabajos próximos; la discusión explica su utilidad para quien interpreta un mapa.
- El argumento distingue una puntuación media de acuerdo de una comparación concreta que se mantiene o cambia de dirección. También separa cambiar artículos, cambiar modelos y cambiar el procesamiento de los vectores. No se afirma prioridad absoluta ni que el consenso demuestre una verdad temática.

Cifras, resumen, título y 522 archivos protegidos permanecen iguales. Se han revisado las 49 páginas de los dos artículos. Los paquetes editables reconstruyen exactamente los cuatro PDF, incluidos los suplementos conservados.

## Material preparado y comprobado

Hay **19 ZIP de datos: 51.143.981.543 bytes (51,14 GB), con 58.201 archivos**. Incluyen vectores congelados, identificadores, selecciones exactas, candidatos, resultados por condición y copias de los programas que produjeron cada fase. El código de esta entrega está en `shape-of-science-code-v1.0.0.zip`, preparado para el mismo registro de Zenodo. `CODE_VERSION.json` identifica el commit y su huella.

| Comprobación | Resultado y alcance |
| --- | --- |
| Integridad | Los 19 ZIP y sus 58.201 archivos descomprimidos coinciden con las huellas guardadas. |
| Resúmenes de las cuatro figuras principales | Recalculados desde medidas por condición. La prueba pequeña funciona aislada, sin datos locales adicionales ni acceso a Internet. |
| Cálculos desde vectores | Comprobación independiente con diez modelos: 40 conjuntos de centros, 180 comparaciones de estructura, 60 casos geométricos y 13.500 recuentos exactos de vecinos, además de cinco contrastes de entrada/receta. |
| Archivo de código | El ZIP del commit pasó su prueba de integridad y reproduce los resúmenes al extraer solo sus archivos de comprobación. |
| Precisión | Error numérico máximo de 1,28 × 10⁻¹², por debajo de la tolerancia fijada de 10⁻⁸. Todos los recuentos enteros coinciden. |

La comprobación desde vectores cubre condiciones fijadas de las cuatro figuras. **No es una repetición completa de todas las condiciones y análisis suplementarios.** Tampoco regenera los vectores desde los textos originales. Los ejecutores históricos y sus límites se conservan; el comprobador público es independiente de ellos.

Las tablas históricas con títulos/resúmenes usados como entrada y los pesos de los modelos no se distribuyen. Se conservan identificadores, huellas y metadatos sin esos textos. No se sustituye el corpus por una consulta nueva a OpenAlex.

Guía pública: [reproducibility/README.md](reproducibility/README.md). Detalle: [diccionario](reproducibility/DATA_DICTIONARY.md), [licencias aceptadas](LICENSING.md), [procedencia de terceros](reproducibility/THIRD_PARTY.md). Evidencia: `research/public_release_2026-09-20/`.

## Continuación exacta

Seguir [ZENODO_UPLOAD.md](ZENODO_UPLOAD.md). El borrador ya tiene título, autor, versión, descripción, licencia y 75 GB de espacio. Su DOI reservado es `10.5281/zenodo.22863543`.

El selector del navegador no permitió adjuntar los archivos mediante las herramientas disponibles. Queda arrastrar la carpeta de entrega al formulario, esperar la carga y publicar. Después se debe comprobar el acceso público y actualizar la declaración de disponibilidad y la cita formal del depósito en ambos idiomas. La redacción condicional está preparada en [docs/AVAILABILITY_AFTER_PUBLICATION.md](docs/AVAILABILITY_AFTER_PUBLICATION.md).

No se han iniciado nuevos experimentos ni se ha enviado el artículo a la revista.
