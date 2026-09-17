import hashlib
import json
from pathlib import Path
import tempfile
import shutil
import unittest

from sos_download.runner import Runner
from sos_download.store import Store
from sos_prepare.runner import CleanRunner
from tests.test_download import config, FakeAPI, Crash


class FakeQuality:
    model_sha = 'fixture-model'

    def __init__(self):
        self.policy = dict(ambiguous_language='keep_flagged',boilerplate_abstracts={},reviewed_records={})

    def diagnose_many(self, records):
        return {r['text_sha256']:dict(language_clear_non_english=int(r['work_id'][1:])%7==0,
                                     language_ambiguous=False) for r in records}


class PreparationRecovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root/'original'
        r = Runner(self.source,config(),FakeAPI());r.run();r.close()
        self.before = self.hashes()

    def tearDown(self):
        self.tmp.cleanup()

    def hashes(self):
        return {str(p.relative_to(self.source)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.source.rglob('*') if p.is_file() and not p.name.endswith(('-wal','-shm'))}

    def run_clean(self, name, **kwargs):
        return CleanRunner(self.root/name,config(),FakeAPI(),FakeQuality(),self.source,**kwargs)

    def ids(self, name):
        s = Store(self.root/name,config())
        ids = [r[0] for r in s.db.execute('SELECT work_id FROM works ORDER BY selection_order')]
        s.close();return ids

    def test_cleaning_refills_base_before_extra_and_preserves_source(self):
        run = self.run_clean('clean');run.run()
        rows = run.store.db.execute('SELECT work_id,cohort FROM works ORDER BY selection_order').fetchall()
        self.assertEqual([r[1] for r in rows],['base']*8+['extra']*4)
        self.assertTrue(all(int(r[0][1:])%7 for r in rows))
        self.assertEqual(len({r[0] for r in rows}),12)
        self.assertTrue(any(p.is_symlink() for p in (self.root/'clean/raw').iterdir()))
        run.close();self.assertEqual(self.hashes(),self.before)

    def test_transaction_interruption_replays_same_selection(self):
        baseline = self.run_clean('baseline');baseline.run();baseline.close()
        def fault(point):
            if point=='during_apply':raise Crash()
        run = self.run_clean('restart',fault=fault)
        with self.assertRaises(Crash):run.run()
        self.assertEqual(run.store.db.execute('SELECT count(*) FROM decisions').fetchone()[0],0)
        self.assertEqual(run.store.db.execute('SELECT count(*) FROM processed_blocks').fetchone()[0],0)
        run.close()
        run = self.run_clean('restart');run.run();run.close()
        self.assertEqual(self.ids('restart'),self.ids('baseline'))
        self.assertEqual(self.hashes(),self.before)

    def test_original_pages_need_no_api_requests_when_sufficient(self):
        class AllGood(FakeQuality):
            def diagnose_many(self,records):
                return {r['text_sha256']:dict(language_clear_non_english=False,language_ambiguous=False) for r in records}
        api = FakeAPI()
        run = CleanRunner(self.root/'same',config(),api,AllGood(),self.source)
        run.run();run.close()
        self.assertEqual(api.calls,[])
        self.assertEqual(self.ids('same'),self.ids('original'))

    def test_guard_rejects_writing_to_original_before_opening_store(self):
        with self.assertRaises(ValueError):
            CleanRunner(self.source,config(),FakeAPI(),FakeQuality(),self.source)
        self.assertEqual(self.hashes(),self.before)

    def test_new_download_fills_global_base_before_using_cell_blocks(self):
        class Sparse(FakeQuality):
            def diagnose_many(self,records):
                return {r['text_sha256']:dict(language_clear_non_english=int(r['work_id'][1:])%2!=0,
                                             language_ambiguous=False) for r in records}
        api=FakeAPI();run=CleanRunner(self.root/'sparse',config(),api,Sparse(),self.source)
        run.run()
        self.assertTrue(api.calls)
        self.assertIn('primary_topic.field.id:!null',api.calls[0]['filter'])
        self.assertEqual([r[0] for r in run.store.db.execute('SELECT cohort FROM works ORDER BY selection_order')],['base']*8+['extra']*4)
        self.assertTrue(all(int(r[0][1:])%2==0 for r in run.store.db.execute('SELECT work_id FROM works')))
        run.close();self.assertEqual(self.hashes(),self.before)

    def test_rebuild_adopts_additional_complete_pages_without_redownloading(self):
        class Sparse(FakeQuality):
            def diagnose_many(self,records):
                return {r['text_sha256']:dict(language_clear_non_english=int(r['work_id'][1:])%2!=0,
                                             language_ambiguous=False) for r in records}
        first=CleanRunner(self.root/'first',config(),FakeAPI(),Sparse(),self.source)
        first.run()
        pages=first.store.db.execute("SELECT p.path FROM pages p JOIN origins o ON p.block_id=o.block_id WHERE o.origin='additional'").fetchall()
        self.assertTrue(pages)
        first.close()
        for row in pages:
            target=self.root/'rebuilt'/row[0];target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(self.root/'first'/row[0],target)
        api=FakeAPI();second=CleanRunner(self.root/'rebuilt',config(),api,Sparse(),self.source)
        second.run();second.close()
        self.assertEqual(api.calls,[])
        self.assertEqual(self.ids('rebuilt'),self.ids('first'))
        self.assertEqual(self.hashes(),self.before)


if __name__ == '__main__':
    unittest.main()
