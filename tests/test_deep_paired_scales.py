import unittest
import numpy as np
from sos_deep.paired_neighbor_scales import paired_candidates


class PairedScaleTests(unittest.TestCase):
    def test_candidates_keep_queries_counts_and_period_composition(self):
        periods=np.tile(np.arange(5),40);sub=np.arange(80);field=np.arange(200);q=np.array([2,7,11,21,44])
        a,b=paired_candidates(q,sub,field,periods,321,n=60)
        self.assertEqual(len(set(a)),60);self.assertEqual(len(set(b)),60)
        self.assertTrue(set(q)<=set(a));self.assertTrue(set(q)<=set(b))
        np.testing.assert_array_equal(np.bincount(periods[a]),np.bincount(periods[b]))
        self.assertTrue((a<80).all());self.assertTrue((b>=80).any())


if __name__=='__main__':unittest.main()
