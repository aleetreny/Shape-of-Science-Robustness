import unittest
import numpy as np
from sos_analysis.neighbors import exact_neighbors, independent_neighbors, shared_counts


class NeighborTests(unittest.TestCase):
    def test_matches_independent_cosine_and_batch_sizes(self):
        rng = np.random.default_rng(82)
        x = rng.normal(size=(71, 12))
        ids = np.arange(71) * 3 + 10
        a, _ = exact_neighbors(x, ids, k=10, batch_size=1)
        b, _ = exact_neighbors(x, ids, k=10, batch_size=17)
        expected = independent_neighbors(x, ids, x, ids, k=10)
        np.testing.assert_array_equal(a, b)
        np.testing.assert_array_equal(a, expected)
        self.assertFalse((a == ids[:, None]).any())

    def test_large_tie_and_self_not_first(self):
        x = np.ones((12, 5))
        ids = np.asarray([17, 2, 5, 10, 11, 42, 32, 31, 25, 4, 16, 21])
        actual, stats = exact_neighbors(x, ids, k=3, batch_size=4)
        self.assertEqual(stats['boundary_tie_queries_at_max_k'], len(x))
        for row, query in zip(actual, ids):
            np.testing.assert_array_equal(row, np.sort(ids[ids != query])[:3])

    def test_external_queries_and_overlap(self):
        rng = np.random.default_rng(83)
        ref = rng.normal(size=(21, 9)); q = np.vstack([ref[4], rng.normal(size=9)])
        ids = np.arange(21); query_ids = np.array([4, 100])
        actual, _ = exact_neighbors(ref, ids, queries=q, query_ids=query_ids, k=5)
        expected = independent_neighbors(ref, ids, q, query_ids, k=5)
        np.testing.assert_array_equal(actual, expected)
        np.testing.assert_array_equal(shared_counts(actual, actual, 5), [5, 5])
        a = np.array([[1,2,3], [10,11,12]])
        b = np.array([[3,2,4], [4,5,6]])
        np.testing.assert_array_equal(shared_counts(a, b, 3), [2, 0])

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            exact_neighbors(np.ones((3, 2)), [0,0,1], k=1)
        with self.assertRaises(ValueError):
            exact_neighbors(np.ones((3, 2)), [0,1,2], k=3)


if __name__ == '__main__':
    unittest.main()
