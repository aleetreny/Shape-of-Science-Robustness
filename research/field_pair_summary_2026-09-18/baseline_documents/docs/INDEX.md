# Guía del repositorio

## Para entender el estudio

1. [README](../README.md): pregunta, material y entrada rápida.
2. [Revisión antes del paper](../PREPAPER_REVIEW.md): qué se comprobó y qué límites quedan.
3. [Resultados principales](../ROBUSTNESS_RESULTS.md) y [conclusiones frente a controles](../CONCLUSION_CONTROLS.md).
4. [Artículos, especialidades y relaciones concretas](../CASE_ATLAS.md).
5. [Antecedentes y aportación](../references/RELATED_WORK.md), [biblioteca verificada](../references/README.md).
6. [Propiedades concretas de la forma](../MORPHOLOGY_RESULTS.md): nuevo piloto, con controles y límites de fragmentación.
7. [Esquema para QSS](../PAPER_OUTLINE.md). Aún no es un manuscrito.

## Para revisar o repetir los cálculos

| Etapa | Documento de referencia | Código / salida |
| --- | --- | --- |
| Corpus | [Protocolo](../CORPUS_PROTOCOL.md), [limpieza](../CLEANING.md), [inventario anterior](../INVENTORY.md) | `sos_download/`, `sos_prepare/`; `data/corpus_clean_v1/` |
| Diez modelos | [Selección](../MODEL_SELECTION.md), [cálculo](../EMBEDDINGS.md), [auditoría](../EMBEDDINGS_AUDIT.md) | `sos_embed/`; `data/embeddings_v1/` |
| Forma y vecinos | [Protocolo](../ANALYSIS_PROTOCOL.md), [métodos](../METHODS_ANALYSIS.md) | `sos_analysis/`; `data/analysis_v1/` |
| Tres entradas y recetas | [Checklist](../CHECKLIST_PROTOCOL.md), [métodos](../METHODS_CHECKLIST.md) | `sos_followup/`; `data/checklist_v1/` |
| Ampliación y controles | [Métodos](../METHODS_ROBUSTNESS.md), [recetas](../POOLING.md), [estabilidad](../SAMPLING_STABILITY.md) | `sos_deep/`; `data/robustness_v2/` |
| Casos concretos y revisión | [Protocolo del atlas](../CASE_ATLAS_PROTOCOL.md), [revisión](../PREPAPER_REVIEW.md) | `sos_review/`; `data/prepaper_v1/`; `reports/prepaper_v1/` |

[Reproducción](REPRODUCING.md), [catálogo de datos](../DATA_CATALOG.md), [preparación del archivo público](DATA_RELEASE.md), [comprobación QSS](QSS_CHECK.md).

## Qué es actual y qué es historial

**Actual:** `ROBUSTNESS_RESULTS.md` reúne la ampliación a 52k. `PREPAPER_REVIEW.md` añade la última auditoría y los casos. El atlas no sustituye los resultados generales.

**Historial conservado:** `ANALYSIS_RESULTS.md` y `CHECKLIST_RESULTS.md` describen fases válidas con otras selecciones/tamaños. `ANALYSIS_PROPOSAL.md`, `02_open_questions.md` y planes iniciales contienen propuestas históricas. No reabrir decisiones por leerlos fuera de fecha.

**Versiones retiradas del uso actual:** `control_review/` mezcla dos tipos de comparación MiniLM; usar `control_review_v2/`. `structural_review/` y `structural_review_v2/` son intentos previos; usar `structural_review_v3/`. Las carpetas `preview/` son vistas provisionales. No borrar estos antecedentes ni mezclarlos con las entregas finales.

Se mantienen las rutas originales porque los manifiestos y programas congelados las utilizan. La organización se hace con este índice y catálogos, no rompiendo esos enlaces.

## Para retomar el trabajo

Leer [NEXT_STEPS.md](../NEXT_STEPS.md), [AGENTS.md](../AGENTS.md) y el final de [DECISIONS.md](../DECISIONS.md), [progress.md](../progress.md) y [task_plan.md](../task_plan.md). Las automatizaciones anteriores están pausadas.


## Piloto de morfología, 18-09-2026

[Resultados](../MORPHOLOGY_RESULTS.md) · [Protocolo fijado](../MORPHOLOGY_PROTOCOL.md) · [Registro técnico](../METHODS_MORPHOLOGY.md) · [Literatura y alternativas](../research/morphology_2026-09-18/LITERATURE.md). Código separado `sos_morphology/`; salidas `data/morphology_pilot_v1/` y `reports/morphology_pilot_v1/`. Veinte tablas y cinco figuras. Las decisiones históricas de no añadir morfología se referían al cierre anterior; esta exploración fue autorizada después. No se sustituyen CKA/vecinos ni se modifican sus cifras.
