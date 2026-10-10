"""Tests for scope/provenance refusal. All fixtures are public development."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_guides import check_contracts, inspect_repo, REQUIRED_HEADINGS, REQUIRED_DISCLOSURES


P = {"gate": {"status": "PASSED_SCOPED"},
     "source": {"sha256": "x", "required_anchors": {"eq:ca-operator": {"line": 1}}},
     "claims": [{"id": id} for id in (
         "right_homomorphism", "faithful", "split_injective", "image", "non_surjective")],
     "unresolved": ["high-level GROUP construction not verified"]}
B = {"proof_obligations": [{"id": id, "status": "independently_derived"}
                           for id in ("O1", "O2", "O3")]
                           + [{"id": "O4", "status": "unverified_out_of_scope"}],
     "artifact_provenance": {"source_advanced_theorem_verified": False},
     "boundaries": ["counterexample"], "unknowns": ["source theorem not checked"]}
HEADER = "\n".join((*REQUIRED_HEADINGS, *REQUIRED_DISCLOSURES))
GUIDE197 = HEADER + "\n" + "\n".join(f"<!-- proof-ref: {id} -->" for id in
                           ("right_homomorphism", "faithful", "split_injective", "image", "non_surjective"))
GUIDE017 = HEADER + "\n" + "\n".join(f"<!-- obligation-ref: {id} -->" for id in ("O1", "O2", "O3"))


class GuideGateTests(unittest.TestCase):
    def verify(self, p=None, b=None, a=None, c=None, source=None):
        return check_contracts(p if p is not None else P,
                               b if b is not None else B,
                               a if a is not None else GUIDE197,
                               c if c is not None else GUIDE017,
                               source_bytes=source)

    def test_positive_development_fixture(self):
        result = self.verify()
        self.assertFalse(result["human_outcomes_measured"])
        self.assertEqual(len(result["source197_claim_refs"]), 5)

    def test_blocked_source_refused(self):
        p = copy.deepcopy(P); p["gate"]["status"] = "BLOCKED"
        with self.assertRaisesRegex(ValueError, "gate"):
            self.verify(p=p)

    def test_missing_claim_refused(self):
        p = copy.deepcopy(P); p["claims"].pop()
        with self.assertRaisesRegex(ValueError, "conditional claims"):
            self.verify(p=p)

    def test_missing_unverified_disclosure_refused(self):
        with self.assertRaisesRegex(ValueError, "disclosure"):
            self.verify(a=GUIDE197.replace("原始论文主定理没有在本项目得到独立验证", ""))

    def test_missing_reader_claim_refused(self):
        with self.assertRaisesRegex(ValueError, "omits"):
            self.verify(a=GUIDE197.replace("<!-- proof-ref: image -->", ""))

    def test_unknown_claim_refused(self):
        with self.assertRaisesRegex(ValueError, "absent producer claim"):
            self.verify(a=GUIDE197 + "\n<!-- proof-ref: advanced_unproved -->")

    def test_source_hash_mismatch_refused(self):
        with self.assertRaisesRegex(ValueError, "SHA|hash"):
            self.verify(source=b"modified TeX")

    def test_unverified_017_cannot_be_promoted(self):
        with self.assertRaisesRegex(ValueError, "unverified obligation"):
            self.verify(c=GUIDE017 + "\n<!-- obligation-ref: O4 -->")

    def test_017_proof_tier_loss_refused(self):
        b = copy.deepcopy(B); b["proof_obligations"][0]["status"] = "source_only"
        with self.assertRaisesRegex(ValueError, "evidence tier"):
            self.verify(b=b)

    def test_017_main_theorem_not_certified(self):
        b = copy.deepcopy(B); b["artifact_provenance"]["source_advanced_theorem_verified"] = True
        with self.assertRaisesRegex(ValueError, "unverified"):
            self.verify(b=b)

    def test_live_repository_guides(self):
        repo = Path(__file__).resolve().parents[5]
        r = inspect_repo(repo, require_original=False)
        self.assertEqual(len(r["source017_obligation_refs"]), 3)


if __name__ == "__main__":
    unittest.main()
