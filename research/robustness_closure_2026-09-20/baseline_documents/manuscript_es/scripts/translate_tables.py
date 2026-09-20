"""Translate display text only; source values and English originals stay intact."""
from pathlib import Path
import re, json, hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'manuscript_es'
PAIRS=r'''
Corpus and analytical panels.|||Corpus y muestras de análisis.
Embedding models and primary representation settings.|||Modelos de embeddings y reglas principales de representación.
Clean corpus by Field, period and cohort.|||Corpus limpio por área, período y muestra.
Frozen checkpoints, text formats and native truncation.|||Versiones fijas, formatos de texto y recorte habitual.
Coverage and chronology of the comparison blocks.|||Cobertura y cronología de los bloques de comparación.
Agreement of alternative measures and retained stability alerts.|||Acuerdo de medidas alternativas y alertas de estabilidad conservadas.
Input changes by model, averaged equally over the 26 Fields.|||Cambios de entrada por modelo, con el mismo peso para las 26 áreas.
Input-alert transitions for the nested 26k and 52k panels.|||Transición de alertas de entrada entre las muestras anidadas de 26,000 y 52,000.
Matched Field/Subfield neighbour searches.|||Búsquedas emparejadas de vecinos en áreas y especialidades.
All twelve rule-selected article examples, including source caveats.|||Los doce artículos seleccionados por la regla, con sus advertencias de fuente.
Temporal endpoint changes and Field heterogeneity.|||Cambios entre períodos extremos y diferencias entre áreas.
Discipline agreement with observed and balanced Subfield composition.|||Acuerdo por disciplina con composición observada y equilibrada de especialidades.
Descriptive model-trait fits and identifiability.|||Ajustes descriptivos de características de modelos e identificabilidad.
Selection stability of the geometric properties.|||Estabilidad de las propiedades geométricas ante la selección.
Construct checks on all nine saved synthetic clouds.|||Comprobación del significado de las medidas en las nueve nubes sintéticas.
All Field-pair conclusions under four minimum relative differences.|||Conclusiones de todas las parejas con cuatro diferencias relativas mínimas.
Persistent opposition and identical witnesses across alternatives and model panels.|||Oposición persistente de los mismos modelos con medidas y conjuntos alternativos.
Point controls: retention of the original opposing models.|||Controles puntuales: conservación de los modelos opuestos originales.
Versions and access status of the source objects.|||Versiones y situación de acceso de los materiales de origen.
Articles and representation|||Artículos y representación
Comparison and scope|||Comparación y alcance
Original corpus|||Corpus original
Three text inputs|||Tres entradas de texto
Common fragment|||Fragmento común
Matched group size|||Grupos de igual tamaño
Paired searches|||Búsquedas emparejadas
Geometry / Field pairs|||Geometría / parejas de áreas
500,000 IDs: 400,000 base + 100,000 supplement. Ten models; title + abstract.|||500,000 identificadores: 400,000 base + 100,000 de refuerzo. Diez modelos; título y resumen.
26 Fields, five periods. Global summaries use the base; the full corpus is not population-proportional.|||26 áreas, cinco períodos. Los resúmenes globales usan la base; el corpus completo no es proporcional a la población.
52,000 IDs; 400 per Field-period, 2,000 per Field. Title, abstract and both.|||52,000 identificadores; 400 por área y período, 2,000 por área. Título, resumen y ambos.
Same articles and candidates between models. Includes the 26,000-article pilot.|||Mismos artículos y candidatos entre modelos. Incluye el piloto de 26,000 artículos.
A different 52,000-ID panel; 400 per Field-period.|||Otra muestra distinta de 52,000 identificadores; 400 por área y período.
Paired native/shared content; model-specific tokenization. Distinct from the three-input panel.|||Contenido habitual y común emparejado; tokenización propia de cada modelo. Distinta de la muestra de tres entradas.
256 articles per centre; 26 Fields, 217 Subfields, or 26 Subfield centres.|||256 artículos por centro; 26 áreas, 217 especialidades o 26 centros de especialidades.
Within groups: 26 Fields and the same 183 Subfields at 128, 256 and 512 articles. Different objects from centres.|||Dentro de grupos: 26 áreas y las mismas 183 especialidades con 128, 256 y 512 artículos. Objetos distintos de los centros.
217 Subfields; 50 fixed queries each (10,850 total). Ten candidate selections.|||217 especialidades; 50 consultas fijas por cada una (10,850 en total). Diez selecciones de candidatos.
256 candidates in each scope, including all 50 queries. The Field pool is conditioned on these queries.|||256 candidatos en cada ámbito, incluidas las 50 consultas. El conjunto del área está condicionado por esas consultas.
2,000 per Field; twenty halves of 1,000 and five selections of 2,000.|||2,000 por área; veinte mitades de 1,000 y cinco selecciones de 2,000.
325 Field pairs and two properties; 26 saved conditions. Alternative metrics have different coverage.|||325 parejas y dos propiedades; 26 condiciones guardadas. Las medidas alternativas tienen distinta cobertura.
Panel|||Muestra
Checkpoint and full revision|||Modelo y versión completa
Input / truncation|||Entrada / recorte
Title [SEP] abstract|||Título [SEP] resumen
Title, blank line, abstract|||Título, línea vacía, resumen
Revision:|||Versión:
Adapter:|||Adaptador:
Limit:|||Límite:
Truncated:|||Recortado:
CLS + adapter|||CLS + adaptador
CLS, pre-pooler|||CLS, antes del pooler
Readout|||Representación
Reference|||Referencia
Mean|||Media
Models|||Modelos
Model|||Modelo
Agricultural and Biological Sciences|||Ciencias agrícolas y biológicas
Arts and Humanities|||Artes y humanidades
Biochemistry, Genetics and Molecular Biology|||Bioquímica, genética y biología molecular
Business, Management and Accounting|||Negocios, gestión y contabilidad
Chemical Engineering|||Ingeniería química
Chemistry|||Química
Computer Science|||Informática
Decision Sciences|||Ciencias de la decisión
Earth and Planetary Sciences|||Ciencias de la Tierra y planetarias
Economics, Econometrics and Finance|||Economía, econometría y finanzas
Energy|||Energía
Engineering|||Ingeniería
Environmental Science|||Ciencias ambientales
Immunology and Microbiology|||Inmunología y microbiología
Materials Science|||Ciencia de materiales
Mathematics|||Matemáticas
Medicine|||Medicina
Neuroscience|||Neurociencia
Nursing|||Enfermería
Pharmacology, Toxicology and Pharmaceutics|||Farmacología, toxicología y farmacia
Physics and Astronomy|||Física y astronomía
Psychology|||Psicología
Social Sciences|||Ciencias sociales
Veterinary|||Veterinaria
Dentistry|||Odontología
Health Professions|||Profesiones sanitarias
Field|||Área
Block|||Bloque
Coverage|||Cobertura
When specified|||Cuándo se fijó
Interpretation|||Interpretación
Initial comparison|||Comparación inicial
500,000 corpus; 130 cells; 45 fixed model pairs|||Corpus de 500,000; 130 grupos; 45 parejas fijas de modelos
Before this phase's agreements|||Antes de conocer los acuerdos de esta fase
Normalised vectors; corrected CKA, k25; CLS/SEP and size checks.|||Vectores normalizados; CKA corregida, k25; controles CLS/SEP y de tamaño.
52,000 paired IDs, distinct from the input panel|||52,000 identificadores emparejados, distintos de la muestra de entradas
Before first scientific comparison|||Antes de la primera comparación científica
Same content characters; native tokenizers and separators.|||Mismos caracteres de contenido; tokenizadores y separadores propios.
Centres / random groups|||Centros / grupos aleatorios
256 per centre; 26/217/26 centres|||256 por centro; 26/217/26 centros
Added after initial results|||Añadido tras los resultados iniciales
Matched dates/sizes; addresses centre averaging, not thematic validity.|||Fechas y tamaños iguales; comprueba el promedio de centros, no la validez temática.
Input expansion|||Ampliación de entradas
26,000 to 52,000 nested IDs|||De 26,000 a 52,000 identificadores anidados
After pilot; before expanded result|||Después del piloto; antes del resultado ampliado
Three inputs and pooling crossed; 100 comparable selections.|||Tres entradas cruzadas con reglas de representación; 100 selecciones comparables.
Matched local searches|||Búsquedas locales emparejadas
217 groups, 50 queries, ten selections|||217 grupos, 50 consultas, diez selecciones
Expanded phase design|||Diseño de la fase ampliada
256 candidates per scope, including identical queries and matched dates.|||256 candidatos por ámbito, con consultas idénticas y fechas iguales.
217 Subfields; 183 in sensitivity panel; 12 paper examples|||217 especialidades; 183 en controles de sensibilidad; 12 artículos de ejemplo
After global results; before reading selected titles|||Tras los resultados globales; antes de leer los títulos seleccionados
Rule-selected examples; source errors retained.|||Ejemplos elegidos por una regla; errores de la fuente conservados.
Morphology|||Morfología
52,000 IDs; alternative measures and synthetic clouds|||52,000 identificadores; medidas alternativas y nubes sintéticas
Exploratory extension after core results|||Ampliación exploratoria tras los resultados principales
Protocol before new real-data metrics. Neighbour-fraction check added during execution.|||Protocolo anterior a las nuevas medidas con datos reales. Control de fracción de vecinos añadido durante la ejecución.
Field pairs|||Parejas de áreas
325 pairs per property; 26 saved conditions|||325 parejas por propiedad; 26 condiciones guardadas
After morphology results|||Después de los resultados de morfología
Direction/magnitude rules fixed before new pair counts; no new inference.|||Reglas de dirección y magnitud anteriores a los nuevos recuentos; sin inferencia nueva.
Measures compared|||Medidas comparadas
Cells|||Grupos
Mean rank agreement|||Acuerdo medio de rangos
Minimum|||Mínimo
Maximum|||Máximo
Corrected CKA / Procrustes|||CKA corregida / Procrustes
Corrected CKA / Distance ranks|||CKA corregida / Rangos de distancias
Procrustes / Distance ranks|||Procrustes / Rangos de distancias
Title: shape|||Título: forma
Abstract: shape|||Resumen: forma
Title: neighbours|||Título: vecinos
Abstract: neighbours|||Resumen: vecinos
Selections / scope|||Selecciones / ámbito
Contrasts|||Contrastes
26k alerts|||Alertas 26k
52k alerts|||Alertas 52k
Persist|||Persisten
Resolved|||Resueltas
New|||Nuevas
model-Field|||modelo-área
Field average|||Media de áreas
Field overlap|||Coincidencia en área
Subfield overlap|||Coincidencia en especialidad
Difference (pp)|||Diferencia (pp)
Lower / higher|||Menor / mayor
Subfields|||Especialidades
Article and OpenAlex ID|||Artículo e identificador de OpenAlex
Subfield label|||Etiqueta de especialidad
Selection range|||Rango de selección
Inspection note|||Nota de inspección
Table \thetable{} (continued)|||Tabla \thetable{} (continuación)
Continued on next page|||Continúa en la página siguiente
Geriatrics and Gerontology|||Geriatría y gerontología
Applied Mathematics|||Matemáticas aplicadas
General Decision Sciences|||Ciencias de la decisión generales
Discrete Mathematics and Combinatorics|||Matemáticas discretas y combinatoria
Safety Research|||Investigación en seguridad
Safety, Risk, Reliability and Quality|||Seguridad, riesgo, fiabilidad y calidad
Political Science and International Relations|||Ciencia política y relaciones internacionales
Nuclear and High Energy Physics|||Física nuclear y de altas energías
Ceramics and Composites|||Cerámica y materiales compuestos
Ophthalmology|||Oftalmología
Software|||Software
Classics|||Estudios clásicos
No clear issue in this limited inspection; not expert validation.|||Sin problema claro en esta inspección limitada; no es validación experta.
Mathematics education under Applied Mathematics; administrative label.|||Enseñanza de matemáticas bajo Matemáticas aplicadas; etiqueta administrativa.
Persuasion economics under Safety Research; label caveat.|||Economía de la persuasión bajo Investigación en seguridad; advertencia de etiqueta.
Bacterial-infection abstract labelled as politics.|||Resumen de infección bacteriana etiquetado como política.
History-book description labelled as physics; type caveat.|||Descripción de libro de historia etiquetada como física; advertencia de tipo.
Substantial formula code in abstract; input caveat.|||Abundante código de fórmulas en el resumen; advertencia de entrada.
Announcement / atlas review; not detected by the original notice screen.|||Anuncio detectado al revisar el atlas; no por el filtro original de avisos.
Measure / candidate design|||Medida / diseño de candidatos
Mean change|||Cambio medio
Positive|||Positivo
Negative|||Negativo
Non-monotone|||No monótono
CKA, native groups|||CKA, grupos propios
CKA, 2,048 per group|||CKA, 2,048 por grupo
Distance ranks, native|||Rangos de distancias, propio
Procrustes, native|||Procrustes, propio
k25, all candidates|||k25, todos los candidatos
k25, 2,048 / mean|||k25, 2,048 / media
Ten|||Diez
Eight|||Ocho
CKA bal.|||CKA equil.
k25 bal.|||k25 equil.
Outcome|||Resultado
Rank|||Rango
Condition no.|||N.º de condición
R squared|||R cuadrado
Unidentified coefficients after omission|||Coeficientes no identificables tras omisión
CKA / primary|||CKA / principal
CKA / 2,048 articles|||CKA / 2,048 artículos
CKA / quality filter|||CKA / filtro de calidad
Neighbours k25 / mean|||Vecinos k25 / media
Neighbours k25 / CLS|||Vecinos k25 / CLS
Neighbours k25 / SEP|||Vecinos k25 / SEP
Property|||Propiedad
Selection design|||Diseño de selección
Cases|||Casos
Alerts|||Alertas
Median width|||Amplitud mediana
Maximum width|||Amplitud máxima
Angular spread|||Apertura angular
Effective linear dimension|||Dimensión lineal efectiva
Linear dimension|||Dimensión lineal
Connection|||Conexión
20 half samples|||20 medias muestras
5 equal-size selections|||5 selecciones de igual tamaño
Cloud|||Nube
Gap k25|||Brecha k25
Radius 90/50|||Radio 90/50
Max/median edge|||Arista máx./mediana
Mutual giant|||Componente mayor mutuo
One round cloud|||Nube redonda
One narrow cloud|||Nube estrecha
One wide cloud|||Nube ancha
One elongated cloud|||Nube alargada
One low-rank cloud|||Nube de rango bajo
Two separated groups|||Dos grupos separados
Four separated groups|||Cuatro grupos separados
Two groups with bridges|||Dos grupos con puentes
One cloud with outliers|||Nube con puntos atípicos
All ten agree|||Acuerdo de los diez
Opposition|||Oposición
Unresolved|||Sin resolver
Pairs|||Parejas
Model panel|||Conjunto de modelos
Spread + alternatives|||Apertura + alternativas
Spread|||Apertura
PR + alternatives|||PR + alternativas
All ten|||Los diez
Six similarity models|||Seis de similitud
Omit |||Sin 
Matched reference|||Referencia emparejada
Models changed|||Modelos cambiados
Spread retained|||Apertura conservada
PR retained|||PR conservada
Title only|||Solo título
Abstract only|||Solo resumen
Word BERTs: CLS|||BERT de palabras: CLS
Word BERTs: SEP|||BERT de palabras: SEP
Global centring|||Centrado global
Quality flags|||Marcas de calidad
Extreme-point removal|||Retirada de extremos
common\_native|||Entrada habitual del panel común
trim\_random|||Retirada aleatoria
half|||Media muestra
primary|||Principal
Object|||Material
Manifest / SHA-256|||Manifiesto / SHA-256
Access|||Acceso
Clean corpus|||Corpus limpio
Embedding audit|||Auditoría de embeddings
Core report|||Informe principal
Expanded report|||Informe ampliado
Case atlas|||Atlas de casos
Writing blueprint|||Plano de escritura
500,000 IDs; local|||500,000 identificadores; local
Ten models; local vectors|||Diez modelos; vectores locales
Tables / figures; public baseline|||Tablas / figuras; versión base pública
Examples; public baseline|||Ejemplos; versión base pública
Local extension; no data deposit|||Ampliación local; sin depósito de datos
Local editorial plan|||Plan editorial local
'''
LABELS=dict(line.split('|||',1) for line in PAIRS.strip().splitlines())
NOTES={
'T01':[r'Las filas se solapan y no deben sumarse. Períodos: 2000--04, 2005--09, 2010--14, 2015--19 y 2020--24. Cada comparación usa los mismos identificadores entre modelos. En la búsqueda, cada artículo de consulta se excluye a sí mismo. Los 1,300 artículos de prueba técnica no forman otra muestra científica. Filtros y cuotas completos: Tabla S1.'],
'T02':[r'MPNet y MiniLM utilizan all-mpnet-base-v2 y all-MiniLM-L6-v2, respectivamente. Los límites cuentan tokens, incluidos los símbolos especiales. Media: promedio de posiciones sin relleno de la última capa, con símbolos especiales. CLS: primera posición antes del pooler; SPECTER2 añade su adaptador de proximidad. En MPNet/MiniLM, la referencia describe el marco Sentence-BERT, no el entrenamiento exacto de esas versiones. Las reglas alternativas no son modelos adicionales. Versiones, formatos y recorte: Tabla S2.'],
'S01':[r'Total: 500,000 identificadores distintos de OpenAlex. Las columnas de períodos contienen base y refuerzo; las dos últimas reparten esos mismos artículos y no se vuelven a sumar. Catálogo principal; años 2000--2024; artículos, revisiones y congresos; etiqueta inglesa de OpenAlex, título no vacío, resumen reconstruible de al menos 50 palabras según expresión regular, área principal conocida y sin marca de retractación o paratexto. La limpieza adicional rechaza fallos claros de idioma o contenido y marca casos ambiguos. No se afirma que todos los resúmenes sean exclusivamente ingleses o estén bien etiquetados. Los CSV incluyen cantidades anuales, muestras y marcas de calidad; la descarga original terminó el 15 de septiembre de 2026. No es una fotografía simultánea de la base de datos.'],
'S02':[r'El recorte se mide en los 500,000 artículos con título y resumen y no es una tasa de error. MiniLM mantiene 256 tokens como principal; la variante de 512 es un control separado. CLS/SEP solo se aplican como alternativas a BERT, SciBERT, BioBERT y PubMedBERT. SEP toma la última posición sin relleno, no el separador del título. Igualar tokens no igualaría el texto porque los tokenizadores difieren. Los CSV contienen enlaces a las fichas de los modelos y todas las versiones.'],
'S03':[r'Es una secuencia de fases documentadas, no un estudio prerregistrado. Fuentes: ANALYSIS\_PROTOCOL, ROBUSTNESS\_PROTOCOL, CASE\_ATLAS\_PROTOCOL, MORPHOLOGY\_PROTOCOL y FIELD\_PAIR\_PROTOCOL, con sus decisiones fechadas. Los controles posteriores no se presentan como hipótesis iniciales.'],
'S04':[r'El panel presenta correlaciones descriptivas de Spearman del acuerdo entre parejas de modelos dentro de cada uno de los 130 grupos de área y período. Comparan medidas, no validan el contenido temático. La tabla se acompaña de los 41 resúmenes guardados y todas las alertas originales individuales.',r'Una amplitud cero al usar todo el grupo no demuestra estabilidad con menos artículos. Son controles dentro del corpus, no intervalos de confianza poblacionales. Las alertas de diseños diferentes se mantienen separadas.'],
'S05':[r'Mismos 52,000 identificadores y 2,000 candidatos por área. Cambio de forma: 1 menos CKA corregida. Cambio de vecinos: fracción de los 25 vecinos sustituidos. Título o resumen comparan cada modelo con su propia entrada completa. Los CSV incluyen medias del cambio de modelo, valores por área y cruce completo de reglas. Son cambios prácticos de entrada con límites propios, no una separación causal de modelo y longitud.',r'Contraste cambio de modelo menos cambio de entrada de solo título (positivo: cambiar modelo tiene mayor efecto medio): MEDIA, forma = 0.0042; MEDIA, vecinos = -0.0191; CLS, forma = 0.0363; CLS, vecinos = 0.0304; SEP, forma = 0.0627; SEP, vecinos = 0.0171. Solo cambian los cuatro BERT de palabras en CLS/SEP. Medias próximas no demuestran equivalencia.'],
'S06':[r'Las cinco alertas restantes de modelo, área y entrada con 100 selecciones son: BioBERT / Ciencias agrícolas y biológicas / resumen (amplitud 0.047); BioBERT / Ciencias de la Tierra y planetarias / resumen (0.045); BioBERT / Economía, econometría y finanzas / resumen (0.042); BioBERT / Inmunología y microbiología / resumen (0.063); PubMedBERT / Profesiones sanitarias / título (0.040). No tener alerta no implica un efecto distinto de cero. Los recuentos originales de 20 selecciones y posteriores de 100 se mantienen separados.'],
'S07':[r'Diferencia: especialidad menos área. Cada ámbito contiene 256 candidatos, incluidas las mismas 50 consultas, con fechas iguales; el propio artículo se excluye al buscar. Medias de diez selecciones de candidatos. La comparación amplia está condicionada por las consultas, no son 256 artículos del área seleccionados libremente. Las 217 especialidades están en el diseño emparejado; 183 cumplen todos los tamaños del control separado de 128/256/512. Se adjuntan los resultados completos de tamaño, regla de representación y k.'],
'S08':[r'Los valores son coincidencias k25 promediadas sobre 45 parejas de modelos; los rangos abarcan diez selecciones de candidatos. Los seis primeros y últimos ejemplos proceden de orígenes con alto y bajo acuerdo según la regla registrada. Los títulos se leyeron después de seleccionar y se conservan en su idioma original para identificarlos. Los CSV contienen identificadores, títulos y apoyos por modelo de orígenes y destinos para ambos tipos de relación. Se seleccionó la relación más dependiente del modelo para cada origen; no estima frecuencia. También se conserva un resumen de destino incompleto, marcado en la Figura S3. Ningún control valida las etiquetas de OpenAlex.'],
'S09':[r'Final menos inicio: 2020--24 frente a 2000--04. Cada fila describe 26 áreas con igual peso; los cambios de vecinos son fracciones, por lo que se multiplican por 100 para obtener puntos porcentuales. Se usan cinco períodos para clasificar la monotonicidad. Los CSV incluyen controles k10/k25/k50, reglas, consultas idénticas y parejas. El número de candidatos puede cambiar el signo. Son contrastes descriptivos entre períodos, no convergencia histórica causal.'],
'S10':[r'Ocho excluye BioBERT y PubMedBERT. 2,048 artículos por área con cuotas idénticas por fecha; media de diez selecciones. Energía tiene una especialidad válida, por lo que equilibrarla no genera un cambio comparable de composición. Se muestran las cuatro áreas de la Figura S5; se proporcionan las 26 y sus contrastes emparejados. Composición y entrenamiento biomédico no son explicaciones causales aisladas.'],
'S11':[r'Diez modelos fijos producen 45 parejas solapadas. R cuadrado describe esas parejas, no validez predictiva. La última columna cuenta filas de coeficientes no disponibles en las diez omisiones de un modelo, no modelos o pruebas independientes. En SEP, omitir SimCSE impide identificar coeficientes; esos valores siguen ausentes. Arquitectura, origen, corpus final, objetivo, dominio y regla de representación son características correlacionadas. Se adjuntan definiciones, enlaces de fuentes, coeficientes, referencias de permutación de etiquetas de parejas y omisiones. No se afirma un efecto causal del entrenamiento.'],
'S12':[r'Un caso combina modelo y área. La amplitud es el rango central del 90\% dividido por el valor principal; también se comprueba el desplazamiento de la mediana. Umbrales: 5\% apertura, 10\% PR, 20\% conexión. Son umbrales operativos de sensibilidad, no normas de la revista ni precisión poblacional. Las cuatro alertas de PR en medias muestras siguen visibles aunque pasen las cinco selecciones de igual tamaño. PR es dimensión lineal efectiva, no cantidad de temas. Las alternativas espectrales comparten el espectro de covarianza y no validan independientemente el significado temático.'],
'S13':[r'Cada nube guardada contiene 1,000 puntos. Una brecha menor puede aparecer sin grupos separados; los cocientes de radios y aristas pueden responder a puntos atípicos o nubes alargadas. El grafo de unión k25 está conectado en los 260 casos principales de modelo y área. La conexión describe el grafo y no queda validada como fragmentación temática general. Las cinco selecciones de igual tamaño conservan 51 alertas de conexión (Tabla S12).',r'Se incluyen las 780 filas de referencias gaussianas. Sus errores respecto a lo observado van de -4.69\% a 4.60\% en apertura y de -10.47\% a 19.78\% en PR. Los muestreos gaussianos conservan los momentos ajustados solo en esperanza antes de renormalizar; no son pruebas nulas calibradas. Se adjuntan controles n/k completos; el de fracción fija de vecinos se añadió durante la ejecución.'],
'S14':[r'Cada propiedad usa las 325 parejas de áreas y diez modelos. La dirección debe persistir en las 26 condiciones: muestra principal, veinte mitades y cinco selecciones de igual tamaño. La oposición necesita al menos dos modelos fijos persistentemente opuestos; la unanimidad, los diez. Los demás casos quedan sin resolver, no son iguales. La diferencia simétrica con signo es $2(B-A)/(A+B)$; el mínimo es un corte operativo de magnitud, no significación estadística ni proporción de ciencia correctamente representada. Se adjuntan las 650 filas de pareja y propiedad y las 6,500 direcciones por modelo.'],
'S15':[r'Todos los recuentos son sobre 325 y con magnitud mínima cero. Las alternativas deben conservar las direcciones de los mismos modelos opuestos; no se sustituyen por otros entre medidas. Las alternativas angulares tienen 26 condiciones guardadas y las espectrales tres. Los seis de similitud son SPECTER, SPECTER2, SciNCL, MPNet, MiniLM y SimCSE. Menos modelos ofrecen menos oportunidades de oposición; este conjunto no aísla un efecto del entrenamiento. Los CSV incluyen los cuatro cortes de magnitud y la identidad de los modelos que sustentan la oposición.'],
'S16':[r'Los numeradores conservan la misma pareja original de modelos y sus signos tanto en la referencia como en la variante. Los denominadores son las oposiciones persistentes originales: 262 de apertura y 221 de PR. No son nuevas pruebas de estabilidad de 26 condiciones. El fragmento común utiliza su muestra emparejada propia; retirar extremos se compara con retirar al azar a igual tamaño. Calidad, extremos y tamaño cambian identificadores según lo especificado; los demás controles los conservan. Se incluyen todas las magnitudes y los 7,150 registros de parejas de controles puntuales.'],
'S17':[r'Las huellas identifican los bytes del manifiesto o catálogo indicado, no directamente toda la carpeta; cada catálogo registra sus archivos. La reproducción local es más amplia que el acceso público. No se afirma un depósito persistente, licencia general o nueva publicación. El paquete excluye corpus, vectores, pesos, claves de API y textos completos de terceros. Los dos PDF pueden reconstruirse con el LaTeX y las figuras y tablas incluidos, sin el corpus. Reproducir todos los experimentos sigue requiriendo el plan de publicación de datos autorizado por separado.']}
ITEMS={
'Original Field-period screen: 50 alerts among 5,850 comparisons; largest central-95\\% selection width among flagged cases: 0.064.':r'Control original de área y período: 50 alertas entre 5,850 comparaciones; mayor amplitud central del 95\% entre los casos marcados: 0.064.',
'The larger sample does not equal the entire group: 2,628 alerts / 8,235 comparisons; 183 Subfields.':'La muestra mayor no abarca todo el grupo: 2,628 alertas / 8,235 comparaciones; 183 especialidades.',
'The larger sample equals the entire group: 213 alerts / 3,060 comparisons; 68 Subfields.':'La muestra mayor abarca todo el grupo: 213 alertas / 3,060 comparaciones; 68 especialidades.'}
LABELS.update(ITEMS)
pattern=re.compile('|'.join(re.escape(k) for k in sorted(LABELS,key=len,reverse=True)))
note_pattern=re.compile(r'\\par\\smallskip\{\\small (.*?)\\par\}',re.S)
protected=re.compile(r'\\(?:nolinkurl|seqsplit|citep)\{[^}]*\}')

