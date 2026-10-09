import unittest,json,copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from artifact_contract_validator import validate

class ArtifactContractsTests(unittest.TestCase):
    def setUp(self):
        path=Path(__file__).resolve().parents[1]/"artifact_contracts_dev_v02.json"
        self.doc=json.loads(path.read_text())

    def test_both_existing_artifacts_are_explicitly_unverified_high_level(self):
        result=validate(self.doc)
        self.assertTrue(result["ok"],result["errors"])
        self.assertEqual(result["development_artifacts_checked"],2)
        self.assertFalse(result["complete_semantic_verification"])

    def test_no_silent_proof_repair(self):
        bad=copy.deepcopy(self.doc)
        bad["artifacts"][0]["no_silent_repair"]=False
        self.assertFalse(validate(bad)["ok"])

    def test_invalid_promotion_from_no_lean_build_fails(self):
        bad=copy.deepcopy(self.doc)
        bad["artifacts"][0]["formal_contract"]["statement_correspondence"]="confirmed"
        self.assertFalse(validate(bad)["ok"])

    def test_missing_obligations_fails(self):
        bad=copy.deepcopy(self.doc)
        bad["artifacts"][1]["obligations"]=[]
        self.assertFalse(validate(bad)["ok"])

if __name__=="__main__":unittest.main()
