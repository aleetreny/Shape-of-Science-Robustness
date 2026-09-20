# Revisión del texto completo

18-09-2026. Se conserva la apertura anterior y su revisión de fuentes. Esta entrega añade métodos, resultados, discusión, conclusión, resumen y métodos suplementarios, y revisa el conjunto. No cambia ningún resultado científico.

## Voz, extensión e hilo

La pregunta que organiza el texto es qué comparación sobrevive al cambiar la representación. El cuerpo no intenta enumerar todos los experimentos. Tiempo, Medicina, familias, casos y controles extensos tienen su desarrollo en el suplemento; los límites que cambian la lectura principal aparecen también en el cuerpo. La discusión tiene tres apartados, sin repetir una lista de las tres preguntas o todas las cifras de resultados.

4.383 palabras de cuerpo, sin encabezados, citas expandidas, tablas/pies, matemáticas ni declaraciones; resumen 190. Regla reproducible en `check_text.py` y resultado en `word_count.json`. El presupuesto histórico de 6.750 no se rellenó. Inglés académico claro, párrafos de longitudes diferentes, mecanismos y denominadores visibles. Se evitó una historia ficticia de descubrimiento, superlativos, primacía absoluta, modelos ganadores y traducción literal del blog. Esta revisión no acredita que el autor haya aprobado todavía la voz inglesa.

## Correspondencia con los resultados

| Parte | Fuente vigente | Comprobación y límite |
| --- | --- | --- |
| Corpus y reparto | CORPUS_PROTOCOL, CLEANING; Table S1 y su CSV | 500k = 400k + 100k; mínimo 2.165/celda. Etiqueta English y filtro conservador no garantizan que todos los resúmenes estén solo en inglés. Introducción corregida a «labelled English». |
| Modelos y entradas | POOLING, METHODS_ANALYSIS, METHODS_ROBUSTNESS; configuración y Table S2 | Diez checkpoints; cuatro mean con símbolos especiales incluidos. Dos paneles distintos de 52k. MiniLM256 es habitual, 512 sensibilidad. |
| Medidas | METHODS_ANALYSIS, METHODS_MORPHOLOGY, METHODS_FIELD_PAIRS | Normalizar antes de centrar; fórmula de corrección y orden de operaciones en suplemento. PR no cuenta temas; alternativas no son evidencias independientes. |
| Centros | CSV de centroid_scales y manifiesto figura 1 | Medias 0,939/0,911/0,902; referencias aleatorias 0,63–0,64. Objetos diferentes a comparación interna, sin efecto causal de escala. |
| Vecinos | ANALYSIS_RESULTS y `structure_paired_scope_summary.csv` | 30,3/31,9/17,5% con tres universos distintos. 127/90 y −1,35 pp solo en 217 Subfields, 50 consultas incluidas en ambos conjuntos de 256. |
| Acuerdo de medidas | Resumen principal y Table S4 | 0,891/0,881 comparan orden de pares; 0,920 forma–vecinos compara 45 promedios dependientes. No prueba de independencia. |
| Entrada | Tablas `input_input_effect_*` | 0,370/0,366/0,027; cambios de vecinos 68,8/70,7/22,1%. Promedios próximos no demuestran equivalencia. Recetas cambian también la referencia entre modelos. |
| Estabilidad de entrada | `input_alert_transition_counts.csv` | 72→5 en 100 selecciones y 31→4 en veinte, ambos sobre 520; no sustituir recuentos ni extender a toda métrica. |
| Geometría | Tablas de field_pair_summary y morphology | Todos los 325 pares, 26 condiciones; alternativas espectrales solo tres; mínimos operativos, no significación ni corte universal. |
| Centrado | `control_summary.csv` | 145/262 y 218/221 conservan los mismos modelos y signos en referencia y variante. Control puntual, no 26 repeticiones nuevas. |
| Conexión | Nueve nubes simuladas y Table S12–S13 | Contraejemplos y 51 alertas adicionales conservados; no llamar fragmentación temática al índice. |
| Casos y fuente | CASE_ATLAS y PREPAPER_REVIEW | Ejemplos seleccionados antes de leer títulos, después de acuerdos generales. Se conservan libro de historia, infección/política y anuncio. No prevalencia estimada de errores. |
| Tiempo/Medicina/familias | Tables S9–S11 | Cambio de signo con candidatos; composición y modelos biomédicos no explican una causa aislada; coeficientes no identificables se mantienen ausentes. |

