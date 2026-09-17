import unittest
import numpy as np
import torch
from sos_deep.inputs52 import assemble_literal, AUDIT_COLUMNS
from sos_embed.models import pool


class FakePrior:
    manifest = {'poolings': ['mean', 'cls', 'sep'], 'dimension': 2}
    def __init__(self, rows):
        self.rows = {r['row_index']: r for r in rows}
    def row(self, index):
        if index not in self.rows:
            return None
        row = {**self.rows[index], **{k: False if k=='truncated' else 1 for k in AUDIT_COLUMNS}}
        return row, {p: np.array([index, i+.25], np.float32) for i,p in enumerate(self.manifest['poolings'])}


class FakeEncoder:
    def __init__(self):
        self.seen = []
    def encode_literal(self, rows, condition):
        self.seen += [r['row_index'] for r in rows]
        vec = {p: np.array([[r['row_index'], i+.75] for r in rows], np.float32)
               for i,p in enumerate(['mean','cls','sep'])}
        audit = [{k: False if k=='truncated' else 2 for k in AUDIT_COLUMNS} for _ in rows]
        return vec, audit, {}


class NestedInputs(unittest.TestCase):
    def setUp(self):
        self.rows = [{'row_index': i, 'work_id': str(i), 'text_sha256': str(i),
                      'source_text_sha256': 'full'+str(i)} for i in [2,5,7,11]]
    def test_mixed_rows_preserve_identity_and_every_old_pooling(self):
        prior = FakePrior(self.rows[::2]);encoder=FakeEncoder()
        vectors,audit,stats=assemble_literal(self.rows,'title',prior,encoder)
        self.assertEqual(encoder.seen,[5,11])
        self.assertEqual([r['reuse_origin'] for r in audit],['pilot26k','new_inference']*2)
        self.assertEqual(stats['reused_rows'],2);self.assertEqual(stats['new_rows'],2)
        for i,row in enumerate(self.rows):
            for p,vec in vectors.items():
                self.assertEqual(vec[i,0],row['row_index'])
                if i%2==0:self.assertTrue(np.array_equal(vec[i],prior.row(row['row_index'])[1][p]))
    def test_all_old_rows_require_no_encoder_and_mismatched_id_is_rejected(self):
        prior=FakePrior(self.rows)
        _,_,stats=assemble_literal(self.rows,'abstract',prior,None)
        self.assertEqual(stats['new_rows'],0)
        bad=[{**r,'work_id':'wrong'} for r in self.rows]
        with self.assertRaises(AssertionError):assemble_literal(bad,'abstract',prior,None)
    def test_pooling_semantics_including_special_and_excluding_padding(self):
        hidden=torch.tensor([[[1.,10.],[3.,30.],[5.,50.],[999.,999.]],
                             [[2.,20.],[4.,40.],[6.,60.],[8.,80.]]])
        mask=torch.tensor([[1,1,1,0],[1,1,1,1]])
        self.assertTrue(torch.equal(pool(hidden,mask,'cls'),torch.tensor([[1.,10.],[2.,20.]])))
        self.assertTrue(torch.equal(pool(hidden,mask,'sep'),torch.tensor([[5.,50.],[8.,80.]])))
        self.assertTrue(torch.equal(pool(hidden,mask,'mean'),torch.tensor([[3.,30.],[5.,50.]])))


if __name__=='__main__':unittest.main()
