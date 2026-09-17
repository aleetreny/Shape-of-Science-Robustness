# Bibliografía y trabajos similares

## Science mapping / “same data, different results”

### Gläser, Glänzel & Scharnhorst (2017)
**Same data—different results? Towards a comparative approach to the identification of thematic structures in science.**  
*Scientometrics, 111, 981–998.*

- Antecedente conceptual central.
- Pregunta cuánto de una estructura temática procede de la ciencia y cuánto del método.
- Impide reclamar como novedad general que “el mapa depende del método”.

https://doi.org/10.1007/s11192-017-2296-z

### Boyack et al. (2011)
**Clustering More than Two Million Biomedical Publications: Comparing the Accuracies of Nine Text-Based Similarity Approaches.**  
*PLOS ONE, 6(3), e18029.*

- Mismos papers, distintas medidas de similitud, distintos resultados de clustering.
- Precedente fuerte de comparación sistemática de relatedness.

https://doi.org/10.1371/journal.pone.0018029

### Xie & Waltman (2025)
**A comparison of citation-based clustering and topic modeling for science mapping.**  
*Scientometrics.*

- Compara estructuras recuperadas por metodologías distintas.
- Evidencia de solapamiento limitado entre diferentes instrumentos de science mapping.

https://doi.org/10.1007/s11192-025-05324-z

---

## Scientific document embeddings

### Cohan et al. (2020)
**SPECTER: Document-level Representation Learning using Citation-informed Transformers.**  
*ACL 2020.*

- Document embeddings científicos informados por citaciones.
- Referencia base para SPECTER/SPECTER2.

https://aclanthology.org/2020.acl-main.207/

### Ostendorff et al. (2022)
**Neighborhood Contrastive Learning for Scientific Document Representations with Citation Embeddings.**  
*EMNLP 2022.*

- Introduce SciNCL.
- Relatedness científica aprendida mediante contrastive learning y estructura de citaciones.

https://aclanthology.org/2022.emnlp-main.802/

### Singh et al. (2023)
**SciRepEval: A Multi-Format Benchmark for Scientific Document Representations.**  
*EMNLP 2023.*

- Benchmark de representaciones científicas sobre tareas diferentes.
- Base de SPECTER2.
- Importante para justificar que una representación no es universalmente óptima.

https://aclanthology.org/2023.emnlp-main.338/

### Lamers, van Eck & Colavizza (2021)
**An appraisal of publication embedding techniques in the context of conventional bibliometric relatedness measures.**

- Compara BERT, SciBERT, SPECTER y representaciones relacionadas con citaciones/texto.
- Prior art muy cercano.
- Compara relatedness y clustering, no una matriz sistemática de representational similarity entre espacios high-dimensional.

Registro y versión de ISSI 2021: https://cris.unibo.it/handle/11585/948699

Corrección del 15-09-2026: el DOI qss_a_00168 atribuido antes a este título corresponde a otro artículo. Verificación Crossref y niveles de lectura en [ACADEMIC_MODEL_USAGE.md](ACADEMIC_MODEL_USAGE.md).

---

## Comparaciones empíricas entre varios embeddings

### *The Landscape of Biomedical Research* (2024)

- Compara múltiples encoders sobre el mismo corpus biomédico.
- Incluye BERT, SciBERT, BioBERT, PubMedBERT, SBERT/MPNet, SPECTER, SciNCL y SimCSE.
- Evalúa especialmente con kNN y visualización.
- Muy cercano experimentalmente, pero orientado a seleccionar una representación útil, no a medir directamente agreement geométrico entre espacios.

https://pmc.ncbi.nlm.nih.gov/articles/PMC11240179/

### Imel & Hafen (2025)
**Density, asymmetry and citation dynamics in scientific literature.**

- ~53k papers.
- 9 disciplinas.
- 5 representaciones.
- Estudia densidad y asimetría local bajo embeddings distintos.
- Relaciona geometría con citas.
- Prior art central para cualquier claim sobre geometría bajo múltiples embeddings.

https://arxiv.org/abs/2506.23366

### Huang et al. (2025)
**A framework for demonstrating, forecasting, and explaining topic evolution by analyzing geometrical motion of topic embeddings.**  
*Quantitative Science Studies, 6, 171–193.*

- Topic embeddings con MiniLM, MPNet y BERT.
- Estudia movimiento geométrico, predicción de centroides y decoding de topics.
- Usa varios encoders como robustness check, pero no compara directamente cuánto se parecen sus espacios.

https://doi.org/10.1162/qss_a_00344

### Cross-model triangulation en science mapping (2026)

- Existen trabajos recientes que comparan resultados obtenidos con varios encoders/modelos para evaluar estabilidad de clusters/topics.
- Importante para no reclamar como novedad “usar varios modelos para comprobar robustez”.
- Debe revisarse con detalle antes de cerrar el related work.

