# Evidencia y fuentes

## Revisión vigente antes del manuscrito, 17-09-2026

- Informe: [PREPAPER_REVIEW.md](PREPAPER_REVIEW.md). Quince componentes científicos revalidados; seis comparaciones de forma reconstruidas con otra fórmula y 300 consultas ordenadas de forma independiente coinciden. Pasan 32 pruebas en el entorno de análisis y 20 en el de embeddings. No hubo inferencia nueva.
- [Atlas de casos](CASE_ATLAS.md): 217 especialidades; posiciones contrastadas en las mismas 183 bajo 27 condiciones. Tecnología de medios, construcción y renovables mantienen posiciones altas; álgebra, estudios religiosos e historia, bajas. Esto no elimina las alertas de precisión de forma ni valida las etiquetas.
- Una relación SIRT6–sirtuinas/inflamación aparece en los 25 vecinos de los diez modelos en diez repeticiones. Una relación entre capas de sílice/cobalto y películas cerámicas aparece en seis modelos y en ninguno de los cuatro BERT de palabras con mean. Ambas son ejemplos seleccionados, no estimaciones de frecuencia mundial.
- Los 500.000 IDs/huellas y etiquetas están alineados; 30 registros ilustrados coinciden con las páginas originales de OpenAlex. Entre los extremos hay una descripción de un libro de brujería clasificada en Física, una pieza sobre invasión bacteriana en Política y un aviso. Son fallos de la fuente confirmados, no fallos de cruce de filas. Un abstract de destino empieza incompleto y está anotado.
- Diagnóstico posterior de títulos genéricos: 82/500k; 67 no tenían marcas estrictas previas. Retirar cinco consultas entre 10.850 cambia el promedio equilibrado por especialidad de 45,344% a 45,349%. Candidatos intactos. **No estima los errores de clasificación temática**; las conclusiones siguen condicionadas a OpenAlex.
- La comparación emparejada Field/Subfield conserva 50 consultas del mismo Subfield en ambas búsquedas de 256; la búsqueda amplia está condicionada, no es una selección libre del Field. Se aclara el método sin alterar resultados.
- [Biblioteca canónica](references/README.md): 45 entradas verificadas; una advertencia documentada de páginas ICLR, cero errores/duplicados. Corregidos autores de Ahlgren/Colliander, DOI atribuido a Lamers, páginas de SciBERT/SemCSE y versiones editoriales. Lectura y acceso diferenciados por fuente.
- [Antecedentes próximos](references/RELATED_WORK.md) delimitan el hueco: fiabilidad de conclusiones sobre mapas científicos con controles explícitos. Comparar embeddings, inputs, geometría y vecinos ya tiene antecedentes. No reclamar prioridad absoluta.
- QSS: acceso directo 403; normas oficiales indexadas consultadas, pendientes de actualización antes del envío. Datos/código siguen locales sin depósito permanente ni licencia general elegida. [Lista de preparación](docs/QSS_CHECK.md).

La documentación anterior se conserva como historial. Estado y continuación: [NEXT_STEPS.md](NEXT_STEPS.md).

## Lo comprobado antes de esta revisión

- `INVENTORY.md`: corpus completo de 2.378.036 papers y SPECTER2; correspondencia de IDs verificada; archivos en `/Users/alejandrotreny/Workspace/Mapping-Science`.
- `FIELD_COUNTS.csv`: recuentos locales de los 26 Fields y comparación con conteos históricos de OpenAlex.
- `FIELD_SAMPLING.md`: propuesta anterior, **no aprobada**. Sus cifras de disponibilidad son útiles; su recomendación de 5.000 no está justificada como tamaño final.
- Conteos históricos 2000–2024: 71.667.731 trabajos clasificados, artículos/preprints en inglés con abstract, sin retractados/paratext. Antes de ciertos filtros locales de calidad textual. No confundir con recuentos actuales.

## Comprobaciones del 2026-09-14

- La clave OpenAlex ya existe en el entorno privado del TFM y funciona. No se copió ni mostró.
- Primera consulta actual: 326.269.690 trabajos en el corpus predeterminado de OpenAlex. Consulta de referencia 2000–2024, artículo/preprint, inglés, abstract, sin retractados/paratext: `meta.count=61.079.645`; devuelve 26 grupos Field. La documentación actual distingue el corpus principal de una ampliación opcional; las consultas iniciales usan el predeterminado.
- Respuestas y parámetros sin clave guardados en `research/openalex_counts_2026-09-14/`.
- Reconciliación: 61.061.439 tienen uno de los 26 Fields; 18.206 no tienen Field, confirmado por consulta `primary_topic.field.id:null`. Los 25 recuentos anuales suman 61.079.645.
- Antes de tipo/idioma/abstract, con 2000–2024 y exclusión de retractados/paratext, OpenAlex devuelve 201.706.981. No confundir el total con la suma de Fields conocidos.
- Veterinaria: 101.802 candidatos con los filtros básicos anteriores, frente a 19.573 locales. Todavía falta limpieza; no es un recuento garantizado de textos válidos.
- La consulta por tipo encuentra además 9.022.151 `conference-paper` en inglés con abstract, 2000–2024, sin retractados/paratext. Reconsiderar explícitamente su inclusión para evitar recortar informática/ingeniería. No se ha aprobado todavía cambiar los tipos del corpus.
- Como referencia fuera del período anterior: 4.026.794 candidatos en 2025 y 2.461.082 en 2026. El año 2026 está incompleto; no se ha cerrado el período final.
- Boyack et al. (2011) comparan nueve métodos en 2.153.769 documentos de 2004–2008, seleccionados por disponibilidad de texto, MeSH y referencias. Fuente: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0018029 . Evidencia de que una comparación puede usar millones; no establece un reparto universal entre Fields.
- Imel y Hafen (2025), preprint, comparan cinco representaciones en unas 53.000 publicaciones de nueve disciplinas. Métodos consultados en https://arxiv.org/html/2506.23366v1 .
- Métodos de Imel y Hafen ya leídos: parten de al menos 30.000 por disciplina, seleccionados expandiendo una red desde un paper inicial según semejanza SciBERT; conservan 53.080 papers, entre 4.114 y 7.556 por disciplina, tras exigir estabilidad de vecinos. Su visualización sí usa 1.000 por disciplina. No son muestra aleatoria global ni ejemplo de igualdad obligatoria; copiar una selección guiada por un modelo sería problemático para nuestro objetivo. Ellos explican que el tamaño también dependió de conveniencia de acceso.
- González-Márquez et al. (2024): el cuerpo del artículo publicado confirma 20.687.150 papers tras limpieza. Algunos ensayos usan un subconjunto de un millón y varias medidas usan selecciones aleatorias menores para evaluar; no confundir esas cantidades con el corpus completo. Fuente editorial: https://doi.org/10.1016/j.patter.2024.100968 .
- Texto completo editorial obtenido con Europe PMC y comprobado con el lector JATS de paper-lookup: `research/literature/landscape_2024.xml`. Contiene cuerpo completo, no solo resumen.
- Lakens (2022), https://doi.org/10.1525/collabra.33267 , distingue justificaciones por población completa, recursos, potencia, precisión y reglas prácticas. Apoya justificar tamaño según la información requerida; no proporciona un número universal para este proyecto ni una fórmula específica de CKA/kNN.
- Ampliar el filtro a article/preprint/conference-paper da 70.101.796 candidatos en 2000–2024; 70.050.675 con uno de los 26 Fields. Se guardó la consulta separada, sin alterar el corpus ni aceptar aún ese cambio.
- Se verificaron las 650 celdas Field×año de la referencia básica: 25 años por Field, cada suma coincide con su total y todas suman 61.061.439. CSV por Field y por Field/año en `research/openalex_counts_2026-09-14/`.
- Comprobación posterior de `corpus=all`: 474.716.562 trabajos en el catálogo ampliado completo; 73.176.918 clasificados con filtros básicos y 82.760.353 con congresos. Se guardaron tres respuestas adicionales y columnas por Field. No se calculó el desglose anual de la ampliación ni se aprobó incluirla. Total: 37 respuestas API. La diferencia de catálogos no está demostrada como explicación de las diferencias con el TFM.
- Statistics Canada diferencia asignación proporcional, igual y orientada a precisión de grupos: https://www150.statcan.gc.ca/n1/pub/12-001-x/2017001/article/14817/03-eng.htm . No establece un único reparto óptimo independiente del objetivo.

