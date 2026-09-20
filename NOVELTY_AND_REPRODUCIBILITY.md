# Qué aporta el artículo y cómo hacerlo reproducible públicamente

**Propuesta ya aplicada:** [PUBLIC_RELEASE.md](PUBLIC_RELEASE.md) registra la integración de los párrafos, las licencias aceptadas y el paquete numérico comprobado. Este informe conserva la investigación previa; sus decisiones pendientes están sustituidas por la autorización posterior del autor.

Revisión dirigida del 20-09-2026. **Recomiendo reforzar la aportación alrededor de las comparaciones concretas entre disciplinas y preparar una entrega en GitHub + Zenodo.** La evidencia científica ya permite defender esa contribución. La reproducción pública completa todavía necesita trabajo: el código público corresponde al 17 de septiembre y no contiene las últimas fases del artículo.

Esta revisión entrega propuestas y una prueba local de reproducción. No modifica el manuscrito, no ejecuta nuevos experimentos y no publica archivos ni elige licencias. La aprobación del texto y del depósito sigue pendiente.

## 1. La aportación que podemos defender

La idea central se puede explicar así:

> Una comparación entre disciplinas puede dar la misma respuesta cada vez que elegimos otros artículos y, aun así, dar respuestas contrarias según el modelo. El estudio permite distinguir esa contradicción persistente de una diferencia pequeña o de una comparación que cambia demasiado entre selecciones.

Es una aportación empírica y de evaluación de mapas científicos. Su fuerza está en comprobar **la afirmación que se extrae del mapa**. Por ejemplo: «los artículos del área A tienen mayor apertura angular que los del área B». Se sigue esa misma comparación al cambiar artículos, modelos y procesamiento. El resultado puede repetirse dentro de cada modelo sin sostenerse entre ellos.

No conviene presentar como nuevas la comparación de modelos, la combinación de estructura y vecinos, el uso de varias recetas de representación o la idea general de que un mapa depende del método. Tampoco el número de modelos es, por sí solo, la aportación: un antecedente próximo ya compara diecinueve.

### Contraste con los antecedentes más próximos

La columna final expresa mi valoración de la diferencia entre preguntas; no una demostración de prioridad absoluta. La búsqueda es dirigida, no exhaustiva.

