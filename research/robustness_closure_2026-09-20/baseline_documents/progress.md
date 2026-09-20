# Registro de trabajo

**Punto vigente, 20-09-2026:** V2 elegida y reescritura clara entregada en inglés y español. Ver [MANUSCRIPT_CLARITY.md](MANUSCRIPT_CLARITY.md) y [NEXT_STEPS.md](NEXT_STEPS.md). Los bloques fechados que siguen son históricos; no reiniciar los cálculos que describían en marcha.

## 2026-09-14 — Inventario y recuentos locales

- Localizada la copia completa del TFM en `/Users/alejandrotreny/Workspace/Mapping-Science`.
- Creado `INVENTORY.md`; verificados corpus, shards SPECTER2, IDs e índices en lectura.
- Creados `FIELD_COUNTS.csv` y `FIELD_SAMPLING.md`; confirmados 26 Fields.
- Se propusieron 5.000 papers por Field y 200 por año. **El usuario no lo aceptó; pide una justificación mejor y permite plantear más datos.**

## 2026-09-14 — Preferencias y continuidad

- Creado `AGENTS.md`: responder siempre muy sencillo y mantener este registro entre chats.
- Creados `DECISIONS.md`, `task_plan.md` y `findings.md` con separación de decisiones y propuestas.
- Se usan las guías planning-with-files y paper-lookup para organización y búsquedas.
- Revisados tres estudios comparables y fuentes sobre cómo justificar tamaños. Referencias y recomendación sencilla en `FIELD_SAMPLING.md`.

## 2026-09-14 — Revisión del reparto y OpenAlex

- Reemplazada la recomendación de 5.000 por Field; su versión histórica está en `research/FIELD_SAMPLING_initial_proposal.md`. El usuario todavía no ha aceptado el nuevo diseño.
- Propuesta actual: base proporcional por área y año, complementos donde se necesite precisión por área y mismos papers para todos los modelos. El número final requiere justificación, no se fijó otro número por comodidad.
- Creado `OPENALEX_COUNTS.md`: 61.061.439 candidatos clasificados con filtros básicos, o 70.050.675 con congresos, antes de limpieza, en el corpus predeterminado. Veterinaria: 101.802 candidatos básicos.
- Guardadas respuestas API con fecha y filtros, sin la clave, en `research/openalex_counts_2026-09-14/`. Exportados `OPENALEX_FIELD_COUNTS.csv` y `OPENALEX_FIELD_YEAR_COUNTS.csv`; reconciliadas las 650 celdas anuales.
- Se distinguió el catálogo principal de la ampliación opcional actual de OpenAlex. Esta última contiene 474.716.562 trabajos totales y 82.760.353 candidatos clasificados con congresos y filtros básicos; queda pendiente decidir si entra. Hay 37 respuestas guardadas y columnas ampliadas por Field; las 650 celdas anuales siguen siendo del principal.
- Actualizados brief y preguntas abiertas para recoger la decisión ya tomada sobre los 26 Fields. `DECISIONS.md` distingue decisiones del usuario y nuevas propuestas.
- Verificado: ambos repositorios anteriores siguen limpios en Git; enlaces de los informes válidos; clave ausente de los archivos del proyecto. No se creó código experimental ni se descargó un nuevo corpus.

## Para continuar

**Comparación científica en marcha, 17-09-2026.** El usuario delegó las decisiones y autorizó forma, vecinos y diagnóstico/corrección de MiniLM. Leer `ANALYSIS_PROTOCOL.md` y `config/analysis_v1.json`; no volver a preguntar las decisiones delegadas.

Salidas nuevas en `data/analysis_v1/`, evidencia en `research/analysis_2026-09-17/`. MiniLM 512 usa un programa separado; el resultado de 256 permanece principal. La preparación del control de texto común de 52.000 está en curso. La primera comparación de forma se ha lanzado tras siete pruebas matemáticas aprobadas. No alterar código/configuración de una salida activa; hay huellas y bloqueo de reanudación.

Los dos recordatorios antiguos siguen pausados. No repetir descarga ni los diez modelos originales. No tratar el control técnico antiguo de 1.300 como el nuevo control científico.

## 2026-09-14 — Decisión delegada de preparación

- Actualizado `AGENTS.md` con la regla pedida: decidir por solidez científica y recursos solo cuando el usuario lo delegue; justificar después. QSS es el objetivo inicial, sin prometer aceptación.
- Creado `CORPUS_PROTOCOL.md`, decisión de 500.000, filtros, reparto automático, criterios de comparación, costes y entregables. `FIELD_SAMPLING.md` es ahora un resumen de esta decisión; la propuesta previa queda en `research/FIELD_SAMPLING_review_proposal.md`.
- Creada carpeta `research/feasibility_2026-09-14/` con scripts, versiones, resultados y `RESULTS.md`. Pruebas de API, dos modelos, tamaño en cuatro casos y memoria/búsqueda sobre 500.000 vectores.
- Las cuatro cribas de tamaño pasaron. Se mantuvo la distinción entre apoyo preliminar y demostración de estabilidad de todo el estudio; los modelos finales aún no están decididos.
- Guardadas proyecciones de reparto por Field y por Field/período, no cuotas definitivas. El total decidido sí es 500.000; las cuotas se calculan después de limpiar la base general.
- Actualizados `DECISIONS.md`, brief, preguntas, inventario y recuentos para que apunten al protocolo vigente. Entorno/descargas de modelos/textos de prueba excluidos de Git mediante `.gitignore`. Sin commits ni push.

## 2026-09-15 — Consulta sobre pérdida de internet

- Verificado que todavía no existe el extractor final; los scripts actuales son pruebas de viabilidad.
- Anotado el requisito técnico de conservar el progreso y reanudar sin pérdidas ni duplicados, con prueba de interrupción antes de la descarga completa. No se inició ninguna descarga.

## 2026-09-15 — Programa preparado para que lo ejecute el usuario

- La última instrucción sustituye el arranque desde el asistente: el usuario ejecutará la descarga completa y volverá a consultar el avance. No hay seguimiento automático.
- Creados `download.sh`, `sos_download/`, `config/corpus.json`, `config/smoke.json`, `requirements.txt`, entorno `.venv`, pruebas y `DOWNLOAD.md`. La clave ya existente se lee de forma privada; no se copió. No se modificó `.zshrc`; el comando no depende de `pyenv`.
- Preparado `data/cache/legacy_index.sqlite` con 2.378.036 IDs y huellas del texto antiguo, unos 213 MiB. Se conservó el TFM en lectura.
- Implementados páginas comprimidas con guardado seguro, estado y selección por bloque, limpieza común, base aleatoria, complemento automático, bloqueo de ejecuciones simultáneas, consulta de avance y exportación final. Sin embeddings.
- Pasan 21 pruebas offline, incluido cierre brusco de un proceso, pérdida de conexión en un servidor local y reanudación sin modificar los IDs. Revisión independiente terminada; se corrigieron dos casos de agotamiento/contador y se reforzó la comprobación de páginas interiores.
- Prueba real final en `data/smoke_verified_2026-09-15/`: 124 IDs únicos, 120 base y 4 complemento, seis páginas, pausa y reinicio reales. Todos los valores de la tabla coinciden con las respuestas guardadas. La primera prueba está en `data/smoke_2026-09-15/`; ninguna se incorpora a producción.
- Evidencia: `research/download_validation_2026-09-15/RESULTS.md`, `verification.json`, `tests.txt` y `verify.py`. Programa de la prueba final y módulos entregados coinciden. Sin clave en los artefactos inspeccionados; Git del proyecto anterior sigue limpio.
- Punto exacto: **el usuario puede ejecutar `./download.sh`** desde este repositorio. Para ver el avance: `./download.sh status`. Ctrl+C pausa y el mismo comando reanuda. La comprobación final de esta sesión indica que `data/corpus_500k/state.sqlite` todavía no existe: producción no iniciada. Sin commits ni push.

## 2026-09-15 — Supervisión y auditoría solicitadas tras el arranque

- Proceso de descarga del usuario confirmado en marcha, PID 4569, iniciado a las 10:13:34 UTC. Primera revisión: 397.730 base, 4.580 páginas. A las 12:03:37 UTC termina el bloque que completa los 400.000 de la base; se inicia el complemento.
- Configuración y huellas de todos los módulos coinciden con el arranque. 26 Fields, cinco períodos, margen de unos 296 GiB de disco. Fallos temporales registrados y recuperados, sin pausa por error en el momento de la comprobación.
- Autorizado y creado seguimiento temporal del hilo, ID `auditar-descarga-openalex`. Ahora se audita en lectura; no hay cambios del extractor ni segunda descarga.
- Siguiente paso actual: auditoría detallada de los bloques guardados, complemento y tabla final. No usar el antiguo estado “producción sin iniciar” como estado actual.

### Auditoría de contenido mientras termina el complemento

- Auditor principal en `scripts/audit_corpus.py`; log `data/corpus_audit.log`, progreso `data/corpus_audit/progress.json`, bloqueo `data/corpus_audit/audit.lock`. Solo lectura de producción y cache separado.
- Auditor adicional de idioma en `scripts/audit_language.py --watch`, entorno `.venv-audit`; log `data/corpus_language_audit.log`, resultados `language_summary.json` y `language_review_candidates.csv`. No confundirlo con los embeddings del experimento: es una comprobación de calidad que no cambia el corpus.
- Confirmados textos en otros idiomas, algunos avisos de retirada y contenido de páginas de revistas/errores DOI almacenado como abstract. Se están cuantificando y marcando. `AUDIT.md` es provisional; no dar por cerrado el material para modelos sin resolver las decisiones de limpieza.

### Estado intermedio y reservas

- A las 12:26 UTC: 483.717 seleccionados, descarga activa. Auditoría y detector de idioma continúan en paralelo con bloqueos separados. No se han identificado discrepancias entre registros guardados y respuestas originales.
- El último bloque aleatorio de la base contiene 6.531 candidatos válidos según las reglas actuales que no están en la base seleccionada; 6.419 tienen primera etiqueta de idioma inglés en el detector. CSV e informe en `available_global_reserve.csv` y `reserve_summary.json`. Son reservas posibles, no reemplazos ya aprobados.
- Identificados mensajes de error DOI y descripciones genéricas de revistas/bibliotecas como abstracts. Script de diagnóstico `scripts/audit_content_flags.py`, sin cambios del corpus. Hay que repetirlo al acabar para cerrar el recuento final.
- Preparado script de figuras `scripts/audit_figures.py`, a ejecutar cuando ambas auditorías lleguen a 500.000. Entorno y bibliotecas diagnósticas fijados en `requirements-audit.txt`; entorno del extractor intacto.

## 2026-09-15 — Descarga y auditoría completas

- Descarga del usuario terminada a las 12:30:35 UTC, unas 2 h 17 min desde el arranque. 6.138 páginas y 613.800 candidatos recibidos. Los 22 fallos temporales se recuperaron. 400.000 base + 100.000 complemento; 80 celdas reforzadas, ninguna agotada.
- Auditoría completa a las 12:30:55 UTC: todas las páginas, todos los registros contra sus respuestas originales, selección reproducida, descartes reproducidos, reparto independiente y todas las filas de Parquet. Sin discrepancias ni IDs repetidos. 26 Fields y 130 celdas con mínimo 2.163; 252 Subfields y 4.477 temas.
- Idioma comprobado en los 500.000 y alineado por ID, orden y huella: 8.544 alertas de primera etiqueta fuera del inglés, 5.122 con puntuación ≥0,9. No se han convertido las puntuaciones en umbrales de descarte aprobados.
- 166 alertas por contenido de páginas/catálogos; 12 posibles avisos por título; 80 grupos de título+abstract exactos repetidos (173 registros) y siete de DOI (18 registros). Ver `AUDIT.md`, `readiness.json` y CSV; hay solapamientos.
- 27.562 IDs del TFM presentes; 22.118 textos exactos coincidentes. Sus 22.118 vectores se localizaron en los 119 shards, se contrastaron los IDs de los metadatos y se comprobaron todos numéricamente: finitos y no nulos. No se copiaron ni recalcularon. Procedencia exacta del modelo todavía pendiente.
- Creados `AUDIT.md`, `NEXT_STEPS.md`, scripts de auditoría, `requirements-audit.txt`, recuentos, listas de revisión, reservas, manifiesto de huellas, índice de vectores candidatos y figuras. Evidencia en `research/corpus_audit_2026-09-15/`. Los originales y `sos_download/` siguen intactos. El proyecto antiguo sigue limpio según Git.
- Estado final: material original descargado y auditado, listo para acordar la limpieza. No está aprobado todavía para los experimentos finales. Sin commits ni push. Se desactiva el seguimiento temporal porque la tarea de supervisión ha terminado.

