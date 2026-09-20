# Decisiones y preguntas pendientes

Este es el registro principal para retomar el proyecto. Actualizado: 2026-09-17.

**Estado más reciente:** la checklist adicional también está terminada. Su cierre y sus decisiones están al final de este documento; entrega en `CHECKLIST_RESULTS.md`. Las secciones anteriores conservan la cronología, no reabren decisiones cerradas.

## Comparación de forma y vecinos terminada: decisiones delegadas vigentes, 17-09-2026

La petición nueva del usuario aprueba forma y luego vecinos y delega las cuestiones científicas de esta fase. Sustituye los estados previos de propuesta pendiente. Protocolo fijado antes de inspeccionar acuerdos: `ANALYSIS_PROTOCOL.md` y `config/analysis_v1.json`.

- Principal: CKA lineal corregida por tamaño, con Procrustes angular y RSA de rangos como comprobaciones. No prometer una medida universalmente superior. Usar todas las filas por Field/período y solo la base de 400.000 para el resultado proporcional global.
- Vectores de longitud igual; media como regla común para los cuatro BERT, con originales/CLS/SEP como controles. Estabilidad por selección, calidad, composición y familias fijada por escrito.
- MiniLM: no hay error en el límite habitual de 256. Se calcula una variante de 512 en una salida separada, como control de longitud; el original queda como principal. Se reutilizan vectores únicamente cuando texto y operación efectiva son idénticos.
- Control común: 52.000 IDs elegidos sin consultar acuerdos, 400 por área/período. Interpretación principal por Field con 2.000 artículos, cinco períodos de igual peso. El presupuesto debe contrastarse con estabilidad; no se afirma suficiencia universal.
- Vecinos: exactos dentro de cada área/período para los 500.000, principal k=25 con k=10/50 como controles; además 13.000 consultas contra la base general de 400.000. Excluir el propio artículo, controlar azar, empates y precisión.

Los motivos, limitaciones, fuentes y presentación prevista están en el protocolo. Sigue fuera del alcance publicar/enviar el paper, cambiar el TFM o afirmar prioridad sin una revisión adicional. La ejecución y auditoría terminaron el 17-09-2026 a las 10:19 de Madrid. Resultados: `ANALYSIS_RESULTS.md`; entrega numérica: `reports/analysis_v1/final/`.

## Historial: revisión técnica terminada, antes de la delegación del 17-09-2026

Los diez modelos terminaron a las 06:29 de Madrid. Revisión completa de archivos, filas, textos, versiones y pruebas técnicas aprobada; `EMBEDDINGS_AUDIT.md` conserva los límites. Se organizaron los resultados mediante catálogo e índice separado, sin mover originales. `sos_analysis/` permite leer los mismos artículos en bloques; ocho pruebas y lectura de las 18 variantes aprobadas.

Es ejecución técnica de la petición del 16-09, **no una nueva decisión científica delegada**. Se documenta la propuesta de comparar forma general + vecinos en `ANALYSIS_PROPOSAL.md`; sigue sin aceptar. El tamaño científico del control, medidas, normalización, salida principal de los cuatro BERT y reglas de estabilidad/calidad permanecen abiertos. No se iniciaron comparaciones científicas. El seguimiento temporal está pausado y comprobado; la antigua automatización OpenAlex también permanece pausada. Evidencia: `research/embedding_final_audit_2026-09-17/automation_closed.json`.

## Seguimiento y revisión final solicitados, 16-09-2026

El usuario pide comprobar el progreso y programar una revisión al acabar, organizar datos y dejar preparada la fase siguiente. Autoriza seguimiento temporal del hilo y organización técnica, sin cambiar el cálculo en marcha ni delegar todas las decisiones científicas abiertas. Plan de revisión: `POST_EMBEDDING_REVIEW.md`. Primera comprobación prevista dentro de cinco horas; si sigue activo, continuar con comprobaciones espaciadas hasta poder auditarlo. La hora estimada de finalización se recalcula a partir del avance, no de la suposición inicial de cinco horas.

## Decidido por el usuario

| Fecha | Decisión | Motivo |
| --- | --- | --- |
| 2026-09-14 | Estudiar cuánto cambia la forma de la ciencia al cambiar el modelo que representa los papers. | Pregunta del nuevo paper. |
| 2026-09-14 | Usar los 26 Fields como unidad principal. | Corrección explícita del usuario respecto a los Subfields. |
| 2026-09-14 | Explicar todo de forma muy sencilla, breve y con analogías cuando ayuden. | Las respuestas técnicas anteriores no se entendían. Regla general en `AGENTS.md`. |
| 2026-09-14 | Mantener un registro escrito de decisiones, dudas, resultados y siguiente paso. | Poder continuar con otras personas y en otros chats. |
| 2026-09-14 | El diseño puede necesitar ampliar OpenAlex; los datos existentes no son un techo. | El usuario permite plantear una extracción mayor si hace falta. |
| 2026-09-14 | Conservar el proyecto anterior sin cambios. | Reutilizarlo como referencia. |
| 2026-09-14 | El asistente decide cuestiones científicas solo cuando se le delegan explícitamente; en ese caso decide y justifica después. En los demás casos presenta opciones y pregunta antes de cerrar la decisión. | Control del usuario, con autonomía dentro del alcance delegado. Regla en `AGENTS.md`. |
| 2026-09-14 | Priorizar solidez científica y decisiones defendibles ante revisores, con QSS como objetivo inicial. | Petición explícita del usuario; no supone garantizar aceptación editorial. |
| 2026-09-14 | Delegar ahora tamaño y reparto del corpus de preparación, con pruebas acotadas en el M5 Pro/48 GB. | Equilibrar representatividad, número de modelos, tiempo de extracción y cómputo. No es una delegación general de decisiones futuras. |
| 2026-09-15 | Preparar y probar el programa; el usuario inicia la descarga completa desde su terminal. | Sustituye la petición inmediatamente anterior de arrancarla desde este chat. Quiere consultar el avance cuando vuelva; no pide seguimiento automático. |
| 2026-09-15 | Comparar más de cuatro modelos y priorizar los usados en trabajos académicos para mapear ciencia. | Peticiones «Quiero más de 4» y «mira los que se suelen usar […] para este propósito». Sustituye el criterio de variedad general como prioridad de selección; no aprueba nombres concretos ni inicia modelos. |

