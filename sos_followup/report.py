"""Rebuild a reviewable checklist delivery from immutable numerical results."""
import argparse
import csv
import json
import shutil
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pyarrow.parquet as pq

from sos_embed.storage import file_sha, write_json, utcnow

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'config/checklist_v1.json'
D = json.loads(DESIGN.read_text())
EXIST = ROOT / 'data/checklist_v1/existing_v2'
INP = ROOT / 'data/checklist_v1/inputs'
CMP = ROOT / 'data/checklist_v1/input_comparisons'
CAND = ROOT / 'data/checklist_v1/candidate_check'
PROFILE = ROOT / 'data/checklist_v1/text_profile'
RECIPES = ROOT / 'data/checklist_v1/input_recipes'
RESEARCH = ROOT / 'research/checklist_2026-09-17'
MODELS = list(D['poolings'])
LABELS = ['SPECTER', 'SPECTER2', 'SciNCL', 'SciBERT', 'BERT', 'MPNet',
          'MiniLM', 'PubMedBERT', 'BioBERT', 'SimCSE']
COLORS = ['#22648d', '#ce6a32', '#2b876f']


def read(path):
    with Path(path).open(newline='') as f:
        return list(csv.DictReader(f))


def save(path, rows):
    if not rows:
        raise ValueError(f'Empty table: {path}')
    with Path(path).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def verify_files(folder, record):
    for name, digest in record['files'].items():
        assert file_sha(folder / name) == digest, str(folder / name)


