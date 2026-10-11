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
    def test_unknown_does_not_become_false(self):
        gold = audit.build_dataset()[1]["labels"]
        for key in ("017_source_main_unknown", "197_group_existence_unknown"):
            self.assertEqual(gold[key]["claim"], "NOT_INDEPENDENTLY_AUDITED")
            self.assertEqual(gold[key]["proof"], "NOT_AUDITED")

    def test_grader_detects_unsupported_certification(self):
        gold = audit.gold_labels()["197_group_existence_unknown"]
        scored = audit.score_labels({"claim": "LOCALLY_ESTABLISHED", "proof": "NOT_AUDITED"}, gold)
        self.assertTrue(scored["unsupported_certification"])
        self.assertFalse(scored["claim_label_correct"])

    def test_grader_distinguishes_false_theorem_from_invalid_proof(self):
        gold = audit.gold_labels()["197_true_claim_bad_step"]
        scored = audit.score_labels({"claim": "EXACTLY_REFUTED", "proof": "INVALID_STEP"}, gold)
        self.assertTrue(scored["proof_label_correct"])
        self.assertTrue(scored["incorrectly_falsified_true_claim_after_gap"])

    def test_bad_response_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid"):
            audit.score_labels({"claim": "MAYBE", "proof": "INVALID_STEP"}, audit.gold_labels()["017_true_claim_bad_step"])

    def test_files_stable_and_no_gold_in_cards(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            d = audit.write_data(p)
            self.assertEqual(d["human_participants"], 0)
            cards = json.loads((p / "cards_public_dev.json").read_text(encoding="utf-8"))
            gold = json.loads((p / "gold_public_dev.json").read_text(encoding="utf-8"))
            checks = json.loads((p / "checks_public_dev.json").read_text(encoding="utf-8"))
            self.assertNotIn("gold", str(cards).lower())
            self.assertIn("labels", gold)
            self.assertEqual(checks["count_cards"], 9)
            with tempfile.TemporaryDirectory() as tmp2:
                q = Path(tmp2)
                audit.write_data(q)
                for name in ("cards_public_dev.json", "gold_public_dev.json", "checks_public_dev.json"):
                    self.assertEqual((p / name).read_bytes(), (q / name).read_bytes())

    def test_no_paid_inference_or_human_scores(self):
        c, g, d = audit.build_dataset()
        self.assertEqual(c["human_outcomes"], "NOT_MEASURED")
        self.assertEqual(g["human_outcomes"], "NOT_MEASURED")
        self.assertEqual(d["human_participants"], 0)


if __name__ == "__main__":
    unittest.main()
