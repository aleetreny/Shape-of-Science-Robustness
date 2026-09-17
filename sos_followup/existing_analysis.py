"""Explicit time, discipline and family summaries of verified frozen v1 tables."""
import csv
import itertools
import json
from collections import Counter
from pathlib import Path
import platform

import numpy as np
import pyarrow.parquet as pq
from scipy.stats import spearmanr

from sos_embed.storage import file_sha, write_json, utcnow, run_lock

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config/checklist_v1.json'
D=json.loads(CONFIG.read_text())
SRC=ROOT/D['parent_report']
OUT=ROOT/'data/checklist_v1/existing'
MODELS=list(D['poolings']);PAIRS=list(itertools.combinations(MODELS,2));FIELDS=list(range(11,37));PERIODS=D['temporal']['periods']
I,J=np.triu_indices(10,1)
assert [(MODELS[i],MODELS[j]) for i,j in zip(I,J)]==PAIRS


def read(name):
    return list(csv.DictReader((SRC/'tables'/f'{name}.csv').open()))


def save(name,rows):
    if not rows:raise ValueError('Empty output '+name)
    p=OUT/(name+'.csv');tmp=p.with_suffix('.partial.csv')
    with tmp.open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    tmp.replace(p)


def stats(x):
    x=np.asarray(x,float)
    if not np.isfinite(x).all():raise ValueError('Nonfinite statistic')
    return {'mean':float(x.mean()),'median':float(np.median(x)),'min':float(x.min()),'max':float(x.max()),'q05':float(np.quantile(x,.05)),'q95':float(np.quantile(x,.95))}


def index(row):
    a,b=row['model_a'].split('/')[0],row['model_b'].split('/')[0]
    return FIELDS.index(int(row['field_id'])),PERIODS.index(int(row['period_start'])),PAIRS.index((a,b))


def build_arrays():
    arrays={}
    for row in read('shape_all_stages'):
        stage=row['stage']
        for metric in (['cka_debiased','rsa_spearman','procrustes_similarity'] if stage=='primary' else ['cka_debiased']):
            name=('cka' if metric=='cka_debiased' else metric)+'_'+stage
            arrays.setdefault(name,np.full((26,5,45),np.nan))[index(row)]=float(row[metric])
    arrays['cka_equal2048']=arrays['cka_primary'].copy()
    for r in read('shape_sample_stability'):arrays['cka_equal2048'][index(r)]+=float(r['median2048_minus_full'])
    for r in read('neighbors_local'):
        k=int(r['k']);name=f'neighbors_all_k{k}'
        arrays.setdefault(name,np.full((26,5,45),np.nan))[index(r)]=float(r['mean_overlap'])
    for r in read('neighbors_equal2048'):
        name=f'neighbors_2048_{r["recipe"]}_k{r["k"]}'
        arrays.setdefault(name,np.full((26,5,45),np.nan))[index(r)]=float(r['mean_overlap'])
    for n,x in arrays.items():
        if not np.isfinite(x).all():raise ValueError('Missing cell/pair '+n)
    return arrays


def temporal(arrays):
    period_rows=[];trajectories=[];summary={}
    t=np.arange(5,dtype=float);tc=t-t.mean()
    for name,x in arrays.items():
        for p,year in enumerate(PERIODS):
            period_rows.append({'outcome':name,'period_start':year,'comparisons':1170,**stats(x[:,p,:])})
        deltas=x[:,-1,:]-x[:,0,:];slopes=np.einsum('fpq,p->fq',x,tc)/np.dot(tc,tc)
        for fi,f in enumerate(FIELDS):
            for pi,(a,b) in enumerate(PAIRS):
                steps=np.diff(x[fi,:,pi])
                trajectories.append({'outcome':name,'field_id':f,'model_a':a,'model_b':b,
                  'first':float(x[fi,0,pi]),'last':float(x[fi,-1,pi]),'endpoint_change':float(deltas[fi,pi]),
                  'slope_per_five_years':float(slopes[fi,pi]),'increasing_steps':int((steps>0).sum()),'decreasing_steps':int((steps<0).sum())})
        summary[name]={'period_means':[float(x[:,p,:].mean()) for p in range(5)],
          'endpoint_change':stats(deltas),'increasing_endpoints':int((deltas>0).sum()),
          'decreasing_endpoints':int((deltas<0).sum()),'all_four_steps_increasing':int((np.diff(x,axis=1)>0).all(axis=1).sum()),
          'all_four_steps_decreasing':int((np.diff(x,axis=1)<0).all(axis=1).sum())}
    save('temporal_by_period',period_rows);save('temporal_paired_changes',trajectories)
    field_rows=[]
    for name,x in arrays.items():
        for fi,f in enumerate(FIELDS):
            for p,year in enumerate(PERIODS):field_rows.append({'outcome':name,'field_id':f,'period_start':year,'mean':float(x[fi,p].mean()),'median':float(np.median(x[fi,p]))})
    save('temporal_by_field',field_rows)
    return summary


