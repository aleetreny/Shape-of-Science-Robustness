# Entrega de datos y código

**Cambio de empaquetado, 21-09-2026:** el depósito excluye los artículos y suplementos, sus fuentes y copias históricas, en ambos idiomas, además de los registros internos de trabajo. El ZIP del código es una distribución científica seleccionada del commit `cc61517`, no una copia completa del repositorio. `CODE_VERSION.json` y su `PACKAGE_MANIFEST.json` identifican archivos y cambios de documentación. Los 19 ZIP de datos permanecen iguales. Total actual: 32 archivos, 51,19 GB. [Guía de carga](../ZENODO_UPLOAD.md).

**Estado, 20-09-2026:** el autor ha autorizado la entrega y confirmado MIT para código propio y CC BY 4.0 para documentos/resultados propios. OpenAlex conserva CC0. Hay 19 ZIP verificados de datos, 51,14 GB y 58.201 archivos. El registro de Zenodo `22863543` está guardado como borrador, con DOI reservado y 75 GB de capacidad, **sin archivos publicados**.

La entrega vigente es [PUBLIC_RELEASE.md](../PUBLIC_RELEASE.md); [ZENODO_UPLOAD.md](../ZENODO_UPLOAD.md) explica la carga manual y la publicación posterior. El código se archiva junto con los datos, en un ZIP de una versión concreta de GitHub, con ámbitos de licencia separados. Esto sustituye la propuesta preliminar de dos registros y conserva juntas las dos partes de la entrega.

## Qué incluye

Identificadores y metadatos sin resúmenes; vectores de los diez modelos y sus variantes; las selecciones, consultas y candidatos exactos; las medidas por condición, controles y fuentes congeladas de cada fase. El piloto de 26.000, la ampliación de texto a 52.000 y el control separado de fragmento común de 52.000 conservan su identidad.

Los pesos de los modelos y las tablas históricas de títulos/resúmenes de entrada quedan fuera. Se conservan identificadores, huellas y exportaciones separadas de columnas sin texto. El manifiesto enumera las exclusiones; los archivos omitidos no se sustituyen silenciosamente por contenido distinto.

## Qué se ha probado

- Integridad de todos los ZIP y de sus 58.201 archivos descomprimidos.
- Resúmenes de las cuatro figuras principales desde medidas por condición, en una carpeta aislada y sin Internet.
- Cálculos independientes desde los ZIP de vectores, con los diez modelos y condiciones fijadas de las cuatro figuras.
- Reconstrucción exacta de los cuatro PDF desde los paquetes fuente.

La repetición de **todos** los cálculos originales no está certificada. Los ejecutores históricos conservan dependencias de sus rutas y entradas originales. Los comandos portables, las condiciones verificadas y los límites están en [reproducibility/README.md](../reproducibility/README.md).

## Antes del envío

Terminar la carga, publicar el registro y comprobar sus archivos desde el enlace público. Después actualizar la declaración, la cita de datos y el Suplemento S8 con la [redacción preparada](AVAILABILITY_AFTER_PUBLICATION.md). Un DOI reservado no equivale a acceso público.

El inventario preliminar y la revisión bibliográfica se conservan como historial en [NOVELTY_AND_REPRODUCIBILITY.md](../NOVELTY_AND_REPRODUCIBILITY.md). No reabren la decisión de licencia ya aceptada.
