"""Exact local mathematical diagnostics and a label-only scorer (no semantic grading)."""
from __future__ import annotations
import itertools
from fractions import Fraction as F

CLAIM_LABELS = {"LOCALLY_ESTABLISHED", "EXACTLY_REFUTED", "NOT_INDEPENDENTLY_AUDITED"}
PROOF_LABELS = {"VALID_LOCAL", "INVALID_STEP", "NOT_AUDITED"}

def barrier_ok(value: F, a: F, theta: F, nu: F) -> bool:
    """Exact arithmetic for one *specific rational instance*, never a universal oracle."""
    return F(0) < theta < a < F(1) and value < theta and nu * (a - theta) > 1 - theta


def nonconvex(a: F) -> F:
    return a * a - 3 * a**3 * (1 - a)**2


def permutations():
    return list(itertools.permutations(range(3)))


def mul(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Permutation product p after q, with an explicit multiplication convention."""
    return tuple(p[q[i]] for i in range(3))


def finite_operator_checks() -> dict:
    """Independent finite S3 spot-check of a general associativity derivation.

    A finite enumeration is NOT a proof for every monoid or algebra.
    """
    elements = permutations()
    identity = (0, 1, 2)
    u, v = (1, 0, 2), (0, 2, 1)
    assert u in elements and v in elements
    assert mul(u, v) != mul(v, u)
    tested = 0
    for g in elements:
        for p in elements:
            for q in elements:
                assert mul(p, mul(g, q)) == mul(mul(p, g), q)
                tested += 1
    # At g=e, the spurious swap uev=veu is demonstrably false.
    assert mul(mul(u, identity), v) != mul(mul(v, identity), u)
    return {"s3_associativity_instances": tested,
            "false_commutation_witness": {"u": list(u), "v": list(v), "g": list(identity),
                                          "uv": list(mul(u, v)), "vu": list(mul(v, u))}}


def monoid_shift_checks(limit: int = 64) -> dict:
    """Finite sanity check; the accompanying symbolic two-case proof is universal."""
    left = lambda n: max(n - 1, 0)
    right = lambda n: n + 1
    assert limit > 0
    for n in range(limit):
        assert left(right(n)) == n
    assert right(left(0)) == 1 != 0
    return {"prefix_checked": limit, "LR_identity_symbolic": "L(R(n))=L(n+1)=n for all n>=0",
            "RL_failure_witness": {"n": 0, "R_L_n": 1}}


def exact_diagnostics() -> dict:
    a, theta = F(3, 4), F(31, 64)
    h = nonconvex(a)
    nu = F(39, 20)
    assert h == F(495, 1024)
    assert barrier_ok(h, a, theta, nu)
    slack = nu * (a - theta) - (1 - theta)
    assert slack == F(3, 1280)
    # A published threshold conclusion can be true while a candidate proof is wrong.
    theta_bad = F(5, 8)
    assert a*a < theta_bad < a
    assert not (a - theta_bad > a - a*a)  # invalid proof's reversed inequality
    assert a - theta_bad == F(1, 8) and a - a*a == F(3, 16)
    # Explicit feasible positive instance for f(A)=A^2, nu > 2.
    assert barrier_ok(F(7, 8)**2, F(7, 8), F(25, 32), F(5, 2))
    return {"nonconvex": {"A": "3/4", "theta": "31/64", "nu": "39/20",
                          "f_A": "495/1024", "slack": str(slack)},
            "invalid_proof_step": {"A": "3/4", "theta": "5/8",
                                   "A_minus_theta": "1/8", "A_minus_A_squared": "3/16"},
            "positive_square_example": {"A": "7/8", "theta": "25/32", "nu": "5/2"}}


def score_labels(answer: dict, gold: dict) -> dict:
    """Only classify labels. Human explanations need a blinded expert rubric."""
    if answer.get("claim") not in CLAIM_LABELS or answer.get("proof") not in PROOF_LABELS:
        raise ValueError("invalid claim or proof status")
    return {"claim_label_correct": answer["claim"] == gold["claim"],
            "proof_label_correct": answer["proof"] == gold["proof"],
            "unsupported_certification": gold["claim"] == "NOT_INDEPENDENTLY_AUDITED" and answer["claim"] == "LOCALLY_ESTABLISHED",
            "incorrectly_falsified_true_claim_after_gap": gold["claim"] == "LOCALLY_ESTABLISHED" and gold["proof"] == "INVALID_STEP" and answer["claim"] == "EXACTLY_REFUTED",
            "reasoning_quality": "REQUIRES_BLINDED_HUMAN_EXPERT_RUBRIC"}

