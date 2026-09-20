"""Check that the Spanish review copy preserves the English evidence and structure."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import re

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = Path(__file__).resolve().parent
EN = ROOT / 'manuscript'
ES = ROOT / 'manuscript_es'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def numbers(text, spanish=False):
    text = re.sub(r'\\(?:nolinkurl|seqsplit|url|cite[pt]?|label|ref|input)\{[^}]*\}', '', text)
    # Equations are checked separately, exactly, so their comma-separated sets
    # must not be mistaken for locale-specific numeric tokens.
    text = re.sub(r'(?<!\\)\$.+?(?<!\\)\$|\\\[.+?\\\]|\\begin\{align\*\}.+?\\end\{align\*\}', '', text, flags=re.S)
    text = text.replace('{,}', ',').replace('{.}', '.').replace('--', ' ')
    found = []
    for match in re.finditer(r'(?<![\w])[-−]?\d+(?:[.,]\d+)*(?:k\b)?', text):
        token = match.group().replace('−', '-')
        multiplier = 1000 if token.endswith('k') else 1
        token = token.removesuffix('k')
        if spanish:
            token = token.replace('.', '').replace(',', '.')
        else:
            token = token.replace(',', '')
        found.append(str(Decimal(token) * multiplier))
    return found


def body(text):
    return text.split(r'\begin{document}', 1)[1].split(r'\bibliographystyle', 1)[0]


def equations(text):
    blocks = re.findall(r'(?<!\\)\$(.+?)(?<!\\)\$|\\\[(.+?)\\\]|\\begin\{align\*\}(.+?)\\end\{align\*\}', text, re.S)
    return [re.sub(r'\s+', '', next(v for v in group if v)).replace('{,}', '.') for group in blocks]


def run():
    baseline = json.loads((EVIDENCE / 'baseline_manifest.json').read_text())
    for name, digest in baseline['english_originals'].items():
        assert sha(ROOT / name) == digest, ('English original changed', name)

    documents = {}
    for name, table_ids, figure_ids in [
        ('main', ['1', '2'], [str(i) for i in range(1, 5)]),
        ('supplement', ['S'+str(i) for i in range(1, 18)], ['S'+str(i) for i in range(1, 11)]),
    ]:
        en = (EN / f'{name}.tex').read_text()
        es = (ES / f'{name}.tex').read_text()
        for command in ('citep', 'citet', 'label', 'ref', 'input'):
            pattern = r'\\' + command + r'\{([^}]*)\}'
            assert re.findall(pattern, en) == re.findall(pattern, es), (name, command)
        for level in ('section', 'subsection'):
            pattern = r'\\' + level + r'\{'
            assert len(re.findall(pattern, en)) == len(re.findall(pattern, es)), (name, level)
        assert equations(en) == equations(es), (name, 'equations')
        a, b = Counter(numbers(body(en))), Counter(numbers(body(es), True))
        assert a == b, (name, 'numbers', a-b, b-a)
        pdf = ROOT / 'output/pdf/es' / f'{name}.pdf'
        reader = PdfReader(pdf)
        texts = [p.extract_text() for p in reader.pages]
        all_text = '\n'.join(texts)
        assert all(len(t.strip()) > 60 for t in texts), (name, 'empty page')
        assert all(c not in all_text for c in ('\ufffd', '£', '??')), (name, 'glyph or reference')
        assert '¿Qué conclusiones' in all_text, (name, 'inverted question mark')
        for label in table_ids:
            assert re.search(r'T\s*abla\s+' + label + r'\s*:', all_text), (name, 'table', label)
        for label in figure_ids:
            assert re.search(r'Figura\s+' + label + r'\s*:', all_text), (name, 'figure', label)
        log = pdf.with_suffix('.log').read_text()
        for token in ('Overfull', 'Missing character', 'undefined references', 'undefined citations', 'Citation `'):
            assert token not in log, (name, token)
        documents[name] = {
            'path': str(pdf.relative_to(ROOT)), 'pages': len(reader.pages), 'sha256': sha(pdf),
            'citations_references_and_inputs_same_order': True, 'equations_identical': True,
            'numeric_occurrences_identical_after_localization': True,
            'all_tables_and_figures_present': True, 'no_overflow_missing_glyphs_or_unresolved_references': True,
        }

    table_count = 0
    for path in sorted((EN / 'tables/tex').glob('*.tex')):
        es_path = ES / 'tables/tex' / path.name
        en_rows = [row for row in path.read_text().splitlines() if '&' in row]
        es_rows = [row for row in es_path.read_text().splitlines() if '&' in row]
        assert len(en_rows) == len(es_rows), path.name
        for i, (a, b) in enumerate(zip(en_rows, es_rows)):
            assert numbers(a) == numbers(b, True), (path.name, i, numbers(a), numbers(b, True))
        def table_content(p):
            return '\n'.join(line for line in p.read_text().splitlines()
                             if line and not line.startswith('%') and
                             (not line.startswith('\\') or line.startswith((r'\item', r'\captionof'))))
        assert Counter(numbers(table_content(path))) == Counter(numbers(table_content(es_path), True)), (path.name, 'captions and notes')
        assert not re.search(r'(?<!\\)%', es_path.read_text()), path.name
        table_count += 1

    csv_files = list(EN.rglob('*.csv'))
    for path in csv_files:
        assert sha(path) == sha(ES / path.relative_to(EN)), path
    for relative in ('references.bib', 'context_references.bib', 'tables/manifest.json', 'figures/manifest.json'):
        assert sha(EN / relative) == sha(ES / relative), relative
    figures = json.loads((ES / 'figures/manifest.json').read_text())
    assert len(figures) == 14 and table_count == 19 and len(csv_files) == 98
    result = {
        'created_at': datetime.now(timezone.utc).isoformat(),
        'scope': 'Full Spanish translation for author review; English remains canonical.',
        'english_original_files_preserved': len(baseline['english_originals']),
        'documents': documents, 'table_groups_checked_row_by_row': table_count,
        'table_caption_and_note_numbers_preserved': True,
        'figures_with_identical_source_and_value_manifests': len(figures),
        'unchanged_csv_attachments': len(csv_files), 'unchanged_bibliographies': True,
        'new_scientific_computation': False, 'publication_or_submission': False,
        'linguistic_review': 'Full prose, captions and notes translated; bibliography and original example titles retained for identification.',
        'visual_review': 'Recorded separately in visual_review.json after rendering final PDFs.',
    }
    (EVIDENCE / 'translation_audit.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    run()
