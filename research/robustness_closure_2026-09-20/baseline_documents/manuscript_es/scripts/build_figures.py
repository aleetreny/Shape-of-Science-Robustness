"""Presentation only: copy saved chart data and redraw at manuscript size.

No embedding, neighbour search, new simulation or scientific threshold is run.
The group means/medians below are the same descriptive reductions used by the
sealed presentation exporters. Every input and displayed value is catalogued.
"""
from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import json
import shutil
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'manuscript_es'
ROB = 'reports/robustness_v2/final/tables/'
MOR = 'reports/morphology_pilot_v1/'
PAIR = 'reports/field_pair_summary_v1/'
ATLAS = 'reports/prepaper_v1/'
MODELS = ['specter', 'specter2', 'scincl', 'scibert', 'bert', 'mpnet', 'minilm', 'pubmedbert', 'biobert', 'simcse']
NAMES = ['SPECTER', 'SPECTER2', 'SciNCL', 'SciBERT', 'BERT', 'MPNet', 'MiniLM', 'PubMedBERT', 'BioBERT', 'SimCSE']
(BLUE, ORANGE, GREEN, RED, GRAY) = ('#0072B2', '#D55E00', '#009E73', '#CC79A7', '#B7BDC3')
SHORT = ['Agricultura / biología', 'Artes / humanidades', 'Bioquímica / genética', 'Negocios / gestión', 'Ingeniería química', 'Química', 'Informática', 'Ciencias de la decisión', 'Tierra / planetas', 'Economía / finanzas', 'Energía', 'Ingeniería', 'Ciencias ambientales', 'Inmunología / microbiología', 'Ciencia de materiales', 'Matemáticas', 'Medicina', 'Neurociencia', 'Enfermería', 'Farmacología / toxicología', 'Física / astronomía', 'Psicología', 'Ciencias sociales', 'Veterinaria', 'Odontología', 'Profesiones sanitarias']
SPANISH_LABELS = {'Observed groups': 'Grupos observados', 'Random groups': 'Grupos aleatorios', 'Corrected CKA': 'CKA corregida', 'A  Between group centres': 'A  Entre centros', 'B  Within groups': 'B  Dentro de los grupos', '26 Fields': '26 áreas', 'Same 183 Subfields': 'Mismas 183 especialidades', 'Articles per group': 'Artículos por grupo', 'Higher within Subfield (90)': 'Mayor en especialidad (90)', 'Lower within Subfield (127)': 'Menor en especialidad (127)', 'Neighbour overlap within the parent Field': 'Coincidencia de vecinos en el área', 'Neighbour overlap within the Subfield': 'Coincidencia de vecinos en la especialidad', 'A  Shape change': 'A  Cambio de forma', 'B  Neighbour change': 'B  Cambio de vecinos', '1 - corrected CKA': '1 - CKA corregida', 'Fraction of 25 neighbours changed': 'Fracción de 25 vecinos sustituidos', 'A  Angular spread': 'A  Apertura angular', 'B  Effective linear dimension (PR)': 'B  Dimensión lineal efectiva (PR)', 'Field pairs (325 for each property)': 'Parejas de áreas (325 por propiedad)', 'All ten agree': 'Acuerdo de los diez', 'Persistent opposition': 'Oposición persistente', 'Unresolved': 'Sin resolver', 'Flagged input contrasts (out of 520)': 'Contrastes de entrada con alerta (de 520)', 'Media Technology': 'Tecnología de medios', 'Building and Construction': 'Edificación y construcción', 'Renewable Energy, Sustainability and the Environment': 'Energía renovable, sostenibilidad y medio ambiente', 'Toxicology': 'Toxicología', 'Automotive Engineering': 'Ingeniería del automóvil', 'Water Science and Technology': 'Ciencia y tecnología del agua', 'Algebra and Number Theory': 'Álgebra y teoría de números', 'Religious studies': 'Estudios religiosos', 'Numerical Analysis': 'Análisis numérico', 'History': 'Historia', 'Literature and Literary Theory': 'Literatura y teoría literaria', 'Geometry and Topology': 'Geometría y topología', 'SIRT6 / cancer [b]': 'SIRT6 / cáncer [b]', 'Mathematics education [a]': 'Enseñanza matemática [a]', 'State-owned businesses': 'Empresas estatales', 'Petrol dispatch': 'Distribución de combustible', 'Persuasive talk [a]': 'Persuasión [a]', 'Pedestrian injuries': 'Lesiones de peatones', 'Invasion Strategy [a]': 'Estrategia de invasión [a]', 'Witch trials [a]': 'Juicios de brujería [a]', 'Cobalt / silica layers': 'Cobalto / capas de sílice', 'Announcement [a]': 'Anuncio [a]', 'Expert-system conversion': 'Conversión de sistema experto', 'Arthurian poetry': 'Poesía artúrica', 'Equal group size': 'Tamaño igualado', '2,048 candidates': '2.048 candidatos', 'All candidates': 'Todos los candidatos', 'A  Shape': 'A  Forma', 'B  Neighbours': 'B  Vecinos', 'Change from 2000-04': 'Cambio desde 2000-04', 'Observed / ten models': 'Observada / diez modelos', 'Balanced / ten models': 'Equilibrada / diez modelos', 'Observed / eight models': 'Observada / ocho modelos', 'Balanced / eight models': 'Equilibrada / ocho modelos', 'A  Shape: corrected CKA': 'A  Forma: CKA corregida', 'B  Neighbour overlap at k = 25': 'B  Coincidencia de vecinos con k = 25', 'Medicine': 'Medicina', 'Energy*': 'Energía*', 'Mathematics': 'Matemáticas', 'Physics': 'Física', 'A  Mean': 'A  Media', 'B  Linear dimension': 'B  Dimensión lineal', 'C  Connection': 'C  Conexión', 'Articles per Field': 'Artículos por área', 'Change from n = 2,000 (%)': 'Cambio respecto a n = 2.000 (%)', 'Quality flags': 'Marcas de calidad', 'Common fragment': 'Fragmento común', 'Abstract only': 'Solo resumen', 'Title only': 'Solo título', 'Word BERTs: CLS': 'BERT de palabras: CLS', 'Word BERTs: SEP': 'BERT de palabras: SEP', 'Global centring': 'Centrado global', 'A  Spread': 'A  Apertura', 'B  Dimension': 'B  Dimensión', 'Spearman agreement of Field rankings': 'Acuerdo de rangos de áreas (Spearman)', 'One round cloud': 'Nube redonda', 'One narrow cloud': 'Nube estrecha', 'One wide cloud': 'Nube ancha', 'One elongated cloud': 'Nube alargada', 'One low-rank cloud': 'Nube de rango bajo', 'Two separated groups': 'Dos grupos separados', 'Four separated groups': 'Cuatro grupos separados', 'Two groups with bridges': 'Dos grupos con puentes', 'One cloud with outliers': 'Nube con puntos atípicos', 'A  Spectral gap': 'A  Brecha espectral', 'B  Radius ratio': 'B  Cociente de radios', 'C  Edge ratio': 'C  Cociente de aristas', 'Agriculture / biology': 'Agricultura / biología', 'Arts / humanities': 'Artes / humanidades', 'Biochemistry / genetics': 'Bioquímica / genética', 'Business / management': 'Negocios / gestión', 'Chemical engineering': 'Ingeniería química', 'Chemistry': 'Química', 'Computer science': 'Informática', 'Decision sciences': 'Ciencias de la decisión', 'Earth / planetary science': 'Tierra / planetas', 'Economics / finance': 'Economía / finanzas', 'Energy': 'Energía', 'Engineering': 'Ingeniería', 'Environmental science': 'Ciencias ambientales', 'Immunology / microbiology': 'Inmunología / microbiología', 'Materials science': 'Ciencia de materiales', 'Neuroscience': 'Neurociencia', 'Nursing': 'Enfermería', 'Pharmacology / toxicology': 'Farmacología / toxicología', 'Physics / astronomy': 'Física / astronomía', 'Psychology': 'Psicología', 'Social sciences': 'Ciencias sociales', 'Veterinary': 'Veterinaria', 'Dentistry': 'Odontología', 'Health professions': 'Profesiones sanitarias', '26 Field\ncentres': '26\náreas', '217 Subfield\ncentres': '217\nespecial.', '26 Subfield\ncentres': '26\nespecial.', 'Change\nmodel': 'Cambiar\nmodelo', 'Remove\nabstract': 'Quitar\nresumen', 'Remove\ntitle': 'Quitar\ntítulo', 'Minimum\nrelative difference': 'Diferencia\nrelativa mínima', '20 selections\nOriginal check': '20 selecciones\nControl original', '100 selections\nAdditional check': '100 selecciones\nControl adicional', 'Relative agreement rank (%)\nLower agreement to higher agreement': 'Posición relativa de acuerdo (%)\nDe menor a mayor acuerdo', 'Upper triangle: angular spread\nLower triangle: effective linear dimension': 'Triángulo superior: apertura angular\nTriángulo inferior: dimensión lineal efectiva'}
MANIFEST = {}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.labelsize': 9, 'axes.titlesize': 10, 'legend.fontsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8, 'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42, 'svg.fonttype': 'none', 'svg.hashsalt': 'sos-layout-v1', 'figure.facecolor': 'white', 'savefig.facecolor': 'white'})

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(item, relative):
    path = ROOT / relative
    target = OUT / 'figures' / 'data' / item / path.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copyfile(path, target)
    with target.open() as stream:
        rows = list(csv.DictReader(stream))
    entry = {'source': relative, 'included': str(target.relative_to(OUT)), 'sha256': sha(target), 'rows': len(rows)}
    MANIFEST.setdefault(item, {'sources': [], 'displayed_values': {}})['sources'].append(entry)
    return rows

