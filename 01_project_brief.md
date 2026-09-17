# Project brief — *How Much of the Shape of Science Is in the Embedding?*

> Estado, 17-09-2026: documento conceptual histórico, no protocolo de análisis aprobado. Los **26 Fields**, los **500.000 trabajos: 400.000 base + 100.000 complemento**, los cinco períodos y los **diez modelos** ya están decididos; los embeddings terminaron y fueron revisados. El usuario aceptó uso habitual + control de fragmento común. Medidas y reglas científicas concretas siguen pendientes: ver `DECISIONS.md` y `ANALYSIS_PROPOSAL.md`. Las afirmaciones de medidas/variantes que aparecen debajo son propuestas, no nuevas autorizaciones.

**Objetivo.** Estudiar hasta qué punto la estructura geométrica que observamos en la literatura científica es una propiedad robusta de la propia ciencia o depende del modelo de embeddings utilizado para representarla. La pregunta central no es cuál es el “mejor” embedding, sino **cuánto coinciden distintos modelos al representar exactamente los mismos papers y qué partes de esa estructura permanecen invariantes**.

**Datos.** Utilizar OpenAlex como fuente bibliográfica. Cada paper debe conservar como mínimo `work_id`, año, título, abstract y clasificación temática. La unidad principal son los **26 Fields**, por decisión del usuario. El corpus completo contiene 252 Subfields; el subconjunto analítico temporal del TFM conservaba 241. Los Subfields pueden ayudar a organizar la selección dentro de cada Field.

**Experimento 1 — Native embedding pipelines.** Seleccionar varios modelos representativos, por ejemplo SPECTER2, SciNCL y uno o dos encoders semánticos generales. Cada modelo se utiliza con **el input para el que fue diseñado o recomendado**. Se generan embeddings para exactamente los mismos papers y se comparan directamente los espacios originales, sin UMAP/t-SNE. El análisis debe realizarse para toda la ciencia, por Field/Subfield y por diferentes ventanas temporales. La medida global primaria será **linear CKA**; como complemento local, **kNN overlap**. El muestreo será emparejado entre modelos y estratificado por tiempo/disciplina para obtener estimaciones de estabilidad e intervalos de incertidumbre.

**Experimento 2 — Controlled input.** Repetir la comparación manteniendo constante el texto de entrada. Por ejemplo: `title`, `abstract` y `title + abstract`, siempre que técnicamente sean inputs razonables para los modelos considerados. Esto permitirá separar aproximadamente dos fuentes de variación: **qué información recibe el modelo** y **cómo el encoder transforma esa información**. Se repetirá la misma matriz de comparaciones globales, disciplina por disciplina y temporalmente.

**Expansión morfológica.** Después de conocer el grado de concordancia entre embeddings, estudiar **qué estructuras concretas son robustas y cuáles desaparecen al cambiar de representación**. En lugar de seleccionar muchas métricas arbitrarias desde el principio, esta fase será secundaria y guiada por los resultados. Se pueden estudiar propiedades predefinidas como dispersión, dimensionalidad intrínseca y conectividad/fragmentación, además de localizar regiones o Subfields cuyos vecindarios permanecen estables entre modelos frente a aquellos que cambian radicalmente.

**Resultado principal esperado.** Una matriz de similitud entre representaciones para cada contexto:

\[
M_{ij}=CKA(X_i,X_j)
\]

y estudiar cómo \(M\) cambia en función de:

\[
	ext{modelo}	imes	ext{input}	imes	ext{disciplina}	imes	ext{tiempo}.
\]

La contribución científica sería determinar **qué parte de la “shape of science” es robusta al instrumento de representación y qué parte es específica del embedding**.

**Principio metodológico.** Evitar optimizar el análisis después de observar los resultados. Predefinir modelos, corpus, ventanas temporales, CKA como medida global primaria y kNN overlap como medida local. Las métricas morfológicas adicionales deben utilizarse para **explicar** los desacuerdos encontrados, no para buscar retrospectivamente una historia interesante.

**Deliverable inicial para código.** Construir primero un pipeline reproducible:

`OpenAlex → sample matching → text preparation → embeddings/model → aligned matrices → CKA + kNN overlap → bootstrap/stratified resampling → field/time comparison → plots/tables`.

Ese sería el núcleo. Yo empezaría con **2–3 Fields, 2 periodos y 3 modelos** como piloto antes de escalar a todo OpenAlex; así podemos detectar enseguida problemas de memoria, inputs, tamaños de muestra y cálculo de CKA sin gastar semanas procesando millones de papers.
