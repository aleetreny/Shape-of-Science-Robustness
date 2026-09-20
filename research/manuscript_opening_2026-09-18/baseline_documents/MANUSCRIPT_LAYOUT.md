# Maqueta del artículo y suplemento

18-09-2026. Ya están generadas las tablas, las figuras y la estructura editable en LaTeX. El texto pendiente aparece como **Writing plan**. Los resultados son reales; el artículo completo todavía no está redactado.

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

Siguiente paso: redactar métodos y resultados cuando se solicite, siguiendo [el plano](MANUSCRIPT_BLUEPRINT.md) y [la voz del autor](AUTHOR_VOICE.md). Autoría, afiliaciones, declaraciones, licencia y depósito siguen pendientes. No se ha hecho otro commit/push ni enviado el trabajo.

Trazabilidad: [tablas](manuscript/tables/manifest.json), [figuras](manuscript/figures/manifest.json) y [auditoría de esta entrega](research/manuscript_layout_2026-09-18/). Los PDF y sus datos son una presentación nueva de salidas existentes, no otra versión científica del estudio.
