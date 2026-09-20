# Cobertura de la revisión editorial de QSS

Fecha: 18-09-2026. Objetivo: estructura y argumentación de artículos empíricos/metodológicos próximos a mapas de ciencia, representaciones de documentos, comparación y validez de medidas, clasificación y calidad de fuentes. No revisión sistemática de efectos ni censo de retórica de la revista.

Marco: todos los registros Crossref del ISSN 2641-3337 publicados hasta esta fecha. 465 esperados y 465 recuperados; dos páginas con cursor. No equivale a 465 artículos leídos: incluye editoriales y otros tipos. Cribado temático de títulos/resúmenes; selección intencional de casos cercanos y controles metodológicos, distribuida por años disponibles. Comprobar también archivo/editorial e índices externos para detectar huecos. Priorizar texto editorial; cuando solo haya manuscrito de autor, identificar versión y no atribuirle maquetación editorial.

Antes de codificar las frecuencias: anotar título, DOI, año, motivo de inclusión, fuente y profundidad real de acceso. En los textos: jerarquía de secciones, papel de antecedentes, orden método/resultado, movimientos de resumen/introducción/discusión, ubicación de controles/límites, ejemplos y disponibilidad. No inferir aprobación de revisores a partir de publicación. No copiar expresiones de autores como prosa propia ni contar menciones bibliográficas como estructura.

Se conservarán búsquedas, selección, notas por artículo y las limitaciones de acceso. Las copias completas de terceros permanecerán solo en data/, fuera de Git. La lectura estructural no es una replicación técnica de cada trabajo. No declarar revisadas todas las páginas/suplementos si no lo están.

Incidencias: Crossref rechaza ordenar published con cursor y DOI como campo de orden; recuperación válida con created. Página oficial directa de QSS devuelve 403; guía leída mediante índice, rastreo antiguo, pendiente revalidación antes del envío.

## Cierre y alcance real de la lectura

Cribado dirigido de metadatos mediante temas de mapas, embeddings, clasificación, consistencia, relatedness, validación, fuentes y calidad; 34 elegidos como casos informativos, no una muestra aleatoria ni una inclusión exhaustiva de cada coincidencia. La selección de títulos y la revisión cualitativa contienen juicio del lector. No se realizó doble codificación independiente ni se estimaron frecuencias poblacionales de estilos.

Se consultaron 33 cuerpos para lectura estructural; once con pasajes adicionales sobre comparación/interpretación/límites. No lectura íntegra de todas sus páginas/suplementos. Un acceso parcial queda excluido de conclusiones estructurales. Versiones y lecciones codificadas manualmente en `curated_notes.json`; el exportador no transforma automáticamente una descarga en lectura. Distribución y huellas en `coverage.json` y `article_matrix.json`.

La respuesta OpenAlex contenía registros duplicados para dos DOI; se trataron como ubicaciones de los mismos artículos. No se contaron como estudios nuevos. Se rechazó el cuerpo ajeno recibido con la ficha de Donner/Henneken. En Q13/Q28 se verificó identidad temática, pero no se certificó versión tipográfica del texto devuelto. Q34 es un preprint anterior con métodos al final; no representa una excepción editorial comprobada. No se usaron como normas las guías de otras revistas devueltas por la búsqueda.

Incidencias de exportación: una clave duplicada en el generador de metadatos se corrigió antes de crear la entrega; el primer reemplazo de PAPER_OUTLINE no fue aplicado porque el editor rechazó dos operaciones sobre la misma ruta. Se escribió el archivo completo después, conservando su copia anterior. Sin efecto en resultados científicos. Un aviso bibliográfico por volumen ausente de Q34 se conserva sin inventar metadatos.
