import unittest
import numpy as np
from sos_deep.medicine_composition import eligible_groups,select


class MedicineTests(unittest.TestCase):
    def test_eligibility_time_quotas_balancing_and_single_group_identity(self):
        cells={('A',0):list(range(0,40)),('B',0):list(range(40,50)),('C',0):[50],
               ('A',1):list(range(100,140)),('B',1):list(range(140,150)),('C',1):[150]}
        groups=eligible_groups(cells,[0,1],10);self.assertEqual(groups,['A','B'])
        a,b=select(cells,groups,27,0,[0,1],[10,10])
        self.assertEqual(len(a),20);self.assertEqual(len(set(b)),20)
        self.assertEqual(int((b<40).sum()),5);self.assertEqual(int(((b>=40)&(b<100)).sum()),5)
        c,d=select(cells,['A'],27,0,[0,1],[10,10]);np.testing.assert_array_equal(c,d)


if __name__=='__main__':unittest.main()
