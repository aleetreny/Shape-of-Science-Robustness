## Versión definitiva aprobada, 21-09-2026

El autor declara definitiva la versión actual y pide cerrar la entrega para QSS y arXiv. Inglés oficial para envío y cita; español como traducción profesional final. Afiliación solicitada: University College London, London, United Kingdom, sin inventar departamento, correo ni cargo. Esta aprobación sustituye las notas históricas de revisión personal pendiente.

Se retiran marcas de borrador de portadas, cabeceras y metadatos; se completan CRediT, declaraciones y disponibilidad del DOI público 10.5281/zenodo.22876602. Las declaraciones de herramientas se retiran después por instrucción del autor; el requisito editorial correspondiente queda sin cubrir y se comunica en el chat. Se mantienen voz, cuerpo científico, resultados y datos congelados.

Fuentes arXiv en `output/arxiv_source.zip`; PDF oficiales en `output/pdf/`, traducción en `output/pdf/es/`. Carta y copias para endorsement fuera del repositorio, en la carpeta local hermana `Shape of Science Submission/2026-09-21`. Guía vigente: `docs/SUBMISSION_READY.md`. No se han enviado solicitudes de endorsement ni realizado el envío a QSS o arXiv. No archivar el repositorio en modo de solo lectura: conservarlo disponible para las revisiones editoriales.

## 21-09-2026 — Publicación compacta terminada

