# Manuscrito y suplemento: maqueta de trabajo

Los dos documentos tienen estructura, tablas y figuras reales. La prosa del artículo sigue pendiente y aparece como *Writing plan*. Los nombres de autores, afiliaciones y declaraciones no se han rellenado por suposición.

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
| Suplemento | 17 grupos | 10 |

Cada tabla suplementaria tiene una versión legible en el PDF y sus CSV completos, sin redondear, en `tables/data/S01/` a `S17/`. La numeración no oculta miles de filas tras puntos suspensivos: los resúmenes indican su selección y los archivos completos los acompañan. [Registro de tablas](tables/manifest.json).

Todas las figuras se entregan en PDF vectorial, SVG editable y PNG/TIFF a 300 dpi. Son copias de presentación, con rótulos ingleses y tamaño de página uniforme. Sus valores dibujados y fuentes se registran en [el manifiesto de figuras](figures/manifest.json). Los datos originales no se movieron ni editaron. La Figura S10 reúne apertura y dimensión en los dos triángulos de una matriz para que las 650 clasificaciones se puedan leer a tamaño de artículo.

## Formato de QSS

No se ha localizado una clase LaTeX oficial específica en la búsqueda realizada. La [guía de QSS consultada](https://direct.mit.edu/qss/pages/submission-guidelines) acepta un primer envío con formato flexible y las figuras/tablas integradas. Esta es una **maqueta propia**, no una plantilla oficial ni una reproducción del diseño editorial publicado.

Se usa una columna, letra serif de 12 puntos, secciones/páginas numeradas, figuras junto a la sección correspondiente y referencias autor-año. El interruptor `\reviewcopytrue` en `preamble.tex` permite doble espacio y números de línea. El resumen y las palabras clave son planes de contenido; no un resumen terminado. Antes del envío se revisarán las normas y el estilo bibliográfico final. El acceso directo a la guía falló; el buscador daba un rastreo de hace unos 1,3 años, por lo que la consulta no certifica todos los requisitos vigentes.

La bibliografía copiada procede de la biblioteca canónica de 54 entradas. El PDF imprime solo las referencias utilizadas en la tabla de modelos. Las citas de introducción/discusión se incorporarán al redactar y comprobar las frases concretas; no se añaden automáticamente todos los antecedentes leídos.

## Reconstruir solo la presentación

Con el entorno de análisis ya existente, desde la raíz:

```sh
.venv-analysis/bin/python manuscript/scripts/build_figures.py
.venv-analysis/bin/python manuscript/scripts/build_tables.py
./manuscript/build.sh
```

Los exportadores leen tablas guardadas, aplican los mismos resúmenes descriptivos de los gráficos anteriores y escriben únicamente dentro de `manuscript/`. No importan ejecutores científicos. Una modificación de fórmulas, criterios o resultados pertenece a otra fase, no a estos programas. Para reproducir los exportadores de tablas se necesitan los catálogos locales indicados en S17; para compilar el ZIP bastan sus archivos incluidos.

## Límites que deben seguir visibles

Conservar los errores de etiquetas y avisos de OpenAlex; las alertas de cada diseño; el carácter exploratorio de las ampliaciones; la dependencia entre pares y selecciones; y la diferencia entre geometría y validez temática. El cambio de formato no modifica esas conclusiones.

La revisión de la voz sigue [AUTHOR_VOICE.md](../AUTHOR_VOICE.md); el contenido y las citas previstas, [MANUSCRIPT_BLUEPRINT.md](../MANUSCRIPT_BLUEPRINT.md). El siguiente paso es redactar métodos y resultados cuando el usuario lo pida. Autoría, declaraciones, depósito, licencia y envío siguen pendientes.