## 2026-09-15 — Limpieza y reposición autorizadas

- El usuario pide limpiar, aprovechar las páginas guardadas y ampliar solo si hace falta. Se prepara una salida separada; no se arranca ningún modelo de embeddings.
- Pregunta pendiente sobre idioma dudoso: recomendación conservar y marcar casos ambiguos, excluir los ajenos al inglés con evidencia clara. Preparación técnica en curso.

### Ampliación de la limpieza antes de la tabla final

- Revisados los 286 grupos de abstract idéntico del original. Se descubrieron más plantillas de páginas/avisos/recursos, además de las seis iniciales, y casos de resumen asignado al título equivocado.
- Primer recorrido pausado y archivado en `data/corpus_clean_v1_initial_pass`; no se declaró preparado. Se reutiliza su diagnóstico de idioma, cuyas reglas no cambian. La selección final empieza de nuevo sobre las mismas páginas con la configuración ampliada y congelada.
- Tabla revisable de 286 grupos en `research/cleaning_2026-09-15/repeated_abstract_review.csv`; decisiones exactas y huellas en `config/cleaning_v1.json`. No se borran los grupos científicos solo por duplicarse.

- La comprobación de firmas de páginas se extendió a las 6.138 páginas ya guardadas: 461 pares ID/texto identificados por estructuras claras de navegación, avisos o anuncios. La lista final contiene 538 textos completos identificados por huella; no es una lista de 538 descartes ni una garantía de detección exhaustiva. Se conservaron ejemplos de artículos válidos sobre publicidad como controles contra falsos positivos.
- Segundo recorrido provisional archivado en `data/corpus_clean_v1_second_pass`. Se reconstruye ahora con todas las reglas finales, sin cambiar población o reparto; las páginas y predicciones se reutilizan. Las reglas se cierran antes de cualquier cálculo de embeddings.

### Corrección de la comprobación de páginas nuevas

- El tercer recorrido completó 500.000 y pasó la reproducción del guardado; la revisión adicional detectó una página ACS nueva (`W1972646318`) no incluida en el catálogo inicial. No se entregó como terminado.
- Causa identificada y corregida: las estructuras específicas de páginas se aplican ahora también a cualquier candidato nuevo dentro del filtro común. La prueba de regresión falló antes del cambio y las 14 pruebas pasan después; también se prueba reutilizar páginas adicionales sin API.
- Se archiva el tercer recorrido y se conserva la página nueva con la misma huella. La reconstrucción definitiva usa `./prepare.sh prepare --offline`; no solicita datos otra vez. Evidencia en `content_regression_fix.json`, log en `data/preparation_closed_run.log`.

## 2026-09-15 — Limpieza y preparación completas

- Final verificado a las 14:27:20 UTC; segunda comprobación de idioma/contenido aprobada en los 500.000. Cero discrepancias de idioma al repetir el detector y cero estructuras conocidas de páginas restantes. Selección y 576.585 decisiones examinadas reproducidas; 6.139 páginas contrastadas. El archivo original conserva su huella.
- Resultado: 500.000 IDs distintos, 400.000+100.000, mínimo 2.165 por área/período y 650 combinaciones área/año. 5.776 registros originales apartados por calidad y 123 válidos no reelectos al reajustar cuotas. 494.101 IDs originales conservados, 5.889 candidatos sobrantes aprovechados y diez registros de una página adicional de 100. La última reconstrucción no hizo consultas API.
- 9.883 idiomas dudosos y 3.002 posibles textos mixtos conservados con marcas; el resto de alertas, duplicados y el efecto por Field están en los CSV y `CLEANING.md`. Son diagnósticos, no una garantía de calidad perfecta.
- Las 14 pruebas específicas pasan; se reprodujo el fallo de páginas nuevas antes de corregirlo. Comprobada de nuevo la localización y validez de los 22.118 vectores históricos candidatos; no se copiaron ni recalcularon. La figura final se inspeccionó y su título ya no queda recortado.
- Nuevos: `sos_prepare/`, `prepare.sh`, `config/cleaning_v1.json`, `requirements-preparation.txt`, pruebas de preparación, scripts de comprobación, `CLEANING.md`, `EMBEDDINGS_READY.md`, tablas finales y evidencia de limpieza. Actualizados los documentos de protocolo, inventario y continuidad. Copia de 25 archivos de código/reglas/pruebas/dependencias en `data/corpus_clean_v1/source_snapshot/`.
- `./prepare.sh preflight` devuelve `ready_for_model_configuration`. Entorno sin conflictos según pip; clave ausente de los artefactos de texto inspeccionados; TFM limpio según Git. Sin cambios del extractor original, sin embeddings, sin commits ni push.

## 2026-09-15 — Reparto final y opciones de modelos

- Recalculados los recuentos desde el Parquet final en lectura: 500.000, 400.000+100.000, 26 Fields, 130 períodos y 650 áreas/año. Coinciden todos los recuentos por área/período con las tablas de limpieza. Huella actual y verificaciones en `research/model_review_2026-09-15/balance_verification.json`.
- Creados `CORPUS_BALANCE.md`, tablas de proporciones y diagnóstico reproducible. Mínimo 2.165 en 12 combinaciones; 80 quedan en 2.165–2.166. El menor año aislado tiene 282, Informática 2000. No se modificaron cuotas ni datos.
- Examinada la unión de marcas de idioma dudoso/resumen corto para señalar debilidades: es un escenario hipotético, no otra limpieza. Matemáticas antigua y Artes/Humanidades antigua merecen controles específicos.
- Revisión dirigida de artículos y fichas oficiales mediante las guías paper-lookup/citation-management. SemCSE verificado en texto completo y Crossref; Imel/Hafen en métodos completos; SemCSE-Multi solo resumen/metadatos. La búsqueda editorial Crossref para Imel/Hafen no encontró coincidencia entre sus tres resultados; no demuestra ausencia de publicación. Fuentes y límites en `MODEL_SELECTION.md`.
- Propuesta sin aceptar: SPECTER2 + SemCSE_cosine + MPNet + Qwen3-Embedding-0.6B; SciNCL quinto opcional. La variedad de entrenamiento y uso motiva la selección; cuatro no es un requisito de QSS. SemCSE/Qwen aún no tienen prueba local de velocidad/compatibilidad.
- Actualizados `DECISIONS.md`, `findings.md`, `task_plan.md`, `NEXT_STEPS.md` y el punto de continuación de este registro. No se descargaron artículos/pesos ni se iniciaron embeddings. Preparación final intacta; modelos/versiones/entrada pendientes de respuesta.

## 2026-09-15 — Más modelos y prioridad a los usados en mapas científicos

- El usuario pide más de cuatro; durante la ampliación precisa que quiere priorizar usos académicos para mapear la ciencia. Se archiva la propuesta de variedad de familias en `research/MODEL_SELECTION_diversity_proposal.md` y se sustituye la recomendación vigente sin registrar ninguna lista como aceptada.
- Creados `ACADEMIC_MODEL_USAGE.md`, `academic_sources/studies.json`, frecuencias y manifiesto dentro de `research/model_review_2026-09-15/`. Diez estudios contrastados; separados modelos usados, citados, antecesores y evaluados en tareas distintas. Algunas fuentes son métodos completos; Lamers solo resumen institucional; Huang código y fragmentos editoriales. No es un censo de uso mundial.
- Reutilizado XML del mapa biomédico. Obtenidos XML de Nanoscience, PDF de Cosmos, HTML de dos aplicaciones y código de Huang solo para leer. La descarga PDF de Lamers falló. `lxml` no estaba instalado: se utilizó el lector XML estándar y el parser de paper-lookup; no se añadió dependencia. PDF leído con pypdf del runtime ya disponible. No se ejecutó código ajeno.
- Verificado en Crossref que qss_a_00168 era una atribución errónea a Lamers; corregida en bibliografía. Publicación Liang confirmada como IP&M 2026, DOI 10.1016/j.ipm.2025.104557. SemCSE-Multi confirmado en ACL 2026, corrigiendo el estado anterior de preprint.
- Nueva propuesta: SPECTER, SPECTER2, SciNCL, SciBERT, BERT, MPNet, MiniLM y PubMedBERT; BioBERT/SimCSE si se eligen diez. TF-IDF propuesto aparte. Generales con uso académico permanecen; modelos recientes sin ese respaldo identificado pasan a alternativas.
- Actualizados guía de modelos, decisiones, reglas generales, tareas, siguiente paso y hallazgos. Pendiente elección ocho/diez y recetas. Sin pesos nuevos, embeddings, cambios del corpus, commits ni push.

## 2026-09-15 — Diez modelos preparados para ejecución desde terminal

- El usuario eligió los diez, aceptó uso habitual + control de fragmento común y pidió iniciar él mismo el cálculo completo. Se respetó: no se ha iniciado ningún bloque completo del corpus de 500.000.
- Entorno separado `.venv-embed/`; archivos oficiales fijados/verificados y SciNCL/MPNet reutilizados de la caché. `config/embeddings_v1.json`, `requirements-embeddings.txt` y `research/embedding_setup_2026-09-15/assets_manifest.json` documentan las versiones.
- Implementados `sos_embed/`, `embed.sh` y `start_embeddings.sh`: procesamiento offline por bloques, escritura segura, comprobación de identidad/huellas, reanudación, bloqueo de instancias concurrentes por salida, progreso y registro de mensajes. No se cambiaron `sos_download/`, `sos_prepare/` ni el corpus.
- Diecisiete pruebas aprobadas. Los diez modelos pasaron la prueba real sobre 1.300 artículos y otra sobre el fragmento común; auditoría independiente de filas/vectores, recuperación y huellas aprobada. Reanudación real de SPECTER sin recalcular el primer bloque. Fuente y resultados en `research/embedding_setup_2026-09-15/`.
- Extrapolación directa: 24,14 horas; planificación comunicada: 25–35 horas. Vectores: 25,03 GiB más índices; reservar 35 GB. No equivale a tiempo medido durante un día ni a prueba de suficiencia científica.
- Se conservan media/CLS/SEP para cuatro modelos sin repetir la inferencia; principal y normalización pendientes antes de analizar. Control actual de 1.300 técnico; tamaño científico final aún abierto. No se reutilizan vectores antiguos de versión desconocida.
- Actualizados AGENTS, DECISIONS, MODEL_SELECTION, ACADEMIC_MODEL_USAGE, EMBEDDINGS_READY, NEXT_STEPS, findings y task_plan. Sin commits ni push.
- **Punto exacto:** usuario ejecuta `./start_embeddings.sh`. Consultar avance con `./embed.sh status --scope full` y el registro `data/embeddings_run.log`. Al terminar, validar diez modelos completos antes de análisis.

## 2026-09-16 — Progreso y recordatorio de revisión final

