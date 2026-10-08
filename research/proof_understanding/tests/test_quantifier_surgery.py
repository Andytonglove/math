import unittest
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from quantifier_surgery import (truth,alternate_truth,generate_case,
                                 build,CASES,MODES)

class QuantifierSurgeryTests(unittest.TestCase):
    def test_expected_motifs(self):
        expected={"uniform":"111","parameter_dependent":"011",
                  "input_dependent":"001","missing_input":"000"}
        for i in range(20):
            for kind in CASES:
                t=generate_case(i,kind)
                self.assertEqual(truth(t),expected[kind])
                self.assertEqual(truth(t),alternate_truth(t))

    def test_strong_implies_original_implies_weak(self):
        for i in range(200):
            for kind in CASES:
                label=truth(generate_case(i*17,kind))
                self.assertIn(label,("111","011","001","000"))

    def test_balanced_dataset_and_no_answer_leakage(self):
        d=build(seed=3,bases=11)
        self.assertEqual(Counter(x["answer"] for x in d["gold"]),
                         {"111":11,"011":11,"001":11,"000":11})
        self.assertEqual(len(d["prompts"]),44*len(MODES))
        self.assertTrue(all("answer" not in x and "case_kind" not in x
                            for x in d["prompts"]))

    def test_reproducibility_and_invalid_size(self):
        self.assertEqual(build(22,3),build(22,3))
        for n in (0,1001):
            with self.assertRaises(ValueError):build(bases=n)

if __name__=="__main__":unittest.main()
