import unittest,sys
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from convex_barrier_transfer import FAMILIES,value,slope,critical,certificate,valid,witness,nonconvex,controlled_counterexample,generate

class ConvexBarrierTests(unittest.TestCase):
    def test_square_recovers_017_parameter_gate(self):
        self.assertEqual(critical(FAMILIES[0][1]),F(2))
        self.assertEqual(certificate(FAMILIES[0][1]),[F(1)])
    def test_same_endpoint_derivative_not_same_polynomial(self):
        self.assertEqual(critical(FAMILIES[2][1]),F(3,2))
        self.assertEqual(critical(FAMILIES[3][1]),F(3,2))
        self.assertEqual(critical(FAMILIES[4][1]),F(13,9))
    def test_exact_positive_certificate(self):
        for _,terms in FAMILIES:
            s=slope(terms);coeff=certificate(terms)
            self.assertTrue(all(c>=0 for c in coeff))
            for x in (F(1,7),F(1,3),F(3,4),F(99,100)):
                q=sum((c*x**k for k,c in enumerate(coeff)),F(0))
                self.assertGreater(q,0)
                self.assertEqual(value(terms,x)-s*x+s-1,(1-x)**2*q)
    def test_boundary_and_witness(self):
        for _,terms in FAMILIES:
            b=critical(terms)
            for e in (F(1,1000),F(1,20)):
                self.assertIsNone(witness(terms,b-e))
                self.assertIsNone(witness(terms,b))
                a,t=witness(terms,b+e)
                self.assertTrue(valid(value(terms,a),b+e,a,t))
    def test_nonconvex_invalidates_derivative_only_rule(self):
        c=controlled_counterexample()
        self.assertEqual(c["f(A)"],"495/1024")
        self.assertEqual(c["gap"],"3/1280")
        self.assertTrue(valid(nonconvex(F(3,4)),F(39,20),F(3,4),F(31,64)))
    def test_development_generator(self):
        d=generate()
        self.assertEqual(d,generate())
        self.assertEqual(d["meta"]["count"],23)
        self.assertEqual(d["meta"]["positives"],9)
        self.assertEqual(len(set(t["id"] for t in d["tasks"])),23)
        self.assertEqual([t["id"] for t in d["tasks"]],[g["id"] for g in d["gold"]])
        self.assertTrue(all(len(t["id"])==16 for t in d["tasks"]))
    def test_reject_invalid_mixture(self):
        for terms in ([],[(2,F(1,2))],[(1,F(1))],[(3,F(-1))]):
            with self.assertRaises(ValueError):value(terms,F(1,2))
