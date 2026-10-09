import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bicyclic_monoid_transfer import left,right,compose,verify_prefix,mathematical_certificate

class MonoidTransferTests(unittest.TestCase):
    def test_left_after_right_identity_on_arbitrary_large_prefix(self):
        for n in list(range(300))+[1024,100000,10**9]:
            self.assertEqual(compose(left,right,n),n)

    def test_right_after_left_not_identity(self):
        self.assertEqual(compose(right,left,0),1)
        self.assertEqual(compose(right,left,1),1)
        self.assertNotEqual(compose(right,left,0),0)

    def test_two_distinct_monoid_points_collapse_after_multiplying_R(self):
        # Id*R = R, (R L)*R = R(LR)=R.
        # Point test at n checks equality of these maps in the transformation monoid.
        for n in list(range(100))+[10000]:
            idR=right(n)
            qpR=compose(right,left,right(n))
            self.assertEqual(idR,qpR)
        # Yet Id != R L since at zero they differ.
        self.assertNotEqual(0,compose(right,left,0))

    def test_explicit_configuration_excluded_from_image(self):
        cert=mathematical_certificate()
        self.assertIn("delta_Id",cert["excluded_configuration"])
        self.assertFalse(cert["advanced_source_theorem_verified"])
        self.assertIn("GROUP algebra",cert["source_scope"])

    def test_prefix_and_input_validation(self):
        p=verify_prefix(120)
        self.assertTrue(p["p_times_q_identity_on_prefix"])
        self.assertTrue(p["q_times_p_not_identity_witness_at_0"])
        with self.assertRaises(ValueError):left(-1)
        with self.assertRaises(ValueError):right(-1)
        with self.assertRaises(ValueError):verify_prefix(0)

if __name__=="__main__":unittest.main()
