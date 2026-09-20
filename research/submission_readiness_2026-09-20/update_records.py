"""Record the completed review without authorising the proposed public release."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
changes = {
    'AGENTS.md': '''**Revisión previa al envío, 20-09-2026:** el autor pide aclarar la novedad y explorar la reproducción pública. Entrega: [NOVELTY_AND_REPRODUCIBILITY.md](NOVELTY_AND_REPRODUCIBILITY.md). Contraste dirigido con antecedentes y redacción EN/ES propuesta, sin modificar el artículo. GitHub sigue en `44c9410` (17-09): faltan las fases de geometría y cierre posterior. Sin licencia general ni depósito persistente. Propuesta GitHub + Zenodo, inventario y demostración local de parte de Figura 4 preparados; no equivalen a reproducción pública completa. La guía QSS sigue inaccesible directamente (403); se consultó su versión oficial indexada. No publicar, elegir licencia o enviar por extensión de esta revisión. Continuar con la integración editorial o preparación del paquete cuando el autor lo solicite.''',
    'DECISIONS.md': '''**Petición y revisión cerrada, 20-09-2026:** el autor solicita examinar la novedad y cómo cumplir la reproducción pública antes de enviar a QSS. Se ha realizado la revisión dirigida y preparado propuestas concretas: [NOVELTY_AND_REPRODUCIBILITY.md](NOVELTY_AND_REPRODUCIBILITY.md). La redacción sobre comparaciones persistentes entre áreas y la vía GitHub + Zenodo son recomendaciones, no elecciones científicas nuevas ni autorización de depósito. MIT para código propio y CC BY 4.0 para resultados propios son propuestas aún no aceptadas. El ejemplo local recalcula parte de Figura 4 desde medidas guardadas; no reabre experimentos ni demuestra reproducción completa. El manuscrito y sus PDF se conservan. Publicación de datos, licencias y envío siguen pendientes.''',
    'progress.md': '''**Revisión de novedad y reproducción pública terminada, 20-09-2026:** [informe y recomendaciones](NOVELTY_AND_REPRODUCIBILITY.md). Ocho antecedentes contrastados con alcance de lectura explícito; versiones arXiv comprobadas y actualización editorial de Bascur 2026 identificada. Estado público verificado: `44c9410`, 852 archivos, sin fases del 18/20 ni licencia general. Inventario: 57,576 GB de carpetas relevantes, antes de separar duplicados/textos. Demostración de 672.054 bytes ejecutada en carpeta aislada con Python 3.12.14 y biblioteca estándar: ocho clasificaciones de 325 parejas y dos retenciones de modelos coinciden. Redacción EN/ES y especificación del paquete preparadas. Sin cambios al artículo, datos científicos o remoto. Continuación: propuestas del informe; paquete completo, licencias y depósito aún pendientes.''',
    'findings.md': '''**Novedad y acceso público, 20-09-2026:** la aportación defendible se concentra en seguir comparaciones entre áreas que persisten al cambiar artículos pero pueden invertirse entre modelos o procesamiento. La distinción general entre similitud y estabilidad tiene antecedentes; no afirmar prioridad. [Informe, matriz y fuentes](NOVELTY_AND_REPRODUCIBILITY.md). La comprobación remota muestra que el repositorio público aún no corresponde al artículo final. QSS directo devuelve 403; la normativa se recoge con esa limitación. El inventario y la demostración local están en `research/submission_readiness_2026-09-20/`; solo el ejemplo de agregación de Figura 4 se ha probado de forma autónoma en esta fase.''',
    'NEXT_STEPS.md': '''**Última entrega, 20-09-2026:** [novedad y reproducción pública](NOVELTY_AND_REPRODUCIBILITY.md). Hay redacción propuesta EN/ES y una especificación concreta de depósito, con un ejemplo local comprobado. El manuscrito sigue en la versión de primera lectura. Para el envío queda integrar la redacción que acepte el autor, preparar y probar el paquete completo, resolver licencias/entradas textuales y publicar la versión autorizada con identificadores reales. Ninguno de esos pasos se da por completado por haber terminado esta investigación.''',
    'docs/INDEX.md': '''**Preparación del envío, 20-09-2026:** [Novedad y reproducción pública](../NOVELTY_AND_REPRODUCIBILITY.md): contraste de antecedentes, redacción propuesta, estado real de GitHub, inventario y vía de depósito. Incluye un ejemplo autónomo para parte de Figura 4; no es un depósito público.''',
    'references/RELATED_WORK.md': '''**Consulta dirigida adicional, 20-09-2026:** [novedad y reproducción pública](../NOVELTY_AND_REPRODUCIBILITY.md) concentra la contribución en comparaciones disciplinares persistentes y sus límites de representación. Se contrastan ocho antecedentes; Raju se revisa en v5 y se identifica la publicación de Bascur, Costas y Verberne del 15-09-2026 (DOI 10.1515/jdis-2026-0114). [Fuentes y profundidad de lectura](../research/submission_readiness_2026-09-20/SOURCES.md). No se cambia automáticamente la biblioteca del manuscrito ni se afirma prioridad absoluta.''',
}

def save(path, text):
    target = ROOT / path
    before = target.read_text()
    backup = HERE / 'baseline_documents' / path
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
    target.write_text(text)

for name, paragraph in changes.items():
    text = (ROOT / name).read_text()
    if paragraph not in text:
        heading, rest = text.split('\n', 1)
        save(name, heading + '\n\n' + paragraph + '\n' + rest)

plan = '''# Tarea terminada: novedad y vía de reproducción pública, 20-09-2026

1. Contrastar la aportación con antecedentes y versiones actuales: **complete**; búsqueda dirigida con límites de lectura registrados.
2. Comprobar política QSS y opciones de depósito: **complete** dentro del acceso disponible; guía oficial indexada, acceso directo 403.
3. Auditar estado público y archivos locales: **complete**; remoto `44c9410` y tamaños guardados.
4. Preparar redacción EN/ES y especificación de paquete: **complete**; son propuestas separadas, no cambios ya aprobados al artículo.
5. Comprobar un ejemplo autónomo de reproducción: **complete** para parte de Figura 4. El paquete científico completo sigue **pending**, igual que licencias, depósito y envío.

Entrega: [NOVELTY_AND_REPRODUCIBILITY.md](NOVELTY_AND_REPRODUCIBILITY.md). No hubo experimentos nuevos, modificación del manuscrito, commit/push o publicación.

---

'''
current = (ROOT / 'task_plan.md').read_text()
if not current.startswith(plan):
    save('task_plan.md', plan + current)

qss = (ROOT / 'docs/QSS_CHECK.md').read_text()
old = '**20-09-2026:** cierre metodológico terminado, con límites incorporados al manuscrito. Estado: READY WITH MINOR CAVEATS; no es aprobación editorial ni autorización de envío. Las normas externas descritas abajo no se han vuelto a comprobar en esta fase.'
new = '**20-09-2026, revisión previa al envío:** [novedad y reproducción pública](../NOVELTY_AND_REPRODUCIBILITY.md) es la comprobación vigente. El cierre científico anterior no equivale a estar listo para enviar: faltan versión pública completa, licencias y depósito probado. La consulta directa de QSS se ha repetido y devuelve 403; la guía oficial indexada conserva la limitación de antigüedad indicada abajo.'
if old in qss:
    qss = qss.replace(old, new)
qss = qss.replace('Resumen inglés de 200 palabras; cuerpo de 4.570 sin pies/tablas/referencias.', 'Revisión de primera lectura: resumen inglés de 195 palabras, cuerpo de 6.567 y PDF de 24 páginas; [entrega vigente](../FIRST_READER_REVIEW.md).')
qss = qss.replace('Código, tablas y figuras incluidos en la versión autorizada para GitHub; corpus/vectores todavía locales. Falta depósito permanente y probar su reconstrucción; [plan preparado](DATA_RELEASE.md).', 'GitHub verificado en `44c9410` (17-09), anterior a geometría y al cierre del 20-09. Corpus/vectores locales, sin licencia general ni depósito persistente. [Especificación y prueba parcial preparadas](../NOVELTY_AND_REPRODUCIBILITY.md).')
save('docs/QSS_CHECK.md', qss)

release = (ROOT / 'docs/DATA_RELEASE.md').read_text()
paragraph = '**Revisión vigente, 20-09-2026:** [informe de novedad y reproducción](../NOVELTY_AND_REPRODUCIBILITY.md) y [especificación del paquete](../research/submission_readiness_2026-09-20/RELEASE_SPEC.md). Se verificó que GitHub sigue en el 17-09 y no incluye las fases posteriores del artículo. Inventario y ejemplo autónomo de parte de Figura 4 terminados. GitHub + Zenodo y las licencias sugeridas siguen siendo propuestas; no se ha publicado ningún depósito. El material que sigue documenta la preparación anterior, no la cobertura de la versión pública actual.'
if paragraph not in release:
    heading, rest = release.split('\n', 1)
    save('docs/DATA_RELEASE.md', heading + '\n\n' + paragraph + '\n' + rest)

readme = (ROOT / 'README.md').read_text()
paragraph = '**Preparación del envío, 20-09-2026:** [Novedad y reproducción pública](NOVELTY_AND_REPRODUCIBILITY.md). Revisión de antecedentes, estado público comprobado y propuesta de paquete; demostración local para parte de Figura 4. Depósito y reproducción pública completa pendientes.'
if paragraph not in readme:
    heading, rest = readme.split('\n', 1)
    save('README.md', heading + '\n\n' + paragraph + '\n' + rest)
print('Continuity records updated; no manuscript or scientific file edited.')
