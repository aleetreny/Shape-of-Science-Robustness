# Plano detallado del manuscrito

**18-09-2026. Preparación solicitada por el autor; todavía no es el texto del paper.** Desarrolla [PAPER_OUTLINE.md](PAPER_OUTLINE.md) y aplica la [revisión de QSS](QSS_STRUCTURE_REVIEW.md). La guía de voz obligatoria es [AUTHOR_VOICE.md](AUTHOR_VOICE.md).

Este documento dice qué escribir, en qué orden, con qué evidencia y dónde colocar cada elemento. Los identificadores de párrafo son referencias de trabajo: no aparecerán en el manuscrito ni obligan a mantener una prosa de bloques iguales. Se podrán unir o dividir al redactar sin cambiar afirmaciones, resultados o límites.

## 1. La historia que debe entender el lector

**Representar los mismos artículos con modelos distintos puede conservar una organización amplia y, a la vez, cambiar relaciones locales y comparaciones concretas entre disciplinas.** Comprobar que una conclusión resiste cambiar artículos y comprobar que resiste cambiar representación son tareas diferentes.

Título de trabajo: **Which conclusions about science maps survive a change of embedding model?** Sigue siendo provisional. “Science maps” se define como relaciones en los espacios de representación; no evaluamos el parecido visual de proyecciones bidimensionales.

Tres preguntas, ya propuestas y ahora desarrolladas:

- **RQ1:** Which structural relationships are shared across embedding models, and how does agreement depend on the scale of comparison?
- **RQ2:** How much do text input and pooling choices change agreement relative to changing the embedding model?
- **RQ3:** Which geometric comparisons between fields persist, reverse or remain unresolved across models and article selections?

RQ3 corresponde a una ampliación exploratoria posterior. El orden de presentación no convierte el estudio en un experimento entero registrado de antemano. No se elige un ganador ni se mide una proporción de «ciencia correcta».

## 2. Índice final de trabajo y reparto

Los nombres de esta tabla son los que usaríamos en el manuscrito. El resto del documento los explica en español.

| Sección | Subapartados | Palabras orientativas del cuerpo |
| --- | --- | ---: |
| **1. Introduction** | Sin subtítulos internos | 800 |
| **2. Background and research questions** | 2.1 Representation choices in science mapping; 2.2 Agreement, stability and interpretation; 2.3 Research questions and scope | 750 |
| **3. Data and comparative design** | 3.1 Corpus and analytical panels; 3.2 Models and text representations; 3.3 Objects and measures; 3.4 Matched comparisons and stability; 3.5 Scope of robustness checks | 1.600 |
| **4. Results** | 4.1 Shared broad structure and within-field variation; 4.2 Neighbour agreement under matched comparisons; 4.3 Text input and representation choices; 4.4 Persistence and reversal of geometric field comparisons | 2.250 |
| **5. Discussion** | 5.1 What is shared and what depends on representation; 5.2 Relation to prior work; 5.3 Implications for using science maps; 5.4 Limitations and next questions | 1.150 |
| **6. Conclusion** | Un párrafo | 200 |
| **Total previsto** | Seis secciones, dos tablas, cuatro figuras principales | **6.750** |

Es un presupuesto editorial propio. No es un límite impuesto por QSS. Resumen, pies, tablas, referencias y suplemento se contabilizan aparte en esta planificación; verificar el cómputo exigido al enviar. La guía editorial consultada por índice permite estructuras diversas; su acceso directo y vigencia siguen pendientes de revalidación.

## 3. Antes del cuerpo

**Título:** conservar la pregunta hasta tener la discusión definitiva. No incluir “first”, “universal” ni “model-independent”.

**Abstract, objetivo 190 palabras:** cinco funciones, sin escribirlo todavía: problema y uso del mapa (30); comparación sobre mismos artículos, diez modelos y alcance de selecciones (45); estructura/vecinos (35); inversión de comparaciones y efecto de exigir magnitud (50); consecuencia práctica y límite de validez temática (30). No insinuar que las tres entradas se calcularon sobre 500.000. Al seleccionar cifras, mantener su denominador y explicar “reversal”.

**Keywords, propuesta de seis:** science mapping; scientific document embeddings; representation similarity; robustness; neighbourhood agreement; OpenAlex. La elección final se revisa con título/resumen; no es una nueva decisión de análisis.

## 4. Guion del cuerpo, párrafo a párrafo

### 1. Introduction — 800 palabras

**I1 · 170 palabras. El uso concreto.** Empezar por qué se hace un mapa: resumir relaciones entre publicaciones y comparar áreas. Plantear el problema de interpretar esa organización cuando depende de la herramienta que convierte textos en números. Puede entrar una analogía breve, si simplifica la explicación; no abrir con una historia general de la IA. Citas de apoyo: `refa0d2d707e6`, `refbe130e2973` y `refc0e2cc29e0`.

