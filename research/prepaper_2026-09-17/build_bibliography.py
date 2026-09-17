"""Canonical bibliography: use editorial exports, preserve API evidence and corrections."""
import hashlib
import html
import json
import re
import sys
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(Path.home() / '.codex/skills/citation-management/scripts'))
from _common import parse_bibtex, render_entry
from extract_metadata import MetadataExtractor


def get(url, name):
    path = HERE / 'reference_raw' / name
    if path.exists() and path.suffix != '.failed':
        return path.read_text()
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    path.write_text(r.text)
    return r.text


def main():
    records = json.loads((HERE / 'reference_verification.json').read_text())
    records += json.loads((HERE / 'reference_supplement.json').read_text())
    ex = MetadataExtractor()
    entries, corrections, index = [], [], []
    superseded = {'arxiv:2308.15706': 'doi:10.1162/qss_a_00349',
                  'arxiv:2512.13054': 'doi:10.1016/j.ipm.2025.104557',
                  'arxiv:2408.00531': 'ICLR 2025', 'arxiv:2108.01661': 'NeurIPS 2021',
                  'arxiv:2110.14739': 'NeurIPS 2021'}
    for r in records:
        identifier = r['identifier']
        if identifier in superseded or r.get('historical_wrong_attribution'):
            index.append({'identifier': identifier, 'status': 'use published version' if identifier in superseded else 'excluded: unrelated historical DOI',
                          'use_instead': superseded.get(identifier, 'Lamers ISSI 2021'), 'title': r['metadata']['title']})
            continue
        m = r['metadata']
        key = r.get('citation_key') or 'ref' + hashlib.sha256(identifier.encode()).hexdigest()[:10]
        entry = parse_bibtex(ex.metadata_to_bibtex(m, key))[0]
        source = r['request_url']
        if identifier.startswith('doi:10.18653/v1/'):
            acl = identifier.split('v1/', 1)[1]
            source = 'https://aclanthology.org/' + acl + '.bib'
            official = parse_bibtex(get(source, acl + '.bib'))
            assert len(official) == 1
            for name in ['pages', 'year', 'title', 'author']:
                before, after = entry['fields'].get(name, ''), official[0]['fields'].get(name, '')
                if re.sub(r'\s+', ' ', before).replace('--', '-') != re.sub(r'\s+', ' ', after).replace('--', '-'):
                    corrections.append({'identifier': identifier, 'field': name, 'api': before, 'editorial': after, 'source': source})
            entry = official[0]
        entry['fields'].pop('abstract', None)
        entry['fields'] = {k: html.unescape(v) for k, v in entry['fields'].items()}
        entries.append(entry)
        index.append({'identifier': identifier, 'citation_key': entry['key'], 'title': html.unescape(m['title']),
                      'status': 'verified metadata; content-review depth in RELATED_WORK.md', 'source': source})
    for stem in ['ding2021', 'williams2021']:
        entry = parse_bibtex((HERE / 'reference_raw' / (stem + '.bib')).read_text())[0]
        entries.append(entry)
        index.append({'identifier': stem, 'citation_key': entry['key'], 'title': entry['fields']['title'], 'status': 'editorial BibTeX', 'source': entry['fields']['url']})
    for slug in ['v97/kornblith19a', 'v285/williams24a']:
        source = 'https://proceedings.mlr.press/' + slug + '.html'
        page = get(source, slug.replace('/', '_') + '.html')
        match = re.search(r'<code[^>]*id="bibtex"[^>]*>(.*?)</code>', page, re.S)
        if not match:
            match = re.search(r'(<pre[^>]*>.*?@InProceedings.*?</pre>)', page, re.S)
        assert match, source
        bib = html.unescape(re.sub('<[^>]+>', '', match.group(1)))
        parsed = parse_bibtex(bib)
        assert len(parsed) == 1, source
        entry = parsed[0]
        entry['fields'].pop('abstract', None)
        entries.append(entry)
        index.append({'identifier': slug, 'citation_key': entry['key'], 'title': entry['fields']['title'], 'status': 'editorial BibTeX in official HTML', 'source': source})
    # Existing ReSi entry was checked against ICLR's official current record this turn.
    entry = next(e for e in parse_bibtex((ROOT / 'research/analysis_2026-09-17/references_analysis.bib').read_text()) if e['key'] == 'klabunde2025')
    entries.append(entry)
    index.append({'identifier': 'ICLR ReSi 2025', 'citation_key': entry['key'], 'title': entry['fields']['title'], 'status': 'official proceedings verified', 'source': entry['fields']['url']})
    # No DOI found for this proceedings paper; bibliographic fields come from the inspected official book.
    fields = {'author': 'Lamers, Wout S. and van Eck, Nees Jan and Colavizza, Giovanni',
        'title': 'An appraisal of publication embedding techniques in the context of conventional bibliometric relatedness measures',
        'booktitle': 'Proceedings of the 18th International Conference on Scientometrics and Informetrics',
        'year': '2021', 'pages': '633--638', 'url': 'https://www.issi-society.org/proceedings/issi_2021/Proceedings%20ISSI%202021.pdf',
        'note': 'No DOI located. Official proceedings pp. 633--638; visible PDF pages 665--670 checked.'}
    entries.append({'type': 'inproceedings', 'key': 'lamers2021appraisal', 'fields': fields})
    index.append({'identifier': 'ISSI Lamers 2021', 'citation_key': 'lamers2021appraisal', 'title': fields['title'], 'status': 'official full text; no DOI located', 'source': fields['url']})
    assert len({e['key'] for e in entries}) == len(entries)
    target = ROOT / 'references'
    (target / 'references.bib').write_text('\n\n'.join(render_entry(e['type'], e['key'], e['fields']) for e in entries) + '\n')
    (target / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2))
    (HERE / 'reference_editorial_corrections.json').write_text(json.dumps(corrections, ensure_ascii=False, indent=2))
    print('Canonical entries:', len(entries), 'editorial field changes:', len(corrections))


if __name__ == '__main__':
    main()
