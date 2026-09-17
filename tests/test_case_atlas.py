import unittest
import numpy as np
from sos_review.case_atlas import anchor_counts, rank_centers


class CaseAtlasTests(unittest.TestCase):
    def test_edges_ignore_non_anchor_candidates_and_preserve_rank_cutoffs(self):
        q = np.array([[10, 30, 90]])
        n = np.empty((2, 1, 3, 50), dtype=int)
        for rep in range(2):
            for source in range(3):
                n[rep, 0, source] = np.arange(100, 150)
        n[0, 0, 0, 0] = 30
        n[1, 0, 0, 12] = 30
        n[1, 0, 0, 40] = 90
        got = anchor_counts(n, q)
        np.testing.assert_array_equal(got[0, 0, 1], [1, 2, 2])
        np.testing.assert_array_equal(got[0, 0, 2], [0, 0, 1])
        self.assertEqual(int(got.sum()), 6)

    def test_center_ranks_normalize_exclude_self_and_break_ties_by_id(self):
        x = np.array([[2, 0], [3, 0], [0, 1]], dtype=float)
        got = rank_centers(x, np.array([20, 10, 30]))
        np.testing.assert_array_equal(got, [[3, 1, 2], [1, 3, 2], [2, 1, 3]])


if __name__ == '__main__':
    unittest.main()
