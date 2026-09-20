# Versión española para revisar el manuscrito

**Revisión vigente para una primera lectura, 20-09-2026:** por petición expresa del autor, se ha releído y revisado el artículo completo para alguien sin contexto. Entrega: [FIRST_READER_REVIEW.md](../FIRST_READER_REVIEW.md). Se conserva la voz aceptada; se explican los conceptos, el propósito y los artículos de cada prueba, y el significado de las cifras. Inglés: 6.567 palabras de cuerpo, 195 de resumen y 24 páginas. Español: 7.332, 211 y 25 páginas. Cifras científicas, figuras, bibliografía, declaraciones y suplementos conservados. Las revisiones que siguen son históricas; aprobación personal pendiente.

**Edición anterior, 20-09-2026:** [38 comentarios aclarados](../MANUSCRIPT_EXPLANATIONS.md). Cuerpo español: 6.090 palabras; resumen: 240 para revisión. Inglés: 5.412 y 200. Suplemento conservado. Apartado de IA retirado del borrador por petición del autor; historial real de asistencia conservado y requisitos de declaración pendientes de comprobar antes del envío.

**Cierre posterior del 20-09-2026:** pruebas finales integradas; [informe](../ROBUSTNESS_CLOSURE_REPORT.md) y [cambios](../ROBUSTNESS_MANUSCRIPT_CHANGELOG.md). Se conserva el tono claro aceptado. Dos tablas y cuatro figuras principales; veinte grupos de tablas y once figuras suplementarias. Los manifiestos de presentación identifican los CSV usados actualmente; otros CSV conservados documentan la procedencia histórica. Revisión personal del autor pendiente.

**Edición anterior de voz, 20-09-2026:** V2 elegida y explicación reescrita en ambos idiomas. Guía: [MANUSCRIPT_CLARITY.md](../MANUSCRIPT_CLARITY.md). La aprobación personal del texto sigue pendiente.

Traducción completa del borrador inglés revisado el 20-09-2026: artículo, suplemento, tablas, notas y rótulos de las 15 figuras. Se conserva su organización, numeración, cifras, fórmulas, referencias y límites. Es la traducción de los resultados actualizados después del cierre de robustez; no es un resumen.

- Artículo: `../output/pdf/es/main.pdf` (25 páginas).
- Suplemento: `../output/pdf/es/supplement.pdf` (41 páginas).
- Fuentes: `main.tex`, `supplement.tex`, tablas y figuras de esta carpeta.
- Paquete separado: `../output/manuscript_source_es.zip`.

Los títulos bibliográficos, los títulos originales de artículos en la Tabla S8, los identificadores y los nombres de modelos se mantienen para poder identificarlos. En el texto, tablas y ejes se usa coma decimal. Los CSV conservan exactamente el formato y los valores originales.

En esta versión, **área** corresponde a **Field**, **especialidad** a **Subfield**, **acuerdo** a **agreement** y **regla de combinación de las salidas** a **pooling**. Las preguntas PI1--PI3 corresponden a RQ1--RQ3. La paginación cambia por la longitud de la traducción; los números de secciones, tablas y figuras siguen siendo los mismos.

Para comentar cambios basta con indicar una sección o copiar la frase. Los cinco comentarios del 18-09-2026 y los 38 del 20-09-2026 se han aplicado a ambos idiomas. La retirada posterior del apartado de IA sustituye su redacción breve anterior. Las copias anteriores están archivadas. Esta traducción no sustituye automáticamente al inglés.

## Compilar

Desde la raíz del repositorio:

```sh
./manuscript_es/build.sh
```

Solo reconstruye los dos PDF españoles. No descarga artículos ni ejecuta modelos o análisis. Para compilar el paquete extraído bastan Tectonic, o XeLaTeX y BibTeX, sobre `main.tex` y `supplement.tex`. No se ha probado una carga remota en Overleaf.

## Reconstruir la presentación traducida

Los textos principales se han traducido directamente. Los programas de esta carpeta permiten volver a generar los rótulos y tablas desde la presentación inglesa del repositorio completo:

```sh
python3 manuscript_es/scripts/translate_tables.py
python3 manuscript_es/scripts/layout_adjustments.py
python3 manuscript_es/scripts/localize_figures.py
.venv-analysis/bin/python manuscript_es/scripts/build_figures.py
./manuscript_es/build.sh
```

Los tres primeros programas usan solo la biblioteca estándar de Python. El exportador de figuras usa el entorno numérico ya existente. Leen fuentes guardadas y escriben únicamente en `manuscript_es/`. No se modifica ningún cálculo científico. Después de regenerar hay que comprobar la maquetación.

Las dos tablas principales toman su redacción revisada de `tables/editorial/T01.tex` y `T02.tex`. Si se edita su explicación, actualizar esas fuentes y exportar; `tables/tex/` contiene las copias usadas al compilar. Los exportadores respetan estas versiones y registran su procedencia. Los CSV científicos siguen intactos. Los programas de exportación necesitan el repositorio completo; compilar los PDF desde el ZIP solo requiere las fuentes incluidas.

Procedencia de la traducción: `../research/manuscript_spanish_2026-09-18/`. Revisión actual: `../FIRST_READER_REVIEW.md`. Historial: `../MANUSCRIPT_COMMENTS.md` y `../research/manuscript_comments_2026-09-18/`. El paquete permite reconstruir la presentación, no sustituye las entradas necesarias para reproducir todo el estudio. No hay depósito, licencia o envío nuevos. El texto sigue pendiente de revisión personal del autor.