---

## Sensibilidad al input

### Singh & Singh (2024)
**CoSAEmb: Contrastive Section-aware Aspect Embeddings for Scientific Articles.**  
*SDP 2024.*

- Explora representaciones científicas con información textual más rica que título+abstract.
- Relevante para justificar el experimento de sensibilidad al input.

https://aclanthology.org/2024.sdp-1.27/

### SPECTER2 documentation

- Revisar input recomendado, adapters, pooling y límites.
- No asumir que todos los adapters producen “el” embedding SPECTER2.

https://github.com/allenai/SPECTER2

### SciNCL documentation

- Revisar input exacto, pooling y preprocessing recomendado.

https://github.com/malteos/scincl

---

## Representational similarity / comparación de espacios

### Kornblith et al. (2019)
**Similarity of Neural Network Representations Revisited.**  
*ICML 2019.*

- Referencia principal de CKA.
- Fundamental para definir qué invariancias tiene la medida.

https://proceedings.mlr.press/v97/kornblith19a.html

### Williams (2024)
**Equivalence between representational similarity analysis, centered kernel alignment, and canonical correlations analysis.**

- Relación matemática entre RSA, CKA y CCA.
- Importante para entender qué información realmente añade cada medida.

https://proceedings.mlr.press/v285/williams24a.html

### Heimerl et al.
**embComp: Visual Interactive Comparison of Vector Embeddings.**

- Comparación global/local de distintos espacios de embeddings.
- Literatura general relevante fuera de scientometrics.

https://pubmed.ncbi.nlm.nih.gov/33347410/

### Survey: similarity of neural network models

- Revisar survey reciente de medidas funcionales y representacionales.
- Importante porque no existe una métrica universalmente superior para todos los escenarios.

https://doi.org/10.1145/3728458

---

## Métodos potencialmente relevantes

### CKA
- Comparación global de representaciones con correspondencia entre objetos.
- Revisar invariancias, sensibilidad a anisotropía, kernel y sample size.

### RSA
- Comparación mediante matrices de similitud/distancia.
- Revisar redundancia conceptual con CKA.

### Procrustes analysis
- Alineamiento entre espacios mediante transformaciones geométricas.
- Potencial robustness check.

### Gromov–Wasserstein
- Comparación de espacios métricos.
- Especialmente útil cuando no existe correspondencia directa entre puntos; aquí esa correspondencia sí existe.

### kNN overlap / neighborhood preservation
- Comparación local.
- Revisar dependencia de `k`, baseline esperado y alternativas rank-based.

### Intrinsic dimensionality
- TwoNN.
- Levina–Bickel MLE.
- Effective rank.

### Persistent homology
- Potencial herramienta para estudiar conectividad/fragmentación sin fijar un único clustering.
- Revisar escalabilidad.

### MMD / classifier two-sample tests
- Más naturales para comparar distribuciones temporales dentro del mismo embedding space que para comparar directamente dos encoders con coordenadas distintas.

---

## Diferenciación provisional frente a trabajos previos

El proyecto NO debe venderse como:

- primera comparación de embeddings científicos;
- primera comparación de métodos de science mapping;
- primer estudio de geometría científica;
- primer robustness check con varios encoders;
- primera aplicación de CKA.

El hueco que se está investigando es más específico:

> **Comparación sistemática del agreement entre espacios de scientific-document embeddings sobre exactamente los mismos papers, estudiando cómo ese agreement cambia por disciplina, periodo e input y qué estructuras permanecen invariantes entre representaciones.**

Este claim sigue siendo provisional y debe verificarse antes de redactar el paper.

---

# Revistas objetivo y papers de referencia de estilo

## 1. Quantitative Science Studies (QSS) — objetivo principal

**Encaje:** muy alto. El paper trata directamente sobre representación, estructura y mapping de la ciencia.  
**Estrategia:** escribir el manuscrito pensando primero en QSS.

### Papers especialmente útiles como referencia

1. **Constantino, I., Kojaku, S., Fortunato, S. & Ahn, Y.-Y. (2025).**  
   *Representing the disciplinary structure of physics: A comparative evaluation of graph and text embedding methods.*  
   *Quantitative Science Studies, 6, 263–280.*  
   DOI: 10.1162/qss_a_00349  
   **Por qué leerlo:** es probablemente el paper de estilo y framing más cercano al nuestro: compara distintas representaciones de papers y pregunta qué estructura científica capturan.

2. **Huang, S. et al. (2025).**  
   *A framework for demonstrating, forecasting, and explaining topic evolution by analyzing geometrical motion of topic embeddings.*  
   *Quantitative Science Studies, 6, 171–193.*  
   DOI: 10.1162/qss_a_00344  
   **Por qué leerlo:** ejemplo reciente de geometría de embeddings + evolución científica + múltiples encoders.

