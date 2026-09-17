> PROPUESTA HISTÓRICA, NO APROBADA. Sustituida por `../FIELD_SAMPLING.md` el 2026-09-14. Se conserva para saber qué se había planteado.

# Muestreo por Field: conteos y propuesta

Revisión: 14-09-2026. **Unidad principal: los 26 Fields.** Los Subfields pueden servir como estratos internos de muestreo. Esto es una propuesta de diseño: no se ha seleccionado una muestra ni ejecutado experimentos.

## Qué tenemos

Conteos calculados sobre los **2.378.036 papers del corpus completo**, incluidos los que quedaron fuera del subconjunto analítico temporal del TFM. Todos tienen SPECTER2 según la auditoría anterior.

| Field | Papers disponibles | % de nuestra muestra | % referencia OpenAlex filtrada |
| --- | ---: | ---: | ---: |
| Medicine | 403.376 | 16,96 % | 17,88 % |
| Social Sciences | 207.257 | 8,72 % | 10,22 % |
| Engineering | 157.673 | 6,63 % | 16,25 % |
| Biochemistry, Genetics and Molecular Biology | 135.852 | 5,71 % | 5,76 % |
| Arts and Humanities | 123.705 | 5,20 % | 3,14 % |
| Computer Science | 109.980 | 4,62 % | 8,63 % |
| Environmental Science | 109.936 | 4,62 % | 4,57 % |
| Agricultural and Biological Sciences | 104.207 | 4,38 % | 4,50 % |
| Health Professions | 99.687 | 4,19 % | 2,02 % |
| Mathematics | 88.331 | 3,71 % | 1,71 % |
| Business, Management and Accounting | 79.204 | 3,33 % | 2,94 % |
| Materials Science | 78.777 | 3,31 % | 3,23 % |
| Neuroscience | 78.137 | 3,29 % | 1,59 % |
| Earth and Planetary Sciences | 77.009 | 3,24 % | 1,87 % |
| Physics and Astronomy | 76.364 | 3,21 % | 3,97 % |
| Psychology | 63.317 | 2,66 % | 2,60 % |
| Chemistry | 60.000 | 2,52 % | 2,08 % |
| Chemical Engineering | 50.059 | 2,11 % | 0,30 % |
| Immunology and Microbiology | 48.771 | 2,05 % | 1,01 % |
| Decision Sciences | 39.291 | 1,65 % | 1,03 % |
| Dentistry | 36.586 | 1,54 % | 0,44 % |
| Energy | 36.253 | 1,52 % | 0,65 % |
| Nursing | 33.850 | 1,42 % | 0,47 % |
| Pharmacology, Toxicology and Pharmaceutics | 30.841 | 1,30 % | 0,41 % |
| Economics, Econometrics and Finance | 30.000 | 1,26 % | 2,58 % |
| Veterinary | 19.573 | 0,82 % | 0,15 % |
| **Total** | **2.378.036** | **100 %** | **100 %** |

La referencia es el conjunto histórico de **71.667.731 trabajos clasificados** de 2000–2024, artículos/preprints en inglés con abstract, excluyendo retractados/paratext según el código de extracción. Los conteos NO incorporan las validaciones locales de título ≥5 palabras y abstract reconstruible ≥80 palabras. Son una aproximación al universo elegible, no cifras actuales ni una garantía de representatividad tras limpieza.

El CSV adjunto conserva también los conteos de referencia sin restricciones de tipo/idioma/abstract (194.184.528; siguen aplicándose año, clasificación conocida y exclusión de retractados/paratext). No deben confundirse con todo OpenAlex. Los conteos Field×año coinciden exactamente con la suma de sus Subfields en las 650 celdas y las cuatro variantes de filtros.

## Igual o proporcional

**Para comparar los Fields, recomiendo igual número por Field.** Así la comparación no concede casi toda la muestra a las disciplinas más grandes. No garantiza igual precisión: la heterogeneidad de cada Field también importa.

**Para un resultado que refleje el volumen de publicaciones, utilizar proporciones del universo objetivo.** Ese resultado responde a una pregunta diferente. Por ejemplo, repartir 130.000 papers proporcionalmente a la referencia filtrada daría aproximadamente 23.249 a Medicine, 21.129 a Engineering y solo 191 a Veterinary. Es una asignación poco conveniente para comparar esas tres disciplinas con detalle.

