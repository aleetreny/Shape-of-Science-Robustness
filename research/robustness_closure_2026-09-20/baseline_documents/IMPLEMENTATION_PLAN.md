# Implementación de la descarga reanudable

> Para quien retome: ejecución local por pasos con la guía `superpowers:executing-plans`; diseño científico ya aprobado en `CORPUS_PROTOCOL.md`. La instrucción más reciente del usuario es dejarlo preparado para que **él ejecute el comando**, no iniciar el corpus completo.

Objetivo: programa probado que descarga 400.000 trabajos base y 100.000 de complemento, conserva cada página y reanuda sin duplicados tras cortes.

Arquitectura: respuestas comprimidas guardadas de forma atómica, SQLite para estado y trabajos seleccionados, transacciones por bloque y exportación a Parquet. Selección de bloques completos aleatorios y mezcla reproducible antes de cortar el último bloque, para no depender del orden de páginas que devuelva OpenAlex. Una única ejecución puede escribir en cada carpeta de descarga.

Tecnologías: Python 3.12, requests, SQLite, PyArrow, unittest; entorno `.venv` separado. Mapping-Science sigue en lectura.

- [x] Crear pruebas que fallen para limpieza, reparto, reinicio tras guardar página, repetición segura de bloque, desconexión/reintento, cambio de páginas al reanudar y exportación.
- [x] Implementar `sos_download/records.py`: abstract reconstruido, filtro fijado, hash de texto, reparto de 100.000 con desempates por Field/período.
- [x] Implementar `sos_download/store.py`: estado SQLite, páginas JSON.gz con guardado temporal + renombrado, filas únicas, configuración inmutable, exportación por lotes y reportes de duplicados potenciales.
- [x] Implementar `sos_download/runner.py`: cliente API sin claves en logs, espera/reintento, bloques completos, comprobación de páginas guardadas al reiniciar y pausa segura si hay cambios que impidan continuar la misma selección.
- [x] Implementar `sos_download/cli.py`, `config/corpus.json` y `download.sh`: iniciar/reanudar, estado, pausa con Ctrl+C, prevención de dos descargas simultáneas y proceso que mantiene el Mac despierto mientras está abierto.
- [x] Preparar índice local de IDs y hashes del TFM en `data/cache/`, sin copiar su corpus ni modificarlo. Registrar coincidencia exacta de texto para la posible reutilización posterior de vectores.
- [x] Ejecutar pruebas offline con fallos simulados y un servidor HTTP de prueba. El reinicio debe dar exactamente los mismos IDs que una ejecución sin cortes y no repetir páginas persistidas.
- [x] Ejecutar una descarga real pequeña en carpeta separada, detenerla y reanudarla. Verificar que termina con los tamaños previstos, texto válido y sin IDs duplicados. No usar esa prueba como parte de los 500.000 definitivos.
- [x] Revisar el código, corregir problemas, guardar validaciones y documentación. Dejar `./download.sh` y `./download.sh status` listos, sin iniciar producción.

Fallos y recuperación: no registrar una respuesta incompleta; no avanzar el bloque hasta confirmar sus páginas; si la conexión vuelve, reintentar la petición pendiente. Si los IDs de una página cambian al reanudar, pausar y conservar toda la evidencia para revisión, sin cambiar silenciosamente la selección. Ctrl+C detiene entre operaciones o deja una transacción sin aplicar, que se repite íntegra al reanudar.

Verificación principal: `.venv/bin/python -m unittest discover -s tests -v`. Prueba real: configuración de 120 base + 4 complemento, aparte del corpus final. El comando de producción debe seguir sin ejecutarse al cerrar esta tarea.

Resultado final: `research/download_validation_2026-09-15/RESULTS.md` y `verification.json`. 21 pruebas offline y prueba real de 124 IDs pasan; descarga definitiva sin iniciar. Revisión independiente terminada y hallazgos corregidos. Manual: `DOWNLOAD.md`.
