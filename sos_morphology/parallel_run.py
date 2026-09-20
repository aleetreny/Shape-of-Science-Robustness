"""Execution-only scheduler: unchanged frozen scientific functions, disjoint models.

Three OS processes, one numerical thread each; no agents or new scientific choices.
"""
from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse
import json
import multiprocessing
from pathlib import Path
import time
from sos_embed.storage import file_sha, write_json, run_lock, utcnow
from . import run


def worker(model):
    data=run.NativeData(run.ROOT,max_bytes=6*1024**3)
    with run.np.load(run.OUT/'selections.npz',allow_pickle=False) as z:
        selections={k:z[k] for k in z.files}
    start=time.monotonic()
    for stage,fn in [('native',run.native_stage),('temporal',run.temporal_stage),('controls',run.controls_stage)]:
        fn(data,selections,model,run.D['models'][model])
        print(f'WORKER {model} {stage} complete; elapsed {time.monotonic()-start:.1f}s',flush=True)
    return model


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=3);args=parser.parse_args()
    assert 1<=args.workers<=3
    with run_lock(run.OUT):
        manifest=json.loads((run.OUT/'manifest.json').read_text())
        for key in ['source_files','parent_files']:
            for name,digest in manifest[key].items():assert file_sha(run.ROOT/name)==digest,name
        name='sos_morphology/parallel_run.py'
        provenance={'source':name,'source_sha256':file_sha(run.ROOT/name),'workers':args.workers,
                    'numerical_threads_per_worker':1,'unchanged_scientific_manifest':file_sha(run.OUT/'manifest.json')}
        path=run.OUT/'execution_manifest.json'
        if path.exists():assert json.loads(path.read_text())==provenance
        else:write_json(path,provenance)
        snap=run.OUT/'source_snapshot'/name;snap.parent.mkdir(exist_ok=True,parents=True)
        if snap.exists():assert file_sha(snap)==provenance['source_sha256']
        else:snap.write_bytes((run.ROOT/name).read_bytes())
        start=time.monotonic();done=[]
        with ProcessPoolExecutor(max_workers=args.workers,mp_context=multiprocessing.get_context('spawn')) as pool:
            jobs={pool.submit(worker,m):m for m in run.D['models']}
            for job in as_completed(jobs):
                model=job.result();done.append(model)
                write_json(run.OUT/'progress.json',{'state':'running','completed_models':done,'updated_at':utcnow(),'elapsed_s':time.monotonic()-start})
        run.audit()
        write_json(run.OUT/'progress.json',{'state':'complete','completed_models':done,'updated_at':utcnow(),'elapsed_s':time.monotonic()-start})


if __name__=='__main__':main()