def numerical_audit(require_complete):
    a = json.loads((EXIST / 'audit.json').read_text())
    m = json.loads((EXIST / 'manifest.json').read_text())
    assert a['all_complete'] and a['medicine_decomposition_exact']
    assert m['design_sha256'] == file_sha(DESIGN)
    assert m['source_sha256'] == file_sha(ROOT / 'sos_followup/existing_analysis_v2.py')
    assert m['source_sha256'] == file_sha(EXIST / 'source_snapshot.py')
    assert m['metadata_sha256'] == file_sha(ROOT / 'data/analysis_ready_v1/metadata.parquet')
    parent = ROOT / D['parent_report']
    assert m['parent_catalog_sha256'] == file_sha(parent / 'catalog.json')
    for name, digest in m['source_tables'].items():
        assert file_sha(parent / name) == digest, name
    verify_files(EXIST, a)
    preflight = json.loads((RESEARCH / 'input_preflight.json').read_text())
    assert preflight['all_models_pass']
    result = {'existing_results_verified': True, 'input_preflight_all_ten_pass': True,
              'existing_manifest_sha256': file_sha(EXIST / 'manifest.json'),
              'all_complete': False}
    candidate = json.loads((CAND / 'audit.json').read_text())
    candidate_manifest = json.loads((CAND / 'manifest.json').read_text())
    assert candidate['all_complete'] and candidate['source_papers_matched'] == 266240
    assert candidate_manifest['source_sha256'] == file_sha(ROOT / 'sos_followup/candidate_check.py')
    assert candidate_manifest['source_sha256'] == file_sha(CAND / 'source_snapshot.py')
    assert candidate['manifest_sha256'] == file_sha(CAND / 'manifest.json')
    verify_files(CAND, candidate)
    for name, digest in candidate['parent_files'].items():
        assert file_sha(ROOT / name) == digest
    result['candidate_query_match_verified'] = True
    profile = json.loads((PROFILE / 'audit.json').read_text())
    assert profile['all_complete'] and profile['rows'] == 26000
    assert profile['input_sha256'] == file_sha(INP / 'native_input.parquet')
    assert profile['source_sha256'] == file_sha(ROOT / 'sos_followup/input_text_profile.py')
    assert profile['source_sha256'] == file_sha(PROFILE / 'source_snapshot.py')
    verify_files(PROFILE, profile)
    result['source_text_profile_verified'] = True
    audit_path = CMP / 'audit.json'
    if not audit_path.exists():
        if require_complete:
            raise ValueError('Input comparisons are not complete')
        return result
    ca = json.loads(audit_path.read_text())
    assert ca['all_complete'] and ca['independent_neighbor_queries'] == 7800
    verify_files(CMP, ca)
    cm = json.loads((CMP / 'manifest.json').read_text())
    assert cm['design_sha256'] == file_sha(DESIGN)
    for name, digest in cm['source_files'].items():
        assert file_sha(ROOT / name) == digest
        assert file_sha(CMP / 'source_snapshot' / name) == digest
    input_manifest = json.loads((INP / 'input_manifest.json').read_text())
    verify_files(INP, input_manifest)
    assert input_manifest['definition']['source_sha256'] == file_sha(ROOT / 'data/corpus_clean_v1/embedding_input.parquet')
    assert input_manifest['definition']['design_sha256'] == file_sha(DESIGN)
    assert len(input_manifest['cells']) == 130 and all(c['selected'] == 200 for c in input_manifest['cells'])
    rows = reused = checks = 0
    input_audits = {}
    for model in MODELS:
        for condition in D['conditions']:
            ap = RESEARCH / 'input_audit' / (model + '_' + condition + '.json')
            ia = json.loads(ap.read_text())
            folder = INP / condition / model
            sm = json.loads((folder / 'manifest.json').read_text())
            assert ia['all_pass'] and ia['rows'] == ia['token_sequences_checked'] == 26000
            assert ia['source_identity_text_order_checked'] and ia['all_saved_poolings_checked']
            assert ia['manifest_sha256'] == file_sha(folder / 'manifest.json')
            assert ia['manifest_sha256'] == cm['input_manifests'][model + '/' + condition]
            assert ia['auditor_sha256'] == file_sha(ROOT / 'sos_followup/audit_inputs.py')
            assert ia['input_sha256'] == sm['input_sha256']
            for name, digest in sm['source_files'].items():
                assert file_sha(ROOT / name) == digest
                assert file_sha(INP / 'source_snapshot' / name) == digest
            rows += ia['rows']
            reused += ia['native_exact_reuse']
            input_audits[ap.name] = file_sha(ap)
    for field in range(11, 37):
        folder = CMP / 'fields' / str(field)
        fc = json.loads((folder / 'commit.json').read_text())
        verify_files(folder, fc)
        checks += fc['independent_neighbor_queries']
        assert all(c['absolute_error'] < 2e-10 for c in fc['feature_formula_checks'])
    checkpoint = json.loads((RESEARCH / 'resume_checkpoint.json').read_text())
    for name, digest in checkpoint.items():
        assert file_sha(ROOT / name) == digest, 'Resume changed original checkpoint'
    assert rows == 780000 and reused == 260000 and checks == 7800
    if not (RECIPES / 'audit.json').exists():
        if require_complete:
            raise ValueError('Input recipe sensitivity is not complete')
        result['primary_input_complete'] = True
        return result
    ra = json.loads((RECIPES / 'audit.json').read_text())
    rm = json.loads((RECIPES / 'manifest.json').read_text())
    assert ra['all_complete'] and ra['independent_neighbor_queries'] == 6240
    assert rm['design_sha256'] == file_sha(ROOT / 'config/checklist_input_recipes_v1.json')
    assert rm['parent_design_sha256'] == file_sha(DESIGN)
    assert rm['parent_manifest_sha256'] == file_sha(CMP / 'manifest.json')
    assert rm['input_manifests'] == cm['input_manifests']
    verify_files(RECIPES, ra)
    for name, digest in rm['source_files'].items():
        assert file_sha(ROOT / name) == digest
        assert file_sha(RECIPES / 'source_snapshot' / name) == digest
    for field in range(11, 37):
        folder = RECIPES / 'fields' / str(field)
        rc = json.loads((folder / 'commit.json').read_text())
        verify_files(folder, rc)
        assert rc['parent_commit_sha256'] == file_sha(CMP / 'fields' / str(field) / 'commit.json')
    assert ra['primary_cka_max_absolute_error'] < 1e-10 and ra['primary_neighbor_max_absolute_error'] < 1e-12
    result.update(all_complete=True, pilot_rows=26000, representations=30,
                  checked_representation_rows=rows, exact_reused_rows=reused,
                  newly_inferred_rows=rows-reused, input_audits=input_audits,
                  independent_neighbor_queries=checks, real_cka_formula_checks=78,
                  original_resume_checkpoint_unchanged=True,
                  input_comparison_counts=ca['counts'],
                  input_manifest_sha256=file_sha(INP / 'input_manifest.json'),
                  comparison_manifest_sha256=file_sha(CMP / 'manifest.json'))
    result.update(input_recipe_controls_complete=True, alternative_neighbor_queries_checked=6240,
                  total_input_neighbor_queries_checked=14040, input_recipe_counts=ra['counts'],
                  recipe_primary_reproduction_cka_max_error=ra['primary_cka_max_absolute_error'])
    return result


