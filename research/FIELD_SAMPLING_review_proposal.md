> HISTÓRICO: propuesta previa, sustituida por la decisión delegada de `../CORPUS_PROTOCOL.md`.

# Cómo repartir los papers: propuesta revisada

14-09-2026. **Recomendación pendiente de aceptar.** No se han elegido papers, ejecutado experimentos ni ampliado la extracción.

## Respuesta breve

No pondría a todas las áreas el límite de la más pequeña. Propondría **una selección al azar que respete el tamaño de cada área y año, con un complemento para las áreas que necesiten más papers para obtener resultados precisos**. Todos los modelos estudiarían exactamente los mismos papers en cada comparación.

Es como fotografiar un bosque: la foto general debe respetar cuántos árboles hay de cada clase. Podemos tomar más fotos de una especie escasa para estudiarla mejor, sin hacerla parecer más abundante en la foto general.

Los 5.000 por Field y 200 por año anteriores eran un presupuesto práctico sin justificación suficiente como tamaño final. Esa propuesta queda sustituida por esta revisión, también pendiente de aprobación. Se conserva la [versión anterior](../research/FIELD_SAMPLING_initial_proposal.md).

## Reparto propuesto

1. **Definir qué literatura estudiamos.** Mismos años, idioma, tipos de trabajo y requisitos del texto. La referencia actual es 2000–2024; conviene valorar incluir congresos, especialmente para Informática e Ingeniería. No se ha cerrado ningún filtro nuevo.
2. **Crear una base común proporcional.** Si un área representa el 10 % de los trabajos elegibles, aporta aproximadamente el 10 % de esta base. Selección al azar dentro de cada área y año, sin elegir papers por citas, prestigio o parecido según uno de los modelos que vamos a comparar.
3. **Completar las áreas que lo necesiten.** Si la base común deja una comparación por área demasiado imprecisa, añadir papers de esa área, también al azar. No es necesario que todas terminen con el mismo número. La necesidad depende también de la variedad de sus temas, no solo del tamaño del área.
4. **Separar las dos lecturas.** Para la forma conjunta de la ciencia, usar la base proporcional. Para estudiar cada Field, usar además su complemento. Los papers compartidos solo se procesan una vez por modelo. Un promedio de resultados por área no sustituye al análisis conjunto de las relaciones entre áreas.

Así se aprovechan los Fields grandes sin dejar los pequeños con unos pocos ejemplos. Es una recomendación adaptada a esta pregunta, no una regla universal demostrada como óptima.

## Cuántos y cómo justificarlo

No hay evidencia para fijar ahora 5.000, 50.000 o cualquier otra cifra como suficiente. Tampoco hay una obligación de reducir los 2,38 millones a una muestra pequeña. Tener SPECTER2 calculado ahorra trabajo, pero cada modelo nuevo todavía tendrá que procesar los textos que elijamos.

Antes del estudio final, una prueba de tamaño debe comprobar cuánto varían las medidas al repetir la selección y al añadir papers. Hay que fijar previamente qué margen de variación toleramos, el límite de recursos y la regla para ampliar cada área. Se busca precisión, no parar cuando los modelos parezcan coincidir. La prueba debe representar los modelos y comparaciones previstos; SPECTER2 solo no demuestra la suficiencia para los demás.

Después se fija el tamaño y el procedimiento del estudio final. Puede requerir cientos de miles o millones: todavía no se ha medido. Un umbral razonable exige una decisión científica explícita; ningún reparto elimina todas las decisiones humanas.

## Cómo tratar los años

Sí, controlar el año desde la selección. **Dentro de cada área, conservar el peso de cada año en la población elegible**, también al añadir un complemento. No imponer 200 por año ni dar automáticamente el mismo peso a 2000 y 2024.

Para preguntar si la coincidencia entre modelos cambia con el tiempo, comparar los mismos períodos entre modelos y áreas. La duración de esos períodos se decidirá según los datos y la precisión disponible. Si se busca una comparación con idéntica composición temporal entre áreas, será una comprobación adicional expresamente definida; el reparto proporcional por sí solo no elimina diferencias de edad entre Fields.

## Qué hacen trabajos relacionados

| Trabajo | Qué hicieron | Qué aporta aquí |
| --- | --- | --- |
| [Boyack et al., 2011, PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0018029) | Compararon nueve métodos de semejanza textual sobre 2.153.769 publicaciones biomédicas. | Comparar métodos puede hacerse con millones de documentos; no exige un tamaño pequeño. No estudian nuestros 26 Fields. |
| [González-Márquez et al., 2024, Patterns](https://doi.org/10.1016/j.patter.2024.100968) | Construyeron un mapa de 20.687.150 papers; algunos ensayos usaron un subconjunto de un millón y varias medidas se estimaron sobre selecciones menores. | El tamaño del corpus y el número de papers evaluados en cada cálculo son decisiones diferentes. |
| [Imel y Hafen, 2025, preprint](https://arxiv.org/abs/2506.23366) | Compararon cinco representaciones en 53.080 papers de nueve disciplinas, con 4.114–7.556 por disciplina después de filtrar. | No igualaron obligatoriamente el tamaño final. Su selección estuvo guiada por SciBERT; no conviene copiarla al evaluar la dependencia del modelo. |

La literatura de muestreo distingue repartir según el tamaño de los grupos y asegurar precisión dentro de cada grupo: [Statistics Canada](https://www150.statcan.gc.ca/n1/pub/12-001-x/2017001/article/14817/03-eng.htm). [Lakens, 2022](https://doi.org/10.1525/collabra.33267) explica por qué el tamaño debe justificarse por el objetivo, la precisión o los recursos. Estas fuentes apoyan el razonamiento; no fijan un número óptimo para nuestros modelos.

## Qué impide hacerlo automáticamente con los datos actuales

- El TFM limitó a 400 papers por Subfield y año. Por eso los 2.378.036 actuales **no conservan las proporciones naturales**. Elegir al azar entre ellos no corrige ese reparto.
- Los recuentos actuales de OpenAlex son anteriores a la limpieza. Las proporciones finales deben referirse a la población que supera los filtros; habrá que estimarlas o contarla siguiendo un procedimiento documentado. Las probabilidades de selección del TFM no se reconstruyen exactamente tras sus descartes y reposiciones.
- Para una base proporcional defendible, primero fijar la selección y sus probabilidades; recuperar de los archivos existentes los IDs seleccionados y descargar solo lo que falte. Conservar sin más todos los trabajos antiguos y añadir otros no convierte el conjunto en representativo.
- Algunas medidas de forma cambian con el número de puntos o de vecinos disponibles. Añadir un chequeo con tamaños comparables y referencias controladas permite distinguir ese efecto del cambio de modelo. Ponderar solo un resultado final no corrige automáticamente estas diferencias.

Disponibilidad comprobada en el catálogo principal: **61.061.439 candidatos clasificados**, o **70.050.675 añadiendo congresos**, antes de limpieza. OpenAlex ofrece además un catálogo ampliado: eleva esas cifras a 73.176.918 y 82.760.353, pero su inclusión requiere revisar su cobertura y no está decidida. Ver [recuentos completos y límites](../OPENALEX_COUNTS.md). Veterinaria tiene 101.802 candidatos básicos en el principal; sus 19.573 locales no son el techo de las demás áreas.
