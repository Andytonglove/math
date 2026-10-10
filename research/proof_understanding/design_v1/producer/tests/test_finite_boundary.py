import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from finite_boundary import MAPS,IDENTITY,compose,multiply_masks,enumerate_one_sided_inverse_pairs,transfer_boundary_cards
class FiniteBoundaryTests(unittest.TestCase):
    def test_monoid_multiplication(self):
        eid=MAPS[IDENTITY]
        for f in MAPS:
            self.assertEqual(compose(eid,f),f)
            self.assertEqual(compose(f,eid),f)
        for f in MAPS:
            for g in MAPS:
                for h in MAPS:
                    self.assertEqual(compose(compose(f,g),h),compose(f,compose(g,h)))
    def test_exact_algebra_associative(self):
        for x in range(16):
            for y in range(16):
                for z in range(16):
                    self.assertEqual(multiply_masks(multiply_masks(x,y),z),
                                     multiply_masks(x,multiply_masks(y,z)))
    def test_no_one_sided_defect_in_finite_example(self):
        d=enumerate_one_sided_inverse_pairs()
        self.assertEqual(d['ordered_pairs_examined'],256)
        self.assertTrue(d['all_two_sided'])
        self.assertGreater(len(d['one_sided_inverse_pairs']),0)
    def test_unknown_and_scope_not_falsity(self):
        cards={x['case']:x for x in transfer_boundary_cards()}
        self.assertEqual(cards['source_group_witness']['expected'],'UNKNOWN')
        self.assertEqual(cards['finite_dim_algebra']['expected'],'NO')
        self.assertEqual(cards['infinite_bicyclic_monoid']['expected'],'YES')
    def test_invalid_masks(self):
        with self.assertRaises(ValueError):multiply_masks(-1,0)
        with self.assertRaises(ValueError):multiply_masks(16,0)
if __name__=='__main__':unittest.main()
