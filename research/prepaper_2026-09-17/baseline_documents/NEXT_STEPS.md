# Estado actual: cierre experimental ampliado terminado

**17-09-2026. R01–R12 completos y auditados. No quedan cálculos activos.** Se conservan el corpus de 500.000, los diez modelos originales y todas las fases anteriores. Las tres entradas se compararon sobre 52.000 artículos; también terminaron especialidades, estabilidad local, Medicina, tiempo, familias, controles y literatura.

## Punto exacto para continuar

1. Leer [ROBUSTNESS_RESULTS.md](ROBUSTNESS_RESULTS.md) y [CONCLUSION_CONTROLS.md](CONCLUSION_CONTROLS.md): resultados vigentes y qué límites conserva cada conclusión.
2. Cuando se solicite, redactar siguiendo [PAPER_OUTLINE.md](PAPER_OUTLINE.md), [METHODS_ROBUSTNESS.md](METHODS_ROBUSTNESS.md) y los métodos de las dos fases anteriores. La revisión de [antecedentes próximos](research/robustness_2026-09-17/RELATED_WORK_UPDATE.md) ya incluye los cinco trabajos pedidos y estudios de 2025–2026; no atribuir novedad a comparar CKA/vecinos/familias por sí solo.
3. No repetir descargas, inferencia o vecinos por retomar el proyecto. Las salidas y versiones están en [DATA_CATALOG.md](DATA_CATALOG.md); la evidencia de cada requisito, en [ROBUSTNESS_SCOPE.md](ROBUSTNESS_SCOPE.md).
4. Un experimento adicional deberá resolver una afirmación concreta todavía insuficientemente apoyada. No ampliar automáticamente las entradas a 500.000 ni añadir morfología o modelos.

## Decisiones y límites que se conservan

- **Mean principal** para los cuatro BERT de palabras; CLS/SEP son controles. [POOLING.md](POOLING.md) define operaciones exactas y cómo cambian los resultados. No elegir después la receta que produzca más acuerdo.
- Tres entradas en **52.000**, 400 por cada área/período, incluyendo el piloto de 26.000. Los 52.000 del control de fragmento común son otra selección; no emparejar por posición local.
- Alertas de entrada: con 100 selecciones comparables, **72/520 en 26k → 5/520 en 52k**. Con 20 se reproduce 31 → 4. Las 50 iniciales y las de especialidades son otras comprobaciones. [SAMPLING_STABILITY.md](SAMPLING_STABILITY.md) conserva claves, magnitudes y límites; no son intervalos de confianza poblacionales. Sin alerta no significa contraste distinto de cero.
- No hay una bajada universal del acuerdo al aumentar el detalle. Con consultas/candidatos/fechas emparejados, k25 baja en 127/217 Subfields y sube en 90. Todos los 500.000 IDs tienen resultados locales, pero solo 10.850 consultas tienen diez selecciones controladas de candidatos.
- Para fechas, separar el efecto de consultas del de candidatos. El signo de vecinos cambia al igualar tamaño; la forma aumenta entre extremos en la mayoría, pero no continuamente en todas las áreas. No afirmar convergencia histórica causal.
- Reequilibrar especialidades de Medicina cambia poco su acuerdo; retirar biomédicos no elimina su diferencia de forma. Los rasgos de familias son asociaciones de diez modelos, dependientes de la receta; no causas independientes identificadas.
- CKA corregida y vecinos k25 principales; Procrustes, rangos, k10/k50 y controles como comprobaciones. No se añadió morfología. No hay modelo ganador por consenso ni verdad temática externa en las etiquetas OpenAlex.

## Archivos y verificación

| Material | Ubicación |
| --- | --- |
| Entrega vigente, 50 tablas y siete figuras PDF/SVG/PNG | `reports/robustness_v2/final/` |
| Auditoría numérica conjunta, 15 componentes | `data/robustness_v2/final_audit/audit.json` y `summary.json` |
| Auditoría de presentación y catálogo | `reports/robustness_v2/final/audit.json` y `catalog.json` |
| Revisión visual de siete figuras | `research/robustness_2026-09-17/final_visual_review.json` |
| Cierre documental e inventario de entrega | `research/robustness_2026-09-17/closure_audit.json` |
| Comparaciones, selecciones, controles y fuentes congeladas | `data/robustness_v2/` |
| Origen, versiones y huellas comprobadas | `data/robustness_v2/provenance/` |
| Historial inicial sobre 500.000 | `reports/analysis_v1/final/` y `ANALYSIS_RESULTS.md` |
| Historial del piloto de 26.000 | `reports/checklist_v1/final/` y `CHECKLIST_RESULTS.md` |

Usar `control_review_v2` para separar MiniLM consigo mismo de MiniLM frente a los otros nueve. Usar `structural_review_v3` como resumen estructural. Las versiones previas se conservan como historial, no se mezclan. Las vistas provisionales no sustituyen los archivos finales.

Para reconstruir solo la presentación vigente desde los resultados guardados:

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_deep.report
```

El exportador exige la auditoría numérica completa y no ejecuta modelos ni vecinos. Una nueva exportación registra la revisión visual como pendiente; revisar los nuevos archivos antes de volver a sellarla. Las fuentes científicas, configuraciones y datos están congelados; un cambio metodológico requiere otra versión de salida.

No relanzar `start_embeddings.sh`, el extractor ni los ejecutores de cierre terminados. Los PIDs de `ACTIVE_RUNS.json` son históricos, con estado completo. Las automatizaciones anteriores siguen pausadas. Los datos grandes permanecen locales y fuera de Git; el repositorio remoto no es su copia de seguridad. La redacción completa, distribución de datos y envío no se han realizado ni se asumen autorizados por este cierre.
