"""Reconcile immutable analysis outputs and export descriptive tables and figures.

No hypothesis tests or population intervals are inferred from model pairs.
This module never changes embeddings or individual comparison results.
"""
import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.stats import rankdata, spearmanr

from sos_embed.storage import file_sha, object_sha, utcnow, write_json
from .run_shape import strict_quality

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/analysis_v1'
DESIGN = json.loads((ROOT/'config/analysis_v1.json').read_text())
MODELS = list(DESIGN['poolings'])
PAIRS = list(itertools.combinations(MODELS, 2))
FIELDS_ES = {11:'Agricultura y biología',12:'Artes y humanidades',13:'Bioquímica y genética',
 14:'Empresa y contabilidad',15:'Ingeniería química',16:'Química',17:'Informática',
 18:'Ciencias de la decisión',19:'Ciencias de la Tierra',20:'Economía y finanzas',21:'Energía',
 22:'Ingeniería',23:'Ciencias ambientales',24:'Inmunología y microbiología',25:'Ciencia de materiales',
 26:'Matemáticas',27:'Medicina',28:'Neurociencias',29:'Enfermería',30:'Farmacología y toxicología',
 31:'Física y astronomía',32:'Psicología',33:'Ciencias sociales',34:'Veterinaria',
 35:'Odontología',36:'Profesiones de la salud'}
LABELS = {'specter':'SPECTER','specter2':'SPECTER2','scincl':'SciNCL','scibert':'SciBERT',
 'bert':'BERT','mpnet':'MPNet','minilm':'MiniLM','pubmedbert':'PubMedBERT',
 'biobert':'BioBERT','simcse':'SimCSE'}


def summary(values):
    x = np.asarray(values, dtype=float)
    if not len(x): return {'count': 0}
    if not np.isfinite(x).all(): raise ValueError('Non-finite report statistic')
    return {'count':len(x),'mean':float(x.mean()),'median':float(np.median(x)),
            'min':float(x.min()),'max':float(x.max()),
            'q05':float(np.quantile(x,.05)),'q95':float(np.quantile(x,.95))}


def key(record):
    a,b = (record[f'model_{c}'].split('/')[0] for c in ('a','b'))
    return (a,b) if MODELS.index(a)<MODELS.index(b) else (b,a)


def checked(path, manifest=None):
    if file_sha(path) != json.loads(path.with_suffix('.sha.json').read_text())['sha256']:
        raise ValueError(f'Changed result: {path}')
    result = json.loads(path.read_text())
    if manifest is not None and result['manifest_sha256'] != object_sha(manifest):
        raise ValueError(f'Wrong result manifest: {path}')
    return result


def table(out, name, rows):
    if not rows: return
    folder = out/'tables'; folder.mkdir(parents=True,exist_ok=True)
    columns = list(dict.fromkeys(c for row in rows for c in row))
    with (folder/(name+'.csv')).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=columns)
        writer.writeheader();writer.writerows(rows)


def verify_manifest(folder):
    manifest=json.loads((folder/'manifest.json').read_text())
    for name,digest in manifest['files'].items():
        if file_sha(ROOT/name)!=digest or file_sha(folder/'source_snapshot'/name)!=digest:
            raise ValueError(f'Changed scientific implementation: {name}')
    return manifest


