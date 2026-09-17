"""Summaries of fixed-size, composition and per-paper controls, with paired keys."""
import json
from collections import defaultdict
import numpy as np
import pyarrow.parquet as pq
from scipy.stats import spearmanr
from sos_deep.artifacts import ROOT,read_csv,save_csv,verify_audit,freeze,finish
from sos_deep.control_review import stats
from sos_embed.storage import write_json,run_lock

BASE=ROOT/'data/robustness_v2';OUT=BASE/'structural_review_v2'
BIO={'biobert','pubmedbert'}


def aggregate(rows,keys,value):
    groups=defaultdict(list)
    for r in rows:groups[tuple(r[k] for k in keys)].append(float(r[value]))
    return [{**dict(zip(keys,k)),**stats(v)} for k,v in groups.items()]


def size_and_stability():
    src=BASE/'subfield_controls'
    shapes=read_csv(src/'shape.csv'); neighbors=read_csv(src/'neighbors.csv')
    sets=[{r['group'] for r in shapes if r['level']=='subfield' and r['selection']==str(n)} for n in [128,256,512]]
    common=set.intersection(*sets);assert len(common)==183
    output=[];regional=[];within=[]
    for measure,rows,column in [('shape',shapes,'cka_debiased'),('neighbors',neighbors,'mean_overlap')]:
        for population in ['all_eligible','same_183_subfields']:
            subset=[r for r in rows if r['level'] in ['field','subfield'] and
                    (population=='all_eligible' or r['level']=='field' or r['group'] in common)]
            keys=['level','selection','recipe']+(['k'] if measure=='neighbors' else [])
            for r in aggregate(subset,keys,column):output.append({'population':population,'measure':measure,'k':'',**r})
        if measure=='neighbors':continue
        for r in aggregate([r for r in rows if r['level']=='subfield' and r['selection']=='256' and r['recipe']=='mean'],
                           ['group','field_id'],column):regional.append(r)
        selected=[r for r in rows if r['level']=='subfield' and r['selection']=='256' and r['recipe']=='mean']
        for group in ['all','without_biomedical','one_biomedical','both_biomedical']:
            def keep(r):
                n=int(r['model_a'] in BIO)+int(r['model_b'] in BIO)
                return group=='all' or n=={'without_biomedical':0,'one_biomedical':1,'both_biomedical':2}[group]
            for r in aggregate([r for r in selected if keep(r)],['field_id'],column):within.append(dict(model_group=group,**r))
    save_csv(OUT/'matched_size_agreement.csv',output)
    save_csv(OUT/'subfield_fixed256_regions.csv',regional)
    save_csv(OUT/'within_subfields_biomedical.csv',within)
    stability=read_csv(src/'selection_stability.csv');summ=[]
    for whole in [False,True]:
        rs=[r for r in stability if (r['large_sample_equals_whole_group']=='True')==whole]
        summ.append({'large_sample_equals_whole_group':whole,'comparisons':len(rs),
            'subfields':len({r['subfield_id'] for r in rs}),'passed':sum(r['passes_operational_screen']=='True' for r in rs),
            'alerts':sum(r['passes_operational_screen']!='True' for r in rs),
            'max_width':max(float(r['central95_width']) for r in rs),
            'max_median_change':max(float(r['median_size_change']) for r in rs)})
    save_csv(OUT/'subfield_stability_summary.csv',summ)
    alerts=[r for r in stability if r['passes_operational_screen']!='True']
    if alerts:save_csv(OUT/'subfield_stability_alerts.csv',alerts)
    return {'common_subfields_all_sizes':len(common),'all_sizes_counts':list(map(len,sets)),
            'stability':summ,'fixed256_subfields':len(regional)}


