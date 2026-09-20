"""Predefined descriptive summaries; no new selection or metric definitions."""
from collections import defaultdict
import itertools
import numpy as np
import pyarrow.parquet as pq
from scipy.stats import spearmanr
from sos_pair_summary.analyze import relative_difference,persistent_direction,classify
from .common import *

def grouped(rows,keys):
 d=defaultdict(list)
 for row in rows:d[tuple(row[k] for k in keys)].append(row)
 return d

def centres():
 src=OUT/'centres';rep=read_csv(src/'repetitions.csv');pairs=read_csv(src/'model_pairs.csv');loo=read_csv(src/'leave_one_field_out.csv')
 prior=read_csv(ROOT/'data/robustness_v2/centroid_scales/comparisons.csv');old={}
 for r in prior:
  if r['groups']=='real':old.setdefault(r['condition'],[]).append(float(r['cka_debiased']))
 old={k:float(np.mean(v)) for k,v in old.items()}
 summary=[];reference=[];nested=[];pairsummary=[];influence=[];ranks=[]
 for (design,typ),rr in grouped(rep,['design','grouping']).items():
  values=np.array([float(r['mean']) for r in rr]);condition='matched_field' if design.endswith('_field') else 'matched_subfield' if design=='repeat256_subfield217' else 'one_subfield_per_field' if design=='nested26' else None
  summary.append({'design':design,'grouping':typ,**stats(values),'old_reference':old.get(condition),'largest_difference_from_old':float(np.max(abs(values-old[condition]))) if condition else None})
 for (design,),rr in grouped(rep,['design']).items():
  a=np.array([float(r['mean']) for r in rr if r['grouping']=='observed']);b=np.array([float(r['mean']) for r in rr if r['grouping']=='random']);assert len(a)==len(b)
  reference.append({'design':design,'repetitions':len(a),'observed_mean':float(a.mean()),'random_mean':float(b.mean()),'mean_difference':float((a-b).mean()),'smallest_paired_difference':float((a-b).min()),'random_max':float(b.max()),'observed_min':float(a.min()),'observed_p025':float(np.quantile(a,.025)),'random_at_least_observed_p025':int(np.sum(b>=np.quantile(a,.025))),'random_at_least_any_observed':int(np.sum(b>=a.min())),'random_at_least_paired_observed':int(np.sum(b>=a))})
 for key,rr in grouped(pairs,['design','grouping','model_a','model_b']).items():pairsummary.append(dict(zip(['design','grouping','model_a','model_b'],key),**stats([float(r['cka']) for r in rr])))
 for typ in ['observed','random']:
  rr=sorted([r for r in rep if r['design']=='nested26' and r['grouping']==typ],key=lambda r:int(r['repeat']));v=np.array([float(r['mean']) for r in rr]).reshape(50,10);means=v.mean(1);sds=v.std(1,ddof=1)
  nested.append({'grouping':typ,'outer_subfield_choices':50,'inner_article_choices':10,'between_subfield_mean_sd':float(means.std(ddof=1)),'mean_within_subfield_article_sd':float(sds.mean()),'median_within_subfield_article_sd':float(np.median(sds)),'largest_within_article_range':float(np.ptp(v,axis=1).max()),**{'outer_'+k:w for k,w in stats(means).items()}})
 for key,rr in grouped(loo,['selection','omitted_field']).items():
  v=np.array([float(r['without']) for r in rr]);delta=np.array([float(r['change']) for r in rr]);influence.append({'selection':int(key[0]),'omitted_field':int(key[1]),'mean_without':float(v.mean()),'mean_change':float(delta.mean()),'largest_pair_change':float(abs(delta).max())})
 influencepairs=[]
 for key,rr in grouped(loo,['omitted_field','model_a','model_b']).items():influencepairs.append(dict(zip(['omitted_field','model_a','model_b'],key),**stats([float(r['change']) for r in rr]),largest_absolute_change=max(abs(float(r['change'])) for r in rr)))
 index={(r['design'],r['grouping'],int(r['repeat']),r['model_a'],r['model_b']):float(r['cka']) for r in pairs}
 for level in ['field','subfield183']:
  for a,b in [(128,256),(256,512),(128,512)]:
   values=[]
   for repno in range(50):
    x=[index[f'size{a}_{level}','observed',repno,MODELS[i],MODELS[j]] for i,j in PAIRS];y=[index[f'size{b}_{level}','observed',repno,MODELS[i],MODELS[j]] for i,j in PAIRS];values.append(float(spearmanr(x,y).statistic))
   ranks.append({'level':level,'size_a':a,'size_b':b,**stats(values)})
 for name,rows in [('centres_summary',summary),('centres_random_reference',reference),('centres_model_pairs',pairsummary),('centres_nested_sources',nested),('centres_omissions',influence),('centres_omission_model_pairs',influencepairs),('centres_size_rank_stability',ranks)]:save_csv(REPORT/(name+'.csv'),rows)
 return {'original_means':old,'summary':summary,'random_reference':reference,'nested_sources':nested,'original_omission_mean_range':stats([r['mean_without'] for r in influence if r['selection']==-1]),'largest_original_omission_mean':max([r for r in influence if r['selection']==-1],key=lambda r:abs(r['mean_change'])),'largest_original_model_pair_omission':max([r for r in loo if r['selection']=='-1'],key=lambda r:abs(float(r['change']))),'size_pair_rank_stability':ranks}

