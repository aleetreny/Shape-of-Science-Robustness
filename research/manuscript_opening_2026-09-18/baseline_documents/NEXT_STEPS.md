# Estado actual: maqueta, tablas y figuras preparadas

**18-09-2026.** El usuario pidió generar todos los elementos y ver la estructura renderizada. [MANUSCRIPT_LAYOUT.md](MANUSCRIPT_LAYOUT.md) enlaza los dos PDF y el paquete editable; [la guía](manuscript/README.md) explica cómo compilar. Principal: dos tablas/cuatro figuras. Suplemento: 17 grupos de tablas/diez figuras, con CSV completos. El texto del artículo sigue como plan; pies y notas describen resultados guardados. No se repitió ningún experimento.

El formato es una maqueta propia para primera entrega flexible de QSS, no una plantilla oficial localizada. La consulta de normas sigue limitada por un índice antiguo. No se han supuesto nombres, afiliaciones, declaraciones, licencia o depósito.

## Punto exacto para continuar

1. Revisar la maqueta en [MANUSCRIPT_LAYOUT.md](MANUSCRIPT_LAYOUT.md). Compilar con `./manuscript/build.sh`. Leer [MANUSCRIPT_BLUEPRINT.md](MANUSCRIPT_BLUEPRINT.md) y [AUTHOR_VOICE.md](AUTHOR_VOICE.md). Para el fundamento editorial, [QSS_STRUCTURE_REVIEW.md](QSS_STRUCTURE_REVIEW.md). Distinguir normas oficiales consultadas mediante índice antiguo, prácticas observadas y propuesta propia. Los 465 registros del marco no son 465 artículos leídos; las versiones de autor no certifican la estructura editorial final.
2. Revisar [ROBUSTNESS_RESULTS.md](ROBUSTNESS_RESULTS.md), [CONCLUSION_CONTROLS.md](CONCLUSION_CONTROLS.md) y [CASE_ATLAS.md](CASE_ATLAS.md): resultados generales y ejemplos concretos.
3. Redactar solo cuando el usuario lo solicite. Empezar por métodos/resultados, siguiendo el plano y su [matriz de evidencia](research/writing_blueprint_2026-09-18/claim_evidence.csv), y comprobar la adaptación inglesa de la voz en el primer bloque. Para geometría usar [FIELD_PAIR_RESULTS.md](FIELD_PAIR_RESULTS.md), [METHODS_FIELD_PAIRS.md](METHODS_FIELD_PAIRS.md) y [MORPHOLOGY_RESULTS.md](MORPHOLOGY_RESULTS.md). Biblioteca científica canónica: 54 entradas; revisión QSS: 34 con solapamientos; escritura: cuatro para trabajo editorial. No sumarlas como referencias únicas ni añadir automáticamente las de estilo al paper.
4. Antes de enviar, completar [QSS_CHECK.md](docs/QSS_CHECK.md) y el [depósito de datos/código](docs/DATA_RELEASE.md). El commit/push solicitado previamente se cumplió en `44c9410`; esta revisión no implica otra subida automática. Corpus y vectores siguen locales; no hay depósito permanente, licencia general elegida ni envío a revista.

## Límites que deben acompañar las conclusiones

- Corpus de 500k: 400k base + 100k complemento; inglés, abstract disponible, 2000–2024 y clasificación OpenAlex. No representa toda la producción mundial.
- Tres entradas en 52k, con el piloto de 26k incluido; el control de fragmento común de 52k es otra selección. Mean principal para cuatro BERT; CLS/SEP como controles.
- Se conservan cinco alertas de entrada en 52k/100 selecciones, las 50 originales y las de Subfields. No son intervalos poblacionales ni tareas que se resuelvan cambiando umbrales.
- No hay caída universal de acuerdo al pasar a especialidades. Los candidatos condicionan la comparación: ambos ámbitos incluyen las 50 consultas del Subfield en sus 256 candidatos.
- Los casos muestran errores de OpenAlex y un aviso no detectado. Se mantuvieron con notas. La pequeña sensibilidad a 82 títulos genéricos no estima el error temático total ni limpia los candidatos.
- Atlas: 217 especialidades, 183 comparadas bajo 27 condiciones; 10.850 consultas con diez selecciones y 531.650 relaciones siempre elegibles. Los ejemplos son exploratorios. Centros de especialidades: 23.436 parejas, receta principal; sin control de receta adicional.
- Consenso no es calidad. CKA no es porcentaje de ciencia correcta; 45 pares no son independientes. Familias/Medicina no identifican causas; el cambio temporal no demuestra convergencia causal.
- La biblioteca tiene 54 entradas comprobadas. Ya existen trabajos cercanos sobre forma, vecinos, entrada, categorías y familias; defender aportación concreta, sin primacía absoluta.