3. **Boyack, K. W. & Klavans, R. (2020).**  
   *A comparison of large-scale science models based on textual, direct citation and hybrid relatedness.*  
   *Quantitative Science Studies, 1(4), 1570–1585.*  
   DOI: 10.1162/qss_a_00085  
   **Por qué leerlo:** muy útil para ver cómo QSS presenta una comparación metodológica de distintas representaciones/medidas de relatedness.

### Aspectos de estilo a observar
- Introducción centrada rápidamente en una pregunta concreta.
- Related work usado para justificar el gap, no como revisión interminable.
- Métodos reproducibles y comparaciones claras.
- Resultados cuantitativos acompañados de interpretación scientométrica.
- Claims moderados y discusión explícita de limitaciones.

---

## 2. Journal of Informetrics — segunda opción

**Encaje:** muy alto si el paper mantiene un núcleo metodológico fuerte.  
**Estrategia:** especialmente adecuado si la contribución termina siendo una comparación rigurosa de representaciones, métricas y robustez.

### Papers especialmente útiles como referencia

1. **Klavans, R. & Boyack, K. W. (2009).**  
   *Document–document similarity approaches and science mapping: Experimental comparison of five approaches.*  
   *Journal of Informetrics, 3(1), 49–63.*  
   DOI: 10.1016/j.joi.2008.11.003  
   **Por qué leerlo:** antecedente directo del tipo de diseño “mismos documentos, distintas medidas de similitud”.

2. **Xie, Q., Zhang, X., Ding, Y. & Song, M. (2020).**  
   *Monolingual and multilingual topic analysis using LDA and BERT embeddings.*  
   *Journal of Informetrics, 14(3), 101055.*  
   DOI: 10.1016/j.joi.2020.101055  
   **Por qué leerlo:** ejemplo claro de uso de embeddings modernos dentro de una pregunta informétrica.

3. **An ESTs detection research based on paper entity mapping: Combining scientific text modeling and neural prophet (2024).**  
   *Journal of Informetrics, 18(4), 101551.*  
   DOI: 10.1016/j.joi.2024.101551  
   **Por qué leerlo:** referencia reciente para ver el nivel de detalle metodológico, validación y presentación esperado en trabajos computacionales.

### Aspectos de estilo a observar
- Definición muy precisa del problema y de las métricas.
- Comparación explícita con baselines.
- Validación cuantitativa extensa.
- Menos énfasis narrativo y más énfasis en metodología/measurement.
- Importancia de demostrar por qué el método aporta algo frente a alternativas existentes.

---

## 3. Scientometrics — tercera opción / fallback fuerte

**Encaje:** excelente y probablemente la opción más segura de las tres si el paper está bien ejecutado.  
**Estrategia:** especialmente apropiada si el framing final enfatiza science mapping, robustez metodológica e implicaciones para estudios bibliométricos.

### Papers especialmente útiles como referencia

1. **Xie, Q. & Waltman, L. (2025).**  
   *A comparison of citation-based clustering and topic modeling for science mapping.*  
   *Scientometrics, 130, 2497–2522.*  
   DOI: 10.1007/s11192-025-05324-z  
   **Por qué leerlo:** posiblemente el mejor modelo de escritura para una comparación de metodologías de science mapping.

2. **Bascur, J. P., Verberne, S., van Eck, N. J. et al. (2025).**  
   *Which topics are best represented by science maps? An analysis of clustering effectiveness for citation and text similarity networks.*  
   *Scientometrics, 130, 1181–1199.*  
   DOI: 10.1007/s11192-024-05218-6  
   **Por qué leerlo:** muy próximo conceptualmente a la pregunta de qué estructuras sobreviven a distintas formas de construir un mapa científico.

3. **Aria, M., Cuccurullo, C., D’Aniello, L., Misuraca, M. et al. (2024).**  
   *Comparative science mapping: a novel conceptual structure analysis with metadata.*  
   *Scientometrics, 129, 7055–7081.*  
   DOI: 10.1007/s11192-024-05161-6  
   **Por qué leerlo:** útil para observar cómo se vende y estructura una contribución metodológica de comparative science mapping.

### Aspectos de estilo a observar
- Contextualización bibliométrica más extensa.
- Metodología explicada con bastante detalle.
- Importancia de conectar los resultados con problemas de science mapping.
- Buen lugar para análisis de sensibilidad y robustness checks amplios.
- Discussion normalmente más explícita sobre implicaciones para la práctica scientométrica.

---

## Orden provisional de envío

1. **Quantitative Science Studies**
2. **Journal of Informetrics**
3. **Scientometrics**

Este orden es provisional y puede cambiar según el resultado final, la profundidad metodológica y el framing del manuscrito.
