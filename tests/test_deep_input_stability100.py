import unittest
from sos_deep.input_stability100 import summarize


class StabilityTests(unittest.TestCase):
    def test_cross_zero_is_separate_from_sampling_alert(self):
        r=summarize([-0.005,0.005]*50,0)
        self.assertTrue(r['crosses_zero']);self.assertTrue(r['passes_operational_screen'])
        self.assertEqual(r['fraction_positive'],0.5)
        r=summarize([0.1,0.2]*50,0.15)
        self.assertFalse(r['passes_operational_screen']);self.assertFalse(r['crosses_zero'])


if __name__=='__main__':unittest.main()