- Morfología: 52k principales, 20 medias muestras y cinco selecciones del corpus de 500k; 16.884 conjuntos de medidas. No son experimentos independientes ni intervalos poblacionales.
- Apertura/PR repiten bien en general; conservar cuatro alertas de PR en medias muestras y 51 de conexión en las selecciones adicionales. No mezclarlas con las alertas anteriores.
- La apertura depende del centro/receta; PR no cuenta temas y D80 puede cambiar puestos. La conexión depende de n y k y no equivale a fragmentación temática. No añadir nuevos índices o inferencia automáticamente.
- Parejas: apertura 42 acuerdos de diez / 262 contradicciones persistentes / 21 sin conclusión común; PR 54 / 221 / 50, siempre de 325. Contradicción significa al menos dos modelos con signos opuestos persistentes; no los diez en desacuerdo. A 5% quedan 96/177 contradicciones y a 10%, 19/126; no ocultar magnitudes pequeñas ni declarar un corte universal.
- Son direcciones persistentes en principal + 20 medias muestras + 5 selecciones del corpus; no intervalos poblacionales. Alternativas espectrales solo tienen tres condiciones guardadas. Los controles son puntuales. Centrado global conserva los mismos testigos en 145/262 aperturas y 218/221 PR; seis modelos de similitud mantienen 231/160 contradicciones. No convertir esos grupos en una explicación causal.

## Dónde está cada entrega

| Material | Ubicación |
| --- | --- |
| Maqueta, fuentes, 19 grupos de tablas y 14 figuras | `manuscript/`, `output/`, `research/manuscript_layout_2026-09-18/` |
| Resumen científico, 12 tablas y dos figuras | `reports/field_pair_summary_v1/`, `data/field_pair_summary_v1/`, `research/field_pair_summary_2026-09-18/` |
| Piloto de morfología, 20 tablas y cinco figuras | `reports/morphology_pilot_v1/`, `data/morphology_pilot_v1/`, `research/morphology_2026-09-18/` |
| Nueva revisión y atlas | `reports/prepaper_v1/`, `data/prepaper_v1/`, `research/prepaper_2026-09-17/` |
| Resultados ampliados, 50 tablas y siete figuras | `reports/robustness_v2/final/` |
| Auditoría de 15 componentes | `data/robustness_v2/final_audit/` |
| Comparación inicial sobre 500k | `reports/analysis_v1/final/` |
| Piloto histórico de 26k | `reports/checklist_v1/final/` |
| Catálogo e índice de documentos | `DATA_CATALOG.md`, `docs/INDEX.md` |

Usar `control_review_v2` y `structural_review_v3`; versiones anteriores y vistas provisionales se conservan como historial. Las fuentes científicas y sus salidas tienen huellas/copia. No editarlas y reanudar como si fueran la misma versión.

## Un comando para reconstruir solo la presentación del atlas

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_review.report
```

No ejecuta modelos ni vecinos. Después hay que revisar visualmente las figuras reconstruidas. Más opciones y requisitos en [REPRODUCING.md](docs/REPRODUCING.md).

Los datos grandes siguen locales y fuera de Git. No relanzar `start_embeddings.sh`, descargas ni ejecutores ya terminados. Las automatizaciones anteriores permanecen pausadas. Una ampliación futura debe responder a una afirmación concreta que aún no tenga apoyo suficiente.
