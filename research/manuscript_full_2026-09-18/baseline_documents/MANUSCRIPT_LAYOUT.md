# Maqueta del artículo y suplemento

18-09-2026. Introducción y antecedentes/preguntas ya están redactados como primer borrador: unas 1.000 palabras conjuntas, en las páginas 3–5 del PDF principal. Las demás secciones conservan **Writing plan**. Tablas y figuras contienen resultados reales; el artículo completo todavía no está redactado. El PDF principal tiene ahora 17 páginas; el suplemento mantiene sus 32.

| Abrir | Contenido |
| --- | --- |
| [Artículo renderizado](output/pdf/main.pdf) | Seis secciones, dos tablas y cuatro figuras principales, con sus pies. |
| [Suplemento renderizado](output/pdf/supplement.pdf) | Ocho secciones, 17 grupos de tablas y diez figuras de controles/casos. |
| [Paquete editable](output/manuscript_source.zip) | LaTeX, bibliografía, figuras y tablas; preparado para compilar también en Overleaf. |
| [Guía de uso](manuscript/README.md) | Archivos, comando, formatos y límites. |

Las figuras tienen versión vectorial y archivos PNG/TIFF de 300 dpi. Cada tabla suplementaria incluye su resumen legible y los CSV completos, sin redondear. En total: 14 figuras y 19 grupos de tablas. No se repitieron los experimentos ni se modificaron los informes anteriores.

No se ha localizado una plantilla oficial específica de QSS. Se ha preparado una maqueta propia acorde con la flexibilidad de primera entrega que permite la [guía consultada](https://direct.mit.edu/qss/pages/submission-guidelines). La consulta fue a una versión indexada antigua; las normas se comprobarán otra vez antes de enviar. No se imita el diseño de un artículo ya publicado.

Para regenerar los dos PDF desde la raíz:

```sh
./manuscript/build.sh
```

La primera compilación descarga soporte estándar de LaTeX si hace falta; no descarga papers ni modelos. Los archivos originales están en [main.tex](manuscript/main.tex) y [supplement.tex](manuscript/supplement.tex).

Siguiente paso: revisar los dos bloques con el autor y continuar con las secciones que solicite, siguiendo [el plano](MANUSCRIPT_BLUEPRINT.md) y [la voz del autor](AUTHOR_VOICE.md). [Revisión de la apertura](research/manuscript_opening_2026-09-18/CLAIM_REVIEW.md). Autoría, afiliaciones, declaraciones, licencia y depósito siguen pendientes. No se ha hecho otro commit/push ni enviado el trabajo.

Trazabilidad: [tablas](manuscript/tables/manifest.json), [figuras](manuscript/figures/manifest.json), [auditoría de la maqueta original](research/manuscript_layout_2026-09-18/) y [actualización de la redacción](research/manuscript_opening_2026-09-18/). Las auditorías históricas se conservan; el PDF y ZIP actuales incorporan los nuevos párrafos. No es otra versión científica del estudio.