def moments(values):
    x = np.asarray(values, float)
    assert len(x) and np.isfinite(x).all()
    return {'mean': float(x.mean()), 'median': float(np.median(x)),
            'min': float(x.min()), 'max': float(x.max())}


def aggregate_inputs(tables):
    rows = read(CMP / 'effects.csv')
    out = []
    for metric in ['cka', 'rsa', 'neighbors25']:
        for model in MODELS + ['mean_of_ten_fixed_models']:
            for condition in ['title', 'abstract']:
                chosen = [r for r in rows if r['metric'] == metric and
                          (r['model'] == model or model == 'mean_of_ten_fixed_models')
                          and r['input_condition'] == condition]
                assert len(chosen) == (260 if model == 'mean_of_ten_fixed_models' else 26)
                out.append({'metric': metric, 'model': model, 'input_condition': condition,
                            'field_model_cells': len(chosen),
                            **{col: float(np.mean([float(r[col]) for r in chosen])) for col in
                               ['model_change_at_full', 'input_change_from_full', 'model_minus_input']},
                            'cells_model_change_larger': sum(float(r['model_minus_input']) > 0 for r in chosen)})
    save(tables / 'input_effects_by_model.csv', out)
    by_field = []
    for metric in ['cka', 'rsa', 'neighbors25']:
        for field in range(11, 37):
            for condition in ['title', 'abstract']:
                chosen = [r for r in rows if r['metric'] == metric and int(r['field_id']) == field
                          and r['input_condition'] == condition]
                assert len(chosen) == 10
                by_field.append({'metric': metric, 'field_id': field, 'input_condition': condition,
                                 **{col: float(np.mean([float(r[col]) for r in chosen])) for col in
                                    ['model_change_at_full', 'input_change_from_full', 'model_minus_input']}})
    save(tables / 'input_effects_by_field.csv', by_field)
    stability = read(CMP / 'stability.csv')
    alerts = [r for r in stability if r['passes_operational_screen'] != 'True']
    if alerts:
        save(tables / 'input_stability_alerts.csv', alerts)
    screen = []
    for model in MODELS + ['mean_of_ten_fixed_models']:
        for condition in ['title', 'abstract']:
            ss = [r for r in stability if r['model'] == model and r['input_condition'] == condition]
            assert len(ss) == 26
            screen.append({'model': model, 'input_condition': condition, 'fields': len(ss),
                           'pass': sum(r['passes_operational_screen'] == 'True' for r in ss),
                           'max_median_change': max(float(r['absolute_median_change']) for r in ss),
                           'max_central95_width': max(float(r['central95_width500']) for r in ss)})
    save(tables / 'input_stability_by_model.csv', screen)
    conditions = []
    shape, nn = read(CMP / 'shape.csv'), read(CMP / 'neighbors.csv')
    for condition in D['conditions']:
        sh = [r for r in shape if r['kind'] == 'model' and r['input_a'] == condition]
        n = [r for r in nn if r['kind'] == 'model' and r['input_a'] == condition and r['k'] == '25']
        assert len(sh) == len(n) == 1170
        conditions.append({'input_condition': condition,
                           'mean_cka': np.mean([float(r['cka_debiased']) for r in sh]).item(),
                           'mean_rsa': np.mean([float(r['rsa_spearman']) for r in sh]).item(),
                           'mean_neighbors25': np.mean([float(r['mean_overlap']) for r in n]).item()})
    save(tables / 'between_models_by_input.csv', conditions)
    audits = []
    for model in MODELS:
        for condition in D['conditions']:
            a = json.loads((RESEARCH / 'input_audit' / (model+'_'+condition+'.json')).read_text())
            audits.append({k: a[k] for k in ['model', 'condition', 'rows', 'truncated_rows',
                                           'original_tokens', 'lost_tokens', 'native_exact_reuse']})
    save(tables / 'input_tokens_and_truncation.csv', audits)
    transitions = read(CMP / 'all_transition_effects.csv')
    secondary = {metric: {k: np.mean([float(r[k]) for r in transitions if r['metric'] == metric]).item()
                          for k in ['model_change_all_inputs', 'input_change_all_transitions', 'model_minus_input']}
                 for metric in ['cka', 'rsa', 'neighbors25']}
    return {'effects_by_model': out, 'stability_by_model': screen,
            'stability_failures': alerts,
            'between_models_by_input': conditions, 'all_transitions_secondary': secondary,
            'stability_scope': '20 subsets within the fixed pilot, not population confidence intervals'}


