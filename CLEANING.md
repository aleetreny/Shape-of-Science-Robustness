# Limpieza del corpus — 15-09-2026

**Terminada y comprobada.** Hay **500.000 registros con IDs distintos** preparados para configurar los embeddings: 400.000 base aleatoria global y 100.000 complemento recalculado. La descarga original se conserva intacta.

## Resultado

| Comprobación | Resultado |
| --- | --- |
| Cobertura | 26 Fields, 130 combinaciones área/período y las 650 combinaciones área/año de 2000–2024. |
| Mínimo por área/período | 2.165 trabajos. No se recortaron las áreas grandes ni se igualaron los años a mano. |
| Registros originales apartados por calidad | 5.776, entre ellos 4.651 por la regla conservadora de idioma. Los motivos pueden solaparse. |
| Cambio por reajuste del reparto | Otros 123 registros válidos del original no volvieron a entrar al reconstruir la base y el complemento. No son errores de calidad. |
| Reutilización de la descarga | 494.101 IDs de la selección original + 5.889 candidatos que habían quedado guardados sin seleccionar. |
| Descarga adicional | Una página de 100 candidatos, de la que se incorporaron 10. La reconstrucción corregida reutilizó esa misma página sin consultas nuevas. |
| Comprobación del guardado | 6.139 páginas, reproducción de todas las decisiones examinadas y contraste de las 500.000 filas con sus respuestas de origen. Sin discrepancias. |
| Segunda comprobación de texto | Detector de idioma ejecutado de nuevo sobre los 500.000 abstracts, sin diferencias con los diagnósticos guardados. Cero estructuras conocidas de páginas/avisos restantes. |

Recuento por área: [field_summary.csv](research/cleaning_2026-09-15/field_summary.csv). [Figura del reparto](research/cleaning_2026-09-15/field_period_coverage.png). [Efecto de la limpieza por área](research/cleaning_2026-09-15/cleaning_impact_by_field.csv).

La limpieza no afecta a todas las áreas igual: apartó el 3,53 % de los registros originales de Artes y Humanidades, el 2,61 % de Ciencias Sociales y el 2,26 % de Enfermería. Estas cifras describen esta selección original, no la tasa de errores de todo OpenAlex.

## Casos conservados con marcas

- 9.883 abstracts con idioma dudoso; 3.002 aparecen como posibles textos mixtos. Son conjuntos que se solapan.
- 33 registros conservados con una observación de contenido y cuatro posibles avisos por título; estas marcas también pueden solaparse.
- 42.849 abstracts de 50–79 palabras y 249 de más de 2.000. La longitud por sí sola no decide si un resumen sirve.
- 62 grupos con título+abstract exactamente iguales, 64 al normalizar espacios y mayúsculas, y siete grupos con DOI compartido. Hay 88 grupos con abstract idéntico. Se conservan los IDs distintos y se documentan los grupos.

Las marcas permiten comprobar después si las conclusiones cambian al apartar estos casos. **La validación confirma el guardado y la aplicación de las reglas; no demuestra que todos los metadatos sean perfectos ni que todos los textos sean exclusivamente ingleses.** La correspondencia semántica título/resumen se inspeccionó en los casos revisados; el control de las 500.000 filas comprueba correspondencia con la fuente, no lectura humana de todos los resúmenes.

## Reglas aplicadas

- Mantener población, años y filtros originales. No traducir, reescribir ni generar resúmenes.
- Excluir los textos completos identificados como descripciones de revistas/bibliotecas/catálogos o un mensaje de error DOI. Se compara el texto completo, normalizando solo espacios para esta comprobación; no basta un comienzo parecido.
- Aplicar también las estructuras específicas de páginas, anuncios y avisos a todos los candidatos, incluidos los recién descargados. Por ejemplo, una página ACS se reconoce por la combinación de cabecera de navegación, bloque de métricas y exportación de citas; la palabra «advertisement» por sí sola no basta.
- Excluir títulos con una etiqueta explícita `WITHDRAWN:`/`RETRACTED:` y tres casos revisados: un erratum, un trabajo con retirada explícita en el título y un aviso cuyo abstract completo es una expresión de preocupación editorial. La evidencia y huella del texto quedan en la configuración.
- Idioma: usar fastText lid.176.bin sobre el abstract completo. Excluir como claramente ajeno al inglés solo si la primera etiqueta no es inglés con puntuación ≥0,9 y las tres partes consecutivas del abstract coinciden en ese mismo idioma con puntuaciones ≥0,8. Los cortes son una regla operativa conservadora, no probabilidades garantizadas ni umbrales exigidos por una revista. Las partes usan el mismo detector y no son pruebas independientes.
- Conservar y marcar los demás casos dudosos o bilingües. Se consultó esa preferencia y se comunicó el criterio conservador; no se afirma que todos los textos retenidos sean exclusivamente ingleses. La comparación posterior debe examinar la sensibilidad al apartarlos.
- Mantener los IDs distintos y marcar DOI/texto repetidos. No fusionar por parecido ni cambiar silenciosamente la unidad de selección a estudios únicos.
- Resúmenes de 50–79 palabras, textos muy largos y avisos dudosos quedan marcados; no se borran por longitud o palabras sueltas.

