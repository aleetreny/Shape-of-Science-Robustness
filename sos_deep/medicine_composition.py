"""Paired Field composition perturbations at fixed size and period distribution."""
import hashlib
import itertools
import json
import math
import numpy as np
import pyarrow.parquet as pq
from sos_analysis.native_data import NativeData
from sos_analysis.neighbors import exact_neighbors,independent_neighbors,shared_counts
from sos_followup.pilot_statistics import cosine_grams,cka_matrix,rsa_matrix
from sos_deep.artifacts import ROOT,read_csv,save_csv,freeze,finish
from sos_embed.storage import file_sha,write_json,utcnow,run_lock

CONFIG=ROOT/'config/medicine_composition_v1.json';D=json.loads(CONFIG.read_text());OUT=ROOT/D['output']
BASE=json.loads((ROOT/'config/analysis_v1.json').read_text());MODELS=list(BASE['poolings'])
NAMES=[m+'/'+BASE['poolings'][m] for m in MODELS];PAIRS=list(itertools.combinations(range(10),2))


def seed(*parts):
    return int.from_bytes(hashlib.sha256(':'.join(map(str,(D['seed'],*parts))).encode()).digest()[:8],'little')


def eligible_groups(cells,periods,maximum_quota):
    groups=sorted({s for s,p in cells})
    while groups:
        minimum=math.ceil(maximum_quota/len(groups))
        keep=[s for s in groups if min(len(cells.get((s,p),[])) for p in periods)>=minimum]
        if keep==groups:break
        groups=keep
    return groups


