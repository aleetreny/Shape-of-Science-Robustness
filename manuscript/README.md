# Manuscrito completo y suplemento: borrador para revisión

**Revisión vigente para una primera lectura, 20-09-2026:** por petición expresa del autor, se ha releído y revisado el artículo completo para alguien sin contexto. Entrega: [FIRST_READER_REVIEW.md](../FIRST_READER_REVIEW.md). Se conserva la voz aceptada; se explican los conceptos, el propósito y los artículos de cada prueba, y el significado de las cifras. Inglés: 6.567 palabras de cuerpo, 195 de resumen y 24 páginas. Español: 7.332, 211 y 25 páginas. Cifras científicas, figuras, bibliografía, declaraciones y suplementos conservados. Las revisiones que siguen son históricas; aprobación personal pendiente.

**Edición anterior, 20-09-2026:** [38 comentarios aclarados](../MANUSCRIPT_EXPLANATIONS.md), con ejemplos, porcentajes y Tabla 1 reorganizada. El apartado de IA se retira del borrador por petición del autor; la historia real de asistencia queda conservada y las declaraciones exigidas se revisarán antes del envío.

**Cierre posterior del 20-09-2026:** pruebas finales integradas; [informe](../ROBUSTNESS_CLOSURE_REPORT.md) y [cambios](../ROBUSTNESS_MANUSCRIPT_CHANGELOG.md). Se conserva el tono claro aceptado. Dos tablas y cuatro figuras principales; veinte grupos de tablas y once figuras suplementarias. Los manifiestos de presentación identifican los CSV usados actualmente; otros CSV conservados documentan la procedencia histórica. Revisión personal del autor pendiente.

**Edición del 20-09-2026.** El autor elige V2 y solicita una explicación mucho más clara. La nueva redacción introduce los conceptos antes de usarlos y explica la finalidad de cada muestra. El suplemento incorpora una guía de lectura. [Cambios y comprobaciones](../MANUSCRIPT_CLARITY.md).

Título vigente: **How much does the map of science depend on the embedding model?** Los cinco comentarios del autor del 18-09-2026 están aplicados en ambas versiones. Detalles y comprobaciones en [MANUSCRIPT_COMMENTS.md](../MANUSCRIPT_COMMENTS.md).

El texto científico está completo y revisado: introducción, antecedentes, métodos, resultados, discusión, conclusión y resumen. El cuerpo tiene **6.567 palabras**, sin tablas, pies, citas expandidas ni declaraciones; el resumen, **195**. Principal: 24 páginas, incluidas figuras y referencias. Suplemento: 39 páginas. La revisión de primera lectura explica pasos que antes quedaban implícitos; el registro está en [FIRST_READER_REVIEW.md](../FIRST_READER_REVIEW.md).

Autor confirmado: **Alejandro Treny Ortega**, **Independent researcher**. Ha declarado que no hay financiación externa ni conflictos de interés. El historial real de asistencia se conserva en el proyecto. El texto sigue siendo un borrador pendiente de lectura y aprobación del autor; no está enviado a la revista.

## Abrir y compilar

- Principal: `../output/pdf/main.pdf`; fuente editable: [main.tex](main.tex).
- Suplemento: `../output/pdf/supplement.pdf`; fuente editable: [supplement.tex](supplement.tex).
- Formato compartido: [preamble.tex](preamble.tex).

Desde la raíz del repositorio:

```sh
./manuscript/build.sh
```

Compila los dos documentos con Tectonic. No descarga artículos, calcula embeddings ni repite experimentos. La primera compilación puede descargar archivos habituales de LaTeX; después se reutilizan. En este ordenador se ha preparado Tectonic 0.17.0 en una carpeta local excluida de Git. En otro equipo puede usarse Tectonic instalado o compilar en Overleaf con XeLaTeX y BibTeX, eligiendo `main.tex` o `supplement.tex` como documento principal.

El paquete `../output/manuscript_source.zip` contiene las fuentes, imágenes, tablas y CSV necesarios para abrir esta maqueta en Overleaf. El directorio de registro/auditoría y los programas científicos se mantienen en el repositorio. No es un depósito público de datos.

## Qué contiene

| Documento | Tablas | Figuras |
| --- | ---: | ---: |
| Principal | 2 | 4 |
| Suplemento | 20 grupos | 11 |

