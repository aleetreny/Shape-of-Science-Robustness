# Prueba del programa de descarga — 15-09-2026

**Resultado: preparado y probado. La descarga definitiva no se ha iniciado.** El usuario la ejecutará con `./download.sh`. Manual en `DOWNLOAD.md`.

## Evidencia comprobada

- **21 pruebas offline pasan.** Registro completo: `tests.txt`. Cubren filtros, límite de 50 palabras, reparto automático, IDs únicos, exportación, fallos de conexión, reintentos tras HTTP 429, páginas dañadas y exclusión de dos escritores simultáneos.
- Un proceso real fue terminado de golpe después de guardar una página y antes de registrarla en la base de estado. La reanudación produjo exactamente los mismos IDs y orden que una ejecución sin cortes. También se probaron cortes durante la selección y después de guardarla.
- Un servidor HTTP local cerró la conexión y después devolvió un límite temporal. El cliente reintentó correctamente. No se desconectó la red del ordenador ni se afectaron otras aplicaciones.
- **Prueba real final: 120 base + 4 complemento = 124 IDs únicos.** Se guardó una página, el proceso terminó con `--max-pages 1` y se volvió a ejecutar el comando. Comprobó los IDs guardados, continuó y terminó. Se guardaron seis páginas con 600 candidatos; el resto no se incorpora por conveniencia.
- Todos los datos exportados de esos 124 trabajos coinciden con sus respuestas originales: ID, texto, clasificación, año y demás campos normalizados. Huellas, tamaños y registro de reanudación: `verification.json`.
- La implementación guardada por esa descarga coincide con los módulos entregados. El ejecutable pasa la comprobación de sintaxis de Bash. El comando `status` informa que la descarga definitiva no se ha iniciado.
- Índice de **2.378.036** trabajos antiguos preparado en `data/cache/legacy_index.sqlite`, unos 213 MiB. El proyecto anterior continúa sin cambios según Git. Una prueba con un archivo pequeño confirma que crear el índice no modifica la fuente.
- Clave ausente de documentos, configuración, código y datos de la prueba inspeccionados. Viaja en la cabecera de autenticación; no se imprime ni se copia a archivos.

Carpeta de la prueba final: `data/smoke_verified_2026-09-15/`. La primera prueba, anterior a los últimos ajustes, está en `data/smoke_2026-09-15/`. Ambas están separadas de `data/corpus_500k/`. No se han calculado embeddings.

## Correcciones comprobadas durante la revisión

La revisión independiente encontró dos casos que no cubrían las primeras 18 pruebas. Se añadieron pruebas que fallaban antes de corregirlos:

1. Si una celda agotada tenía más candidatos que el pequeño bloque solicitado, el programa repetía muestras pequeñas sin llegar a demostrar su agotamiento. Ahora duplica el tamaño tras un bloque sin nuevos válidos, hasta el máximo permitido. La prueba de siete candidatos, un único válido ya usado y plazas pendientes termina reasignándolas correctamente.
2. El mensaje de pausa tras 20 bloques vacíos consultaba un contador ausente. Ahora se guarda el cero y la pausa muestra su motivo.

También se reforzó la reanudación: se comprueban los IDs de **todas** las páginas ya guardadas del bloque incompleto, con `select=id`, sin volver a descargar sus textos. Una prueba que modifica solo una página interior detiene la reanudación. La revisión posterior confirmó las correcciones y las 21 pruebas.

## Límites

- Estas pruebas verifican el programa y la recuperación en los fallos ejercitados; no sustituyen la validación del corpus de 500.000 cuando termine.
- OpenAlex cambia durante la extracción. Se congelan los textos y clasificaciones recibidos, con fecha por página. Verificar los IDs guardados no demuestra que todos los registros de OpenAlex pertenezcan a una misma instantánea global ni detecta todo cambio de metadatos con ID constante.
- Un bloque completamente guardado puede procesarse sin volver a consultarlo. Si un bloque incompleto ya no coincide, se conserva y se pausa para revisión; no se cambia automáticamente la semilla.
- `meta.count` con `sample` es el tamaño del resultado muestreado, no el tamaño de la población. Solo se declara agotamiento si una muestra completa tiene menos candidatos que los pedidos. Si no se puede demostrar agotamiento dentro del máximo de 10.000 y se acumulan 20 bloques vacíos, se pausa para revisión. No se reasignan plazas basándose solo en ausencia de éxito.
- Los grupos grandes no se recortan. El complemento no vuelve proporcionales los 500.000 juntos. El protocolo y las decisiones científicas pendientes se mantienen.

## Referencia de OpenAlex y reproducción

La API actual acepta autenticación por cabecera, páginas de hasta 100 registros y muestras de hasta 10.000; los límites temporales se gestionan con espera y reintento. [Documentación oficial de autenticación y límites](https://help.openalex.org/api/authentication/). Los parámetros de paginación admiten hasta 10.000 resultados con páginas normales. [Documentación oficial de paginación](https://help.openalex.org/api/paging/). Consultadas el 15-09-2026; las rutas antiguas redirigen al nuevo centro de ayuda.

Para repetir las pruebas **sin pedir datos nuevos a OpenAlex**, mientras la carpeta de prueba y el programa coincidan con esta versión:

```bash
.venv/bin/python research/download_validation_2026-09-15/verify.py
```

Ese verificador espera que producción todavía no esté iniciada. Después de iniciarla, usar `.venv/bin/python -m unittest discover -s tests -v` para las pruebas offline y `./download.sh status` para el estado real. El verificador no inicia producción.

Versiones medidas: Python 3.12.14, requests 2.34.2, PyArrow 25.0.1 y python-dotenv 1.2.3; confirmación automática en `verification.json`.
