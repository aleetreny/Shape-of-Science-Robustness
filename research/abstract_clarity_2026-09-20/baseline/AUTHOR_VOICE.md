# Cómo escribir con la voz de Alejandro

**Aceptación expresa, 20-09-2026:** «me gusta este tono mucho, conservalo». El cierre de robustez conserva esa voz clara en ambos idiomas. Las nuevas pruebas cambian algunos límites de las conclusiones, no el modo de explicar. La elección de tono está cerrada; no equivale a aprobación final del contenido.

**Regla prioritaria del autor, 20-09-2026.** V2 queda elegida como orientación de voz. El autor considera que incluso esa versión era demasiado densa: la identidad debe estar en el razonamiento claro, no en palabras cultas o construcciones difíciles. La reescritura vigente está en [MANUSCRIPT_CLARITY.md](MANUSCRIPT_CLARITY.md).

- Explicar primero qué queremos averiguar, qué mantenemos igual y qué cambiamos. Después dar el nombre de la medida o del procedimiento.
- Introducir cada término necesario con una explicación cotidiana. Por ejemplo, un vector es la lista de números con la que el modelo sitúa un artículo; sus vecinos son los artículos que quedan más cerca.
- Identificar las muestras por su pregunta, no solo por un número. Los 26.000 son la primera prueba del experimento de texto, incluidos en sus 52.000. El control de fragmento común usa otros 52.000. Repetir esta distinción donde cambie la comparación.
- Dar significado a los resultados antes de acumular cifras. Explicar una pareja como dos áreas que comparamos y mostrar qué significa obtener respuestas contrarias. En el resumen basta el hallazgo comprensible; los recuentos completos van después.
- Usar verbos concretos, palabras corrientes y primera persona puntual. Mantener un ritmo natural; no convertir toda la prosa en frases telegráficas, preguntas retóricas o analogías.
- Conservar cifras, alcance, citas, controles y límites. Mover una fórmula al suplemento cuando ayude, dejando su explicación y referencia en el cuerpo. Simplificar no permite atribuir corrección temática a una coincidencia entre modelos.

Estas reglas rigen en ambos idiomas y en revisiones futuras. La elección de V2 no es aprobación final del artículo.

**Origen de la guía, 18-09-2026.** La lectura del portfolio que sigue documenta cómo se adaptó la voz del autor a un artículo de QSS. Se conserva como referencia; la petición directa del 20-09 tiene prioridad sobre estas observaciones.

La referencia es alguien que quiere entender un problema y te lleva por su razonamiento: qué ocurre, qué hizo para mirarlo y qué puede concluir. El registro académico debe conservar esa cercanía intelectual sin trasladar literalmente una conversación de blog.

## Qué se ha leído

