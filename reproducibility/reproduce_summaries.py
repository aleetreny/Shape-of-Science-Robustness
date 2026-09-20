"""Reaggregate figure-level results from per-condition measurements, offline."""
import collections, csv, gzip, hashlib, json, math, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ABS_TOL=1e-12

def read(name):
    with gzip.open(HERE/'inputs'/name,'rt',newline='') as f:return list(csv.DictReader(f))
def mean(x):return math.fsum(x)/len(x)
def close(a,b):assert math.isclose(a,b,rel_tol=0,abs_tol=ABS_TOL),(a,b)

def main():
    provenance=json.loads((HERE/'inputs/manifest.json').read_text())
    for name,h in provenance.items():assert hashlib.sha256((HERE/'inputs'/name).read_bytes()).hexdigest()==h,name
    groups=collections.defaultdict(list)
    for r in read('centres.csv.gz'):groups[r['design'],r['grouping']].append(float(r['mean']))
    expected=read('centres_expected.csv.gz')
    for r in expected:
        x=groups[r['design'],r['grouping']];assert len(x)==int(r['n']);close(mean(x),float(r['mean']))
    centre_result={k[0]:mean(v) for k,v in groups.items() if k[1]=='observed' and k[0] in ['repeat256_field','repeat256_subfield217']}
    scope=collections.defaultdict(list)
    for r in read('scope.csv.gz'):scope[int(r['k']),r['subfield_id'],r['scope']].append(float(r['mean_overlap']))
    fields=sorted({k[1] for k in scope});scope_result=[]
    for r in read('scope_expected.csv.gz'):
        k=int(r['k']);a=[mean(scope[k,f,'subfield']) for f in fields];b=[mean(scope[k,f,'field']) for f in fields];d=[x-y for x,y in zip(a,b)]
        assert len(d)==int(r['subfields'])==217
        lower=sum(x<0 for x in d);higher=sum(x>0 for x in d)
        assert lower==int(r['subfields_lower_agreement']) and higher==int(r['subfields_higher_agreement'])
        close(mean(d),float(r['mean_difference']));scope_result.append({'k':k,'lower':lower,'higher':higher,'mean_difference':mean(d)})
    headline=collections.defaultdict(list)
    for r in read('headline.csv.gz'):
        for measure in ['model_change','title_only_change','title_minus_model']:headline[r['recipe'],int(r['k']),measure,int(r['repeat'])].append(float(r[measure]))
    grand=collections.defaultdict(list)
    for key,x in headline.items():assert len(x)==26;grand[key[:3]].append(mean(x))
    for r in read('headline_expected.csv.gz'):
        x=grand[r['recipe'],int(r['k']),r['measure']];assert len(x)==int(r['n'])==50;close(mean(x),float(r['mean']))
    subprocess.run([sys.executable,'-I','-S',str(HERE/'figure4/reproduce.py')],check=True,stdout=subprocess.DEVNULL)
    print(json.dumps({'all_checks_passed':True,'centres':centre_result,'search_scope':scope_result,'headline_mean_k25':{m:mean(grand['mean',25,m]) for m in ['model_change','title_only_change','title_minus_model']},'figure4':'all eight classifications and same-model retention verified','scope':'aggregation from per-condition measurements; not regeneration of vectors or all metrics'},indent=2))

if __name__=='__main__':main()
