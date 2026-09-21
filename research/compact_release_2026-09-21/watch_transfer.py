"""Read-only monitor of the already running compact transfer; never publishes."""
import importlib.util,json,subprocess,time,urllib.error,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('z',ROOT/'scripts/zenodo_upload.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);token=m.load_token()
last=None;started=time.monotonic()
while time.monotonic()-started<10800:
 try:
  req=urllib.request.Request('https://zenodo.org/api/deposit/depositions/22876602',headers={'Authorization':'Bearer '+token,'User-Agent':'ShapeOfScienceReproduction/1.1'})
  with urllib.request.urlopen(req,timeout=30) as response:d=json.load(response)
  n=len(d['files'])
  if n!=last:
   print(json.dumps({'completed':n,'total':15,'MB':round(sum(f['filesize'] for f in d['files'])/1e6,2)}),flush=True);last=n
   p=HERE/'live_state.json';state=json.loads(p.read_text());state['zenodo_files_completed']=n;p.write_text(json.dumps(state,indent=2)+'\n')
  if n==15:
   run=json.loads(subprocess.check_output(['gh','run','view','35612671848','--repo','aleetreny/Shape-of-Science-Reproducibility','--json','status,conclusion'],text=True))
   if run['status']=='completed':
    assert run['conclusion']=='success',run
    print('All uploads complete and workflow succeeded; ready for separate publication verification.',flush=True);raise SystemExit()
 except (OSError,urllib.error.URLError) as exc:print('Transient read failure:',type(exc).__name__,flush=True)
 time.sleep(30)
raise SystemExit('Monitor stopped after three hours; inspect the workflow state.')
