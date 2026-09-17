"""Continuous per-paper agreement, model omissions and regional coverage, no population CIs."""
import itertools
import json
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.stats import rankdata,spearmanr
from sos_deep.artifacts import ROOT,save_csv,verify_audit,freeze,finish
from sos_embed.storage import file_sha,write_json,object_sha,run_lock

OUT=ROOT/'data/robustness_v2/regions_native'
D=json.loads((ROOT/'config/analysis_v1.json').read_text());MODELS=list(D['poolings'])
PAIRS=list(itertools.combinations(MODELS,2));KS=[10,25,50]
OMIT={**{m:{m} for m in MODELS},**{f'set_{key}':set(value) for key,value in D['family_sensitivity'].items()},
      'set_biomedical':{'biobert','pubmedbert'}}


def paper_scores(counts,k,candidates):
    counts=np.asarray(counts);assert counts.ndim==2 and counts.shape[1]==45
    assert (counts>=0).all() and (counts<=k).all() and candidates>k+1
    value=counts.astype(float)/k;raw=value.mean(1);chance=k/(candidates-1)
    omissions=np.stack([value[:,[not(set(pair)&removed) for pair in PAIRS]].mean(1) for removed in OMIT.values()],axis=1)
    return {'mean':raw,'adjusted':(raw-chance)/(1-chance),
            'leave_one_min':omissions[:,:10].min(1),'leave_one_max':omissions[:,:10].max(1),
            'leave_family_min':omissions[:,10:].min(1),'leave_family_max':omissions[:,10:].max(1),
            'within_search_percentile':rankdata(raw,method='average')/len(raw)}


def verified_commit(folder,manifest=None):
    c=json.loads((folder/'commit.json').read_text())
    if manifest is not None:assert c['manifest_sha256']==object_sha(manifest)
    for n,h in c['files'].items():assert file_sha(folder/n)==h,(folder,n)
    return c


def summarize_regions(meta,columns):
    groups={};rows=[];sens=[]
    for level in ['field_id','subfield_id','period_start']:
        for i,key in enumerate(meta[level].to_pylist()):groups.setdefault((level,str(key)),[]).append(i)
    groups['all','all']=list(range(len(meta)))
    quality=np.zeros(len(meta),bool)
    for flag in D['quality_sensitivity_flags']+['duplicate_doi','duplicate_text']:quality|=meta[flag].to_numpy().astype(bool)
    groups['quality','any_flag']=np.flatnonzero(quality);groups['quality','no_flag']=np.flatnonzero(~quality)
    for scope in ['field_period','subfield']:
        for k in KS:
            raw=columns[f'{scope}_k{k}_mean'];valid=np.isfinite(raw)
            low,high=np.quantile(raw[valid],[.1,.9])
            for (level,group),ids in groups.items():
                ix=np.asarray(ids,dtype=int);chosen=ix[valid[ix]];v=raw[chosen]
                rows.append({'scope':scope,'k':k,'level':level,'group':group,'papers':len(ix),'eligible':len(chosen),
                    'mean':float(v.mean()) if len(v) else None,'median':float(np.median(v)) if len(v) else None,
                    'p10':float(np.quantile(v,.1)) if len(v) else None,'p90':float(np.quantile(v,.9)) if len(v) else None,
                    'mean_chance_adjusted':float(columns[f'{scope}_k{k}_adjusted'][chosen].mean()) if len(v) else None,
                    'global_lower_decile_count':int((v<=low).sum()),'global_upper_decile_count':int((v>=high).sum()),
                    'lower_decile_cutoff':float(low),'upper_decile_cutoff':float(high),
                    'mean_candidate_count':float(columns[f'{scope}_candidates'][chosen].mean()) if len(v) else None,
                    'interpretation':'Observed candidates differ across groups; use matched-size control for rankings'})
            for other in KS:
                if other<=k:continue
                v2=columns[f'{scope}_k{other}_mean'];both=valid&np.isfinite(v2)
                sens.append({'scope':scope,'k_a':k,'k_b':other,'papers':int(both.sum()),
                             'spearman':float(spearmanr(raw[both],v2[both]).statistic)})
    save_csv(OUT/'regions.csv',rows);save_csv(OUT/'k_rank_consistency.csv',sens)