## Interpretación y límites

> Actualización posterior: la recomendación de esta sección fue sustituida por la decisión explícitamente delegada de `CORPUS_PROTOCOL.md`. El historial se conserva; los resultados nuevos están en la sección final y en el informe de pruebas.

- `FIELD_SAMPLING.md` reúne la recomendación revisada; es una propuesta, no una decisión aceptada. Base proporcional para el resultado conjunto y complemento donde haga falta precisión por Field. Tamaño a justificar con una regla previa y una prueba; no un techo igual para todos.
- Conservar proporciones por año representa la literatura del período; igualarlas representa otro objetivo. Ninguna de esas elecciones elimina todos los efectos temporales automáticamente.
- `OPENALEX_COUNTS.md` contiene los 26 Fields, filtros y límites. Los recuentos API no incorporan toda la limpieza local. No se ha establecido por qué difieren de los históricos del TFM.
- No se hicieron nuevos experimentos ni una descarga masiva. Ambos checkouts anteriores siguen sin cambios según Git. Se comprobaron los enlaces locales y la ausencia de la clave API en los nuevos archivos.

## Herramientas utilizadas

Organización mediante planning-with-files; consulta y lectura de artículos mediante paper-lookup y su lector JATS. Referencia de este último, como herramienta de apoyo y no como evidencia del diseño: Kassis, T., Agarwal, V., He, Y., Patel, D., y Brueckner, A. M. (2026). *Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*. https://doi.org/10.48550/arXiv.2609.00065 . Metadatos comprobados en arXiv el 14-09-2026, versión vigente v2; sin publicación editorial indicada.

## Incidencias de acceso

- DOI de Lamers devuelve 403; se localizó una versión abierta en el repositorio de la Universidad de Bolonia, sin cambiar el artículo solicitado.
- PMC mostró una comprobación de navegador; se consultan fuentes abiertas alternativas y editorial.
- Python del TFM avisa de LibreSSL antiguo; las primeras consultas HTTPS terminaron correctamente. No se modificó el entorno.
- Un segundo acceso web a Statistics Canada agotó el tiempo, después de haber leído la página correctamente. El enlace antiguo de documentación OpenAlex redirige al centro de ayuda nuevo; se consultó su referencia actual.
- Una edición de Markdown falló por intentar borrar y crear el mismo archivo en un único parche. Se repitió como actualización, correctamente; la propuesta anterior se conservó antes de reemplazarla.

## Decisión delegada y pruebas del 14-09-2026

- El usuario delegó el tamaño y reparto del corpus de preparación y autorizó pruebas. Se registró en `AGENTS.md` la regla general: autonomía científica solo con delegación explícita, explicación posterior, opciones y pregunta en los demás casos.
- Hardware comprobado: M5 Pro, 18 núcleos CPU, 48 GiB. Entorno aislado `.venv-benchmark`, pesos en `.benchmark-models`, sin cambiar el TFM. Se aplicó la guía hf-cli para descargar versiones fijadas de dos modelos públicos, sin autenticación implícita.
- Pruebas: 36 consultas API en esta fase (27 recuentos y 9 páginas), hasta 900 registros; 512 textos por modelo para medir velocidad; 15.780 textos adicionales de cuatro combinaciones área/período para una criba de tamaño frente a SPECTER2 heredado; búsqueda de vecinos para 256 consultas sobre 500.000 vectores reales.
- Evidencia y límites detallados en `research/feasibility_2026-09-14/RESULTS.md`. El par SciNCL/SPECTER2 pasó las cuatro cribas, con criterios fijados antes de calcular resultados. No prueba suficiencia de todos los Fields ni de modelos sin examinar. Los rangos son condicionales a las bases de prueba, no intervalos poblacionales.
- Velocidad SciNCL ~50,5 papers/s, MPNet ~64,6. La prueba de 15.780 sostuvo ~50,5 papers/s durante unos 312 segundos. Escenario de 500.000: 2,1–2,8 horas ideales por modelo; presupuesto 3–6 por modelo comparable. Una matriz de 768 dimensiones y 32 bits: 1,43 GiB. No materializar todas las distancias.
- Nueva población decidida: catálogo principal, 2000–2024, article/review/conference-paper, inglés, abstract reconstruible ≥50 palabras y título no vacío; exclusiones y clasificación en protocolo. Cuenta API antes de limpiar: 67.202.824. Prueba general: 357/400 pasan ≥50, 315/400 pasan ≥80. Solo 4/400 coinciden con IDs locales; no extrapolar un gran ahorro de descarga por reutilización.
- Decisión: 500.000 válidos = 400.000 base aleatoria general + 100.000 complemento automático a celdas Field×quinquenio menos numerosas. Los porcentajes de base no se fijan con recuentos anteriores a limpiar. Cinco períodos, 26 Fields. Proyección mínima por celda ~2.200, cantidades exactas después de limpiar la base.
- Nuevas fuentes: versión de autores del artículo de Constantino et al. publicado en QSS, https://arxiv.org/html/2308.15706v2 (red 452.096, abstracts 159.375); modelos https://huggingface.co/malteos/scincl y https://huggingface.co/sentence-transformers/all-mpnet-base-v2 ; CKA https://proceedings.mlr.press/v97/kornblith19a.html ; parámetros y muestreo API https://help.openalex.org/api/llm-quick-reference/ . No hay un mínimo editorial inferido de esos tamaños.
- Incidencias: rutas editoriales QSS devolvieron 403 o no se pudieron abrir; se leyó la versión de autores. La ruta adivinada de muestreo OpenAlex no abrió; se utilizó la referencia oficial disponible. Transformers avisó de longitud sin truncar al contar tokens; la inferencia sí aplicó truncamiento 512/384. No hubo fallos de ejecución de las pruebas finales.

## Extractor preparado y probado, 15-09-2026

- Evidencia de ejecución, recuperación, revisión y límites en `research/download_validation_2026-09-15/RESULTS.md`; resultado automático en `verification.json`. No se repite aquí el detalle.
- Confirmadas 21 pruebas offline y una prueba real final de 124 IDs únicos (120+4), pausada y reanudada. Estado de producción: no iniciado desde el asistente. El usuario lo lanzará con `./download.sh`.
- La prueba real verifica también `Authorization: Bearer` y la selección paginada con semilla. Al reanudar se solicitan solo IDs de páginas anteriores. Documentación vigente: https://help.openalex.org/api/authentication/ y https://help.openalex.org/api/paging/ .
- Importante para futuros cambios: `meta.count` con `sample` no es el número de trabajos de la población. El detector de agotamiento no debe interpretar `count == sample` como censo.
- El aviso `pyenv` procede de la configuración general de la terminal. El programa usa `.venv/bin/python` explícitamente y funciona sin modificar esa configuración.

