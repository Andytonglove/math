# Understanding AI-Generated Mathematical Proofs — Research Pilot

Working branch for a reproducible **machine proof understanding** investigation. The original OpenAI/math artefacts are untouched.

## Research question

Can a model extract, manipulate, and transfer mathematical information from an unfamiliar research proof, beyond restating the theorem or copying a formal derivation?

**Not** a theorem-proving benchmark yet; **not** evidence of human comprehension. No human experiment is required for the first phase.

## Implemented in the first commit

- `scripts/catalog_audit.mjs`: dependency-free Node catalogue parser for `overview.tex`, README reasoning summary links, and presence of Lean scope notes.
- `data/catalog_index.json`: frozen family-level inventory at upstream/fork commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
- `tests/catalog_audit.test.mjs`: tests for TeX nested braces, summary metadata, and basic source invariants.

Regenerate from the repository root:

    node research/proof_understanding/scripts/catalog_audit.mjs . research/proof_understanding/data/catalog_index.json fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb
    node --test research/proof_understanding/tests/catalog_audit.test.mjs

## Important labels

- `lean_scope_doc`: existence of a scope **description**, not an independent Lean compilation or validation.
- `reasoning_summary`: an abridged public write-up, not a verified internal chain of thought.
- `manuscripts`: source links, not truth labels. Use the actual manuscript and scope notes before drawing conclusions.

## Proposed evaluation tracks (not yet benchmark scores)

1. **Claim & scope grounding:** distinguish the theorem actually formalized from stronger or different claims.
2. **Proof structure:** identify what imported formal ingredients are invoked; avoid equating file imports with full proof dependence.
3. **Counterfactual mathematics:** perturb assumptions; require a checked proof, a checked counterexample, or an explicit unknown judgment.
4. **Transfer:** solve a withheld, genuinely new related problem with a separately checked oracle.

All future test items need source provenance, leakage checks, and a clear verification level. Baselines should include paper-only, paper+Lean, paper+summary, and structural representation **without assuming any graph is better**.

## Pilot selection

- **017:** irrationality exponent of pi. Strong initial source-level case: main formal theorem, Lean scope note, and abridged reasoning summary.
- **102:** Unique Games and reductions; useful later for graph/CS-rich structure.
- **197:** Kaplansky direct-finiteness counterexamples; useful for disproof versus proof.

Start with 017. Do not claim to understand the mathematical novelty before reading its manuscript, reasoning summary and dependencies and obtaining appropriate mathematical review.