Las **50 entradas publicadas** de [aleetreny.github.io](https://github.com/aleetreny/aleetreny.github.io), revisión `5361e0354dd8419b4cf72089b7e8e51124830cfb`: 27 proyectos, 13 experiencias, tres entradas de formación y siete notas personales. Se leyó toda la prosa española de sus bloques de texto/listas y se inspeccionaron los pies. Son aproximadamente **12.800 palabras** de prosa/listas, sin títulos, pies ni traducciones; el recuento por espacios es orientativo.

La copia pública `fixtures/demo-content.json` es el contenido inicial del sitio, no una colección ficticia deducida de su nombre. Sus cuatro archivos de contenido/procedencia consultados coinciden con el repositorio local. El README documenta traducción automática: **no usamos la versión inglesa como prueba de tu inglés escrito a mano**. No se consultó la base de datos del sitio; pueden existir cambios publicados allí que todavía no estén en este commit. Tampoco se leyeron todos los sitios externos enlazados desde las entradas.

Tomamos la autoría de tu indicación; Git no permite certificar qué frase se escribió a mano. No atribuimos estilo a README, documentación técnica, código ni traducciones. [Inventario completo y lectura](research/writing_blueprint_2026-09-18/author_corpus.csv) · [Procedencia](research/writing_blueprint_2026-09-18/author_provenance.json) · [Notas de lectura](research/writing_blueprint_2026-09-18/AUTHOR_READING_NOTES.md).

## Rasgos que sí aparecen en los textos

Los ejemplos siguientes son fragmentos del autor. Las posiciones remiten a bloques del archivo fijado; se conserva la redacción original. Son observaciones cualitativas, no una firma estadística de autoría.

| Rasgo observado | Ejemplo y procedencia | Cómo llevarlo al paper |
| --- | --- | --- |
| Primero das una razón práctica para mirar el problema | «El gran problema de las empresas de este sector es la liquidez»; [Siemens, bloque 4](https://github.com/aleetreny/aleetreny.github.io/blob/5361e0354dd8419b4cf72089b7e8e51124830cfb/fixtures/demo-content.json#L5) | Abrir con qué decisión se apoya en un mapa y qué cambia si depende del modelo. Evitar una apertura genérica sobre la revolución de la IA. |
| Explicas la transformación paso a paso | «cada uno de estos puede ser transformado a un vector de cientos de variables»; [Mapping Science, bloque 2](https://github.com/aleetreny/aleetreny.github.io/blob/5361e0354dd8419b4cf72089b7e8e51124830cfb/fixtures/demo-content.json#L3957) | Explicar cómo se pasa del artículo al vector y del vector a la comparación, antes de acumular nombres de medidas. |
| Aterrizas la utilidad con ejemplos y objetos concretos | [Localízate, bloques 2–5](https://github.com/aleetreny/aleetreny.github.io/blob/5361e0354dd8419b4cf72089b7e8e51124830cfb/fixtures/demo-content.json#L4130): registros mensuales, locales, meses y hexágonos | Explicar qué significa conservar un vecino o invertir una comparación entre dos áreas. Dar denominador y unidad a las cifras. |
| Dices qué probaste y cuándo algo falló | «Incluso probamos modelos de supervivencia como Cox [...] pero no funcionaron bien»; [Siemens, bloque 10](https://github.com/aleetreny/aleetreny.github.io/blob/5361e0354dd8419b4cf72089b7e8e51124830cfb/fixtures/demo-content.json#L5) | Contar por qué conexión no quedó validada como fragmentación. Mostrar el límite relevante sin esconderlo detrás de una frase de cortesía. |
| Matizas una representación recordando el objeto que simplifica | «Una película es mucho más que su texto»; [Hollywood Mirror, bloque 2](https://github.com/aleetreny/aleetreny.github.io/blob/5361e0354dd8419b4cf72089b7e8e51124830cfb/fixtures/demo-content.json#L4543) | Distinguir geometría de temática: un vector y su forma no agotan lo que es una disciplina. |
| La curiosidad lleva a una pregunta examinable | [Vexilología, bloques 1–2](https://github.com/aleetreny/aleetreny.github.io/blob/5361e0354dd8419b4cf72089b7e8e51124830cfb/fixtures/demo-content.json#L4401): una pregunta sobre patrones conduce a construir variables | Formular una pregunta central y explicar cómo los análisis permiten responderla. No presentar una colección de técnicas como aportación. |
| Alternas desarrollo y remate breve | [Tropical, bloques 7–8](https://github.com/aleetreny/aleetreny.github.io/blob/5361e0354dd8419b4cf72089b7e8e51124830cfb/fixtures/demo-content.json#L457) contiene explicaciones extensas; «Plena autonomía» cierra un pasaje de Accenture | No volver todo telegráfico. Una frase corta puede cerrar una idea ya demostrada; no usar un eslogan al final de cada párrafo. |
| Sitúas una decisión en quien la tomó y explicas su coste | [Frulogy, bloques 3–4](https://github.com/aleetreny/aleetreny.github.io/blob/5361e0354dd8419b4cf72089b7e8e51124830cfb/fixtures/demo-content.json#L6253): trabajo, límites de tiempo y cierre | Nombrar nuestras elecciones de diseño y lo que permiten, sin hacerlas pasar por leyes del campo. |

El tono varía: experiencias largas y personales, proyectos explicativos y notas mucho más informales. No existe una única longitud de frase ni un número de analogías que imitar. Para el paper, pesan especialmente Mapping Science, Localízate, Hollywood Mirror, Siemens, Tropical y los proyectos del laboratorio; las otras entradas ayudan a entender el ritmo y la relación con el lector.

## Qué conservamos y qué adaptamos

**Conservar:** motivación concreta, verbos de acción, explicaciones encadenadas, gusto por mecanismos y ejemplos, juicio propio justificado y límites reconocibles. El lector debe poder reconstruir por qué hicimos la comparación.

**Adaptar:** el entusiasmo pasa a una pregunta interesante y una observación precisa. Las anécdotas laborales, chistes, exclamaciones, segunda persona continua y expresiones como «brutal» o «lo chulo» se quedan en el blog. Corregimos errores de escritura sin convertir la prosa en burocracia. No copiamos afirmaciones antiguas sobre «medidas objetivas», ausencia de sesgo o significatividad: los límites del estudio actual mandan.

**Persona gramatical:** preferir sujeto y acción a pasivas innecesarias. Usar primera persona cuando haga visible una decisión. No fijar un plural de autores antes de confirmar la lista real de autoría; también sirven “the analysis”, “the comparison” y construcciones directas. Evitar repetir “this study” al inicio de cada frase.

**Idioma:** esquema y conversación en español sencillo; títulos y futuro manuscrito en inglés académico claro. Trasladar tu razonamiento al inglés, sin calcar giros españoles ni sustituirlo por vocabulario grandilocuente. Mantener términos científicos estables, por ejemplo *agreement* para coincidencia y *thematic validity* para validez temática.

## Ejemplos breves de edición

Son ejemplos de estilo, **no párrafos redactados para insertar en el manuscrito**. Deben revisarse con su contexto y evidencia cuando toque escribir.

| Evitar | Dirección de edición más cercana a tu voz |
| --- | --- |
| “This comprehensive investigation offers profound insights into the intricate landscape of science.” | “The comparison asks which relationships remain when the same papers are represented by different models.” |
| “A multi-perspective assessment of representation-dependent neighbourhood preservation was conducted.” | “For each paper, the analysis checks how many of its 25 nearest neighbours are shared by two models.” |
| “These findings unequivocally demonstrate the superiority of robust methodological triangulation.” | “A field comparison can persist across article selections and still reverse between models.” |
| “The results may potentially suggest important implications for future research.” | Nombrar qué uso concreto cambia y cuál es el límite. Si no hay una consecuencia respaldada, quitar la frase. |

No convertir estas frases en moldes repetidos. En métodos importa la precisión de la operación; en resultados, qué ocurrió; en discusión, qué interpretación admite. Una misma voz puede cumplir las tres funciones sin el mismo ritmo en todos los apartados.

## Cómo evitar una escritura prefabricada

La [revisión de cuatro estudios primarios](research/writing_blueprint_2026-09-18/STYLE_RESEARCH.md) apoya prestar atención al vocabulario ornamental, las construcciones densas y los patrones repetidos, con límites importantes. No existe una lista fiable de palabras que certifique autoría ni una garantía de «indetectabilidad».

Para este proyecto:

1. Escribir desde la afirmación y su evidencia, no desde una plantilla retórica vacía.
2. Preferir “compared”, “kept”, “changed” o “excluded” cuando describen exactamente la acción. Usar el verbo técnico si aporta precisión.
3. No llamar al trabajo exhaustivo, pionero o robusto sin decir qué cobertura o comprobación justifica esa palabra.
4. No añadir conectores, resúmenes y moralejas automáticas a cada párrafo. No imponer simetría entre apartados con distinta carga de evidencia.
5. No usar sinónimos para disimular repetición si cambian el significado. “Stability” no sustituye a “validity”.
6. Introducir, si ayuda, una sola analogía breve al explicar la representación. Después volver a artículos, vectores y medidas. No llenar el manuscrito de cámaras, mapas y lupas superpuestas.
7. No inventar errores, sentimientos ni una historia de descubrimiento. No ocultar que la ampliación geométrica fue posterior.
8. Revisar en voz alta: quitar lo que Alejandro no diría por sonar impostado; conservar lo necesario para que otro investigador pueda verificarlo.

La revisión final será sobre sentido, voz y evidencia. Los detectores no serán una condición de aceptación. La asistencia utilizada se registra con fidelidad y se declarará según corresponda; esta guía no sustituye la revisión y responsabilidad del autor.

## Regla para retomar la escritura

El manuscrito completo está reescrito por petición del autor y revisado con esta guía. Leer `MANUSCRIPT_CLARITY.md` y `manuscript/main.tex` antes de modificarlo. La preparación histórica no es el estado vigente. Mantener frases directas, párrafos de distinta longitud y límites ligados a resultados concretos. No añadir fórmulas retóricas ni rellenar el presupuesto inicial de palabras.

Autoría confirmada: Alejandro Treny Ortega, investigador independiente. La voz inglesa y el texto científico esperan su lectura personal; no afirmar que ya los aprobó. El alcance no incluye nuevas investigaciones, depósito o envío por extensión.

## Historial de tres alternativas, 19-09-2026

El autor considera que el borrador necesita más identidad y pide tres versiones graduales, en inglés y español. Se mantienen título, estructura, evidencia y límites. [MANUSCRIPT_VOICES.md](MANUSCRIPT_VOICES.md) reúne los seis artículos completos y compara sus aperturas.

V1 concreta la explicación sin primera persona; V2 hace visible el razonamiento del autor con primera persona puntual; V3 abre con el problema que revela el resultado y hace más explícito su criterio interpretativo. La recomendación fue V2. **El autor la eligió el 20-09 y pidió una reescritura más clara, ahora incorporada al manuscrito canónico.**

La primera persona singular responde al autor único confirmado y permanece como propuesta de redacción para su revisión. No implica una aprobación del texto ni elimina la declaración de asistencia. La mayor personalidad no permite ampliar conclusiones, atribuir causalidad o inventar una historia de descubrimiento.