def aggregate_recipes(tables):
    rows = read(RECIPES / 'effects.csv')
    out = []
    for recipe in ['mean','cls','sep']:
        for metric in ['cka','neighbors10','neighbors25','neighbors50']:
            for model in MODELS + ['mean_of_ten_fixed_models']:
                for condition in ['title','abstract']:
                    chosen = [r for r in rows if r['recipe']==recipe and r['metric']==metric and
                              (r['model']==model or model=='mean_of_ten_fixed_models') and r['input_condition']==condition]
                    assert len(chosen)==(260 if model=='mean_of_ten_fixed_models' else 26)
                    out.append({'recipe':recipe,'metric':metric,'model':model,'input_condition':condition,
                                **{k:float(np.mean([float(r[k]) for r in chosen])) for k in
                                   ['model_change_at_full','input_change_from_full','model_minus_input']}})
    save(tables / 'input_recipe_effects_by_model.csv', out)
    return out


def figure_save(fig, folder, name):
    for extension in ['png', 'pdf', 'svg']:
        fig.savefig(folder / (name+'.'+extension), dpi=190, bbox_inches='tight')
    plt.close(fig)


def figure_time(summary, folder):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.1))
    x = np.arange(5)
    temporal = summary['temporal']
    for i, (name, label) in enumerate([('cka_primary', 'All available papers'),
                                      ('cka_equal2048', '2,048 papers (subset medians)'),
                                      ('cka_quality', 'Quality screen')]):
        axes[0].plot(x, temporal[name]['period_means'], label=label, color=COLORS[i],
                     marker=['o','s','^'][i], linestyle=['-','--',':'][i])
    for i, (name, label) in enumerate([('neighbors_all_k25', 'All available candidates'),
                                      ('neighbors_2048_mean_k25', '2,048 equal candidates')]):
        axes[1].plot(x, np.array(temporal[name]['period_means'])*100, color=COLORS[i],
                     marker=['o','s'][i], label=label)
    same_queries = summary['candidate_query_check']['25']['fixed_queries_all_candidates']['period_means']
    axes[1].plot(x, np.array(same_queries)*100, color=COLORS[2], marker='^', linestyle=':',
                 label='All candidates; same 2,048 queries')
    for ax in axes:
        ax.set_xticks(x, ['2000–04','2005–09','2010–14','2015–19','2020–24'])
        ax.tick_params(axis='x', labelsize=9)
        ax.grid(axis='y', alpha=.2)
        ax.legend(fontsize=8, frameon=False)
        ax.spines[['top','right']].set_visible(False)
    axes[0].set(title='A   Shape agreement', ylabel='Corrected linear CKA (mean)')
    axes[1].set(title='B   Shared neighbors: candidate size changes the trend', ylabel='Shared top-25 neighbors (%)')
    fig.text(.01, -.025, 'Equal weights for 26 fields and 45 model pairs. Descriptive comparisons of fixed current models; no causal historical trend.', fontsize=8)
    fig.tight_layout()
    figure_save(fig, folder, '02_time_and_candidate_size')


def figure_biomedical(folder):
    rows = read(EXIST / 'biomedical_pair_groups.csv')
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    fields, labels = [27,21,31,26], ['Medicine','Energy','Physics &\nastronomy','Mathematics']
    for ax, outcome in zip(axes, ['cka_primary','neighbors_2048_mean_k25']):
        for i, label in enumerate(['Neither biomedical model (28 pairs)',
                                    'One biomedical model (16 pairs)', 'BioBERT–PubMedBERT (1 pair)']):
            vals = [next(float(r['mean']) for r in rows if r['outcome']==outcome and
                         int(r['field_id'])==f and int(r['biomedical_models_in_pair'])==i) for f in fields]
            scale = 100 if outcome.startswith('neighbors') else 1
            ax.bar(np.arange(4)+(i-1)*.24, np.array(vals)*scale, width=.23, color=COLORS[i], label=label)
        ax.set_xticks(range(4), labels, fontsize=9)
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y', alpha=.15)
    axes[0].set(title='A   Shape agreement', ylabel='Corrected linear CKA (mean)', ylim=(0,1))
    axes[1].set(title='B   Shared neighbors with 2,048 candidates', ylabel='Shared top-25 neighbors (%)', ylim=(0,65))
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=3, fontsize=8, frameon=False, bbox_to_anchor=(.5,-.035))
    fig.tight_layout(rect=(0,.07,1,1))
    figure_save(fig, folder, '03_medicine_and_biomedical_models')