- Comprobados procesos reales, avance, veinte bloques recientes de PubMedBERT, configuraciones/programas y validaciones guardadas. Siete modelos completos, PubMedBERT 209.920/500.000 a las 23:31, dos aún sin empezar. Sin errores encontrados en el registro consultado. Esta comprobación no sustituye verificar todos los vectores al acabar.
- Estimación base restante: 7,42 horas; margen comunicado: 7–9 horas continuas. La estimación inicial del usuario de cinco horas no se convierte en hora garantizada de finalización.
- Creado y verificado el seguimiento temporal `revisar-embeddings-y-preparar-siguiente-fase` en este mismo hilo: primera revisión dentro de cinco horas desde las 23:42; después cada hora si todavía calcula. El seguimiento anterior de OpenAlex permanece pausado.
- Creado `POST_EMBEDDING_REVIEW.md` con revisión final y preparación técnica autorizadas. Evidencia en `research/embedding_review_2026-09-16/progress_snapshot.json` y configuración del recordatorio en `automation_configuration.json`.
- Actualizados `AGENTS.md`, `DECISIONS.md`, `task_plan.md` y este registro. No se modificaron programas, entorno, pesos, configuración o datos en uso; no se reinició ni duplicó el cálculo.

## 2026-09-17 — Primera revisión automática, 04:44 Madrid

- Nueve modelos completos; SimCSE 172,032/500.000 y avanzando. Procesos reales confirmados, sin auditoría final paralela o entregada. Programas/configuraciones coinciden; nueve validaciones guardadas completas y coherentes con sus manifiestos. No equivale a una nueva lectura de todos los vectores.
- Seguimiento cambiado de cinco horas a una hora y verificado; antigua automatización de OpenAlex sigue pausada. No se ha reiniciado ni modificado el cálculo.
- Evidencia: `research/embedding_review_2026-09-17/progress_024441.json`. Estimación 1,8 h a la velocidad reciente. Esperar a que termine la cola para la auditoría final; no avisar de avance normal sin acción necesaria.

## 2026-09-17 — Revisión automática, 05:46 Madrid

- Nueve modelos completos; SimCSE 362.496/500.000, proceso 57837 y cola 43938 vivos y avance confirmado. Unos 45 minutos a la velocidad reciente de 51.48 artículos/s. Sin necesidad de acción del usuario.
- Seguimiento horario verificado y conservado; no se ha modificado ni reiniciado el cálculo. No hay otra auditoría en marcha o entregada. Evidencia: `research/embedding_review_2026-09-17/progress_034605.json`. Auditoría completa al acabar, según `POST_EMBEDDING_REVIEW.md`.

## 2026-09-17 — Inicio de auditoría final, 06:47 Madrid

Los diez modelos tienen 500.000 filas y no queda proceso de cálculo ni otra auditoría activa. SimCSE terminó a las 04:29:16 UTC; el registro de la cola contiene su validación global. Se inicia una comprobación nueva de todos los archivos, procedencia y organización en `research/embedding_final_audit_2026-09-17/`. No se considera cerrada hasta verificar y preparar el acceso para la siguiente fase.

## 2026-09-17 — Auditoría final y acceso para análisis terminados

- Corpus y modelos verificados de nuevo: `prepare.sh preflight`, `embed.sh preflight`, y `embed.sh verify` en full, pilot y control. Evidencia nueva en `research/embedding_final_audit_2026-09-17/`.
- `audit.py` contrasta procedencia, filas, versiones, programa, entorno, recortes y coherencia del control. Se crearon catálogo, inventario, recuentos de recorte y `data/analysis_ready_v1/metadata.parquet`; los archivos grandes se mantienen en sus rutas.
- Implementado lector independiente `sos_analysis/reader.py`. Ocho pruebas específicas aprobadas, incluida correspondencia equivocada aunque las huellas sean coherentes. `verify_reader.py` leyó las 18 variantes sobre los 500.000 artículos, conservando base/complemento y calidad; máximo observado de memoria de 0,72 GB. No se calcularon medidas científicas.
- Creados `EMBEDDINGS_AUDIT.md`, `DATA_CATALOG.md` y `ANALYSIS_PROPOSAL.md`. Actualizados NEXT_STEPS, EMBEDDINGS_READY, AGENTS, DECISIONS, findings, task_plan, brief/preguntas y notas de estado de modelos/cálculo. La propuesta futura no se registra como aceptada.
- Sin nueva extracción, inferencia, instalación, movimiento o eliminación de datos originales; sin commits ni push. Seguimiento temporal pausado mediante la herramienta de automatizaciones y estado comprobado; OpenAlex sigue pausado. Evidencia: `research/embedding_final_audit_2026-09-17/automation_closed.json`. Siguiente paso: respuesta del usuario a la propuesta científica.

## Comparación científica delegada, 17-09-2026

El usuario autoriza continuar con la comparación de la forma y después de los vecinos, delegando las cuestiones pendientes de esta fase con criterio de solidez para QSS. Autoriza investigar medidas más robustas, ejecutar las comparaciones, inspeccionar resultados y preparar su presentación. Pide diagnosticar el recorte de MiniLM y corregir/recalcular si procede. Esta petición sustituye las restricciones previas de solo preparación y de esperar nuevas respuestas para esas decisiones. Se decidirán y documentarán medidas, recetas, controles y presupuesto antes de inspeccionar acuerdos. Conservar las salidas congeladas; cualquier corrección o variante nueva irá en una salida separada. No implica publicación, envío a revista ni cambios al TFM.

Inicio de revisión metodológica y diagnóstico de MiniLM. Se mantienen las guías planning-with-files y paper-lookup para continuidad y fuentes.

## 2026-09-17 — Protocolo y primeras comprobaciones de análisis

- Consulta dirigida de fuentes primarias sobre CKA corregida, Procrustes angular, RSA y ReSi; seis registros arXiv recibidos y reconciliados. Una página PMC mostró un captcha; se usó el PDF editorial de NeurIPS. Fuentes y alcance en ANALYSIS_PROTOCOL.
- Congelado `config/analysis_v1.json` antes de los acuerdos. Decisiones por delegación en DECISIONS; no se pidieron permisos ya concedidos.
- Nuevo entorno `.venv-analysis/` para NumPy/SciPy/Arrow/figuras, con versiones en `requirements-analysis.txt`. No se modificó `.venv-embed/`.
- `extra_embeddings.py`: MiniLM 512 separado, reanudable y con reutilización por identidad. Primer bloque de 1.024 verificado: 527 vectores idénticos reutilizados, 497 recortes originales y 67 a 512. Cálculo completo reanudado desde ese bloque, sin recalcularlo. Control común de 52.000 en preparación.
- `geometry.py`, `native_data.py`, `run_shape.py`: comparación y lectura en memoria acotada, manifiestos y salidas por celda. Siete pruebas pasan, con fórmula alternativa de CKA, invariancias, datos aleatorios, mezcla de IDs y cálculo por bloques. Primera celda real en curso.

- Control común preparado: 52.000 artículos, 25.143 textos acortados y un título acortado; 26.857 textos intactos podrán reutilizarse. Campo/período: 400 cada uno. Selección y huellas guardadas.
- Primera celda real de forma completada y comprobada: 45 pares y 45 referencias mezcladas; valores finitos y CKA mezclada cerca de cero. Arrancada la ejecución reanudable de todas las etapas, conservando esa celda.
- Ajuste técnico de vecinos antes de verlos: CPU exacta float64 por coste viable (~13 minutos proyectados con datos artificiales) y mayor precisión; configuración separada `neighbors_v1.json`, sin cambiar el diseño ya congelado de forma/texto.

- Completada la primera medida de forma en las 130 celdas, con Procrustes, RSA y referencia permutada. Se continúa con resultados globales y controles; aún no se interpreta el resumen provisional como conclusión final.
- Cuatro pruebas de vecinos pasan, incluida resolución de grupos grandes de empates, autoexclusión y coincidencia con una implementación independiente. Iniciada búsqueda exacta de vecinos después de completar la forma primaria. CPU float64, cuatro hilos por proceso; MPS dedicado a controles de texto.

## 2026-09-17 — Controles y primeras salidas completas

- MiniLM 512 terminado: 500.000 filas, 489 bloques; 34.331 recortes (6,8662%), frente a 247.910 (49,582%) a 256. Es sensibilidad de longitud, no corrección de un fallo ni prueba de mejora semántica. Original intacto.
- Forma primaria, global, centros de áreas, originales, CLS, SEP y criba de calidad terminados. La criba conserva 448.886 registros, mínimo 1.375 por celda. Las selecciones de estabilidad siguen calculándose; no se presentan como intervalos poblacionales.
- Vecinos internos completos para los diez modelos; consultas globales en curso. Cuatro pruebas y contraste numérico independiente en consultas reales. Se concreta un control adicional de 2.048 candidatos por celda y recetas comunes antes de inspeccionar los acuerdos de vecinos, porque la corrección por azar no elimina todo el efecto de tamaños distintos.
- El control de texto común procesa diez modelos con 52.000 IDs emparejados; sin recortes adicionales en los modelos terminados. Se reutilizan los 26.857 textos que no cambian.
- `compare_controls.py` calcula recetas dentro de un modelo, MiniLM 512, texto común y vecinos con candidatos iguales; su implementación queda congelada al empezar los controles tempranos. Los ejecutores dependen de bloqueos de los cálculos previos y comprueban sus estados antes de continuar. No hay automatizaciones periódicas nuevas.
- `report.py` reconcilia resultados, exporta tablas y figuras en salidas separadas. `reports/analysis_v1/preview/` es provisional: no confundirla con la entrega final. La figura de relaciones entre áreas e interior de áreas se inspeccionó; las medidas describen objetos distintos.
- Consulta adicional a la documentación oficial de OpenAlex: los Fields derivan de una clasificación automática que usa texto, citas y revista. Se utilizarán como grupos de análisis, nunca como verdad independiente para proclamar un modelo ganador. Fuente: https://help.openalex.org/data/topics/ .

## 2026-09-17 — Comparación de forma y vecinos terminada

- Todos los procesos científicos finalizaron. El ejecutor `run_complete_analysis.py` cerró con código 0 y `COMPLETE ANALYSIS AND FINAL NUMERICAL AUDIT`; la entrega se generó a las 08:19 UTC / 10:19 de Madrid. Registro en `research/analysis_2026-09-17/complete_analysis.log`.
- Forma: seis etapas de 130 celdas, resultado sobre base de 400.000, centros, 20 selecciones por tamaño/celda y tres medidas. 5.800 de 5.850 comparaciones pasan la regla; 50 alertas en 13 celdas, todas por amplitud. No se cambiaron umbrales ni descartaron resultados adversos.
- Vecinos: 500.000 artículos × diez modelos dentro de área/período; 13.000 consultas equilibradas contra 400.000 de base; k=10/25/50, ajuste por azar y 18 variantes en el control con 2.048 candidatos por celda. 13.260 consultas reales contrastadas con ordenación independiente. Coincidencia equilibrada de 25 vecinos: 30,285%; control de candidatos iguales: 31,860%.
- MiniLM 512: 500.000 filas, 247.910 recalculadas y 252.090 reutilizadas exactamente. Recortes 6,8662%, frente a 49,582% original. Unos 23 minutos de ejecución. No había fallo en el límite habitual; conservar 256 principal y 512 sensibilidad.
- Control común: diez × 52.000, 400 por área/período, ningún recorte adicional. Cada modelo reutiliza 26.857 textos intactos; 25.143 cambian. Comparaciones emparejadas y estabilidad por Field terminadas. MiniLM + controles: 1.020.000 filas modelo–artículo auditadas, 520.660 reutilizadas bit a bit; los cuatro modelos BERT de palabras verifican las tres salidas guardadas.
- Seguimiento de centros en programas separados: recetas, calidad, longitud original y texto común. Se añadieron después del resultado inicial y se identifican como tales. La reconstrucción principal coincidió. Veinte repartos aleatorios por condición conservan tamaño, fechas e identidad compartida entre modelos; no son pruebas de significación.
- Entrega final: `reports/analysis_v1/final/summary.json`, `audit.json`, `catalog.json`, 33 tablas y ocho figuras PDF/SVG/PNG. Las ocho figuras se inspeccionaron; se corrigió una etiqueta superpuesta en la figura de forma/vecinos antes del cierre. Tabla por artículo: 500.000 IDs, Field/período/base-refuerzo y coincidencias locales.
- Informe nuevo `ANALYSIS_RESULTS.md`, métodos y esquema concreto de cuatro figuras principales en `METHODS_ANALYSIS.md` y `PAPER_OUTLINE.md`. Actualizados DECISIONS, AGENTS, task_plan, findings, README, DATA_CATALOG, NEXT_STEPS y nota vigente de 02_open_questions. `.gitignore` excluye la entrega provisional y el Parquet derivado por artículo; los archivos se conservan localmente.
- Incidencias resueltas sin cambiar salidas científicas: la primera versión del auditor adicional comparaba una huella de objeto JSON con la del archivo; se corrigió el auditor y pasó sobre los once conjuntos. Un contador NumPy necesitó convertirse a entero para escribir el informe; se corrigió el exportador. Un ejecutor que solo esperaba se interrumpió antes de empezar comparaciones y se sustituyó para solapar controles independientes; no se pararon ni reiniciaron cálculos científicos. Una consulta auxiliar de resumen agrupaba generadores ya consumidos; se corrigió para redactar la tabla, sin tocar mediciones.
- Decisión final dentro de la delegación: no ampliar todo el corpus; mantener alertas y límites al interpretar diferencias pequeñas. No se presentan intervalos poblacionales, una verdad temática o una métrica universalmente mejor. El acuerdo entre forma y vecinos es positivo y fuerte (0,920), no independencia.
- Sin cambios a corpus/embeddings/programas originales ni al TFM, sin nuevos modelos principales, sin automatizaciones nuevas, sin commits/push/publicación. Antiguos seguimientos permanecen pausados. Punto de continuación: redactar el manuscrito y contrastar su aportación con antecedentes próximos, usando la entrega final.

