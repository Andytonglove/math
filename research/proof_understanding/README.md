# Understanding AI-Generated Mathematical Proofs — Research Pilot

Working branch for a reproducible **machine proof understanding** investigation. The original OpenAI/math artefacts are untouched.

## Research question

Can a model extract, manipulate, and transfer mathematical information from an unfamiliar research proof, beyond restating the theorem or copying a formal derivation?

**Not** a theorem-proving benchmark yet; **not** evidence of human comprehension. No human experiment is required for the first phase.

## Implemented

- `scripts/catalog_audit.mjs`: dependency-free Node catalogue parser for `overview.tex`, README reasoning summary links, and presence of Lean scope notes.
- `data/catalog_index.json`: frozen family-level inventory at upstream/fork commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
- `tests/catalog_audit.test.mjs`: tests for TeX nested braces, summary metadata, and source invariants.
- `cases/017_pi_exponent.md`: concrete first case comparing comparator scope, visible Lean source, and mathematical boundaries.
- `data/case017_proof_spine.json`: manually grounded, deliberately incomplete local proof-invocation spine.
- `evaluation/pilot_tasks.json`: five candidate tasks; four **source-grounded controls** and one **transfer oracle pending**.
- `scripts/validate_pilot.mjs`: source anchor validation, not mathematical correctness testing.

Regenerate/check from the repository root:

    node research/proof_understanding/scripts/catalog_audit.mjs . research/proof_understanding/data/catalog_index.json fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb
    node --test research/proof_understanding/tests/*.test.mjs
    node research/proof_understanding/scripts/validate_pilot.mjs .

## Important labels

- `lean_scope_doc`: existence of a scope **description**, not an independent Lean compilation or validation.
- `reasoning_summary`: an abridged public write-up, not a verified internal discovery trace.
- `manuscripts`: source links, not truth labels. Use the actual manuscript and scope notes before drawing conclusions.
- The selected comparator theorem is narrower than all possible claims in a paper. A `sorry` in ComparatorChallenges is a challenge target, not itself a proof gap.

## Evaluation tracks (NOT results)

1. **Claim & scope grounding:** distinguish the theorem actually formalized from stronger or different claims.
2. **Proof structure:** trace source-level ingredients, with explicit distinction between import graph and mathematical necessity.
3. **Counterfactual mathematics:** perturb assumptions; require checked proof, checked counterexample, or principled abstention.
4. **Transfer:** solve a withheld, genuinely new related problem with a separately checked oracle.

All test items need source provenance, leakage checks, and a specified verification level. Baselines should include paper-only, paper+Lean, paper+summary, and structure-aware representations **without assuming graph helps**.

## Pilot selection

- **017 (active case):** π irrationality exponent; has source, Lean notes and reasoning summary PDF. Current audit explicitly has NOT examined PDF reasoning details.
- **102 (queue):** Unique Games and reductions, a later graph/CS-rich case.
- **197 (queue):** Kaplansky-related counterexamples; useful for disproof versus proof.

## Next gate

Read the actual paper and abridged reasoning summary, follow a mathematically meaningful dependency in 017, construct a **verified withheld transfer task**, and only then run language-model baselines. See `evaluation/PROTOCOL.md`.


## Iteration 02 — mathematical mechanism probes

- cases/017_method_audit.md: manuscript-based argument skeleton, sharp parameter feasibility boundary, source-vs-mechanism limitations.
- data/017_mechanism_graph.json: **manually curated hypothesis graph**, not the Lean proof DAG.
- scripts/parameter_oracle.py and tests/test_parameter_oracle.py: exact Fraction witnesses and finite collision oracle.
- evaluation/MECHANISM_TASKS.md: five machine-only probe specifications, not measured scores.
- reports/2026-10-08_iteration02.md: completed work, local test outcomes, limitations and next gate.

Generate/check, from the repository root:

~~~sh
python3 research/proof_understanding/scripts/parameter_oracle.py --output research/proof_understanding/data/parameter_witnesses.json
python3 -m unittest discover -s research/proof_understanding/tests -p 'test_*.py' -v
node --test research/proof_understanding/tests/*.test.mjs
~~~

No full Lean compilation or actual model inference has been performed.


## LaTeX graph baseline

scripts/tex_reference_audit.mjs extracts **syntactic** label-reference links in case 017 from five source TeX files, and refuses unresolved/duplicate labels. cases/017_graph_diagnostic.md contrasts this with the human-curated mechanism graph. Neither graph has yet been shown to improve any model benchmark score.


## Project focus (Iteration 04)

**Core:** Understanding AI-Generated Mathematical Proofs, not a Graph product.

- [Research charter](CORE_RESEARCH_CHARTER.md): falsifiable hypotheses, machine-only understanding tasks, controls for no-proof baselines, and conditions under which Graph should be rejected.
- [Iteration 04 report](reports/2026-10-08_iteration04_understanding_focus.md): cross-family data, CI failures/fixes, oracles and scientific limitations.
- [Candidate argument hypergraphs](data/argument_hypergraphs_v0.json): manually hypothesized, **not** verified semantic graph.
- [Exact unit oracles](scripts/understanding_oracles.py), [8-task generator](scripts/build_understanding_pilot.py), [strict scorer](scripts/score_understanding_pilot.py): preparatory infrastructure, **no model scores yet**.

The next research gate is a genuinely source-conditioned, mathematically independently checked intervention, not adding more graph nodes.