**I2 · 210. Lo que ya sabemos.** Exponer que cambiar clasificación, fuente o método puede alterar lo observado. Unir las comparaciones de mapas con el problema de pasar de un acuerdo agregado a una conclusión concreta. Reconocer antecedentes directos de comparación de embeddings, forma, vecinos y recetas. Citas: `QSSreviewQ03`, `QSSreviewQ09`, `QSSreviewQ12`, `ref4e1e0d5582`. No reconstruir aquí toda la bibliografía ni fingir un vacío absoluto.

**I3 · 210. Nuestro recorte del problema.** Precisar qué se mantiene: artículos identificados y comparaciones emparejadas. Qué varía: encoder, texto, receta y ámbito de comparación. Explicar por qué importa distinguir el mapa amplio, los vecinos y una afirmación entre dos áreas. Presentar el alcance —corpus de 500.000 y selecciones específicas— sin descargar detalles de extracción en la introducción.

**I4 · 210. Aportación y dirección de lectura.** Adelantar tres observaciones cualitativas: estructura amplia compartida, relaciones condicionadas por representación/entrada y comparaciones geométricas que pueden invertirse pese a persistir al cambiar artículos. Nombrar la ausencia de criterio temático externo. Cerrar conduciendo a conceptos y preguntas; como máximo una frase sobre la organización del paper. Reservar cifras y controles para resultados. No anunciar una métrica nueva.

**Elementos:** texto y citas; ninguna tabla o figura. **Voz:** partir de la utilidad, como en Localízate, y explicar el problema antes de nombrar técnicas.

### 2. Background and research questions — 750 palabras

**2.1. Representation choices in science mapping · 250 palabras.**

- **B11 · 140:** distinguir métodos de construir relaciones —texto, citas, combinaciones— y formas de agruparlas. Sintetizar Boyack/Klavans y Constantino: misma literatura no implica idéntica representación ni idéntico criterio de evaluación. Usar `QSSreviewQ09` o su entrada canónica `ref6a2f5912bc`, y `refc0e2cc29e0`; no citar ambos registros del mismo trabajo.
- **B12 · 110:** conectar con los antecedentes que comparan embeddings/recetas y perturbaciones del texto: `ref4e1e0d5582`, `refbe130e2973`, `singh-singh-2022-inefficiency`. Explicar la diferencia de pregunta y cobertura de nuestro estudio. La revisión temática [RELATED_WORK.md](references/RELATED_WORK.md) impide reducir la aportación a “comparamos muchos modelos”.

**2.2. Agreement, stability and interpretation · 280 palabras.**

- **B21 · 160:** definir tres conceptos con una frase por concepto: acuerdo entre representaciones; persistencia al cambiar artículos o decisiones; validez respecto al tema real. Explicar por qué no se sustituyen entre sí. Citas: `QSSreviewQ07`, `QSSreviewQ03`, `QSSreviewQ17`, `QSSreviewQ18`.
- **B22 · 120:** definir “forma” como objetos separados: relaciones entre centros, organización interna, vecinos y dos propiedades geométricas. Avisar de que promediar puede ocultar variación. Las propiedades no cuentan temas y una referencia aleatoria no valida su significado. Remitir al método sin introducir aún todas las fórmulas.

**2.3. Research questions and scope · 220 palabras.**

- **B31 · 130:** formular RQ1–RQ3 con sus objetos, evitando repetir el párrafo final de la introducción. Cada pregunta debe anticipar el bloque que la responde: 4.1–4.2, 4.3 y 4.4, respectivamente.
- **B32 · 90:** fijar el alcance descriptivo, los modelos seleccionados y la ampliación exploratoria posterior. No son tres hipótesis confirmatorias registradas externamente. La clasificación OpenAlex organiza el análisis, sin funcionar como verdad independiente.

**Elementos:** texto, preguntas enumeradas si facilita la lectura; ninguna figura. **Voz:** explicar una distinción por su consecuencia, sin hacer una lista de definiciones desconectadas.

### 3. Data and comparative design — 1.600 palabras

**3.1. Corpus and analytical panels · 360 palabras.**

- **M11 · 180:** OpenAlex, extracción de 15-09-2026, publicaciones 2000–2024, tipos/idioma/abstract/filtros, 26 Fields del tema principal y cinco períodos. Distinguir base de 400.000 y complemento de 100.000. La extracción conservada no es una instantánea simultánea de todo OpenAlex. Documentar idiomas/abstracts excluidos y marcas conservadas. Fuentes: [CORPUS_PROTOCOL.md](CORPUS_PROTOCOL.md), [CLEANING.md](CLEANING.md), [METHODS_ROBUSTNESS.md](METHODS_ROBUSTNESS.md).
- **M12 · 180:** presentar las selecciones de la **Tabla 1** y por qué existen. Separar 52.000 de tres entradas de otros 52.000 de fragmento común; identificar candidatos/consultas del análisis emparejado. Explicar promedios equilibrados y que no representan automáticamente proporciones mundiales. Introducir tabla y colocarla al terminar este párrafo. No sumar selecciones solapadas como artículos únicos adicionales.

