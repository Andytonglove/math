# Reference graph vs proposed proof-mechanism graph — 017 diagnostic

We deliberately created **two different kinds of graphs** on the same source.

1. The **syntactic LaTeX reference graph** has a label declaration for each LaTeX label, and a directed link for each source occurrence of ref/eqref/autoref/cref/Cref.
2. The **manually curated mechanism graph** identifies argumentative roles: interpolation, nonzero determinant, arithmetic lower bound, analytic upper bound, collision-versus-approximation branching, and parameter contradiction.

A raw lexical/LaTeX graph is not a proof of logical dependence, and neither is a model of a reader's understanding.

## Actual manuscript-level reference extraction (5 TeX files)

| Property | Count |
|---|---:|
| Label declarations | 70 |
| Reference occurrences | 92 |
| References crossing source files | 27 |
| Duplicate declarations | 0 |
| Unresolved references | 0 |

The most cited labels are the theorem thm:main and the interpolation claim geom:interpolation, with seven mentions each. The collision estimate det:collision and the parameter feasibility lemma par:constants have **only one explicit reference each**, even though the former is used to build one entire branch of the determinant comparison and the latter controls the sharp \(\nu>2\) parameter choice.

This is a **single source-level observation**, not yet an empirical proof that degree centrality mispredicts importance. Text references do not encode conceptual novelty, and importance needs an independent operational definition.

## Hypotheses for later experiments

- A syntax-only reference graph may omit key mechanism roles expressed in prose rather than in label invocations.
- Ranking LaTeX nodes only by reference frequency may hide a mechanism that is decisive in a proof by cases.
- A typed mechanism graph might improve transfer on *held-out mathematics*, but it must outperform source-only and text-summary baselines with controlled information budget.

## Reproduction

From repository root, run:

~~~sh
node research/proof_understanding/scripts/tex_reference_audit.mjs . /tmp/017_tex_reference_graph.json
node --test research/proof_understanding/tests/tex_reference_audit.test.mjs
~~~

The script rejects unresolved LaTeX labels (not missing mathematical assumptions). Run only on the pinned source snapshot; later releases may alter counts.
