"""Export compact, non-text inputs for an offline standard-library check."""
from pathlib import Path
import gzip,hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'reproducibility';(OUT/'inputs').mkdir(parents=True,exist_ok=True)
mapping={
 'centres.csv.gz':'data/robustness_closure_v1/centres/repetitions.csv',
 'centres_expected.csv.gz':'reports/robustness_closure_v1/centres_summary.csv',
 'scope.csv.gz':'data/robustness_v2/paired_neighbor_scales/groups.csv',
 'scope_expected.csv.gz':'reports/robustness_v2/final/tables/structure_paired_scope_summary.csv',
 'headline.csv.gz':'data/robustness_closure_v1/headline/field_repetitions.csv',
 'headline_expected.csv.gz':'reports/robustness_closure_v1/headline_summary.csv',
}
manifest={};source={}
for name,rel in mapping.items():
 data=(ROOT/rel).read_bytes();compressed=gzip.compress(data,mtime=0);(OUT/'inputs'/name).write_bytes(compressed)
 manifest[name]=hashlib.sha256(compressed).hexdigest();source[name]={'source':rel,'source_sha256':hashlib.sha256(data).hexdigest()}
(OUT/'inputs/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'inputs/provenance.json').write_text(json.dumps(source,indent=2)+'\n')
shutil.copytree(ROOT/'research/submission_readiness_2026-09-20/replication_demo',OUT/'figure4',dirs_exist_ok=True)
print('Quickstart inputs exported')
