# Tarea terminada: revisión previa al manuscrito y atlas de casos concretos

17-09-2026. Nueva petición: revisar análisis, referencias y presentación; identificar artículos, Subfields y relaciones que resisten o dependen del modelo. Esta revisión amplía el cierre anterior. No redactar ni publicar todavía. Se conserva la entrega previa y su documentación sellada en `research/prepaper_2026-09-17/baseline_documents/`.

1. Inventariar estado, guardar cierre previo y registrar alcance: **complete**. Los 23 documentos sellados anteriores se verificaron y copiaron; cierre histórico intacto.
2. Revisar cada etapa científica y contrastar cifras/implementaciones relevantes de forma independiente: **complete**. Quince componentes, seis reconstrucciones de forma, 300 consultas reales y 52 pruebas aprobadas en sus entornos; límites en `PREPAPER_REVIEW.md`.
3. Fijar selección de casos y extraer un atlas trazable de artículos, especialidades y relaciones concretas, con controles: **complete**. `CASE_ATLAS.md`, 217 especialidades, 10.850 consultas y relaciones trazables; errores de OpenAlex comprobados y anotados.
4. Verificar referencias, versiones y trabajos cercanos; contrastar normas actuales de QSS y delimitar la contribución: **complete**. Biblioteca de 45 entradas y matriz de antecedentes. Guía oficial indexada consultada; acceso directo 403 y revalidación antes del envío pendientes explícitos.
5. Ordenar la entrada al repositorio, README, métodos, resultados y material para revisión, sin mover salidas congeladas: **complete**. `docs/`, `references/`, atlas, dos figuras inspeccionadas y nueve tablas; originales intactos.
6. Verificar entrega, enlaces, reproducción, originales y límites; actualizar continuidad: **complete**. `research/prepaper_2026-09-17/closure_audit.json`: 23 copias históricas, 73 archivos de la entrega anterior, fuentes congeladas, atlas y catálogo actual verificados; enlaces locales válidos y continuidad cerrada.

Las nuevas comparaciones derivadas están en una salida propia. No se cambiaron recetas, umbrales o resultados anteriores para favorecer la historia. Los errores de clasificación detectados se documentan y conservan; no se presenta el corpus como validado temáticamente. No prometer ausencia de críticas ni prioridad absoluta. Continuación exacta: `NEXT_STEPS.md`.

## Historial de fases anteriores

# Tarea terminada: cierre experimental ampliado antes de redactar

17-09-2026. Objetivo íntegro y requisitos R01–R12 en `ROBUSTNESS_SCOPE.md`, todos verificados. Entrega: `ROBUSTNESS_RESULTS.md`. Originales y programas científicos conservados; no hay cálculos activos.

1. Registrar alcance/diseño y verificar cobertura: **complete**. `ROBUSTNESS_PROTOCOL.md`, configuraciones congeladas y auditoría de tamaños.
2. Ampliar entradas a 52k, auditar reutilización, comparar forma/vecinos/recetas y 100 selecciones (R01–R02): **complete**. Treinta condiciones verificadas; `input_review` e `input_stability100`.
3. Subfields, tamaño, escalas y estabilidad por artículo/región (R03–R04): **complete**. `SCALES_AND_DISCIPLINES.md`, 252 grupos nativos y controles de cobertura explícita.
4. Tiempo y composición de Medicina con controles emparejados (R05–R06): **complete**. `TEMPORAL_REVIEW.md` y controles de composición.
5. Familias, métricas, alertas y controles (R07–R10): **complete**. `MODEL_FAMILIES.md`, `METRICS.md`, `SAMPLING_STABILITY.md` y `CONCLUSION_CONTROLS.md`.
6. Literatura y comparación explícita de antecedentes (R11): **complete**. Revisión dirigida fechada, fuentes primarias y solapamientos/acceso limitado explícitos.
7. Exportar, auditar, congelar y actualizar inventario (R12): **complete**. Quince componentes, 50 tablas, siete figuras inspeccionadas, catálogo de huellas, datos originales comprobados y continuidad actualizada.