def headline():
 src=OUT/'headline';rr=read_csv(src/'field_repetitions.csv');effects=read_csv(src/'effects.csv');old=read_csv(ROOT/'data/robustness_v2/input_recipes/effects.csv');baseline={}
 for key,vals in grouped([r for r in old if r['input_condition']=='title' and r['metric'].startswith('neighbors')],['recipe','metric']).items():
  baseline[key[0],int(key[1][9:])]={'model_change':float(np.mean([float(r['model_change_at_full']) for r in vals])),'title_only_change':float(np.mean([float(r['input_change_from_full']) for r in vals])),'title_minus_model':-float(np.mean([float(r['model_minus_input']) for r in vals]))}
 grand=[]
 for (recipe,k,rep),values in grouped(rr,['recipe','k','repeat']).items():
  assert len(values)==26;grand.append({'recipe':recipe,'k':int(k),'repeat':int(rep),**{v:float(np.mean([float(r[v]) for r in values])) for v in ['model_change','title_only_change','title_minus_model']}})
 summary=[]
 for (recipe,k),vals in grouped(grand,['recipe','k']).items():
  for measure in ['model_change','title_only_change','title_minus_model']:
   x=np.array([r[measure] for r in vals]);ref=baseline[recipe,k][measure];summary.append({'recipe':recipe,'k':k,'measure':measure,'full52000':ref,**stats(x),'opposite_sign_fraction':float(np.mean(x*ref<0)),'negative_fraction':float(np.mean(x<0))})
 local=[]
 for key,vals in grouped(effects,['recipe','k','field_id','model']).items():
  x=np.array([float(r['title_minus_model']) for r in vals]);local.append(dict(zip(['recipe','k','field_id','model'],key),**stats(x),positive_fraction=float(np.mean(x>0)),negative_fraction=float(np.mean(x<0))))
 bymodel=[]
 for key,vals in grouped(effects,['recipe','k','model','repeat']).items():bymodel.append(dict(zip(['recipe','k','model','repeat'],key),title_minus_model=float(np.mean([float(r['title_minus_model']) for r in vals]))))
 models=[]
 for key,vals in grouped(bymodel,['recipe','k','model']).items():models.append(dict(zip(['recipe','k','model'],key),**stats([r['title_minus_model'] for r in vals])))
 fields=[]
 for key,vals in grouped(rr,['recipe','k','field_id']).items():fields.append(dict(zip(['recipe','k','field_id'],key),**stats([float(r['title_minus_model']) for r in vals]),positive_fraction=float(np.mean([float(r['title_minus_model'])>0 for r in vals]))))
 for name,rows in [('headline_grand_repetitions',grand),('headline_summary',summary),('headline_field_model_stability',local),('headline_models',models),('headline_fields',fields)]:save_csv(REPORT/(name+'.csv'),rows)
 mainmodels=[r for r in models if r['recipe']=='mean' and r['k']=='25'];mainfields=[r for r in fields if r['recipe']=='mean' and r['k']=='25']
 return {'summary':summary,'primary_k25_model_range':stats([r['mean'] for r in mainmodels]),'primary_k25_field_range':stats([r['mean'] for r in mainfields]),'primary_k25_models':mainmodels,'primary_k25_fields':mainfields}

