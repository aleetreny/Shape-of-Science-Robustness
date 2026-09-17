# Cómo ha quedado el reparto

Comprobado el **15-09-2026**, sobre la copia final `data/corpus_clean_v1/corpus.parquet`.

**El reparto parece razonable para comenzar la comparación. No recomiendo ampliar la descarga ahora.** Hay 500.000 artículos: 400.000 de base general y 100.000 de refuerzo. Ninguna combinación de área y período de cinco años queda por debajo de 2.165. Esto da cobertura; la estabilidad de las conclusiones todavía tiene que comprobarse con los modelos elegidos.

## Proporciones por área

“Base” es el porcentaje dentro de los 400.000 artículos de la selección general, después de los filtros. “Final” es el porcentaje dentro de los 500.000, después del refuerzo. **La base aproxima el reparto de la población que cumple nuestros filtros; no son porcentajes exactos de todo OpenAlex.** Los nombres se han abreviado; el CSV conserva los nombres originales.

| Área | Artículos finales | % base | % final |
| --- | ---: | ---: | ---: |
| Agricultura y Biología | 19.423 | 4,73 | 3,88 |
| Artes y Humanidades | 12.630 | 2,67 | 2,53 |
| Bioquímica, Genética y Biología Molecular | 24.497 | 6,12 | 4,90 |
| Empresa, Gestión y Contabilidad | 13.218 | 2,78 | 2,64 |
| Ingeniería Química | 10.830 | 0,30 | 2,17 |
| Química | 10.830 | 1,82 | 2,17 |
| Informática | 32.828 | 8,21 | 6,57 |
| Ciencias de la Decisión | 10.830 | 0,95 | 2,17 |
| Tierra y Planetas | 10.830 | 1,81 | 2,17 |
| Economía y Finanzas | 11.509 | 2,15 | 2,30 |
| Energía | 10.830 | 0,65 | 2,17 |
| Ingeniería | 67.148 | 16,79 | 13,43 |
| Medio Ambiente | 18.984 | 4,64 | 3,80 |
| Inmunología y Microbiología | 10.830 | 1,11 | 2,17 |
| Materiales | 14.233 | 3,33 | 2,85 |
| Matemáticas | 10.830 | 1,15 | 2,17 |
| Medicina | 78.669 | 19,67 | 15,73 |
| Neurociencia | 10.830 | 1,71 | 2,17 |
| Enfermería | 10.830 | 0,52 | 2,17 |
| Farmacología, Toxicología y Farmacia | 10.830 | 0,43 | 2,17 |
| Física y Astronomía | 14.822 | 3,69 | 2,96 |
| Psicología | 13.045 | 2,70 | 2,61 |
| Ciencias Sociales | 37.549 | 9,39 | 7,51 |
| Veterinaria | 10.827 | 0,16 | 2,17 |
| Odontología | 10.825 | 0,56 | 2,17 |
| Profesiones Sanitarias | 11.493 | 1,93 | 2,30 |
| **Total** | **500.000** | **100** | **100** |

Porcentajes redondeados: las columnas pueden no sumar exactamente 100 al sumar lo mostrado.

El cambio es intencionado. Veterinaria tiene 642 artículos en la base y 10.827 con el refuerzo. Medicina conserva sus 78.669. **No hemos reducido todas las áreas al tamaño de la menor.**

Para describir el conjunto de la literatura elegible, usar la base general como referencia. Para comparar áreas pequeñas y períodos, aprovechar el refuerzo. Mezclar los 500.000 y presentar sus porcentajes como el tamaño real de las áreas sería incorrecto. Un análisis conjunto con ponderaciones necesitaría su propia especificación; no se ha cerrado aquí.

## Proporciones por período

| Período | Artículos finales | % base | % final |
| --- | ---: | ---: | ---: |
| 2000–2004 | 68.427 | 9,53 | 13,69 |
| 2005–2009 | 83.908 | 15,13 | 16,78 |
| 2010–2014 | 101.289 | 20,98 | 20,26 |
| 2015–2019 | 107.858 | 22,95 | 21,57 |
| 2020–2024 | 138.518 | 31,41 | 27,70 |
| **Total** | **500.000** | **100** | **100** |

Los años recientes siguen pesando más, como sucede en la base. El refuerzo protege especialmente las combinaciones antiguas y pequeñas. No se han igualado los 25 años ni fijado nuevas cuotas.

## Las combinaciones menos numerosas

