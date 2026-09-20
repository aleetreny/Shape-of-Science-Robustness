# Alternativas completas de voz

Tres versiones del artículo principal en inglés y español, preparadas el 19 de septiembre de 2026 para elección del autor. Las fuentes principales anteriores se conservan en manuscript/ y manuscript_es/. Las alternativas no cambian el estudio ni sustituyen automáticamente el borrador canónico.

## Archivos

- versions/v1_en/main.tex y versions/v1_es/main.tex: directa y sobria.
- versions/v2_en/main.tex y versions/v2_es/main.tex: razonamiento propio.
- versions/v3_en/main.tex y versions/v3_es/main.tex: voz marcada y reflexiva.
- base/en/ y base/es/: copias de los elementos comunes, sin cambios de contenido. Incluyen preámbulos, bibliografías, tablas, figuras y suplemento.
- edits/: párrafos redactados para cada opción, asociados a sus posiciones en el borrador de partida.
- variants.json: catálogo de alternativas, archivos y párrafos modificados.
- build.py: compila las fuentes completas.
- assemble.py: reconstruye las fuentes completas a partir de la base y los párrafos de edits/.

Los seis PDF se guardan en output/pdf/voice_variants/ al ejecutar desde este repositorio. La comparación de estilos está en [MANUSCRIPT_VOICES.md](../MANUSCRIPT_VOICES.md).

## Compilar

Se necesita Python 3 y Tectonic. No se importan los programas científicos ni se cargan corpus o vectores.

Desde la raíz del repositorio:

    python3 manuscript_variants/build.py

Solo una versión:

    python3 manuscript_variants/build.py --only v2_es

El programa utiliza el compilador local del repositorio si existe; después busca tectonic en PATH. También se puede indicar:

    python3 manuscript_variants/build.py --compiler /ruta/al/tectonic --output-dir /ruta/a/pdf

El mismo comando funciona desde el paquete extraído, siempre que el compilador esté disponible. Los archivos comunes se copian a una carpeta temporal; no hay que mover las fuentes. La fecha de compilación está fijada para poder comparar las salidas. Una instalación nueva de Tectonic podría descargar componentes de TeX al compilar por primera vez.

## Editar

Se puede editar directamente el main.tex de una opción y volver a compilar con build.py. Este comando conserva las ediciones directas.

Para mantener también el registro de párrafos, editar el archivo correspondiente en edits/ y ejecutar explícitamente:

    python3 manuscript_variants/assemble.py
    python3 manuscript_variants/build.py

assemble.py vuelve a generar las seis fuentes y reemplaza sus cambios directos. Por eso no se ejecuta automáticamente al compilar.

## Alcance del paquete

El ZIP contiene las seis fuentes y los elementos necesarios para reconstruir su presentación. No incluye el corpus, los vectores, los pesos de modelos ni las ejecuciones científicas completas. Los CSV completos de las tablas y los paquetes originales del estudio permanecen en sus ubicaciones previas.

El suplemento técnico es común y conserva sus fuentes en base/en/supplement.tex y base/es/supplement.tex. No hay tres interpretaciones distintas de sus controles. Las declaraciones del autor y la ayuda de Codex se conservan en las seis alternativas.

La recomendación editorial es la opción 2; la selección y aprobación corresponden al autor.