def shape_report(meta,cells,out,facts,audit,complete):
    folder=BASE/'shape';manifest=verify_manifest(folder)
    quality=strict_quality(SimpleNamespace(metadata=meta,design=DESIGN))
    stages={};flat=[];null=[]
    for stage in ('primary','raw','cls','sep','quality','stability'):
        rows={}
        for cell,ids in cells.items():
            path=folder/stage/f'{cell[0]}_{cell[1]}.json'
            if not path.exists():
                if complete:raise ValueError(f'Missing {path}')
                continue
            x=checked(path,manifest)
            chosen=ids[quality[ids]] if stage=='quality' else ids
            digest=hashlib.sha256(chosen.astype('<i8').tobytes()).hexdigest()
            if x['n']!=len(chosen) or x['indices_sha256']!=digest:
                raise ValueError(f'Shape rows mismatch: {path}')
            if len(x['scores'])!=(1800 if stage=='stability' else 45):
                raise ValueError(f'Wrong pair count: {path}')
            rows[cell]=x
            if stage!='stability':
                for r in x['scores']:
                    if not all(np.isfinite(r[c]) for c in ('cka_debiased','procrustes_similarity')):
                        raise ValueError('Non-finite shape output')
                    flat.append({'stage':stage,'field_id':cell[0],'period_start':cell[1],**r})
            if stage=='primary':
                null.extend({'field_id':cell[0],'period_start':cell[1],**r} for r in x['null_scores'])
        stages[stage]=rows
    audit['shape_cells']={s:len(v) for s,v in stages.items()}
    table(out,'shape_all_stages',flat);table(out,'shape_permutation_reference',null)
    primary=stages['primary']
    facts['shape']={c:summary([r[c] for x in primary.values() for r in x['scores']])
                    for c in ('cka_debiased','procrustes_similarity','rsa_spearman')}
    facts['null']={c:summary([r[c] for r in null]) for c in ('cka_debiased','procrustes_similarity')}
    global_rows=[]
    for label in ('global_base_unit','global_base_raw'):
        x=checked(folder/'global'/f'{label}.json',manifest)
        if x['n']!=400000 or len(x['scores'])!=45:raise ValueError('Wrong global shape coverage')
        global_rows.extend({'stage':label,**r} for r in x['scores'])
    table(out,'shape_global_base',global_rows)
    facts['global_shape']={c:summary([r[c] for r in global_rows if r['stage']=='global_base_unit'])
                          for c in ('cka_debiased','procrustes_similarity','rsa_spearman')}
    pair_rows=[];cell_rows=[]
    for pair in PAIRS:
        selected=[r for x in primary.values() for r in x['scores'] if key(r)==pair]
        row={'model_a':pair[0],'model_b':pair[1],'cells':len(selected)}
        for c in ('cka_debiased','procrustes_similarity','rsa_spearman'):
            row.update({f'{c}_{k}':v for k,v in summary([r[c] for r in selected]).items() if k!='count'})
        pair_rows.append(row)
    for cell,x in primary.items():
        row={'field_id':cell[0],'period_start':cell[1],'n':x['n']}
        for c in ('cka_debiased','procrustes_similarity','rsa_spearman'):
            row[c+'_median']=float(np.median([r[c] for r in x['scores']]))
        cell_rows.append(row)
    table(out,'shape_by_pair',pair_rows);table(out,'shape_by_cell',cell_rows)
    facts['shape_pairs_low_high']={'lowest':sorted(pair_rows,key=lambda r:r['cka_debiased_median'])[:3],
                                  'highest':sorted(pair_rows,key=lambda r:r['cka_debiased_median'])[-3:]}
    facts['shape_cells_low_high']={'lowest':sorted(cell_rows,key=lambda r:r['cka_debiased_median'])[:5],
                                  'highest':sorted(cell_rows,key=lambda r:r['cka_debiased_median'])[-5:]}
    correlations=[]
    for cell,x in primary.items():
        for c in ('procrustes_similarity','rsa_spearman'):
            correlations.append({'field_id':cell[0],'period_start':cell[1],'comparison':c,
               'spearman_across_45_pairs':float(spearmanr([r['cka_debiased'] for r in x['scores']],
                                                       [r[c] for r in x['scores']]).statistic)})
    table(out,'metric_agreement',correlations)
    facts['metric_agreement']={c:summary([r['spearman_across_45_pairs'] for r in correlations if r['comparison']==c])
                              for c in ('procrustes_similarity','rsa_spearman')}
    deltas=[]
    for stage in ('raw','cls','sep','quality'):
        for cell,x in stages[stage].items():
            reference={key(r):r for r in primary[cell]['scores']}
            for r in x['scores']:
                before=reference[key(r)]
                deltas.append({'stage':stage,'field_id':cell[0],'period_start':cell[1],
                    'n_before':primary[cell]['n'],'n_after':x['n'],'model_a':key(r)[0],'model_b':key(r)[1],
                    'cka_before':before['cka_debiased'],'cka_after':r['cka_debiased'],
                    'delta_cka':r['cka_debiased']-before['cka_debiased'],
                    'delta_procrustes':r['procrustes_similarity']-before['procrustes_similarity']})
    table(out,'shape_control_deltas',deltas)
    facts['shape_controls']={s:{'delta':summary([r['delta_cka'] for r in deltas if r['stage']==s]),
        'absolute_delta':summary([abs(r['delta_cka']) for r in deltas if r['stage']==s])}
        for s in ('raw','cls','sep','quality')}
    facts['quality_rows']={'retained':int(quality.sum()),'removed':int((~quality).sum()),
                            'minimum_cell':min(int(quality[ids].sum()) for ids in cells.values())}
    stability=[]
    for cell,x in stages['stability'].items():
        full={key(r):r['cka_debiased'] for r in primary[cell]['scores']}
        for pair in PAIRS:
            small=[r['cka_debiased'] for r in x['scores'] if key(r)==pair and r['sample_size']==1024]
            large=[r['cka_debiased'] for r in x['scores'] if key(r)==pair and r['sample_size']==2048]
            if len(small)!=20 or len(large)!=20:raise ValueError('Wrong subsampling count')
            delta=abs(float(np.median(large)-np.median(small)))
            width=float(np.quantile(large,.975)-np.quantile(large,.025))
            stability.append({'field_id':cell[0],'period_start':cell[1],'model_a':pair[0],'model_b':pair[1],
                'median_change_1024_to_2048':delta,'central95_width_at2048':width,
                'median2048_minus_full':float(np.median(large)-full[pair]),
                'passes_operational_screen':delta<=.02 and width<=.04})
    table(out,'shape_sample_stability',stability)
    if stability:
        facts['sample_stability']={'comparisons':len(stability),'passes':sum(r['passes_operational_screen'] for r in stability),
            'median_change':summary([r['median_change_1024_to_2048'] for r in stability]),
            'central_width':summary([r['central95_width_at2048'] for r in stability]),
            'absolute_delta_to_full':summary([abs(r['median2048_minus_full']) for r in stability])}
    families=[]
    for excluded,members in {'none':[],**DESIGN['family_sensitivity']}.items():
        selected=[r for x in primary.values() for r in x['scores'] if not set(key(r))&set(members)]
        families.append({'excluded_family':excluded,**summary([r['cka_debiased'] for r in selected])})
    table(out,'shape_family_sensitivity',families);facts['shape_families']=families
    return stages,pair_rows,cell_rows


def centroid_report(out,facts):
    x=checked(BASE/'shape/centroids/relations.json')
    if len(x['scores'])!=225 or len(x['edges'])!=16250:raise ValueError('Wrong centroid coverage')
    table(out,'centroid_agreement',x['scores']);table(out,'centroid_distances',x['edges'])
    facts['centroid_agreement']=summary([r['centroid_edge_spearman'] for r in x['scores']])
    period_rows=[];ranks={};lookup={}
    for period in (2000,2005,2010,2015,2020):
        period_rows.append({'period_start':period,**summary([r['centroid_edge_spearman'] for r in x['scores'] if r['period_start']==period])})
        for model in MODELS:
            rows=[r for r in x['edges'] if r['period_start']==period and r['model'].split('/')[0]==model]
            values=rankdata([r['cosine_distance'] for r in rows])
            for row,value in zip(rows,values):
                edge=(row['field_a'],row['field_b']);ranks[period,model,edge]=float(value)
                lookup[period,model,edge]=row['cosine_distance']
    table(out,'centroid_agreement_by_period',period_rows)
    rows=[]
    for period in (2000,2005,2010,2015,2020):
        for edge in itertools.combinations(range(11,37),2):
            values=[ranks[period,m,edge] for m in MODELS]
            rows.append({'period_start':period,'field_a':edge[0],'field_b':edge[1],
                         'median_rank':float(np.median(values)),'rank_min':min(values),'rank_max':max(values),
                         'rank_iqr':float(np.quantile(values,.75)-np.quantile(values,.25))})
    table(out,'centroid_edge_rank_disagreement',rows)
    temporal=[]
    for edge in itertools.combinations(range(11,37),2):
        changes=[ranks[2020,m,edge]-ranks[2000,m,edge] for m in MODELS]
        temporal.append({'field_a':edge[0],'field_b':edge[1],'median_rank_change':float(np.median(changes)),
            'models_closer_in_rank':sum(v<0 for v in changes),'models_farther_in_rank':sum(v>0 for v in changes),
            'minimum_change':min(changes),'maximum_change':max(changes)})
    table(out,'centroid_temporal_rank_changes',temporal)
    facts['centroid_temporal']={'relations':325,'all_ten_same_direction':sum(max(r['models_closer_in_rank'],r['models_farther_in_rank'])==10 for r in temporal),
        'at_least_eight_same_direction':sum(max(r['models_closer_in_rank'],r['models_farther_in_rank'])>=8 for r in temporal),
        'interpretation':'Relative ranks among 325 relations; descriptive endpoints, not historical causal changes'}