def select(cells,groups,field,repeat,periods,quotas):
    observed=[];balanced=[]
    for p,quota in zip(periods,quotas):
        # A common priority for each ID couples the two conditions without favoring a model.
        pool=np.concatenate([cells[s,p] for s in groups]);rng=np.random.default_rng(seed(field,repeat,p))
        order=rng.permutation(pool);observed.extend(order[:quota])
        order_groups=sorted(groups,key=lambda s:hashlib.sha256(f'{seed(field,repeat,p)}:{s}'.encode()).digest())
        budget={s:quota//len(groups)+(i<quota%len(groups)) for i,s in enumerate(order_groups)}
        remaining=dict(budget)
        membership={int(i):s for s in groups for i in cells[s,p]}
        for i in order:
            s=membership[int(i)]
            if remaining[s]>0:balanced.append(i);remaining[s]-=1
        assert not any(remaining.values())
    return np.sort(observed),np.sort(balanced)


def compare(ids,arrays,seed_value):
    grams=cosine_grams(arrays);ck=cka_matrix(grams);rs=rsa_matrix(grams,seed_value)
    neighbors=[];queries=np.linspace(0,len(ids)-1,5,dtype=int)
    for name,x in zip(NAMES,arrays):
        nn,_=exact_neighbors(x,ids,k=50)
        check=independent_neighbors(x,ids,x[queries],ids[queries],k=50)
        assert np.array_equal(nn[queries],check),name
        neighbors.append(nn)
    result=[]
    for col,(i,j) in enumerate(PAIRS):
        common={'model_a':MODELS[i],'model_b':MODELS[j],
                'biomedical_count':len(set([MODELS[i],MODELS[j]])&{'biobert','pubmedbert'})}
        result.extend([{**common,'metric':'cka_debiased','value':float(ck[i,j])},
                       {**common,'metric':'rsa_spearman','value':float(rs[i,j])}])
        for k in [10,25,50]:
            overlap=float(shared_counts(neighbors[i],neighbors[j],k).mean()/k)
            result.append({**common,'metric':f'neighbors_k{k}','value':overlap})
    return result


def main():
    with run_lock(OUT):
        freeze(OUT,['sos_deep/medicine_composition.py','sos_deep/artifacts.py','config/medicine_composition_v1.json',
                    'sos_analysis/native_data.py','sos_analysis/reader.py','sos_analysis/geometry.py',
                    'sos_analysis/neighbors.py','sos_followup/pilot_statistics.py'],
               ['data/analysis_ready_v1/metadata.parquet',BASE['catalog'],
                'research/robustness_2026-09-17/medicine_composition_eligibility.json'],D)
        corpus=NativeData(ROOT,max_bytes=16*1024**3);meta=corpus.metadata;by={}
        for r in meta.select(['row_index','field_id','subfield_id','period_start']).to_pylist():
            by.setdefault(r['field_id'],{}).setdefault((r['subfield_id'],r['period_start']),[]).append(r['row_index'])
        all_records=[];coverage=[];selected=[]
        periods=meta['period_start'].to_numpy();sf=meta['subfield_id'].to_numpy()
        for field,cells in sorted(by.items()):
            groups=eligible_groups(cells,D['periods'],max(D['period_quotas']))
            assert groups,field
            count=sum(len(ids) for (s,p),ids in cells.items() if s in groups)
            coverage.append({'field_id':field,'eligible_subfields':len(groups),'all_subfields':len({s for s,p in cells}),
                             'eligible_papers':count,'excluded_papers':sum(map(len,cells.values()))-count,
                             'subfield_ids':'|'.join(groups),'composition_can_change':len(groups)>1})
            for repeat in range(D['repeats']):
                ids_pair=select(cells,groups,field,repeat,D['periods'],D['period_quotas'])
                if len(groups)==1:assert np.array_equal(*ids_pair)
                for condition,ids in zip(D['conditions'],ids_pair):
                    folder=OUT/'groups'/str(field)/str(repeat)/condition;folder.mkdir(parents=True,exist_ok=True)
                    assert len(ids)==D['rows_per_field'] and len(set(ids))==len(ids)
                    assert [int((periods[ids]==p).sum()) for p in D['periods']]==D['period_quotas']
                    if (folder/'commit.json').exists():
                        c=json.loads((folder/'commit.json').read_text())
                        for name,h in c['files'].items():assert file_sha(folder/name)==h
                        assert np.array_equal(np.load(folder/'row_indices.npy'),ids)
                    else:
                        arrays=[corpus.get(n,ids) for n in NAMES]
                        rows=compare(ids,arrays,seed(field,repeat))
                        save_csv(folder/'comparisons.csv',[{'field_id':field,'repeat':repeat,'condition':condition,**r} for r in rows])
                        np.save(folder/'row_indices.npy',ids,allow_pickle=False)
                        write_json(folder/'commit.json',{'completed_at':utcnow(),'independent_neighbor_queries':50,
                            'files':{p.name:file_sha(p) for p in folder.iterdir() if p.is_file()}})
                    all_records.extend(read_csv(folder/'comparisons.csv'))
                    for p in D['periods']:
                        for s in groups:selected.append({'field_id':field,'repeat':repeat,'condition':condition,'period_start':p,
                            'subfield_id':s,'papers':int(((periods[ids]==p)&(sf[ids]==s)).sum())})
                print('COMPOSITION CONTROL',field,repeat+1,D['repeats'],flush=True)
        save_csv(OUT/'coverage.csv',coverage);save_csv(OUT/'selected_composition.csv',selected)
        save_csv(OUT/'comparisons.csv',all_records)
        summary=[];deltas=[]
        values={}
        for r in all_records:values.setdefault((int(r['field_id']),int(r['repeat']),r['condition'],r['metric']),[]).append(r)
        for (field,rep,condition,metric),rows in sorted(values.items()):
            for label,bio in [('all',None),('without_biomedical',0),('one_biomedical',1),('both_biomedical',2)]:
                chosen=[float(r['value']) for r in rows if bio is None or int(r['biomedical_count'])==bio]
                summary.append({'field_id':field,'repeat':rep,'condition':condition,'metric':metric,
                                'model_group':label,'pairs':len(chosen),'mean_agreement':float(np.mean(chosen))})
        keyed={(r['field_id'],r['repeat'],r['condition'],r['metric'],r['model_group']):r['mean_agreement'] for r in summary}
        for field,rep,condition,metric,label in keyed:
            if condition!=D['conditions'][0]:continue
            a=keyed[field,rep,D['conditions'][0],metric,label];b=keyed[field,rep,D['conditions'][1],metric,label]
            deltas.append({'field_id':field,'repeat':rep,'metric':metric,'model_group':label,
                           'observed':a,'balanced':b,'balanced_minus_observed':b-a})
        save_csv(OUT/'model_group_summary.csv',summary);save_csv(OUT/'composition_changes.csv',deltas)
        assert len(all_records)==26*D['repeats']*2*45*5
        finish(OUT,fields=26,repeats=D['repeats'],all_conditions_same_period_sizes=True,
               comparisons=len(all_records),eligible_papers=sum(r['eligible_papers'] for r in coverage),
               single_subfield_fields=[r['field_id'] for r in coverage if not r['composition_can_change']],
               independent_neighbor_queries=26*D['repeats']*2*50)
        print('MEDICINE COMPOSITION CONTROL COMPLETE',flush=True)


if __name__=='__main__':main()
