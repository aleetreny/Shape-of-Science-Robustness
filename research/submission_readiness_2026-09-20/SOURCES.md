# Fuentes, consultas y límites de esta revisión

Consulta dirigida: 20-09-2026. Pregunta: qué diferencia concreta sostiene el artículo frente a los trabajos próximos y cómo preparar su reproducción pública para QSS. No es una revisión sistemática ni una prueba de ausencia de trabajos equivalentes.

## Literatura y versiones

| Fuente primaria | Acceso utilizado | Uso en la revisión |
| --- | --- | --- |
| [Caspari et al., arXiv:2407.08275v1](https://arxiv.org/html/2407.08275v1) | HTML: métodos, experimentos, discusión y conclusión; metadatos actuales por API. | Antecedente de comparación conjunta de estructura, recuperación y familias. |
| [Constantino et al., arXiv:2308.15706v2](https://arxiv.org/html/2308.15706v2); [publicación QSS](https://doi.org/10.1162/qss_a_00349) | Texto de autor: pregunta, datos y métodos; versión API v2. | Comparación de representaciones y jerarquía disciplinar. |
| [González-Márquez et al., Patterns 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11240179/); [preprint](https://www.biorxiv.org/content/10.1101/2023.04.10.536208v1.full) | Página primaria indexada y métodos del preprint. PMC directo devolvió comprobación de navegador. | Reconocer la evaluación previa de modelos y recetas para construir un mapa. No se atribuyen al artículo cantidades obtenidas de actualizaciones posteriores del atlas. |
| [Bascur et al., Scientometrics 2025](https://link.springer.com/article/10.1007/s11192-024-05218-6) | Página editorial con texto: pregunta, evaluación y resultados. | Diferenciar evaluación temática y acuerdo entre representaciones. |
| [Imel y Hafen, arXiv:2506.23366v1](https://arxiv.org/html/2506.23366v1) | Datos, representaciones, resultados y discusión; versión API v1. | Geometría local de publicaciones y límites de inferencia. |
| [Raju, arXiv:2601.09173v5](https://arxiv.org/html/2601.09173v5) | Metadatos y resumen de v5, introducción y definición; v1 consultada inicialmente. | La síntesis final usa v5, de 06-07-2026. No reutiliza como vigente la formulación de v1 de correlación aproximadamente nula. |
| [Brinner y Zarrieß, ACL 2026](https://aclanthology.org/2026.acl-long.1884/) | Ficha de actas y resumen. | Delimitar su objetivo de modelos por aspectos; no prueba de ausencia de un análisis concreto en todo el artículo. |
| [Bascur, Costas y Verberne, JDIS 2026](https://doi.org/10.1515/jdis-2026-0114); [MetaROR versión 2](https://metaror.org/article/use-of-diverse-data-sources-to-control-which-topics-emerge-in-a-science-map-2/) | Texto del autor y evaluación de MetaROR. Crossref confirma título editorial y fecha 15-09-2026. La página editorial agotó el tiempo de acceso. | Actualización respecto al título del preprint de 2024. En esta revisión no se afirma haber leído completa la versión editorial. |

La búsqueda adicional por «science mapping embedding robustness», inversiones de orden y estabilidad geométrica se usó para contrastar el encuadre. Sus resultados no autorizan una afirmación de «primero en». Los trabajos históricos ya citados en el manuscrito siguen siendo pertinentes; no se han borrado ni sustituido sus registros.

## Normas y plataformas

| Fuente oficial | Fecha/estado de acceso | Evidencia utilizada |
| --- | --- | --- |
| [QSS: submission guidelines](https://direct.mit.edu/qss/pages/submission-guidelines) | 20-09: HTTP 403 directo; página oficial indexada, rastreo indicado aproximadamente 1,3 años antes. | Apartado de datos/materiales y cita de conjuntos. No se certifica vigencia completa. |
| [Zenodo: archivos](https://help.zenodo.org/docs/deposit/manage-files/) | Página oficial, rastreo de tres días. | Límites de tamaño y número de archivos. |
| [Zenodo: cuota](https://help.zenodo.org/docs/deposit/manage-quota/) | Página oficial, rastreo de tres días. | Cuota adicional; debe verificarse el saldo de la cuenta antes de preparar la carga. |
| [Zenodo: DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/) | Página oficial, rastreo de tres días. | Diferencia entre reserva y publicación. |
| [GitHub: licencias](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) | Página oficial consultada. | Necesidad de permisos explícitos de reutilización. |
| [OpenAlex: cómo se construye](https://help.openalex.org/data/how-its-built/) | Página oficial, actualizada 18-08-2026. | Declaración CC0. |
| [OpenAlex: atributos de Works](https://help.openalex.org/data/works/attributes/#abstract_inverted_index) | Página oficial consultada. La documentación antigua redirige al nuevo centro de ayuda. | Tratamiento específico de los abstracts y advertencia de formato por razones legales. |

Las copias completas de terceros permanecen en `data/submission_readiness_v1/` cuando se conservaron; no forman parte del ejemplo de reproducción. Los enlaces anteriores permiten localizar las fuentes. Los párrafos del informe son una síntesis propia, no una reproducción de las normas o artículos.

## Consultas reproducibles

API arXiv, una petición acotada:

```text
GET https://export.arxiv.org/api/query
id_list=2407.08275,2308.15706,2506.23366,2601.09173,2609.00065
max_results=5
```

Resultado: cinco registros solicitados y cinco recibidos. Analizados con `paper-lookup/scripts/arxiv_atom.py`; salida en `arxiv_metadata.json`. Versiones: Caspari v1, Constantino v2, Imel/Hafen v1, Raju v5 y Scientific Agent Skills v2. No se interpreta la ausencia de DOI editorial en arXiv como ausencia de publicación.

API Crossref:

```text
GET https://api.crossref.org/works/10.1515%2Fjdis-2026-0114
```

Respuesta directa contrastada por título, autores, revista y fecha. Copia local en `data/submission_readiness_v1/bascur_crossref.json`.

Consultas web principales, además de abrir los identificadores anteriores:

```text
site.direct.mit.edu/qss "data" "persistent" submission guidelines
Quantitative Science Studies submission guidelines reproducibility data code 2026
"Bascur" "embedding" "2025"
"SemCSE-Multi"
"science mapping" "embedding" "robustness" models
"scientific" "embedding" "rank reversals"
"Geometric Stability: The Missing Axis of Representations"
"Use of diverse data sources to control which topics emerge in a science map"
"The landscape of biomedical research" "eight" "SEP"
site:help.zenodo.org upload 50 GB 100 files reserve DOI draft review
site:help.openalex.org "CC0"
site:docs.openalex.org "abstract_inverted_index" "legal"
site:docs.github.com "without a license"
```

Solo se usaron fuentes primarias para sostener comparaciones científicas o normas. Se descartaron resultados no pertinentes y guías de otras revistas. La documentación de OpenAlex se resolvió finalmente siguiendo los enlaces del nuevo centro de ayuda, no atribuyendo vigencia a la URL antigua.

## Estado público y prueba local

`inventory.py` consulta la API de GitHub para el repositorio, el commit de `main` y el árbol recursivo de ese commit. Guarda `public_state.json` y `remote_tree.json`; no hace fetch, commit, push ni modifica el remoto. El inventario de tamaños usa el tamaño lógico de cada archivo, no el espacio físico comprimido del disco.

`build_demo.py` exporta valores guardados sin modificar los originales. `replication_demo/reproduce.py` utiliza solamente la biblioteca estándar. La prueba se ejecutó con Python 3.12.14, `-I -S`, desde una carpeta temporal que contenía exclusivamente el ZIP extraído. El programa no hace llamadas de red. La evidencia completa está en `demo_portability_audit.json`; la comprobación cubre agregación de medidas, no generación de embeddings ni geometría desde vectores.

## Herramienta de consulta

Se aplicó la guía `paper-lookup`; se comprobó la forma y el número de registros de la respuesta, así como la versión vigente de los preprints. Procedencia: Timothy Kassis, Vinayak Agarwal, Yuhuan He, Darshil Patel y Aubrey M. Brueckner (2026), [*Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*](https://arxiv.org/abs/2609.00065). Consulta confirmó v2. Esta referencia documenta la herramienta, no sustenta los resultados científicos del manuscrito.