def local_numbers(text):
    def convert(m):
        return m.group().replace(',','@').replace('.',',').replace('@','.')
    return re.sub(r'(?<![A-Za-z0-9])\d+(?:,\d{3})+(?:\.\d+)?|(?<![A-Za-z0-9])\d+\.\d+',convert,text)

counts={}
manifest_path=OUT/'tables/manifest.json'
manifest=json.loads(manifest_path.read_text())
for src in sorted((ROOT/'manuscript/tables/tex').glob('*.tex')):
    editorial = OUT/'tables/editorial'/src.name
    if editorial.exists():
        reviewed=editorial.read_text()
        (OUT/'tables/tex'/src.name).write_text(reviewed)
        counts[src.stem] = {'editorial_source': str(editorial.relative_to(OUT))}
        header_line=next(line for line in reviewed.splitlines() if line.startswith(r'\textbf') and ' & ' in line)
        manifest[src.stem]['rendered_parts']=[{
            'caption': re.search(r'\\captionof\{table\}\{([^}]+)\}',reviewed).group(1),
            'headers': re.findall(r'\\textbf\{([^}]+)\}',header_line),
            'rows': sum(' & ' in line for line in reviewed.splitlines())-1,
        }]
        manifest[src.stem]['editorial_source']={
            'path': str(editorial.relative_to(OUT)),
            'sha256': hashlib.sha256(editorial.read_bytes()).hexdigest(),
        }
        manifest[src.stem]['summary_rule']='Explicación por finalidad revisada el 20-09-2026; tamaños y reglas de modelos sin cambios.'
        continue
    text=src.read_text(); saved=[]
    def protect(m):
        saved.append(m.group()); return f'ZZPROTECTED{len(saved)-1}ZZ'
    text=protected.sub(protect,text)
    if src.stem=='S08':
        text=re.sub(r'^[^\n]+(?=\\newline\{\\footnotesizeZZPROTECTED)',protect,text,flags=re.M)
    notes=NOTES[src.stem]; assert len(note_pattern.findall(text))==len(notes)
    it=iter(notes)
    # Protect translated notes so broad cell-label translations never touch them.
    text=note_pattern.sub(lambda m:protect(type('M',(),{'group':lambda self:'\\par\\smallskip{\\small '+next(it)+'\\par}'})()),text)
    text=pattern.sub(lambda m:LABELS[m.group()],text)
    for i in reversed(range(len(saved))):text=text.replace(f'ZZPROTECTED{i}ZZ',saved[i])
    # Translate numeric typography only in content lines, never column widths or hashes.
    result=[]
    for line in text.splitlines():
        if (' & ' in line or line.startswith(('\\par\\smallskip','\\item','\\caption'))):
            keep=[]
            def keep_item(m):keep.append(m.group());return f'ZZNUM{len(keep)-1}ZZ'
            line=protected.sub(keep_item,line)
            line=local_numbers(line)
            for i,v in enumerate(keep):line=line.replace(f'ZZNUM{i}ZZ',v)
        result.append(line)
    target=OUT/'tables/tex'/src.name;target.write_text('\n'.join(result)+'\n')
    counts[src.stem]={'notes':len(notes)}
(OUT/'tables/translation_index.json').write_text(json.dumps(counts,indent=2)+'\n')
manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Translated 19 display tables, preserving raw CSV files and bibliographic titles.')
