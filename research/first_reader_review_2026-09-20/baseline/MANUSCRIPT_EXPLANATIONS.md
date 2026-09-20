# Los 38 comentarios aplicados al manuscrito

**20-09-2026. Revisión editorial solicitada por el autor.** Se ha aclarado el artículo en inglés y español. El tono elegido y el título se conservan. No se han repetido experimentos ni modificado resultados, figuras, bibliografía o suplemento. Se han convertido recuentos ya guardados a porcentajes para facilitar su lectura.

- [Artículo en español](output/pdf/es/main.pdf): 22 páginas; 6.090 palabras de cuerpo y 240 de resumen para revisión.
- [Artículo en inglés](output/pdf/main.pdf): 21 páginas; 5.412 palabras de cuerpo y 200 de resumen.
- [Fuentes inglesas](output/manuscript_source.zip) y [españolas](output/manuscript_source_es.zip).

El recuento usa el mismo procedimiento de las revisiones anteriores: excluye títulos, tablas, pies, citas, fórmulas y declaraciones. La explicación aumenta el cuerpo inglés en 842 palabras; el español mantiene su número de páginas.

## Cambios que se notan al leer

Los términos se presentan con su función: qué artículo sirve de partida, cuáles pueden aparecer como vecinos, qué significa volver a elegir artículos y cuándo se marca una alerta. El ejemplo de Cardiología y Medicina explica la búsqueda emparejada. La Tabla 1 separa las preguntas y aclara qué conjuntos se reutilizan. Las comparaciones entre áreas usan porcentajes con denominador explícito. La discusión conecta cada prueba con la conclusión que permite sostener.

## Seguimiento de cada comentario

Las ubicaciones son las secciones actuales; las páginas pueden haber cambiado. Las descripciones siguientes resumen cómo se atendieron los comentarios, no son citas literales del autor. Cada fila se ha trasladado a ambos idiomas.

