import unittest
from fractions import Fraction as F
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from parameter_threshold_transfer import (
    threshold,possible,rational_witness,verify_witness,
    elementary_upper_gap_positive,generate
)

class ParameterThresholdTests(unittest.TestCase):
    def test_sharp_boundary_various_degrees(self):
        for r in range(2,22):
            cut=threshold(r)
            self.assertFalse(possible(r,cut))
            self.assertFalse(possible(r,cut-F(1,1000)))
            self.assertTrue(possible(r,cut+F(1,1000)))
            self.assertIsNone(rational_witness(r,cut))

    def test_exact_constructive_witnesses(self):
        for r in range(2,16):
            for excess in (F(1,1000),F(1,10),F(3,2)):
                nu=threshold(r)+excess
                A,theta=rational_witness(r,nu)
                self.assertTrue(verify_witness(r,nu,A,theta))
                self.assertTrue(elementary_upper_gap_positive(r,A))

    def test_integer_r_equals_two_reproduces_boundary_two(self):
        self.assertEqual(threshold(2),F(2))
        self.assertEqual(threshold(3),F(3,2))
        self.assertEqual(threshold(4),F(4,3))
        for bad in (0,1,-2):
            with self.assertRaises(ValueError):threshold(bad)

    def test_generated_task_gold_and_witness_provenance(self):
        d=generate()
        self.assertEqual(len(d["tasks"]),33)
        self.assertEqual(len(d["gold"]),33)
        self.assertEqual(sum(g["answer"] for g in d["gold"]),11)
        self.assertEqual(d["tasks"][0]["family"],"017")
        self.assertEqual(d["gold"][2]["critical_nu"],"2")

if __name__=="__main__":unittest.main()
