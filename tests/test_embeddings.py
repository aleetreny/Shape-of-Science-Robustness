"""Protect the costly outputs: identity, interruption, corruption and pooling."""
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import pyarrow as pa
import torch


class EmbeddingTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('sos_embed'), 'Embedding implementation is missing')
        from sos_embed import storage, models
        self.s, self.m = storage, models
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.rows = pa.table({'row_index': [2, 7, 11, 20], 'work_id': ['W2','W7','W11','W20'],
                              'text_sha256': ['a','b','c','d']})
        self.manifest = {'rows':4, 'dimension':3, 'poolings':['cls'], 'input_sha256':'fixed',
                         'model_revision':'fixed', 'shard_size':2}
        self.vectors = {'cls':np.arange(1, 13, dtype=np.float32).reshape(4,3)}

    def store(self):
        return self.s.Store(self.root/'run', self.manifest)

    def test_resume_keeps_exact_ids_and_vectors(self):
        s = self.store()
        s.commit(0, self.rows.slice(0,2), {'cls':self.vectors['cls'][:2]}, {'seconds':1})
        first = self.s.file_sha(s.path/'shards'/'000000000-000000002'/'cls.npy')
        s = self.store()
        self.assertEqual(s.scan(self.rows)['rows'], 2)
        s.commit(2, self.rows.slice(2,2), {'cls':self.vectors['cls'][2:]}, {'seconds':1})
        self.assertEqual(s.scan(self.rows)['rows'],4)
        self.assertEqual(first, self.s.file_sha(s.path/'shards'/'000000000-000000002'/'cls.npy'))

    def test_committed_shard_cannot_be_overwritten(self):
        s=self.store(); s.commit(0,self.rows.slice(0,2),{'cls':self.vectors['cls'][:2]}, {})
        with self.assertRaises((FileExistsError,ValueError)):
            s.commit(0,self.rows.slice(0,2),{'cls':self.vectors['cls'][:2]}, {})

    def test_changed_recipe_refuses_resume(self):
        self.store()
        with self.assertRaisesRegex(ValueError,'manifest|configuration'):
            self.s.Store(self.root/'run', {**self.manifest,'model_revision':'different'})

    def test_corrupt_vectors_are_detected(self):
        s=self.store(); s.commit(0,self.rows.slice(0,2),{'cls':self.vectors['cls'][:2]}, {})
        p=s.path/'shards'/'000000000-000000002'/'cls.npy'
        b=bytearray(p.read_bytes());b[-1]^=1;p.write_bytes(b)
        with self.assertRaisesRegex(ValueError,'checksum'):
            s.scan(self.rows)

    def test_row_permutation_is_detected(self):
        s=self.store(); s.commit(0,self.rows.take([1,0]),{'cls':self.vectors['cls'][:2]}, {})
        with self.assertRaisesRegex(ValueError,'identity'):
            s.scan(self.rows)

    def test_gap_is_detected(self):
        s=self.store(); s.commit(2,self.rows.slice(2,2),{'cls':self.vectors['cls'][2:]}, {})
        with self.assertRaisesRegex(ValueError,'gap|order'):
            s.scan(self.rows)

    def test_partial_directories_are_not_completed_work(self):
        s=self.store();(s.path/'shards'/'.partial-test').mkdir()
        self.assertEqual(s.scan(self.rows)['rows'],0)

    def test_invalid_numbers_dimensions_and_zero_vectors_refused(self):
        for values in (np.zeros((2,3),np.float32),np.full((2,3),np.nan,np.float32),
                       np.ones((2,2),np.float32),np.ones((2,3),np.float64)):
            with self.subTest(values=values), self.assertRaises(ValueError):
                self.store().commit(0,self.rows.slice(0,2),{'cls':values},{})

    def test_pooling_uses_last_real_token_and_excludes_padding(self):
        hidden=torch.tensor([[[1.,2.],[3.,4.],[5.,6.],[999.,999.]],
                             [[2.,4.],[6.,8.],[999.,999.],[999.,999.]]])
        mask=torch.tensor([[1,1,1,0],[1,1,0,0]])
        self.assertTrue(torch.equal(self.m.pool(hidden,mask,'cls'),torch.tensor([[1.,2.],[2.,4.]])))
        self.assertTrue(torch.equal(self.m.pool(hidden,mask,'sep'),torch.tensor([[5.,6.],[6.,8.]])))
        self.assertTrue(torch.equal(self.m.pool(hidden,mask,'mean'),torch.tensor([[3.,4.],[4.,6.]])))

    def test_input_separators_are_explicit(self):
        self.assertEqual(self.m.format_text('Title','Abstract','sep','[SEP]'),'Title[SEP]Abstract')
        self.assertEqual(self.m.format_text('Title','Abstract','blank_line','[SEP]'),'Title\n\nAbstract')
        with self.assertRaises(ValueError):self.m.format_text('T','A','unknown','[SEP]')

    def test_lock_blocks_second_process(self):
        with self.s.run_lock(self.root):
            code='from sos_embed.storage import run_lock; from pathlib import Path\nwith run_lock(Path(__import__("sys").argv[1])): pass'
            result=subprocess.run([sys.executable,'-c',code,str(self.root)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('already running',result.stderr)

    def test_killed_process_keeps_only_committed_work(self):
        code='''import os, signal, sys, json
from pathlib import Path
import numpy as np, pyarrow as pa
from sos_embed.storage import Store
s=Store(Path(sys.argv[1]),json.loads(sys.argv[2]))
s.commit(0,pa.table({'row_index':[2,7],'work_id':['W2','W7'],'text_sha256':['a','b']}),{'cls':np.arange(1,7,dtype=np.float32).reshape(2,3)},{})
(s.path/'shards'/'.partial-killed').mkdir()
os.kill(os.getpid(), signal.SIGKILL)
'''
        r=subprocess.run([sys.executable,'-c',code,str(self.root/'run'),json.dumps(self.manifest)],capture_output=True)
        self.assertNotEqual(r.returncode,0)
        self.assertEqual(self.store().scan(self.rows)['rows'],2)
        self.store().commit(2,self.rows.slice(2,2),{'cls':self.vectors['cls'][2:]},{})
        self.assertEqual(self.store().scan(self.rows)['rows'],4)

    def test_full_run_needs_resolved_input_policy(self):
        self.assertIsNotNone(importlib.util.find_spec('sos_embed.runner'), 'Runner is missing')
        from sos_embed.runner import check_scope
        with self.assertRaisesRegex(ValueError,'policy'):
            check_scope({'production_input_policy_approved':False}, 'full')
        check_scope({'production_input_policy_approved':False}, 'pilot')
        check_scope({'production_input_policy_approved':True}, 'full')

    def test_modified_input_is_refused(self):
        self.assertIsNotNone(importlib.util.find_spec('sos_embed.runner'), 'Runner is missing')
        from sos_embed.runner import verify_input
        p=self.root/'table';p.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'input'):
            verify_input(p,{'input_sha256':'original'})

    def test_same_fragment_fits_every_tokenizer_and_keeps_source_prefix(self):
        self.assertIsNotNone(importlib.util.find_spec('sos_embed.common_text'), 'Common text preparation is missing')
        from sos_embed.common_text import common_fragment
        class SmallTokenizer:
            sep_token='|'
            def __init__(self, multiplier):self.multiplier=multiplier
            def __call__(self,text,**kwargs):
                return {'input_ids':list(range(len(text.replace('|',' ').split())*self.multiplier+2))}
        pairs=[({'text_format':'blank_line','max_length':8},SmallTokenizer(1)),
               ({'text_format':'sep','max_length':8},SmallTokenizer(2))]
        title,abstract=common_fragment('Alpha beta','one two three four five',pairs)
        self.assertEqual(title,'Alpha beta')
        self.assertTrue('one two three four five'.startswith(abstract))
        for spec,t in pairs:
            s=self.m.format_text(title,abstract,spec['text_format'],t.sep_token)
            self.assertLessEqual(len(t(s)['input_ids']),spec['max_length'])
        title2,abstract2=common_fragment('Alpha beta gamma delta epsilon','one two',pairs)
        self.assertTrue('Alpha beta gamma delta epsilon'.startswith(title2))
        self.assertEqual(abstract2,'')


if __name__=='__main__': unittest.main()
