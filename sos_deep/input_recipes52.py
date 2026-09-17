"""Input-versus-model sensitivity to saved word-BERT poolings; no inference."""
import csv
import json
from pathlib import Path
import numpy as np
from sos_embed.storage import file_sha,write_json,utcnow,run_lock
from sos_analysis.neighbors import exact_neighbors,independent_neighbors,shared_counts
from .input_analysis52 import verified_inputs,NAMES,COMPARISONS,MODELS,INPUTS,OUT as PRIMARY
from sos_followup.pilot_statistics import cosine_grams,cka_matrix,effect_rows

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config/input52_recipes_v1.json';R=json.loads(CONFIG.read_text())
D=json.loads((ROOT/R['parent_design']).read_text());OUT=ROOT/R['output'];WORDS=R['word_models']
VARIANTS=[(m,D['poolings'][m],c) for m,c in NAMES]
VARIANTS += [(m,p,c) for p in ['cls','sep'] for m,c in NAMES if m in WORDS]
assert len(VARIANTS)==54 and len(set(VARIANTS))==54


def read(path):
    with Path(path).open() as f:return list(csv.DictReader(f))


def save(path,rows):
    with Path(path).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def choice(recipe):
    return [VARIANTS.index((m,recipe if m in WORDS else D['poolings'][m],c)) for m,c in NAMES]


def field_run(field,positions,metadata,arrays):
    target=OUT/'fields'/str(field);target.mkdir(parents=True,exist_ok=True)
    if (target/'commit.json').exists():
        old=json.loads((target/'commit.json').read_text())
        for name,digest in old['files'].items():assert file_sha(target/name)==digest
        return
    source=PRIMARY/'fields'/str(field);pc=json.loads((source/'commit.json').read_text())
    for name,digest in pc['files'].items():assert file_sha(source/name)==digest
    ids=metadata['row_index'].to_numpy()[positions]
    assert np.array_equal(ids,np.load(source/'row_indices.npy')) and len(ids)==D['per_cell']*len(D['temporal']['periods'])
    selected=[arrays[n][positions] for n in VARIANTS]
    ck=cka_matrix(cosine_grams(selected))
    primary_nn=np.load(source/'neighbors.npy');assert primary_nn.shape==(30,len(ids),50)
    neighbors=list(primary_nn);proof_count=0
    for n,x in zip(VARIANTS[30:],selected[30:]):
        nn,_=exact_neighbors(x,ids,k=50)
        query=np.linspace(0,len(ids)-1,10,dtype=int)
        proof=independent_neighbors(x,ids,x[query],ids[query],k=50)
        assert np.array_equal(nn[query],proof),(field,n)
        proof_count+=len(query);neighbors.append(nn)
    neighbors=np.stack(neighbors);np.save(target/'alternative_neighbors.npy',neighbors[30:],allow_pickle=False)
    old_shape={(r['model_a'],r['input_a'],r['model_b'],r['input_b']):float(r['cka_debiased']) for r in read(source/'shape.csv')}
    old_nn={(r['model_a'],r['input_a'],r['model_b'],r['input_b'],int(r['k'])):float(r['mean_overlap']) for r in read(source/'neighbors.csv')}
    shapes=[];neighbor_rows=[];effects=[];max_shape_error=0.;max_neighbor_error=0.
    for recipe in R['recipes']:
        select=choice(recipe);mat=ck[np.ix_(select,select)]
        for i,j in COMPARISONS:
            a,ca=NAMES[i];b,cb=NAMES[j];value=float(mat[i,j])
            shapes.append({'field_id':field,'recipe':recipe,'model_a':a,'input_a':ca,'model_b':b,'input_b':cb,'kind':'model' if ca==cb else 'input','cka_debiased':value})
            if recipe=='mean':max_shape_error=max(max_shape_error,abs(value-old_shape[a,ca,b,cb]))
        er,_=effect_rows(mat,NAMES,MODELS)
        effects.extend({'field_id':field,'recipe':recipe,'metric':'cka',**r} for r in er)
        for k in [10,25,50]:
            matrix=np.eye(30)
            for i,j in COMPARISONS:
                value=float(shared_counts(neighbors[select[i]],neighbors[select[j]],k).mean()/k)
                matrix[i,j]=matrix[j,i]=value
                a,ca=NAMES[i];b,cb=NAMES[j]
                neighbor_rows.append({'field_id':field,'recipe':recipe,'k':k,'model_a':a,'input_a':ca,'model_b':b,'input_b':cb,'kind':'model' if ca==cb else 'input','mean_overlap':value})
                if recipe=='mean':max_neighbor_error=max(max_neighbor_error,abs(value-old_nn[a,ca,b,cb,k]))
            er,_=effect_rows(matrix,NAMES,MODELS)
            effects.extend({'field_id':field,'recipe':recipe,'metric':'neighbors'+str(k),**r} for r in er)
    assert max_shape_error<1e-10 and max_neighbor_error<1e-12
    save(target/'shape.csv',shapes);save(target/'neighbors.csv',neighbor_rows);save(target/'effects.csv',effects)
    write_json(target/'commit.json',{'field_id':field,'rows':len(ids),'independent_neighbor_queries':proof_count,
        'primary_cka_max_absolute_error':max_shape_error,'primary_neighbor_max_absolute_error':max_neighbor_error,
        'parent_commit_sha256':file_sha(source/'commit.json'),'completed_at':utcnow(),
        'files':{p.name:file_sha(p) for p in target.iterdir() if p.is_file() and p.name!='commit.json'}})
    print('INPUT RECIPE CONTROL Field',field,'complete',flush=True)


