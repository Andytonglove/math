# 017 — Auditing a mathematical mechanism rather than only the Lean dependency tree

**Evidence standard:** source-level reading and exact arithmetic experiments only. We have NOT independently reviewed the whole proof or compiled the Lean library.

The complete mathematical paper is available as modular LaTeX: main.tex and four included sections (interpolation, determinant, conclusion, series). The released *abridged reasoning summary* is a PDF that could not be processed through our current GitHub text connector. This report reconstructs the submitted **proof argument**, NOT the internal model's actual reasoning trace.

## Claim and scope

The selected formal statement asserts that for every real exponent \(\nu>2\), there is an eventual threshold \(Q(\nu)\) for \(|\pi-p/q|\ge q^{-\nu}\). It also characterizes the irrationality exponent as two. It does **not** assert the stronger exponent-two uniform bound, nor offer a computable explicit threshold.

The manuscript additionally claims Flint–Hills convergence. The comparator challenge targets only the irrationality-exponent theorem, although a *separate* summability theorem appears in Lean Main. The distinction is per-statement, not merely per-paper.

## Source-grounded proof skeleton

| Role | Claim in the submitted argument | Anchor |
|---|---|---|
| Assumption for contradiction | Arbitrarily good rational approximations with \(\nu>2\) | conclusion.tex, par:good |
| Geometric existence | Surjectivity of weighted multivariable jet interpolation | interpolation.tex, geom:interpolation |
| Witness | Select a nonzero full-row-rank minor \(\Delta_H\) | determinant.tex, det:matrix |
| Arithmetic floor | Clear denominators and exploit nonzero Gaussian integer modulus \(\ge1\) | determinant.tex, det:arithmetic |
| Analytic ceiling | Translation to entire-function tests and a collision estimate | determinant.tex, det:translation and det:collision |
| Branching structure | If many small indices: collision saving; otherwise: approximation-error saving | determinant.tex, det:comparison |
| Global contradiction | Fix dimensions/weights/denominators in the specified order; choose enough margin | conclusion.tex, par:constants and par:dimension |
| Corollary | Dyadic spacing controls exceptional small sine values | series.tex, series:dyadic |

The graph in ../data/017_mechanism_graph.json contains these typed claims with provenance labels. It is intentionally **hand-curated**. A compiler import graph or a theorem-reference graph is not the same as an explanatory proof mechanism.

## Independently checked primitive #1: feasibility boundary

The paper asks for \(\nu,\theta,A,B,C,\eta\) satisfying

\[
0<\theta<A<B<1,\quad C>1,\quad B<1/C,\quad B<C\theta<1,\quad
\nu(A-\theta)>1-\theta,\quad
\nu(A(1-\eta)-\theta)>1-\theta.
\]

The middle constraints force \(A^2<\theta\): since \(A<C\theta\) and \(AC<1\), we have \(A^2<\theta\).

For \(\nu\le2\), these very constraints are impossible, because

\[
(1-\theta)-2(A-\theta)=1-2A+\theta>(1-A)^2>0.
\]

Thus \(\nu(A-\theta)\le2(A-\theta)<1-\theta\), contradicting the required strict gap. **This shows that this parameter construction cannot be extended unchanged to \(\nu=2\)**. It does not settle whether \(\pi\) satisfies any stronger approximation inequality.

For rational \(\nu>2\) we implement the manuscript's construction with exact rational values: choose a rational \(b\in(1/2,1-1/\nu)\); a small rational \(\delta>0\); set \(\theta=1-\delta\), \(A=1-b\delta\); choose \(C\) strictly between \(A/\theta\) and \(1/A\), and \(B\) strictly between \(A\) and \(\min(1/C,C\theta)\); finally choose \(\eta\) to retain half of the positive margin. The independent script constructs exact witnesses and checks nine constraints.

Seven examples passed: \(\nu\in\{2001/1000,9/4,5/2,3,4,7,100\}\). The statement about arbitrary reals still relies on the mathematical density argument, not the finite test set.

## Independently checked primitive #2: quadratic index collisions

The paper's determinant expansion uses the fact that repeated Taylor indices force vanishing coefficients; distinct degrees have to be used within each group. This induces a quadratic discount depending on group counts \(n_i\).

Separately, for \(n\) rows and at most \(D\) possible group labels, balanced counts minimize the number of same-label unordered pairs:

\[
\min \sum_i \binom{n_i}{2}
=r\binom{q+1}{2}+(D-r)\binom q2,
\qquad n=qD+r,\ 0\le r<D.
\]

Examples: \(n=7,D=3\) yields 5; \(n=10,D=3\) yields 12. The finite formula was exhaustively compared with all occupancy assignments for \(D=1,2,3,4\) and \(n=0,\ldots,9\).

This proves neither the complex analytic determinant estimate nor the main theorem. It isolates a *checkable mathematical primitive* that a model should be able to transfer.

## Why this matters for our research

A weak model can retrieve the statement "the proof uses a collision lemma." A stronger test asks it to explain what **fails** if the indices do not collide, or to transfer the same bound to a fresh occupation problem. Another weak model can quote "nu > 2"; a stronger test derives the parameter infeasibility at \(\nu=2\) and avoids incorrectly claiming that the theorem fails at this boundary.

These examples suggest a workable machine-only research program: **extract a specific proof mechanism → design a verified intervention → compare model access to source, imports, and semantic explanation**. The graph is only a representation hypothesis, not a performance conclusion.

## Not done (do not silently upgrade confidence)

- Independent check of the nontrivial geometric interpolation/surjectivity proof.
- Comparator execution or auditing permitted Lean axioms.
- Mathematical expert review of the claimed \(\mu(\pi)=2\) theorem.
- Extraction of the full PDF-only abridged reasoning summary.
- Any model inference or experimental comparison of graph and text.

Source files are under preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections.
