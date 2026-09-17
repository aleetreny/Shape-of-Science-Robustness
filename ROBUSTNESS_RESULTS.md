# Qué hemos aprendido al ampliar las comprobaciones

**Revisión posterior de esta entrega:** [PREPAPER_REVIEW.md](PREPAPER_REVIEW.md) añade comprobaciones independientes, casos concretos y errores de clasificación de OpenAlex confirmados en la fuente. Las cifras de este informe se conservan; deben interpretarse con esos límites y con el [atlas](CASE_ATLAS.md).

**17-09-2026. Ampliación terminada y auditada, incluidas las 100 selecciones en ambos tamaños.** Corpus original de 500.000 intacto. Tres entradas en 52.000 artículos, diez modelos, 26 áreas y 252 especialidades con cobertura explícita. Esta entrega amplía las fases anteriores; no es el manuscrito.

**La conclusión central es que importa tanto la cámara como qué le enseñamos y dónde acercamos la lupa.** Hay estructura compartida, pero las coincidencias no son uniformes por artículo, especialidad, receta o tipo de texto.

## Quitar el resumen tiene un efecto medio parecido a cambiar de modelo

Muestra anidada: 400 artículos de cada área y período, manteniendo los 26.000 del piloto. Las 30 condiciones están auditadas: 1.560.000 combinaciones modelo–artículo–entrada; dos tercios reutilizados exactamente y un tercio calculado nuevo. Todos los modelos reciben los mismos artículos dentro de cada comparación.

| Cambio desde título + resumen | Cambio de forma: 1 − CKA | Vecinos de 25 que cambian |
| --- | ---: | ---: |
| Cambiar de modelo y conservar el texto | 0,3700 | 68,76% |
| Conservar el modelo y dejar solo título | 0,3658 | 70,67% |
| Conservar el modelo y dejar solo resumen | 0,0269 | 22,12% |

Promedios equilibrados entre 26 áreas y los diez modelos fijados. **No son porcentajes de ciencia incorrecta.** Los vecinos se buscan entre 2.000 candidatos por área. Eliminar el resumen tiene un impacto medio parecido al cambio de modelo; eliminar solo el título tiene menor impacto. No implica que cada modelo/área se comporte igual ni que un abstract solo sea la mejor entrada para cualquier tarea.

Las diferencias de receta se conservan completas. Mean sigue siendo principal para los cuatro BERT de palabras; CLS y SEP son controles. [Significado exacto y trazabilidad](POOLING.md). No escogemos después la receta que haga coincidir más a los modelos.

La media oculta dos comportamientos. Con mean, dejar solo título cambia más la forma que cambiar modelo en los promedios de los cuatro BERT de palabras y SimCSE; sucede lo contrario en SPECTER, SPECTER2, SciNCL, MPNet y MiniLM. Son descripciones de estos modelos, no una regla universal de familias.

La receta también cambia el orden de los efectos locales: con mean, título solo cambia 70,67% de vecinos frente a 68,76% por cambiar modelo; con CLS, son 73,56% frente a 76,60%; con SEP, 71,22% frente a 72,93%. Por eso no concluimos que el texto o el modelo «gane» siempre. La receta de los cuatro BERT de palabras se cambia a la vez en esos escenarios; los otros seis modelos permanecen fijos.

## Más detalle no significa siempre menos acuerdo

Los centros de las grandes áreas muestran mucho acuerdo. Al mirar los artículos aparecen diferencias, pero **no hay una caída universal al pasar de área a especialidad**.

Con las mismas consultas, 256 candidatos y fechas iguales, la coincidencia de 25 vecinos pasa en media de 46,69% buscando dentro del área a 45,34% dentro de la especialidad. Baja en 127 de 217 especialidades y sube en 90. Con 50 vecinos la dirección se reparte casi por mitad. El tamaño de búsqueda explica parte de las diferencias entre porcentajes de distintos análisis.

Ya hay resultados por los 500.000 IDs y un control repetido de candidatos para 10.850 consultas. Los pequeños grupos y valores no calculables siguen visibles. [Escalas, regiones y cobertura](SCALES_AND_DISCIPLINES.md).

## Tiempo, Medicina y familias