def main():
    with run_lock(OUT):
        assert json.loads((PRIMARY/'audit.json').read_text())['all_complete']
        meta,primary,parents=verified_inputs()
        names=['sos_deep/input_recipes52.py','sos_deep/input_analysis52.py','sos_followup/pilot_statistics.py',
               'sos_analysis/neighbors.py','sos_analysis/geometry.py','requirements-analysis.txt',
               'config/input52_recipes_v1.json','config/input52_v1.json']
        manifest={'design_sha256':file_sha(CONFIG),'parent_design_sha256':file_sha(ROOT/R['parent_design']),
            'source_files':{n:file_sha(ROOT/n) for n in names},'parent_manifest_sha256':file_sha(PRIMARY/'manifest.json'),
            'input_manifests':parents,'representations':[list(n) for n in VARIANTS],
            'environment':json.loads((PRIMARY/'manifest.json').read_text())['environment']}
        path=OUT/'manifest.json'
        if path.exists():assert json.loads(path.read_text())==manifest,'Use a new output version'
        else:write_json(path,manifest)
        for n,h in manifest['source_files'].items():
            dest=OUT/'source_snapshot'/n;dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():assert file_sha(dest)==h
            else:dest.write_bytes((ROOT/n).read_bytes())
        arrays={(m,D['poolings'][m],c):x for (m,c),x in primary.items()}
        for m,p,c in VARIANTS[30:]:
            arrays[m,p,c]=np.concatenate([np.load(s/(p+'.npy'),allow_pickle=False) for s in sorted((INPUTS/c/m/'shards').glob('[0-9]*'))])
            assert len(arrays[m,p,c])==D['rows']
        fields=meta['field_id'].to_numpy()
        for f in range(11,37):
            field_run(f,np.flatnonzero(fields==f),meta,arrays)
            write_json(OUT/'progress.json',{'state':'running','last_field':f,'updated_at':utcnow()})
        counts={}
        for name in ['shape','neighbors','effects']:
            rows=[]
            for f in range(11,37):rows.extend(read(OUT/'fields'/str(f)/(name+'.csv')))
            save(OUT/(name+'.csv'),rows);counts[name]=len(rows)
        assert counts=={'shape':12870,'neighbors':38610,'effects':6240},counts
        checks=[json.loads((OUT/'fields'/str(f)/'commit.json').read_text()) for f in range(11,37)]
        write_json(OUT/'audit.json',{'all_complete':True,'counts':counts,'completed_at':utcnow(),
            'independent_neighbor_queries':sum(c['independent_neighbor_queries'] for c in checks),
            'primary_cka_max_absolute_error':max(c['primary_cka_max_absolute_error'] for c in checks),
            'primary_neighbor_max_absolute_error':max(c['primary_neighbor_max_absolute_error'] for c in checks),
            'files':{p.name:file_sha(p) for p in sorted(OUT.glob('*.csv'))}})
        write_json(OUT/'progress.json',{'state':'complete','updated_at':utcnow()})
        print('52K INPUT RECIPE CONTROLS COMPLETE',flush=True)


if __name__=='__main__':main()
