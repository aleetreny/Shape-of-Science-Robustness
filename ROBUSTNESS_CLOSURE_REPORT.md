# Executive conclusion

**El estudio se sostiene, pero hemos estrechado dos conclusiones.** La apertura de las áreas depende mucho de cómo se preparan los vectores. Y la frase «quitar el resumen importa tanto como cambiar de modelo» solo describe una media: no funciona como regla para cada modelo.

- **¿Alguna prueba debilita el artículo?** Sí: el cambio de referencia global limita de forma importante qué podemos afirmar sobre la apertura. Lo hemos incorporado al cuerpo y a la Figura 4.
- **¿Ha caído el resultado central?** No. La organización general se conserva y los vecinos cambian mucho entre modelos, también después del filtro de calidad. No debemos defender una apertura independiente del procesamiento ni una equivalencia general entre texto y modelo.
- **¿Sigue siendo defendible para QSS?** Sí, como estudio de dependencia de las representaciones, con estos límites explícitos. Esto no predice la decisión de la revista.
- **¿Qué cambia en el texto?** Centros con repeticiones; entrada frente a modelo con sus diferencias; cobertura completa de las alternativas; efecto fuerte del centrado sobre apertura; efecto pequeño del filtro sobre vecinos; alertas locales visibles.
- **Preparación metodológica: READY WITH MINOR CAVEATS.** Las comprobaciones solicitadas están completas. No ha aparecido un problema metodológico que exija otro experimento antes del envío. Quedan límites declarados: corpus concreto, errores de origen que el filtro no detecta, diez modelos y análisis exploratorios. Antes del envío real siguen pendientes la revisión personal, correspondencia y depósito/licencia del material esencial; esta etiqueta no da esos trámites por hechos.

## 1. Centros: el resultado general se mantiene

**Pregunta.** ¿Dependía de haber elegido justo 256 artículos o unas pocas áreas?

**Qué hicimos.** Cincuenta selecciones a 256 artículos con las mismas fechas; cincuenta a cada tamaño 128/256/512; referencias aleatorias con los mismos artículos; omisión de cada área. Para una especialidad por área: cincuenta elecciones de especialidad y diez de artículos dentro de cada elección. Se usa la misma receta anterior, incluida la normalización del centro después de promediar.

**Resultado.**

| Grupos | Antes, una selección | Media de selecciones | Rango central del 95 % entre selecciones |
| --- | ---: | ---: | ---: |
| 26 áreas, 256 artículos | 0,939 | 0,940 | 0,937–0,943 |
| 217 especialidades, 256 artículos | 0,911 | 0,911 | 0,910–0,912 |
| Una especialidad por área | 0,902, media de 20 elecciones | 0,904 | 0,878–0,926 |

Con 128/256/512 artículos, las áreas dan 0,938/0,940/0,941 y las mismas 183 especialidades, 0,913/0,914/0,915. Las referencias aleatorias de 256 dan 0,627 y 0,636; ninguna media aleatoria alcanza la menor media observada. Omitir un área da 0,933–0,946. Matemáticas tiene la mayor influencia media: 0,00687; el máximo por pareja es 0,02355 para MiniLM–BioBERT.

En el diseño restringido cambia más la elección de especialidades que la de artículos dentro de ellas: desviaciones típicas descriptivas 0,01205 y 0,00157. La referencia restringida antigua mezclaba artículos de las 217 especialidades; la nueva solo mezcla los artículos de las 26 elegidas. Su media aleatoria es 0,660. Esta diferencia de procedencia queda declarada.

**Interpretación.** La organización general no parece un resultado de una selección afortunada ni de una sola área. Los rangos describen este corpus; no son intervalos para toda la ciencia.

**Impacto.** Afirmación reforzada. Figura 1 actualizada y Tabla S18. Evidencia: `centres_*.csv` en el directorio de resultados.

## 2. Texto frente a modelo: media estable, respuestas distintas

**Pregunta.** ¿Se repite directamente el resultado de los vecinos, y se aplica a todos los modelos?

**Qué hicimos.** Cincuenta selecciones equilibradas de 1.000 candidatos por área del experimento de texto, con los mismos artículos para cada comparación. Las cifras originales usaban 2.000; no se mezclan esos tamaños. Vecinos 10/25/50 y dos reglas alternativas de los cuatro BERT.

**Resultado.**

| Regla y vecinos | Cambiar modelo: vecinos sustituidos | Quitar resumen | Diferencia en puntos | Rango central de la diferencia |
| --- | ---: | ---: | ---: | ---: |
| Principal, 10 | 70,20 % | 72,17 % | +1,97 | 1,85–2,08 |
| Principal, 25 | 64,93 % | 66,49 % | +1,56 | 1,44–1,69 |
| Principal, 50 | 60,11 % | 61,15 % | +1,04 | 0,94–1,18 |
| CLS, 25 | 72,82 % | 69,70 % | −3,13 | −3,22 a −3,03 |
| SEP, 25 | 69,15 % | 67,15 % | −2,00 | −2,10 a −1,88 |

