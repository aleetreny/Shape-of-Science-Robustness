# Subir a Zenodo desde la terminal

**21-09-2026: cargador corregido para enviar un archivo cada vez.** La prueba real del ZIP `embeddings_minilm.zip` duró casi seis minutos y alcanzó el 12,9 % (unos 100 MB), sin errores ni reintentos. Se detuvo manualmente para dejar libre el cargador. Esta prueba comprueba la continuidad más allá de los cortes observados; **no confirma todavía el envío completo de un archivo grande**.

Siguen completos y verificados **18 de 32 archivos**; quedan **14 archivos y 51.078.598.017 bytes (51,08 GB)**. Al ejecutar el comando, el ZIP de prueba empezará de nuevo; los 18 archivos completos se omiten. No queda ninguna subida de prueba activa. Los mensajes de `brew` y `pyenv` al abrir Terminal son ajenos a este problema.

La causa más probable de los cortes es la subida simultánea: el comportamiento coincide con la [incidencia 975 de Zenodo](https://github.com/zenodo/zenodo-rdm/issues/975). Es una coincidencia diagnóstica, no una causa del servidor confirmada.

## Comando recomendado

Abre Terminal y pega esta línea:

```sh
"/Users/alejandrotreny/Documents/ChatGPT/Shape of Science Robustness/upload_zenodo.sh"
```

La clave ya está guardada en el **Llavero de macOS**, fuera del repositorio. El script la lee al arrancar; no tienes que pegarla ni añadirla al comando. La entrada del Llavero se llama `shape-of-science-zenodo-22863543`, cuenta `zenodo.org`. Si macOS pide acceso al Llavero, permite el acceso para esta ejecución.

El script usa la API oficial de archivos grandes y envía **un archivo cada vez, de menor a mayor tamaño**. La ejecución anterior con dos conexiones mostró cortes repetidos; se ha desactivado la subida en paralelo. Muestra el nombre, porcentaje, velocidad y tiempo restante aproximado de cada archivo. Antes de enviar comprueba que la copia local coincide con la huella de la entrega congelada; después compara tamaño y MD5 con Zenodo. Los archivos que ya están completos se comprueban y se saltan.

Deja la Terminal abierta y el Mac conectado, con la tapa abierta. El lanzador evita el reposo por inactividad mientras trabaja. No inicies ninguna otra subida a este borrador desde el navegador u otra terminal mientras trabaja.

**Si se corta:** vuelve a ejecutar el mismo comando. Conserva y salta los archivos completos. El archivo que quedó a medias empieza desde cero: esta versión reanuda por archivo, no por bloques dentro del ZIP. Los errores temporales se reintentan hasta cinco veces; si encuentra una copia remota distinta, se detiene sin sobrescribirla. `Ctrl+C` interrumpe también la operación de red. La espera máxima de una operación de envío pasa a cinco minutos; esto no limita la duración total del archivo. Cada error muestra su tipo y el progreso queda guardado tras completar cada archivo.

Para consultar el estado sin subir nada, cuando el cargador no esté ejecutándose:

```sh
"/Users/alejandrotreny/Documents/ChatGPT/Shape of Science Robustness/upload_zenodo.sh" --status
```

La caché de huellas y el último estado quedan en `data/zenodo_upload_v1/`, que Git excluye. No contienen la clave. El cargador solo admite una conexión: `--workers 1` sigue siendo válido; otros valores se rechazan. La API no garantiza más velocidad que el navegador. Si se mantiene una velocidad de 0,3 MB/s, 51 GB necesitarían unas 47 horas de transmisión, sin contar interrupciones; es una estimación, no un plazo garantizado.

## Cuando termine

El mensaje final debe indicar **32/32 completos y cero pendientes**. El script deja el registro como borrador y **no pulsa Publish**.

1. Abre [el borrador de Zenodo](https://zenodo.org/uploads/22863543) y recarga la página.
2. Revisa los 32 nombres, pulsa **Save draft** y **Preview**. Comprueba autor, descripción, versión 1.0.0, licencias y fecha de publicación. El ZIP de código debe terminar en `-data-only.zip`.
3. Pulsa **Publish** cuando la vista previa sea correcta.

El DOI `10.5281/zenodo.22863543` sigue reservado hasta publicar. Después hay que comprobar el registro público y actualizar la cita, la disponibilidad y S8 en ambos idiomas.

## Contenido de la entrega

**Versión preparada el 21-09-2026: 32 archivos, 51,19 GB.** El conjunto incluye datos, código científico y documentación de reproducción. Se han retirado el artículo, los suplementos en inglés y español, sus fuentes editables, versiones anteriores y registros internos de trabajo. Las figuras científicas sueltas de los informes se conservan.

La lista exacta es `output/zenodo/UPLOAD_FILES.txt`. Sus 32 archivos son:

- 19 ZIP de datos numéricos, sin cambios.
- Un ZIP de código: **`shape-of-science-code-v1.0.0-data-only.zip`**.
- 12 archivos de documentación, versiones e integridad: `README.md`, `DATA_DICTIONARY.md`, `DATA_EXCLUSIONS.json`, `DATA_MANIFEST.json`, `SCHEMAS.json`, `CODE_VERSION.json`, `CHECK_RESULTS.json`, `LICENSE`, `LICENSING.md`, `THIRD_PARTY.md`, `SHA256SUMS` y `UPLOAD_FILES.txt`.

El cargador solo admite los nombres de esa lista, cuya huella está fijada en el programa. Omite archivos ajenos a ella, incluido el temporal `robustness_v2.zip.partial` encontrado en la carpeta. Ese temporal no se ha borrado ni forma parte de la entrega. No selecciones toda la carpeta sin revisar sus nombres si vuelves a usar el navegador.

El ZIP antiguo que contenía el manuscrito está conservado fuera de esta entrega. Artículo, suplementos y paquetes editables en ambos idiomas siguen excluidos. Puedes retocar su narrativa sin modificar estos datos. No se han cambiado los archivos congelados ni sus licencias: MIT para código propio, CC BY 4.0 para resultados y documentos propios, CC0 para metadatos OpenAlex.

## Comprobación del cargador

- Programa: [scripts/zenodo_upload.py](scripts/zenodo_upload.py); lanzador: [upload_zenodo.sh](upload_zenodo.sh). Solo biblioteca estándar de Python 3.9 o posterior y el Llavero de macOS; no necesita instalar paquetes.
- Diecisiete pruebas locales cubren reintentos, respuesta perdida, omisión de archivos completos, corrupción local, conflicto remoto, cuota, cancelación, envío en serie, conservación del progreso, límites de espera y errores sin revelar credenciales.
- [Primera verificación](research/zenodo_upload_2026-09-21/verification.json): subida completa del archivo de 3,35 MB y omisión al repetir.
- [Verificación de la corrección](research/zenodo_upload_fix_2026-09-21/verification.json): prueba continua de casi seis minutos, interrupción manual, 17 pruebas locales aprobadas y los 18 archivos completos comprobados de nuevo por tamaño y MD5. El registro sigue sin publicar.
- API utilizada: [documentación oficial de Zenodo](https://developers.zenodo.org/#quickstart-upload). La subida usa `PUT` al destino de archivos del propio borrador; la comprobación usa `GET`. El programa no edita metadatos, no elimina archivos y no publica.
