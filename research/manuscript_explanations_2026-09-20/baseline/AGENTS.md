# Cómo trabajar en este proyecto

**Última revisión editorial, 20-09-2026:** abstract aclarado por petición del autor en inglés y español; ver `ABSTRACT_CLARITY.md`. Mantener el comienzo que le gusta y explicar la comparación antes del resultado: disciplinas con ejemplos, posición media de sus artículos, título solo frente a título y resumen, orden contrario entre disciplinas y cambio del punto desde el que se miden los ángulos. No usar «quitar el resumen», «los grupos» o «otro procesamiento» como atajos sin referente. Inglés: 200 palabras; español para revisión: 235. Cuerpo, resultados y suplemento intactos. Esta revisión editorial es posterior al cierre de robustez; no reabrir análisis.

**Cierre vigente, 20-09-2026:** la revisión de robustez delegada está terminada. Leer `ROBUSTNESS_CLOSURE_REPORT.md`, `ROBUSTNESS_MANUSCRIPT_CHANGELOG.md` y `NEXT_STEPS.md`. Centros, contraste directo de vecinos, centrado completo, alternativas de dimensión y calidad están congelados en `data/robustness_closure_v1/`; resúmenes en `reports/robustness_closure_v1/`. Se actualizaron ambos idiomas después de congelar resultados. No repetir análisis por retomar. Las fuentes de `sos_closure/`, su configuración y protocolo son inmutables para esta versión.

**Límites que sustituyen resúmenes parciales anteriores:** apertura: 262 oposiciones originales frente a 151 tras centrar, con 128 que conservan los mismos modelos y direcciones; PR: 221 frente a 211, con 204 conservadas. Al 5 %, apertura pasa de 96 a 11. Las dos alternativas de dimensión cubren ahora 26 condiciones y conservan 190/221 oposiciones originales de PR, no las 196 del control histórico parcial. Las medias del contraste texto/modelo se repiten, pero hay respuestas opuestas por modelo y receta; no afirmar equivalencia. El filtro de calidad apenas cambia el acuerdo local agregado. Mantener visibles las 2.628/8.235 alertas locales. Estos controles no son intervalos poblacionales ni validación temática.

**Tono aceptado expresamente:** «me gusta este tono mucho, conservalo». Mantener la explicación clara sobre V2 en los dos idiomas, sin volver al registro denso ni reabrir la elección de voz. La aprobación del contenido completo, correspondencia, depósito/licencia y envío siguen pendientes. Esta entrega no incluye commit/push, descarga, inferencia o automatización nueva.

**Estado vigente, 20-09-2026: V2 elegida y explicación reescrita.** El autor ha elegido la versión 2, pero exige una lectura mucho más clara. El artículo canónico y su copia española están reescritos; entrega en `MANUSCRIPT_CLARITY.md`. Primero explicar el problema y la comparación, después introducir su nombre técnico. Usar palabras corrientes y frases naturales, sin perder precisión. Cada muestra debe aparecer con su finalidad y su relación con las demás: 500.000 de partida; 52.000 para título/resumen/ambos, incluidos los 26.000 de la prueba inicial; esos mismos 52.000 para geometría; otros 52.000 para fragmento común. No acumular cifras o siglas sin explicar qué responden. Esta regla se aplica al manuscrito y a cualquier chat futuro. Ver `AUTHOR_VOICE.md`.

El título se conserva. Inglés: 3.989 palabras de cuerpo, resumen de 192; PDF de 19 páginas y suplemento de 34. Español: 20 y 36 páginas. Las seis alternativas del 19-09 y la edición anterior están conservadas. Cifras, figuras, archivos de datos y declaraciones no cambian; la tabla de muestras y los pies se explican mejor. La elección de voz está cerrada; la revisión personal del contenido sigue pendiente. Continuar con los comentarios del autor, sin nuevos experimentos ni envío.

**Historial de alternativas de voz, 19-09-2026; elección resuelta el 20-09:** el autor conserva expresamente el título actual, «How much does the map of science depend on the embedding model?», y pide tres redacciones con identidad creciente en inglés y español. Entrega completa en MANUSCRIPT_VOICES.md y manuscript_variants/: seis PDF revisados, 19 páginas por inglés y 21 por español. V1 directa y sobria; V2 razonamiento propio; V3 voz marcada y reflexiva. En aquella entrega se recomendó V2 y se conservó el manuscrito canónico. La elección posterior y la reescritura autorizada del 20-09 sustituyen ese estado pendiente. Las seis alternativas permanecen intactas como historial; no reiniciar análisis ni dar el texto por aprobado.

**Revisión vigente de los cinco comentarios del PDF, 18-09-2026:** ver `MANUSCRIPT_COMMENTS.md` y `research/manuscript_comments_2026-09-18/`. Título actualizado, tablas más legibles, Figura 1B con medias y dispersión descriptiva de resultados guardados, declaración de IA en dos frases. No son intervalos de confianza ni se han recalculado experimentos. Mantener sincronizados inglés y español; las auditorías anteriores son históricas. La aprobación personal sigue pendiente.

Estas instrucciones se aplican a todo el repositorio y a cualquier chat o persona que lo retome.

**Estado histórico del primer borrador, 18-09-2026:** manuscrito y suplemento completos por petición directa, con revisión editorial y visual. Leer `MANUSCRIPT_REVIEW.md`, `MANUSCRIPT_LAYOUT.md`, `AUTHOR_VOICE.md` y `NEXT_STEPS.md`. Cuerpo: 4.383 palabras; resumen: 190. PDF principal: 19 páginas; suplemento: 33. Autor confirmado: Alejandro Treny Ortega, Independent researcher, sin financiación externa ni conflictos de interés. El texto espera su revisión personal. No reiniciar experimentos ni realizar otra publicación/envío por retomar.