**3.2. Models and text representations · 270 palabras.**

- **M21 · 140:** diez modelos elegidos por antecedentes documentados, con objetivos y dominios distintos. Presentar **Tabla 2** después del párrafo. No llamarlos muestra aleatoria, diez familias independientes ni los mejores modelos actuales. Separar los cuatro BERT de palabras de los seis ajustados para representaciones de similitud. Fuente: [MODEL_SELECTION.md](MODEL_SELECTION.md), cuyo estado histórico se completa con [POOLING.md](POOLING.md).
- **M22 · 130:** explicar entrada habitual, límites de lectura, separador, media principal y controles CLS/SEP. Mean incluye símbolos especiales y excluye relleno; SimCSE toma CLS antes de su capa de ajuste; SPECTER2 incluye adaptador. MiniLM 256 es principal y 512 sensibilidad. Normalización se aplica en el análisis; no confundir con cómo se almacenaron los vectores. Fuente exacta: [configuración](config/embeddings_v1.json) y POOLING.

**3.3. Objects and measures · 460 palabras.**

- **M31 · 230:** describir CKA lineal corregida, aplicada a vectores normalizados y luego centrados, y fracción compartida de los 25 vecinos; excluir el propio ID. Centros son medias de vectores unitarios y no una proyección 2D. Explicar qué detecta cada medida y el papel de Procrustes/RSA/k10/k50. Citas: `pmlr-v97-kornblith19a`, `refa961d84a4e`, `NEURIPS2021_252a3dba`, `pmlr-v285-williams24a`. Fórmula de vecinos y explicación verbal en cuerpo; desarrollo de la corrección de CKA en S2.1, con referencia inequívoca desde aquí.
- **M32 · 230:** definir apertura como ángulo mediano entre pares y PR como reparto de variación entre direcciones lineales de la covarianza centrada. Incluir la definición breve `PR=(sum λ)²/sum λ²`, con λ como autovalores de esa covarianza. No equiparar con diversidad temática, isotropía o dimensión intrínseca. Explicar alternativas y por qué conexión no pasó como fragmentación general. Fuentes: [METHODS_MORPHOLOGY.md](METHODS_MORPHOLOGY.md); citas `roy_2007_40328`, `rudman-etal-2022-isoscore`, `vonLuxburg2007tutorial`, precisando qué medida fundamenta cada una, sin atribuirles la definición de todas las demás.

**3.4. Matched comparisons and stability · 340 palabras.**

- **M41 · 170:** mismos IDs entre modelos, 400 por Field/período en las entradas y candidatos comparables donde se indica. En Field/Subfield: mismas 50 consultas, incluidos esos 50 artículos en ambos conjuntos de 256; diez selecciones, cuotas de fecha iguales. No confundir universo de búsqueda con número de consultas. Explicar selecciones del corpus fijo y alertas, remitiendo umbrales/cobertura a S2/S3.
- **M42 · 170:** 325 parejas de Fields, 26 condiciones por modelo, diferencia relativa simétrica `2(B−A)/(A+B)`. Persistencia exige el mismo signo en todas las condiciones; unanimidad, los diez modelos; contradicción, al menos dos testigos persistentes opuestos; resto, no resuelto. Presentar mínimos 0%, 1%, 5%, 10% como sensibilidad de magnitud, no significación. Fuente: [METHODS_FIELD_PAIRS.md](METHODS_FIELD_PAIRS.md). Conservar tolerancia numérica y desigualdades exactas en S7.1.

**3.5. Scope of robustness checks · 170 palabras.**

- **M51 · 100:** resumir tres grupos de controles según qué cambian: artículos/candidatos; representación/entrada/receta; medida/interpretación. Diferenciar repeticiones de controles puntuales y señalar que no se cruzaron todas las combinaciones. Dirigir a Tabla S3 de cobertura y cronología.
- **M52 · 70:** registro local por fases, fuentes/huellas, comprobaciones independientes y ampliaciones posteriores. Material disponible y falta de depósito permanente se declaran con su estado real. Los 45 pares comparten modelos; los rangos de selección no son intervalos poblacionales.

**Elementos:** Tabla 1 tras M12, Tabla 2 tras M21. Las fórmulas estrictamente necesarias se definen aquí; derivaciones/implementación en suplemento. **Voz:** cada elección debe ir unida a lo que permite comparar, sin narrar comandos ni incidencias del desarrollo.

### 4. Results — 2.250 palabras

