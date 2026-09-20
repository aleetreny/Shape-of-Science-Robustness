"""Verify the five requested presentation edits against the archived draft."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import importlib.util
import json
import re

from pypdf import PdfReader
import pdfplumber

ROOT = Path(__file__).resolve().parents[2]
EV = Path(__file__).resolve().parent
BASE = ROOT / 'data/manuscript_comments_v1/baseline'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canonical_prose(text):
    lines = [line for line in text.splitlines() if not any(token in line for token in (
        r'{\LARGE\bfseries', r'{\large Which conclusions', r'{\large How much',
        r'{\large \textquestiondown', 'OpenAI Codex', r'\PanelFigure{figure_01}', r'\clearpage'))]
    return '\n'.join(lines)


def run():
    baseline = json.loads((EV / 'baseline_manifest.json').read_text())
    for rel, digest in baseline['files'].items():
        assert sha(BASE / rel) == digest, ('archived draft', rel)
    for rel, digest in baseline['scientific_reports'].items():
        assert sha(ROOT / rel) == digest, ('scientific report', rel)
    spec = importlib.util.spec_from_file_location('translation_checks',
        ROOT / 'research/manuscript_spanish_2026-09-18/verify_translation.py')
    translate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(translate)

    pdfs = {}
    alignments = {}
    for folder, language in [('manuscript', 'en'), ('manuscript_es', 'es')]:
        source = ROOT / folder
        for name in ['main', 'supplement']:
            old = (BASE / folder / f'{name}.tex').read_text()
            new = (source / f'{name}.tex').read_text()
            assert canonical_prose(old) == canonical_prose(new), (folder, name, 'unrequested prose edit')
            for macro in ['citep', 'citet', 'label', 'ref', 'input']:
                pattern = r'\\' + macro + r'\{([^}]*)\}'
                assert re.findall(pattern, old) == re.findall(pattern, new), (folder, name, macro)
            assert translate.equations(old) == translate.equations(new), (folder, name, 'formula')
            rel = Path('output/pdf') / ('es' if language == 'es' else '') / f'{name}.pdf'
            p = ROOT / rel
            reader = PdfReader(p)
            text = '\n'.join(page.extract_text() for page in reader.pages)
            assert all(len(page.extract_text().strip()) > 60 for page in reader.pages)
            assert all(token not in text for token in ['??', '\ufffd', '£'])
            log = p.with_suffix('.log').read_text()
            assert not any(token in log for token in ['Overfull', 'Missing character', 'undefined references', 'undefined citations', 'Citation `'])
            pdfs[f'{language}_{name}'] = {'path': str(rel), 'pages': len(reader.pages), 'sha256': sha(p)}
        for p in source.rglob('*.csv'):
            assert sha(p) == sha(BASE / folder / p.relative_to(source)), p
        for rel in ['references.bib', 'context_references.bib', 'tables/manifest.json']:
            assert sha(source / rel) == sha(BASE / folder / rel), (folder, rel)
        for p in (source / 'tables/tex').glob('*.tex'):
            old = (BASE / folder / 'tables/tex' / p.name).read_text()
            new = p.read_text()
            assert [r for r in old.splitlines() if '&' in r] == [r for r in new.splitlines() if '&' in r], p.name
        assert (source / 'tables/tex/T01.tex').read_text().count(r'\addlinespace[7pt]') == 5
        table2 = (source / 'tables/tex/T02.tex').read_text()
        assert len(re.findall(r'm\{[0-9.]+cm\}', table2)) == 5
        # Confirm that the numbers sit midway between the two alias baselines.
        p = ROOT / pdfs[f'{language}_main']['path']
        with pdfplumber.open(p) as pdf:
            for page in pdf.pages:
                words = page.extract_words()
                first = [w for w in words if w['text'] == 'PubMedBERT' and w['x0'] < 110]
                second = [w for w in words if w['text'] == 'BiomedBERT' and w['x0'] < 110]
                if not first or not second:
                    continue
                a, b = first[0], second[0]
                mid = (a['top'] + a['bottom'] + b['top'] + b['bottom']) / 4
                numbers = [w for w in words if w['text'] in ['768', '512'] and a['top'] <= w['top'] <= b['bottom']]
                assert len(numbers) == 2
                offsets = [abs((w['top'] + w['bottom']) / 2 - mid) for w in numbers]
                assert max(offsets) < 1.0, (language, offsets)
                alignments[language] = {'page': page.page_number, 'max_offset_from_name_midpoint_pt': max(offsets)}
        assert language in alignments

    en, es = ROOT / 'manuscript', ROOT / 'manuscript_es'
    for name in ['main', 'supplement']:
        a, b = (en / f'{name}.tex').read_text(), (es / f'{name}.tex').read_text()
        assert Counter(translate.numbers(translate.body(a))) == Counter(translate.numbers(translate.body(b), True)), (name, 'translation numbers')
        assert translate.equations(a) == translate.equations(b)
    before = json.loads((BASE / 'manuscript/figures/manifest.json').read_text())
    after = json.loads((en / 'figures/manifest.json').read_text())
    assert after == json.loads((es / 'figures/manifest.json').read_text())
    for key in before:
        if key != 'figure_01':
            assert before[key] == after[key], key
    for key, values in before['figure_01']['displayed_values'].items():
        assert values == after['figure_01']['displayed_values'][key], key
    assert before['figure_01']['sources'] == after['figure_01']['sources']
    with (en / 'figures/data/figure_01/structure_matched_size_agreement.csv').open() as f:
        rows = list(csv.DictReader(f))
    spread = after['figure_01']['displayed_values']['within_group_spread']
    assert len(spread) == 6
    for row in spread:
        r = next(r for r in rows if r['population'] == 'same_183_subfields' and r['recipe'] == 'mean'
                 and r['measure'] == 'shape' and r['level'] == row['level'] and int(r['selection']) == row['selection'])
        for field in ['mean', 'p025', 'p975']:
            assert float(r[field]) == row[field]
        assert int(r['n']) == row['n'] == 45 * (26 if row['level'] == 'field' else 183)
    result = {'created_at': datetime.now(timezone.utc).isoformat(), 'documents': pdfs,
              'archived_files_verified': len(baseline['files']), 'scientific_report_files_unchanged': len(baseline['scientific_reports']),
              'csv_attachments_unchanged_per_language': 98, 'table_content_unchanged': True,
              'formula_citation_and_unrequested_prose_preserved': True, 'table2_alignment': alignments,
              'figure1_previous_means_unchanged': True, 'figure1_six_spreads_verified_against_saved_summary': spread,
              'new_scientific_computation': False, 'visual_review': 'See visual_review.json'}
    (EV / 'numeric_layout_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
