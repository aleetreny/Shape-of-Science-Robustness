# Qué aporta medir propiedades concretas de la forma

Revisión dirigida, 18-09-2026. No es una revisión sistemática exhaustiva. Se buscaron definiciones, garantías y contraejemplos para tres propiedades fijadas antes de los resultados nuevos. Se usaron fuentes primarias; los resultados de búsqueda secundarios no sustentan las decisiones.

## Selección de propiedades, no de resultados favorables

La forma no es una magnitud única. Una nube puede abrirse sin ganar direcciones; puede alargarse sin separarse; puede tener dos partes unidas por pocos puntos. La elección de medidas se hace explícita y se contrasta con nubes conocidas. Repetir una muestra comprueba estabilidad numérica; **no demuestra que el nombre que damos a la medida sea correcto**.

| Fuente y lectura | Qué justifica aquí | Lo que no se toma de ella |
| --- | --- | --- |
| [Rudman et al., IsoScore, 2022](https://aclanthology.org/2022.findings-acl.262/). PDF: definición y pruebas de invariancia. | Separar dirección media/apertura de distribución de varianza. Una nube puede tener un ángulo medio pequeño y conservar muchas direcciones. | No se aplica IsoScore ni se llama isotropía al coseno medio. No demuestra calidad semántica de nuestros documentos. |
| [Roy y Vetterli, 2007](https://www.eurasip.org/Proceedings/Eusipco/Eusipco2007/Papers/a5p-h05.pdf). Definición, propiedades y ejemplo de covarianza. | Entropía efectiva de una matriz positiva; aquí se usa explícitamente covarianza, no los valores singulares de la matriz de artículos. | No confundir PR, entropía y D80 con tres validaciones temáticas independientes; describen el mismo espectro con énfasis distintos. |
| [Erba, Gherardi y Rotondo, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6868201/). Texto completo: submuestreo y alcance de su estimador. | Justifica no estimar la dimensión intrínseca verdadera con un método local sobre pocos puntos y muchas coordenadas sin controles específicos. | Este piloto no implementa ni valida FCI. PR se llama dimensión efectiva lineal. No se atribuyen las garantías de su estimador a PR. |
| [von Luxburg, 2007](https://www.tml.cs.uni-tuebingen.de/team/luxburg/publications/Luxburg07_tutorial.pdf). Definición de Laplacianos y discusión práctica de grafos/escalas. | La unión y la reciprocidad de vecinos conectan densidades de manera distinta; la conectividad depende de la construcción del grafo. | No se infiere un número verdadero de temas ni se ejecuta partición espectral. La brecha describe conexiones, no fragmentación semántica. |
| [Zelnik-Manor y Perona, 2004](https://proceedings.neurips.cc/paper_files/paper/2004/hash/40173ea48d9567f1f393b20c855bb40b-Abstract.html). PDF: fórmula de escala local. | Comprobar una afinidad con escala por punto, además del grafo sin pesos. | Usamos su fórmula de afinidad sobre soporte kNN, no el algoritmo completo ni su selección del número de grupos. |
| [Rolle y Scoccola, 2024](https://www.jmlr.org/papers/v25/21-1185.html). Resumen y alcance de resultados teóricos. | Una jerarquía que incorpora distancia y densidad merece más cuidado que elegir un corte único; algunas reducciones pueden ser inestables. | No se implementa Persistable ni se trasladan sus teoremas a nuestro enlace simple. No se ha auditado toda la demostración de 74 páginas. |
| [Radovanović et al., 2010](https://www.jmlr.org/papers/v11/radovanovic10a.html). Resumen y definición de ocurrencias como vecino. | Guardar la desigualdad del número de veces que un punto aparece como vecino. Puede influir en el grafo. | Un artículo que aparece muy a menudo no es necesariamente importante o multidisciplinar; no se atribuye causa a esa asociación. |
| [Imel y Hafen, 2025](https://arxiv.org/html/2506.23366v1). Métodos de densidad/asimetría y diseño. | Antecedente directo: geometría local de documentos en varias representaciones y disciplinas. | La aportación no puede ser «medir densidad científica por primera vez». Aquí se estudia dependencia de descripciones respecto al encoder, sin predecir citas. |

## Alternativas consideradas y por qué no resuelven por sí solas fragmentación

- Número de componentes con un k o un radio: puede saturarse o cambiar al variar ese valor. Se calculan varias escalas, conservando componentes pequeños y puntos aislados.
- Arista más larga del árbol de conexión: sensible a un punto extremo. Se acompaña de radios necesarios para conectar fracciones de la masa y de retirada controlada de extremos. El cociente de radios tampoco es universal: falló ante cuatro grupos y una sola nube de pocas direcciones en nuestras simulaciones.
- Brecha de conexión: detecta puentes débiles, pero también nubes alargadas. Referencias gaussianas y controles de dimensión informan esa ambigüedad; no la eliminan por decreto.
- Número de grupos de un algoritmo, silhouette o modularidad: dependen de la partición, escala y grafo. Añadirlos como un único valor no establece un significado externo de «fragmentación». [Fortunato y Barthélemy, 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC1765466/) documentan límites de resolución de modularidad. Se deja fuera una búsqueda de particiones óptimas en este piloto.
- Topología de dimensiones superiores: respondería preguntas sobre huecos/ciclos que aún no tienen una interpretación científica fijada para estos datos. No se añade por ser más sofisticada.

[Kleinberg, 2002](https://www.cs.cornell.edu/home/kleinber/nips15.pdf) muestra incompatibilidad entre tres axiomas de agrupación. No demuestra que toda agrupación sea inútil o imposible; ilustra por qué hay que declarar qué propiedades se priorizan. Aquí no se invoca para sustituir validación empírica.

## Hueco posible en el artículo

La ampliación puede hacer concreta la pregunta actual: **¿se conservan afirmaciones como «esta área se abre más» o «utiliza más direcciones» cuando cambiamos la cámara?** Es una prueba de sensibilidad de afirmaciones geométricas; no una teoría nueva de la organización de la ciencia. Debe acompañar a CKA/vecinos, conservando resultados desfavorables y límites de etiquetas, texto, receta, muestras y coordenadas. La recomendación final se hará después de los resultados, sin cambiar la selección de medidas.

## Trazabilidad bibliográfica

Se consultaron Crossref, exportaciones oficiales ACL/NeurIPS/JMLR y copia editorial EURASIP/depósito Zenodo. Registros: `metadata_records.json`, `metadata_corrections.json`, `bibliography_validation.json`; material completo de terceros solo en la carpeta local ignorada `data/morphology_pilot_v1/literature/`. Erba usa número de artículo 17133; Roy pp. 606–610 de la edición impresa; se corrigieron entidades HTML en dos apellidos de JMLR. No inventar DOI o páginas ausentes de exportaciones oficiales.

Se aplicaron `paper-lookup` y `citation-management`; procedencia en la referencia ya existente [Kassis et al., 2026, v2](https://arxiv.org/abs/2609.00065v2), comprobada de nuevo el 18-09. Es una herramienta de trabajo, no evidencia sobre nuestros resultados. Primeras búsquedas/selección precedieron al cálculo; se amplió la justificación de alternativas durante su ejecución, sin cambiar medidas, muestras o reglas.
