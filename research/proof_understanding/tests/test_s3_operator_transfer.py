import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from s3_operator_transfer import audit
class S3Tests(unittest.TestCase):
    def test_complete_basis(self):
        d=audit()
        self.assertEqual(d["pair_count"],4096)
        self.assertEqual(d["operator_basis_equations"],49152)
        self.assertEqual(d["coefficient_recovery_equations"],384)
        self.assertEqual(d["invertible_pairs"],12)
        self.assertEqual(d["one_sided_only_pairs"],0)
        self.assertIsNotNone(d["wrong_orientation_example"])