def profiles():
    table=pq.read_table(ROOT/'data/analysis_ready_v1/metadata.parquet').to_pylist()
    cells={}
    for r in table:cells.setdefault((r['field_id'],r['period_start']),[]).append(r)
    rows=[]
    for (f,p),items in sorted(cells.items()):
        sub=Counter(r['subfield_id'] for r in items);prob=np.array(list(sub.values()))/len(items)
        types=Counter(r['type'] for r in items)
        row={'field_id':f,'period_start':p,'rows':len(items),'distinct_subfields':len(sub),
             'effective_subfields':float(np.exp(-np.sum(prob*np.log(prob)))),'largest_subfield_share':float(max(prob)),
             'mean_abstract_words':float(np.mean([r['abstract_word_count'] for r in items])),
             'mean_title_words':float(np.mean([r['title_word_count'] for r in items])),
             'duplicate_doi_rate':float(np.mean([r['duplicate_doi'] for r in items])),
             'duplicate_text_rate':float(np.mean([r['duplicate_text'] for r in items])),
             'ambiguous_language_rate':float(np.mean([r['language_ambiguous'] for r in items])),
             'short_abstract_rate':float(np.mean([r['abstract_50_79'] for r in items])),
             'type_counts_json':json.dumps(dict(types),sort_keys=True)}
        rows.append(row)
    save('cell_composition',rows)
    return rows


def disciplines(arrays,composition):
    bio=set(D['discipline']['biomedical_models']);groups=np.array([len(set(pair)&bio) for pair in PAIRS]);assert [(groups==i).sum() for i in range(3)]==[28,16,1]
    model_rows=[];pair_rows=[];group_rows=[];decomp=[];desc=[];assoc=[]
    for name,x in arrays.items():
        means=x.mean(axis=1);field_mean=means.mean(axis=1);pair_mean=means.mean(axis=0);grand=means.mean()
        for fi,f in enumerate(FIELDS):
            for mi,m in enumerate(MODELS):
                choose=np.array([m in pair for pair in PAIRS])
                model_rows.append({'outcome':name,'field_id':f,'model':m,'mean_agreement_other_nine':float(means[fi,choose].mean()),'pair_and_field_adjusted_residual':float((means[fi]-field_mean[fi]-pair_mean+grand)[choose].mean())})
            for pi,(a,b) in enumerate(PAIRS):
                pair_rows.append({'outcome':name,'field_id':f,'model_a':a,'model_b':b,'mean':float(means[fi,pi]),'residual':float(means[fi,pi]-field_mean[fi]-pair_mean[pi]+grand)})
            for g in range(3):group_rows.append({'outcome':name,'field_id':f,'biomedical_models_in_pair':g,'model_pairs':int((groups==g).sum()),'mean':float(means[fi,groups==g].mean())})
        for other in [21,31,26]:
            contrast=means[FIELDS.index(27)]-means[FIELDS.index(other)]
            parts=[]
            for g in range(3):
                value=float(contrast[groups==g].mean());weighted=value*float((groups==g).mean());parts.append(weighted)
                decomp.append({'outcome':name,'field_a':27,'field_b':other,'biomedical_models_in_pair':g,'model_pairs':int((groups==g).sum()),'group_difference':value,'weighted_contribution':weighted,'total_difference':float(contrast.mean())})
            assert abs(sum(parts)-contrast.mean())<1e-12
        for feature in ['effective_subfields','largest_subfield_share','mean_abstract_words','duplicate_text_rate','ambiguous_language_rate']:
            vals=np.array([np.mean([r[feature] for r in composition if r['field_id']==f]) for f in FIELDS])
            assoc.append({'outcome':name,'composition_feature':feature,'spearman_across_26_fields':float(spearmanr(field_mean,vals).statistic)})
    save('model_by_field',model_rows);save('pair_by_field_residuals',pair_rows);save('biomedical_pair_groups',group_rows);save('medicine_gap_decomposition',decomp);save('field_composition_associations',assoc)
    return {'groups_pair_counts':[28,16,1],'focus_fields':[27,21,31,26],'interpretation':'Means and additive descriptions; neither causal training effects nor independent field taxonomies'}


def family_design(poolings):
    f=D['families'];obj=f['objective'];domain=f['broad_domain']
    return np.array([[1.,float(obj[a]==obj[b]),float(domain[a]==domain[b]),float(poolings[a]==poolings[b])] for a,b in PAIRS])


def fit(y,x):
    rank=np.linalg.matrix_rank(x)
    if rank<x.shape[1]:raise ValueError('Rank deficient family design')
    beta=np.linalg.lstsq(x,y,rcond=None)[0];sse=np.sum((y-x@beta)**2);sst=np.sum((y-y.mean())**2)
    return beta,float(1-sse/sst)


