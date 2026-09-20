# Estado actual: V2 elegida y manuscrito reescrito con más claridad

**20-09-2026.** El autor elige la voz 2 y pide una explicación más fácil de seguir. La [entrega vigente](MANUSCRIPT_CLARITY.md) reescribe todo el artículo en inglés y español: presenta el problema antes de las medidas, explica qué pregunta responde cada muestra y hace comprensible el resumen.

Inglés: 3.989 palabras de cuerpo y 192 de resumen; 19 páginas con figuras y referencias. Español: 20 páginas. Suplementos: 34 y 36 páginas. Se mantienen el título confirmado, las cifras, las figuras, las declaraciones y los resultados científicos. Las ediciones anteriores y las seis alternativas están archivadas.

Autoría y declaraciones confirmadas: Alejandro Treny Ortega, investigador independiente, sin financiación externa ni conflictos de interés. La ayuda de Codex consta en el texto. El formato propio no es una plantilla oficial QSS. La elección de voz no equivale a aprobación del contenido completo.

## Punto exacto para continuar

1. Recoger los comentarios del autor sobre la nueva lectura, especialmente resumen, introducción y explicación de las muestras. V2 ya está elegida; no volver a pedir esa decisión. Referencias: [AUTHOR_VOICE.md](AUTHOR_VOICE.md), [MANUSCRIPT_CLARITY.md](MANUSCRIPT_CLARITY.md) y el [plano histórico de evidencia](MANUSCRIPT_BLUEPRINT.md).
2. Aplicar los cambios solicitados en ambos idiomas, conservando cifras y límites. Compilar con `./manuscript/build.sh` y `./manuscript_es/build.sh`. Las tablas principales tienen fuentes editoriales propias para que regenerarlas no recupere el texto antiguo.
3. Antes de enviar: correspondencia, aprobación personal de texto y contribuciones, normas QSS vigentes y estilo bibliográfico, según [QSS_CHECK.md](docs/QSS_CHECK.md).
4. Acordar el [depósito persistente del material esencial](docs/DATA_RELEASE.md) y la licencia. El commit/push anterior se cumplió en `44c9410`; esta revisión no incluye nueva subida, depósito ni envío. No reactivar automatizaciones ni repetir experimentos por retomar.

Los [cinco comentarios del PDF](MANUSCRIPT_COMMENTS.md), la [primera revisión editorial](MANUSCRIPT_REVIEW.md) y las [alternativas de voz](MANUSCRIPT_VOICES.md) se conservan como historial. Sus recuentos describen aquellas ediciones.

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
| Tres alternativas completas de voz, inglés y español | MANUSCRIPT_VOICES.md, manuscript_variants/, output/pdf/voice_variants/ |
| Manuscrito completo, 19 grupos de tablas y 14 figuras | `manuscript/`, `output/`, `research/manuscript_full_2026-09-18/` |
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