def values(item, name, value):
    MANIFEST[item]['displayed_values'][name] = value

def grouped(rows, keys, value):
    g = defaultdict(list)
    for row in rows:
        g[tuple((row[k] for k in keys))].append(float(row[value]))
    return {key: float(np.mean(vals)) for (key, vals) in g.items()}

def save(item, fig):
    from matplotlib.ticker import ScalarFormatter, FuncFormatter
    for axis in fig.axes:
        for dimension in (axis.xaxis, axis.yaxis):
            formatter = dimension.get_major_formatter()
            if isinstance(formatter, ScalarFormatter):
                dimension.set_major_formatter(FuncFormatter(lambda value, position: format(value, 'g').replace('.', ',')))
    paths = []
    for ext in ('pdf', 'svg', 'png', 'tiff'):
        path = OUT / 'figures' / f'{item}.{ext}'
        kwargs = {'metadata': {'CreationDate': None}} if ext == 'pdf' else {}
        if ext == 'svg':
            kwargs = {'metadata': {'Date': None}}
        if ext == 'tiff':
            kwargs = {'pil_kwargs': {'compression': 'tiff_lzw'}}
        fig.savefig(path, dpi=300, **kwargs)
        paths.append(str(path.relative_to(OUT)))
    MANIFEST[item]['files'] = paths
    MANIFEST[item]['size_inches'] = list(fig.get_size_inches())
    plt.close(fig)

