# Qué hemos encontrado al comparar los diez modelos

**Análisis terminado y comprobado el 17-09-2026.** Son los mismos 500.000 artículos, diez modelos, 26 áreas y cinco períodos. Los originales se conservan intactos.

Ampliación posterior, también terminada: [CHECKLIST_RESULTS.md](CHECKLIST_RESULTS.md) añade el piloto de tres entradas, tiempo, disciplinas y familias. Este informe conserva los resultados de la primera fase; el [esquema del paper](PAPER_OUTLINE.md) integra ambas.

**La conclusión principal:** el mapa se parece más cuando miramos las grandes áreas que cuando nos acercamos a cada artículo. Dos modelos pueden situar las disciplinas de forma parecida y, aun así, colocar al lado de un artículo trabajos diferentes. Además, importa cómo convertimos la salida de un modelo en una representación del artículo.

## Los resultados que llevaría al paper

| Pregunta | Resultado | Lectura correcta |
| --- | --- | --- |
| ¿Se conservan las relaciones entre grandes áreas? | Correlación de orden mediana **0,847** entre las 325 relaciones, en los 45 pares de modelos y cinco períodos. | Bastante acuerdo sobre qué áreas están más cerca. No significa «84,7% de ciencia correcta». |
| ¿Se conserva la organización dentro de cada área? | Correlación de orden mediana **0,519**. La medida principal de forma, CKA corregida, tiene mediana **0,610**. | Hay acuerdo, pero quedan diferencias importantes. Las dos medidas usan escalas distintas. |
| ¿Se conservan los 25 vecinos de cada artículo? | Coincidencia media **30,3%: 7,6 de 25**. | Media que da el mismo peso a cada área, período y par de modelos; vecinos buscados dentro del área y período. |
| ¿Lo explica el distinto tamaño de las áreas? | Con exactamente 2.048 candidatos por área/período, coinciden **31,9%: 8,0 de 25**. | El desacuerdo general persiste cuando igualamos la cantidad de candidatos. |
| ¿Qué sucede al buscar en toda la base general? | Coinciden **17,5%: 4,4 de 25**. | Son 13.000 artículos de consulta frente a 400.000 candidatos. Cambian tanto las fronteras como el tamaño de la búsqueda; no atribuir la caída a una sola causa. |

Entre áreas e interior se usa la misma clase de correlación de orden, pero aplicada a objetos distintos: centros de áreas frente a pares de artículos. El contraste es descriptivo; no demuestra una ley universal por la que toda medida empeore al acercarse al detalle.

El resultado global de forma sobre los **400.000 de base**, sin mezclar el refuerzo como si fuera proporcional, tiene mediana CKA **0,603**, Procrustes **0,603** y correlación de orden **0,392** entre los 45 pares. La literatura representada sigue limitada por nuestros filtros de cobertura, idioma, fechas y disponibilidad de resumen.

### Los modelos no discrepan todos por igual

| Pareja | Vecinos compartidos, de 25 | Coincidencia media |
| --- | ---: | ---: |
| MPNet – MiniLM | **14,1** | **56,5%** |
| PubMedBERT – BioBERT | 13,0 | 52,2% |
| SciBERT – PubMedBERT | 13,0 | 51,9% |
| SPECTER2 – SimCSE | **4,5** | **18,0%** |

Los extremos anteriores son extremos del resumen de vecinos, no ganadores ni perdedores en calidad. La mayor similitud de forma corresponde a PubMedBERT–BioBERT: mediana CKA **0,858**. La menor corresponde a MiniLM–PubMedBERT: **0,492**.

Forma y vecinos están **fuertemente relacionados**: la correlación de orden entre los 45 resúmenes por pareja es **0,920**. No debemos vender el resultado como dos fenómenos independientes. La aportación es mostrar qué conserva y qué pierde cada comparación: un índice de forma de 0,85 no promete conservar el 85% de vecinos.