## Auditoría de producción en marcha, 15-09-2026

- Se comprueban en lectura todas las páginas y todos los registros seleccionados, y se reproduce su selección; no se modifica el extractor. `scripts/audit_corpus.py --watch`, evidencia en `research/corpus_audit_2026-09-15/`.
- Hallazgos confirmados por lectura del texto: abstracts en coreano/ucraniano con metadato `language=en`; títulos WITHDRAWN/RETRACTED con `is_retracted=false`; descripciones de revistas o mensajes de error DOI guardados como abstract. Ejemplos y grupos repetidos quedan identificados. No confundir estas incidencias de origen con corrupción de la descarga.
- Para medir el idioma del abstract se utiliza fastText lid.176.bin en `.venv-audit`, separado del entorno de descarga. Modelo oficial, versión completa de 126 MB, huella y licencia en `language_model.json`. Predicciones diagnósticas sobre título y abstract por separado; sin eliminar, traducir o sustituir trabajos ni aprobar umbrales de exclusión.
- OpenAlex documenta que `language` es una estimación automática sobre metadatos, no necesariamente el idioma del texto completo, y que los abstracts pueden contener texto extra procedente de páginas. Fuente consultada: https://help.openalex.org/data/works/attributes/ . Documentación del detector: https://fasttext.cc/docs/en/language-identification.html . Estos límites respaldan comprobar el texto recibido, no prometer metadatos perfectos.
- La implementación independiente del reparto (nivel común y desempate por celda) coincide con la del extractor en 50 casos generados con semilla, con y sin celdas agotadas. Además se contrastará el reparto real final.

## Resultado definitivo de la auditoría, 15-09-2026

- Resumen y utilidad en `AUDIT.md`; evidencia completa en `research/corpus_audit_2026-09-15/final_validation.json`, con huella Parquet coincidente con la validación del extractor. Se comprobaron todos los 500.000 registros, no una muestra.
- `readiness.json` distingue integridad aprobada de calidad de metadatos pendiente de limpieza. `language_alignment.json` verifica que los 500.000 diagnósticos corresponden a los mismos IDs, orden y textos del corpus.
- 22.118 vectores históricos candidatos comprobados individualmente en sus shards, todos finitos y no nulos, y alineados con los IDs de sus metadatos. Evidencia: `legacy_embedding_summary.json` y `legacy_embedding_candidates.parquet`. No demuestra procedencia exacta del modelo ni aprueba su reutilización final.
- Figuras inspeccionadas y recuentos por Field, año/período y conjunto disponibles. El resultado no demuestra estabilidad de las métricas o representatividad de idiomas/publicaciones fuera de la población definida.

## Limpieza: evidencia de reglas, 15-09-2026

- Los 166 textos de páginas detectados corresponden exactamente a seis abstracts distintos; se han leído completos. Se usará coincidencia del texto completo normalizado, no borrar cualquier abstract que comparta el comienzo.
- Una puntuación global fastText ≥0,9 puede corresponder a un abstract bilingüe con un bloque completo en inglés. Se preparan comprobaciones por tres secciones para conservar y marcar esos casos, a falta de cerrar el criterio consultado.
- Fuentes comprobadas: https://fasttext.cc/docs/en/language-identification.html , https://help.openalex.org/data/works/attributes/ , https://help.openalex.org/api/llm-quick-reference/ . La ruta supuesta `/api/sample/` no abrió; la referencia oficial general sí documenta muestra/semilla/límites.

- Ampliación durante limpieza: revisión de los 286 grupos de abstract idéntico del original, no solo las primeras seis familias. Aparecen más textos de páginas, instrucciones, anuncios y recursos ajenos a artículos. Se pausó el primer recorrido antes de publicarlo como limpio. La configuración final incorporará coincidencias completas comprobadas y casos de texto asignado al artículo equivocado, conservando la evidencia del primer recorrido y sin modificar originales.

## Preparación final verificada, 15-09-2026

- Evidencia vigente: `research/cleaning_2026-09-15/final_validation.json`, `quality_recheck.json`, `readiness.json`; explicación y límites en `CLEANING.md`. Son los resultados de la copia final, no de los tres recorridos provisionales archivados.
- 500.000 IDs distintos, 400.000 base y 100.000 complemento; 26 Fields, 130 celdas con mínimo 2.165 y 650 combinaciones Field/año. Todos los registros y filas coinciden con las respuestas guardadas; selección y decisiones reproducidas.
- Se apartaron 5.776 originales por reglas de calidad y 123 válidos dejaron de entrar al recalcular el reparto. La limpieza afecta de forma diferente a las áreas: CSV `cleaning_impact_by_field.csv`; estas tasas no se extrapolan como tasas de error de OpenAlex.
- 499.990 registros finales proceden de páginas originales y diez de una sola página adicional de 100 candidatos. La segunda comprobación detectó un fallo de aplicación de las firmas a esa página nueva, se corrigió con prueba de regresión y se reconstruyó sin más consultas. Ver `content_regression_fix.json` y `tests.txt`.
- Predicciones de idioma ejecutadas de nuevo sobre los 500.000, sin discrepancias. Quedan 9.883 ambiguos, incluidos posibles casos mixtos; 3.002 tienen etiquetas distintas entre partes. Las partes solo se examinan cuando la primera etiqueta global no es inglés: no se detectan necesariamente todos los casos bilingües. No son probabilidades calibradas ni una validación humana independiente.
- Las inspecciones de 286 grupos de abstract repetido, estructuras en todas las páginas guardadas, 30 ejemplos de idioma y los diez nuevos textos apoyan la limpieza operativa; no demuestran haber encontrado todos los errores semánticos. Se mantienen marcas y límites explícitos.
- 22.118 vectores antiguos con texto exacto localizados y comprobados numéricamente de nuevo; sin aprobación de uso final por versiones no identificadas. La lista de IDs y textos ya está fija; modelos y formatos siguen pendientes.

## Reparto y revisión de modelos, 15-09-2026

- Evidencia nueva en `research/model_review_2026-09-15/`: recuentos directos del Parquet final, huella del archivo, concordancia con las tablas previas, porcentajes con denominadores separados y escenario de marcas contadas sin duplicar registros. Explicación en `CORPUS_BALANCE.md`.
- 12 combinaciones área/período tienen 2.165; otras 68, 2.166. El mínimo anual, 282, no es el mínimo del período de cinco años. La composición final refuerza áreas pequeñas y no debe presentarse como el peso poblacional de cada Field.
- Matemáticas 2000–2004 quedaría hipotéticamente en 1.376 al omitir idioma dudoso o resúmenes de 50–79 palabras; Artes/Humanidades 2000–2004 tiene 10,62 % de idioma dudoso. Son diagnósticos para controles futuros, no etiquetas de error confirmado ni exclusiones nuevas.
- Revisión primaria y recomendación sin aprobar en `MODEL_SELECTION.md`. SPECTER2 requiere identificar base/adaptador; SemCSE_cosine tiene una receta distinta de SemCSE principal; MPNet de uso general incluye datos científicos en su entrenamiento; Qwen3-Embedding-0.6B aporta una arquitectura distinta con coste local todavía desconocido. No tratar ciencia/general como una intervención causal aislada.
- Antecedentes comprobados: Imel/Hafen ya comparan cinco representaciones; SemCSE compara modelos científicos y generales; SemCSE-Multi plantea mapas de distintos aspectos. La revisión dirigida no establece prioridad del proyecto. Consulta exacta y niveles de lectura documentados en el informe.
- SemCSE confirmado como artículo EMNLP 2025, DOI 10.18653/v1/2025.emnlp-main.1662. La búsqueda Crossref por título de Imel/Hafen solo devolvió tres trabajos diferentes; se conserva como consulta no concluyente. No se inventa una publicación editorial a partir del preprint.

