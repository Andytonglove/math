import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contract_audit import mul,audit,regularity_case,existence_case,extra_dependency_case

class SemanticContractTests(unittest.TestCase):
    def setUp(self):
        self.fixtures=Path(__file__).resolve().parents[1]/"cases_v0.json"

    def test_polynomial_expansion(self):
        p=[1,-1,-1,1]
        wrong=mul([-1,1],[1,2,1])
        correct=mul([1,-2,1],[1,1])
        self.assertNotEqual(wrong,p)
        self.assertEqual(correct,p)
        self.assertEqual((p[0],wrong[0]),(1,-1))

    def test_weak_estimate_cannot_imply_strong_regular_bound_by_itself(self):
        case={"natural_language_derivative_loss":4,
              "formal_derivative_loss":5,"expected":"formal_requires_higher_input_regularity"}
        r=regularity_case(case)
        self.assertEqual(r["finding"],case["expected"])
        self.assertEqual(r["exact_certificate"]["generic_derivative_operator_countermodel"]["higher_derivative_magnitudes"],[2,3,5,11])
        self.assertIn("not original NS inverse operator",r["verified_scope"])

    def test_unmet_presupposition_is_proven_symbolically(self):
        r=existence_case({"finite_samples":101,"expected":"existence_presupposition_is_false"})
        self.assertEqual(r["finding"],"existence_presupposition_is_false")
        self.assertEqual(r["exact_certificate"]["finite_root_checks"],101)
        self.assertIn("for every natural n",r["exact_certificate"]["symbolic_witness"])

    def test_additional_rhs_dependency_not_misreported_as_logical_implication(self):
        case={"nl_rhs_dependencies":["B","R"],"formal_rhs_dependencies":["A","B","R"],
              "expected":"formal_adds_rhs_dependencies"}
        r=extra_dependency_case(case)
        self.assertEqual(r["exact_certificate"]["additional_formal_symbols"],["A"])
        self.assertIn("UNDETERMINED",r["verified_scope"])

    def test_full_fixture_all_cases_scoped(self):
        import json
        data=json.loads(self.fixtures.read_text())
        r=audit(data)
        self.assertEqual(r["cases_checked"],5)
        self.assertEqual(r["semantic_equivalence_of_full_NL_and_Lean"],"NOT_ESTABLISHED")
        self.assertEqual(r["model_inference_runs"],0)
        self.assertEqual(len({c["id"] for c in r["cases"]}),5)

    def test_unknown_contract_not_guessed(self):
        with self.assertRaises(ValueError):
            audit({"cases":[{"id":"new","kind":"arbitrary_NL","expected":"equivalent"}]})

if __name__=="__main__":
    unittest.main()
