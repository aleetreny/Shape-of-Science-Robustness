"""Size-matched groups, recipes, repeated selections and comparable Subfield dates."""
import gc
import hashlib
import itertools
import json
import numpy as np
import pyarrow.parquet as pq
from sos_analysis.native_data import NativeData
from sos_analysis.reader import EmbeddingCorpus
from sos_analysis.geometry import shape_scores, normalize_rows
from sos_analysis.neighbors import exact_neighbors, independent_neighbors, shared_counts
from sos_followup.pilot_statistics import cosine_grams, cka_matrix, rsa_matrix
from sos_deep.artifacts import ROOT, read_csv, save_csv, freeze, finish, verify_audit
from sos_embed.storage import file_sha, write_json, utcnow, run_lock

CONFIG=ROOT/'config/subfield_controls_v1.json';D=json.loads(CONFIG.read_text())
OUT=ROOT/D['output'];BASE=json.loads((ROOT/'config/analysis_v1.json').read_text())
MODELS=list(BASE['poolings']);WORD=['bert','scibert','pubmedbert','biobert']
NAMES=[m+'/'+p for m,pool in BASE['poolings'].items() for p in (['mean','cls','sep'] if m in WORD else [pool])]
PRIMARY=[m+'/'+BASE['poolings'][m] for m in MODELS]
PAIRS=list(itertools.combinations(range(10),2))


def sample_order(ids,work_ids,level,group):
    prefix=f"{D['seed']}:{level}:{group}:"
    return np.array(sorted(ids,key=lambda i:hashlib.sha256((prefix+work_ids[i]).encode()).digest()),dtype=np.int64)


def prepared_groups(meta):
    records=meta.select(['row_index','work_id','field_id','subfield_id','period_start']).to_pylist()
    groups={};periods={};ids=[r['work_id'] for r in records]
    for r in records:
        for level,column in [('field','field_id'),('subfield','subfield_id')]:
            groups.setdefault((level,str(r[column])),[]).append(r['row_index'])
        periods.setdefault((str(r['subfield_id']),r['period_start']),[]).append(r['row_index'])
    ordered={key:sample_order(value,ids,*key) for key,value in groups.items()}
    fields=meta['field_id'].to_numpy()
    for (level,group),selection in ordered.items():
        if level=='subfield':assert len(np.unique(fields[selection]))==1,('Subfield crosses Fields',group)
    return ordered,periods


def commit(folder,extra):
    write_json(folder/'commit.json',{**extra,'completed_at':utcnow(),
        'files':{p.name:file_sha(p) for p in sorted(folder.iterdir()) if p.is_file() and p.name!='commit.json'}})


def committed(folder):
    if not (folder/'commit.json').exists():return False
    d=json.loads((folder/'commit.json').read_text())
    for name,h in d['files'].items():assert file_sha(folder/name)==h,(folder,name)
    return True


def measure(ids,arrays,recipes=('mean','cls','sep'),procrustes=True):
    names=list(arrays);grams=cosine_grams(list(arrays.values()))
    ck=cka_matrix(grams);rs=rsa_matrix(grams,D['seed'])
    nn={};verified=0
    for name,x in arrays.items():
        nn[name],_=exact_neighbors(x,ids,k=50)
        q=np.unique(np.linspace(0,len(ids)-1,min(5,len(ids)),dtype=int))
        proof=independent_neighbors(x,ids,x[q],ids[q],k=50)
        assert np.array_equal(nn[name][q],proof),name
        verified+=len(q)
    proc={}
    if procrustes:
        proc={(r['model_a'],r['model_b']):r['procrustes_similarity']
              for r in shape_scores([arrays[n] for n in PRIMARY],PRIMARY,procrustes=True)}
    shapes=[];neighbors=[];counts={}
    for recipe in recipes:
        selected=[m+'/'+(recipe if m in WORD else BASE['poolings'][m]) for m in MODELS]
        for i,j in PAIRS:
            a,b=selected[i],selected[j];ai,bi=names.index(a),names.index(b)
            shapes.append({'recipe':recipe,'model_a':MODELS[i],'model_b':MODELS[j],
                'cka_debiased':float(ck[ai,bi]),'rsa_spearman':float(rs[ai,bi]),
                'procrustes_similarity':proc.get((a,b)) if recipe=='mean' else None})
        for k in [10,25,50]:
            c=np.stack([shared_counts(nn[selected[i]],nn[selected[j]],k) for i,j in PAIRS],axis=1)
            if recipe=='mean':counts[k]=c
            chance=k/(len(ids)-1)
            for column,(i,j) in enumerate(PAIRS):
                overlap=float(c[:,column].mean()/k)
                neighbors.append({'recipe':recipe,'model_a':MODELS[i],'model_b':MODELS[j],'k':k,
                                  'mean_overlap':overlap,'chance_adjusted':(overlap-chance)/(1-chance)})
    return shapes,neighbors,counts,verified


