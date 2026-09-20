"""Record the author's V2 choice and the completed clarity revision."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

def change(name, old, new):
    path = ROOT / name
    text = path.read_text()
    assert text.count(old) == 1, (name, old[:100], text.count(old))
    path.write_text(text.replace(old, new, 1))

def insert_after_title(name, text):
    path = ROOT / name
    head, rest = path.read_text().split('\n\n', 1)
    path.write_text(head + '\n\n' + text.strip() + '\n\n' + rest)

insert_after_title('AGENTS.md', '''**Estado vigente, 20-09-2026: V2 elegida y explicación reescrita.** El autor ha elegido la versión 2, pero exige una lectura mucho más clara. El artículo canónico y su copia española están reescritos; entrega en `MANUSCRIPT_CLARITY.md`. Primero explicar el problema y la comparación, después introducir su nombre técnico. Usar palabras corrientes y frases naturales, sin perder precisión. Cada muestra debe aparecer con su finalidad y su relación con las demás: 500.000 de partida; 52.000 para título/resumen/ambos, incluidos los 26.000 de la prueba inicial; esos mismos 52.000 para geometría; otros 52.000 para fragmento común. No acumular cifras o siglas sin explicar qué responden. Esta regla se aplica al manuscrito y a cualquier chat futuro. Ver `AUTHOR_VOICE.md`.

El título se conserva. Inglés: 3.989 palabras de cuerpo, resumen de 192; PDF de 19 páginas y suplemento de 34. Español: 20 y 36 páginas. Las seis alternativas del 19-09 y la edición anterior están conservadas. Cifras, figuras, archivos de datos y declaraciones no cambian; la tabla de muestras y los pies se explican mejor. La elección de voz está cerrada; la revisión personal del contenido sigue pendiente. Continuar con los comentarios del autor, sin nuevos experimentos ni envío.''')
change('AGENTS.md', '**Alternativas de voz, 19-09-2026:**', '**Historial de alternativas de voz, 19-09-2026; elección resuelta el 20-09:**')
change('AGENTS.md', 'Se recomienda V2, pero **ninguna está elegida**. Manuscrito canónico, traducción previa, cifras, figuras, tablas, declaraciones y suplemento permanecen intactos. Continuar con la elección o comentarios del autor; no sustituir automáticamente la voz canónica, reiniciar análisis ni dar el texto por aprobado.', 'En aquella entrega se recomendó V2 y se conservó el manuscrito canónico. La elección posterior y la reescritura autorizada del 20-09 sustituyen ese estado pendiente. Las seis alternativas permanecen intactas como historial; no reiniciar análisis ni dar el texto por aprobado.')
change('AGENTS.md', '**Estado vigente, 18-09-2026:**', '**Estado histórico del primer borrador, 18-09-2026:**')
change('AGENTS.md', '**Copia española solicitada después:**', '**Copia española inicial, 18-09-2026 (paginación histórica):**')

insert_after_title('AUTHOR_VOICE.md', '''**Regla prioritaria del autor, 20-09-2026.** V2 queda elegida como orientación de voz. El autor considera que incluso esa versión era demasiado densa: la identidad debe estar en el razonamiento claro, no en palabras cultas o construcciones difíciles. La reescritura vigente está en [MANUSCRIPT_CLARITY.md](MANUSCRIPT_CLARITY.md).

- Explicar primero qué queremos averiguar, qué mantenemos igual y qué cambiamos. Después dar el nombre de la medida o del procedimiento.
- Introducir cada término necesario con una explicación cotidiana. Por ejemplo, un vector es la lista de números con la que el modelo sitúa un artículo; sus vecinos son los artículos que quedan más cerca.
- Identificar las muestras por su pregunta, no solo por un número. Los 26.000 son la primera prueba del experimento de texto, incluidos en sus 52.000. El control de fragmento común usa otros 52.000. Repetir esta distinción donde cambie la comparación.
- Dar significado a los resultados antes de acumular cifras. Explicar una pareja como dos áreas que comparamos y mostrar qué significa obtener respuestas contrarias. En el resumen basta el hallazgo comprensible; los recuentos completos van después.
- Usar verbos concretos, palabras corrientes y primera persona puntual. Mantener un ritmo natural; no convertir toda la prosa en frases telegráficas, preguntas retóricas o analogías.
- Conservar cifras, alcance, citas, controles y límites. Mover una fórmula al suplemento cuando ayude, dejando su explicación y referencia en el cuerpo. Simplificar no permite atribuir corrección temática a una coincidencia entre modelos.

Estas reglas rigen en ambos idiomas y en revisiones futuras. La elección de V2 no es aprobación final del artículo.''')
change('AUTHOR_VOICE.md', '**18-09-2026. Guía de escritura para este repositorio y cualquier chat que lo retome.** El usuario pide conservar su forma de explicar, adaptada a un artículo de QSS. Esta guía prepara la redacción; no contiene un borrador del manuscrito.', '**Origen de la guía, 18-09-2026.** La lectura del portfolio que sigue documenta cómo se adaptó la voz del autor a un artículo de QSS. Se conserva como referencia; la petición directa del 20-09 tiene prioridad sobre estas observaciones.')

insert_after_title('MANUSCRIPT_VOICES.md', '''**Elección cerrada, 20-09-2026:** el autor elige **V2**, pero pide rehacer la explicación porque la lectura seguía siendo demasiado difícil. La [edición vigente, más clara](MANUSCRIPT_CLARITY.md), aplica esa orientación en inglés y español. Los seis PDF enlazados aquí son las alternativas originales del 19-09, conservadas para comparación. No son los archivos canónicos actuales.''')
change('MANUSCRIPT_VOICES.md', '**Recomiendo la segunda.**', '**Recomendación de aquella entrega: la segunda.**')
change('MANUSCRIPT_VOICES.md', 'La elección sigue pendiente.', 'La elección se resolvió después a favor de V2; la revisión personal del texto continúa pendiente.')

path = ROOT / 'NEXT_STEPS.md'
text = path.read_text()
tail = text.split('## Límites que deben acompañar las conclusiones', 1)[1]
path.write_text('''# Estado actual: V2 elegida y manuscrito reescrito con más claridad

**20-09-2026.** El autor elige la voz 2 y pide una explicación más fácil de seguir. La [entrega vigente](MANUSCRIPT_CLARITY.md) reescribe todo el artículo en inglés y español: presenta el problema antes de las medidas, explica qué pregunta responde cada muestra y hace comprensible el resumen.

Inglés: 3.989 palabras de cuerpo y 192 de resumen; 19 páginas con figuras y referencias. Español: 20 páginas. Suplementos: 34 y 36 páginas. Se mantienen el título confirmado, las cifras, las figuras, las declaraciones y los resultados científicos. Las ediciones anteriores y las seis alternativas están archivadas.

Autoría y declaraciones confirmadas: Alejandro Treny Ortega, investigador independiente, sin financiación externa ni conflictos de interés. La ayuda de Codex consta en el texto. El formato propio no es una plantilla oficial QSS. La elección de voz no equivale a aprobación del contenido completo.

## Punto exacto para continuar

1. Recoger los comentarios del autor sobre la nueva lectura, especialmente resumen, introducción y explicación de las muestras. V2 ya está elegida; no volver a pedir esa decisión. Referencias: [AUTHOR_VOICE.md](AUTHOR_VOICE.md), [MANUSCRIPT_CLARITY.md](MANUSCRIPT_CLARITY.md) y el [plano histórico de evidencia](MANUSCRIPT_BLUEPRINT.md).
2. Aplicar los cambios solicitados en ambos idiomas, conservando cifras y límites. Compilar con `./manuscript/build.sh` y `./manuscript_es/build.sh`. Las tablas principales tienen fuentes editoriales propias para que regenerarlas no recupere el texto antiguo.
3. Antes de enviar: correspondencia, aprobación personal de texto y contribuciones, normas QSS vigentes y estilo bibliográfico, según [QSS_CHECK.md](docs/QSS_CHECK.md).
4. Acordar el [depósito persistente del material esencial](docs/DATA_RELEASE.md) y la licencia. El commit/push anterior se cumplió en `44c9410`; esta revisión no incluye nueva subida, depósito ni envío. No reactivar automatizaciones ni repetir experimentos por retomar.

Los [cinco comentarios del PDF](MANUSCRIPT_COMMENTS.md), la [primera revisión editorial](MANUSCRIPT_REVIEW.md) y las [alternativas de voz](MANUSCRIPT_VOICES.md) se conservan como historial. Sus recuentos describen aquellas ediciones.

## Límites que deben acompañar las conclusiones''' + tail)

path = ROOT / 'README.md'
text = path.read_text()
start = text.index('**Estado · 19 septiembre 2026:**')
stop = text.index('\n\n', start)
text = text[:start] + '**Estado · 20 septiembre 2026:** el autor ha elegido la voz 2 y el [manuscrito se ha reescrito para explicar el estudio con más claridad](MANUSCRIPT_CLARITY.md), en inglés y español. El texto presenta cada pregunta antes de sus medidas y distingue las muestras por su finalidad. Se conservan título, resultados y versiones anteriores. Inglés: 3.989 palabras de cuerpo y 192 de resumen. La revisión personal y el depósito de datos siguen pendientes. [Estado exacto y continuación →](NEXT_STEPS.md)' + text[stop:]
text = text.replace('| Ver el artículo y suplemento | [PDF, fuentes y comando](MANUSCRIPT_LAYOUT.md) |', '| Leer el artículo y suplemento vigentes | [Reescritura clara, PDF y fuentes](MANUSCRIPT_CLARITY.md) |')
text = text.replace('| Elegir una voz con más personalidad | [Tres versiones completas, en dos idiomas](MANUSCRIPT_VOICES.md) |', '| Consultar las alternativas de voz anteriores | [Tres versiones; V2 elegida](MANUSCRIPT_VOICES.md) |')
path.write_text(text)

path = ROOT / 'docs/INDEX.md'
text = path.read_text()
start = text.index('**Última entrega de escritura')
stop = text.index('## Para entender el estudio', start)
text = text[:start] + '''**Última entrega, 20-09-2026:** [reescritura clara del artículo en inglés y español](../MANUSCRIPT_CLARITY.md). V2 está elegida. Se explica la finalidad de cada comparación y la relación entre las muestras antes de presentar resultados. La aprobación del contenido completo continúa pendiente.

La [primera revisión](../MANUSCRIPT_REVIEW.md), los [cinco comentarios resueltos](../MANUSCRIPT_COMMENTS.md) y las [seis alternativas de voz](../MANUSCRIPT_VOICES.md) se conservan como historial. Para continuar, leer [NEXT_STEPS.md](../NEXT_STEPS.md).

''' + text[stop:]
text = text.replace('48 párrafos de trabajo, títulos, dos tablas, cuatro figuras, citas, evidencia y suplemento.', 'plan histórico de párrafos, elementos, citas y evidencia; la redacción vigente está en MANUSCRIPT_CLARITY.')
text = text.replace('Pendiente de valoración personal del autor.', 'V2 elegida; la petición de claridad del 20-09 es prioritaria.')
text = text.replace('[Manuscrito completo y paquete editable](../MANUSCRIPT_LAYOUT.md)', '[Manuscrito vigente y paquete editable](../MANUSCRIPT_CLARITY.md)')
path.write_text(text)

for name in ['MANUSCRIPT_LAYOUT.md', 'MANUSCRIPT_REVIEW.md', 'MANUSCRIPT_COMMENTS.md']:
    insert_after_title(name, '''**Edición vigente, 20-09-2026:** [V2 elegida y explicación reescrita](MANUSCRIPT_CLARITY.md). Inglés: 3.989 palabras de cuerpo y resumen de 192, PDF de 19 páginas; español: 20 páginas. Suplementos: 34 y 36. El título, los resultados y las declaraciones se conservan. Las cifras de extensión y páginas que siguen pertenecen al registro histórico del 18-09; las rutas estables de PDF ahora abren la edición vigente.

## Registro histórico de esta revisión''')

insert_after_title('MANUSCRIPT_BLUEPRINT.md', '''**Redacción vigente, 20-09-2026:** [MANUSCRIPT_CLARITY.md](MANUSCRIPT_CLARITY.md). El autor ha elegido V2 y pedido una explicación más sencilla. Las seis secciones principales se conservan; sus apartados presentan ahora preguntas y hallazgos concretos. La tabla de muestras empieza por su propósito. Los detalles técnicos y sus fuentes se mantienen en el suplemento. Cuerpo inglés: 3.989 palabras, sin rellenar el presupuesto inicial. El esquema de párrafos de abajo es histórico y sirve para seguir la evidencia, no para volver a imponer aquella redacción.''')
change('MANUSCRIPT_BLUEPRINT.md', 'Las [tres alternativas de voz](MANUSCRIPT_VOICES.md) mantienen ese título y esperan elección.', 'Las [tres alternativas de voz](MANUSCRIPT_VOICES.md) mantienen ese título; el autor eligió V2 el 20-09 y pidió la reescritura clara vigente.')

path = ROOT / 'MANUSCRIPT_SPANISH.md'
text = path.read_text().replace('**18-09-2026.** Traducción completa del artículo y suplemento, con tablas, notas y rótulos de las figuras en español.', '**20-09-2026.** Versión española de la reescritura clara elegida sobre V2. Artículo y suplemento completos; mismas secciones, cifras y resultados que el inglés. [Qué ha cambiado y comprobaciones vigentes](MANUSCRIPT_CLARITY.md).')
text = text.replace('21 páginas, incluidas las referencias.', '20 páginas, incluidas las referencias.').replace('35 páginas.', '36 páginas.')
text = text.replace('La traducción inicial conservó el inglés; la revisión posterior modifica ambas versiones por petición del autor y archiva los PDF/ZIP previos.', 'La traducción inicial conservó el inglés; las revisiones posteriores modifican ambas versiones por petición del autor y archivan las ediciones previas. Evidencia de la entrega vigente: [revisión de claridad](research/manuscript_clarity_2026-09-20/closure_audit.json).')
path.write_text(text)

change('manuscript/README.md', 'El cuerpo tiene **4.383 palabras**, sin tablas, pies, citas expandidas ni declaraciones; el resumen, **190**. Principal: 19 páginas, incluidas figuras y referencias. Suplemento: 33 páginas con métodos detallados, controles y casos.', 'El cuerpo tiene **3.989 palabras**, sin tablas, pies, citas expandidas ni declaraciones; el resumen, **192**. Principal: 19 páginas, incluidas figuras y referencias. Suplemento: 34 páginas con métodos detallados, controles y casos.')
insert_after_title('manuscript/README.md', '**Edición del 20-09-2026.** El autor elige V2 y solicita una explicación mucho más clara. La nueva redacción introduce los conceptos antes de usarlos y explica la finalidad de cada muestra. El suplemento incorpora una guía de lectura. [Cambios y comprobaciones](../MANUSCRIPT_CLARITY.md).')
change('manuscript/README.md', 'El resumen está escrito y hay seis palabras clave.', 'El resumen está escrito y hay cinco palabras clave.')
insert_after_title('manuscript_es/README.md', '**Edición vigente, 20-09-2026:** V2 elegida y explicación reescrita en ambos idiomas. Guía: [MANUSCRIPT_CLARITY.md](../MANUSCRIPT_CLARITY.md). La aprobación personal del texto sigue pendiente.')
change('manuscript_es/README.md', 'Traducción completa del borrador inglés del 18-09-2026:', 'Traducción completa del borrador inglés revisado el 20-09-2026:')
change('manuscript_es/README.md', '(21 páginas).', '(20 páginas).')
change('manuscript_es/README.md', '(35 páginas).', '(36 páginas).')
for folder in ['manuscript', 'manuscript_es']:
    path = ROOT / folder / 'README.md'
    text = path.read_text()
    anchor = '## Límites que deben seguir visibles' if folder == 'manuscript' else 'Procedencia de la traducción:'
    note = '''Las dos tablas principales toman su redacción revisada de `tables/editorial/T01.tex` y `T02.tex`. Si se edita su explicación, actualizar esas fuentes y exportar; `tables/tex/` contiene las copias usadas al compilar. Los exportadores respetan estas versiones y registran su procedencia. Los CSV científicos siguen intactos. Los programas de exportación necesitan el repositorio completo; compilar los PDF desde el ZIP solo requiere las fuentes incluidas.

'''
    assert anchor in text
    text = text.replace(anchor, note + anchor, 1)
    text = text.replace('La revisión vigente de los comentarios está en', 'El historial de los comentarios está en')
    text = text.replace('Revisión vigente: `../MANUSCRIPT_COMMENTS.md`', 'Revisión actual: `../MANUSCRIPT_CLARITY.md`. Historial: `../MANUSCRIPT_COMMENTS.md`')
    path.write_text(text)

change('DECISIONS.md', 'Este es el registro principal para retomar el proyecto. Actualizado: 2026-09-17.', 'Este es el registro principal para retomar el proyecto. Actualizado: 2026-09-20.')
change('DECISIONS.md', '**Estado más reciente:** la checklist adicional también está terminada. Su cierre y sus decisiones están al final de este documento; entrega en `CHECKLIST_RESULTS.md`. Las secciones anteriores conservan la cronología, no reabren decisiones cerradas.', '**Estado más reciente:** V2 elegida por el autor y reescritura clara terminada en ambos idiomas; entrega en `MANUSCRIPT_CLARITY.md`. La elección de voz está cerrada y la aprobación personal del contenido sigue pendiente. Las secciones anteriores conservan la cronología, no reabren decisiones cerradas.')
for name in ['progress.md', 'findings.md']:
    insert_after_title(name, '**Punto vigente, 20-09-2026:** V2 elegida y reescritura clara entregada en inglés y español. Ver [MANUSCRIPT_CLARITY.md](MANUSCRIPT_CLARITY.md) y [NEXT_STEPS.md](NEXT_STEPS.md). Los bloques fechados que siguen son históricos; no reiniciar los cálculos que describían en marcha.')

print('Voice rules and current navigation updated; historical records preserved.')
