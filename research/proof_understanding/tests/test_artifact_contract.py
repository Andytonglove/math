import json,sys,unittest
from pathlib import Path
from fractions import Fraction as F
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"scripts"))
from convex_barrier_transfer import nonconvex,valid,local_threshold

class ManualArtifactContractTests(unittest.TestCase):
    def test_claims_status_and_evidence(self):
        p=BASE/"design_v1/artifacts/017_rational_barrier_dev_v01.json"
        d=json.loads(p.read_text())
        for field in ("artifact_id","claim_contract","mechanism","proof_obligations",
                      "boundaries","reusable_results","evidence","unknowns","artifact_provenance"):
            self.assertIn(field,d)
        self.assertFalse(d["artifact_provenance"]["source_advanced_theorem_verified"])
        self.assertEqual(d["artifact_provenance"]["eval_visibility"],
                         "public development; tests known before artifact freeze")
        self.assertTrue(any(o["status"]=="unverified_out_of_scope" for o in d["proof_obligations"]))
        self.assertTrue(d["unknowns"])
    def test_adversarial_witness_and_global_boundary(self):
        d=json.loads((BASE/"design_v1/artifacts/017_rational_barrier_dev_v01.json").read_text())
        a,t,nu=F(3,4),F(31,64),F(39,20)
        self.assertTrue(valid(nonconvex(a),nu,a,t))
        self.assertEqual(local_threshold(nonconvex(a),a),F(529,273))
        self.assertIn("3/1280",str(d["boundaries"]))