No se han escrito ni enviado el manuscrito ni una nueva extracción. Las cinco alertas de entrada a 52k/100, las 50 originales y las de especialidades se conservan como límites; no son tareas incumplidas que se oculten cambiando umbrales. Solo continuar con nuevas actuaciones cuando se soliciten.

## Historial de fases anteriores

# Tarea terminada: checklist de entradas, tiempo, disciplinas y familias

17-09-2026. Petición y delegación nuevas: avanzar con la checklist, pilotando entradas antes de ampliar a 500.000. Protocolo: `CHECKLIST_PROTOCOL.md`; configuración nueva, originales intactos.

1. Fijar comparaciones, receta principal y comprobar fuentes de familias: **complete**.
2. Implementar y probar piloto de título/resumen sobre 26.000 IDs: **complete**. Diez modelos reproducen los resultados originales y el texto literal correcto.
3. Ejecutar y auditar las veinte condiciones nuevas; reutilizar ambas partes: **complete**. 780.000 filas modelo–artículo–entrada comprobadas, 260.000 reutilizadas exactamente y 520.000 nuevas.
4. Explotar tiempo, modelo × disciplina y familias en los resultados ya guardados: **complete**. `existing_v2/` y comprobación posterior de consultas temporales idénticas; presentación integrada.
5. Comparar efecto del modelo y del texto, estabilidad y límites del piloto: **complete**. Cruce CLS/SEP terminado, reproducción de mean comprobada. Pasan 52/52 promedios de área y 489/520 contrastes individuales de forma; se conservan 31 alertas. No ampliar ahora a 500.000.
6. Preparar tablas, figuras, informe y actualización del enfoque del paper: **complete**. `CHECKLIST_RESULTS.md`, 33 tablas, siete figuras, métodos y continuidad actualizados. Auditoría final completa; sin cálculos activos.

Continuación: redactar cuando se solicite, siguiendo `PAPER_OUTLINE.md` y `NEXT_STEPS.md`. No quedan decisiones necesarias para cerrar esta checklist; las limitaciones están documentadas, no resueltas por cambiar umbrales.

## Incidencias de esta fase

- El control de familias detectó que, usando SEP y quitando SimCSE, no se pueden separar tres rasgos de entrenamiento/receta. El primer ejecutor se detuvo y sus salidas parciales quedan intactas. La versión separada `existing_analysis_v2.py` marca coeficientes no identificables, conserva el ajuste descriptivo y no inventa un efecto único.

- La primera llamada al script de prueba no encontraba el paquete local al arrancar desde `research/`; se añadió la raíz del repositorio a su ruta de importación. No había empezado inferencia ni cambiado resultados.

- Lectura inicial de `sos_embed/encoders.py`: no existe; la implementación real está en `sos_embed/models.py`, localizada y leída. No se cambió ningún archivo anterior.

## Historial: fase anterior terminada

# Tarea actual terminada: comparar forma y vecinos

17-09-2026. El usuario delegó las cuestiones de esta fase con criterio de robustez para el paper. La comparación, los controles y la presentación quedaron terminados; los originales permanecen intactos.

1. Revisar fuentes primarias, alternativas de medidas y MiniLM: **complete**. Revisión dirigida y ocho referencias en `research/analysis_2026-09-17/`.
2. Registrar protocolo antes de inspeccionar los acuerdos correspondientes y comprobar métodos: **complete**. Siete pruebas matemáticas y cuatro de vecinos; ampliaciones posteriores identificadas.
3. Calcular controles de texto y recetas en salidas separadas: **complete**. MiniLM 512 sobre 500.000 y diez controles comunes de 52.000; once conjuntos auditados, reutilización exacta comprobada.
4. Ejecutar forma, calidad y estabilidad: **complete**. 130 celdas en seis etapas, base general y centros; 5.800/5.850 superan la regla, 50 alertas visibles. Seguimientos de centros y referencias aleatorias completos.
5. Comparar vecinos: **complete**. Todos los artículos dentro de área/período, 13.000 consultas globales, k=10/25/50, ajuste por azar, recetas y candidatos iguales. 13.260 consultas reales verificadas de forma independiente.
6. Auditar, presentar y actualizar continuidad: **complete**. `reports/analysis_v1/final/`, ocho figuras revisadas en tres formatos, 33 tablas, resumen por artículo, `ANALYSIS_RESULTS.md`, `METHODS_ANALYSIS.md` y `PAPER_OUTLINE.md`.