def main_figures():
    item = 'figure_01'
    r = read(item, 'data/robustness_v2/centroid_scales/comparisons.csv')
    means = grouped(r, ['condition', 'groups'], 'cka_debiased')
    inner = read(item, ROB + 'structure_matched_size_agreement.csv')
    (fig, axes) = plt.subplots(1, 2, figsize=(6.8, 3.75))
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.29, top=0.84, wspace=0.48)
    conditions = ['matched_field', 'matched_subfield', 'one_subfield_per_field']
    x = np.arange(3)
    for (off, group, label, color) in [(-0.18, 'real', 'Grupos observados', BLUE), (0.18, 'random_period_preserved', 'Grupos aleatorios', GRAY)]:
        y = [means[c, group] for c in conditions]
        axes[0].bar(x + off, y, 0.35, label=label, color=color)
        values(item, group, y)
    axes[0].set(xticks=x, xticklabels=['26\náreas', '217\nespecial.', '26\nespecial.'], ylim=(0, 1), ylabel='CKA corregida', title='A  Entre centros')
    axes[0].legend(loc='upper left', bbox_to_anchor=(-0.1, -0.24), ncol=2, frameon=False)
    spread = []
    for (level, label, color, offset, marker) in [('field', '26 áreas', BLUE, -0.18, 'o'), ('subfield', 'Mismas 183 especialidades', ORANGE, 0.18, '^')]:
        selected = [next((a for a in inner if a['population'] == 'same_183_subfields' and a['recipe'] == 'mean' and (a['level'] == level) and (a['selection'] == str(n)) and (a['measure'] == 'shape'))) for n in (128, 256, 512)]
        y = np.arange(3) + offset
        means_inner = [float(a['mean']) for a in selected]
        low = [float(a['p025']) for a in selected]
        high = [float(a['p975']) for a in selected]
        axes[1].hlines(y, low, high, color=color, linewidth=2, alpha=0.55)
        axes[1].scatter(means_inner, y, color=color, marker=marker, s=27, label=label, zorder=3)
        for (a, mean_value, yy) in zip(selected, means_inner, y):
            axes[1].annotate(format(mean_value, '.3f').replace('.', ','), (mean_value, yy), xytext=(0, -10 if offset > 0 else 6), textcoords='offset points', ha='center', fontsize=6.6, color=color)
            spread.append({'level': level, 'selection': int(a['selection']), 'n': int(a['n']), 'mean': mean_value, 'p025': float(a['p025']), 'p975': float(a['p975'])})
        values(item, level, means_inner)
    values(item, 'within_group_spread', spread)
    axes[1].set(yticks=[0, 1, 2], yticklabels=['128', '256', '512'], ylim=(2.6, -0.6), xlim=(0, 1), xticks=[0, 0.2, 0.4, 0.6, 0.8, 1], xlabel='CKA corregida', ylabel='Artículos por grupo', title='B  Dentro de los grupos')
    axes[1].legend(frameon=False, loc='upper left', bbox_to_anchor=(-0.14, -0.27), fontsize=6.5)
    axes[0].grid(axis='y', alpha=0.15)
    axes[1].grid(axis='x', alpha=0.15)
    for ax in axes:
        ax.set_axisbelow(True)
    save(item, fig)
    item = 'figure_02'
    r = read(item, ROB + 'structure_paired_scope_changes.csv')
    r = [x for x in r if x['k'] == '25']
    a = grouped(r, ['subfield_id', 'field_id'], 'field')
    b = grouped(r, ['subfield_id', 'field_id'], 'subfield')
    (fig, ax) = plt.subplots(figsize=(6.1, 4.8))
    fig.subplots_adjust(left=0.15, right=0.97, bottom=0.14, top=0.96)
    points = []
    for (higher, label, color, marker) in [(True, 'Mayor en especialidad (90)', BLUE, '^'), (False, 'Menor en especialidad (127)', ORANGE, 'o')]:
        keys = [k for k in a if (b[k] > a[k]) == higher]
        assert len(keys) == (90 if higher else 127)
        ax.scatter([a[k] for k in keys], [b[k] for k in keys], s=21, marker=marker, color=color, alpha=0.78, label=label, zorder=3)
        points += [{'subfield_id': k[0], 'field_id': k[1], 'x': a[k], 'y': b[k]} for k in keys]
    assert len(points) == 217
    ax.plot([0.25, 0.75], [0.25, 0.75], '--', color='#697683', linewidth=1)
    ax.set(xlim=(0.25, 0.75), ylim=(0.25, 0.75), xlabel='Coincidencia de vecinos en el área', ylabel='Coincidencia de vecinos en la especialidad')
    ax.set_aspect('equal')
    ax.grid(alpha=0.15)
    ax.legend(frameon=False, loc='upper left')
    ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    values(item, 'points', points)
    save(item, fig)
    item = 'figure_03'
    r = read(item, ROB + 'input_input_effect_by_field.csv')
    (fig, axes) = plt.subplots(1, 2, figsize=(6.8, 3.8))
    fig.subplots_adjust(left=0.09, right=0.98, top=0.86, bottom=0.22, wspace=0.34)
    for (ax, metric, title) in zip(axes, ['cka', 'neighbors25'], ['A  Cambio de forma', 'B  Cambio de vecinos']):
        data = [[float(a['mean']) for a in r if a['metric'] == metric and a['input_condition'] == cond and (a['measure'] == measure)] for (cond, measure) in [('title', 'model_change_at_full'), ('title', 'input_change_from_full'), ('abstract', 'input_change_from_full')]]
        assert all((len(v) == 26 for v in data))
        ax.boxplot(data, positions=[0, 1, 2], widths=0.5, showfliers=False, patch_artist=True, boxprops={'facecolor': '#E8EFF4'}, medianprops={'color': '#233746'})
        for (i, v) in enumerate(data):
            ax.scatter(i + np.linspace(-0.12, 0.12, len(v)), v, s=11, color=[BLUE, ORANGE, GREEN][i], alpha=0.7, zorder=3)
        ax.set(xticks=[0, 1, 2], xticklabels=['Cambiar\nmodelo', 'Quitar\nresumen', 'Quitar\ntítulo'], ylabel='1 - CKA corregida' if metric == 'cka' else 'Fracción de 25 vecinos sustituidos', title=title, ylim=(0, 1 if metric == 'neighbors25' else 0.85))
        ax.grid(axis='y', alpha=0.15)
        values(item, metric, data)
    save(item, fig)
    item = 'figure_04'
    r = read(item, PAIR + 'classification_summary.csv')
    (fig, axes) = plt.subplots(2, 1, figsize=(6.8, 4.75))
    fig.subplots_adjust(left=0.13, right=0.98, bottom=0.19, top=0.93, hspace=0.55)
    for (ax, metric, title) in zip(axes, ['angle_p50', 'pr'], ['A  Apertura angular', 'B  Dimensión lineal efectiva (PR)']):
        rows = sorted([x for x in r if x['metric'] == metric and x['rule'] == 'all_saved'], key=lambda x: float(x['minimum_relative_difference']))
        left = np.zeros(4)
        for (key, color) in [('unanimous', BLUE), ('contradiction', ORANGE), ('unresolved', GRAY)]:
            vv = np.array([int(x[key]) for x in rows])
            ax.barh(range(4), vv, left=left, color=color, height=0.68)
            for (y, (start, val)) in enumerate(zip(left, vv)):
                if val:
                    ax.text(start + val / 2, y, str(val), ha='center', va='center', fontsize=8, color='white' if key != 'unresolved' else '#202B36')
            left += vv
        assert np.all(left == 325)
        ax.set(yticks=range(4), yticklabels=['0%', '1%', '5%', '10%'], xlim=(0, 325), xticks=[0, 100, 200, 325], ylabel='Diferencia\nrelativa mínima', title=title)
        ax.invert_yaxis()
        ax.spines[['left', 'bottom']].set_visible(False)
        ax.tick_params(length=0)
        values(item, metric, rows)
    axes[1].set_xlabel('Parejas de áreas (325 por propiedad)')
    fig.legend(handles=[Patch(color=c, label=l) for (c, l) in [(BLUE, 'Acuerdo de los diez'), (ORANGE, 'Oposición persistente'), (GRAY, 'Sin resolver')]], loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.015))
    save(item, fig)