La distinción entre asignación orientada a estimaciones de grupos y asignación orientada a población se explica en [Statistics Canada](https://www150.statcan.gc.ca/n1/pub/12-001-x/2017001/article/14817/03-eng.htm). El tamaño poblacional, la variabilidad y el coste intervienen en una asignación óptima; la proporcionalidad por sí sola no la garantiza ([Penn State, muestreo estratificado](https://online.stat.psu.edu/stat506/Lesson06)). La recomendación para este proyecto es una decisión metodológica basada en su pregunta, no un resultado experimental.

## Propuesta concreta, pendiente de decidir

1. **5.000 papers por Field para el conjunto 2000–2024: 130.000 papers únicos.** Es un presupuesto candidato, no una cifra de potencia estadística demostrada.
2. **200 por año y Field**, para comparar disciplinas con la misma composición temporal. Equivale a 1.000 por Field en cada ventana de cinco años. Este diseño representa una comparación con el tiempo estandarizado; no imita el crecimiento histórico de la producción.
3. **Dentro de cada Field×año, ajustar el reparto entre Subfields a sus conteos de referencia**, seleccionando sin reemplazo entre los papers ya disponibles. Fórmula de cupo antes del redondeo: `200 × N(Subfield,año) / N(Field,año)`. La selección aleatoria uniforme entre todos los papers actuales de un Field heredaría el equilibrio artificial por Subfield del TFM. Usarlos para muestrear no cambia la unidad de estudio.
4. **Congelar los mismos IDs, textos, etiquetas y orden para todos los modelos.** Si hay fallos de procesamiento, documentar y mantener una comparación emparejada.

**Viabilidad comprobada:** todas las celdas Field×año tienen al menos 658 papers. También se comprobaron los cupos internos: con 200 por Field×año, ningún cupo proporcional continuo supera los papers disponibles del Subfield×año; el máximo uso de una celda sería aproximadamente el 43,4 %. Los dos Subfield×año sin papers también tienen conteo de referencia cero. El redondeo y la selección de IDs quedan pendientes.

**Tamaño definitivo:** evaluar después tamaños anidados de 1.000, 2.000 y 5.000 por Field, con repeticiones y criterios de precisión/estabilidad fijados antes de interpretar resultados. Si interesa comparar ventanas temporales, comprobar suficiencia por Field×ventana: 5.000 repartidos en 25 años no equivalen a 5.000 en cada período. Si no estabiliza, ampliar o revisar el alcance. Para kNN, fijar `k` y universo de candidatos; al crecer la muestra cambia el vecindario, por lo que no se exige que el valor sea idéntico para todo tamaño.

## Límites que debemos conservar en el paper

- Los conteos guardados permiten controlar aproximadamente la composición de OpenAlex. No reconstruyen exactamente la distribución de papers que pasarían la limpieza ni probabilidades individuales de inclusión: hubo sobremuestreo, descartes y backfill. No presentar los pesos como una corrección exacta de representatividad.
- Aumentar el tamaño no elimina sesgos de cobertura por idioma, texto disponible o tipos documentales. La población del estudio debe describirse con esos filtros.
- Una media de los 26 CKAs, incluso ponderada por tamaño de Field, es un **promedio de acuerdos dentro de Fields**. No equivale a CKA sobre todos los papers juntos, que incluye relaciones entre disciplinas. Esto se deduce del centrado conjunto en la [definición de CKA lineal](https://proceedings.mlr.press/v97/kornblith19a/kornblith19a.pdf). Un análisis global proporcional requiere una muestra o un cálculo ponderado definido para ese objetivo; para kNN tampoco basta con ponderar el resultado final.

## Archivos y alcance

- Tabla completa exportada: `FIELD_COUNTS.csv`, en este mismo repositorio.
- Fuentes locales, base `/Users/alejandrotreny/Workspace/Mapping-Science`: `data/processed/works_text_2000_2024_400py.parquet`, `data/interim/field_year_counts_2000_2024_400py.parquet`, `data/interim/subfield_year_counts_2000_2024_400py.parquet` y taxonomía/manifiesto existentes.
- Se hicieron agregaciones y comprobaciones en lectura. No se descargó OpenAlex, no se alteró Mapping-Science y no se calcularon nuevos embeddings ni métricas experimentales.