def paired_scopes():
    rows=read_csv(BASE/'paired_neighbor_scales/groups.csv')
    keyed={(r['subfield_id'],r['repeat'],r['k'],r['scope']):r for r in rows}
    deltas=[]
    for (sf,rep,k,scope),r in keyed.items():
        if scope!='subfield':continue
        broad=keyed[sf,rep,k,'field']
        deltas.append({'subfield_id':sf,'field_id':r['field_id'],'repeat':rep,'k':k,
                       'subfield':float(r['mean_overlap']),'field':float(broad['mean_overlap']),
                       'subfield_minus_field':float(r['mean_overlap'])-float(broad['mean_overlap'])})
    save_csv(OUT/'paired_scope_changes.csv',deltas)
    grouped=aggregate(deltas,['subfield_id','field_id','k'],'subfield_minus_field')
    save_csv(OUT/'paired_scope_subfield_summary.csv',grouped)
    save_csv(OUT/'paired_scope_field_summary.csv',aggregate(deltas,['field_id','k'],'subfield_minus_field'))
    summary=[]
    for k in ['10','25','50']:
        selected=[r for r in deltas if r['k']==k]
        repeated=aggregate(selected,['repeat'],'subfield_minus_field')
        sfs=[r for r in grouped if r['k']==k]
        summary.append({'k':int(k),'subfields':len(sfs),
            'subfield_mean':float(np.mean([r['subfield'] for r in selected])),
            'field_mean':float(np.mean([r['field'] for r in selected])),
            'mean_difference':float(np.mean([r['subfield_minus_field'] for r in selected])),
            'subfields_lower_agreement':sum(r['mean']<0 for r in sfs),
            'subfields_higher_agreement':sum(r['mean']>0 for r in sfs),
            'min_repeat_mean_difference':min(r['mean'] for r in repeated),
            'max_repeat_mean_difference':max(r['mean'] for r in repeated)})
    save_csv(OUT/'paired_scope_summary.csv',summary)
    paper=pq.read_table(BASE/'paired_neighbor_scales/paper_agreement.parquet').to_pylist()
    meta=pq.read_table(ROOT/'data/analysis_ready_v1/metadata.parquet',columns=['work_id','field_display_name','subfield_display_name']).to_pylist()
    for r in paper:
        r.update(meta[r['row_index']]);r['range_over_repeats']=r['max_over_repeats']-r['min_over_repeats']
    save_csv(OUT/'paper_repetition_summary.csv',aggregate(paper,['scope','k'],'range_over_repeats'))
    examples=[]
    for scope in ['subfield','field']:
        selected=[r for r in paper if r['scope']==scope and r['k']==25]
        for tail,subset in [('lower',sorted(selected,key=lambda r:r['mean_over_repeats'])[:50]),
                            ('upper',sorted(selected,key=lambda r:r['mean_over_repeats'])[-50:])]:
            examples.extend(dict(tail=tail,**r) for r in subset)
    save_csv(OUT/'controlled_paper_examples.csv',examples)
    # Group comparisons weight each selected article equally within each Subfield.
    regional=aggregate([r for r in paper if r['k']==25],['scope','field_id'],'mean_over_repeats')
    save_csv(OUT/'controlled_paper_field_regions.csv',regional)
    save_csv(OUT/'controlled_paper_period_regions.csv',aggregate([r for r in paper if r['k']==25],
             ['scope','period_start'],'mean_over_repeats'))
    return summary