def figure_families(folder):
    rows = read(EXIST / 'family_groups.csv')
    families = ['citation_document','masked_language','sentence_contrastive']
    labels = ['Citation\ndocument (3)', 'Masked\nlanguage (4)', 'Sentence\ncontrastive (3)']
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.7))
    for ax, outcome, title in zip(axes, ['cka_primary','neighbors_2048_mean_k25'],
                                  ['A   Shape agreement', 'B   Shared top-25 neighbors (%)']):
        mat = np.full((3,3), np.nan); counts = np.zeros((3,3), int)
        for r in rows:
            if r['outcome'] != outcome: continue
            i,j = families.index(r['family_a']), families.index(r['family_b'])
            mat[i,j] = mat[j,i] = float(r['mean'])*(100 if outcome.startswith('neighbors') else 1)
            counts[i,j] = counts[j,i] = int(r['model_pairs'])
        vmax = 65 if outcome.startswith('neighbors') else 1
        ax.imshow(mat, vmin=0, vmax=vmax, cmap='Blues')
        for i in range(3):
            for j in range(3):
                number = f'{mat[i,j]:.1f}%' if outcome.startswith('neighbors') else f'{mat[i,j]:.3f}'
                ax.text(j, i, number+f'\n{counts[i,j]} pairs', ha='center', va='center',
                        color='white' if mat[i,j]>.62*vmax else '#162e41', fontsize=10)
        ax.set_xticks(range(3), labels, fontsize=9); ax.set_yticks(range(3), labels, fontsize=9)
        ax.set_title(title)
    fig.text(.01,.01,'Groups describe final training objectives, not disjoint training corpora. Means use equal field/period/pair weights.',fontsize=8)
    fig.tight_layout(rect=(0,.04,1,1))
    figure_save(fig, folder, '04_training_objective_families')


def figure_interactions(folder, field_names):
    rows = read(EXIST / 'model_by_field.csv')
    fields = sorted(field_names)
    fig, axes = plt.subplots(1, 2, figsize=(11, 9.5), sharey=True)
    labels = [field_names[f].replace('Biochemistry, Genetics and Molecular Biology','Biochemistry / genetics').replace('Economics, Econometrics and Finance','Economics / finance').replace('Business, Management and Accounting','Business / management').replace('Pharmacology, Toxicology and Pharmaceutics','Pharmacology / toxicology') for f in fields]
    for ax, outcome, title in zip(axes, ['cka_primary','neighbors_2048_mean_k25'],
                                  ['A   Shape: residual agreement', 'B   Neighbors: residual percentage points']):
        values = np.array([[next(float(r['pair_and_field_adjusted_residual']) for r in rows if
                          r['outcome']==outcome and r['model']==m and int(r['field_id'])==f) for m in MODELS] for f in fields])
        limit = .06
        if outcome.startswith('neighbors'): values*=100;limit*=100
        im = ax.imshow(values, cmap='RdBu', vmin=-limit, vmax=limit, aspect='auto')
        ax.set_xticks(range(10), LABELS, rotation=60, ha='right', fontsize=8)
        ax.set_yticks(range(26), labels, fontsize=8)
        ax.set_title(title, fontsize=11)
        fig.colorbar(im, ax=ax, orientation='horizontal', fraction=.035, pad=.15)
    fig.text(.01,.01,'Residuals subtract each field mean and model-pair mean. Positive means more agreement than that additive baseline; not greater accuracy.', fontsize=8)
    fig.tight_layout(rect=(0,.04,1,1))
    figure_save(fig, folder, '05_model_by_field_residuals')


