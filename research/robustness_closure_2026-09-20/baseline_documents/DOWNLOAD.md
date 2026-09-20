# Cómo iniciar la descarga

**Ya está preparado. La descarga completa la inicia el usuario.** Objetivo: 500.000 papers válidos, con el reparto de `CORPUS_PROTOCOL.md`.

Desde la terminal situada en este proyecto:

```bash
./download.sh
```

Para consultar el avance desde otra terminal situada aquí:

```bash
./download.sh status
```

Para pausar, pulsa **Ctrl+C** en la terminal de la descarga. Para continuar, escribe otra vez **`./download.sh`**. No cambies nombres ni borres la carpeta `data` entre ejecuciones.

Si pierdes internet, el programa espera y vuelve a intentarlo. Si apagas el ordenador o cierras el programa, repite el mismo comando al volver. Se conservan las páginas completas que ya se guardaron; una petición que quedó a medias se repite.

Deja el Mac conectado a la corriente, con la tapa abierta y la terminal abierta. El comando evita el reposo por inactividad mientras trabaja; cerrar la tapa puede suspender el Mac. La pantalla sí puede apagarse. Calculábamos unas **3–6 horas**, pero los límites de OpenAlex o cortes pueden alargarlo.

El aviso `command not found: pyenv` de tu terminal **no impide usar este comando**. El programa utiliza su propio entorno ya instalado en `.venv`; no necesitas activarlo. No se ha modificado `.zshrc`.

## Qué verás

La terminal muestra las páginas que se van guardando. El contador de papers válidos sube al terminar cada bloque, después de comprobar sus textos. Al principio puede marcar cero mientras las páginas ya están quedando guardadas.

Primero reúne los 400.000 de la base general. Después calcula el reparto de los 100.000 adicionales y los reúne. Finalmente comprueba los datos y crea la tabla. **No calcula embeddings ni inicia experimentos.**

Si vuelves a lanzar el comando mientras ya está funcionando, la segunda ejecución se detiene para evitar dos descargas a la vez. El comando `status` puede usarse siempre.

## Dónde queda cada cosa

| Archivo o carpeta | Para qué sirve |
| --- | --- |
| `data/corpus_500k/progress.json` | Último avance y fase actual. |
| `data/corpus_500k/state.sqlite` | Trabajos seleccionados, reparto, bloques, semillas e incidencias. Permite reanudar. |
| `data/corpus_500k/raw/` | Respuestas completas comprimidas, con fecha y parámetros sin clave. No borrarlas. |
| `data/corpus_500k/corpus.parquet` | Tabla maestra, creada al reunir todos los trabajos. |
| `data/corpus_500k/field_year_counts.csv` | Recuento por Field, año y conjunto. |
| `data/corpus_500k/field_period_counts.csv` | Recuento por Field, período y conjunto. |
| `data/corpus_500k/validation.json` | Comprobaciones finales y huella de la tabla. Solo aparece al completar la preparación. |
| `data/cache/legacy_index.sqlite` | Índice de los 2.378.036 IDs y textos antiguos para detectar coincidencias. Se construyó leyendo el TFM, sin modificarlo. |
| `config/corpus.json` | Cantidad y reglas definitivas. No cambiar durante la descarga. |
| `sos_download/` | Programa de extracción, limpieza, guardado, reparto y exportación. |

Los datos y el entorno están excluidos de Git. Los documentos, configuración y programa sí pueden versionarse. La clave existente se lee de forma privada; no hace falta ponerla en el comando ni copiarla al repositorio.

## Si el programa pide una revisión

OpenAlex puede cambiar sus resultados con el tiempo. Al retomar un bloque incompleto, se comprueban los IDs de sus páginas guardadas, sin volver a pedir sus títulos y abstracts. Si ya no coinciden, se pausa y conserva todo. En ese caso, pide revisar el estado: **no borres los datos ni fuerces otra selección por tu cuenta**.

También se pausa ante archivos dañados, cambios de configuración o del programa, problemas permanentes de acceso, o 20 bloques seguidos sin ningún trabajo nuevo. Estas pausas evitan continuar con un resultado engañoso. No existe una garantía de descarga ininterrumpida frente a cualquier cambio externo.

Los textos ya recibidos conservan su contenido y fecha originales. Esta descarga no es una copia de OpenAlex tomada toda en el mismo segundo; las fechas y respuestas permiten estudiar esos límites después.

## Para otra persona que retome el proyecto

Leer `AGENTS.md`, `DECISIONS.md`, `progress.md` y `CORPUS_PROTOCOL.md`. Antes de tocar código, consultar `./download.sh status`. No cambiar el programa mientras la descarga está abierta. Se guardan huellas de los módulos al comenzar para impedir una reanudación silenciosa con otras reglas.

El cruce con el TFM marca coincidencia de ID y de título+abstract exactos. **Esto identifica posibles reutilizaciones; todavía hay que comprobar la entrada y versión del modelo antes de reutilizar un embedding.** El corpus antiguo no se añade por conveniencia a la selección aleatoria nueva.

Pruebas: `research/download_validation_2026-09-15/RESULTS.md`. Las carpetas `data/smoke_2026-09-15/` y `data/smoke_verified_2026-09-15/` son pruebas pequeñas, completamente separadas del corpus definitivo.

## Estado posterior, 15-09-2026

La descarga del corpus de 500.000 ya terminó. Para consultarla basta `./download.sh status`; no es necesario volver a iniciarla. Resultado de auditoría y continuación: `AUDIT.md` y `NEXT_STEPS.md`.

### Preparación posterior terminada

La copia limpia y completada está en `data/corpus_clean_v1/`. No hace falta volver a ejecutar la descarga original. Para comprobar los archivos preparados: `./prepare.sh preflight`. Resultado en `CLEANING.md`; guía de la fase de modelos en `EMBEDDINGS_READY.md`. Conservar `data/corpus_500k/`, porque sigue siendo la evidencia de origen.
