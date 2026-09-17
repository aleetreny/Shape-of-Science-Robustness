# Medidas que mantenemos y por qué

Decisión de cierre, 17-09-2026, dentro de la delegación actual. **Conservamos dos preguntas principales: cuánto se parece la organización general y cuántos vecinos conserva cada artículo.** No añadimos un índice geométrico nuevo en esta fase.

## Forma y vecinos

- **Forma: CKA lineal corregida.** Compara las relaciones de los mismos artículos, aunque los modelos usen distinto número de coordenadas. Vectores con longitud uno; centrado según la implementación congelada. La corrección reduce el acuerdo artificial asociado al tamaño y la dimensión. No da un porcentaje de ciencia correcta ni demuestra calidad semántica.
- **Detalle: vecinos por coseno exactos, k=25 principal.** Fracción de los 25 artículos próximos que se repiten entre dos modelos; sin incluir el propio artículo. k=10 y 50 comprueban dependencia del tamaño del vecindario. Se guarda también corrección respecto a selección aleatoria, y controles con candidatos, consultas y fechas iguales. El resultado depende del universo donde se busca.
- **Comprobaciones de forma:** Procrustes ortogonal y correlación de rangos de similitudes (RSA). Comprueban aspectos distintos. No se promedian con CKA ni se convierten en una puntuación total. RSA utiliza los pares comunes fijados por el programa. Procrustes se interpreta con especial cautela al comparar tamaños/dimensiones diferentes.

El orden de prioridad se conserva aunque una medida dé una historia menos vistosa. Las 45 parejas comparten modelos y no son observaciones independientes. Las medidas se calculan sobre los vectores originales transformados según protocolo, no sobre un dibujo 2D.

## ¿Coinciden las medidas?

Se ha reconstruido el acuerdo entre medidas por unidad, conservando todos los pares de modelos. La tabla muestra la mediana de la correlación de sus ordenaciones; **no es la similitud media entre modelos**.

| Unidad | CKA–Procrustes | CKA–rangos | Procrustes–rangos |
| --- | ---: | ---: | ---: |
| 130 áreas × períodos, originales | 0,884 | 0,881 | 0,795 |
| 251 especialidades con forma calculable, originales | 0,912 | 0,895 | 0,850 |
| Áreas, 256 artículos cada una | 0,926 | 0,886 | 0,867 |
| 217 especialidades, 256 artículos cada una | 0,928 | 0,892 | 0,896 |

Hay concordancia amplia, no identidad. Por ejemplo, Procrustes–rangos baja hasta 0,626 en una especialidad original. Los valores por grupo y controles de receta están en `data/robustness_v2/control_review_v2/metric_consistency_by_unit.csv`. No extrapolar el mínimo de una unidad a todo el corpus.

## Por qué no añadimos morfología ahora

La pregunta del paper es cuánto depende el mapa de la representación elegida. Las distancias relativas y los vecinos ya responden directamente a esa pregunta; tamaños, recetas, entradas, selección y grupos aleatorios comprueban sus principales puntos débiles.

Dispersión, dimensionalidad intrínseca y conectividad preguntarían respectivamente cuánto se extiende una nube, cuántas direcciones necesita y cómo se conecta bajo una regla concreta. Son propiedades diferentes. Añadirlas exigiría definir nuevas hipótesis, escalas y parámetros; no arregla por sí solo la estabilidad de una comparación. **No se han calculado ni se presentarán como resultados implícitos de CKA.**

La lectura de [Gröger et al., 2026](https://arxiv.org/html/2602.14486v2) refuerza corregir sesgos y fijar tamaños, no sumar métricas indiscriminadamente. [Shesha, versión 5 de julio de 2026](https://arxiv.org/html/2601.09173v5), mide una consistencia interna dependiente de coordenadas; no sustituye una comparación entre modelos que debe tolerar rotaciones. Los antecedentes locales y de forma quedan en [la revisión de literatura](research/robustness_2026-09-17/RELATED_WORK_UPDATE.md).

Esta decisión cierra la lista de medidas para esta fase. Una investigación futura sobre morfología deberá distinguir las tres propiedades y conservar este análisis como referencia, sin cambiar retrospectivamente el criterio principal.
