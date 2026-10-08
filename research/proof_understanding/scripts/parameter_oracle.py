"""Exact rational oracle for the parameter construction in OpenAI/math family 017.

Scope: the sufficient inequalities in conclusion.tex (par:constants).
NOT a proof of the irrationality exponent of pi, NOT a Lean/Comparator run.
"""
from __future__ import annotations
from fractions import Fraction
import argparse
import json


class InfeasibleParameter(ValueError):
    pass


def construct(nu: Fraction) -> dict[str, Fraction]:
    """Construct rational theta,A,B,C,eta for the proof's sufficient inequalities."""
    nu = Fraction(nu)
    if nu <= 2:
        raise InfeasibleParameter("these sufficient inequalities require nu > 2")
    b = (Fraction(1, 2) + (1 - 1 / nu)) / 2
    delta = min(Fraction(1, 4), (2 * b - 1) / (4 * b * b))
    theta = 1 - delta
    A = 1 - b * delta
    C = (A / theta + 1 / A) / 2
    B = (A + min(1 / C, C * theta)) / 2
    gap0 = nu * (A - theta) - (1 - theta)
    eta = gap0 / (2 * nu * A)
    g = nu * (A * (1 - eta) - theta) - (1 - theta)
    w = dict(nu=nu, b=b, delta=delta, theta=theta, A=A, B=B, C=C, eta=eta, g=g)
    assert all(checks(w).values()), checks(w)
    return w


def checks(w: dict[str, Fraction]) -> dict[str, bool]:
    nu, theta, A, B, C, eta, g = (w[k] for k in ("nu", "theta", "A", "B", "C", "eta", "g"))
    return {
        "nu_above_two": nu > 2,
        "positive_separated_weights": 0 < theta < A < B < 1,
        "C_above_one": C > 1,
        "B_below_C_inverse": B < 1 / C,
        "B_below_Ctheta_below_one": B < C * theta < 1,
        "arithmetic_gap_at_eta_zero": nu * (A - theta) > 1 - theta,
        "eta_in_unit_interval": 0 < eta < 1,
        "positive_perturbed_gap": g > 0 and g == nu * (A * (1 - eta) - theta) - (1 - theta),
        "hidden_A_squared_below_theta": A * A < theta,
    }


def minimum_pairwise_collisions(n: int, types: int) -> int:
    """Exact minimum of sum_i binom(n_i,2) over at most types groups."""
    if n < 0 or types <= 0:
        raise ValueError("require n >= 0 and types >= 1")
    q, r = divmod(n, types)
    return r * ((q + 1) * q // 2) + (types - r) * (q * (q - 1) // 2)



def collision_scaling_example(H: int, m: int = 1) -> dict:
    """Idealized low-index collision budget, *not* the original determinant theorem.

    Let M=H^(m+1) rows, D=H^m permitted low-index types, with
    half of rows assigned to low types. Compare exact normalized
    quadratic vs hypothetical only-linear penalty.
    """
    if H <= 0 or H % 2 or m < 1 or m > 5:
        raise ValueError("H positive even and 1<=m<=5 required")
    M = H ** (m + 1)
    D = H ** m
    n_low = M // 2
    min_pairs = minimum_pairwise_collisions(n_low,D)
    low_square_mass = 2 * min_pairs + n_low
    quadratic = Fraction(low_square_mass, M * H)
    linear = Fraction(M, M * H)
    return {"H":H,"dimension":m,"row_count":M,"low_types":D,
            "low_rows":n_low,
            "normalized_quadratic_saving":str(quadratic),
            "normalized_linear_saving":str(linear)}

def score_ratio(w: dict[str, Fraction]) -> dict[str, float]:
    # Diagnostic only. Not the entire proof's quantitative requirements.
    from math import log
    theta, A, B, C = (w[k] for k in ("theta", "A", "B", "C"))
    return {
        "log_B_over_A": log(float(B / A)),
        "log_C_times_B": log(float(C * B)),
        "log_Ctheta_over_B": log(float(C * theta / B)),
    }


def serialize(w: dict[str, Fraction]) -> dict:
    return {
        "nu": str(w["nu"]),
        "parameters": {k: str(v) for k, v in w.items() if k != "nu"},
        "checked": checks(w),
        "diagnostic_log_ratios": score_ratio(w),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    samples = [Fraction(2001, 1000), Fraction(9, 4), Fraction(5, 2),
               Fraction(3), Fraction(4), Fraction(7), Fraction(100)]
    rows = [serialize(construct(nu)) for nu in samples]
    result = {
        "status": "exact rational feasibility witnesses; not a full theorem proof",
        "source": "preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections/conclusion.tex (par:constants)",
        "samples": rows,
        "caution": "The checks concern sufficient parameter inequalities, not the global interpolation/determinant claims.",
    }
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print(json.dumps({"samples": len(rows),
                      "all_checks_pass": all(all(r["checked"].values()) for r in rows),
                      "nu_values": [r["nu"] for r in rows]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
