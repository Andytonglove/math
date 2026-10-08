import unittest
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from determinant_surgery import (random_base,surgeries,classify,independent_oracle,
    normalized_bounds,make_dataset,sanity_baselines,MODES)

class ProofSurgeryTests(unittest.TestCase):
    def test_math_oracles_agree_on_all_interventions(self):
        for seed in range(120):
            for mode,x in surgeries(random_base(seed)).items():
                with self.subTest(seed=seed,mode=mode):
                    self.assertEqual(classify(x),independent_oracle(x))

    def test_six_way_surgery_and_boundary_equality(self):
        changes=surgeries(random_base(10))
        expected={"unmodified":"BOTH","weaken_collision":"ONLY_APPROX",
            "weaken_approx":"ONLY_COLLISION","weaken_both":"NEITHER",
            "tie_collision":"ONLY_APPROX","tie_approx":"ONLY_COLLISION"}
        self.assertEqual({k:classify(v) for k,v in changes.items()},expected)
        lo,c,a=normalized_bounds(changes["tie_collision"])
        self.assertEqual(lo,c)
        lo,c,a=normalized_bounds(changes["tie_approx"])
        self.assertEqual(lo,a)

    def test_balance_and_repeatability(self):
        data=make_dataset(1703,12)
        self.assertEqual(data,make_dataset(1703,12))
        self.assertEqual(len(data["gold"]),72)
        self.assertEqual(len(data["prompts"]),72*len(MODES))
        self.assertEqual(Counter(r["answer"] for r in data["gold"]),
                         {"BOTH":12,"ONLY_COLLISION":24,"ONLY_APPROX":24,"NEITHER":12})

    def test_visible_prompts_do_not_expose_gold(self):
        data=make_dataset(17,3)
        self.assertEqual(len({r["id"] for r in data["gold"]}),18)
        for r in data["prompts"]:
            self.assertNotIn("answer",r)
            self.assertNotIn("surgery",r)
            self.assertNotIn("bounds",r)
            self.assertIn("Uc=En-C",r["prompt"])
        self.assertEqual(len([r for r in data["prompts"] if r["condition"]=="minimal"]),18)

    def test_oracle_baseline_and_incorrect_or_baseline(self):
        base=sanity_baselines(make_dataset(1908,12)["gold"])
        self.assertEqual(base["exact_AND"],{"correct":72,"total":72})
        self.assertEqual(base["invalid_OR_shortcut"],{"correct":24,"total":72})
        self.assertIn("NOT language model",base["notice"])

    def test_invalid_base_counts(self):
        for n in (0,1001):
            with self.assertRaises(ValueError):make_dataset(bases=n)

if __name__=="__main__":unittest.main()