def verify_neighbors(folder,manifest,ids,meta,cell=None):
    record=json.loads((folder/'commit.json').read_text())
    if record['manifest_sha256']!=object_sha(manifest):raise ValueError('Neighbor manifest mismatch')
    for name,digest in record['files'].items():
        if file_sha(folder/name)!=digest:raise ValueError('Changed neighbor output')
    query=np.load(folder/'query_row_index.npy');np.testing.assert_array_equal(query,ids)
    if (folder/'neighbors.npy').exists():
        a=np.load(folder/'neighbors.npy',mmap_mode='r')
        if a.shape!=(len(ids),50) or np.any(a<0) or np.any(a>=len(meta)):raise ValueError('Invalid neighbor array')
        if np.any(a==ids[:,None]) or np.any(np.diff(np.sort(a,axis=1),axis=1)==0):raise ValueError('Self or repeated neighbor')
        if cell is not None:
            if np.any(meta['field_id'].to_numpy()[a]!=cell[0]) or np.any(meta['period_start'].to_numpy()[a]!=cell[1]):
                raise ValueError('Candidate escaped its cell')
        elif np.any(meta['cohort'].to_numpy()[a]!='base'):raise ValueError('Global non-base reference')
        if record['stats']['validation']!='exact_match':raise ValueError('Missing independent validation')
    return record


def neighbors_report(meta,cells,out,facts,audit,stages,complete):
    folder=BASE/'neighbors';manifest=verify_manifest(folder);local=[];individual=[];passed=0
    for cell,ids in cells.items():
        path=folder/'overlap/local'/f'{cell[0]}_{cell[1]}'
        if not (path/'commit.json').exists():
            if complete:raise ValueError('Missing neighbor overlap')
            continue
        for model in MODELS:
            r=verify_neighbors(folder/'local'/f'{cell[0]}_{cell[1]}'/model,manifest,ids,meta,cell)
            passed+=r['stats']['independent_queries']
        verify_neighbors(path,manifest,ids,meta)
        x=json.loads((path/'summary.json').read_text());counts=np.load(path/'shared_counts.npy')
        if x['pairs']!=[list(p) for p in PAIRS] or x['ks']!=[10,25,50] or counts.shape!=(len(ids),45,3):
            raise ValueError('Wrong neighbor summary axes')
        for pi,pair in enumerate(PAIRS):
            for ki,k in enumerate((10,25,50)):
                raw=counts[:,pi,ki]/k;chance=k/(len(ids)-1)
                given=next(r for r in x['scores'] if (r['model_a'],r['model_b'],r['k'])==(*pair,k))
                if not np.isclose(raw.mean(),given['mean_overlap'],rtol=0,atol=1e-12):raise ValueError('Neighbor mean differs from counts')
                if not np.isclose(((raw-chance)/(1-chance)).mean(),given['mean_chance_adjusted_overlap'],rtol=0,atol=1e-12):
                    raise ValueError('Chance adjustment mismatch')
                if np.any(counts[:,pi,ki]>k):raise ValueError('Impossible shared count')
                local.append({'field_id':cell[0],'period_start':cell[1],**given})
        value=counts[:,:,1].astype(float)/25
        chance=25/(len(ids)-1)
        individual.append(pa.table({'row_index':ids,'mean_overlap_k25':value.mean(1),
            'mean_adjusted_k25':((value-chance)/(1-chance)).mean(1),
            'min_overlap_k25':value.min(1),'max_overlap_k25':value.max(1)}))
    table(out,'neighbors_local',local)
    audit['local_neighbor_cells']=len(individual);audit['independent_neighbor_queries']=passed
    if not local:return [],[]
    articles=pa.concat_tables(individual).sort_by('row_index')
    identity=meta.take(articles['row_index']).select(['work_id','field_id','period_start','cohort'])
    for column in identity.column_names:
        articles=articles.append_column(column,identity[column])
    pq.write_table(articles,out/'article_neighbor_stability.parquet',compression='zstd')
    facts['article_neighbors']=summary(articles['mean_overlap_k25'].to_numpy())
    pair_rows=[];cell_rows=[]
    for pair in PAIRS:
        rows=[r for r in local if (r['model_a'],r['model_b'])==pair and r['k']==25]
        pair_rows.append({'model_a':pair[0],'model_b':pair[1],
           'cell_mean_overlap':float(np.mean([r['mean_overlap'] for r in rows])),
           'cell_median_overlap':float(np.median([r['mean_overlap'] for r in rows])),
           'cell_mean_adjusted':float(np.mean([r['mean_chance_adjusted_overlap'] for r in rows])),
           'corpus_article_weighted_mean':float(np.average([r['mean_overlap'] for r in rows],weights=[r['queries'] for r in rows]))})
    for cell in cells:
        rows=[r for r in local if (r['field_id'],r['period_start'],r['k'])==(*cell,25)]
        if not rows:continue
        shapes={key(r):r['cka_debiased'] for r in stages['primary'][cell]['scores']}
        cell_rows.append({'field_id':cell[0],'period_start':cell[1],
            'mean_overlap':float(np.mean([r['mean_overlap'] for r in rows])),
            'mean_adjusted':float(np.mean([r['mean_chance_adjusted_overlap'] for r in rows])),
            'shape_neighbor_spearman':float(spearmanr([shapes[key(r)] for r in rows],[r['mean_overlap'] for r in rows]).statistic)})
    table(out,'neighbors_by_pair',pair_rows);table(out,'neighbors_by_cell',cell_rows)
    facts['neighbors']={str(k):{'cell_pair_overlap':summary([r['mean_overlap'] for r in local if r['k']==k]),
            'cell_pair_adjusted':summary([r['mean_chance_adjusted_overlap'] for r in local if r['k']==k])} for k in (10,25,50)}
    facts['neighbor_pair_low_high']={'lowest':sorted(pair_rows,key=lambda r:r['cell_mean_overlap'])[:3],
                                   'highest':sorted(pair_rows,key=lambda r:r['cell_mean_overlap'])[-3:]}
    families=[]
    for excluded,members in {'none':[],**DESIGN['family_sensitivity']}.items():
        vals=[r['mean_overlap'] for r in local if r['k']==25 and not set(key(r))&set(members)]
        families.append({'excluded_family':excluded,**summary(vals)})
    table(out,'neighbor_family_sensitivity',families);facts['neighbor_families']=families
    path=folder/'overlap/global/anchors'
    if (path/'commit.json').exists():
        ids=np.load(path/'query_row_index.npy')
        if len(ids)!=13000:raise ValueError('Wrong global query count')
        for model in MODELS:
            r=verify_neighbors(folder/'global'/model,manifest,ids,meta)
            audit['independent_neighbor_queries']+=r['stats']['independent_queries']
        verify_neighbors(path,manifest,ids,meta)
        x=json.loads((path/'summary.json').read_text());table(out,'neighbors_global',x['scores'])
        counts=np.load(path/'shared_counts.npy',mmap_mode='r')
        if counts.shape!=(13000,45,3):raise ValueError('Wrong global overlap array')
        fields=meta['field_id'].to_numpy()[ids];periods=meta['period_start'].to_numpy()[ids]
        global_cells=[]
        for cell in cells:
            use=(fields==cell[0])&(periods==cell[1])
            if int(use.sum())!=100:raise ValueError('Global queries are not balanced as declared')
            for pi,pair in enumerate(PAIRS):
                for ki,k in enumerate((10,25,50)):
                    global_cells.append({'field_id':cell[0],'period_start':cell[1],
                        'model_a':pair[0],'model_b':pair[1],'k':k,'queries':100,
                        'mean_overlap':float(counts[use,pi,ki].mean()/k)})
        table(out,'neighbors_global_by_cell',global_cells)
        facts['global_neighbors']={str(k):summary([r['mean_overlap'] for r in x['scores'] if r['k']==k]) for k in (10,25,50)}
        facts['global_neighbors']['query_interpretation']='100 queries per cell; balanced design, not population weighted'
    elif complete:raise ValueError('Missing global neighbor control')
    return pair_rows,cell_rows


