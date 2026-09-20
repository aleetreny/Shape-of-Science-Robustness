# Propuesta aplicada de estructura para QSS

**18-09-2026. Propuesta para conversar con el usuario. No es un manuscrito.**

Basada en [la revisión de 34 trabajos de QSS](QSS_STRUCTURE_REVIEW.md), con lectura estructural de 33 y acceso parcial a uno. El esquema anterior está conservado en [la copia de inicio](research/qss_structure_2026-09-18/baseline_documents/PAPER_OUTLINE.md). No se modifican protocolos ni resultados.

## Qué paper proponemos

**Un estudio de qué conclusiones sobre los mapas de ciencia resisten cambios razonables en la representación de los mismos artículos.**

La contribución se explica mostrando qué parte del resultado es compartida y dónde cambia la conclusión, con su magnitud y sus controles. El tamaño del corpus y los diez modelos hacen posible esa comparación; no constituyen por sí solos la novedad.

Título de trabajo, aún orientativo: **Which conclusions about science maps survive a change of embedding model?**

La analogía es fotografiar los mismos objetos con distintas cámaras. Primero mirar la escena general, después los detalles y, finalmente, comprobar si cambia nuestra respuesta a “¿cuál de estas dos áreas parece más abierta o repartida entre más direcciones?”.

El paper no evalúa una verdad temática externa ni busca un modelo ganador. Define “forma” mediante objetos distintos: relaciones entre grupos, organización interna, vecinos y dos descripciones geométricas. No los suma en un porcentaje único de ciencia conservada.

## Tres preguntas que ordenan la evidencia

| Pregunta propuesta | Qué resultado la responde | Qué no responde |
| --- | --- | --- |
| **P1. ¿Qué estructura y relaciones se conservan entre modelos, y a qué escala?** | Estructura entre áreas, interior de grupos y vecinos; controles emparejados de Field/Subfield | Cuál es el mapa científicamente correcto |
| **P2. ¿Cuánto depende la comparación del texto que recibe cada modelo y de la forma de resumirlo?** | Tres entradas sobre los mismos 52.000 IDs; media como receta principal y CLS/SEP como controles | Efecto causal puro de arquitectura, contenido o entrenamiento |
| **P3. ¿Se mantienen las comparaciones geométricas entre disciplinas al cambiar el modelo?** | Apertura y reparto entre direcciones; 325 parejas, selecciones repetidas, alternativas y magnitudes | Diversidad semántica, número de temas o fragmentación general |

Estas preguntas organizan ahora el manuscrito. **No son tres hipótesis registradas antes de toda la evidencia.** P3 procede de una ampliación exploratoria posterior; también hay controles añadidos tras conocer fases anteriores.

## Índice y presupuesto

Presupuesto propio de **6.750 palabras de cuerpo**, sin contar aquí resumen, referencias, tablas y pies. No es requisito de QSS; confirmar el cómputo editorial al preparar el envío. Resumen propuesto: 180–200 palabras para problema, diseño, dos resultados y consecuencia. Se redactará después.

| Sección | Palabras | Función |
| --- | ---: | --- |
| 1. Introduction | 800 | Dar importancia al problema y delimitar la aportación |
| 2. Background and research questions | 750 | Definir conceptos, situar antecedentes y plantear P1–P3 |
| 3. Data and comparative design | 1.600 | Permitir entender y evaluar la comparación |
| 4. Results | 2.250 | Responder en cuatro bloques conectados |
| 5. Discussion | 1.150 | Explicar consecuencias, antecedentes y límites |
| 6. Conclusion | 200 | Cerrar la pregunta sin nuevas afirmaciones |

### 1. Introduction

Cuatro movimientos, sin cuatro subsecciones obligatorias:

1. Para qué se usan mapas de ciencia y por qué importa la dependencia de la representación.
2. Qué se sabe ya sobre dependencia de fuentes, clasificaciones y métodos.
3. Qué añade esta comparación: mismos artículos, encoders/entradas, escalas y persistencia de comparaciones entre áreas.
4. Aportación y adelanto: estructura amplia compartida, detalle condicionado y algunas comparaciones que se invierten.

No abrir con arquitecturas ni descargas. No afirmar que nadie ha comparado representaciones o que todo desacuerdo invalida un mapa.

### 2. Background and research questions

**2.1. Representation choices in science mapping.** Comparación de mapas/clasificaciones y perspectivas distintas del mismo objeto. Núcleo: Boyack/Klavans, Sīle y Constantino, junto con antecedentes próximos de la biblioteca.

**2.2. Agreement, stability and interpretation.** Coincidencia, persistencia y validez temática son cosas distintas. Waltman, Wang/Schneider y Held/Held–Velden ayudan a fijar esa diferencia. Definir qué llamamos forma.