Todas las cifras se extraen de la [matriz de evidencia](research/writing_blueprint_2026-09-18/claim_evidence.csv). Las referencias a R01–R12 o nombres de carpetas quedan fuera del manuscrito. Las figuras muestran resultados; el texto explica su lectura sin recitar cada punto.

**4.1. Shared broad structure and within-field variation · 450 palabras.**

- **R11 · 100:** responder primero sobre relaciones entre centros. Introducir el panel A de **Figura 1** con tamaños de grupo comparables y diferencias respecto a grupos aleatorios. No presentar su altura como probabilidad de verdad.
- **R12 · 120:** explicar el control de 26 frente a 217 centros, y qué separa del simple efecto de promediar. Citar la figura y colocarla después del párrafo. Fuente: `centroid_scales/comparisons.csv` y exportador de la figura; no inventar un único promedio para objetos distintos.
- **R13 · 140:** panel B, interior sobre los mismos 183 Subfields elegibles y 26 Fields en 128/256/512 artículos. Explicar heterogeneidad y sostener únicamente la comparación que este diseño permite. Las 50 alertas originales siguen aparte de esta vista resumida.
- **R14 · 90:** interpretar la distancia entre estructura agregada y organización interna sin inferir su causa. Puente a vecinos: un mapa parecido a gran escala deja abierta la identidad de los artículos cercanos. Este es el enlace a 4.2, no una conclusión general del estudio.

**4.2. Neighbour agreement under matched comparisons · 500 palabras.**

- **R21 · 120:** contextualizar el acuerdo de vecinos original —30,3% equilibrado por celda; 31,9% con candidatos iguales— con su diseño y límite. No atribuirlo a las consultas emparejadas de 256 ni al experimento de entrada de 52.000. Unos vecinos distintos no son vecinos incorrectos.
- **R22 · 130:** presentar **Figura 2**: mismas consultas y oportunidades comparables de búsqueda entre Field y Subfield. Baja en 127/217 y sube en 90; diferencia media de −1,35 puntos porcentuales para k25. Colocar la figura después del párrafo. Explicar qué representa un punto y la diagonal.
- **R23 · 140:** mostrar que el resultado no sostiene una caída universal: a k50 el signo casi se divide por mitad, 109 frente a 108. Añadir una mención breve del atlas con su regla de selección posterior, sin elegir un caso por ser llamativo. Si se incluye un título, tomarlo de la tabla auditada y advertir su etiqueta dudosa cuando corresponda. La evidencia exhaustiva va a S4.
- **R24 · 110:** límite central: candidatos amplios condicionados a las 50 consultas, y solo 10.850 consultas con diez selecciones controladas. La persistencia por artículo no se extiende automáticamente a todos los 500.000. Puente a 4.3: el encoder no es la única elección de representación.

**4.3. Text input and representation choices · 500 palabras.**

- **R31 · 100:** presentar la comparación de usos sobre los mismos 52.000: ambos textos como referencia, título solo y abstract solo. Introducir **Figura 3**, con media del cambio de modelo respecto a los otros nueve y cambio de entrada dentro de cada modelo.
- **R32 · 150:** cambios medios de vecinos k25: 68,76% al cambiar modelo, 70,67% con título solo y 22,12% con abstract solo. Forma: 0,3700, 0,3658 y 0,0269 en `1−CKA`. Explicar qué se cuenta como cambio y que las dos escalas no se mezclan. Colocar Figura 3 tras este párrafo. Medias próximas no demuestran equivalencia.
- **R33 · 150:** variación por área/modelo y cambio del orden con receta/medida. Mantener mean como principal sin reoptimizarla; CLS/SEP, texto común y MiniLM512 permiten acotar interpretaciones. No atribuir todo al contenido puro: hay recorte y entrenamiento diferentes.
- **R34 · 100:** ampliación 26k→52k: con 100 selecciones, 72/520→5/520 alertas de entrada. Es una comprobación de la comparación principal de forma, no garantía universal de vecinos/recetas ni precisión poblacional. Dirigir a S3 para historia de 20 repeticiones y las 31 alertas originales. Puente a la consecuencia concreta: cambiar de representación puede cambiar una comparación entre áreas.

**4.4. Persistence and reversal of geometric field comparisons · 800 palabras.**

