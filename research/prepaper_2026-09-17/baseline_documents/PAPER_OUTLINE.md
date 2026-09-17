# Cómo presentar el trabajo a QSS

Esquema actualizado con la ampliación a 52.000 entradas y los controles de especialidades del 17-09-2026. Es una propuesta de organización; **no es un manuscrito ni un envío**. La evidencia vigente está en [ROBUSTNESS_RESULTS.md](ROBUSTNESS_RESULTS.md), que amplía las dos entregas anteriores. La auditoría y el estado de cierre se consultan en [NEXT_STEPS.md](NEXT_STEPS.md).

## Pregunta y aportación

**¿Qué relaciones del mapa de la ciencia se conservan al cambiar cómo representamos los mismos artículos?**

Título de trabajo: **How much of a map of science survives a change of embedding model?**

La analogía es mirar mapas con cámaras distintas y a distintas distancias. Las cámaras pueden coincidir en dónde están las grandes áreas y discrepar sobre los vecinos de un artículo. También importa cuánto texto les mostramos y cómo resumimos lo que leen.

La contribución defendible es localizar relaciones resistentes y relaciones dependientes de decisiones razonables, distinguiendo entrada, receta, nivel, fechas y candidatos. **Comparar modelos mediante CKA, vecinos o familias no es una novedad por sí sola.** Caspari y otros antecedentes ya combinan varios de esos componentes. La [revisión actualizada](research/robustness_2026-09-17/RELATED_WORK_UPDATE.md) compara expresamente los cinco trabajos pedidos y estudios próximos de 2025–2026. No afirmar prioridad absoluta.

## Orden del argumento

1. **Mismos artículos, condiciones trazables.** 500.000 registros, diez modelos, 26 áreas y cinco períodos; distinguir 400.000 base y 100.000 complemento. Experimento de tres entradas en 52.000, 400 por área/período, que contiene los 26.000 del piloto. El control de texto común tiene otra selección de 52.000 y otra pregunta.
2. **Estructura amplia compartida, detalle variable.** Comparar centros, organización interna y vecinos como objetos distintos. Los grupos reales superan referencias aleatorias; los controles de tamaño no apoyan una caída universal de acuerdo al pasar de Field a Subfield.
3. **El texto puede importar tanto como el modelo.** Con mean principal, cambiar modelo, quitar resumen y quitar título cambian respectivamente 68,76%, 70,67% y 22,12% de los 25 vecinos. CKA muestra un contraste similar entre quitar resumen y cambiar modelo. Las medias cercanas no prueban equivalencia; hay diferencias por modelo/área y el pequeño orden local se invierte con CLS/SEP.
4. **El universo de comparación importa.** Con las mismas consultas, 256 candidatos y fechas iguales, el acuerdo baja en promedio 1,35 puntos al buscar dentro del Subfield; baja en 127/217 y sube en 90. El signo temporal de vecinos también depende del tamaño de búsqueda. No comparar porcentajes de búsquedas distintas como si tuvieran el mismo denominador.
5. **Explicaciones parciales, límites claros.** Equilibrar la composición de Medicina cambia poco su acuerdo; retirar biomédicos no elimina su diferencia de forma. Objetivo y linaje se asocian al acuerdo, pero los diez modelos no separan causalmente arquitectura, corpus y dominio. La receta altera esa lectura.
6. **Estabilidad y decisiones que sí cambian conclusiones.** Mostrar alertas y todos los controles, incluidos resultados que contradicen una historia sencilla. Las selecciones son variaciones dentro de un corpus fijo, no intervalos poblacionales.

## Cuatro figuras principales propuestas

| Orden | Mensaje | Figura |
| --- | --- | --- |
| 1. Estructura amplia y organización interna | Un mapa amplio compartido no garantiza el mismo detalle; referencia aleatoria y tamaño explícitos. | [02_scales.pdf](reports/robustness_v2/final/figures/02_scales.pdf) |
| 2. Modelo frente a entrada | Distribución entre áreas del cambio por modelo, título solo y resumen solo. | [01_input_effect.pdf](reports/robustness_v2/final/figures/01_input_effect.pdf) |
| 3. Vecinos con condiciones comparables | La media baja algo al pasar a especialidades, con muchas excepciones. | [03_paired_neighbors.pdf](reports/robustness_v2/final/figures/03_paired_neighbors.pdf) |
| 4. Tiempo y candidatos | Los promedios temporales cambian de lectura al controlar el universo de búsqueda. | [04_time_controls.pdf](reports/robustness_v2/final/figures/04_time_controls.pdf) |

Pies que deben acompañarlas:

