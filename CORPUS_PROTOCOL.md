# Decisión para preparar el corpus

**14-09-2026 · Decisión tomada por delegación explícita del usuario.** Tamaño de la primera fase: **500.000 trabajos válidos y con IDs distintos**. Este documento sustituye las propuestas de tamaño anteriores. La descarga original se completó el 15-09-2026. El usuario autorizó después limpiar y completar una copia separada con el mismo tamaño y reparto; reglas y resultado en `CLEANING.md`.

## Qué vamos a preparar

- **400.000 trabajos para la imagen general.** Selección aleatoria de la población que cumple los filtros. Sus proporciones por área y año surgen de esa selección, sin imponer cuotas iguales ni usar los porcentajes anteriores a la limpieza como si fueran los definitivos.
- **100.000 trabajos adicionales para las áreas y períodos con menos ejemplos.** Se suman a los anteriores; no se cuentan dos veces. Sirven para comparar bien cada área.
- **26 Fields y cinco períodos:** 2000–2004, 2005–2009, 2010–2014, 2015–2019 y 2020–2024. Guardar el año exacto de cada trabajo. Dentro de cada período, no imponer el mismo número por año.
- **Mismos IDs y textos para todos los modelos** en cada comparación. Título y abstract se guardan por separado para poder cambiar más adelante la forma de entrada sin descargar de nuevo.

Es una base grande compartida: no necesitamos 500.000 papers distintos por modelo, ni volver a reunirlos para cada comprobación.

## Reparto del complemento, sin elegir cuotas a mano

Una vez limpios los 400.000 de la base general, contar sus trabajos en las **130 combinaciones de Field y período**. Asignar los 100.000 adicionales a las combinaciones menos numerosas hasta igualar, en lo posible, sus tamaños mínimos. Los grupos que ya son grandes no se recortan.

La regla puede ejecutarse asignando cada plaza al grupo con menos trabajos; resolver empates por ID de Field y comienzo de período. Después seleccionar al azar los trabajos correspondientes dentro de cada grupo, excluyendo IDs ya elegidos. Si un grupo agota los trabajos elegibles, conservar los disponibles, registrar el déficit y reasignar las plazas restantes con la misma regla.

Los conteos actuales, **antes de limpieza**, proyectan unas **2.200 publicaciones por área y período como mínimo**, unas 11.000 por área pequeña en el conjunto de los 25 años. Como ejemplos aproximados: Medicina 76.600, Ingeniería 65.700, Informática 32.500 y Veterinaria 11.000. **Son previsiones, no cuotas definitivas ni cantidades ya descargadas.** El reparto exacto se calculará con la base general limpia.

La proyección completa está en [allocation_projection.csv](research/feasibility_2026-09-14/allocation_projection.csv). Esta asignación protege a los grupos pequeños sin poner su tamaño como techo a los grandes. No presupone que todos los grupos tienen igual variedad temática o que igual tamaño garantiza igual precisión.

## Población y limpieza que quedan fijadas

| Decisión | Motivo |
| --- | --- |
| Catálogo principal de OpenAlex (`corpus=core`) | Evitar mezclar en esta primera fase la ampliación opcional de repositorios y datasets. |
| Años 2000–2024 | Ventana completa de 25 años, compatible con el TFM y menos expuesta al retraso en completar metadatos recientes. |
| Tipos `article`, `review`, `conference-paper` | Incluir revisiones y no dejar fuera una vía importante de publicación en Informática e Ingeniería. |
| Excluir `preprint` | Reducir la mezcla de versiones preliminares y publicadas. Esto no garantiza eliminar todas las versiones duplicadas. |
| Inglés, título no vacío y abstract reconstruible de al menos **50 palabras por regex** | Asegurar una cantidad mínima de texto sin conservar el descarte anterior de títulos de menos de cinco palabras. La longitud es una regla operativa explícita, no una garantía de calidad semántica. |
| Excluir retractados y material auxiliar; exigir Field conocido | Coherencia con la población definida y con las comparaciones de las 26 áreas. |
| Clasificación del tema principal de OpenAlex, congelada al extraer | Un trabajo cuenta en un único Field en el análisis principal. Conservar también temas secundarios para futuras comprobaciones. |

El filtro API básico, antes de la limpieza de texto, es:

```text
publication_year:2000-2024,type:article|review|conference-paper,language:en,has_abstract:true,is_retracted:false,is_paratext:false,primary_topic.field.id:!null
```

Este conjunto tiene **67.202.824 candidatos** en la consulta del 14-09-2026. No equivale al número final después de limpiar. En una prueba aleatoria de 400 candidatos, 357 pasaron título no vacío y abstract ≥50 palabras; 315 pasaron ≥80 palabras. En Artes, la diferencia fue 82 frente a 69 de 100. Por eso se conserva el texto entre 50 y 79 palabras y se marca: permitirá repetir más adelante una comprobación con ≥80 sin otra descarga ni nuevos embeddings para los restantes.

La población de nuestras conclusiones será **esta literatura cubierta por OpenAlex que cumple los filtros**. No se presentará como todos los trabajos del mundo, en todos los idiomas, ni como representativa de publicaciones sin abstract.

