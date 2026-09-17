# Propuesta para comparar los diez modelos

**17-09-2026. Propuesta pendiente de respuesta.** La preparación técnica terminó. Este documento no aprueba medidas, umbrales, nuevas muestras ni cálculos científicos. Se han inspeccionado calidad, recortes y correspondencia; aún no se han mirado los resultados de acuerdo entre modelos.

## Primera decisión: qué queremos comparar

Recomiendo dos preguntas conectadas:

1. **¿Se conserva la forma general dentro de cada área al cambiar de modelo?** Como comparar dos mapas de una misma ciudad.
2. **¿Cada artículo sigue teniendo cerca los mismos artículos?** Como comprobar si una casa conserva sus vecinos.

La primera sería el resultado principal; la segunda ayudaría a entenderlo. Se podría empezar solo por la primera: cuesta menos, pero deja sin responder cambios pequeños que pueden quedar ocultos en una medida general. Ninguna de las dos demuestra qué modelo refleja la ciencia «verdadera».

Los **26 Fields y los cinco períodos ya están decididos**. Debe distinguirse el resultado dentro de cada área del resultado conjunto: la separación entre disciplinas podría explicar gran parte de este último. Las comparaciones entre modelos deben usar siempre los mismos artículos. Los dibujos en dos dimensiones servirían para explicar, no para medir el acuerdo.

## Decisiones siguientes, todavía abiertas

| Decisión | Opciones que se valoran | Propuesta y motivo; aún sin aprobar |
| --- | --- | --- |
| Medida general | Comparar relaciones entre artículos; o alinear directamente las coordenadas de los mapas. | Partir de CKA lineal, que compara relaciones entre los mismos artículos y admite tamaños de vector distintos. Validar su comportamiento con el tamaño disponible, ejemplos conocidos y correspondencias mezcladas antes de fijar estimador/umbral. No llamar «forma» a todo lo que una sola medida pueda captar. |
| Vecinos | Comparar los artículos más cercanos; o quedarse solo con la medida general. | Añadir coincidencia de vecinos como resultado secundario. Faltan número de vecinos, distancia y colección donde buscarlos. Probar coste antes de decidir búsqueda exacta o aproximada; comprobar el error si se aproxima. |
| Longitud de los vectores | Igualar la longitud de cada vector; o conservar la longitud original. | Proponer longitud igual para la comparación principal y originales como comprobación. Cambia la geometría y debe acordarse; el lector entrega los originales y no toma esta decisión. |
| Cuatro BERT con varias salidas | Una regla común para los cuatro; o una receta específica por modelo según antecedentes. | Proponer la media como regla común y CLS/SEP como comprobaciones predefinidas, sin elegir el ganador tras ver resultados. PubMedBERT tiene un antecedente de mapa con SEP: hay que contrastar explícitamente esta alternativa. No hay una receta universal ya demostrada para las 26 áreas. |
| Control de texto idéntico | Ampliar la muestra común; o limitar inicialmente ciertas comprobaciones a textos cortos ya leídos completos. | Ampliar según una regla de estabilidad acordada. Usar solo textos cortos seleccionaría un tipo distinto de artículo. Los 1.300 actuales son técnicos; no fijar otra cantidad por comodidad ni repetir automáticamente los 500.000. |
| Base y complemento | Resultado global con la base; resultados por área con el refuerzo, distinguiendo la composición; o estimación conjunta con pesos justificados. | Conservar la base de 400.000 para el resumen proporcional. Definir la agregación por período antes de usar el complemento en resúmenes por área. Los 500.000 juntos no representan las proporciones de publicación. |
| Calidad y estabilidad | Conservar todos los casos marcados con comprobaciones separadas; o cambiar la población mediante una criba nueva. | Conservar la versión congelada y predefinir controles de idioma, texto breve y duplicados. Fijar selección repetida, grupos de duplicados, incertidumbre y criterios de estabilidad antes de comparar. No eliminar silenciosamente registros. |

La propuesta es del proyecto, no una exigencia de QSS. La aprobación de las dos preguntas principales no resuelve automáticamente todos los parámetros de esta tabla.

## Orden de trabajo propuesto

1. Acordar las dos preguntas y después las recetas concretas de la tabla; anotarlas en `DECISIONS.md`.
2. Crear un protocolo fechado de análisis: qué se mide, qué comparaciones son principales, qué controles se harán y cuándo se considera suficiente la estabilidad. Evitar escoger lo que dé una historia más atractiva.
3. Probar la implementación y el coste en una selección pequeña fijada por una regla ajena al acuerdo observado entre modelos. Incluir el caso pequeño y los contrastes de longitud identificados; la selección y el presupuesto siguen por acordar.
4. Fijar tamaño del control común y repeticiones según esa prueba; pedir autorización para el cálculo adicional necesario. Conservar IDs y semillas.
5. Calcular resultados principales y controles acordados. Guardar cada análisis en una carpeta nueva, enlazada al catálogo, con configuración y versiones. No sobrescribir embeddings.

No se ha iniciado ninguno de esos cálculos científicos. El acceso listo está en [DATA_CATALOG.md](DATA_CATALOG.md); la limitación de texto se resume en [EMBEDDINGS_AUDIT.md](EMBEDDINGS_AUDIT.md).

## Fuentes y límites

- [Kornblith et al. (2019), Similarity of Neural Network Representations Revisited](https://proceedings.mlr.press/v97/kornblith19a.html): referencia primaria de CKA para comparar representaciones. Apoya considerarla; no establece el tamaño de muestra ni el umbral adecuado para este proyecto.
- [Imel y Hafen (2025), versión 1 del preprint](https://arxiv.org/html/2506.23366v1): estudian geometría local en unas 53.000 publicaciones, nueve disciplinas y cinco representaciones. Es un antecedente relacionado; no demuestra que nuestras medidas o diez modelos sean suficientes ni garantiza novedad.
- [EMBEDDINGS.md](EMBEDDINGS.md) y [ACADEMIC_MODEL_USAGE.md](ACADEMIC_MODEL_USAGE.md): evidencia ya reunida sobre recetas y mapas científicos. El mapa biomédico usa SEP para PubMedBERT; esa elección no se generaliza sin comprobar a las 26 áreas.

Fuentes externas anteriores consultadas el 17-09-2026. Se conserva una pregunta principal y un complemento interpretativo; no se convierten todas las ideas del brief histórico en experimentos.
