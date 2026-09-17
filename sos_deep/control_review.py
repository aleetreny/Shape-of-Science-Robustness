"""Reconstruct inherited stability and compare measures; no scientific reruns."""
import itertools
import json
from collections import defaultdict
from types import SimpleNamespace
import numpy as np
import pyarrow.parquet as pq
from scipy.stats import spearmanr
from sos_deep.artifacts import ROOT, read_csv, save_csv, verify_audit, freeze, finish
from sos_embed.storage import file_sha, write_json, run_lock
from sos_analysis.run_shape import strict_quality

OUT = ROOT / 'data/robustness_v2/control_review'
OLD = ROOT / 'reports/analysis_v1/final'
TABLES = OLD / 'tables'


def stats(values):
    v = np.asarray(list(values), float)
    assert len(v) and np.isfinite(v).all()
    return dict(n=len(v), mean=float(v.mean()), median=float(np.median(v)),
                min=float(v.min()), max=float(v.max()),
                p025=float(np.quantile(v, .025)), p975=float(np.quantile(v, .975)))


def pair(row):
    return row['model_a'].split('/')[0], row['model_b'].split('/')[0]


def alert_review():
    old = {(int(r['field_id']), int(r['period_start']), *pair(r)): r
           for r in read_csv(TABLES / 'shape_sample_stability.csv')}
    full = {(int(r['field_id']), int(r['period_start']), *pair(r)): float(r['cka_debiased'])
            for r in read_csv(TABLES / 'shape_all_stages.csv') if r['stage'] == 'primary'}
    rows=[]; raw_hashes={}
    for path in sorted((ROOT/'data/analysis_v1/shape/stability').glob('*.json')):
        if path.name.endswith('.sha.json'): continue
        digest = file_sha(path)
        assert json.loads(path.with_suffix('.sha.json').read_text())['sha256'] == digest
        raw_hashes[str(path.relative_to(ROOT))]=digest
        obj=json.loads(path.read_text()); groups=defaultdict(dict)
        for r in obj['scores']:
            groups[pair(r)].setdefault(r['sample_size'], []).append(r['cka_debiased'])
        assert len(groups)==45
        for models, bysize in groups.items():
            small=np.asarray(bysize[1024]); large=np.asarray(bysize[2048])
            assert len(small)==len(large)==20
            key=(obj['field_id'],obj['period_start'],*models); before=old[key]
            shift=abs(float(np.median(large)-np.median(small)))
            qlo,qhi=np.quantile(large,[.025,.975]); width=float(qhi-qlo)
            offset=float(np.median(large)-full[key]); passed=shift<=.02 and width<=.04
            for name,value in [('median_change_1024_to_2048',shift),('central95_width_at2048',width),
                               ('median2048_minus_full',offset)]:
                assert abs(value-float(before[name]))<1e-12,(key,name)
            assert passed==(before['passes_operational_screen']=='True')
            rows.append({'field_id':key[0],'period_start':key[1],'model_a':key[2],'model_b':key[3],
                'full_cka':full[key],'median_1024':float(np.median(small)),
                'median_2048':float(np.median(large)),'median_change':shift,
                'p025_2048':float(qlo),'p975_2048':float(qhi),'central95_width':width,
                'median_minus_full':offset,'passes_original_screen':passed,
                'width_alert':bool(width>.04),'size_shift_alert':bool(shift>.02),
                'status':'original_alert_retained' if not passed else 'original_screen_passed'})
    assert len(rows)==5850 and sum(not r['passes_original_screen'] for r in rows)==50
    save_csv(OUT/'original_stability_reconstructed.csv',rows)
    alerts=[r for r in rows if not r['passes_original_screen']]
    save_csv(OUT/'original_50_alerts.csv',alerts)
    write_json(OUT/'stability_raw_hashes.json',raw_hashes)
    return {'comparisons':len(rows),'retained_alerts':len(alerts),
            'alert_cells':len({(r['field_id'],r['period_start']) for r in alerts}),
            'width_alerts':sum(r['width_alert'] for r in rows),
            'shift_alerts':sum(r['size_shift_alert'] for r in rows),
            'max_absolute_offset_to_full':max(abs(r['median_minus_full']) for r in rows),
            'max_width':max(r['central95_width'] for r in rows)}


