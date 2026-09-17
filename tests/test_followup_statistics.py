import unittest
import numpy as np
from sos_followup.pilot_statistics import cosine_grams,cka_matrix,rsa_matrix,effect_rows,u_center
from sos_analysis.geometry import shape_scores

class PairedStatistics(unittest.TestCase):
    def test_dual_equals_independent_frozen_feature_formula(self):
        rng=np.random.default_rng(42)
        xs=[rng.normal(size=(81,d)) for d in [15,38,120]]
        xs[1][:,:15]+=.5*xs[0]
        got=cka_matrix(cosine_grams(xs))
        ref=shape_scores(xs,procrustes=False)
        for r in ref:self.assertAlmostEqual(got[int(r['model_a']),int(r['model_b'])],r['cka_debiased'],places=11)
    def test_row_alignment_and_rotation(self):
        rng=np.random.default_rng(71);x=rng.normal(size=(100,40));q,_=np.linalg.qr(rng.normal(size=(40,40)))
        score=cka_matrix(cosine_grams([x,x@q,x[rng.permutation(100)]]))
        self.assertAlmostEqual(score[0,1],1,places=11)
        self.assertLess(abs(score[0,2]),.1)
    def test_effects_keep_model_and_input_separate(self):
        models=['a','b','c'];names=[(m,c) for c in ['title','abstract','title_abstract'] for m in models]
        # Different models orthogonal, all input conditions identical within each model.
        matrix=np.array([[float(a==b) for b,d in names] for a,c in names])
        rows,s=effect_rows(matrix,names,models)
        self.assertTrue(all(r['input_change_from_full']==0 for r in rows));self.assertEqual(s['model_minus_input'],1)
        # Model has no effect, input condition is orthogonal.
        matrix=np.array([[float(c==d) for b,d in names] for a,c in names])
        rows,s=effect_rows(matrix,names,models)
        self.assertTrue(all(r['model_change_at_full']==0 for r in rows));self.assertEqual(s['model_minus_input'],-1)
    def test_rsa_and_common_reordering(self):
        rng=np.random.default_rng(34);x=rng.normal(size=(70,9));p=rng.permutation(70)
        grams=cosine_grams([x,3*x]);s=rsa_matrix(grams,44)
        self.assertAlmostEqual(s[0,1],1,places=10)
        np.testing.assert_allclose(cka_matrix(grams),cka_matrix(grams[:,p][:,:,p]),atol=1e-11)
    def test_degenerate_rejected(self):
        with self.assertRaises(ValueError):cka_matrix(np.ones((2,10,10)))

if __name__=='__main__':unittest.main()
