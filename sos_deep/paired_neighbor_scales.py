"""Same papers and candidate date counts, two topical search scopes."""
import itertools
import json
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from sos_analysis.native_data import NativeData
from sos_analysis.neighbors import exact_neighbors,independent_neighbors,shared_counts
from sos_deep.subfield_controls import prepared_groups
from sos_deep.artifacts import ROOT,save_csv,freeze,finish
from sos_embed.storage import file_sha,write_json,run_lock

CONFIG=ROOT/'config/paired_neighbor_scales_v1.json';D=json.loads(CONFIG.read_text());OUT=ROOT/D['output']
BASE=json.loads((ROOT/'config/analysis_v1.json').read_text());MODELS=list(BASE['poolings'])
PAIRS=list(itertools.combinations(range(10),2));KS=D['metrics']


def paired_candidates(query_ids,subfield_ids,field_ids,periods,seed,n=256):
    rng=np.random.default_rng(seed);q=set(map(int,query_ids))
    narrow_pool=np.array([i for i in subfield_ids if int(i) not in q])
    extra=rng.choice(narrow_pool,n-len(query_ids),replace=False)
    broad=[]
    for p in np.unique(periods[extra]):
        need=int((periods[extra]==p).sum())
        available=np.array([i for i in field_ids if periods[i]==p and int(i) not in q])
        broad.extend(rng.choice(available,need,replace=False))
    a=np.sort(np.concatenate([query_ids,extra]));b=np.sort(np.concatenate([query_ids,broad]))
    assert len(set(a))==len(set(b))==n and q<=set(a) and q<=set(b)
    assert np.array_equal(np.sort(periods[a]),np.sort(periods[b]))
    return a,b