**Copia española inicial, 18-09-2026 (paginación histórica):** `MANUSCRIPT_SPANISH.md` enlaza la traducción completa de artículo y suplemento para revisión del autor, en `manuscript_es/` y `output/pdf/es/` (21 y 35 páginas). El inglés sigue siendo canónico. Los cinco comentarios posteriores del autor se han aplicado a ambas versiones; copias anteriores archivadas. Conservar la correspondencia de secciones, tablas y figuras; trasladar al inglés las correcciones que solicite el autor. No interpretar la traducción como aprobación personal del texto ni como nueva decisión científica.

**Publicación de código autorizada después:** el usuario pide «haz commit y push antes de empezar con el texto». Autoriza versionar y subir código, documentación, tablas y figuras al repositorio `aleetreny/Shape-of-Science-Robustness`. Corpus, vectores, pesos, secretos y copias completas de terceros siguen excluidos. No equivale a autorizar depósito de datos, elección de licencia ni redacción automática. Las prohibiciones históricas de commit/push quedan sustituidas para esta entrega.

## Cómo responder al usuario

- Responder siempre en español muy sencillo, con frases cortas y vocabulario cotidiano.
- Empezar por la respuesta y explicar solo lo necesario para entenderla.
- Usar una analogía breve cuando ayude: por ejemplo, comparar modelos es como fotografiar los mismos objetos con cámaras distintas.
- Evitar jerga, siglas sin explicar, fórmulas y palabras rebuscadas. Si un término es imprescindible, explicar inmediatamente qué significa con palabras normales.
- No sustituir una explicación sencilla por una lista enorme de conceptos o posibilidades. Dar una recomendación concreta, su motivo y la limitación que realmente importa.
- Dejar los detalles técnicos y las fuentes ampliadas en Markdown; la respuesta del chat debe ser breve y comprensible por sí sola.
- Distinguir claramente lo comprobado, lo recomendado y lo que todavía no sabemos. No presentar un número elegido por comodidad como el tamaño correcto para un paper.

## Voz del autor al preparar el paper

- El usuario pide expresamente que la escritura conserve su voz personal y evite un registro impersonal o prefabricado. Leer [AUTHOR_VOICE.md](AUTHOR_VOICE.md) antes de escribir; [MANUSCRIPT_BLUEPRINT.md](MANUSCRIPT_BLUEPRINT.md) fija contenido, fuentes y posición de elementos.
- La guía procede de las 50 entradas españolas del portfolio en el commit `5361e0354dd8419b4cf72089b7e8e51124830cfb`, leídas completas en su prosa. No usar las traducciones automáticas, README o documentación como muestras de escritura manual. No afirmar que se verificó forensemente la autoría de cada frase.
- Conservar el razonamiento concreto: problema, funcionamiento, decisión, resultado y límite pertinente. Adaptarlo a inglés académico claro; evitar autoelogios, tecnicismos ornamentales, conectores repetidos y párrafos intercambiables. No volver todas las frases igual de cortas ni inventar experiencias o faltas.
- No usar detectores como prueba de autoría ni prometer que nadie percibirá ayuda automática. Mantener el registro real de asistencia y las declaraciones aplicables. La revisión de estilo no cambia afirmaciones, alertas o decisiones científicas.
- La petición posterior de escribir el resto y revisar el paper **autoriza el manuscrito completo** y sustituye el alcance anterior de solo introducción/antecedentes. El borrador ya está terminado; continuar con las revisiones que pida el autor. Las declaraciones confirmadas no se vuelven a preguntar. Correspondencia, aprobación final, depósito, licencia y envío siguen pendientes.

## Cómo tomar decisiones científicas

- Si el usuario **delega explícitamente** una decisión (por ejemplo, «haz lo que consideres» o «toma esta decisión por mí»), resolverla dentro de ese alcance y justificarla después, con palabras sencillas. No pedir otra confirmación para la decisión ya delegada.
- Priorizar un estudio sólido y defendible ante la revisión científica, con **Quantitative Science Studies (QSS)** como revista objetivo inicial. Favorecer comparaciones justas, selección reproducible, controles necesarios, límites claros y una carga de trabajo viable. No prometer aceptación ni ausencia de críticas.
- Si no hay delegación explícita para una decisión científica nueva, presentar las opciones que se están valorando, sus diferencias y la recomendación, y preguntar al usuario antes de cerrarla. Las comprobaciones necesarias y las tareas ya autorizadas pueden seguir avanzando.
- La delegación es específica: no convierte todas las futuras decisiones en autónomas. Registrar el alcance delegado, la opción elegida, la evidencia, sus límites y qué sigue abierto en `DECISIONS.md`.
- Desde el 14-09-2026, el usuario ha delegado **el tamaño y reparto del corpus de la primera fase de preparación**, teniendo en cuenta representatividad, extracción, varios modelos y su MacBook Pro M5 Pro con 48 GB de RAM. Autoriza pruebas acotadas para decidirlo. Esta delegación sustituye la prohibición anterior de esas pruebas; no equivale a iniciar todos los experimentos finales.

## Cómo mantener el trabajo entre chats

