# Cómo se ha hecho la checklist adicional

Ampliación del 17-09-2026. Se conserva la comparación original de [METHODS_ANALYSIS.md](METHODS_ANALYSIS.md). La autorización y las decisiones previas al nuevo piloto están en [CHECKLIST_PROTOCOL.md](CHECKLIST_PROTOCOL.md). Los programas nuevos viven en `sos_followup/`; no se cambian los datos o programas anteriores.

## 1. Las tres entradas y la muestra

Se eligen 200 artículos de cada combinación de 26 áreas y cinco períodos: 26.000 en total. La selección ordena la huella SHA-256 de la semilla `sos-checklist-v1-input` concatenada con el ID OpenAlex. Los registros se guardan después por su posición global original. No interviene ningún parecido calculado por un modelo.

Cada uno de los diez modelos representa exactamente esos artículos en tres condiciones: título, resumen y título + resumen. La última reutiliza bit a bit los vectores originales. Las otras dos usan el campo literal, sin inventar un campo vacío ni añadir un separador entre campos ausentes. Se conservan las versiones, límites de lectura y recetas anteriores. No se entrena ningún modelo.

Por tanto, hay 30 condiciones modelo–entrada, con 780.000 filas: 260.000 reutilizadas y 520.000 nuevas. Esas cifras cuentan el mismo artículo varias veces; el número de artículos distintos es 26.000. Las salidas alternativas CLS/SEP de los cuatro BERT se guardan también, pero no incrementan el número de modelos.

La comparación principal reúne los cinco períodos dentro de cada área: 1.000 artículos, 200 por período. No pretende estimar con solo 200 las diferencias pequeñas de cada área y fecha. Las tres condiciones mantienen los mismos IDs, filas y candidatos.

Se describen las repeticiones de texto dentro de esa misma unidad, sin cambiar la selección según la entrada. El perfil previo a interpretar los nuevos acuerdos encuentra seis filas en tres parejas de títulos repetidos, y ningún abstract repetido dentro de área. Hay 465 títulos con menos de cuatro palabras separadas por espacios; no se confunde esa cuenta con los tokens internos de cada modelo. Evidencia reproducible en `data/checklist_v1/text_profile/`.

## 2. Receta y medidas

Se confirma la media de las posiciones no rellenadas, incluidos símbolos especiales, para BERT, SciBERT, BioBERT y PubMedBERT. Esa regla ya se había fijado antes del análisis inicial. Su confirmación en esta checklist es posterior a conocer las sensibilidades; no se describe como una decisión nueva tomada a ciegas. No se escoge la variante que maximice el acuerdo. CLS/SEP permanecen como comprobaciones de la primera fase.

La medida principal es CKA lineal corregida con vectores divididos por su longitud, conforme al método anterior. En el piloto se calcula de forma equivalente sobre las matrices de similitud entre artículos, con diagonal cero y centrado corregido. Esta implementación admite dimensiones diferentes y se ha contrastado con la fórmula de la primera fase en pruebas artificiales y comparaciones reales. No se usa una proyección a dos dimensiones.

La comprobación de forma compara los rangos de 20.000 distancias coseno, idénticos entre condiciones dentro de cada área. Los vecinos se buscan de forma exacta entre sus 1.000 artículos, excluyendo el propio ID, con números de 64 bits y desempate por posición global tras redondear a doce decimales. Se cuentan 25 vecinos como resultado principal y 10/50 como controles. Una segunda implementación por ordenación completa comprueba diez consultas de cada representación y área: 7.800 consultas en total.

## 3. Qué llamamos efecto del modelo y de la entrada

Para cada modelo y área se toma título + resumen como referencia.

- **Cambiar modelo:** promedio del desacuerdo de esa representación frente a las de los otros nueve modelos, manteniendo título + resumen.
- **Quitar resumen:** desacuerdo entre ambas partes y título solo, manteniendo modelo.
- **Quitar título:** desacuerdo entre ambas partes y resumen solo, manteniendo modelo.

Para forma, desacuerdo significa `1 − CKA`; para vecinos, fracción no conservada. También se exporta la comparación título frente a resumen. No se mezclan ambas escalas. `1 − CKA` no se presenta como distancia matemática garantizada ni como porcentaje de ciencia errónea.