El signo de cada media se mantiene en las cincuenta selecciones. Pero la diferencia por modelo va de **−14,04 puntos en MPNet a +16,59 en SciBERT**. Por área, de −4,43 a +5,63. No podemos convertir el promedio en una regla general.

**Interpretación.** Las dos decisiones pueden cambiar muchos vecinos. Cuál pesa más depende del modelo y de cómo se obtiene su vector. No hemos hecho una prueba de equivalencia.

**Impacto.** Resumen, título de la sección de entrada, resultados, discusión y conclusión matizados. Evidencia: `headline_*.csv`; Figura S11 y Tabla S18.

## 3. Cambiar la referencia global: el matiz más importante

**Pregunta.** ¿Las respuestas opuestas entre áreas sobreviven a una preparación razonable distinta de los mismos vectores?

**Qué hicimos.** Restar la media de los 52.000 vectores unitarios de cada modelo y volver a ajustar cada vector a longitud uno. La misma referencia para todas sus áreas y selecciones. Repetir las 26 condiciones completas: principal, veinte mitades y cinco selecciones adicionales.

**Resultado.**

| Propiedad | Oposiciones originales | Oposiciones tras centrar | Originales que siguen opuestas | Con los mismos modelos y respuestas | Nuevas |
| --- | ---: | ---: | ---: | ---: | ---: |
| Apertura angular | 262 | 151 | 142 | 128 | 9 |
| Dimensión PR | 221 | 211 | 204 | 204 | 7 |

En apertura, 120 oposiciones originales dejan de serlo: 53 quedan sin resolver y 67 pasan a acuerdo de los diez. Solo 27 de los 42 acuerdos originales de los diez conservan su dirección. En PR, 17 oposiciones originales dejan de serlo: 16 quedan sin resolver y una pasa a acuerdo; 48 de los 54 acuerdos originales se mantienen.

La diferencia es aún más visible al exigir una magnitud del 5 %: la apertura pasa de **96 a 11** oposiciones, con solo una que conserva los mismos modelos y direcciones; PR pasa de 177 a 156, con 151 que los conservan. Al 10 %, las oposiciones angulares pasan de 19 a una, y ninguna de las originales conserva los mismos modelos y respuestas. Todos los cortes están guardados.

Además, en diez parejas de áreas hay al menos una pareja original de modelos que invierte ambas respuestas; son 19 parejas concretas de modelos. Ese recuento puede solaparse con otras categorías: no se suma a los anteriores. No ocurre para PR.

**Interpretación.** La apertura no es una propiedad que podamos presentar como independiente de esta preparación. La dimensión se conserva bastante mejor, aunque tampoco es idéntica. Ninguna preparación queda declarada «la correcta».

**Impacto.** Matiz material en resumen, resultados, discusión y conclusión. Figura 4 y Tabla S20 muestran el efecto; no queda escondido en el suplemento. Evidencia: `morphology_centering_*.csv` y `morphology_classification.csv`.

## 4. Alternativas de dimensión: comprobación completa

**Pregunta.** ¿Solo obteníamos el resultado por escoger PR?

**Qué hicimos.** Completar entropía y D80 con las mismas 26 selecciones. Mantener los modelos concretos y sus respuestas; no buscar otros para salvar un caso. Los empates de D80 quedan sin resolver.

**Resultado.** PR tiene 221 oposiciones persistentes. Entropía tiene 252 en total y conserva 209 de las oposiciones originales de PR con los mismos modelos y direcciones. D80 tiene 283 en total y conserva 190. Las dos alternativas a la vez conservan **190 de 221**; antes, con solo tres condiciones, eran 196. No confundir el total de oposiciones de una medida con las mismas oposiciones conservadas de PR.

También hay un límite: solo cinco de los 54 acuerdos originales de los diez modelos conservan una dirección no nula en todos los modelos bajo ambas alternativas. Muchas comparaciones no cumplen esa exigencia, incluidos empates de D80. Por eso hablamos de apoyo para muchas oposiciones, no de equivalencia entre medidas.

**Impacto.** Sustituido el 196 de cobertura parcial por 190 y actualizados los conjuntos de modelos de la Tabla S15. Evidencia: `dimension_alternative_retention.csv` y `model_panel_summary_full_alternatives.csv`.

## 5. Calidad y duplicados: efecto pequeño en el resultado general

**Pregunta.** ¿El desacuerdo de vecinos se debía principalmente a los registros marcados y duplicados detectados?

