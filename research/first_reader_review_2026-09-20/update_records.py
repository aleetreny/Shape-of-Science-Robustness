from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
report=json.loads((HERE/'text_audit.json').read_text());en=report['documents']['en'];es=report['documents']['es']
latest=f'''**Revisión vigente para una primera lectura, 20-09-2026:** por petición expresa del autor, se ha releído y revisado el artículo completo para alguien sin contexto. Entrega: [FIRST_READER_REVIEW.md](FIRST_READER_REVIEW.md). Se conserva la voz aceptada; se explican los conceptos, el propósito y los artículos de cada prueba, y el significado de las cifras. Inglés: {en['body_words']:,} palabras de cuerpo, {en['abstract_words']} de resumen y {en['pages']} páginas. Español: {es['body_words']:,}, {es['abstract_words']} y {es['pages']} páginas. Cifras científicas, figuras, bibliografía, declaraciones y suplementos conservados. Las revisiones que siguen son históricas; aprobación personal pendiente.'''.replace('6,567','6.567').replace('7,332','7.332')
def after_heading(name,text):
 p=ROOT/name;s=p.read_text();line,rest=s.split('\n',1);p.write_text(line+'\n\n'+text.strip()+'\n'+rest)
for name in ['AGENTS.md','progress.md','findings.md','DECISIONS.md','NEXT_STEPS.md']:after_heading(name,latest)
after_heading('AUTHOR_VOICE.md','''**Regla de primera lectura, 20-09-2026:** el autor conserva la personalidad y pide releer el artículo entero sin asumir conocimiento del estudio. Cada prueba debe presentar la pregunta, qué se mantiene igual, qué cambia y cómo interpretar el resultado. Nombrar conjuntos por su finalidad y explicar sus relaciones; distinguir estructura, dispersión, orden entre áreas y dirección de un vector. Explicar denominadores y cambios de candidatos junto a las cifras. Definir los términos donde hacen falta y usar ejemplos breves sin convertir el artículo en una sucesión de analogías. Aplicación completa en [FIRST_READER_REVIEW.md](FIRST_READER_REVIEW.md). No es aprobación personal final ni permiso para nuevos análisis.''')
after_heading('DECISIONS.md','''**Alcance aceptado directamente, 20-09-2026:** la nueva petición amplía la revisión de frases marcadas a la lectura completa del artículo. Autoriza una versión editorial revisada con más contexto, ejemplos y continuidad, manteniendo la voz que gusta al autor. Se aplica al inglés canónico y a su copia española. No cambia las decisiones científicas cerradas. El aumento de explicación y los dos nuevos apartados de métodos son decisiones editoriales dentro de ese encargo; no se han elegido nuevos parámetros, datos o modelos.''')
p=ROOT/'task_plan.md';s=p.read_text();p.write_text('''# Revisión completa para una primera lectura, 20-09-2026

Petición: releer todo el artículo sin asumir contexto y entregar una versión más comprensible conservando la personalidad.

1. Leer artículo completo, tablas y pies; identificar conceptos y transiciones sin explicación: **complete**.
2. Revisar inglés y español, con nombres de conjuntos, ejemplos y significado de cifras: **complete**.
3. Comprobar correspondencia, cifras y archivos científicos conservados: **complete**.
4. Compilar e inspeccionar ambos PDF; reconstruir paquetes editables: **in_progress**. Cierre verificable en `research/first_reader_review_2026-09-20/closure_audit.json` cuando termine.

Entrega: `FIRST_READER_REVIEW.md`. Continuación: comentarios del autor; no reabrir experimentos.

---

'''+s)
p=ROOT/'README.md';s=p.read_text();s=re.sub(r'\*\*Estado · 20 septiembre 2026:\*\*[^\n]+',f'**Estado · 20 septiembre 2026:** [cierre científico terminado](ROBUSTNESS_CLOSURE_REPORT.md) y [revisión completa para una primera lectura](FIRST_READER_REVIEW.md), en inglés y español. Tono conservado; conceptos, pruebas y resultados explicados con más contexto. Inglés: {en["pages"]} páginas; español: {es["pages"]}. Revisión personal y depósito de datos pendientes. [Estado exacto →](NEXT_STEPS.md)',s);p.write_text(s)
p=ROOT/'docs/INDEX.md';s=p.read_text();s=s.replace('**Última revisión editorial, 20-09-2026:** [los 38 comentarios aplicados](../MANUSCRIPT_EXPLANATIONS.md), con registro por comentario, dos PDF y fuentes editables. Esta es la entrega de texto vigente; los cierres científicos se conservan.','**Última revisión editorial, 20-09-2026:** [primera lectura completa](../FIRST_READER_REVIEW.md), con explicaciones, transiciones, ejemplos y dos PDF sincronizados. Los [38 comentarios anteriores](../MANUSCRIPT_EXPLANATIONS.md) y los cierres científicos se conservan como historial.');s=s.replace('la redacción vigente está en MANUSCRIPT_CLARITY','la redacción vigente está en FIRST_READER_REVIEW').replace('[Manuscrito vigente y paquete editable](../MANUSCRIPT_CLARITY.md)','[Manuscrito vigente y paquete editable](../FIRST_READER_REVIEW.md)');p.write_text(s)
for folder,lang in [('manuscript','en'),('manuscript_es','es')]:
 p=ROOT/folder/'README.md';s=p.read_text();s=s.replace('**Última edición, 20-09-2026:**','**Edición anterior, 20-09-2026:**',1)
 line,rest=s.split('\n',1);s=line+'\n\n'+latest.replace('(FIRST_READER_REVIEW.md)','(../FIRST_READER_REVIEW.md)')+'\n'+rest
 if lang=='en':
  s=re.sub(r'El texto científico está completo y revisado:[^\n]+',f'El texto científico está completo y revisado: introducción, antecedentes, métodos, resultados, discusión, conclusión y resumen. El cuerpo tiene **6.567 palabras**, sin tablas, pies, citas expandidas ni declaraciones; el resumen, **195**. Principal: {en["pages"]} páginas, incluidas figuras y referencias. Suplemento: 39 páginas. La revisión de primera lectura explica pasos que antes quedaban implícitos; el registro está en [FIRST_READER_REVIEW.md](../FIRST_READER_REVIEW.md).',s)
  s=s.replace('La ayuda de Codex está descrita.','El historial real de asistencia se conserva en el proyecto.')
 else:
  s=s.replace('**Edición vigente, 20-09-2026:**','**Edición anterior de voz, 20-09-2026:**')
  s=s.replace('(22 páginas)','(25 páginas)').replace('Revisión actual: `../MANUSCRIPT_CLARITY.md`','Revisión actual: `../FIRST_READER_REVIEW.md`')
 p.write_text(s)
print('Current editorial state and source READMEs updated; earlier records retained.')