## Elección posterior del usuario: diez modelos, 15-09-2026

«Los 10. Vamos hazlo perfecto» elige los ocho de `MODEL_SELECTION.md` más BioBERT y SimCSE. Lista: SPECTER original, SPECTER2, SciNCL, SciBERT, BERT, all-mpnet-base-v2, all-MiniLM-L6-v2, PubMedBERT/BiomedBERT abstract-fulltext, BioBERT v1.1 y SimCSE no supervisado BERT-base-uncased. Sustituye la pregunta ocho/diez. TF-IDF y paraphrase-MPNet no están incluidos.

Se prepara un programa reanudable y una prueba técnica sobre la tabla ya congelada. Se fijan revisiones oficiales sin entrenar ni elegir modelos según sus resultados. El usuario responde y acepta **uso habitual + control de fragmento común**. Después pide dejar un comando y una estimación: **él iniciará el cálculo completo; el asistente solo hace las pruebas acotadas necesarias**. No se cierran medidas finales, normalización ni el resumen principal de las representaciones de palabras de los cuatro BERT sin ajuste para similitud. Se conservan varias salidas de la misma pasada para no repetir horas de cálculo; no se cuentan como modelos independientes.

## Decidido por el asistente dentro de la delegación sobre el corpus

Protocolo vigente: **`CORPUS_PROTOCOL.md`**, 14-09-2026.

| Decisión | Justificación y alcance |
| --- | --- |
| Preparar **500.000 trabajos válidos con IDs distintos**. | Presupuesto de preparación basado en cobertura y medidas reales de tiempo/memoria; no garantía universal de precisión para todas las métricas. |
| **400.000** en una selección aleatoria global tras filtros; **100.000** de complemento. | Mantener una base proporcional y proteger comparaciones pequeñas sin limitar todas las áreas por la menor. |
| Complemento automático a las celdas Field×período menos numerosas; cinco períodos de cinco años en 2000–2024. | Reparto explícito sin elegir 130 cuotas manuales. Proyección: mínimos cercanos a 2.200 por celda; cantidades finales tras la limpieza. |
| Catálogo principal; artículos, revisiones y congresos; inglés; título no vacío y abstract reconstruible ≥50 palabras; sin retractados/paratext y con Field principal conocido. | Incluir vías importantes de publicación, conservar títulos cortos y reducir descartes desiguales por longitud. Marcar abstracts 50–79 para sensibilidad a ≥80. |
| Excluir preprints de esta primera población. | Reducir la mezcla de versiones preliminares y publicadas; auditar posibles duplicados restantes. |
| Conservar la separación entre base general y complemento en los análisis. | Los 500.000 juntos no tienen reparto proporcional. Conclusiones generales limitadas a la literatura que cumple los filtros. |
| Reutilizar por ID y contenido comprobados, con versiones de modelos identificadas. | No incorporar el corpus antiguo por conveniencia ni mezclar embeddings de procedencia incierta. |

Estas decisiones sustituyen las propuestas anteriores de reparto. **Extracción terminada el 15-09-2026: 400.000 base y 100.000 complemento. Limpieza y reposición autorizadas posteriormente; consultar el estado de ejecución y `CLEANING.md`.**

## Propuestas que NO están aprobadas

- 5.000 papers por Field y 200 por año: propuesta anterior cuestionada por el usuario y retirada como recomendación actual. Archivada en `research/FIELD_SAMPLING_initial_proposal.md`; no estaba justificada como tamaño final.
- La segunda propuesta, sin tamaño cerrado, está archivada en `research/FIELD_SAMPLING_review_proposal.md`. Sustituida por la decisión delegada de 500.000; no confundir ambos estados.
- El conjunto concreto de modelos, variantes de texto y tamaños de muestra del brief son un punto de partida; no tratarlos como protocolo cerrado.
- Propuesta inicial de cuatro y ampliación provisional por diversidad a ocho: **sustituidas** por el criterio posterior del usuario de priorizar uso en mapas científicos. Historial en `research/MODEL_SELECTION_diversity_proposal.md`; nunca fueron aprobadas.
- Propuesta tras revisión académica: ocho más BioBERT/SimCSE. **El usuario aceptó los diez después**; esa elección está registrada arriba. Evidencia y límites en `ACADEMIC_MODEL_USAGE.md` y `MODEL_SELECTION.md`.

## Cierre de las decisiones delegadas, 17-09-2026

Las medidas, normalización, recetas, texto común, calidad y referencias de vecinos ya se decidieron y ejecutaron. No volver a pedir esos acuerdos. La auditoría completa y la presentación están terminadas. Esta sección sustituye el estado previo «controles en curso».

| Decisión dentro del alcance delegado | Evidencia y motivo | Límite |
| --- | --- | --- |
| Mantener el corpus actual, sin una nueva extracción general. | 5.800/5.850 comparaciones pasan la comprobación de selección; resultados principales con todas las filas y controles completos. | 50 alertas en 13 celdas permanecen visibles. No afirmar precisión poblacional ni interpretar diferencias pequeñas en ellas como firmes. |
| Mantener MiniLM 256 como principal y 512 como control. | El límite original es el habitual del modelo, no un error. 512 reduce recortes de 49,58% a 6,87%; cambio medio de coincidencia con otros modelos +0,78 puntos. | Leer más no demuestra representar mejor; no convertirlo en un undécimo modelo. |
| Usar tres vistas: relaciones entre áreas, organización interna y vecinos. | Correlación de rangos mediana 0,847 frente a 0,519; vecinos locales 30,3%, con 31,9% al igualar candidatos. | Distintos objetos y medidas; no son porcentajes intercambiables de acierto. |
| Presentar la dependencia de modelo y receta; conservar media como principal. | Alternativas de receta cambian sustancialmente la forma; texto común mueve típicamente menos el acuerdo. | No seleccionar después la receta con mayor acuerdo ni llamar calidad al consenso. |
| Añadir control de 2.048 candidatos iguales y recetas comunes. | Decidido antes de inspeccionar acuerdos de vecinos; el ajuste por azar no elimina todo el efecto del tamaño. | Es una comparación separada con menos candidatos, no reemplaza los 500.000. |
| Comprobar centros con texto, calidad, recetas y grupos aleatorios. | Seguimiento posterior al primer resultado, con código separado; el acuerdo amplio persiste, con referencia aleatoria positiva alrededor de 0,60. | Declarar que son controles posteriores. No ocultar SPECTER–BERT, excepción a superar su referencia mediana con texto habitual. |
| Seleccionar cuatro figuras principales y cuatro de suplemento. | `PAPER_OUTLINE.md`: niveles, parejas, áreas y recetas. Todas las tablas y controles disponibles. | Manuscrito y aportación bibliográfica por redactar; no prioridad absoluta ni aceptación garantizada. |