def metric_review():
    unit_rows=[]
    sources=[('field_period_native',read_csv(TABLES/'shape_all_stages.csv')),
             ('subfield_native',read_csv(ROOT/'data/robustness_v2/subfields_native/shape.csv')),
             ('matched',read_csv(ROOT/'data/robustness_v2/subfield_controls/shape.csv'))]
    for source,rows in sources:
        groups=defaultdict(list)
        for r in rows:
            if source=='field_period_native':
                if r['stage']!='primary':continue
                key=(source,r['field_id'],r['period_start'],'mean')
            elif source=='subfield_native':
                if r['status']!='computed':continue
                key=(source,r['subfield_id'],'all','mean')
            else:key=(r['level'],r['group'],r['selection'],r['recipe'])
            groups[key].append(r)
        for key,group in groups.items():
            assert len(group)==45
            for a,b in itertools.combinations(['cka_debiased','procrustes_similarity','rsa_spearman'],2):
                if any(not r.get(a) or not r.get(b) for r in group):continue
                x=[float(r[a]) for r in group];y=[float(r[b]) for r in group]
                rho=float(spearmanr(x,y).statistic)
                assert np.isfinite(rho)
                unit_rows.append({'source':source,'level':key[0],'group':key[1],'selection':key[2],
                    'recipe':key[3],'metric_a':a,'metric_b':b,'pairs':45,'spearman':rho})
    save_csv(OUT/'metric_consistency_by_unit.csv',unit_rows)
    groups=defaultdict(list)
    for r in unit_rows:groups[(r['source'],r['level'],r['selection'] if r['source']=='matched' else 'all',
                             r['recipe'],r['metric_a'],r['metric_b'])].append(r['spearman'])
    save_csv(OUT/'metric_consistency_summary.csv',[dict(source=k[0],level=k[1],selection=k[2],recipe=k[3],
        metric_a=k[4],metric_b=k[5],**stats(v)) for k,v in groups.items()])
    original={(r['field_id'],r['period_start'],r['comparison']):float(r['spearman_across_45_pairs'])
              for r in read_csv(TABLES/'metric_agreement.csv')}
    for r in unit_rows:
        if r['source']=='field_period_native' and r['metric_a']=='cka_debiased':
            assert abs(r['spearman']-original[r['group'],r['selection'],r['metric_b']])<1e-12
    return {'unit_comparisons':len(unit_rows),'original_metric_correlations_reproduced':True}


def control_stats():
    rows=[]
    def add(source,control,col,subset=None):
        values=read_csv(TABLES/source)
        if subset:values=[r for r in values if subset(r)]
        rows.append({'source':source,'control':control,'measure':col,**stats(float(r[col]) for r in values)})
        rows.append({'source':source,'control':control,'measure':'absolute_'+col,
                     **stats(abs(float(r[col])) for r in values)})
    for stage in ['raw','cls','sep','quality']:
        add('shape_control_deltas.csv',stage,'delta_cka',lambda r:r['stage']==stage)
    for col in ['cka_debiased','procrustes_similarity','rsa_spearman']:
        add('common_text_shape_change.csv','same_text',f'delta_{col}')
    add('minilm_shape_change.csv','minilm512','delta_cka')
    for k in [10,25,50]:
        add('minilm_neighbor_change.csv',f'minilm512_k{k}','delta_overlap',lambda r:int(r['k'])==k)
        add('common_text_neighbor_change.csv',f'same_text_k{k}','delta_overlap',lambda r:int(r['k'])==k)
    save_csv(OUT/'control_magnitudes.csv',rows)
    null=read_csv(TABLES/'shape_permutation_reference.csv')
    save_csv(OUT/'paper_shuffle_reference.csv',[{'metric':m,**stats(float(r[m]) for r in null)}
             for m in ['cka_biased','cka_debiased','procrustes_similarity']])
    q=json.loads((ROOT/'config/analysis_v1.json').read_text())
    meta=pq.read_table(ROOT/'data/analysis_ready_v1/metadata.parquet')
    mask=strict_quality(SimpleNamespace(metadata=meta,design=q))
    ref=json.loads((OLD/'summary.json').read_text())['quality_rows']
    assert int(mask.sum())==ref['retained']
    save_csv(OUT/'quality_flags.csv',[{'flag':name,'marked_rows':int(meta[name].to_numpy().sum()),
                                    'not_additive':True}
         for name in q['quality_sensitivity_flags']+['duplicate_doi','duplicate_text']])
    np.save(OUT/'strict_quality_row_indices.npy',np.flatnonzero(mask))
    return {'quality_retained':int(mask.sum()),'quality_removed':int((~mask).sum()),
        'quality_and_deduplication_joint_control':True,'separate_causal_effect_not_identified':True,
        'control_rows':len(rows)}


def main():
    with run_lock(OUT):
        catalog=json.loads((OLD/'catalog.json').read_text())
        for name,digest in catalog['files'].items():assert file_sha(OLD/name)==digest,name
        for name in ['subfields_native','subfield_controls']:verify_audit(ROOT/'data/robustness_v2'/name)
        freeze(OUT,['sos_deep/control_review.py','sos_deep/artifacts.py','sos_analysis/run_shape.py'],
            ['reports/analysis_v1/final/catalog.json','data/robustness_v2/subfields_native/audit.json',
             'data/robustness_v2/subfield_controls/audit.json','config/analysis_v1.json'],
            {'purpose':'R08-R10 reconstruction and descriptive consistency, no changed thresholds',
             'alert_thresholds':[.02,.04],'sample_quantiles':[.025,.975],
             'uncertainty':'finite fixed corpus selection variation, not population confidence interval'})
        summary={'stability':alert_review(),'metrics':metric_review(),'controls':control_stats()}
        write_json(OUT/'summary.json',summary)
        finish(OUT,all_original_files_verified=True,all_5850_stability_rows_reproduced=True,
               original_50_alerts_retained=True,original_metric_correlations_reproduced=True)
        print('ORIGINAL CONTROLS AND METRIC CONSISTENCY VERIFIED',flush=True)


if __name__=='__main__':main()
