# Shape of Science Robustness

Estudiamos cuánto cambia el mapa de la ciencia cuando representamos los mismos artículos con modelos distintos.

**Entrega vigente terminada y auditada, 17-09-2026:** comparación original sobre 500.000 y experimento de título, resumen y ambos sobre 52.000, con diez modelos. La ampliación incluye especialidades, candidatos comparables, estabilidad, Medicina, familias y literatura reciente. Estado preciso en [NEXT_STEPS.md](NEXT_STEPS.md).

**La idea principal:** hay una estructura amplia compartida, pero los vecinos de cada artículo dependen bastante del modelo y del texto. Acercar la lupa no reduce siempre el acuerdo. La receta y el tamaño de búsqueda pueden cambiar la interpretación.

- [Resultados vigentes](ROBUSTNESS_RESULTS.md): hallazgos, límites y controles de la ampliación.
- [Conclusiones frente a controles](CONCLUSION_CONTROLS.md): qué se sostiene, qué cambia y qué no se comprobó conjuntamente.
- [Catálogo de datos](DATA_CATALOG.md): rutas y alcance de cada archivo, sin mover los originales.
- [Métodos nuevos](METHODS_ROBUSTNESS.md), [recetas](POOLING.md) y [estabilidad](SAMPLING_STABILITY.md): definiciones y reproducción.
- [Propuesta de presentación](PAPER_OUTLINE.md): argumento y cuatro figuras principales; todavía no es un manuscrito.
- [Antecedentes actualizados](research/robustness_2026-09-17/RELATED_WORK_UPDATE.md): cinco trabajos solicitados y estudios cercanos de 2025–2026.
- [Alcance y comprobaciones R01–R12](ROBUSTNESS_SCOPE.md), [decisiones](DECISIONS.md) y [registro](progress.md): trazabilidad y continuidad.
- [Reglas para trabajar](AGENTS.md): comunicación, permisos y conservación.

Los 400.000 artículos de base y los 100.000 de complemento siguen identificados. Los modelos usan los mismos IDs dentro de cada comparación. Las entradas de 52.000 contienen el piloto de 26.000; el control de fragmento común de 52.000 tiene su propia selección y no debe confundirse con ellas.

La comparación inicial está en [ANALYSIS_RESULTS.md](ANALYSIS_RESULTS.md); el piloto anterior, en [CHECKLIST_RESULTS.md](CHECKLIST_RESULTS.md). Se conservan como historial verificado. Sus búsquedas tienen otros tamaños: no comparar porcentajes sin especificar candidatos y grupos.

Los datos grandes, pesos y entornos permanecen locales y fuera de Git. El repositorio remoto no sería una copia de seguridad de esos archivos. La presentación se reconstruye desde resultados guardados con el comando de [NEXT_STEPS.md](NEXT_STEPS.md), sin repetir descargas, modelos o vecinos. Redactar, distribuir datos y enviar a una revista son tareas posteriores.
