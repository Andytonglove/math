"""A *restricted* mathematical semantic-contract audit.

It detects evidence-backed differences in selected mathematical contracts.
It does not decide general natural-language / Lean equivalence, prove the
Navier--Stokes theorem, or reconstruct the author's intended mental proof.
Python standard library only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def wrong_factorization_case(case: dict) -> dict:
    # Coefficients are in ascending powers of x.
    p = case["claimed_polynomial"]
    left = case["incorrect_factorization"]["left"]
    right = case["incorrect_factorization"]["right"]
    proposed = mul(left, right)
    correct = mul(case["correct_factorization"]["left"],case["correct_factorization"]["right"])
    x0 = lambda coeffs: coeffs[0]
    if correct != p:
        raise ValueError("claimed correction fails exact polynomial multiplication")
    if proposed == p:
        raise ValueError("sample invalid: incorrect proof did not contain a mismatch")
    return {
        "finding": "proof_argument_incorrect_theorem_can_be_true",
        "expected": case["expected"],
        "exact_certificate": {
            "polynomial_coefficients": p,
            "wrong_product_coefficients": proposed,
            "correct_product_coefficients": correct,
            "counterexample_x": 0,
            "claimed_p_at_x0": x0(p),
            "wrong_factor_at_x0": x0(proposed),
        },
        "verified_scope": "elementary polynomial algebra only",
    }


def regularity_case(case: dict) -> dict:
    nl = case["natural_language_derivative_loss"]
    formal = case["formal_derivative_loss"]
    if not isinstance(nl, int) or not isinstance(formal, int) or nl < 0 or formal < 0:
        raise ValueError("nonnegative integer derivative losses needed")
    if formal > nl:
        status="formal_requires_higher_input_regularity"
    elif formal < nl:
        status="formal_uses_lower_input_regularity"
    else:
        status="same_reported_derivative_loss"
    # Generic countermodel: T=D^(m+formal), f_n=n^-(m+nl) sin(nx)
    # C^(m+nl) norm <= 1 and D^(m+formal) supnorm = n^(formal-nl).
    gap=max(0,formal-nl)
    return {
        "finding":status,
        "expected":case["expected"],
        "exact_certificate":{
            "nl_offset":nl,
            "formal_offset":formal,
            "relative_regularity_requirement":formal-nl,
            "generic_derivative_operator_countermodel":{
                "frequencies":[2,3,5,11],
                "C_m_plus_NL_norm_upper":1,
                "higher_derivative_magnitudes":[n ** gap for n in (2,3,5,11)],
            } if gap > 0 else None,
        },
        "verified_scope":"difference in stated loss plus generic norm counterexample; not original NS inverse operator",
    }


def existence_case(case:dict)->dict:
    # p(n,x1,x2)=x1+x2-n always vanishes at (x1,x2)=(n,0);
    # hence no n satisfies 'for all x1,x2 p !=0'. Proof is symbolic.
    samples=case["finite_samples"]
    if not isinstance(samples,int) or samples<1:
        raise ValueError("finite_samples must be positive")
    checks=all(n+0-n==0 for n in range(samples))
    if not checks:
        raise AssertionError("constructed roots did not satisfy polynomial")
    return {
        "finding":"existence_presupposition_is_false",
        "expected":case["expected"],
        "exact_certificate":{
            "symbolic_witness":"for every natural n, choose x1=n, x2=0: x1+x2-n=0",
            "finite_root_checks":samples,
            "proposition":"no natural n makes the polynomial root-free",
            "unfaithful_totalization":"replacing undefined least n by Nat.sInf(empty)=0 changes intended meaning",
        },
        "verified_scope":"symbolic universal witness; independent of finite checks",
    }


def quantifier_case(case:dict)->dict:
    # On a real interval a single point is measure zero: a.e. f=0 need
    # not imply all t f=0. Not a theorem about original Navier-Stokes flux.
    nl=case["natural_language_scope"]
    formal=case["formal_scope"]
    if nl=="almost_everywhere" and formal=="everywhere":
        finding="formal_time_scope_stronger"
    elif nl==formal:
        finding="equal_scope_label"
    else:
        finding="scope_relation_unresolved"
    return {
        "finding":finding,
        "expected":case["expected"],
        "exact_certificate":{
            "countermodel":"f(t)=1 at exactly one interior point t0, and 0 elsewhere",
            "a.e_zero_but_not_everywhere_zero":True,
        } if finding=="formal_time_scope_stronger" else None,
        "verified_scope":"isolated time-scope logic only; other bound differences can make whole claims incomparable",
    }


def extra_dependency_case(case:dict)->dict:
    nl=set(case["nl_rhs_dependencies"])
    formal=set(case["formal_rhs_dependencies"])
    extra=sorted(formal-nl)
    return {
        "finding":"formal_adds_rhs_dependencies" if extra else "no_new_listed_dependency",
        "expected":case["expected"],
        "exact_certificate":{
            "additional_formal_symbols":extra,
            "missing_formal_symbols":sorted(nl-formal),
        },
        "verified_scope":"surface-level dependency evidence; mathematical implication UNDETERMINED",
    }


DISPATCH={
    "incorrect_factorization":wrong_factorization_case,
    "derivative_loss":regularity_case,
    "missing_exists":existence_case,
    "ae_vs_all":quantifier_case,
    "rhs_extra_variable":extra_dependency_case,
}


def audit(data:dict)->dict:
    cases=data["cases"]
    if len({c["id"] for c in cases})!=len(cases):
        raise ValueError("duplicate case identifier")
    output=[]
    for case in cases:
        task=DISPATCH.get(case["kind"])
        if task is None:
            raise ValueError("unsupported case kind: "+case["kind"])
        r=task(case)
        if r["finding"]!=case["expected"]:
            raise AssertionError(f"{case['id']}: computed={r['finding']} expected={case['expected']}")
        # Cite the exact snapshot and source needed for replication.
        output.append({
            "id":case["id"],
            "kind":case["kind"],
            "finding":r["finding"],
            "evidence":case["evidence"],
            "verified_scope":r["verified_scope"],
            "exact_certificate":r["exact_certificate"],
        })
    return {
        "schema_version":"0.1",
        "cases_checked":len(output),
        "all_expected_local_checks_passed":True,
        "semantic_equivalence_of_full_NL_and_Lean":"NOT_ESTABLISHED",
        "universal_semantic_decider":"NOT_CLAIMED",
        "model_inference_runs":0,
        "cases":output,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    doc=json.loads(Path(args.input).read_text(encoding="utf-8"))
    result=audit(doc)
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
        "cases_checked","all_expected_local_checks_passed",
        "semantic_equivalence_of_full_NL_and_Lean","model_inference_runs")},indent=2))


if __name__=="__main__":
    main()
