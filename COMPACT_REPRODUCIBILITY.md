# Distribución compacta para QSS

**21-09-2026. Publicado y verificado en GitHub y Zenodo.** El paquete seleccionado ocupa 492,15 MB frente a los 51,19 GB anteriores: una reducción del 99,04 %. Los originales se conservan.

## Lo que pide QSS

La [guía oficial de QSS](https://direct.mit.edu/qss/pages/submission-guidelines) distingue dos cosas: compartir el código es una recomendación fuerte; publicar los datos esenciales para reproducir los resultados principales es una exigencia. Los datos deben estar en un repositorio público con identificador permanente, por ejemplo un DOI. La entrega bajo petición no basta. Se permiten excepciones legales o éticas, que deben explicarse, y el artículo debe incluir una declaración de disponibilidad. Se comprobó también directamente la sección de datos en la página oficial, abierta en el navegador el 21-09-2026; coincide con el texto indexado consultado al principio.

No se deduce de esa norma que haya que subir todos los archivos que produjo el ordenador. Tampoco basta con poner el código en GitHub y omitir los datos que utiliza. La decisión aplicada conserva las medidas de las comparaciones, sus identidades y sus controles, y retira las grandes cachés de vectores y listas de vecinos.

## Selección exacta

| Archivo | Contenido y motivo |
| --- | --- |
| `code-and-guides.zip` | Código científico, configuraciones, versiones, protocolos, informes de referencia y comprobadores de reproducción. |
| `data-analysis-ready-v1.zip` | Metadatos sin títulos ni resúmenes de los 500.000 registros; identificadores, áreas, fechas y marcas de calidad. |
| `data-analysis-v1.zip` | Medidas iniciales de estructura, recuentos de vecinos por consulta, selecciones y controles. |
| `data-checklist-v1.zip` | Prueba inicial de entradas de texto, recetas, tiempo y composición. |
| `data-robustness-v2.zip` | Ampliación a 52.000, especialidades, estabilidad y controles adicionales. |
| `data-robustness-closure-v1.zip` | Repeticiones de centros, comparación texto/modelo, geometría centrada y filtro de calidad. |
| `data-morphology-pilot-v1.zip` | Medidas geométricas por modelo, área y selección; referencias y controles. |
| `data-field-pair-summary-v1.zip` | Contrastes entre las 325 parejas de áreas. |
| `data-prepaper-v1.zip` | Casos y diagnósticos de origen que sustentan los límites discutidos. |
| `data-embeddings-v1.zip` | Solo manifiestos y fuentes de configuración, unos 40 kB; no contiene los vectores. |
| `README.md`, `LICENSE`, `LICENSING.md`, `REPRODUCTION_CHECK.json`, `release-manifest.json` | Guía, licencias, comprobación y huellas de los archivos descargables. |

La lista completa de miembros incluidos y omitidos está en `SELECTION.json`, dentro del ZIP de código. Los datos científicos seleccionados son copias idénticas, verificadas por SHA-256, de los archivos congelados. Artículo, suplementos, fuentes editoriales, registros internos y credenciales quedan fuera.

## Qué se ha comprobado

Desde los ZIP extraídos en una carpeta nueva se recalcularon 25 tablas, con 106.445 filas; coincidieron exactamente con las tablas guardadas. Se verificaron 17.550 medidas locales de vecinos desde sus recuentos por consulta, además de las medias local/global y los resúmenes de las cuatro figuras principales. La misma prueba pasó en un entorno Linux nuevo con las versiones fijadas; todas las celdas de los CSV fueron idénticas. [Ejecución pública](https://github.com/aleetreny/Shape-of-Science-Reproducibility/actions/runs/35610529164). No se cambió ningún resultado científico.

Esta vía empieza en las medidas producidas por los modelos. No repite la generación de embeddings desde los textos ni reconstruye todas las listas de vecinos. Los textos históricos no se redistribuyen porque sus permisos no están establecidos; recuperar hoy los mismos identificadores de OpenAlex puede devolver textos distintos. Se publican los programas, las versiones, los identificadores y las huellas para documentar esa fase, sin afirmar una reproducción íntegra desde el texto. Tampoco se certifica la repetición de todos los análisis históricos suplementarios.

## Repositorio y DOI

La entrega usa [GitHub](https://github.com/aleetreny/Shape-of-Science-Reproducibility) para código y archivos de versión. La transferencia a Zenodo se realiza desde un proceso de GitHub, evitando las largas conexiones desde el Mac. El depósito está publicado como [10.5281/zenodo.22876602](https://doi.org/10.5281/zenodo.22876602), con los 15 archivos verificados por tamaño y huella. Los archivos de GitHub se descargaron sin autenticación y se verificaron también por SHA-256. El borrador anterior `22863543` queda intacto y sin publicar.

Figshare sería una alternativa válida: proporciona DOI y 20 GB de almacenamiento personal gratuito. GitHub por sí solo facilita el acceso, pero no sustituye el identificador permanente que pide QSS. Para esta entrega, aprovechar GitHub y el acceso a Zenodo ya configurado evita crear otra cuenta y permite verificar la transferencia de servidor a servidor.

Fuentes: [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases), [almacenamiento de Figshare](https://help.figshare.com/article/paid-services), [DOI de Figshare](https://help.figshare.com/article/guide-to-sharing-nih-funded-research-on-figshare-com), [API de Zenodo](https://developers.zenodo.org/). La selección es una aplicación razonada de la política; la revista conserva la decisión editorial sobre suficiencia.

## Incidencia de transporte corregida

La primera transferencia remota completó 12 archivos. El registro mostró que las cargas mayores agotaban exactamente los 300 segundos de una llamada de envío, aunque la conexión hubiera avanzado. El cargador remoto enviaba el archivo entero en una sola operación. Se corrigió para enviar bloques de 256 kB con el tamaño total declarado, conservando un único archivo en curso y la comprobación del archivo completo al terminar. Una prueba con un receptor local lento reproduce el fallo anterior y verifica que el transporte corregido entrega todos los bytes. No se ofrece reanudación dentro de un archivo interrumpido; se conservan los archivos completos.

La [documentación de Python](https://docs.python.org/3/library/socket.html#socket.socket.sendall) explica que la espera de `sendall` limita la duración total de esa operación. Evidencia: `cloud_transfer_cancelled.log` y `streamed_transfer_test.json` en `research/compact_release_2026-09-21/`. La corrección afecta a la transferencia, no a los archivos científicos publicados.
