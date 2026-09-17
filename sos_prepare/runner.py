"""Replay saved random blocks under common quality rules; fetch only deficits."""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import random
import sqlite3

from sos_download.records import normalize_work
from sos_download.runner import Runner, PageDrift
from sos_download.store import utcnow, write_json
from .quality import reasons_for


def readonly(path):
    db = sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA query_only=ON')
    return db


class CleanRunner(Runner):
    def __init__(self, root, config, api, quality, source, **kwargs):
        if Path(root).resolve() == Path(source).resolve():
            raise ValueError('Clean output must never be the original download')
        super().__init__(root,config,api,**kwargs)
        self.quality = quality
        self.source = Path(source).resolve()
        if self.store.root.resolve() == self.source:
            raise ValueError('Clean output must never be the original download')
        self.store.db.executescript('''
            CREATE TABLE IF NOT EXISTS origins(block_id INTEGER PRIMARY KEY, origin TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS processed_blocks(sequence INTEGER PRIMARY KEY, block_id INTEGER UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS decisions(block_id INTEGER, candidate_rank INTEGER, work_id TEXT,
                text_sha256 TEXT, outcome TEXT NOT NULL, reasons TEXT NOT NULL,
                PRIMARY KEY(block_id,candidate_rank));
            CREATE INDEX IF NOT EXISTS decision_id ON decisions(work_id);
        ''')
        self.bind_identity()
        self.import_original()

    def bind_identity(self):
        repo = Path(__file__).resolve().parents[1]
        identity = dict(policy=self.quality.policy,model_sha256=self.quality.model_sha,
                        source=str(self.source),source_validation=json.loads((self.source/'validation.json').read_text()),
                        source_hashes={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()
                                       for folder in ('sos_download','sos_prepare') for p in sorted((repo/folder).glob('*.py'))})
        old = self.store.get_meta('preparation_identity')
        if old is not None and old != identity:
            raise ValueError('Preparation rules, source or code changed. Do not resume with different rules.')
        if old is None:
            self.store.set_meta('preparation_identity',identity)
            write_json(self.store.root/'preparation_identity.json',identity)

    def import_original(self):
        if self.store.get_meta('original_imported'):
            return
        src = readonly(self.source/'state.sqlite')
        try:
            source_config = json.loads(src.execute("SELECT value FROM meta WHERE key='config'").fetchone()[0])
            if source_config != self.config or not src.execute("SELECT 1 FROM meta WHERE key='complete'").fetchone():
                raise ValueError('Original download must be complete with the identical population configuration')
            blocks = src.execute('SELECT * FROM blocks ORDER BY id').fetchall()
            pages = src.execute('SELECT * FROM pages ORDER BY block_id,page').fetchall()
            # Links avoid duplicate raw downloads/copies. All page access is read-only.
            for page in pages:
                target = self.source/page['path']
                link = self.store.page_path(page['block_id'],page['page'])
                if link.is_symlink():
                    if link.resolve() != target.resolve():
                        raise ValueError('Raw-page reference changed')
                elif link.exists():
                    raise ValueError('Unexpected existing file at original-page reference')
                else:
                    link.symlink_to(os.path.relpath(target,link.parent.resolve()))
            with self.store.db:
                for b in blocks:
                    self.store.db.execute('''INSERT INTO blocks(id,cohort,field_id,period_start,seed,sample_size,status,
                        n_pages,sample_result_count,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)''',
                        (b['id'],b['cohort'],b['field_id'],b['period_start'],b['seed'],b['sample_size'],
                         'available',b['n_pages'],b['sample_result_count'],b['created_at']))
                    self.store.db.execute('INSERT INTO origins VALUES(?,?)',(b['id'],'original'))
                self.store.db.executemany('INSERT INTO pages VALUES(?,?,?,?,?,?)',[tuple(p) for p in pages])
                self.store.db.execute('INSERT INTO meta VALUES(?,?)',('original_imported',json.dumps(dict(blocks=len(blocks),pages=len(pages)))))
            self.store.event('original_pages_referenced',dict(blocks=len(blocks),pages=len(pages)))
        finally:
            src.close()

    def new_block(self, cohort, cell=None):
        block = super().new_block(cohort,cell)
        with self.store.db:
            self.store.db.execute('INSERT INTO origins VALUES(?,?)',(block['id'],'additional'))
        return block

    def choose_block(self, cohort, cell=None):
        field,period = cell or (None,None)
        block = self.store.db.execute('''SELECT * FROM blocks WHERE cohort=? AND field_id IS ? AND period_start IS ?
            AND status IN ('available','downloading') ORDER BY id LIMIT 1''',(cohort,field,period)).fetchone()
        if block is None:
            return self.new_block(cohort,cell)
        if block['status'] == 'available':
            with self.store.db:
                self.store.db.execute("UPDATE blocks SET status='downloading' WHERE id=?",(block['id'],))
        return self.block(block['id'])

    def candidates(self, block):
        result,seen = [],set()
        for page in range(1,block['n_pages']+1):
            envelope = self.store.read_page(block['id'],page)
            if envelope['parameters'] != self.params(block,page):
                raise ValueError('Saved page parameters do not match its random block')
            self.validate_page(block,page,envelope['response'])
            for index,raw in enumerate(envelope['response']['results']):
                if raw['id'] in seen:
                    raise PageDrift('Duplicate ID within a saved sample block')
                seen.add(raw['id'])
                result.append((raw,page,index,envelope['retrieved_at']))
        random.Random(block['seed']).shuffle(result)
        return result

    def apply_block(self, block):
        candidates = self.candidates(block)
        normalized = [normalize_work(x[0],self.config) for x in candidates]
        diagnoses = self.quality.diagnose_many([r for r,reason in normalized if not reason])
        db = self.store.db
        counts = self.store.counts()
        cohort = block['cohort']
        cell = (block['field_id'],block['period_start'])
        if cohort == 'base':
            remaining = self.config['base_target']-counts.get('base',0)
        else:
            target = db.execute('SELECT target FROM allocations WHERE field_id=? AND period_start=?',cell).fetchone()[0]
            have = db.execute("SELECT count(*) FROM works WHERE cohort='extra' AND field_id=? AND period_start=?",cell).fetchone()[0]
            remaining = target-have
        if remaining <= 0:
            raise ValueError('Attempted to select for a filled cell')
        order = sum(counts.values())
        stats = Counter(candidates=len(candidates),accepted=0)
        origin = db.execute('SELECT origin FROM origins WHERE block_id=?',(block['id'],)).fetchone()[0]
        with db:
            sequence = db.execute('SELECT COALESCE(max(sequence),0)+1 FROM processed_blocks').fetchone()[0]
            db.execute('INSERT INTO processed_blocks VALUES(?,?)',(sequence,block['id']))
            for rank,((raw,page,index,retrieved),(r,reason)) in enumerate(zip(candidates,normalized)):
                if stats['accepted'] >= remaining:
                    break
                outcome = 'rejected_original_filter' if reason else None
                reasons = [reason] if reason else []
                wid = raw.get('id','').rsplit('/',1)[-1]
                text_sha = None if r is None else r['text_sha256']
                if r:
                    if cohort == 'extra' and (r['field_id'],r['period_start']) != cell:
                        raise PageDrift('Cell sample contains a different field or period')
                    reasons = reasons_for(r,diagnoses[text_sha],self.quality.policy)
                    if reasons:
                        outcome = 'rejected_quality'
                    elif db.execute('SELECT 1 FROM works WHERE work_id=?',(wid,)).fetchone():
                        outcome,reasons = 'duplicate_work_id',['already_selected']
                    else:
                        outcome = 'accepted'
                        order += 1
                        r.update(cohort=cohort,selection_order=order,source_block=block['id'],source_page=page,
                                 source_page_index=index,source_seed=block['seed'],retrieved_at=retrieved,
                                 legacy_id_present=False,legacy_text_match=False,source_origin=origin)
                        if self.legacy:
                            r['legacy_id_present'],r['legacy_text_match'] = self.legacy.lookup(wid,text_sha)
                        db.execute('INSERT INTO works VALUES(?,?,?,?,?,?,?,?,?)',
                            (wid,order,cohort,r['field_id'],r['period_start'],r['doi'],text_sha,block['id'],json.dumps(r,ensure_ascii=False)))
                        self.fault('during_apply')
                stats[outcome] += 1
                db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?)',
                    (block['id'],rank,wid,text_sha,outcome,json.dumps(reasons,ensure_ascii=False)))
            stats['not_examined_after_target'] = len(candidates)-sum(v for k,v in stats.items() if k!='candidates')
            db.execute("UPDATE blocks SET status='applied',applied_at=?,stats_json=? WHERE id=?",(utcnow(),json.dumps(stats),block['id']))
            if cohort == 'extra' and len(candidates)<block['sample_size'] and stats['accepted']<remaining:
                db.execute('UPDATE allocations SET exhausted=1 WHERE field_id=? AND period_start=?',cell)
        self.fault('after_apply')
        self.status('bloque limpiado',block=block['id'],message=f"{stats['accepted']} válidos; origen {origin}.")
        if not stats['accepted']:
            rows = db.execute('''SELECT b.stats_json FROM blocks b JOIN processed_blocks p ON p.block_id=b.id
                WHERE b.cohort=? AND b.field_id IS ? AND b.period_start IS ? ORDER BY p.sequence DESC LIMIT 20''',
                (cohort,*cell)).fetchall()
            if len(rows)==20 and all(json.loads(r[0])['accepted']==0 for r in rows):
                raise ValueError('20 blocks without progress; inspect without changing the population')

    def run(self, max_pages=None, max_blocks=None):
        if self.store.get_meta('clean_complete'):
            self.status('limpieza ya terminada')
            return self.store.get_meta('clean_complete')
        applied = 0
        while True:
            counts = self.store.counts()
            if counts.get('base',0) < self.config['base_target']:
                block = self.choose_block('base')
            elif counts.get('extra',0) < self.config['extra_target']:
                self.reallocate()
                cell = self.store.db.execute('''SELECT a.field_id,a.period_start FROM allocations a LEFT JOIN
                    (SELECT field_id,period_start,count(*) n FROM works WHERE cohort='extra' GROUP BY 1,2) w
                    ON a.field_id=w.field_id AND a.period_start=w.period_start
                    WHERE a.exhausted=0 AND a.target>COALESCE(w.n,0) ORDER BY a.field_id,a.period_start LIMIT 1''').fetchone()
                if cell is None:
                    raise ValueError('No cell available while supplement is incomplete')
                block = self.choose_block('extra',tuple(cell))
            else:
                # Unused saved blocks remain documented, with zero selected rows.
                with self.store.db:
                    self.store.db.execute("UPDATE blocks SET status='applied',stats_json=? WHERE status='available'",
                                          (json.dumps(dict(accepted=0,unused_saved_block=True)),))
                if self.store.db.execute("SELECT 1 FROM blocks WHERE status='downloading'").fetchone():
                    raise ValueError('Unexpected unfinished block at completion')
                self.status('comprobando y exportando corpus limpio')
                return self.store.export(self.config)
            if max_blocks is not None and applied >= max_blocks:
                self.status('pausado después de bloques de prueba')
                return None
            if not self.download_block(block,max_pages):
                self.status('pausado tras el límite de páginas nuevas')
                return None
            self.apply_block(self.block(block['id']))
            applied += 1