Cada tabla suplementaria tiene una versión legible en el PDF y sus CSV completos, sin redondear, en `tables/data/S01/` a `S20/`. La numeración no oculta miles de filas tras puntos suspensivos: los resúmenes indican su selección y los archivos completos los acompañan. [Registro de tablas](tables/manifest.json).

Todas las figuras se entregan en PDF vectorial, SVG editable y PNG/TIFF a 300 dpi. Son copias de presentación, con rótulos ingleses y tamaño de página uniforme. Sus valores dibujados y fuentes se registran en [el manifiesto de figuras](figures/manifest.json). Los datos originales no se movieron ni editaron. La Figura S10 reúne apertura y dimensión en los dos triángulos de una matriz para que las 650 clasificaciones se puedan leer a tamaño de artículo.

## Formato de QSS

No se ha localizado una clase LaTeX oficial específica en la búsqueda realizada. La [guía de QSS consultada](https://direct.mit.edu/qss/pages/submission-guidelines) acepta un primer envío con formato flexible y las figuras/tablas integradas. Esta es una **maqueta propia**, no una plantilla oficial ni una reproducción del diseño editorial publicado.

Se usa una columna, letra serif de 12 puntos, secciones/páginas numeradas, figuras junto a la sección correspondiente y referencias autor-año. El interruptor `\reviewcopytrue` en `preamble.tex` permite doble espacio y números de línea. El resumen está escrito y hay cinco palabras clave. Antes del envío se revisarán las normas y el estilo bibliográfico final. El acceso directo a la guía falló; el buscador daba un rastreo de hace unos 1,3 años, por lo que la consulta no certifica todos los requisitos vigentes.

La biblioteca científica canónica de 54 entradas permanece intacta. Su copia tipográfica escapa un guion largo. `context_references.bib` contiene Held y Velden (2022), ya verificado en la revisión QSS, Priem et al. (2022) y la documentación oficial de temas de OpenAlex. Los dos textos citan **26 referencias únicas**, comprobadas sin claves ausentes, duplicados o errores de metadatos. El registro de revisión separa esta comprobación formal del contraste de las afirmaciones.

## Reconstruir solo la presentación

Con el entorno de análisis ya existente, desde la raíz:

```sh
.venv-analysis/bin/python manuscript/scripts/build_figures.py
.venv-analysis/bin/python manuscript/scripts/build_tables.py
./manuscript/build.sh
```

Los exportadores leen tablas guardadas, aplican los mismos resúmenes descriptivos de los gráficos anteriores y escriben únicamente dentro de `manuscript/`. No importan ejecutores científicos. Una modificación de fórmulas, criterios o resultados pertenece a otra fase, no a estos programas. Para reproducir los exportadores de tablas se necesitan los catálogos locales indicados en S17; para compilar el ZIP bastan sus archivos incluidos.

Las dos tablas principales toman su redacción revisada de `tables/editorial/T01.tex` y `T02.tex`. Si se edita su explicación, actualizar esas fuentes y exportar; `tables/tex/` contiene las copias usadas al compilar. Los exportadores respetan estas versiones y registran su procedencia. Los CSV científicos siguen intactos. Los programas de exportación necesitan el repositorio completo; compilar los PDF desde el ZIP solo requiere las fuentes incluidas.

## Límites que deben seguir visibles

Conservar los errores de etiquetas y avisos de OpenAlex; las alertas de cada diseño; el carácter exploratorio de las ampliaciones; la dependencia entre pares y selecciones; y la diferencia entre geometría y validez temática. El cambio de formato no modifica esas conclusiones.

La revisión de la voz sigue [AUTHOR_VOICE.md](../AUTHOR_VOICE.md), y el contenido procede del [plano y matriz de evidencia](../MANUSCRIPT_BLUEPRINT.md). La revisión de la redacción está en [MANUSCRIPT_REVIEW.md](../MANUSCRIPT_REVIEW.md). El historial de los comentarios está en [MANUSCRIPT_COMMENTS.md](../MANUSCRIPT_COMMENTS.md) y `../research/manuscript_comments_2026-09-18/`. Los enlaces externos a esta carpeta corresponden al repositorio completo.

Antes de enviar quedan la lectura/aprobación del autor, sus datos de correspondencia, el depósito autorizado del material esencial, la licencia y la comprobación final de normas/referencias. No se ha hecho commit/push, depósito ni envío en esta entrega. Las versiones anteriores se conservan.
