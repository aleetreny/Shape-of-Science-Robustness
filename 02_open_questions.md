# Preguntas abiertas, decisiones pendientes e ideas

> **Importante:** este documento no fija decisiones. Es una batería de cuestiones por resolver antes de cerrar el protocolo.

> Actualización, 14-09-2026: decididos los **26 Fields** y, por delegación explícita, la preparación de **500.000 trabajos: 400.000 base + 100.000 complemento, en cinco períodos de 2000–2024**. Filtros y reparto en `CORPUS_PROTOCOL.md`; registro vigente en `DECISIONS.md`. Esta lista conserva ideas de partida: las preguntas sobre tamaño, períodos y filtros ya resueltas se subordinan al protocolo. No hay que resolver todas las ideas de esta lista ni convertirlas en experimentos.

## Punto actual, 17-09-2026

Los diez modelos, sus versiones y el uso habitual + control común están elegidos; el cálculo y su revisión terminaron. La lista extensa de abajo es histórica, no una lista de tareas obligatorias. Las preguntas de extracción, versiones, reanudación y almacenamiento se resolvieron en los documentos de preparación. La selección concreta sigue siendo diez, no ocho.

El usuario delegó después las decisiones de esta fase y autorizó ejecutarla. Medidas, normalización, recetas, texto común, estabilidad, calidad y vecinos están definidos en `ANALYSIS_PROTOCOL.md`. La comparación y todos sus controles terminaron: resultados y límites en `ANALYSIS_RESULTS.md`, presentación en `PAPER_OUTLINE.md`. No queda una decisión pendiente del usuario para cerrar esta fase. El siguiente trabajo es redactar y contrastar la aportación con los antecedentes próximos; el envío y nuevas ampliaciones no están incluidos. Las opciones antiguas de `ANALYSIS_PROPOSAL.md` no son acuerdos pendientes.

**Actualización posterior del mismo día:** también terminó la checklist de entradas, tiempo, disciplinas y familias. `CHECKLIST_RESULTS.md` reúne sus seis puntos; mean está confirmada y las tres entradas usan 26.000 artículos, sin ampliación automática a 500.000. Se mantienen 31 alertas nuevas y 50 anteriores, de comprobaciones distintas. No se reabren estas decisiones al leer preguntas históricas de abajo. Quedan como trabajo futuro la redacción, el contraste bibliográfico y las comprobaciones dirigidas que una afirmación concreta pudiera necesitar.

**Cierre ampliado posterior del mismo día:** R01–R12 completos; tres entradas ahora en 52.000, comparación por especialidades y estabilidad local, controles de Medicina/familias/tiempo y literatura actualizada. Estado vigente en `ROBUSTNESS_RESULTS.md` y `NEXT_STEPS.md`. Las 31 alertas históricas se trazaron; con 100 selecciones quedan cinco en 52k, frente a 72 en 26k. No reabrir automáticamente decisiones cerradas ni convertir toda esta lista histórica en trabajo pendiente. Redactar o hacer nuevos experimentos requiere un encargo posterior.

## Pregunta científica
- ¿Cuál es exactamente el claim principal del paper?
- ¿Queremos medir similitud entre espacios completos o robustez de conclusiones científicas?
- ¿Qué significa operacionalmente “misma forma”?
- ¿Qué transformaciones deben considerarse irrelevantes: rotación, reflexión, escala, traslación?
- ¿Queremos hablar de “shape”, “representation”, “geometry” o “scientific relatedness”?
- **Resuelto:** los 26 Fields son la unidad principal; cada paper es una observación. Queda por precisar la comparación conjunta y temporal.
- ¿Cuál sería el criterio para afirmar que dos representaciones son “suficientemente similares”?
- ¿Necesitamos una hipótesis formal o un estudio principalmente descriptivo/metodológico?
- ¿Qué resultado sería científicamente interesante si todos los modelos producen espacios muy similares?
- ¿Qué resultado sería interesante si producen espacios muy distintos?