Si cada uno de los 500.000 artículos pesa lo mismo, la coincidencia local media es **28,2%**, frente al 30,3% equilibrado por área/período. Ambos resúmenes quedan disponibles, con sus denominadores. Ninguno convierte el corpus reforzado en una selección proporcional de toda la ciencia.

## Qué comprobaciones sostienen esa lectura

### El acuerdo entre grandes áreas no desaparece en los controles

La correlación mediana entre áreas es **0,836–0,847** al cambiar la receta de los cuatro BERT, apartar casos dudosos o conservar la longitud original de los vectores. Con los mismos 52.000 artículos y 2.000 por área, pasa de **0,8494** con lectura habitual a **0,8493** con contenido común.

Resumir muchos artículos en un centro ya puede producir acuerdo. Para comprobarlo, también hicimos 20 repartos aleatorios, con el mismo tamaño y mezcla de períodos que las áreas reales. La referencia mediana es **0,603** con texto habitual y **0,611** con texto común, frente a aproximadamente **0,849** con las áreas reales. En el texto habitual, 44 de 45 parejas superan su propia referencia mediana; **SPECTER–BERT es la excepción**. Con texto común la superan las 45. No son pruebas de significación ni evidencias de «verdad» de las etiquetas.

Estos controles de centros se añadieron después de observar el primer resultado y están identificados como seguimiento en el protocolo. Su referencia positiva debe acompañar cualquier afirmación de gran acuerdo.

### La receta importa

En los cuatro BERT que representan palabras, hay que decidir cómo resumir su salida para obtener un vector del artículo. Mantuvimos la media como receta principal, fijada antes de ver acuerdos, y comprobamos dos posiciones especiales alternativas, llamadas CLS y SEP.

Cambiar los cuatro a CLS mueve CKA una cantidad absoluta mediana de **0,101**; cambiarlos a SEP, **0,090**. Dentro del propio BERT, media frente a SEP da solo **0,307** de similitud de forma mediana. Por tanto, el nombre del modelo por sí solo no define un mapa reproducible.

Con exactamente los mismos 2.048 candidatos por celda, la coincidencia de vecinos es **31,9%** con la receta principal, **23,9%** con CLS y **27,6%** con SEP. Esto no demuestra que la media sea más correcta: mide acuerdo, no acierto. No hemos escogido retrospectivamente la receta que sale mejor. El control de contenido común agrupa por área y usa una selección menor: comparar sus cambios con los de receta no equivale a separar exactamente todas las causas del desacuerdo.

### Leer distinta cantidad de texto explica una parte, no el resultado entero

En 52.000 artículos emparejados, todos los modelos recibieron el mismo contenido literal que cabe en ellos. Los diez terminaron sin recorte adicional. Al comparar los mismos IDs, el cambio absoluto mediano en CKA es **0,005**, aunque llega a **0,088** en una comparación: no es irrelevante en todos los casos.

Para vecinos se mantienen los mismos 400 candidatos por área/período en ambas condiciones. La coincidencia pasa de **42,20% a 42,35%**, una diferencia media de **+0,15 puntos porcentuales**. No comparar ese 42% directamente con el 30% del corpus completo: el conjunto de candidatos es mucho menor. El cambio varía de −4,36 a +3,98 puntos entre comparaciones.

Al repetir el control de forma con selecciones emparejadas de 1.000 artículos por área, la diferencia mediana respecto al efecto con 2.000 es **0,00023**, con máximo **0,00381**. La amplitud central del cambio tiene mediana **0,00617**, máximo **0,02603**. Son variaciones dentro de la selección fija; no intervalos de confianza sobre OpenAlex.

### MiniLM: diagnóstico y nueva pasada terminados