**2.3. Research questions and scope.** Presentar P1–P3 y el carácter posterior de la ampliación de propiedades. Mantener antecedentes fuera de QSS, especialmente Caspari y los trabajos sobre entrada, recetas y sesgos de [RELATED_WORK.md](references/RELATED_WORK.md).

Comparar aportaciones; no escribir un párrafo aislado por cada uno de los 34 artículos.

### 3. Data and comparative design

**3.1. Corpus and analytical panels.** OpenAlex, inglés, resumen disponible, 2000–2024, 26 Fields y cinco períodos. Los 400.000 de base y 100.000 de complemento, filtros, congelación e IDs comunes. Explicar para qué se usa cada selección. Una muestra equilibrada entre áreas no reproduce la composición mundial de la ciencia.

**3.2. Models and text representations.** Diez modelos, versiones, formatos y límites habituales. Media para los cuatro BERT de palabras; CLS/SEP como sensibilidad. MiniLM 256 es el principal oficial y 512 un control separado; el límite original no fue un error de código.

**3.3. Objects and measures.** Definiciones mínimas de acuerdo de forma, vecinos compartidos, apertura angular y dimensión efectiva lineal —reparto de variación entre direcciones, PR—. Centros e interior son objetos distintos. CKA corregida y k25 principales; Procrustes/RSA y otros k como comprobaciones. No escoger después la medida que produce más diferencias.

**3.4. Matched comparisons and stability.** Mismos IDs, tamaños/candidatos comparables donde procede, selecciones repetidas y reglas de contradicción. Para las 325 parejas, oposición persistente exige dos modelos con signos opuestos, cada uno persistente en las condiciones fijadas; unanimidad exige los diez. Explicar diferencia relativa simétrica y varios mínimos, sin llamarlos significación ni importancia universal.

**3.5. Scope of robustness checks.** Receta, entrada, fragmento común, calidad, tamaño, centrado, Medicina, tiempo y familias. Distinguir repeticiones y controles puntuales; explicar qué se decidió antes de cada bloque y qué se añadió después. Remitir a una tabla de cobertura en suplemento. Las selecciones del corpus no son intervalos poblacionales.

Fuentes de esta sección: [METHODS_ANALYSIS.md](METHODS_ANALYSIS.md), [METHODS_ROBUSTNESS.md](METHODS_ROBUSTNESS.md), [POOLING.md](POOLING.md), [METHODS_MORPHOLOGY.md](METHODS_MORPHOLOGY.md) y [METHODS_FIELD_PAIRS.md](METHODS_FIELD_PAIRS.md).

### 4. Results

| Bloque | Mensaje | Evidencia y límite |
| --- | --- | --- |
| **4.1. Shared broad structure and within-field variation** · 450 palabras | Acuerdo entre grupos amplios no garantiza el mismo acuerdo dentro de ellos | Referencias aleatorias y tamaños comparables; centros e interior son objetos diferentes. Figura 1 |
| **4.2. Neighbour agreement under matched comparisons** · 500 | Las relaciones locales dependen de la representación; acercarse al Subfield no reduce siempre el acuerdo | Baja en 127/217 y sube en 90; media −1,35 puntos para k25. Candidatos controlados y ejemplo exploratorio breve. Figura 2 |
| **4.3. Text input and representation choices** · 500 | Quitar el resumen puede alterar tanto como cambiar modelo bajo el diseño principal | Cambios de vecinos: 68,76% por modelo, 70,67% con título solo, 22,12% con resumen solo. Medias próximas no prueban equivalencia; orden dependiente de receta. Figura 3 |
| **4.4. Persistence and reversal of geometric field comparisons** · 800 | Una comparación persistente al cambiar artículos puede invertirse entre encoders | De 325 parejas: 262 contradicciones en apertura, 221 en PR; con mínimo relativo de 5%, 96 y 177. Magnitudes, alternativas, casos no resueltos y centrado/receta. Figura 4 |

Cada cifra mantiene su denominador. No mezclar el acuerdo de vecinos de las celdas originales —30,3%; 31,9% con candidatos iguales— con el experimento de entrada de 52.000 como si fueran el mismo cálculo.

El bloque 4.4 es exploratorio posterior, aunque sus reglas se fijaron antes de esos recuentos. No reemplaza las medidas principales anteriores. Mostrar acuerdos y casos no resueltos, no solo inversiones.

Los controles que cambian la lectura se resumen junto al resultado: ausencia de caída universal a Subfield; cambio temporal dependiente de candidatos; apertura sensible al centrado; alertas con denominadores separados. El detalle completo queda en suplemento.

### 5. Discussion

**5.1. What is shared and what depends on representation.** Responder P1–P3 sin repetir todas las cifras. Qué puede asumirse al interpretar un mapa, separando coincidencia y verdad.

