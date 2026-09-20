# Manuscrito completo y suplemento

**Edición vigente, 20-09-2026:** [V2 elegida y explicación reescrita](MANUSCRIPT_CLARITY.md). Inglés: 3.989 palabras de cuerpo y resumen de 192, PDF de 19 páginas; español: 20 páginas. Suplementos: 34 y 36. El título, los resultados y las declaraciones se conservan. Las cifras de extensión y páginas que siguen pertenecen al registro histórico del 18-09; las rutas estables de PDF ahora abren la edición vigente.

## Registro histórico de esta revisión

**Actualización posterior:** [cinco comentarios del autor resueltos](MANUSCRIPT_COMMENTS.md), con las dos versiones sincronizadas. La evidencia nueva está en `research/manuscript_comments_2026-09-18/`; los cierres citados más abajo describen la entrega anterior.

**18-09-2026.** Borrador completo, revisado en contenido, voz y presentación. El cuerpo tiene **4.383 palabras** y el resumen **190**. Son **19 páginas principales**, incluidas las referencias y figuras, y **33 de suplemento**. No se ha alargado hasta el presupuesto original de 6.750 palabras.

| Abrir | Contenido |
| --- | --- |
| [Artículo renderizado](output/pdf/main.pdf) | Seis secciones completas, dos tablas y cuatro figuras principales. |
| [Suplemento renderizado](output/pdf/supplement.pdf) | Métodos, controles, casos, 17 grupos de tablas y diez figuras. |
| [Paquete editable](output/manuscript_source.zip) | LaTeX, bibliografía, figuras y 98 adjuntos CSV; comprobado desde una copia extraída. |
| [Guía de uso](manuscript/README.md) | Comando, archivos y límites de reproducción. |
| [Revisión y decisiones editoriales](MANUSCRIPT_REVIEW.md) | Evidencia, cambios visuales, cifras y punto de continuación. |

La historia central distingue repetir una comparación con otros artículos de repetirla con otro modelo. Los detalles largos van al suplemento. Se mantienen todas las alertas, las magnitudes pequeñas, los errores de etiquetas y el carácter exploratorio de las ampliaciones.

Autor: Alejandro Treny Ortega, investigador independiente. Financiación externa y conflictos: ninguno, confirmado por el autor. La ayuda de Codex está declarada. La lectura y aprobación personal del texto siguen pendientes.

El formato es propio, preparado para una primera entrega flexible, **no una plantilla oficial de QSS**. Las normas se consultaron mediante un índice antiguo y deben comprobarse antes del envío. No se ha elegido licencia, depositado datos, hecho otra subida ni enviado el trabajo.

Compilar desde la raíz:

```sh
./manuscript/build.sh
```

No ejecuta modelos ni experimentos. Fuente: [main.tex](manuscript/main.tex) y [supplement.tex](manuscript/supplement.tex). Figuras en PDF/SVG y PNG/TIFF a 300 dpi; tablas completas acompañadas de resúmenes legibles. Los 150 archivos de resultados previos y la biblioteca canónica permanecen intactos. Auditoría de la redacción inicial: [research/manuscript_full_2026-09-18](research/manuscript_full_2026-09-18/). Revisión vigente: [MANUSCRIPT_COMMENTS.md](MANUSCRIPT_COMMENTS.md). Los cierres anteriores conservan su estado histórico.