`verify_claims.py` vuelve a contrastar las 23 entradas de evidencia del plano, añade tres comprobaciones sobre centros/resumen original y verifica las 217 direcciones de la figura 2. `verify_package.py` comprueba fuentes, cuotas, modelos, recuentos y alertas. Estas comprobaciones son sobre resultados guardados; no repiten experimentos ni constituyen validación temática externa.

## Fuentes externas empleadas al completar el manuscrito

La revisión de los ocho antecedentes de apertura y nueve fuentes de modelos está conservada en `../manuscript_opening_2026-09-18/CLAIM_REVIEW.md`. No se repite la búsqueda global para aparentar una nueva revisión exhaustiva.

| Fuente primaria consultada en esta entrega | Uso y profundidad |
| --- | --- |
| [Kornblith et al., 2019](https://proceedings.mlr.press/v97/kornblith19a.html) | Página oficial/resumen y metadatos: CKA y problema de comparar representaciones. La implementación exacta se verifica contra nuestros métodos guardados. |
| [Murphy et al., 2024](https://arxiv.org/abs/2405.01012) | Registro de autores/resumen v1: sesgo de CKA dependiente de tamaño/dimensión; mantenido como preprint. No se atribuye insesgadez exacta al cociente completo. |
| [Williams et al., 2021](https://proceedings.neurips.cc/paper/2021/hash/252a3dbaeb32e7690242ad3b556e626b-Abstract.html) | Página oficial/resumen: contexto de métricas y alineamiento. Las invariancias concretas se delimitan por nuestra normalización. |
| [Williams, 2024](https://proceedings.mlr.press/v285/williams24a.html) | Página PMLR: relación entre medidas; no se afirma que nuestra RSA por rangos sea idéntica a CKA corregida. |
| [Rudman et al., 2022](https://aclanthology.org/2022.findings-acl.262/) | Página oficial/resumen/metadatos: límites al interpretar geometría como isotropía. No se afirma que hayamos calculado IsoScore. |
| [Roy y Vetterli, 2007](https://www.eurasip.org/Proceedings/Eusipco/Eusipco2007/Papers/a5p-h05.pdf) | PDF, definición §2.1: rango basado en entropía, aplicado aquí a la matriz de covarianza. No se atribuye a ese artículo la fórmula PR. |
| [von Luxburg, 2007](https://link.springer.com/article/10.1007/s11222-007-9033-z) | Página editorial y registro canónico previo: fundamento de grafos/espectro; no valida la fragmentación temática de nuestro corpus. |
| [Priem et al., 2022](https://arxiv.org/abs/2205.01833v2) | Registro de autores v2 y metadatos: recurso OpenAlex, no sus recuentos actuales o clasificación posterior. |
| [OpenAlex Topics](https://help.openalex.org/data/topics/) | Documentación oficial consultada el 18-09-2026: jerarquía y asignación basada en título/resumen/citas/revista. Etiquetas inferidas, no verdad externa. |

Solo las dos últimas son nuevas entradas de contexto respecto a la biblioteca ya preparada. La biblioteca raíz de 54 no se modifica. `citation_validation.json` comprueba las 26 referencias realmente citadas en ambos documentos: cero errores, avisos, duplicados o claves ausentes. Es validación formal, diferenciada de la revisión de afirmaciones de arriba. El estilo autor-año se conserva como formato de trabajo; revisión editorial final pendiente.

## Declaraciones

El usuario confirmó directamente nombre completo, trabajo independiente, ninguna financiación y ningún conflicto de interés. Se usa «Alejandro Treny Ortega», «Independent researcher», «no external funding» y «no competing interests». No se añade institución, correo u ORCID. Contribuciones descritas de forma limitada al proyecto dirigido por el autor, sin inventar una validación humana terminada. La ayuda de Codex se declara en búsqueda, código, comprobación, presentación y redacción.

El corpus/vectores y ejecuciones completas no están depositados en archivo persistente. La disponibilidad no se infla por existir un repositorio GitHub. Lectura personal, datos de correspondencia, revisión final de normas, licencia y depósito siguen pendientes antes de enviar.
