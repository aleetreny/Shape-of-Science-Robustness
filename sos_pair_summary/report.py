"""Presentation only: does not recompute or classify scientific observations."""
import csv
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/field_pair_summary_v1'
DATA = ROOT / 'data/field_pair_summary_v1'
COLORS = {'unanimous': '#0072B2', 'contradiction': '#D55E00', 'unresolved': '#B7BDC3'}
LABELS = {'unanimous': 'Misma dirección en todos', 'contradiction': 'Direcciones opuestas persistentes',
          'unresolved': 'Sin conclusión común clara'}
METRICS = {'angle_p50': 'Apertura de la nube', 'pr': 'Reparto entre direcciones (PR)'}
SHORT_FIELDS = ['Agricultura y biología', 'Artes y humanidades', 'Bioquímica y genética',
    'Empresa y gestión', 'Ingeniería química', 'Química', 'Informática', 'Decisiones',
    'Tierra y planetas', 'Economía y finanzas', 'Energía', 'Ingeniería', 'Medio ambiente',
    'Inmunología', 'Materiales', 'Matemáticas', 'Medicina', 'Neurociencia', 'Enfermería',
    'Farmacología', 'Física y astronomía', 'Psicología', 'Ciencias sociales',
    'Veterinaria', 'Odontología', 'Profesiones sanitarias']


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def table(name):
    with (OUT / (name + '.csv')).open() as f: return list(csv.DictReader(f))


def save(fig, name):
    for ext in ['png', 'pdf', 'svg']:
        fig.savefig(OUT / (name + '.' + ext), dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def main():
    audit = json.loads((DATA / 'audit.json').read_text())
    assert audit['all_complete']
    for name, digest in audit['files'].items(): assert sha(ROOT / name) == digest, name
    assert json.loads((DATA / 'independent_audit.json').read_text())['all_complete']
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'axes.spines.top': False, 'axes.spines.right': False})
    summaries = table('classification_summary')
    fig, axes = plt.subplots(1, 2, figsize=(13.7, 4.5), sharey=True)
    for ax, (metric, title) in zip(axes, METRICS.items()):
        rows = [r for r in summaries if r['metric'] == metric and r['rule'] == 'all_saved']
        rows.sort(key=lambda r: float(r['minimum_relative_difference']))
        bottom = np.zeros(4)
        for cls in COLORS:
            counts = np.array([int(r[cls]) for r in rows])
            ax.barh(range(4), counts, left=bottom, color=COLORS[cls], height=.64)
            for i, count in enumerate(counts):
                if count >= 8:
                    ax.text(bottom[i] + count / 2, i, str(count), ha='center', va='center',
                            color='white' if cls != 'unresolved' else '#24292F', fontsize=7 if count < 17 else 11, fontweight='bold')
            bottom += counts
        ax.set_title(title, pad=15, fontsize=14)
        ax.set_xlim(0, 325); ax.set_xticks([0, 65, 130, 195, 260, 325])
        ax.set_xlabel('Parejas de disciplinas (325 en cada fila)')
        ax.set_yticks(range(4), ['Cualquier diferencia', 'Más del 1%', 'Más del 5%', 'Más del 10%'])
        ax.grid(axis='x', alpha=.18); ax.set_axisbelow(True)
    axes[0].invert_yaxis()
    fig.suptitle('Cuántas conclusiones se mantienen al cambiar de modelo', fontsize=17, y=1.04)
    fig.text(.5, .96, 'Diez modelos · dirección persistente en el principal y las 25 selecciones adicionales', ha='center', fontsize=11)
    fig.legend(handles=[Patch(color=COLORS[c], label=LABELS[c]) for c in COLORS],
               loc='lower center', bbox_to_anchor=(.5, -.13), ncol=3, frameon=False)
    fig.text(.5, -.17, 'El porcentaje es una diferencia relativa simétrica; los cortes son sensibilidades, no pruebas de significación.', ha='center', fontsize=10)
    fig.subplots_adjust(top=.83, bottom=.16, wspace=.10)
    save(fig, '01_conclusions_and_magnitude')

    pair_rows = table('pair_summary')
    fields = sorted({int(r[k]) for r in pair_rows for k in ['field_a', 'field_b']})
    assert fields == list(range(11, 37)) and len(SHORT_FIELDS) == 26
    position = {field: i for i, field in enumerate(fields)}
    fig, axes = plt.subplots(1, 2, figsize=(16.5, 10.4), sharex=True, sharey=True)
    cmap = ListedColormap([COLORS[k] for k in COLORS]); cmap.set_bad('white')
    label_to_value = {key: i for i, key in enumerate(COLORS)}
    ticks = [f'{i+1:02d}' for i in range(26)]
    for ax, (metric, title) in zip(axes, METRICS.items()):
        arr = np.full((26, 26), np.nan)
        for row in pair_rows:
            if row['metric'] == metric:
                i, j = position[int(row['field_a'])], position[int(row['field_b'])]
                arr[i, j] = label_to_value[row['class']]
        ax.imshow(np.ma.masked_invalid(arr), cmap=cmap, vmin=0, vmax=2, interpolation='none')
        ax.set_title(title, fontsize=15, pad=16)
        ax.set_xticks(range(26), ticks, rotation=90, fontsize=8)
        ax.set_yticks(range(26), [f'{i+1:02d}  {name}' for i, name in enumerate(SHORT_FIELDS)], fontsize=10)
        ax.set_xticks(np.arange(-.5, 26, 1), minor=True); ax.set_yticks(np.arange(-.5, 26, 1), minor=True)
        ax.grid(which='minor', color='white', linewidth=.65); ax.tick_params(which='minor', length=0)
        for spine in ax.spines.values(): spine.set_visible(False)
    fig.suptitle('Qué comparaciones se conservan entre disciplinas', fontsize=19, y=.98)
    fig.text(.5, .933, 'Recetas principales · cualquier diferencia con dirección persistente · cada casilla es una pareja de áreas', ha='center', fontsize=11)
    fig.legend(handles=[Patch(color=COLORS[c], label=LABELS[c]) for c in COLORS],
               loc='lower center', bbox_to_anchor=(.5, .055), ncol=3, frameon=False)
    fig.text(.5, .025, 'Blanco: diagonal o pareja ya representada. Acuerdo no significa que la descripción sea temáticamente correcta.', ha='center', fontsize=10)
    fig.subplots_adjust(left=.19, right=.98, top=.89, bottom=.13, wspace=.065)
    save(fig, '02_all_field_pairs')

    files = {p.name: sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'catalog.json'}
    catalog = {'created_at': datetime.now(timezone.utc).isoformat(), 'files': files,
               'report_source_sha256': sha(Path(__file__)), 'scientific_audit_sha256': sha(DATA / 'audit.json'),
               'independent_audit_sha256': sha(DATA / 'independent_audit.json')}
    (OUT / 'catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'files': len(files), 'tables': 12, 'figures': 2}))


if __name__ == '__main__': main()
