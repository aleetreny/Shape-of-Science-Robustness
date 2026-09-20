# Estado actual: manuscrito completo para revisión del autor

**Última entrega, 19-09-2026:** [tres versiones completas con identidad creciente](MANUSCRIPT_VOICES.md), cada una en inglés y español. El autor ha confirmado el título vigente. Se recomienda V2, razonamiento propio, pero ninguna opción está elegida. Los seis PDF están revisados y los originales permanecen intactos.

**Revisión previa:** [cinco comentarios del PDF resueltos](MANUSCRIPT_COMMENTS.md). Tablas, título, Figura 1B y declaración breve de IA actualizados en inglés y español, sin cambios científicos.

**18-09-2026.** El artículo y suplemento están redactados. [MANUSCRIPT_LAYOUT.md](MANUSCRIPT_LAYOUT.md) enlaza PDF y fuentes; [MANUSCRIPT_REVIEW.md](MANUSCRIPT_REVIEW.md), la revisión. Principal: 4.383 palabras de cuerpo, resumen de 190, dos tablas y cuatro figuras; 19 páginas con referencias. Suplemento: 33 páginas, 17 grupos de tablas y diez figuras. Resultados, corpus y modelos conservados.

Autoría y declaraciones confirmadas: Alejandro Treny Ortega, investigador independiente, sin financiación externa ni conflictos de interés. La ayuda de Codex consta en el texto. El formato propio no es una plantilla oficial QSS; no presupone que el autor ya haya aprobado el borrador.

**Copia para leer en español:** [MANUSCRIPT_SPANISH.md](MANUSCRIPT_SPANISH.md), artículo de 21 páginas y suplemento de 35. Traducción completa solicitada después, con tablas y figuras. Los cinco comentarios posteriores del autor ya están aplicados a ambas versiones; la numeración se conserva y los originales anteriores están archivados.

## Punto exacto para continuar

1. Elegir una de las [tres alternativas de voz](MANUSCRIPT_VOICES.md) o señalar qué pasajes combinar. Leer primero resumen, introducción, comienzo de la discusión y conclusión. La recomendación V2 no sustituye la elección personal. El manuscrito anterior sigue siendo canónico; no volver a redactar por encontrar planes históricos. Referencia editorial: [AUTHOR_VOICE.md](AUTHOR_VOICE.md), [MANUSCRIPT_BLUEPRINT.md](MANUSCRIPT_BLUEPRINT.md) y [QSS_STRUCTURE_REVIEW.md](QSS_STRUCTURE_REVIEW.md).
2. Aplicar los cambios que pida el autor, conservando la correspondencia con los resultados y los límites de cada control. No repetir experimentos ni añadir modelos automáticamente. El paquete se recompila con `./manuscript/build.sh`.
3. Antes de enviar: datos de correspondencia, revisión humana de texto/contribuciones, normas QSS vigentes y estilo de referencias, según [QSS_CHECK.md](docs/QSS_CHECK.md). El texto científico está terminado como borrador, no certificado para envío.
4. Acordar y verificar el [depósito persistente del material esencial](docs/DATA_RELEASE.md) y la licencia. El commit/push previo se cumplió en `44c9410`; esta entrega no incluye otra subida, depósito o envío. No reactivar automatizaciones.

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
