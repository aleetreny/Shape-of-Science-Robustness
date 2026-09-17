import unittest
import numpy as np
from sos_deep.regions import paper_scores,PAIRS


class RegionTests(unittest.TestCase):
    def test_omission_detects_single_model_and_trivial_graph_rejected(self):
        c=np.full((3,45),25,np.uint8)
        c[:,[i for i,p in enumerate(PAIRS) if 'minilm' in p]]=0
        r=paper_scores(c,25,100)
        np.testing.assert_allclose(r['mean'],.8)
        np.testing.assert_allclose(r['leave_one_max'],1)
        self.assertTrue((r['leave_one_min']<r['mean']).all())
        with self.assertRaises(AssertionError):paper_scores(c,25,26)


if __name__=='__main__':unittest.main()
