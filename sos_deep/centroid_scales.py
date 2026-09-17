"""Field/Subfield centroid agreement with equal sizes and period-preserving random groups."""
import json
import numpy as np
from sos_analysis.native_data import NativeData
from sos_analysis.geometry import normalize_rows
from sos_followup.pilot_statistics import cosine_grams,cka_matrix,rsa_matrix
from sos_deep.subfield_controls import prepared_groups
from sos_deep.artifacts import ROOT,save_csv,freeze,finish
from sos_embed.storage import file_sha,write_json,run_lock

CONFIG=ROOT/'config/scale_checks_v1.json';D=json.loads(CONFIG.read_text());OUT=ROOT/'data/robustness_v2/centroid_scales'
BASE=json.loads((ROOT/'config/analysis_v1.json').read_text());MODELS=list(BASE['poolings'])


def shuffled_assignments(ids,periods,repeats,seed):
    result=[]
    for rep in range(repeats):
        rng=np.random.default_rng(seed+rep);order=np.arange(len(ids))
        for p in np.unique(periods):
            positions=np.flatnonzero(periods==p);order[positions]=rng.permutation(positions)
        assert np.array_equal(np.sort(order),np.arange(len(ids)))
        assert np.array_equal(periods[order],periods)
        result.append(order)
    return np.stack(result)


def scores(arrays,seed):
    grams=cosine_grams(arrays);ck=cka_matrix(grams);rs=rsa_matrix(grams,seed)
    return [{'model_a':MODELS[i],'model_b':MODELS[j],'cka_debiased':float(ck[i,j]),
             'rsa_spearman':float(rs[i,j])} for i in range(10) for j in range(i+1,10)]


def main():
    with run_lock(OUT):
        freeze(OUT,['sos_deep/centroid_scales.py','sos_deep/artifacts.py','sos_deep/subfield_controls.py',
                    'config/scale_checks_v1.json','config/subfield_controls_v1.json',
                    'sos_analysis/native_data.py','sos_analysis/reader.py','sos_analysis/geometry.py',
                    'sos_followup/pilot_statistics.py'],['data/analysis_ready_v1/metadata.parquet',BASE['catalog']],D)
        data=NativeData(ROOT,max_bytes=2*1024**3);meta=data.metadata;groups,_=prepared_groups(meta)
        field=meta['field_id'].to_numpy();period=meta['period_start'].to_numpy()
        fields=sorted([key for key in groups if key[0]=='field'],key=lambda k:int(k[1]))
        subfields=sorted([key for key in groups if key[0]=='subfield'])
        eligible=[key for key in subfields if len(groups[key])>=D['candidate_count']]
        chosen={'field':fields,'subfield':eligible};orders={};selected={};parents=[]
        for level,keys in chosen.items():
            ids=np.concatenate([np.sort(groups[key][:D['candidate_count']]) for key in keys]);selected[level]=ids
            np.save(OUT/(level+'_selected_ids.npy'),ids,allow_pickle=False)
            orders[level]=shuffled_assignments(ids,period[ids],D['random_group_repeats'],D['seed']+(level=='field')*100)
            np.save(OUT/(level+'_null_assignments.npy'),ids[orders[level]],allow_pickle=False)
        subparents=np.array([field[groups[key][0]] for key in eligible])
        selections=[]
        for rep in range(D['random_group_repeats']):
            rng=np.random.default_rng(D['seed']+200+rep)
            selections.append([rng.choice(np.flatnonzero(subparents==f)) for f in range(11,37)])
        selections=np.array(selections);np.save(OUT/'one_subfield_per_field.npy',selections,allow_pickle=False)
        centers={};randoms={}
        for m,pool in BASE['poolings'].items():
            path=OUT/(m+'_centroids.npz')
            if path.exists() and path.with_suffix('.commit.json').exists():
                c=json.loads(path.with_suffix('.commit.json').read_text());assert file_sha(path)==c['sha256']
                loaded=np.load(path);centers[m]={k:loaded[k] for k in ['native_field','native_subfield','matched_field','matched_subfield']}
                randoms[m]={k:loaded['random_'+k] for k in ['field','subfield']};continue
            raw=data.get(m+'/'+pool,slice(None));native_sf=[];counts=[];native_parent=[]
            for key in subfields:
                ids=groups[key];native_sf.append(normalize_rows(raw[ids]).mean(0));counts.append(len(ids));native_parent.append(field[ids[0]])
            native_sf=np.stack(native_sf);counts=np.array(counts);native_parent=np.array(native_parent)
            native_f=np.stack([np.average(native_sf[native_parent==f],axis=0,weights=counts[native_parent==f]) for f in range(11,37)])
            # Independent direct check on one Field for each model.
            np.testing.assert_allclose(native_f[0],normalize_rows(raw[groups['field','11']]).mean(0),rtol=0,atol=2e-14)
            values={'native_field':native_f,'native_subfield':native_sf};rand={}
            for level,ids in selected.items():
                x=normalize_rows(raw[ids]);g=len(chosen[level]);values['matched_'+level]=x.reshape(g,D['candidate_count'],-1).mean(1)
                rand[level]=np.stack([x[order].reshape(g,D['candidate_count'],-1).mean(1) for order in orders[level]])
            np.savez(path,**values,**{'random_'+k:v for k,v in rand.items()})
            write_json(path.with_suffix('.commit.json'),{'sha256':file_sha(path),'direct_field_mean_check':True})
            centers[m]=values;randoms[m]=rand
            print('CENTROID SCALES',m,flush=True)
        rows=[]
        for condition in ['native_field','native_subfield','matched_field','matched_subfield']:
            arrays=[centers[m][condition] for m in MODELS]
            rows.extend({'condition':condition,'groups':'real','repeat':-1,'centroid_count':len(arrays[0]),**r} for r in scores(arrays,D['seed']))
        for rep in range(D['random_group_repeats']):
            for level in ['field','subfield']:
                arrays=[randoms[m][level][rep] for m in MODELS]
                rows.extend({'condition':'matched_'+level,'groups':'random_period_preserved','repeat':rep,
                             'centroid_count':len(arrays[0]),**r} for r in scores(arrays,D['seed']))
            for label,arrays in [
                ('real',[centers[m]['matched_subfield'][selections[rep]] for m in MODELS]),
                ('random_period_preserved',[randoms[m]['subfield'][rep,selections[rep]] for m in MODELS])]:
                rows.extend({'condition':'one_subfield_per_field','groups':label,'repeat':rep,
                             'centroid_count':26,**r} for r in scores(arrays,D['seed']))
        save_csv(OUT/'comparisons.csv',rows)
        write_json(OUT/'group_labels.json',{'native_subfields':[k[1] for k in subfields],
                   'matched_subfields':[k[1] for k in eligible],'matched_subfield_parents':subparents.tolist(),
                   'fields':list(range(11,37))})
        finish(OUT,field_centroids=26,native_subfield_centroids=len(subfields),matched_subfield_centroids=len(eligible),
               random_repeats=D['random_group_repeats'],same_source_papers_and_period_composition_in_null=True,
               direct_field_means_verified=True,comparison_rows=len(rows))
        print('CENTROID SCALE CONTROLS COMPLETE',flush=True)


if __name__=='__main__':main()