El contraste principal resta cambio por entrada al cambio por modelo, por separado para quitar título y quitar resumen. Un número positivo indica mayor cambio por modelo en esa comparación concreta. Cada área y cada modelo pesan lo mismo. La media entre modelos no supone que sean diez réplicas independientes.

Como resumen secundario se comparan las 135 parejas de modelos con entrada idéntica —45 en cada una de las tres entradas— con las 30 transiciones entre entradas dentro del mismo modelo. Este promedio depende de esas transiciones elegidas: no es un porcentaje universal de variación explicado por cada causa.

El cambio de modelo incluye su representación habitual —pesos, receta y reglas de lectura—, no solo una arquitectura aislada. Los textos de origen coinciden, pero el contenido efectivo puede diferir por los límites de cada modelo. El control anterior de texto común ayuda a valorar esa limitación, sin constituir una descomposición causal completa del piloto actual.

## 4. Estabilidad y alcance del piloto

Se realizan 20 selecciones emparejadas de 500 artículos por área, 100 de cada período, y se repite el contraste de forma. La regla operativa, fijada antes de inspeccionar el piloto, exige cambio de mediana ≤0,02 frente a los 1.000 y amplitud central del 95% ≤0,04. Se comprueba por modelo y también para la media de los diez modelos: 520 y 52 comparaciones, respectivamente.

Son variaciones dentro de un conjunto fijo; no intervalos de confianza sobre toda la ciencia. La comprobación se refiere al contraste de forma, no demuestra por sí sola precisión poblacional de vecinos ni estabilidad de cada par de modelos. Los casos que fallen se conservan. Ampliar a 500.000 no se decide por rutina: debe resolver una incertidumbre concreta.

Quitar el título puede dejar espacio para más resumen antes del límite; quitar un campo cambia su formato efectivo. Los modelos entrenados con ambos campos reciben una entrada poco habitual al ver solo uno. Medimos el efecto práctico de esas entradas, no un efecto causal puro de eliminar palabras manteniendo todas las demás condiciones iguales. El control previo de contenido común sobre 52.000 responde a otra pregunta y no elimina completamente esta limitación.

Se añade un control cruzado de entrada y receta, definido durante la inferencia y antes de mirar los acuerdos del piloto: repetir el contraste con CLS y SEP en los cuatro BERT. Los otros seis modelos mantienen sus recetas habituales. Usa exclusivamente vectores ya guardados; reutiliza los 30 conjuntos principales de vecinos por área y calcula 24 alternativas. La reproducción de mean debe coincidir con todos los acuerdos principales y se contrastan independientemente otras 6.240 consultas. Se exportan CKA y vecinos 10/25/50. La criba con selecciones de 500 sigue refiriéndose a mean: no se finge una comprobación de estabilidad que no se hizo en las otras recetas. Configuración separada: `config/checklist_input_recipes_v1.json`.

## 5. Tiempo y número de candidatos

Se reutilizan las cinco fechas ya calculadas: 2000–04, 2005–09, 2010–14, 2015–19 y 2020–24. Se promedian con el mismo peso para cada área y pareja de modelos. Además de los promedios por fecha se conservan las 1.170 trayectorias área–pareja, diferencias primera/última fecha y pendientes descriptivas sobre cinco puntos.

La forma completa se contrasta con las medianas de selecciones de 2.048 guardadas en la fase anterior, criba de calidad y recetas CLS/SEP. Para los vecinos se priorizan los mismos 2.048 candidatos por celda; los tamaños completos varían entre áreas y fechas.

Tras observar que el signo temporal dependía de este control se añadió una comprobación identificada como posterior. Usa exactamente las 2.048 consultas del control en dos búsquedas ya guardadas: todos los candidatos de su celda y los 2.048 candidatos. Reutiliza las coincidencias individuales y separa así el cambio de consultas del cambio de candidatos. No calcula nuevos vectores o vecinos. Se repite para 10, 25 y 50 vecinos.

Los modelos son actuales y los artículos pertenecen a distintas fechas. Esto no reconstruye modelos históricos ni elimina diferencias de cobertura, longitud, composición o exposición durante entrenamiento. No se atribuye la tendencia a una convergencia causal de la ciencia.