## 2026-09-17 — Inicio de checklist adicional

Petición nueva registrada. Leídos decisiones/progreso/plan, programas reutilizables y configuraciones congeladas. Protocolo nuevo y presupuesto de piloto fijados antes de ejecutar las nuevas condiciones. Uso continuado de planning-with-files para registro. Revisadas fichas oficiales de SPECTER2, SciNCL, MPNet y SimCSE; el objetivo de ajuste y el origen compartido son rasgos distintos. No cambiar el modelo para forzar familias homogéneas.

Piloto preparado: 26.000 IDs, 200 por celda. Diez pruebas reales sobre cuatro artículos/modelo reproducen las salidas originales con diferencias máximas menores de 0,000006; los tokens de título/resumen coinciden con el campo literal y la inferencia individual coincide con el lote. Iniciada cola reanudable: original combinado reutilizado y veinte condiciones nuevas. El primer bloque MiniLM se conserva para comprobar reanudación sin reescritura. Código nuevo separado; fuente congelada al empezar.

Cinco pruebas del nuevo cálculo del piloto pasan: equivalencia de CKA con la fórmula congelada, rotaciones y mezcla de IDs, separación de efecto de modelo/entrada en ejemplos conocidos, rangos y rechazo de casos degenerados. La regresión de familias detectó una omisión no identificable en el control SEP; versión nueva separada la informa en lugar de atribuir coeficientes únicos.

Prueba completa adicional con entradas artificiales idénticas: desacuerdo de entrada cero, vecinos preservados al 100%, correspondencia de IDs y reanudación sin modificar archivos; aprobada. El detalle de entrada compara usos prácticos: límites/separadores pueden cambiar el texto efectivo al quitar un campo; se documenta antes de interpretar el piloto y no se afirmará causalidad pura del contenido eliminado.

Exportador separado `sos_followup/report.py`: entrega provisional de resultados existentes, cuatro figuras PDF/SVG/PNG inspeccionadas visualmente. El exportador exige auditorías completas para una entrega final. El cálculo de entradas sigue activo.

Control temporal posterior en `candidate_check.py`: mantiene consultas idénticas para separar su selección del cambio de candidatos, reutilizando las matrices por artículo anteriores. 266.240 consultas, 17.550 comparaciones, tres valores de k y 130 celdas comprobados. El signo temporal cambia también con consultas iguales. Protocolo actualizado con su carácter posterior al hallazgo.

Consulta auxiliar de metadatos: el nombre real es `field_display_name`, no `field_name`; corregido solo en la consulta exploratoria. No afectó a programas de cálculo ni resultados.

Métodos adicionales redactados en `METHODS_CHECKLIST.md`. Contrastados antecedentes de entrada: Constantino et al. ya compara título y abstract en física; SemCSE incluye tareas título–abstract y una comprobación de concatenación. Nota de alcance en `research/checklist_2026-09-17/RELATED_INPUT_WORK.md`. Acceso editorial QSS devolvió 403; se leyó versión de autores. No afirmar novedad de las entradas por sí solas.

Antes de que empiece `input_analysis.py` (la cola de inferencia aún va por el cuarto modelo), se añade al manifiesto el número de versión de Python/NumPy/SciPy/PyArrow y la huella de `requirements-analysis.txt`. No se cambia ninguna medida ni el código de inferencia activo. La primera ejecución científica de esta comparación congelará esta versión completa.

Las seis pruebas matemáticas/de flujo vuelven a pasar tras completar los metadatos; registro `tests_final.log`. El informe final rechaza correctamente un piloto incompleto y no crea una falsa entrega final (`report_gate_test.json`). Perfil de texto adicional, anterior a inspeccionar acuerdos de entradas: seis filas en tres títulos repetidos por área, cero resúmenes repetidos; `input_text_profile.py` guarda recuentos reproducibles, sin exclusiones ni cambios de muestra.

Antes de inspeccionar efectos de entrada se añade el cruce de recetas, porque la fase anterior ya había detectado sensibilidad fuerte. Configuración separada `checklist_input_recipes_v1.json`, registro temporal `recipe_control_decision.json` y programa `input_recipe_control.py`: reutiliza vectores y vecinos principales, calcula solo vecinos alternativos y exige reproducir mean. Prueba integrada con rotaciones inocuas y un título deliberadamente desalineado: solo cambia el efecto de entrada/receta correspondiente, y la reanudación conserva el archivo; aprobada en `recipe_tests.log`. `finish_recipes.py` espera al análisis principal y ejecutará el control. No se tocó la inferencia activa.

## 2026-09-17 — Checklist terminada y auditada

- Cola de entradas completa; ejecutores cerrados con éxito. Las 30 condiciones cubren los mismos 26.000 artículos. Auditoría de 780.000 filas modelo–artículo–entrada, 260.000 reutilizadas exactamente y 520.000 nuevas. Originales, configuración anterior, pesos y bloque de reanudación intactos.
- Comparación principal completa: 4.290 filas de forma, 12.870 de vecinos, 1.560 de efectos, 78 resúmenes secundarios y 10.400 repeticiones de estabilidad. Cruce mean/CLS/SEP: 12.870 de forma, 38.610 de vecinos y 6.240 de efectos. Siete pruebas matemáticas/de flujo aprobadas; 78 contrastes reales de fórmula y 14.040 consultas independientes de vecinos.
- El cruce reproduce la principal con error máximo CKA 7,82 × 10⁻¹⁴ y coincidencia exacta de vecinos. No se editaron módulos científicos ni configuraciones una vez congelados. La primera versión parcial de familias permanece en `existing/`; `existing_v2/` es la completa.
- Resultado de entrada: cambiar modelo, quitar resumen y quitar título pierden en promedio 16,2/16,7/5,0 de 25 vecinos con mean. Las cifras son del piloto con 1.000 candidatos por área. El orden de los dos primeros cambia con receta y hay diferencias claras entre modelos. Se conservan todos los casos y medidas, sin seleccionar el resultado más cómodo.
- Estabilidad: pasan los 52 promedios de área y 489/520 contrastes individuales de forma; 31 alertas de amplitud en 17 áreas, sin fallos de cambio de mediana. Decisión delegada: mantener 26.000 para patrones generales, no repetir las dos entradas sobre 500.000. No afirmar precisión poblacional, equivalencia ni estabilidad de vecinos basándose en esa criba.
- Tiempo, disciplina y familias terminados. Se mantiene como posterior el control temporal con consultas idénticas. Medicina no es última en todas las medidas; el papel de biomédicos/composición/familias se presenta como asociación con controles, no causa probada.
- Entrega nueva: `CHECKLIST_RESULTS.md`, `METHODS_CHECKLIST.md`, `reports/checklist_v1/final/`: 33 CSV, siete figuras en PDF/SVG/PNG, resumen, auditoría, catálogo y copia del exportador. Las siete figuras se inspeccionaron visualmente; las figuras 2–5 finales coinciden con los PNG ya inspeccionados de la vista provisional.
- Actualizados `AGENTS.md`, `DECISIONS.md`, `task_plan.md`, `findings.md`, `README.md`, `DATA_CATALOG.md`, `NEXT_STEPS.md`, `02_open_questions.md` y `PAPER_OUTLINE.md`. Enlace de continuidad añadido a `ANALYSIS_RESULTS.md`; se conserva su contenido científico. El esquema integra cuatro figuras principales y once de suplemento, sin borrar resultados anteriores.
- Comprobación de cierre y estado en `research/checklist_2026-09-17/closure_audit.json` y `checklist_status.json`. Una consulta auxiliar intentó importar pandas en el entorno de análisis, que no lo incluye; se sustituyó por `csv` de Python, sin instalar ni cambiar el entorno o cálculos.
- No hay nuevos modelos, descargas de corpus, automatizaciones, commits, push, publicación o envío. Seguimientos previos pausados. No quedan decisiones necesarias del usuario para cerrar la checklist.

**Punto exacto para continuar:** cuando el usuario lo solicite, redactar el manuscrito con `PAPER_OUTLINE.md` y ambos informes/métodos. Mantener las 31 alertas nuevas y las 50 antiguas separadas. Solo ampliar una comparación concreta si una afirmación esencial lo necesita; no relanzar inferencia ni vecinos por recuperar el proyecto en otro chat.

## 2026-09-17 — Nuevo objetivo de cierre experimental ampliado

Leído objetivo activo completo y estado real. No hay cálculos científicos activos al iniciar. Se conserva la entrega anterior; se registra nueva meta y evidencia requerida en `ROBUSTNESS_SCOPE.md`, sin redefinirla como solo ampliación de entradas. Configuración `input52_v1.json`: mismo diseño, semilla y modelos, 400 por celda y 52.000 totales.

Auditoría de cobertura con metadatos congelados: 252 Subfields; tamaños agrupando fechas de 3 a 17.974; 1.255 celdas Subfield×período no vacías, de 1 a 4.858. 217 Subfields tienen al menos 256 artículos y contienen 495.828 registros; 183 alcanzan 512 y contienen 482.931. Por período, 796 celdas alcanzan 128. Se guarda `size_audit.json` antes de definir la comparación de escalas. Espacio disponible inicial: 186 GiB.

### 52k en ejecución y comparación preparada

Preparada selección exacta de 52.000: conserva los 26.000 y añade 200 por cada celda. Tres pruebas de reutilización/identidad/recetas aprobadas. Prueba real MiniLM: 1.024 filas, 521 copias bit a bit y 503 nuevas; tokens comprobados y cuatro inferencias individuales reproducidas con error máximo 5,36e-7. La reanudación real preservó el primer bloque.

Cola autorizada activa: `run_inputs52.py`, PID 93254, sesión de herramienta 85571; registro `input52_run.log`. Solo infiere nuevas filas, no cambia los originales. Programas/configuración de inferencia ya congelados. Auditor independiente `sos_deep/audit_inputs52.py` verificará también las 520.000 filas de entradas sencillas reutilizadas del piloto.

Comparadores separados `input_analysis52.py` y `input_recipes52.py`: dos pruebas integradas aprobadas, entradas idénticas, mezcla intencional de filas, invariancia a rotación, reanudación y reproducción de la principal. `finish_input52.py` espera la auditoría de la cola viva y hará ambas comparaciones. Configuración de recetas actualizada a 52k antes de su ejecución; no usa los tamaños del padre de 26k. Alcance de la fase completa en `ROBUSTNESS_SCOPE.md`; aún quedan R03–R12 y seguimiento definitivo de alertas.

