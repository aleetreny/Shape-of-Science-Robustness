# Revisión completa para una primera lectura

**Edición posterior:** [PUBLIC_RELEASE.md](PUBLIC_RELEASE.md) integra los tres párrafos de novedad y conserva esta revisión de claridad. Los PDF enlazados apuntan a la edición vigente.

20 de septiembre de 2026. Petición del autor: releer todo el artículo desde la perspectiva de alguien sin contexto, aclarar conceptos, pruebas y resultados, y conservar la personalidad del texto.

La versión revisada está en [español](output/pdf/es/main.pdf) y en [inglés](output/pdf/main.pdf). El inglés sigue siendo canónico. La revisión personal del autor queda pendiente.

## Qué dificultaba la lectura

El principal problema era la información que el texto dejaba implícita. Una frase podía ser correcta y sencilla, pero exigir recordar qué conjunto se estaba utilizando, qué comparación servía de referencia o qué significaba una palabra en ese apartado. La revisión añade esos enlaces al razonamiento y mantiene los límites científicos.

| Lugar | Dificultad encontrada | Cambio aplicado |
| --- | --- | --- |
| Resumen e introducción | «Representar un artículo» podía sugerir que el modelo leía el trabajo entero. | Se identifican título y resumen como texto de entrada; se explica qué hace el modelo con ellos. OpenAlex se presenta como catálogo bibliográfico. |
| Introducción y preguntas | El paso de organización general a vecinos y dispersión parecía una lista de análisis. | Cada paso tiene una pregunta concreta y se explica por qué se comprueba con otras selecciones de artículos. |
| Antecedentes | Mapa, estructura y dispersión podían parecer sinónimos. | Se distinguen el patrón de relaciones entre objetos, la separación dentro de un área y el dibujo bidimensional que aquí no se analiza. |
| Acuerdo y estabilidad | Se podía interpretar que repetir artículos confirmaba el acuerdo entre modelos. | Se explica qué permanece fijo en cada prueba: artículos al comparar modelos, modelo al cambiar artículos. |
| Datos | Los conjuntos se identificaban sobre todo por números. | Se mantienen nombres ligados a su propósito: experimento de texto y comprobación de fragmento común. Se explica la reutilización de los primeros 26.000 dentro de los 52.000 y el uso de estos últimos en geometría. |
| Datos y Tabla 1 | Faltaba un ejemplo inmediato de grupo de área y período. | Medicina en 2000–04 sitúa la idea; después se explican los cinco períodos, las 26 áreas y los 130 grupos. La tabla funciona como guía de preguntas y artículos. |
| Modelos y Tabla 2 | Se acumulaban tokens, capas, relleno, pooling y pooler. | Primero se explica el paso de texto a salidas y de salidas a un vector. Se distinguen media, CLS y SEP con palabras corrientes. La configuración exacta sigue en la tabla y el suplemento. |
| Centros | Normalización, centro y grupo aleatorio requerían conocimiento previo. | Se introduce la imagen de una flecha; se explica cómo se forma el centro y por qué se redistribuyen los mismos artículos al azar. |
| Vecinos | Se podía perder la diferencia entre artículo de partida, candidato y vecino. | Un apartado propio describe los tres objetos y el modo de comparar dos listas. Cada alcance de búsqueda tiene un propósito explícito. |
| Medidas | Una CKA alta podía leerse como porcentaje correcto; la correlación de rangos quedaba sin interpretación. | Se explica que se comparan patrones de relaciones y órdenes de parejas de modelos. La dirección de lectura de las puntuaciones se da junto a ellas. |
| Dispersión | «Dirección» se utilizaba para objetos distintos. | Se separan hacia dónde apunta el vector, cómo se reparte la variación y qué área tiene el valor mayor. Para este último caso se utiliza «orden persistente». |
| Repeticiones | Alerta, oposición y comparación sin resolver podían confundirse. | Se explica qué pregunta responde cada regla, qué pasa con los empates y qué significan las 26 condiciones. |
| Resultados de calidad | 30,3 % y 30,58 % parecían dos versiones del mismo dato. | Se indica que la segunda cifra utiliza solo los artículos de partida conservados por el filtro. |
| Experimento de texto | 68,8 % y 64,93 % aparecían sin recordar el cambio de búsqueda. | Se especifican los 2.000 candidatos por área del experimento completo y los 1.000 de sus selecciones repetidas. Se distingue la fracción compartida de la sustituida. |
| Diferencias entre áreas | El porcentaje mínimo de diferencia podía confundirse con el porcentaje de parejas. | Se explican ambos denominadores; también se distingue conservar la clase de oposición de conservar una misma pareja de modelos con las mismas respuestas. |
| Discusión | Composición, familias y tiempo podían sugerir explicaciones causales. | Se describen las operaciones concretas y lo que permiten concluir. Se recuerda que son modelos actuales aplicados a artículos de épocas distintas. |
| Pies de figura | Faltaban instrucciones para leer algunos elementos gráficos. | Se explican ejes, diagonal, cajas, líneas y colores junto con la pregunta correspondiente. |

