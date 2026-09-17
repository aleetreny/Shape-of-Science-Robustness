# Pruebas para decidir el tamaño

Autorizadas expresamente el 14-09-2026. Hardware comprobado: Apple M5 Pro, 18 núcleos CPU, 48 GiB de memoria unificada y unos 308 GiB libres al empezar.

Se prepara un entorno separado `.venv-benchmark`; Mapping-Science se consulta en lectura. Los textos de prueba son 512 filas elegidas con prioridades aleatorias uniformes, semilla 20260914, a lo largo de los 2.378.036 trabajos. Cubren las 26 áreas. No constituyen la muestra científica final.

Objetivos: velocidad real de extracción/limpieza, velocidad de dos modelos en GPU, memoria y coste de cálculos posteriores. Una prueba de velocidad no certifica la estabilidad científica de una muestra grande ni de modelos todavía sin elegir.

Los textos, respuestas con abstracts y matrices de prueba están excluidos de Git. Las versiones, scripts y resultados resumidos se conservan aquí.

Pruebas terminadas. Leer [RESULTS.md](RESULTS.md) para resultados y límites. La decisión vigente está en [CORPUS_PROTOCOL.md](../../CORPUS_PROTOCOL.md): 500.000 trabajos, 400.000 de base y 100.000 de complemento. No se ha descargado ese corpus completo.