| Área | Períodos con el mínimo exacto | Artículos en cada período |
| --- | --- | ---: |
| Odontología | Los cinco períodos | 2.165 |
| Veterinaria | 2010–2014, 2015–2019 y 2020–2024 | 2.165 |
| Profesiones Sanitarias | 2000–2004, 2005–2009, 2010–2014 y 2015–2019 | 2.165 |

Son 12 combinaciones con 2.165. Otras 68 tienen 2.166. La diferencia de un artículo procede del reparto y no es una debilidad científica. Por ejemplo, Veterinaria 2000–2004 pasó de **58 a 2.166**: este era precisamente el problema que resolvía el refuerzo.

Hay datos en las 650 combinaciones área/año, pero el mínimo anual es **282, en Informática de 2000**. No confundir la cobertura de cinco años con haber demostrado precisión para comparaciones anuales. Los cinco períodos siguen siendo la organización vigente.

## Lo más delicado: calidad del texto

El número bruto no cuenta toda la historia. Las marcas conservadas permiten examinar dónde un control más estricto cambiaría más el conjunto:

| Área y período | Artículos actuales | Si omitiéramos tanto idioma dudoso como resúmenes de 50–79 palabras |
| --- | ---: | ---: |
| Matemáticas, 2000–2004 | 2.166 | 1.376 |
| Matemáticas, 2005–2009 | 2.166 | 1.381 |
| Matemáticas, 2010–2014 | 2.166 | 1.414 |
| Matemáticas, 2015–2019 | 2.166 | 1.495 |
| Artes y Humanidades, 2000–2004 | 2.166 | 1.554 |

**Es una cuenta hipotética, no una nueva limpieza ni un diagnóstico de artículos malos.** Se ha contado la unión de ambas marcas, sin duplicar artículos. En total quedarían 449.217 si se aplicara esa regla. Un resumen corto puede ser perfectamente válido, especialmente en Matemáticas. El detector de idioma también puede equivocarse.

Artes y Humanidades 2000–2004 presenta la mayor proporción de idioma dudoso: 230/2.166 = 10,62 %. Conviene comprobar especialmente estas áreas al estudiar si las conclusiones cambian al omitir casos señalados. No se han eliminado registros ni aprobado un umbral nuevo.

## ¿Es suficiente para comparar?

La [prueba de preparación](research/feasibility_2026-09-14/RESULTS.md) comparó SPECTER2 heredado y SciNCL en cuatro casos de Medicina/Veterinaria y dos períodos. Entre muestras de 1.024 y 2.048, el cambio de la medida global fue menor de 0,002 en los cuatro casos. Es evidencia a favor de comenzar con este orden de tamaño.

El límite es concreto: solo se probó un par de modelos, una medida global y dos áreas, sobre pequeñas bases históricas. Las selecciones compartían artículos. Sus rangos no son intervalos de confianza sobre toda la población; no prueban estabilidad en los 26 Fields, en otros modelos o en los vecinos más cercanos de cada artículo.

Recomendación pendiente del protocolo de análisis: usar los mismos artículos para comparar modelos y comprobar si las conclusiones se mantienen al cambiar la selección y su tamaño. Controlar también el tamaño al comparar áreas/períodos; una medida puede variar solo porque hay más artículos. En análisis de vecinos, fijar el conjunto de candidatos para distinguir ese efecto del cambio de modelo. Los umbrales, tamaños de control y medidas aún requieren acuerdo.

**No descargaría más ahora.** Si después falla una comparación concreta, decidir entre ampliar esa parte o limitar la conclusión. Más artículos no arreglan por sí solos errores de idioma, textos pobres o una comparación desigual. El alcance sigue siendo la literatura 2000–2024 que cumple los filtros, no toda la producción científica mundial.

## Evidencia reproducible

- [Tabla por área](research/model_review_2026-09-15/field_proportions.csv), [tabla por período](research/model_review_2026-09-15/period_proportions.csv), [130 combinaciones y marcas](research/model_review_2026-09-15/field_period_diagnostics.csv).
- [Verificación](research/model_review_2026-09-15/balance_verification.json): recuentos calculados directamente del Parquet final y contrastados con las tablas de limpieza; coinciden. Incluye huellas de datos y programa.
- Repetición local: `.venv-audit/bin/python research/model_review_2026-09-15/summarize_balance.py`. Solo lee el corpus y escribe estos resúmenes; no llama a OpenAlex ni calcula embeddings.
- Siguiente propuesta: [MODEL_SELECTION.md](MODEL_SELECTION.md). Modelos todavía sin elegir.