## 17-09-2026 — Cierre ampliado: primeras comprobaciones terminadas

La meta R01–R12 permanece activa. Actualizados los encabezados de README/NEXT_STEPS para distinguir este trabajo de las dos entregas históricas.

- `subfields_native` terminó: 252 grupos, 500.000 filas cubiertas, 11.340 comparaciones de forma, 34.020 de vecinos y 25.100 consultas independientes. Grupos diminutos conservados; medidas no disponibles explícitas. Sesión 41399 terminada. No resume ni modifica matrices originales.
- `temporal_review` reconstruye exactamente 23.400 trayectorias y la separación consulta/candidatos; prueba aprobada. CKA aumenta entre extremos en 23/26 áreas (24 con igual tamaño), pero solo 4 tienen todos los pasos positivos. Calidad reduce a 20/26. Vecinos con candidatos iguales aumenta en 20/26; con todos, 10/26. Entrega y auditoría en `data/robustness_v2/temporal_review/`.
- `regions` terminó: puntuaciones continuas para cada ID, k=10/25/50, omisión de modelos/familias, cobertura y ejemplos. Reproduce exactamente el k25 por artículo anterior. `data/robustness_v2/regions_native/`; aún requiere el control de tamaño para interpretar diferencias entre grupos. Prueba de omisión/modelo influyente y grupo trivial aprobada.
- `family_traits` terminó: arquitectura desde configuraciones fijadas, linaje, grupo documentado de corpus, señal de entrenamiento, dominio y receta por separado. Ocho resultados con 5.000 permutaciones y omisiones; prueba rechaza coeficientes únicos en diseños de rango insuficiente. Configuración `family_traits_v2.json`; sus grupos de corpus no son una medición de solapamiento real de artículos. Interpretación final pendiente.
- Sigue la inferencia 52k y su ejecutor de comparaciones. Nuevo ejecutor `finish_stability100.py` espera la auditoría de recetas antes de ampliar repeticiones en ambos tamaños; conserva y comprueba las primeras 20 y todas las 31 claves. Prueba aprobada.
- `subfield_controls` está activo después del cierre nativo: tamaños 128/256/512, tres recetas, 20 selecciones y fechas con 128 candidatos por Subfield elegible en los cinco períodos. Prueba de selecciones anidadas, rotaciones y vecinos aprobada; configuración y fuentes ya congeladas.
- Nuevo control de composición de Medicina, con las 26 áreas: 2.048 por área, mismas cuotas de fechas, mezcla observada frente a igual cantidad por Subfield elegible; diez selecciones. La elegibilidad, calculada antes de acuerdos, cubre 485.119 artículos. Energía y Enfermería conservan un solo Subfield en este control y no pueden informar un cambio de composición; se muestran aparte. Prueba de cuotas y caso de un único grupo aprobada. Proceso activo; no editar sus fuentes.

La búsqueda encontró trabajos cercanos de 2026 y una versión de julio de Shesha cuya definición cambió respecto al resumen de enero. No usar resúmenes antiguos sin versión. Crossref por búsqueda devolvió registros ajenos pese a HTTP 200; no se usaron. El DOI directo de Xie/Waltman sí coincide. El PDF de Lamers en Bolonia devolvió 403; la copia oficial del libro ISSI se descargó completa en un segundo intento tras un timeout y falta de soporte de reanudación. El lector disponible es pypdf, no PyMuPDF. Incidencias técnicas sin cambio de datos científicos.

### Controles ampliados completos; cierre integrado aún pendiente

- Terminaron `subfield_controls`, `medicine_composition`, `paired_neighbor_scales` y `centroid_scales`. Cobertura: 217 Subfields con 256 candidatos, 183 comunes a 128/256/512, 125 con los cinco períodos a 128. Vecinos emparejados: 10.850 consultas fijas, diez selecciones y 43.400 comprobaciones independientes.
- Revisión trazable de controles en `control_review_v2`: reproduce las 5.850 filas originales y conserva las 50 alertas. Distingue MiniLM contra los otros nueve de MiniLM contra sí mismo; mezclar ambas preguntas distorsiona su media. Primera salida de revisión conservada como histórica, no usarla para ese resumen.
- Integración estructural vigente: `structural_review_v3`. Las versiones iniciales del exportador se detuvieron por una clave k repetida y por logaritmo de cero en una categoría sin artículos. Se preservaron sus fuentes/salidas y se corrigió en versiones separadas; las comparaciones científicas no se repitieron ni cambiaron. La tercera versión terminó con auditoría.
- Control de procedencia completo en `data/robustness_v2/provenance/`: 6.139 respuestas comprimidas únicas de OpenAlex verificadas; original y corpus limpio intactos; 4.890 bloques y 8.802 archivos de vectores originales verificados, además de versiones/pesos/fuentes. Es una extracción de páginas a lo largo del 15-09, no una copia mundial simultánea de OpenAlex.
- `METRICS.md` cierra CKA corregida, vecinos k25 y comprobaciones Procrustes/rangos/k10/k50. No añadir morfología sin otra hipótesis: no hace falta para responder la pregunta actual. Literatura actualizada con antecedentes directos y limitaciones de acceso en `research/robustness_2026-09-17/RELATED_WORK_UPDATE.md`.
- Hallazgo nuevo que limita una historia demasiado simple: el control local con mismas consultas/tamaños/fechas baja 1,35 puntos de coincidencia al pasar de Field a Subfield, pero solo baja en 127/217 Subfields con k25; con k50, 109/217. No hay ley universal de caída con detalle.
- Estabilidad Subfield: 2.628 alertas/8.235 pares en 183 grupos con muestra grande inferior al grupo; otros 213/3.060 en 68 grupos donde la muestra grande es el grupo entero. Su amplitud cero en ese segundo caso no prueba precisión poblacional. Un grupo de tres artículos queda sin CKA. Mantener estas limitaciones en el cierre.

Sigue activa la inferencia de entradas a 52k y sus ejecutores dependientes. No cerrar la meta R01–R12 todavía. Faltan resultados de entradas/recetas/100 selecciones, presentación integrada, matriz de conclusiones/controles y auditoría final de toda la ampliación.

- Pruebas consolidadas: 12 de análisis y 3 de inferencia aprobadas en sus entornos correspondientes. La primera ejecución conjunta intentó importar torch desde el entorno de análisis; se dejó ese fallo de entorno registrado y se separaron las pruebas sin cambiar paquetes ni código científico. Registros vigentes: `tests_analysis.txt` y `tests_embedding.txt`.
- Cinco figuras estructurales renderizadas e inspeccionadas; se apartó una leyenda que tapaba parte de una barra antes de la exportación final. Avance no equivale a cierre: faltan entrada/alertas finales y auditoría integrada.

### 52k: inferencia y auditoría independiente cerradas

La cola terminó con código 0 y `52K INPUTS FINISHED AND AUDITED`. Las 30 condiciones pasan: 1.560.000 combinaciones modelo–artículo–entrada, 520.000 reutilizadas del corpus original, 520.000 del piloto y 520.000 inferidas nuevas. Se verificaron todas las recetas guardadas, textos, tokens, orden y copia bit a bit; checkpoint de reanudación intacto. La comparación de forma/vecinos/recetas empieza ahora desde esos resultados auditados. Continúan los ejecutores de 100 selecciones y de entrega; no declarar aún el cierre completo.

## 2026-09-17 — Cierre experimental ampliado terminado: R01–R12

- Entradas y recetas a 52k terminadas: 30 condiciones auditadas, 1.560.000 combinaciones; 520.000 copias exactas del corpus completo, 520.000 del piloto y 520.000 nuevas. Comparación principal: 4.290 filas de forma, 12.870 de vecinos y 1.560 de efectos. Recetas: 12.870/38.610/6.240, con principal reproducida.
- Cien selecciones en ambos tamaños completas. Se reproducen exactamente las primeras veinte y se guardan todas las selecciones/valores. Alertas comparables 72/520 en 26k → 5/520 en 52k; con veinte, 31 → 4. Las 31 claves antiguas siguen trazadas. Cinco actuales por amplitud; ninguna por desplazamiento mediano. Pasan las 52 medias de área; seis incluyen cero. Detalle en `SAMPLING_STABILITY.md`.
- `input_review` terminó y la auditoría conjunta verificó 15 componentes: fuentes actuales/copias/huellas y padres, archivos de centros y vecinos; 52k anidado y 130 cuotas exactas; 2.170 pares de candidatos reconstruidos y 520 selecciones de composición; identidad de los 500.000 artículos preservada. `data/robustness_v2/final_audit/`.
- Entrega `reports/robustness_v2/final/`: 50 CSV, siete figuras PDF/SVG/PNG, resumen JSON, copia del exportador y catálogo de 73 archivos comprobados. Siete PNG inspeccionados; en la primera figura se adelantaron los puntos para que las cajas no los taparan, sin cambiar valores. Los otros seis PNG conservaron exactamente su huella. Revisión visual sellada por separado en `final_visual_review.json`.
- Doce pruebas de análisis y tres de entradas aprobadas en sus entornos, junto con los contrastes independientes reales de vecinos, fórmulas, tokens y reutilización. No se modificaron paquetes, corpus, pesos ni programas científicos congelados.
- Actualizados `ROBUSTNESS_RESULTS.md`, `SAMPLING_STABILITY.md`, `POOLING.md`, `CONCLUSION_CONTROLS.md`, `PAPER_OUTLINE.md`, `README.md`, `NEXT_STEPS.md`, `DATA_CATALOG.md`, `INVENTORY.md`, `ROBUSTNESS_SCOPE.md`, `AGENTS.md`, `DECISIONS.md`, `task_plan.md`, `findings.md` y `02_open_questions.md`. R01–R12 apuntan a evidencia comprobada. La revisión de literatura y métodos ampliados ya están guardados.
- Incidencias menores de edición/consulta: un parche que intentaba borrar/añadir el mismo documento fue rechazado antes de escribir; se reescribió solo ese esquema. Una consulta auxiliar pidió `field_name`, inexistente en el índice; se usó su columna real `field_display_name`. No afectaron resultados ni ejecuciones científicas.
- Ambos ejecutores finales terminaron con código 0, sesiones cerradas; reexportación de presentación también terminada. `ACTIVE_RUNS.json` queda como registro histórico completo. Sin nueva extracción, modelos, automatizaciones, commits, push, distribución de datos ni envío. Las automatizaciones previas siguen pausadas.

**Punto exacto para continuar:** la fase experimental solicitada está cerrada. El siguiente encargo puede ser redactar con `PAPER_OUTLINE.md`, resultados/métodos vigentes y revisión bibliográfica ampliada. No ampliar automáticamente a 500k las entradas, no presentar un modelo ganador ni una caída universal con detalle, no ocultar alertas. Comprobación final de documentos, catálogo y estado en `research/robustness_2026-09-17/closure_audit.json`.

## 2026-09-17 — Inicio de revisión previa al manuscrito

Leídas reglas, decisiones y cierre previo. Verificadas las 23 huellas documentales del cierre y guardadas copias en `research/prepaper_2026-09-17/baseline_documents/` antes de editar continuidad. El cierre histórico permanece intacto; las nuevas ediciones se sellarán aparte. Skills: planning-with-files, paper-lookup y citation-management. La consulta inicial de QSS devolvió también normas de otras revistas; no se usarán como reglas de QSS. Se requieren páginas oficiales específicas.

## 2026-09-17 — Revisión previa al manuscrito y atlas terminados