def field_summary(meta,cells,stages,out):
    def read(name):
        path=out/'tables'/f'{name}.csv'
        return list(csv.DictReader(path.open())) if path.exists() else []
    neighbor=read('neighbors_by_cell');stability=read('shape_sample_stability');equal=read('neighbors_equal2048')
    global_cells=read('neighbors_global_by_cell');rows=[]
    for f in range(11,37):
        ids=np.flatnonzero(meta['field_id'].to_numpy()==f)
        vals=[r['cka_debiased'] for cell,x in stages['primary'].items() if cell[0]==f for r in x['scores']]
        row={'field_id':f,'field':FIELDS_ES[f],'rows':len(ids),
             'min_cell_rows':min(len(v) for cell,v in cells.items() if cell[0]==f),
             'cka_median_all_pairs_periods':float(np.median(vals))}
        n=[float(r['mean_overlap']) for r in neighbor if int(r['field_id'])==f]
        if n:row['neighbor_mean_k25_equal_periods']=float(np.mean(n))
        selected=[r for r in stability if int(r['field_id'])==f]
        row['stability_comparisons_present']=len(selected)
        row['stability_screen_failures']=sum(r['passes_operational_screen']=='False' for r in selected)
        if selected:
            full={(cell[1],key(r)):r['cka_debiased'] for cell,x in stages['primary'].items() if cell[0]==f for r in x['scores']}
            row['cka_median_equal2048']=float(np.median([full[int(r['period_start']),(r['model_a'],r['model_b'])]+float(r['median2048_minus_full']) for r in selected]))
        e=[float(r['mean_overlap']) for r in equal if int(r['field_id'])==f and r['recipe']=='mean' and int(r['k'])==25]
        if e:row['equal2048_neighbor_mean_k25']=float(np.mean(e))
        g=[float(r['mean_overlap']) for r in global_cells if int(r['field_id'])==f and int(r['k'])==25]
        if g:row['global_anchors_neighbor_mean_k25']=float(np.mean(g))
        rows.append(row)
    table(out,'field_summary',rows)
    return rows


