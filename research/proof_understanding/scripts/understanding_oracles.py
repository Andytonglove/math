"""Small, independently checkable mathematics for AI-proof-understanding pilots.

THESE ARE UNIT-LEVEL COUNTERFACTUAL ORACLES, NOT VERIFICATION OF THE
ORIGINAL OPENAI MATHEMATICS RESEARCH CLAIMS. Standard-library only.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product


def xor_translation_assignment(vertices: int, bits: int,
                               constraints: list[tuple[int,int,int]]) -> tuple[bool,list[int]|None]:
    """Solve x[v] = x[u] xor shift over F_2^bits, including disconnected graphs."""
    if vertices < 1 or bits < 1 or bits > 12:
        raise ValueError("vertices>=1 and 1<=bits<=12 required")
    neighbors: list[list[tuple[int,int]]] = [[] for _ in range(vertices)]
    for u,v,shift in constraints:
        if not (0 <= u < vertices and 0 <= v < vertices and 0 <= shift < 2**bits):
            raise ValueError("invalid endpoint or alphabet shift")
        neighbors[u].append((v,shift))
        neighbors[v].append((u,shift))  # shifts are self-inverse in F_2^bits
    labels: list[int|None] = [None]*vertices
    for root in range(vertices):
        if labels[root] is not None:
            continue
        labels[root] = 0
        queue = [root]
        for u in queue:
            for v,shift in neighbors[u]:
                want = labels[u] ^ shift
                if labels[v] is None:
                    labels[v] = want
                    queue.append(v)
                elif labels[v] != want:
                    return False,None
    answer = [int(x) for x in labels]
    assert all(answer[v] == (answer[u] ^ s) for u,v,s in constraints)
    return True,answer


def exact_unique_game_value(vertices: int, bits: int,
                            constraints: list[tuple[int,int,int]],
                            max_labelings: int = 100_000) -> Fraction:
    """Exhaustive small-instance optimum. Never called on research-scale games."""
    if vertices < 1 or bits < 1:
        raise ValueError("vertices and bits must be positive")
    if not constraints:
        raise ValueError("nonempty constraints required")
    if 2**(vertices*bits) > max_labelings:
        raise ValueError("instance too large for exact exhaustive oracle")
    # Reuse endpoint/alphabet validation.
    for u,v,shift in constraints:
        if not (0<=u<vertices and 0<=v<vertices and 0<=shift<2**bits):
            raise ValueError("invalid constraint")
    best = 0
    for a in product(range(2**bits),repeat=vertices):
        count = sum(a[v] == (a[u]^s) for u,v,s in constraints)
        best = max(best,count)
        if best == len(constraints):break
    return Fraction(best,len(constraints))


def cyclic_gf2_product(order: int, a: int, b: int) -> int:
    """Multiply bitmask group algebra elements in F_2[C_order]."""
    if order < 1 or order > 16 or not (0 <= a < 2**order and 0 <= b < 2**order):
        raise ValueError("invalid order or element encoding")
    out = 0
    for i in range(order):
        if not ((a >> i) & 1):
            continue
        for j in range(order):
            if (b >> j) & 1:
                out ^= 1 << ((i+j)%order)
    return out


def enumerate_one_sided_pairs(order: int) -> tuple[int,int]:
    """Return (# ab=1 pairs, # among those with ba!=1) for SMALL cyclic groups."""
    if order < 1 or order > 7:
        raise ValueError("small orders only")
    total,violations = 0,0
    for a in range(2**order):
        for b in range(2**order):
            if cyclic_gf2_product(order,a,b) == 1:
                total += 1
                if cyclic_gf2_product(order,b,a) != 1:
                    violations += 1
    return total,violations


def shift_right(x: int) -> int:
    """Unilateral shift R(e_i)=e_(i+1) in countably infinite basis over F_2."""
    if x < 0:raise ValueError("negative finite-support vector")
    return x << 1


def shift_left(x: int) -> int:
    """Unilateral shift L(e_0)=0, L(e_(i+1))=e_i."""
    if x < 0:raise ValueError("negative finite-support vector")
    return x >> 1


def example_games() -> dict:
    # 4-cycle, bipartition {0,2}/{1,3}, with translations in F_2^2.
    consistent=[(0,1,1),(1,2,2),(2,3,3),(0,3,0)]
    broken=[(0,1,1),(1,2,2),(2,3,3),(0,3,1)]
    return {"consistent":consistent,"one_edge_perturbed":broken}
