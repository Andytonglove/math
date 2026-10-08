# Family 017 — new proof-mechanism transfer: changing a power constraint

Source: the family 017 conclusion section, which uses A^2<theta and a strict approximation gap nu*(A-theta)>1-theta. The geometric interpolation argument in that manuscript is NOT assumed correct or generalized here.

Consider a new, self-contained **elementary** problem with integer r>=2:

Find rational 0<theta<A<1 such that A^r<theta and nu*(A-theta)>1-theta.

**Proposition:** This is feasible if and only if nu>r/(r-1).

## Necessity (complete exact argument)

For fixed A in (0,1), (A-theta)/(1-theta) strictly decreases with theta. Since theta>A^r,

(A-theta)/(1-theta) < (A-A^r)/(1-A^r).

For 0<A<1,

r*(A-A^r) < (r-1)*(1-A^r)

is equivalent to A^r-r*A+(r-1)>0. This last expression is positive: it vanishes at A=1 and has derivative r*(A^(r-1)-1)<0 throughout (0,1). Thus the ratio is strictly below (r-1)/r. The strict gap nu*(A-theta)>1-theta requires nu>r/(r-1).

## Sufficiency (exact rational witnesses)

For nu>r/(r-1), take rational A<1 sufficiently close to 1. The ratio (A-A^r)/(1-A^r) tends to (r-1)/r; hence nu*(A-A^r)>1-A^r. Choose a rational theta strictly between A^r and the smaller of A and (nu*A-1)/(nu-1). This ensures both inequalities. The script constructs A=1-2^(-k), searches for a valid k, and chooses the midpoint theta using exact Fraction arithmetic.

## Why this is more informative than recall

The 2026 paper's special constraint r=2 gives critical nu=2. Changing the abstract power r to 3 gives critical nu=3/2; r=4 gives 4/3. This is a genuine mathematical generalization of the **elementary parameter-feasibility mechanism**, not a claim about rational approximations to pi or validity of a new interpolation theorem.

The test family explores r=2..12 with exponents below, exactly at, and above the critical value (33 tasks, 11 constructive positive witnesses). The complete independent proof above supplies the oracle, while code checks rational witnesses exactly. These are mechanism-transfer **candidates**, not a reliable high-difficulty model understanding benchmark on their own.

Commands from root:
    python3 -m unittest discover -s research/proof_understanding/tests -p 'test_parameter_threshold_transfer.py' -v
    python3 research/proof_understanding/scripts/parameter_threshold_transfer.py --root . --out-dir /tmp/parameter_transfer_017
