from pathlib import Path
from datetime import datetime,timezone
import difflib,hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Archive the two additional navigation/status records before updating them.
p=HERE/'baseline_manifest.json';base=json.loads(p.read_text());protected_path=HERE/'protected_manifest.json';protected=json.loads(protected_path.read_text())
for rel in ['docs/INDEX.md','docs/QSS_CHECK.md']:
 assert rel not in base
 dest=HERE/'baseline'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest);base[rel]=sha(dest)
 protected.pop(rel,None)
p.write_text(json.dumps(base,indent=2)+'\n');protected_path.write_text(json.dumps(protected,indent=2)+'\n')
rows=[
(1,'Ejemplo de búsquedas emparejadas','Se usan 50 artículos de Cardiología en dos conjuntos de 256: especialidad y Medicina.','3.3'),
(2,'Diez selecciones','Los 50 artículos de partida siguen fijos; se eligen diez veces los otros 206. Se excluye el propio artículo al buscar sus vecinos.','3.3'),
(3,'Qué significa CKA','Se explica el parecido entre patrones de relaciones, sin convertirlo en porcentaje de acierto.','3.4'),
(4,'Para qué se vuelven a elegir artículos','Se indica que se eligen para recalcular la posición media de cada disciplina.','Resumen'),
(5,'Título como entrada del modelo','Se dice qué texto recibe el modelo: solo título frente a título y resumen.','Resumen'),
(6,'Final del resumen','Se explica el propósito positivo: identificar relaciones compartidas y decisiones de las que dependen.','Resumen'),
(7,'Tabla de muestras','Seis preguntas concretas; columnas de comparación y artículos; se separan organización general y vecinos. La colección inicial pasa a la nota.','Tabla 1'),
(8,'Sin resolver','Se definen las dos reglas y el caso restante. Un empate no cuenta como dirección persistente; no basta con que un modelo empate para invalidar la oposición de otros dos.','3.5'),
(9,'Qué es una selección','Definición temprana y explicación de conjuntos solapados dentro de la colección fija.','2.2 y 3.5'),
(10,'Alerta de selección','Resultado sensible a cambiar artículos o tamaño según la tolerancia registrada; no error de un registro.','3.5 y 4.1'),
(11,'26 especialidades de la figura','Una por cada una de las 26 áreas; 50 elecciones, con diez elecciones de artículos para cada una.','Figura 1'),
(12,'2.048 candidatos comunes','Misma cantidad por grupo; mismos identificadores entre modelos dentro del grupo, no entre disciplinas.','4.2'),
(13,'Búsqueda global','100 artículos de partida por cada uno de 130 grupos; sus vecinos se buscan entre 400.000 registros.','4.2'),
(14,'Dos cambios a la vez','Se amplían disciplinas/períodos y cantidad de candidatos; no se separan sus efectos.','4.2'),
(15,'Filtro de calidad','Se retiran las marcas indicadas y se conserva un representante por grupo de duplicados. Antes y después son unos ocho vecinos compartidos de 25.','4.2'),
(16,'Cambiar el alcance','Se explica si las listas coinciden más o menos, con 58,5% frente a 41,5% de especialidades y el reparto casi igual con 50 vecinos.','4.2'),
(17,'Área amplia','Se identifica como el área que contiene la especialidad, con Medicina como ejemplo.','Figura 2'),
(18,'Especialidad','Se identifica como rama más concreta, con Cardiología y Medicina Cardiovascular como ejemplo.','Figura 2'),
(19,'Casos y errores de origen','Se cuenta qué se revisó y cómo se comprobó contra los registros descargados. Los ejemplos no estiman la frecuencia del problema.','4.2'),
(20,'Tres entradas','Cada uno de los mismos 52.000 artículos se representa con título, resumen y ambos; se distinguen las dos comparaciones con la referencia combinada.','4.3'),
(21,'Reglas de combinación','Media frente a primera o última salida; se nombran los cuatro BERT afectados y se explica que se recalculan ambas comparaciones.','4.3'),
(22,'De 26.000 a 52.000','Se explica que se añaden 26.000 con el mismo diseño y se conserva el primer conjunto dentro del total.','4.3'),
(23,'Alertas geométricas','Se distinguen veinte medias muestras de 1.000 y cinco selecciones de 2.000; cuatro alertas equivalen al 1,5% de 260 casos.','4.4'),
(24,'Un área por encima de otra','Mayor valor de la medida, no posición en un dibujo ni calidad de la investigación.','4.4'),
(25,'Recuentos de parejas','Se presentan porcentajes de las 325 parejas para oposición, unanimidad, casos sin resolver y cortes de magnitud. Los recuentos permanecen en figura y tablas.','4.4'),
(26,'Medidas alternativas','Se recuerdan entropía y D80, sus empates y los denominadores. Conservar una oposición exige al menos una misma pareja de modelos en las mismas direcciones.','4.4'),
(27,'Punto de referencia','Media común de 52.000 vectores por modelo, resta a cada vector y reajuste de longitud.','3.5 y 4.4'),
(28,'Efecto del centrado','Se distinguen proporción total de parejas opuestas y conservación de parejas originales; cifras completas remitidas a S20.','4.4'),
(29,'Por qué se probó la fragmentación','Se explica la posible utilidad y por qué una conexión geométrica débil no quedó validada como división temática.','4.4'),
(30,'Veinte mitades y cinco selecciones','26 condiciones: principal de 2.000, veinte mitades de 1.000 y cinco elecciones adicionales de 2.000 por área.','Figura 4'),
(31,'Repetir artículos no es cambiar modelo','Ejemplo de A mayor que B en un modelo y orden contrario en otro, aun repitiendo artículos.','5.1'),
(32,'Qué controlan los centros','Recalcular medias con otros artículos, con tres tamaños y omitiendo cada área.','5.2'),
(33,'Calidad, entrada y medias','Se explica el cambio pequeño del filtro y los comportamientos distintos que reúne la media de entrada.','5.2'),
(34,'Matiz repetido sobre corrección','Se retira la frase repetitiva y se conserva la distinción general entre acuerdo y evidencia externa donde corresponde.','5.2'),
(35,'Consecuencia del procesamiento','La comparación de dispersión debe indicar representación, punto de referencia y medida.','5.2'),
(36,'Medicina, familias y tiempo','Se explican los controles de composición y modelos biomédicos, los límites de causa y el cambio de signo al igualar candidatos.','5.2'),
(37,'Conclusión','Se formula una consecuencia concreta: comprobar la relación que se quiere sostener y mostrar cuánto cambia.','6'),
(38,'Retirar sección de IA','Se retira de ambos artículos y se elimina la remisión que quedaría sin destino. El historial real de asistencia permanece.','Declaraciones'),
]
assert [r[0] for r in rows]==list(range(1,39))
record=[{'comment':n,'topic':topic,'change':change,'location':loc,'languages':['en','es'],'status':'applied'} for n,topic,change,loc in rows]
(HERE/'comment_coverage.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
report='''# Los 38 comentarios aplicados al manuscrito

**20-09-2026. Revisión editorial solicitada por el autor.** Se ha aclarado el artículo en inglés y español. El tono elegido y el título se conservan. No se han repetido experimentos ni modificado resultados, figuras, bibliografía o suplemento. Se han convertido recuentos ya guardados a porcentajes para facilitar su lectura.

- [Artículo en español](output/pdf/es/main.pdf): 22 páginas; 6.090 palabras de cuerpo y 240 de resumen para revisión.
- [Artículo en inglés](output/pdf/main.pdf): 21 páginas; 5.412 palabras de cuerpo y 200 de resumen.
- [Fuentes inglesas](output/manuscript_source.zip) y [españolas](output/manuscript_source_es.zip).

El recuento usa el mismo procedimiento de las revisiones anteriores: excluye títulos, tablas, pies, citas, fórmulas y declaraciones. La explicación aumenta el cuerpo inglés en 842 palabras; el español mantiene su número de páginas.

## Cambios que se notan al leer

Los términos se presentan con su función: qué artículo sirve de partida, cuáles pueden aparecer como vecinos, qué significa volver a elegir artículos y cuándo se marca una alerta. El ejemplo de Cardiología y Medicina explica la búsqueda emparejada. La Tabla 1 separa las preguntas y aclara qué conjuntos se reutilizan. Las comparaciones entre áreas usan porcentajes con denominador explícito. La discusión conecta cada prueba con la conclusión que permite sostener.

## Seguimiento de cada comentario

Las ubicaciones son las secciones actuales; las páginas pueden haber cambiado. Las descripciones siguientes resumen cómo se atendieron los comentarios, no son citas literales del autor. Cada fila se ha trasladado a ambos idiomas.

| N.º | Tema | Cambio aplicado | Ubicación |
| ---: | --- | --- | --- |
'''
report+='\n'.join(f'| {n} | {topic} | {change} | {loc} |' for n,topic,change,loc in rows)
report+='''

## Comprobaciones y alcance

- Los 24 porcentajes de esta revisión se comprueban contra los recuentos guardados en [percentage_audit.csv](research/manuscript_explanations_2026-09-20/percentage_audit.csv). No son experimentos nuevos.
- El ejemplo de Cardiología como especialidad de Medicina se comprobó en el índice de metadatos local; la búsqueda global de 100 artículos por grupo se contrastó con los métodos guardados.
- Las cifras de 66 bloques del cuerpo corresponden entre inglés y español. Citas, referencias a figuras/tablas, fórmulas y títulos se conservan. Las fuentes y PDF del suplemento permanecen intactos.
- Los 43 folios de los dos artículos se han inspeccionado visualmente. Tabla 1, pies y referencias caben sin recortes ni superposiciones. Se evita partir una entrada bibliográfica entre páginas.
- Las versiones previas están en [baseline/](research/manuscript_explanations_2026-09-20/baseline/). El [registro final](research/manuscript_explanations_2026-09-20/closure_audit.json) reúne las verificaciones, las huellas de archivos protegidos y la reconstrucción desde los ZIP.

## Comentario 38 y continuación

Por petición explícita del autor, el borrador ya no incluye el apartado de uso de IA. También se retira la remisión a ese apartado desde las contribuciones. Esto modifica la presentación del borrador, no la historia real del trabajo: las copias previas y los registros de asistencia permanecen intactos. No se añade ninguna afirmación de ausencia de asistencia.

Antes de un eventual envío habrá que comprobar las declaraciones que exija la revista y presentarlas de forma fiel al trabajo realizado. No se ha comprobado de nuevo la política editorial en esta revisión ni se ha enviado o publicado el artículo. Siguen pendientes la lectura personal y aprobación final del autor, la correspondencia y las decisiones de depósito y licencia.
'''
(ROOT/'MANUSCRIPT_EXPLANATIONS.md').write_text(report)
status='**Revisión editorial más reciente, 20-09-2026:** los 38 comentarios del autor están aplicados en inglés y español; ver [MANUSCRIPT_EXPLANATIONS.md](MANUSCRIPT_EXPLANATIONS.md). Se explican selecciones, candidatos, alertas y casos sin resolver, con ejemplos y porcentajes comprobados. Inglés: 5.412 palabras de cuerpo, 200 de resumen y 21 páginas. Español: 6.090, 240 y 22 páginas. Suplementos intactos (39 y 41 páginas). El apartado de IA se ha retirado del borrador por petición expresa; el registro real de asistencia se conserva y las declaraciones exigidas se comprobarán antes del envío. Título y tono conservados; revisión personal pendiente. Los estados de edición que siguen son históricos.\n\n'
def prepend_after_title(rel,text):
 p=ROOT/rel;s=p.read_text();a,b=s.split('\n',1);p.write_text(a+'\n\n'+text+b.lstrip('\n'))
for rel in ['AGENTS.md','DECISIONS.md','progress.md','findings.md']:
 prepend_after_title(rel,status)
prepend_after_title('AUTHOR_VOICE.md','**Aclaraciones del autor, 20-09-2026:** explicar qué se mantiene y qué cambia en cada comparación, con ejemplos concretos. Definir selección, artículo de partida, candidato y alerta antes de usarlos. Dar denominadores con porcentajes; sustituir «por encima» por «mayor valor de la medida». Reducir avisos repetidos sin perder los límites. Aplicado a los 38 comentarios en `MANUSCRIPT_EXPLANATIONS.md`. La retirada del apartado de IA afecta a la presentación del borrador y no borra el registro real de asistencia.\n\n')
p=ROOT/'task_plan.md';s=p.read_text();s=s.split('\n---\n',1)[1]
p.write_text('''# Tarea terminada: aclarar los 38 comentarios del PDF, 20-09-2026

1. Contrastar ejemplos con metadatos y resultados guardados: **complete**.
2. Revisar artículo y Tabla 1 en ambos idiomas: **complete**.
3. Compilar, comprobar cifras/referencias y revisar 43 páginas: **complete**.
4. Actualizar registros y paquetes editables: **complete**; comprobación final en `research/manuscript_explanations_2026-09-20/closure_audit.json`.

Entrega: `MANUSCRIPT_EXPLANATIONS.md`. Título y tono conservados. Apartado de IA retirado por petición expresa, con historial real conservado y requisitos de envío pendientes de comprobar. Sin nuevos experimentos, publicación, commit/push ni cambios al suplemento. Continuar con los comentarios personales del autor.

---
'''+s)
p=ROOT/'NEXT_STEPS.md';s=p.read_text();start=s.index('El abstract se ha aclarado después');end=s.index('\n\n',start)
s=s[:start]+status.strip()+s[end:];s=s.replace('revisión actual de normas y referencias.','revisión actual de normas, referencias y declaraciones exigidas, incluida la asistencia real utilizada.');p.write_text(s)
p=ROOT/'README.md';s=p.read_text();start=s.index('**Estado · 20 septiembre 2026:**');end=s.index('\n\n',start)
s=s[:start]+'**Estado · 20 septiembre 2026:** [cierre científico terminado](ROBUSTNESS_CLOSURE_REPORT.md) y [38 comentarios editoriales aplicados](MANUSCRIPT_EXPLANATIONS.md) en inglés y español. El tono claro está aceptado. Inglés: 5.412 palabras de cuerpo, 200 de resumen y 21 páginas; español: 22 páginas. Revisión personal y depósito de datos pendientes. [Estado exacto →](NEXT_STEPS.md)'+s[end:];p.write_text(s)
p=ROOT/'manuscript/README.md';s=p.read_text().replace('4.570 palabras','5.412 palabras').replace('Principal: 20 páginas','Principal: 21 páginas').replace('tras la [aclaración solicitada por el autor](../ABSTRACT_CLARITY.md)','tras aplicar los [38 comentarios del autor](../MANUSCRIPT_EXPLANATIONS.md)');p.write_text(s)
prepend_after_title('manuscript/README.md','**Última edición, 20-09-2026:** [38 comentarios aclarados](../MANUSCRIPT_EXPLANATIONS.md), con ejemplos, porcentajes y Tabla 1 reorganizada. El apartado de IA se retira del borrador por petición del autor; la historia real de asistencia queda conservada y las declaraciones exigidas se revisarán antes del envío.\n\n')
p=ROOT/'manuscript_es/README.md';s=p.read_text();start=s.index('**Abstract aclarado después');end=s.index('\n\n',start)
s=s[:start]+'**Última edición, 20-09-2026:** [38 comentarios aclarados](../MANUSCRIPT_EXPLANATIONS.md). Cuerpo español: 6.090 palabras; resumen: 240 para revisión. Inglés: 5.412 y 200. Suplemento conservado. Apartado de IA retirado del borrador por petición del autor; historial real de asistencia conservado y requisitos de declaración pendientes de comprobar antes del envío.'+s[end:]
s=s.replace('Los cinco comentarios del autor del 18-09-2026 se han aplicado tanto al inglés como al español: título, tablas, Figura 1B y declaración breve de IA.', 'Los cinco comentarios del 18-09-2026 y los 38 del 20-09-2026 se han aplicado a ambos idiomas. La retirada posterior del apartado de IA sustituye su redacción breve anterior.');p.write_text(s)
prepend_after_title('docs/INDEX.md','**Última revisión editorial, 20-09-2026:** [los 38 comentarios aplicados](../MANUSCRIPT_EXPLANATIONS.md), con registro por comentario, dos PDF y fuentes editables. Esta es la entrega de texto vigente; los cierres científicos se conservan.\n\n')
p=ROOT/'docs/QSS_CHECK.md';s=p.read_text();lines=s.splitlines();lines=[('| Uso de IA y herramientas | Apartado retirado del borrador por petición explícita del autor el 20-09-2026 (comentario 38). El historial real de asistencia se conserva. Antes del envío, comprobar la política vigente y aportar las declaraciones exigidas de forma fiel. No se ha repetido la consulta de normas en esta revisión. [Registro](../MANUSCRIPT_EXPLANATIONS.md#comentario-38-y-continuación). |' if line.startswith('| Uso de IA y herramientas |') else line) for line in lines];p.write_text('\n'.join(lines)+'\n')
# Preserve actual final diffs, including small precision/layout corrections after initial drafting.
for folder in ['manuscript','manuscript_es']:
 for name in ['main.tex','tables/editorial/T01.tex']:
  a=(HERE/'baseline'/folder/name).read_text();b=(ROOT/folder/name).read_text()
  target=HERE/(folder+'_'+Path(name).name+'.diff');target.write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+folder+'/'+name,tofile='after/'+folder+'/'+name)))
manifest=json.loads((HERE/'render_manifest.json').read_text())
(HERE/'visual_review.json').write_text(json.dumps({'reviewed_at':datetime.now(timezone.utc).isoformat(),'documents':{k:{'sha256':v['sha256'],'pages_reviewed':list(range(1,v['pages']+1))} for k,v in manifest.items()},'result':'All 43 pages inspected; final changed pages re-inspected. No clipping, overlap or missing glyphs. Table and figure captions readable; bibliography entries kept together.','method':'Full-page renders and four-page contact sheets; unchanged final page images matched the first inspection.'},indent=2)+'\n')
print('38 comments recorded; current project instructions and delivery metadata updated.')