## Modelos de embedding
- ¿Qué modelos exactos se compararán?
- ¿Cuántos modelos son suficientes?
- ¿Debe haber modelos científicos y modelos generalistas?
- ¿Qué familias de entrenamiento deben estar representadas?
- ¿SPECTER o SPECTER2?
- ¿Qué adapter de SPECTER2 usar?
- ¿SciNCL debe incluirse obligatoriamente?
- ¿Qué modelo generalista usar como contraste?
- ¿Tiene sentido incluir SciBERT aunque no sea un document encoder nativo?
- ¿Qué pooling usar cuando el modelo no tiene representación documental canónica?
- ¿Normalizamos embeddings?
- ¿Usamos las revisiones exactas de Hugging Face y congelamos commits?
- ¿Cómo documentamos dimensiones distintas entre modelos?
- ¿Qué modelos tienen entrenamiento basado en citaciones?
- ¿Qué modelos comparten datos/objetivos y por tanto no son realmente independientes?
- ¿Debemos incluir modelos de distintas generaciones/años?

## Inputs
- ¿Qué significa exactamente “native input” para cada modelo?
- ¿Título + abstract es realmente el input recomendado en todos los modelos científicos elegidos?
- ¿Qué hacer con modelos que no tienen un input documental explícitamente recomendado?
- ¿Controlled input debe probar `title`, `abstract`, `title + abstract`?
- ¿Tiene sentido usar solo abstract?
- ¿Tiene sentido usar solo título en modelos entrenados con título+abstract?
- ¿Cómo interpretar un resultado obtenido con un input fuera de distribución?
- ¿Cómo truncar abstracts largos?
- ¿Debemos igualar la longitud máxima entre modelos o respetar la nativa?
- ¿Cómo medir el porcentaje de texto truncado por modelo?
- ¿Debemos usar full text en algún experimento?
- ¿Qué hacer con papers sin abstract?
- ¿Los missing abstracts introducen sesgo temporal o disciplinar?
- ¿Debemos restringirnos a inglés?
- ¿Cómo detectar el idioma?
- ¿Qué hacer con títulos multilingües o abstracts traducidos?

## OpenAlex y corpus
- ¿Qué snapshot exacto de OpenAlex usar?
- **Resuelto:** Field como categorización principal, con los 26 Fields.
- ¿Qué hacer con papers asignados a múltiples Fields?
- ¿Usar solo el primary topic/field?
- ¿Permitir que un paper aparezca en varias disciplinas?
- ¿Cómo evitar contaminación entre grupos?
- ¿Qué tipos de works incluir: articles, proceedings, reviews, preprints?
- ¿Excluir editoriales, letters, books, datasets?
- ¿Qué rango temporal usar?
- ¿Desde qué año la cobertura de abstracts es suficientemente buena?
- ¿Hasta qué año incluir para evitar datos incompletos?
- ¿Qué tamaño mínimo debe tener cada Field/Subfield?
- ¿Balancear número de papers entre disciplinas?
- ¿Usar distribución natural de papers para “all science”?
- ¿Necesitamos dos resultados globales: natural y balanced?
- ¿Cómo tratar duplicados/preprints/versiones?
- ¿Cómo tratar papers retractados?
- ¿Qué hacer con works sin referencias/citations si el modelo depende de ellas?
- ¿Cómo controlar sesgos de cobertura de OpenAlex?

## Tiempo
- ¿Qué ventanas temporales usar?
- ¿Ventanas de 1, 5, 10 años?
- ¿Periodos consecutivos o cortes históricos concretos?
- ¿Usar ventanas no solapadas?
- ¿Comparar estabilidad del agreement a lo largo del tiempo?
- ¿El tamaño de la ventana debe variar según disciplina?
- ¿Cómo controlar que la composición temática cambia dentro de un Field?
- ¿Es válido comparar años antiguos con modelos entrenados con conocimiento posterior?
- ¿Training-time leakage afecta a la interpretación histórica?
- ¿Necesitamos modelos entrenados antes de determinados años?
- ¿Queremos medir evolución real o solo representación retrospectiva?

## Muestreo
- ¿Cuántos papers por celda Field × periodo?
- ¿Cuál es el mínimo N para que CKA sea estable?
- ¿Cómo medir la convergencia de CKA con N?
- ¿Subsampling sin reemplazo o bootstrap?
- ¿Qué constituye una réplica?
- ¿Estratificar por año?
- ¿Estratificar por Subfield dentro de Field?
- ¿Estratificar por venue?
- ¿Estratificar por tipo de documento?
- ¿Cómo manejar dependencia entre papers?
- ¿Es correcto llamar a los intervalos “confidence intervals”?
- ¿Es mejor hablar de “sampling stability intervals”?
- ¿Block bootstrap por año/Subfield?
- ¿Cuántas réplicas son necesarias?
- ¿Cómo estimar Monte Carlo error?
- ¿La inferencia debe generalizar a OpenAlex o a una población conceptual de ciencia?