**No había un error en nuestro código:** el uso habitual del modelo limita la lectura a 256 piezas de texto. Su arquitectura admite 512. Calculamos esa variante larga por separado sobre los 500.000 artículos, conservando el original como principal. La capacidad de leer más no demuestra que haya aprendido a usar mejor ese texto. [Ficha oficial](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

| Comprobación | MiniLM habitual | MiniLM ampliado |
| --- | ---: | ---: |
| Límite de lectura | 256 | 512 |
| Artículos con texto recortado | 247.910 | 34.331 |
| Porcentaje afectado | **49,58%** | **6,87%** |

Se recalcularon 247.910 vectores y se reutilizaron 252.090 idénticos, comprobados número por número. La ejecución tardó unos **23 minutos**. La forma original/ampliada tiene similitud mediana **0,974**, pero conserva **82,25%** de sus propios vecinos: la longitud sí mueve relaciones locales.

Frente a los otros nueve modelos, ampliar MiniLM aumenta la coincidencia media solo **0,78 puntos porcentuales**, y la forma CKA **0,014** de media. No explica por sí solo el desacuerdo observado entre modelos. Ambas variantes quedan guardadas; no se cuenta la ampliación como un modelo independiente.

### Calidad, cantidad y familias

| Comprobación | Resultado | Consecuencia |
| --- | --- | --- |
| Apartar marcas de calidad y repetidos según la regla fijada | Quedan **448.886** artículos; cambio absoluto mediano CKA **0,012**, máximo **0,155**. | El efecto típico es moderado, pero hay casos sensibles. No afirmar que la calidad nunca importa. |
| Vecinos k=10 / 25 / 50 | Coincidencia media **26,2% / 30,3% / 33,9%**. | Cambiar la cantidad de vecinos no elimina el desacuerdo. |
| Descontar coincidencia uniforme por azar, k=25 | **29,6%**, frente a 30,3% sin ajustar. | No es una corrección completa de tamaño o densidad; también se usa el control de 2.048 candidatos. |
| Excluir una familia de modelos cada vez | Vecinos medios entre **31,2% y 36,1%**. | El resultado no depende solo de incluir los cuatro BERT de palabras; al quitarlos queda 36,1%. |
| Mezclar la identidad de los artículos | CKA mediana cerca de **0**; Procrustes **0,205**. | Procrustes tiene un fondo positivo en esta prueba; no leer todas las medidas con el mismo cero. |
| Tres medidas de forma | Correlación mediana de sus ordenaciones de parejas: CKA–Procrustes **0,884** y CKA–rangos **0,881**. | Hay apoyo de medidas con sensibilidades distintas, sin presentarlas como votos independientes. |

El caso más sensible a la criba de calidad es **SciNCL–BioBERT en Artes y humanidades, 2000–2004**: CKA pasa de 0,391 a 0,547. Esa excepción se conserva y limita afirmaciones específicas sobre ese grupo. La criba cambia la población operativa y no reemplaza silenciosamente el corpus.

## Dónde hay más diferencias

La tabla está ordenada de menor a mayor acuerdo de forma. Presenta todas las áreas para evitar elegir solo ejemplos favorables. Los resúmenes dan el mismo peso a los cinco períodos y a las 45 parejas.

| Área | Artículos | Forma¹ | Vecinos, todos² | Vecinos, 2.048² | Alertas³ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Medicina | 78.669 | 0.474 | 24.2% | 29.8% | 2 |
| Profesiones de la salud | 11.493 | 0.494 | 30.2% | 30.6% | 0 |
| Psicología | 13.045 | 0.530 | 30.2% | 31.1% | 0 |
| Empresa y contabilidad | 13.218 | 0.533 | 27.5% | 28.4% | 0 |
| Economía y finanzas | 11.509 | 0.553 | 29.7% | 30.2% | 6 |
| Artes y humanidades | 12.630 | 0.555 | 25.4% | 26.4% | 0 |
| Veterinaria | 10.827 | 0.562 | 34.2% | 34.4% | 0 |
| Bioquímica y genética | 24.497 | 0.565 | 29.9% | 32.9% | 3 |
| Agricultura y biología | 19.423 | 0.566 | 30.5% | 33.2% | 9 |
| Ciencias sociales | 37.549 | 0.567 | 23.8% | 28.4% | 11 |
| Ingeniería | 67.148 | 0.569 | 25.3% | 32.6% | 6 |
| Ciencias de la decisión | 10.830 | 0.571 | 32.7% | 32.9% | 0 |
| Odontología | 10.825 | 0.571 | 32.9% | 33.2% | 0 |
| Informática | 32.828 | 0.573 | 27.8% | 32.3% | 1 |
| Ciencia de materiales | 14.233 | 0.593 | 29.1% | 30.5% | 0 |
| Inmunología y microbiología | 10.830 | 0.599 | 30.8% | 31.0% | 0 |
| Ciencias ambientales | 18.984 | 0.599 | 31.5% | 34.0% | 12 |
| Farmacología y toxicología | 10.830 | 0.612 | 33.2% | 33.5% | 0 |
| Enfermería | 10.830 | 0.617 | 34.1% | 34.4% | 0 |
| Neurociencias | 10.830 | 0.620 | 34.6% | 34.9% | 0 |
| Física y astronomía | 14.822 | 0.636 | 31.3% | 33.3% | 0 |
| Ciencias de la Tierra | 10.830 | 0.643 | 33.6% | 34.0% | 0 |
| Matemáticas | 10.830 | 0.664 | 28.9% | 29.1% | 0 |
| Química | 10.830 | 0.665 | 29.7% | 30.1% | 0 |
| Ingeniería química | 10.830 | 0.668 | 32.7% | 33.1% | 0 |
| Energía | 10.830 | 0.764 | 33.6% | 34.0% | 0 |

¹ Mediana CKA corregida; más alto significa más parecido entre estas representaciones, no mayor calidad científica. ² Media del porcentaje de los 25 vecinos compartidos, sin ajuste por azar; «todos» usa todos los candidatos del área/período, y «2.048» iguala su número. ³ Comparaciones que no superan la comprobación de estabilidad, de 225 por área.

Medicina tiene el menor acuerdo de forma y Energía el mayor. Este orden apenas cambia en la comprobación de tamaño. En vecinos, comparar áreas exige más cuidado: Ingeniería pasa de **25,3% a 32,6%** al igualar candidatos. Artes y humanidades sigue en la parte baja, con **26,4%** en ese control. No confundir un conjunto de búsqueda más grande con una disciplina intrínsecamente menos estable.

## Los 50 casos que debemos señalar

Se hicieron 20 selecciones de 1.024 y 20 de 2.048 artículos por área/período. **5.800 de 5.850 comparaciones (99,15%)** superan la regla fijada. Las 50 restantes pertenecen a 13 grupos:

| Área | Período | Comparaciones señaladas de 45 | Mayor amplitud |
| --- | --- | ---: | ---: |
| Agricultura y biología | 2010–2014 | 5 | 0.048 |
| Agricultura y biología | 2020–2024 | 4 | 0.045 |
| Bioquímica y genética | 2005–2009 | 3 | 0.044 |
| Informática | 2010–2014 | 1 | 0.041 |
| Economía y finanzas | 2020–2024 | 6 | 0.056 |
| Ingeniería | 2010–2014 | 5 | 0.047 |
| Ingeniería | 2015–2019 | 1 | 0.041 |
| Ciencias ambientales | 2015–2019 | 5 | 0.048 |
| Ciencias ambientales | 2020–2024 | 7 | 0.064 |
| Medicina | 2005–2009 | 1 | 0.041 |
| Medicina | 2010–2014 | 1 | 0.040 |
| Ciencias sociales | 2015–2019 | 6 | 0.052 |
| Ciencias sociales | 2020–2024 | 5 | 0.045 |

Todas superan el criterio de cambio de mediana al pasar de 1.024 a 2.048; las 50 alertas corresponden a una amplitud central superior a 0,04. El mayor caso es SPECTER2–BioBERT en Ciencias ambientales 2020–2024, con amplitud **0,0636**. La diferencia absoluta entre la mediana a 2.048 y el resultado con todas las filas tiene máximo **0,00891**.

**Decisión dentro de la delegación: no ampliar ahora todo el corpus.** Los resultados principales ya usan todas las filas, no solo 2.048. Los patrones amplios resisten las comprobaciones y los centros, textos y candidatos tienen controles separados. Las alertas se mantienen: no usar pequeñas diferencias entre parejas de esos grupos como conclusiones firmes ni cambiar el umbral para que aprueben. Esta prueba no demuestra representatividad universal ni precisión poblacional; una futura afirmación que dependa de esos casos concretos necesitará una comprobación dirigida.

## Cómo lo presentaría y qué falta

La idea central para el paper es **qué parte del mapa depende de la herramienta y de su receta**, desde relaciones entre áreas hasta vecinos de cada artículo. No propondría un ranking del «mejor modelo». Tampoco un artículo basado solo en diez dibujos bonitos o en contar vecinos, que ya tiene antecedentes.

La revisión de [Imel y Hafen](https://arxiv.org/html/2506.23366v1) y [ReSi](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2eef1f75516b0cfd3e944345e5f88c08-Abstract-Conference.html) ayuda a situar la aportación: selección común de artículos, cobertura de 26 áreas y controles emparejados de texto, receta, tamaño y calidad. El detalle y los límites de esta búsqueda dirigida están en [METRIC_REVIEW.md](research/analysis_2026-09-17/METRIC_REVIEW.md). No se ha demostrado prioridad absoluta ni garantizado encaje editorial.

[PAPER_OUTLINE.md](PAPER_OUTLINE.md) fija el argumento y una selección de cuatro figuras principales. El siguiente paso es convertir estos resultados y [METHODS_ANALYSIS.md](METHODS_ANALYSIS.md) en un borrador, contrastando de nuevo los antecedentes más próximos. La fase de cálculo pedida está cerrada; no hace falta otra descarga ni repetir los diez modelos para comenzar a escribir.

No extrapolar a toda la literatura mundial, todos los modelos o todos los idiomas. Las etiquetas de OpenAlex son automáticas y no son una verdad externa. Los modelos comparten entrenamiento y sus 45 parejas no son independientes. Los cambios entre períodos son descriptivos: no prueban una evolución histórica causal. La mayor estabilidad entre centros tampoco valida individualmente todas las relaciones entre áreas.

## Archivos y comprobaciones

- [Resumen numérico completo](reports/analysis_v1/final/summary.json) y [auditoría final](reports/analysis_v1/final/audit.json): coberturas completas, huellas, IDs, valores y denominadores reconciliados.
- [Catálogo de entrega](reports/analysis_v1/final/catalog.json): tablas, figuras y huellas de archivos. Ocho figuras, cada una en PDF/SVG/PNG, y 33 tablas CSV.
- [Resumen de las 26 áreas](reports/analysis_v1/final/tables/field_summary.csv) y [detalle de estabilidad](reports/analysis_v1/final/tables/shape_sample_stability.csv).
- [Resultado por artículo](reports/analysis_v1/final/article_neighbor_stability.parquet): 500.000 IDs con sus medias y extremos de coincidencia entre parejas; las listas exactas de vecinos están en `data/analysis_v1/neighbors/`.
- [Auditoría de nuevas representaciones](research/analysis_2026-09-17/extra_output_audit/): MiniLM 512 y diez controles comunes; 1.020.000 filas modelo–artículo verificadas, incluidas 520.660 reutilizadas exactamente.
- Vecinos: **13.260 consultas reales** contrastadas con ordenación completa independiente; comprobación de autoexclusión, IDs, candidatos y archivos. Métodos: once pruebas específicas nuevas, además de las ocho del lector ya superadas.
- Resultados intermedios y copias de programas: `data/analysis_v1/`; inventario en [DATA_CATALOG.md](DATA_CATALOG.md). No usar `reports/analysis_v1/preview/` como entrega final.

Para regenerar **solo la entrega** a partir de resultados guardados, sin volver a calcular modelos ni buscar vecinos:

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_analysis.report --require-complete
```

El comando vuelve a comprobar la integridad de las salidas antes de escribir el informe. No publicar datos ni enviar el manuscrito sin la instrucción correspondiente del usuario.
