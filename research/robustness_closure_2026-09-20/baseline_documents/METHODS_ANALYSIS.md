# Cómo se ha hecho la comparación

Versión de análisis 1, 17-09-2026. El objetivo es fotografiar **los mismos artículos con diez cámaras** y comprobar qué relaciones se conservan. No intentamos demostrar qué cámara dice la verdad. El protocolo fechado y sus ampliaciones están en [ANALYSIS_PROTOCOL.md](ANALYSIS_PROTOCOL.md); la procedencia de los modelos está en [EMBEDDINGS_AUDIT.md](EMBEDDINGS_AUDIT.md).

## Datos y unidades

Se analizan 500.000 registros distintos de OpenAlex: 400.000 de selección general y 100.000 de refuerzo para grupos pequeños. Son publicaciones de 2000–2024, con los filtros de tipo, idioma, título, resumen y calidad de [CORPUS_PROTOCOL.md](CORPUS_PROTOCOL.md). No representan literatura sin resumen, todos los idiomas ni todo lo publicado en el mundo.

Los mismos IDs y textos de origen se mantienen en los diez modelos. Cada artículo pertenece al Field de su tema principal de OpenAlex, congelado al extraer. Las comparaciones internas usan 26 Fields × cinco períodos de cinco años, con todas las filas disponibles de cada grupo. El resultado global utiliza exclusivamente la base de 400.000. Los promedios equilibrados por las 130 combinaciones se etiquetan como tales; no son estimaciones de las proporciones de OpenAlex.

