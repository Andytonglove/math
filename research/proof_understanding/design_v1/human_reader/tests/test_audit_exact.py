"""Public proof-audit development regression tests; not proof certification."""
import json
import sys
import tempfile
import unittest
from fractions import Fraction as F
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "audit_lab" / "audit_cases.py"
sys.path.insert(0, str(MODULE.parent))
import audit_cases as audit


class AuditCardTests(unittest.TestCase):
    def test_9_cards_and_gold_separated(self):
        cards, gold, checks = audit.build_dataset()
        self.assertEqual(len(cards["cases"]), 9)
        self.assertEqual(checks["count_cards"], 9)
        self.assertNotIn("labels", cards)
        self.assertEqual(len(gold["labels"]), 9)
        self.assertEqual(cards["human_outcomes"], "NOT_MEASURED")

    def test_nonconvex_fraction_witness(self):
        a, theta, nu = F(3, 4), F(31, 64), F(39, 20)
        self.assertEqual(audit.nonconvex(a), F(495, 1024))
        self.assertTrue(audit.barrier_ok(audit.nonconvex(a), a, theta, nu))
        self.assertEqual(nu * (a - theta) - (1 - theta), F(3, 1280))

    def test_wrong_inequality_in_true_theorem(self):
        a, theta = F(3, 4), F(5, 8)
        self.assertTrue(a*a < theta < a)
        self.assertFalse(a - theta > a - a*a)
        data = audit.build_dataset()[1]["labels"]["017_true_claim_bad_step"]
        self.assertEqual((data["claim"], data["proof"]), ("LOCALLY_ESTABLISHED", "INVALID_STEP"))

    def test_exact_positive_square(self):
        self.assertTrue(audit.barrier_ok(F(7, 8)**2, F(7, 8), F(25, 32), F(5, 2)))
        self.assertFalse(audit.barrier_ok(F(7, 8)**2, F(7, 8), F(25, 32), F(2)))

    def test_s3_noncommuting_witness(self):
        checks = audit.finite_operator_checks()
        self.assertEqual(checks["s3_associativity_instances"], 216)
        self.assertNotEqual(checks["false_commutation_witness"]["uv"], checks["false_commutation_witness"]["vu"])

    def test_monoid_not_group(self):
        checks = audit.monoid_shift_checks(99)
        self.assertEqual(checks["prefix_checked"], 99)
        self.assertEqual(checks["RL_failure_witness"]["R_L_n"], 1)


if __name__ == "__main__":
    unittest.main()