| N.º | Tema | Cambio aplicado | Ubicación |
| ---: | --- | --- | --- |
| 1 | Ejemplo de búsquedas emparejadas | Se usan 50 artículos de Cardiología en dos conjuntos de 256: especialidad y Medicina. | 3.3 |
| 2 | Diez selecciones | Los 50 artículos de partida siguen fijos; se eligen diez veces los otros 206. Se excluye el propio artículo al buscar sus vecinos. | 3.3 |
| 3 | Qué significa CKA | Se explica el parecido entre patrones de relaciones, sin convertirlo en porcentaje de acierto. | 3.4 |
| 4 | Para qué se vuelven a elegir artículos | Se indica que se eligen para recalcular la posición media de cada disciplina. | Resumen |
| 5 | Título como entrada del modelo | Se dice qué texto recibe el modelo: solo título frente a título y resumen. | Resumen |
| 6 | Final del resumen | Se explica el propósito positivo: identificar relaciones compartidas y decisiones de las que dependen. | Resumen |
| 7 | Tabla de muestras | Seis preguntas concretas; columnas de comparación y artículos; se separan organización general y vecinos. La colección inicial pasa a la nota. | Tabla 1 |
| 8 | Sin resolver | Se definen las dos reglas y el caso restante. Un empate no cuenta como dirección persistente; no basta con que un modelo empate para invalidar la oposición de otros dos. | 3.5 |
| 9 | Qué es una selección | Definición temprana y explicación de conjuntos solapados dentro de la colección fija. | 2.2 y 3.5 |
| 10 | Alerta de selección | Resultado sensible a cambiar artículos o tamaño según la tolerancia registrada; no error de un registro. | 3.5 y 4.1 |
| 11 | 26 especialidades de la figura | Una por cada una de las 26 áreas; 50 elecciones, con diez elecciones de artículos para cada una. | Figura 1 |
| 12 | 2.048 candidatos comunes | Misma cantidad por grupo; mismos identificadores entre modelos dentro del grupo, no entre disciplinas. | 4.2 |
| 13 | Búsqueda global | 100 artículos de partida por cada uno de 130 grupos; sus vecinos se buscan entre 400.000 registros. | 4.2 |
| 14 | Dos cambios a la vez | Se amplían disciplinas/períodos y cantidad de candidatos; no se separan sus efectos. | 4.2 |
| 15 | Filtro de calidad | Se retiran las marcas indicadas y se conserva un representante por grupo de duplicados. Antes y después son unos ocho vecinos compartidos de 25. | 4.2 |
| 16 | Cambiar el alcance | Se explica si las listas coinciden más o menos, con 58,5% frente a 41,5% de especialidades y el reparto casi igual con 50 vecinos. | 4.2 |
| 17 | Área amplia | Se identifica como el área que contiene la especialidad, con Medicina como ejemplo. | Figura 2 |
| 18 | Especialidad | Se identifica como rama más concreta, con Cardiología y Medicina Cardiovascular como ejemplo. | Figura 2 |
| 19 | Casos y errores de origen | Se cuenta qué se revisó y cómo se comprobó contra los registros descargados. Los ejemplos no estiman la frecuencia del problema. | 4.2 |
| 20 | Tres entradas | Cada uno de los mismos 52.000 artículos se representa con título, resumen y ambos; se distinguen las dos comparaciones con la referencia combinada. | 4.3 |
| 21 | Reglas de combinación | Media frente a primera o última salida; se nombran los cuatro BERT afectados y se explica que se recalculan ambas comparaciones. | 4.3 |
| 22 | De 26.000 a 52.000 | Se explica que se añaden 26.000 con el mismo diseño y se conserva el primer conjunto dentro del total. | 4.3 |
| 23 | Alertas geométricas | Se distinguen veinte medias muestras de 1.000 y cinco selecciones de 2.000; cuatro alertas equivalen al 1,5% de 260 casos. | 4.4 |
| 24 | Un área por encima de otra | Mayor valor de la medida, no posición en un dibujo ni calidad de la investigación. | 4.4 |
| 25 | Recuentos de parejas | Se presentan porcentajes de las 325 parejas para oposición, unanimidad, casos sin resolver y cortes de magnitud. Los recuentos permanecen en figura y tablas. | 4.4 |
| 26 | Medidas alternativas | Se recuerdan entropía y D80, sus empates y los denominadores. Conservar una oposición exige al menos una misma pareja de modelos en las mismas direcciones. | 4.4 |
| 27 | Punto de referencia | Media común de 52.000 vectores por modelo, resta a cada vector y reajuste de longitud. | 3.5 y 4.4 |
| 28 | Efecto del centrado | Se distinguen proporción total de parejas opuestas y conservación de parejas originales; cifras completas remitidas a S20. | 4.4 |
| 29 | Por qué se probó la fragmentación | Se explica la posible utilidad y por qué una conexión geométrica débil no quedó validada como división temática. | 4.4 |
| 30 | Veinte mitades y cinco selecciones | 26 condiciones: principal de 2.000, veinte mitades de 1.000 y cinco elecciones adicionales de 2.000 por área. | Figura 4 |
| 31 | Repetir artículos no es cambiar modelo | Ejemplo de A mayor que B en un modelo y orden contrario en otro, aun repitiendo artículos. | 5.1 |
| 32 | Qué controlan los centros | Recalcular medias con otros artículos, con tres tamaños y omitiendo cada área. | 5.2 |
| 33 | Calidad, entrada y medias | Se explica el cambio pequeño del filtro y los comportamientos distintos que reúne la media de entrada. | 5.2 |
| 34 | Matiz repetido sobre corrección | Se retira la frase repetitiva y se conserva la distinción general entre acuerdo y evidencia externa donde corresponde. | 5.2 |
| 35 | Consecuencia del procesamiento | La comparación de dispersión debe indicar representación, punto de referencia y medida. | 5.2 |
| 36 | Medicina, familias y tiempo | Se explican los controles de composición y modelos biomédicos, los límites de causa y el cambio de signo al igualar candidatos. | 5.2 |
| 37 | Conclusión | Se formula una consecuencia concreta: comprobar la relación que se quiere sostener y mostrar cuánto cambia. | 6 |
| 38 | Retirar sección de IA | Se retira de ambos artículos y se elimina la remisión que quedaría sin destino. El historial real de asistencia permanece. | Declaraciones |

## Comprobaciones y alcance

- Los 24 porcentajes de esta revisión se comprueban contra los recuentos guardados en [percentage_audit.csv](research/manuscript_explanations_2026-09-20/percentage_audit.csv). No son experimentos nuevos.
- El ejemplo de Cardiología como especialidad de Medicina se comprobó en el índice de metadatos local; la búsqueda global de 100 artículos por grupo se contrastó con los métodos guardados.
- Las cifras de 66 bloques del cuerpo corresponden entre inglés y español. Citas, referencias a figuras/tablas, fórmulas y títulos se conservan. Las fuentes y PDF del suplemento permanecen intactos.
- Los 43 folios de los dos artículos se han inspeccionado visualmente. Tabla 1, pies y referencias caben sin recortes ni superposiciones. Se evita partir una entrada bibliográfica entre páginas.
- Las versiones previas están en [baseline/](research/manuscript_explanations_2026-09-20/baseline/). El [registro final](research/manuscript_explanations_2026-09-20/closure_audit.json) reúne las verificaciones, las huellas de archivos protegidos y la reconstrucción desde los ZIP.

## Comentario 38 y continuación

Por petición explícita del autor, el borrador ya no incluye el apartado de uso de IA. También se retira la remisión a ese apartado desde las contribuciones. Esto modifica la presentación del borrador, no la historia real del trabajo: las copias previas y los registros de asistencia permanecen intactos. No se añade ninguna afirmación de ausencia de asistencia.

Antes de un eventual envío habrá que comprobar las declaraciones que exija la revista y presentarlas de forma fiel al trabajo realizado. No se ha comprobado de nuevo la política editorial en esta revisión ni se ha enviado o publicado el artículo. Siguen pendientes la lectura personal y aprobación final del autor, la correspondencia y las decisiones de depósito y licencia.