**Entrega vigente, 21-09-2026:** distribución compacta v1.1.0 publicada y comprobada: 15 archivos, 492.154.568 bytes. [GitHub](https://github.com/aleetreny/Shape-of-Science-Reproducibility/releases/tag/v1.1.0) y [archivo con DOI](https://doi.org/10.5281/zenodo.22876602). Sustituye la carga de 51 GB. Se conservan medidas, recuentos, identidades, selecciones y controles; se excluyen grandes cachés de vectores/listas, textos históricos, artículo, suplementos y notas internas. Reproducción estadística comprobada desde los ZIP en macOS y en un entorno Linux nuevo: 25 tablas, 106.445 filas idénticas y 17.550 medidas de vecinos coincidentes. No se certifica regeneración desde textos históricos ni todos los análisis suplementarios. El borrador antiguo 22863543 permanece sin publicar; el cargador local está retirado. No queda una subida a cargo del autor. Detalles: [COMPACT_REPRODUCIBILITY.md](COMPACT_REPRODUCIBILITY.md).

Disponibilidad, cita del conjunto de datos y S8 actualizados en ambos idiomas; artículo y suplementos siguen fuera del depósito. Se preservan los archivos científicos congelados y las ediciones previas del autor. La revisión personal y el envío a revista siguen separados de esta entrega. Las notas siguientes conservan la cronología y no reabren la carga antigua.

# Estado actual: cierre final de robustez terminado

**Última entrega, 20-09-2026:** [novedad integrada y material público preparado](PUBLIC_RELEASE.md). Licencias aprobadas y aplicadas; datos numéricos empaquetados y comprobados. Zenodo tiene un borrador con DOI reservado, pero faltan los archivos y su publicación. Seguir [los pasos de carga](ZENODO_UPLOAD.md). Las revisiones editoriales siguientes documentan el historial; los PDF vigentes incorporan los tres párrafos nuevos.

**Revisión vigente para una primera lectura, 20-09-2026:** por petición expresa del autor, se ha releído y revisado el artículo completo para alguien sin contexto. Entrega: [FIRST_READER_REVIEW.md](FIRST_READER_REVIEW.md). Se conserva la voz aceptada; se explican los conceptos, el propósito y los artículos de cada prueba, y el significado de las cifras. Inglés: 6.567 palabras de cuerpo, 195 de resumen y 24 páginas. Español: 7.332, 211 y 25 páginas. Cifras científicas, figuras, bibliografía, declaraciones y suplementos conservados. Las revisiones que siguen son históricas; aprobación personal pendiente.

**20-09-2026.** El autor ha aceptado el tono claro. Las pruebas que delegó están terminadas y se han integrado en los dos idiomas. [Informe sencillo](ROBUSTNESS_CLOSURE_REPORT.md) · [Cambios del texto](ROBUSTNESS_MANUSCRIPT_CHANGELOG.md).

**Revisión editorial más reciente, 20-09-2026:** los 38 comentarios del autor están aplicados en inglés y español; ver [MANUSCRIPT_EXPLANATIONS.md](MANUSCRIPT_EXPLANATIONS.md). Se explican selecciones, candidatos, alertas y casos sin resolver, con ejemplos y porcentajes comprobados. Inglés: 5.412 palabras de cuerpo, 200 de resumen y 21 páginas. Español: 6.090, 240 y 22 páginas. Suplementos intactos (39 y 41 páginas). El apartado de IA se ha retirado del borrador por petición expresa; el registro real de asistencia se conserva y las declaraciones exigidas se comprobarán antes del envío. Título y tono conservados; revisión personal pendiente. Los estados de edición que siguen son históricos.

## Punto exacto para continuar

1. Lectura personal del autor y comentarios al texto. La voz ya está elegida y aceptada; no volver a preguntar por V1/V2/V3. Mantener `AUTHOR_VOICE.md`.
2. Aplicar comentarios en ambos idiomas. Compilar con `./manuscript/build.sh` y `./manuscript_es/build.sh`. Los exportadores conservan las tablas editoriales y añaden los resultados de este cierre.
3. Antes de enviar: correspondencia, aprobación final de texto/contribuciones y revisión actual de normas, referencias y declaraciones exigidas, incluida la asistencia real utilizada. Ver [lista de envío](docs/QSS_CHECK.md).
4. Cargar los archivos de `output/zenodo/` al borrador `22863543`, publicar y comprobar su acceso. Después actualizar disponibilidad, cita de datos y Suplemento S8. Licencias ya confirmadas; no volver a preguntarlas. La [guía de reproducción](reproducibility/README.md) delimita qué comprobaciones se han repetido. El envío a revista sigue pendiente.

No queda otra prueba necesaria dentro del encargo. No reiniciar extracción, embeddings, análisis terminados o automatizaciones. Cualquier ampliación futura debe responder a un problema nuevo concreto.

## Qué queda respaldado y qué hay que matizar

- La organización entre centros se conserva al cambiar artículos, tamaño y omitir cada área. La receta incluye normalizar el centro tras promediar.
- El desacuerdo de vecinos sigue siendo grande tras el filtro conocido de calidad/duplicados. Ese filtro no detecta todo error de origen.
- Texto y modelo producen cambios medios grandes, pero la comparación difiere por modelo y regla de combinación. No hablar de equivalencia ni de un orden universal.
- Apertura: 262 oposiciones originales y 151 tras centrar; 128 conservan los mismos modelos y respuestas. Con mínimo 5 %, 96→11. PR cambia menos: 221→211, con 204 conservadas.
- Las alternativas de dimensión cubren ahora las 26 condiciones; ambas retienen 190/221 oposiciones originales de PR. El 196 de tres condiciones y los controles puntuales 145/262 y 218/221 son históricos, no la comprobación completa actual.
- Persisten 2.628/8.235 alertas locales de especialidades, las 50 originales, cinco de entrada a 52k, cuatro de PR y 51 de conexión, cada una con su diseño y denominador. Una media estable no elimina ninguna.
- Los 500k, diez modelos, restricciones de idioma/abstract y etiquetas OpenAlex delimitan el estudio. Las selecciones solapadas no permiten precisión poblacional; consenso no es verdad temática; familias, Medicina y tiempo no identifican causas.
- Se conservan los errores ilustrativos de OpenAlex y los límites de los conjuntos de candidatos. No borrar ejemplos o cambiar umbrales para mejorar el relato.

## Dónde está cada entrega

| Material | Ubicación |
| --- | --- |
| Informe y cambios del cierre actual | `ROBUSTNESS_CLOSURE_REPORT.md`, `ROBUSTNESS_MANUSCRIPT_CHANGELOG.md` |
| Protocolo, código y configuración sellados | `ROBUSTNESS_CLOSURE_PROTOCOL.md`, `sos_closure/`, `config/robustness_closure_v1.json` |
| Selecciones, centros, búsquedas y huellas locales | `data/robustness_closure_v1/` |
| 25 tablas y resumen del cierre | `reports/robustness_closure_v1/` |
| Auditoría y copias anteriores | `research/robustness_closure_2026-09-20/` |
| Artículo/suplemento; 22 grupos de tablas, 15 figuras | `manuscript/`, `manuscript_es/`, `output/` |
| Resultados científicos anteriores | `ROBUSTNESS_RESULTS.md`, `FIELD_PAIR_RESULTS.md`, `MORPHOLOGY_RESULTS.md`, `CASE_ATLAS.md` |
| Historial de redacción y voz | `MANUSCRIPT_CLARITY.md`, `MANUSCRIPT_VOICES.md` |

Datos grandes y pesos siguen locales y fuera de Git. No modificar una fuente científica congelada y reanudar como si fuera la misma versión. [Reproducción](docs/REPRODUCING.md) · [Catálogo](DATA_CATALOG.md).