def main():
    with run_lock(OUT):
        freeze(OUT,['sos_deep/paired_neighbor_scales.py','sos_deep/artifacts.py','sos_deep/subfield_controls.py',
                    'config/paired_neighbor_scales_v1.json','config/subfield_controls_v1.json',
                    'sos_analysis/native_data.py','sos_analysis/reader.py','sos_analysis/geometry.py','sos_analysis/neighbors.py'],
               ['data/analysis_ready_v1/metadata.parquet',BASE['catalog']],D)
        data=NativeData(ROOT,max_bytes=2*1024**3);meta=data.metadata;groups,_=prepared_groups(meta)
        fields=meta['field_id'].to_numpy();periods=meta['period_start'].to_numpy()
        keys=sorted([key for key,ids in groups.items() if key[0]=='subfield' and len(ids)>=D['candidates']])
        g=len(keys);queries=np.stack([np.sort(groups[key][:D['queries']]) for key in keys])
        candidates=np.empty((D['repeats'],g,2,D['candidates']),np.int64)
        for gi,key in enumerate(keys):
            for rep in range(D['repeats']):
                a,b=paired_candidates(queries[gi],groups[key],groups['field',str(fields[queries[gi,0]])],
                                      periods,D['seed']+int(key[1])*100+rep,D['candidates'])
                candidates[rep,gi]=[a,b]
        for name,value in [('query_ids',queries),('candidate_ids',candidates)]:
            p=OUT/(name+'.npy')
            if p.exists():assert np.array_equal(np.load(p),value)
            else:np.save(p,value,allow_pickle=False)
        for m,pooling in BASE['poolings'].items():
            folder=OUT/'models'/m;folder.mkdir(parents=True,exist_ok=True)
            if (folder/'commit.json').exists():
                c=json.loads((folder/'commit.json').read_text());assert file_sha(folder/'neighbors.npy')==c['neighbors_sha256'];continue
            raw=data.get(m+'/'+pooling,slice(None));nn=np.empty((D['repeats'],g,2,D['queries'],max(KS)),np.int32)
            checks=0
            for rep in range(D['repeats']):
                for gi,key in enumerate(keys):
                    q=queries[gi]
                    for scope in range(2):
                        ids=candidates[rep,gi,scope]
                        nn[rep,gi,scope],_=exact_neighbors(raw[ids],ids,queries=raw[q],query_ids=q,k=max(KS))
                        proof=independent_neighbors(raw[ids],ids,raw[q[:1]],q[:1],k=max(KS))
                        assert np.array_equal(nn[rep,gi,scope,:1],proof),(m,key,rep,scope)
                        checks+=1
                print('PAIRED SCOPE',m,rep+1,D['repeats'],flush=True)
            np.save(folder/'neighbors.npy',nn,allow_pickle=False)
            write_json(folder/'commit.json',{'neighbors_sha256':file_sha(folder/'neighbors.npy'),
                'independent_queries':checks,'candidate_sha256':file_sha(OUT/'candidate_ids.npy'),
                'query_sha256':file_sha(OUT/'query_ids.npy')})
        loaded=[np.load(OUT/'models'/m/'neighbors.npy',mmap_mode='r').reshape(-1,max(KS)) for m in MODELS]
        count=np.empty((D['repeats']*g*2*D['queries'],45,len(KS)),np.uint8)
        for pi,(i,j) in enumerate(PAIRS):
            for ki,k in enumerate(KS):count[:,pi,ki]=shared_counts(loaded[i],loaded[j],k)
        count=count.reshape(D['repeats'],g,2,D['queries'],45,len(KS))
        np.save(OUT/'shared_counts.npy',count,allow_pickle=False)
        values=count.mean(axis=4)/np.asarray(KS);rows=[];papers=[];pairs=[]
        for gi,key in enumerate(keys):
            f=int(fields[queries[gi,0]])
            for si,scope in enumerate(['subfield','field']):
                for ki,k in enumerate(KS):
                    for rep in range(D['repeats']):
                        val=values[rep,gi,si,:,ki].mean()
                        rows.append({'subfield_id':key[1],'field_id':f,'scope':scope,'repeat':rep,'k':k,
                                     'queries':D['queries'],'candidates':D['candidates'],'mean_overlap':float(val),
                                     'chance_adjusted':float((val-k/(D['candidates']-1))/(1-k/(D['candidates']-1)))})
                        for pi,(a,b) in enumerate(PAIRS):
                            pairs.append({'subfield_id':key[1],'field_id':f,'scope':scope,'repeat':rep,'k':k,
                                'model_a':MODELS[a],'model_b':MODELS[b],
                                'mean_overlap':float(count[rep,gi,si,:,pi,ki].mean()/k)})
                    for qi,idx in enumerate(queries[gi]):
                        v=values[:,gi,si,qi,ki]
                        papers.append({'row_index':int(idx),'subfield_id':key[1],'field_id':f,'period_start':int(periods[idx]),
                            'scope':scope,'k':k,'mean_over_repeats':float(v.mean()),'min_over_repeats':float(v.min()),
                            'max_over_repeats':float(v.max()),'repeats':D['repeats']})
        save_csv(OUT/'groups.csv',rows);pq.write_table(pa.Table.from_pylist(papers),OUT/'paper_agreement.parquet',compression='zstd')
        pq.write_table(pa.Table.from_pylist(pairs),OUT/'model_pair_agreement.parquet',compression='zstd')
        write_json(OUT/'axes.json',{'counts':['repeat','subfield','scope','query','model_pair','k'],
            'subfields':[key[1] for key in keys],'scopes':['subfield','field'],'pairs':[[MODELS[i],MODELS[j]] for i,j in PAIRS],'k':KS})
        finish(OUT,subfields=g,unique_queries=int(queries.size),repeats=D['repeats'],candidate_count=D['candidates'],
               query_ids_and_dates_matched=True,independent_queries=10*D['repeats']*g*2,
               pair_rows=len(pairs),paper_rows=len(papers))
        print('PAIRED NEIGHBOR SCALES COMPLETE',flush=True)


if __name__=='__main__':main()
