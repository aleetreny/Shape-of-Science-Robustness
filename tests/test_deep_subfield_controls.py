import unittest
import numpy as np
from sos_deep.subfield_controls import sample_order, measure, NAMES, PRIMARY


class ControlsTests(unittest.TestCase):
    def test_deterministic_nested_selection_and_model_recipe_invariance(self):
        ids=np.arange(60);work=['W'+str(i) for i in ids]
        a=sample_order(ids,work,'subfield','1234')
        np.testing.assert_array_equal(a,sample_order(ids[::-1],work,'subfield','1234'))
        self.assertEqual(set(a),set(ids))
        rng=np.random.default_rng(4);x=rng.normal(size=(60,7))
        arrays={n:x@np.linalg.qr(rng.normal(size=(7,7)))[0] for n in NAMES}
        shapes,neighbors,counts,verified=measure(ids,arrays)
        self.assertEqual(len(shapes),135);self.assertEqual(len(neighbors),405)
        for r in shapes:self.assertAlmostEqual(r['cka_debiased'],1,places=10)
        for r in neighbors:self.assertAlmostEqual(r['mean_overlap'],1)
        for k,c in counts.items():self.assertTrue((c==k).all())
        self.assertEqual(verified,len(NAMES)*5)


if __name__=='__main__':unittest.main()
