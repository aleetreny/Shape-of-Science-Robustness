"""Post-result check: hold queries fixed when changing candidate-pool size."""
import csv
import itertools
import json
from pathlib import Path
import numpy as np
from sos_embed.storage import file_sha, object_sha, write_json, utcnow

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/checklist_v1/candidate_check'
LOCAL=ROOT/'data/analysis_v1/neighbors'
CONTROL=ROOT/'data/analysis_v1/robustness_controls'
DESIGN=ROOT/'config/checklist_v1.json'
D=json.loads(DESIGN.read_text());MODELS=list(D['poolings']);PAIRS=list(itertools.combinations(MODELS,2))


def save(name,rows):
    with (OUT/(name+'.csv')).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={'source_sha256':file_sha(__file__),'design_sha256':file_sha(DESIGN),
        'local_manifest_sha256':file_sha(LOCAL/'manifest.json'),
        'control_manifest_sha256':file_sha(CONTROL/'manifest.json'),
        'scope':'post-result query-matched candidate-size check; no new embeddings or neighbor searches'}
    mp=OUT/'manifest.json'
    if mp.exists():assert json.loads(mp.read_text())==manifest,'Use new version for changed implementation'
    else:write_json(mp,manifest)
    (OUT/'source_snapshot.py').write_bytes(Path(__file__).read_bytes())
    lm=json.loads((LOCAL/'manifest.json').read_text());cm=json.loads((CONTROL/'manifest.json').read_text())
    rows=[];parents={};verified=0
    for field in range(11,37):
        for period in D['temporal']['periods']:
            folder=LOCAL/'overlap/local'/f'{field}_{period}';commit=json.loads((folder/'commit.json').read_text())
            assert commit['manifest_sha256']==object_sha(lm)
            for name,digest in commit['files'].items():assert file_sha(folder/name)==digest
            detail=json.loads((folder/'summary.json').read_text())
            assert detail['pairs']==[list(p) for p in PAIRS] and detail['ks']==[10,25,50]
            ids=np.load(folder/'query_row_index.npy');counts=np.load(folder/'shared_counts.npy')
            assert counts.shape==(len(ids),45,3) and len(set(ids))==len(ids)
            path=CONTROL/'equal2048_neighbors/summary'/f'{field}_{period}.json'
            assert file_sha(path)==json.loads(path.with_suffix('.sha.json').read_text())['sha256']
            eq=json.loads(path.read_text());assert eq['manifest_sha256']==object_sha(cm)
            selected=np.array(eq['indices']);assert len(selected)==len(set(selected))==2048
            lookup={v:i for i,v in enumerate(ids)};positions=np.array([lookup[v] for v in selected])
            scores={(r['model_a'],r['model_b'],r['k']):r['mean_overlap'] for r in eq['scores'] if r['recipe']=='mean'}
            for pi,(a,b) in enumerate(PAIRS):
                for ki,k in enumerate([10,25,50]):
                    full=float(counts[:,pi,ki].mean()/k)
                    matched=float(counts[positions,pi,ki].mean()/k)
                    small=float(scores[a,b,k])
                    rows.append({'field_id':field,'period_start':period,'model_a':a,'model_b':b,'k':k,
                        'all_candidates':len(ids),'fixed_queries':2048,'all_queries_all_candidates':full,
                        'fixed_queries_all_candidates':matched,'fixed_queries_2048_candidates':small,
                        'query_selection_change':matched-full,'candidate_change_same_queries':small-matched})
            parents[str(folder.relative_to(ROOT))+'/commit.json']=file_sha(folder/'commit.json')
            parents[str(path.relative_to(ROOT))]=file_sha(path)
            verified+=len(selected)
    save('paired_candidate_comparison',rows)
    period_rows=[];summary={}
    for k in [10,25,50]:
        summary[str(k)]={}
        for outcome in ['all_queries_all_candidates','fixed_queries_all_candidates','fixed_queries_2048_candidates',
                        'query_selection_change','candidate_change_same_queries']:
            values=[]
            for period in D['temporal']['periods']:
                v=np.array([r[outcome] for r in rows if r['k']==k and r['period_start']==period]);assert len(v)==1170
                values.append(float(v.mean()));period_rows.append({'k':k,'outcome':outcome,'period_start':period,'mean':float(v.mean())})
            summary[str(k)][outcome]={'period_means':values,'endpoint_change':values[-1]-values[0]}
    save('paired_candidate_time',period_rows)
    write_json(OUT/'summary.json',summary)
    write_json(OUT/'audit.json',{'all_complete':True,'source_papers_matched':verified,'cells':130,
        'comparison_rows':len(rows),'parent_files':parents,'manifest_sha256':file_sha(mp),'completed_at':utcnow(),
        'files':{p.name:file_sha(p) for p in sorted(OUT.glob('*.csv'))}})
    assert verified==266240 and len(rows)==17550
    print('QUERY-MATCHED CANDIDATE CHECK COMPLETE',flush=True)


if __name__=='__main__':main()
