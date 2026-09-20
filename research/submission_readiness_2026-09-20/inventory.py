"""Read-only size and public-version audit for a possible replication deposit."""
from pathlib import Path
import collections
import csv
import datetime
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
GROUPS = [
    'data/corpus_clean_v1', 'data/analysis_ready_v1', 'data/embeddings_v1',
    'data/analysis_v1', 'data/checklist_v1', 'data/robustness_v2',
    'data/prepaper_v1', 'data/morphology_pilot_v1',
    'data/field_pair_summary_v1', 'data/robustness_closure_v1',
    'reports', 'manuscript', 'manuscript_es', 'config',
]

def gh(*args):
    return json.loads(subprocess.check_output(['gh', *args], cwd=ROOT, text=True))

def main():
    rows = []
    summary = {}
    for group in GROUPS:
        files = [p for p in (ROOT / group).rglob('*') if p.is_file()]
        entries = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                    'suffix': p.suffix or '(none)', 'group': group} for p in files]
        rows.extend(entries)
        by_ext = collections.Counter()
        for e in entries:
            by_ext[e['suffix']] += e['bytes']
        by_child = collections.Counter()
        for e in entries:
            child = Path(e['path']).relative_to(group).parts[0]
            by_child[child] += e['bytes']
        summary[group] = {
            'files': len(entries), 'bytes': sum(e['bytes'] for e in entries),
            'by_suffix': dict(by_ext), 'by_child': dict(by_child),
            'largest_files': sorted(entries, key=lambda e: -e['bytes'])[:4],
        }
    with (OUT / 'local_inventory.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['path', 'bytes', 'suffix', 'group'])
        writer.writeheader()
        writer.writerows(rows)
    repo = gh('api', 'repos/aleetreny/Shape-of-Science-Robustness')
    commit = gh('api', 'repos/aleetreny/Shape-of-Science-Robustness/commits/main')
    tree = gh('api', f"repos/aleetreny/Shape-of-Science-Robustness/git/trees/{commit['sha']}?recursive=1")
    public_paths = {e['path'] for e in tree['tree'] if e['type'] == 'blob'}
    important = ['manuscript/main.tex', 'sos_morphology/run.py',
                 'sos_pair_summary/analyze.py', 'sos_closure/morphology.py',
                 'sos_closure/centres.py', 'sos_closure/headline.py',
                 'sos_closure/quality.py', 'LICENSE', 'CITATION.cff']
    remote = {
        'url': repo['html_url'], 'private': repo['private'],
        'head': commit['sha'], 'committed_at': commit['commit']['committer']['date'],
        'license': repo['license'], 'tree_truncated': tree['truncated'],
        'tracked_files': len(public_paths),
        'important_paths': {p: p in public_paths for p in important},
    }
    (OUT / 'remote_tree.json').write_text(json.dumps(tree, indent=2) + '\n')
    (OUT / 'public_state.json').write_text(json.dumps(remote, indent=2) + '\n')
    result = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'sizes_are': 'logical uncompressed bytes; directory totals include intermediate duplicates and text',
              'groups': summary, 'public': remote}
    (OUT / 'inventory_summary.json').write_text(json.dumps(result, indent=2) + '\n')
    for group, item in summary.items():
        print(f"{group}: {item['files']} files; {item['bytes']/1e9:.3f} GB")
    print(json.dumps(remote, indent=2))
    protected = []
    for name in ['manuscript/main.tex', 'manuscript_es/main.tex', 'manuscript/supplement.tex',
                 'manuscript_es/supplement.tex', 'references/references.bib',
                 'output/pdf/main.pdf', 'output/pdf/es/main.pdf']:
        p = ROOT / name
        protected.append({'path': name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    target = OUT / 'editorial_baseline.json'
    if not target.exists():
        target.write_text(json.dumps(protected, indent=2) + '\n')

if __name__ == '__main__':
    main()
