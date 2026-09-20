"""Known-case tests for the descriptive decision rules, not scientific claims."""
import unittest
import numpy as np
from .analyze import relative_difference, persistent_direction, classify, count_classes


class DirectionRules(unittest.TestCase):
    def test_all_agree_and_partial_agreement(self):
        s = persistent_direction([[.2, .1], [.3, .2], [.1, .2]])
        self.assertEqual(str(classify(s)), 'unanimous')
        self.assertEqual(str(classify([1, 1, 0])), 'unresolved')

    def test_opposite_persistent_models(self):
        self.assertEqual(str(classify([1, -1, 0, 0])), 'contradiction')

    def test_one_bad_draw_prevents_persistence(self):
        self.assertEqual(int(persistent_direction([.1] * 24 + [-.001])), 0)
        self.assertEqual(int(persistent_direction([.1, 0.])), 0)

    def test_small_but_stable_is_separate_from_magnitude(self):
        self.assertEqual(int(persistent_direction([.003, .004])), 1)
        self.assertEqual(int(persistent_direction([.003, .004], .01)), 0)
        self.assertEqual(int(persistent_direction([-.06, -.07], .05)), -1)

    def test_boundary_and_roundoff(self):
        self.assertEqual(int(persistent_direction([.05, .08], .05)), 0)
        self.assertEqual(int(persistent_direction([1e-12, 2e-12])), 0)

    def test_swapping_fields_changes_sign_not_class(self):
        a = np.array([10., 12., 3.]); b = np.array([12., 9., 4.])
        np.testing.assert_allclose(relative_difference(a, b), -relative_difference(b, a))
        s = persistent_direction(relative_difference(a, b)[:, None])
        self.assertEqual(str(classify(s)), str(classify(-s)))

    def test_units_do_not_change_relative_difference(self):
        np.testing.assert_allclose(relative_difference([3, 4], [6, 5]),
                                   relative_difference([30, 40], [60, 50]))

    def test_permuting_models_changes_nothing(self):
        s = np.array([[1, -1, 0], [1, 1, 1], [0, 1, 1]])
        np.testing.assert_array_equal(classify(s), classify(s[:, [2, 0, 1]]))
        self.assertEqual(count_classes(s), {'unanimous': 1, 'contradiction': 1, 'unresolved': 1, 'pairs': 3, 'models': 3})

    def test_threshold_can_only_remove_directions(self):
        rng = np.random.default_rng(124)
        x = rng.normal(.02, .05, (50, 10, 3))
        lo = persistent_direction(x)
        hi = persistent_direction(x, .05)
        self.assertTrue(np.all((hi == 0) | (hi == lo)))

    def test_invalid_inputs_are_not_silent_ties(self):
        for x in [[], [np.nan], [np.inf]]:
            with self.assertRaises(ValueError): persistent_direction(x)
        with self.assertRaises(ValueError): relative_difference([0], [1])
        with self.assertRaises(ValueError): classify([2, 1])

    def test_same_witnesses_required(self):
        original = np.array([1, -1, 0, 0])
        changed = np.array([0, 0, 1, -1])
        retained = np.where(original == changed, original, 0)
        self.assertEqual(str(classify(changed)), 'contradiction')
        self.assertEqual(str(classify(retained)), 'unresolved')


if __name__ == '__main__':
    unittest.main()