Al comenzar, leer `DECISIONS.md`, `progress.md` y `task_plan.md`. Consultar `findings.md` y los documentos enlazados según la tarea.

- `DECISIONS.md`: decisiones aceptadas por el usuario, propuestas sin aceptar y preguntas pendientes. Registrar fecha, motivo y qué decisión sustituye, si corresponde.
- `progress.md`: qué se hizo, qué archivos cambiaron y el punto exacto donde continuar.
- `task_plan.md`: pasos de la tarea actual y su estado.
- `findings.md`: comprobaciones, fuentes y límites de la evidencia. Enlazar informes existentes en vez de duplicarlos.
- Actualizar estos archivos al cerrar una cuestión o terminar una sesión significativa. Distinguir decisiones aceptadas directamente por el usuario, decisiones tomadas por delegación explícita y propuestas aún sin aceptar.

## Alcance del proyecto

- La unidad principal son los **26 Fields**. Los Subfields pueden servir para organizar la selección de papers, sin convertirse por ello en la unidad principal.
- Los datos existentes no limitan el diseño: se puede proponer ampliar la extracción de OpenAlex cuando haya una razón. No fijar el tamaño de todos los Fields por el tamaño disponible del más pequeño.
- El tamaño de preparación decidido por delegación explícita es **500.000: 400.000 base general + 100.000 complemento**, según `CORPUS_PROTOCOL.md`. Las propuestas anteriores de 5.000 por Field y 200 por año están sustituidas; no reutilizarlas como protocolo.
- El usuario ha elegido **diez modelos**: SPECTER, SPECTER2, SciNCL, SciBERT, BERT, MPNet (`all-mpnet-base-v2`), MiniLM (`all-MiniLM-L6-v2`), PubMedBERT/BiomedBERT (abstract-fulltext), BioBERT y SimCSE. `ACADEMIC_MODEL_USAGE.md` reúne los antecedentes y `MODEL_SELECTION.md` identifica la selección. No volver a preguntar ocho o diez.
- El proyecto anterior, `/Users/alejandrotreny/Workspace/Mapping-Science`, es una referencia de solo lectura. Reutilizar datos y evitar descargas duplicadas.
- El 15-09-2026 el usuario pidió implementar y probar el extractor, pero **ejecutará él mismo la descarga completa desde su terminal**. Dejar el comando listo; no arrancar la extracción masiva por cuenta del asistente. Las pruebas pequeñas de funcionamiento y reanudación están autorizadas. El usuario volverá a consultar el avance; no configurar avisos automáticos sin petición.
- No mostrar ni guardar claves de API en documentos, resultados o mensajes. Si ya existe una clave autorizada, usarla de forma privada sin pedirla otra vez.

## Seguimiento autorizado, 15-09-2026

- El usuario ya inició la descarga y ahora pide supervisarla y auditar los resultados hasta que termine, dejando la siguiente fase preparada. Esta petición autoriza seguimiento automático temporal en este chat y sustituye la ausencia anterior de esa petición. No modificar los módulos `sos_download/` durante la descarga. No lanzar otra instancia ni iniciar embeddings o cerrar decisiones científicas nuevas.
- Esta supervisión ya terminó: 500.000 registros descargados y auditados el 15-09-2026. El seguimiento temporal está desactivado. La limpieza fue autorizada después, como indica la sección siguiente. No repetir la descarga original ni empezar modelos automáticamente.

## Limpieza autorizada, 15-09-2026

- El usuario pide ahora limpiar y completar el corpus, reutilizando lo descargado y permitiendo descargar más si hace falta. Se autoriza ejecutar esa preparación desde el asistente en una salida separada, conservando los originales. Esta petición sustituye las limitaciones anteriores de solo auditoría y descarga a cargo del usuario para la reposición necesaria. No iniciar embeddings finales ni elegir modelos automáticamente.

## Material preparado, 15-09-2026

- La limpieza y reposición terminaron: usar `data/corpus_clean_v1/embedding_input.parquet` y su manifiesto, después de `./prepare.sh preflight`. Son 500.000 filas comprobadas, 400.000 base y 100.000 complemento. Originales intactos y casos dudosos marcados; detalles en `CLEANING.md`.
- `EMBEDDINGS_READY.md` y `NEXT_STEPS.md` describen la continuación. No usar carpetas provisionales ni repetir la descarga. El manifiesto de limpieza conserva su estado histórico; la ejecución de modelos se registra por separado.

## Diez modelos elegidos, 15-09-2026

- «Los 10. Vamos hazlo perfecto» acepta los ocho propuestos más BioBERT y SimCSE y autoriza preparar su cálculo, fijar versiones oficiales y comprobar funcionamiento/reanudación con una prueba acotada. Sustituye la prohibición anterior de escoger esos modelos o probar sus embeddings. No añade TF-IDF ni una segunda variante de MPNet.
- El usuario acepta **uso habitual + comprobación con texto idéntico**. El 15-09-2026 aclara que quiere **un comando para lanzarlo él desde su terminal y una estimación del tiempo**. No iniciar el cálculo completo desde el asistente. Sí terminar preparación, descarga de pesos y pruebas pequeñas de funcionamiento/tiempo/reanudación.
- No mezclar los vectores SPECTER2 antiguos con los nuevos mientras su procedencia no esté identificada. Mantener intactos el corpus congelado y sus programas de preparación.
- Cuando el usuario haya iniciado el cálculo, no editar `sos_embed/`, su configuración, entorno o pesos mientras siga en marcha. La reanudación rechaza cambios para no mezclar resultados. Los análisis futuros pueden prepararse en archivos separados.
- Los 1.300 artículos de las pruebas y del control común actual son una comprobación técnica. El tamaño científico definitivo del control, las medidas y la receta principal de los cuatro BERT de palabras siguen abiertos; no tratarlos como decisiones cerradas.