**5.2. Relation to prior work.** Contrastar los antecedentes próximos de representaciones, mapas y consistencia de medidas. Reconocer lo ya demostrado y precisar qué añade la persistencia de conclusiones en nuestro diseño.

**5.3. Implications for using science maps.** Declarar encoder/entrada/receta; mantener comparables los conjuntos de búsqueda; comprobar conclusiones sustantivas con alternativas justificadas; informar magnitud y casos no resueltos. No prescribir un modelo correcto por consenso ni consecuencias de política científica no estudiadas.

**5.4. Limitations and next questions.** Corpus/modelos acotados; etiquetas imperfectas; solapamiento con entrenamiento desconocido; comparaciones no independientes; ausencia de validación temática externa; controles con alcance distinto; ampliaciones posteriores y remuestreo no poblacional. Una validación temática dirigida sería otra pregunta, no una prueba ya realizada.

Se pueden combinar apartados al redactar. Separar discusión y resultados nos ayuda a distinguir observación y explicación; QSS admite otras organizaciones.

### 6. Conclusion

Un párrafo breve: respuesta central, consecuencia práctica y límite esencial. Sin nuevas cifras ni un mapa verdadero. Redactarlo al final junto con título y resumen.

Después: autoría, financiación, intereses, disponibilidad y declaraciones pertinentes según la guía vigente. Completar con información real. No declarar depósito de datos o licencia todavía inexistentes.

## Dos tablas principales

**Tabla 1. Diseño y alcance de cada análisis.**

| Panel | Alcance |
| --- | --- |
| Corpus original | 500.000 IDs; 400.000 base + 100.000 complemento; diez encoders |
| Tres entradas | 52.000 IDs; 400 por Field/período; incluye el piloto de 26.000 |
| Fragmento común | Otra selección de 52.000, distinta del experimento de tres entradas |
| Field/Subfield emparejado | 217 grupos; 50 consultas cada uno; diez selecciones de 256 candidatos; consultas incluidas en ambos ámbitos |
| Morfología y parejas | Principal de 2.000 por Field; veinte medias muestras y cinco selecciones adicionales; alternativas espectrales y controles puntuales con alcance distinto |

**Tabla 2. Modelos y uso principal.** Diez nombres, referencia, versión identificable, longitud máxima, texto y receta. Huellas completas y variantes a suplemento/material reproducible. Usar [MODEL_SELECTION.md](MODEL_SELECTION.md), [EMBEDDINGS.md](EMBEDDINGS.md) y [POOLING.md](POOLING.md). Dieciocho variantes originales no son dieciocho modelos independientes.

La matriz de conclusiones y controles va al suplemento; no exige una tercera tabla principal.

## Cuatro figuras existentes

| Orden | Archivo | Qué debe decir el pie |
| --- | --- | --- |
| 1. Estructura entre grupos y dentro de ellos | [02_scales.pdf](reports/robustness_v2/final/figures/02_scales.pdf) | Centros de 256 artículos; grupos aleatorios con tamaños/fechas conservados; control del número de centros. Interior sobre los mismos 183 Subfields elegibles en tres tamaños y 26 áreas. CKA no es porcentaje de ciencia correcta |
| 2. Vecinos en ámbitos comparables | [03_paired_neighbors.pdf](reports/robustness_v2/final/figures/03_paired_neighbors.pdf) | 217 Subfields, 50 consultas fijas, diez selecciones de 256, cuotas temporales iguales y k25. El Field está condicionado a incluir las consultas del Subfield; k50 casi divide por mitad el signo |
| 3. Modelo frente a entrada | [01_input_effect.pdf](reports/robustness_v2/final/figures/01_input_effect.pdf) | 52.000 IDs, 2.000 candidatos por área reuniendo fechas; punto = resumen de área, no intervalo de confianza. Uso habitual, con recortes efectivos distintos |
| 4. Conclusiones y magnitud | [01_conclusions_and_magnitude.pdf](reports/field_pair_summary_v1/01_conclusions_and_magnitude.pdf) | 325 parejas, diez modelos y 26 condiciones de selección. Dos testigos opuestos bastan; mínimos relativos son sensibilidad; casos no resueltos visibles. Ampliación posterior, sin interpretación temática |

**Centrado global:** conserva los mismos testigos en 145/262 aperturas y 218/221 PR; debe aparecer en el cuerpo. El panel de seis modelos de similitud mantiene 231/160 contradicciones sin mínimo; tener menos pares posibles impide atribuir causalmente el descenso al entrenamiento.

Artes/Medicina puede ilustrar una inversión, junto a todas las parejas y declarado como ejemplo elegido después de los resultados. No necesita una figura principal adicional.

## Suplemento propuesto

Organizarlo por la afirmación que comprueba. No incluir automáticamente todo gráfico producido.

