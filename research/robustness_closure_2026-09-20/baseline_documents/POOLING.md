# Qué significan mean, CLS y SEP en este proyecto

Son tres formas de convertir la salida de un modelo en una sola lista de números por artículo. Como resumir una página: podemos promediar todas sus posiciones o tomar una posición especial que el modelo ha actualizado al leerla.

**Principal para BERT, SciBERT, BioBERT y PubMedBERT: `mean`.** Ya se fijó antes del primer análisis. CLS/SEP son comprobaciones; no se elige después la que coincida más con los demás modelos. La ampliación a 52k conserva exactamente esta regla.

| Nombre | Operación exacta en el código | Qué no significa |
| --- | --- | --- |
| `mean` | Media de los estados de la **última capa** en todas las posiciones con máscara de atención 1. Incluye los símbolos especiales de inicio/final y cualquier separador presente. Excluye el relleno añadido al lote. | No es media solo de palabras, de capas o de los 500.000 artículos. |
| `CLS` / `cls` | Estado de la última capa en la posición 0, correspondiente al símbolo de inicio del tokenizador. | No usa `pooler_output`, la capa densa/tanh del pooler BERT ni una cabeza de clasificación. |
| `SEP` / `sep` | Estado de la última capa en la posición `attention_mask.sum() - 1`: último símbolo no rellenado, que aquí es el separador final. | No es el primer separador entre título y resumen ni la última palabra normal. |

Los tokenizadores tienen relleno a la derecha. Las tres recetas se extraen de la misma pasada, con el mismo texto y límite. Si hay recorte, el separador final sigue estando presente, pero el modelo no ha leído el texto que quedó fuera. Una posición especial no garantiza por sí sola una representación documental de buena calidad.

## Receta principal por modelo

| Modelo | Principal | Alternativas guardadas |
| --- | --- | --- |
| SPECTER | CLS | — |
| SPECTER2 | CLS, con adaptador de proximidad | — |
| SciNCL | CLS | — |
| SciBERT | Mean | CLS y SEP |
| BERT | Mean | CLS y SEP |
| MPNet | Mean | — |
| MiniLM | Mean | — |
| PubMedBERT/BiomedBERT | Mean | CLS y SEP |
| BioBERT | Mean | CLS y SEP |
| SimCSE | CLS | — |

Hay diez modelos y dieciocho salidas por condición, no dieciocho modelos independientes. Cambiar la receta de los cuatro BERT deja intacta la de los otros seis. No se entrena ninguna receta nueva.

## Texto y normalización

Los cuatro BERT combinan título y resumen mediante dos saltos de línea. El tokenizador añade los símbolos externos; en esa entrada no se añade un separador interior explícito. SPECTER/SPECTER2/SciNCL sí usan el separador de su tokenizador entre campos. Con solo título o solo resumen se envía el campo literal y se añaden los símbolos habituales del tokenizador, sin fabricar campos vacíos.

Los vectores se guardan sin normalizar, en `float32`. La comparación principal los divide después por su longitud; no se reescribe el almacenamiento. Media de **posiciones del texto**, normalización de **cada vector de artículo** y media de **artículos para un centro de área** son operaciones distintas.

## Trazabilidad y prueba

- Implementación congelada: [pool y Encoder](sos_embed/models.py). `pool` define las tres operaciones; el ejecutor entrega `last_hidden_state`.
- Versiones exactas, límites y formatos: [embeddings_v1.json](config/embeddings_v1.json).
- Decisión principal anterior: [analysis_v1.json](config/analysis_v1.json). La ampliación conserva el mismo mapa en [input52_v1.json](config/input52_v1.json).
- [pooling_trace.json](research/robustness_2026-09-17/pooling_trace.json): huellas del código/configuraciones, versiones, receta principal y ejemplos de las tres entradas con tokens y posiciones, comprobados en los diez tokenizadores locales.
- [test_deep_input52.py](tests/test_deep_input52.py): prueba con valores conocidos, dos longitudes y relleno, que distingue media, inicio y final. Verifica también la copia exacta de todas las recetas antiguas al ampliar la muestra.
- [input52_recipes_v1.json](config/input52_recipes_v1.json): cruce de entradas y recetas en 52k, terminado y auditado. Resultados y alcance en la sección de cierre siguiente.

La salida de cada modelo identifica el orden de IDs, huellas de texto/tokens, revisión de pesos y archivos de cada receta. Los manifiestos nuevos registran además de qué salida anterior procede cada copia. El auditor compara las copias bit a bit y vuelve a reconstruir los tokens.

## Cierre del cruce a 52k, 17-09-2026

El cruce de las tres entradas con mean/CLS/SEP terminó y fue auditado en `data/robustness_v2/input_recipes/`. Reproduce la principal y conserva 12.870 comparaciones de forma, 38.610 de vecinos y 6.240 contrastes de efectos. Para cada modelo, Field y entrada se puede localizar el cambio y su dirección.

La receta altera el resultado: al comparar título solo frente a cambiar modelo, la diferencia media de forma «efecto modelo menos efecto entrada» es +0,0042 con mean, +0,0363 con CLS y +0,0627 con SEP. En vecinos k25 cambia de −0,0191 con mean a +0,0304 con CLS y +0,0171 con SEP. No se elige una receta según el signo deseado.

Con título solo, el signo del contraste de forma cambia en 15/260 casos modelo×área al pasar de mean a CLS y en 20/260 al pasar a SEP. Dentro de los cuatro BERT de palabras, son 9/104 y 13/104. Con abstract solo no cambia el signo en estos controles, aunque sí cambia la magnitud. Las tablas `input_review/recipe_sensitivity_all_cases.csv` y `recipe_sign_changes.csv` conservan todos los casos; un cambio de signo cercano a cero no implica por sí mismo una diferencia importante ni una prueba estadística.

Mean se conserva por coherencia con el protocolo, trazabilidad y comparación completa; no porque haya demostrado ser semánticamente la mejor. *The landscape of biomedical research* eligió PubMedBERT-SEP para otra evaluación, con etiquetas derivadas de revistas. Ese antecedente no convierte SEP en la solución universal para nuestra pregunta.

Estos escenarios cambian las cuatro representaciones de palabras a la vez. El «efecto modelo» incluye compararlos con los otros nueve: puede cambiar también para un modelo cuya propia receta no cambie. La incertidumbre de 100 selecciones se calcula sobre el contraste principal mean; no se ha repetido todo ese remuestreo para CLS y SEP. Sus diferencias finas no reciben por defecto la misma garantía de selección.
