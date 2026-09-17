# Registro de la revisión bibliográfica

Consulta: 17-09-2026. Revisión dirigida del proyecto y ampliación desde los antecedentes próximos; no búsqueda sistemática exhaustiva. Este documento resume las familias de consultas y accesos. Los identificadores exactos de las consultas API y sus resultados están en los JSON enlazados; no es una transcripción completa de todas las llamadas del navegador.

## Búsqueda y comprobación

- Partida: biblioteca y revisión anterior del proyecto, conservadas en `baseline_documents/` y `legacy_bibliography_original.md`.
- Familias de búsqueda: mapas de ciencia y comparación de embeddings; geometría/vecinos entre modelos; sensibilidad a título/resumen y recetas; qué temas representan los mapas; estabilidad de representaciones; medidas de similitud 2025–2026; normas oficiales de QSS.
- Seguimiento: títulos, DOI, identificadores arXiv y referencias de los trabajos próximos. Se priorizaron editoriales, actas oficiales y manuscritos de autores.
- [reference_candidates.json](reference_candidates.json), [reference_verification.json](reference_verification.json) y [reference_supplement.json](reference_supplement.json): candidatos y 45 verificaciones por identificador (41 + 4). Las referencias editoriales sustituyen a preprints duplicados; la biblioteca final tiene 45 entradas.
- [editorial_bibtex_downloads.json](editorial_bibtex_downloads.json) y [reference_editorial_corrections.json](reference_editorial_corrections.json): contraste con ACL, NeurIPS, PMLR e ISSI; autores/páginas/versiones corregidos.
- [bibliography_validation.json](bibliography_validation.json): 45 entradas válidas, cero duplicados/errores y una advertencia por páginas no presentes en el registro ICLR de ReSi. Aún no hay manuscrito para auditar sus citas.
- Las respuestas API y exportaciones originales se conservan en `reference_raw/`, solo para consulta local. [RELATED_WORK.md](../../references/RELATED_WORK.md) distingue la profundidad de lectura de cada antecedente.

## Acceso y límites

| Fuente o tarea | Acceso de esta revisión | Consecuencia |
| --- | --- | --- |
| Singh & Singh, Findings ACL 2022 | PDF editorial descargado y apartados de métodos/resultados consultados. | Antecedente directo de entrada y vecinos; no reclamar novedad de esas piezas. |
| SemCSE-Multi, ACL 2026 | PDF editorial descargado; métodos, evaluación, límites y apéndice consultados. | Distinguir aspectos válidos de similitud de acuerdo entre modelos. |
| Bascur 2025 y Schumacher et al. 2026 | Texto editorial mediante navegación; sin copia PDF local nueva. | Profundidad de lectura declarada en la matriz de antecedentes. |
| Ballester & Penner 2022 | Fuente editorial indexada; el PDF de autor falló por certificado TLS. | No se desactivó la comprobación del certificado ni se afirmó lectura del PDF. |
| QSS, submission-guidelines | Acceso directo 403; guía oficial indexada, rastreo anterior. | Revalidar normas antes del envío. No sustituirlas por guías de otras revistas. |
| PMLR, BibTeX | La ruta supuesta `.bib` no existía; se recuperó la exportación del HTML oficial. | Metadatos finales tomados de la fuente editorial comprobada. |
| NeurIPS, exportaciones | El lector web no aceptaba su tipo de respuesta; descarga directa posterior verificada. | No confundir el error del lector con ausencia de publicación. |
| Reconstrucción de la biblioteca | Primera extracción PMLR buscaba `pre`; la página usaba `code`. | Fallo registrado, regla corregida; ejecución final válida en `bibliography_run_corrected.log`. |

Los dos PDF nuevos y sus huellas figuran en `literature_downloads.json`; las copias completas se conservan fuera de Git. El material de lectura no forma parte de un paquete autorizado para distribuir.

## Cierre

La combinación de modelos, entradas, medidas de forma y vecinos tiene antecedentes claros. La contribución propuesta se centra en qué conclusiones sobre organización científica resisten controles emparejados, sus excepciones y casos trazables. Metadatos verificados no implican que todas las fuentes se hayan leído completas. Actualizar búsqueda/versiones antes del envío y comprobar entonces cada cita contra la afirmación exacta del manuscrito.
