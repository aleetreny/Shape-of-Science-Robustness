# Abstract: explicar la comparación antes de dar el resultado

20-09-2026. Revisión editorial solicitada después del cierre de robustez. Se conserva el comienzo y el tono que el autor ha aceptado. No cambian el cuerpo del artículo, sus resultados, tablas, figuras, declaraciones, referencias o suplemento.

| Expresión anterior | Explicación actual |
| --- | --- |
| Áreas | Disciplinas de investigación, con Medicina y Física como ejemplos. |
| Organización general y tamaño de grupos | Comparar las posiciones medias de las disciplinas, cambiando qué artículos se eligen y cuántos se usan por disciplina. |
| Quitar el resumen | Dar al modelo el título de cada artículo en vez del título y el resumen. |
| Respuestas opuestas sobre dispersión | Un modelo sitúa los artículos de una disciplina más juntos que los de otra; otro invierte ese orden. Se identifica la comparación angular. |
| Repetir frente a otro procesamiento | Elegir otros artículos puede mantener la respuesta, mientras cambiar de modelo o el punto de referencia para medir los ángulos puede alterarla. |

No se afirma que los mapas sean dibujos en dos dimensiones, que los modelos acierten por coincidir ni que los efectos de texto sean iguales para todos. El abstract destaca la sensibilidad angular, sin atribuirla a todas las propiedades geométricas.

## Español para revisión

Los mapas de la ciencia usan las relaciones entre artículos para describir cómo se organiza la investigación. Cuando esas relaciones proceden de embeddings de texto, un modelo convierte cada artículo en una lista de números. ¿Otro modelo daría la misma imagen? Comparo diez modelos con 500.000 publicaciones de OpenAlex de 2000–2024, repartidas en 26 disciplinas, como Medicina o Física. Al representar cada disciplina mediante la posición media de sus artículos, los modelos muestran una organización parecida. Esto se mantiene al elegir otros artículos o cambiar cuántos usamos por disciplina. Sin embargo, dentro de una disciplina y período, dos modelos comparten, en promedio, solo ocho de los 25 artículos que sitúan más cerca de un mismo artículo. Usar solo el título de cada artículo, en vez del título y el resumen, también cambia buena parte de esa lista, aunque el efecto varía según el modelo. Un modelo puede situar los artículos de una disciplina más juntos que los de otra, mientras otro modelo invierte ese orden. Esta comparación utiliza los ángulos entre las posiciones asignadas a los artículos. Mover el punto desde el que medimos esos ángulos puede cambiar la respuesta, incluso cuando elegir otros artículos no la cambia. Por tanto, repetir la selección de artículos no asegura que otro modelo, u otro punto de referencia para medir los ángulos, respalde la misma comparación. Estas pruebas no establecen qué modelo describe mejor la investigación.

## English

Science maps use relationships between papers to describe how research is organised. When these relationships come from text embeddings, a model turns each paper into a list of numbers. Would another model give the same picture? I compare ten models using 500,000 OpenAlex publications from 2000–2024, covering 26 disciplines such as Medicine and Physics. Representing each discipline by its papers' average position produces similar arrangements across models, even when the selected papers and their number change. Yet within a discipline and period, two models share, on average, only eight of the 25 papers closest to a given paper. Using each paper's title alone, instead of its title and abstract, also changes much of that list, although the effect varies between models. One model can place a discipline's papers closer together than another discipline's, while another model reverses that order. This comparison uses angles between paper positions. Moving the point from which these angles are measured can change the answer even when selecting other papers does not. Repeating article selection therefore does not ensure that another model, or another reference point for measuring angles, supports the same comparison. These checks do not establish which model best describes the research.

## Entrega y comprobaciones

- [Artículo en español](output/pdf/es/main.pdf): 22 páginas; resumen de 235 palabras.
- [Artículo en inglés](output/pdf/main.pdf): 20 páginas; abstract de 200 palabras según el contador conservador del proyecto.
- Fuentes actualizadas en `manuscript/main.tex` y `manuscript_es/main.tex`; paquetes editables en `output/manuscript_source.zip` y `output/manuscript_source_es.zip`.
- La copia española es para lectura del autor y se permite una traducción más larga. La versión inglesa mantiene el máximo de 200 palabras que se está usando para preparar el envío.
- Texto anterior, PDF y paquetes previos conservados en `research/abstract_clarity_2026-09-20/baseline/`. Las auditorías del cierre anterior describen aquella versión; no se sobrescriben.
- [Auditoría de esta revisión](research/abstract_clarity_2026-09-20/closure_audit.json): cambios limitados al abstract, correspondencia entre idiomas, fuentes conservadas, compilación, maquetación y paquetes.

Esta entrega sigue pendiente de la lectura personal del autor. No se han ejecutado nuevos análisis, publicado ni enviado documentos.