- **R41 · 130:** identificar esta ampliación como exploratoria; explicar la pregunta “¿A presenta mayor apertura o PR que B?”. Distinguir persistencia al cambiar artículos del acuerdo entre modelos. Usar, si hace falta, Artes/Medicina como ilustración elegida tras los resultados, junto al examen de todas las parejas.
- **R42 · 140:** presentar **Figura 4** y las tres clases completas. Apertura: 42 unanimidades, 262 contradicciones, 21 no resueltas; PR: 54, 221 y 50. Siempre 325 parejas por propiedad. Dos modelos opuestos bastan: no afirmar oposición de los diez. Colocar figura después del párrafo.
- **R43 · 140:** preguntar cuánto cambia la lectura al exigir magnitud. A 5% quedan 96 y 177 contradicciones; a 10%, 19 y 126. Mostrar también 1% en figura/suplemento. Dar visibilidad a lo no resuelto y explicar por qué pequeñas diferencias explican una parte del recuento de apertura.
- **R44 · 140:** alternativas y panel de modelos. Los mismos testigos conservan dirección bajo alternativas en 225 aperturas y 196 PR; cobertura angular de 26 condiciones, espectral de tres. Seis modelos de similitud: 231 y 160 sin mínimo. No atribuir el descenso al entrenamiento: hay menos oportunidades de oposición. Referencias S7.2–S7.3.
- **R45 · 170:** el control que cambia la interpretación debe estar en el cuerpo: centrar globalmente conserva los mismos testigos en 145/262 aperturas y 218/221 PR. Los controles son puntuales; no heredan 25 repeticiones propias. Conservar cuatro alertas de PR y declarar que conexión no se validó como fragmentación. Otros controles a S6/S7, sin vender una propiedad independiente de receta/procesamiento.
- **R46 · 80:** respuesta acotada a RQ3: hay comparaciones persistentes dentro de un modelo que no se trasladan entre modelos. No concluir que una disciplina contiene más temas ni que los mapas carecen de utilidad. Cerrar la evidencia y dejar consecuencias generales para discusión.

### 5. Discussion — 1.150 palabras

**5.1. What is shared and what depends on representation · 250 palabras.**

- **D11 · 140:** integrar las tres preguntas sin repetir las tablas de números. Una organización amplia compartida y diferencias locales pueden coexistir; los cambios de entrada y receta delimitan la lectura de las diferencias entre modelos.
- **D12 · 110:** explicar el resultado más específico: estabilidad frente a selección no garantiza una conclusión común entre representaciones. No confundir estabilidad numérica con independencia del método o significado temático. Mantener la dependencia del centrado al hablar de apertura.

**5.2. Relation to prior work · 280 palabras.**

- **D21 · 150:** comparar directamente con `ref4e1e0d5582` —forma/recuperación/familias—, `refbe130e2973` —representaciones y recetas— y `refc0e2cc29e0` —comparación con clasificación externa en Física—. Decir qué pregunta y controles añade nuestro diseño y qué ya existía. No hacer una lista de citas decorativa ni afirmar una primera demostración.
- **D22 · 130:** volver a `QSSreviewQ03`, `QSSreviewQ09`, `QSSreviewQ12`, `QSSreviewQ17`/`QSSreviewQ18`: acuerdo agregado, resultados particulares y dependencia de clasificación. Vincular propiedades geométricas con `ref6da178065c` como antecedente, sin confundir usos de densidad con nuestras medidas. Definir el hueco como alcance y conclusión comprobada.

**5.3. Implications for using science maps · 220 palabras.**

- **D31 · 130:** recomendación proporcional a lo observado: documentar encoder/entrada/receta, comparar oportunidades de búsqueda y someter la conclusión de interés a alternativas justificadas. Una diferencia de método importa por la interpretación que cambia, además de por una puntuación global.
- **D32 · 90:** aplicación práctica acotada: al afirmar que dos áreas difieren, informar signo, magnitud y persistencia. No recomendar un encoder ganador por consenso ni trasladar el resultado a políticas de financiación que no se evaluaron. La selección de controles depende del uso, no de intentar probarlo todo siempre.

**5.4. Limitations and next questions · 400 palabras.**

- **D41 · 150:** alcance de datos/modelos: inglés, abstract, períodos, tipos, complemento y clasificación OpenAlex; errores de etiquetas/avisos comprobados. Revisar títulos genéricos no estima la prevalencia del error temático. No sabemos todo el solapamiento con el entrenamiento ni representamos todos los modelos actuales.
- **D42 · 160:** alcance de comparación: pares/selecciones dependientes, controles puntuales y combinaciones no cruzadas; sensibilidad a recetas/centrado; ampliación exploratoria; alternativas que comparten fundamentos; ausencia de validación temática. Tiempo, Medicina y familias aportan asociaciones con límites y están en S5. Mencionar que el signo temporal de vecinos cambia con candidatos para impedir una lectura de convergencia histórica causal.
- **D43 · 90:** siguiente pregunta posible: validación temática externa y dirigida a afirmaciones concretas, con expertos o referencias adecuadas al uso. Presentarla como trabajo futuro, no como control ya resuelto ni tarea automáticamente autorizada. Evitar un catálogo de experimentos nuevos que diluya el cierre.

**Elementos:** texto y referencias; remisiones a suplemento. No introducir resultados inéditos aquí. **Voz:** tomar posición a partir de lo comprobado y explicar el límite concreto, como haces al contar por qué una herramienta dejó de servir para otro uso.

### 6. Conclusion — 200 palabras

