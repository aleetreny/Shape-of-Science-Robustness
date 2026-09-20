from pathlib import Path
import json,csv,sys
import numpy as np
sys.path.insert(0,str(Path('.').resolve()))
from sos_embed.storage import file_sha,write_json
from sos_followup.pilot_statistics import cosine_grams,cka_matrix
root=Path('.');o=root/'research/robustness_closure_2026-09-20';a=json.loads((o/'audit_probe.json').read_text())
verified={}
for folder in ['data/robustness_v2/centroid_scales','data/morphology_pilot_v1','data/field_pair_summary_v1','data/robustness_v2/input_comparisons','data/robustness_v2/input_recipes']:
 p=root/folder/'audit.json'
 if not p.exists():continue
 d=json.loads(p.read_text());assert d['all_complete']
 for name,h in d['files'].items():assert file_sha((root/folder/name) if (root/folder/name).exists() else root/name)==h,(folder,name)
 verified[folder]={'audit_sha256':file_sha(p),'files_verified':len(d['files'])}
base=root/'data/robustness_v2/centroid_scales';models=list(json.loads((root/'config/analysis_v1.json').read_text())['poolings'])
with (base/'comparisons.csv').open() as st:rows=list(csv.DictReader(st))
checks={}
for cond in ['matched_field','matched_subfield']:
 xs=[]
 for m in models:
  p=base/(m+'_centroids.npz');assert file_sha(p)==json.loads(p.with_suffix('.commit.json').read_text())['sha256'];xs.append(np.load(p)[cond])
 ck=cka_matrix(cosine_grams(xs));errors=[abs(ck[models.index(r['model_a']),models.index(r['model_b'])]-float(r['cka_debiased'])) for r in rows if r['condition']==cond and r['groups']=='real'];checks[cond]=max(errors);assert max(errors)<1e-12
with (root/'reports/robustness_v2/final/tables/structure_subfield_stability_alerts.csv').open() as st:alerts=list(csv.DictReader(st))
c=sum(r['large_sample_equals_whole_group']=='False' for r in alerts);assert c==2628
fixed=np.load(base/'one_subfield_per_field.npy');assert fixed.shape==(20,26)
assert a['quality_retained']==448886 and all(x['period_exact'] for x in a['centroid_random_checks'].values())
write_json(o/'phase0_audit.json',{'status':'passed_no_scientific_bug_found','prior_audits':verified,'saved_centre_reproduction_max_errors':checks,'subfield_local_alerts':2628,'subfield_local_comparisons':8235,'restricted_subfield_repetitions':20,'restricted_subfield_article_resampling':False,'restricted_subfield_reported_reduction':'mean over 20 selections x 45 model pairs','reporting_omission':'Article unit vectors are averaged; centres are unit-normalised again before corrected CKA. Frozen config documents this, main methods should state it explicitly.','minimum_clean_cell':min(r['clean'] for r in a['cell_counts']),'cells_eligible2048':sum(r['clean']>=2048 for r in a['cell_counts']),'minimum_input_clean_cell':min(r['input_clean'] for r in a['cell_counts']),'kernel_feature_error':a['kernel_feature_cka_error']})
print(json.loads((o/'phase0_audit.json').read_text()))