def figure_inputs(inputs, folder):
    rows = inputs['effects_by_model']
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 6.3), sharey=True)
    for ax, metric, title in zip(axes, ['cka','neighbors25'], ['A   Change in shape (1 − CKA)', 'B   Lost top-25 neighbors (%)']):
        for offset, column, condition, label, color in [(-.24,'model_change_at_full','title','Change model; keep title + abstract',COLORS[0]),
                (0,'input_change_from_full','title','Keep model; remove abstract',COLORS[1]),
                (.24,'input_change_from_full','abstract','Keep model; remove title',COLORS[2])]:
            values = [next(r[column] for r in rows if r['metric']==metric and r['model']==m and r['input_condition']==condition) for m in MODELS]
            scale = 100 if metric=='neighbors25' else 1
            ax.barh(np.arange(10)+offset, np.array(values)*scale, height=.22, label=label, color=color)
        ax.set_yticks(range(10),LABELS);ax.set_title(title,fontsize=11)
        ax.grid(axis='x',alpha=.2);ax.spines[['top','right']].set_visible(False)
        ax.set_xlim(left=0)
    axes[0].invert_yaxis()
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower center',ncol=1,fontsize=9,frameon=False,bbox_to_anchor=(.5,.035))
    fig.text(.01,.01,'26,000 paired papers. Equal field weights; 1,000 candidates per field. Input changes are practical formatting/reading conditions.',fontsize=8)
    fig.tight_layout(rect=(0,.16,1,1))
    figure_save(fig,folder,'01_model_versus_input')


def figure_input_stability(folder, field_names):
    samples = read(CMP / 'stability_replicates.csv')
    screens = read(CMP / 'stability.csv')
    fields = sorted(field_names)
    fig, axes = plt.subplots(1, 2, figsize=(11, 9), sharey=True, sharex=True)
    labels = [field_names[f].replace('Biochemistry, Genetics and Molecular Biology','Biochemistry / genetics').replace('Economics, Econometrics and Finance','Economics / finance').replace('Business, Management and Accounting','Business / management').replace('Pharmacology, Toxicology and Pharmaceutics','Pharmacology / toxicology') for f in fields]
    for ax, condition, title in zip(axes, ['title','abstract'],
            ['A   Remove abstract: retain title', 'B   Remove title: retain abstract']):
        for y, field in enumerate(fields):
            chosen = [r for r in samples if int(r['field_id']) == field and r['input_condition'] == condition]
            vals = [np.mean([float(r['model_minus_input']) for r in chosen if int(r['repeat']) == rep]) for rep in range(20)]
            lo, median, hi = np.quantile(vals, [.025,.5,.975])
            screen = next(r for r in screens if int(r['field_id'])==field and r['input_condition']==condition and r['model']=='mean_of_ten_fixed_models')
            ax.hlines(y,lo,hi,color=COLORS[0],linewidth=2)
            ax.plot(median,y,'|',color=COLORS[0],markersize=8)
            ax.plot(float(screen['effect_full1000']),y,'o',color='#222222',markersize=3.5)
            if screen['passes_operational_screen'] != 'True':
                ax.plot(float(screen['effect_full1000']),y,'s',mfc='none',mec='#bd3832',markersize=8)
        ax.axvline(0,color='#777777',linestyle='--',linewidth=1)
        ax.set_yticks(range(26),labels,fontsize=8);ax.set_title(title,fontsize=11)
        ax.set_xlabel('Change model − change input (CKA scale)',fontsize=9)
        ax.grid(axis='x',alpha=.15);ax.spines[['top','right']].set_visible(False)
    axes[0].invert_yaxis()
    axes[0].plot([],[],'o',color='#222222',markersize=4,label='1,000 papers (full pilot field)')
    axes[0].plot([],[],color=COLORS[0],label='Central 95% of 20 subsets of 500')
    axes[0].plot([],[],'s',mfc='none',mec='#bd3832',label='Area-average stability screen failed')
    handles,legend=axes[0].get_legend_handles_labels()
    fig.legend(handles,legend,loc='lower center',ncol=1,frameon=False,fontsize=8,bbox_to_anchor=(.64,.024))
    fig.text(.01,.008,'Means of ten fixed models. Subset ranges describe this fixed pilot; they are not population confidence intervals.',fontsize=8)
    fig.tight_layout(rect=(0,.095,1,1))
    figure_save(fig,folder,'06_input_pilot_stability')


