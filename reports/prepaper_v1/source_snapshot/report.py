"""Rebuild presentation from the sealed atlas; never recompute scientific results."""
import csv
import json
import shutil
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pyarrow.parquet as pq

from sos_deep.artifacts import ROOT, read_csv, save_csv, verify_audit
from sos_embed.storage import file_sha, write_json

DATA = ROOT / 'data/prepaper_v1/case_atlas'
OUT = ROOT / 'reports/prepaper_v1'
MODELS = list(json.loads((ROOT / 'config/analysis_v1.json').read_text())['poolings'])
NOTES = {
    99305: 'Etiqueta temática incompatible con el resumen: infección bacteriana clasificada en política.',
    202595: 'Etiqueta y tipo problemáticos: descripción de un libro de historia clasificada en física.',
    93549: 'Announcement: texto de reseña de atlas clínico; marca de aviso no detectada en la limpieza original.',
    115771: 'Economía de la persuasión; su adscripción a Safety Research merece cautela.',
    452340: 'Educación matemática dentro de Applied Mathematics; grupo administrativo, no verdad externa.',
    349858: 'Resumen comienza a mitad de una frase y tiene menos de 80 palabras; cautela interpretativa.',
    327954: 'Resumen con bastante código de fórmulas; posible factor de entrada, sin prueba causal.'
}


def save_figure(fig, stem):
    for suffix in ['png', 'pdf', 'svg']:
        fig.savefig(OUT / 'figures' / (stem + '.' + suffix), dpi=300, facecolor='white')
    plt.close(fig)


