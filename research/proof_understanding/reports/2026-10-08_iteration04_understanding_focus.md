# Iteration 04 — Return to the research core (2026-10-08)

**Branch:** research/proof-understanding-pilot  
**Focus:** Understanding AI-Generated Mathematical Proofs. Graph is an auxiliary hypothesis, not the research objective.

## Actual engineering and mathematical work

1. Expanded modular LaTeX processing across three manuscript families (017, 102, 197). Fixed two real CI failures: resolving TeX includes relative to the project compilation root, and handling an explicitly identified external font-map preamble file without silently ignoring missing mathematical sections. Added regression tests.
2. Added independent unit oracles in understanding_oracles.py: F2 binary translation-game consistency, small exact game optimum, GF2 cyclic-group ring product enumeration and infinite-dimensional shift identities. They deliberately do not assume the advanced OpenAI theorem is valid.
3. Built 8 deterministic task cards with source anchor checks, separating prompts and oracle labels. Added strict answer-only scorer with abstention and missing counts. No model inference scores have been collected.
4. Created sourced, manually hypothesized argument hypergraphs: 017 (13 nodes, 6 typed relations), 102 (6 nodes, 1 typed relation), 197 (8 nodes, 3 typed relations). Source anchors are checkable but edge semantics are *not* certified.
5. Wrote [CORE_RESEARCH_CHARTER.md](../CORE_RESEARCH_CHARTER.md) to define understanding scientifically, compare sources against no-proof baselines, and explicitly permit Graph to fail.

## Three-paper source measurements, GitHub Actions run 37775212838

| Family | Source TeX files | LaTeX labels | Text references | Cross-file refs |
|---|---:|---:|---:|---:|
| 017 (pi exponent) | 5 | 70 | 92 | 27 |
| 102 (Unique Games) | 13 | 128 | 191 | 76 |
| 197 (Kaplansky) | 10 | 76 | 117 | 44 |

All three had zero unresolved in-paper refs and zero duplicate labels under our simplified parser. The 197 corpus included one known external LaTeX font-map input which was explicitly annotated.

## CI failure and recovery log

- 37774893863: failed — nested LaTeX paths wrongly resolved (fixed).
- 37775003157: failed — font-map file incorrectly required in repository (fixed).
- 37775212838: passed — 3 manuscript graphs plus parser regressions.
- 37775700438: passed — generated the eight toy tasks and oracle checks.
- 37776012144: passed — task generation, mathematical oracles and hypergraph provenance checks.
- Strict scorer tests were added subsequently; verify their status in a newer CI run before treating them as validated.

## Mathematical interpretation, carefully limited

The 017 case uses a proof-by-cases analytic saving mechanism; 102 combines a quantified reduction with completeness and soundness; 197's disproof needs two independent product certificates. A typed hypergraph records these logical roles better than an import-count chart, but no model evaluation has shown improved proof understanding. All source papers are research claims rather than independently certified truths in this project.

The oracle tasks are elementary and often solvable without access to the source proof. **Do not publish them as a proof-understanding benchmark** until tests demonstrate nontrivial, proof-conditioned ability.

## Remaining work and costs

Not done: language model baselines, full Lean compilation/Comparator, expert mathematical review, high-difficulty held-out source-conditioned tasks, understanding scores. No paid model inference was initiated this iteration. GitHub-hosted Actions compute was used; no billing amount is asserted.

## Next experimental gate

1. Audit enough of the 102 and 197 proofs to identify true source-specific interventions beyond elementary general mathematics.
2. Build at least one independently verified new target per family and compare B0 (no proof) vs B2 (full proof) vs B5 (token-matched mechanism explanation) before any graph-specific claims.
3. Only if graph-related improvements survive these controls, test B4 typed hypergraphs.
4. Keep exact artifact provenance, versioned oracles, experiment logs and explicit confidence levels.
