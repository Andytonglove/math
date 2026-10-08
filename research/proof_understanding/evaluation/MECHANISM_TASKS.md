# Source-derived mechanism probes — Case 017 (NOT benchmark scores)

These are **unit probes** with independent mathematical gold results. No model has been evaluated. The first experiments must include a no-source control, because all five may be solvable using general training knowledge.

| ID | Intervention / task | Independently checkable answer |
|---|---|---|
| PARAM-BOUNDARY | Keep all of the parameter lemma's constraints but set nu = 2. Can any theta,A,B,C satisfy them? | No. Other constraints force A² < theta, hence 2(A-theta)<1-theta. |
| PARAM-WITNESS | Set nu=9/4. Produce rational theta,A,B,C,eta satisfying all strict constraints. | Constructed with scripts/parameter_oracle.py and verified exactly using Fraction. |
| COLLISION-7-3 | Seven rows have at most three possible Taylor index groups. What is the minimum number of unordered same-group pairs? | 5, realized by groups of sizes 3,2,2. |
| COLLISION-10-3 | Ten rows have at most three possible groups. What is the minimum? | 12, realized by 4,3,3. |
| FULL-RANK-FAIL | Does having three polynomial coefficients for two prescribed jet values guarantee interpolation surjectivity if the two constraints may be identical? | No: map (x,y,z) to (x,x) has rank one. |

**Scoring protocol required before real experiments:** rephrase to avoid direct lexical overlap; withhold proof segments when necessary; use independent proof/counterexample oracles; compare without source, with paper, with Lean scope, and with curated mechanism explanation; record failure and abstention. Do not claim a "human understanding" outcome from machine-only data.