**Control de texto añadido el 15-09-2026:** la etiqueta `language=en` de OpenAlex no garantiza que el abstract esté en inglés. La limpieza autorizada excluye alertas claras consistentes y contenido ajeno al resumen; conserva y marca idiomas dudosos o mixtos. Las reglas exactas y sus límites están en `CLEANING.md`. La población operativa es la que pasa esos filtros; no se afirma que todos los textos retenidos sean exclusivamente ingleses.

## Cómo mantener una selección defendible

1. Extraer bloques aleatorios con semillas registradas, guardar las respuestas y el orden de llegada. No seleccionar por citas ni por parecido según un embedding.
2. Reconstruir y limpiar de forma idéntica todos los candidatos. Descartar IDs repetidos entre bloques y continuar hasta reunir los **400.000 válidos distintos**. Esta selección aleatoria global, seguida de un filtro común, evita tener que conocer previamente el número exacto de textos válidos en cada área y año.
3. Aplicar el complemento de 100.000 según los recuentos limpios. Guardar para cada ID si pertenece a la base general o al complemento, su grupo y su procedencia.
4. La API cambia: registrar fechas, parámetros, semillas, IDs, textos y huellas de contenido. Las semillas por sí solas no hacen reproducible una consulta futura sobre otra versión de OpenAlex.
5. Deduplicar siempre por `work_id`. Marcar DOI repetido y texto idéntico para auditar posibles versiones del mismo trabajo. No fusionar por parecido del título de forma automática. La unidad de selección inicial es el registro de OpenAlex; la sensibilidad a versiones duplicadas debe comprobarse antes de afirmar resultados sobre estudios únicos.

El bloque de 400.000 conserva la comparación con la población definida. **No tratar los 500.000 juntos, sin corrección, como una muestra proporcional:** el complemento aumenta deliberadamente la presencia de grupos pequeños.

### Interrupciones de conexión — requisito añadido el 15-09-2026

El extractor debe guardar localmente cada página completa y su estado de procesamiento, de forma que un corte de internet o un reinicio no obligue a descargar otra vez lo ya guardado. Ante fallos temporales, esperar y reintentar; si el proceso termina, poder reanudar desde el último avance válido. Una respuesta incompleta no se marca como terminada. Evitar duplicar IDs o contar dos veces una página al reanudar.

Conservar las respuestas ya recibidas, las semillas, el orden de selección y los descartes. Una interrupción no debe cambiar deliberadamente el reparto ni las reglas de selección. Como OpenAlex cambia, una reanudación tardía debe detectar posibles cambios en las páginas y registrarlos; guardar solo el número de página no basta para garantizar la misma selección.

**Antes de la descarga grande, verificar con una prueba pequeña un corte de conexión y un reinicio del proceso**, comprobando que se conservan los datos completos y se reanuda sin pérdidas ni duplicados. Implementado y probado el 15-09-2026; evidencia en `research/download_validation_2026-09-15/RESULTS.md`. La descarga completa queda a cargo del usuario.

Para resultados por área y período se usa la base más el complemento del grupo correspondiente. Si después se resume un Field juntando los 25 años, habrá que conservar sus proporciones temporales mediante un cálculo expresamente definido; no mezclar esos períodos sin considerar el refuerzo. Tampoco una media de resultados por Field sustituye a medir las relaciones entre Fields. Estas decisiones sobre las medidas finales se presentarán al usuario cuando toque.

## Por qué 500.000

Es un **presupuesto de datos justificado por cobertura y recursos**, con una comprobación de estabilidad antes de las conclusiones. No se afirma haber demostrado un tamaño óptimo universal.

- Da una base general grande y permite dedicar 100.000 trabajos a proteger las comparaciones menos numerosas.
- Permite estudiar cinco períodos sin repartir unos pocos miles de papers entre 25 años y dejar cada comparación casi vacía.
- Con los modelos probados, el coste de procesar 500.000 textos es del orden de horas por modelo. Duplicar a un millón duplicaría ese trabajo; aumentar el número de modelos y entradas también multiplica el coste.
- El valor del paper dependerá de comparar justamente los modelos, de controlar los cambios al muestrear y de formular conclusiones acordes a los datos. El volumen por sí solo no resuelve esos puntos.

