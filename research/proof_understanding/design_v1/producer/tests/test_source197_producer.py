import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from source197_producer import SOURCE_REL,produce,symbolic_word_checks

# Synthetic fixture: validates recognizer mutations; never count as a real-paper test.
MOCK = r'''
\begin{equation}\label{eq:ca-operator}(T_cx)(g)=\sum_{u\in G}c_u x(gu).\end{equation}
\begin{equation}\label{eq:ca-composition}T_c\circ T_d=T_{cd}\end{equation}
\begin{equation}\label{eq:ca-coefficient}(T_c\delta_h)(1_G)=c_h\end{equation}
\begin{equation}\label{eq:ca-image}\im(\tau)=\{y\in K^G:T_{ba}y=y\}\end{equation}
\begin{equation}\label{eq:ca-leftinverse}T_a\circ\tau=T_{ab}=T_1\end{equation}
\begin{lemma}\label{lem:ca-representation}For every field $K$ and group $G$, the assignment works.\end{lemma}
\begin{proof}\sum_u c_u\sum_v d_vx(guv), so T_cd.\end{proof}
\begin{proposition}\label{prop:ca-transfer}Let $K$ be a finite field, $G$ a group, and $a,b\in K[G]$ satisfy $ab=1$. If $ba\ne1$ then non-surjective.\end{proposition}
\begin{proof}If $(ba-1)_h\ne0$ then delta_h is excluded.\end{proof}
'''

class ProducerTests(unittest.TestCase):
    def test_synthetic_positive_gate(self):
        artifact=produce(MOCK,'synthetic fixture')
        self.assertEqual(artifact['gate']['status'],'PASSED_SCOPED',artifact['gate']['failures'])
        self.assertEqual(len(artifact['claims']),5)
        self.assertEqual(artifact['transfer']['target_carrier'],'unital associative monoid')
        self.assertIn('not independently verified',artifact['unresolved'][0])

    def test_right_left_mutation_blocks(self):
        a=produce(MOCK.replace('x(gu)','x(ug)'))
        self.assertEqual(a['gate']['status'],'BLOCKED')
        self.assertEqual(a['claims'],[])
        self.assertIn('SOURCE_CONTRACT_MISMATCH:operator_right_neighbor',a['gate']['failures'])

    def test_reversed_product_mutation_blocks(self):
        a=produce(MOCK.replace('T_{cd}','T_{dc}'))
        self.assertEqual(a['claims'],[])
        self.assertIn('SOURCE_CONTRACT_MISMATCH:source_homomorphism_order',a['gate']['failures'])

    def test_falsified_proof_does_not_silently_repair(self):
        a=produce(MOCK.replace('d_vx(guv)','d_vx(gvu)'))
        self.assertEqual(a['gate']['status'],'BLOCKED')
        self.assertIn('PROOF_STEP_UNVERIFIED:ordered_right_expansion',a['gate']['failures'])

    def test_missing_premise_blocks(self):
        a=produce(MOCK.replace('$ab=1$. If','$ba=1$. If'))
        self.assertIn('PROPOSITION_PREMISE_MISSING:one_sided_inverse_premise',a['gate']['failures'])

    def test_missing_finite_field_for_CA_blocks(self):
        a=produce(MOCK.replace('a finite field','an arbitrary field'))
        self.assertIn('PROPOSITION_PREMISE_MISSING:finite_alphabet_premise',a['gate']['failures'])

    def test_nonzero_defect_proof_removed_blocks(self):
        a=produce(MOCK.replace('If $(ba-1)_h\\ne0$ then delta_h is excluded.', 'We claim it is clear.'))
        self.assertIn('PROOF_STEP_UNVERIFIED:nonzero_defect_witness',a['gate']['failures'])

    def test_word_calculus(self):
        a=symbolic_word_checks()
        self.assertEqual(a['right_composition'],['g','u','v'])
        self.assertEqual(a['left_anti_composition'],['v','u','g'])
        self.assertEqual(a['left_right_commutation'],['v','g','u'])

    def test_real_source_if_present(self):
        root=Path(__file__).resolve().parents[5]
        original=root / SOURCE_REL
        if not original.exists():
            self.skipTest('original manuscript not in this shallow local checkout')
        a=produce(original.read_text(encoding='utf-8'),str(original))
        self.assertEqual(a['gate']['status'],'PASSED_SCOPED',a['gate']['failures'])
        self.assertEqual(len(a['claims']),5)

if __name__=='__main__':unittest.main()