**C1 · 200:** responder la pregunta central en un párrafo: qué se conserva, qué comparaciones dependen de la representación y por qué probar artículos distintos no basta para resolverlo. Una consecuencia práctica y el límite de validez temática. Sin nuevas cifras, referencias nuevas ni repetición del resumen entero. Evitar proclamar una revolución metodológica. Se redactará al final; si repite discusión, acortarlo en vez de rellenar el presupuesto.

## 5. Tablas principales: contenido y ubicación exactos

### Table 1. Corpus and analytical panels

**Después de M12, en 3.1.** Columnas: panel; artículos/grupos; textos y modelos; unidad de comparación; alcance. [Contenido estructurado preparado](research/writing_blueprint_2026-09-18/table1_panels.csv).

| Fila | Información que debe quedar visible |
| --- | --- |
| Corpus y análisis originales | 500.000 IDs, 400.000 base + 100.000 complemento; diez modelos, título+abstract; 26 Fields × cinco períodos. Base general exclusiva para el resumen global y candidatos globales. |
| Tres entradas | 52.000 IDs; 400 por Field/período, 2.000 por Field; título, abstract y ambos; diez modelos. Incluye los 26.000 del piloto. |
| Fragmento común | Otra selección de 52.000; comparación emparejada habitual/común. Mismos caracteres de contenido, diferentes tokenizadores y separadores habituales. |
| Centros e interior a tamaño comparable | Centros de 256 artículos; 26 Fields/217 Subfields/control de 26 centros. Interior: 26 Fields y los mismos 183 Subfields a 128/256/512. |
| Vecinos Field/Subfield | 217 Subfields × 50 consultas = 10.850; diez selecciones de 256 candidatos por ámbito. Los 50 artículos de consulta están en ambos ámbitos, antes de excluir el propio al buscar. |
| Geometría y parejas | 2.000 por Field, 20 medias muestras de 1.000 y cinco selecciones de 2.000 del corpus; 325 parejas × dos propiedades. Cobertura distinta de alternativas/controles. |

**Pie necesario:** filas solapadas, no sumar como corpus distintos; períodos 2000–04, 2005–09, 2010–14, 2015–19, 2020–24; mismos IDs entre modelos en cada comparación. Los 1.300 técnicos no son una muestra científica adicional. Detalles de cuotas/filtros a S1.

### Table 2. Embedding models and primary representation settings

**Después de M21, en 3.2.** Diez filas; columnas: nombre e identificador exacto, dimensión, límite habitual de tokens, receta principal y referencia. [Filas verificadas contra configuración](research/writing_blueprint_2026-09-18/table2_models.csv). Revisiones completas y separadores se conservan ahí y en Tabla S2, para que la tabla principal sea legible.

| Modelo | Dimensión | Límite | Principal |
| --- | ---: | ---: | --- |
| SPECTER | 768 | 512 | CLS |
| SPECTER2 | 768 | 512 | CLS + adaptador de proximidad |
| SciNCL | 768 | 512 | CLS |
| SciBERT | 768 | 512 | Mean |
| BERT | 768 | 512 | Mean |
| MPNet (`all-mpnet-base-v2`) | 768 | 384 | Mean |
| MiniLM (`all-MiniLM-L6-v2`) | 384 | 256 | Mean |
| PubMedBERT/BiomedBERT (`abstract-fulltext`) | 768 | 512 | Mean |
| BioBERT (`v1.1`) | 768 | 512 | Mean |
| SimCSE (`unsup-simcse-bert-base-uncased`) | 768 | 512 | CLS antes del pooler |

**Pie necesario:** tokens incluyen símbolos especiales y no equivalen a palabras; límites nativos diferentes; mean exacta de POOLING; diez modelos, no 18 independientes. Para MPNet/MiniLM distinguir la referencia a Sentence-BERT del checkpoint concreto documentado por su ficha. No atribuir el entrenamiento exacto del checkpoint al artículo de la arquitectura base.

## 6. Figuras principales: orden de lectura y pies

Las cuatro bases visuales ya existen. Esta fase fija su función y posición, sin cambiar ni recalcular medidas. [Registro de elementos](research/writing_blueprint_2026-09-18/display_items.csv) con fuente y estado. Al maquetar habrá que aplicar numeración final, rótulos ingleses coherentes y pies completos; la figura de parejas aún usa rótulos españoles.