def families(arrays):
    names=['intercept','same_objective','same_broad_domain','same_primary_pooling']
    perm=np.array([np.random.default_rng(202609170+i).permutation(10) for i in range(D['families']['permutations'])])
    rows=[];loo=[];groups=[];perms=[];summ={}
    keep_names=['cka_primary','cka_equal2048','cka_cls','cka_sep','cka_quality',
                'neighbors_2048_mean_k25','neighbors_2048_cls_k25','neighbors_2048_sep_k25']
    for name in keep_names:
        y=arrays[name].mean(axis=(0,1));poolings=dict(D['poolings'])
        if name=='cka_cls' or '_cls_' in name:
            for m in ['bert','scibert','pubmedbert','biobert']:poolings[m]='cls'
        if name=='cka_sep' or '_sep_' in name:
            for m in ['bert','scibert','pubmedbert','biobert']:poolings[m]='sep'
        x=family_design(poolings);beta,r2=fit(y,x)
        mat=np.eye(10)
        mat[I,J]=y;mat[J,I]=y
        yp=mat[perm[:,I],perm[:,J]];pinv=np.linalg.pinv(x)
        bp=yp@pinv.T;pred=bp@x.T
        r2p=1-np.sum((yp-pred)**2,axis=1)/np.sum((yp-yp.mean(axis=1,keepdims=True))**2,axis=1)
        tail=float((1+(r2p>=r2).sum())/(1+len(r2p)))
        for j,n in enumerate(names):rows.append({'outcome':name,'feature':n,'coefficient':float(beta[j]),'r_squared':r2,'rank':4,'design_condition_number':float(np.linalg.cond(x)),'reference_fraction_R2_ge_observed':tail})
        for pi,rr in enumerate(r2p):perms.append({'outcome':name,'permutation':pi,'r_squared':float(rr)})
        deviations=[];held=[];base=[]
        for m in MODELS:
            keep=np.array([m not in pair for pair in PAIRS]);b2,r22=fit(y[keep],x[keep]);deviations.append(b2)
            held.extend((y[~keep]-x[~keep]@b2)**2);base.extend((y[~keep]-y[keep].mean())**2)
            for j,n in enumerate(names):loo.append({'outcome':name,'omitted_model':m,'feature':n,'coefficient':float(b2[j]),'r_squared':r22})
        obj=D['families']['objective']
        for ga,gb in itertools.combinations_with_replacement(sorted(set(obj.values())),2):
            mask=np.array([sorted([obj[a],obj[b]])==sorted([ga,gb]) for a,b in PAIRS])
            groups.append({'outcome':name,'family_a':ga,'family_b':gb,'model_pairs':int(mask.sum()),'mean':float(y[mask].mean())})
        same=x[:,1].astype(bool);dev=np.array(deviations)
        summ[name]={'coefficients':dict(zip(names,map(float,beta))),'r_squared':r2,'reference_tail_fraction':tail,
          'same_objective_agreement':float(y[same].mean()),'different_objective_agreement':float(y[~same].mean()),
          'leave_one_coefficient_min':dict(zip(names,map(float,dev.min(axis=0)))),
          'leave_one_coefficient_max':dict(zip(names,map(float,dev.max(axis=0)))),
          'leave_one_model_prediction_improvement_over_training_mean':float(1-sum(held)/sum(base))}
    save('family_regression',rows);save('family_leave_one_model',loo);save('family_groups',groups);save('family_permutation_reference',perms)
    return summ


def main():
    with run_lock(OUT):
        cat=json.loads((SRC/'catalog.json').read_text())
        needed=['shape_all_stages','shape_sample_stability','neighbors_local','neighbors_equal2048']
        files={f'tables/{n}.csv':cat['files'][f'tables/{n}.csv'] for n in needed}
        for name,sha in files.items():assert file_sha(SRC/name)==sha,name
        manifest={'schema_version':1,'design_sha256':file_sha(CONFIG),'source_sha256':file_sha(__file__),
            'source_tables':files,'parent_catalog_sha256':file_sha(SRC/'catalog.json'),
            'metadata_sha256':file_sha(ROOT/'data/analysis_ready_v1/metadata.parquet'),
            'interpretation':'descriptive; fixed dependent models; source groups fixed before followup summaries'}
        p=OUT/'manifest.json'
        if p.exists():assert json.loads(p.read_text())==manifest,'New output version required'
        else:write_json(p,manifest)
        (OUT/'source_snapshot.py').write_bytes(Path(__file__).read_bytes())
        arrays=build_arrays();c=profiles()
        result={'completed_at':utcnow(),'temporal':temporal(arrays),'discipline':disciplines(arrays,c),'families':families(arrays)}
        write_json(OUT/'summary.json',result)
        write_json(OUT/'audit.json',{'all_complete':True,'outcomes':len(arrays),'values_per_outcome':5850,
            'source_tables_verified':True,'family_design_full_rank':True,'medicine_decomposition_exact':True,
            'source_sha256':file_sha(__file__),'files':{p.name:file_sha(p) for p in sorted(OUT.glob('*.csv'))}})
        print('EXISTING FOLLOWUP COMPLETE',flush=True)
        print(json.dumps({'time':result['temporal']['neighbors_2048_mean_k25'],'families':result['families']['cka_primary']},indent=2),flush=True)

if __name__=='__main__':main()
