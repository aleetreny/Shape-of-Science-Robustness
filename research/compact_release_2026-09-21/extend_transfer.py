"""Continue the active, authorized transfer with enough time after a file finishes."""
from pathlib import Path
import importlib.util,json,re,subprocess,time,urllib.request
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('z',ROOT/'scripts/zenodo_upload.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);token=m.load_token()
repo='aleetreny/Shape-of-Science-Reproducibility';old='35609364390';start=time.monotonic();last=None
while time.monotonic()-start<2400:
 request=urllib.request.Request('https://zenodo.org/api/deposit/depositions/22876602',headers={'Authorization':'Bearer '+token,'User-Agent':'ShapeOfScienceReproduction/1.1'})
 with urllib.request.urlopen(request,timeout=30) as response:d=json.load(response)
 n=len(d['files'])
 if n!=last:print('Completed files:',n,flush=True);last=n
 if n==15:print('All files completed; no restart needed.',flush=True);raise SystemExit()
 state=json.loads(subprocess.check_output(['gh','run','view',old,'--repo',repo,'--json','status,conclusion'],text=True))
 if n>=13 or state['status']=='completed':
  if state['status']!='completed':
   subprocess.run(['gh','run','cancel',old,'--repo',repo],check=True,capture_output=True,text=True)
   for _ in range(24):
    state=json.loads(subprocess.check_output(['gh','run','view',old,'--repo',repo,'--json','status,conclusion'],text=True))
    if state['status']=='completed':break
    time.sleep(5)
   assert state['status']=='completed','Old job must finish before continuing'
  result=subprocess.run(['gh','workflow','run','deposit.yml','--repo',repo,'--ref','main'],check=True,capture_output=True,text=True)
  print(result.stdout,flush=True)
  found=re.search(r'/runs/(\d+)',result.stdout);assert found,'Read new run ID from workflow response'
  p=HERE/'live_state.json';live=json.loads(p.read_text());live['workflow_run_id']=int(found[1]);live['workflow_extended_from']=int(old);live['workflow_timeout_minutes']=180;p.write_text(json.dumps(live,indent=2)+'\n')
  print('Transfer continued; completed uploads retained.',flush=True);raise SystemExit()
 time.sleep(20)
raise SystemExit('No completed-file boundary within 40 minutes; inspect the active job before retrying.')
