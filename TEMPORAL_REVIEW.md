# ¿Los modelos coinciden más en los artículos recientes?

**En promedio, sí para la forma, pero la subida es pequeña y no continua en todas las áreas. Para los vecinos, hay que igualar primero dónde buscamos.** Comparar una cesta pequeña antigua con una cesta grande reciente puede cambiar incluso el signo de la conclusión.

Cinco períodos: 2000–04, 2005–09, 2010–14, 2015–19 y 2020–24. Se reconstruyeron 23.400 trayectorias de área×par de modelos×medida/control. Se conservaron cambios entre extremos, pendiente y dirección de cada paso. No se hizo una prueba tratando los 45 pares como independientes.

| Medida/control | Cambio medio 2020–24 menos 2000–04 | Áreas que suben entre extremos | Áreas que suben en los cuatro pasos |
| --- | ---: | ---: | ---: |
| Forma, todos los artículos de cada celda | +0,02074 CKA | 23/26 | 4/26 |
| Forma, 2.048 por celda | +0,02064 CKA | 24/26 | 4/26 |
| Forma, filtro estricto de calidad/duplicados | +0,01153 CKA | 20/26 | 7/26 |
| Vecinos 25, todos los candidatos disponibles | −0,87 puntos porcentuales | 10/26 | 1/26 |
| Vecinos 25, 2.048 candidatos por celda | +0,91 puntos porcentuales | 20/26 | 6/26 |

Las unidades de CKA y puntos porcentuales de vecinos son distintas. La mayoría de trayectorias tiene algún paso en cada dirección. Para forma con 2.048, 43 de los 45 promedios por pareja suben entre extremos; para vecinos con 2.048, 35/45. Eso tampoco significa que suba cada combinación individual área×pareja.

## Separar tiempo, consultas y candidatos

El control adicional conserva exactamente las mismas consultas mientras cambia el conjunto donde buscan vecinos. Descomposición del cambio entre extremos, k=25:

- Resultado original con todas las consultas/candidatos: −0,008692.
- Contribución de escoger el subconjunto de consultas: −0,000303.
- Contribución de igualar candidatos con consultas idénticas: +0,018110.
- Resultado final con conjunto comparable: +0,009115.

Las piezas suman exactamente. Por tanto, el cambio de signo no puede contarse como un descubrimiento histórico sin explicar el universo de búsqueda. Las comprobaciones con k=10/50 y otras recetas están en las tablas, no se descartaron.

El control de calidad reduce claramente el aumento medio de forma. No conocemos por separado cuánto procede de cobertura, longitud/estilo de abstracts, duplicación residual, composición temática o evolución real. No afirmar que la ciencia «converge» causalmente porque los modelos coincidan más en fechas recientes.

## Especialidades y archivos

El control adicional conserva 125 Subfields con 128 artículos en cada uno de los cinco períodos. Su cobertura no equivale a las 252 especialidades: las restantes siguen visibles como no elegibles en `period_coverage.csv`. La entrega incluye sus trayectorias con los mismos grupos y tamaños.

En estas especialidades, CKA media aumenta 0,01770 entre extremos y sube en 86/125 grupos. Los vecinos de 25 aumentan 1,29 puntos porcentuales y suben en 83/125. La tendencia media se mantiene en este control, con numerosas excepciones. No comparar directamente ese porcentaje de vecinos con universos de 2.048 o de todos los candidatos.

- Todas las trayectorias por área/par y coincidencia de signos entre controles: `data/robustness_v2/temporal_review/`.
- Consultas emparejadas y descomposición: `data/checklist_v1/candidate_check/` y `temporal_review/candidate_decomposition.json`.
- Tiempo por Subfield con tamaño fijo: `reports/robustness_v2/final/tables/subfield_time_fixed128.csv`.
- Figura con ambos signos de vecinos: `reports/robustness_v2/final/figures/04_time_controls.pdf`.

Los análisis temporales son descriptivos de este corpus y de estas versiones de modelos; no se entrenó un modelo diferente para cada fecha.

Tampoco disponemos de listas completas que permitan excluir cada artículo visto durante el entrenamiento de todos los modelos. La exposición previa puede diferir por fecha y disciplina. Por eso esta comparación no demuestra comportamiento sobre documentos nunca vistos ni separa ese efecto de una evolución histórica real.