## Revisión final programada, 16-09-2026

- El usuario ya inició los embeddings y pide comprobar el progreso y dejar un recordatorio para la revisión final, organización de datos y preparación de la siguiente fase. Autoriza seguimiento temporal en este chat y la auditoría/organización técnica de `POST_EMBEDDING_REVIEW.md`.
- No reiniciar, duplicar o cambiar el cálculo activo. Mantener los archivos congelados en sus rutas y organizar con catálogos/documentación o derivados separados. Las decisiones científicas que siguen abiertas se consultan antes de cerrarlas; esta petición no es una delegación general.
- Desactivar el seguimiento cuando la revisión y preparación estén entregadas, o cuando solo quede una decisión del usuario. Avisar ante finalización, un problema o una acción necesaria; no repetir avisos sin cambios útiles.

## Auditoría y preparación técnica terminadas, 17-09-2026

- Los diez modelos completos y las pruebas habitual/común han sido verificados. Informe vigente: `EMBEDDINGS_AUDIT.md`; catálogo: `DATA_CATALOG.md` y `research/embedding_final_audit_2026-09-17/catalog.json`.
- Nuevo índice separado: `data/analysis_ready_v1/metadata.parquet`. Lector en `sos_analysis/`, comprobado sobre las 18 variantes completas. No normaliza, descarta o pondera por defecto; cada salida se solicita explícitamente. No volver a descargar o calcular los modelos por continuar con el análisis.
- MiniLM recorta el texto en el 49,58% de los artículos y MPNet en el 20,16%; conservar ese diagnóstico por área/período. Los 1.300 artículos de control siguen siendo técnicos.
- El seguimiento temporal está desactivado (PAUSED), comprobado el 17-09. No reactivarlo sin una nueva petición. Consultar `ANALYSIS_PROPOSAL.md` y preguntar por las decisiones científicas pendientes antes de cerrarlas. Forma general + vecinos es una propuesta, no una decisión aceptada; tampoco se aprobaron todavía normalización, receta principal de los cuatro BERT, tamaño final del control o reglas de estabilidad.
- Mantener intactos corpus, archivos de vectores, configuración, pesos y programas congelados; los análisis irán en salidas separadas. No modificar el manifiesto histórico de limpieza para reflejar el estado de los modelos.

## Comparación científica delegada, 17-09-2026

El usuario autoriza continuar con la comparación de la forma y después de los vecinos, delegando las cuestiones pendientes de esta fase con criterio de solidez para QSS. Autoriza investigar medidas más robustas, ejecutar las comparaciones, inspeccionar resultados y preparar su presentación. Pide diagnosticar el recorte de MiniLM y corregir/recalcular si procede. Esta petición sustituye las restricciones previas de solo preparación y de esperar nuevas respuestas para esas decisiones. Se decidirán y documentarán medidas, recetas, controles y presupuesto antes de inspeccionar acuerdos. Conservar las salidas congeladas; cualquier corrección o variante nueva irá en una salida separada. No implica publicación, envío a revista ni cambios al TFM.

- Protocolo vigente: `ANALYSIS_PROTOCOL.md`; configuración congelada `config/analysis_v1.json` y ajuste de precisión `config/neighbors_v1.json`. Media para los cuatro BERT, CKA corregida como principal, Procrustes/RSA como comprobaciones; texto común de 52.000, MiniLM 512 separado y controles de calidad/receta/tamaño.
- No editar los módulos de análisis que figuran en manifiestos mientras calculan, ni mezclar salidas de versiones distintas. Los programas guardan copias y huellas; para cambios científicos posteriores se necesita una versión nueva.
- Se conservan el MiniLM oficial de 256 como principal y su variante de 512 como sensibilidad. No hay fallo de límite en el código original. La comparación de vecinos usa todos los candidatos de cada celda y añade un control separado de 2.048 candidatos iguales; no confundirlo con el análisis completo.

## Comparación terminada y cierre de la delegación, 17-09-2026

- Entrega vigente: `ANALYSIS_RESULTS.md`, `reports/analysis_v1/final/`, `METHODS_ANALYSIS.md` y `PAPER_OUTLINE.md`. Forma, vecinos y todos los controles autorizados están terminados y comprobados. No quedan procesos activos ni decisiones necesarias del usuario para cerrar esta fase.
- MiniLM 256 sigue como principal y 512 como control separado. Se verificó que el límite original no era un error. El control común científico usa 52.000, no los 1.300 de la prueba técnica. Las recetas, normalización y medidas se fijaron en el protocolo dentro de la delegación; no volver a preguntarlas por recuperar un estado histórico.
- Resultados principales: más acuerdo entre áreas que dentro; vecinos equilibrados 30,3% y 31,9% con candidatos iguales. Forma y vecinos sí se asocian fuertemente. No convertir CKA/correlaciones en porcentajes de ciencia correcta ni elegir un modelo ganador por consenso.
- Mantener las 50 alertas de estabilidad de 5.850 comparaciones; no cambiar umbrales ni declararlas resueltas. No se amplía el corpus ahora. Las selecciones son variaciones dentro de un corpus fijo, no intervalos poblacionales; los 45 pares de modelos no son independientes.
- Los controles adicionales de centros y grupos aleatorios son posteriores al resultado inicial y deben describirse así. Las etiquetas OpenAlex no son verdad temática externa. No afirmar prioridad absoluta, representatividad mundial o convergencia histórica causal.
- Conservar las rutas, datos originales y copias/huellas de los programas científicos en `data/analysis_v1/`. No editar una implementación congelada y reanudar como si fuera la misma versión. El exportador puede reconstruir la entrega con el comando de `NEXT_STEPS.md`, sin repetir inferencia ni vecinos.
- Continuación: redacción del manuscrito y contraste con los antecedentes más próximos cuando se solicite. La delegación de esta fase no es autorización general para nuevas extracciones, modelos, publicación o envío. Las automatizaciones previas permanecen pausadas; no reactivarlas sin petición.

