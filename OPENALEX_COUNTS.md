# Cuántos trabajos hay disponibles en OpenAlex

Consulta real de la API: **14 de septiembre de 2026**. Son candidatos antes de la limpieza final, no promesas de textos utilizables. No se descargó un corpus nuevo.

> Recuentos de las alternativas iniciales. El filtro fijado después por delegación está en `CORPUS_PROTOCOL.md`: artículos, revisiones y congresos, excluyendo preprints; **67.202.824 candidatos** clasificados antes de limpiar. Su evidencia está en `research/feasibility_2026-09-14/`. No sustituir las etiquetas de las tablas históricas por las del filtro nuevo.

OpenAlex ofrece un **catálogo principal**, usado por defecto en la API, y una **ampliación opcional**, con muchos registros de repositorios y datasets. Los primeros recuentos y las 650 celdas anuales corresponden al principal. También se consultó la ampliación para no presentarlos como el límite absoluto de OpenAlex. [Explicación oficial](https://help.openalex.org/api/).

## Totales

| Conjunto | Trabajos |
| --- | ---: |
| Catálogo principal, cualquier año y tipo | 326.269.690 |
| 2000–2024, excluyendo retractados y material auxiliar, antes de filtrar tipo, idioma o abstract | 201.706.981 |
| 2000–2024, artículos o preprints, inglés, con abstract, mismas exclusiones | 61.079.645 |
| De los anteriores, con uno de los 26 Fields | **61.061.439** |
| De los anteriores, sin Field | 18.206 |
| Añadiendo también trabajos de congresos a los filtros básicos | 70.101.796 |
| De los anteriores, con uno de los 26 Fields | **70.050.675** |

Si se incluye también el catálogo ampliado (`corpus=all`):

| Conjunto ampliado | Trabajos |
| --- | ---: |
| Cualquier año y tipo | **474.716.562** |
| Filtros básicos 2000–2024, artículos/preprints | 73.209.685 |
| De los anteriores, con Field | **73.176.918** |
| Mismos filtros, añadiendo congresos | 82.879.747 |
| De los anteriores, con Field | **82.760.353** |

La ampliación no se ha auditado para el proyecto ni se ha decidido incluirla. Las tablas CSV por Field contienen ambas variantes; el desglose por año usa solo el catálogo principal. La tabla siguiente también usa el principal.

OpenAlex distingue `conference-paper` de `article`. Incluir congresos aumentaría especialmente los candidatos de Informática (3.793.873 → 5.995.907) e Ingeniería (7.826.953 → 11.303.314). Su inclusión es una propuesta pendiente.

## Las 26 áreas

La columna básica usa artículos/preprints; la última añade congresos. El corpus local ya pasó filtros de texto adicionales. Por eso no se deben interpretar sus diferencias como trabajos que basta con descargar y añadir.

| Field | Papers locales | Candidatos básicos | Con congresos |
| --- | ---: | ---: | ---: |
| Medicine | 403.376 | 12.606.989 | 12.941.032 |
| Engineering | 157.673 | 7.826.953 | 11.303.314 |
| Social Sciences | 207.257 | 6.536.372 | 6.962.688 |
| Biochemistry, Genetics and Molecular Biology | 135.852 | 3.929.536 | 4.059.893 |
| Computer Science | 109.980 | 3.793.873 | 5.995.907 |
| Agricultural and Biological Sciences | 104.207 | 3.020.886 | 3.197.049 |
| Environmental Science | 109.936 | 2.857.778 | 3.143.868 |
| Physics and Astronomy | 76.364 | 2.321.455 | 2.801.986 |
| Materials Science | 78.777 | 2.061.799 | 2.319.319 |
| Arts and Humanities | 123.705 | 1.971.559 | 2.066.441 |
| Business, Management and Accounting | 79.204 | 1.801.412 | 1.998.160 |
| Psychology | 63.317 | 1.698.032 | 1.830.262 |
| Economics, Econometrics and Finance | 30.000 | 1.694.229 | 1.772.641 |
| Chemistry | 60.000 | 1.403.627 | 1.461.215 |
| Health Professions | 99.687 | 1.346.742 | 1.417.312 |
| Mathematics | 88.331 | 1.149.293 | 1.209.573 |
| Neuroscience | 78.137 | 1.070.311 | 1.160.555 |
| Earth and Planetary Sciences | 77.009 | 1.063.089 | 1.237.283 |
| Immunology and Microbiology | 48.771 | 716.535 | 724.719 |
| Decision Sciences | 39.291 | 575.342 | 704.995 |
| Energy | 36.253 | 386.024 | 456.233 |
| Nursing | 33.850 | 336.042 | 344.938 |
| Dentistry | 36.586 | 320.927 | 326.075 |
| Pharmacology, Toxicology and Pharmaceutics | 30.841 | 292.046 | 297.057 |
| Chemical Engineering | 50.059 | 178.786 | 212.670 |
| Veterinary | 19.573 | 101.802 | 105.490 |

## Años y límites

- Se verificaron **650 recuentos: 26 Fields × 25 años**. Cada suma anual coincide con su Field, y todos suman 61.061.439. No se han asignado cupos ni elegido IDs.
- Veterinaria tiene 101.802 candidatos: desde 1.827 en 2000 hasta un máximo de 6.494 en 2023. Su número local, 19.573, no es un límite de OpenAlex.
- Fuera del período anterior, los mismos filtros básicos devuelven 4.026.794 en 2025 y 2.461.082 en 2026, incluidos trabajos sin Field. El año 2026 está incompleto. El período definitivo no está decidido.
- Tener abstract en la API no garantiza que podamos reconstruirlo ni que cumpla la longitud y calidad exigidas. Faltan esas comprobaciones y la resolución de versiones duplicadas.
- Los 71.667.731 de la referencia histórica del TFM y los recuentos actuales proceden de consultas de fechas distintas. No se ha establecido la causa de la diferencia; no concluir que OpenAlex perdió esos trabajos. Mantener ambas referencias identificadas por separado.
- Estos filtros describen una parte de la literatura indexada, no toda la ciencia mundial.

## Cómo reproducir y localizar los datos

Se consultó `GET https://api.openalex.org/works`, agrupando por `primary_topic.field.id` o `publication_year`. Filtro básico exacto:

```text
publication_year:2000-2024,type:article|preprint,language:en,has_abstract:true,is_retracted:false,is_paratext:false
```

Para cada Field se añadió `primary_topic.field.id:<ID>`. Para la variante con congresos se usó `type:article|preprint|conference-paper`. Se contó cada trabajo por el Field de su tema principal, sin sumarlo en varias áreas.

Respuestas originales, parámetros y hora de consulta: [carpeta de evidencia](research/openalex_counts_2026-09-14/). Se guardaron 37 respuestas de recuentos, todas correctas, con comprobaciones adicionales de las sumas. La clave existente funcionó y no se guardó en estos archivos. Consultar la [referencia oficial de la API](https://help.openalex.org/api) para futuros cambios de sintaxis.

- [Tabla por Field](research/openalex_counts_2026-09-14/OPENALEX_FIELD_COUNTS.csv).
- [Tabla por Field y año](research/openalex_counts_2026-09-14/OPENALEX_FIELD_YEAR_COUNTS.csv).
- [Recuentos locales e históricos](FIELD_COUNTS.csv), conservados sin sustituirlos por datos actuales.
