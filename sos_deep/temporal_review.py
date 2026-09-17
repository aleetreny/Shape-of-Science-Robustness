"""Heterogeneity of time trends; every Field/pair retained, no independent-pair tests."""
import itertools
import json
import numpy as np
from scipy.stats import spearmanr
from sos_deep.artifacts import ROOT, read_csv, save_csv, verify_audit, freeze, finish
from sos_embed.storage import write_json, run_lock
from sos_followup.existing_analysis_v2 import build_arrays

OUT = ROOT / 'data/robustness_v2/temporal_review'
MODELS = list(json.loads((ROOT / 'config/analysis_v1.json').read_text())['poolings'])
PAIRS = list(itertools.combinations(MODELS, 2))


def trend(x):
    x = np.asarray(x, float)
    assert x.shape[1] == 5 and np.isfinite(x).all()
    delta = x[:, -1] - x[:, 0]
    steps = np.diff(x, axis=1)
    slope = x @ np.arange(-2., 3.) / 10
    return delta, slope, (steps > 0).sum(1), (steps < 0).sum(1)


def main():
    with run_lock(OUT):
        src = ROOT / 'data/checklist_v1/existing_v2'
        verify_audit(src); verify_audit(ROOT / 'data/checklist_v1/candidate_check')
        freeze(OUT, ['sos_deep/temporal_review.py', 'sos_deep/artifacts.py',
                     'sos_followup/existing_analysis_v2.py'],
               ['data/checklist_v1/existing_v2/audit.json', 'data/checklist_v1/candidate_check/audit.json',
                'reports/analysis_v1/final/catalog.json'],
               {'purpose': 'R05 all trajectories and control sign consistency; descriptive fixed corpus',
                'periods': [2000, 2005, 2010, 2015, 2020], 'tolerance': 1e-12})
        arrays = build_arrays()
        old = {(r['outcome'], int(r['field_id']), r['model_a'], r['model_b']): r
               for r in read_csv(src / 'temporal_paired_changes.csv')}
        trajectories=[]; field_rows=[]; pair_rows=[]; summary=[]
        for name, x in arrays.items():
            y=x.transpose(0,2,1).reshape(-1,5)
            d,s,inc,dec=trend(y)
            for z,(f,pair) in enumerate(itertools.product(range(11,37),PAIRS)):
                ref=old[name,f,*pair]
                assert abs(d[z]-float(ref['endpoint_change']))<1e-12
                assert abs(s[z]-float(ref['slope_per_five_years']))<1e-12
                trajectories.append({'outcome':name,'field_id':f,'model_a':pair[0],'model_b':pair[1],
                    **{f'value_{year}':float(y[z,i]) for i,year in enumerate([2000,2005,2010,2015,2020])},
                    'endpoint_change':float(d[z]),'slope':float(s[z]),
                    'increasing_steps':int(inc[z]),'decreasing_steps':int(dec[z]),
                    'endpoint_and_slope_same_sign':bool(np.sign(d[z])==np.sign(s[z]))})
            for level,values,keys,destination in [
                ('field',x.mean(2),range(11,37),field_rows),
                ('pair',x.mean(0).T,range(45),pair_rows)]:
                dd,ss,ii,jj=trend(values)
                for z,key in enumerate(keys):
                    row={'outcome':name,'group':key,'endpoint_change':float(dd[z]),'slope':float(ss[z]),
                         'increasing_steps':int(ii[z]),'decreasing_steps':int(jj[z]),
                         'minimum':float(values[z].min()),'maximum':float(values[z].max())}
                    if level=='pair':row.update(model_a=PAIRS[key][0],model_b=PAIRS[key][1])
                    destination.append(row)
                summary.append({'outcome':name,'unit':level,'groups':len(values),
                    'positive_endpoint':int((dd>1e-12).sum()),'negative_endpoint':int((dd< -1e-12).sum()),
                    'all_four_steps_up':int((ii==4).sum()),'all_four_steps_down':int((jj==4).sum()),
                    'nonmonotone':int(((ii>0)&(jj>0)).sum()),'mean_endpoint_change':float(dd.mean()),
                    'min_endpoint_change':float(dd.min()),'max_endpoint_change':float(dd.max())})
        concordance=[]
        for base,checks in [('cka_primary',['cka_equal2048','cka_quality','cka_raw','cka_cls','cka_sep',
                                             'rsa_spearman_primary','procrustes_similarity_primary']),
                            ('neighbors_2048_mean_k25',['neighbors_all_k25','neighbors_2048_mean_k10',
                               'neighbors_2048_mean_k50','neighbors_2048_cls_k25','neighbors_2048_sep_k25'])]:
            for other in checks:
                for level,axis in [('field',1),('pair',0),('field_pair',None)]:
                    da=arrays[base][:,-1,:]-arrays[base][:,0,:]
                    db=arrays[other][:,-1,:]-arrays[other][:,0,:]
                    a=(da.mean(axis) if axis is not None else da).ravel()
                    b=(db.mean(axis) if axis is not None else db).ravel()
                    concordance.append({'primary':base,'control':other,'unit':level,'groups':len(a),
                        'same_endpoint_sign':int((np.sign(a)==np.sign(b)).sum()),
                        'positive_both':int(((a>0)&(b>0)).sum()),'negative_both':int(((a<0)&(b<0)).sum()),
                        'rank_correlation_of_changes':float(spearmanr(a,b).statistic)})
        for name,rows in [('trajectories',trajectories),('fields',field_rows),('pairs',pair_rows),
                          ('heterogeneity',summary),('control_consistency',concordance)]:
            save_csv(OUT/(name+'.csv'),rows)
        decomposition=json.loads((ROOT/'data/checklist_v1/candidate_check/summary.json').read_text())
        for k,d in decomposition.items():
            a=d['all_queries_all_candidates']['endpoint_change']
            b=d['query_selection_change']['endpoint_change']
            c=d['candidate_change_same_queries']['endpoint_change']
            t=d['fixed_queries_2048_candidates']['endpoint_change']
            assert abs(a+b+c-t)<1e-12,(k,a,b,c,t)
        write_json(OUT/'candidate_decomposition.json',decomposition)
        finish(OUT,reconstructed_trajectories=len(trajectories),all_old_endpoints_and_slopes_match=True,
               candidate_decomposition_exact=True,paired_models_not_independent=True)
        print('TEMPORAL HETEROGENEITY VERIFIED',flush=True)


if __name__=='__main__':main()
