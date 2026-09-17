"""Bounded direct-identifier check using citation-management's metadata/BibTeX parser.
Raw responses are cached; this is not a relevance review or a systematic search.
"""
import hashlib
import json
import sys
import time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path.home() / '.codex/skills/citation-management/scripts'))
from extract_metadata import MetadataExtractor


class RecordingSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.last_data = None
        self.last_url = None

    def get(self, url, **kwargs):
        if url == 'http://export.arxiv.org/api/query':
            url = 'https://export.arxiv.org/api/query'
        prepared = requests.Request('GET', url, params=kwargs.get('params')).prepare().url
        key = hashlib.sha256(prepared.encode()).hexdigest()
        raw = HERE / 'reference_raw' / (key + '.response')
        raw.parent.mkdir(exist_ok=True)
        meta_path = raw.with_suffix('.json')
        if raw.exists():
            record = json.loads(meta_path.read_text())
            response = requests.Response()
            response.status_code = record['status_code']
            response._content = raw.read_bytes()
            response.url = prepared
        else:
            if 'arxiv.org' in url:
                time.sleep(3.1)
            response = super().get(url, **kwargs)
            raw.write_bytes(response.content)
            meta_path.write_text(json.dumps({'url': prepared, 'status_code': response.status_code,
                'retrieved_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, indent=2))
        self.last_url = prepared
        self.last_data = response
        return response


def main():
    candidates = json.loads((HERE / 'reference_candidates.json').read_text())
    extra_dois = ['10.1007/s41109-026-00830-2', '10.18653/v1/2022.findings-acl.249',
                  '10.18653/v1/D19-1371', '10.18653/v1/N19-1423', '10.1093/bioinformatics/btz682',
                  '10.1145/3458754', '10.1038/s41598-026-48795-7']
    for d in extra_dois:
        candidates.setdefault('doi:' + d, ['prepaper review'])
    for a in ['2408.00531', '2110.14739']:
        candidates.setdefault('arxiv:' + a, ['original metrics bibliography'])
    candidates.pop('doi:10.48550/arxiv.2609.00065', None)  # Same arXiv record, DataCite rather than Crossref.
    extractor = MetadataExtractor()
    session = RecordingSession()
    extractor.session = session
    records, bib = [], []
    for ident, origins in candidates.items():
        kind, value = ident.split(':', 1)
        metadata = extractor.extract_from_doi(value) if kind == 'doi' else extractor.extract_from_arxiv(value)
        record = {'identifier': ident, 'origins': origins, 'metadata': metadata, 'request_url': session.last_url,
                  'status_code': session.last_data.status_code, 'verified': False}
        if metadata:
            assert metadata['title'] and metadata['authors'] and metadata['year'], ident
            if kind == 'doi':
                payload = session.last_data.json()
                assert payload['status'] == 'ok' and payload['message-type'] == 'work'
                message = payload['message']
                assert message['DOI'].lower() == value.lower()
                if message.get('article-number') and not metadata.get('pages'):
                    metadata['pages'] = str(message['article-number'])
                    record['locator_kind'] = 'article number (publisher field), not page range'
                record['publisher_dates'] = {k: message.get(k) for k in ['published', 'published-online', 'published-print', 'created']}
            else:
                # Preserve the exact currently returned version independently of the stable citation URL.
                import xml.etree.ElementTree as ET
                root = ET.fromstring(session.last_data.content)
                ns = {'a': 'http://www.w3.org/2005/Atom'}
                record['current_version_url'] = root.findtext('a:entry/a:id', '', ns)
                record['updated'] = root.findtext('a:entry/a:updated', '', ns)
            record['verified'] = True
            record['citation_key'] = 'ref' + hashlib.sha256(ident.encode()).hexdigest()[:10]
            record['historical_wrong_attribution'] = value.lower() == '10.1162/qss_a_00168'
            if not record['historical_wrong_attribution']:
                bib.append(extractor.metadata_to_bibtex(metadata, record['citation_key']))
            print('VERIFIED', ident, metadata['title'], flush=True)
        else:
            print('UNRESOLVED', ident, flush=True)
        records.append(record)
        (HERE / 'reference_verification.json').write_text(json.dumps(records, indent=2, ensure_ascii=False))
    target = ROOT / 'references'
    target.mkdir(exist_ok=True)
    (target / 'verified_api.bib').write_text('\n\n'.join(bib) + '\n')
    print('FINISHED', len(records), sum(r['verified'] for r in records), flush=True)


if __name__ == '__main__':
    main()
