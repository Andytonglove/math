import itertools
import unittest
from fractions import Fraction
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from parameter_oracle import construct, checks, minimum_pairwise_collisions, collision_scaling_example, InfeasibleParameter


class TestParameterOracle(unittest.TestCase):
    def test_exact_rational_witnesses(self):
        for nu in [Fraction(2001, 1000), Fraction(9, 4), Fraction(5, 2),
                   Fraction(3), Fraction(4), Fraction(7), Fraction(100)]:
            with self.subTest(nu=str(nu)):
                w = construct(nu)
                self.assertTrue(all(checks(w).values()))
                self.assertEqual(w["g"], (nu * (w["A"] - w["theta"]) - (1 - w["theta"])) / 2)

    def test_boundary_rejected(self):
        for nu in [Fraction(-1), Fraction(0), Fraction(1), Fraction(19, 10), Fraction(2)]:
            with self.subTest(nu=str(nu)):
                with self.assertRaises(InfeasibleParameter):
                    construct(nu)

    def test_balanced_collision_minimum_matches_bruteforce(self):
        for bins in range(1, 5):
            for n in range(0, 10):
                brute = min(sum(k * (k - 1) // 2 for k in occupancy)
                            for occupancy in itertools.product(range(n + 1), repeat=bins)
                            if sum(occupancy) == n)
                self.assertEqual(minimum_pairwise_collisions(n, bins), brute, (n, bins))


    def test_quadratic_vs_linear_collision_normalization(self):
        # With M=H^2, D=H and half the rows assigned to low groups,
        # balanced occupancies give a fixed 1/4 normalized quadratic
        # contribution, whereas any linear total-M penalty is 1/H.
        for H in (4,8,16,32):
            with self.subTest(H=H):
                result=collision_scaling_example(H,m=1)
                self.assertEqual(result["normalized_quadratic_saving"],"1/4")
                self.assertEqual(result["normalized_linear_saving"],str(Fraction(1,H)))
        with self.assertRaises(ValueError):
            collision_scaling_example(3,m=1)

    def test_collision_invalid_inputs(self):
        for n, b in [(-1, 1), (0, 0), (2, -1)]:
            with self.assertRaises(ValueError):
                minimum_pairwise_collisions(n, b)


if __name__ == "__main__":
    unittest.main()