## Checklist adicional autorizada, 17-09-2026

- El usuario pide ejecutar seis puntos y delega cómo encajarlos: título/resumen/ambos, efecto de modelo frente a entrada, receta principal, tiempo, modelo por disciplina y familias. Esta petición amplía la fase anterior. No es autorización para recalcular automáticamente todas las entradas sobre 500.000 ni para publicar.
- Protocolo fijado: `CHECKLIST_PROTOCOL.md` y `config/checklist_v1.json`. Piloto de 26.000, 200 por área/período; análisis por área con 1.000 candidatos iguales. Se confirma mean como receta principal de los cuatro BERT, conservando CLS/SEP como controles y declarando que esta confirmación es posterior a las primeras sensibilidades.
- Nuevas salidas en `data/checklist_v1/`. Los programas anteriores, corpus y vectores originales se conservan. No editar `sos_followup/input_embeddings.py`, `input_analysis.py`, `pilot_statistics.py`, configuración o entornos mientras sus cálculos están activos.
- Tiempo, disciplina y familias están calculados en `existing_v2/`. El intento parcial `existing/` se conserva; en SEP al omitir SimCSE los coeficientes no son identificables y se declaran ausentes.
- La cola `research/checklist_2026-09-17/run_inputs.py` y sus ejecutores `finish_pilot.py`/`finish_recipes.py` terminaron. Sus registros se conservan; no volver a iniciarlos por retomar el proyecto. No reactivar automatizaciones antiguas.
- Antes de inspeccionar acuerdos de entrada se añadió el cruce de recetas: `config/checklist_input_recipes_v1.json` y `input_recipe_control.py`. El cruce CLS/SEP está terminado y auditado, reutilizando vectores guardados. Mean sigue siendo principal.

## Checklist terminada y cierre de su delegación, 17-09-2026

- Entrega vigente: `CHECKLIST_RESULTS.md`, `reports/checklist_v1/final/`, `METHODS_CHECKLIST.md`. Se conserva también `ANALYSIS_RESULTS.md`: la ampliación no invalida los resultados anteriores. Seis puntos completados, 33 tablas nuevas y siete figuras nuevas; auditoría completa y programas/huellas guardados.
- Tres entradas en los mismos 26.000 IDs: 200 por área/período, 1.000 por área al reunir fechas. Título + resumen reutilizado exactamente; no repetir los 500.000. Media de posiciones no rellenadas, incluidos símbolos especiales, confirmada como principal de los cuatro BERT; CLS/SEP son controles, sin elegir la receta que maximiza acuerdo.
- Quitar el resumen puede cambiar tanto como cambiar el modelo; las medias ocultan diferencias entre modelos y el orden cambia con medida/receta. Quitar solo el título cambia menos, pero también modifica vecinos. Es una comparación de usos prácticos, no una separación causal pura de arquitectura y contenido.
- Mantener 31 alertas de amplitud entre 520 contrastes modelo–área–entrada, en 17 áreas. Los 52 promedios de área pasan la criba de forma. Esa criba no demuestra estabilidad de vecinos ni precisión poblacional. No recalcular ahora título/resumen sobre 500.000; diferencias pequeñas que resulten esenciales exigirían una comprobación dirigida. Las 50 alertas anteriores siguen vigentes por separado.
- Tiempo: aumento medio pequeño de forma; el signo de vecinos cambia con el número de candidatos. Priorizar 2.048 candidatos iguales para comparar fechas y conservar la comprobación posterior con consultas idénticas. No afirmar convergencia histórica causal.
- Medicina tiene menor forma con la receta principal, pero no el menor acuerdo de vecinos. BioBERT/PubMedBERT se parecen entre sí; la diferencia con Energía persiste sin ambos. Composición y familias ofrecen asociaciones, no una causa probada. Las familias de entrenamiento son grupos amplios definidos por fuentes; su explicación depende de la receta y no forman tres bloques cerrados.
- Siguiente trabajo, cuando se solicite: redacción del manuscrito con `PAPER_OUTLINE.md` y antecedentes próximos. No hay una decisión necesaria del usuario para cerrar esta checklist. Este cierre no autoriza nuevas extracciones, modelos, publicación o envío. Automatizaciones pausadas; originales y programas científicos congelados intactos.

## Cierre experimental ampliado solicitado después, 17-09-2026

El nuevo objetivo activo está íntegro en `ROBUSTNESS_SCOPE.md` (R01–R12). Autoriza ampliar a 52.000 con el mismo diseño, repetir entradas/recetas/CKA/kNN, añadir Subfields y estabilidad por artículo, profundizar tiempo/Medicina/familias, revisar medidas/controles/alertas/literatura y congelar una entrega reproducible antes de redactar. Sustituye la decisión anterior de detener entradas en 26.000. Se permite la inferencia necesaria de los artículos nuevos; reutilizar los anteriores. No es permiso para nuevos modelos, extracción masiva, publicación o envío. Las decisiones necesarias para cumplir estos puntos se justifican y registran.