def morphology():
 rows=pq.read_table(OUT/'morphology/metrics.parquet').to_pylist();index={(r['representation'],r['model'],r['kind'],r['repeat'],r['field_id']):r for r in rows};conditions=[('primary',0)]+[('half',i) for i in range(20)]+[('external',i) for i in range(5)];fp=list(itertools.combinations(FIELDS,2));ia,ib=np.array([[FIELDS.index(a),FIELDS.index(b)] for a,b in fp]).T
 cubes={}
 for representation,metric in [('original','angle_p50'),('original','pr'),('original','erank'),('original','d80'),('global_centered','angle_p50'),('global_centered','pr')]:
  values=np.array([[[index[representation,m,k,r,f][metric] for k,r in conditions] for f in FIELDS] for m in MODELS]);assert np.isfinite(values).all();cubes[representation,metric]=relative_difference(values[:,ia,:],values[:,ib,:]).transpose(1,0,2)
  for f in FIELDS:
   for k,r in conditions:assert len({index[representation,m,k,r,f]['selection_sha256'] for m in MODELS})==1
 summary=[];pair_rows=[];direction_rows=[];transitions=[];witnessrows=[];controls=[];alts=[]
 for floor in D['morphology']['floors']:
  signs={key:persistent_direction(value,floor,1e-10) for key,value in cubes.items()};classes={key:classify(v) for key,v in signs.items()}
  for (representation,metric),labels in classes.items():
   summary.append({'representation':representation,'metric':metric,'cutoff':floor,'unanimous':int(np.sum(labels=='unanimous')),'contradiction':int(np.sum(labels=='contradiction')),'unresolved':int(np.sum(labels=='unresolved')),'pairs':325,'conditions':26})
   for j,(a,b) in enumerate(fp):
    pair_rows.append({'representation':representation,'metric':metric,'cutoff':floor,'field_a':a,'field_b':b,'class':str(labels[j]),'positive_models':int(np.sum(signs[representation,metric][j]==1)),'negative_models':int(np.sum(signs[representation,metric][j]==-1))})
    for mi,m in enumerate(MODELS):
     v=cubes[representation,metric][j,mi];direction_rows.append({'representation':representation,'metric':metric,'cutoff':floor,'field_a':a,'field_b':b,'model':m,'direction':int(signs[representation,metric][j,mi]),'smallest_relative_difference':float(v.min()),'largest_relative_difference':float(v.max())})
  for metric in ['angle_p50','pr']:
   orig=signs['original',metric];new=signs['global_centered',metric];co=classes['original',metric];cn=classes['global_centered',metric];same=[];reversed_=[];wtotal=wsame=wreverse=0
   for pi,(a,b) in enumerate(fp):
    witnesses=[(i,j) for i,j in PAIRS if orig[pi,i]*orig[pi,j]==-1];ret=[];rev=[]
    for i,j in witnesses:
     retained=bool(new[pi,i]==orig[pi,i] and new[pi,j]==orig[pi,j]);reverse=bool(new[pi,i]==-orig[pi,i] and new[pi,j]==-orig[pi,j]);ret.append(retained);rev.append(reverse);witnessrows.append({'metric':metric,'cutoff':floor,'field_a':a,'field_b':b,'model_a':MODELS[i],'model_b':MODELS[j],'original_direction_a':int(orig[pi,i]),'original_direction_b':int(orig[pi,j]),'centered_direction_a':int(new[pi,i]),'centered_direction_b':int(new[pi,j]),'same_directions':retained,'both_reversed':reverse})
    same.append(any(ret));reversed_.append(any(rev));wtotal+=len(witnesses);wsame+=sum(ret);wreverse+=sum(rev)
   for a in ['unanimous','contradiction','unresolved']:
    for b in ['unanimous','contradiction','unresolved']:transitions.append({'metric':metric,'cutoff':floor,'original':a,'centered':b,'pairs':int(np.sum((co==a)&(cn==b)))})
   controls.append({'metric':metric,'cutoff':floor,'original_oppositions':int(np.sum(co=='contradiction')),'centered_oppositions':int(np.sum(cn=='contradiction')),'retained_opposition_class':int(np.sum((co=='contradiction')&(cn=='contradiction'))),'lost_opposition_class':int(np.sum((co=='contradiction')&(cn!='contradiction'))),'new_oppositions':int(np.sum((co!='contradiction')&(cn=='contradiction'))),'same_fixed_witness_directions_retained':int(sum(same)),'at_least_one_fixed_witness_both_reversed':int(sum(reversed_)),'original_witness_model_pairs':wtotal,'witness_model_pairs_same_directions':wsame,'witness_model_pairs_both_reversed':wreverse,'unanimous_class_retained':int(np.sum((co=='unanimous')&(cn=='unanimous'))),'unanimous_same_direction_retained':int(np.sum((co=='unanimous')&np.all(orig==new,axis=1))),'original_oppositions_now_unresolved':int(np.sum((co=='contradiction')&(cn=='unresolved')))})
  original=signs['original','pr'];baseclass=classes['original','pr']
  for label,metrics in [('erank',['erank']),('d80',['d80']),('both',['erank','d80'])]:
   valid=np.ones_like(original,dtype=bool)
   for m in metrics:valid &= persistent_direction(cubes['original',m],0.0,1e-10)==original
   joint=np.where(valid,original,0);jointclass=classify(joint)
   alts.append({'alternative':label,'cutoff':floor,'PR_oppositions':int(np.sum(baseclass=='contradiction')),'same_witness_directions_retained':int(np.sum(jointclass=='contradiction')),'same_unanimous_directions_retained':int(np.sum(jointclass=='unanimous')),'conditions':26,'alternative_cutoff':0.0,'cutoff_applies_to':'PR'})
 for name,r in [('morphology_classification',summary),('morphology_pairs',pair_rows),('morphology_directions',direction_rows),('morphology_centering_transitions',transitions),('morphology_centering_witnesses',witnessrows),('morphology_centering_summary',controls),('dimension_alternative_retention',alts)]:save_csv(REPORT/(name+'.csv'),r)
 panel_rows=read_csv(ROOT/'reports/field_pair_summary_v1/model_panel_summary.csv')
 for r in panel_rows:
  if r['metric']!='pr':continue
  cutoff=float(r['minimum_relative_difference']);panel=r['panel']
  subset=list(range(10)) if panel=='all_ten' else [MODELS.index(m) for m in ['specter','specter2','scincl','mpnet','minilm','simcse']] if panel=='six_similarity' else [i for i,m in enumerate(MODELS) if m!=panel.removeprefix('omit_')]
  assert len(subset)==int(r['models']),(panel,subset)
  sp=persistent_direction(cubes['original','pr'],cutoff,1e-10);valid=np.ones_like(sp,dtype=bool)
  for alt in ['erank','d80']:valid &= persistent_direction(cubes['original',alt],0.0,1e-10)==sp
  cl=classify(np.where(valid,sp,0)[:,subset]);r['contradiction_and_alternatives']=int(np.sum(cl=='contradiction'));r['unanimous_and_alternatives']=int(np.sum(cl=='unanimous'))
 save_csv(REPORT/'model_panel_summary_full_alternatives.csv',panel_rows)
 original={r['metric']:r['contradiction'] for r in summary if r['representation']=='original' and r['cutoff']==0};assert original['angle_p50']==262 and original['pr']==221,original
 return {'classification':summary,'centering':controls,'alternatives':alts}

