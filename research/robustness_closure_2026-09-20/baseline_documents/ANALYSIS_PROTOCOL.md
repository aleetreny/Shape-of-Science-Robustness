# Protocolo de comparación: primera ejecución

**17-09-2026. Decisiones tomadas por delegación explícita del usuario.** Se fija antes de calcular acuerdos entre modelos. Sustituye las propuestas pendientes de `ANALYSIS_PROPOSAL.md` dentro de esta fase. Configuración exacta: `config/analysis_v1.json`.

## Pregunta y medida principal

Preguntamos cuánto depende el mapa del modelo, usando siempre los mismos artículos. La medida principal será **CKA lineal con corrección del sesgo por tamaño**: compara relaciones entre artículos, admite dimensiones distintas y evita parte de la similitud artificial que puede aparecer con pocos artículos y muchas coordenadas. Se conservarán valores negativos cuando aparezcan; no significan una geometría «negativa», sino ausencia de alineación detectable con ese estimador.

No consideraremos que una cifra por sí sola describa toda la forma. Se añaden dos comprobaciones fijadas de antemano:

- **Procrustes angular:** cuánto falta para alinear las nubes de puntos después de trasladar, girar/reflejar y ajustar una escala global, sin deformarlas libremente. Las dimensiones menores se entienden completadas con ceros. Se conservará también su similitud de alineación; son dos expresiones del mismo cálculo, no dos confirmaciones independientes.
- **RSA de rangos:** si los mismos pares de artículos aparecen relativamente cerca o lejos, mediante correlación de rangos de distancias coseno. Usa 20.000 pares aleatorios reproducibles por contexto, sin tratar esos pares como observaciones independientes para intervalos poblacionales.

La corrección de CKA, las distancias de forma y las comparaciones de rangos tienen límites diferentes. Buscaremos conclusiones que sobrevivan a esas diferencias; los desacuerdos se mostrarán. No se elige la medida que produzca la historia más atractiva. Una permutación independiente de IDs por modelo y celda será una referencia diagnóstica de azar, **no un test de significación**. Procrustes ajustado y medido sobre los mismos puntos puede tener un nivel de fondo apreciable; se interpretará con esta referencia y con estabilidad por tamaño.

## Recetas y población

- Diez modelos aceptados, en sus versiones congeladas. Media para SciBERT, BERT, PubMedBERT y BioBERT como regla común; las otras dos salidas guardadas se usan como controles. SEP tiene un antecedente relevante en el mapa biomédico; no se presupone que la media sea superior ni se escoge mirando nuestros resultados.
- Igualar la longitud de cada vector para comparar direcciones; centrar las columnas para las medidas de forma. No aplicar blanqueamiento, PCA, UMAP o correcciones aprendidas que eliminen diferencias que queremos estudiar. Repetir la forma con valores originales como control.
- Usar **todos los artículos disponibles en cada una de las 130 celdas Field/período**. Conservar los 500.000; no limitar todos los Fields por el menor.
- Resultado conjunto de población: solo los **400.000 de base**. Un promedio de las 130 celdas será una vista con igual peso por área y período, etiquetada como tal. No confundirlo con las proporciones de OpenAlex ni con una geometría global calculada directamente.
- Relaciones entre áreas: centros de los 26 Fields dentro de cada período, calculados a partir de vectores de artículos de longitud igual; comparar las 325 relaciones entre centros. Complementa la forma interna y evita confundir «separar áreas» con conservar lo que ocurre dentro de ellas.
- Los períodos describen cómo modelos actuales representan literatura de distintas fechas. No son reconstrucciones de qué sabía un modelo en cada año ni pruebas causales de evolución de la ciencia.

## Estabilidad y controles

La sensibilidad a la selección se examina con 20 selecciones emparejadas de 1.024 y 2.048 artículos por celda. Criba operativa heredada del estudio de viabilidad: cambio de mediana ≤0,02 y amplitud central del 95% ≤0,04 a 2.048. Es una comprobación de estabilidad dentro del corpus, no un intervalo poblacional ni un requisito de QSS. Se registrarán celdas y pares que fallen; no se ocultarán ni se cambiará el umbral después.

Calidad: repetir apartando los casos con las marcas fijadas en la configuración y reteniendo un solo registro por grupo conectado de DOI/texto normalizado duplicado. No se borra nada del corpus original. Cambia la población analizada: se documentará su tamaño y composición. Los dos cambios de receta de los cuatro BERT se harán de manera común (todos CLS, todos SEP), sin buscar entre combinaciones el mayor acuerdo.