def medicine():
    src=BASE/'medicine_composition'
    raw=read_csv(src/'model_group_summary.csv');change=read_csv(src/'composition_changes.csv')
    summary=aggregate(raw,['field_id','condition','metric','model_group'],'mean_agreement')
    save_csv(OUT/'medicine_composition_summary.csv',summary)
    save_csv(OUT/'medicine_composition_change_summary.csv',aggregate(change,['field_id','metric','model_group'],
                                                                    'balanced_minus_observed'))
    key={(r['field_id'],r['repeat'],r['condition'],r['metric'],r['model_group']):float(r['mean_agreement']) for r in raw}
    contrast=[]
    for field in ['21','26','31']:
        for (f,rep,condition,metric,group),value in key.items():
            if f!='27':continue
            other=key[field,rep,condition,metric,group]
            contrast.append({'field_id':field,'repeat':rep,'condition':condition,'metric':metric,
                'model_group':group,'medicine':value,'comparison_field':other,'medicine_minus_other':value-other})
    save_csv(OUT/'medicine_paired_field_contrasts.csv',contrast)
    save_csv(OUT/'medicine_field_contrast_summary.csv',aggregate(contrast,
         ['field_id','condition','metric','model_group'],'medicine_minus_other'))
    diversity=[]
    comp=read_csv(src/'selected_composition.csv');groups=defaultdict(lambda:defaultdict(int))
    for r in comp:groups[r['field_id'],r['repeat'],r['condition']][r['subfield_id']]+=int(r['papers'])
    for (f,rep,c),counts in groups.items():
        p=np.asarray(list(counts.values()),float);p/=p.sum()
        diversity.append({'field_id':f,'repeat':rep,'condition':c,'represented_subfields':len(p),
                          'effective_subfields_entropy':float(np.exp(-(p*np.log(p)).sum())),
                          'largest_subfield_share':float(p.max())})
    save_csv(OUT/'composition_diversity.csv',diversity)
    # This association is across the 26 fixed Fields; it is not a causal regression.
    byfield={r['field_id']:r['mean'] for r in aggregate([r for r in diversity if r['condition']=='observed_eligible_composition'],
                                                    ['field_id'],'effective_subfields_entropy')}
    associations=[]
    for metric in sorted({r['metric'] for r in raw}):
        values=[r for r in summary if r['condition']=='observed_eligible_composition' and r['metric']==metric and r['model_group']=='all']
        associations.append({'metric':metric,'fields':len(values),'spearman_diversity_agreement':float(spearmanr(
            [byfield[r['field_id']] for r in values],[r['mean'] for r in values]).statistic),
            'interpretation':'Descriptive, correlated Field attributes not separated'})
    save_csv(OUT/'diversity_associations.csv',associations)
    return {'comparisons':len(raw),'field_contrasts':len(contrast),'associations':associations}


def families():
    src=BASE/'family_traits';raw=read_csv(src/'leave_one_model.csv');summary=[]
    for outcome in sorted({r['outcome'] for r in raw}):
        for feature in sorted({r['feature'] for r in raw}):
            rs=[r for r in raw if r['outcome']==outcome and r['feature']==feature]
            vals=[float(r['coefficient']) for r in rs if r['identified']=='True']
            summary.append({'outcome':outcome,'feature':feature,'omissions':len(rs),'identified':len(vals),
                'positive':sum(v>0 for v in vals),'negative':sum(v<0 for v in vals),
                'minimum':min(vals) if vals else None,'maximum':max(vals) if vals else None})
    save_csv(OUT/'family_trait_omission_ranges.csv',summary)
    return {'rows':len(summary),'causal_attribution':False,'exact_training_document_overlap_known':False}


def main():
    parents=['subfield_controls','paired_neighbor_scales','medicine_composition','family_traits']
    with run_lock(OUT):
        for name in parents:verify_audit(BASE/name)
        freeze(OUT,['sos_deep/structural_review_v2.py','sos_deep/artifacts.py','sos_deep/control_review.py'],
               [f'data/robustness_v2/{name}/audit.json' for name in parents],
               {'purpose':'R03 R04 R06 R07 descriptive summaries of already frozen comparisons',
                'same_size_subfields_intersection':183,'primary_k':25,'primary_size':256,
                'medicine_field':27,'comparators':[21,26,31],'no_pair_independence_assumption':True})
        summary={'size':size_and_stability(),'paired_scopes':paired_scopes(),
                 'medicine':medicine(),'families':families()}
        write_json(OUT/'summary.json',summary);finish(OUT,paired_keys_verified=True)
        print('STRUCTURAL REVIEW COMPLETE',flush=True)


if __name__=='__main__':main()