Programas nuevos `sos_deep/`, datos `data/robustness_v2/`, evidencia `research/robustness_2026-09-17/`. Mantener originales y programas congelados; no editar una versión mientras calcula. No declarar la meta completa sin evidencia para R01–R12. Los Subfields añaden un nivel de análisis, no eliminan la unidad Field ni cambian el corpus.

## Cierre ampliado terminado y delegación cerrada, 17-09-2026

- Entrega vigente: `ROBUSTNESS_RESULTS.md`, `METHODS_ROBUSTNESS.md`, `SAMPLING_STABILITY.md`, `CONCLUSION_CONTROLS.md` y `reports/robustness_v2/final/`. R01–R12 comprobados: 15 componentes auditados, 50 tablas y siete figuras inspeccionadas. No quedan cálculos activos.
- Las tres entradas usan 52.000 artículos, 400 por área/período, incluyendo los 26.000 del piloto. No confundir esta selección con el control de fragmento común de otros 52.000. Se reutilizaron exactamente dos tercios de las 1.560.000 combinaciones modelo–artículo–entrada.
- Con 100 selecciones comparables, alertas de entrada 72/520 en 26k → 5/520 en 52k. La comparación histórica de 20 reproduce 31 → 4; conservar ambas y las 31 claves. No mezclar esos conteos con las 50 alertas originales o las de Subfields. Sin alerta no significa contraste distinto de cero ni precisión poblacional.
- Mean permanece principal para los cuatro BERT de palabras; `POOLING.md` define exactamente mean/CLS/SEP. El cruce completo de recetas/entradas está calculado. El remuestreo de 100 selecciones se aplica al contraste principal, no a todas las recetas y vecinos.
- No hay descenso universal de acuerdo al pasar de Field a Subfield. Con consultas/candidatos/fechas iguales, k25 baja en 127/217 y sube en 90. Los 500.000 tienen resultados locales; solo 10.850 consultas tienen diez selecciones controladas de candidatos. Grupos diminutos y alertas siguen visibles.
- Las comprobaciones de Medicina, tiempo y familias son completas dentro del diseño y tienen límites causales. No identificar una causa única de Medicina ni separar causalmente entrenamiento/arquitectura con diez modelos. CKA corregida y vecinos k25 siguen principales; no añadir morfología sin nueva pregunta autorizada.
- Rutas vigentes: `control_review_v2` y `structural_review_v3` bajo `data/robustness_v2/`. Las versiones anteriores se conservan como historial; no mezclar sus resúmenes. Fuentes/configuraciones y resultados científicos congelados, con huellas y copias; cualquier cambio científico necesita versión nueva.
- Literatura actualizada y esquema revisado en `research/robustness_2026-09-17/RELATED_WORK_UPDATE.md` y `PAPER_OUTLINE.md`. La combinación de forma/vecinos/familias ya tiene antecedentes; no afirmar novedad absoluta. No ampliar entradas automáticamente a 500.000.
- Continuación: redactar cuando se solicite. Este cierre no autoriza otras extracciones/modelos, publicación, envío ni distribución de datos. Las automatizaciones previas permanecen pausadas.

## Revisión previa al manuscrito y atlas terminados, 17-09-2026

- Nueva petición del usuario: revisar el estudio, literatura, referencias y presentación antes de redactar; profundizar en artículos, Subfields y relaciones concretas. Se autorizaron derivados separados y mejoras documentales, sin inferencia, extracción masiva, publicación ni envío.
- Entrega: `PREPAPER_REVIEW.md`, `CASE_ATLAS.md`, `reports/prepaper_v1/`, biblioteca canónica `references/references.bib` y guía `docs/INDEX.md`. El cierre anterior y sus documentos sellados están conservados en `research/prepaper_2026-09-17/baseline_documents/`.
- Atlas exploratorio: 217 Subfields a tamaño 256; persistencia en 183 bajo 27 condiciones; 10.850 consultas con diez selecciones; 531.650 relaciones dirigidas con ambos extremos siempre elegibles; 23.436 parejas de centros. Reglas fijadas antes de leer los títulos, después de los resultados generales. No presentarlo como preregistro de todo el estudio.
- Los extremos incluyen un libro de historia clasificado en Física, un texto de infección bacteriana en Política y un Announcement. Comprobados contra OpenAlex original. No son errores de alineamiento; no corregir a mano ni borrar ejemplos. El diagnóstico de 82 títulos genéricos cambia muy poco el promedio al excluir cinco consultas, pero no mide la prevalencia de errores temáticos ni limpia los candidatos.
- La búsqueda emparejada de Field/Subfield incluye las 50 consultas del mismo Subfield en ambos grupos de 256. Es un diseño condicionado; no describir la muestra amplia como 256 candidatos libres del Field. Los centros del atlas no tienen control adicional de receta.
- Biblioteca: 45 entradas verificadas, versiones editoriales preferidas y errores de autores/páginas corregidos. Caspari, Singh 2022, Bascur 2025 y SemCSE-Multi 2026 son antecedentes próximos. No afirmar prioridad absoluta, precisión temática por consenso ni explicación causal de Medicina/familias.
- Preparado para iniciar redacción cuando se pida. Antes del envío faltan manuscrito revisado por autores, depósito persistente de material esencial y declaraciones reales. Las normas QSS se consultaron desde su índice porque el acceso directo dio 403; volver a comprobarlas antes de enviar. No hay licencia general elegida ni publicación de datos autorizada.
- Programas anteriores, corpus y vectores siguen intactos. `sos_review/case_atlas.py` y su configuración tienen versión/copia congelada; cambios científicos requieren otra salida. El exportador de presentación es separado. No reactivar automatizaciones pausadas.