**Qué hicimos.** Aplicar la regla existente, sin inventar otra: 448.886 artículos conservados. Comparar las mismas consultas antes/después y repetir a tamaños iguales. Se añadieron 1.024 candidatos en todas las celdas porque solo 63 de 130 permiten 2.048 después del filtro.

**Resultado.** Con 25 vecinos, el acuerdo de las mismas consultas pasa de **30,58 a 31,43 %: +0,85 puntos**. La media original de todas las consultas era 30,29 %; usar solo las conservadas explica parte de esa diferencia y se informa por separado. A tamaño fijo, la subida es **0,28 puntos con 1.024 candidatos** y **0,19 con 2.048**. Con 10/50 vecinos, los cambios en búsquedas completas son +0,66/+1,04 puntos.

Matemáticas es el área que más cambia de media: +2,72 puntos en búsquedas completas. La mayor subida media por pareja es +1,43 para SPECTER2–SciBERT. El control de entrada conserva un cambio fuerte: tras filtrar, cambiar modelo sustituye el 64,27 % y quitar el resumen el 66,45 % de los 25 vecinos, con 1.000 candidatos por área.

**Interpretación.** Los problemas que detecta este filtro no explican la mayor parte del desacuerdo. Eso no certifica los demás registros ni descarta problemas que la regla no ve.

**Impacto.** Evidencia nueva añadida a resultados y límites, Tabla S19. Archivos: `quality_*.csv`.

## 6. Promedios estables no significan que todo sea estable

**Pregunta.** ¿La poca variación de la media estaba ocultando comparaciones sensibles?

**Qué hicimos.** Verificar la tabla original, sus umbrales y denominadores, sin cambiar la regla de alertas.

**Resultado.** La media interna ronda 0,63–0,64 con 128/256/512 artículos, pero **2.628 de 8.235 comparaciones locales, el 31,9 %, conservan alertas** en las mismas 183 especialidades. Las otras 68 especialidades, donde el tamaño mayor usa todos sus artículos, forman otro grupo: 213 alertas de 3.060. No se suman ni intercambian esos denominadores.

**Interpretación.** Un termómetro medio puede cambiar poco mientras algunos sitios cambian bastante. Aquí pasa algo parecido: la media general no asegura cada comparación concreta.

**Impacto.** El 31,9 % aparece ahora en resultados del artículo y se retoma en la interpretación. No se han eliminado alertas.

## Evidencia, cambios y continuación

- [Auditoría de las once afirmaciones](research/robustness_closure_2026-09-20/CLAIM_AUDIT.md).
- [Registro de cambios del manuscrito](ROBUSTNESS_MANUSCRIPT_CHANGELOG.md).
- [Protocolo de estas pruebas](ROBUSTNESS_CLOSURE_PROTOCOL.md).
- [Resultados legibles por programas](reports/robustness_closure_v1/summary.json); tablas en ese mismo directorio.
- Selecciones, vectores de centros, vecinos, programas y huellas: `data/robustness_closure_v1/`.
- Artículo y suplemento actualizados en `manuscript/` y `manuscript_es/`; PDF en `output/pdf/` y `output/pdf/es/`.

La comprobación independiente reproduce 78.000 direcciones, los promedios originales de vecinos y las 900 selecciones de centros/referencias. Los programas y resultados previos permanecen intactos. Las semillas numéricas están registradas en `research/robustness_closure_2026-09-20/random_seeds.csv`.

El siguiente paso es la lectura personal del autor y la preparación de los materiales de envío. No se propone otro experimento por el simple hecho de que sea posible.


## Documentos y comprobación de entrega

| Documento | Español | Inglés |
| --- | --- | --- |
| Artículo | [PDF, 22 páginas](output/pdf/es/main.pdf) | [PDF, 20 páginas](output/pdf/main.pdf) |
| Suplemento | [PDF, 41 páginas](output/pdf/es/supplement.pdf) | [PDF, 39 páginas](output/pdf/supplement.pdf) |
| Fuentes editables | [ZIP español](output/manuscript_source_es.zip) | [ZIP inglés](output/manuscript_source.zip) |

Se han inspeccionado las 122 páginas y comprobado 22 grupos de tablas, 15 figuras y 129 CSV idénticos entre idiomas. El cuerpo inglés tiene 4.570 palabras y el resumen 192; los detalles nuevos quedan sobre todo en S9. Los dos ZIP extraídos reconstruyen exactamente los cuatro PDF. La tipografía bibliográfica usa interlineado normal para evitar una última página casi vacía.

El título y las declaraciones no cambian. Los documentos actuales están revisados, pero siguen pendientes de tu aprobación personal. La [auditoría final](research/robustness_closure_2026-09-20/closure_audit.json) enlaza las comprobaciones numéricas, de traducción, presentación y reproducción.
