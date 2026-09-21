## Versión definitiva aprobada, 21-09-2026

El autor declara definitiva la versión actual y pide cerrar la entrega para QSS y arXiv. Inglés oficial para envío y cita; español como traducción profesional final. Afiliación solicitada: University College London, London, United Kingdom, sin inventar departamento, correo ni cargo. Esta aprobación sustituye las notas históricas de revisión personal pendiente.

Se retiran marcas de borrador de portadas, cabeceras y metadatos; se completan CRediT, declaraciones y disponibilidad del DOI público 10.5281/zenodo.22876602. Las declaraciones de herramientas se retiran después por instrucción del autor; el requisito editorial correspondiente queda sin cubrir y se comunica en el chat. Se mantienen voz, cuerpo científico, resultados y datos congelados.

Fuentes arXiv en `output/arxiv_source.zip`; PDF oficiales en `output/pdf/`, traducción en `output/pdf/es/`. Carta y copias para endorsement fuera del repositorio, en la carpeta local hermana `Shape of Science Submission/2026-09-21`. Guía vigente: `docs/SUBMISSION_READY.md`. No se han enviado solicitudes de endorsement ni realizado el envío a QSS o arXiv. No archivar el repositorio en modo de solo lectura: conservarlo disponible para las revisiones editoriales.

**Entrega vigente, 21-09-2026:** distribución compacta v1.1.0 publicada y comprobada: 15 archivos, 492.154.568 bytes. [GitHub](https://github.com/aleetreny/Shape-of-Science-Reproducibility/releases/tag/v1.1.0) y [archivo con DOI](https://doi.org/10.5281/zenodo.22876602). Sustituye la carga de 51 GB. Se conservan medidas, recuentos, identidades, selecciones y controles; se excluyen grandes cachés de vectores/listas, textos históricos, artículo, suplementos y notas internas. Reproducción estadística comprobada desde los ZIP en macOS y en un entorno Linux nuevo: 25 tablas, 106.445 filas idénticas y 17.550 medidas de vecinos coincidentes. No se certifica regeneración desde textos históricos ni todos los análisis suplementarios. El borrador antiguo 22863543 permanece sin publicar; el cargador local está retirado. No queda una subida a cargo del autor. Detalles: [COMPACT_REPRODUCIBILITY.md](COMPACT_REPRODUCIBILITY.md).

El contenido siguiente documenta las entregas anteriores y sus cifras históricas.

# Novedad y entrega reproducible, 20-09-2026

**Paquete vigente, 21-09-2026:** el autor pide excluir artículo y suplementos de ambos idiomas. La carpeta de subida sigue teniendo 32 archivos y ahora ocupa 51,19 GB. El ZIP es `shape-of-science-code-v1.0.0-data-only.zip`: distribución científica filtrada del commit `cc61517`, con documentación actualizada y manifiesto de contenido. No incluye borradores, fuentes editoriales, versiones anteriores ni registros internos. Los 19 ZIP numéricos no cambian. [Guía exacta](ZENODO_UPLOAD.md). Los PDF enlazados a continuación permanecen en el proyecto y fuera del paquete de Zenodo.

Los recuentos y el ZIP de la entrega del 20-09 que siguen se conservan como historial; quedan sustituidos para la carga por esta revisión.

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
