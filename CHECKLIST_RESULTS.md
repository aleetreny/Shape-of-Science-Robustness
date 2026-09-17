# Checklist terminada: texto, modelos, años y áreas

**17-09-2026. Los seis puntos están calculados y auditados.** La comparación original de 500.000 artículos se conserva. Se añadió un piloto de **26.000 artículos**, con 200 por área/período, en los diez modelos y las tres entradas. Entrega nueva: [resumen](reports/checklist_v1/final/summary.json), [auditoría](reports/checklist_v1/final/audit.json), 33 tablas y siete figuras en PDF/SVG/PNG.

**Lo más importante:** quitar el resumen puede cambiar el mapa tanto como cambiar de modelo. Quitar solo el título afecta menos, pero tampoco deja todos los vecinos iguales. La respuesta depende del modelo, de la receta y de qué parte del mapa medimos.

| Punto de la checklist | Resultado |
| --- | --- |
| Título / resumen / ambos | Tres entradas sobre los mismos 26.000 artículos; todas comprobadas. |
| Modelo frente a entrada | Comparados con las mismas filas, medidas y candidatos. Resultados por modelo y área. |
| Receta de los cuatro BERT | Se confirma **mean**, la media ya fijada antes de la primera comparación. CLS/SEP se conservan y se cruzan también con las entradas. |
| Tiempo | Cinco períodos completos; el signo de la tendencia de vecinos cambia según los candidatos disponibles. |
| Modelo por disciplina | Las 26 áreas; controles específicos de Medicina y los dos modelos biomédicos. |
| Familias | Grupos definidos por fuentes, comparación sistemática, omisión de modelos y controles de receta. Hay asociaciones y excepciones; no una causa única demostrada. |

## Cambiar de modelo frente a cambiar el texto

Partimos siempre de **título + resumen**. Esta tabla usa la receta principal y promedia por igual las áreas y los modelos. Cada área tiene los mismos 1.000 candidatos en todas las condiciones, con sus cinco períodos reunidos. No se mezcla con las búsquedas anteriores de 2.048 candidatos por área/período.

| Qué cambiamos | Cambio de forma: 1 − CKA | Vecinos que dejan de estar entre los 25 más cercanos |
| --- | ---: | ---: |
| Cambiar el modelo, conservando título + resumen | 0,369 | **16,2 de 25** |
| Conservar modelo y usar solo título | 0,366 | **16,7 de 25** |
| Conservar modelo y usar solo resumen | 0,027 | **5,0 de 25** |

La primera medida resume cambios de relaciones: más alto significa más cambio; **no es un porcentaje de ciencia correcta o incorrecta**. «Cambiar modelo» promedia los otros nueve modelos. La similitud de las dos primeras medias no es una prueba de equivalencia, y esconde diferencias entre modelos.

En la comparación de forma, quitar el resumen cambia menos que cambiar de modelo en SPECTER, SPECTER2, SciNCL, MPNet y MiniLM, al promediar áreas. Cambia más en SciBERT, BERT, PubMedBERT, BioBERT y SimCSE. Esa división también aparece en sus medias de vecinos. No permite declarar un modelo mejor.

Conservar el resumen y quitar el título tiene un efecto menor que cambiar de modelo en las **260 combinaciones modelo–área**; esto también se mantiene con CLS y SEP, tanto en forma como en vecinos. Sin embargo, perder unos cinco vecinos de 25 en la receta principal no es un efecto nulo.

[Figura por modelo](reports/checklist_v1/final/figures/01_model_versus_input.pdf) · [tabla completa](reports/checklist_v1/final/tables/input_effects_by_model.csv) · [tabla por área](reports/checklist_v1/final/tables/input_effects_by_field.csv).

## La receta queda cerrada, con sus límites visibles

**Mean sigue siendo la principal.** Resume las posiciones del texto que no son relleno, incluidos símbolos especiales. Era la regla común fijada antes del primer análisis; conservarla evita escoger después la variante que dé el resultado más cómodo. No significa que sea la mejor representación semántica posible.