Las familias de entrenamiento se usarán para describir dependencias y repetir los resúmenes omitiendo cada familia. Los diez modelos y sus 45 pares no son réplicas independientes ni una muestra aleatoria de todos los modelos posibles.

## Texto común y MiniLM

**MiniLM no presenta un error de límite en nuestro código:** la configuración oficial usa 256 fragmentos de palabra y la arquitectura permite hasta 512. Conservar 256 como uso habitual; calcular 512 aparte como control de longitud. Ampliar no garantiza mejor representación ni hace que todos los abstracts quepan. No sustituir retrospectivamente el original ni contar la variante como un undécimo modelo independiente.

Se amplía el control común a **52.000 artículos: 400 por celda y 2.000 por Field**, elegidos mediante una huella de ID y semilla, ajena a los acuerdos. Mantener los caracteres originales del título y el comienzo del abstract que quepan en todos los modelos; conservar los separadores habituales. El control principal se interpretará por Field reuniendo los cinco períodos con igual peso. Sus celdas de 400 sirven de diagnóstico, no sostienen por sí solas todas las conclusiones temporales.

Es un presupuesto acotado y reproducible, no un tamaño universalmente suficiente. Se contrastará n=1.000 frente a los 2.000 por Field y el resultado nativo frente al común **sobre exactamente esos mismos IDs**. Si no es estable, la conclusión correspondiente quedará limitada o se justificará una ampliación concreta. Los artículos cuyo texto y receta no cambien pueden reutilizar sus vectores verificados; no se vuelven a calcular por obligación. Los 1.300 del control técnico se conservan como historial separado.

## Vecinos, después de la forma

Para cada uno de los 500.000 artículos, buscar los más cercanos dentro de su misma área y período, excluyendo el propio artículo. Cálculo exacto por bloques, con distancia coseno. Principal: 25 vecinos; controles: 10 y 50. Reportar proporción compartida y corrección por la coincidencia esperada por azar según el tamaño del grupo. No confundir 25 compartidos con 25%.

Como control de la frontera entre áreas, 100 consultas por celda —13.000 en total— buscarán vecinos entre los 400.000 artículos de base, sin restringir área o período. Es una comprobación global sobre consultas seleccionadas, no los vecinos globales de los 500.000. La referencia será idéntica entre modelos. Se validará el cálculo numérico contra CPU de mayor precisión en consultas fijadas y se registrarán empates/cambios cerca del corte.

El acuerdo de vecinos ya tiene antecedentes. La contribución buscada es identificar **qué conclusiones sobre áreas y períodos se conservan al cambiar de modelo, receta y cantidad de texto**, y cuándo el acuerdo general oculta cambios locales. No se promete prioridad o aceptación editorial.

## Presentación prevista antes de ver resultados

1. Matriz de los diez modelos y mapa de 26 áreas × cinco períodos para la forma; distinguir vista proporcional y vista equilibrada.
2. Comparación de las tres medidas de forma, estabilidad por tamaño y referencias de azar.
3. Relaciones entre áreas que se conservan o cambian; comprobar que no se confunden con la forma interna.
4. Cambio al igualar texto y al ampliar MiniLM, sobre IDs emparejados.
5. Forma frente a conservación de vecinos, con distribución por artículo y áreas; resúmenes y casos ilustrativos seleccionados por una regla explícita.

Las figuras definitivas se adaptarán a lo encontrado sin ocultar controles o comparaciones adversas. La configuración y los resultados completos quedan guardados en salidas separadas, con huellas y reanudación.

## Fuentes primarias y alcance de la búsqueda

Búsqueda dirigida el 17-09-2026, no revisión sistemática ni censo de todos los métodos. Metadatos arXiv y parámetros en `research/analysis_2026-09-17/sources/`.

