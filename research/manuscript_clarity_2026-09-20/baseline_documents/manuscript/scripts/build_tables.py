"""Typeset saved research tables; no scientific calculation is restarted.

Each supplementary number denotes a table group: a readable PDF summary plus
complete, unrounded CSV attachments. Filters and reductions are explicit below
and in tables/manifest.json. Counts/means for layout are not new experiments.
"""
from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import json
import shutil
import statistics

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'manuscript'
ROB = 'reports/robustness_v2/final/tables/'
MOR = 'reports/morphology_pilot_v1/'
PAIR = 'reports/field_pair_summary_v1/'
ATLAS = 'reports/prepaper_v1/'
BLUEPRINT = 'research/writing_blueprint_2026-09-18/'
MANIFEST = {}
MODELS = ['specter', 'specter2', 'scincl', 'scibert', 'bert', 'mpnet', 'minilm', 'pubmedbert', 'biobert', 'simcse']
NAMES = dict(zip(MODELS, ['SPECTER','SPECTER2','SciNCL','SciBERT','BERT','MPNet','MiniLM','PubMedBERT','BioBERT','SimCSE']))
FIELD = {}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def tex(value):
    chars = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
             '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(chars.get(c, c) for c in str(value)).replace('–', '--').replace('—', '---').replace('×', r'$\times$').replace('‘', '`').replace('’', "'").replace('“', '``').replace('”', "''")


def num(value, places=3): return f'{float(value):.{places}f}'


def pct(value, places=1): return num(100 * float(value), places) + r'\%'


def integer(value): return f'{int(value):,}'


def read(item, relative):
    p = ROOT / relative; q = OUT / 'tables/data' / item / p.name
    q.parent.mkdir(parents=True, exist_ok=True)
    if p.exists(): shutil.copyfile(p, q)
    with q.open() as f: rows = list(csv.DictReader(f))
    MANIFEST.setdefault(item, {'sources': [], 'rendered_parts': []})['sources'].append(
        {'source': relative, 'included': str(q.relative_to(OUT)), 'sha256': sha(q), 'rows': len(rows)})
    return rows


def note(text): return '\\par\\smallskip{\\small ' + text + '\\par}\n'


def table(item, caption, headers, rows, widths, label=None):
    """Longtable keeps selectable text and permits clean multipage continuation."""
    MANIFEST.setdefault(item, {'sources': [], 'rendered_parts': []})['rendered_parts'].append(
        {'caption': caption, 'headers': headers, 'rows': len(rows)})
    cell_type = 'm' if item == 'T02' else 'p'
    spec = '@{}' + ''.join((r'>{\centering\arraybackslash}' if item == 'T02' and i in (1, 2)
                           else r'>{\raggedright\arraybackslash}') + cell_type + '{' + str(w) + 'cm}'
                          for i, w in enumerate(widths)) + '@{}'
    # Row cells are intentionally pre-escaped, allowing citations and code links.
    head = ' & '.join(r'\textbf{' + tex(h) + '}' for h in headers) + r' \\'
    lab = r'\label{' + (label or 'tab:' + item) + '}'
    if item != 'S08':
        # Keep finite summary tables together; only the long article atlas needs
        # continuation pages. Smaller corpus/provenance typesetting fits a page.
        font = r'\fontsize{9.5}{11}\selectfont' if item == 'S01' else r'\small'
        stretch = '1.03' if item in ('S01', 'S02') else '1.13'
        return ('\\par\\noindent\\begin{minipage}{\\linewidth}\n' + font + '\n'
            + '\\setlength{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{' + stretch + '}\n'
            + '\\captionof{table}{' + caption + '}' + lab + '\n'
            + '\\begin{tabular}{' + spec + '}\n\\toprule\n' + head + '\n\\midrule\n'
            + ('\n\\addlinespace[7pt]\n' if item == 'T01' else
               '\n\\addlinespace[2pt]\n' if item == 'T02' else '\n').join(' & '.join(row) + r' \\' for row in rows)
            + '\n\\bottomrule\n\\end{tabular}\n\\end{minipage}\\par\n')
    return ('{\\small\n\\setlength{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.16}\n'
        + '\\begin{longtable}{' + spec + '}\n\\caption{' + caption + '}' + lab + r'\\' + '\n\\toprule\n'
        + head + '\n\\midrule\n\\endfirsthead\n'
        + r'\multicolumn{' + str(len(headers)) + r'}{l}{\small\itshape Table \thetable{} (continued)} \\'
        + '\n\\toprule\n' + head + '\n\\midrule\n\\endhead\n'
        + '\\midrule\n\\multicolumn{' + str(len(headers)) + r'}{r}{\small Continued on next page} \\'
        + '\n\\endfoot\n\\bottomrule\n\\endlastfoot\n'
        + '\n'.join(' & '.join(row) + r' \\' for row in rows)
        + '\n\\end{longtable}\n}\n')


def write(item, content, selection):
    (OUT / 'tables/tex' / (item + '.tex')).write_text(content)
    MANIFEST[item]['summary_rule'] = selection


def main_tables():
    item = 'T01'; data = read(item, BLUEPRINT + 'table1_panels.csv')
    compact = [
        ('Original corpus', '500,000 IDs: 400,000 base + 100,000 supplement. Ten models; title + abstract.',
         '26 Fields, five periods. Global summaries use the base; the full corpus is not population-proportional.'),
        ('Three text inputs', '52,000 IDs; 400 per Field-period, 2,000 per Field. Title, abstract and both.',
         'Same articles and candidates between models. Includes the 26,000-article pilot.'),
        ('Common fragment', 'A different 52,000-ID panel; 400 per Field-period.',
         'Paired native/shared content; model-specific tokenization. Distinct from the three-input panel.'),
        ('Matched group size', '256 articles per centre; 26 Fields, 217 Subfields, or 26 Subfield centres.',
         'Within groups: 26 Fields and the same 183 Subfields at 128, 256 and 512 articles. Different objects from centres.'),
        ('Paired searches', '217 Subfields; 50 fixed queries each (10,850 total). Ten candidate selections.',
         '256 candidates in each scope, including all 50 queries. The Field pool is conditioned on these queries.'),
        ('Geometry / Field pairs', '2,000 per Field; twenty halves of 1,000 and five selections of 2,000.',
         '325 Field pairs and two properties; 26 saved conditions. Alternative metrics have different coverage.')]
    assert len(data) == len(compact) == 6
    content = table(item, 'Corpus and analytical panels.', ['Panel', 'Articles and representation', 'Comparison and scope'],
                    [[tex(c) for c in row] for row in compact], [2.9, 5.8, 6.45])
    content += note('Rows overlap and must not be added. Periods: 2000--04, 2005--09, 2010--14, 2015--19 and 2020--24. '
        'Each model comparison uses the same IDs. Query articles exclude themselves during neighbour search. '
        'The 1,300 technical test articles are not an additional scientific panel. Full filters and quotas: Table S1.')
    write(item, content, 'All six blueprint rows, condensed without changing their denominators; full source CSV included.')

    item = 'T02'; models = read(item, BLUEPRINT + 'table2_models.csv'); rows = []
    for r in models:
        ref = r['reference'].split(';')[0]
        recipe = 'CLS + adapter' if r['model'] == 'specter2' else 'CLS, pre-pooler' if r['model'] == 'simcse' else r['primary_pooling'].upper() if r['primary_pooling'] == 'cls' else 'Mean'
        model = r'\textbf{' + tex(r['display_name']) + '}'
        rows.append([model, r['dimension'], r['native_max_tokens'], tex(recipe), r'\citep{' + ref + '}'])
    content = table(item, 'Embedding models and primary representation settings.',
                    ['Model', 'Dim.', 'Tokens', 'Readout', 'Reference'], rows, [3.3, 1.1, 1.45, 3.0, 5.6])
    content += note('MPNet and MiniLM use all-mpnet-base-v2 and all-MiniLM-L6-v2, respectively. '
        'Limits count tokens including special symbols. Mean: last-layer average over non-padding positions, '
        'including special symbols. CLS: first-position state before the pooler; SPECTER2 adds its proximity adapter. '
        'For MPNet/MiniLM, the reference describes the Sentence-BERT framework, not the exact checkpoint training. '
        'Readout variants are not additional models. Full revisions, formats and truncation: Table S2.')
    write(item, content, 'All ten models; configuration-verified blueprint rows. Full checkpoints and hashes retained in S02.')


def supplementary_tables():
    item = 'S01'
    cells = read(item, 'research/cleaning_2026-09-15/field_period_counts.csv')
    fields = read(item, 'research/cleaning_2026-09-15/field_summary.csv')
    read(item, 'research/cleaning_2026-09-15/field_year_counts.csv')
    read(item, 'research/cleaning_2026-09-15/quality_by_field_period.csv')
    read(item, ROB + 'controls_quality_flags.csv')
    FIELD.update({r['field_id']: r['field_name'] for r in fields})
    rows = []
    for r in fields:
        counts = [next(a['total'] for a in cells if a['field_id'] == r['field_id'] and a['period_start'] == str(y))
                  for y in (2000, 2005, 2010, 2015, 2020)]
        assert sum(map(int, counts)) == int(r['total'])
        rows.append([tex(r['field_name'])] + [integer(x) for x in counts] + [integer(r['base']), integer(r['extra'])])
    rows.append([r'\textbf{Total}'] + [integer(sum(int(a['total']) for a in cells if a['period_start'] == str(y)))
                 for y in (2000, 2005, 2010, 2015, 2020)] + ['400,000', '100,000'])
    content = table(item, 'Clean corpus by Field, period and cohort.',
             ['Field', '2000-04', '2005-09', '2010-14', '2015-19', '2020-24', 'Base', 'Extra'],
             rows, [5.1, 1.23, 1.23, 1.23, 1.23, 1.23, 1.23, 1.23])
    content += note('Total: 500,000 distinct OpenAlex work IDs. Period columns contain base plus extra; the last two columns '
        'divide those same articles and must not be added again. Core catalogue; years 2000--2024; article, review and conference-paper; '
        'OpenAlex English label, non-empty title, reconstructible abstract with at least 50 regex words, known primary Field, '
        'no retraction or paratext flag. Additional cleaning rejects clear language/content failures and marks ambiguous cases. '
        'No claim that every retained abstract is exclusively English or correctly labelled. Exact annual/cohort counts and '
        'quality flags are included as CSVs; raw retrieval ended on 15 September 2026. The database was not a simultaneous snapshot.')
    write(item, content, 'Every Field and every period, with base/extra totals; full yearly/cell quality tables included.')

    item = 'S02'
    models = read(item, BLUEPRINT + 'table2_models.csv')
    trunc = read(item, 'research/embedding_final_audit_2026-09-17/truncation_by_model.csv')
    read(item, 'research/embedding_final_audit_2026-09-17/truncation_by_field_period_cohort.csv')
    read(item, 'research/embedding_final_audit_2026-09-17/full_text_coverage_by_field_period.csv')
    rows = []
    for r in models:
        t = next(t for t in trunc if t['model'] == r['model'])
        cell = r'\nolinkurl{' + r['repo_id'] + r'}\newline Revision: {\ttfamily\seqsplit{' + r['revision'] + '}}'
        if r['adapter_repo']:
            cell += r'\newline Adapter: \nolinkurl{' + r['adapter_repo'] + r'}\newline{\ttfamily\seqsplit{' + r['adapter_revision'] + '}}'
        cell = r'{\footnotesize ' + cell + '}'
        formatting = 'Title [SEP] abstract' if r['text_format'] == 'sep' else 'Title, blank line, abstract'
        rows.append([tex(NAMES[r['model']]), cell,
            tex(formatting) + r'\newline Limit: ' + r['native_max_tokens'] + r'\newline Truncated: ' + num(t['truncated_percent'], 2) + r'\%'])
    content = table(item, 'Frozen checkpoints, text formats and native truncation.',
                     ['Model', 'Checkpoint and full revision', 'Input / truncation'], rows, [2.8, 8.1, 4.25])
    content += note('Truncation is measured on the full 500,000-article title-plus-abstract corpus and is not an error rate. '
        'The principal MiniLM limit remains 256 tokens; its 512-token variant is a separate sensitivity. CLS/SEP alternatives '
        'apply only to BERT, SciBERT, BioBERT and PubMedBERT. SEP takes the last non-padding position, not the title separator. '
        'Tokenizer differences mean that equal token limits would not imply equal text. Model-card URLs and all revisions are in the CSV.')
    write(item, content, 'All model revisions, exact separators and full-corpus truncation rates; native limits unchanged.')

    item = 'S03'
    rows = [
        ['Initial comparison', '500,000 corpus; 130 cells; 45 fixed model pairs', 'Before this phase\'s agreements', 'Normalised vectors; corrected CKA, k25; CLS/SEP and size checks.'],
        ['Common fragment', '52,000 paired IDs, distinct from the input panel', 'Before first scientific comparison', 'Same content characters; native tokenizers and separators.'],
        ['Centres / random groups', '256 per centre; 26/217/26 centres', 'Added after initial results', 'Matched dates/sizes; addresses centre averaging, not thematic validity.'],
        ['Input expansion', '26,000 to 52,000 nested IDs', 'After pilot; before expanded result', 'Three inputs and pooling crossed; 100 comparable selections.'],
        ['Matched local searches', '217 groups, 50 queries, ten selections', 'Expanded phase design', '256 candidates per scope, including identical queries and matched dates.'],
        ['Atlas', '217 Subfields; 183 in sensitivity panel; 12 paper examples', 'After global results; before reading selected titles', 'Rule-selected examples; source errors retained.'],
        ['Morphology', '52,000 IDs; alternative measures and synthetic clouds', 'Exploratory extension after core results', 'Protocol before new real-data metrics. Neighbour-fraction check added during execution.'],
        ['Field pairs', '325 pairs per property; 26 saved conditions', 'After morphology results', 'Direction/magnitude rules fixed before new pair counts; no new inference.']]
    content = table(item, 'Coverage and chronology of the comparison blocks.',
                     ['Block', 'Coverage', 'When specified', 'Interpretation'], [[tex(x) for x in row] for row in rows], [2.6, 4.1, 3.4, 5.05])
    content += note(r'This is a sequence of documented phases, not a preregistered study. Sources: ANALYSIS\_PROTOCOL, '
        r'ROBUSTNESS\_PROTOCOL, CASE\_ATLAS\_PROTOCOL, MORPHOLOGY\_PROTOCOL and FIELD\_PAIR\_PROTOCOL, '
        'with their dated decision entries. Later controls are not relabelled as initial hypotheses.')
    # The structured rendering itself is the complete chronology table.
    p = OUT / 'tables/data/S03/chronology.csv'; p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w') as f:
        w = csv.writer(f); w.writerow(['block', 'coverage', 'timing', 'interpretation']); w.writerows(rows)
    MANIFEST[item]['sources'].append({'source': 'Dated protocols and DECISIONS.md; explicit synthesis',
        'included': str(p.relative_to(OUT)), 'sha256': sha(p), 'rows': len(rows)})
    write(item, content, 'Complete descriptive chronology; manually condensed from dated protocols, not inferred from results.')

    item = 'S04'
    rows = read(item, ROB + 'controls_metric_consistency_summary.csv')
    alerts = read(item, ROB + 'controls_original_50_alerts.csv')
    read(item, ROB + 'controls_original_stability_reconstructed.csv')
    read(item, ROB + 'controls_control_magnitudes.csv')
    read(item, ROB + 'controls_paper_shuffle_reference.csv')
    sub = read(item, ROB + 'structure_subfield_stability_summary.csv')
    read(item, ROB + 'structure_subfield_stability_alerts.csv')
    names = {'cka_debiased': 'Corrected CKA', 'procrustes_similarity': 'Procrustes', 'rsa_spearman': 'Distance ranks'}
    selected = [r for r in rows if r['source'] == 'field_period_native']
    content = table(item, 'Agreement of alternative measures and retained stability alerts.',
        ['Measures compared', 'Cells', 'Mean rank agreement', 'Minimum', 'Maximum'],
        [[tex(names[r['metric_a']] + ' / ' + names[r['metric_b']]), r['n'], num(r['mean']), num(r['min']), num(r['max'])] for r in selected],
        [6.1, 1.2, 3.0, 2.1, 2.1])
    content += note('The top panel reports descriptive Spearman correlations of model-pair agreements within each of 130 Field-period cells. '
        'These correlations compare measures; they do not validate thematic content. All 41 saved summaries and all individual original '
        'alerts accompany the table.')
    content += r'\begin{itemize}' + '\n'
    content += r'\item Original Field-period screen: ' + str(len(alerts)) + r' alerts among 5,850 comparisons; largest central-95\% selection width among flagged cases: ' + num(max(float(r['central95_width']) for r in alerts)) + '.\n'
    for r in sub:
        label = 'The larger sample equals the entire group' if r['large_sample_equals_whole_group'] == 'True' else 'The larger sample does not equal the entire group'
        content += r'\item ' + label + ': ' + integer(r['alerts']) + ' alerts / ' + integer(r['comparisons']) + ' comparisons; ' + r['subfields'] + ' Subfields.\n'
    content += r'\end{itemize}' + '\n' + note('A zero selection width when the whole group is used does not establish stability at a smaller size. '
        'These are within-corpus screens, not population confidence intervals. Alerts from different designs remain separate.')
    write(item, content, 'Top panel: all three native Field-period metric comparisons; alerts from complete saved screens, not discarded.')

    item = 'S05'
    model = read(item, ROB + 'input_input_effect_by_model.csv')
    read(item, ROB + 'input_input_effect_by_field.csv'); read(item, ROB + 'input_input_effect_summary.csv')
    recipes = read(item, ROB + 'input_recipe_effect_summary.csv')
    read(item, ROB + 'input_recipe_sensitivity_all_cases.csv'); read(item, ROB + 'input_recipe_sign_changes.csv')
    def effect(m, metric, cond):
        return next(r['mean'] for r in model if r['model'] == m and r['metric'] == metric
                    and r['input_condition'] == cond and r['measure'] == 'input_change_from_full')
    content = table(item, 'Input changes by model, averaged equally over the 26 Fields.',
        ['Model', 'Title: shape', 'Abstract: shape', 'Title: neighbours', 'Abstract: neighbours'],
        [[tex(NAMES[m]), num(effect(m, 'cka', 'title')), num(effect(m, 'cka', 'abstract')),
          pct(effect(m, 'neighbors25', 'title')), pct(effect(m, 'neighbors25', 'abstract'))] for m in MODELS],
        [3.0, 2.7, 2.7, 3.1, 3.1])
    content += note('Same 52,000 IDs and 2,000 candidates per Field. Shape change: 1 minus corrected CKA. Neighbour change: '
        'fraction of the 25 neighbours replaced. Title/abstract conditions compare each model with its own full input. '
        'Model-choice means and all Field-specific values are included as CSVs, alongside the full recipe cross. '
        'These are practical input changes with native text limits, not a causal separation of encoder and text length.')
    selected = [r for r in recipes if r['metric'] in ['cka','neighbors25'] and r['input_condition'] == 'title' and r['measure'] == 'model_minus_input']
    content += note('Title-only model-minus-input contrast (positive: changing model has the larger mean effect): ' +
        '; '.join(tex(r['recipe'].upper() + ', ' + ('shape' if r['metric'] == 'cka' else 'neighbours')) + ' = ' + num(r['mean'], 4) for r in selected) +
        '. Only the four word BERTs change readout in CLS/SEP. Close means do not establish equivalence.')
    write(item, content, 'Ten model-specific input effects; all Field, recipe and original-precision summaries in attachments.')

    item = 'S06'
    rows = read(item, ROB + 'input_alert_transition_counts.csv')
    current = read(item, ROB + 'input_current52_alerts.csv')
    read(item, ROB + 'input_original31_tracking.csv'); read(item, ROB + 'input_nested_sample_effect_changes.csv')
    content = table(item, 'Input-alert transitions for the nested 26k and 52k panels.',
        ['Selections / scope', 'Contrasts', '26k alerts', '52k alerts', 'Persist', 'Resolved', 'New'],
        [[r['repeats'] + ' / ' + ('model-Field' if r['scope'] == 'individual_models' else 'Field average'),
          r['comparisons'], r['alerts26k'], r['alerts52k'], r['persists'], r['resolved'], r['new']] for r in rows],
        [3.5, 1.95, 1.7, 1.7, 1.45, 1.95, 1.2])
    current100 = [r for r in current if r['repeats'] == '100' and r['alert52k'] == 'True']
    assert len(current100) == 5
    content += note('The five remaining model-Field-input alerts with 100 selections are: ' +
        '; '.join(tex(NAMES[r['model']] + ' / ' + FIELD[r['field_id']] + ' / ' + r['input_condition']) +
                  ' (width ' + num(r['width52k']) + ')' for r in current100) +
        '. No alert does not imply an effect different from zero. Original 20-selection and later 100-selection counts are kept separate.')
    write(item, content, 'All four transition rows and all five current 100-selection alerts; original 31 identities retained in CSV.')

    item = 'S07'
    rows = read(item, ROB + 'structure_paired_scope_summary.csv')
    read(item, ROB + 'structure_paired_scope_subfield_summary.csv')
    read(item, ROB + 'structure_paired_scope_field_summary.csv')
    read(item, ROB + 'structure_matched_size_agreement.csv')
    read(item, ATLAS + 'subfields.csv'); read(item, ATLAS + 'subfield_sensitivity_panels.csv')
    content = table(item, 'Matched Field/Subfield neighbour searches.',
        ['k', 'Field overlap', 'Subfield overlap', 'Difference (pp)', 'Lower / higher', 'Subfields'],
        [[r['k'], pct(r['field_mean']), pct(r['subfield_mean']), num(100*float(r['mean_difference']), 2),
          r['subfields_lower_agreement'] + ' / ' + r['subfields_higher_agreement'], r['subfields']] for r in rows],
        [.65, 2.7, 2.7, 3.0, 3.3, 2.1])
    content += note('Difference is Subfield minus Field. Each scope contains 256 candidates, including the same 50 query articles, '
        'with matched dates; self is excluded during search. Means use ten candidate selections. The broader Field comparison '
        'is conditioned on the queries and is not 256 unrestricted Field draws. All 217 Subfields appear in the paired design; '
        '183 meet all size conditions of the separate 128/256/512 sensitivity panel. Full size/readout/k results accompany the table.')
    write(item, content, 'All three k values; complete group-size and Subfield sensitivity attachments.')

    item = 'S08'
    papers = read(item, ATLAS + 'paper_examples_readable.csv')
    read(item, ATLAS + 'article_relations_readable.csv'); read(item, ATLAS + 'subfield_relation_examples.csv')
    read(item, ATLAS + 'subfield_examples.csv'); read(item, ATLAS + 'paper_example_pairs.csv')
    notes = {'99305': 'Bacterial-infection abstract labelled as politics.',
        '202595': 'History-book description labelled as physics; type caveat.',
        '93549': 'Announcement / atlas review; not detected by the original notice screen.',
        '115771': 'Persuasion economics under Safety Research; label caveat.',
        '452340': 'Mathematics education under Applied Mathematics; administrative label.',
        '327954': 'Substantial formula code in abstract; input caveat.'}
    rr = []
    for r in papers:
        title = tex(r['title']) + r'\newline{\footnotesize\nolinkurl{' + r['work_id'] + '}; ' + r['publication_year'] + '}'
        comment = notes.get(r['row_index'], 'No clear issue in this limited inspection; not expert validation.')
        rr.append([title, tex(r['subfield_display_name']), pct(r['k25_mean']),
                   pct(r['k25_min']) + '--' + pct(r['k25_max']), tex(comment)])
    content = table(item, 'All twelve rule-selected article examples, including source caveats.',
        ['Article and OpenAlex ID', 'Subfield label', 'Mean', 'Selection range', 'Inspection note'], rr,
        [4.9, 3.1, 1.25, 2.0, 3.55])
    content += note('Numbers are k25 overlap averaged over 45 model pairs; ranges span ten candidate selections. '
        'The first/last six examples come from high/low agreement sources under the recorded rule. Titles were read after '
        'selection. Full source/target IDs, titles and per-model supports for both relation types are in the accompanying CSVs. '
        'The most model-dependent link was selected for each source; this does not estimate prevalence. '
        'An incomplete target abstract is also retained and marked in Figure S3. None of these checks validates OpenAlex labels.')
    write(item, content, 'All 12 fixed sources, not cherry-picked again for layout; all 24 article and 16 centre-relation examples included.')

    item = 'S09'
    rows = read(item, ROB + 'time_heterogeneity.csv')
    read(item, ROB + 'time_control_consistency.csv'); read(item, ROB + 'time_fields.csv')
    read(item, ROB + 'time_pairs.csv'); read(item, ROB + 'subfield_time_fixed128.csv')
    chosen = ['cka_primary', 'cka_equal2048', 'rsa_spearman_primary', 'procrustes_similarity_primary',
              'neighbors_all_k25', 'neighbors_2048_mean_k25', 'neighbors_2048_cls_k25', 'neighbors_2048_sep_k25']
    labels = ['CKA, native groups', 'CKA, 2,048 per group', 'Distance ranks, native', 'Procrustes, native',
              'k25, all candidates', 'k25, 2,048 / mean', 'k25, 2,048 / CLS', 'k25, 2,048 / SEP']
    rr = []
    for key, label in zip(chosen, labels):
        r = next(r for r in rows if r['outcome'] == key and r['unit'] == 'field')
        rr.append([tex(label), num(r['mean_endpoint_change'], 4), r['positive_endpoint'],
                   r['negative_endpoint'], r['nonmonotone']])
    content = table(item, 'Temporal endpoint changes and Field heterogeneity.',
        ['Measure / candidate design', 'Mean change', 'Positive', 'Negative', 'Non-monotone'], rr,
        [6.0, 2.4, 2.15, 2.15, 2.15])
    content += note('End minus start: 2020--24 versus 2000--04. Each row describes 26 Fields with equal weight; neighbour changes '
        'are fractions, so multiply by 100 for percentage points. Five periods are used to classify monotonicity. '
        'Full k10/k25/k50, recipe, identical-query and pair-level checks are in the CSVs. Candidate counts can change the sign. '
        'These are descriptive period contrasts, not causal historical convergence.')
    write(item, content, 'Eight named primary/size/recipe outcomes at Field level; all 40 saved summaries and matched controls included.')

    item = 'S10'
    rows = read(item, ROB + 'structure_medicine_composition_summary.csv')
    read(item, ROB + 'structure_medicine_composition_change_summary.csv')
    read(item, ROB + 'structure_medicine_field_contrast_summary.csv')
    read(item, ROB + 'structure_medicine_paired_field_contrasts.csv')
    read(item, ROB + 'structure_composition_diversity.csv'); read(item, ROB + 'structure_diversity_associations.csv')
    read(item, ROB + 'structure_within_subfields_biomedical.csv')
    rr = []
    for field in ['27','21','26','31']:
        for group in ['all','without_biomedical']:
            vals = [next(r['mean'] for r in rows if r['field_id'] == field and r['model_group'] == group
                         and r['metric'] == metric and r['condition'] == condition)
                    for metric in ['cka_debiased', 'neighbors_k25']
                    for condition in ['observed_eligible_composition', 'equal_subfield_composition']]
            rr.append([tex(FIELD[field]), 'Ten' if group == 'all' else 'Eight', num(vals[0]), num(vals[1]), pct(vals[2]), pct(vals[3])])
    content = table(item, 'Discipline agreement with observed and balanced Subfield composition.',
       ['Field', 'Models', 'CKA obs.', 'CKA bal.', 'k25 obs.', 'k25 bal.'], rr, [4.35, 1.55, 2.2, 2.2, 2.2, 2.2])
    content += note('Eight excludes BioBERT and PubMedBERT. 2,048 articles per Field with identical date quotas; mean of ten '
        'selections. Energy has one eligible Subfield, so balancing does not introduce a comparable composition change there. '
        'The display focuses on the four Fields of Figure S5; all 26 Fields and matched contrasts are supplied. '
        'Composition and biomedical training are not isolated causal explanations.')
    write(item, content, 'All conditions for the four preselected display Fields and ten/eight model panels; complete 26-Field data included.')

    item = 'S11'
    traits = read(item, ROB + 'families_model_traits.csv')
    fits = read(item, ROB + 'families_identifiability.csv')
    read(item, ROB + 'families_coefficients.csv'); omissions = read(item, ROB + 'families_leave_one_model.csv')
    read(item, ROB + 'families_marginal_associations.csv'); read(item, ROB + 'families_permutation_reference.csv')
    read(item, ROB + 'structure_family_trait_omission_ranges.csv')
    rr = []
    labels = {'cka_primary': 'CKA / primary', 'cka_equal2048': 'CKA / 2,048 articles',
              'cka_quality': 'CKA / quality filter', 'cka_cls': 'CKA / CLS',
              'cka_sep': 'CKA / SEP', 'neighbors_2048_mean_k25': 'Neighbours k25 / mean',
              'neighbors_2048_cls_k25': 'Neighbours k25 / CLS',
              'neighbors_2048_sep_k25': 'Neighbours k25 / SEP'}
    for r in fits:
        unavailable = sum(x['identified'] != 'True' for x in omissions if x['outcome'] == r['outcome'])
        rr.append([tex(labels[r['outcome']]), r['rank'] + '/' + r['columns'],
                   num(r['condition_number'], 2), num(r['r_squared']), str(unavailable)])
    content = table(item, 'Descriptive model-trait fits and identifiability.',
        ['Outcome', 'Rank', 'Condition no.', 'R squared', 'Unidentified coefficients after omission'], rr,
        [5.5, 1.2, 2.3, 1.8, 4.3])
    content += note('Ten fixed models yield 45 overlapping pairs. R squared describes these pairs, not predictive validity. '
        'The final column counts unavailable coefficient rows across the ten leave-one-model checks, not independent models '
        'or tests. In the SEP design, omitting SimCSE makes coefficients non-identifiable; those values remain missing. '
        'Architecture, lineage, final corpus, objective, domain and readout are correlated traits. Full trait definitions, '
        'source URLs, coefficients, pair-label permutation references and omissions accompany this table. No causal training effect is claimed.')
    write(item, content, 'All eight model-trait fits; source outcome keys expanded into readable labels. Counts of saved non-identifiable omission coefficients; all model traits included.')

    item = 'S12'
    stability = read(item, MOR + 'selection_stability.csv')
    read(item, MOR + 'primary_metrics.csv'); read(item, MOR + 'alternative_metric_agreement.csv')
    read(item, MOR + 'between_model_field_ranks.csv'); read(item, MOR + 'rank_stability.csv')
    read(item, MOR + 'control_rank_stability.csv'); read(item, MOR + 'paired_controls.csv')
    rr = []
    for metric, label in [('angle_p50','Angular spread'), ('pr','Effective linear dimension'), ('gap_25','Connection')]:
        for kind, design in [('half','20 half samples'), ('external','5 equal-size selections')]:
            rows = [r for r in stability if r['metric'] == metric and r['kind'] == kind]
            rr.append([tex(label), tex(design), str(len(rows)), str(sum(r['passes_both'] != 'True' for r in rows)),
                pct(statistics.median(float(r['relative_width']) for r in rows), 2),
                pct(max(float(r['relative_width']) for r in rows), 2)])
    content = table(item, 'Selection stability of the geometric properties.',
        ['Property', 'Selection design', 'Cases', 'Alerts', 'Median width', 'Maximum width'], rr,
        [3.5, 3.7, 1.2, 1.2, 2.5, 2.6])
    content += note(r'A case is one model-Field combination. Width is the central 90\% range divided by the primary value; '
        r'the screen also checks median shift. Thresholds: 5\% angular spread, 10\% PR, 20\% connection. These are operational '
        'sensitivity thresholds, not journal standards or population precision. The four PR half-sample alerts remain visible '
        'even though the five equal-size selections pass. PR is effective linear dimension, not number of topics. '
        'Spectral alternatives share the same covariance spectrum and do not independently validate thematic meaning.')
    write(item, content, 'All three properties and both selection designs, counting passes from saved Boolean flags; full individual cases included.')

    item = 'S13'
    clouds = read(item, 'data/morphology_pilot_v1/synthetic/clouds.csv')
    read(item, MOR + 'sample_size.csv'); read(item, MOR + 'connectivity_fixed_fraction.csv')
    gauss = read(item, MOR + 'gaussian_reference_diagnostics.csv')
    labels = {'one_round':'One round cloud','one_narrow':'One narrow cloud','one_wide':'One wide cloud',
        'one_elongated':'One elongated cloud','low_rank':'One low-rank cloud','two_separated':'Two separated groups',
        'four_separated':'Four separated groups','two_with_bridges':'Two groups with bridges','one_with_outliers':'One cloud with outliers'}
    content = table(item, 'Construct checks on all nine saved synthetic clouds.',
        ['Cloud', 'Gap k25', 'Radius 90/50', 'Max/median edge', 'Mutual giant'],
        [[tex(labels[r['cloud']]), num(r['gap_25']), num(r['connect_ratio90_50']), num(r['mst_max_median']), pct(r['mutual_giant_25'])] for r in clouds],
        [5.2, 2.25, 2.55, 2.7, 2.0])
    content += note('Each saved cloud has 1,000 points. Smaller gap can arise without separate groups; radius/edge ratios can '
        'respond to outliers or elongated clouds. In all 260 primary model-Field cases the union k25 graph is connected. '
        'Connection therefore remains a graph description and is not validated as general thematic fragmentation. '
        'The five equal-size selections retain 51 connection alerts (Table S12).')
    content += note('The 780 Gaussian reference rows are included. Observed-relative reference errors span ' +
        pct(min(float(r['spread_reference_relative_error']) for r in gauss), 2) + ' to ' +
        pct(max(float(r['spread_reference_relative_error']) for r in gauss), 2) + ' for angular spread, and ' +
        pct(min(float(r['pr_reference_relative_error']) for r in gauss), 2) + ' to ' +
        pct(max(float(r['pr_reference_relative_error']) for r in gauss), 2) +
        ' for PR. Gaussian draws preserve fitted moments only in expectation before renormalisation; they are not calibrated null tests. '
        'Full n/k controls accompany the table; the fixed-neighbour-fraction check was added during execution.')
    write(item, content, 'All nine saved simulation rows; complete size/fraction/Gaussian tables included; no new simulation.')

    item = 'S14'
    counts = read(item, PAIR + 'classification_summary.csv')
    read(item, PAIR + 'pair_summary.csv'); read(item, PAIR + 'pair_sensitivity.csv')
    read(item, PAIR + 'model_pair_directions.csv'); read(item, PAIR + 'field_summary.csv')
    rows = [r for r in counts if r['rule'] == 'all_saved']
    content = table(item, 'All Field-pair conclusions under four minimum relative differences.',
        ['Property', 'Minimum', 'All ten agree', 'Opposition', 'Unresolved', 'Pairs'],
        [[tex('Angular spread' if r['metric'] == 'angle_p50' else 'Linear dimension'),
          pct(r['minimum_relative_difference'],0), r['unanimous'], r['contradiction'], r['unresolved'],r['pairs']] for r in rows],
        [4.3, 1.9, 2.7, 2.25, 2.3, 1.55])
    content += note('Every property uses all 325 Field pairs and ten models. A model direction must persist in all 26 saved '
        'conditions: primary sample, twenty halves and five equal-size selections. Opposition needs at least two fixed models '
        'with persistent opposite directions; unanimity needs all ten. Other cases are unresolved, not equal. The signed '
        'symmetric difference is $2(B-A)/(A+B)$; the minimum is an operational magnitude cutoff, not statistical significance '
        'or a share of science correctly represented. Full 650 pair-property rows and all 6,500 model directions accompany the table.')
    write(item, content, 'Eight exhaustive counts, all_saved rule, all four thresholds. Full pair and model decisions included.')

    item = 'S15'
    panels = read(item, PAIR + 'model_panel_summary.csv')
    read(item, PAIR + 'alternative_support.csv'); read(item, PAIR + 'alternative_metric_summary.csv')
    read(item, PAIR + 'model_pair_witnesses.csv')
    selected = [r for r in panels if float(r['minimum_relative_difference']) == 0]
    rr=[]
    for panel in dict.fromkeys(r['panel'] for r in selected):
        p=[next(r for r in selected if r['panel']==panel and r['metric']==metric) for metric in ['angle_p50','pr']]
        label = 'All ten' if panel=='all_ten' else 'Six similarity models' if panel=='six_similarity' else 'Omit '+NAMES[panel[5:]]
        rr.append([tex(label),p[0]['models'],p[0]['contradiction'],p[0]['contradiction_and_alternatives'],
                   p[1]['contradiction'],p[1]['contradiction_and_alternatives']])
    content=table(item,'Persistent opposition and identical witnesses across alternatives and model panels.',
        ['Model panel','Models','Spread','Spread + alternatives','PR','PR + alternatives'],rr,[3.95,1.55,1.55,3.15,1.5,3.05])
    content+=note('All counts are out of 325 at zero minimum magnitude. Alternatives must retain the directions of the '
        'same opposing models; different witnesses cannot be substituted between measures. Angular alternatives have 26 '
        'saved conditions, spectral alternatives three. Six similarity models: SPECTER, SPECTER2, SciNCL, MPNet, MiniLM and SimCSE. '
        'Fewer models provide fewer opportunities for opposition; this panel does not isolate a training effect. All four '
        'magnitude cutoffs and witness identities are supplied as CSVs.')
    write(item,content,'All 12 panels at t=0 with same-witness alternatives; full 96 panel rows and 90 witness summaries included.')

    item='S16'
    controls=read(item,PAIR+'control_summary.csv');read(item,PAIR+'control_pairs.csv')
    labels={'abstract':'Abstract only','common':'Common fragment','global_centered':'Global centring','quality':'Quality flags',
        'trim_extreme':'Extreme-point removal','minilm512':'MiniLM 512','size500':'n = 500','size4000':'n = 4,000',
        'title':'Title only','pool_cls':'Word BERTs: CLS','pool_sep':'Word BERTs: SEP'}
    rr=[]
    for condition in dict.fromkeys(r['condition'] for r in controls):
        p=[next(r for r in controls if r['condition']==condition and r['metric']==metric and float(r['minimum_relative_difference'])==0) for metric in ['angle_p50','pr']]
        rr.append([tex(labels.get(condition,condition)),tex(p[0]['reference']),p[0]['affected_models'],
          p[0]['same_original_witness_pair_retained']+'/'+p[0]['original_persistent_contradictions'],
          p[1]['same_original_witness_pair_retained']+'/'+p[1]['original_persistent_contradictions']])
    content=table(item,'Point controls: retention of the original opposing models.',
        ['Control','Matched reference','Models changed','Spread retained','PR retained'],rr,[4.3,3.35,2.4,2.3,2.3])
    content+=note('Numerators retain the same original model pair with its original signs in both matched reference and '
        'variant. Denominators are the original persistent oppositions (262 angular spread; 221 PR). Values are not new '
        '26-condition stability tests. The common fragment uses its own matched panel; extreme-point removal compares '
        'with random removal at equal size. Quality/extreme/size controls change IDs as specified; other matched controls '
        'retain IDs. All magnitudes and all 7,150 point pair records are included.')
    write(item,content,'All 11 controls at zero threshold, same original witness pairs; complete thresholds included.')

    item='S17'
    assets=[
        ('Clean corpus','data/corpus_clean_v1/embedding_manifest.json','500,000 IDs; local','./prepare.sh preflight'),
        ('Embedding audit','research/embedding_final_audit_2026-09-17/full_verification.json','Ten models; local vectors','See EMBEDDINGS_AUDIT.md'),
        ('Core report','reports/analysis_v1/final/catalog.json','Tables / figures; public baseline','See METHODS_ANALYSIS.md'),
        ('Expanded report','reports/robustness_v2/final/catalog.json','Tables / figures; public baseline','See METHODS_ROBUSTNESS.md'),
        ('Case atlas','reports/prepaper_v1/catalog.json','Examples; public baseline','See CASE_ATLAS.md'),
        ('Morphology','reports/morphology_pilot_v1/catalog.json','Local extension; no data deposit','See METHODS_MORPHOLOGY.md'),
        ('Field pairs','reports/field_pair_summary_v1/catalog.json','Local extension; no data deposit','See METHODS_FIELD_PAIRS.md'),
        ('Writing blueprint','research/writing_blueprint_2026-09-18/closure_audit.json','Local editorial plan','See MANUSCRIPT_BLUEPRINT.md')]
    rr=[]; records=[]
    for name,path,access,command in assets:
        h=sha(ROOT/path)
        rr.append([tex(name),r'{\footnotesize\nolinkurl{'+path+r'}}\newline{\ttfamily\seqsplit{'+h+'}}',tex(access)])
        records.append({'object':name,'manifest':path,'sha256':h,'access':access,'verification_or_methods':command})
    content=table(item,'Versions and access status of the source objects.',
        ['Object','Manifest / SHA-256','Access'],rr,[2.65,9.45,3.15])
    content+=note('Hashes identify the listed manifest/catalogue bytes, not the whole folder directly; each catalogue records '
        'its own assets. Local reproducibility is broader than public access. No persistent data deposit, general licence or '
        'new public release is claimed. Corpus, vectors, model weights, API keys and third-party full texts are excluded from '
        'the manuscript bundle. The two PDFs can be rebuilt from the included LaTeX and figure/table assets without the corpus. '
        'Full experimental reproduction still requires the separately authorised data-release plan.')
    p=OUT/'tables/data/S17/provenance.csv';p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    MANIFEST[item]['sources'].append({'source':'Current source catalogues, read-only','included':str(p.relative_to(OUT)),
                                    'sha256':sha(p),'rows':len(records)})
    write(item,content,'Eight manifest SHA-256 values and truthful access states; this is an inventory, not a new data release.')


if __name__=='__main__':
    (OUT/'tables/tex').mkdir(parents=True,exist_ok=True)
    main_tables(); supplementary_tables()
    assert len(MANIFEST)==19
    (OUT/'tables/manifest.json').write_text(json.dumps(MANIFEST,indent=2)+'\n')
    print('2 main tables and 17 supplementary table groups exported, with complete source CSVs.')
