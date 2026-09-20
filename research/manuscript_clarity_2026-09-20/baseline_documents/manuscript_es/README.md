# Versión española para revisar el manuscrito

Traducción completa del borrador inglés del 18-09-2026: artículo, suplemento, tablas, notas y rótulos de las 14 figuras. Se conserva su organización, numeración, cifras, fórmulas, referencias y límites. No es un resumen ni una nueva versión de los resultados.

- Artículo: `../output/pdf/es/main.pdf` (21 páginas).
- Suplemento: `../output/pdf/es/supplement.pdf` (35 páginas).
- Fuentes: `main.tex`, `supplement.tex`, tablas y figuras de esta carpeta.
- Paquete separado: `../output/manuscript_source_es.zip`.

Los títulos bibliográficos, los títulos originales de artículos en la Tabla S8, los identificadores y los nombres de modelos se mantienen para poder identificarlos. En el texto, tablas y ejes se usa coma decimal. Los CSV conservan exactamente el formato y los valores originales.

En esta versión, **área** corresponde a **Field**, **especialidad** a **Subfield**, **acuerdo** a **agreement** y **regla de combinación de las salidas** a **pooling**. Las preguntas PI1--PI3 corresponden a RQ1--RQ3. La paginación cambia por la longitud de la traducción; los números de secciones, tablas y figuras siguen siendo los mismos.

Para comentar cambios basta con indicar una sección o copiar la frase. Los cinco comentarios del autor del 18-09-2026 se han aplicado tanto al inglés como al español: título, tablas, Figura 1B y declaración breve de IA. Las copias anteriores están archivadas. Esta traducción no sustituye automáticamente al inglés.

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

Procedencia de la traducción: `../research/manuscript_spanish_2026-09-18/`. Revisión vigente: `../MANUSCRIPT_COMMENTS.md` y `../research/manuscript_comments_2026-09-18/`. El paquete permite reconstruir la presentación, no sustituye las entradas necesarias para reproducir todo el estudio. No hay depósito, licencia o envío nuevos. El texto sigue pendiente de revisión personal del autor.
