# Guía del repositorio

**Cierre vigente, 20-09-2026:** controles finales terminados y congelados; [informe para el autor](../ROBUSTNESS_CLOSURE_REPORT.md) y [cambios del manuscrito](../ROBUSTNESS_MANUSCRIPT_CHANGELOG.md). El tono claro está aceptado. La revisión personal del contenido sigue pendiente.

La [primera revisión](../MANUSCRIPT_REVIEW.md), los [cinco comentarios resueltos](../MANUSCRIPT_COMMENTS.md) y las [seis alternativas de voz](../MANUSCRIPT_VOICES.md) se conservan como historial. Para continuar, leer [NEXT_STEPS.md](../NEXT_STEPS.md).

## Para entender el estudio

1. [README](../README.md): pregunta, material y entrada rápida.
2. [Revisión antes del paper](../PREPAPER_REVIEW.md): qué se comprobó y qué límites quedan.
3. [Resultados principales](../ROBUSTNESS_RESULTS.md) y [conclusiones frente a controles](../CONCLUSION_CONTROLS.md).
4. [Artículos, especialidades y relaciones concretas](../CASE_ATLAS.md).
5. [Antecedentes y aportación](../references/RELATED_WORK.md), [biblioteca verificada](../references/README.md).
6. [Propiedades concretas de la forma](../MORPHOLOGY_RESULTS.md): nuevo piloto, con controles y límites de fragmentación.
7. [Resumen final de las 325 parejas](../FIELD_PAIR_RESULTS.md): acuerdos, contradicciones, magnitudes y límites.
8. [Estructura y argumentación en QSS](../QSS_STRUCTURE_REVIEW.md): 34 artículos seleccionados, versiones y límites de lectura explícitos.
9. [Plano detallado del manuscrito](../MANUSCRIPT_BLUEPRINT.md): plan histórico de párrafos, elementos, citas y evidencia; la redacción vigente está en MANUSCRIPT_CLARITY. [Vista general](../PAPER_OUTLINE.md).
10. [Voz del autor](../AUTHOR_VOICE.md): lectura de 50 entradas del portfolio y reglas usadas para adaptar esa voz a QSS; [investigación sobre escritura](../research/writing_blueprint_2026-09-18/STYLE_RESEARCH.md). V2 elegida; la petición de claridad del 20-09 es prioritaria.

11. [Manuscrito vigente y paquete editable](../MANUSCRIPT_CLARITY.md): cuerpo, resumen, declaraciones y suplemento escritos. [Revisión editorial/visual](../MANUSCRIPT_REVIEW.md) y [comprobación de afirmaciones](../research/manuscript_full_2026-09-18/CLAIM_REVIEW.md). La apertura anterior se conserva como historial.

## Para revisar o repetir los cálculos

| Etapa | Documento de referencia | Código / salida |
| --- | --- | --- |
| Corpus | [Protocolo](../CORPUS_PROTOCOL.md), [limpieza](../CLEANING.md), [inventario anterior](../INVENTORY.md) | `sos_download/`, `sos_prepare/`; `data/corpus_clean_v1/` |
| Diez modelos | [Selección](../MODEL_SELECTION.md), [cálculo](../EMBEDDINGS.md), [auditoría](../EMBEDDINGS_AUDIT.md) | `sos_embed/`; `data/embeddings_v1/` |
| Forma y vecinos | [Protocolo](../ANALYSIS_PROTOCOL.md), [métodos](../METHODS_ANALYSIS.md) | `sos_analysis/`; `data/analysis_v1/` |
| Tres entradas y recetas | [Checklist](../CHECKLIST_PROTOCOL.md), [métodos](../METHODS_CHECKLIST.md) | `sos_followup/`; `data/checklist_v1/` |
| Ampliación y controles | [Métodos](../METHODS_ROBUSTNESS.md), [recetas](../POOLING.md), [estabilidad](../SAMPLING_STABILITY.md) | `sos_deep/`; `data/robustness_v2/` |
| Casos concretos y revisión | [Protocolo del atlas](../CASE_ATLAS_PROTOCOL.md), [revisión](../PREPAPER_REVIEW.md) | `sos_review/`; `data/prepaper_v1/`; `reports/prepaper_v1/` |
| Propiedades de la forma | [Protocolo](../MORPHOLOGY_PROTOCOL.md), [métodos](../METHODS_MORPHOLOGY.md) | `sos_morphology/`; `data/morphology_pilot_v1/` |
| Resumen de parejas | [Protocolo](../FIELD_PAIR_PROTOCOL.md), [métodos](../METHODS_FIELD_PAIRS.md) | `sos_pair_summary/`; `data/field_pair_summary_v1/`; `reports/field_pair_summary_v1/` |