| Pregunta | Respuesta comprobada |
| --- | --- |
| ¿Coinciden más en fechas recientes? | La forma sube entre extremos en 24/26 áreas con tamaños iguales, pero solo cuatro suben en todos los pasos. Para vecinos, el signo cambia si no igualamos candidatos. [Detalle](TEMPORAL_REVIEW.md). |
| ¿Medicina discrepa solo por la mezcla de especialidades? | Reequilibrarlas apenas cambia su resultado. Retirar los dos modelos biomédicos mejora algo el acuerdo, pero no elimina la diferencia de forma. No se ha identificado una causa única. [Control](SCALES_AND_DISCIPLINES.md). |
| ¿Los modelos forman familias claras? | Hay asociaciones con entrenamiento y linaje, pero la lectura cambia con la receta. Los diez modelos no permiten aislar arquitectura, corpus y dominio como causas independientes. [Detalle](MODEL_FAMILIES.md). |
| ¿Hace falta otra medida de geometría? | Mantenemos CKA corregida y vecinos; Procrustes, rangos y otros tamaños de vecindario comprueban la sensibilidad. No añadimos morfología para acumular indicadores. [Decisión](METRICS.md). |

## Qué sigue siendo menos preciso

Con 100 selecciones comparables, las alertas de entradas bajan de **72/520 en 26k a 5/520 en 52k**. Las cinco se deben a una variación de selección mayor que el límite fijado; no se cambió ese límite. Pasan los 52 promedios de área, aunque en seis su rango todavía incluye cero: superar la regla no demuestra que modelo o texto domine claramente.

La comparación histórica con 20 selecciones se reproduce: 31 → 4, con tres persistentes, 28 que desaparecen y una nueva. Aumentar las repeticiones descubre más variación en las colas; no significa que los datos hayan empeorado. De las 31 claves originales, cuatro siguen alertadas al usar 52k y 100 selecciones. La quinta actual es otra clave. [Tabla completa y casos](SAMPLING_STABILITY.md).

Las 50 alertas originales se conservan, igual que las de especialidades. Las selecciones describen variación dentro del corpus fijo; no son intervalos de confianza sobre toda la ciencia. Un grupo donde se seleccionan todos los artículos tiene rango nulo por construcción, no certeza poblacional. [Reglas y límites](SAMPLING_STABILITY.md).

El texto común, MiniLM 512 y los filtros estrictos cambian algunas cifras; la receta puede cambiar bastante la interpretación. La [matriz de conclusiones y controles](CONCLUSION_CONTROLS.md) distingue qué se sostiene, qué cambia y qué no se cruzó por completo. No proclamamos un modelo ganador por consenso.

## Qué puede aportar el paper

Ya existen comparaciones de modelos mediante forma, vecinos y familias. Nuestra aportación defendible es **localizar qué relaciones científicas resisten decisiones razonables y cuáles dependen de ellas**, distinguiendo niveles, entrada, receta, fechas y composición. La revisión incluye los cinco antecedentes pedidos y trabajos cercanos de 2025–2026, con acceso y solapamientos explícitos: [antecedentes actualizados](research/robustness_2026-09-17/RELATED_WORK_UPDATE.md).

Las etiquetas OpenAlex no son verdad temática externa; desconocemos el solapamiento exacto con los corpus de entrenamiento. La población está delimitada por idioma, tipos, fechas y disponibilidad de abstract. No afirmar prioridad absoluta, representatividad mundial o evolución histórica causal.

## Archivos para continuar

- [Métodos y reproducción](METHODS_ROBUSTNESS.md); [protocolo](ROBUSTNESS_PROTOCOL.md); [requisitos R01–R12](ROBUSTNESS_SCOPE.md).
- Datos y controles: `data/robustness_v2/`. Las fuentes, selecciones y huellas quedan junto a cada cálculo.
- [Presentación integrada](reports/robustness_v2/final/): 50 tablas, siete figuras en PDF/SVG/PNG, resumen y catálogo con huellas. Las siete figuras fueron inspeccionadas. [Comparación de entradas](reports/robustness_v2/final/figures/01_input_effect.png) y [seguimiento de alertas](reports/robustness_v2/final/figures/07_input_alerts.png).
- Originales y versiones verificadas: `data/robustness_v2/provenance/`. 6.139 respuestas únicas de OpenAlex, corpus original/limpio y vectores de diez modelos conservados.

La auditoría conjunta verifica 15 componentes, las selecciones reales y sus cuotas, los 500.000 IDs y las copias/huellas de programas. Pasaron doce pruebas de análisis y tres de preparación de entradas, además de las comprobaciones independientes sobre datos reales. Evidencia: `data/robustness_v2/final_audit/` y `research/robustness_2026-09-17/closure_audit.json`. Los cálculos están terminados.

No hace falta ampliar automáticamente las entradas a 500.000 para cerrar este objetivo. Las diferencias finas con alertas se presentan como límites, no se ocultan ni se declaran resueltas por escoger otra receta.