## Reposición y reproducibilidad

Volver a recorrer los bloques globales originales en su orden y con su mezcla aleatoria guardada, aplicando las reglas comunes a todos los candidatos. Tomar los primeros 400.000 válidos con IDs distintos. Después recalcular las 130 cuotas área/período y usar los bloques aleatorios correspondientes ya descargados. Solo pedir nuevos bloques si queda un hueco; guardar respuestas, semillas, fechas y razones de descarte.

Se revisaron los 286 grupos de abstract idéntico del original y se comprobaron firmas específicas de páginas en todas las 6.138 páginas de candidatos. La configuración final reúne 538 huellas de textos impropios; además hay decisiones por ID para textos claramente asignados al trabajo equivocado y marcas para casos dudosos. Se excluyen también páginas enteras que envuelven o sustituyen al resumen: no se intenta recuperar un resumen mediante recortes inciertos. Las reglas se establecen a partir de esta inspección del corpus, antes de los embeddings; no se presentan como una limpieza registrada antes de observar los datos.

Configuración exacta: `config/cleaning_v1.json`. Código separado: `sos_prepare/`. Pruebas: `tests/test_preparation_quality.py` y `tests/test_preparation_recovery.py`. Evidencia: `research/cleaning_2026-09-15/`.

## Archivos finales

- `data/corpus_clean_v1/corpus.parquet`: tabla maestra con marcas de calidad y procedencia.
- `data/corpus_clean_v1/embedding_input.parquet`: IDs, títulos y abstracts en un orden común para todos los modelos; sin formato específico, traducción ni truncamiento.
- `data/corpus_clean_v1/embedding_manifest.json`: huellas de archivos y del orden de IDs/textos.
- Informes de descartes, recuentos y validación completa en la carpeta de evidencia.

Los modelos y sus versiones no se eligen en esta limpieza. Tampoco se calculan embeddings. Las copias originales se conservan: la nueva carpeta usa referencias relativas a sus páginas, por lo que hay que guardar ambas carpetas juntas.

## Incidencias resueltas antes de la entrega

Se conservaron tres recorridos provisionales en `data/corpus_clean_v1_initial_pass/`, `data/corpus_clean_v1_second_pass/` y `data/corpus_clean_v1_third_pass/`. Los dos primeros permitieron ampliar el catálogo de errores observados. El tercero superó la comprobación de guardado, pero la revisión adicional encontró una página ACS entre los candidatos nuevos: la regla de estructura solo se estaba usando al preparar el catálogo de textos antiguos.

Se corrigió la causa aplicando la misma regla a todos los candidatos. La prueba que reproduce ese fallo falló antes de corregirlo; después pasaron las 14 pruebas específicas. La selección se reconstruyó y verificó con el código corregido. La página nueva se conserva byte por byte y se reutiliza sin consultarla otra vez. Esas carpetas provisionales no son entradas para modelos. Evidencia: `research/cleaning_2026-09-15/content_regression_fix.json`.

Fuentes: [modelo fastText](https://fasttext.cc/docs/en/language-identification.html), [atributos OpenAlex](https://help.openalex.org/data/works/attributes/), [API y muestreo](https://help.openalex.org/api/llm-quick-reference/). Las fuentes documentan herramientas y límites; no garantizan el acierto de la regla de limpieza elegida.

## Evidencia y siguiente paso

- [Validación completa](research/cleaning_2026-09-15/final_validation.json), [segunda comprobación de idioma y contenido](research/cleaning_2026-09-15/quality_recheck.json) y [estado de preparación](research/cleaning_2026-09-15/readiness.json).
- [14 pruebas aprobadas](research/cleaning_2026-09-15/tests.txt): reglas, interrupción y reanudación, conservación de originales, reposición y reutilización de páginas. La prueba pequeña inicial de 12 registros está documentada; la última versión pasó además el recorrido completo de producción.
- [Lista de registros originales no retenidos](research/cleaning_2026-09-15/original_records_not_selected.csv), con motivo individual. `quality_exclusions.csv` registra decisiones por candidato y puede repetir un ID entre bloques: no sumar sus filas como trabajos únicos.
- Configuración y huellas en `data/corpus_clean_v1/preparation_identity.json`. Copia de 25 archivos de programa, reglas, pruebas y dependencias en `data/corpus_clean_v1/source_snapshot/`, con su manifiesto. Entorno: `.venv-audit`, dependencias fijadas en `requirements-preparation.txt`.
- Lectura de los diez pares título/resumen nuevos en `additional_page_review.json`; revisión acotada de idioma en `language_spot_check.json`. Fueron inspecciones del asistente, no una validación humana independiente ni una estimación de precisión del detector.

Datos preparados. La guía para configurar modelos es [EMBEDDINGS_READY.md](EMBEDDINGS_READY.md). No se han calculado embeddings en esta limpieza.