La delegación termina con esta fase. No quedan preguntas necesarias para cerrar lo solicitado. El siguiente trabajo es convertir la evidencia en manuscrito, no ejecutar todas las ideas antiguas de `02_open_questions.md`. Una ampliación sustantiva, nuevos modelos, publicación de datos o envío a revista no se asumen autorizados por este cierre.


## Estado de ejecución

**Preparación y comparación científica terminadas y auditadas.** Los 500.000 artículos originales y los diez modelos se conservan intactos. `ANALYSIS_RESULTS.md` contiene la entrega; `ANALYSIS_PROTOCOL.md` sustituye la propuesta anterior. `task_plan.md` y `progress.md` registran el cierre. No repetir la descarga ni los diez cálculos principales. Las automatizaciones antiguas permanecen pausadas.

## Detalles de ejecución dentro de la tarea autorizada, 15-09-2026

- Conservar páginas completas antes de seleccionar y aplicar cada bloque de una sola vez. Mezclar reproduciblemente el bloque completo antes de conservar los primeros válidos necesarios; no depender del orden devuelto en las páginas.
- Guardar semillas, fechas, orden dentro de página y de selección, descartes, configuración y huellas del programa. Un ID solo puede entrar una vez.
- Comprobar todos los IDs ya guardados al reanudar un bloque incompleto; si cambian, pausar para revisión. Conservar los textos recibidos, con sus fechas. No afirmar que la API viva ofrece una instantánea global inmutable.
- Ajustar el tamaño de los bloques del complemento a las plazas pendientes para ahorrar peticiones. Si un bloque no añade trabajos, ampliar progresivamente la petición hasta 10.000 candidatos. Solo declarar agotamiento cuando se recibe el conjunto completo, no por unos cuantos descartes. Sin esa evidencia, pausar tras 20 bloques vacíos y revisar, sin sustituir cuotas o población de forma silenciosa.
- Mantener un índice local de IDs/huellas del TFM. Coincidencia de texto no equivale por sí sola a autorizar reutilizar un embedding sin comprobar su procedencia.

Son detalles necesarios para ejecutar el protocolo ya decidido. No cambian el tamaño, el reparto, la población ni las decisiones científicas pendientes.

## Supervisión solicitada después del arranque, 15-09-2026

El usuario informa de 397.730 trabajos y pide permanecer supervisando hasta terminar, auditar si los datos sirven y dejar la fase siguiente preparada. Esta petición sustituye la ausencia anterior de seguimiento automático. Se configura seguimiento temporal del hilo cada cinco minutos, `auditar-descarga-openalex`, que debe desactivarse al concluir. No implica delegar modelos, medidas ni filtros nuevos, ni iniciar embeddings.

## Cierre histórico de la auditoría, 15-09-2026

El estado de aprobación de esta sección fue sustituido por la petición de limpieza que se registra a continuación. Las cifras describen el diagnóstico inicial, no todos los errores detectados después.

- Terminada la descarga y la auditoría completa: 500.000 IDs únicos, 26 Fields, 130 celdas, mínimo 2.163 por celda. No se ha cambiado el tamaño o reparto científico.
- Diagnóstico: 8.544 posibles abstracts fuera del inglés (5.122 con puntuación ≥0,9); 166 registros señalados por contenido de páginas/catálogos; 12 posibles avisos por título; duplicados documentados. Son alertas que pueden solaparse, no una regla de exclusión ya aprobada.
- Propuesta sin aprobar: limpiar con reglas comunes y completar primero la base aleatoria, después recalcular el complemento. Alternativa: aceptar un tamaño menor tras limpiar y justificarlo. Las opciones están en `NEXT_STEPS.md`; preguntar antes de cerrar esa decisión.
- No se eliminaron, tradujeron ni sustituyeron registros. No se iniciaron embeddings. Los 22.118 vectores antiguos candidatos requieren resolver procedencia y compatibilidad antes de su uso final.

## Limpieza autorizada por el usuario, 15-09-2026

La petición «sigue con limpieza […] aprovecha lo ya descargado o descarga más si lo necesitas» acepta realizar la limpieza y completar el objetivo 400.000+100.000. Sustituye el estado anterior de propuesta sin aprobar para esta fase y autoriza las descargas adicionales necesarias desde el asistente. Los originales se conservan. No implica elegir los modelos finales o iniciar su cálculo. El tratamiento de idiomas dudosos se ha consultado expresamente; reglas concretas y resultados se recogerán en `CLEANING.md`.

### Ejecución conservadora de la limpieza autorizada

Se consultó al usuario el tratamiento de idiomas dudosos. Mientras no se indique una criba más estricta, se mantiene el criterio recomendado: excluir solo alertas fuertes consistentes en el resumen completo y sus tres secciones; conservar el resto con marcas. Se comunicó este criterio antes de seleccionar. No se presenta el corte numérico como una garantía de acierto ni como exigencia de QSS. La posibilidad de una criba más estricta queda abierta para sensibilidad. Se conservan los duplicados entre IDs distintos como grupos marcados, según el protocolo original; no se cambia la unidad de selección ni se fusionan estudios.

## Cierre de la preparación autorizada, 15-09-2026

