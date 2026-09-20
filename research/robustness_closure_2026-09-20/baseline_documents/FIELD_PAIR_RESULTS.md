# Qué conclusiones sobre disciplinas se conservan

**Resumen final terminado, 18-09-2026.** La inversión entre Medicina y Artes no era un caso aislado. Al comparar todas las parejas de áreas, muchas relaciones cambian de dirección según el modelo, incluso cuando cada modelo repite su conclusión al cambiar los artículos. La magnitud importa: parte de esas diferencias es pequeña.

Se reutilizaron las medidas guardadas. No hubo descargas, nuevos embeddings ni recálculo de la morfología. Los diez modelos, las recetas principales y las 26 áreas se mantienen. Los resultados describen este corpus y este panel; no toda la ciencia ni cualquier modelo posible.

## Las 325 parejas, completas

Para cada pareja preguntamos qué área tiene mayor apertura o mayor reparto entre direcciones. Exigimos que cada modelo mantenga su respuesta en el resultado principal y las **25 selecciones adicionales**: veinte medias muestras y cinco selecciones del mismo corpus de 500k.

| Resultado por pareja | Apertura de la nube | Reparto entre direcciones, PR |
| --- | ---: | ---: |
| Los diez mantienen la misma dirección | **42 / 325 (12,9%)** | **54 / 325 (16,6%)** |
| Hay modelos con direcciones opuestas que persisten | **262 / 325 (80,6%)** | **221 / 325 (68,0%)** |
| No queda una conclusión común clara | **21 / 325 (6,5%)** | **50 / 325 (15,4%)** |

«Direcciones opuestas» significa que al menos un modelo mantiene A>B y otro mantiene B>A; **no significa que los diez discrepen entre sí**. En el tercer grupo también entran acuerdos parciales: no es una prueba de empate ni de ausencia de diferencia. El acuerdo de todos tampoco identifica la descripción temáticamente correcta.

Una respuesta constante en estas muestras no garantiza una diferencia grande. [Tabla completa](reports/field_pair_summary_v1/pair_summary.csv) y [mapa de las 325 parejas](reports/field_pair_summary_v1/02_all_field_pairs.png).

## Separar diferencias pequeñas y grandes

La tabla siguiente vuelve a contar contradicciones exigiendo una diferencia mínima **en todas las selecciones de cada modelo testigo**, con signos opuestos entre ambos. El porcentaje se calcula respecto al promedio de los valores de las dos áreas, no como porcentaje de artículos ni de «ciencia equivocada».

| Diferencia mínima exigida | Apertura: parejas con contradicción | PR: parejas con contradicción |
| --- | ---: | ---: |
| Cualquier diferencia de dirección persistente | 262 / 325 | 221 / 325 |
| Más del 1% | 238 / 325 | 213 / 325 |
| Más del 5% | **96 / 325 (29,5%)** | **177 / 325 (54,5%)** |
| Más del 10% | 19 / 325 | 126 / 325 |

Los cortes se fijaron antes de calcular este resumen, como comprobaciones, **sin declarar que 5% sea el umbral científicamente correcto**. Los casos que no pasan permanecen en el denominador. La cifra grande de apertura debe acompañarse de esta sensibilidad: no sería honesto presentar las 262 inversiones como diferencias grandes.

[Figura principal propuesta](reports/field_pair_summary_v1/01_conclusions_and_magnitude.png), [los tres resultados bajo todos los cortes](reports/field_pair_summary_v1/classification_summary.csv) y [cada pareja bajo cada regla](reports/field_pair_summary_v1/pair_sensitivity.csv).

## No depende solo de una medida ni de los cuatro BERT

Al exigir que **los mismos modelos** conserven sus direcciones con las otras medidas de esa propiedad, quedan **225 parejas contradictorias en apertura y 196 en PR**. Si además exigimos más del 5% en la medida principal, quedan 95 y 159. No se cambian los modelos testigo para cada medida.

Las alternativas de apertura tienen las 25 repeticiones completas. Entropía/D80 solo tienen el principal y una repetición de cada diseño: la comprobación es más limitada y D80 admite empates. Son descripciones relacionadas, no tres validaciones independientes de significado. [Resultados](reports/field_pair_summary_v1/alternative_support.csv).