El cruce nuevo confirma que la receta modifica las cifras. Por ejemplo, con mean quitar el resumen pierde 66,6% de vecinos frente a 64,9% al cambiar de modelo. Con CLS el orden se invierte: 69,8% frente a 72,8%; con SEP, 67,3% frente a 69,2%. Por ello **no afirmaremos que uno de los dos cambios siempre domina**. Quitar solo el título sigue teniendo un efecto claramente menor en las tres recetas.

[Figura del cruce entrada–receta](reports/checklist_v1/final/figures/07_input_by_pooling_recipe.pdf). Los otros seis modelos permanecen iguales y se reutilizan los vectores guardados; no se añadieron modelos nuevos.

## Tiempo: un cambio pequeño cuyo signo exige controlar la búsqueda

Estas cifras reutilizan el análisis de los 500.000, con igual peso por área y pareja de modelos. Son **medias**, no las medianas de algunas tablas de la entrega anterior.

| Período | Acuerdo de forma, CKA | Vecinos compartidos: todos los candidatos disponibles | Vecinos compartidos: 2.048 candidatos iguales |
| --- | ---: | ---: | ---: |
| 2000–04 | 0,628 | 30,66% | 31,41% |
| 2005–09 | 0,631 | 30,60% | 31,77% |
| 2010–14 | 0,633 | 30,35% | 31,92% |
| 2015–19 | 0,642 | 30,04% | 31,88% |
| 2020–24 | 0,649 | 29,79% | 32,32% |

La forma aumenta ligeramente: +0,0207; con la criba de calidad, +0,0115. No aumenta en todas las áreas y parejas ni todos los pasos son ascendentes.

En vecinos, el cambio entre extremos es **−0,87 puntos** con todos los candidatos y **+0,91 puntos** con 2.048. Comprobamos además exactamente las mismas consultas: frente a todos los candidatos el cambio sigue siendo −0,90 puntos; con candidatos limitados pasa a +0,91. La inversión también aparece con 10 y 50 vecinos. Esta comprobación adicional se añadió después de observar el primer cambio de signo.

Esto describe cómo se comportan nuestros modelos actuales con publicaciones de distintas fechas. **No demuestra una convergencia histórica causal de la ciencia.**

[Figura temporal](reports/checklist_v1/final/figures/02_time_and_candidate_size.pdf) · [comprobación con consultas idénticas](reports/checklist_v1/final/tables/paired_candidate_time.csv).

## Medicina: el menor acuerdo de forma no equivale al peor resultado en todo

| Área | Acuerdo de forma, media CKA | Vecinos compartidos, candidatos iguales |
| --- | ---: | ---: |
| Medicina | 0,554 | 29,82% |
| Energía | 0,783 | 33,97% |
| Física y astronomía | 0,667 | 33,27% |
| Matemáticas | 0,671 | 29,14% |

Medicina tiene la menor CKA media con la receta principal, y sigue así tras la criba de calidad. En vecinos con candidatos iguales queda quinta por abajo entre las 26 áreas: Matemáticas tiene algo menos acuerdo. No hay un único orden válido para todas las medidas.

BioBERT y PubMedBERT **se parecen bastante entre sí en Medicina**: CKA 0,838 y 54,8% de vecinos compartidos. Al retirar ambos, los otros 28 pares siguen teniendo menor forma en Medicina que en Energía: 0,571 frente a 0,787. No podemos culpar de toda la diferencia a los biomédicos.

Una pista es la amplitud de las áreas. En nuestra muestra, el Subfield más frecuente concentra aproximadamente 11,4% de Medicina y 73,8% de Energía, promediando períodos. La asociación entre diversidad de Subfields y acuerdo es negativa, pero moderada. **Es una hipótesis de composición, no una explicación causal demostrada**, y la clasificación OpenAlex tampoco es una verdad externa.

[Figura de los biomédicos](reports/checklist_v1/final/figures/03_medicine_and_biomedical_models.pdf) · [26 áreas](reports/checklist_v1/final/tables/field_summary_means.csv) · [diferencias de cada modelo por área](reports/checklist_v1/final/figures/05_model_by_field_residuals.pdf).

## Familias: hay parecidos y excepciones