No quedan cálculos activos. No se crearon nuevas automatizaciones; las antiguas siguen pausadas. El siguiente paso está en `NEXT_STEPS.md`: redactar a partir de estos resultados y comprobar antecedentes próximos, sin repetir inferencia o descargas. No se publicó ni envió el trabajo.

## Historial anterior

# Tarea actual: revisión final y preparación técnica terminadas

17-09-2026. Respuesta a la petición de seguimiento, revisión final, organización y preparación siguiente.

1. Comprobar progreso y programar seguimiento temporal: **complete**. El último modelo terminó a las 06:29 de Madrid del 17-09.
2. Verificar corpus, modelos, archivos, identidades, versiones y control técnico: **complete**. Diez × 500.000 artículos; evidencia en `research/embedding_final_audit_2026-09-17/`.
3. Preparar catálogo, informe y lectura de datos: **complete**. `EMBEDDINGS_AUDIT.md`, `DATA_CATALOG.md`, `sos_analysis/`; ocho pruebas aprobadas y lectura real de las 18 variantes completas.
4. Actualizar continuidad y presentar decisiones pendientes: **complete**. `ANALYSIS_PROPOSAL.md` y `NEXT_STEPS.md`. No se cerraron ni ejecutaron análisis científicos nuevos.
5. Desactivar seguimiento y preparar la entrega: **complete**. Automatización pausada y comprobada; antigua automatización OpenAlex sigue pausada. Solo queda acordar la siguiente fase científica con el usuario.

Originales, programas de preparación/cálculo, configuración, pesos y entorno preservados. No se repitieron descargas o modelos.

## Historial: preparar y probar los diez modelos elegidos

15-09-2026. El usuario acepta los diez. No volver a preguntar su número.

1. Registrar la elección y comprobar el corpus congelado: **complete**. `./prepare.sh preflight` vuelve a pasar.
2. Fijar revisiones y recetas oficiales; preguntar la política de texto: **complete**. El usuario acepta uso habitual + control común.
3. Preparar entorno separado, pesos verificados y cálculo por bloques con reanudación: **complete**.
4. Probar correspondencia de filas, interrupción, corrupción y resultados reales de los diez: **complete**. Diecisiete pruebas y dos pasadas técnicas de los diez verificadas.
5. Documentar costes medidos, comandos, límites y decisiones pendientes: **complete**. `EMBEDDINGS.md` y `research/embedding_setup_2026-09-15/RESULTS.md`.

La prueba es técnica; no se examinan resultados científicos para elegir recetas. El usuario ha pedido lanzarlo él mismo; no arrancar el cálculo completo desde el asistente. Corpus y manifiesto de limpieza permanecen intactos.

## Historial: elegir candidatos según uso académico en mapas de ciencia

Estado de esta sección histórica sustituido por la aceptación de diez y las pruebas terminadas arriba.

15-09-2026. Tras revisar el reparto, el usuario pide más de cuatro modelos y priorizar los empleados en trabajos académicos para mapear ciencia. El criterio queda fijado; los nombres/cantidad y recetas siguen pendientes.

1. Leer decisiones, estado y evidencia final: **complete**.
2. Recalcular proporciones y mínimos desde la copia final, contrastar con auditoría y examinar marcas de calidad: **complete**. `CORPUS_BALANCE.md` y `research/model_review_2026-09-15/`.
3. Revisar antecedentes y fichas oficiales, proponer mezcla y cantidad con límites de novedad/coste: **complete**. Propuesta inicial archivada al cambiar el criterio.
4. Contrastar usos reales en diez trabajos, distinguir menciones/tareas y contar familias: **complete**. `ACADEMIC_MODEL_USAGE.md` y `academic_sources/studies.json`.
5. Registrar resultados, corregir referencias y actualizar propuesta: **complete**. `MODEL_SELECTION.md`, ocho candidatos y dos adicionales para diez.
6. Elegir modelos/versiones/entrada y autorizar el siguiente cálculo: **pendiente de respuesta del usuario; tarea siguiente**. No convertir las propuestas en decisiones por ausencia de respuesta.

