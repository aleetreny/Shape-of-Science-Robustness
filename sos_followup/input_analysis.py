"""Paired model versus input effects on the fixed 26k pilot; no production edits."""
import csv
import itertools
import importlib.metadata
import json
import platform
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq

from sos_embed.storage import Store,file_sha,write_json,utcnow,run_lock
from sos_analysis.neighbors import exact_neighbors,independent_neighbors,shared_counts
from sos_analysis.geometry import shape_scores
from .pilot_statistics import cosine_grams,cka_matrix,rsa_matrix,effect_rows

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config/checklist_v1.json';D=json.loads(CONFIG.read_text())
INPUTS=ROOT/'data/checklist_v1/inputs';OUT=ROOT/'data/checklist_v1/input_comparisons'
MODELS=list(D['poolings']);CONDITIONS=D['conditions'];NAMES=[(m,c) for c in CONDITIONS for m in MODELS]
COMPARISONS=[(i,j) for i,j in itertools.combinations(range(len(NAMES)),2) if NAMES[i][0]==NAMES[j][0] or NAMES[i][1]==NAMES[j][1]]
assert len(COMPARISONS)==165


def write_csv(path,rows):
    with Path(path).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def verified_inputs():
    inp=json.loads((INPUTS/'input_manifest.json').read_text())
    for name,digest in inp['files'].items():assert file_sha(INPUTS/name)==digest,name
    manifests={};arrays={};native=pq.read_table(INPUTS/'native_input.parquet')
    for model,condition in NAMES:
        folder=INPUTS/condition/model;m=json.loads((folder/'manifest.json').read_text())
        assert m['condition']==condition and m['model']['key']==model
        for name,digest in m['source_files'].items():
            assert file_sha(ROOT/name)==digest,name
            assert file_sha(INPUTS/'source_snapshot'/name)==digest,name
        path=INPUTS/(('native' if condition=='title_abstract' else condition)+'_input.parquet')
        assert file_sha(path)==m['input_sha256']
        expected=pq.read_table(path,columns=['row_index','work_id','text_sha256'])
        report=Store(folder,m).scan(expected)
        if not report['complete']:raise ValueError('Unfinished input '+model+'/'+condition)
        assert expected['row_index'].equals(native['row_index']) and expected['work_id'].equals(native['work_id'])
        p=D['poolings'][model]
        arrays[(model,condition)]=np.concatenate([np.load(s/(p+'.npy'),allow_pickle=False) for s in sorted((folder/'shards').glob('[0-9]*'))])
        manifests[model+'/'+condition]=file_sha(folder/'manifest.json')
    return native,arrays,manifests


