# Revisión final de los embeddings

**Terminados y comprobados los diez modelos: 500.000 artículos en cada uno.** El último acabó el 17-09-2026 a las 06:29 de Madrid. La revisión posterior no encontró archivos dañados, huecos, IDs desordenados ni valores numéricos inválidos. La preparación técnica para comparar está lista; el diseño científico sigue pendiente de acuerdo.

## Qué se ha comprobado

- Los mismos 500.000 IDs y textos de origen en los diez modelos, en el mismo orden: 400.000 de base y 100.000 de complemento. 26 áreas y 130 combinaciones área/período; mínimo 2.165 artículos.
- Todos los bloques, huellas de los archivos, tamaños de vector y valores. Son **8.802 archivos de vectores, 4.890 bloques y 18 variantes de diez modelos**. Ningún bloque provisional pendiente.
- Corpus, configuración, versiones oficiales, pesos, programa guardado y entorno coinciden con los fijados. No se han reutilizado los SPECTER2 antiguos de procedencia incierta.
- Pruebas habitual y de texto común: 1.300 artículos en cada modelo. El control común no produce recortes adicionales. En los 678 artículos cuyo texto no cambió, las 18 variantes reproducen el resultado con diferencias numéricas mínimas; máximo absoluto inferior a 0,000007. Esto comprueba coherencia de ejecución, no suficiencia científica del control.
- El nuevo lector ha recorrido las 18 variantes completas, manteniendo IDs, calidad y grupos. Ocho pruebas adicionales comprueban errores de correspondencia, archivos alterados, huecos, dimensiones, valores inválidos y filtros. Todo aprobado.

## Diferencias en cuánto texto pudo leer cada modelo

«Recortado» significa que el título y resumen preparados superaban el límite de entrada del modelo; **no** que se perdiera el archivo o el artículo. El porcentaje cuenta artículos afectados, no la proporción del texto que falta.

| Modelo | Artículos con texto recortado | Porcentaje |
| --- | ---: | ---: |
| SPECTER | 28.285 | 5.66% |
| SPECTER2 | 24.988 | 5.00% |
| SciNCL | 24.985 | 5.00% |
| SciBERT | 24.808 | 4.96% |
| BERT | 34.331 | 6.87% |
| MPNet | 100.799 | 20.16% |
| MiniLM | 247.910 | 49.58% |
| PubMedBERT / BiomedBERT | 23.728 | 4.75% |
| BioBERT | 45.016 | 9.00% |
| SimCSE | 34.331 | 6.87% |

MiniLM recorta con más frecuencia y de forma desigual entre áreas: de 20,26% en Matemáticas a 75,89% en Inmunología y Microbiología. MPNet va de 5,04% en Informática a 40,49% en Medicina. Las cifras incluyen base y complemento, por lo que describen **este corpus**, no todo OpenAlex.

**Esto debe formar parte del análisis:** las diferencias entre mapas pueden reflejar tanto el modelo como la cantidad de texto que leyó. El usuario ya aceptó comprobar también un fragmento idéntico. Falta acordar el tamaño científico de ese control. Los 252.089 artículos leídos completos por todos permiten otras comprobaciones, pero seleccionar solo esos textos cortos cambia la composición y no sustituye automáticamente el control.

Detalle por modelo, área, período y grupo: [truncation_by_field_period_cohort.csv](research/embedding_final_audit_2026-09-17/truncation_by_field_period_cohort.csv). Resumen por área: [truncation_by_field.csv](research/embedding_final_audit_2026-09-17/truncation_by_field.csv). Cobertura completa conjunta: [full_text_coverage_by_field_period.csv](research/embedding_final_audit_2026-09-17/full_text_coverage_by_field_period.csv).

## Qué conserva límites y decisiones pendientes

Los archivos correctos no demuestran ausencia de sesgo ni precisión suficiente para cualquier comparación. Se conservan los filtros y límites de [CLEANING.md](CLEANING.md) y [CORPUS_BALANCE.md](CORPUS_BALANCE.md). Hay 9.883 registros con idioma ambiguo, 3.002 con posible mezcla de idiomas, 42.849 resúmenes de 50–79 palabras, 33 casos marcados para revisión de contenido, 18 registros con DOI duplicado y 124 con texto idéntico. Las marcas se solapan y no significan necesariamente errores; no se aplicaron exclusiones nuevas. Los grupos de texto normalizado también siguen disponibles.

La base y el refuerzo permanecen separados. Las cuatro familias BERT conservan media/CLS/SEP; principal y normalización siguen abiertos. La población sigue siendo la literatura que cumple los filtros, no toda la ciencia. No se han calculado acuerdos entre modelos ni elegido recetas según resultados favorables.

## Organización y evidencia

- [DATA_CATALOG.md](DATA_CATALOG.md): rutas, versiones, variantes y lector listo para usar. Los originales permanecen en sus ubicaciones; se añade solo un índice de unos 45 MB, sin copiar textos o vectores.
- [ANALYSIS_PROPOSAL.md](ANALYSIS_PROPOSAL.md): comparación propuesta y decisiones que deben acordarse antes de ejecutar.
- [audit_summary.json](research/embedding_final_audit_2026-09-17/audit_summary.json): resumen comprobable; [audit.py](research/embedding_final_audit_2026-09-17/audit.py): auditoría independiente de procedencia, tablas y recortes.
- [full_verification.json](research/embedding_final_audit_2026-09-17/full_verification.json): lectura y verificación de los diez resultados completos. [model_preflight.json](research/embedding_final_audit_2026-09-17/model_preflight.json) y [corpus_preflight.json](research/embedding_final_audit_2026-09-17/corpus_preflight.json): pesos, entorno y corpus. [pilot_verification.json](research/embedding_final_audit_2026-09-17/pilot_verification.json) y [control_verification.json](research/embedding_final_audit_2026-09-17/control_verification.json): pruebas técnicas.
- [reader_tests.txt](research/embedding_final_audit_2026-09-17/reader_tests.txt) y [reader_verification.json](research/embedding_final_audit_2026-09-17/reader_verification.json): ocho pruebas y lectura real de las 18 variantes. Máximo de memoria del lector: 0,72 GB en esta máquina.

Los vectores ocupan 26,88 GB decimales (25,04 GiB). La suma de tiempo de inferencia registrado es 24,13 horas; no incluye todas las pausas, carga, escrituras o revisión. No es el tiempo transcurrido en el reloj desde el primer arranque.