| Antecedente | Qué cubre y qué debemos reconocer | Diferencia concreta que podemos defender |
| --- | --- | --- |
| [Caspari et al., 2024, *Beyond Benchmarks*](https://arxiv.org/html/2407.08275v1) | Compara 19 modelos en cinco conjuntos de recuperación. Combina CKA, coincidencia de resultados y orden de recuperación; examina familias. Es el antecedente metodológico más directo. | Nuestro objeto es la interpretación de mapas de disciplinas. Añadimos el seguimiento de comparaciones entre áreas con modelos identificados, artículos repetidos y tamaño de diferencia explícito. CKA + vecinos no debe presentarse como invención. |
| [Constantino et al., 2025, QSS](https://doi.org/10.1162/qss_a_00349), [texto de autor](https://arxiv.org/html/2308.15706v2) | Evalúa representaciones de citas y texto frente a la clasificación jerárquica de física. Ya relaciona representación, nivel de detalle y evaluación disciplinar. | Aquí se mantienen emparejados los artículos y se pregunta qué comparaciones se conservan entre representaciones de 26 áreas. No buscamos el modelo que mejor reproduce una clasificación externa. |
| [González-Márquez et al., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11240179/), [métodos del preprint](https://www.biorxiv.org/content/10.1101/2023.04.10.536208v1.full) | Construye un mapa biomédico y compara modelos y reglas de extracción de vectores para su evaluación. | La aportación aquí es comprobar cómo esas decisiones afectan a la conclusión que se quiere sostener. Probar modelos o *pooling* tampoco es nuevo. |
| [Bascur et al., 2025, Scientometrics](https://doi.org/10.1007/s11192-024-05218-6) | Mide qué clases de temas biomédicos quedan mejor agrupadas en redes de citas o texto, usando MeSH. | Su evaluación temática es un complemento que este estudio no sustituye. Nuestro acuerdo entre modelos no demuestra que una agrupación sea temáticamente correcta. |
| [Imel y Hafen, 2025](https://arxiv.org/html/2506.23366v1) | Estudia densidad y asimetría de vecindarios en nueve disciplinas, con cinco representaciones y relaciones con citas. | La geometría de la literatura ya se estudia. Aquí el resultado central es la persistencia o inversión de un orden entre áreas, y su dependencia del procesamiento. |
| [Raju, 2026, versión 5](https://arxiv.org/html/2601.09173v5) | Distingue similitud entre representaciones y estabilidad de su geometría; propone una medida basada en particiones de coordenadas. | Debemos reconocer esa distinción general. Aquí seguimos artículos y comparaciones disciplinares concretas bajo diez modelos; no proponemos una nueva medida general de estabilidad. |
| [Brinner y Zarrieß, ACL 2026, SemCSE-Multi](https://aclanthology.org/2026.acl-long.1884/) | Desarrolla representaciones de distintos aspectos de un resumen y recursos para interpretar mapas científicos. | Nuestro objetivo es auditar resultados de representaciones existentes. No aportamos un nuevo modelo ni un sistema de mapas por aspectos. |
| [Bascur, Costas y Verberne, 2026](https://doi.org/10.1515/jdis-2026-0114), [versión evaluada en MetaROR](https://metaror.org/article/use-of-diverse-data-sources-to-control-which-topics-emerge-in-a-science-map-2/) | Examina cómo otras fuentes de relaciones entre documentos cambian los temas favorecidos por un mapa. La versión editorial se publicó el 15-09-2026 con un título más preciso. | Refuerza que la dependencia del diseño ya es conocida. Nuestro contraste mantiene los documentos y sigue afirmaciones concretas al cambiar la representación. |

Se comprobaron métodos y resultados relevantes de Caspari, Constantino, Bascur 2025, Imel y Raju. Para SemCSE-Multi se usaron la ficha editorial y el resumen; para el mapa biomédico, la página primaria indexada y los métodos del preprint. La página directa de PMC devolvió una comprobación de navegador. Bascur 2026 se contrastó con MetaROR y Crossref; la página editorial agotó el tiempo de acceso. No se presenta ese acceso parcial como lectura íntegra de la versión publicada.

### Qué evidencia hace que la aportación sea algo más que una advertencia

| Resultado ya calculado | Qué permite sostener | Límite que debe acompañarlo |
| --- | --- | --- |
| 262 de 325 parejas de áreas tienen modelos con órdenes persistentemente opuestos en apertura angular; 221 en dimensión efectiva. | La contradicción puede mantenerse en las 26 condiciones de selección, con los mismos modelos. | No implica que los diez modelos discrepen ni identifica cuál tiene razón. |
| Al exigir diferencias superiores al 5 %, quedan 96 y 177 oposiciones, respectivamente. | La dirección y el tamaño de la diferencia se pueden examinar por separado. | La mera existencia de una inversión pequeña no demuestra relevancia científica. |
| El centrado y la renormalización llevan las oposiciones angulares de 262 a 151; solo 128 conservan alguna misma pareja de modelos con sus mismas direcciones. En PR se conservan 204. | La estabilidad al cambiar artículos no protege frente a toda decisión de representación. Las dos propiedades responden de forma diferente. | Centrar no convierte una representación en la correcta. |
| Comparación de texto/modelo con los mismos artículos; control de recetas; comparación de especialidad/área con consultas, candidatos y fechas emparejados. | Permite precisar qué decisión cambia cada resultado. | Las medias no son una equivalencia universal; el diseño de búsqueda amplio está condicionado por las consultas comunes. |

Las cifras proceden de los resultados congelados y del manuscrito vigente. El ejemplo de reproducción preparado en esta revisión ha vuelto a obtener los recuentos de apertura y PR desde las medidas individuales; no ha recalculado las medidas.

### Cómo lo llevaría al artículo

Concentraría la aportación en una frase al final de la introducción, una comparación explícita con los antecedentes en el apartado 2 y la consecuencia práctica en la discusión. El resto de los controles debe sostener ese argumento. La ampliación geométrica debe seguir apareciendo como exploratoria y posterior a los primeros resultados.

Hay una [propuesta completa en inglés y español](research/submission_readiness_2026-09-20/MANUSCRIPT_POSITIONING_DRAFT.md), lista para integrar sin cambiar el título ni las cifras. No la he introducido automáticamente en los PDF. Recomiendo evitar «por primera vez», «nuevo marco general» y «demostramos la forma real de la ciencia»: la revisión dirigida no respalda esas afirmaciones.

## 2. Qué pide QSS y qué falta hoy

La [guía oficial de QSS](https://direct.mit.edu/qss/pages/submission-guidelines) exige compartir los datos esenciales para repetir los principales hallazgos en un repositorio público con identificador persistente, y explicar su disponibilidad en el artículo. Recomienda compartir código. No acepta sustituir el depósito por ofrecer los datos bajo petición. Admite excepciones legales o éticas explicadas y pide compartir cuanto sea posible en esos casos. También requiere citar formalmente los conjuntos públicos utilizados.

**Límite de la consulta:** el 20-09 se volvió a intentar el acceso directo y devolvió HTTP 403. El contenido anterior procede de la página oficial indexada, cuyo rastreo se fecha aproximadamente 1,3 años atrás. Es una base clara para preparar la entrega, pero no certifica que hoy no existan requisitos adicionales. Debe contrastarse en el formulario de envío antes de enviarlo.

### Estado comprobado del proyecto

| Elemento | Situación al 20-09-2026 |
| --- | --- |
| GitHub público | `44c941019ecc34417641929ada97da79bf12fe58`, del 17-09. Comprobado mediante la API de GitHub; árbol completo, 852 archivos. |
| Correspondencia con el artículo actual | Faltan en ese árbol `manuscript/`, `sos_morphology/`, `sos_pair_summary/` y `sos_closure/`. El enlace actual no ofrece aún todo el código del artículo. |
| Licencia general y cita de software | No se encontró `LICENSE` ni `CITATION.cff`; la API devuelve licencia nula. |
| Datos y vectores | Locales. No existe un depósito persistente declarado en el proyecto. |
| Reproducción del documento | Los paquetes editables ya reconstruyen los PDF. Eso verifica el documento, no el análisis científico. |
| Reproducción de esta revisión | Un paquete de 672.054 bytes recupera ocho clasificaciones de 325 parejas y dos comprobaciones de conservación de modelos. Funciona desde una carpeta temporal aislada, sin bibliotecas instaladas ni red. Cubre una parte de la Figura 4. |

La evidencia está en [public_state.json](research/submission_readiness_2026-09-20/public_state.json), [inventario de archivos](research/submission_readiness_2026-09-20/local_inventory.csv) y [prueba de portabilidad](research/submission_readiness_2026-09-20/demo_portability_audit.json).

## 3. Vía recomendada: código versionado y datos en Zenodo

Propongo **una versión de código en GitHub, archivada con DOI, y un registro de datos en Zenodo, enlazados entre sí**. Los datos se agruparían por su función. El registro debe permitir llegar desde cada figura o conclusión hasta sus archivos de entrada y el comando que la reproduce.

Conviene ofrecer tres recorridos claramente identificados:

1. **Comprobación rápida:** recalcular resúmenes y figuras desde los valores por selección, área y modelo. Un lector puede revisar cifras y reglas sin una descarga grande.
2. **Repetición de los análisis:** partir de los vectores congelados y las selecciones exactas para volver a calcular estructura, vecinos, geometría y controles. Este es el objetivo principal de la entrega científica propuesta.
3. **Reconstrucción de las representaciones:** documentar y, cuando los permisos lo permitan, conservar los textos exactos, el procesamiento, las revisiones de los modelos y sus entornos. Es una etapa distinta, con mayor coste de cálculo. Una nueva consulta a OpenAlex no garantiza recuperar el texto histórico.

La primera vía es útil, pero por sí sola no demuestra que se puedan repetir todas las conclusiones. La segunda permite comprobarlas sin depender de descargar otra vez los modelos. La tercera verifica además cómo se obtuvieron los vectores. La declaración de disponibilidad debe explicar el alcance real alcanzado en cada vía.

### El tamaño es manejable

Los archivos de vectores principales ocupan **26,881 GB**; la carpeta completa que los contiene, con índices y manifiestos, **27,533 GB**. Las carpetas inventariadas de embeddings, análisis y controles suman **57,576 GB**, antes de depurar duplicados y separar textos. Es una medición de archivos locales sin comprimir, no el tamaño definitivo del depósito. Los informes legibles ocupan aproximadamente 0,104 GB.

[Zenodo permite 50 GB y hasta 100 archivos por registro](https://help.zenodo.org/docs/deposit/manage-files/). Su [guía de cuota](https://help.zenodo.org/docs/deposit/manage-quota/) describe una asignación adicional de hasta 150 GB distribuible entre registros. Por tanto, el volumen observado cabe en una vía ordinaria de depósito; habría que comprobar la cuota disponible de la cuenta. Agrupar miles de bloques en archivos por componente permite respetar el límite de archivos. No hace falta subir los pesos de los modelos, entornos locales, cachés ni todas las copias históricas.

La [reserva de DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/) permite preparar los enlaces antes de publicar. Un DOI reservado no es todavía un depósito público: se registra al publicar. El manuscrito debe citar la versión concreta que se haya comprobado.

### Licencias y textos: una separación necesaria

Recomiendo MIT para el código propio y CC BY 4.0 para los resultados propios que se puedan distribuir, conservando la procedencia CC0 de los metadatos OpenAlex. Son propuestas para el autor; no se han aplicado. La [documentación de GitHub](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) distingue un repositorio visible de uno con permisos de reutilización explícitos.

OpenAlex declara sus datos [bajo CC0](https://help.openalex.org/data/how-its-built/), pero explica que [no entrega abstracts en texto plano por razones legales](https://help.openalex.org/data/works/attributes/#abstract_inverted_index). No conviene convertir esa declaración general en una autorización que nosotros otorgamos sobre cualquier texto de terceros. La entrega debe registrar de dónde procede cada componente y qué condiciones lo acompañan. Los índices y las huellas de texto ya permiten identificar la entrada utilizada; los vectores permiten repetir los análisis sin redistribuir abstracts en claro.

Para la reconstrucción desde texto hay dos posibilidades que deben quedar resueltas al preparar la entrega: compartir la entrada histórica cuando su distribución esté documentada, o describir la restricción concreta y conservar públicamente todo lo distribuible. Si se propone incluir los índices invertidos originales, también hay que documentar su procedencia y condiciones; cambiar el formato no es por sí solo una solución jurídica. Las condiciones de los diez modelos deben constar sin asumir que su licencia autoriza cualquier material ajeno. No es necesario redistribuir sus pesos para la vía que parte de vectores.

## 4. Trabajo concreto antes de enviar

La [especificación del paquete](research/submission_readiness_2026-09-20/RELEASE_SPEC.md) identifica componentes, etapas y criterios de aceptación. Recomiendo este orden:

1. Integrar la redacción de la aportación y cerrar la versión del artículo que se quiere acompañar.
2. Preparar una versión del código que incluya las fases del 18 y 20 de septiembre. Conservar los programas científicos congelados; añadir por separado las instrucciones y adaptadores necesarios para otra máquina.
3. Seleccionar archivos mediante un manifiesto explícito, con licencia/procedencia por componente. Preparar el diccionario de datos, las selecciones exactas, las versiones de modelos y las huellas de integridad.
4. Repetir las cuatro figuras principales y los resultados esenciales del suplemento en una carpeta limpia que solo vea los archivos de la entrega. Registrar tiempo, memoria, tamaño y diferencias numéricas. No basta con que el programa omita cálculos porque encuentra una auditoría histórica marcada como completa.
5. Publicar los materiales autorizados, comprobar la descarga pública de la versión definitiva y añadir sus DOI a la declaración de datos y a las referencias del artículo.

Esta investigación permite concretar el trabajo, pero no permite todavía declarar «estudio completamente reproducible en público». Falta completar y probar el paquete. No propongo nuevos experimentos para reforzar la novedad: primero haría visible la contribución ya respaldada y cerraría esta entrega verificable.

## Material preparado y procedencia

- [Redacción propuesta, inglés y español](research/submission_readiness_2026-09-20/MANUSCRIPT_POSITIONING_DRAFT.md).
- [Especificación de la entrega pública](research/submission_readiness_2026-09-20/RELEASE_SPEC.md).
- [Ejemplo de reproducción, ZIP](research/submission_readiness_2026-09-20/replication_demo.zip) y [explicación de su alcance](research/submission_readiness_2026-09-20/replication_demo/README.md).
- [Fuentes, versiones, consultas y límites](research/submission_readiness_2026-09-20/SOURCES.md).

Se aplicó la guía `paper-lookup` para la consulta bibliográfica y su comprobación de versiones: Kassis, Agarwal, He, Patel y Brueckner (2026), [*Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*](https://arxiv.org/abs/2609.00065), versión vigente comprobada v2. Se cita como procedencia de la herramienta de esta revisión, no como evidencia científica del artículo.