def main():
    with run_lock(OUT):
        verify_audit(ROOT/'data/robustness_v2/subfields_native')
        freeze(OUT,['sos_deep/regions.py','sos_deep/artifacts.py','config/analysis_v1.json'],
               ['data/robustness_v2/subfields_native/audit.json','data/analysis_v1/neighbors/manifest.json',
                'data/analysis_ready_v1/metadata.parquet','reports/analysis_v1/final/catalog.json'],
               {'scope':'R04 per-paper and regional agreement','k':KS,'primary_k':25,'omissions':{k:sorted(v) for k,v in OMIT.items()},
                'tail_rule':'Global empirical deciles, ties included; descriptive, not stable/unstable truth',
                'missing':'Groups with at most k+1 papers have no informative score; retained with null',
                'candidate_warning':'Within Field-period versus pooled Subfield changes both scope and period; not a pure detail effect'})
        meta=pq.read_table(ROOT/'data/analysis_ready_v1/metadata.parquet');n=len(meta);columns={};coverage=[]
        for scope in ['field_period','subfield']:
            columns[scope+'_candidates']=np.zeros(n,np.int32)
            for k in KS:
                for metric in ['mean','adjusted','leave_one_min','leave_one_max','leave_family_min','leave_family_max','within_search_percentile']:
                    columns[f'{scope}_k{k}_{metric}']=np.full(n,np.nan)
            if scope=='field_period':
                base=ROOT/'data/analysis_v1/neighbors';manifest=json.loads((base/'manifest.json').read_text())
                folders=sorted((base/'overlap/local').iterdir())
            else:folders=sorted((ROOT/'data/robustness_v2/subfields_native/groups').iterdir());manifest=None
            seen=np.zeros(n,bool)
            for folder in folders:
                c=verified_commit(folder,manifest)
                ids=np.load(folder/('query_row_index.npy' if scope=='field_period' else 'row_indices.npy'))
                assert not seen[ids].any();seen[ids]=True;columns[scope+'_candidates'][ids]=len(ids)
                if scope=='field_period':
                    info=json.loads((folder/'summary.json').read_text());assert info['pairs']==[list(p) for p in PAIRS] and info['ks']==KS
                    all_counts=np.load(folder/'shared_counts.npy')
                else:assert c['pair_order']==[list(p) for p in PAIRS]
                for ki,k in enumerate(KS):
                    valid=len(ids)>k+1
                    coverage.append({'scope':scope,'group':folder.name,'k':k,'papers':len(ids),'informative':valid})
                    if not valid:continue
                    counts=all_counts[:,:,ki] if scope=='field_period' else np.load(folder/f'shared_counts_k{k}.npy')
                    scores=paper_scores(counts,k,len(ids))
                    for metric,value in scores.items():columns[f'{scope}_k{k}_{metric}'][ids]=value
                print('PAPER AGREEMENT',scope,folder.name,len(ids),flush=True)
            assert seen.all(),scope
        prior=pq.read_table(ROOT/'reports/analysis_v1/final/article_neighbor_stability.parquet')
        assert np.array_equal(prior['row_index'].to_numpy(),np.arange(n))
        np.testing.assert_allclose(columns['field_period_k25_mean'],prior['mean_overlap_k25'].to_numpy(),rtol=0,atol=1e-12)
        keep=['row_index','work_id','field_id','field_display_name','subfield_id','subfield_display_name','period_start','publication_year','cohort',
              'duplicate_doi','duplicate_text']+D['quality_sensitivity_flags']
        table=meta.select(keep)
        for name,value in columns.items():table=table.append_column(name,pa.array(value,mask=~np.isfinite(value) if value.dtype.kind=='f' else None))
        pq.write_table(table,OUT/'paper_agreement.parquet',compression='zstd')
        summarize_regions(meta,columns);save_csv(OUT/'coverage.csv',coverage)
        examples=[];titles=pq.read_table(ROOT/'data/corpus_clean_v1/embedding_input.parquet',columns=['title'])['title']
        for scope in ['field_period','subfield']:
            raw=columns[scope+'_k25_mean'];ids=np.flatnonzero(np.isfinite(raw));order=ids[np.lexsort((ids,raw[ids]))]
            for tail,chosen in [('lower',order[:50]),('upper',order[-50:][::-1])]:
                for rank,i in enumerate(chosen,1):
                    r=meta.slice(int(i),1).to_pylist()[0]
                    examples.append({'scope':scope,'tail':tail,'rank':rank,'row_index':int(i),'work_id':r['work_id'],
                                     'title':titles[int(i)].as_py(),'field':r['field_display_name'],'subfield':r['subfield_display_name'],
                                     'year':r['publication_year'],'mean_overlap_k25':float(raw[i]),
                                     'candidates':int(columns[scope+'_candidates'][i]),
                                     'duplicate_doi':r['duplicate_doi'],'duplicate_text':r['duplicate_text']})
        save_csv(OUT/'paper_examples.csv',examples)
        finish(OUT,papers=n,scopes=2,source_counts_checked=True,original_paper_means_reproduced=True,
               all_ids_retained=True,missing_scores_null=True,not_sampling_intervals=True)
        print('PER-PAPER REGIONS COMPLETE',flush=True)


if __name__=='__main__':main()