def supplementary_figures():
    item = 'figure_S01'
    r = read(item, ROB + 'input_alert_transition_counts.csv')
    (fig, ax) = plt.subplots(figsize=(6.6, 3.6))
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.2, top=0.94)
    for (offset, size, color) in [(-0.17, '26k', ORANGE), (0.17, '52k', BLUE)]:
        y = [int(next((a['alerts' + size] for a in r if a['scope'] == 'individual_models' and a['repeats'] == str(rep)))) for rep in (20, 100)]
        bars = ax.bar(np.arange(2) + offset, y, 0.32, color=color, label=size)
        ax.bar_label(bars, padding=3)
        values(item, size, y)
    ax.set(xticks=[0, 1], xticklabels=['20 selecciones\nControl original', '100 selecciones\nControl adicional'], ylabel='Contrastes de entrada con alerta (de 520)', ylim=(0, 85))
    ax.legend(frameon=False)
    ax.grid(axis='y', alpha=0.15)
    ax.set_axisbelow(True)
    save(item, fig)
    item = 'figure_S02'
    r = read(item, ATLAS + 'subfield_examples.csv')
    (fig, ax) = plt.subplots(figsize=(6.8, 5.5))
    fig.subplots_adjust(left=0.47, right=0.97, bottom=0.14, top=0.96)
    for (i, row) in enumerate(r):
        color = GREEN if row['tail'] == 'higher' else ORANGE
        (a, b) = (100 * float(row['worst_percentile']), 100 * float(row['best_percentile']))
        ax.plot([a, b], [i, i], lw=3, color=color)
        ax.scatter([a, b], [i, i], s=18, color=color)
    ax.set(yticks=range(len(r)), yticklabels=['\n'.join(textwrap.wrap(SPANISH_LABELS.get(x['name'], x['name']), 34)) for x in r], xlim=(0, 102), xticks=[0, 25, 50, 75, 100], xlabel='Posición relativa de acuerdo (%)\nDe menor a mayor acuerdo')
    ax.invert_yaxis()
    ax.axhline(5.5, color=GRAY, linewidth=0.7)
    ax.grid(axis='x', alpha=0.15)
    values(item, 'examples', r)
    save(item, fig)
    item = 'figure_S03'
    papers = read(item, ATLAS + 'paper_examples_readable.csv')
    edges = read(item, ATLAS + 'article_relation_examples.csv')
    matrix = np.array([[float(next((e for e in edges if e['source_row'] == r['row_index'] and e['relation'] == 'encoder_dependent'))[m + '_support']) for m in MODELS] for r in papers])
    (fig, ax) = plt.subplots(figsize=(6.8, 4.95))
    fig.subplots_adjust(left=0.33, right=0.98, bottom=0.24, top=0.96)
    ax.imshow(matrix, vmin=0, vmax=1, cmap='viridis', aspect='auto')
    labels = ['SIRT6 / cáncer [b]', 'Enseñanza matemática [a]', 'Empresas estatales', 'Distribución de combustible', 'Persuasión [a]', 'Lesiones de peatones', 'Estrategia de invasión [a]', 'Juicios de brujería [a]', 'Cobalto / capas de sílice', 'Anuncio [a]', 'Conversión de sistema experto', 'Poesía artúrica']
    ax.set_yticks(range(12), labels)
    ax.set_xticks(range(10), NAMES, rotation=55, ha='right')
    for i in range(12):
        for j in range(10):
            ax.text(j, i, str(round(matrix[i, j] * 10)), ha='center', va='center', fontsize=8, color='white' if matrix[i, j] < 0.6 else '#142738')
    ax.axhline(5.5, color='white', linewidth=2)
    values(item, 'support_out_of_ten', (matrix * 10).tolist())
    save(item, fig)
    item = 'figure_S04'
    rows = read(item, 'data/robustness_v2/temporal_review/trajectories.csv')
    (fig, axes) = plt.subplots(1, 2, figsize=(6.8, 3.6))
    fig.subplots_adjust(left=0.11, right=0.98, top=0.84, bottom=0.26, wspace=0.4)
    for (ax, cases, title) in [(axes[0], [('cka_equal2048', BLUE, 'Tamaño igualado')], 'A  Forma'), (axes[1], [('neighbors_2048_mean_k25', GREEN, '2.048 candidatos'), ('neighbors_all_k25', ORANGE, 'Todos los candidatos')], 'B  Vecinos')]:
        for (outcome, color, label) in cases:
            matrix = []
            for field in range(11, 37):
                subset = [x for x in rows if x['outcome'] == outcome and x['field_id'] == str(field)]
                assert subset
                matrix.append([np.mean([float(r['value_' + str(year)]) for r in subset]) for year in (2000, 2005, 2010, 2015, 2020)])
            matrix = np.array(matrix)
            matrix -= matrix[:, [0]]
            if len(cases) == 1:
                for line in matrix:
                    ax.plot(range(5), line, color=color, alpha=0.15, linewidth=0.7)
            ax.plot(range(5), matrix.mean(0), 'o-', color=color, label=label, linewidth=2, markersize=4)
            values(item, outcome, {'fields': matrix.tolist(), 'mean': matrix.mean(0).tolist()})
        ax.set(xticks=range(5), xticklabels=['2000-04', '2005-09', '2010-14', '2015-19', '2020-24'], ylabel='Cambio desde 2000-04', title=title)
        ax.tick_params(axis='x', rotation=35)
        ax.axhline(0, color=GRAY, linewidth=0.7)
        ax.grid(alpha=0.12)
    (handles, labels) = ([], [])
    for ax in axes:
        (h, l) = ax.get_legend_handles_labels()
        handles += h
        labels += l
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.005), ncol=3, frameon=False, fontsize=8)
    save(item, fig)
    item = 'figure_S05'
    rows = read(item, ROB + 'structure_medicine_composition_summary.csv')
    (fig, axes) = plt.subplots(2, 1, figsize=(6.8, 5.3))
    fig.subplots_adjust(left=0.1, right=0.98, top=0.94, bottom=0.23, hspace=0.45)
    cases = [('observed_eligible_composition', 'all', 'Observada / diez modelos', BLUE), ('equal_subfield_composition', 'all', 'Equilibrada / diez modelos', GREEN), ('observed_eligible_composition', 'without_biomedical', 'Observada / ocho modelos', ORANGE), ('equal_subfield_composition', 'without_biomedical', 'Equilibrada / ocho modelos', RED)]
    for (ax, metric, title) in zip(axes, ['cka_debiased', 'neighbors_k25'], ['A  Forma: CKA corregida', 'B  Coincidencia de vecinos con k = 25']):
        for (j, (condition, group, label, color)) in enumerate(cases):
            r = [next((a for a in rows if a['field_id'] == f and a['condition'] == condition and (a['model_group'] == group) and (a['metric'] == metric))) for f in ['27', '21', '26', '31']]
            y = np.array([float(a['mean']) for a in r])
            lo = np.array([float(a['min']) for a in r])
            hi = np.array([float(a['max']) for a in r])
            ax.bar(np.arange(4) + (j - 1.5) * 0.19, y, 0.18, color=color, label=label, yerr=[y - lo, hi - y], error_kw={'linewidth': 0.7, 'capsize': 2})
            values(item, metric + ':' + condition + ':' + group, r)
        ax.set(xticks=range(4), xticklabels=['Medicina', 'Energía*', 'Matemáticas', 'Física'], ylim=(0, 0.9 if metric == 'cka_debiased' else 0.4), title=title)
        ax.grid(axis='y', alpha=0.15)
        ax.set_axisbelow(True)
    (handles, labels) = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.02))
    save(item, fig)
    item = 'figure_S06'
    rows = read(item, 'reports/analysis_v1/final/tables/shape_all_stages.csv')
    (fig, axes) = plt.subplots(1, 3, figsize=(6.8, 3.55))
    fig.subplots_adjust(left=0.13, right=0.98, top=0.84, bottom=0.32, wspace=0.12)
    for (idx, (ax, stage, title)) in enumerate(zip(axes, ['primary', 'cls', 'sep'], ['A  Media', 'B  CLS', 'C  SEP'])):
        groups = defaultdict(list)
        for row in rows:
            if row['stage'] == stage:
                groups[row['model_a'].split('/')[0], row['model_b'].split('/')[0]].append(float(row['cka_debiased']))
        a = np.eye(10)
        for ((m, n), v) in groups.items():
            (i, j) = (MODELS.index(m), MODELS.index(n))
            a[i, j] = a[j, i] = np.mean(v)
        im = ax.imshow(a, vmin=0, vmax=1, cmap='viridis')
        ax.set_xticks(range(10), [str(i + 1) for i in range(10)], fontsize=7)
        ax.set_yticks(range(10), NAMES if idx == 0 else [], fontsize=7)
        ax.set_title(title)
        values(item, stage, a.tolist())
    cax = fig.add_axes([0.3, 0.13, 0.5, 0.04])
    fig.colorbar(im, cax=cax, orientation='horizontal', label='CKA corregida')
    save(item, fig)
    item = 'figure_S07'
    rows = read(item, MOR + 'sample_size.csv')
    (fig, axes) = plt.subplots(1, 3, figsize=(6.8, 3.85))
    fig.subplots_adjust(left=0.1, right=0.98, top=0.87, bottom=0.35, wspace=0.48)
    for (ax, metric, title) in zip(axes, ['angle_p50', 'pr', 'gap_25'], ['A  Apertura angular', 'B  Dimensión lineal', 'C  Conexión']):
        for (i, model) in enumerate(MODELS):
            vals = [float(np.median([float(r['relative_to_2000']) for r in rows if r['model'] == model and r['metric'] == metric and (r['n'] == str(n))])) for n in (500, 1000, 2000, 4000)]
            y = 100 * (np.array(vals) - 1)
            ax.plot([500, 1000, 2000, 4000], y, marker='o', markersize=2.5, linewidth=1, label=NAMES[i], color=plt.get_cmap('tab10')(i))
            values(item, metric + ':' + model, y.tolist())
        ax.axhline(0, color=GRAY, linestyle='--', linewidth=0.7)
        ax.set_xscale('log', base=2)
        ax.set_xticks([500, 1000, 2000, 4000], ['500', '1k', '2k', '4k'])
        ax.set(title=title, xlabel='Artículos por área')
        ax.grid(alpha=0.15)
    axes[0].set_ylabel('Cambio respecto a n = 2.000 (%)')
    fig.legend(*axes[0].get_legend_handles_labels(), loc='lower center', ncol=5, bbox_to_anchor=(0.5, 0.03), frameon=False, fontsize=7.5, columnspacing=1.1)
    save(item, fig)
    item = 'figure_S08'
    rows = read(item, MOR + 'control_rank_stability.csv')
    kinds = ['quality', 'common', 'abstract', 'title', 'pool_cls', 'pool_sep', 'global_centered']
    labels = ['Marcas de calidad', 'Fragmento común', 'Solo resumen', 'Solo título', 'BERT de palabras: CLS', 'BERT de palabras: SEP', 'Centrado global']
    (fig, axes) = plt.subplots(1, 3, figsize=(6.8, 3.7))
    fig.subplots_adjust(left=0.23, right=0.98, top=0.86, bottom=0.22, wspace=0.21)
    for (i, (ax, metric, title, color)) in enumerate(zip(axes, ['angle_p50', 'pr', 'gap_25'], ['A  Apertura', 'B  Dimensión', 'C  Conexión'], [BLUE, GREEN, ORANGE])):
        for (j, kind) in enumerate(kinds):
            vals = [float(r['field_rank_spearman']) for r in rows if r['metric'] == metric and r['condition'] == kind and r['field_rank_spearman']]
            ax.scatter(vals, [j] * len(vals), s=12, color=color, alpha=0.7)
            ax.plot([min(vals), max(vals)], [j, j], color=color, alpha=0.35)
            values(item, metric + ':' + kind, vals)
        ax.set_yticks(range(7), labels if i == 0 else [])
        ax.invert_yaxis()
        ax.set(xlim=(-1.03, 1.03), xticks=[-1, 0, 1], title=title)
        ax.axvline(0.9, color=GRAY, linestyle='--', linewidth=0.7)
        ax.grid(axis='x', alpha=0.15)
    fig.text(0.6, 0.065, 'Acuerdo de rangos de áreas (Spearman)', ha='center', fontsize=9)
    save(item, fig)
    item = 'figure_S09'
    rows = read(item, 'data/morphology_pilot_v1/synthetic/clouds.csv')
    simnames = {'one_round': 'Nube redonda', 'one_narrow': 'Nube estrecha', 'one_wide': 'Nube ancha', 'one_elongated': 'Nube alargada', 'low_rank': 'Nube de rango bajo', 'two_separated': 'Dos grupos separados', 'four_separated': 'Cuatro grupos separados', 'two_with_bridges': 'Dos grupos con puentes', 'one_with_outliers': 'Nube con puntos atípicos'}
    (fig, axes) = plt.subplots(1, 3, figsize=(6.8, 4.0))
    fig.subplots_adjust(left=0.28, right=0.98, top=0.84, bottom=0.14, wspace=0.27)
    for (i, (ax, metric, title)) in enumerate(zip(axes, ['gap_25', 'connect_ratio90_50', 'mst_max_median'], ['A  Brecha espectral', 'B  Cociente de radios', 'C  Cociente de aristas'])):
        vals = [float(r[metric]) for r in rows]
        ax.barh(range(9), vals, color=[ORANGE if r['cloud'] in ['one_elongated', 'low_rank', 'one_with_outliers'] else BLUE for r in rows])
        ax.set_yticks(range(9), [simnames[r['cloud']] for r in rows] if i == 0 else [])
        ax.invert_yaxis()
        ax.set_title(title)
        ax.grid(axis='x', alpha=0.15)
        ax.set_axisbelow(True)
        values(item, metric, vals)
    save(item, fig)
    item = 'figure_S10'
    rows = read(item, PAIR + 'pair_summary.csv')
    matrix = np.full((26, 26), np.nan)
    counts = defaultdict(int)
    for r in rows:
        (i, j) = (int(r['field_a']) - 11, int(r['field_b']) - 11)
        assert i < j
        target = (i, j) if r['metric'] == 'angle_p50' else (j, i)
        matrix[target] = ['unanimous', 'contradiction', 'unresolved'].index(r['class'])
        counts[r['metric'] + ':' + r['class']] += 1
    assert np.isfinite(matrix).sum() == 650
    (fig, ax) = plt.subplots(figsize=(6.8, 6.55))
    fig.subplots_adjust(left=0.3, right=0.97, top=0.9, bottom=0.16)
    cmap = ListedColormap([BLUE, ORANGE, GRAY])
    cmap.set_bad('#FFFFFF')
    ax.imshow(matrix, cmap=cmap, norm=BoundaryNorm([-0.5, 0.5, 1.5, 2.5], 3), interpolation='nearest')
    ax.set_yticks(range(26), [f'{i + 1:02}  {n}' for (i, n) in enumerate(SHORT)], fontsize=7.5)
    ax.set_xticks(range(26), [f'{i + 1:02}' for i in range(26)], rotation=90, fontsize=7)
    ax.set_title('Triángulo superior: apertura angular\nTriángulo inferior: dimensión lineal efectiva', fontsize=10, pad=12)
    ax.tick_params(length=0)
    ax.spines[['left', 'bottom']].set_visible(False)
    fig.legend(handles=[Patch(color=c, label=l) for (c, l) in [(BLUE, 'Acuerdo de los diez'), (ORANGE, 'Oposición persistente'), (GRAY, 'Sin resolver')]], loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.04), fontsize=8)
    values(item, 'classification_counts', dict(counts))
    values(item, 'cell_encoding', [[None if np.isnan(x) else int(x) for x in row] for row in matrix])
    save(item, fig)
if __name__ == '__main__':
    (OUT / 'figures').mkdir(exist_ok=True, parents=True)
    main_figures()
    supplementary_figures()
    assert len(MANIFEST) == 14
    (OUT / 'figures/manifest.json').write_text(json.dumps(MANIFEST, indent=2) + '\n')
    print('14 figures exported as PDF, SVG, 300 dpi PNG and TIFF; all plotted values catalogued.')
