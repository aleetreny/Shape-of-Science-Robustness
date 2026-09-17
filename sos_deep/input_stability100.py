"""Nested 26k/52k finite-corpus stability with 100 repetitions and explicit alert tracking."""
import json
import numpy as np
import pyarrow.parquet as pq
from sos_deep.input_analysis52 import verified_inputs,NAMES,MODELS
from sos_followup.pilot_statistics import cosine_grams,cka_matrix,effect_rows
from sos_deep.artifacts import ROOT,read_csv,save_csv,verify_audit,freeze,finish
from sos_embed.storage import file_sha,write_json,utcnow,run_lock

CONFIG=ROOT/'config/input_stability100_v1.json';D=json.loads(CONFIG.read_text());OUT=ROOT/D['output']


def summarize(vals,full):
    vals=np.asarray(vals,float)
    median=float(np.median(vals));shift=abs(median-full)
    lo,hi=map(float,np.quantile(vals,[.025,.975]));width=hi-lo
    return {'full_effect':float(full),'median_effect':median,'absolute_median_change':shift,
            'p025':lo,'p975':hi,'central95_width':width,
            'fraction_positive':float((vals>0).mean()),'fraction_negative':float((vals<0).mean()),
            'crosses_zero':lo<=0<=hi,
            'passes_operational_screen':shift<=D['max_median_effect_change'] and width<=D['max_central95_width']}


def main():
    with run_lock(OUT):
        old=ROOT/'data/checklist_v1/input_comparisons';new=ROOT/'data/robustness_v2/input_comparisons'
        verify_audit(old);verify_audit(new)
        freeze(OUT,['sos_deep/input_stability100.py','sos_deep/input_analysis52.py','sos_deep/artifacts.py',
                    'sos_followup/pilot_statistics.py','config/input_stability100_v1.json'],
               ['data/checklist_v1/input_comparisons/audit.json','data/robustness_v2/input_comparisons/audit.json',
                'data/robustness_v2/inputs/input_manifest.json'],D)
        meta,arrays,_=verified_inputs()
        oldmeta=pq.read_table(ROOT/'data/checklist_v1/inputs/native_input.parquet')
        prior=set(oldmeta['row_index'].to_pylist());global_ids=meta['row_index'].to_numpy()
        field_ids=meta['field_id'].to_numpy();all_periods=meta['period_start'].to_numpy()
        all_summaries=[];all_replicates=[]
        for total,source in [(26000,old),(52000,new)]:
            original={(int(r['field_id']),int(r['repeat']),r['model'],r['input_condition']):float(r['model_minus_input'])
                      for r in read_csv(source/'stability_replicates.csv')}
            fullref={(int(r['field_id']),r['model'],r['input_condition']):float(r['model_minus_input'])
                     for r in read_csv(source/'effects.csv') if r['metric']=='cka'}
            for field in range(11,37):
                folder=OUT/str(total)/str(field);folder.mkdir(parents=True,exist_ok=True)
                if (folder/'commit.json').exists():
                    c=json.loads((folder/'commit.json').read_text())
                    for n,h in c['files'].items():assert file_sha(folder/n)==h
                else:
                    pos=np.flatnonzero(field_ids==field)
                    if total==26000:pos=np.array([p for p in pos if int(global_ids[p]) in prior])
                    assert len(pos)==total//26
                    periods=all_periods[pos];nper=total//130
                    grams=cosine_grams([arrays[n][pos] for n in NAMES]);samples=[];choices=[]
                    for rep in range(D['repeats']):
                        rng=np.random.default_rng(20260917000+100*field+rep)
                        chosen=np.sort(np.concatenate([rng.choice(np.flatnonzero(periods==p),nper//2,replace=False)
                                                      for p in [2000,2005,2010,2015,2020]]))
                        choices.append(global_ids[pos[chosen]])
                        ck=cka_matrix(grams[:,chosen][:,:,chosen]);rows,_=effect_rows(ck,NAMES,MODELS)
                        for r in rows:
                            if rep<20:assert abs(r['model_minus_input']-original[field,rep,r['model'],r['input_condition']])<2e-10
                            samples.append({'corpus_rows':total,'field_id':field,'repeat':rep,**r})
                    np.save(folder/'selected_ids.npy',np.stack(choices),allow_pickle=False)
                    save_csv(folder/'replicates.csv',samples);summaries=[]
                    for model in MODELS+['mean_of_ten_fixed_models']:
                        for cond in ['title','abstract']:
                            full=(np.mean([fullref[field,m,cond] for m in MODELS]) if model=='mean_of_ten_fixed_models'
                                  else fullref[field,model,cond])
                            vals=np.array([np.mean([r['model_minus_input'] for r in samples
                                if r['repeat']==rep and r['input_condition']==cond
                                and (model=='mean_of_ten_fixed_models' or r['model']==model)]) for rep in range(D['repeats'])])
                            for repeats in [20,100]:
                                summaries.append({'corpus_rows':total,'field_id':field,'model':model,'input_condition':cond,
                                                  'repeats':repeats,**summarize(vals[:repeats],full)})
                    save_csv(folder/'summary.csv',summaries)
                    write_json(folder/'commit.json',{'first20_match_frozen_parent':True,'completed_at':utcnow(),
                        'files':{p.name:file_sha(p) for p in folder.iterdir() if p.is_file()}})
                    print('100-REPEAT INPUT STABILITY',total,field,flush=True)
                all_summaries.extend(read_csv(folder/'summary.csv'));all_replicates.extend(read_csv(folder/'replicates.csv'))
        save_csv(OUT/'summary.csv',all_summaries);save_csv(OUT/'replicates.csv',all_replicates)
        keyed={(int(r['corpus_rows']),int(r['repeats']),int(r['field_id']),r['model'],r['input_condition']):r for r in all_summaries}
        transitions=[]
        for repeats in [20,100]:
            for f in range(11,37):
                for m in MODELS+['mean_of_ten_fixed_models']:
                    for cond in ['title','abstract']:
                        a=keyed[26000,repeats,f,m,cond];b=keyed[52000,repeats,f,m,cond]
                        pa=a['passes_operational_screen']=='True';pb=b['passes_operational_screen']=='True'
                        original=keyed[26000,20,f,m,cond]['passes_operational_screen']=='False'
                        transitions.append({'repeats':repeats,'field_id':f,'model':m,'input_condition':cond,
                            'original_31_alert':original,'alert26k':not pa,'alert52k':not pb,
                            'transition':('no_alert' if pa else 'resolved') if pb else ('new' if pa else 'persists'),
                            'width26k':a['central95_width'],'width52k':b['central95_width'],
                            'full_effect26k':a['full_effect'],'full_effect52k':b['full_effect'],
                            'crosses_zero26k':a['crosses_zero'],'crosses_zero52k':b['crosses_zero']})
        assert sum(r['original_31_alert'] and r['repeats']==20 for r in transitions)==31
        save_csv(OUT/'alert_transitions.csv',transitions)
        finish(OUT,summary_rows=len(all_summaries),replicate_rows=len(all_replicates),
               first20_reproduced_both_sizes=True,original_31_retained=True,repeats=100)
        print('INPUT STABILITY 100 COMPLETE',flush=True)


if __name__=='__main__':main()