## Uso académico de modelos: revisión ampliada, 15-09-2026

- Evidencia, protocolo de conteo y límites en `ACADEMIC_MODEL_USAGE.md`; registro por estudio y frecuencias en `research/model_review_2026-09-15/academic_sources/`. Diez trabajos de mapas, estructura, relaciones bibliométricas o evolución temática; revisión dirigida, no muestra representativa de la literatura.
- SPECTER/SciBERT: cinco estudios cada uno; BERT/MPNet/MiniLM: tres; SciNCL: dos. MPNet incluye dos variantes distintas. La unión general MPNet/MiniLM/SBERT sin identificar aparece en seis, sin duplicar Huang. Versiones de una misma publicación se cuentan una vez.
- Liang compara cuatro científicos en mapeo de PubMed; sus E5/Ada/BERT se evalúan en otra tarea. Imel excluye expresamente SPECTER; Cosmos describe SciBERT como antecesor, no otro modelo usado. El artículo de emergencia interdisciplinar ejecuta MiniLM y solo menciona MPNet. Bascur llama BERT a una red hecha con SPECTER. Estos casos evitan inflar frecuencias.
- PubMedBERT/BioBERT/SimCSE aparecen en el mapa biomédico o su comparación previa. No se afirma que tengan adopción general en los 26 Fields. La misma revisión no permite llamar habituales en mapeo a Qwen/BGE/Gemma/GTE/Jina.
- Corregida referencia equivocada de Lamers en bibliografía tras consulta Crossref: qss_a_00168 corresponde a Twitter/opioides. Registro ISSI de Lamers confirmado; PDF inaccesible en esta consulta. Huang confirmado mediante código de autores y fragmentos editoriales, no por lectura editorial completa.
- PubMedBERT está renombrado como BiomedBERT según la ficha oficial de Microsoft. Fijar la variante abstract-fulltext y resolver revisión/equivalencia antes de usarla. SemCSE-Multi ya tiene publicación ACL 2026; solo se comprobaron resumen/metadatos editoriales.

## Preparación de diez modelos, 15-09-2026

- Aceptados los diez y la combinación de uso habitual + control de fragmento común. El usuario inicia el cálculo completo; las pruebas técnicas pequeñas siguen autorizadas.
- `./prepare.sh preflight` vuelve a pasar. Los manifiestos de limpieza son históricos e inmutables; los nuevos estados se guardan por modelo.
- Revisiones fijadas en `config/embeddings_v1.json`; todos los archivos de once repositorios (diez modelos y un adaptador) comprobados contra identificadores del autor. Se reutilizan SciNCL/MPNet de la caché existente.
- Las fichas confirman 512 piezas de texto para los BERT científicos/generales, 384 para MPNet y 256 para MiniLM. El límite de arquitectura de MiniLM (512) no se confunde con su configuración de uso (256). BioBERT conserva mayúsculas; no se fuerza minúscula.
- Fuente primaria de recetas: repositorios/model cards enlazados en `MODEL_SELECTION.md`. SimCSE no supervisado recomienda CLS antes de la capa de ajuste. SPECTER2 requiere base + adaptador de proximidad.
- Corrección de una hipótesis de esta sesión: Landscape 2024 eligió SEP para PubMedBERT, no media. El XML original compara media, CLS y SEP. Se conservan las tres salidas para cuatro modelos de palabras sin seleccionar a posteriori la que dé un resultado atractivo. La principal queda abierta hasta acordar los análisis.
- Evidencia operativa en `research/embedding_setup_2026-09-15/`. Doce pruebas de almacenamiento pasaron; ampliadas después a política de entrada y fragmentos comunes. Fallos iniciales esperados guardados. Un primer parche de documentos no se aplicó por contexto inexistente en findings.md; se corrigió sin cambiar el corpus.

- Cierre de las pruebas: `research/embedding_setup_2026-09-15/verification.json` verifica diez modelos × dos entradas × 1.300 filas, finitud/dimensiones, alineación y los 678 textos sin cambios entre entradas. Ningún recorte adicional en el control común. Diecisiete pruebas pasan en `tests_all.txt`.
- Tiempos medidos y extrapolación (24,14 h; margen comunicado 25–35 h), almacenamiento y límites en `research/embedding_setup_2026-09-15/RESULTS.md`. Se comprobó la ausencia de cálculo completo y se conserva el corpus original.

## Progreso y revisión programada, 16-09-2026

- A las 23:31 de Madrid: siete modelos completos, con validaciones guardadas y manifiestos coincidentes; PubMedBERT activo en 209.920 filas. Programa y configuración coinciden con lo congelado. La velocidad de sus últimos veinte bloques es 46,36 artículos/s; sumada a las pruebas de los dos modelos pendientes, da 7,42 horas restantes sin pausas. Estimación orientativa 7–9 h.
- Evidencia en `research/embedding_review_2026-09-16/progress_snapshot.json`; no se presenta esta comprobación de avance como auditoría final de todos los valores.
- Seguimiento temporal creado/verificado en este hilo, primera revisión dentro de cinco horas, y plan concreto en `POST_EMBEDDING_REVIEW.md`. Los datos/programas activos siguen intactos. Se revisará y organizará mediante índices y documentación antes de cerrar las decisiones científicas pendientes.

## Auditoría final de los diez modelos, 17-09-2026

- `EMBEDDINGS_AUDIT.md` resume la revisión completa, con evidencia en `research/embedding_final_audit_2026-09-17/`. Diez × 500.000, 18 variantes, 8.802 archivos de vectores y 4.890 bloques. Corpus, IDs/orden/textos, valores, dimensiones, huellas, pesos, programa guardado y entorno comprobados. Sin bloques incompletos encontrados.
- Recortes desiguales: MiniLM 49,582%, MPNet 20,1598%; resto entre 4,7456% y 9,0032%. Se conservan tablas por Field, período y base/complemento. El porcentaje cuenta artículos afectados, no longitud perdida. No se interpreta como corrupción de datos ni se cambia el protocolo.
- Control técnico: 1.300 por modelo, sin recorte adicional; 678 textos sin cambio reproducen las 18 salidas dentro de tolerancias numéricas. No demuestra precisión suficiente del control para el paper.
- Organización sin mover originales: `DATA_CATALOG.md`, catálogo JSON/CSV, índice ligero de 45 MB y `sos_analysis/`. Ocho pruebas de lectura/errores aprobadas; pasada real sobre todas las variantes, máximo observado 716.455.936 bytes de memoria. No se calcularon medidas de comparación entre modelos.
- Propuesta pendiente `ANALYSIS_PROPOSAL.md`: una medida general y coincidencia de vecinos como complemento. Referencia primaria CKA consultada: https://proceedings.mlr.press/v97/kornblith19a.html ; antecedente geométrico relacionado: https://arxiv.org/html/2506.23366v1 . No son una justificación del tamaño final del control o de un umbral de similitud.

## Inicio de la comparación, 17-09-2026

Búsqueda dirigida de fuentes primarias: aparecen Generalized Shape Metrics on Neural Representations (Williams et al., 2021), Grounding Representation Similarity with Statistical Testing (Ding et al., 2021), Reliability of CKA (2022) y ReSi (ICLR 2025). Deben leerse antes de decidir: CKA no mide todas las propiedades y otras medidas también tienen límites. No se ha elegido una métrica según nuestros resultados. MiniLM: contrastar límite habitual con capacidad posicional; no cambiar silenciosamente la receta oficial.

