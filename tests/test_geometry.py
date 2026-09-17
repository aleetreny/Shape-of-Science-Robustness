import unittest
import numpy as np
from scipy.stats import spearmanr

from sos_analysis.geometry import (shape_scores, sample_pairs, rsa_scores,
                                   streamed_moments, centered_moments)


def direct_unbiased_hsic(x, y):
    k, l = x @ x.T, y @ y.T
    np.fill_diagonal(k, 0)
    np.fill_diagonal(l, 0)
    n = len(x)
    return ((k * l).sum() + k.sum() * l.sum() / ((n-1)*(n-2)) -
            2 * np.dot(k.sum(0), l.sum(0)) / (n-2)) / (n*(n-3))


class GeometryTests(unittest.TestCase):
    def test_feature_formula_matches_independent_gram_formula(self):
        rng = np.random.default_rng(12)
        x = rng.normal(size=(37, 11)) + 30
        y = rng.normal(size=(37, 7)) - 7
        expected = direct_unbiased_hsic(x, y) / np.sqrt(direct_unbiased_hsic(x, x) * direct_unbiased_hsic(y, y))
        got = shape_scores([x, y], normalize=False)[0]
        self.assertAlmostEqual(expected, got['cka_debiased'], places=9)

    def test_rigid_shape_invariance_and_different_dimensions(self):
        rng = np.random.default_rng(13)
        x = rng.normal(size=(80, 12))
        q = np.linalg.qr(rng.normal(size=(12, 12)))[0]
        y = np.pad(3 * x @ q + 5, ((0, 0), (0, 3)))
        result = shape_scores([x, y], normalize=False)[0]
        self.assertAlmostEqual(result['cka_debiased'], 1, places=12)
        self.assertAlmostEqual(result['procrustes_similarity'], 1, places=12)
        self.assertLess(result['procrustes_angle_degrees'], 0.00001)

    def test_shuffled_correspondence_is_not_same_labeled_shape(self):
        rng = np.random.default_rng(14)
        x = rng.normal(size=(300, 10))
        out = shape_scores([x, x[rng.permutation(len(x))]], normalize=False)[0]
        self.assertLess(abs(out['cka_debiased']), .03)
        self.assertLess(out['procrustes_similarity'], .25)

    def test_bias_correction_on_unrelated_high_dimensional_data(self):
        rng = np.random.default_rng(15)
        x, y = rng.normal(size=(2, 100, 500))
        out = shape_scores([x, y], normalize=False, procrustes=False)[0]
        self.assertGreater(out['cka_biased'], .75)
        self.assertLess(abs(out['cka_debiased']), .04)

    def test_streaming_matches_direct(self):
        rng = np.random.default_rng(16)
        arrays = [rng.normal(size=(73, 8)), rng.normal(size=(73, 5))]
        get = lambda name, ids: arrays[int(name)][ids]
        streamed = streamed_moments(get, np.arange(73), ['0', '1'], [8, 5], normalize=False, chunk=13)
        direct = centered_moments(arrays)
        for a, b in zip(streamed, direct):
            np.testing.assert_allclose(a, b, atol=1e-10, rtol=1e-12)

    def test_pairs_unique_and_rsa_matches_scipy(self):
        a, b = sample_pairs(10, 1000, 17)
        self.assertEqual(len(a), 45)
        self.assertTrue(np.all(a < b))
        self.assertEqual(len(set(zip(a, b))), 45)
        rng = np.random.default_rng(18)
        arrays = [rng.normal(size=(10, 5)), rng.normal(size=(10, 3))]
        arrays = [x / np.linalg.norm(x, axis=1)[:, None] for x in arrays]
        result = rsa_scores(lambda name, ids: arrays[int(name)][ids], np.arange(10), ['0','1'], count=1000, seed=17)
        expected = spearmanr(1-(arrays[0][a]*arrays[0][b]).sum(1), 1-(arrays[1][a]*arrays[1][b]).sum(1)).statistic
        self.assertAlmostEqual(result[('0','1')], expected, places=12)

    def test_degenerate_input_fails(self):
        with self.assertRaises(ValueError):
            shape_scores([np.ones((10, 2)), np.ones((10, 3))], normalize=False)


if __name__ == '__main__':
    unittest.main()