| Número/título propuesto | Posición | Base y lectura |
| --- | --- | --- |
| **Figure 1. Agreement between group centres and within groups** | Tras R12 | [02_scales.pdf](reports/robustness_v2/final/figures/02_scales.pdf). A: centros reales/repartos aleatorios, mismo tamaño y control de número de centros. B: organización interna en grupos elegibles fijos a tres tamaños. |
| **Figure 2. Neighbour agreement in matched Field and Subfield searches** | Tras R22 | [03_paired_neighbors.pdf](reports/robustness_v2/final/figures/03_paired_neighbors.pdf). Diagonal de igualdad; cada punto es una especialidad; Medicina diferenciada visualmente, sin convertirlo en prueba causal. |
| **Figure 3. Changes associated with the encoder and text input** | Tras R32 | [01_input_effect.pdf](reports/robustness_v2/final/figures/01_input_effect.pdf). A: `1−CKA` corregida. B: fracción de vecinos k25 cambiados. Tres condiciones claramente rotuladas. |
| **Figure 4. Persistence, reversal and magnitude of field comparisons** | Tras R42 | [01_conclusions_and_magnitude.pdf](reports/field_pair_summary_v1/01_conclusions_and_magnitude.pdf). Dos propiedades; acuerdo de diez, contradicción persistente y no resuelto; cuatro mínimos relativos. |

**Especificación del pie 1:** 256 artículos por centro; 26/217/26 centros; repartos conservan tamaño y fechas; panel interior con mismos 183 Subfields y 26 Fields, receta principal. Definir corrección de CKA por referencia a método. Los paneles comparan objetos distintos y no se restan como efectos causales. Fuente adicional de centros local: `data/robustness_v2/centroid_scales/comparisons.csv`.

**Pie 2:** 217 Subfields, 50 consultas fijas, 256 candidatos incluyendo las consultas, diez selecciones y fechas emparejadas. Media de pares/selecciones según método, propio ID excluido, k25. Detallar el condicionamiento del Field. Aclarar que dispersión de puntos es heterogeneidad entre grupos.

**Pie 3:** 52.000 IDs del experimento de entradas, 2.000 candidatos por Field; cambio de modelo desde ambos textos frente a cambio de entrada dentro de modelo. Cada punto es una media de Field; cajas y puntos no son intervalos de confianza. Mantener efectos de uso habitual y recortes. Ninguno de sus ejes es precisión temática.

**Pie 4:** 325 parejas por propiedad; diez modelos; 26 condiciones. Definición de los testigos opuestos, casos no resueltos y diferencia simétrica. Umbrales de magnitud operativos, sin significación. Seguimiento exploratorio; condiciones solapadas y controles de centrado/receta no incluidos como 25 repeticiones adicionales. No ocultar resultados a 0% cuando se comenta 5%.

Ninguna figura principal será un mapa 2D vistoso sin papel en la comparación. El atlas y el mapa de las 325 parejas quedan disponibles en el suplemento, donde se pueden leer sin sobrecargar el argumento principal.

## 7. Suplemento: índice, tablas y figuras reservadas

Numeración propuesta para preparar el archivo suplementario. **“Tabla” puede agrupar un resumen legible y un CSV completo** con el mismo identificador; no volcar miles de filas dentro de un PDF. Esta numeración no significa que el suplemento final ya esté maquetado.

