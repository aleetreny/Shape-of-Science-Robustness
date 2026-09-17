import unittest
import numpy as np
from sos_deep.family_traits import identified_fit


class FamilyTests(unittest.TestCase):
    def test_rank_deficiency_cannot_produce_named_coefficients(self):
        x=np.array([[1,0,0],[1,1,1],[1,2,2]],float)
        fit=identified_fit(x,np.array([0,1,2.]))
        self.assertFalse(fit['identified']);self.assertIsNone(fit['coefficients'])
        self.assertAlmostEqual(fit['r_squared'],1)
        fit=identified_fit(x[:,:2],np.array([0,1,2.]))
        self.assertTrue(fit['identified'])
        np.testing.assert_allclose(fit['coefficients'],[0,1],atol=1e-12)


if __name__=='__main__':unittest.main()
