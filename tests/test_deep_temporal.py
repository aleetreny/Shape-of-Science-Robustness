import unittest
import numpy as np
from sos_deep.temporal_review import trend


class TemporalTests(unittest.TestCase):
    def test_nonmonotonicity_and_endpoint_do_not_imply_same_slope(self):
        x=np.array([[0,1,2,3,4],[4,3,2,1,0],[0,10,1,0,1.]])
        d,s,i,j=trend(x)
        np.testing.assert_allclose(d,[4,-4,1])
        self.assertLess(s[2],0)
        np.testing.assert_array_equal(i,[4,0,2])
        np.testing.assert_array_equal(j,[0,4,2])


if __name__=='__main__':unittest.main()