| Bloque | Contenido y fuente |
| --- | --- |
| S1. Corpus y procedencia | Filtros, reparto, calidad, modelos, texto y recortes. [PREPAPER_REVIEW.md](PREPAPER_REVIEW.md), [EMBEDDINGS_AUDIT.md](EMBEDDINGS_AUDIT.md) |
| S2. Acuerdo y estabilidad | Matrices, alternativas, tamaños y alertas. [CONCLUSION_CONTROLS.md](CONCLUSION_CONTROLS.md), [SAMPLING_STABILITY.md](SAMPLING_STABILITY.md) |
| S3. Entradas y recetas | Tres entradas, mean/CLS/SEP, MiniLM 256/512, fragmento común y 26k→52k. [ROBUSTNESS_RESULTS.md](ROBUSTNESS_RESULTS.md) |
| S4. Escala y casos | Comparación emparejada, otros k, atlas y reglas. [SCALES_AND_DISCIPLINES.md](SCALES_AND_DISCIPLINES.md), [CASE_ATLAS.md](CASE_ATLAS.md) |
| S5. Tiempo, Medicina y familias | Resultados y límites. [TEMPORAL_REVIEW.md](TEMPORAL_REVIEW.md), [MODEL_FAMILIES.md](MODEL_FAMILIES.md), figuras 04–06 de robustez |
| S6. Geometría | Apertura/PR, alternativas, selecciones y controles; conexión con contraejemplos. [MORPHOLOGY_RESULTS.md](MORPHOLOGY_RESULTS.md) |
| S7. Todas las parejas | Magnitudes, mismos testigos, seis modelos, retirar uno y centrado/receta. [FIELD_PAIR_RESULTS.md](FIELD_PAIR_RESULTS.md), [mapa completo](reports/field_pair_summary_v1/02_all_field_pairs.pdf) |
| S8. Reproducción | Configuración, fuentes/huellas, entorno y acceso real. [REPRODUCING.md](docs/REPRODUCING.md), [DATA_RELEASE.md](docs/DATA_RELEASE.md) |

Tiempo, Medicina y familias matizan el argumento; no necesitan tres historias principales. El atlas permite un ejemplo breve. Los errores de fuente detectados y los límites importantes sí aparecen en el cuerpo. Los centros del atlas no tienen control adicional de receta.

## Límites que deben sobrevivir al acortar

- Cinco alertas de entrada a 52k/100 selecciones; 50 originales y las de Subfields por separado. Cuatro alertas de PR y 51 de conexión. Sin alerta no significa precisión poblacional.
- PR/entropía/D80 describen el mismo espectro, no validación temática independiente. Las alternativas espectrales de parejas solo tienen tres condiciones guardadas.
- La conexión no se validó como fragmentación general; conservar contraejemplos. Las referencias gaussianas conservan momentos solo en expectativa antes de normalizar y no son pruebas estadísticas.
- Apertura depende del centrado/receta. Los mínimos 1%, 5%, 10% son sensibilidad de magnitud, no cortes universales.
- Tiempo: vecinos −0,87 puntos con todos los candidatos y +0,91 con 2.048; forma crece entre extremos en 24/26 áreas, solo cuatro monótonas. No convergencia histórica causal.
- Medicina no tiene el menor acuerdo en todas las medidas; retirar biomédicos no elimina su contraste de forma con Energía. No hay una causa única probada.
- Los errores de OpenAlex y un Announcement se conservan. Revisar títulos genéricos no estima todo error temático ni limpia candidatos.
- Pares de modelos/áreas y selecciones comparten elementos; no son observaciones independientes.
- Los 500.000 tienen resultados locales, pero solo 10.850 consultas del atlas tienen diez selecciones controladas de candidatos.
- No todos los controles se cruzaron entre sí. Los controles puntuales de parejas no tienen automáticamente sus propias 25 repeticiones. No mostrar figuras de 26k como resultados de 52k.
- Datos grandes locales. La publicación previa es `44c9410`; las ampliaciones posteriores no se presuponen subidas ni depositadas.

## Continuación

Recomiendo **un único paper con este hilo**, geometría como cuarto bloque acotado y los análisis explicativos como apoyo. Separarlo ahora perdería la conexión entre acuerdo general y consecuencias concretas; dar igual espacio a todos los experimentos diluiría la pregunta. Es una propuesta de presentación, no una decisión científica nueva ya aceptada.

El próximo paso es conversar sobre este esquema. Cuando se pida redactar, empezar por métodos/resultados y después discusión, introducción, título/resumen. Esta propuesta no necesita nuevos cálculos. Mantener [NEXT_STEPS.md](NEXT_STEPS.md) y [QSS_CHECK.md](docs/QSS_CHECK.md) como continuidad.