def field_run(field,positions,metadata,arrays):
    out=OUT/'fields'/str(field);out.mkdir(parents=True,exist_ok=True)
    if (out/'commit.json').exists():
        c=json.loads((out/'commit.json').read_text())
        for name,digest in c['files'].items():assert file_sha(out/name)==digest,name
        return
    selected=[arrays[n][positions] for n in NAMES]
    ids=metadata['row_index'].to_numpy()[positions]
    periods=metadata['period_start'].to_numpy()[positions]
    assert len(ids)==1000 and all((periods==p).sum()==200 for p in D['temporal']['periods'])
    grams=cosine_grams(selected);ck=cka_matrix(grams);rsa=rsa_matrix(grams,20260917+field)
    # Reconcile the dual-kernel implementation with frozen feature-space CKA on real data.
    checks=[]
    for i,j in [(0,10),(0,1),(6,26)]:
        ref=shape_scores([selected[i],selected[j]],procrustes=False)[0]['cka_debiased']
        delta=abs(ck[i,j]-ref);assert delta<2e-10,(field,i,j,delta)
        checks.append({'a':i,'b':j,'absolute_error':float(delta)})
    records=[]
    for i,j in COMPARISONS:
        a,ca=NAMES[i];b,cb=NAMES[j]
        records.append({'field_id':field,'model_a':a,'input_a':ca,'model_b':b,'input_b':cb,'kind':'model' if ca==cb else 'input','rows':1000,'cka_debiased':float(ck[i,j]),'rsa_spearman':float(rsa[i,j])})
    write_csv(out/'shape.csv',records)
    neighbors=[];verified=0
    for name,x in zip(NAMES,selected):
        nn,info=exact_neighbors(x,ids,k=50)
        anchor=np.arange(0,1000,100)
        proof=independent_neighbors(x,ids,x[anchor],ids[anchor],k=50)
        assert np.array_equal(nn[anchor],proof),(field,name)
        neighbors.append(nn);verified+=len(anchor)
    neighbors=np.stack(neighbors);np.save(out/'neighbors.npy',neighbors,allow_pickle=False);np.save(out/'row_indices.npy',ids,allow_pickle=False)
    matrices={};records=[]
    for k in [10,25,50]:
        mat=np.eye(30)
        for i,j in COMPARISONS:
            overlap=float(shared_counts(neighbors[i],neighbors[j],k).mean()/k);mat[i,j]=mat[j,i]=overlap
            a,ca=NAMES[i];b,cb=NAMES[j]
            records.append({'field_id':field,'k':k,'model_a':a,'input_a':ca,'model_b':b,'input_b':cb,'kind':'model' if ca==cb else 'input','mean_overlap':overlap,'chance_adjusted':(overlap-k/999)/(1-k/999)})
        matrices[k]=mat
    write_csv(out/'neighbors.csv',records)
    effects=[];overall=[]
    for metric,matrix in [('cka',ck),('rsa',rsa),('neighbors25',matrices[25])]:
        rr,global_effect=effect_rows(matrix,NAMES,MODELS)
        effects.extend({'field_id':field,'metric':metric,**r} for r in rr)
        overall.append({'field_id':field,'metric':metric,**global_effect})
    write_csv(out/'effects.csv',effects);write_csv(out/'all_transition_effects.csv',overall)
    samples=[]
    for repeat in range(D['stability']['repeats']):
        rng=np.random.default_rng(20260917000+100*field+repeat)
        chosen=np.sort(np.concatenate([rng.choice(np.flatnonzero(periods==p),100,replace=False) for p in D['temporal']['periods']]))
        sub=cka_matrix(grams[:,chosen][:,:,chosen]);rr,_=effect_rows(sub,NAMES,MODELS)
        samples.extend({'field_id':field,'repeat':repeat,**r} for r in rr)
    write_csv(out/'stability_replicates.csv',samples)
    stability=[]
    for effect in [r for r in effects if r['metric']=='cka']:
        vals=np.array([r['model_minus_input'] for r in samples if r['model']==effect['model'] and r['input_condition']==effect['input_condition']])
        error=abs(float(np.median(vals))-effect['model_minus_input']);width=float(np.quantile(vals,.975)-np.quantile(vals,.025))
        stability.append({'field_id':field,'model':effect['model'],'input_condition':effect['input_condition'],'effect_full1000':effect['model_minus_input'],
              'median_effect500':float(np.median(vals)),'absolute_median_change':error,'central95_width500':width,
              'passes_operational_screen':error<=D['stability']['max_median_effect_change'] and width<=D['stability']['max_central95_width']})
    # Averaging ten fixed models is also reported; model pairs are not treated as independent replicates.
    for condition in ['title','abstract']:
        full=np.mean([r['model_minus_input'] for r in effects if r['metric']=='cka' and r['input_condition']==condition])
        vals=np.array([np.mean([r['model_minus_input'] for r in samples if r['repeat']==rep and r['input_condition']==condition]) for rep in range(D['stability']['repeats'])])
        error=abs(float(np.median(vals))-full);width=float(np.quantile(vals,.975)-np.quantile(vals,.025))
        stability.append({'field_id':field,'model':'mean_of_ten_fixed_models','input_condition':condition,'effect_full1000':float(full),
              'median_effect500':float(np.median(vals)),'absolute_median_change':error,'central95_width500':width,
              'passes_operational_screen':error<=D['stability']['max_median_effect_change'] and width<=D['stability']['max_central95_width']})
    write_csv(out/'stability.csv',stability)
    write_json(out/'commit.json',{'field_id':field,'rows':len(ids),'completed_at':utcnow(),'independent_neighbor_queries':verified,'feature_formula_checks':checks,
        'files':{p.name:file_sha(p) for p in sorted(out.iterdir()) if p.name!='commit.json'}})
    print('INPUT COMPARISONS Field',field,'complete',flush=True)


def main():
    with run_lock(OUT):
        meta,arrays,parents=verified_inputs()
        source_names=['sos_followup/input_analysis.py','sos_followup/pilot_statistics.py','sos_analysis/geometry.py','sos_analysis/neighbors.py','sos_embed/storage.py','requirements-analysis.txt']
        manifest={'schema_version':1,'design_sha256':file_sha(CONFIG),'input_manifests':parents,'source_files':{n:file_sha(ROOT/n) for n in source_names},'representations':[list(n) for n in NAMES],'unit':'1000 papers per Field; 200 each period','comparisons_per_field':165,
                  'environment':{'python':platform.python_version(),'packages':{p:importlib.metadata.version(p) for p in ['numpy','scipy','pyarrow']}}}
        p=OUT/'manifest.json'
        if p.exists():assert json.loads(p.read_text())==manifest,'Input-analysis version changed'
        else:write_json(p,manifest)
        for n,h in manifest['source_files'].items():
            target=OUT/'source_snapshot'/n;target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():assert file_sha(target)==h
            else:target.write_bytes((ROOT/n).read_bytes())
        field_ids=meta['field_id'].to_numpy()
        for field in sorted(set(field_ids)):
            field_run(int(field),np.flatnonzero(field_ids==field),meta,arrays)
            write_json(OUT/'progress.json',{'state':'running','last_field':int(field),'updated_at':utcnow()})
        counts={};verifications=0
        for name in ['shape','neighbors','effects','all_transition_effects','stability_replicates','stability']:
            rows=[]
            for field in range(11,37):rows.extend(csv.DictReader((OUT/'fields'/str(field)/(name+'.csv')).open()))
            write_csv(OUT/(name+'.csv'),rows);counts[name]=len(rows)
        for field in range(11,37):verifications+=json.loads((OUT/'fields'/str(field)/'commit.json').read_text())['independent_neighbor_queries']
        assert counts=={'shape':4290,'neighbors':12870,'effects':1560,'all_transition_effects':78,'stability_replicates':10400,'stability':572},counts
        write_json(OUT/'audit.json',{'all_complete':True,'counts':counts,'independent_neighbor_queries':verifications,'fields':26,'rows_per_field':1000,'parent_manifests_verified':True,'completed_at':utcnow(),'files':{p.name:file_sha(p) for p in sorted(OUT.glob('*.csv'))}})
        write_json(OUT/'progress.json',{'state':'complete','updated_at':utcnow()})
        print('PAIRED INPUT ANALYSIS COMPLETE',flush=True)

if __name__=='__main__':main()
