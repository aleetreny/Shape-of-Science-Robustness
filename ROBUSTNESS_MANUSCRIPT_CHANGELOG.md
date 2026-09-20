# Cambios del manuscrito tras el cierre de robustez

20-09-2026. Cambios sincronizados en inglés y español. Se conserva el título y el tono claro aceptado. El original está archivado en `research/robustness_closure_2026-09-20/baseline_documents/`. No se han sustituido resultados históricos ni cambiado una regla para sostener una conclusión.

| Parte | Antes | Ahora | Motivo y evidencia |
| --- | --- | --- | --- |
| Resumen | Similitud media entre quitar resumen y cambiar modelo; procesamiento mencionado en general. | Diferencias claras entre modelos/reglas; apertura sensible al centrado; centros respaldados por repeticiones. | `headline_summary.csv`, `morphology_centering_summary.csv`, `centres_summary.csv`. |
| Métodos: centros | Una selección de 256 y referencia aleatoria resumida. Normalización final del centro implícita. | Receta completa, cincuenta selecciones, tamaños, omisiones y diseño anidado. | Auditoría del código y `centres_*.csv`. |
| Métodos: calidad | Filtro de calidad documentado para otros análisis. | Vecinos con idénticas consultas, candidatos completos y tamaños fijos; solo 63 celdas admiten 2.048. | `quality_summary.csv`; controles de 1.024 en las 130. |
| Métodos: forma | Alternativas espectrales parciales y centrado puntual. | Cobertura de 26 condiciones con transformación explícita. | `morphology_classification.csv`; `dimension_alternative_retention.csv`. |
| Resultados 4.1 / Figura 1 | 0,939/0,911/0,902 puntuales o con variación de especialidad. | 0,940/0,911/0,904; rangos de selecciones, tamaños y omisiones. | `centres_summary.csv`; normalización de centros sin cambios. |
| Resultados 4.1 | Media interna casi constante. | Añade 2.628/8.235 alertas locales (31,9 %). | Tabla original verificada; sin umbral nuevo. |
| Resultados 4.2 | 30,3 % de vecinos compartidos. | Conserva ese resultado y añade 30,58 a 31,43 % entre las mismas consultas; cambios pequeños con candidatos igualados. | `quality_summary.csv`; no afirma que todos los errores de origen sean inocuos. |
| Resultados 4.3 / encabezado | Quitar el resumen puede importar tanto como cambiar modelo. | Medias parecidas ocultan resultados opuestos por modelo. Se cuantifican las repeticiones, k y CLS/SEP. | `headline_*.csv`; medias no equivalentes ni universales. |
| Resultados 4.4 / Tabla S15 | Alternativas de dimensión: 196/221 con tres condiciones. | 209 con entropía; 190 con D80 y ambas, con 26 condiciones. | `dimension_alternative_retention.csv`; conjuntos de modelos actualizados. |
| Resultados 4.4 / Figura 4 | Centrado: retención puntual 145/262 y 218/221. | Repetición completa: 151/211 oposiciones totales; mismos modelos y direcciones, 128/204. Apertura al 5 %: 96 a 11. | `morphology_centering_summary.csv`; matiz adverso en el cuerpo. |
| Discusión / conclusión | Dependencia del modelo y advertencia general sobre procesamiento. | Distingue estabilidad media, diferencias entre modelos y dependencia fuerte de apertura respecto al procesamiento. | Conjunto de pruebas; no se declara una representación correcta. |
| Suplemento S4/S6/S7 | Centros y cobertura previos. | Receta exacta; convención de cuantiles de apertura explicitada; alternativas completas; controles puntuales conservados como tales. | Código congelado y auditoría de procedencia. |
| Suplemento S9 / Tablas S18–S20 / Figura S11 | No existían. | Diseños, rangos, omisiones, calidad, transiciones, modelos concretos y límites. | Todos los CSV del nuevo cierre, sin nueva inferencia. |

Los cambios de prosa completos, antes/después y por idioma, están en `research/robustness_closure_2026-09-20/main_changes.json` y `supplement_changes.json`. La Figura 3 conserva el experimento completo de 52.000; las nuevas repeticiones usan 26.000 por selección y se identifican por separado. Las declaraciones personales, referencias y título no cambian.