def controls_report(cells,out,facts,audit,stages,complete):
    folder=BASE/'robustness_controls'
    if not (folder/'manifest.json').exists():
        if complete:raise ValueError('Robustness controls have not started')
        return
    manifest=verify_manifest(folder);pooling=[];mini=[];mini_neighbors=[];preservation=[]
    common=[];common_own=[];common_stability=[];common_neighbors=[];equal=[]
    def read(path):
        if not path.exists():
            if complete:raise ValueError(f'Missing {path}')
            return None
        return checked(path,manifest)
    for model in ('scibert','bert','pubmedbert','biobert'):
        for field,period in cells:
            x=read(folder/'pooling'/model/f'{field}_{period}.json')
            if x:pooling.extend({'model':model,'field_id':field,'period_start':period,**r} for r in x['scores'])
    for cell,ids in cells.items():
        x=read(folder/'minilm512'/f'{cell[0]}_{cell[1]}.json')
        if x:
            full={key(r):r for r in stages['primary'][cell]['scores']}
            for r in x['scores']:
                other=r['model_a'].split('/')[0]
                if other=='minilm':
                    preservation.append({'field_id':cell[0],'period_start':cell[1],'n':len(ids),
                        'cka_native_extended':r['cka_debiased'],
                        **{f'overlap_k{k}':v for k,v in x['minilm_neighbor_preservation'].items()}})
                else:
                    pair=(other,'minilm') if MODELS.index(other)<MODELS.index('minilm') else ('minilm',other)
                    before=full[pair]['cka_debiased']
                    mini.append({'field_id':cell[0],'period_start':cell[1],'other_model':other,
                        'native_cka':before,'extended_cka':r['cka_debiased'],'delta_cka':r['cka_debiased']-before})
            mini_neighbors.extend({'field_id':cell[0],'period_start':cell[1],**r} for r in x['comparison_with_others'])
        x=read(folder/'common_neighbors'/f'{cell[0]}_{cell[1]}.json')
        if x:
            if x['n']!=400 or len(x['scores'])!=135:raise ValueError('Common neighbor coverage')
            common_neighbors.extend({'field_id':cell[0],'period_start':cell[1],**r} for r in x['scores'])
        x=read(folder/'equal2048_neighbors/summary'/f'{cell[0]}_{cell[1]}.json')
        if x:
            if x['n']!=2048 or len(x['scores'])!=405:raise ValueError('Equal neighbor coverage')
            equal.extend({'field_id':cell[0],'period_start':cell[1],**r} for r in x['scores'])
    for field in range(11,37):
        x=read(folder/'common_fields'/f'{field}.json')
        if not x:continue
        if x['n']!=2000 or len(x['native_scores'])!=45 or len(x['common_scores'])!=45:
            raise ValueError('Common shape coverage')
        before={key(r):r for r in x['native_scores']};after={key(r):r for r in x['common_scores']}
        for pair in PAIRS:
            row={'field_id':field,'model_a':pair[0],'model_b':pair[1]}
            for metric in ('cka_debiased','procrustes_similarity','rsa_spearman'):
                row.update({f'native_{metric}':before[pair][metric],f'common_{metric}':after[pair][metric],
                            f'delta_{metric}':after[pair][metric]-before[pair][metric]})
            common.append(row)
            sample={}
            for r in x['subsamples_n1000']:
                if key(r)==pair:sample[r['text'],r['repeat']]=r['cka_debiased']
            deltas=[sample['common',rep]-sample['native',rep] for rep in range(20)]
            full_delta=after[pair]['cka_debiased']-before[pair]['cka_debiased']
            common_stability.append({'field_id':field,'model_a':pair[0],'model_b':pair[1],
                'delta_common_native_n2000':full_delta,'median_delta_n1000':float(np.median(deltas)),
                'absolute_median_error':abs(float(np.median(deltas))-full_delta),
                'central95_width_delta_n1000':float(np.quantile(deltas,.975)-np.quantile(deltas,.025)),
                'min_delta_n1000':min(deltas),'max_delta_n1000':max(deltas)})
        common_own.extend({'field_id':field,**r} for r in x['same_model_native_common'])
    for name,rows in [('pooling_same_model',pooling),('minilm_shape_change',mini),('minilm_neighbor_change',mini_neighbors),
        ('minilm_native_extended_preservation',preservation),('common_text_shape_change',common),
        ('common_text_same_model',common_own),('common_text_sample_stability',common_stability),
        ('common_text_neighbor_change',common_neighbors),('neighbors_equal2048',equal)]:table(out,name,rows)
    audit['control_rows']={name:len(rows) for name,rows in [('pooling',pooling),('minilm_shape',mini),
        ('common_shape',common),('common_neighbors',common_neighbors),('equal_neighbors',equal)]}
    if complete and audit['control_rows']!={'pooling':1560,'minilm_shape':1170,'common_shape':1170,
                                           'common_neighbors':17550,'equal_neighbors':52650}:
        raise ValueError('Incomplete control coverage')
    facts['pooling_same_model']={model:{p:summary([r['cka_debiased'] for r in pooling if r['model']==model and
        (r['model_a'].split('/')[1],r['model_b'].split('/')[1])==tuple(p.split('-'))])
        for p in ('mean-cls','mean-sep','cls-sep')} for model in ('scibert','bert','pubmedbert','biobert')}
    if preservation:
        facts['minilm']={'own_cka':summary([r['cka_native_extended'] for r in preservation]),
            'own_neighbors25':summary([r['overlap_k25'] for r in preservation]),
            'own_neighbors25_article_weighted':float(np.average([r['overlap_k25'] for r in preservation],weights=[r['n'] for r in preservation])),
            'between_model_delta_cka':summary([r['delta_cka'] for r in mini]),
            'between_model_absolute_delta_cka':summary([abs(r['delta_cka']) for r in mini]),
            'between_model_delta_neighbors25':summary([r['delta_overlap'] for r in mini_neighbors if r['k']==25 and r['other_model']!='minilm'])}
    if common:
        facts['common_text']={c:{'native':summary([r['native_'+c] for r in common]),
            'common':summary([r['common_'+c] for r in common]),'delta':summary([r['delta_'+c] for r in common]),
            'absolute_delta':summary([abs(r['delta_'+c]) for r in common])}
            for c in ('cka_debiased','procrustes_similarity','rsa_spearman')}
        facts['common_text']['paired_subsample_stability']={c:summary([r[c] for r in common_stability])
                         for c in ('absolute_median_error','central95_width_delta_n1000')}
    if common_neighbors:
        facts['common_neighbors']={c:summary([r[c] for r in common_neighbors if r['k']==25])
                                  for c in ('native_overlap','common_overlap','delta_overlap','native_adjusted','common_adjusted')}
    if equal:
        facts['equal_neighbors']={recipe:{str(k):summary([r['mean_overlap'] for r in equal if r['recipe']==recipe and r['k']==k])
            for k in (10,25,50)} for recipe in ('mean','cls','sep')}
        if complete:
            arrays=list((folder/'equal2048_neighbors/arrays').glob('*/*/validation.json'))
            if len(arrays)!=18:raise ValueError('Missing equal-size neighbor variants')
            for path in arrays:
                record=checked(path,manifest)
                if record['rows']!=266240 or record['neighbors_sha256']!=file_sha(path.parent/'neighbors.npy'):
                    raise ValueError('Changed equal-size control array')
            audit['equal_neighbor_variants']=18