## Ejemplos del cambio

**De dos propiedades abstractas a dos operaciones.** Ahora se lee: «Para medir el acuerdo, mantengo los artículos y comparo modelos. Para comprobar la estabilidad ante la selección, mantengo el modelo y elijo otros artículos con las mismas reglas».

**De una palabra ambigua a su objeto.** «Un orden es persistente solo si se mantiene en las 26 condiciones. Esto se refiere al orden de los dos valores medidos, no a la dirección en la que apunta un vector».

**De una cifra aparentemente distinta a su base.** Antes del 30,58 %, se explica que ambos promedios de calidad usan solo los artículos de partida que sobreviven al filtro. Así queda claro por qué la cifra inicial difiere del 30,3 % general.

**De una comparación sin contexto a sus dos cambios.** En el experimento de texto se parte de título más resumen y se compara mantener el texto y cambiar de modelo con mantener el modelo y darle solo el título. Se explica además que un porcentaje de vecinos sustituidos crece cuando hay menos acuerdo.

## Cobertura y entrega

Se han leído el resumen, las seis secciones, las declaraciones, las dos tablas principales y los cuatro pies de figura. Los 69 bloques del documento anterior tienen registro de revisión; 56 cambian, incluyendo un ajuste para mantener juntas las preguntas. Se han añadido dos apartados de métodos: búsqueda de vecinos y dispersión dentro de un área. El documento final tiene 80 bloques de cuerpo alineados entre idiomas.

| Documento | Palabras del cuerpo | Resumen | Páginas con figuras y referencias |
| --- | ---: | ---: | ---: |
| Inglés | 6.567 | 195 | 24 |
| Español | 7.332 | 211 | 25 |

El texto es más largo porque desarrolla los pasos que antes quedaban implícitos. Los recuentos del cuerpo excluyen tablas, pies, citas expandidas y declaraciones. La edición anterior tenía 5.412 palabras de cuerpo en inglés y 6.090 en español.

Fuentes: [inglés](manuscript/main.tex), [español](manuscript_es/main.tex). Paquetes: [fuentes inglesas](output/manuscript_source.zip), [fuentes españolas](output/manuscript_source_es.zip). Cada paquete contiene también el suplemento previo, conservado.

## Qué se ha comprobado

- Correspondencia de cifras por bloque entre inglés y español, citas, referencias, tablas y figuras.
- Conservación de los valores científicos y de las fuentes numéricas; comprobación de 24 porcentajes contra los recuentos guardados.
- Título y declaraciones idénticos a la versión inmediatamente anterior. Bibliografía, figuras y suplementos conservados; no se han ejecutado experimentos nuevos.
- Inspección visual de las 49 páginas de los dos artículos, con ajuste de tablas y de la transición a métodos. Sin texto cortado, tablas superpuestas ni referencias sin resolver.
- Reconstrucción de los PDF desde los paquetes editables, registrada al cerrar la entrega. Esto reproduce la presentación del manuscrito, no los experimentos a partir de un depósito público de datos.

La revisión de claridad es editorial. No se ha medido la comprensión con lectores externos ni se presenta como tal. La personalidad se conserva mediante el razonamiento del autor, la primera persona puntual y ejemplos concretos, sin atribuirle vivencias nuevas.

## Registro para continuar

[Revisión por bloque, antes y después](research/first_reader_review_2026-09-20/paragraph_review.json), [comprobación de texto](research/first_reader_review_2026-09-20/text_audit.json), [porcentajes](research/first_reader_review_2026-09-20/percentage_audit.csv), [revisión visual](research/first_reader_review_2026-09-20/visual_review.json) y [cierre de entrega](research/first_reader_review_2026-09-20/closure_audit.json).

La [copia anterior](research/first_reader_review_2026-09-20/baseline/) conserva fuentes, PDF, paquetes y registros vigentes antes de esta revisión. Los resultados científicos cerrados siguen vigentes. No se ha publicado, enviado ni subido esta revisión al repositorio remoto.
