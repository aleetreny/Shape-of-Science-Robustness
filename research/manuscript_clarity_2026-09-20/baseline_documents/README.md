# Shape of Science Robustness

**¿Cuánto del mapa de la ciencia se conserva cuando cambiamos el modelo que lo dibuja?**

Comparamos los mismos artículos con diez modelos. Es como fotografiar una misma escena con cámaras distintas: buscamos qué relaciones permanecen y cuáles dependen de la cámara, del texto que recibe o de los artículos con los que se compara.

| Corpus | Modelos | Áreas principales | Experimento de entrada |
| --- | --- | --- | --- |
| 500.000 registros | 10 | 26 Fields | 52.000 × título, resumen y ambos |

**Estado · 19 septiembre 2026:** manuscrito completo y [tres alternativas de voz en inglés y español](MANUSCRIPT_VOICES.md), pendientes de elección del autor. Se conserva el título confirmado. Las alternativas tienen entre 4.250 y 4.462 palabras de cuerpo en inglés y mantienen las dos tablas, cuatro figuras y el suplemento común. [Artículo anterior, suplemento y fuentes](MANUSCRIPT_LAYOUT.md) · [Revisión previa](MANUSCRIPT_REVIEW.md) · [Cinco comentarios resueltos](MANUSCRIPT_COMMENTS.md). La aprobación personal y el depósito de datos siguen pendientes. [Estado exacto y continuación →](NEXT_STEPS.md)

## Empieza aquí

| Para… | Abrir |
| --- | --- |
| Entender qué sabemos y qué límites quedan | [Revisión antes del paper](PREPAPER_REVIEW.md) |
| Leer los resultados generales | [Resultados](ROBUSTNESS_RESULTS.md) · [Qué resiste a los controles](CONCLUSION_CONTROLS.md) |
| Ver cuántas conclusiones cambian de dirección | [Resumen de las 325 parejas](FIELD_PAIR_RESULTS.md) · [Métodos](METHODS_FIELD_PAIRS.md) |
| Entender qué rasgos de la forma cambian | [Piloto de morfología](MORPHOLOGY_RESULTS.md) · [Métodos y controles](METHODS_MORPHOLOGY.md) |
| Ver artículos y relaciones concretas | [Atlas de casos](CASE_ATLAS.md) |
| Comparar con otros trabajos | [Antecedentes y aportación](references/RELATED_WORK.md) · [54 referencias verificadas](references/README.md) |
| Revisar métodos y repetir comprobaciones | [Guía de reproducción](docs/REPRODUCING.md) · [Catálogo de datos](DATA_CATALOG.md) |
| Ver el artículo y suplemento | [PDF, fuentes y comando](MANUSCRIPT_LAYOUT.md) |
| Elegir una voz con más personalidad | [Tres versiones completas, en dos idiomas](MANUSCRIPT_VOICES.md) |
| Revisar el texto en español | [Artículo y suplemento traducidos](MANUSCRIPT_SPANISH.md) |
| Revisar la redacción | [Plano detallado del manuscrito](MANUSCRIPT_BLUEPRINT.md) · [Voz del autor](AUTHOR_VOICE.md) · [Estructuras de QSS](QSS_STRUCTURE_REVIEW.md) · [Qué falta antes de enviar](docs/QSS_CHECK.md) |

## Qué estamos encontrando

Hay una organización amplia compartida, pero los vecinos de cada artículo dependen del modelo y del texto. Acercar la lupa no reduce siempre el acuerdo. El tamaño de búsqueda y la forma de resumir el texto pueden cambiar la interpretación.

El resumen de todas las parejas encuentra direcciones opuestas persistentes en 262/325 comparaciones de apertura y 221/325 de reparto entre direcciones. Al exigir diferencias superiores al 5%, quedan 96 y 177: la magnitud debe acompañar a la dirección. Acuerdo de todos, contradicción y casos no resueltos permanecen visibles. [Resumen final →](FIELD_PAIR_RESULTS.md) · [Piloto y límites de fragmentación →](MORPHOLOGY_RESULTS.md)

El atlas localiza especialidades que conservan posiciones altas o bajas al cambiar 27 condiciones. También permite seguir una relación concreta modelo por modelo.

![Especialidades que mantienen posiciones altas o bajas de acuerdo](reports/prepaper_v1/figures/01_subfield_persistence.png)

**Acuerdo no significa verdad.** La revisión encontró avisos bibliográficos y etiquetas temáticas erróneas que proceden de OpenAlex. Se conservan y explican en [la auditoría](PREPAPER_REVIEW.md). Los resultados describen este corpus y estos modelos, no toda la ciencia ni un encoder ganador.

## Cómo está organizado

- `config/`: decisiones y versiones de cada cálculo.
- `sos_download/`, `sos_prepare/`, `sos_embed/`: extracción, limpieza y modelos ya terminados.
- `sos_analysis/`, `sos_followup/`, `sos_deep/`: análisis y controles de las fases conservadas.
- `sos_review/`: atlas y presentación de esta revisión.
- `sos_morphology/`: piloto separado de propiedades de la forma y sus controles.
- `sos_pair_summary/`: resumen final de las 325 parejas, a partir de medidas ya guardadas.
- `reports/`: tablas, figuras y entregas científicas conservadas.
- `manuscript/`: manuscrito LaTeX, figuras y tablas del paper; `output/`: PDF y paquete editable.
- `references/`: biblioteca y comparación con antecedentes.
- `research/`: registros y evidencia de las revisiones; copias de consulta locales fuera de Git.
- `data/`: corpus, vectores y grandes derivados locales, fuera de Git.

[Índice completo de documentos y versiones →](docs/INDEX.md)

Los 400.000 registros de base y los 100.000 de complemento permanecen separados. El control de fragmento común y el experimento de tres entradas tienen selecciones propias de 52.000. Los resultados se calculan en los espacios originales; un dibujo en dos dimensiones no decide las conclusiones.

Un clon del repositorio permite leer la entrega y ejecutar pruebas pequeñas. Repetir todo el estudio requiere los datos locales, todavía sin depósito público permanente: [plan de disponibilidad](docs/DATA_RELEASE.md). No relanzar descargas o modelos por abrir el proyecto.

Para continuar entre personas o chats: [AGENTS.md](AGENTS.md), [DECISIONS.md](DECISIONS.md), [progress.md](progress.md) y [task_plan.md](task_plan.md). El TFM anterior se mantiene como referencia de solo lectura.
