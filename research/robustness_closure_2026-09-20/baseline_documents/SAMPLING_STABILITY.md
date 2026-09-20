# Cómo reportamos la estabilidad de selección

**Cambiar de modelo y cambiar la selección de artículos son dos preguntas distintas.** La primera mide acuerdo entre representaciones. La segunda comprueba cuánto se mueve ese acuerdo al usar otros artículos del conjunto disponible.

## Qué representa una repetición

Se seleccionan sin reemplazo artículos del corpus fijo. Los mismos IDs se usan para todos los modelos y condiciones de una repetición. Los períodos mantienen las cuotas declaradas cuando la unidad los reúne. No se vuelven a consultar OpenAlex ni se vuelven a calcular modelos para estas selecciones.

Para cada comparación se guardan tamaño completo y reducido, IDs/semilla, todas las repeticiones, mediana, percentiles 2,5 y 97,5, amplitud entre ambos y diferencia respecto al cálculo completo. Las selecciones se solapan: no son réplicas independientes del mundo ni modelos nuevos.

Esos percentiles describen **variación dentro del corpus observado**. No son intervalos de confianza sobre toda la literatura mundial, ni estiman por sí solos el error de clasificación de OpenAlex, sesgo de cobertura o calidad semántica.

## Alertas y ampliación a 52k

Las 31 alertas de entradas pertenecen al contraste de forma «cambio por modelo menos cambio por entrada», con mean principal. La regla conserva cambio de mediana ≤0,02 y amplitud central ≤0,04. No es una frontera universal que una revista haya establecido.

| Experimento | Por área, cinco períodos reunidos | Por repetición | Repeticiones comparables |
| --- | ---: | ---: | ---: |
| Piloto 26k | 1.000, 200 por período | 500, 100 por período | 20 |
| Ampliación 52k | 2.000, 400 por período | 1.000, 200 por período | 20 |

La tabla de seguimiento conserva las mismas claves modelo/área/entrada y distingue: alerta que persiste, que desaparece, que aparece nueva y caso sin alerta en ambos. Se conservan también magnitud/dirección del contraste y cambios de mediana: contar alertas no sustituye a examinar sus cifras.

Veinte repeticiones dan una descripción poco precisa de las colas. Se completaron **100 repeticiones en ambos tamaños**, con la misma regla; las primeras 20 reproducen los resultados guardados. Se separan los dos cambios: más artículos y más repeticiones.

| Repeticiones | Alertas en 26k, de 520 | Alertas en 52k, de 520 | Persisten al ampliar | Desaparecen | Nuevas |
| --- | ---: | ---: | ---: | ---: | ---: |
| 20, comparación histórica | 31 | 4 | 3 | 28 | 1 |
| 100, comprobación ampliada | 72 | 5 | 5 | 67 | 0 |

Los 52 promedios de área superan la regla en ambos tamaños y cantidades de repeticiones. Con 52k y 100 repeticiones, cuatro contrastes individuales y seis promedios de área tienen un rango central que incluye cero. No deben confundirse con las alertas de amplitud: una diferencia puede ser pequeña y estable, sin permitir afirmar qué efecto es mayor.

Las cinco alertas actuales, con 52k y 100 repeticiones:

| Área | Modelo | Entrada frente a título + resumen | Amplitud central | Cambio absoluto de mediana |
| --- | --- | --- | ---: | ---: |
| Agricultural and Biological Sciences | BioBERT | Abstract | 0,04736 | 0,00224 |
| Earth and Planetary Sciences | BioBERT | Abstract | 0,04499 | 0,00272 |
| Economics, Econometrics and Finance | BioBERT | Abstract | 0,04154 | 0,00283 |
| Immunology and Microbiology | BioBERT | Abstract | 0,06296 | 0,00576 |
| Health Professions | PubMedBERT | Title | 0,04000896 | 0,00156 |

Todas incumplen por amplitud mayor de 0,04; ninguna por cambio mediano mayor de 0,02. El caso de Health Professions supera el límite por muy poco: permanece marcado, sin redondearlo para hacerlo pasar. Ninguna de estas cinco cruza cero. En las cuatro de abstract el efecto modelo es mayor; en la de título es menor. La alerta limita la precisión de la magnitud, no obliga a invertir ese signo.

De las 31 claves originales, cuatro siguen con alerta en 52k/100 y 27 no; la quinta actual no pertenecía a aquellas 31. Para atribuir diferencias al tamaño se usa la comparación 100 contra 100 de la tabla, no 31 contra 5 mezclando repeticiones. Más repeticiones describen mejor las colas: el aumento 31 → 72 en 26k no indica que se hayan estropeado los datos.

Evidencia: `data/robustness_v2/input_stability100/` conserva IDs y valores de las 100 selecciones; `input_review/original31_tracking.csv`, `current52_alerts.csv` y `alert_transition_counts.csv` conservan cada clave y transición. Este control usa mean principal; no se extrapola como validación de todas las recetas o de vecinos.

Las 50 alertas de la primera fase pertenecen a otra unidad y diseño. Se conservan sus claves y umbrales originales; no sumarlas sin explicación con las de entradas. Los Subfields tienen sus propios tamaños, cobertura y diagnóstico. Los grupos que no permiten reducir tamaño o calcular una medida quedan identificados, sin asignarles una precisión ficticia.

## Revisión completada de las alertas originales y de especialidades

Las 5.850 filas originales se reconstruyeron desde sus valores brutos y huellas. Las 50 alertas siguen siendo las mismas: 13 celdas, ocho áreas; todas por amplitud mayor de 0,04, ninguna por cambio mediano entre tamaños mayor de 0,02. En 48 aparece BioBERT. Esa concentración no demuestra un fallo del modelo ni autoriza a retirarlo. El mayor desplazamiento absoluto de la mediana de 2.048 respecto al cálculo de toda la celda es 0,00891. Registro completo: `data/robustness_v2/control_review_v2/original_50_alerts.csv`.

En Subfields hay 2.628 alertas de 8.235 comparaciones de 183 grupos donde la muestra grande de 512 aún es menor que el grupo. En otros 68 grupos, la muestra grande agota el grupo: 213/3.060 alertas por cambio frente al tamaño pequeño y rango prácticamente nulo por construcción. El grupo restante tiene tres artículos y no permite CKA. Guardar estos conjuntos separados; sumarlos sin sus tamaños y significado oculta la diferencia. Son controles de selecciones reducidas, no la incertidumbre poblacional de las comparaciones nativas con todos los artículos disponibles.

## Vecinos por artículo

La fracción de vecinos conservados entre modelos describe acuerdo local para ese artículo y conjunto de candidatos. Su variación al cambiar k, omitir modelos o modificar candidatos no es un intervalo de muestreo poblacional. Se registran esas sensibilidades por separado y no se traslada automáticamente una criba de CKA a kNN.

Una diferencia pequeña puede seguir siendo incierta aunque los promedios generales sean estables. Se mantienen visibles las alertas; no se cambian sus umbrales después de mirar los resultados ni se afirma que duplicar la muestra garantice eliminarlas.