def selection_stability(corpus,groups):
    for (level,group),ids in groups.items():
        if level!='subfield':continue
        folder=OUT/'stability'/group;folder.mkdir(parents=True,exist_ok=True)
        if committed(folder):continue
        if len(ids)<D['minimum_stability_rows']:
            write_json(folder/'unavailable.json',{'rows':len(ids),'reason':'Too few to compare two CKA subset sizes'})
            commit(folder,{'status':'too_small','rows':len(ids)});continue
        small=min(D['stability_small_cap'],len(ids)//2);large=min(D['stability_large_cap'],len(ids))
        all_arrays={name:corpus.get(name,ids) for name in PRIMARY}
        vals=np.empty((D['repeats'],2,45));choices=[]
        for rep in range(D['repeats']):
            rng=np.random.default_rng(D['seed']+int(group)*100+rep)
            positions=rng.choice(len(ids),large,replace=False);choices.append(ids[positions])
            grams=cosine_grams([x[positions] for x in all_arrays.values()])
            for si,n in enumerate([small,large]):
                scores=cka_matrix(grams[:,:n,:n]);vals[rep,si]=[scores[i,j] for i,j in PAIRS]
        np.save(folder/'selected_ids.npy',np.stack(choices),allow_pickle=False)
        np.save(folder/'cka_replicates.npy',vals,allow_pickle=False)
        med=np.median(vals,axis=0);width=np.quantile(vals[:,1],.975,axis=0)-np.quantile(vals[:,1],.025,axis=0)
        rows=[]
        for col,(i,j) in enumerate(PAIRS):
            shift=abs(med[1,col]-med[0,col])
            rows.append({'subfield_id':group,'corpus_rows':len(ids),'small_n':small,'large_n':large,
                'model_a':MODELS[i],'model_b':MODELS[j],'repeats':D['repeats'],
                'median_small':float(med[0,col]),'median_large':float(med[1,col]),
                'median_size_change':float(shift),'central95_width':float(width[col]),
                'passes_operational_screen':bool(shift<=D['screen_max_median_change'] and width[col]<=D['screen_max_central_width']),
                'large_sample_equals_whole_group':large==len(ids)})
        save_csv(folder/'summary.csv',rows);commit(folder,{'status':'computed','rows':len(ids),'small':small,'large':large})
        print('SUBFIELD SELECTION STABILITY',group,len(ids),flush=True)


def main():
    with run_lock(OUT):
        verify_audit(ROOT/'data/robustness_v2/subfields_native')
        freeze(OUT,['sos_deep/subfield_controls.py','sos_deep/artifacts.py','config/subfield_controls_v1.json',
                    'sos_followup/pilot_statistics.py','sos_analysis/native_data.py','sos_analysis/reader.py',
                    'sos_analysis/geometry.py','sos_analysis/neighbors.py','sos_embed/storage.py'],
               ['data/robustness_v2/subfields_native/audit.json','data/analysis_ready_v1/metadata.parquet',
                BASE['catalog']],D)
        corpus=NativeData(ROOT,max_bytes=16*1024**3);groups,periods=prepared_groups(corpus.metadata)
        selection_stability(corpus,groups)
        corpus.cache.clear();corpus.cached_bytes=0;gc.collect()
        tasks=[];coverage=[]
        for (level,group),ids in sorted(groups.items()):
            coverage.append({'level':level,'group':group,'corpus_rows':len(ids),
                **{f'eligible_{size}':len(ids)>=size for size in D['sizes']}})
            for size in D['sizes']:
                if len(ids)>=size:tasks.append((level,group,str(size),np.sort(ids[:size]),('mean','cls','sep')))
        fields=corpus.metadata['field_id'].to_numpy();sf=corpus.metadata['subfield_id'].to_pylist()
        work=corpus.metadata['work_id'].to_pylist();period_coverage=[]
        for group in sorted({key[0] for key in periods}):
            eligible=all(len(periods.get((group,p),[]))>=128 for p in [2000,2005,2010,2015,2020])
            for p in [2000,2005,2010,2015,2020]:
                ids=periods.get((group,p),[])
                period_coverage.append({'subfield_id':group,'period_start':p,'rows':len(ids),'eligible_all_five':eligible})
                if eligible:
                    chosen=sample_order(ids,work,'subfield_period',group+'_'+str(p))[:128]
                    tasks.append(('subfield_period',group,str(p),np.sort(chosen),('mean',)))
        save_csv(OUT/'coverage.csv',coverage);save_csv(OUT/'period_coverage.csv',period_coverage)
        union=np.unique(np.concatenate([t[3] for t in tasks]));np.save(OUT/'selection_union.npy',union,allow_pickle=False)
        lookup=np.full(len(corpus.metadata),-1,dtype=np.int64);lookup[union]=np.arange(len(union))
        arrays={}
        # Stream one variant at a time; retain only required rows, not 18 complete 500k matrices.
        reader=EmbeddingCorpus(ROOT,catalog_sha256=BASE['catalog_sha256'])
        for name in NAMES:
            m,p=name.split('/');dim=reader.catalog['models'][m]['dimension']
            x=np.empty((len(union),dim),np.float32);seen=0
            for meta,blocks in reader.iter_aligned({m:p}):
                ix=lookup[meta['row_index'].to_numpy()];keep=ix>=0
                x[ix[keep]]=blocks[m][keep];seen+=int(keep.sum())
            assert seen==len(union);arrays[name]=x
            print('SIZE CONTROL VECTORS',name,len(union),flush=True)
        for z,(level,group,label,ids,recipes) in enumerate(tasks):
            folder=OUT/'groups'/level/group/label;folder.mkdir(parents=True,exist_ok=True)
            if not committed(folder):
                needed=NAMES if len(recipes)>1 else PRIMARY
                selected={n:arrays[n][lookup[ids]] for n in needed}
                shapes,neighbors,counts,verified=measure(ids,selected,recipes,procrustes=level!='subfield_period')
                common={'level':level,'group':group,'selection':label,'rows':len(ids),
                        'field_id':int(fields[ids[0]]) if level!='field' else int(group)}
                save_csv(folder/'shape.csv',[{**common,**r} for r in shapes])
                save_csv(folder/'neighbors.csv',[{**common,**r} for r in neighbors])
                np.save(folder/'row_indices.npy',ids,allow_pickle=False)
                for k,c in counts.items():np.save(folder/f'shared_counts_k{k}.npy',c,allow_pickle=False)
                commit(folder,{**common,'independent_queries':verified})
            write_json(OUT/'progress.json',{'tasks_complete':z+1,'target_tasks':len(tasks),'updated_at':utcnow()})
            print('SIZE CONTROL',level,group,label,z+1,len(tasks),flush=True)
        for table in ['shape','neighbors']:
            save_csv(OUT/(table+'.csv'),[r for t in tasks for r in read_csv(OUT/'groups'/t[0]/t[1]/t[2]/(table+'.csv'))])
        save_csv(OUT/'selection_stability.csv',[r for p in sorted((OUT/'stability').glob('*/summary.csv')) for r in read_csv(p)])
        finish(OUT,groups=len(groups),matched_tasks=len(tasks),union_rows=len(union),
               primary_subfields=sum(r['level']=='subfield' and r['eligible_256'] for r in coverage),
               temporal_subfields=sum(r['eligible_all_five'] and r['period_start']==2000 for r in period_coverage),
               same_ids_across_models_and_recipes=True,all_group_commits_verified=True)
        print('SUBFIELD SIZE AND SELECTION CONTROLS COMPLETE',flush=True)


if __name__=='__main__':main()