OpenAlex asigna temas mediante un sistema que utiliza texto, citas y revista. Es una clasificación de trabajo, no una verdad independiente que permita declarar ganador al modelo que mejor la reproduzca. El análisis global y los vecinos globales no requieren imponer esas fronteras a sus candidatos. [Documentación oficial](https://help.openalex.org/data/topics/).

## Qué significa «forma» aquí

Se comparan **relaciones entre artículos identificados**, conservando qué fila corresponde a cada artículo. No se compara solo la silueta de una nube sin etiquetas. Mezclar los IDs puede dejar intacta esa silueta y destruir la correspondencia que interesa al estudio.

No se reduce la dimensión para medir. Un dibujo en dos dimensiones puede deformar las distancias; las cifras se calculan sobre los vectores completos de 384 o 768 componentes. No se usa el parecido visual de dos gráficos como prueba.

La receta principal toma la salida habitual de los seis modelos entrenados para representar documentos o frases. Para los cuatro BERT de palabras utiliza la media de las posiciones no rellenadas, incluidos sus símbolos especiales, como regla común explícita. También se comparan las salidas de la primera posición (CLS) y del último separador (SEP). Esas alternativas son recetas de los mismos modelos, no modelos independientes. No se elige después la receta que más acuerdo produzca.

## Las tres medidas de forma

Primero se divide cada vector por su longitud. Para CKA y Procrustes se resta después la media de las columnas. La corrección del sesgo por tamaño de **CKA lineal** es la medida principal. Procrustes y la comparación por rangos sirven como comprobaciones con distinta sensibilidad, no como votos independientes sobre la misma hipótesis.

Para verificar exactamente la implementación, sean X e Y las matrices ya centradas, con n filas. Se calculan:

```
Sxy = ||XᵀY||²_F
Rxy = suma_i (||X_i||² · ||Y_i||²)
Tx  = suma_i ||X_i||²
Hxy = Sxy − n/(n−2) · Rxy + Tx·Ty/((n−1)(n−2))
CKA_corregida = Hxy / sqrt(Hxx · Hyy)
```

El factor común de HSIC, `1/[n(n−3)]`, se cancela en el cociente. La expresión se contrastó con una implementación alternativa sobre matrices de relaciones con diagonal cero. «Corregida» no significa que el cociente completo sea un estimador perfectamente insesgado en cualquier situación. Se conservan valores negativos y se rechazan entradas degeneradas.

**Procrustes angular** permite girar/reflejar y ajustar una escala global de las matrices preparadas, sin una deformación arbitraria. Su similitud es la suma de valores singulares de `XᵀY` dividida por `sqrt(Tx·Ty)`. El ángulo es su arco coseno, exportado en grados. Las dimensiones diferentes se pueden interpretar completando la menor con ceros. Ángulo y similitud son dos expresiones del mismo resultado. Como la igualación de longitudes ocurre antes del centrado, no se afirma invariancia ante trasladar arbitrariamente los vectores originales y volver a normalizarlos.

**RSA de rangos** compara el orden de las distancias coseno de 20.000 pares de artículos seleccionados sin reemplazo y con semilla guardada. Los mismos pares se usan en los modelos de una comparación. Se emplean rangos medios en caso de empate. No se trata a esos pares como observaciones independientes para calcular significación o intervalos de población.

Referencias: [Kornblith et al., 2019](https://proceedings.mlr.press/v97/kornblith19a.html), [Williams et al., 2021](https://proceedings.neurips.cc/paper/2021/hash/252a3dbaeb32e7690242ad3b556e626b-Abstract.html), [Murphy et al., 2024](https://arxiv.org/abs/2405.01012v1). Sus resultados metodológicos motivan estas elecciones; no validan automáticamente este corpus científico.

## Centros de áreas y vecinos

Para cada modelo y período se calcula la media de los vectores de longitud igual de cada Field. Las 325 distancias coseno entre los 26 centros se comparan mediante correlación de rangos. Esta vista resume relaciones entre áreas; no sustituye medir la organización interna de cada una.

Para cada uno de los 500.000 artículos se buscan exactamente los 50 más cercanos de su mismo Field y período. Se compara la fracción compartida entre modelos para k=25, con k=10 y k=50 como controles. El propio artículo se excluye por ID. El cálculo coseno utiliza números de 64 bits, bloques y todos los candidatos. Se redondea a doce decimales para resolver empates numéricos por la posición global menor. Se contrasta con una implementación independiente por ordenación completa en consultas fijadas.

La coincidencia esperada entre dos listas uniformes independientes es `k/M`, donde M es el número de candidatos tras excluir el propio artículo. La versión ajustada es:

```
(fracción_compartida − k/M) / (1 − k/M)
```

Esto es una referencia combinatoria. No elimina todos los efectos de tamaños, densidades o artículos muy populares como vecinos. Por eso se añade una comparación con los mismos 2.048 candidatos por celda y las tres recetas comunes de los cuatro BERT. La selección se hace por huella de ID, no por las coincidencias observadas.

Además, 100 consultas por celda buscan entre los 400.000 artículos de base sin fronteras de Field o período. Las 13.000 consultas están equilibradas por celda; su promedio no representa automáticamente la mezcla de artículos de toda la población. No se afirma haber buscado vecinos globales para todos los 500.000.

## Controles y límites de la incertidumbre

- **Selección:** 20 selecciones de 1.024 y otras 20 de 2.048 por celda, emparejadas entre modelos. Se conserva la criba previa: diferencia de medianas ≤0,02 y amplitud central del 95% ≤0,04 a 2.048. Son selecciones de un corpus fijo; su rango no es un intervalo de confianza poblacional. La fracción seleccionada varía entre celdas, por lo que una amplitud pequeña cerca del tamaño completo no demuestra igual precisión poblacional.
- **Azar diagnóstico:** una permutación independiente de filas por modelo y celda. No proporciona un valor p. Procrustes se ajusta y mide en los mismos puntos y puede mostrar un fondo positivo; debe leerse junto a esa referencia.
- **Calidad:** se omiten las marcas predefinidas y se conserva el menor `row_index` de cada componente conectado por DOI o texto repetido. La regla de representante se aplica antes de las marcas: si el representante está marcado, puede salir el grupo entero. Esta criba deja 448.886 registros y cambia la población operativa; no es una corrección silenciosa del corpus.
- **Texto común:** 52.000 artículos, 400 por celda. Se preserva el comienzo literal de los textos que cabe en todos los modelos, con sus separadores habituales. Son los mismos caracteres de contenido, no los mismos tokens internos. El resultado principal del control se interpreta por Field: 2.000 artículos, con igual peso de sus cinco períodos. Se contrasta además con selecciones emparejadas de 1.000. Los vecinos del control comparan exactamente los mismos 400 candidatos en ambas condiciones y no se equiparan a los del corpus completo.
- **MiniLM:** se conserva su uso oficial de 256 y se añade una variante de 512, límite que admite su arquitectura. Se reutilizan exactamente los vectores de textos no recortados. La ampliación no garantiza mejor calidad y no convierte todos los abstracts en textos completos. [Ficha oficial](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
- **Familias:** se repiten resúmenes dejando fuera cada una de las tres familias definidas en la configuración. Los modelos comparten arquitecturas, datos y objetivos; sus 45 pares no son observaciones independientes.

## Qué no permite afirmar este estudio

Un acuerdo alto no demuestra verdad temática; un desacuerdo no identifica cuál modelo está equivocado. Los diez modelos son una selección fija con antecedentes y controles, no una muestra aleatoria de todos los modelos ni una evaluación de todos los modelos recientes. Los cuatro BERT de palabras no fueron entrenados específicamente para similitud de documentos.

Los modelos actuales representan artículos de distintas fechas: esto no reconstruye el conocimiento disponible en cada año. Los cambios entre períodos pueden reflejar composición temática, estilo, longitud del texto, cobertura o exposición de los modelos a publicaciones de ciertas épocas. Las tendencias temporales serán descriptivas.

Las decisiones fueron documentadas localmente antes de las comparaciones correspondientes, con ampliaciones posteriores identificadas. No se presenta este registro como una prerregistración externa. La búsqueda bibliográfica es dirigida; no permite asegurar prioridad absoluta. [Ding et al., 2021](https://arxiv.org/abs/2108.01661v2) y [ReSi, 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2eef1f75516b0cfd3e944345e5f88c08-Abstract-Conference.html) explican por qué no se presume una medida universalmente mejor.

## Reproducción

Los programas nuevos están en `sos_analysis/`; las salidas en `data/analysis_v1/`. Cada ejecución conserva implementación, versiones, configuración, huellas y archivos por grupo. No se modifican `sos_embed/`, el entorno de inferencia original ni los vectores principales. `requirements-analysis.txt` fija el entorno numérico separado. Los comandos y la entrega de tablas/figuras están en [ANALYSIS_RESULTS.md](ANALYSIS_RESULTS.md) y [DATA_CATALOG.md](DATA_CATALOG.md); no hay que reiniciar el cálculo original de embeddings para analizarlos.

## Seguimiento de los centros de áreas

Después del primer resultado entre áreas se añadieron controles identificados como posteriores: reconstruir los centros con las recetas CLS/SEP, criba de calidad y vectores sin igualar longitud. La reconstrucción de la receta principal coincidió con la salida ya guardada. También se compararon centros habituales/comunes sobre los mismos 52.000 artículos: 2.000 por Field, con 400 por período, reuniendo las cinco fechas por igual.

Como referencia para el efecto de promediar, se hicieron 20 repartos aleatorios de esos 52.000 en 26 grupos de 2.000. Cada grupo conserva 400 de cada período; la asignación aleatoria es idéntica en los diez modelos, sin consultar los acuerdos. Se calculan las 325 relaciones en cada reparto y condición habitual/común. La referencia conserva la correspondencia de los artículos entre modelos; no es una permutación independiente que destruya esa correspondencia. Por ello su acuerdo puede ser positivo. Se describe su distribución, sin valores p ni inferencia sobre modelos independientes.

Implementación y procedencia: `sos_analysis/macro_controls.py`, `research/analysis_2026-09-17/centroid_random_groups.py` y sus manifiestos separados. Estos controles no cambian la receta principal ni cuentan como decisiones anteriores a toda inspección de datos.

## Estado de la verificación

La entrega final pasó el 17-09-2026. Incluye 130 celdas en las seis etapas de forma, 13.260 consultas de vecinos contrastadas independientemente y los once conjuntos de inferencia adicional comprobados. [audit.json](reports/analysis_v1/final/audit.json) registra cobertura y huellas. El programa de informe reconcilia los resultados guardados; no modifica sus medidas. Las ocho figuras se revisaron visualmente y se conservan también como PDF/SVG para el manuscrito.