MiniLM comprobado localmente en la revisión fijada: `sentence_bert_config.json` tiene max_seq_length=256; `config.json` permite 512 posiciones. La ficha oficial confirma recorte habitual a 256 y ajuste con secuencias limitadas a 128; admitir 512 no prueba mejor calidad. Se conserva la versión habitual y se añade una sensibilidad. Metadatos arXiv: 6 solicitados, 6 recibidos; consulta exacta guardada por arxiv_atom.

## 17-09-2026 — Comparación científica delegada

Protocolo vigente en `ANALYSIS_PROTOCOL.md`, métodos reproducibles en `METHODS_ANALYSIS.md` y revisión dirigida de medidas en `research/analysis_2026-09-17/METRIC_REVIEW.md`. Metadatos y ocho referencias en esa carpeta; no se afirma revisión sistemática o novedad garantizada.

Ya se calcularon forma, relaciones entre áreas y vecinos principales. Resúmenes de trabajo en `reports/analysis_v1/preview/`, explícitamente provisionales mientras terminan controles. La forma y los vecinos no son la misma medida ni sus cifras son porcentajes intercambiables. El acuerdo entre centros de áreas no garantiza conservar relaciones dentro de ellas.

MiniLM 512: 34.331 recortes frente a 247.910 en su uso habitual de 256. No se detectó un error en el límite original. Ambos se conservan; leer más no demuestra representar mejor. El control común mantiene el contenido literal que cabe en todos los modelos, sobre 52.000 IDs seleccionados sin consultar resultados.

Limitación adicional verificada: los Fields de OpenAlex provienen de clasificación automática de texto/citas/revista; se usan como grupos, no como verdad independiente. Fuentes en los métodos. Shesha (versión 5 de julio de 2026) responde a estabilidad dentro de una representación ante dividir coordenadas; su sensibilidad declarada a rotaciones no encaja como sustituto de nuestra comparación de forma. Es una valoración del alcance, no una refutación experimental del método.

## Resultados comprobados y cierre, 17-09-2026

Evidencia vigente: [ANALYSIS_RESULTS.md](ANALYSIS_RESULTS.md), [summary.json](reports/analysis_v1/final/summary.json), [audit.json](reports/analysis_v1/final/audit.json) y catálogo de entrega. Las cifras de `preview/` quedan sustituidas.

- Relaciones entre áreas: correlación de orden mediana 0,847; dentro de área/período 0,519. La medida principal CKA corregida tiene mediana 0,610. Objetos y escalas explícitos; no porcentajes de acierto.
- Vecinos locales: 30,3% compartidos en promedio equilibrado; 31,9% con 2.048 candidatos iguales; 17,5% en 13.000 consultas globales sobre base de 400.000. No atribuir la diferencia local/global solo a fronteras: cambia también el tamaño de candidatos.
- Forma y vecinos se asocian entre las 45 parejas: correlación de orden 0,920. No vender independencia. Mayor acuerdo local MPNet–MiniLM (56,5%); menor SPECTER2–SimCSE (18,0%). El consenso no identifica el mejor modelo.
- Texto común: cambio absoluto mediano CKA 0,005; vecinos +0,15 puntos porcentuales en la comparación emparejada con los mismos 400 candidatos. Receta CLS en los cuatro BERT: cambio absoluto mediano CKA 0,101. Hay excepciones y rangos completos en el informe.
- MiniLM ampliado: ningún fallo de código en el límite habitual; 512 reduce recortes a 6,87% y conserva 82,25% de sus propios vecinos, pero aumenta el acuerdo con los demás solo 0,78 puntos de media. Original intacto; ampliación como control.
- Estabilidad: 50 de 5.850 comparaciones no cumplen amplitud, en 13 celdas; se conservan y limitan conclusiones específicas. Calidad afecta especialmente a SciNCL–BioBERT en Artes y humanidades 2000–2004 (CKA +0,155). No ocultar esos casos tras la media general.
- Centros: acuerdo parecido bajo controles; referencia aleatoria positiva (~0,60). Con texto habitual SPECTER–BERT es la excepción a superar su propia referencia mediana. Los 20 repartos son diagnósticos, no valores p; controles declarados posteriores al resultado inicial.

Las fuentes ampliadas y los ocho registros bibliográficos verificados están en `research/analysis_2026-09-17/`. La aportación propuesta es la dependencia de las relaciones científicas respecto al modelo, nivel y receta, con controles emparejados. La revisión es dirigida: falta contrastar la prioridad y contextualización de la aportación durante la redacción, no repetir el cálculo por defecto.

## Checklist: fuentes de familias, 17-09-2026

SPECTER2 y SciNCL declaran origen SciBERT y uso de citas/vecindarios para ajuste. Compartir ese origen no hace idéntica la tarea final: SciBERT de palabras se conserva separado por objetivo. MPNet/MiniLM/SimCSE se estudiarán como grupo operativo de representaciones de frases, sin asumir que comparten corpus. Protocolo y enlaces primarios en `CHECKLIST_PROTOCOL.md`. No se han inspeccionado todavía nuevos resultados de entrada, tendencias agregadas o regresión de familias.

MPNet declara ajuste con una mezcla de más de mil millones de parejas, incluyendo S2ORC y ejemplos SPECTER: «general» no significa «sin ciencia». La ficha de SimCSE remite a su ajuste no supervisado con un millón de frases de Wikipedia; sus datos no son la mezcla de MPNet/MiniLM. Se usarán etiquetas amplias con esta limitación, no como medidas de solapamiento exacto del corpus.

Fuentes de las diez familias sintetizadas en `research/checklist_2026-09-17/MODEL_PROFILES.md`: PubMedBERT abstract-fulltext se entrena desde cero con PubMed/PMC; BioBERT v1.1 parte de BERT cased y añade PubMed. La etiqueta biomédica no implica origen idéntico. No se han usado sus acuerdos para asignar familias.

Resultados adicionales terminados sobre las tablas previas: vecinos con todos los candidatos pasan de 30,66% a 29,79% entre primera/última fecha; con 2.048 candidatos iguales pasan de 31,41% a 32,32%. Es una inversión del signo al controlar el tamaño. CKA media aumenta de 0,6281 a 0,6488; con criba de calidad el aumento es menor (+0,0115). No interpretar como convergencia histórica causal. Evidencia: `data/checklist_v1/existing_v2/summary.json`.

Medicina: BioBERT–PubMedBERT mantiene CKA media 0,838 y vecinos iguales 54,8%; los otros 28 pares sin ambos modelos también tienen menor forma en Medicina que en Energía (0,571 frente a 0,787). Los biomédicos no explican por sí solos la diferencia. Objetivo compartido se asocia con más acuerdo en la receta principal; el dominio amplio tiene coeficiente inestable al quitar modelos. No se ha demostrado un efecto causal del entrenamiento.

Comprobación temporal posterior motivada por la inversión de signo: al mantener exactamente las mismas 2.048 consultas por celda y buscar frente a todos los candidatos, el cambio de vecinos sigue siendo −0,900 puntos; limitando también los candidatos a 2.048 pasa a +0,911 puntos. Elegir las consultas modifica la tendencia solo −0,030 puntos; cambiar los candidatos de esas mismas consultas, +1,811. El signo también cambia con 10 y 50 vecinos. Se reutilizaron coincidencias existentes, sin nuevas búsquedas; `data/checklist_v1/candidate_check/` verifica 266.240 consultas y 130 celdas. Sigue siendo un contraste sobre subconjuntos concretos, no una ley causal del tamaño.