- Auditada la cadena desde extracción/limpieza hasta inferencia, forma, vecinos, entradas, escalas, tiempo y familias. `PREPAPER_REVIEW.md` separa comprobaciones y límites. Los 15 componentes científicos vigentes pasan verificación de archivos/fuentes. Auditoría nueva por otra vía: seis comparaciones de forma con error inferior a 1e−10 y 300 consultas reales, con coincidencia exacta de sus primeros 50 vecinos. Se leyeron con validación las 500k filas de tres modelos; no se recalcularon embeddings.
- Fijados `CASE_ATLAS_PROTOCOL.md` y `config/case_atlas_v1.json` antes de leer los nuevos títulos. Implementación separada `sos_review/case_atlas.py`, congelada con copia y huellas. Atlas de 217 Subfields a 256, persistencia en las mismas 183 bajo 27 condiciones, 10.850 consultas repetidas, 531.650 relaciones dirigidas entre consultas siempre presentes y 23.436 parejas de centros. Otras 34.200 reconstrucciones de intersecciones/enlaces y 2.170 ordenaciones de centros verificadas. Selección exploratoria, no preregistro del estudio entero.
- Revisados los doce artículos seleccionados y sus destinos. Los 30 registros ilustrados coinciden con respuestas originales de OpenAlex. Dos errores claros de etiqueta, un aviso bibliográfico y un resumen de destino incompleto quedan anotados. Comprobados los IDs/huellas y correspondencia de etiquetas de las 500k filas: no hay cruce de filas. Diagnóstico posterior de 82 títulos genéricos; excluir cinco consultas cambia el promedio de 45,344% a 45,349%, con candidatos intactos. No estima errores temáticos del corpus ni sustituye validación externa.
- Precisado un límite del control Field/Subfield: las 50 consultas del mismo Subfield permanecen en ambas listas de 256 candidatos. El ámbito amplio está condicionado; no describirlo como muestreo libre del Field. No se alteraron cálculos ni cifras.
- Pasan 32 pruebas en `.venv-analysis` y 20 en `.venv-embed`, incluidos selección/ordenación del atlas, interrupción, almacenamiento y entradas. El intento inicial mezcló entornos y falló al importar torch; se conserva el registro y se repitieron las pruebas en el entorno adecuado. No se instalaron paquetes ni se cambiaron entornos congelados.
- Biblioteca central en `references/references.bib`: 45 entradas verificadas, sin duplicados ni errores de estructura. Corregidos autores, páginas y versiones; una advertencia legítima de páginas ausentes en ICLR conservada. `references/RELATED_WORK.md` compara antecedentes y profundidad de lectura; `SEARCH_LOG.md` y JSON de consulta documentan acceso/identificadores. Copias completas de literatura locales fuera de Git; metadatos, estudios y registros de evidencia conservados en el material versionable.
- Presentación: README nuevo, `docs/INDEX.md`, `docs/REPRODUCING.md`, `docs/DATA_RELEASE.md`, `docs/QSS_CHECK.md`, `PREPAPER_REVIEW.md` y `CASE_ATLAS.md`. `reports/prepaper_v1/`: nueve CSV, doce casos explicados y dos figuras PDF/SVG/PNG. Ambas inspeccionadas; se corrigió el margen de la primera y se añadieron notas de calidad/selección a la segunda. Catálogo y revisión visual guardados. Los archivos científicos y figuras anteriores permanecen intactos.
- Continuidad actualizada en AGENTS, DECISIONS, task_plan, findings, NEXT_STEPS, DATA_CATALOG y esquema del paper. Enlazada la revisión desde resultados/matriz de controles y precisados los métodos. Bibliografía histórica conservada en `legacy_bibliography_original.md`; su entrada antigua dirige a la biblioteca canónica. `.gitignore` excluye archivos de editor, secretos, entornos y copias completas de terceros, sin borrar los locales.
- Incidencias de consulta: guía QSS directa 403, versión oficial indexada con fecha de rastreo anterior; PDF de autor de Ballester falló por certificado sin desactivar TLS. Acceso/editorial parcial identificado, no lectura inventada. Exportaciones PMLR/NeurIPS recuperadas desde sus fuentes reales después de fallos de ruta/formato; reconstrucción final de bibliografía validada. Algún parche documental rechazado no llegó a escribir archivos y se reaplicó con contexto exacto.
- No se escribió manuscrito, publicó, subió datos, eligió licencia, inició inferencia/extracción ni reactivó seguimiento. No hay cálculos activos. Datos originales y TFM de referencia intactos. La auditoría de cierre de esta revisión queda separada en `research/prepaper_2026-09-17/closure_audit.json`; no se sobreescribió el cierre anterior.

**Punto exacto para continuar:** empezar la redacción solo cuando se pida, usando `PAPER_OUTLINE.md`, `PREPAPER_REVIEW.md` y `references/references.bib`. La contribución es la fiabilidad de conclusiones del mapa bajo controles explícitos, no la invención de CKA/vecinos ni un modelo ganador. Mantener visibles errores de fuente, alertas, condicionamiento de candidatos y límites de representación. Antes de enviar: revisión humana de afirmaciones/casos, actualización de normas/literatura, declaraciones reales y depósito reproducible autorizado. No prometer validación temática ni reproducibilidad pública completa mientras falten.

Comprobación final aprobada: 23 copias históricas y 73 archivos de la entrega previa coinciden; 36 fuentes científicas previas siguen intactas; atlas, fuentes/candidatos, diagnóstico de origen y catálogo de presentación pasan sus huellas. Enlaces locales comprobados sin roturas. Búsqueda de patrones de credenciales en el material versionable sin hallazgos; no se imprimieron ni recopilaron claves. `task_plan.md` queda completo. El repositorio sigue local y sin nuevos commits ni push; no hay publicación implícita.

## 2026-09-17 — Primera versión para GitHub, autorizada por el usuario

- Petición expresa de commit y push antes del texto. Comprobados destino público `aleetreny/Shape-of-Science-Robustness`, permisos y ausencia de historial remoto. La carpeta local también partía sin commits/remoto; no hay historial ajeno que sobrescribir.
- Esta versión reúne código, documentación, tablas, figuras, referencias y evidencia auxiliar. Los datos grandes, vectores, pesos, entornos, secretos, archivos del editor y copias completas de terceros permanecen fuera de Git. No se cambió ningún cálculo científico ni se inició redacción.
- Se conserva el cierre de revisión anterior sin sobrescribir: las ocho versiones documentales que cambian para registrar esta publicación están en `research/github_release_2026-09-17/pre_release_documents/`, con huellas en `pre_release_snapshot.json`. Las demás rutas/documentos científicos siguen iguales.
- Verificación de publicación: comprobar que `main` local y `origin/main` coinciden, el árbol de trabajo está limpio y GitHub muestra este mismo commit. El primer commit no puede registrar su propio identificador dentro de sus archivos; consultarlo con `git log -1 --oneline` y `git ls-remote origin refs/heads/main`.

Continuación: redacción cuando se solicite. El código y la entrega legible de esta versión están preparados para GitHub; compartir el corpus/vectores y crear un depósito permanente siguen siendo tareas separadas.

### Publicación comprobada

Commit inicial del estudio: `8c1a9e3105a65f286622cc28284b05c6fcc4dbc2`, árbol `a8ebedae5750ec3ac860284f79d90bd82a014182`, 851 archivos. GitHub confirmó exactamente esos identificadores y el README. `main` es la rama principal y sigue `origin/main`; carpeta limpia tras el envío. Registro: `research/github_release_2026-09-17/publication_verification.json`. Esta actualización posterior solo documenta el cierre.