## Comparación global de representaciones
- ¿Linear CKA será suficiente?
- ¿Kernel CKA aporta algo distinto?
- ¿Qué kernel tendría sentido?
- ¿Qué invariancias queremos explícitamente?
- ¿CKA responde realmente a nuestra noción de “forma”?
- ¿Cómo interpretar magnitudes de CKA?
- ¿Necesitamos un null model?
- ¿Permutar correspondencias paper-paper como baseline?
- ¿Debemos comparar con embeddings aleatorios?
- ¿Debemos comparar un modelo consigo mismo bajo distintas muestras?
- ¿Cómo obtener un “noise ceiling” o máximo esperable?
- ¿Tiene sentido comparar espacios de distinta dimensionalidad directamente con CKA?
- ¿La anisotropía de los embeddings sesga CKA?
- ¿Hay que centrar/whiten los embeddings?
- ¿Whitening elimina señal real?
- ¿Procrustes debe usarse como robustness check?
- ¿RSA/distancia-matriz debe usarse?
- ¿Gromov–Wasserstein aporta algo pese a conocer la correspondencia exacta?
- ¿Qué métricas deben quedar fuera para evitar metric shopping?

## Comparación local
- ¿kNN overlap es la mejor medida local?
- ¿Qué distancia usar: cosine, angular, Euclidean?
- ¿Qué k usar?
- ¿Un único k o una curva multi-escala?
- ¿Resumir la curva con AUC?
- ¿Cómo corregir el overlap esperado por azar?
- ¿Cómo estudiar qué papers cambian más de vecinos?
- ¿Cómo estudiar qué Fields/Subfields son localmente más estables?
- ¿Cómo separar desacuerdo local de desacuerdo global?
- ¿Queremos medir rank correlation de vecinos?
- ¿Queremos medir trustworthiness/continuity entre espacios?

## Escalas de estructura
- ¿El agreement cae al pasar de Field → Subfield → Topic → paper neighborhood?
- ¿Podemos definir una “resolution of robustness”?
- ¿Cómo separar macroestructura de microestructura?
- ¿El CKA global está dominado por separación entre Fields?
- ¿Hay que calcular CKA dentro de cada Field?
- ¿Debemos residualizar/eliminar el centro de cada Field antes de comparar?
- ¿Cómo medir agreement within-field sin destruir estructura real?
- ¿Comparar centroides de Fields tiene sentido?
- ¿Comparar relaciones entre Fields tiene sentido?

## Morfología secundaria
- ¿Qué propiedades morfológicas queremos analizar, si alguna?
- ¿Cómo evitar escoger métricas retrospectivamente?
- ¿Dispersión debe ser distancia media al centro o distancia media entre pares?
- ¿Cosine spread o Euclidean spread?
- ¿Usar traza de covarianza?
- ¿Cómo afecta la normalización?
- ¿Qué significa fragmentación sin imponer clustering?
- ¿Persistent homology H0 es viable computacionalmente?
- ¿Qué resumen de persistencia usar?
- ¿Número de componentes persistentes?
- ¿Total persistence?
- ¿Entropy de persistence?
- ¿Qué estimador de dimensionalidad intrínseca usar?
- ¿TwoNN?
- ¿Levina–Bickel MLE?
- ¿Effective rank?
- ¿Qué sensibilidad tienen al tamaño de muestra?
- ¿Tiene sentido medir anisotropía?
- ¿Tiene sentido medir densidad?
- ¿Replicar densidad/asimetría de Imel & Hafen?
- ¿Qué aporta nuestra morfología que no esté ya en Imel & Hafen?
- ¿Podemos distinguir “propiedad invariante” de “misma métrica con valor parecido”?