[Reproducción](REPRODUCING.md), [catálogo de datos](../DATA_CATALOG.md), [preparación del archivo público](DATA_RELEASE.md), [comprobación QSS](QSS_CHECK.md).

## Qué es actual y qué es historial

**Actual:** `ROBUSTNESS_RESULTS.md` reúne la ampliación a 52k. `PREPAPER_REVIEW.md` añade la auditoría y los casos. `MORPHOLOGY_RESULTS.md` y `FIELD_PAIR_RESULTS.md` añaden las propiedades y el resumen de todas las parejas. Las entregas se complementan; no sustituyen las cifras de fases anteriores.

**Historial conservado:** `ANALYSIS_RESULTS.md` y `CHECKLIST_RESULTS.md` describen fases válidas con otras selecciones/tamaños. `ANALYSIS_PROPOSAL.md`, `02_open_questions.md` y planes iniciales contienen propuestas históricas. No reabrir decisiones por leerlos fuera de fecha.

**Versiones retiradas del uso actual:** `control_review/` mezcla dos tipos de comparación MiniLM; usar `control_review_v2/`. `structural_review/` y `structural_review_v2/` son intentos previos; usar `structural_review_v3/`. Las carpetas `preview/` son vistas provisionales. No borrar estos antecedentes ni mezclarlos con las entregas finales.

Se mantienen las rutas originales porque los manifiestos y programas congelados las utilizan. La organización se hace con este índice y catálogos, no rompiendo esos enlaces.

## Para retomar el trabajo

Leer [NEXT_STEPS.md](../NEXT_STEPS.md), [AGENTS.md](../AGENTS.md) y el final de [DECISIONS.md](../DECISIONS.md), [progress.md](../progress.md) y [task_plan.md](../task_plan.md). Las automatizaciones anteriores están pausadas.


## Piloto de morfología, 18-09-2026

[Resultados](../MORPHOLOGY_RESULTS.md) · [Protocolo fijado](../MORPHOLOGY_PROTOCOL.md) · [Registro técnico](../METHODS_MORPHOLOGY.md) · [Literatura y alternativas](../research/morphology_2026-09-18/LITERATURE.md). Código separado `sos_morphology/`; salidas `data/morphology_pilot_v1/` y `reports/morphology_pilot_v1/`. Veinte tablas y cinco figuras. Las decisiones históricas de no añadir morfología se referían al cierre anterior; esta exploración fue autorizada después. No se sustituyen CKA/vecinos ni se modifican sus cifras.


## Cierre final de robustez, 20-09-2026

[Informe del autor](../ROBUSTNESS_CLOSURE_REPORT.md) · [Cambios del texto](../ROBUSTNESS_MANUSCRIPT_CHANGELOG.md) · [Protocolo](../ROBUSTNESS_CLOSURE_PROTOCOL.md) · [Auditoría de once afirmaciones](../research/robustness_closure_2026-09-20/CLAIM_AUDIT.md). Las cifras actuales sobre centrado y alternativas sustituyen los controles parciales anteriores, que siguen conservados como historial.