- Terminada la limpieza y reposición pedidas por el usuario, manteniendo 500.000 = 400.000+100.000. No se reabrió el tamaño ni se eligieron cuotas nuevas. Mínimo final: 2.165 por Field/período; 650 combinaciones Field/año presentes.
- 5.776 registros originales apartados por calidad; otros 123 válidos no se reeligieron al recalcular el reparto. Se aprovecharon 5.889 candidatos sobrantes y diez de una única página adicional de 100 candidatos. Los 499.990 restantes proceden de las páginas originales.
- Los casos ambiguos se conservan con marcas según el criterio conservador comunicado. La ausencia de respuesta a la pregunta no se registra como aprobación explícita de los umbrales. La petición sí autoriza implementar la limpieza; una criba más estricta sigue abierta para la fase de controles.
- Reglas de contenido ampliadas al inspeccionar el corpus y aplicadas a todos los candidatos antes de embeddings. No son reglas registradas antes de observar los datos. Se corrige y documenta el fallo de aplicación a una página nueva; el archivo final pasó todas las comprobaciones.
- Hay 22.118 vectores antiguos candidatos con textos idénticos, localizados y válidos numéricamente. Esto resuelve el número de coincidencias, pero no su procedencia exacta ni su aprobación para el paper.
- Próxima decisión científica: conjunto final de modelos, versiones y formato de entrada. Se presentarán opciones al usuario salvo delegación expresa. No hay delegación general para iniciar experimentos.

## Revisión del reparto y propuesta de modelos, 15-09-2026

- Petición del usuario: identificar áreas/períodos débiles, valorar suficiencia y proporciones y preguntar por los modelos, considerando publicación y originalidad. Autoriza esta revisión; no delega cerrar el conjunto de modelos.
- Comprobado directamente en el corpus final: las 130 combinaciones coinciden con los recuentos de limpieza. Mínimo 2.165 en 12 combinaciones; otras 68 tienen 2.166. Detalle en `CORPUS_BALANCE.md`. El refuerzo conserva los tamaños grandes y protege los pequeños; los porcentajes finales no son los porcentajes de la población.
- Recomendación: mantener los 500.000 preparados y no ampliar ahora. No se cambia el tamaño previamente delegado ni se afirma suficiencia universal. La prueba anterior solo apoya comenzar; la estabilidad de nuevos modelos, áreas y medidas queda por comprobar.
- Diagnóstico, sin aplicar exclusiones: al omitir hipotéticamente idioma dudoso o resúmenes de 50–79 palabras, Matemáticas 2000–2004 quedaría en 1.376. Señala dónde priorizar controles, no una nueva regla aceptada ni evidencia de que esos artículos sean inválidos.
- Modelos, variantes, formatos y reglas de análisis siguen abiertos. Preguntas presentadas: mezcla ciencia/general frente a solo ciencia; cuatro propuestos frente a añadir SciNCL como quinto. Los motivos y la revisión de trabajos relacionados están en `MODEL_SELECTION.md`.
- Originalidad propuesta: conclusiones sobre relaciones entre áreas y cambios temporales que resisten cambios de modelo, selección y entrada. La búsqueda dirigida identifica antecedentes; no demuestra prioridad. No se inició ningún modelo ni se cambiaron datos, filtros o cuotas.

## Criterio académico para ampliar modelos, 15-09-2026

- El usuario rechaza limitarse a cuatro y precisa que quiere cubrir los usados para mapear ciencia. Se investigan aplicaciones y comparaciones reales, separadas de popularidad comercial y de pruebas generales de recuperación.
- Se contrastan diez trabajos: SPECTER y SciBERT aparecen en cinco cada uno; MPNet, MiniLM y BERT en tres; SciNCL en dos. Frecuencias por familia/estudio dentro de una revisión dirigida, no cuotas de uso de toda la comunidad. Hay variantes y niveles de acceso distintos, registrados en el informe.
- Se recomienda cubrir esos seis comparadores recurrentes y añadir SPECTER2 por su antecedente reciente/continuidad del TFM y PubMedBERT por el mapa biomédico completo. Estos dos tienen un antecedente cada uno en la revisión: no se presentan como igualmente habituales.
- Más de cuatro y el criterio de antecedentes quedan aceptados por instrucción directa. El grupo exacto de ocho/diez, el control TF-IDF y las recetas siguen como propuestas. No se considera delegación general ni autorización para calcular.
- Corregida una atribución bibliográfica: el DOI qss_a_00168 no corresponde a Lamers. Se usa el registro ISSI comprobado. SemCSE-Multi tiene publicación ACL 2026; la revisión previa solo había localizado el preprint.

## Comparación científica delegada, 17-09-2026

El usuario autoriza continuar con la comparación de la forma y después de los vecinos, delegando las cuestiones pendientes de esta fase con criterio de solidez para QSS. Autoriza investigar medidas más robustas, ejecutar las comparaciones, inspeccionar resultados y preparar su presentación. Pide diagnosticar el recorte de MiniLM y corregir/recalcular si procede. Esta petición sustituye las restricciones previas de solo preparación y de esperar nuevas respuestas para esas decisiones. Se decidirán y documentarán medidas, recetas, controles y presupuesto antes de inspeccionar acuerdos. Conservar las salidas congeladas; cualquier corrección o variante nueva irá en una salida separada. No implica publicación, envío a revista ni cambios al TFM.

## Ampliación delegada mediante checklist, 17-09-2026

El usuario pide ejecutar el piloto título/resumen/ambos, comparar entrada frente a modelo, cerrar la receta, analizar tiempo, disciplina y familias, «encajándolo como veas correcto». Autoriza esta ampliación y las decisiones necesarias dentro de ella; sustituye el cierre previo solo para estos puntos. No autoriza automáticamente recalcular las otras dos entradas sobre 500.000 ni publicar. Protocolo previo a los resultados nuevos: `CHECKLIST_PROTOCOL.md`, `config/checklist_v1.json`. Se confirma media como principal y CLS/SEP como controles, por continuidad del criterio fijado y sin seleccionar por mayor acuerdo. Piloto de 26.000 estratificado, estabilidad explícita y resultados separados. Los grupos de entrenamiento se apoyan en fuentes, no se definen por cómo salgan sus acuerdos.

