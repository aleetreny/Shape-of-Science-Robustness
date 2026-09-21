"""Update delivery and continuity notes only after anonymous archive verification."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
public=json.loads((HERE/'public_verification.json').read_text());assert public['published'] and public['record']==22876602
assert json.loads((HERE/'manuscript_update.json').read_text())['all_checks_passed'] is True
DOI='https://doi.org/10.5281/zenodo.22876602';GITHUB='https://github.com/aleetreny/Shape-of-Science-Reproducibility/releases/tag/v1.1.0'
summary=f'''**Entrega vigente, 21-09-2026:** distribución compacta v1.1.0 publicada y comprobada: 15 archivos, 492.154.568 bytes. [GitHub]({GITHUB}) y [archivo con DOI]({DOI}). Sustituye la carga de 51 GB. Se conservan medidas, recuentos, identidades, selecciones y controles; se excluyen grandes cachés de vectores/listas, textos históricos, artículo, suplementos y notas internas. Reproducción estadística comprobada desde los ZIP en macOS y en un entorno Linux nuevo: 25 tablas, 106.445 filas idénticas y 17.550 medidas de vecinos coincidentes. No se certifica regeneración desde textos históricos ni todos los análisis suplementarios. El borrador antiguo 22863543 permanece sin publicar; el cargador local está retirado. No queda una subida a cargo del autor. Detalles: [COMPACT_REPRODUCIBILITY.md](COMPACT_REPRODUCIBILITY.md).\n'''
for name in ['AGENTS.md','DECISIONS.md','progress.md','findings.md','NEXT_STEPS.md']:
 p=ROOT/name;s=p.read_text();p.write_text('## 21-09-2026 — Publicación compacta terminada\n\n'+summary+'\nDisponibilidad, cita del conjunto de datos y S8 actualizados en ambos idiomas; artículo y suplementos siguen fuera del depósito. Se preservan los archivos científicos congelados y las ediciones previas del autor. La revisión personal y el envío a revista siguen separados de esta entrega. Las notas siguientes conservan la cronología y no reabren la carga antigua.\n\n'+s)
p=ROOT/'task_plan.md';s=p.read_text();a=s.index('# En curso: distribución compacta');b=s.index('\n# Entrega actual:',a)
s=s[:a]+'''# Terminada: distribución compacta y publicación, 21-09-2026

1. Comprobar la política literal de QSS y alternativas: **complete**.
2. Seleccionar datos y verificar los cálculos: **complete**; 492 MB, 25 tablas/106.445 filas y 17.550 controles de vecinos.
3. Publicar código y archivos en GitHub y transferir desde sus servidores: **complete**.
4. Verificar descargas públicas y publicar el DOI compacto: **complete**; 15 archivos verificados, DOI 10.5281/zenodo.22876602.
5. Actualizar disponibilidad y entregar enlaces: **complete**; inglés y español, con el alcance público explícito.

El historial siguiente está sustituido en cuanto a las cargas pendientes.
'''+s[b:];p.write_text(s)
p=ROOT/'COMPACT_REPRODUCIBILITY.md';s=p.read_text().replace('**21-09-2026. Preparación y pruebas terminadas; publicación en curso.**','**21-09-2026. Publicado y verificado en GitHub y Zenodo.**')
s=s.replace('El nuevo identificador reservado es `10.5281/zenodo.22876602`; **todavía no debe citarse como depósito público hasta terminar y comprobar la publicación**.',f'El depósito está publicado como [10.5281/zenodo.22876602]({DOI}), con los 15 archivos verificados por tamaño y huella. Los archivos de GitHub se descargaron sin autenticación y se verificaron también por SHA-256.')
s=s.replace('No se cambió ningún resultado científico.', 'La misma prueba pasó en un entorno Linux nuevo con las versiones fijadas; todas las celdas de los CSV fueron idénticas. [Ejecución pública](https://github.com/aleetreny/Shape-of-Science-Reproducibility/actions/runs/35610529164). No se cambió ningún resultado científico.')
p.write_text(s)
p=ROOT/'README.md';s=p.read_text().replace('El depósito con DOI se está completando desde GitHub; el registro anterior no debe publicarse.',f'El depósito está publicado con DOI [10.5281/zenodo.22876602]({DOI}); el registro anterior no debe publicarse.');p.write_text(s)
(ROOT/'ZENODO_UPLOAD.md').write_text(f'''# La entrega ya está publicada

No hay que ejecutar ningún cargador ni subir los archivos de `output/zenodo/`.

- [Datos y código con DOI]({DOI}).
- [Descarga alternativa en GitHub]({GITHUB}).
- [Selección, comandos comprobados y límites](COMPACT_REPRODUCIBILITY.md).

Son 15 archivos y 492 MB. Artículo y suplementos están fuera: la narrativa puede seguir editándose sin alterar esta versión de los datos. El borrador anterior 22863543 se conserva sin publicar; no lo publiques.

La guía anterior se conserva en `research/compact_release_2026-09-21/superseded/ZENODO_UPLOAD.md`.
''')
for name in ['PUBLIC_RELEASE.md','docs/DATA_RELEASE.md']:
 p=ROOT/name;s=p.read_text();p.write_text((summary.replace('(COMPACT_REPRODUCIBILITY.md)','(../COMPACT_REPRODUCIBILITY.md)') if name.startswith('docs/') else summary)+'\nEl contenido siguiente documenta las entregas anteriores y sus cifras históricas.\n\n'+s)
p=ROOT/'reproducibility/README.md';s=p.read_text();s=s.replace('Its DOI archival copy is being finalized.',f'Its DOI archive is public at [10.5281/zenodo.22876602]({DOI}).');p.write_text(s)
p=HERE/'release_notes.md';s=p.read_text().replace('Verified locally:', 'Verified from extracted archives locally and in a clean Linux environment:').replace('Permanent archive: DOI 10.5281/zenodo.22876602 (reserved while the archival transfer is in progress; this note will be updated after publication).',f'Permanent archive: [10.5281/zenodo.22876602]({DOI}). All 15 deposited files were verified against the release sizes and checksums. [Public Linux reproduction run](https://github.com/aleetreny/Shape-of-Science-Reproducibility/actions/runs/35610529164).');p.write_text(s)
p=ROOT/'data/compact_release_v1/package/README.md';s=p.read_text().replace('Dataset identifier (reserved; archival transfer in progress):','Permanent dataset identifier:').replace('The same assets are being transferred to the DOI archive above; GitHub downloads are already public.','The same assets are archived with the DOI above; both download routes are public.');p.write_text(s)
p=HERE/'live_state.json';d=json.loads(p.read_text());d.update({'stage':'Complete: public GitHub release, DOI archive and manuscript availability verified','published_doi':True,'pdf_edits_prepared_not_applied':False,'pdf_updates_applied':True});p.write_text(json.dumps(d,indent=2)+'\n')
for name in ['docs/AVAILABILITY_AFTER_PUBLICATION.md','docs/REPRODUCING.md','reproducibility/DATA_DICTIONARY.md']:
 p=ROOT/name
 saved=HERE/'superseded'/name
 if p.exists() and not saved.exists():
  saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(p.read_bytes())
 if name=='docs/AVAILABILITY_AFTER_PUBLICATION.md':
  p.write_text(f'# Disponibilidad aplicada al manuscrito\n\nEl depósito está publicado: [{DOI}]({DOI}). Las declaraciones vigentes ya están integradas en [el artículo inglés](../manuscript/main.tex) y [la copia española](../manuscript_es/main.tex), con la cita formal del conjunto de datos y el detalle de S8.\n\nEl alcance y los comandos comprobados están en [COMPACT_REPRODUCIBILITY.md](../COMPACT_REPRODUCIBILITY.md). Se repiten comparaciones desde medidas congeladas; no se certifica una nueva inferencia completa desde textos históricos. La plantilla anterior se conserva en el directorio de auditoría.\n')
 else:
  p.write_text(f'**Ruta pública vigente, 21-09-2026:** [distribución compacta con DOI]({DOI}) y [comandos y límites](../COMPACT_REPRODUCIBILITY.md). Los inventarios y comandos históricos siguientes pueden referirse a cachés locales excluidas; para la entrega pública debe seguirse el README de la versión 1.1.0.\n\n'+p.read_text())
print('Delivery notes updated from the verified public record.')
