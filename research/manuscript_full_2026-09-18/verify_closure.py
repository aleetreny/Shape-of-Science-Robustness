"""Tie the editorial checks to the exact delivered files; no scientific execution."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    names = ['package_audit', 'portable_source_audit', 'numeric_claim_audit',
             'citation_validation', 'word_count', 'visual_review']
    records = {name: json.loads((EVIDENCE / f'{name}.json').read_text()) for name in names}
    package = records['package_audit']
    portable = records['portable_source_audit']
    visual = records['visual_review']
    assert package['numeric_and_integrity_complete']
    assert package['source_attachments_verified'] == 98
    assert package['previous_report_files_unchanged'] == 150
    assert package['previous_documents_preserved'] == 20
    assert records['numeric_claim_audit']['verified']
    assert records['word_count']['body_words'] == 4383
    assert records['word_count']['abstract_words'] == 190
    citations = records['citation_validation']
    assert citations['total_entries'] == citations['valid_entries'] == 26
    assert not citations['errors'] and not citations['warnings'] and not citations['duplicates']
    assert not citations['manuscript_results']['missing_keys']
    assert portable['compiled_from_extracted_sources'] and portable['extracted_files_match']
    assert portable['files'] == 184 and sha(ROOT / portable['package']) == portable['sha256']
    assert not visual['unresolved_clipping_or_missing_content']
    for name, expected_pages in [('main', 19), ('supplement', 33)]:
        actual = ROOT / 'output/pdf' / f'{name}.pdf'
        fingerprint = sha(actual)
        for audit in [package, portable, visual]:
            assert audit['documents'][name]['sha256'] == fingerprint, (name, 'stale check')
        pages = visual['documents'][name]['pages']
        assert [page['page'] for page in pages] == list(range(1, expected_pages + 1))
        assert package['documents'][name]['pages'] == expected_pages
        assert portable['documents'][name]['identical_extracted_text']
        for page in pages:
            assert sha(ROOT / page['render']) == page['render_sha256']
        source = (ROOT / 'manuscript' / f'{name}.tex').read_text()
        assert not re.search(r'Writing plan|\\placeholder\b|TODO|TBD', source)
        assert 'Alejandro Treny Ortega' in source and 'Independent researcher' in source
    assert len(visual['figures']) == 14
    for name, item in visual['figures'].items():
        assert item['full_figure_inspected']
        assert sha(ROOT / 'manuscript/figures' / f'{name}.png') == item['sha256']
    prose = (ROOT / 'manuscript/main.tex').read_text()
    assert 'no competing interests' in prose and 'no external funding' in prose
    assert 'OpenAI Codex assisted' in prose
    # All currently cited keys remain covered after layout edits.
    keys = set()
    for file in (ROOT / 'manuscript').rglob('*.tex'):
        for group in re.findall(r'\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]+)\}', file.read_text()):
            keys.update(key.strip() for key in group.split(','))
    assert keys == set(citations['manuscript_results']['cited_keys'])
    # Current entry documents must resolve their local links.
    current_docs = ['MANUSCRIPT_REVIEW.md', 'MANUSCRIPT_LAYOUT.md', 'NEXT_STEPS.md',
                    'manuscript/README.md', 'docs/INDEX.md', 'docs/QSS_CHECK.md']
    links = 0
    for relative in current_docs:
        path = ROOT / relative
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            target = raw.strip('<>')
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                continue
            target = unquote(target.split('#', 1)[0])
            destination = (path.parent / target).resolve()
            # The document links to this audit, written only after checks pass.
            assert destination.exists() or destination == EVIDENCE / 'closure_audit.json', (relative, target)
            links += 1
    plan = (ROOT / 'task_plan.md').read_text().split('\n---\n', 1)[0]
    assert '**pending**' not in plan and '**in_progress**' not in plan
    evidence = {name: sha(EVIDENCE / f'{name}.json') for name in names}
    result = {
        'created_at': datetime.now(timezone.utc).isoformat(),
        'status': 'complete_as_author_review_draft',
        'author_personal_approval': False,
        'scientific_recomputation': False,
        'commit_push_deposit_or_submission': False,
        'body_words': 4383, 'abstract_words': 190,
        'pages_main': 19, 'pages_supplement': 33,
        'all_52_pages_and_14_figures_visually_reviewed': True,
        'cited_references_verified': 26,
        'source_attachments_verified': 98,
        'portable_files': 184, 'portable_pdf_bytes_identical': True,
        'local_links_verified': links,
        'evidence_sha256': evidence,
        'current_document_sha256': {p: sha(ROOT / p) for p in current_docs},
        'remaining_before_submission': [
            'Author reads and approves prose and interpretations',
            'Correspondence details', 'Authorised persistent material deposit and licence',
            'Current QSS requirements and final reference style'
        ]
    }
    (EVIDENCE / 'closure_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