La forma media de Medicina es 0,554 y la mediana de la entrega anterior era 0,474: son resúmenes distintos, no resultados incompatibles. Con calidad, Medicina sigue siendo el área de menor CKA media (0,566); con SEP Artes/Humanidades queda ligeramente por debajo. Con candidatos iguales Medicina ocupa el quinto lugar por abajo en vecinos, por delante de Matemáticas (29,82% frente a 29,14%). No afirmar que el orden de áreas sea idéntico para todas las medidas.

Los grupos de entrenamiento tampoco son bloques cerrados: dentro de MPNet/MiniLM/SimCSE la CKA media es 0,649; entre ese grupo y SPECTER/SPECTER2/SciNCL es 0,675. Sus coincidencias de vecinos son 34,9% y 36,2%, respectivamente. El contraste global dentro/fuera pondera parejas (12 dentro: 3 de citas, 6 de palabras y 3 de frases), no familias iguales. La asociación media positiva no se cumple como regla en cada grupo. `same_objective` es una etiqueta operativa amplia de entrenamiento, no identidad de funciones matemáticas ni una intervención causal.

## Checklist terminada: entradas, recetas y estabilidad, 17-09-2026

Evidencia final: [CHECKLIST_RESULTS.md](CHECKLIST_RESULTS.md), [summary.json](reports/checklist_v1/final/summary.json) y [audit.json](reports/checklist_v1/final/audit.json). Son resultados finales, no estimaciones durante la cola.

- 26.000 IDs compartidos en 30 condiciones. Reutilización exacta de 260.000 filas modelo–artículo y 520.000 nuevas; todas auditadas, incluidas recetas alternativas. El bloque usado para comprobar reanudación permanece idéntico.
- Principal mean: desacuerdo de forma por cambiar modelo 0,369423; por quitar resumen 0,365867; por quitar título 0,026845. Pérdida de vecinos respectivos: 64,9225%, 66,6394% y 19,8498%, esto es 16,2/16,7/5,0 de 25. Mismos 1.000 candidatos por área, cinco fechas reunidas.
- Las medias esconden una división: quitar resumen cambia menos que cambiar modelo para SPECTER/SPECTER2/SciNCL/MPNet/MiniLM, y más para los cuatro BERT de palabras y SimCSE. Ocurre en las medias de forma y vecinos. Conservar resumen y quitar título cambia menos que cambiar modelo en las 260 combinaciones y las tres recetas.
- La comprobación por rangos da desacuerdos medios de 0,4603/0,3925/0,0286. La cercanía de las dos primeras medias de CKA no es una prueba de equivalencia ni una conclusión independiente de la medida.
- Cruce con recetas: vecinos perdidos al cambiar modelo/quitar resumen son 72,8%/69,8% con CLS y 69,2%/67,3% con SEP. Se invierte el pequeño orden de las medias principales. No declarar dominancia universal ni seleccionar retrospectivamente la receta que favorezca un mensaje.
- Estabilidad del contraste de forma: 52/52 promedios de área y 489/520 casos individuales pasan. Quedan 31 alertas de amplitud en 17 áreas; ningún fallo por cambio de mediana. Máxima amplitud 0,090754; máximo cambio de mediana 0,012021. Se mantiene el piloto, sin convertir esta criba en intervalos poblacionales ni en garantía de estabilidad de vecinos. Las 50 alertas anteriores siguen separadas.
- Familias: CKA media 0,759 dentro frente a 0,592 entre grupos; vecinos iguales 43,2% frente a 27,7%. La proporción de variación entre 45 promedios de parejas descrita por la regresión pasa de 0,399 con mean a 0,027 con SEP. Asociación condicionada por receta, no efecto causal ni porcentaje de ciencia explicado.
- 78 contrastes reales de fórmulas CKA y 14.040 consultas de vecinos comprobadas con implementación independiente. El cruce reproduce mean: error CKA máximo 7,82 × 10⁻¹⁴ y error de vecinos cero. Siete pruebas matemáticas/de flujo aprobadas, además de las pruebas reales de los diez modelos.
- La entrada compara usos prácticos: cambia cantidad de contenido y, a veces, texto que cabe o separadores. El control común previo no hace del experimento una descomposición causal pura. Fuentes y diferencias frente a trabajos anteriores en `RELATED_INPUT_WORK.md`; no afirmar novedad de título frente a abstract por sí sola.

## Cobertura antes de ampliar a Subfields, 17-09-2026

`research/robustness_2026-09-17/size_audit.json`: 252 Subfields, 1.255 celdas por fecha. Hay Subfields con 3, 21 o 27 registros, por lo que no todos admiten CKA/50 vecinos o una precisión comparable. Un control de 256 agrupando fechas cubre 217/252 y 495.828/500.000 artículos; debe mostrar los grupos pequeños excluidos y no convertirlos en ceros. El campo real del nombre es `subfield_display_name`; IDs Subfield son cadenas.

Búsqueda inicial nueva (17-09): localizado por fin el PDF editorial de Lamers et al. en el repositorio de Bolonia, además del registro institucional. No confundir la fecha de indexación reciente con publicación: es ISSI 2021. Aparecen como candidatos de 2026 la revisión de Misuraca sobre text mining/science mapping y estudios de correspondencia entre representaciones; aún requieren lectura/clasificación. Consultas y resultados del segundo bloque guardados en `research/robustness_2026-09-17/literature/search_web_02.txt`. La revisión de literatura R11 sigue abierta.

Revisión metodológica nueva: Gröger, Wen y Brbić, ICML 2026 camera-ready (arXiv:2602.14486v2, 25-06-2026), examinan referencias por permutación y sesgo de tamaño/dimensión en medidas de representaciones. Leídos planteamiento, calibración, definición de CKA corregida y apéndice E.4. Este último informa proximidad entre calibración y CKA corregida: no interpretar el artículo como una refutación automática de nuestra medida. Enlace primario: https://arxiv.org/html/2602.14486v2 . El contraste de tamaños/medidas y referencias requiere revisión antes del cierre R08; no se cambió la métrica durante la inferencia.

El lector web no recuperó el PDF público de Lamers (403); el índice sí expone su dirección y resumen. No se ha leído todavía el texto completo y R11 no está cerrado. No hay `pdftotext` en PATH: si se recupera PDF, usar el entorno de documentos disponible en lugar de instalar herramientas o inventar el contenido.

## 17-09-2026 — Evidencia del cierre experimental ampliado

Documentos nuevos con resultados y límites: `SCALES_AND_DISCIPLINES.md`, `TEMPORAL_REVIEW.md`, `MODEL_FAMILIES.md`, `METRICS.md` y `CONCLUSION_CONTROLS.md`. Las comparaciones estructurales están auditadas; entrada 52k tiene las 30 condiciones verificadas y siguen sus comparaciones/100 selecciones. No extrapolar ese estado a meta completa.

La hipótesis de caída universal al aumentar detalle no se sostiene: con consultas/candidatos/fechas iguales, k25 baja en 127/217 especialidades y sube en 90. El tamaño de búsqueda cambia mucho los porcentajes. Las alertas originales se concentran: 48/50 involucran BioBERT, sin prueba de error del modelo. Hay 2.841 alertas adicionales de especialidades en dos regímenes de tamaño diferentes; conservar ambos y no confundirlo con error poblacional.

