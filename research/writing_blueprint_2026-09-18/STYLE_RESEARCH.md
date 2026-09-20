# Escritura natural: evidencia y aplicación al proyecto

18-09-2026. Revisión dirigida para preparar la escritura, no un estudio de detección de autoría. Se buscaron estudios sobre lenguaje científico generado, variación del estilo y límites de los detectores. Se consultaron métodos, resultados y limitaciones de cuatro fuentes primarias. No es una revisión sistemática ni una lista universal de «señales de IA».

## Qué aportan los estudios

| Fuente primaria y versión leída | Hallazgo pertinente | Límite y aplicación editorial propia |
| --- | --- | --- |
| Kobak, González-Márquez, Horvát y Lause (2025), [Science Advances](https://doi.org/10.1126/sciadv.adt3813); texto de autor [arXiv v5](https://arxiv.org/html/2406.07016v5), resultados y discusión | En resúmenes biomédicos aparecen aumentos bruscos de vocabulario de estilo tras la llegada de los asistentes. Los autores separan palabras de contenido y palabras ornamentales. | Es una comparación de corpus: no identifica qué resumen individual recibió ayuda. Tampoco separa todos los motivos de un cambio de vocabulario. Aplicación: revisar adjetivos de autoelogio y verbos adornados cuando no añaden significado; no prohibir palabras comunes por asociación estadística. |
| Bagdasarov y Alves (2025), [ACL Anthology](https://aclanthology.org/2025.lm4dh-1.4/), PDF editorial, §§3, 5–7 y Limitations | Comparan resúmenes de lingüística computacional con versiones de GPT-4o, Llama 3.1 y Qwen 2.5. Observan menos variación sintáctica y más acumulación de modificadores nominales en los textos generados. La diversidad de vocabulario no es necesariamente menor. | Depende del modelo, tarea, idioma y prompt. Los modelos reciben el artículo completo para generar el resumen. Aplicación: preferir sujeto y verbo claros frente a cadenas de nombres; no forzar sinónimos ni imponer una longitud de frase supuestamente humana. |
| Tripto, Venkatraman, Nahar y Lee (2025), [EMNLP](https://aclanthology.org/2025.emnlp-main.600/), PDF editorial, §§3–6 y Limitations | En noticias, correos y ensayos, comparan introducción, cuerpo y cierre. Encuentran diferencias de variación entre segmentos; controlar su longitud cambia varios resultados y elimina algunas diferencias. | Tres géneros, cuatro modelos y segmentación discutible; no demuestra cómo debe escribirse un paper de QSS. Aplicación: dejar que cada sección cumpla su función, sin obligar a todos los párrafos a la misma secuencia de presentación, lista y conclusión. |
| Liang, Yuksekgonul, Mao, Wu y Zou (2023), [Patterns](https://doi.org/10.1016/j.patter.2023.100779); texto de autor [arXiv v3](https://arxiv.org/abs/2304.02819v3), resultados y discusión | Los detectores evaluados confundieron con frecuencia ensayos de hablantes no nativos con textos generados. También examinan diferencias de lenguaje en resúmenes académicos. | Muestras y herramientas de 2023; no es una evaluación de todos los detectores actuales. Aplicación: no usar una puntuación de detección para aceptar/rechazar nuestra prosa ni sacrificar un inglés sencillo para satisfacerla. |

Estas aplicaciones son decisiones de edición, no resultados experimentales de esos trabajos. Ninguna fuente prueba que «usar tres elementos», un guion largo o una transición concreta identifique autoría. Tampoco prueba que eliminar esos rasgos garantice una percepción determinada.

## Qué revisaremos al escribir

1. **Frases intercambiables.** Si un párrafo sirve para cualquier artículo cambiando dos nombres, concretar qué problema, observación o decisión describe.
2. **Importancia proclamada.** Sustituir «comprehensive», «groundbreaking» o «robust insights» cuando solo elogian el estudio por la comparación y el control que realmente se hicieron. No es una lista de palabras prohibidas.
3. **Densidad innecesaria.** Deshacer cadenas de sustantivos si ocultan quién hace qué. Conservar el término técnico preciso cuando es necesario.
4. **Ritmo de plantilla.** No terminar cada párrafo con la misma moraleja ni anunciar cada paso con un conector. La relación entre frases debe bastar cuando ya es clara.
5. **Sinónimos que cambian el objeto.** No alternar indiscriminadamente agreement, validity, stability y accuracy. Repetir el término correcto es preferible a aparentar variedad.
6. **Cautela vacía.** Reemplazar cadenas de “may potentially suggest” por una afirmación acotada y su límite concreto. Tampoco convertir una asociación en causa.
7. **Cercanía impostada.** No inventar experiencias, emociones, dudas previas o descubrimientos accidentales. No introducir faltas deliberadas para simular espontaneidad.

La guía positiva procede de [la voz del autor](../../AUTHOR_VOICE.md), no de perseguir una puntuación de «humanidad». El texto debe ser claro, reconocible para el autor y comprobable. La edición no cambia el registro real de herramientas utilizadas ni las declaraciones que correspondan al enviar.

## Procedencia

- Consulta: 18-09-2026. Búsquedas por escritura científica generada, variación léxica/sintáctica y sesgo de detectores; se descartaron consejos de redes sociales y páginas comerciales como evidencia.
- Lecturas completas descargadas solo para consulta en `data/writing_blueprint_v1/literature/`, excluido de Git. No se copian al material publicable.
- [BibTeX](writing_research.bib): cuatro referencias. Metadatos de DOI para Science Advances/Patterns y BibTeX oficial de ACL para los otros dos. Colección de trabajo editorial; no se añade automáticamente a las 54 referencias científicas del estudio.
- Se completó el identificador de artículo `eadt3813` de Kobak desde Crossref y el DOI de Bagdasarov desde su PDF editorial, confirmado por Crossref con título/páginas coincidentes. No se dedujeron del nombre de archivo. La validación final no tiene errores, duplicados ni avisos.
- Los trabajos sobre escritura no tienen por qué citarse en el paper sobre mapas: fundamentan nuestra manera de preparar el texto, no sus resultados científicos.