## Regiones estables e inestables
- ¿Cómo definir una región que “se mantiene” entre embeddings?
- ¿Por neighborhood overlap?
- ¿Por correspondencia de clusters?
- ¿Por local CKA?
- ¿Por alineamiento Procrustes local?
- ¿Cómo localizar áreas que desaparecen?
- ¿Qué hacer si un cluster de un modelo se divide en dos en otro?
- ¿Qué hacer si dos clusters se fusionan?
- ¿Cómo visualizar estabilidad sin depender de UMAP?
- ¿Podemos construir un score por paper/Subfield de representational stability?
- ¿Cómo validar que una región estable es científicamente interpretable?

## Validación externa
- ¿Necesitamos ground truth?
- ¿Qué podría servir como validación externa: citations, Topics de OpenAlex, venues, expert labels?
- ¿Usar labels convertiría el proyecto en un benchmark de accuracy?
- ¿Podemos usar labels solo como interpretación, no como criterio de “verdad”?
- ¿Deberíamos comparar con citation-based similarity?
- ¿Una representación más parecida a citaciones es necesariamente mejor?
- ¿Qué significa “correcto” si distintos modelos capturan distintos tipos de relatedness?
- ¿Necesitamos un pequeño estudio cualitativo con papers concretos?

## Estadística
- ¿Reportar medias, medianas o distribuciones completas?
- ¿Qué tamaño de efecto es relevante?
- ¿Hacer tests de hipótesis o solo estimation?
- ¿Cómo manejar multiplicidad entre Fields × periodos × pares de modelos?
- ¿FDR?
- ¿Modelos jerárquicos para resumir agreement entre disciplinas?
- ¿Debemos modelar Field y periodo como efectos?
- ¿Cómo comparar matrices de CKA entre periodos?
- ¿Cómo cuantificar heterogeneidad entre Fields?
- ¿Necesitamos preregistration interno del protocolo?
- ¿Qué decisiones deben congelarse antes del run final?

## Reproducibilidad y cómputo
- ¿Cuánto almacenamiento requieren todos los embeddings?
- ¿Guardar float32, float16 o quantized?
- ¿Qué precisión afecta a CKA?
- ¿Cómo calcular CKA sin matrices NxN gigantes?
- ¿Cómo hacer kNN a escala?
- ¿FAISS exacto o aproximado?
- ¿Cuánto error introduce ANN?
- ¿CPU o GPU?
- ¿Qué hardware disponible condiciona modelos/tamaños?
- ¿Guardar embeddings completos o regenerarlos?
- ¿Qué metadata/versiones registrar?
- ¿Cómo hacer pipeline reanudable?
- ¿Cómo verificar determinismo?
- ¿Cómo versionar muestras y splits?
- ¿Cómo evitar que Codex cambie decisiones metodológicas sin registrar?

## Novelty y framing
- ¿Cuál es exactamente nuestra diferencia frente a Lamers et al.?
- ¿Cuál es exactamente nuestra diferencia frente a *The Landscape of Biomedical Research*?
- ¿Cuál es exactamente nuestra diferencia frente a Imel & Hafen?
- ¿Cuál es exactamente nuestra diferencia frente a cross-model triangulation?
- ¿Qué parte es aplicación de CKA y qué parte es contribución scientométrica?
- ¿Es suficiente una aplicación nueva de métodos existentes?
- ¿Necesitamos un nuevo índice/resumen metodológico?
- ¿Podemos aportar un benchmark público de robustness?
- ¿Publicar embeddings/muestras/código?
- ¿Qué revista/conferencia encaja mejor?
- ¿QSS, Scientometrics, Journal of Informetrics, Information Processing & Management u otra?
- ¿Qué claim de “first” puede sostenerse realmente?
- ¿Qué systematic literature search necesitamos antes de fijar el claim?

## Riesgos
- ¿Y si todos los modelos tienen CKA casi 1?
- ¿Y si todos tienen CKA muy bajo?
- ¿Y si el resultado depende totalmente de una sola familia de modelos?
- ¿Y si el Field explica casi todo el CKA global?
- ¿Y si la cobertura de abstracts hace imposible comparar periodos antiguos?
- ¿Y si los modelos generalistas no son comparables conceptualmente?
- ¿Y si el controlled-input experiment es demasiado artificial?
- ¿Y si la morfología no añade nada más allá de CKA?
- ¿Y si el paper queda como un benchmark demasiado descriptivo?
- ¿Qué análisis sería imprescindible para que la contribución sea suficientemente profunda?