Los grupos amplios de entrenamiento comparten más acuerdo en promedio: CKA **0,759 dentro** frente a **0,592 entre grupos**; vecinos **43,2% frente a 27,7%**. Se ponderan parejas, no tres familias del mismo tamaño. Compartir grupo de entrenamiento tiene una asociación más estable que compartir la etiqueta amplia «científico», «biomédico» o «general».

Hay dos límites importantes. MPNet/MiniLM/SimCSE son menos uniformes: su acuerdo interno de forma es 0,649, menor que el 0,675 entre ese grupo y los tres modelos guiados por citas. Además, el ajuste de familias cambia mucho con SEP: la proporción de variación entre los 45 promedios de parejas descrita por la regresión pasa de 0,399 con mean a 0,027. No equivale a un porcentaje de ciencia explicado ni demuestra un mecanismo de entrenamiento.

Las 45 parejas comparten modelos. Se usaron permutaciones de nombres y omisiones de modelos como referencias; no errores estándar que finjan independencia. Con SEP, omitir SimCSE no permite separar coeficientes: se declara, sin inventarlos. «Mismo objetivo» es una agrupación operativa amplia, no identidad de la función matemática. MPNet y MiniLM incluyen textos científicos: general no significa sin ciencia.

[Figura de familias](reports/checklist_v1/final/figures/04_training_objective_families.pdf) · [procedencia de los modelos](research/checklist_2026-09-17/MODEL_PROFILES.md) · [métodos precisos](METHODS_CHECKLIST.md).

## Decisión sobre ampliar el piloto

**No recalcular ahora las otras dos entradas sobre los 500.000.** Los 52 resúmenes de área —dos cambios de entrada por 26 áreas— superan la comprobación de estabilidad del contraste de forma. A nivel de modelo y área pasan 489 de 520; quedan **31 alertas de amplitud en 17 áreas**, con todos los cambios de mediana por debajo del límite. Se conservan la [tabla completa](reports/checklist_v1/final/tables/input_stability.csv) y las [31 alertas](reports/checklist_v1/final/tables/input_stability_alerts.csv). La [figura](reports/checklist_v1/final/figures/06_input_pilot_stability.pdf) muestra los resúmenes de área. Esta comprobación no demuestra por sí sola estabilidad de vecinos ni precisión poblacional.

El piloto permite sostener estos patrones generales dentro del corpus y los modelos estudiados. No justifica afirmar diferencias pequeñas en cada caso ni precisión sobre toda la población. Si el manuscrito necesita una de esas comparaciones finas, se ampliará de manera dirigida. Las **50 alertas de la fase anterior** siguen vigentes por separado; no se han borrado ni declarado resueltas.

## Qué queda preparado

- Tres entradas completas, identidades/textos/tokens comprobados y 260.000 filas modelo–artículo reutilizadas bit a bit; 520.000 nuevas. Los cuatro BERT conservan todas sus recetas.
- Siete pruebas matemáticas y de flujo, pruebas reales de los diez modelos y 14.040 consultas de vecinos del piloto contrastadas de forma independiente. El control de recetas reproduce la principal, con error máximo de CKA menor de 0,000000000001 y coincidencia exacta de vecinos.
- Siete figuras inspeccionadas, 33 tablas, catálogo de huellas, métodos y decisiones. No quedan cálculos activos de esta checklist.

La entrada compara usos habituales: al cambiar modelo cambian también sus reglas de lectura; al quitar un campo puede cambiar cuánto texto cabe. No es una separación causal perfecta entre arquitectura y contenido. El control anterior de texto común aporta contexto, pero no convierte estos efectos en factores puros.

Siguiente paso: redactar con [PAPER_OUTLINE.md](PAPER_OUTLINE.md). Ya existen comparaciones de título/resumen y mapas científicos; la [nota de antecedentes](research/checklist_2026-09-17/RELATED_INPUT_WORK.md) precisa el alcance. La contribución debe ser **qué conclusiones resisten las decisiones de representación**, sin proclamar prioridad absoluta o un modelo ganador.

Reconstrucción de la entrega, sin repetir inferencia o vecinos:

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_followup.report --require-complete
```
