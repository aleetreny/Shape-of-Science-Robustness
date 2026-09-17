from pathlib import Path
import argparse,json,os,subprocess,sys,time
root=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--input-pid',type=int,required=True);args=p.parse_args()
audit=root/'research/robustness_2026-09-17/input_audit/audit_summary.json'
print('Waiting for live input queue PID',args.input_pid,flush=True)
while True:
 if audit.exists() and json.loads(audit.read_text())['all_complete']:break
 try:os.kill(args.input_pid,0)
 except ProcessLookupError:raise RuntimeError('Input queue ended without completed audit; inspect input52_run.log, do not restart automatically')
 time.sleep(20)
subprocess.run([sys.executable,'-m','sos_deep.input_analysis52'],cwd=root,check=True)
subprocess.run([sys.executable,'-m','sos_deep.input_recipes52'],cwd=root,check=True)
print('52K PRIMARY AND RECIPE COMPARISONS COMPLETE',flush=True)
