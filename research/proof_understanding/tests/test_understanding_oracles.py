import unittest
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from understanding_oracles import (
    xor_translation_assignment,exact_unique_game_value,
    cyclic_gf2_product,enumerate_one_sided_pairs,shift_left,shift_right,example_games
)


class UnderstandingOracleTests(unittest.TestCase):
    def test_translation_constraints_on_valid_and_broken_cycle(self):
        games=example_games()
        sat,labels=xor_translation_assignment(4,2,games['consistent'])
        self.assertTrue(sat)
        self.assertEqual(len(labels),4)
        unsat,labels=xor_translation_assignment(4,2,games['one_edge_perturbed'])
        self.assertFalse(unsat)
        self.assertIsNone(labels)

    def test_exhaustive_game_value(self):
        games=example_games()
        self.assertEqual(exact_unique_game_value(4,2,games['consistent']),Fraction(1))
        self.assertEqual(exact_unique_game_value(4,2,games['one_edge_perturbed']),Fraction(3,4))

    def test_xor_disconnected_components_and_bad_arguments(self):
        yes,lab=xor_translation_assignment(5,2,[(0,1,3),(3,4,1)])
        self.assertTrue(yes);self.assertEqual(lab,[0,3,0,0,1])
        with self.assertRaises(ValueError):
            xor_translation_assignment(2,2,[(0,1,9)])
        with self.assertRaises(ValueError):
            exact_unique_game_value(5,5,[(0,1,1)],max_labelings=100)

    def test_finite_group_algebra_products_are_directly_finite_in_small_models(self):
        for n in range(1,7):
            with self.subTest(order=n):
                count,violations=enumerate_one_sided_pairs(n)
                self.assertGreater(count,0)
                self.assertEqual(violations,0)
        self.assertEqual(cyclic_gf2_product(3,2,2),4)  # g*g = g^2 in C_3
        self.assertEqual(cyclic_gf2_product(3,2,4),1)  # g*g^2 = identity

    def test_infinite_dimensional_one_sided_inverse_shift(self):
        for x in range(0,128):
            self.assertEqual(shift_left(shift_right(x)),x)
            self.assertEqual(shift_right(shift_left(x)),x & ~1)
        self.assertNotEqual(shift_right(shift_left(1)),1)

    def test_oracle_invalid_inputs(self):
        with self.assertRaises(ValueError):cyclic_gf2_product(0,1,1)
        with self.assertRaises(ValueError):enumerate_one_sided_pairs(20)
        with self.assertRaises(ValueError):shift_right(-1)
        with self.assertRaises(ValueError):shift_left(-1)


if __name__=='__main__':unittest.main()
