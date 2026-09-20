# Formato consultado para la maqueta

18-09-2026. Fuente primaria: [Submission Guidelines, Quantitative Science Studies](https://direct.mit.edu/qss/pages/submission-guidelines). Búsquedas delimitadas a QSS y la guía; los resultados de Open Mind, TACL y otras revistas no se aplicaron a este proyecto.

La versión indexada acepta un PDF/Word integrado con formato flexible para el primer envío, numeración de páginas/secciones y referencias autor-año. Contempla LaTeX para la revisión. No se localizó en lo consultado una clase o plantilla oficial propia de QSS. Esto no prueba que nunca haya existido una plantilla.

Se crea por tanto una maqueta propia basada en `article`, sin logotipo editorial, volumen, DOI, autores ficticios o licencia supuesta. Las tablas son texto seleccionable sin colores. Las figuras van junto a su sección y también en archivos separados. Se prepara la estructura, no un manuscrito completo ni una revisión ya conforme a APA.

Límite de la consulta: el acceso directo falló y el buscador indicó un rastreo de hace unos 1,3 años. La guía debe volver a comprobarse antes del envío. La revisión anterior y los detalles permanecen en `docs/QSS_CHECK.md`.

## Decisiones de presentación

- Dos documentos: cuerpo con dos tablas/cuatro figuras y suplemento con 17 grupos de tablas/diez figuras.
- Resumen legible de cada grupo y CSV completos separados, con su regla de selección registrada.
- Figuras rehechas a partir de las mismas tablas guardadas, con los mismos promedios/medianas descriptivos que las bases visuales anteriores.
- Figura S10: una matriz con dos triángulos en lugar de dos matrices pequeñas; se conservan exactamente las 325 parejas por propiedad.
- Serif de 12 puntos, una columna y estilo autor-año. Interlineado cómodo en la vista; interruptor opcional de doble espacio/números de línea.
- Leyendas y rótulos ingleses. La prosa futura queda marcada como plan, siguiendo el plano y la guía de voz ya aceptados.

## Incidencias de preparación

La primera compilación descargó el soporte estándar de TeX. Detectó anchuras insuficientes en algunos encabezados/modelos y dos comillas Unicode de un título; se ajustó solo la presentación. La inspección de figuras detectó una leyenda temporal recortada y se recolocó. Dos intentos de parche no coincidieron con el texto esperado; no aplicaron cambios y se repitieron sobre el contenido real. Ninguna incidencia cambió resultados científicos.

La inspección de páginas encontró un porcentaje sin escapar en una nota: LaTeX interpretaba el resto de la línea como comentario. Se corrigió el exportador de tablas y se añadió una comprobación que rechaza porcentajes sin escapar y confirma la presencia de la cifra omitida. También se ajustaron los índices a una página y se mantuvieron los encabezados junto al contenido. La revisión final cubre las 46 páginas; el ZIP recompilado produce PDF idénticos. Evidencia separada en `package_audit.json`, `visual_review.json`, `page_geometry.json` y `portable_source_audit.json`.