## Cierre de la checklist: decisiones tomadas por delegación, 17-09-2026

Los seis puntos solicitados están terminados y auditados. Este cierre sustituye el estado de piloto activo, sin alterar las decisiones ni los originales de la fase anterior. Evidencia: `CHECKLIST_RESULTS.md`, `reports/checklist_v1/final/` y `METHODS_CHECKLIST.md`.

| Decisión | Motivo y evidencia | Límite que conservamos |
| --- | --- | --- |
| Mantener el piloto de 26.000; no repetir ahora título/resumen sobre 500.000. | Los 52 promedios de área pasan la comprobación de forma fijada; los patrones generales se examinan también con rangos, vecinos y recetas. | 31 de 520 contrastes individuales superan la amplitud permitida, en 17 áreas. La criba es de forma, no una garantía de estabilidad de vecinos ni precisión poblacional. Una diferencia pequeña esencial al manuscrito exigiría comprobación dirigida. |
| Confirmar mean para los cuatro BERT, incluidos símbolos especiales; CLS/SEP como controles. | Continuidad de la regla fijada antes del primer análisis; cruce de las tres recetas sobre las tres entradas terminado. | La confirmación es posterior a conocer sensibilidades anteriores. No es una demostración de superioridad semántica ni una elección por el mayor consenso. |
| Separar quitar título de quitar resumen; no proclamar que texto o modelo domina siempre. | Con mean se pierden 16,2/25 vecinos al cambiar modelo, 16,7 al quitar resumen y 5,0 al quitar título. El primer orden se invierte con CLS/SEP y varía entre modelos. | Comparación práctica de formatos y límites habituales, no descomposición causal pura. La cercanía de medias no prueba equivalencia. |
| Priorizar candidatos iguales en las comparaciones temporales y mostrar ambos resultados. | Vecinos: −0,87 puntos entre fechas con todos los candidatos frente a +0,91 con 2.048. El contraste posterior con consultas idénticas conserva la inversión. | Promedios descriptivos de modelos actuales sobre documentos de otras fechas; no historia causal ni aumento uniforme. |
| Presentar Medicina y familias como localización y explicación parcial de diferencias. | Los biomédicos se parecen entre sí y la diferencia Medicina–Energía persiste al omitirlos. Los grupos definidos por fuentes tienen mayor acuerdo interno promedio. | Composición y entrenamiento están asociados, no aislados causalmente. Los grupos no son tres bloques cerrados y el ajuste de familias cambia mucho con SEP. |
| Dar prioridad en el manuscrito a niveles del mapa, pares, efecto de entrada y control temporal. | Esquema actualizado en `PAPER_OUTLINE.md`, conservando todas las tablas y figuras de ambas fases. | La novedad no es usar título/abstract ni contar diez modelos; debe contrastarse frente a los antecedentes próximos. |

La ampliación de recetas se fijó antes de inspeccionar acuerdos del piloto, según `recipe_control_decision.json`. La comprobación temporal con consultas idénticas se añadió después de observar la inversión; describirla como tal. Se mantienen las 50 alertas anteriores, separadas de las 31 nuevas. No se han cambiado umbrales tras los resultados.

No quedan cálculos activos ni decisiones necesarias del usuario para cerrar esta petición. Continuación preparada: redacción cuando se solicite. No se autoriza por extensión una nueva descarga, otros modelos, publicación de datos o envío a revista. Las automatizaciones previas siguen pausadas.

## Nueva ampliación explícita: cierre experimental, 17-09-2026

El usuario fija un objetivo nuevo íntegro en `ROBUSTNESS_SCOPE.md`. Sustituye el cierre con 26k y autoriza 52k, Subfields, estabilidad por artículo y las revisiones allí listadas antes de redactar. Se conserva el diseño estratificado: 400 artículos en cada una de las 130 celdas, misma semilla y regla por ID; los primeros 200 permanecen. Se reutilizan los 26k y el title+abstract original, sin cambiar pesos/formatos/recetas. Configuración separada `config/input52_v1.json`. Media sigue principal; no volver a elegirla por los acuerdos.

La meta no se limita a los datos que ya existen. Se cerrará con verificación individual de R01–R12. Nuevas decisiones necesarias quedan dentro de este objetivo, con justificación y límites; no se asume autorización para redactar, publicar, nuevos modelos o nueva extracción masiva.

## Cierre ampliado: controles de composición y rasgos, 17-09-2026

Por la delegación explícita de la meta vigente, se fijan tamaños/repeticiones/elegibilidad en `ROBUSTNESS_PROTOCOL.md` y sus cuatro configuraciones nuevas antes de sus cálculos. Para Medicina se compara igual tamaño y fechas cambiando solo las cuotas de especialidades entre los artículos elegibles. Motivo: separar una mezcla distinta de temas del mero crecimiento del conjunto. Límite: retirar los grupos pequeños cambia el universo; se muestra la cobertura y dos áreas sin contraste identificable.

La arquitectura se lee de los archivos realmente usados. MiniLM tiene seis capas y 384 dimensiones; MPNet es otra arquitectura; SPECTER2 usa además un adaptador. El linaje y el corpus se documentan aparte. Los diez modelos no permiten atribuir causalmente una diferencia a una sola pieza; se conservan las asociaciones y sus omisiones, sin presentar la regresión como un experimento de entrenamiento.

## 17-09-2026 — Decisiones de cierre ampliado ya verificadas

Por delegación explícita del objetivo R01–R12, se mantiene CKA corregida principal y vecinos exactos k25, con Procrustes/rangos/k10/k50 como comprobaciones. No añadir morfología: dispersión, dimensionalidad y conectividad exigirían otras hipótesis; no son necesarias para contestar esta comparación. Evidencia y revisión reciente en `METRICS.md`.