## 6. Modelo por disciplina

Se muestran las 26 áreas; Medicina, Energía, Física y Matemáticas se destacan por la petición del usuario. Cada modelo se resume frente a los otros nueve. Una segunda tabla resta a cada acuerdo el promedio de su área y el promedio de su pareja de modelos, y devuelve la media general. Así se localizan combinaciones que se apartan de ese punto de referencia común.

Se separan las 45 parejas según incluyan ninguno, uno o ambos modelos biomédicos: 28, 16 y una pareja, respectivamente. La diferencia entre Medicina y cada área de referencia se descompone con pesos 28/45, 16/45 y 1/45. Dejar fuera ambos biomédicos permite comprobar si toda la diferencia depende de ellos. Se conservan controles de calidad, tamaño y receta.

Las asociaciones con diversidad de Subfields, longitud de resúmenes y marcas de calidad son descripciones entre 26 áreas. No identifican una causa. Los Fields y Subfields de OpenAlex proceden de clasificación automática y no constituyen verdad temática independiente.

## 7. Familias: asociación, no mecanismo demostrado

Los grupos se fijan a partir de las fuentes oficiales, resumidas en [MODEL_PROFILES.md](research/checklist_2026-09-17/MODEL_PROFILES.md). Se distinguen objetivo final —documentos con citas, palabras en contexto, contraste de frases— y especialización amplia —científica, biomédica, sin especialización exclusiva—. Esta última categoría puede incluir textos científicos. No conocemos el solapamiento exacto de los corpus de entrenamiento.

La variable `same_objective` representa esos grupos operativos de entrenamiento final, no identidad de su función matemática: los modelos guiados por citas también usan objetivos de contraste. Los nombres combinan señal/tarea y nivel textual. Se conserva la asignación inicial y se declara esta limitación; no se reagrupan modelos para mejorar la explicación.

La regresión descriptiva tiene 45 filas, una por pareja, después de promediar áreas y períodos. Incluye constante y tres indicadores: mismo objetivo, mismo dominio amplio y misma receta. No se calculan errores estándar suponiendo independientes las parejas. Se da una referencia de 4.096 permutaciones simultáneas de nombres de modelos, preservando la estructura de dependencia de la matriz de acuerdos. La fracción de ajustes permutados que alcanzan el observado incluye corrección de una unidad. Es una referencia combinatoria para estos diez modelos, no una prueba causal o una inferencia a todos los modelos posibles.

También se omite cada modelo y se vuelve a ajustar. Se informan rangos de coeficientes y error de predicción de sus parejas retiradas frente al promedio de entrenamiento, solo como sensibilidad entre modelos fijos. Con SEP, omitir SimCSE deja un diseño de rango tres: no hay coeficientes únicos para las cuatro columnas. Esa omisión se declara no identificable y se excluye de resúmenes de coeficientes/predicción; no se inventan valores. Las diez omisiones principales sí son identificables.

## Verificación y reconstrucción

Antes de la inferencia se comprobaron los diez modelos sobre artículos reales: la condición combinada reproduce los vectores originales dentro de tolerancia, los tokens de un solo campo coinciden exactamente con su texto y el lote coincide con la inferencia individual. El almacenamiento guarda bloques reanudables, versión, pesos, huellas de texto/tokens y orden de IDs.

El auditor revisa valores y huellas de todas las salidas guardadas, reconstruye las secuencias de tokens y compara bit a bit la condición reutilizada contra los originales. Las pruebas matemáticas cubren equivalencia entre fórmulas, rotaciones, mezcla de IDs, dimensiones diferentes y ejemplos donde solo cambia modelo o entrada. La prueba integrada verifica entradas idénticas, vecinos preservados y reanudación sin reescribir.

La entrega final solo se genera cuando pasan las auditorías. Para reconstruir sus tablas y figuras desde las medidas guardadas:

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_followup.report --require-complete
```

No vuelve a ejecutar inferencia o búsqueda de vecinos. `reports/checklist_v1/preview/` es provisional; la entrega final incorpora su catálogo de huellas y una copia del exportador.