| Sección suplementaria y subapartados | Tablas/figuras previstas | Fuente existente |
| --- | --- | --- |
| **S1. Corpus, models and provenance**. S1.1 elegibilidad/reparto; S1.2 extracción/limpieza; S1.3 versiones y recortes | Tabla S1: conteos Field×período, base/complemento, filtros. Tabla S2: checkpoints, huellas, formato/receta/límites y recortes. | [CORPUS_PROTOCOL](CORPUS_PROTOCOL.md), [CLEANING](CLEANING.md), [EMBEDDINGS_AUDIT](EMBEDDINGS_AUDIT.md), configuración y catálogos. |
| **S2. Agreement measures and sampling stability**. S2.1 definiciones/validación; S2.2 tamaños/permutaciones; S2.3 alertas y cronología | Tabla S3: cobertura y orden de controles. Tabla S4: alternativas de acuerdo, alertas originales y amplitudes. | [METHODS_ANALYSIS](METHODS_ANALYSIS.md), [METRICS](METRICS.md), [SAMPLING_STABILITY](SAMPLING_STABILITY.md), `controls_*` de robustez. |
| **S3. Text input, pooling and truncation**. S3.1 tres entradas; S3.2 mean/CLS/SEP; S3.3 común/MiniLM512; S3.4 26k→52k | Tabla S5: efectos por modelo/Field/receta. Tabla S6: alertas y transición con 20/100 selecciones. Figura S1: transición de alertas. | Tablas `input_*`; [07_input_alerts.pdf](reports/robustness_v2/final/figures/07_input_alerts.pdf), POOLING. |
| **S4. Scale, neighbourhoods and cases**. S4.1 candidatos/k; S4.2 centros/controles; S4.3 atlas y elegibilidad; S4.4 errores de fuente | Tabla S7: tamaño/granularidad/k. Tabla S8: ejemplos, IDs, relación y reglas de elección. Figuras S2–S3: atlas publicado de persistencia y relaciones. | [CASE_ATLAS](CASE_ATLAS.md), `reports/prepaper_v1/`; `structure_*` de robustez. |
| **S5. Time, disciplinary composition and model families**. S5.1 candidatos y fechas; S5.2 Medicina; S5.3 rasgos de entrenamiento/receta | Tabla S9: tiempo, mismas consultas/candidatos. Tabla S10: composición/contrastes. Tabla S11: rasgos, ajuste/omisiones e identificabilidad. Figuras S4–S6: tiempo, composición y familias. | [04_time_controls.pdf](reports/robustness_v2/final/figures/04_time_controls.pdf), [05_medicine_composition.pdf](reports/robustness_v2/final/figures/05_medicine_composition.pdf), [06_recipe_families.pdf](reports/robustness_v2/final/figures/06_recipe_families.pdf). |
| **S6. Geometric properties and construct checks**. S6.1 apertura/PR; S6.2 tamaño/alternativas; S6.3 receta/centrado; S6.4 conexión y contraejemplos | Tabla S12: propiedades/alternativas/estabilidad, incluidas cuatro alertas PR. Tabla S13: simulaciones, tamaño/regla de vecinos, referencias gaussianas y 51 alertas de conexión. Figuras S7–S9: tamaño, controles y contraejemplos. | [METHODS_MORPHOLOGY](METHODS_MORPHOLOGY.md), `reports/morphology_pilot_v1/`; figuras 03, 05 y 04, respectivamente. |
| **S7. All pairwise field comparisons**. S7.1 reglas/magnitudes; S7.2 alternativas/testigos; S7.3 paneles/omisiones; S7.4 controles puntuales | Tabla S14: 325 parejas × propiedad y mínimos. Tabla S15: mismos testigos, seis modelos y retirar uno. Tabla S16: controles y referencias emparejadas. Figura S10: todas las parejas. | [METHODS_FIELD_PAIRS](METHODS_FIELD_PAIRS.md), doce CSV y [02_all_field_pairs.pdf](reports/field_pair_summary_v1/02_all_field_pairs.pdf). |
| **S8. Reproducibility and access**. S8.1 manifiestos/entornos; S8.2 auditorías; S8.3 disponibilidad y restricciones reales | Tabla S17: objeto, versión, huella, comando, acceso/depósito real. | [REPRODUCING](docs/REPRODUCING.md), [DATA_CATALOG](DATA_CATALOG.md), [DATA_RELEASE](docs/DATA_RELEASE.md), cierres de cada fase. |

S6 debe conservar el resultado negativo de conexión y sus contraejemplos. S5 no presenta explicación causal de Medicina/familias ni convergencia histórica. S7 distingue las 26 condiciones angulares de las tres de alternativas espectrales. S4 conserva los casos con etiquetas dudosas, sin corregirlos a mano.

## 8. Citas y trazabilidad al redactar

Las claves `ref…` y claves nominales están en [references.bib](references/references.bib); `QSSreviewQ…`, en [la colección QSS](research/qss_structure_2026-09-18/qss_review.bib). Algunas entradas son el mismo trabajo: deduplicar por DOI antes de armar la bibliografía del manuscrito. No citar los 34 antecedentes solo porque se leyeron.

Las citas indicadas en cada párrafo son candidatas con una función concreta. Al redactarlo, volver al pasaje pertinente y comprobar que sostiene la frase final. Una matriz de lectura no autoriza extender la conclusión de un estudio a otros corpus. Mantener condición de preprint cuando corresponda. La investigación sobre voz de IA va en documentación editorial, no como bibliografía científica añadida por defecto.

Reglas de cifras: conservar denominador, unidad, panel y receta; usar puntos porcentuales para diferencias de proporciones; CKA no se expresa como porcentaje correcto; rangos de selección no se llaman intervalos poblacionales. Redondear desde la tabla original y nunca desde otra frase del manuscrito. No introducir cifras que solo consten en un borrador histórico.

## 9. Cierre editorial y punto de continuación

Después de la conclusión: referencias y declaraciones reales de contribuciones, financiación, intereses, disponibilidad y uso de herramientas según la guía vigente. Autoría, afiliaciones, licencia y depósito todavía no se rellenan por suposición. Código publicado previamente no equivale a datos públicos ni a las ampliaciones posteriores ya subidas.

Cuando el usuario pida escribir: **métodos → resultados → discusión → introducción/antecedentes → conclusión/resumen/título**. El orden de redacción facilita comprobar afirmaciones; el de lectura seguirá el índice anterior. Usar un primer bloque para contrastar la adaptación inglesa con la voz del autor, sin reabrir decisiones científicas ya cerradas.

Este plano deja preparado qué escribir y con qué material. No necesita nuevos análisis para comenzar. La aceptación final de redacción, ajustes de título/voz y declaraciones corresponde al autor; no iniciar manuscrito, cálculos, depósito, commit/push o envío por extensión de esta tarea.