Se conserva mean para BERT/SciBERT/BioBERT/PubMedBERT, definido exactamente en `POOLING.md`. Su comparación CLS/SEP usa salidas separadas; no se escogerá la receta según qué resultado produzca más acuerdo. Las familias se interpretan como asociaciones de diez modelos fijos, con corpus y otros rasgos parcialmente confundidos, no como causas identificadas: `MODEL_FAMILIES.md`.

La comparación de niveles se presentará como resultados distintos sobre centros, organización interna y vecinos. El control con mismas consultas/candidatos/fechas muestra una bajada media pequeña y muchas excepciones, no una ley universal de menor acuerdo con mayor detalle. `SCALES_AND_DISCIPLINES.md`. Los Subfields siguen siendo nivel adicional; no sustituyen al Field principal.

Se mantienen las 50 alertas originales y todas las nuevas por especialidad; amplitud cero cuando la selección usa todo el grupo no prueba certeza sobre la población. La inferencia de nuevas entradas 52k ha finalizado; siguen pendientes su auditoría/comparaciones/100 selecciones antes de cerrar esa parte y la meta completa. No extender ahora entradas a 500.000 ni iniciar otros modelos, extracciones o manuscrito.

## 17-09-2026 — Cierre definitivo de R01–R12 por la delegación ampliada

La ampliación de entradas a 52k, sus tres condiciones, recetas y 100 selecciones en ambos tamaños están terminadas y auditadas. La regla fijada da 72/520 alertas en 26k frente a 5/520 en 52k al usar 100 selecciones. Se conserva por separado la comparación histórica 31 → 4 con 20. Las cinco actuales incumplen amplitud, no desplazamiento mediano; Health Professions/PubMedBERT/title supera 0,04 por muy poco y no se redondea para hacerlo pasar. De las 31 claves originales, cuatro siguen alertadas en 52k/100. Las 50 originales y las de Subfields se mantienen.

Decisión delegada: conservar la ampliación de 52k como comprobación de entradas de esta fase, sin pasar automáticamente a 500k. Razón: los patrones generales están calculados, las 52 medias de área pasan la regla, y los casos finos que siguen inciertos quedan localizados. Esto no prueba equivalencia modelo/texto, superioridad de una receta ni precisión sobre toda la población. Seis contrastes medios de área incluyen cero pese a superar la criba.

Mean sigue principal; recetas alternativas pueden cambiar la interpretación y están completas por modelo/área/entrada. Se presentan cuatro figuras principales sobre estructura, entrada, vecinos emparejados y tiempo; Medicina, familias y estabilidad aportan comprobaciones adicionales. La revisión bibliográfica identifica solapamiento directo con comparaciones previas de forma/vecinos/familias: la aportación se delimita por los resultados y controles, no por reclamar componentes nuevos.

R01–R12 verificados, sin procesos activos. La delegación de este objetivo termina aquí. Se actualizan resultados, métodos, catálogo, inventario, preguntas históricas, esquema y continuidad. No se amplía autorización a redactar, publicar, distribuir datos, otros modelos o nueva extracción. Reproducción de presentación y siguiente paso en `NEXT_STEPS.md`.

## 17-09-2026 — Revisión previa al manuscrito y casos concretos autorizados

El usuario pide revisar todo el análisis, referencias y repositorio antes de redactar, y profundizar en artículos/Subfields/relaciones especialmente estables o dependientes del encoder. Autoriza esta revisión, las mejoras de presentación y análisis derivados necesarios dentro de ese alcance. Se conservan medidas/recetas y datos anteriores; los nuevos criterios de selección se registrarán antes de examinar los ejemplos. No autoriza nuevas extracciones masivas, modelos adicionales, redacción ni publicación. La revisión buscará debilidades reales y un hueco defendible; no una garantía de aceptación en QSS.

## 17-09-2026 — Cierre de la revisión previa: decisiones dentro del alcance delegado

Estas decisiones ejecutan la revisión y el análisis de casos pedidos. No sustituyen las medidas, recetas, corpus ni reglas de las fases cerradas. Evidencia: `PREPAPER_REVIEW.md`, `CASE_ATLAS_PROTOCOL.md`, `CASE_ATLAS.md` y `research/prepaper_2026-09-17/`.

| Decisión | Motivo y evidencia | Límite / siguiente actuación |
| --- | --- | --- |
| Extraer el atlas de las salidas existentes, sin inferencia nueva. | 217 Subfields a 256; comparación de posición en las mismas 183 especialidades bajo 27 condiciones. Doce artículos elegidos con reglas por ID, sin leer primero los títulos. | Es un seguimiento exploratorio después de los resultados generales, no un preregistro del estudio completo. |
| Comparar relaciones entre consultas siempre presentes. | 531.650 relaciones dirigidas: diez repeticiones por modelo; ambos artículos disponibles en cada búsqueda. Así no se confunde ausencia como candidato con rechazo como vecino. | Son 49 posibles compañeras fijas por consulta dentro de cada Subfield; no todas las parejas de 500k ni todos los controles de entrada/receta. |
| Conservar y anotar los ejemplos desfavorables, incluidos errores de OpenAlex. | Treinta registros ilustrados comprobados contra páginas originales. Dos etiquetas claramente incompatibles y un aviso proceden de la fuente, no de nuestro alineamiento. | No sustituirlos para mejorar la historia ni corregir a mano el corpus. Acuerdo no equivale a precisión temática. |
| Añadir un diagnóstico posterior de títulos genéricos. | 82/500k; cinco entre las consultas controladas. Al excluir solo esas cinco, la media cambia de 45,344% a 45,349%. | No es una limpieza nueva, no cambia candidatos y no estima la tasa de clasificación temática errónea. Validación externa necesaria si se quisiera afirmar precisión o causas disciplinares. |
| Precisar la comparación Field/Subfield. | Ambas búsquedas de 256 conservan las 50 consultas del mismo Subfield; esto favorece la comparabilidad de artículos y su presencia. | La búsqueda amplia está condicionada; no describirla como 256 candidatos extraídos libremente del Field. No cambia ninguna cifra. |
| Centrar la contribución en qué conclusiones resisten decisiones de construcción del mapa. | Antecedentes directos ya comparan modelos, entradas, forma y vecinos. La revisión incluye Caspari, Singh, Bascur y SemCSE-Multi. | No vender diez modelos, CKA o vecinos como innovaciones por sí mismos; no prometer prioridad absoluta. |
| Usar una biblioteca canónica y conservar el historial. | 45 referencias verificadas; autores, versiones, páginas y DOI erróneos corregidos; copia de la bibliografía anterior. | Una advertencia de páginas ausentes en ICLR se conserva. Metadatos verificados no significan lectura completa de todas las fuentes. |
| Ordenar con índices y entregas separadas. | README, `docs/`, `references/`, atlas y catálogos; originales conservados. | No mover rutas congeladas, publicar, elegir licencia o activar automatizaciones. El depósito y las declaraciones se prepararán con autorización y datos reales. |

