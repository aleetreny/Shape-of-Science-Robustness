# Medidas y antecedentes: decisión para esta fase

Revisión dirigida, 17-09-2026. Las fuentes iniciales se consultaron antes de calcular los acuerdos; la comprobación adicional sobre Shesha y las limitaciones de OpenAlex se hizo durante la ejecución. No es una revisión sistemática ni una garantía de novedad.

## Recomendación

Mantener **una medida principal y dos comprobaciones**, más vecinos como segundo nivel. Una colección enorme de medidas no vuelve sólido el estudio si todas se interpretan después de ver qué historia favorecen. Lo defendible aquí es especificar qué conserva cada comparación, probar sus límites y mostrar los desacuerdos.

| Método | Qué nos permite preguntar | Decisión y límite |
| --- | --- | --- |
| CKA lineal corregida | ¿Los mismos artículos mantienen relaciones generales parecidas? | Principal. La corrección reduce el problema de pocas filas frente a muchas coordenadas. Sigue dando más peso a ciertas variaciones del espacio y no mide verdad temática. |
| Procrustes angular | ¿Podemos alinear ambas nubes sin deformarlas libremente? | Comprobación geométrica. Admite rotaciones/reflexiones y una escala. Su ajuste sobre los mismos datos puede producir un fondo positivo; se conserva una referencia de IDs mezclados. |
| RSA por rangos de distancias | ¿Los pares relativamente próximos y lejanos siguen siendo los mismos? | Comprobación que se centra en el orden. No exige que las distancias tengan la misma escala. Los pares no son observaciones independientes. |
| Fracción de vecinos compartidos | ¿Cada artículo mantiene sus compañeros más cercanos? | Resultado local, con 10/25/50 vecinos, azar de referencia, candidatos iguales y búsqueda global. No es un método nuevo. |
| CCA o transformaciones lineales arbitrarias | ¿Pueden alinearse permitiendo deformaciones más generales? | No principal: pueden borrar diferencias que son parte de nuestra pregunta; hay problemas cuando dimensión y tamaño quedan próximos. |
| Topología y otras descripciones de nubes | ¿Se conserva alguna propiedad agregada de conectividad o estructura? | No añadidas por defecto. ReSi no respalda una superioridad universal. Antes habría que fijar qué conclusión científica resolverían y sus parámetros; no basta con parecer más sofisticadas. |
| Shesha, preprint de 2026 | ¿Una representación conserva sus relaciones al observar subconjuntos de sus coordenadas? | Interesante para otra pregunta. El autor indica que cambia al rotar las coordenadas. Aquí un giro por sí solo debe conservar la forma; no sustituye la comparación entre modelos. No se ha ejecutado. |

La invariancia se refiere a las matrices preparadas que define cada método. En particular, normalizar filas y después centrar no es lo mismo que centrar primero. La receta exacta está escrita en `METHODS_ANALYSIS.md`.

## Evidencia principal

- [Kornblith et al. (ICML 2019)](https://proceedings.mlr.press/v97/kornblith19a.html) establece CKA y contrasta sus propiedades con métodos que permiten transformaciones lineales más generales. Se utiliza como fundamento, no como validación de todos nuestros casos.
- [Williams et al. (NeurIPS 2021)](https://proceedings.neurips.cc/paper/2021/hash/252a3dbaeb32e7690242ad3b556e626b-Abstract.html) formaliza distancias entre representaciones, invariancias y límites de estimación con tamaños finitos. Apoya usar una distancia angular con un significado geométrico explícito.
- [Ding et al. (NeurIPS 2021)](https://arxiv.org/abs/2108.01661v2) comprueba que diferentes medidas tienen debilidades distintas al relacionarlas con cambios funcionales. Motiva no identificar alineación con igual comportamiento.
- [Murphy et al. (2024, taller Re-Align de ICLR)](https://arxiv.org/abs/2405.01012v1) muestra similitudes artificiales de CKA sin corrección en situaciones de muchas coordenadas y pocas observaciones. La evidencia original es neural; nuestra aplicación al texto es una decisión metodológica, no un resultado ya demostrado por ese artículo.
- [Klabunde et al., ReSi (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2eef1f75516b0cfd3e944345e5f88c08-Abstract-Conference.html) compara 24 medidas, seis comprobaciones, 14 arquitecturas y siete conjuntos. No identifica una ganadora universal. Se leyó la versión editorial y el [repositorio de autores](https://github.com/mklabunde/resi); no se descargaron sus modelos o datos.
- [Raju, Shesha (preprint, versión 5, julio de 2026)](https://arxiv.org/html/2601.09173v5) estudia estabilidad ante dividir coordenadas dentro de una representación y declara su sensibilidad a rotaciones. Nuestra inferencia es que no debe sustituir una medida cuya pregunta exige ignorar esas rotaciones. No se ha verificado independientemente su evaluación experimental.

## Qué se parece a nuestro trabajo y qué podemos aportar

[Imel y Hafen (2025)](https://arxiv.org/html/2506.23366v1) ya estudian geometría local y citas con cinco representaciones y unas 53.000 publicaciones de nueve disciplinas. Sus medidas incluyen densidad y asimetría del vecindario. Por tanto, «usar vecinos para estudiar ciencia» no es nuestra novedad. Su selección se construye de otra manera; no copiamos una selección guiada por un embedding para evaluar neutralmente ese mismo embedding.

[SciRepEval (EMNLP 2023)](https://aclanthology.org/2023.emnlp-main.338/) compara representaciones científicas en tareas diversas. Es un antecedente para distinguir rendimiento en una tarea de conservación del mapa. Nuestro estudio no sustituye esos conjuntos de evaluación ni proclama el mejor modelo para recuperar artículos.

La revisión previa de mapas científicos está en [ACADEMIC_MODEL_USAGE.md](../../ACADEMIC_MODEL_USAGE.md): incluye aplicaciones grandes, comparaciones entre modelos y variantes de recetas. No permite afirmar que estos sean los diez modelos más utilizados en toda la comunidad.

La aportación defendible que se somete a prueba es **dónde se rompe el acuerdo al pasar de relaciones entre áreas a estructura interna y vecinos**, en un corpus común amplio, con selección no guiada por los modelos y controles de receta, contenido leído, tamaño de candidatos y calidad. Los resultados deberán demostrar qué aporta; ni el volumen ni el número de modelos garantizan novedad o aceptación.

## Registro de acceso

Se conciliaron seis registros arXiv solicitados con seis recibidos en `sources/arxiv_records.json`; uno documenta herramientas, no evidencia científica. Se consultó después el registro y HTML de Shesha versión 5. Una página PMC requirió captcha y se sustituyó por el PDF editorial de NeurIPS; el HTML de un antecedente MDPI de 2022 devolvió 429 en esta sesión y no se utilizó para justificar detalles de métodos. Fuentes oficiales de OpenAlex y MiniLM se enlazan en los métodos. No se han inventado metadatos faltantes ni se ha interpretado falta de acceso como ausencia de trabajos similares.
