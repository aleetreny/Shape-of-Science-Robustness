"""Record the completed closure without rewriting historical scientific reports."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
audit = json.loads((HERE / 'text_audit.json').read_text())
docs = audit['documents']
en, es = docs['en_main'], docs['es_main']
pages = sum(x['pages'] for x in docs.values())

def read(name):
    return (ROOT / name).read_text()

def write(name, text):
    (ROOT / name).write_text(text)

def prepend(name, paragraph):
    title, rest = read(name).split('\n', 1)
    write(name, title + '\n\n' + paragraph + '\n' + rest)

status = ('**Cierre vigente, 20-09-2026:** controles finales terminados y congelados; '
          '[informe para el autor](ROBUSTNESS_CLOSURE_REPORT.md) y '
          '[cambios del manuscrito](ROBUSTNESS_MANUSCRIPT_CHANGELOG.md). '
          'El tono claro está aceptado. La revisión personal del contenido sigue pendiente.')

s = read('AGENTS.md')
old = next(p for p in s.split('\n\n') if p.startswith('**Encargo vigente, 20-09-2026:'))
new = '''**Cierre vigente, 20-09-2026:** la revisión de robustez delegada está terminada. Leer `ROBUSTNESS_CLOSURE_REPORT.md`, `ROBUSTNESS_MANUSCRIPT_CHANGELOG.md` y `NEXT_STEPS.md`. Centros, contraste directo de vecinos, centrado completo, alternativas de dimensión y calidad están congelados en `data/robustness_closure_v1/`; resúmenes en `reports/robustness_closure_v1/`. Se actualizaron ambos idiomas después de congelar resultados. No repetir análisis por retomar. Las fuentes de `sos_closure/`, su configuración y protocolo son inmutables para esta versión.

**Límites que sustituyen resúmenes parciales anteriores:** apertura: 262 oposiciones originales frente a 151 tras centrar, con 128 que conservan los mismos modelos y direcciones; PR: 221 frente a 211, con 204 conservadas. Al 5 %, apertura pasa de 96 a 11. Las dos alternativas de dimensión cubren ahora 26 condiciones y conservan 190/221 oposiciones originales de PR, no las 196 del control histórico parcial. Las medias del contraste texto/modelo se repiten, pero hay respuestas opuestas por modelo y receta; no afirmar equivalencia. El filtro de calidad apenas cambia el acuerdo local agregado. Mantener visibles las 2.628/8.235 alertas locales. Estos controles no son intervalos poblacionales ni validación temática.

**Tono aceptado expresamente:** «me gusta este tono mucho, conservalo». Mantener la explicación clara sobre V2 en los dos idiomas, sin volver al registro denso ni reabrir la elección de voz. La aprobación del contenido completo, correspondencia, depósito/licencia y envío siguen pendientes. Esta entrega no incluye commit/push, descarga, inferencia o automatización nueva.'''
write('AGENTS.md', s.replace(old, new, 1))

s = read('DECISIONS.md')
old = next(p for p in s.split('\n\n') if p.startswith('**Estado más reciente'))
write('DECISIONS.md', s.replace(old, status, 1) + '''

## 20-09-2026 — Cierre delegado de robustez terminado

- El autor acepta el tono claro y delega aplicar la lista de un agente independiente. Alcance en `ROBUSTNESS_CLOSURE_SCOPE.md`; petición original conservada. No se transforma esa delegación en permiso permanente para nuevas ampliaciones.
- Diseño fijado antes de los nuevos resultados: cincuenta selecciones de centros, tamaños 128/256/512 y referencias emparejadas; cincuenta elecciones de especialidad con diez selecciones internas; omisión de áreas. Se explicita la normalización final de los centros que ya hacía el código. La referencia aleatoria restringida nueva usa exactamente los artículos observados; la antigua mezclaba el conjunto de 217 especialidades.
- Vecinos de entrada: cincuenta selecciones de 1.000 candidatos por área; k10/25/50 y CLS/SEP en k25. Conservados los resultados originales de 2.000 candidatos. Centrado y dos alternativas de dimensión sobre las 26 condiciones existentes, sin cambiar cortes o modelos.
- Calidad: misma regla estricta de siete marcas y componentes de duplicados, 448.886 conservados. Controles de 1.024 candidatos en las 130 celdas porque solo 63 conservan 2.048; consultas idénticas antes/después. La elección preserva cobertura sin fingir que las celdas pequeñas permiten el tamaño mayor.
- El resultado de centros se refuerza. Se matizan materialmente apertura y la generalización de la media texto/modelo. La comprobación completa sustituye 196 por 190 en la conservación de oposiciones PR bajo ambas alternativas. No se cambian datos para sostener la historia.
- Todas las ramas congeladas antes de escribir; auditoría de once afirmaciones; manuscrito y suplemento sincronizados; fuentes y resultados históricos conservados. Preparación metodológica: READY WITH MINOR CAVEATS, sin predecir aceptación y sin dar por resueltos los trámites de envío.
- Continuación: lectura personal y decisiones de publicación pendientes. No añadir otros experimentos por rutina. Evidencia y entregables en `ROBUSTNESS_CLOSURE_REPORT.md`.
''')

s = read('task_plan.md')
tail = s.split('\n---\n', 1)[1]
write('task_plan.md', f'''# Tarea terminada: último cierre de robustez, 20-09-2026

Alcance delegado: `ROBUSTNESS_CLOSURE_SCOPE.md`. Tono claro aceptado. Entrega: `ROBUSTNESS_CLOSURE_REPORT.md` y `ROBUSTNESS_MANUSCRIPT_CHANGELOG.md`.

1. Auditoría previa y protocolo reproducible: **complete**.
2. Centros, tamaños, referencias y omisiones; contraste directo modelo/entrada: **complete**.
3. Centrado global y alternativas completas; calidad y vecinos: **complete**.
4. Auditoría de once afirmaciones y congelación numérica: **complete**.
5. Ambos idiomas, figuras, informes, cuatro PDF y paquetes reproducibles: **complete**. {pages} páginas revisadas; 22 grupos de tablas y 15 figuras. Inglés: {en['body_words']:,} palabras de cuerpo y {en['abstract_words']} de resumen.

No quedan cálculos activos. Los originales están archivados, los programas científicos sellados y las automatizaciones siguen pausadas. Continuar con la lectura personal del autor; no repetir pruebas ni publicar por retomar.

---
''' + tail)

prepend('progress.md', status)
write('progress.md', read('progress.md') + f'''

## 20-09-2026 — Cierre final de robustez entregado

- Cinco bloques de análisis derivados en `sos_closure/` y `data/robustness_closure_v1/`; 25 tablas CSV finales, catálogo y resumen. No hubo nuevas descargas ni inferencia. Semillas, selecciones, versiones y huellas conservadas.
- Auditoría numérica independiente: 78.000 direcciones, 900 selecciones de centros/referencias, medias originales de vecinos reproducidas; 446 archivos científicos anteriores y 452 copias archivadas intactos.
- Actualizados `manuscript/` y `manuscript_es/`, Figura 1A, Figura 4, Tabla S15, S9 y Tablas S18–S20; añadida Figura S11. Exportadores completos comprobados. Declaraciones, bibliografía, título y voz conservados.
- Revisadas {pages} páginas: inglés {en['pages']} + {docs['en_supplement']['pages']}; español {es['pages']} + {docs['es_supplement']['pages']}. {audit['csv_files_bilingually_identical']} CSV idénticos entre idiomas; tablas, cifras, citas y fórmulas contrastadas. Paquetes ZIP extraídos reconstruyen los cuatro PDF exactamente.
- Informe para el autor y registro de cambios explican qué se refuerza y qué se limita. Evidencia en `research/robustness_closure_2026-09-20/closure_audit.json`.
- Siguiente paso exacto: lectura personal, correspondencia y depósito/licencia del material antes de autorizar el envío. No hay experimento adicional pendiente dentro de este encargo. Sin commit/push, depósito, envío o automatización.
''')
prepend('findings.md', status)
write('findings.md', read('findings.md') + '''

## Cierre de robustez del 20-09-2026

- Centros: acuerdo medio 0,940/0,911/0,904, estable frente a selección/tamaño/omisión; las distribuciones de medias aleatorias quedan separadas. El control restringido separa elección de especialidades de elección de artículos.
- Texto/modelo: diferencias medias principales +1,97/+1,56/+1,04 puntos en k10/25/50; CLS/SEP invierten el orden. Diferencias por modelo −14,04 a +16,59 puntos. No equivalencia universal.
- Centrado: apertura 262→151 (mismos modelos/direcciones 128); PR 221→211 (204). El efecto de apertura es fuerte, sobre todo con mínimo 5 %: 96→11. Este límite está en el cuerpo y en la Figura 4.
- Alternativas completas: entropía retiene 209 oposiciones PR, D80 y ambas 190/221. Solo cinco de 54 acuerdos de los diez mantienen su dirección bajo ambas; no declarar equivalencia entre medidas. Empates sin resolver.
- Calidad: 30,58→31,43 % de acuerdo k25 con las mismas consultas; +0,28/+0,19 puntos con 1.024/2.048 candidatos. El filtro probado no explica la mayor parte del desacuerdo ni certifica toda la fuente.
- Las 2.628/8.235 alertas locales siguen visibles. Rangos de selecciones solapadas no son intervalos poblacionales. Ver el informe y sus CSV para definiciones, denominadores y límites completos.
''')

write('NEXT_STEPS.md', f'''# Estado actual: cierre final de robustez terminado

**20-09-2026.** El autor ha aceptado el tono claro. Las pruebas que delegó están terminadas y se han integrado en los dos idiomas. [Informe sencillo](ROBUSTNESS_CLOSURE_REPORT.md) · [Cambios del texto](ROBUSTNESS_MANUSCRIPT_CHANGELOG.md).

Inglés: {en['body_words']:,} palabras de cuerpo y {en['abstract_words']} de resumen; {en['pages']} páginas. Español: {es['pages']} páginas. Suplementos: {docs['en_supplement']['pages']} y {docs['es_supplement']['pages']}. El título, autor y declaraciones se conservan. El formato es propio, no una plantilla oficial QSS.

## Punto exacto para continuar

1. Lectura personal del autor y comentarios al texto. La voz ya está elegida y aceptada; no volver a preguntar por V1/V2/V3. Mantener `AUTHOR_VOICE.md`.
2. Aplicar comentarios en ambos idiomas. Compilar con `./manuscript/build.sh` y `./manuscript_es/build.sh`. Los exportadores conservan las tablas editoriales y añaden los resultados de este cierre.
3. Antes de enviar: correspondencia, aprobación final de texto/contribuciones y revisión actual de normas y referencias. Ver [lista de envío](docs/QSS_CHECK.md).
4. Acordar [depósito del material esencial](docs/DATA_RELEASE.md) y licencia. La reproducción local está comprobada; no afirmar que el clon público reproduce los experimentos. El commit/push anterior se cumplió en `44c9410`; este cierre no incluye nueva subida, depósito ni envío.

No queda otra prueba necesaria dentro del encargo. No reiniciar extracción, embeddings, análisis terminados o automatizaciones. Cualquier ampliación futura debe responder a un problema nuevo concreto.

## Qué queda respaldado y qué hay que matizar

- La organización entre centros se conserva al cambiar artículos, tamaño y omitir cada área. La receta incluye normalizar el centro tras promediar.
- El desacuerdo de vecinos sigue siendo grande tras el filtro conocido de calidad/duplicados. Ese filtro no detecta todo error de origen.
- Texto y modelo producen cambios medios grandes, pero la comparación difiere por modelo y regla de combinación. No hablar de equivalencia ni de un orden universal.
- Apertura: 262 oposiciones originales y 151 tras centrar; 128 conservan los mismos modelos y respuestas. Con mínimo 5 %, 96→11. PR cambia menos: 221→211, con 204 conservadas.
- Las alternativas de dimensión cubren ahora las 26 condiciones; ambas retienen 190/221 oposiciones originales de PR. El 196 de tres condiciones y los controles puntuales 145/262 y 218/221 son históricos, no la comprobación completa actual.
- Persisten 2.628/8.235 alertas locales de especialidades, las 50 originales, cinco de entrada a 52k, cuatro de PR y 51 de conexión, cada una con su diseño y denominador. Una media estable no elimina ninguna.
- Los 500k, diez modelos, restricciones de idioma/abstract y etiquetas OpenAlex delimitan el estudio. Las selecciones solapadas no permiten precisión poblacional; consenso no es verdad temática; familias, Medicina y tiempo no identifican causas.
- Se conservan los errores ilustrativos de OpenAlex y los límites de los conjuntos de candidatos. No borrar ejemplos o cambiar umbrales para mejorar el relato.

## Dónde está cada entrega

| Material | Ubicación |
| --- | --- |
| Informe y cambios del cierre actual | `ROBUSTNESS_CLOSURE_REPORT.md`, `ROBUSTNESS_MANUSCRIPT_CHANGELOG.md` |
| Protocolo, código y configuración sellados | `ROBUSTNESS_CLOSURE_PROTOCOL.md`, `sos_closure/`, `config/robustness_closure_v1.json` |
| Selecciones, centros, búsquedas y huellas locales | `data/robustness_closure_v1/` |
| 25 tablas y resumen del cierre | `reports/robustness_closure_v1/` |
| Auditoría y copias anteriores | `research/robustness_closure_2026-09-20/` |
| Artículo/suplemento; 22 grupos de tablas, 15 figuras | `manuscript/`, `manuscript_es/`, `output/` |
| Resultados científicos anteriores | `ROBUSTNESS_RESULTS.md`, `FIELD_PAIR_RESULTS.md`, `MORPHOLOGY_RESULTS.md`, `CASE_ATLAS.md` |
| Historial de redacción y voz | `MANUSCRIPT_CLARITY.md`, `MANUSCRIPT_VOICES.md` |

Datos grandes y pesos siguen locales y fuera de Git. No modificar una fuente científica congelada y reanudar como si fuera la misma versión. [Reproducción](docs/REPRODUCING.md) · [Catálogo](DATA_CATALOG.md).
'''.replace(f"{en['body_words']:,}", f"{en['body_words']:,}".replace(',', '.')))

s = read('README.md')
old = next(p for p in s.split('\n\n') if p.startswith('**Estado ·'))
new = f'''**Estado · 20 septiembre 2026:** [cierre final de robustez completado](ROBUSTNESS_CLOSURE_REPORT.md) e integrado en inglés y español. La organización general se sostiene; la apertura requiere un matiz importante sobre cómo preparamos los vectores. El tono claro está aceptado. Inglés: {en['body_words']:,} palabras de cuerpo y {en['abstract_words']} de resumen. Revisión personal y depósito de datos pendientes. [Estado exacto →](NEXT_STEPS.md)'''.replace(f"{en['body_words']:,}", f"{en['body_words']:,}".replace(',', '.'))
s = s.replace(old, new, 1).replace('| Entender qué sabemos y qué límites quedan | [Revisión antes del paper](PREPAPER_REVIEW.md) |', '| Entender qué cambia tras las últimas pruebas | [Informe del cierre](ROBUSTNESS_CLOSURE_REPORT.md) · [Cambios del texto](ROBUSTNESS_MANUSCRIPT_CHANGELOG.md) |')
s = s.replace('[Reescritura clara, PDF y fuentes](MANUSCRIPT_CLARITY.md)', '[Cierre actual, PDF y fuentes](ROBUSTNESS_CLOSURE_REPORT.md)')
old = next(p for p in s.split('\n\n') if p.startswith('El resumen de todas las parejas'))
s = s.replace(old, 'En la representación original, dos modelos dan respuestas opuestas persistentes en 262 de 325 comparaciones de apertura y 221 de dimensión. Al cambiar la referencia global, quedan 151 y 211; solo 128 y 204 conservan los mismos modelos y respuestas originales. La apertura depende mucho de esa preparación: al exigir diferencias mayores del 5 %, sus oposiciones pasan de 96 a 11. El texto recoge este límite, sin declarar una preparación como la correcta. [Resultados y significado →](ROBUSTNESS_CLOSURE_REPORT.md)')
write('README.md', s)

s = read('docs/INDEX.md')
old = next(p for p in s.split('\n\n') if p.startswith('**Última entrega'))
s = s.replace(old, status.replace('](ROBUSTNESS_', '](../ROBUSTNESS_'), 1)
write('docs/INDEX.md', s + '\n\n## Cierre final de robustez, 20-09-2026\n\n[Informe del autor](../ROBUSTNESS_CLOSURE_REPORT.md) · [Cambios del texto](../ROBUSTNESS_MANUSCRIPT_CHANGELOG.md) · [Protocolo](../ROBUSTNESS_CLOSURE_PROTOCOL.md) · [Auditoría de once afirmaciones](../research/robustness_closure_2026-09-20/CLAIM_AUDIT.md). Las cifras actuales sobre centrado y alternativas sustituyen los controles parciales anteriores, que siguen conservados como historial.\n')
prepend('DATA_CATALOG.md', status + '\n\nEl cierre anterior de parejas se conserva como historial. Para la cobertura completa de centrado y alternativas, usar las rutas nuevas al final.')
write('DATA_CATALOG.md', read('DATA_CATALOG.md') + '''

## Cierre final de robustez, 20-09-2026

| Material | Ruta | Contenido |
| --- | --- | --- |
| Resultados completos | `data/robustness_closure_v1/{centres,headline,morphology,quality}/` | Selecciones, índices, vectores de centros, búsquedas y resultados por condición; fuentes/configuración y huellas. |
| Congelación de ramas | `data/robustness_closure_v1/summary/` | Manifiesto que enlaza las ramas completas; auditoría. |
| Entrega ligera | `reports/robustness_closure_v1/` | 25 CSV, `summary.json` y catálogo de huellas. |
| Semillas y entorno | `research/robustness_closure_2026-09-20/random_seeds.csv`, `execution_environment.json` | 190.884 pares de etiqueta y semilla; versiones y plataforma. |
| Revisión numérica y editorial | `research/robustness_closure_2026-09-20/` | Auditoría previa, once afirmaciones, controles independientes, PDF y paquetes. |

No se movieron corpus o embeddings. Las fuentes y los resultados nuevos están congelados; las figuras y tablas tipográficas son derivados separados de presentación. El ZIP del manuscrito reproduce los documentos, no todos los experimentos.
''')
write('docs/REPRODUCING.md', read('docs/REPRODUCING.md') + '''

## Cierre final de robustez del 20-09-2026

Las cuatro ramas están terminadas y congeladas. No ejecutarlas por continuar el proyecto. `data/robustness_closure_v1/summary/manifest.json` enlaza sus auditorías y `reports/robustness_closure_v1/catalog.json` identifica las tablas finales. El protocolo y la configuración registran selecciones, cortes y recetas; las copias de código/entorno y el registro de semillas están conservados.

Para reconstruir solo los cuatro PDF:

```sh
./manuscript/build.sh
./manuscript_es/build.sh
```

Para regenerar la presentación completa con el repositorio local, seguir los README de `manuscript/` y `manuscript_es/`. Los exportadores aplican al final los resultados del cierre y conservan la redacción editorial de las tablas principales. No ejecutan inferencia ni pruebas científicas. Los ZIP extraídos reconstruyen exactamente los PDF; no se ha probado carga remota en Overleaf ni se ha publicado el corpus.

La evidencia de entrega está en `research/robustness_closure_2026-09-20/closure_audit.json`. Los controles independientes verifican operaciones y correspondencias; no son una validación experta externa ni una demostración de precisión poblacional.
''')
prepend('AUTHOR_VOICE.md', '**Aceptación expresa, 20-09-2026:** «me gusta este tono mucho, conservalo». El cierre de robustez conserva esa voz clara en ambos idiomas. Las nuevas pruebas cambian algunos límites de las conclusiones, no el modo de explicar. La elección de tono está cerrada; no equivale a aprobación final del contenido.')

s = read('MANUSCRIPT_CLARITY.md')
s = s.replace('Esta es la edición vigente del artículo en inglés y español.', 'Este registro describe la edición anterior al último cierre de robustez.')
# Link the historical page counts to the preserved files, not the new PDFs.
archive = 'research/robustness_closure_2026-09-20/baseline_documents/'
s = s.replace('](output/', '](' + archive + 'output/')
write('MANUSCRIPT_CLARITY.md', s)
prepend('MANUSCRIPT_CLARITY.md', '**Registro histórico de la reescritura.** El autor ha aceptado este tono. Los archivos actuales incorporan después el [cierre de robustez](ROBUSTNESS_CLOSURE_REPORT.md); los recuentos inferiores y sus enlaces corresponden a la copia anterior conservada.')
write('MANUSCRIPT_SPANISH.md', f'''# Manuscrito en español para revisión personal

**20-09-2026.** El cierre final de robustez está integrado con el tono claro aceptado. Misma estructura, cifras, conclusiones, referencias y límites que el inglés. [Informe de resultados](ROBUSTNESS_CLOSURE_REPORT.md) · [Cambios](ROBUSTNESS_MANUSCRIPT_CHANGELOG.md).

- [Artículo](output/pdf/es/main.pdf): {es['pages']} páginas, {es['body_words']:,} palabras de cuerpo y {es['abstract_words']} de resumen.
- [Suplemento](output/pdf/es/supplement.pdf): {docs['es_supplement']['pages']} páginas; incorpora S9 y las nuevas tablas/figura.
- [Paquete editable](output/manuscript_source_es.zip): fuentes, figuras y CSV.

Los cuatro PDF se han inspeccionado y los paquetes extraídos los reconstruyen exactamente. Las tablas y los CSV conservan las mismas cifras; la presentación española usa coma decimal. Evidencia: `research/robustness_closure_2026-09-20/`.

El inglés sigue siendo el manuscrito de referencia. Las correcciones se mantienen sincronizadas; la traducción no supone aprobación final. Las ediciones anteriores y seis alternativas se conservan. Continuación: [NEXT_STEPS.md](NEXT_STEPS.md).
'''.replace(f"{es['body_words']:,}", f"{es['body_words']:,}".replace(',', '.')))

s = read('docs/QSS_CHECK.md').replace('[entrega](../MANUSCRIPT_LAYOUT.md). Resumen de 190 palabras; cuerpo de 4.383', '[cierre actual](../ROBUSTNESS_CLOSURE_REPORT.md). Resumen de 192 palabras; cuerpo de 4.570').replace('14 figuras en PDF/SVG/PNG/TIFF; 19 grupos', '15 figuras en PDF/SVG/PNG/TIFF; 22 grupos')
write('docs/QSS_CHECK.md', s)
prepend('docs/QSS_CHECK.md', '**20-09-2026:** cierre metodológico terminado, con límites incorporados al manuscrito. Estado: READY WITH MINOR CAVEATS; no es aprobación editorial ni autorización de envío. Las normas externas descritas abajo no se han vuelto a comprobar en esta fase.')

for folder, lang in [('manuscript', 'en'), ('manuscript_es', 'es')]:
    s = read(folder + '/README.md')
    s = s.replace('3.989', '4.570').replace('192**', '192**')
    s = s.replace('Principal: 19 páginas', 'Principal: 20 páginas').replace('Suplemento: 34 páginas', 'Suplemento: 39 páginas')
    s = s.replace('| Suplemento | 17 grupos | 10 |', '| Suplemento | 20 grupos | 11 |')
    s = s.replace('a `S17/`', 'a `S20/`').replace('de las 14 figuras', 'de las 15 figuras')
    s = s.replace('(20 páginas)', f"({es['pages']} páginas)").replace('(36 páginas)', f"({docs['es_supplement']['pages']} páginas)")
    s = s.replace('No es un resumen ni una nueva versión de los resultados.', 'Es la traducción de los resultados actualizados después del cierre de robustez; no es un resumen.')
    paragraph = ('**Cierre posterior del 20-09-2026:** pruebas finales integradas; [informe](../ROBUSTNESS_CLOSURE_REPORT.md) y [cambios](../ROBUSTNESS_MANUSCRIPT_CHANGELOG.md). '
                 'Se conserva el tono claro aceptado. Dos tablas y cuatro figuras principales; veinte grupos de tablas y once figuras suplementarias. '
                 'Los manifiestos de presentación identifican los CSV usados actualmente; otros CSV conservados documentan la procedencia histórica. '
                 'Revisión personal del autor pendiente.')
    title, rest = s.split('\n', 1)
    write(folder + '/README.md', title + '\n\n' + paragraph + '\n' + rest)

write('ROBUSTNESS_CLOSURE_REPORT.md', read('ROBUSTNESS_CLOSURE_REPORT.md') + f'''

## Documentos y comprobación de entrega

| Documento | Español | Inglés |
| --- | --- | --- |
| Artículo | [PDF, {es['pages']} páginas](output/pdf/es/main.pdf) | [PDF, {en['pages']} páginas](output/pdf/main.pdf) |
| Suplemento | [PDF, {docs['es_supplement']['pages']} páginas](output/pdf/es/supplement.pdf) | [PDF, {docs['en_supplement']['pages']} páginas](output/pdf/supplement.pdf) |
| Fuentes editables | [ZIP español](output/manuscript_source_es.zip) | [ZIP inglés](output/manuscript_source.zip) |

Se han inspeccionado las {pages} páginas y comprobado 22 grupos de tablas, 15 figuras y {audit['csv_files_bilingually_identical']} CSV idénticos entre idiomas. El cuerpo inglés tiene {en['body_words']:,} palabras y el resumen {en['abstract_words']}; los detalles nuevos quedan sobre todo en S9. Los dos ZIP extraídos reconstruyen exactamente los cuatro PDF. La tipografía bibliográfica usa interlineado normal para evitar una última página casi vacía.

El título y las declaraciones no cambian. Los documentos actuales están revisados, pero siguen pendientes de tu aprobación personal. La [auditoría final](research/robustness_closure_2026-09-20/closure_audit.json) enlaza las comprobaciones numéricas, de traducción, presentación y reproducción.
'''.replace(f"{en['body_words']:,}", f"{en['body_words']:,}".replace(',', '.')))
print('Project state, accepted tone, manuscript guides and current findings updated.')