La transferencia completa fue muy lenta y terminó con HTTP 408. Se resolvió enviando doce lotes mediante ramas temporales y un paquete final de 31.458 bytes que reutilizó los archivos ya recibidos, conforme al [protocolo de Git](https://git-scm.com/docs/gitprotocol-pack). Se conservó el commit original sin modificar datos ni forzar historial. Un intento intermedio por la API de árboles devolvió HTTP 502 y no cambió ninguna referencia. Todas las ramas temporales se verificaron y retiraron después de comprobar `main`. Las credenciales existentes se usaron de forma privada y no se guardaron en archivos ni registros.

El repositorio público contiene código y entregas legibles; no es todavía el depósito del corpus/embeddings necesario para repetir todo el estudio. El manuscrito sigue sin empezar.


## 18-09-2026 — Inicio del piloto de morfología

Estado Git inicial limpio: `main` en `44c9410`, igual a remoto. Leídos planes, decisiones y medidas vigentes. Se aplican planning-with-files, paper-lookup y citation-management. El TFM contiene dispersión al centro, vecinos/hubness, espectro PCA y componentes de un grafo kNN; se inspeccionó solo como referencia. No se ejecuta ni modifica. Entorno existente de análisis: NumPy 2.5.3, SciPy 1.18.1, PyArrow 25.0.1; sin sklearn/networkx. Los 52k de entradas tienen 2.000 por área, 400 por período, con diez modelos y recetas ya guardadas. Se preparará un módulo separado, sin cambiar entornos congelados.


### Piloto: ejecución derivada iniciada

Protocolo y configuración fijados y copiados antes del primer cálculo real: `MORPHOLOGY_PROTOCOL.md`, `config/morphology_pilot_v1.json`. `sos_morphology/metrics.py`, `synthetic.py` y `run.py` separados y congelados en `data/morphology_pilot_v1/source_snapshot/`. Pruebas simuladas aprobadas numéricamente; fallos de interpretación preservados. Preparadas 1.406 selecciones, IDs cruzados con índice auditado, n=2.000 por Field/400 por período y tamaños/control definidos. Ejecutando `.venv-analysis/bin/python -m sos_morphology.run --stage all` con bibliotecas a un hilo; registro `data/morphology_pilot_v1/run.log`. No editar estos programas, configuración ni protocolo durante la ejecución. Solo se leen los vectores existentes.


### Organización del cálculo del piloto

Para usar el equipo sin cambiar fórmulas ni muestras, se sustituyó el ejecutor secuencial por tres procesos locales (un hilo numérico por proceso), cada uno encargado de modelos distintos. El proceso original se interrumpió **después de guardar y verificar el bloque nativo de SPECTER**; los bloques completos se reutilizan. Las funciones científicas congeladas permanecen idénticas. El coordinador separado `sos_morphology/parallel_run.py` guarda su propia huella/copia en `execution_manifest.json`; no se ejecutan dos coordinadores a la vez. Registro vigente: `data/morphology_pilot_v1/parallel.log`.


### Auditoría independiente y bibliografía del piloto

Auditoría matemática adicional sobre datos reales: tres modelos (SPECTER, BERT, MiniLM), dos áreas, 128 artículos por comprobación; ángulos por producto escalar, PR/entropía por SVD, brecha por matriz densa y conectividad por MST/componentes. Además, tres comprobaciones a 2.000 contra las cifras guardadas. Errores <1e−8; invariancia al añadir coordenadas nulas y rechazo de entradas degeneradas comprobados. Fuentes y padres congelados intactos. Evidencia: `data/morphology_pilot_v1/independent_audit.json`.

Biblioteca canónica: 54 entradas, cero errores/duplicados y cinco avisos documentados. Nueve incorporaciones con DOI/exportación editorial y correcciones explícitas; lectura dirigida en `research/morphology_2026-09-18/LITERATURE.md`. Se conservaron doce documentos anteriores desde el commit `44c9410` en `baseline_documents/`. La ejecución sigue en marcha, sin editar sus fuentes.


### Cálculo completo del piloto

Diez modelos, 16.884 conjuntos de medidas: 7.290 nativos/tamaño/selección, 6.500 temporales y 3.094 de controles. Treinta bloques terminados con huellas y auditoría de rangos/identidades. Cálculo coordinado terminado con código 0; se conserva el bloque previo y no se rehicieron embeddings. Ahora se generan tablas/figuras y se contrastan las conclusiones; no declarar cerrada la interpretación por completar la ejecución.

### Piloto de morfología cerrado, 18-09-2026

- Entregados `MORPHOLOGY_RESULTS.md` y `METHODS_MORPHOLOGY.md`, veinte tablas CSV y cinco figuras en PNG/PDF/SVG. Figuras inspeccionadas; se separaron las escalas de tamaño y se precisó que CLS/SEP solo cambian los cuatro BERT. Huellas finales en `reports/morphology_pilot_v1/catalog.json` y revisión visual separada.
- La recomendación es incluir apertura y reparto entre direcciones como propiedades del mapa, con el ejemplo ilustrativo de inversión Artes/Medicina. La conexión permanece como diagnóstico; no se presenta como fragmentación semántica. Cuatro alertas de PR y 51 de conexión siguen visibles y separadas de las anteriores.
- Cerrados controles de medidas alternativas, selección, tamaño, entrada, receta, texto común, MiniLM512, centrado, marcas de calidad, extremos y referencias simuladas. Las limitaciones de interpretación y las comprobaciones añadidas después del protocolo se documentan sin cambiar criterios para aprobarlas.
- Actualizados README, catálogo, guía de reproducción, índice, propuesta de figuras y continuidad. Quince documentos previos conservados desde `44c9410`, ampliando las doce copias iniciales. Biblioteca: 54 registros, cinco avisos sin inventar DOI o páginas ausentes.
- Auditoría de cierre: `research/morphology_2026-09-18/closure_audit.json`. Comprueba fuentes/copiados/padres, 30 bloques, 16.884 conjuntos, cálculos independientes, simulaciones, referencias, tablas/cifras, enlaces y figuras. Corpus, vectores, TFM y programas previos conservados; no hay cálculos activos.
- No se escribió el manuscrito ni se publicó esta ampliación. Git permanece en `44c9410` con los nuevos archivos/cambios locales. Automatizaciones pausadas; sin extracción, nuevos modelos o inferencia.

**Punto exacto para continuar:** entregar al usuario las conclusiones del piloto; cuando pida redactar, usar `PAPER_OUTLINE.md` y los métodos/resultados actuales. La propuesta mantiene cuatro figuras principales y pasa el análisis temporal al suplemento. No reabrir cálculos completados por retomar el chat. La revisión técnica no demuestra verdad temática ni aceptación editorial.

## 18-09-2026 — Inicio del último resumen aceptado

El usuario acepta resumir las 325 parejas de Fields con los resultados de morfología ya guardados. Se aplica la planificación persistente existente. Verificados y copiados los documentos sellados del cierre previo en `research/field_pair_summary_2026-09-18/baseline_documents/`; originales/cierres conservados. Fijados `FIELD_PAIR_PROTOCOL.md` y `config/field_pairs_v1.json` antes de los nuevos recuentos. La inspección de cobertura encuentra las alternativas angulares en todas las selecciones; entropía/D80 solo en principal y repetición 0 de medias muestras/selecciones adicionales. No atribuir a estas últimas repeticiones que no existen.

Siguiente paso: implementación separada `sos_pair_summary/`, prueba de reglas y cálculo exclusivamente a partir de medidas almacenadas. No se han generado nuevos embeddings ni ejecutado cálculos de morfología.

Implementadas y comprobadas las reglas en `sos_pair_summary/`: once pruebas aprobadas, incluidas direcciones persistentes pero diminutas y el requisito de mantener los mismos modelos testigo en un control. Se registran 0/1/5/10% sin elegir por el resultado, alternativas con su cobertura real, panel de seis y exclusión de cada modelo por turno. Se inicia el resumen de medidas existentes; configuración/protocolo y fuentes se congelan antes de producir recuentos.

Resumen completo en menos de un segundo de cálculo derivado. `data/field_pair_summary_v1/audit.json` registra doce tablas, 6.500 decisiones modelo–pareja–propiedad, 5.720 comprobaciones de alineamiento de controles y fuentes/padres congelados. `sos_pair_summary/audit.py` contrasta de forma independiente las reglas mediante cocientes B/A y comprueba 442.000 valores: aprobado. Dos figuras exportadas y revisadas; ajuste de orden vertical/rotulación en el exportador separado. Las cifras completas, alternativas y controles se conservan, incluidos cambios por centrado y magnitudes pequeñas.

### Cierre del resumen final, 18-09-2026

- Entregados `FIELD_PAIR_RESULTS.md`, `METHODS_FIELD_PAIRS.md`, doce tablas y dos figuras en tres formatos. Las 325 parejas aparecen completas para cada propiedad; las cifras son descriptivas del panel/corpus, sin pruebas de independencia ni interpretación semántica.
- Apertura 42/262/21 y PR 54/221/50 (acuerdo de diez/oposición persistente/sin conclusión común). Se conservan 0/1/5/10%: a 5%, contradicciones 96/177; a 10%, 19/126. El criterio no se cambió al inspeccionar resultados. Alternativas conjuntas y seis modelos mantienen casos, con límites claros de cobertura y número de oportunidades.
- Comprobación independiente y once pruebas aprobadas, fuentes/copiados/padres verificados. Figuras finales inspeccionadas: `visual_review.json`; cierre reproducible: `research/field_pair_summary_2026-09-18/closure_audit.json`. Los 36 archivos de presentación anteriores y 18 documentos archivados siguen intactos; no se sobrescribió ninguna auditoría histórica.
- Actualizados README, `AGENTS.md`, decisiones, plan, catálogo, índice, guía y `NEXT_STEPS.md`. `PAPER_OUTLINE.md` propone usar recuentos/magnitudes como cuarta figura y conservar mapas y controles en suplemento; organización final pendiente de hablarla con el usuario.
- Sin cálculos activos, nuevos embeddings, extracción, manuscrito o publicación. Los nuevos archivos son locales; Git sigue en `44c9410`. Automatizaciones previas pausadas.

**Punto exacto de continuación:** conversar sobre la estructura del manuscrito con todas las entregas. La ampliación experimental acordada termina aquí; no ejecutar otros análisis por retomar. Mantener diferencias pequeñas, dependencia del centrado, alertas históricas y etiquetas erróneas como límites visibles.

## 18-09-2026 — Inicio de revisión de estructura y lenguaje en QSS

Verificados y copiados los 21 documentos del cierre previo. Próximo paso: catálogo de QSS, normas vigentes y selección transparente de artículos cercanos. Fuentes completas de terceros se guardarán solo en `data/` excluido de Git. No se han iniciado cálculos ni redacción.

## 18-09-2026 — Revisión de estructura y argumentación de QSS completada

- Recuperados 465 registros Crossref y seleccionados 34 trabajos de 2020–2026. Lectura estructural de 33 y acceso parcial a Donner/Henneken; once lecturas focales adicionales. Se documentan versiones de autor y pérdidas de extracción. Un cuerpo equivocado devuelto por recuperación se excluyó.
- Entrega: `QSS_STRUCTURE_REVIEW.md`; matriz, notas por artículo, catálogo y bibliografía en `research/qss_structure_2026-09-18/`. Bibliografía separada: 34 entradas, cero errores/duplicados y un aviso por volumen ausente de Q34. Las 54 referencias canónicas se conservan.
- `PAPER_OUTLINE.md` reemplaza el esquema anterior por una propuesta aplicada: tres preguntas, seis secciones, cuatro bloques de resultados, cuatro figuras y dos tablas, con presupuesto y correspondencia a salidas existentes. La versión anterior queda archivada. La organización no está todavía aceptada ni es un manuscrito.
- Continuidad actualizada en README, guía, QSS_CHECK, AGENTS, catálogo, decisiones, hallazgos y plan. Normas consultadas mediante índice antiguo; comprobar en directo antes del envío.
- No cálculos científicos, cambios a corpus/vectores/fuentes científicas, publicación o automatizaciones. Las copias completas de terceros solo están en `data/`, excluido de Git. Cierre verificable en `research/qss_structure_2026-09-18/closure_audit.json`.

**Continuación exacta:** conversar sobre la estructura propuesta. Mantener visibles errores de OpenAlex, alertas, límites de interpretación, dependencia del centrado y magnitudes. Redactar solo cuando el usuario lo solicite.

## 18-09-2026 — Inicio del plano de escritura y guía de voz

Cierre editorial anterior verificado y archivado. Localizado el repositorio Portfolio con remoto exacto aleetreny/aleetreny.github.io. Su documentación indica contenido bilingüe con traducción automática durante la edición: hay que distinguir el texto original de traducciones antes de atribuir rasgos al autor. Investigación bibliográfica dirigida iniciada.

## 18-09-2026 — Guía detallada de manuscrito y voz del autor

Petición: detallar estructura y aprender el tono del autor de su repositorio público, investigando escritura que suena artificial. Preparación completada; no se redactó el artículo.

- Conservados 16 documentos de estado y huella del cierre QSS en `research/writing_blueprint_2026-09-18/baseline_documents/` y `baseline_manifest.json`.
- Leídas las 50 entradas españolas publicadas del portfolio, verificado commit remoto y equivalencia con los archivos locales consultados. Inventario, procedencia y notas completas guardados; portfolio de solo lectura. Copias completas y traducciones solo en `data/writing_blueprint_v1/`, fuera de Git.
- Leídas secciones pertinentes de cuatro estudios primarios sobre lenguaje generado, variación y detectores. `STYLE_RESEARCH.md` separa hallazgos, límites y recomendaciones propias. BibTeX independiente validado; DOI y número de artículo completados con fuentes editoriales/Crossref.
- Creados `AUTHOR_VOICE.md` y `MANUSCRIPT_BLUEPRINT.md`: 48 párrafos de trabajo, títulos de todas las secciones, ubicación y especificación de dos tablas/cuatro figuras, ocho bloques de suplemento, citas y límites. `build_support.py` prepara índices desde configuración/resultados guardados; no calcula ciencia.
- Preparadas tablas de paneles/modelos, índice de elementos, presupuesto por párrafo y 23 registros de cifras trazables. Actualizados AGENTS, README, PAPER_OUTLINE, NEXT_STEPS, índice y continuidad. Cierre verificable en `research/writing_blueprint_2026-09-18/closure_audit.json`.

Punto exacto de continuación: esperar a la petición de redacción; entonces leer plano y guía de voz, empezar por métodos/resultados y contrastar el registro inglés en el primer bloque. Título, lista real de autores/declaraciones, maquetación, depósito y envío siguen pendientes. Los resultados, corpus, vectores y cierres científicos se conservan; automatizaciones pausadas. No hubo commit/push.

## 18-09-2026 - Inicio de la maqueta renderizada

Se conserva y verifica el cierre del plano anterior. Se preparan copias de presentación en `manuscript/` y PDFs en `output/pdf/`. No se ejecutan inferencia ni comparaciones científicas. La consulta directa de QSS volvió a fallar; la guía indexada es antigua y requiere comprobación antes del envío.

## 18-09-2026 — Maqueta, tablas y figuras terminadas

- Entregados `manuscript/main.tex`, `supplement.tex`, formato compartido, bibliografía y comando `./manuscript/build.sh`. Los documentos renderizados están en `output/pdf/main.pdf` (14 páginas) y `supplement.pdf` (32 páginas). El texto pendiente se distingue de las leyendas y tablas reales.
- Generadas dos tablas/cuatro figuras principales y 17 grupos de tablas/diez figuras suplementarias. Cada figura tiene PDF, SVG, PNG y TIFF a 300 dpi. Los 98 adjuntos CSV (82 de tablas y 16 de figuras) coinciden con sus fuentes, salvo los resúmenes de procedencia identificados como propios. Manifiestos, filtros y selección disponibles en `manuscript/`.
- Inspeccionadas todas las páginas renderizadas y las figuras. Corregidos solo problemas de presentación: anchuras de tablas, leyenda temporal recortada, salto de índices y encabezados, y un porcentaje sin escapar que ocultaba parte de una nota. Compilación final sin referencias indefinidas ni texto desbordado. La nota de estabilidad vuelve a verse completa.
- Paquete `output/manuscript_source.zip`: 183 archivos, unos 10,8 MB. Se extrajo a una carpeta separada y compiló sin el corpus; ambos PDF coinciden en contenido y huella con la entrega. No se realizó una carga o compilación remota en Overleaf. Tectonic está en una carpeta local excluida de Git; los entornos científicos no se modificaron.
- Auditados paneles, modelos y versiones contra la configuración real, recuentos de las 650 comparaciones, alertas, fuentes y bibliografía. Los 13 documentos históricos copiados, 150 archivos de resultados y cierre anterior permanecen intactos. Evidencia: `research/manuscript_layout_2026-09-18/`.

**Continuación exacta:** revisar la maqueta con el usuario y redactar los bloques que solicite, usando `MANUSCRIPT_BLUEPRINT.md` y `AUTHOR_VOICE.md`. No repetir experimentos por retomar. Título definitivo, autores, declaraciones, depósito, licencia y envío siguen pendientes. No hubo commit/push ni reactivación de automatizaciones.

## 18-09-2026 — Inicio de introducción y antecedentes

Leídas la guía de voz y las dos secciones correspondientes del plano; contrastados los antecedentes próximos con textos primarios y los resultados propios guardados. Se conserva la maqueta anterior y se verifican 150 archivos de resultados antes de editar. Se redactarán únicamente las dos secciones solicitadas, con un objetivo conjunto de unas 1.100 palabras. El PDF y el ZIP se actualizarán después; las auditorías históricas no se sobrescriben.

## 18-09-2026 — Introducción y antecedentes entregados

- `manuscript/main.tex`: dos secciones en prosa, 367 + 627 palabras sin títulos/citas, frente a las 1.550 del presupuesto inicial. Se mantiene el razonamiento de la guía de voz, sin forzar una longitud fija de párrafos. Métodos, resultados, discusión y resumen conservan sus planes.
- `output/pdf/main.pdf`: 17 páginas; texto nuevo en las páginas 3–5. Revisadas las 17 páginas finales. Sin glifos ausentes, referencias indefinidas o texto desbordado. Corregidos un guion largo bibliográfico y una línea inicial de párrafo aislada. La prosa de las dos secciones se revisó contra sus fuentes; registro en `CLAIM_REVIEW.md`.
- Ocho referencias únicas en la apertura, 17 incluyendo la tabla de modelos. Validación sin errores, avisos, duplicados ni claves pendientes. La biblioteca canónica permanece intacta; Held/Velden se añade desde la revisión QSS en `manuscript/context_references.bib`. El validador usa el entorno de auditoría existente, sin instalar dependencias.
- ZIP actualizado de 184 archivos. Se recompiló desde una copia extraída; ambos PDF coinciden por contenido y huella. El suplemento no cambió. Se verificaron 180 archivos de presentación sin cambios, 150 resultados científicos y los 19 documentos históricos archivados; cierre anterior conservado.
- Estado, guía de voz, plano, README e índices actualizados. Evidencia final en `research/manuscript_opening_2026-09-18/`. La maqueta previa y su ZIP permanecen archivados; sin nuevos experimentos, commit/push, publicación o automatizaciones.

**Continuación exacta:** el autor revisa los dos bloques o pide el siguiente. La entrega no autoriza redactar automáticamente otras secciones. Conservar el estilo breve, la cronología exploratoria, las magnitudes y los límites temáticos en el resto del manuscrito.

## 18-09-2026 — Inicio del manuscrito completo y revisión

El usuario autoriza el resto del texto y una revisión editorial/visual completa. Borrador, fuentes de presentación y PDF/ZIP archivados; 150 archivos de resultados previos verificados intactos. Se revisan métodos y cifras antes de escribir. La consulta de datos personales no detiene el trabajo sobre el contenido científico.

## 18-09-2026 — Manuscrito completo y revisión entregados

- Completados `manuscript/main.tex` y `supplement.tex`: seis secciones principales, resumen, declaraciones y ocho bloques suplementarios. Cuerpo de 4.383 palabras, resumen de 190. Los controles y casos extensos quedan en el suplemento sin ocultar las limitaciones centrales.
- Incorporadas las respuestas directas del autor: Alejandro Treny Ortega, investigador independiente, sin financiación externa ni conflictos. Asistencia de Codex declarada; no se inventan correo, ORCID, institución o aprobación personal del borrador.
- Revisados tono, secuencia y repeticiones siguiendo `AUTHOR_VOICE.md`. Cifras contrastadas con 23 registros del plano, tres comprobaciones adicionales y los 217 puntos de la Figura 2. Veintiséis referencias citadas sin errores formales; fuentes y profundidad de lectura reales documentadas en `CLAIM_REVIEW.md`.
- Ajustadas las Figuras 1–3, los resúmenes de tablas y la paginación. Se inspeccionaron las 14 figuras y todas las páginas finales: 19 del cuerpo con referencias y 33 de suplemento. Compilación sin desbordamientos, símbolos ausentes ni referencias indefinidas.
- `output/manuscript_source.zip`: 184 archivos, unos 10,8 MB; extraído y recompilado en otra carpeta con ambos PDF idénticos por huella y texto. No hay carga o compilación remota en Overleaf. Se verificaron 98 adjuntos CSV, veinte documentos históricos archivados y 150 resultados científicos intactos.
- Nueva entrada clara: `MANUSCRIPT_REVIEW.md`; actualizados estado, guía, plano, índices, instrucciones y decisiones. Evidencia completa en `research/manuscript_full_2026-09-18/`, sin sobrescribir los cierres anteriores.

**Punto exacto de continuación:** lectura del borrador por Alejandro y cambios que solicite. Antes de enviar: correspondencia, depósito autorizado del material, licencia y comprobación final de normas QSS. No quedan tareas de redacción dentro de esta entrega. No hubo experimentos nuevos, modificaciones a programas científicos congelados, commit/push, depósito, envío o reactivación de automatizaciones.

## 18-09-2026 — Traducción española entregada

- Traducción completa en `manuscript_es/main.tex` y `supplement.tex`, con la misma organización del original. Incluye resumen, seis secciones, declaraciones y ocho bloques suplementarios. Términos principales aclarados en español, manteniendo el significado científico y sus límites.
- Traducidos 19 grupos de tablas y los rótulos de 14 figuras. Programas separados de presentación; 98 CSV y manifiestos de valores sin cambios. Se verificaron cifras de prosa, tablas y notas, fórmulas, orden de citas y referencias internas.
- PDF españoles en `output/pdf/es/`: 21 páginas principales y 35 suplementarias, todas inspeccionadas. Ajustados encabezados, anchuras, signos de interrogación y etiquetas de la Figura 1. Sin desbordamientos, símbolos ausentes o referencias indefinidas.
- `output/manuscript_source_es.zip`: 188 archivos; extraído y recompilado con PDF idénticos por huella y texto. El original inglés, sus PDF/ZIP y el cierre editorial previo permanecen intactos: 188 archivos verificados.
- Entrada para el autor: `MANUSCRIPT_SPANISH.md`. Auditoría en `research/manuscript_spanish_2026-09-18/`. Actualizados instrucciones, estado, índices y registro de decisiones; no hubo cálculos científicos, commit/push, publicación ni reactivación de automatizaciones.

**Continuación exacta:** el autor lee la copia española y señala secciones o frases. Aplicar después los cambios que pida y mantener las dos versiones alineadas; no sustituir automáticamente el original inglés ni dar por aprobado el manuscrito.

## 18-09-2026 — Cinco comentarios del autor incorporados

- Título actualizado en portada, suplemento y metadatos, en inglés y español. Tabla 1 con separación entre filas; Tabla 2 con celdas centradas verticalmente y cifras a mitad del nombre de dos líneas.
- Figura 1B sustituida por medias etiquetadas y dispersión descriptiva de las mismas comparaciones guardadas. Se mantienen escala 0–1, valores originales y límites. Pie sincronizado en ambos idiomas. Declaración de IA acortada a dos frases.
- Revisadas todas las páginas de los artículos principales; portada de cada suplemento inspeccionada y resto de páginas idénticas píxel a píxel a las copias previas. Cuatro PDF: 19/33 páginas inglesas y 21/35 españolas, sin desbordamientos ni referencias indefinidas.
- Los dos ZIP actualizados se extrajeron y recompilaron: 184 archivos ingleses y 188 españoles; cuatro PDF exactamente iguales a los entregados. Se conservan cifras, fórmulas, citas, tablas, 98 CSV por idioma y 211 archivos de informes científicos. Las 389 copias previas están archivadas.
- Guía nueva: `MANUSCRIPT_COMMENTS.md`. Evidencia independiente en `research/manuscript_comments_2026-09-18/`; las auditorías anteriores mantienen su estado histórico. Documentos de continuidad sincronizados.

**Continuación exacta:** el autor sigue revisando el texto. Los cinco comentarios están resueltos; la aprobación completa sigue pendiente. No se ejecutaron nuevos experimentos ni se publicó el material.

## 19-09-2026 — Tres voces completas preparadas para elección

- Título actual aceptado por el autor y conservado en las seis opciones.
- Redactadas V1 directa y sobria, V2 razonamiento propio y V3 voz marcada y reflexiva, en inglés y español. Cada opción incluye el artículo principal completo; se reescriben 30/33/35 párrafos por idioma. El suplemento técnico es común.
- PDF en output/pdf/voice_variants/: 19 páginas por versión inglesa y 21 por española. Revisadas las 120 páginas, las tablas y las cuatro figuras comunes. No se observaron pérdidas de texto, recortes o símbolos ausentes; algunas notas españolas continúan en otra página al cambiar la longitud.
- Comprobadas cifras y fórmulas por párrafo, asociación de citas, estructura, traducción y declaraciones. Conservados 751 archivos previos del manuscrito, informes, bibliografía y entregas.
- Paquete output/manuscript_voice_variants_source.zip: 93 archivos, 681.126 bytes. Extraído en otra carpeta y recompilado: seis PDF exactamente iguales a los entregados.
- Guía para comparar: MANUSCRIPT_VOICES.md. Fuentes: manuscript_variants/. Auditorías y revisión del significado: research/manuscript_voices_2026-09-19/. Actualizados instrucciones, voz, plano, índices y continuidad.

**Punto exacto de continuación:** elegir una opción o recoger cambios del autor. Se recomienda V2, pero no está elegida. Los originales siguen siendo canónicos; no se ha aprobado el manuscrito, publicado material ni ejecutado otros análisis.


## 20-09-2026 — V2 elegida y explicación clara entregada

- Decisión directa del autor: V2 es la orientación elegida. Pide claridad por encima de vocabulario culto o construcciones densas; queda registrada en AGENTS.md y AUTHOR_VOICE.md para cualquier continuación. No equivale a aprobación final.
- Reescritas las seis secciones y el resumen en inglés y español. Cada comparación se presenta por su propósito; se explica la relación entre los 500.000 de partida, los 52.000 de texto con 26.000 incluidos y los otros 52.000 del fragmento común. La geometría reutiliza el conjunto del experimento de texto.
- Tabla 1 organizada por finalidad; conceptos explicados antes de sus nombres; pies de figura más orientativos. El resumen explica el acuerdo local como unos ocho artículos de 25 y evita recuentos de parejas sin contexto. La fórmula PR sigue explícita en S6.
- Inglés: 3.989 palabras de cuerpo y resumen de 192; 19 páginas. Español: 4.592 y 199; 20 páginas. Suplementos: 34/36 páginas. Se han revisado las 109 páginas, la correspondencia de cifras/fórmulas/citas y los límites.
- Dos paquetes fuente de 186/190 archivos reproducen exactamente los cuatro PDF. Las tablas principales conservan su nueva explicación al reexportar; comprobados también los 19 grupos de tablas españoles en una copia separada.
- Conservados 393 archivos de la edición anterior y 472 archivos protegidos de resultados, referencias y alternativas. Datos de presentación, figuras y bibliografías sin cambios. No se ejecutaron experimentos, descarga, inferencia, publicación ni automatización.
- Entrega: MANUSCRIPT_CLARITY.md; evidencia en research/manuscript_clarity_2026-09-20/. Continuar con los comentarios sobre la lectura, sin volver a pedir una elección de voz.