La revisión técnica queda cerrada. Preparado para iniciar redacción cuando se solicite, con los límites anteriores. Antes del envío habrá que actualizar fuentes/normas QSS, revisar las afirmaciones con los autores y verificar un depósito reproducible. No se ha escrito ni enviado el manuscrito.

## 17-09-2026 — Commit y push autorizados expresamente

El usuario pide subir la versión revisada antes de redactar. Destino comprobado: `https://github.com/aleetreny/Shape-of-Science-Robustness`, público, inicialmente vacío y con acceso de administración. La carpeta local no tenía commits ni remoto configurado. Se autoriza la primera versión de código, decisiones, documentación, tablas, figuras y evidencia auxiliar versionable. No se suben corpus, embeddings, pesos, claves, entornos ni textos completos de terceros. No se modifica la visibilidad del repositorio ni se elige licencia. El depósito científico permanente y el manuscrito siguen pendientes.


## 18-09-2026 — Piloto de morfología autorizado expresamente

El usuario pide estudiar medidas concretas de forma, incluyendo fragmentación, ejecutar un análisis preliminar y comprobar alternativas, calidad y estabilidad. Delega las decisiones necesarias para este alcance. Esta petición sustituye **solo para este piloto nuevo** la decisión anterior de no añadir morfología; no cambia retrospectivamente CKA/vecinos ni sus resultados. Se fijarán medidas, muestras, alternativas y criterios antes de calcular los nuevos resultados reales. Se reutilizan vectores existentes en salidas separadas; no hay autorización ampliada para nuevas extracciones/modelos, manuscrito, depósito o publicación. La entrega distinguirá resultados exploratorios, controles satisfactorios, fallos y aspectos aún no demostrados.


### Diseño fijado antes de resultados reales del piloto

`config/morphology_pilot_v1.json` fija tres propiedades: apertura angular (mediana entre pares), dimensión efectiva lineal (participation ratio de la covarianza centrada), conexión de un grafo de vecinos (brecha de Laplaciano normalizado, k=25). Alternativas y escalas se conservan por separado, sin puntuación total. La tercera no se interpretará como fragmentación temática: falló esa interpretación en nubes simuladas. La entropía y D80 son otras lecturas del mismo espectro, no validaciones independientes de significado. Todas las medidas se obtienen en el espacio completo.

Se reutilizan 52k, 2.000 por Field y 400 por período. Veinte selecciones internas de 1.000; cinco nuevas selecciones de 2.000 desde el corpus congelado; tamaños 500–4.000. Entradas/recetas, texto común, MiniLM512, marcas de calidad, extremos, centrado global y referencias gaussianas van separados. Hay controles temporales acotados con tamaños iguales. Las cribas relativas de amplitud (5% apertura, 10% dimensión, 20% conexión) son umbrales operativos del piloto; no justifican precisión poblacional ni se cambian para aprobar resultados. La evidencia continua y las inversiones de orden importan más que un aprobado.


### Comprobación interpretativa de tamaño/conectividad durante la ejecución

Con los k25/k50 ya calculados se añadirá una tabla que aproximadamente conserva k/(n−1) al duplicar n. Se registró antes de revisar las curvas completas; no sustituye el protocolo congelado ni es una decisión inicial. Motivo: cambiar n con k fijo cambia también la definición de la red. Se mostrarán ambas sensibilidades para todos los modelos/áreas, sin seleccionar la favorable. Detalle en `research/morphology_2026-09-18/INTERPRETATION_ADDENDUM.md`.

### Cierre del piloto: decisiones tomadas dentro de la delegación

Evidencia completa en `MORPHOLOGY_RESULTS.md`, `METHODS_MORPHOLOGY.md` y `research/morphology_2026-09-18/closure_audit.json`. Se conserva la fase anterior; las medidas nuevas no sustituyen CKA ni vecinos.

| Decisión | Motivo comprobado | Límite que se conserva |
| --- | --- | --- |
| Retener apertura y PR como descripciones geométricas. | Repetición a igual tamaño: acuerdo mediano del orden de áreas 0,992/0,989; entre modelos 0,319/0,552. De 2.000 a 4.000, cambio mediano −0,03%/+1,14%. | Receta y centrado importan. No llamar diversidad temática a apertura ni temas a PR; cuatro alertas internas de PR siguen vigentes. |
| Conservar conexión como diagnóstico, sin adoptar «fragmentación» genérica. | Nubes alargadas dan conexión débil sin separar grupos; el grafo unión queda conectado en 260/260 casos. Variar la regla de vecinos cambia la lectura del tamaño. | 51 alertas externas de conexión; las alternativas no son intercambiables. No resolverlo eligiendo la más llamativa. |
| No ampliar cálculos del piloto a todas las combinaciones de 500k. | Los controles 500–4.000, veinte medias muestras, cinco selecciones de igual tamaño y alternativas ya permiten responder a la pregunta preliminar. | No fijan un tamaño suficiente para toda afirmación poblacional ni eliminan los casos inestables. Una nueva pregunta necesitaría alcance propio. |
| Añadir un ejemplo de inversión y casos resistentes, marcados como ilustrativos posteriores. | SPECTER sitúa Medicina más abierta que Artes; BERT invierte la relación. Los signos persisten en 20+5 selecciones y tres descripciones angulares alternativas. Odontología/Energía ilustran resistencia con límites de receta. | Los casos se eligieron tras ver resultados; no estiman la frecuencia de inversiones ni indican qué modelo tiene razón. |
| Recomendar una sección breve dentro del argumento actual. | Muestra qué afirmaciones del mapa dependen del encoder, en vez de acumular métricas. Se propone mantener cuatro figuras y trasladar tiempo al suplemento. | Es una recomendación de presentación en `PAPER_OUTLINE.md`, no un manuscrito aprobado ni una garantía de aceptación en QSS. |
| No convertir los patrones temporales o gaussianos en explicaciones causales. | Se observan cambios temporales y diferencias frente a referencias simples; faltan controles de composición para estas nuevas propiedades y las referencias no igualan exactamente el espectro tras normalizar. | No afirmar estrechamiento histórico de la ciencia ni fragmentación temática demostrada. |