La literatura dirigida actualizada identifica Caspari et al. (2024) como antecedente directo de CKA + recuperación + familias y Rozmus/van der Putten (2026) de calibración entre modelos. Nuestros resultados deben presentarse como dependencia de decisiones y niveles al cartografiar ciencia, no como primera comparación entre encoders. Los cinco antecedentes pedidos fueron leídos en fuentes primarias completas; accesos parciales adicionales se distinguen en `RELATED_WORK_UPDATE.md`. Desconocemos las listas exactas de artículos vistos durante entrenamiento; esto también limita interpretar el patrón temporal.

## 17-09-2026 — Hallazgos definitivos de la ampliación a 52k y Subfields

Entrega vigente: `ROBUSTNESS_RESULTS.md`; evidencia detallada y límites en `CONCLUSION_CONTROLS.md`, `POOLING.md`, `SCALES_AND_DISCIPLINES.md`, `MODEL_FAMILIES.md`, `TEMPORAL_REVIEW.md` y `SAMPLING_STABILITY.md`. Los 15 componentes del cierre pasan la auditoría integrada.

- Entradas 52k: cambiar modelo, quitar resumen y quitar título cambian 68,76%, 70,67% y 22,12% de los vecinos k25 (2.000 candidatos por área). CKA: cambios 0,3700/0,3658/0,0269. Parecido de medias no prueba equivalencia; el orden depende de modelo/receta/medida.
- Cien selecciones comparables: alertas 72/520 → 5/520 de 26k a 52k; primeras veinte reproducen 31 → 4. Cuatro de las 31 claves antiguas siguen entre las cinco actuales. Pasan las 52 medias de área, pero seis rangos incluyen cero. No llamar poblacionales a estos rangos.
- Recetas: título solo cambia el signo del contraste de forma en 15/260 casos con CLS y 20/260 con SEP frente a mean; en los cuatro BERT de palabras, 9/104 y 13/104. Las alternativas permanecen como sensibilidades, no candidatas entre las que elegir retrospectivamente la historia preferida.
- Escalas controladas: vecinos k25 baja 1,35 puntos en promedio, pero solo en 127/217 especialidades; con k50, 109/217. La ley universal de menor acuerdo a mayor detalle no se sostiene. El rango mediano entre diez selecciones de candidatos para una consulta de especialidad es 9,33 puntos.
- Medicina: equilibrar pesos de especialidades apenas cambia su acuerdo. Omitir biomédicos mejora algo la forma, pero no elimina la diferencia frente a las referencias. No hay causa única identificada. Familias: objetivo/linaje asociados con mean; receta cambia la lectura y los rasgos siguen confundidos.
- Tiempo: signo de vecinos depende de candidatos, incluso separando exactamente selección de consultas. La mayoría de áreas mejora la forma entre extremos, pocas en todos los pasos. No se demuestra evolución causal ni documentos ajenos al entrenamiento.
- R11: cinco antecedentes pedidos y fuentes próximas 2025–26 revisados. Caspari et al. ya combinan forma, recuperación y familias; Constantino y SemCSE ya contrastan entradas. La aportación no se puede fundar en atribuir novedad a esos componentes.

Se conservan 50 alertas iniciales y todos los diagnósticos de Subfields. Corpus original, respuestas descargadas y vectores intactos; la extracción congelada no es una instantánea mundial simultánea de OpenAlex. Las limitaciones y los cruces no ejecutados se enumeran, sin declararlos resueltos por la auditoría técnica.

## 17-09-2026 — Revisión previa: primeras comprobaciones

Las normas oficiales de QSS recuperadas mediante el índice del editor piden compartir los datos esenciales en repositorio persistente; el acceso directo devuelve 403. No confundir las normas de otras revistas devueltas por búsquedas amplias. La copia indexada puede ir retrasada: se revalidará antes del envío. Nuevo antecedente próximo: Schumacher, Reichelt y Strohmaier, Applied Network Science, 13-09-2026, DOI 10.1007/s41109-026-00830-2, sobre estabilidad de embeddings de nodos y dimensiones, no nuestro experimento de documentos científicos. También debe distinguirse coincidencia entre representaciones de corrección semántica.

Inventariados 33 identificadores bibliográficos explícitos en documentos pertinentes; algunos son referencias históricas erróneas o contrastes secundarios que no deben pasar sin selección a la bibliografía final. Protocolo de casos escrito antes de inspeccionar nuevos ejemplos. Una relación solo puede fallar si su candidato estaba disponible: por eso se usarán pares de consultas fijas para la repetición de vecinos.


## 18-09-2026 — Antecedentes iniciales de morfología

