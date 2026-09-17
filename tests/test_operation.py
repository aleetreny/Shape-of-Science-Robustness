import contextlib
import copy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import random
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from urllib.parse import parse_qs, urlparse

from sos_download.cli import writer_lock, show_status, read_config
from sos_download.legacy import build_index, LegacyIndex
from sos_download.runner import ApiClient, Runner, PageDrift
from sos_download.store import Store
from test_download import FakeAPI, config, work, Crash


class OperationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_second_writer_is_blocked_and_status_does_not_start_work(self):
        with writer_lock(self.root):
            with self.assertRaises(ValueError):
                with writer_lock(self.root):
                    self.fail('A second writer acquired the lock')
        with contextlib.redirect_stdout(io.StringIO()) as text:
            show_status(self.root)
        self.assertIn('no se ha iniciado', text.getvalue())
        self.assertFalse((self.root/'state.sqlite').exists())

    def test_production_config_respects_fixed_protocol(self):
        cfg = read_config(Path(__file__).resolve().parents[1]/'config/corpus.json')
        self.assertEqual((cfg['base_target'], cfg['extra_target']), (400000,100000))
        self.assertEqual(len(cfg['field_ids'])*len(cfg['period_starts']),130)

    def test_local_index_matches_exact_text_and_does_not_change_source(self):
        import pyarrow as pa
        import pyarrow.parquet as pq
        from sos_download.records import text_hash
        source = self.root/'legacy.parquet'
        pq.write_table(pa.Table.from_pylist([dict(work_id='W1', title='DNA', abstract='abc')]),source)
        before = source.read_bytes()
        build_index(source,self.root/'index.sqlite',lambda _:None)
        index = LegacyIndex(self.root/'index.sqlite',source)
        self.assertEqual(index.lookup('W1',text_hash('DNA','abc')),(True,True))
        self.assertEqual(index.lookup('W1','different'),(True,False))
        self.assertEqual(index.lookup('W2','different'),(False,False))
        index.close()
        self.assertEqual(source.read_bytes(),before)

    def test_actual_http_disconnect_then_rate_limit_are_retried_and_key_is_private(self):
        calls = []
        fake = FakeAPI()
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args): pass
            def do_GET(self):
                calls.append((self.path,self.headers.get('Authorization')))
                if len(calls)==1:
                    self.connection.shutdown(socket.SHUT_RDWR);self.connection.close();return
                if len(calls)==2:
                    self.send_response(429);self.send_header('Retry-After','0');self.end_headers();return
                params = {key: values[0] for key,values in parse_qs(urlparse(self.path).query).items()}
                for key in ('sample','seed','page','per_page'): params[key] = int(params[key])
                payload = json.dumps(fake.get(params)).encode()
                self.send_response(200);self.send_header('Content-Length',str(len(payload)))
                self.end_headers();self.wfile.write(payload)
        server = ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread = threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        api = ApiClient('PRIVATE_TEST_KEY', f'http://127.0.0.1:{server.server_port}/works')
        runner = Runner(self.root/'http',config(),api)
        try:
            runner.run()
            self.assertEqual(runner.store.counts(),{'base':8,'extra':4})
            self.assertEqual(runner.store.db.execute("SELECT count(*) FROM events WHERE kind='retry'").fetchone()[0],2)
            for path, authorization in calls:
                self.assertNotIn('PRIVATE_TEST_KEY',path)
                self.assertEqual(authorization,'Bearer PRIVATE_TEST_KEY')
        finally:
            runner.close();api.close();server.shutdown();server.server_close();thread.join()
        for path in (self.root/'http').rglob('*'):
            if path.is_file():self.assertNotIn(b'PRIVATE_TEST_KEY',path.read_bytes())

    def test_real_process_killed_after_page_file_recovers_identical_selection(self):
        program = '''
import sys,time
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tests'))
from test_download import FakeAPI,config
from sos_download.runner import Runner
root=Path(sys.argv[1])
def fault(point):
    if point=='after_page_file':
        (root/'ready').write_text('ready')
        time.sleep(30)
runner=Runner(root,config(),FakeAPI(),fault=fault)
runner.run()
'''
        output = self.root/'killed'
        process = subprocess.Popen([sys.executable,'-c',program,str(output)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            deadline=time.monotonic()+10
            while not (output/'ready').exists() and time.monotonic()<deadline and process.poll() is None:
                time.sleep(.02)
            self.assertTrue((output/'ready').exists())
            process.kill();process.communicate(timeout=5)
        finally:
            if process.poll() is None:process.kill();process.communicate()
        resumed=Runner(output,config(),FakeAPI());resumed.run()
        baseline=Runner(self.root/'baseline',config(),FakeAPI());baseline.run()
        query='SELECT work_id FROM works ORDER BY selection_order'
        self.assertEqual([r[0] for r in resumed.store.db.execute(query)], [r[0] for r in baseline.store.db.execute(query)])
        resumed.close();baseline.close()

    def test_reallocation_after_exhaustion_survives_commit_interruption(self):
        cfg=config();cfg.update(base_target=4,extra_target=8,block_size=20)
        class CensusAPI:
            def get(self,params):
                pool=[work(i,11) for i in range(1,31)] + [work(40,12)]
                if 'primary_topic.field.id:12' in params['filter']:pool=[pool[-1]]
                elif 'primary_topic.field.id:11' in params['filter']:pool=pool[:-1]
                chosen=random.Random(params['seed']).sample(pool,min(params['sample'],len(pool)))
                offset=(params['page']-1)*params['per_page']
                return dict(meta={'count':len(chosen)},results=chosen[offset:offset+params['per_page']])
        baseline=Runner(self.root/'baseline',cfg,CensusAPI());baseline.run()
        def fault(point):
            if point=='after_apply' and interrupted.store.db.execute('SELECT 1 FROM allocations WHERE exhausted=1').fetchone():
                raise Crash()
        interrupted=Runner(self.root/'restart',cfg,CensusAPI(),fault=fault)
        with self.assertRaises(Crash):interrupted.run()
        interrupted.close()
        resumed=Runner(self.root/'restart',cfg,CensusAPI());resumed.run()
        query='SELECT work_id FROM works ORDER BY selection_order'
        self.assertEqual([r[0] for r in resumed.store.db.execute(query)], [r[0] for r in baseline.store.db.execute(query)])
        self.assertEqual(resumed.store.counts(),{'base':4,'extra':8})
        resumed.close();baseline.close()

    def test_duplicate_across_pages_does_not_enter_corpus(self):
        class DuplicateAPI(FakeAPI):
            def get(self,params):
                result=super().get(params)
                if params['page']==2:
                    result['results'][0]=super().get({**params,'page':1})['results'][0]
                return result
        runner=Runner(self.root,config(),DuplicateAPI())
        with self.assertRaises(PageDrift):runner.run()
        self.assertEqual(runner.store.counts(),{})
        runner.close()

    def test_changed_interior_page_on_resume_is_detected_without_redownloading_abstracts(self):
        cfg=config();cfg['block_size']=12
        run=Runner(self.root,cfg,FakeAPI());run.run(max_pages=3);run.close()
        class InteriorDriftAPI(FakeAPI):
            def get(self,params):
                response=super().get(params)
                if params['page']==2:response['results'][0]['id']='https://openalex.org/W999999'
                return response
        api=InteriorDriftAPI();resumed=Runner(self.root,cfg,api)
        with self.assertRaises(PageDrift):resumed.run()
        self.assertEqual(resumed.store.counts(),{})
        self.assertTrue(all(params['select']=='id' for params in api.calls))
        resumed.close()

    def test_twenty_empty_blocks_pause_with_clear_reason(self):
        class NoValidAPI(FakeAPI):
            def get(self,params):
                response=super().get(params)
                for w in response['results']:
                    w['abstract_inverted_index']={f'word{i}':[i] for i in range(49)}
                return response
        runner=Runner(self.root,config(),NoValidAPI())
        with self.assertRaisesRegex(ValueError,'20 bloques'):
            runner.run()
        self.assertEqual(runner.store.counts(),{})
        runner.close()

    def test_exhausted_cell_larger_than_initial_sample_is_fully_checked_and_reallocated(self):
        cfg=config();cfg.update(base_target=1,extra_target=4,block_size=20,seed=106)
        class SparseAPI:
            def get(self,params):
                pool=[work(i,11,words=70 if i==1 else 49) for i in range(1,8)] + [work(i,12) for i in range(21,41)]
                if 'primary_topic.field.id:11' in params['filter']:pool=pool[:7]
                elif 'primary_topic.field.id:12' in params['filter']:pool=pool[7:]
                chosen=random.Random(params['seed']).sample(pool,min(params['sample'],len(pool)))
                offset=(params['page']-1)*params['per_page']
                return dict(meta={'count':len(chosen)},results=chosen[offset:offset+params['per_page']])
        runner=Runner(self.root,cfg,SparseAPI())
        runner.run()
        self.assertEqual(runner.store.counts(),{'base':1,'extra':4})
        self.assertEqual(runner.store.db.execute("SELECT field_id FROM works WHERE cohort='base'").fetchone()[0],11)
        self.assertEqual(runner.store.db.execute('SELECT exhausted FROM allocations WHERE field_id=11').fetchone()[0],1)
        runner.close()


if __name__=='__main__':unittest.main()
