import copy
import json
from pathlib import Path
import tempfile
import unittest

import requests

from sos_download.records import normalize_work, allocate_extra
from sos_download.runner import Runner, ApiClient, PageDrift
from sos_download.store import Store


def work(i, field=11, year=2001, words=70):
    return dict(id=f'https://openalex.org/W{i}',doi=f'https://doi.org/10.1/{i}',title=f'Paper {i}',
        abstract_inverted_index={f'word{j}':[j] for j in range(words)},publication_year=year,
        publication_date=f'{year}-01-01',type='article',language='en',is_retracted=False,is_paratext=False,
        primary_topic={'id':'https://openalex.org/T1','display_name':'Topic',
                       'field':{'id':f'https://openalex.org/fields/{field}','display_name':f'Field {field}'},
                       'subfield':{'id':'https://openalex.org/subfields/1101','display_name':'Sub'},
                       'domain':{'id':'https://openalex.org/domains/1','display_name':'Domain'}},topics=[])


def config(**overrides):
    return dict(schema_version=1,base_target=8,extra_target=4,seed=20260915,block_size=6,
        per_page=3,field_ids=[11,12],period_starts=[2000],year_min=2000,year_max=2004,
        min_abstract_words=50,request_delay=0,retry_seconds=0,**overrides)


class FakeAPI:
    def __init__(self):self.calls=[];self.fail_once=False;self.drift=False
    def get(self,params):
        self.calls.append(dict(params))
        if self.fail_once:
            self.fail_once=False;raise requests.ConnectionError('deliberate disconnected test')
        # A finite stable population with overlap across blocks and two fields.
        import random
        pool=[work(i,11 if i%3 else 12) for i in range(1,81)]
        f=params['filter']
        if 'primary_topic.field.id:11' in f:pool=[w for w in pool if w['primary_topic']['field']['id'].endswith('/11')]
        if 'primary_topic.field.id:12' in f:pool=[w for w in pool if w['primary_topic']['field']['id'].endswith('/12')]
        chosen=random.Random(params['seed']).sample(pool,min(params['sample'],len(pool)))
        offset=(params['page']-1)*params['per_page']; page=copy.deepcopy(chosen[offset:offset+params['per_page']])
        if self.drift and params['page']==1 and page:page[0]['id']='https://openalex.org/W999999'
        return dict(meta={'count':len(pool)},results=page)


class Crash(BaseException):pass


class RecordTests(unittest.TestCase):
    def test_cleaning_and_exact_boundary(self):
        a=work(1,words=50);a['title']='DNA'
        r,reason=normalize_work(a,config());self.assertIsNone(reason)
        self.assertEqual(r['abstract_word_count'],50);self.assertTrue(r['abstract_50_79'])
        self.assertEqual(r['field_id'],11);self.assertEqual(r['work_id'],'W1')
        self.assertEqual(normalize_work(work(2,words=49),config())[1],'short_abstract')

    def test_rejects_invalid_index_and_wrong_population(self):
        for change,reason in [({'type':'preprint'},'type'),({'language':'es'},'language'),
            ({'is_retracted':True},'retracted'),({'publication_year':2025},'year'),({'title':' '},'title')]:
            w=work(1);w.update(change);self.assertEqual(normalize_work(w,config())[1],reason)
        w=work(1);w['abstract_inverted_index']['broken']=[0]
        self.assertEqual(normalize_work(w,config())[1],'abstract_index')

    def test_extra_protects_small_cells_without_capping_large(self):
        self.assertEqual(allocate_extra({(11,2000):10,(12,2000):1,(13,2000):1},5),
                         {(11,2000):0,(12,2000):3,(13,2000):2})


class RecoveryTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def ids(self,path):
        s=Store(path,config());result=[r[0] for r in s.db.execute('select work_id from works order by selection_order')];s.close();return result

    def test_complete_run_sizes_dedup_and_export(self):
        run=Runner(self.root/'run',config(),FakeAPI());run.run();run.close()
        s=Store(self.root/'run',config())
        self.assertEqual(dict(s.db.execute('select cohort,count(*) from works group by cohort')),{'base':8,'extra':4})
        self.assertEqual(s.db.execute('select count(distinct work_id) from works').fetchone()[0],12)
        import pyarrow.parquet as pq
        table=pq.read_table(self.root/'run'/'corpus.parquet')
        self.assertEqual(table.num_rows,12);self.assertTrue(table.column('abstract').null_count==0)
        self.assertEqual(json.loads((self.root/'run'/'validation.json').read_text())['status'],'passed');s.close()

    def test_raw_page_survives_crash_before_database_commit(self):
        baseline=Runner(self.root/'baseline',config(),FakeAPI());baseline.run();baseline.close()
        def fault(point):
            if point=='after_page_file':raise Crash()
        api=FakeAPI();run=Runner(self.root/'restart',config(),api,fault=fault)
        with self.assertRaises(Crash):run.run()
        run.close();self.assertEqual(len(api.calls),1)
        api2=FakeAPI();resumed=Runner(self.root/'restart',config(),api2);resumed.run();resumed.close()
        self.assertEqual(self.ids(self.root/'baseline'),self.ids(self.root/'restart'))
        # Recover the durable raw page; a revalidation is allowed, replacing it is not.
        self.assertTrue(list((self.root/'restart'/'raw').glob('*.json.gz')))

    def test_mid_block_transaction_rolls_back_then_repeats_exactly(self):
        baseline=Runner(self.root/'baseline',config(),FakeAPI());baseline.run();baseline.close()
        def fault(point):
            if point=='during_apply':raise Crash()
        run=Runner(self.root/'restart',config(),FakeAPI(),fault=fault)
        with self.assertRaises(Crash):run.run()
        run.close()
        s=Store(self.root/'restart',config());self.assertEqual(s.db.execute('select count(*) from works').fetchone()[0],0);s.close()
        resumed=Runner(self.root/'restart',config(),FakeAPI());resumed.run();resumed.close()
        self.assertEqual(self.ids(self.root/'baseline'),self.ids(self.root/'restart'))

    def test_resume_after_commit_is_idempotent(self):
        baseline=Runner(self.root/'baseline',config(),FakeAPI());baseline.run();baseline.close()
        def fault(point):
            if point=='after_apply':raise Crash()
        run=Runner(self.root/'restart',config(),FakeAPI(),fault=fault)
        with self.assertRaises(Crash):run.run()
        run.close();resumed=Runner(self.root/'restart',config(),FakeAPI());resumed.run();resumed.close()
        self.assertEqual(self.ids(self.root/'baseline'),self.ids(self.root/'restart'))

    def test_network_cut_retries_and_matches_uninterrupted_run(self):
        baseline=Runner(self.root/'baseline',config(),FakeAPI());baseline.run();baseline.close()
        api=FakeAPI();api.fail_once=True
        run=Runner(self.root/'retry',config(),api);run.run();run.close()
        self.assertEqual(self.ids(self.root/'baseline'),self.ids(self.root/'retry'))

    def test_changed_page_on_resume_fails_closed(self):
        run=Runner(self.root/'restart',config(),FakeAPI());run.run(max_pages=1);run.close()
        api=FakeAPI();api.drift=True;resumed=Runner(self.root/'restart',config(),api)
        with self.assertRaises(PageDrift):resumed.run()
        self.assertEqual(resumed.store.db.execute('select count(*) from works').fetchone()[0],0);resumed.close()

    def test_saved_page_corruption_fails_before_selecting(self):
        run=Runner(self.root/'restart',config(),FakeAPI());run.run(max_pages=1);run.close()
        next((self.root/'restart'/'raw').glob('*.json.gz')).write_bytes(b'broken')
        resumed=Runner(self.root/'restart',config(),FakeAPI())
        with self.assertRaises((ValueError,OSError,EOFError)):resumed.run()
        resumed.close()

    def test_configuration_cannot_change_when_resuming(self):
        s=Store(self.root/'run',config());s.close();different=config();different['base_target']=9
        with self.assertRaises(ValueError):Store(self.root/'run',different)


if __name__=='__main__':unittest.main()