- Figura 1: izquierda, 256 artículos por centro y grupos aleatorios con fechas/tamaños conservados; 26 centros de especialidades controla su número. Derecha, mismos 183 Subfields elegibles en los tres tamaños y las 26 áreas. Centros e interior son objetos diferentes; CKA no es porcentaje de ciencia correcta. La referencia de grupos compartidos no equivale a barajar identidades entre modelos.
- Figura 2: 52.000 IDs, diez modelos fijos y 2.000 candidatos por área reuniendo períodos. Cada punto resume un área; su dispersión no es un intervalo de confianza. Las entradas usan límites habituales, por lo que el contenido y el recorte efectivo no se aíslan perfectamente. Mostrar el cruce completo de recetas en suplemento.
- Figura 3: 217 Subfields, 50 consultas fijas por grupo, diez selecciones de 256 candidatos, mismas cuotas de fechas en ambos ámbitos, k=25. Las 10.850 consultas no equivalen a repetir candidatos para los 500.000 artículos. Con k=50 la dirección se reparte casi por mitad.
- Figura 4: forma con tamaños iguales aumenta entre extremos en 24/26 áreas, pero solo cuatro crecen en todos los pasos. Vecinos cambia −0,87 puntos con todos los candidatos y +0,91 con 2.048. Separar el pequeño efecto de consultas del cambio de candidatos. Controles posteriores al resultado inicial, sin conclusión histórica causal.

## Tablas y suplemento

Tablas principales: corpus y cobertura; versiones/formatos/recetas de los diez modelos; matriz de conclusiones y controles. Usar [CONCLUSION_CONTROLS.md](CONCLUSION_CONTROLS.md) para no afirmar que se ejecutaron cruces que no existen. Hay 18 variantes originales, no 18 modelos independientes.

Las tres figuras nuevas restantes presentan [Medicina](reports/robustness_v2/final/figures/05_medicine_composition.pdf), [recetas y familias](reports/robustness_v2/final/figures/06_recipe_families.pdf) y [alertas de entradas](reports/robustness_v2/final/figures/07_input_alerts.pdf). La tabla de estabilidad debe acompañar siempre al gráfico: más repeticiones pueden descubrir colas que 20 no mostraban.

Las quince figuras de `reports/analysis_v1/final/` y `reports/checklist_v1/final/` se conservan como evidencia anterior. Priorizar en suplemento la matriz de diez modelos, asociación forma/vecinos, MiniLM/texto común, recetas, calidad y cobertura. Identificar siempre las figuras del piloto de 26k; no presentarlas como resultados de 52k. No es necesario incluir todas las figuras en el manuscrito.

Tablas completas y resultados por artículo están en [DATA_CATALOG.md](DATA_CATALOG.md). [POOLING.md](POOLING.md) documenta mean/CLS/SEP; [SAMPLING_STABILITY.md](SAMPLING_STABILITY.md) separa las 50 alertas originales, las de entrada y las de especialidades. En grupos donde se selecciona todo, rango cero no significa certeza sobre la población.

## Interpretación que debe mantenerse

No elegir un modelo ganador por consenso. No interpretar las etiquetas de OpenAlex como verdad temática independiente. No sumar escalas distintas para obtener un porcentaje único de «ciencia conservada». Los 45 pares comparten modelos y no son independientes; las asociaciones de familias no identifican causas. El entrenamiento puede incluir documentos del período estudiado y no conocemos su solapamiento exacto.

La igualdad de tamaños y composición limita ciertas explicaciones, pero no convierte el análisis en una intervención causal. Medicina no ocupa el último lugar en todas las medidas. Calidad y deduplicación se comprobaron conjuntamente, sin aislar cada filtro. Las nuevas sensibilidades se diseñaron con conocimiento de fases anteriores; no llamarlas un registro previo ciego.

No añadimos dispersión, dimensión intrínseca o conectividad para acumular indicadores. Son preguntas diferentes; la decisión y las comprobaciones de las medidas actuales están en [METRICS.md](METRICS.md).

## Continuación

Con R01–R12 verificados, el siguiente encargo puede ser redactar usando [METHODS_ROBUSTNESS.md](METHODS_ROBUSTNESS.md) y los dos métodos anteriores. No ampliar automáticamente las entradas a 500.000 ni repetir inferencia por abrir otro chat. Un análisis adicional debe responder a una afirmación esencial todavía insuficientemente apoyada.

Los datos grandes permanecen locales; preparar su distribución, redactar el manuscrito y enviarlo son tareas posteriores. No se han realizado ni se asumen autorizadas por esta entrega.