def quality():
 rows=read_csv(OUT/'quality/native_comparisons.csv');summary=[];fields=[];pairs=[]
 for (scope,k),r in grouped(rows,['scope','k']).items():
  v=np.array([float(a['original_same_queries_overlap']) for a in r]);w=np.array([float(a['filtered_overlap']) for a in r]);adj=np.array([float(a['filtered_adjusted'])-float(a['original_adjusted']) for a in r]);rawold=[float(a['original_all_queries_overlap']) for a in r if a['original_all_queries_overlap']]
  summary.append({'scope':scope,'k':int(k),'cells':len(set((a['field_id'],a['period']) for a in r)),'original_all_query_overlap':float(np.mean(rawold)) if rawold else None,'original_same_query_overlap':float(v.mean()),'filtered_overlap':float(w.mean()),'change_pp':float(100*(w-v).mean()),'mean_absolute_change_pp':float(100*abs(w-v).mean()),'adjusted_change_pp':float(100*adj.mean()),'largest_absolute_cell_pair_change_pp':float(100*abs(w-v).max())})
 for keys,out in [(['scope','k','field_id'],fields),(['scope','k','model_a','model_b'],pairs)]:
  for key,r in grouped(rows,keys).items():out.append(dict(zip(keys,key),**stats([float(a['change_pp']) for a in r])))
 inp=read_csv(OUT/'quality/input/comparisons.csv');ineffects=read_csv(OUT/'quality/input/effects.csv');ins=[]
 for (k,),r in grouped(inp,['k']).items():
  for label,subset in [('model_change',[a for a in r if a['model_a']!=a['model_b']]),('title_only',[a for a in r if a['input_b']=='title']),('abstract_only',[a for a in r if a['input_b']=='abstract'])]:
   ins.append({'k':int(k),'comparison':label,'original_overlap':float(np.mean([float(a['original_overlap']) for a in subset])),'filtered_overlap':float(np.mean([float(a['filtered_overlap']) for a in subset])),'change_pp':float(np.mean([float(a['change_pp']) for a in subset]))})
 ine=[]
 for key,r in grouped(ineffects,['k','corpus']).items():ine.append({'k':int(key[0]),'corpus':key[1],**{v:float(np.mean([float(a[v]) for a in r])) for v in ['model_change','title_only_change','abstract_only_change','title_minus_model']}})
 for name,r in [('quality_summary',summary),('quality_fields',fields),('quality_model_pairs',pairs),('quality_input_summary',ins),('quality_input_effects',ine)]:save_csv(REPORT/(name+'.csv'),r)
 return {'summary':summary,'input_summary':ins,'input_effects':ine,'largest_field_mean_changes':sorted([r for r in fields if r['scope']=='all' and r['k']=='25'],key=lambda r:abs(r['mean']),reverse=True)[:5],'largest_model_pair_mean_changes':sorted([r for r in pairs if r['scope']=='all' and r['k']=='25'],key=lambda r:abs(r['mean']),reverse=True)[:5]}

def main():
 REPORT.mkdir(parents=True,exist_ok=True)
 for b in ['centres','headline','morphology','quality']:
  a=json.loads((OUT/b/'audit.json').read_text());assert a['all_complete']
  for n,h in a['files'].items():assert file_sha(OUT/b/n)==h,(b,n)
 folder=freeze('summary',['sos_closure/summarize.py','sos_pair_summary/analyze.py'],[str((OUT/b/'audit.json').relative_to(ROOT)) for b in ['centres','headline','morphology','quality']])
 s={'centres':centres(),'headline':headline(),'morphology':morphology(),'quality':quality(),'local_subfield_stability':{'alerts':2628,'comparisons':8235,'percent':2628/8235*100}}
 write_json(REPORT/'summary.json',s);write_json(REPORT/'catalog.json',{'files':{p.name:file_sha(p) for p in sorted(REPORT.glob('*')) if p.is_file() and p.name!='catalog.json'},'source_manifest_sha256':file_sha(folder/'manifest.json')});finish(folder,report_catalog_sha256=file_sha(REPORT/'catalog.json'))
 print('FINAL ROBUSTNESS RESULTS FROZEN')
if __name__=='__main__':main()