- [Kornblith et al. (2019)](https://proceedings.mlr.press/v97/kornblith19a.html): comparación de representaciones con CKA.
- [Williams et al. (2021)](https://proceedings.neurips.cc/paper/2021/hash/252a3dbaeb32e7690242ad3b556e626b-Abstract.html): distancias de forma, invariancias y convergencia con el tamaño de muestra.
- [Ding et al. (2021)](https://arxiv.org/abs/2108.01661): los métodos tienen debilidades distintas; contrastar cambios conocidos, no asumir que similitud geométrica equivale a igual comportamiento.
- [Correcting Biased CKA (2024)](https://arxiv.org/abs/2405.01012): demuestra problemas de CKA sin corrección al variar dimensiones/muestras. Se consulta el preprint; la motivación se traslada con cautela desde datos neurales a este corpus.
- [ReSi, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2eef1f75516b0cfd3e944345e5f88c08-Abstract-Conference.html): comparación amplia de medidas; no hay una vencedora universal. CKA tiene respaldo en sus pruebas de lenguaje, que no equivalen a mapas científicos.
- [MiniLM, ficha oficial](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2): límite habitual, uso previsto y entrenamiento. Se contrasta con los archivos de la revisión fijada localmente.
- [Imel y Hafen, versión 1 (2025)](https://arxiv.org/html/2506.23366v1) y `ACADEMIC_MODEL_USAGE.md`: antecedentes de geometría local y mapas científicos. La originalidad deberá argumentarse sobre resultados y controles, no sobre usar vecinos por primera vez.

La guía de búsqueda utilizada se registra como herramienta, no como evidencia científica de las decisiones: [Kassis et al., Scientific Agent Skills](https://arxiv.org/abs/2609.00065). Registro actualizado consultado durante esta búsqueda.

## Ajuste técnico anterior a los resultados de vecinos

La prueba de coste con datos artificiales estima unos 13 minutos para buscar todos los vecinos internos con CPU y precisión de 64 bits. Se elige esta implementación exacta, más precisa, en vez de la GPU de 32 bits inicialmente prevista; así la GPU puede terminar los controles de texto. `config/neighbors_v1.json` registra el ajuste sin cambiar el protocolo congelado en uso por otros procesos. No cambia k, referencias, consultas ni objetivos. Para tratar diferencias de redondeo se comparan puntuaciones a doce decimales y se resuelven empates por `row_index` menor. Se contrasta con una implementación independiente y distintos tamaños de bloque. Se documentará el tiempo real; la estimación no es una garantía.

## Detalle del control de recetas

Además del cambio común de receta en los cuatro BERT, se contrastan directamente media/CLS/SEP dentro de cada uno, sobre las mismas filas de cada celda. Esto aísla el efecto de resumir un mismo modelo de tres maneras. Se concreta antes de inspeccionar los resultados de esos controles; no se elige una receta nueva según el acuerdo obtenido. No requiere inferencia adicional.

## Control añadido antes de inspeccionar los acuerdos de vecinos

Los grupos tienen tamaños diferentes. Corregir la coincidencia por azar no elimina todo el efecto de ofrecer más candidatos. Se añade una comparación separada con exactamente **2.048 candidatos por cada área y período**, elegidos por una huella del ID con semilla `sos-v1-equal-neighbors`. Todos los modelos reciben los mismos candidatos. Se comparan k=10/25/50 y las tres recetas comunes de los cuatro BERT. Usa vectores existentes, no cambia el análisis principal ni busca una receta ganadora. Permite distinguir sensibilidad al modelo, al conjunto de candidatos y a la receta. La regla se añade antes de calcular o inspeccionar los resúmenes de coincidencia de vecinos, tras detectar esta limitación del diseño; no se presenta como un registro externo anterior a todo el trabajo.

## Comprobación de relaciones entre áreas, añadida después de su primer resultado

El resultado nativo entre centros mostró más acuerdo que las relaciones entre artículos dentro de las áreas. Antes de convertirlo en una conclusión fuerte se decide repetir las 325 relaciones con CLS, SEP, la criba de calidad y vectores originales. También se compara texto habitual/común sobre los mismos 52.000: 2.000 artículos por Field, reuniendo los cinco períodos por igual. Este último control es una vista temporalmente equilibrada, no la geometría proporcional de los 400.000 de base ni cinco pruebas principales con solo 400 artículos por Field. Se comprueba primero que reconstruir la receta principal reproduce su resultado guardado. Es un seguimiento motivado por el primer resultado, declarado como tal; no se presenta como fijado antes de verlo. Código y salidas separados: `sos_analysis/macro_controls.py` y `data/analysis_v1/macro_controls/`.

Además, para comprobar el efecto de resumir muchos artículos en un centro, se calcula una referencia de **20 repartos aleatorios** de esos 52.000 en 26 grupos de 2.000, manteniendo exactamente 400 de cada período por grupo. Cada reparto es idéntico en los diez modelos; se comparan las entradas habituales y comunes. Semillas fijadas con prefijo `sos-centroid-random-groups-v1`; no se buscan particiones favorables. No es una prueba de significación ni convierte los 45 pares dependientes en réplicas. Esta referencia permite ver si el acuerdo entre centros también aparece sin conservar las áreas reales. Es otra comprobación posterior al resultado inicial y anterior a inspeccionar su propio resultado, con programa y salida separados.
