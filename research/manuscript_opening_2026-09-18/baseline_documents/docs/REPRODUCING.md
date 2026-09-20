# Cómo comprobar y reconstruir la entrega

No hay que descargar OpenAlex ni recalcular embeddings para leer resultados o reconstruir las figuras. Los comandos siguientes se ejecutan desde la raíz del repositorio.

## Comprobación pequeña del código

Con el entorno local existente:

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m unittest tests.test_geometry tests.test_neighbors tests.test_case_atlas
```

No inicia modelos ni accede a OpenAlex. Para otro ordenador, usar Python 3.12 y un entorno propio con `requirements-analysis.txt`. No cambiar los entornos congelados para reproducir una fase histórica. Las pruebas que necesitan PyTorch se ejecutan con `.venv-embed`, no con `.venv-analysis`.

La revisión completa de esta sesión queda en `research/prepaper_2026-09-17/tests_analysis_correct_environment.txt` y `tests_embedding.txt`: 32 y 20 pruebas respectivamente. Se conserva el primer fallo de importación por usar el entorno equivocado; no fue un fallo del cálculo científico.

## Reconstruir las tablas y figuras del atlas

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_review.report
```

Lee la salida sellada `data/prepaper_v1/case_atlas/` y reconstruye `reports/prepaper_v1/`. Solo exporta presentación. La revisión visual vuelve a quedar pendiente hasta inspeccionar los nuevos archivos. Para verificar figuras sin cambiar nada, comprobar las huellas de `reports/prepaper_v1/catalog.json`.

La entrega general anterior tiene su propio exportador:

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_deep.report
```

Requiere los 15 componentes terminados y reconstruye `reports/robustness_v2/final/`. No repetirlo por rutina: también renueva el estado de revisión visual.

## Reproducir el atlas desde resultados anteriores

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_review.case_atlas
```

Es un análisis derivado autorizado, sin inferencia nueva. Verifica padres y fuentes; rechaza reanudar con código/configuración diferentes. Requiere los vecinos, selecciones, centros y corpus locales ya existentes. Protocolo: [CASE_ATLAS_PROTOCOL.md](../CASE_ATLAS_PROTOCOL.md).

La auditoría adicional real está en `research/prepaper_2026-09-17/numerical_audit.py`: lee tres modelos completos y reconstruye una muestra de sus comparaciones por otra vía. No modifica los resultados. El diagnóstico de etiquetas/avisos está en `source_quality_audit.py` y se identifica expresamente como posterior al resultado.

## Reproducción desde un clon público

**Todavía no es completa.** Git excluye corpus, vectores, pesos y grandes derivados. Un clon permite leer documentación/tablas/figuras y ejecutar pruebas pequeñas, pero necesita el depósito de datos previsto en [DATA_RELEASE.md](DATA_RELEASE.md) para reconstruir los experimentos. No prometer que una llamada nueva a OpenAlex recuperará exactamente la misma muestra histórica.

Los scripts de verificación bibliográfica de esta sesión usan las herramientas locales `citation-management`; son auxiliares de consulta. La biblioteca final y sus evidencias de metadatos se conservan sin exigir esas herramientas para analizar los datos o leer las referencias.


## Piloto de propiedades de la forma

Completado el 18-09-2026. [Registro y comandos](../METHODS_MORPHOLOGY.md). Reconstruir la entrega desde los resultados guardados:

```sh
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 .venv-analysis/bin/python -m sos_morphology.report
```

No ejecuta modelos. Verifica el cálculo padre antes de exportar; revisar después las figuras. El coordinador de cálculo científico es otro módulo, ya terminado, que reutiliza bloques verificados. Sus fuentes/configuración están congeladas; una nueva fórmula requiere una nueva versión.

## Resumen final de parejas de disciplinas

Completado con medidas guardadas, sin repetir morfología. [Definiciones, cobertura y comandos](../METHODS_FIELD_PAIRS.md). Comprobación independiente:

```sh
.venv-analysis/bin/python -m sos_pair_summary.audit
```

Figuras: `.venv-analysis/bin/python -m sos_pair_summary.report`. El ejecutor `sos_pair_summary.analyze` ya terminó y omite resultados completos con fuentes compatibles. Mantener los archivos congelados; nuevas reglas necesitan otra versión. La entrega completa contiene doce tablas y dos figuras; comprobar de nuevo las figuras si se reconstruyen.

## Compilar la maqueta del manuscrito

```sh
./manuscript/build.sh
```

Genera los dos PDF de `output/pdf/` usando los archivos incluidos en `manuscript/`. No ejecuta modelos, vecinos o morfología. [Guía](../manuscript/README.md) y [procedencia](../research/manuscript_layout_2026-09-18/). Los exportadores de presentación están separados de los programas científicos congelados.
