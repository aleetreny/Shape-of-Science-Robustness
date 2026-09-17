import unittest
import numpy as np
from sos_deep.centroid_scales import shuffled_assignments


class ScaleTests(unittest.TestCase):
    def test_null_preserves_each_group_period_composition_without_replacement(self):
        ids=np.arange(30);periods=np.repeat([0,1,2],10)
        p=shuffled_assignments(ids,periods,5,123)
        self.assertEqual(p.shape,(5,30))
        for r in p:
            np.testing.assert_array_equal(np.sort(r),ids)
            np.testing.assert_array_equal(periods[r],periods)
        self.assertFalse(np.array_equal(p[0],p[1]))


if __name__=='__main__':unittest.main()