Resultado: el corpus preparado permanece intacto. Propuesta vigente de ocho basada en seis comparadores recurrentes y dos con antecedentes específicos; las frecuencias no se presentan como uso mundial. Sin nueva extracción, descarga de pesos ni embeddings. La suficiencia y los costes de todas las comparaciones siguen por comprobar. La evidencia del reparto final está en `CORPUS_BALANCE.md`.

## Historial: limpieza y preparación terminadas

## Autorización, 15-09-2026

El usuario pide continuar con la limpieza, reutilizar lo descargado y descargar más si hace falta, dejando los datos preparados para embeddings. Esto autoriza ejecutar la limpieza y reposición recomendadas; no ejecutar todavía los modelos ni elegir modelos científicos finales. Se ha preguntado cómo tratar idiomas dudosos; se comunicó y aplicó el criterio conservador de conservarlos con marcas. No se presenta la ausencia de respuesta como aprobación explícita de umbrales.

## Pasos

1. Revisar evidencia y fijar reglas de limpieza comprobables: **complete**. Criterio conservador comunicado; dudosos conservados y marcados.
2. Preparar y probar reconstrucción reproducible, con originales intactos: **complete**. Pasan 14 pruebas específicas.
3. Completar primero 400.000 base global y después recalcular 100.000 complemento, usando páginas ya guardadas antes de la API: **complete**.
4. Auditar todos los registros finales, congelar IDs/textos y preparar entrada para embeddings: **complete**.
5. Actualizar informes y continuidad con cifras, límites y siguiente comando: **complete**.

## Reglas

- Original `data/corpus_500k/` y proyecto TFM: solo lectura.
- Salida nueva y separada: `data/corpus_clean_v1/`; evidencia en `research/cleaning_2026-09-15/`.
- Selección por orden aleatorio guardado, sin elección por área/citas/parecido para completar la base.
- Conservar razones de descartes y casos dudosos, hashes y versiones; no traducir ni generar abstracts.
- Modelos finales/entrada específica de cada modelo siguen siendo decisiones de la fase siguiente.

## Incidencias

- El entorno de auditoría no incluía requests/dotenv ni pip. Se habilitó pip con ensurepip y se añadieron únicamente las dependencias fijadas, sin modificar el entorno del extractor.
- Las pruebas detectaron un número incorrecto de columnas al importar páginas y una ruta relativa incorrecta en carpetas temporales enlazadas de macOS. Ambos corregidos antes de ejecutar la selección real; las 12 pruebas pasan.

## Comprobación ampliada antes del cierre

Se amplió la detección a los 286 grupos repetidos y las 6.138 páginas originales de candidatos. Dos recorridos provisionales se archivaron antes de declararlos listos; no se cambió silenciosamente un corpus final ni se realizaron nuevas descargas. La última selección usa la configuración ampliada, fijada antes de los embeddings.

- La revisión adicional del tercer recorrido detectó un texto ACS en la página nueva. Causa: las firmas de páginas solo habían ampliado el catálogo de textos antiguos; no se aplicaban directamente a candidatos nuevos. Se trasladó la misma comprobación al filtro común. Regresión reproducida antes de corregirla y 14 pruebas posteriores aprobadas, incluida reutilización de páginas adicionales sin llamadas API. Tercer recorrido archivado; reconstrucción final con `./prepare.sh prepare --offline`, log `data/preparation_closed_run.log`.
- La figura tenía el título recortado; se ajustó el margen superior, sin cambiar datos ni escala. Exportación final inspeccionada, con el título completo.

- La sustitución de `NEXT_STEPS.md` no pudo hacerse borrando y creando el mismo archivo en un único parche. Se realizó como una escritura única, sin pérdida del original antes de la edición.

## Cierre

Todos los pasos terminados. `readiness.json` y `./prepare.sh preflight` confirman 500.000 filas preparadas; validación completa y segunda comprobación de idioma/contenido aprobadas. Continuar por `EMBEDDINGS_READY.md`, acordando modelos/versiones antes de calcular. Originales intactos; sin embeddings ni commits.
