"""Conservative, source-grounded TeX -> evidence contract for 197 local transfer.

This is a deliberately narrow deterministic producer, not an LLM and NOT a
semantic decision procedure. It refuses source variants whose proof lines
or hypotheses no longer match its independently recorded algebraic derivation.
It never certifies the advanced group-algebra witness or Lean equivalence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

SOURCE_REL = ('preprints/A-Counterexample-to-Kaplanskys-Direct-Finiteness-'
              'Conjecture-in-Characteristic-Two-September-23-2026/build/'
              'sections/06-cellular-automata.tex')
REQUIRED_EQUATIONS = ('eq:ca-operator', 'eq:ca-composition', 'eq:ca-coefficient',
                      'eq:ca-image', 'eq:ca-leftinverse')


def compact(text: str) -> str:
    # No attempt to expand TeX macros. Strip comments and ASCII whitespace only.
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    return re.sub(r'\s+', '', text)


def environment(source: str, kind: str, anchor: str) -> tuple[str, int] | None:
    for match in re.finditer(r'\\begin\{' + re.escape(kind) +
                             r'\}(.*?)\\end\{' + re.escape(kind) + r'\}',
                             source, re.DOTALL):
        if '\\label{' + anchor + '}' in match.group(1):
            return match.group(0), match.start()
    return None


def equation(source: str, label: str) -> tuple[str, int] | None:
    pattern = r'\\begin\{equation\}(.*?)\\end\{equation\}'
    for match in re.finditer(pattern, source, re.DOTALL):
        if '\\label{' + label + '}' in match.group(1):
            return match.group(1), match.start()
    return None


def symbolic_word_checks() -> dict:
    """Check normalized associative words, NOT arbitrary theorem semantics.

    Each tuple represents the order of factors indexing x. Finite sums and
    commutative coefficient multiplication are mathematical premises, not
    machine-proved here. This is a check of the indexed monoid-word step.
    """
    right_nested = ('g', 'u', 'v')
    right_product = ('g',) + ('u', 'v')
    left_nested = ('v', 'u', 'g')
    left_reverse_product = ('v', 'u') + ('g',)
    right_left = ('v', 'g', 'u')
    left_right = ('v',) + ('g', 'u')
    assert right_nested == right_product
    assert left_nested == left_reverse_product
    assert right_left == left_right
    return {'right_composition': list(right_nested),
            'left_anti_composition': list(left_nested),
            'left_right_commutation': list(right_left),
            'certificate_scope': 'free-monoid index words; coefficients and finite sums assumed'}


def produce(source: str, source_path: str = SOURCE_REL) -> dict:
    """Generate a conservative partial mathematical abstraction from raw TeX.

    Always return an explicit blocked artifact for unrecognized changes.
    Its reusable claims remain EMPTY when any required source gate fails.
    """
    digest = hashlib.sha256(source.encode('utf-8')).hexdigest()
    failures: list[str] = []
    anchors = {}
    for label in REQUIRED_EQUATIONS:
        entry = equation(source, label)
        if entry is None:
            failures.append('MISSING_EQUATION:' + label)
        else:
            body, start = entry
            anchors[label] = {'line': source.count('\n', 0, start)+1,
                              'sha256': hashlib.sha256(body.encode('utf-8')).hexdigest()}
    lemma = environment(source, 'lemma', 'lem:ca-representation')
    proposition = environment(source, 'proposition', 'prop:ca-transfer')
    if lemma is None:
        failures.append('MISSING_LEMMA:lem:ca-representation')
    else:
        anchors['lem:ca-representation'] = {'line':source.count('\n', 0, lemma[1])+1}
    if proposition is None:
        failures.append('MISSING_PROPOSITION:prop:ca-transfer')
    else:
        anchors['prop:ca-transfer'] = {'line':source.count('\n', 0, proposition[1])+1}

    checks = {
        'operator_right_neighbor': ('c_ux(gu)', 'eq:ca-operator'),
        'source_homomorphism_order': ('T_c\\circT_d=T_{cd}', 'eq:ca-composition'),
        'delta_coefficient_recovery': ('(T_c\\delta_h)(1_G)=c_h', 'eq:ca-coefficient'),
        'source_image_fixed_point': ('\\im(\\tau)=\\{y\\inK^G:T_{ba}y=y\\}', 'eq:ca-image'),
        'proof_left_inverse': ('T_a\\circ\\tau=T_{ab}=T_1', 'eq:ca-leftinverse'),
    }
    for check, (token, label) in checks.items():
        entry = equation(source, label)
        if entry is None or token not in compact(entry[0]):
            failures.append('SOURCE_CONTRACT_MISMATCH:'+check)
    # Importantly inspect the *scoped proposition*, not occurrences elsewhere.
    if proposition:
        p = compact(proposition[0])
        for check, token in [('finite_alphabet_premise','Let$K$beafinitefield'),
                             ('group_carrier','G$agroup'),
                             ('one_sided_inverse_premise','$ab=1$'),
                             ('reverse_product_conditional','$ba\\ne1$')]:
            if token not in p:
                failures.append('PROPOSITION_PREMISE_MISSING:'+check)
    if lemma:
        l = compact(lemma[0])
        if 'everyfield$K$andgroup$G$' not in l:
            failures.append('LEMMA_SCOPE_UNRECOGNIZED')
    # Check the source's ACTUAL displayed proof step, not only theorem headers.
    if lemma:
        after = source[lemma[1]+len(lemma[0]):]
        match = re.match(r'\s*\\begin\{proof\}(.*?)\\end\{proof\}', after, re.DOTALL)
        if not match or 'd_vx(guv)' not in compact(match.group(1)):
            failures.append('PROOF_STEP_UNVERIFIED:ordered_right_expansion')
    if proposition:
        after = source[proposition[1]+len(proposition[0]):]
        match = re.match(r'\s*\\begin\{proof\}(.*?)\\end\{proof\}', after, re.DOTALL)
        if not match or '(ba-1)_h\\ne0' not in compact(match.group(1)):
            failures.append('PROOF_STEP_UNVERIFIED:nonzero_defect_witness')

    blocked = bool(failures)
    mathematical_certificate = symbolic_word_checks()
    return {
        'schema': 'source197_scoped_producer_v1',
        'producer_kind': 'automatic deterministic template-extractor (limited 197 TeX syntax)',
        'source': {'path': source_path, 'sha256': digest,
                   'required_anchors': anchors, 'source_kind':'original AI manuscript; not verified'},
        'gate': {'status': 'BLOCKED' if blocked else 'PASSED_SCOPED',
                 'failures': sorted(set(failures)),
                 'source_alignment':'restricted textual/syntactic checks only; no global semantic equivalence'},
        'claims': ([] if blocked else [
            {'id':'right_homomorphism','premises':['unital associative monoid','field K',
                    'finitely supported coefficients','right-neighbor T_c'],
             'statement':'T_c composed T_d = T_(c*d)',
             'source_status':'source_lemma_plus_scoped_proof_step_detected',
             'evidence':'index_word_certificate_plus_human_stated_finite_sum_argument'},
            {'id':'faithful','premises':['monoid identity','field K',
                    'delta configurations available'],
             'statement':'(T_c delta_h)(1)=c_h, so c -> T_c injective',
             'source_status':'source_coefficient_equation_detected',
             'evidence':'delta_response_direct_calculation'},
            {'id':'split_injective','premises':['a*b=1','right_homomorphism'],
             'statement':'T_b injective with left inverse T_a',
             'source_status':'source_proposition_premise_detected',
             'evidence':'conditional_algebra'},
            {'id':'image','premises':['a*b=1','right_homomorphism'],
             'statement':'im(T_b)=Fix(T_(b*a))',
             'source_status':'source_image_equation_detected',
             'evidence':'conditional_algebra'},
            {'id':'non_surjective','premises':['a*b=1','b*a != 1','faithfulness'],
             'statement':'T_b injective but not surjective',
             'source_status':'source_conditional_claim_detected',
             'evidence':'delta_h_missing_image_conditional_argument'}]),
        'symbolic_check': mathematical_certificate,
        'transfer': {'target_carrier':'unital associative monoid',
                     'status':'conditional_abstract_derivation; not quoted as source claim' if not blocked else 'WITHHELD',
                     'mathematical_boundary':'requires actual a*b=1 and b*a!=1 in target monoid algebra; group existence not established'},
        'unresolved': ['original group algebra witness is not independently verified',
                       'Lean proposition/proof correspondence NOT checked',
                       'template recognizer does not prove mathematical correctness of arbitrary source TeX',
                       'producer extraction effectiveness on unseen papers NOT measured']
    }


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args=parser.parse_args()
    result=produce(args.source.read_text(encoding='utf-8'),str(args.source))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['gate']['status'],
                      'failures':result['gate']['failures'],
                      'claims':len(result['claims']),
                      'sha256':result['source']['sha256']},indent=2))
    if result['gate']['status']!='PASSED_SCOPED':
        raise SystemExit(2)


if __name__=='__main__':
    main()
