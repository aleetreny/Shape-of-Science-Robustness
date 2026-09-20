"""Read-only verification of the display package and its frozen research inputs."""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pypdf import PdfReader
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
EVID=Path(__file__).resolve().parent
MAN=ROOT/'manuscript'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(path):
    with path.open() as f:return list(csv.DictReader(f))


def run():
    baseline=json.loads((EVID/'baseline_manifest.json').read_text())
    for rel,h in baseline['documents'].items():
        assert sha(EVID/'baseline_documents'/rel)==h,rel
    for rel,h in baseline['scientific_reports'].items():
        assert sha(ROOT/rel)==h,rel
    assert sha(ROOT/'research/writing_blueprint_2026-09-18/closure_audit.json')==baseline['previous_closure_sha256']
    tables=json.loads((MAN/'tables/manifest.json').read_text())
    figs=json.loads((MAN/'figures/manifest.json').read_text())
    assert set(tables)=={'T01','T02'}|{f'S{i:02}' for i in range(1,18)}
    assert set(figs)=={f'figure_{i:02}' for i in range(1,5)}|{f'figure_S{i:02}' for i in range(1,11)}
    for p in (MAN/'tables/tex').glob('*.tex'):
        assert not re.search(r'(?<!\\)%',p.read_text()),('Unescaped percent hides table text',p)
    input_count=0
    for info in list(tables.values())+list(figs.values()):
        for source in info['sources']:
            target=MAN/source['included']; assert sha(target)==source['sha256']
            assert len(rows(target))==source['rows']
            original=ROOT/source['source']
            if original.is_file():assert sha(original)==source['sha256'],source
            input_count+=1
    for key in figs:
        assert len(figs[key]['files'])==4
        assert figs[key]['size_inches'][0]<=7 and figs[key]['size_inches'][1]<=10
        for rel in figs[key]['files']:
            p=MAN/rel;assert 0<p.stat().st_size<10_000_000,p
            if p.suffix in ['.png','.tiff']:
                with Image.open(p) as im:
                    assert all(abs(v-300)<.1 for v in im.info['dpi']),p
    # Independent count checks on the saved classifications and corpus quotas.
    p=rows(MAN/'tables/data/S14/pair_summary.csv')
    assert len(p)==650
    totals=Counter((r['metric'],r['class']) for r in p)
    assert [totals['angle_p50',k] for k in ['unanimous','contradiction','unresolved']]==[42,262,21]
    assert [totals['pr',k] for k in ['unanimous','contradiction','unresolved']]==[54,221,50]
    assert figs['figure_S10']['displayed_values']['classification_counts']=={m+':'+c:n for (m,c),n in totals.items()}
    cells=rows(MAN/'tables/data/S01/field_period_counts.csv')
    assert len(cells)==130 and sum(int(r['base']) for r in cells)==400000
    assert sum(int(r['extra']) for r in cells)==100000
    assert all(int(r['base'])+int(r['extra'])==int(r['total']) for r in cells)
    st=rows(MAN/'tables/data/S12/selection_stability.csv')
    alerts={(m,k):sum(r['passes_both']!='True' for r in st if r['metric']==m and r['kind']==k)
            for m in ['angle_p50','pr','gap_25'] for k in ['half','external']}
    assert alerts['pr','half']==4 and alerts['gap_25','external']==51
    # Frozen model settings match the actual research configuration and bibliography.
    models=rows(MAN/'tables/data/S02/table2_models.csv')
    assert len(models)==10 and len({r['model'] for r in models})==10
    config=json.loads((ROOT/'config/embeddings_v1.json').read_text())['models']
    for r in models:
        original=next(m for m in config if m['key']==r['model'])
        for key in ['repo_id','revision','text_format']:
            assert r[key]==original[key],(r['model'],key)
        assert int(r['dimension'])==original['dimension']
        assert int(r['native_max_tokens'])==original['max_length']
        assert r['primary_pooling'] in original['poolings']
    assert sha(MAN/'references.bib')==sha(ROOT/'references/references.bib')
    documents={}
    for name, table_ids, figure_ids in [('main',['1','2'],[str(i) for i in range(1,5)]),
            ('supplement',['S'+str(i) for i in range(1,18)],['S'+str(i) for i in range(1,11)])]:
        p=ROOT/'output/pdf'/f'{name}.pdf'; d=PdfReader(p)
        text='\n'.join(page.extract_text() for page in d.pages)
        assert all(len(page.extract_text().strip())>60 for page in d.pages),'Empty page'
        assert '\ufffd' not in text,'Missing glyph'
        for label in table_ids:
            assert re.search(r'T\s*able\s+'+label+r'\s*:',text),('table',name,label)
        for label in figure_ids:
            assert re.search(r'Figure\s+'+label+r'\s*:',text),('figure',name,label)
        log=(p.with_suffix('.log')).read_text()
        forbidden=['Overfull','Missing character','undefined references','undefined citations','Citation `']
        assert not any(token in log for token in forbidden),(name,'LaTeX warning')
        assert '??' not in text
        if name=='supplement':assert '0.064' in text,'Stability width note must be visible'
        documents[name]={'pages':len(d.pages),'bytes':p.stat().st_size,'sha256':sha(p),
                         'tables':table_ids,'figures':figure_ids,'latex_warnings':False}
    result={'created_at':datetime.now(timezone.utc).isoformat(),'numeric_and_integrity_complete':True,
        'visual_review':'Separate page-by-page inspection required; see visual_review.json',
        'documents':documents,'main_tables':2,'supplementary_table_groups':17,'figures':14,
        'formats_per_figure':4,'source_attachments_verified':input_count,
        'previous_documents_preserved':len(baseline['documents']),
        'previous_report_files_unchanged':len(baseline['scientific_reports']),
        'original_pr_half_alerts':alerts['pr','half'],'connection_equal_size_alerts':alerts['gap_25','external'],
        'scientific_recomputation':False,'full_manuscript_prose_written':False,
        'publication_or_deposit':False}
    (EVID/'package_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