Como precedente de escala, el estudio de Constantino et al. publicado en QSS utilizó una red de 452.096 papers y encontró abstracts para 159.375. Esto muestra que el tamaño útil depende de la comparación concreta; **no establece un mínimo editorial**. [Artículo y versión de autores](https://doi.org/10.1162/qss_a_00349), [métodos abiertos](https://arxiv.org/html/2308.15706v2).

## Recursos y reutilización

Pruebas reales en este Mac: **Apple M5 Pro, 48 GiB de RAM**. SciNCL procesó unos 50,5 papers/s y MPNet unos 64,6 papers/s sobre 512 textos reales, usando la GPU y precisión de 32 bits. Esta prueba corta da unas **2,1–2,8 horas por modelo** para 500.000 textos. Para planificar reservar **3–6 horas por modelo comparable y una entrada de texto**, y **12–24 horas para un escenario de cuatro modelos**. El conjunto definitivo de modelos sigue abierto; modelos mucho mayores pueden costar más.

La extracción medida con bloques del tamaño previsto da unos 1,1–1,3 segundos por página de 100 trabajos. Con los descartes observados, la proyección ideal ronda dos horas; reservar **3–6 horas de extracción**, ampliables si aparecen límites de API o incidencias. Son estimaciones de tiempo de trabajo del ordenador, no un compromiso de duración.

Una matriz de 500.000 × 768 números de 32 bits ocupa **1,43 GiB por modelo**. Cuatro ocuparían 5,72 GiB, más textos, modelos y memoria de trabajo. Los 48 GiB permiten trabajar por lotes con margen. En cambio, guardar todas las distancias entre 500.000 papers requeriría unos **931 GiB**: ese cálculo se debe hacer por bloques o evaluar consultas seleccionadas contra la base común, sin construir la tabla entera.

Se reutilizan código de limpieza, taxonomía, índices y vectores antiguos para comprobaciones. En la selección nueva se buscarán primero los IDs y textos coincidentes ya disponibles. **No se incorporan los 2,38 millones antiguos por conveniencia**, porque fueron seleccionados con otro reparto. La prueba encontró solo 4 coincidencias locales entre 400 candidatos generales; no se presupone un gran ahorro por coincidencia de IDs. Para reutilizar un embedding final hay que comprobar también texto, entrada y versión del modelo; el presupuesto admite recalcularlo si esa procedencia no puede fijarse.

## Comprobación antes de sacar conclusiones

El tamaño de preparación queda cerrado en 500.000. Antes de interpretar el estudio completo, comprobar que las medidas no cambian demasiado al repetir la selección y al usar fracciones de esos mismos datos. Esto se hará para los modelos y grupos definitivos, reutilizando los embeddings ya calculados.

La prueba acotada actual compara SPECTER2 heredado y SciNCL en Medicina/Veterinaria, períodos 2000–2004 y 2020–2024, con tamaños de 256, 512, 1.024 y 2.048. La regla se guardó antes de calcular resultados: cambio de mediana ≤0,02 al pasar de 1.024 a 2.048 y amplitud del rango empírico central del 95 % ≤0,04 a 2.048. Es una criba de estabilidad, no un intervalo de confianza poblacional ni una exigencia de QSS. Su resultado se recoge en el informe de pruebas.

La comparación de vecinos necesita además controlar qué papers pueden ser vecinos: al cambiar esa base puede cambiar legítimamente el resultado. No extrapolar el chequeo de la medida global a todas las medidas locales.

**Resultado de la prueba acotada:** se procesaron 15.780 textos y las cuatro combinaciones pasaron la criba fijada. El cambio de mediana de 1.024 a 2.048 fue menor de 0,002 en las cuatro. Esto apoya el orden de magnitud previsto para la preparación, pero procede del corpus histórico, cuatro casos y un par de modelos. No certifica todos los Fields, otros modelos ni todos los resultados futuros. [Informe de pruebas y límites](research/feasibility_2026-09-14/RESULTS.md), [datos completos](research/feasibility_2026-09-14/sample_size_probe.json).

Si alguna comparación final no es estable, se registra y se plantea una ampliación **concreta** o una limitación de la conclusión. No se aumenta automáticamente todo el corpus ni se ocultan los casos que fallen. Esa será una nueva decisión, fuera de la delegación de esta primera fase.

## Qué debe quedar al terminar la preparación

- Tabla maestra de 500.000 IDs únicos: 400.000 base + 100.000 complemento.
- Título, abstract, DOI, tipo, idioma, año, fecha, clasificación principal/secundaria y longitud del texto.
- Recuentos por Field, año y período; marcas de procedencia, filtros, duplicados potenciales y pertenencia a cada conjunto.
- Respuestas o evidencia de extracción, semillas, fecha, controles de integridad y huellas del texto.
- Una lista de IDs y textos congelada para todos los modelos. Las versiones exactas de los modelos y sus entradas se decidirán en su fase correspondiente.

Desde el 15-09-2026, el extractor está en `sos_download/` y se ejecuta con `./download.sh`; manual en `DOWNLOAD.md`. La descarga se completó desde la terminal del usuario el 15-09-2026; auditoría y continuación en `AUDIT.md` y `NEXT_STEPS.md`. Evidencia de viabilidad anterior: [carpeta de pruebas](research/feasibility_2026-09-14/), [escenarios de coste](research/feasibility_2026-09-14/budget_scenarios.csv).

## Resultado de preparación, 15-09-2026

La copia limpia final ya está en `data/corpus_clean_v1/`: 500.000 registros, 400.000+100.000, mínimo 2.165 por Field/período y los 26 Fields presentes en cada año de 2000–2024. Se conservaron las proporciones obtenidas sin imponer cuotas anuales iguales. Una página adicional de 100 candidatos aportó diez registros; el resto se recuperó de lo ya guardado. Las reglas de limpieza, su efecto por área y sus límites están en `CLEANING.md`. La entrada común está fijada; los modelos se acordarán en el siguiente paso.
