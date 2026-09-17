"""Durable pages, transactional selection and final exports."""
import collections
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import sqlite3


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    with temp.open('wb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def write_json(path, value):
    atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'))


class Store:
    def __init__(self, root, config):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / 'raw').mkdir(exist_ok=True)
        self.db = sqlite3.connect(self.root / 'state.sqlite', timeout=30)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS blocks(
                id INTEGER PRIMARY KEY, cohort TEXT NOT NULL, field_id INTEGER, period_start INTEGER,
                seed INTEGER UNIQUE NOT NULL, sample_size INTEGER NOT NULL, status TEXT NOT NULL,
                n_pages INTEGER, sample_result_count INTEGER, created_at TEXT NOT NULL,
                applied_at TEXT, stats_json TEXT);
            CREATE TABLE IF NOT EXISTS pages(
                block_id INTEGER NOT NULL, page INTEGER NOT NULL, path TEXT NOT NULL,
                sha256 TEXT NOT NULL, n_records INTEGER NOT NULL, retrieved_at TEXT NOT NULL,
                PRIMARY KEY(block_id,page));
            CREATE TABLE IF NOT EXISTS works(
                work_id TEXT PRIMARY KEY, selection_order INTEGER UNIQUE NOT NULL,
                cohort TEXT NOT NULL, field_id INTEGER NOT NULL, period_start INTEGER NOT NULL,
                doi TEXT, text_sha256 TEXT NOT NULL, block_id INTEGER NOT NULL, record_json TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS works_cohort ON works(cohort);
            CREATE INDEX IF NOT EXISTS works_cell ON works(field_id,period_start);
            CREATE INDEX IF NOT EXISTS works_doi ON works(doi);
            CREATE INDEX IF NOT EXISTS works_text ON works(text_sha256);
            CREATE TABLE IF NOT EXISTS allocations(
                field_id INTEGER NOT NULL, period_start INTEGER NOT NULL,
                target INTEGER NOT NULL, exhausted INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY(field_id,period_start));
            CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY, at TEXT NOT NULL, kind TEXT NOT NULL, details TEXT NOT NULL);
        ''')
        existing = self.get_meta('config')
        if existing is not None and existing != config:
            self.db.close()
            raise ValueError('La configuración no coincide con esta descarga. No se ha cambiado la selección.')
        if existing is None:
            self.set_meta('config', config)
            self.set_meta('created_at', utcnow())
            write_json(self.root / 'config.json', config)

    def close(self):
        self.db.close()

    def get_meta(self, key, default=None):
        row = self.db.execute('SELECT value FROM meta WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else default

    def set_meta(self, key, value):
        with self.db:
            self.db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)', (key, json.dumps(value)))

    def event(self, kind, details):
        with self.db:
            self.db.execute('INSERT INTO events(at,kind,details) VALUES(?,?,?)',
                            (utcnow(), kind, json.dumps(details, ensure_ascii=False)))

    def counts(self):
        return dict(self.db.execute('SELECT cohort,count(*) FROM works GROUP BY cohort'))

    def cell_counts(self, config):
        counts = {(f,p): 0 for f in config['field_ids'] for p in config['period_starts']}
        for row in self.db.execute('SELECT field_id,period_start,count(*) n FROM works GROUP BY field_id,period_start'):
            counts[(row[0], row[1])] = row[2]
        return counts

    def page_path(self, block_id, page):
        return self.root / 'raw' / f'block_{block_id:06d}_page_{page:03d}.json.gz'

    def persist_page(self, block, page, params, response, fault):
        path = self.page_path(block['id'], page)
        envelope = dict(retrieved_at=utcnow(), parameters=params, response=response)
        raw = gzip.compress(json.dumps(envelope, ensure_ascii=False).encode('utf-8'), mtime=0)
        atomic_write(path, raw)
        fault('after_page_file')
        self.register_page(block, page, path, envelope)
        return envelope

    def register_page(self, block, page, path, envelope):
        raw = path.read_bytes()
        total = min(block['sample_size'], envelope['response']['meta']['count'])
        per_page = envelope['parameters']['per_page']
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO pages VALUES(?,?,?,?,?,?)',
                            (block['id'], page, str(path.relative_to(self.root)), hashlib.sha256(raw).hexdigest(),
                             len(envelope['response']['results']), envelope['retrieved_at']))
            self.db.execute('UPDATE blocks SET n_pages=?,sample_result_count=COALESCE(sample_result_count,?) WHERE id=?',
                            (max(1, (total + per_page - 1) // per_page), envelope['response']['meta']['count'], block['id']))

    def read_page(self, block_id, page):
        row = self.db.execute('SELECT * FROM pages WHERE block_id=? AND page=?', (block_id,page)).fetchone()
        path = self.page_path(block_id, page)
        if not path.exists():
            if row:
                raise ValueError('Falta una página que figuraba como guardada')
            return None
        raw = path.read_bytes()
        if row and hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('La copia de una página no supera la comprobación de integridad')
        return json.loads(gzip.decompress(raw))

    def export(self, config):
        import pyarrow as pa
        import pyarrow.parquet as pq
        counts = self.counts()
        if counts.get('base',0) != config['base_target'] or counts.get('extra',0) != config['extra_target']:
            raise ValueError('No se exporta como completo: faltan trabajos')
        if self.db.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
            raise ValueError('El archivo de estado no supera el control de integridad')
        if self.db.execute("SELECT 1 FROM blocks WHERE status!='applied' LIMIT 1").fetchone():
            raise ValueError('Hay un bloque sin terminar; no se marca el corpus como completo')
        # Validate every raw page, including blocks applied before an interruption.
        for page in self.db.execute('SELECT block_id,page FROM pages'):
            self.read_page(page[0], page[1])
        temp = self.root / 'corpus.parquet.tmp'
        writer = None
        schema = pa.schema([
            ('work_id',pa.string()),('doi',pa.string()),('title',pa.string()),('abstract',pa.string()),
            ('publication_year',pa.int32()),('publication_date',pa.string()),('type',pa.string()),('language',pa.string()),
            ('field_id',pa.int32()),('field_display_name',pa.string()),('period_start',pa.int32()),
            ('primary_topic_id',pa.string()),('primary_topic_display_name',pa.string()),
            ('primary_topic_json',pa.string()),('topics_json',pa.string()),
            ('abstract_word_count',pa.int32()),('title_word_count',pa.int32()),('abstract_50_79',pa.bool_()),
            ('text_sha256',pa.string()),('openalex_updated_date',pa.string()),('cited_by_count',pa.int64()),
            ('subfield_id',pa.string()),('subfield_display_name',pa.string()),('domain_id',pa.string()),('domain_display_name',pa.string()),
            ('cohort',pa.string()),('selection_order',pa.int64()),('source_block',pa.int32()),
            ('source_page',pa.int32()),('source_page_index',pa.int32()),('source_seed',pa.int64()),('retrieved_at',pa.string()),
            ('legacy_id_present',pa.bool_()),('legacy_text_match',pa.bool_()),
            ('duplicate_doi',pa.bool_()),('duplicate_text',pa.bool_())])
        doi_dups = {r[0] for r in self.db.execute('SELECT doi FROM works WHERE doi IS NOT NULL GROUP BY doi HAVING count(*)>1')}
        text_dups = {r[0] for r in self.db.execute('SELECT text_sha256 FROM works GROUP BY text_sha256 HAVING count(*)>1')}
        cursor = self.db.execute('SELECT record_json FROM works ORDER BY selection_order')
        total = 0
        from .records import WORDS, text_hash
        try:
            writer = pq.ParquetWriter(temp, schema, compression='zstd')
            while batch := cursor.fetchmany(10000):
                records = [json.loads(r[0]) for r in batch]
                for r in records:
                    if (r['selection_order'] != total + 1 or not r['title'].strip()
                        or len(WORDS.findall(r['abstract'])) != r['abstract_word_count']
                        or r['abstract_word_count'] < config['min_abstract_words']
                        or r['text_sha256'] != text_hash(r['title'], r['abstract'])
                        or r['field_id'] not in config['field_ids']
                        or r['period_start'] not in config['period_starts']
                        or not r['period_start'] <= r['publication_year'] <= r['period_start'] + 4
                        or r['language'] != 'en' or r['type'] not in ('article','review','conference-paper')):
                        raise ValueError('Un trabajo no supera la validación final de texto y selección')
                    r['duplicate_doi'] = r['doi'] in doi_dups
                    r['duplicate_text'] = r['text_sha256'] in text_dups
                    total += 1
                writer.write_table(pa.Table.from_pylist(records, schema=schema))
        finally:
            if writer:
                writer.close()
        with temp.open('rb') as handle:
            os.fsync(handle.fileno())
        os.replace(temp, self.root / 'corpus.parquet')
        if pq.ParquetFile(self.root/'corpus.parquet').metadata.num_rows != total:
            raise ValueError('El Parquet exportado no tiene el número esperado de filas')
        with (self.root/'field_year_counts.csv').open('w', newline='') as f:
            w = csv.writer(f);w.writerow(['field_id','publication_year','cohort','n'])
            w.writerows(self.db.execute("SELECT field_id,json_extract(record_json,'$.publication_year'),cohort,count(*) FROM works GROUP BY 1,2,3 ORDER BY 1,2,3"))
        with (self.root/'field_period_counts.csv').open('w', newline='') as f:
            w=csv.writer(f);w.writerow(['field_id','period_start','cohort','n'])
            w.writerows(self.db.execute('SELECT field_id,period_start,cohort,count(*) FROM works GROUP BY 1,2,3 ORDER BY 1,2,3'))
        with (self.root/'corpus.parquet').open('rb') as handle:
            parquet_sha256 = hashlib.file_digest(handle, 'sha256').hexdigest()
        validation = dict(status='passed',rows=total,counts=counts,unique_work_ids=total,
                          duplicate_doi_groups=len(doi_dups),duplicate_text_groups=len(text_dups),
                          checks=['sqlite_integrity','raw_page_checksums','exact_cohort_sizes','unique_work_ids',
                                  'selection_order','text_hashes','text_lengths','field_period_year','parquet_rows'],
                          completed_at=utcnow(),parquet_sha256=parquet_sha256)
        write_json(self.root/'validation.json', validation)
        self.set_meta('complete', validation)
        return validation