def macro_report(out,facts,audit,complete):
    folder=BASE/'macro_controls';path=folder/'relations.json'
    if not path.exists():
        if complete:raise ValueError('Centroid follow-up is incomplete')
        return
    manifest=verify_manifest(folder);x=checked(path,manifest)
    if not x['native_reconstruction_matches'] or len(x['scores'])!=1215 or len(x['edges'])!=87750:
        raise ValueError('Wrong centroid control coverage')
    for model,digest in manifest['common_manifests_sha256'].items():
        if file_sha(BASE/'controls/common_text_52k'/model/'manifest.json')!=digest:raise ValueError('Common parent changed')
    table(out,'centroid_control_agreement',x['scores']);table(out,'centroid_control_distances',x['edges'])
    facts['centroid_controls']={stage:summary([r['centroid_edge_spearman'] for r in x['scores'] if r['stage']==stage])
        for stage in ('mean','cls','sep','quality','raw','native_paired','common_paired')}
    before={key(r):r['centroid_edge_spearman'] for r in x['scores'] if r['stage']=='native_paired'}
    facts['centroid_controls']['paired_common_delta']=summary([r['centroid_edge_spearman']-before[key(r)] for r in x['scores'] if r['stage']=='common_paired'])
    audit['centroid_followup_native_reconstruction_matches']=True
    audit['centroid_followup_manifest_sha256']=file_sha(folder/'manifest.json')
    reference_folder=BASE/'centroid_random_groups';reference_path=reference_folder/'results.json'
    if not reference_path.exists():
        if complete:raise ValueError('Random-group centroid reference is incomplete')
        return
    reference_manifest=verify_manifest(reference_folder)
    reference=checked(reference_path,reference_manifest)
    if len(reference['scores'])!=1890:raise ValueError('Wrong random group reference coverage')
    table(out,'centroid_random_group_reference',reference['scores'])
    for condition in ('native_paired','common_paired'):
        actual={key(r):r['centroid_edge_spearman'] for r in x['scores'] if r['stage']==condition}
        copied={key(r):r['centroid_edge_spearman'] for r in reference['scores'] if r['condition']==condition and r['groups']=='real'}
        for pair in PAIRS:
            if not np.isclose(actual[pair],copied[pair],atol=1e-12,rtol=0):raise ValueError('Independent common centroid reconstruction differs')
        null={pair:[r['centroid_edge_spearman'] for r in reference['scores'] if r['condition']==condition and r['groups']=='random' and key(r)==pair] for pair in PAIRS}
        facts['centroid_controls'][condition+'_random_reference']={
            'real_across45':summary(list(actual.values())),
            'random_across45x20':summary([v for values in null.values() for v in values]),
            'real_minus_own_random_median':summary([actual[pair]-np.median(null[pair]) for pair in PAIRS]),
            'pairs_with_real_above_own_random_median':int(sum(actual[pair]>np.median(null[pair]) for pair in PAIRS)),
            'interpretation':'Diagnostic matched random partitions, not p-values or independent model samples'}
    audit['random_group_reference_manifest_sha256']=file_sha(reference_folder/'manifest.json')


