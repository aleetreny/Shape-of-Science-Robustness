# Protocolo de la checklist adicional

17-09-2026. El usuario pide avanzar con seis cuestiones y delega encajarlas con criterio de robustez. Esta petición amplía la fase anterior ya cerrada. Se conservan sus resultados y programas; nuevos datos en `data/checklist_v1/`, nuevos programas en `sos_followup/` y entrega en `reports/checklist_v1/`.

## Decisiones anteriores a los nuevos resultados

1. **Piloto de 26.000:** 200 por cada una de las 130 combinaciones de área/período, elegidos por huella del ID y semilla fija, sin mirar acuerdos. Los mismos artículos tienen título, resumen y ambos. La condición de ambos reutiliza los vectores originales. Las dos nuevas mantienen pesos, límites de lectura y recetas, sin entrenar. El texto solo lleva el campo elegido, sin simular un título vacío o añadir un separador entre campos ausentes. Se guardan texto, tokens efectivos, recortes y correspondencia de IDs.
2. **Comparación principal por área:** reunir sus cinco períodos con igual peso, 1.000 artículos por Field. Los 200 de cada celda no se presentan como muestra definitiva para conclusiones finas por fecha. Vecinos exactos con los mismos 1.000 candidatos y k=25; k=10/50 como controles.
3. **Modelo frente a entrada:** comparar el cambio de forma al sustituir el modelo manteniendo el texto con el cambio al quitar título o resumen manteniendo el modelo. Ambos usan las mismas filas y medidas. Principal CKA corregida, comprobación por rangos de distancias y vecinos. `1-CKA` se llama desacuerdo, no distancia matemática garantizada. Quitar el resumen cambia mucha más información que quitar el título: no ocultarlo en una única media de entradas. Promedios equilibrados por área/modelo; las parejas no son réplicas independientes.
4. **Estabilidad del piloto:** 20 selecciones de 500 por Field, 100 de cada período, emparejadas entre condiciones. Comprobar cambio mediano del contraste modelo–entrada ≤0,02 y amplitud central ≤0,04. Es un criterio operativo sobre una selección fija, no prueba de precisión poblacional. No ampliar automáticamente a 500.000: una ampliación debe responder a una incertidumbre concreta.
5. **Receta principal de cuatro BERT:** confirmar `mean` tal como estaba fijada antes del análisis anterior: media de posiciones no rellenadas, incluidos símbolos especiales. Es una regla común explícita y no un resumen documental entrenado. CLS y SEP permanecen como sensibilidades; no escoger después la que maximiza parecido ni introducir una receta nueva para mejorar el resultado. La confirmación actual sucede después de conocer sensibilidades y debe narrarse así, sin fingir una nueva elección ciega.
6. **Tiempo:** resumir las cinco fechas usando las 26 áreas con igual peso, cambios emparejados 2020–24 menos 2000–04 y pendientes descriptivas con los cinco puntos. Vecinos principales de este análisis: candidatos iguales de 2.048, pues el corpus crece de forma desigual. Forma completa contrastada con las medianas ya guardadas de 2.048, calidad y recetas. No confundir estabilidad entre modelos actuales con historia causal de la ciencia; tamaño, cobertura y textos cambian.
7. **Disciplina y biomedicina:** todas las 26 áreas; Medicina, Energía, Física y Matemáticas destacadas por la petición. Separar las 45 parejas en 28 sin BioBERT/PubMedBERT, 16 con solo uno y la pareja de ambos. Mostrar promedios de cada modelo contra los otros nueve, y desviación respecto al promedio de su pareja y del área. Comprobar tamaños, calidad y recetas. Es una localización de diferencias; no demuestra por qué causalmente surgieron.
8. **Familias:** registrar dos rasgos separados de las fichas oficiales: objetivo final y especialización amplia del dominio. MPNet/MiniLM y SimCSE no comparten necesariamente textos o método de entrenamiento; SciBERT comparte origen con los modelos de citas aunque su objetivo final sea distinto. Comparar dentro/fuera de grupos y una regresión descriptiva de las 45 parejas sobre objetivo, dominio amplio y receta. No calcular errores estándar suponiendo 45 pares independientes: referencia de 4.096 permutaciones de nombres de modelos y sensibilidad al quitar cada modelo. La referencia conserva la dependencia entre pares, pero no hace aleatorios a los modelos ni separa causalmente factores confundidos.

La configuración numérica está en `config/checklist_v1.json`. Todos estos análisis son una ampliación motivada por los resultados de la fase anterior; no se presentan como decisiones anteriores a ver cualquier dato. El piloto aún no se ha calculado al fijar esta versión.

## Fuentes iniciales y límites

- SPECTER2: entrenamiento inicial con citas, adaptador de proximidad y origen SciBERT, según [ficha oficial](https://huggingface.co/allenai/specter2).
- SciNCL: origen SciBERT y ejemplos de contraste construidos con vecindarios del grafo de citas, según [ficha oficial](https://huggingface.co/malteos/scincl).
- [MPNet](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) y [SimCSE](https://huggingface.co/princeton-nlp/unsup-simcse-bert-base-uncased): fichas consultadas para distinguir sus ajustes y recetas. Se completará una tabla de procedencia antes de interpretar familias.

No publicar, enviar el paper o modificar el TFM. No repetir la extracción ni los diez cálculos principales.

## Identificabilidad del control de familias

La comprobación del diseño, antes de interpretar coeficientes, detectó que al usar SEP y omitir SimCSE hay columnas dependientes. Se declara esa omisión no identificable: no se publican coeficientes individuales arbitrarios. Las diez comparaciones completas y las omisiones de la receta principal sí tienen rango completo. Los cambios de código se guardan en una salida nueva (`existing_v2`), conservando el intento incompleto. Las predicciones al quitar modelos se resumen solo para omisiones identificables y se informa su número.

## Qué significa aquí efecto de la entrada

El efecto compara formas prácticas de alimentar el mismo modelo, manteniendo su límite de lectura. Al quitar un campo puede cambiar también el separador efectivo; al quitar el título puede caber más resumen antes del límite. No se describirá como un efecto causal puro de esas palabras con todo lo demás idéntico. En los modelos entrenados para título + resumen, las condiciones de un solo campo son pruebas de sensibilidad fuera de su formato documental habitual. El control común de la fase anterior complementa esta limitación, pero no la elimina por sí solo.

## Comprobación temporal añadida después del primer resumen

El signo de la tendencia de vecinos cambia al comparar el conjunto completo con el control de 2.048. Ese control cambia candidatos y también artículos consultados. Para separar ambas cosas, se reutilizarán las coincidencias por artículo ya guardadas: medir los mismos 2.048 artículos frente a todos los candidatos de su celda y frente a los 2.048 candidatos. No se recalculan vectores ni búsquedas. Esta comprobación es posterior al resultado que la motivó; no se modifica la configuración inicial ni se presenta como previa.

## Cruce de entrada y receta, añadido antes de inspeccionar el piloto

Durante la inferencia, antes de calcular acuerdos de entradas, se añade `config/checklist_input_recipes_v1.json`. La fase anterior ya mostraba que la receta importa: por eso se repetirá el contraste modelo–entrada con CLS y SEP en los cuatro BERT, manteniendo los otros seis modelos. Los vectores alternativos ya se guardan; no requiere inferencia nueva. Se reutilizan los vecinos principales y se calculan solo las alternativas con los mismos 1.000 candidatos por área. CKA y vecinos 10/25/50; la receta principal sigue siendo mean. La estabilidad con selecciones de 500 pertenece a la principal y no se atribuye automáticamente a las otras recetas.