Al conservar solo los seis modelos entrenados para similitud de textos —SPECTER, SPECTER2, SciNCL, MPNet, MiniLM y SimCSE—, quedan **231/325 contradicciones de apertura y 160/325 de PR**; al exigir más del 5%, 80 y 114. Por tanto, el fenómeno también aparece en ese grupo. Tener menos modelos reduce las oportunidades de oposición: esto no demuestra que un tipo de entrenamiento sea la causa de la diferencia.

Al retirar cada modelo por turno, las contradicciones oscilan entre 234–262 en apertura y 206–221 en PR. No dependen de un único modelo. [Paneles completos](reports/field_pair_summary_v1/model_panel_summary.csv). Entre las parejas de áreas contradictorias, la mediana es de 15 pares de modelos opuestos de los 45 posibles en apertura y 12 en PR; son pares que comparten modelos, no observaciones independientes.

## Qué controles conservan las contradicciones

Se comprueba si siguen presentes **los mismos modelos testigo y sus signos**, tanto en la referencia emparejada como en la variante. Estos controles son puntuales: no tienen sus propias 25 repeticiones.

| Comprobación | De las 262 contradicciones de apertura | De las 221 de PR |
| --- | ---: | ---: |
| El mismo fragmento de texto para todos | 262 conservadas | 216 conservadas |
| Reposición por las marcas de calidad ya existentes | 262 | 221 |
| Usar 4.000 artículos por área | 262 | 221 |
| Solo resumen | 262 | 221 |
| Solo título | 246 | 193 |
| Cambiar a CLS los cuatro BERT | 253 | 210 |
| Cambiar a SEP los cuatro BERT | 257 | 201 |
| Quitar la dirección común del modelo y normalizar | **145** | **218** |

El último control cambia especialmente la apertura. **No es una propiedad independiente de cómo se construye la representación.** Que desaparezca una contradicción bajo un control no significa que se haya encontrado la representación correcta. Tampoco sería justo conservar solamente los controles favorables.

Los controles de calidad no validan las etiquetas de OpenAlex. Se mantienen los errores de fuente detectados, las cuatro alertas previas de PR y las demás alertas históricas. [Los once controles completos](reports/field_pair_summary_v1/control_summary.csv), [detalle por pareja](reports/field_pair_summary_v1/control_pairs.csv).

## También hay relaciones resistentes

Con las recetas principales, los diez modelos sitúan la apertura de **Odontología por debajo de otras 24 áreas**; la comparación restante no queda resuelta con esta regla. En PR, los diez sitúan **Energía por debajo de otras 22 áreas**. Eso no convierte a esas disciplinas en más simples ni cuenta su número de temas. Las recetas y alternativas pueden cambiar esas descripciones, como mostró el piloto.

El ejemplo conocido Medicina/Artes conserva contradicción en ambas propiedades y al exigir más del 5%. En apertura, seis modelos mantienen Medicina por encima, tres por debajo y uno queda sin dirección resuelta. El ejemplo sigue siendo ilustrativo, seleccionado después del piloto; ahora lo acompaña el universo completo. [Ejemplo trazable](reports/field_pair_summary_v1/example_art_medicine.csv), [resumen por área](reports/field_pair_summary_v1/field_summary.csv).

## Qué aporta al paper y dónde parar

La aportación se vuelve concreta: **cambiar de encoder puede invertir una afirmación comparativa sobre disciplinas, aun cuando repetir los artículos no la invierta**. Se puede mostrar dónde pasa, con qué magnitud y qué decisiones cambian esa lectura. Esto complementa las comparaciones anteriores de forma general y vecinos, sin afirmar que son una nueva técnica o que un modelo representa la ciencia correcta.

Recomendación de presentación: usar el gráfico de recuentos y magnitudes junto al ejemplo, y dejar el mapa completo de parejas y los controles detallados en material adicional. La organización final del manuscrito sigue por acordar con el usuario; [PAPER_OUTLINE.md](PAPER_OUTLINE.md) es una propuesta.

**Este cierre termina la ampliación experimental acordada.** No hace falta abrir ahora fragmentación, nuevos modelos o evolución causal. El corpus, las selecciones y los diez modelos delimitan la conclusión; las 325 parejas comparten disciplinas y no permiten contar 325 pruebas independientes. Las muestras repetidas no son intervalos poblacionales.

Registro y reproducción: [METHODS_FIELD_PAIRS.md](METHODS_FIELD_PAIRS.md), [protocolo](FIELD_PAIR_PROTOCOL.md) y [auditoría final](research/field_pair_summary_2026-09-18/closure_audit.json). No se ha redactado ni publicado el manuscrito.
