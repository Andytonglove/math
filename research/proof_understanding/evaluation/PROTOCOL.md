# Case 017 — Proof understanding pilot tasks

Machine-only candidate task set; NO human subjects, model runs or success-rate claims yet.

## What is being measured?

Phase 0 tests provenance and statement scope. Phase 1 needs genuinely held-out mathematical interventions and independently verified oracles.

Tasks 017-SCOPE-01 / 02 are **formal statement-scope** checks, not evidence that the model grasped the original proof's deep mechanism.
017-SPINE-01 and 017-BRIDGE-01 are **source lookup controls**. Since they expose identifiers, a model may pass by copying exact source strings.
017-TRANSFER-01 is deliberately **unscored** until an independent formal or mathematical oracle has been prepared.

## Anti-leakage and grading rules

- Snapshot the proof corpus at a recorded commit and do not mix tasks with source revisions.
- Split by result family, not manuscript. Companion papers and proofs in the same family must not straddle train and test.
- Literal name retrieval is not conceptual understanding. Require new, separately verified targets for any claimed transfer.
- A proof failing after hypothesis deletion does not imply a false statement. Correct abstention is a legitimate outcome.
- A comparator challenge file containing `sorry` is a goal template. Inspect its configured solution module before claiming a proof gap.
- Never treat a local source invocation graph as the full logical proof dependency graph.
- For no-oracle tasks, report 'pending', not correctness or model accuracy.

## Commands

    node research/proof_understanding/scripts/validate_pilot.mjs .
    node --test research/proof_understanding/tests/pilot_validation.test.mjs

## Next research gates

1. Read the actual paper and the abridged reasoning summary for 017. This initial source audit has NOT independently audited the PDF content.
2. Follow the geometric and analytic dependency chain; identify at least one mathematical mechanism not recoverable by name lookup alone.
3. Construct 1–2 genuinely held-out proof/transfer problems with independent oracle.
4. Only then run model baselines. No HCI experiment required.