def main():
    audit = verify_audit(DATA)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'figures').mkdir(exist_ok=True)
    (OUT / 'source_snapshot').mkdir(exist_ok=True)
    shutil.copyfile(__file__, OUT / 'source_snapshot/report.py')
    for name in ['subfields.csv', 'subfield_sensitivity_panels.csv', 'subfield_examples.csv',
                 'paper_examples.csv', 'paper_example_pairs.csv', 'article_relation_examples.csv',
                 'subfield_relation_examples.csv']:
        shutil.copyfile(DATA / name, OUT / name)
    texts = json.loads((DATA / 'case_texts_local.json').read_text())
    papers = read_csv(DATA / 'paper_examples.csv')
    edges = read_csv(DATA / 'article_relation_examples.csv')
    enriched = []
    for r in papers:
        enriched.append({**r, 'title': texts[r['row_index']]['title'], 'doi': texts[r['row_index']]['doi'],
                         'review_note': NOTES.get(int(r['row_index']), 'Sin incidencia clara en esta lectura; no es validación experta.')})
    save_csv(OUT / 'paper_examples_readable.csv', enriched)
    edge_rows = []
    for r in edges:
        s, t = texts[r['source_row']], texts[r['target_row']]
        edge_rows.append({**r, 'source_work_id': s['work_id'], 'target_work_id': t['work_id'],
            'source_title': s['title'], 'target_title': t['title'], 'source_doi': s['doi'], 'target_doi': t['doi'],
            'source_review_note': NOTES.get(int(r['source_row']), ''), 'target_review_note': NOTES.get(int(r['target_row']), '')})
    save_csv(OUT / 'article_relations_readable.csv', edge_rows)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.labelsize': 8.5,
        'axes.titlesize': 10, 'axes.spines.top': False, 'axes.spines.right': False,
        'pdf.fonttype': 42, 'svg.fonttype': 'none'})
    sf = read_csv(DATA / 'subfield_examples.csv')
    fig, ax = plt.subplots(figsize=(7, 6.2))
    fig.subplots_adjust(left=.48, right=.97, bottom=.21, top=.88)
    for i, r in enumerate(sf):
        color = '#197a78' if r['tail'] == 'higher' else '#b76635'
        a, b = 100 * float(r['worst_percentile']), 100 * float(r['best_percentile'])
        ax.plot([a, b], [i, i], lw=3, color=color, solid_capstyle='round')
        ax.scatter([a, b], [i, i], color=color, s=18, zorder=3)
    ax.set_yticks(range(12), ['\n'.join(textwrap.wrap(r['name'], 37)) for r in sf])
    ax.invert_yaxis()
    ax.set_xlim(0, 102)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.axhline(5.5, color='#d8dde4', lw=.8)
    ax.set_xlabel('Relative agreement ranking (%)\nLower agreement ← → Higher agreement')
    ax.grid(axis='x', color='#e8ebef', lw=.7)
    ax.set_axisbelow(True)
    fig.text(.045, .95, 'Where neighborhood agreement persists', fontsize=13, weight='bold')
    fig.text(.045, .91, 'Rank ranges across 27 size, pooling and neighbor-count settings', fontsize=9, color='#4a5666')
    fig.text(.045, .035, 'Same 183 Subfields in every setting. Ranges are sensitivity checks, not confidence intervals.\nTwelve examples selected by a fixed rule; higher agreement does not mean greater semantic accuracy.', fontsize=7.5, color='#4a5666')
    save_figure(fig, '01_subfield_persistence')
    # All twelve fixed sources are shown, including the problematic records discovered on inspection.
    values = np.array([[float(next(e for e in edges if e['source_row'] == r['row_index'] and e['relation'] == 'encoder_dependent')[m + '_support']) for m in MODELS] for r in papers])
    fig, ax = plt.subplots(figsize=(7, 6.1))
    fig.subplots_adjust(left=.39, right=.98, bottom=.25, top=.86)
    im = ax.imshow(values, vmin=0, vmax=1, cmap='viridis', aspect='auto')
    labels = ['SIRT6 / cancer ‡', 'Mathematics education †', 'State-owned businesses', 'Petrol dispatch',
              'Persuasive talk †', 'Pedestrian injuries', 'Invasion Strategy †', 'Witch trials †',
              'Cobalt / silica layers', 'Announcement †', 'Expert-system conversion', 'Arthurian poetry']
    ax.set_yticks(range(12), labels)
    ax.set_xticks(range(10), MODELS, rotation=55, ha='right', fontsize=8)
    for i in range(12):
        for j in range(10):
            ax.text(j, i, str(round(values[i, j] * 10)), ha='center', va='center', fontsize=7,
                    color='white' if values[i, j] < .6 else '#17263b')
    ax.axhline(5.5, color='white', lw=2)
    fig.text(.045, .95, 'The same link can depend on the encoder', fontsize=13, weight='bold')
    fig.text(.045, .91, 'Most encoder-dependent eligible link for each of the twelve fixed paper examples', fontsize=8.5, color='#4a5666')
    fig.text(.045, .043, 'Cells: repetitions with the target among the 25 nearest papers (0–10); targets listed in the CSV.\n256 candidates; endpoints always eligible. Upper/lower six rows: high/low-agreement sources.\n† Source/label caveat. ‡ Target abstract is incomplete. See individual case notes.\nEach link is selected for maximal model disagreement; this panel does not measure its prevalence.', fontsize=7.5, color='#4a5666')
    save_figure(fig, '02_relation_dependence')
    lines = ['# Artículos y relaciones concretas', '', 'Los doce artículos se eligieron por reglas numéricas antes de leer sus títulos. Se conservan los casos problemáticos y se anotan; no se sustituyen por ejemplos más cómodos.', '',
             'Cada intervalo cubre diez selecciones de 256 candidatos dentro del Subfield. La cifra es el promedio de coincidencia de los 25 vecinos entre las 45 parejas de modelos. No es calidad del artículo ni probabilidad poblacional.', '']
    for r in enriched:
        idx = r['row_index']
        lines += ['## ' + r['title'], '', f"[{r['work_id']}](https://openalex.org/{r['work_id']}) · {r['subfield_display_name']} · {r['publication_year']}", '',
            f"Coincidencia entre modelos: **{100*float(r['k25_mean']):.1f}%**; rango al cambiar candidatos: **{100*float(r['k25_min']):.1f}–{100*float(r['k25_max']):.1f}%**.", '', r['review_note'], '']
        for e in (e for e in edge_rows if e['source_row'] == idx):
            name = 'Relación más repetida' if e['relation'] == 'recurrent' else 'Relación con mayor diferencia entre modelos'
            supports = '; '.join(m + ': ' + str(round(float(e[m + '_support']) * 10)) + '/10' for m in MODELS)
            lines += [f"**{name}:** [{e['target_title']}](https://openalex.org/{e['target_work_id']}).", '', supports + '.', '']
            if e['target_review_note']:
                lines += [e['target_review_note'], '']
    lines += ['## Cómo leer estos ejemplos', '', 'Que la misma relación aparezca en los dos apartados es posible: el enlace más repetido puede seguir siendo muy dependiente del encoder. Coincidencia no significa verdad. Una relación siempre presente en estas muestras no tiene por qué conservarse al buscar entre los 500.000 artículos.', '',
              'Los resúmenes completos se conservan solo en `data/prepaper_v1/case_atlas/case_texts_local.json`; aquí se enlazan IDs y se muestran títulos. No se ha publicado el corpus.']
    (OUT / 'CASES.md').write_text('\n'.join(lines) + '\n')
    write_json(OUT / 'catalog.json', {'source_audit_sha256': file_sha(DATA / 'audit.json'),
        'exporter_sha256': file_sha(Path(__file__)), 'visual_review': 'pending',
        'files': {str(p.relative_to(OUT)): file_sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'catalog.json'}})
    print('Prepared atlas presentation', OUT)


if __name__ == '__main__':
    main()
