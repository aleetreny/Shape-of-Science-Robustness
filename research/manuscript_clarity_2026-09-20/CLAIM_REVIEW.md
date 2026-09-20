# Revisión de la explicación, 20-09-2026

Petición: adoptar la orientación de voz V2 y rehacer el recorrido para que se entienda sin conocer el proyecto. Esta revisión compara la nueva prosa con V2, los documentos científicos ya cerrados y las tablas incluidas. No es una nueva revisión por expertos ni una aprobación del autor.

## Qué cambia

La introducción parte del uso de un mapa y explica después cómo se convierte un texto en una posición. Las preguntas y los apartados de resultados usan acciones reconocibles. Los métodos presentan primero cada comparación y después su nombre técnico. El resumen ya no reúne siglas y recuentos de parejas sin explicación.

La primera persona es puntual, siguiendo V2. No se inventan experiencias o una historia de descubrimiento. Las ampliaciones siguen identificadas como posteriores y exploratorias. El título y las declaraciones se conservan literalmente en cada idioma.

## Correspondencia de afirmaciones

| Afirmación o límite | Dónde queda y qué se ha comprobado |
| --- | --- |
| Diez modelos, 500.000 registros, 26 áreas, 2000–2024 | Resumen, apertura, métodos y T01. El texto dice colección de partida; no afirma haber calculado las tres entradas sobre 500.000. |
| 400.000 generales + 100.000 de refuerzo | 3.1 y T01. Se mantienen los filtros, los 130 grupos y mínimo 2.165; sin atribuir representatividad mundial. |
| Tres entradas en 52.000 | 3.1, T01 y 4.3: 2.000 por área, 400 por período. Los 26.000 son la prueba anterior incluida en estos 52.000. S3 conserva ambas etapas y los controles de 20/100 selecciones. |
| Segundo conjunto de 52.000 | 3.1, 3.2, T01 y S1. El fragmento común usa otra selección; iguala contenido, no los tokens de distintos vocabularios. |
| Geometría por área | 4.4, T01 y S6–S7: reutiliza los 52.000 del experimento de texto con título y resumen. No es un tercer corpus descargado. |
| Modelos y combinación de salidas | 3.2, T02 y S1: diez modelos, dimensiones/límites y reglas sin cambios. Mean incluye símbolos especiales y excluye relleno; CLS antes del pooler y SEP final. No se elige por máximo acuerdo. |
| Recorte de MiniLM/MPNet | 49,58%/20,16%; MiniLM 256 principal y 512 control. No se presenta el límite original como fallo del programa ni la entrada larga como mejor verdad temática. |
| Centros y comparaciones internas | 3.3 y 4.1: 256 artículos por centro; 26/217/26 centros; dentro, 128/256/512 y las mismas 183 especialidades. Las cifras antes concentradas en T01 se explican en el texto. |
| Estructura general | 0,939/0,911/0,902 y referencia aleatoria 0,63–0,64; dentro 0,63/0,64. Conserva el límite: objetos diferentes, sin efecto causal aislado de escala. |
| Medidas de acuerdo | Se explica qué pregunta responde CKA antes de su nombre. No equivale a porcentaje correcto; su corrección no elimina todo sesgo. Procrustes/distancias y fórmulas permanecen en S2. |
| Alertas de estructura | 50/5.850 conservadas; correlaciones alternativas 0,891/0,881. No se borran por estabilidad de una media. |
| Vecinos | 30,3% se explica como unos ocho de 25, un redondeo, no ocho exactos. Permanecen 31,9% con 2.048 candidatos y 17,5% con 13.000 consultas en 400.000; no son diseños intercambiables. |
| Comparación de alcance | 217 × 50 = 10.850; 256 candidatos incluyen las mismas 50 consultas, varían otros 206 diez veces y se igualan fechas. No es una muestra libre del Field. |
| Resultado de alcance | 127 menores/90 mayores, media −1,35 puntos; con 50 vecinos, 109/108. No hay descenso universal. |
| Relación estructura–vecinos | 0,920 sigue siendo correlación de rangos entre 45 medias de parejas, no correlación de observaciones independientes ni prueba de corrección. |
| Entrada | Cambio de modelo 0,370/68,8%; solo título 0,366/70,7%; solo resumen 0,027/22,1%; MPNet 51,7%, SciBERT 84,2%. Medias parecidas no prueban equivalencia. |
| Cambio de pooling | La inversión con CLS/SEP descrita en 4.3 corresponde al orden de sustitución de vecinos, no se ha trasladado por error a CKA. Cambian cuatro representaciones y la referencia entre modelos. |
| Piloto y ampliación | 72→5 alertas de 520 con 100 selecciones se conserva en 4.3; el registro histórico 31→4 con 20 selecciones sigue en S3/S6 y Figura S1. No se intercambian. |
| Apertura y dimensión | Explicaciones geométricas, sin convertirlas en diversidad temática o número de temas. La fórmula PR pasa a S6 de forma explícita y equivalente, sin cambiarla. |
| 325 comparaciones | 3.5 explica que son todas las maneras de elegir dos de 26 áreas. 4.4 da ejemplo A/B antes de interpretar los recuentos. Las parejas no son independientes. |
| Dirección y magnitud | Apertura 42/262/21; PR 54/221/50. Oposición = al menos dos modelos fijos con sentidos persistentes contrarios en principal + 20 medias muestras + 5 selecciones. A 5% 96/177; a 10% 19/126. No resuelto no es igualdad. |
| Alternativas y conjunto de modelos | 225/262 y 196/221 exigen los mismos modelos opuestos y sus direcciones; cobertura 26 frente a 3 selecciones. Seis modelos 231/160; menos oportunidades de oposición, sin conclusión causal sobre entrenamiento. |
| Centrado y pooling | 145/262 y 218/221 conservan los mismos modelos y direcciones en controles puntuales; no son otras 26 repeticiones confirmatorias. |
| PR y conexión | Cuatro alertas de PR en medias muestras no desaparecen por ausencia en cinco selecciones. 51/260 alertas de conexión, ejemplos artificiales fallidos y rechazo de interpretación temática de fragmentación permanecen visibles. |
| Tiempo, Medicina y familias | −0,87/+0,91 puntos según candidatos; Medicina no es siempre menor en vecinos; controles no eliminan su diferencia con Energía; familias dependen de pooling. No se atribuye causalidad. |
| Casos y fuente | Se mantienen historia/física, infección/política y anuncio, confirmados contra registros descargados. S4 conserva 27 condiciones del atlas, extremos seleccionados, 531.650 relaciones elegibles y diagnóstico de títulos genéricos. No se estima prevalencia de error ni precisión por consenso. |
| Acceso y aprobación | Declaraciones literales; sin depósito persistente, nueva licencia, envío, validación temática externa o aprobación personal inventados. |

## Referencias y traducción

Las afirmaciones sobre Gläser, Boyack/Klavans, Constantino, González-Márquez, Singh, Caspari, Imel/Hafen, Held/Velden y las medidas se mantienen dentro de su función anterior. No se añaden afirmaciones de prioridad. Se conserva el conjunto de claves bibliográficas y los archivos bibliográficos. Los preprints siguen identificados como tales en las referencias. Esta entrega no repite una búsqueda de literatura ni certifica normas editoriales actuales.

Se ha leído la correspondencia inglesa y española, incluidos denominadores, direcciones, reglas y límites. Las comprobaciones automáticas comparan cifras, fórmulas y citas por párrafo; la comprobación semántica no se sustituye por esa igualdad formal.

## Presentación

T01 pregunta primero para qué sirve cada selección. T02 mantiene todas las celdas de modelos y explica el tamaño del vector y los tokens. Las notas quedan unidas a sus tablas. Los pies explican ejes, colores, unidades y lo que no representan los rangos. Las figuras y sus CSV no se han recalculado.

La revisión visual queda vinculada a los PDF concretos en visual_review.json. La validez científica y la facilidad de lectura para el autor siguen requiriendo su revisión; no se ha utilizado un detector de autoría.
