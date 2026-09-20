# Biblioteca verificada

Actualización: 18-09-2026. **54 entradas sin duplicados ni errores de estructura** en [references.bib](references.bib). [index.json](index.json) relaciona cada identificador, fuente y versión elegida. [RELATED_WORK.md](RELATED_WORK.md) explica qué dicen los antecedentes y qué hueco queda.

Se verificaron 45 registros mediante identificadores directos en Crossref/arXiv, más exportaciones editoriales de ACL, NeurIPS y PMLR y el libro oficial ISSI. Las publicaciones sustituyen a sus preprints duplicados en la biblioteca final. El archivo `verified_api.bib` es una salida intermedia; **usar `references.bib` para redactar**.

## Correcciones importantes

- Lamers, van Eck y Colavizza es un trabajo de ISSI 2021, pp. 633–638. No se encontró DOI. `qss_a_00168` pertenece a un estudio sobre Twitter y se excluye. El libro oficial fue leído; no se inventó otro DOI.
- *Document–document similarity approaches and science mapping* (2009) es de **Ahlgren y Colliander**, no de Klavans y Boyack como decía una nota inicial.
- Williams 2021 y Ding 2021 tienen versión publicada en NeurIPS; ReSi está en ICLR 2025. El título editorial de Ding usa **Through**, mientras el preprint usa **with**.
- SciBERT: Crossref devuelve pp. 3613–3618; la edición ACL y su exportación dan **3615–3620**, que se adoptan. SemCSE 2025 se corrige igualmente a **32704–32719** desde la exportación editorial.
- Los DOI que incluyen 2024/2025 no fijan el año del volumen: Bascur es 2025; Liang, 2026. BioBERT tiene publicación anticipada anterior a su volumen de 2020. Conservar ambas fechas en la evidencia cuando sean relevantes.
- Raju: consultada v5 de julio de 2026; Gröger et al.: v2 de junio. SemCSE y SemCSE-Multi son distintos de nuestro SimCSE.
- Kassis et al., [Scientific Agent Skills](https://arxiv.org/abs/2609.00065), v2 vigente: procedencia de las herramientas de búsqueda, no apoyo empírico de la hipótesis.

El validador actual conserva cinco advertencias: páginas ausentes de ReSi y de dos exportaciones de NeurIPS (Self-Tuning y Kleinberg), y DOI ausentes de las exportaciones oficiales de dos artículos JMLR. Se conservaron sus URLs, años, autores y páginas disponibles; no se inventaron identificadores para borrar avisos. No existe todavía un manuscrito contra el que comprobar citas usadas/no usadas.

## Cómo se revisó y qué no significa «verificada»

Metadatos correctos no equivalen a haber evaluado todo el contenido. La profundidad de lectura figura en [RELATED_WORK.md](RELATED_WORK.md). Los modelos se justifican además con sus fichas oficiales y revisiones locales: [MODEL_SELECTION.md](../MODEL_SELECTION.md), [perfiles](../research/checklist_2026-09-17/MODEL_PROFILES.md) y `config/embeddings_v1.json`.

Evidencia: `research/prepaper_2026-09-17/reference_verification.json`, `reference_supplement.json`, `reference_editorial_corrections.json` y `bibliography_validation.json`. Se conservaron respuestas originales, fallos de acceso y versiones. Las copias completas de artículos son material local de consulta, no parte de un paquete para redistribuir.

Es una búsqueda dirigida y fechada, ampliada hacia atrás desde trabajos próximos. No una revisión sistemática exhaustiva. Antes del envío se actualizarán las búsquedas, las versiones y el enlace entre cada afirmación y su fuente.


## Ampliación de morfología, 18-09-2026

Nueve referencias añadidas para distinguir apertura, dimensión efectiva, conexiones y límites de agrupación. Evidencia de lectura y elección en [la revisión del piloto](../research/morphology_2026-09-18/LITERATURE.md); verificación actual en `research/morphology_2026-09-18/bibliography_validation.json`. Se conserva la biblioteca anterior de 45 en `research/morphology_2026-09-18/baseline_documents/references/` y en el commit publicado. Se corrigió el número de artículo 17133 de Erba, páginas 606–610 de Roy y entidades HTML de apellidos JMLR. La referencia de Roy usa la edición de congreso y distingue la copia Zenodo.
## Revisión editorial de QSS, 18-09-2026

La [revisión de estructura](../QSS_STRUCTURE_REVIEW.md) añade una colección de consulta de [34 trabajos](../research/qss_structure_2026-09-18/READING_NOTES.md), con [BibTeX separado](../research/qss_structure_2026-09-18/qss_review.bib). No modifica las 54 entradas canónicas ni implica citar los 34 en el manuscrito. Hay referencias compartidas; deduplicar por DOI al preparar una bibliografía final. La validación de esta colección tiene cero errores y un aviso por volumen ausente de Q34 en Crossref, conservado sin inventar el dato.
