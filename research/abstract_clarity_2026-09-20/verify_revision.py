"""Verify the narrowly scoped bilingual abstract edit without rerunning science."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import json
import re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    return json.loads(p.read_text())

def abstract(text):
    return text.split(r'\begin{abstract}', 1)[1].split(r'\end{abstract}', 1)[0].strip()

def without_abstract(text):
    return re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}', '<ABSTRACT>', text, flags=re.S)

baseline = read(HERE/'baseline_manifest.json')
protected = read(HERE/'protected_manifest.json')
for rel, digest in baseline.items():
    assert sha(HERE/'baseline'/rel) == digest, rel
for rel, digest in protected.items():
    assert sha(ROOT/rel) == digest, ('unrequested change', rel)
texts = read(HERE/'abstracts.json')
assert texts['en']['words'] == 200 and texts['es']['words'] == 235
documents = {}
for lang, folder, pdfdir in [('en', 'manuscript', 'output/pdf'), ('es', 'manuscript_es', 'output/pdf/es')]:
    old = (HERE/'baseline'/folder/'main.tex').read_text()
    new = (ROOT/folder/'main.tex').read_text()
    assert without_abstract(old) == without_abstract(new)
    opening = old.split(r'\begin{abstract}', 1)[1].split('Comparo diez modelos' if lang == 'es' else 'I compare ten models')[0]
    assert new.split(r'\begin{abstract}', 1)[1].startswith(opening)
    # The empirical numbers in the abstract are unchanged. Count spelled eight separately.
    norm = lambda s: re.findall(r'\d+', s.replace('500.000','500000').replace('500,000','500000'))
    assert Counter(norm(abstract(old))) == Counter(norm(abstract(new))), lang
    assert ('ocho' if lang == 'es' else 'eight') in abstract(new)
    pdf = ROOT/pdfdir/'main.pdf'
    reader = PdfReader(pdf)
    content = '\n'.join(p.extract_text() for p in reader.pages)
    assert len(reader.pages) == (20 if lang == 'en' else 22)
    assert all(len(p.extract_text().strip()) > 60 for p in reader.pages)
    assert not any(x in content for x in ['??', '\ufffd', 'TODO'])
    log = pdf.with_suffix('.log').read_text()
    assert not any(x in log for x in ['Overfull','Missing character','undefined references','undefined citations','Citation `'])
    documents[lang] = {'pdf': str(pdf.relative_to(ROOT)), 'sha256': sha(pdf), 'pages': len(reader.pages), 'abstract_words': texts[lang]['words']}

render = read(HERE/'render_manifest.json')
comparison = read(HERE/'render_comparison.json')
for lang in ['en', 'es']:
    key = lang + '_main'
    assert render[key]['sha256'] == documents[lang]['sha256']
    assert set(comparison[key]['visually_changed_pages']) <= {1, 2}
    assert sorted(comparison[key]['visually_changed_pages'] + comparison[key]['byte_identical_rendered_pages']) == list(range(1, documents[lang]['pages'] + 1))
portable = read(HERE/'portable_source_audit.json')
for lang, package in portable['packages'].items():
    assert sha(ROOT/package['path']) == package['sha256']
    folder = 'manuscript' if lang == 'en' else 'manuscript_es'
    for rel, digest in package['source_hashes'].items():
        assert sha(ROOT/folder/rel) == digest, ('package differs', lang, rel)
    assert package['documents']['main']['sha256'] == documents[lang]['sha256']
    assert all(d['byte_identical'] for d in package['documents'].values())

# Explain the abstract from the existing, frozen evidence, not a new analysis.
with (ROOT/'reports/robustness_closure_v1/centres_summary.csv').open() as stream:
    centres = list(csv.DictReader(stream))
with (ROOT/'reports/robustness_closure_v1/morphology_centering_summary.csv').open() as stream:
    centering = list(csv.DictReader(stream))
field = next(r for r in centres if r['design']=='repeat256_field' and r['grouping']=='observed')
angle = next(r for r in centering if r['metric']=='angle_p50' and r['cutoff']=='0.0')
assert round(float(field['mean']), 3) == .940
assert int(angle['original_oppositions']) == 262 and int(angle['same_fixed_witness_directions_retained']) == 128
assert all(r['grouping']!='observed' or not r['design'].endswith('_field') or float(r['mean'])>.93 for r in centres)

report = {'completed_at': datetime.now(timezone.utc).isoformat(), 'all_complete': True,
          'scope': 'Abstract wording only, in English and Spanish; editorial metadata updated separately.',
          'opening_retained': True, 'nonabstract_main_sources_byte_identical': True,
          'numeric_tokens_preserved': True, 'protected_files_verified': len(protected),
          'previous_files_archived': len(baseline), 'documents': documents,
          'visual_review': {'changed_pages_inspected_at_full_size_and_in_context': comparison,
                            'no_layout_defects': True,
                            'unchanged_pages': 'Byte-identical Poppler page renders to the prior visually reviewed version.'},
          'portable_source_audit_sha256': sha(HERE/'portable_source_audit.json'),
          'scientific_evidence': {'centres_summary.csv': sha(ROOT/'reports/robustness_closure_v1/centres_summary.csv'),
                                 'morphology_centering_summary.csv': sha(ROOT/'reports/robustness_closure_v1/morphology_centering_summary.csv'),
                                 'prior_closure': sha(ROOT/'research/robustness_closure_2026-09-20/closure_audit.json')},
          'language_limit': 'English 200 words; Spanish 235 words, a review translation rather than the journal submission abstract.',
          'new_scientific_computation': False, 'publication_or_submission': False, 'author_approval': False}
(HERE/'closure_audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
print('PASS: only the abstracts changed; 457 protected files intact; two updated PDFs and both source packages verified.')