## Piloto de morfología autorizado, 18-09-2026

El usuario pide explorar propiedades concretas de forma con medidas alternativas y controles de calidad/estabilidad, y conocer los resultados antes del manuscrito. Autoriza las decisiones necesarias y el cálculo derivado con vectores existentes. Sustituye para esta fase la prohibición anterior de añadir morfología. Mantener originales y cierres previos; no reiniciar inferencia/extracción ni publicar/redactar por extensión. Consultar el encabezado de `task_plan.md` y la nueva entrada de `DECISIONS.md`. No buscar diferencias llamativas a costa de cambiar criterios después de los resultados.

## Piloto de morfología terminado y delegación cerrada, 18-09-2026

- Entrega: `MORPHOLOGY_RESULTS.md`, `METHODS_MORPHOLOGY.md`, `reports/morphology_pilot_v1/` y auditoría en `research/morphology_2026-09-18/closure_audit.json`. Diez modelos, 52.000 artículos principales, 16.884 conjuntos de medidas, 20 tablas y cinco figuras. No hay cálculos activos ni inferencia nueva.
- Apertura angular y dimensión efectiva lineal (PR) son descripciones aprovechables con controles; no son diversidad semántica, isotropía o número de temas. El orden de áreas es más estable al cambiar artículos que al cambiar encoder. La inversión ilustrativa Artes/Medicina se eligió después de los resultados, no es una hipótesis confirmatoria previa.
- Mantener cuatro alertas de PR en 260 casos con veinte medias muestras y 51 de conexión en cinco selecciones de igual tamaño. Son distintas de las alertas anteriores del estudio. Cinco selecciones satisfactorias de PR no borran las cuatro alertas internas ni demuestran precisión poblacional.
- Conexión no queda validada como fragmentación general: nubes alargadas, puntos extremos, tamaño y regla de vecinos alteran la lectura. La comprobación de proporción de vecinos se añadió durante la ejecución y está declarada; no reescribirla como protocolo inicial.
- Receta y centrado pueden cambiar conclusiones. Entropía/D80 son alternativas del mismo espectro, no validación temática independiente. Referencias gaussianas conservan momentos solo en expectativa antes de normalizar; no son controles perfectos ni pruebas estadísticas.
- Protocolo, configuración y fuentes científicas de `sos_morphology/` están congelados por manifiestos en `data/morphology_pilot_v1/`; usar una versión nueva para cambios científicos. El exportador de presentación está separado. Corpus, vectores y programas anteriores permanecen intactos.
- Se recomienda una ampliación breve del paper y controles en suplemento; `PAPER_OUTLINE.md` es una propuesta. Biblioteca actual: 54 entradas, cinco avisos documentados. No se ha redactado el manuscrito ni publicado este piloto. La petición previa de commit/push ya se cumplió en `44c9410`; no tratar esta ampliación como subida automática. No reactivar automatizaciones.

## Resumen final de parejas aceptado y terminado, 18-09-2026

- El usuario acepta el último resumen de las 325 parejas y después hablar de la organización del manuscrito. Entrega: `FIELD_PAIR_RESULTS.md`, `METHODS_FIELD_PAIRS.md`, doce tablas/dos figuras en `reports/field_pair_summary_v1/`, auditoría en `research/field_pair_summary_2026-09-18/closure_audit.json`. Sin nuevos embeddings, medidas o extracción.
- Reglas fijadas antes de los nuevos recuentos, con conocimiento del piloto: `FIELD_PAIR_PROTOCOL.md` y `config/field_pairs_v1.json`. Apertura: 42 acuerdos de diez / 262 contradicciones persistentes / 21 sin conclusión común; PR: 54 / 221 / 50. Contradicción requiere al menos dos modelos con signos opuestos persistentes; no significa diez modelos en desacuerdo.
- Persistencia sobre principal + 20 medias muestras + 5 selecciones del mismo corpus. No son intervalos poblacionales. A 5% relativo simétrico quedan 96/177 contradicciones; a 10%, 19/126. No esconder magnitudes pequeñas ni declarar un corte universal de relevancia. Todos los denominadores siguen en 325.
- Alternativas conjuntas mantienen los mismos modelos testigo en 225/196 contradicciones. Las alternativas espectrales solo tienen tres condiciones guardadas; las angulares tienen 26. Los seis modelos de similitud mantienen 231/160; menos modelos tienen menos oportunidades de oposición. No inferir causalidad de entrenamiento.
- Controles puntuales sin 25 repeticiones propias. Centrado global conserva los mismos testigos en 145/262 aperturas y 218/221 PR; no describir apertura como propiedad independiente del procesamiento. Consenso no valida temas ni cuenta conceptos. Alertas previas y etiquetas erróneas siguen vigentes.
- Fuentes del nuevo `sos_pair_summary/` congeladas por manifiesto en `data/field_pair_summary_v1/`; presentación separada. Cierre previo intacto y 18 documentos anteriores preservados en `baseline_documents/`. No editar reglas congeladas y reanudar como misma versión.
- La ampliación experimental acordada está cerrada. Continuación: hablar con el usuario de `PAPER_OUTLINE.md` con toda la evidencia. No redactar, publicar, abrir nuevas preguntas o reactivar automatizaciones por extensión.
## Revisión de estructura de QSS terminada, 18-09-2026