La delegación de este piloto queda cerrada. Se entregan alternativas, fallos, límites y procedencia; no quedan tareas necesarias para su cierre. No se añade autorización para nuevas extracciones/modelos, redacción, distribución de datos o publicación. El siguiente paso es decidir la incorporación al manuscrito cuando el usuario lo pida.

## 18-09-2026 — Último resumen de parejas aceptado por el usuario

El usuario acepta la propuesta de resumir todas las 325 parejas de disciplinas antes de decidir cómo organizar el manuscrito. Autoriza los derivados y comprobaciones necesarios sobre los resultados existentes. Alcance: apertura/PR, acuerdo de diez, contradicción persistente y casos sin conclusión común clara; tamaños de diferencia y controles ya guardados. No autoriza nuevos embeddings, extracción, modelos, fragmentación, publicación o redacción automática.

`FIELD_PAIR_PROTOCOL.md` y `config/field_pairs_v1.json` fijan las reglas antes de calcular estos recuentos. Persistencia exige igual dirección en principal + 20 medias muestras + 5 selecciones del mismo corpus. Magnitud continua y sensibilidades 0/1/5/10%, sin elegir el corte por su resultado. Todas las parejas conservan denominador; consenso no equivale a acierto. Se comprueban alternativas, recetas/procesamiento y seis modelos de similitud para conocer el alcance; menos modelos implican menos oportunidades de contradicción. Las alternativas espectrales no tienen las 25 repeticiones completas y se declara su cobertura real.

Los resultados previos y el ejemplo Medicina/Artes ya eran conocidos: esta ampliación es exploratoria posterior. Se conservan documentos con sus huellas anteriores antes de actualizar la continuidad. Al terminar se entregará una propuesta de integración; la organización final del manuscrito se hablará con el usuario.

### Cierre del resumen aceptado: resultados y criterio de presentación

`FIELD_PAIR_RESULTS.md` y `METHODS_FIELD_PAIRS.md` cierran el alcance. Apertura: 42 acuerdos de diez, 262 contradicciones persistentes y 21 sin conclusión común; PR: 54, 221 y 50. Las contradicciones a 5% son 96 y 177; a 10%, 19 y 126. Se mostrarán magnitudes junto a direcciones, sin promover retrospectivamente un corte como correcto.

Las alternativas conjuntas conservan 225/196 contradicciones; seis modelos de similitud conservan 231/160, con menos oportunidades de oposición. El centrado global conserva los mismos modelos testigo en 145/262 aperturas y 218/221 PR, límite sustantivo que acompañará el resultado. Calidad/texto común no convierten las etiquetas en verdad externa. No se ocultan los casos no resueltos ni las alertas anteriores.

Decisión dentro del alcance aceptado: terminar aquí los derivados experimentales y entregar las doce tablas, dos figuras y auditoría. Recomendación para discutir con el usuario: dar prioridad a la figura de recuentos/magnitudes, acompañada del ejemplo y la evidencia de forma/vecinos/entrada ya obtenida; mapa completo y controles en suplemento. Es una propuesta de organización, no una autorización para escribir el manuscrito, publicar, añadir modelos o abrir otra pregunta.

## 18-09-2026 — Revisión editorial amplia de QSS autorizada

El usuario solicita estudiar muchos artículos publicados y cercanos al proyecto, entender su estructura y lenguaje, y proponer cómo organizar nuestro paper. Alcance aceptado: búsqueda documentada, lectura estructural y argumentativa y propuesta aplicada. No equivale a redactar el manuscrito, cambiar decisiones científicas o publicar. La estructura resultante seguirá identificada como propuesta para discutir. Se conserva el cierre anterior antes de actualizar documentos.

### Cierre de la revisión editorial: propuesta, no aceptación de estructura

Se completa una revisión dirigida de 34 artículos de QSS, con 33 lecturas estructurales, once de ellas con foco adicional y una parcial. Marco Crossref completo de 465 registros recuperados; no implica lectura de 465 papers. Se separan versiones editoriales, anticipadas y de autor, y dos cuerpos de versión tipográfica no confirmada. Un cuerpo equivocado se rechazó. La guía oficial solo pudo consultarse mediante índice de rastreo antiguo y se revisará antes del envío.

**Recomendación pendiente de conversar:** un único paper sobre qué conclusiones sobreviven al cambio de representación; tres preguntas, seis secciones, cuatro figuras y dos tablas principales, unas 6.750 palabras de cuerpo como presupuesto propio. Resultados: estructura amplia, vecinos, entrada frente a modelo, comparaciones geométricas entre áreas. Tiempo, Medicina y familias como apoyo; límites sustantivos siempre en el cuerpo. Motivación y alternativas en `QSS_STRUCTURE_REVIEW.md` y `PAPER_OUTLINE.md`.

**No se cierra una decisión científica nueva:** se reorganiza evidencia terminada. No nuevas métricas, resultados, inferencia, extracción ni manuscrito. La propuesta no convierte preguntas posteriores en hipótesis previas. El estudio de QSS no demuestra una estructura obligatoria ni garantiza aceptación. La publicación anterior sigue en `44c9410`; esta entrega no se sube automáticamente. Biblioteca editorial de 34 entradas separada de las 54 canónicas, con solapamientos. Próxima conversación: valorar el esquema propuesto y, solo cuando se solicite, redactar.