def figure_input_recipes(rows, folder):
    fig,axes=plt.subplots(1,2,figsize=(10.8,4.5))
    for ax,metric,title in zip(axes,['cka','neighbors25'],
                              ['A   Change in shape (1 − CKA)','B   Lost top-25 neighbors (%)']):
        for offset,column,condition,label,color in [(-.24,'model_change_at_full','title','Change model; keep both',COLORS[0]),
                 (0,'input_change_from_full','title','Remove abstract',COLORS[1]),
                 (.24,'input_change_from_full','abstract','Remove title',COLORS[2])]:
            vals=[next(r[column] for r in rows if r['recipe']==recipe and r['metric']==metric and
                      r['model']=='mean_of_ten_fixed_models' and r['input_condition']==condition) for recipe in ['mean','cls','sep']]
            ax.bar(np.arange(3)+offset,np.array(vals)*(100 if metric=='neighbors25' else 1),width=.23,color=color,label=label)
        ax.set_xticks(range(3),['Mean (primary)','CLS','SEP'])
        ax.set_title(title,fontsize=11);ax.grid(axis='y',alpha=.15);ax.spines[['top','right']].set_visible(False)
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower center',ncol=3,frameon=False,fontsize=9,bbox_to_anchor=(.5,.02))
    fig.text(.01,.005,'Only the four word-BERT recipes change. The other six models, paper IDs and candidate sets remain fixed.',fontsize=8)
    fig.tight_layout(rect=(0,.10,1,1))
    figure_save(fig,folder,'07_input_by_pooling_recipe')


def main():
    p=argparse.ArgumentParser();p.add_argument('--require-complete',action='store_true');args=p.parse_args()
    audit=numerical_audit(args.require_complete)
    out=ROOT/'reports/checklist_v1'/('final' if args.require_complete else 'preview')
    tables=out/'tables';figures=out/'figures';tables.mkdir(parents=True,exist_ok=True);figures.mkdir(parents=True,exist_ok=True)
    for source in sorted(EXIST.glob('*.csv')):shutil.copy2(source,tables/source.name)
    for source in sorted(CAND.glob('*.csv')):shutil.copy2(source,tables/source.name)
    for source in sorted(PROFILE.glob('*.csv')):shutil.copy2(source,tables/source.name)
    summary=json.loads((EXIST/'summary.json').read_text())
    summary['candidate_query_check']=json.loads((CAND/'summary.json').read_text())
    summary['source_text_profile']=json.loads((PROFILE/'summary.json').read_text())
    summary.update(report_created_at=utcnow(),status='complete' if audit['all_complete'] else 'existing_results_only',
                   original_phase_unchanged=True,design_sha256=file_sha(DESIGN))
    meta=pq.read_table(ROOT/'data/analysis_ready_v1/metadata.parquet',columns=['field_id','field_display_name'])
    field_names=dict(zip(meta['field_id'].to_pylist(),meta['field_display_name'].to_pylist()))
    field_rows=[]
    source=read(EXIST/'model_by_field.csv')
    for f in sorted(field_names):
        row={'field_id':f,'field_name':field_names[f]}
        for outcome in ['cka_primary','cka_quality','cka_cls','cka_sep','neighbors_2048_mean_k25']:
            chosen=[float(r['mean_agreement_other_nine']) for r in source if r['outcome']==outcome and int(r['field_id'])==f]
            assert len(chosen)==10
            row[outcome]=float(np.mean(chosen))
        field_rows.append(row)
    save(tables/'field_summary_means.csv',field_rows)
    figure_time(summary,figures);figure_biomedical(figures);figure_families(figures);figure_interactions(figures,field_names)
    if audit['all_complete']:
        for source in sorted(CMP.glob('*.csv')):shutil.copy2(source,tables/('input_'+source.name))
        summary['input_pilot']=aggregate_inputs(tables)
        figure_inputs(summary['input_pilot'],figures)
        figure_input_stability(figures,field_names)
        for source in sorted(RECIPES.glob('*.csv')):shutil.copy2(source,tables/('input_recipe_'+source.name))
        summary['input_recipe_effects']=aggregate_recipes(tables)
        figure_input_recipes(summary['input_recipe_effects'],figures)
    write_json(out/'summary.json',summary)
    audit.update(report_created_at=utcnow(),exporter_sha256=file_sha(__file__),existing_partial_attempt_preserved=True,
                 old_stability_alerts_retained=50,not_population_intervals=True)
    write_json(out/'audit.json',audit)
    shutil.copy2(__file__,out/'exporter_snapshot.py')
    write_json(out/'catalog.json',{'created_at':utcnow(),'all_complete':audit['all_complete'],
        'files':{str(p.relative_to(out)):{'sha256':file_sha(p),'bytes':p.stat().st_size}
                 for p in sorted(out.rglob('*')) if p.is_file() and p.name!='catalog.json'}})
    print('CHECKLIST REPORT',out,'COMPLETE:',audit['all_complete'],flush=True)


if __name__=='__main__':main()