- El usuario solicita estudiar muchos artículos de QSS y proponer cómo organizar nuestro trabajo. Entrega: `QSS_STRUCTURE_REVIEW.md`, `PAPER_OUTLINE.md` y `research/qss_structure_2026-09-18/`.
- Marco Crossref: 465 registros. Selección dirigida de 34 trabajos; lectura estructural de 33, once con lectura focal adicional, y uno de acceso parcial. No afirmar lectura de todos los artículos de QSS ni de todos los párrafos/suplementos. Las versiones consultadas y sus límites están en la matriz.
- La guía oficial se leyó mediante índice de rastreo antiguo tras un 403 directo. Distinguir normas consultadas, prácticas observadas y recomendación propia. No prometer una estructura exigida ni aceptación editorial.
- Se propone un único paper, tres preguntas, seis secciones, cuatro figuras y dos tablas principales; geometría como cuarto bloque y tiempo/Medicina/familias como apoyo. **Es propuesta de presentación pendiente de conversar**, no decisión aceptada ni redacción autorizada.
- Mantener todos los límites de los cierres anteriores. El resumen de las 325 parejas y los controles científicos siguen intactos. No nuevos cálculos, inferencia, extracción ni automatizaciones.
- Biblioteca de la revisión: 34 entradas en una colección separada; biblioteca canónica conserva 54. Hay solapamientos; no sumarlas sin deduplicar. Textos completos de terceros solo en `data/`, fuera de Git. No se publica automáticamente esta entrega.

## Maqueta del manuscrito autorizada, 18-09-2026

- Petición directa: generar tablas/gráficas, documento apropiado para QSS y estructura renderizada. Se autoriza esta presentación, no nuevos experimentos, redacción íntegra, depósito, licencia, publicación o envío.
- Fuentes editables en `manuscript/`; dos PDF en `output/pdf/`; guía `MANUSCRIPT_LAYOUT.md`. Compilar con `./manuscript/build.sh` no ejecuta inferencia ni análisis científicos. Tectonic local en `data/manuscript_layout_v1/toolchain/`, excluido de Git.
- Las tablas de suplemento son grupos: resumen tipográfico y CSV completos. Las 14 figuras conservan los datos guardados y sus resúmenes descriptivos, con copias PDF/SVG/PNG/TIFF. Figura S10 combina las dos propiedades en los triángulos de una matriz, sin perder parejas.
- LaTeX `article` es una maqueta propia. No se encontró plantilla oficial específica; la guía QSS indexada admite formato flexible, pero es antigua y hay que revalidarla antes del envío. No rellenar autoría/declaraciones por suposición.
- Modificar los exportadores de presentación no autoriza alterar medidas, criterios o salidas científicas. Las ampliaciones anteriores y la biblioteca canónica permanecen intactas. La petición histórica de commit/push ya se cumplió; no hay nueva publicación automática.

## Primeros bloques redactados, 18-09-2026

- El usuario pide introducción y antecedentes/preguntas, con su voz y sin alargar el paper. Primer borrador en inglés: 367 y 627 palabras de prosa, sin contar citas/títulos. Los párrafos del plano son una guía, no un molde de longitud fija.
- Se conserva la distinción entre acuerdo, estabilidad y validez temática; RQ3 sigue siendo una ampliación exploratoria. No añadir una prioridad absoluta, un modelo ganador o una muestra mundial a la prosa posterior.
- Ocho antecedentes citados en la apertura y 17 referencias únicas contando la tabla de modelos. Biblioteca canónica intacta; `manuscript/context_references.bib` contiene una entrada de la revisión QSS ya verificada. El único ajuste de `manuscript/references.bib` es escapar tipográficamente un guion largo para que se renderice.
- Revisión de afirmaciones y continuidad en `research/manuscript_opening_2026-09-18/`; maqueta anterior archivada. PDF/ZIP actualizados, sin nuevos experimentos, commit/push ni publicación. El texto sigue sujeto a revisión del autor.

## Manuscrito completo y revisión, 18-09-2026

- Entrega: `manuscript/main.tex`, `supplement.tex`, `output/pdf/` y paquete editable. Cierre en `research/manuscript_full_2026-09-18/`; versiones anteriores conservadas.
- Las seis secciones principales y métodos suplementarios están escritas. 26 referencias únicas entre ambos documentos; biblioteca científica canónica intacta. No quedaron bloques «Writing plan» en los documentos renderizados.
- Se revisaron 14 figuras y 19 grupos de tablas. Cambios de presentación: escala CKA común, puntos de búsqueda por dirección del cambio, operaciones de quitar texto explícitas, tabla de modelos compacta, nombres legibles y paginación corregida. Los datos y criterios científicos no cambiaron.
- Autor confirmó nombre, trabajo independiente, ninguna financiación y ningún conflicto. Se usa «no external funding» y se declara la ayuda de Codex. No inventar correo, institución, ORCID o revisión humana ya realizada.
- No hay permiso nuevo para publicar, depositar datos o enviar. La lectura personal del autor, correspondencia, normas finales, licencia y depósito son los pasos pendientes. Mantener controles y advertencias; no reinterpretar la revisión tipográfica como validación temática externa.