def figures(out,meta,shape_pairs,shape_cells,neighbor_pairs,neighbor_cells,facts):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,
                         'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
    folder=out/'figures';folder.mkdir(parents=True,exist_ok=True)
    def save(fig,name):
        for ext in ('pdf','svg','png'):fig.savefig(folder/f'{name}.{ext}',dpi=200,bbox_inches='tight',facecolor='white')
        plt.close(fig)
    labels=[LABELS[m] for m in MODELS]
    def matrix(rows,value):
        a=np.eye(10)
        for row in rows:
            i,j=MODELS.index(row['model_a']),MODELS.index(row['model_b']);a[i,j]=a[j,i]=row[value]
        np.fill_diagonal(a,np.nan)
        return a
    fig,axes=plt.subplots(1,2,figsize=(12,5.4),layout='constrained')
    values=[(matrix(shape_pairs,'cka_debiased_median'),'A  Shape agreement','Debiased linear CKA'),
            (matrix(neighbor_pairs,'cell_mean_overlap') if neighbor_pairs else np.full((10,10),np.nan),
             'B  Shared nearest neighbours','Fraction shared among 25 neighbours')]
    for ax,(a,title,label) in zip(axes,values):
        im=ax.imshow(a,cmap='viridis',vmin=0,vmax=1)
        ax.set(xticks=range(10),xticklabels=labels,yticks=range(10),yticklabels=labels,title=title)
        plt.setp(ax.get_xticklabels(),rotation=60,ha='right',rotation_mode='anchor')
        for i in range(10):
            for j in range(10):
                if np.isfinite(a[i,j]):ax.text(j,i,f'{a[i,j]:.2f}',ha='center',va='center',fontsize=7,color='white' if a[i,j]<.53 else '#172126')
        fig.colorbar(im,ax=ax,shrink=.72,label=label)
    fig.suptitle('Same papers, ten representations\nShape: median across 130 cells; neighbours: equal-cell mean. Different measures.',fontsize=12)
    save(fig,'01_model_comparison')
    fields=sorted(set(meta['field_id'].to_pylist()));periods=[2000,2005,2010,2015,2020]
    field_names={r['field_id']:r['field_display_name'] for r in meta.select(['field_id','field_display_name']).to_pylist()}
    field_names[13]='Biochemistry, Genetics & Molecular Biology';field_names[30]='Pharmacology, Toxicology & Pharmaceutics'
    fig,axes=plt.subplots(1,2,figsize=(12,9),layout='constrained',sharey=True)
    for ax,rows,value,title in [(axes[0],shape_cells,'cka_debiased_median','A  Shape: median CKA across 45 pairs'),
                               (axes[1],neighbor_cells,'mean_adjusted','B  Neighbours: mean overlap, chance adjusted')]:
        values={(r['field_id'],r['period_start']):r[value] for r in rows}
        a=np.array([[values.get((f,p),np.nan) for p in periods] for f in fields])
        im=ax.imshow(a,aspect='auto',cmap='viridis',vmin=0,vmax=1)
        ax.set(xticks=range(5),xticklabels=[f'{p}–{p+4}' for p in periods],yticks=range(26),
               yticklabels=[field_names[f] for f in fields],title=title)
        plt.setp(ax.get_xticklabels(),rotation=45,ha='right')
        fig.colorbar(im,ax=ax,shrink=.7)
    fig.suptitle('Model dependence by field and publication period\nAll papers in each cell; unequal candidate-set sizes require the fixed-size control.',fontsize=12)
    save(fig,'02_fields_and_periods')
    if neighbor_pairs:
        neighbors={(r['model_a'],r['model_b']):r for r in neighbor_pairs}
        x=np.array([r['cka_debiased_median'] for r in shape_pairs]);y=np.array([neighbors[key(r)]['cell_mean_overlap'] for r in shape_pairs])
        fig,ax=plt.subplots(figsize=(7.4,5.4),layout='constrained')
        family={m:f for f,ms in DESIGN['family_sensitivity'].items() for m in ms}
        colors={'citation_document':'#277da1','word_BERT':'#9d4edd','general_sentence':'#e76f51','between':'#8b949e'}
        groups=[family[r['model_a']] if family[r['model_a']]==family[r['model_b']] else 'between' for r in shape_pairs]
        for label,color in colors.items():
            mask=np.array([g==label for g in groups]);ax.scatter(x[mask],y[mask],s=42,color=color,label=label.replace('_',' '),alpha=.9)
        for index in sorted(set([int(np.argmin(y)),int(np.argmax(y)),int(np.argmax(x))])):
            offset=(0,-20) if index==int(np.argmin(y)) else (5,6)
            r=shape_pairs[index];ax.annotate(LABELS[r['model_a']]+' / '+LABELS[r['model_b']],(x[index],y[index]),xytext=offset,textcoords='offset points',fontsize=8,
                 ha='center' if index==int(np.argmin(y)) else 'left')
        ax.set(xlim=(0,1.04),ylim=(0,1),xlabel='Shape agreement: median debiased CKA',ylabel='Shared fraction among 25 neighbours',
               title='A similar overall map need not preserve local neighbourhoods')
        ax.legend(frameon=False,loc='upper left',fontsize=8)
        ax.text(.98,.02,'45 model pairs; descriptive points, not independent replicates',ha='right',transform=ax.transAxes,fontsize=8)
        save(fig,'03_shape_and_neighbors')
        facts['shape_neighbor_pair_spearman']=float(spearmanr(x,y).statistic)
    centroid=checked(BASE/'shape/centroids/relations.json')
    centroids={pair:float(np.median([r['centroid_edge_spearman'] for r in centroid['scores'] if key(r)==pair])) for pair in PAIRS}
    fig,ax=plt.subplots(figsize=(6.5,5.4),layout='constrained')
    ax.scatter([centroids[key(r)] for r in shape_pairs],[r['rsa_spearman_median'] for r in shape_pairs],s=35,c='#277da1',alpha=.75)
    ax.plot([0,1],[0,1],color='#b1b1b1',linestyle='--',linewidth=1)
    ax.set(xlim=(0,1),ylim=(0,1),xlabel='Between-field relations: median rank correlation',
        ylabel='Within-field paper distances: median rank correlation',title='Coarse structure and internal structure are different views')
    ax.text(.02,.03,'Five periods for centres; 130 cells for internal distances.\nSame correlation measure, different objects.',transform=ax.transAxes,fontsize=8)
    save(fig,'04_between_and_within_fields')
    stability_path=out/'tables/shape_sample_stability.csv'
    if stability_path.exists():
        rows=list(csv.DictReader(stability_path.open()))
        fig,axes=plt.subplots(1,2,figsize=(10,3.8),layout='constrained')
        for ax,column,threshold,title in [(axes[0],'median_change_1024_to_2048',.02,'Change from 1,024 to 2,048 papers'),
                 (axes[1],'central95_width_at2048',.04,'Central range across 20 selections at 2,048')]:
            ax.hist([float(r[column]) for r in rows],bins=40,color='#277da1',alpha=.85)
            ax.axvline(threshold,color='#d1495b',linestyle='--');ax.set(title=title,xlabel='CKA scale',ylabel='Cell × model-pair comparisons')
        fig.suptitle('Sensitivity to selection inside the fixed corpus — not population confidence intervals')
        save(fig,'05_selection_stability')
    common=out/'tables/common_text_shape_change.csv';mini=out/'tables/minilm_shape_change.csv'
    if common.exists() and mini.exists():
        c=list(csv.DictReader(common.open()));m=list(csv.DictReader(mini.open()))
        fig,axes=plt.subplots(1,2,figsize=(10,4.4),layout='constrained')
        for ax,rows,before,after,title in [(axes[0],c,'native_cka_debiased','common_cka_debiased','A  Identical text content; matched 2,000 papers/field'),
                     (axes[1],m,'native_cka','extended_cka','B  MiniLM: 256 versus 512 tokens; same cells')]:
            ax.scatter([float(r[before]) for r in rows],[float(r[after]) for r in rows],s=9,alpha=.25,c='#277da1',rasterized=True)
            ax.plot([0,1],[0,1],color='#999999',linestyle='--');ax.set(xlim=(0,1),ylim=(0,1),xlabel='Native CKA',ylabel='Control CKA',title=title)
        fig.suptitle('Length controls preserve paper identity; changes cannot be attributed to paper selection')
        save(fig,'06_text_controls')
    pooling=out/'tables/pooling_same_model.csv'
    if pooling.exists():
        rows=list(csv.DictReader(pooling.open()));models=['scibert','bert','pubmedbert','biobert']
        combinations=[('mean','cls'),('mean','sep'),('cls','sep')]
        a=np.array([[np.median([float(r['cka_debiased']) for r in rows if r['model']==model and
           (r['model_a'].split('/')[1],r['model_b'].split('/')[1])==pair]) for pair in combinations] for model in models])
        fig,ax=plt.subplots(figsize=(7,4),layout='constrained');im=ax.imshow(a,vmin=0,vmax=1,cmap='viridis',aspect='auto')
        for i in range(4):
            for j in range(3):ax.text(j,i,f'{a[i,j]:.3f}',ha='center',va='center',color='white' if a[i,j]<.53 else '#172126')
        ax.set(xticks=range(3),xticklabels=['Mean / CLS','Mean / SEP','CLS / SEP'],yticks=range(4),
               yticklabels=[LABELS[m] for m in models],title='Same model and papers, different pooling recipes\nMedian debiased CKA across 130 cells')
        fig.colorbar(im,ax=ax,label='Shape agreement');save(fig,'07_pooling_same_model')
    macro=out/'tables/centroid_control_agreement.csv';random=out/'tables/centroid_random_group_reference.csv'
    if macro.exists() and random.exists():
        rows=list(csv.DictReader(macro.open()));null=list(csv.DictReader(random.open()))
        fig,axes=plt.subplots(1,2,figsize=(11,4.4),layout='constrained')
        stage_labels=[('mean','Main'),('cls','CLS'),('sep','SEP'),('quality','Strict quality'),('raw','Raw vectors')]
        series=[[float(r['centroid_edge_spearman']) for r in rows if r['stage']==stage] for stage,label in stage_labels]
        box=axes[0].boxplot(series,tick_labels=[label for stage,label in stage_labels],showfliers=False,whis=(5,95),patch_artist=True)
        for patch in box['boxes']:patch.set(facecolor='#90c7db')
        axes[0].set(title='A  Field relations under alternative recipes',ylabel='Rank agreement across 325 relations',ylim=(0,1))
        series=[[float(r['centroid_edge_spearman']) for r in rows if r['stage']==stage] for stage in ('native_paired','common_paired')]
        series.append([float(r['centroid_edge_spearman']) for r in null if r['condition']=='common_paired' and r['groups']=='random'])
        box=axes[1].boxplot(series,tick_labels=['Native text','Common text','Random groups'],showfliers=False,whis=(5,95),patch_artist=True)
        for patch in box['boxes']:patch.set(facecolor='#90c7db')
        box['boxes'][-1].set(facecolor='#d3d8dd')
        axes[1].set(title='B  Matched 52,000 papers; equal group sizes',ylim=(0,1))
        fig.suptitle('Field-centroid controls\nBoxes show variation across dependent comparisons; whiskers are 5th–95th percentiles, not confidence intervals.',fontsize=11)
        save(fig,'08_centroid_controls')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--require-complete',action='store_true');args=parser.parse_args()
    out=ROOT/'reports/analysis_v1'/('final' if args.require_complete else 'preview')
    out.mkdir(parents=True,exist_ok=True)
    catalog=json.loads((ROOT/DESIGN['catalog']).read_text())
    if file_sha(ROOT/DESIGN['catalog'])!=DESIGN['catalog_sha256']:raise ValueError('Original catalog changed')
    if file_sha(ROOT/catalog['metadata_path'])!=catalog['metadata_sha256']:raise ValueError('Metadata changed')
    meta=pq.read_table(ROOT/catalog['metadata_path'])
    np.testing.assert_array_equal(meta['row_index'].to_numpy(),np.arange(500000))
    field=meta['field_id'].to_numpy();period=meta['period_start'].to_numpy()
    cells={(int(f),int(p)):np.flatnonzero((field==f)&(period==p)) for f in np.unique(field) for p in np.unique(period)}
    if len(cells)!=130 or min(map(len,cells.values()))!=2165:raise ValueError('Unexpected corpus coverage')
    facts={'created_at':utcnow(),'final':args.require_complete,'rows':500000,'base_rows':400000,'cells':130,
           'model_count':10,'interpretation':'All intervals and counts are descriptive; model pairs are dependent.'}
    audit={'metadata_sha256':catalog['metadata_sha256'],'protocol_sha256':file_sha(ROOT/'config/analysis_v1.json')}
    if args.require_complete:
        for directory in ('shape','neighbors','robustness_controls'):
            progress=json.loads((BASE/directory/'progress.json').read_text())
            if progress['state']!='requested_stages_complete':raise ValueError(f'{directory} is still running')
    stages,sp,sc=shape_report(meta,cells,out,facts,audit,args.require_complete)
    centroid_report(out,facts)
    npairs,ncells=neighbors_report(meta,cells,out,facts,audit,stages,args.require_complete)
    controls_report(cells,out,facts,audit,stages,args.require_complete)
    macro_report(out,facts,audit,args.require_complete)
    facts['fields']=field_summary(meta,cells,stages,out)
    figures(out,meta,sp,sc,npairs,ncells,facts)
    audit['source_manifests']={name:file_sha(BASE/name/'manifest.json') for name in ('shape','neighbors','robustness_controls') if (BASE/name/'manifest.json').exists()}
    audit['report_source_sha256']=file_sha(Path(__file__))
    audit['completed_at']=utcnow();audit['all_required_outputs_present']=args.require_complete
    write_json(out/'summary.json',facts);write_json(out/'audit.json',audit)
    write_json(out/'catalog.json',{'created_at':utcnow(),'files':{str(p.relative_to(out)):file_sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='catalog.json'}})
    print(json.dumps({'output':str(out),'audit':audit,'headline':{k:facts[k] for k in ('shape','neighbors','common_text','minilm','sample_stability') if k in facts}},indent=2))


if __name__=='__main__':main()
