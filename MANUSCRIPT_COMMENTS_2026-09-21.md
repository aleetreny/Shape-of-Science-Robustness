# Cinco comentarios del autor aplicados

**21-09-2026.** Revisión del artículo en español y del inglés canónico. Se conserva el título y la voz elegida. Los cambios explican decisiones y resultados ya existentes; no añaden experimentos.

## Qué se ha aclarado

| Comentario | Cambio |
| --- | --- |
| 1. Ángulos y punto de referencia en el resumen | Se explica que la medida compara ángulos entre líneas trazadas desde un mismo punto hasta las posiciones de los artículos. Cambiar ese punto puede invertir cuál disciplina parece más dispersa, aunque elegir otros artículos conserve la respuesta. |
| 2. Primera prueba y ampliación de la muestra | «Una primera prueba». Se añade que ampliar de 26.000 a 52.000 permite comprobar cómo cambian las medidas de acuerdo y su sensibilidad a la elección de artículos. |
| 3. Elección de modelos | Se explicita la prioridad dada a los modelos más utilizados en los estudios de mapas de la ciencia revisados, con SPECTER y SciBERT como ejemplos. El conjunto incluye también modelos usados como comparación en esos trabajos. Se añaden citas a antecedentes ya presentes en la bibliografía. |
| 4. MiniLM con 512 tokens | Se explica que MiniLM recorta parte del texto de casi la mitad de los artículos. La prueba permite ver si leer más texto cambia su acuerdo con los demás modelos; la configuración habitual permanece en la comparación principal. |
| 5. Artículo indefinido en la tabla | «Incluye una primera prueba de 26.000». Se actualiza tanto la fuente editorial como la tabla compilada, en ambos idiomas. |

La redacción española del pasaje del resumen queda así:

> Una de las medidas de dispersión compara los ángulos entre líneas trazadas desde un mismo punto hasta la posición de cada artículo. Cambiar ese punto puede invertir qué disciplina parece más dispersa, aunque el resultado se mantenga al elegir otros artículos.

El criterio de elección se apoya en [la revisión de antecedentes](ACADEMIC_MODEL_USAGE.md) y [la selección documentada](MODEL_SELECTION.md). «Más utilizados» se refiere a los estudios revisados: esa búsqueda dirigida no permite afirmar que los diez sean los más usados de toda la literatura. La inversión de comparaciones al cambiar el origen está documentada en [el cierre de robustez](ROBUSTNESS_CLOSURE_REPORT.md), sin necesidad de recalcular resultados.

## Entrega comprobada

- Artículo español: [PDF de 26 páginas](output/pdf/es/main.pdf), resumen de 214 palabras.
- Artículo inglés: [PDF de 24 páginas](output/pdf/main.pdf), resumen de 196 palabras.
- Fuentes editables actualizadas: [español](output/manuscript_source_es.zip) e [inglés](output/manuscript_source.zip). Ambos paquetes extraídos reconstruyen exactamente sus PDF principal y suplementario.
- Inspección visual de las 50 páginas principales. Sin desbordamientos, caracteres ausentes ni citas pendientes en los registros finales de compilación.
- Cifras científicas y fórmulas conservadas; correspondencia numérica de 82 párrafos entre idiomas. Los dos suplementos conservan exactamente los mismos bytes. En total, 448 archivos protegidos permanecen iguales.

La cita de Liang et al. activa una entrada que ya estaba en los archivos bibliográficos. Se corrige el escape del signo `&` del nombre de la revista para que LaTeX pueda imprimirla; no cambia el contenido de la referencia. Los manifiestos de la Tabla 1 recogen las nuevas huellas de sus fuentes editoriales.

Los **32 archivos de `output/zenodo/` se mantienen sin cambios**. Se han comprobado su listado, tamaño, fecha de modificación e identidad de archivo, y las huellas de los documentos pequeños; no se ha repetido la lectura completa de los 51 GB de archivos congelados. El artículo y los suplementos siguen fuera de ese paquete.

Evidencia de esta edición: [cambios por comentario](research/manuscript_comments_2026-09-21/comment_changes.json), [auditoría de la revisión](research/manuscript_comments_2026-09-21/revision_audit.json), [reconstrucción desde las fuentes](research/manuscript_comments_2026-09-21/portable_source_audit.json) y [revisión visual](research/manuscript_comments_2026-09-21/visual_review.json). Copias anteriores en `research/manuscript_comments_2026-09-21/baseline/`.

Entrega local para revisión del autor. Esta edición no realiza otro commit/push, una carga en Zenodo ni un envío a la revista. La continuación del depósito sigue descrita en [ZENODO_UPLOAD.md](ZENODO_UPLOAD.md).