- El TFM ya separaba dispersión, vecinos/hubness, espectro PCA y conectividad. Sus valores SPECTER2 no deben mezclarse con estos vectores nuevos. Se reutiliza el planteamiento, no sus resultados.
- IsoScore (Rudman et al., 2022, Findings ACL, https://aclanthology.org/2022.findings-acl.262/) advierte que coseno medio no mide por sí mismo isotropía. Separar apertura angular de reparto de varianza.
- Roy y Vetterli (2007, https://www.eurasip.org/Proceedings/Eusipco/Eusipco2007/Papers/a5p-h05.pdf) proponen rango efectivo por entropía; especificar si se aplica a la matriz de datos o su covarianza.
- Imel y Hafen (2025, https://arxiv.org/abs/2506.23366) ya estudian densidad/asimetría en literatura científica: morfología no es una aportación inédita por sí misma.
- Rolle y Scoccola (JMLR 2024, https://www.jmlr.org/papers/v25/21-1185.html) distinguen estabilidad del objeto y estabilidad de un procedimiento/recorte de agrupación. No asumir que escoger una medida topológica elimina parámetros o ruido.
- El sesgo por tamaño afecta al espectro y a estimadores locales de dimensión. Se evitará llamar dimensión intrínseca verdadera a una dimensión efectiva lineal estimada.


### Piloto: pruebas simuladas previas a datos reales

Nueve nubes y quince referencias. Rotar coordenadas cambia las medidas <1,5e−14; multiplicar vectores por una constante positiva no las cambia. Fórmulas espectrales comprobadas por SVD y conectividad por MST/componentes independientes. La nube alargada tiene brecha de conexión 0,091 frente a 0,499 para la redonda, aun sin separar grupos. El cociente de radios 90%/50% marca 1,589 para una sola nube de pocas direcciones, pero solo 1,003 para cuatro grupos separados. Unos pocos puntos extremos disparan la arista máxima. **Estos indicadores no pasan como medidas generales de fragmentación**; se mantienen como diagnósticos con nombres literales. Datos en `data/morphology_pilot_v1/synthetic/` y fuentes en `sos_morphology/`. No se habían calculado nuevos resultados reales.


### Revisión de medidas y primera comprobación real

Lectura dirigida y matriz de decisiones en `research/morphology_2026-09-18/LITERATURE.md`. Grafos unión/mutuos y escalas locales describen conexiones diferentes; máxima arista de enlace simple es sensible a extremos. Antecedentes y exclusiones quedan argumentados. Biblioteca ampliada inicialmente a 52 registros verificados, sin errores/duplicados; avisos por identificadores/páginas ausentes se conservan.

Primer bloque real SPECTER completo: las 26 áreas tienen un único componente en el grafo unión k25, aunque la brecha de conexión varía entre 0,0147 y 0,1160. Es evidencia de saturación del recuento simple en este modelo, no ausencia de grupos temáticos. Todavía no es la comparación final de diez modelos.

## 18-09-2026 — Resultados completos del piloto de morfología

Entrega y cifras comprobadas: `MORPHOLOGY_RESULTS.md`, `METHODS_MORPHOLOGY.md` y `reports/morphology_pilot_v1/`. Diez modelos, 26 áreas, 52k principales y 16.884 conjuntos de medidas con controles. Se reutilizaron vectores, sin extracción/inferencia.

- Apertura y PR repiten bien el orden de áreas al cambiar artículos (0,992/0,989 a igual tamaño), pero los modelos difieren (0,319/0,552). El ejemplo posterior Artes/Medicina invierte el signo con SPECTER/BERT y persiste en veinte medias muestras, cinco selecciones adicionales y tres alternativas angulares. No equivale a corrección semántica.
- Al duplicar 2.000 a 4.000, apertura cambia una mediana de −0,03% y PR +1,14%; máximo absoluto de PR 4,07%. Cuatro alertas internas de PR permanecen: PubMedBERT en Economía/Psicología y BioBERT en Economía/Inmunología. Las cinco muestras externas pasan, con menos capacidad de descubrir colas.
- PR/entropía/D80 concuerdan ampliamente sin dar el mismo puesto exacto. La receta CLS/SEP y el centrado global alteran conclusiones; el texto común no elimina el desacuerdo. Los controles de calidad no validan los Fields de OpenAlex.
- Conexión no identifica por sí sola fragmentación: simulaciones exhiben contraejemplos, unión k10/25/50 satura en un componente en 260 casos. Quedan 51 alertas entre selecciones externas. Duplicar n con k25 cambia la mediana −22,2%; duplicar también k a 50, +3,3%. La comprobación adicional está declarada.
- Frente a 780 referencias gaussianas, la conexión observada es siempre menor; esas referencias no igualan exactamente PR tras normalizar (error máximo +19,8%). No prueba temas separados ni produce un valor p.
- Tiempo es exploratorio: bajan apertura/PR en 203/207 casos de 260, pero no se aislaron cambios de composición/texto/cobertura para esos rasgos. No inferir estrechamiento histórico.

Las medidas tienen antecedentes; Imel/Hafen ya estudian propiedades de densidad científica. La aportación propuesta es la fiabilidad de afirmaciones concretas frente a decisiones de representación, no métricas nuevas ni prioridad absoluta. Biblioteca actual de 54 registros, sin errores/duplicados y cinco avisos editoriales documentados. Revisión dirigida en `research/morphology_2026-09-18/LITERATURE.md`.

## 18-09-2026 — Cobertura comprobada para resumir parejas

Hay 325 parejas únicas de los 26 Fields. Principal, veinte medias muestras y cinco selecciones adicionales están presentes para los diez modelos y ambas propiedades. Las tres alternativas angulares están guardadas en todas esas selecciones; las alternativas de espectro (entropía/D80), solo en principal y primera repetición de cada diseño. Controles de texto, receta, calidad, centrado, extremos y tamaño son puntuales; no tienen repeticiones propias. `FIELD_PAIR_PROTOCOL.md` distingue esas coberturas antes de extraer frecuencias nuevas y separa persistencia numérica de tamaño de efecto y validez temática.

### Resumen calculado y comprobación independiente

Principal: apertura 42 acuerdos de diez / 262 contradicciones persistentes / 21 sin conclusión común; PR 54 / 221 / 50. Contradicción exige dos modelos con direcciones opuestas persistentes, no los diez en oposición. A 5% relativo simétrico: 96 y 177 contradicciones; a 10%, 19 y 126. No ocultar que parte de la apertura corresponde a diferencias pequeñas.

Los mismos modelos testigo conservan direcciones bajo alternativas en 225/262 y 196/221 casos. Con seis modelos de similitud quedan 231/325 y 160/325 contradicciones; a 5%, 80 y 114. Menos modelos también ofrecen menos oportunidades de oposición. El centrado global conserva los mismos testigos en 145/262 aperturas frente a 218/221 PR; no elevar apertura a propiedad independiente del procesamiento. Controles puntuales, sin replicación propia.

Verificación independiente por razones B/A frente a la fórmula de diferencias simétricas: 10.400 filas de sensibilidad, 6.500 decisiones, 7.150 controles por pareja, 442.000 contrastes, 96 resúmenes de panel; originales y 18 documentos previos intactos. No se calcularon nuevos embeddings. Primera inspección de figuras: colores/etiquetas y matriz de áreas legibles; se corrige el orden vertical de umbrales compartidos y se añaden cifras en segmentos pequeños, sin tocar resultados científicos.

## 18-09-2026 — Revisión editorial de QSS: punto de partida

La consulta inicial localiza artículos muy cercanos (Constantino et al., comparación de embeddings; cartografía mesoscópica de IA) y confirma ISSN 2641-3337. El índice web de la guía oficial es antiguo; no tratarlo como verificación fresca del reglamento. Se distinguirán normas oficiales, patrones de una selección temática y decisiones de presentación propias.

La guía oficial indexada especifica expresamente que no impone una estructura única; métodos deben aparecer al principio y permite IMRaD sin exigirlo. Resumen hasta 200 palabras; artículos típicamente 5.000–8.000. Acceso directo 403 y caché antigua: revalidar antes de enviar. Primer inventario Crossref: 465 registros hasta 18-09-2026. El cursor no admite orden por publicación (400); se cambia a orden estable por DOI.

Inventario recuperado: 465/465 registros Crossref (dos páginas, sin truncado). Primera selección temática: 34 artículos de 2020–2026. OpenAlex devuelve 36 registros para 34 DOI por duplicados de qss_a_00035 y qss.a.406: deduplicar por DOI y reunir ubicaciones, no contar como estudios distintos. PDFs editoriales MIT directos devuelven 403; se buscan copias públicas de autores/repositorios y se identificará su versión. La búsqueda detecta dos trabajos recientes de 2026 (mapa de proyectos europeos; taxonomías de contenido), pertinentes para actualizar la comparación.

Exa permitió recuperar 14 textos editoriales completos de la selección, incluyendo Boyack/Klavans, Held, Velden, Huang y los análisis recientes de OpenAlex; se conservan los textos fuera de Git. Se añaden copias de autor/repositorio donde falta la editorial. El índice de QSS revela estructuras diversas: IMRaD, resultados/discusión unidos y artículos organizados por problemas. Esto descarta imponer un molde universal.
## Lectura editorial QSS, 18-09-2026

- Marco recuperado: 465 registros Crossref del ISSN 2641-3337; selección dirigida de 34 trabajos. Hay 33 copias largas para lectura estructural y un acceso parcial (Donner/Henneken). No se han leído 465 artículos ni replicado los 34 estudios.
- Se observa diversidad de organización: resultados/discusión unidos, discusión/conclusión unidos, antecedentes propios y artículos organizados por componentes. La guía indexada no impone IMRaD. La función de cada sección importa más que su rótulo.
- La comparación de métodos y la dependencia de conclusiones tienen antecedentes claros: Wang/Schneider, Boyack/Klavans, Armitage, Sīle, Held/Velden, Constantino y otros. La propuesta debe centrarse en qué conclusiones se conservan bajo cambios controlados, sin prometer una primera demostración de dependencia del método.
- Verificación de acceso: una respuesta de búsqueda para Donner/Henneken traía el cuerpo de otro artículo; se rechazó. Se distingue versión editorial, publicación anticipada, manuscrito de autor y texto cuya versión tipográfica no pudo certificarse. El preprint de Kim coloca métodos al final: no usarlo como prueba de la estructura editorial final ni para contradecir la guía.
- Las copias completas de terceros permanecen en `data/qss_structure_review_v1/`, excluido de Git. El informe y la matriz citarán DOI y fuente real; no incluirán esos textos.
