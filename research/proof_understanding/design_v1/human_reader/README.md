# Human-facing proof understanding (development pilot)

**Why:** The primary beneficiary is a human mathematical reader trying to understand and critically audit AI-generated research proofs. We are not evaluating an AI-to-AI mathematics quiz as the end goal.

- 017_READER_GUIDE.md: why a local rational-parameter threshold is sharp, with a counterexample to derivative-only overgeneralization.
- 197_READER_GUIDE.md: why a right-neighbor group-algebra operator yields conditional injectivity and nonsurjectivity, while the hard GROUP existence claim remains unverified.
- HUMAN_EVAL_PROTOCOL.md: proposed controls and *objective* human understanding/uncertainty measures; no participants have been recruited or evaluated.
- check_guides.py and tests/: machine-readable provenance, unknown-disclosure, reference-marker and source-SHA checks. **Only checks a limited declared contract, NOT proof semantics or pedagogical efficacy.**

Commands, from repository root:

    python3 -m unittest discover -s research/proof_understanding/design_v1/human_reader/tests -p 'test_*.py' -v
    python3 research/proof_understanding/design_v1/human_reader/check_guides.py --repo-root . --require-original

The last command requires the actual source197 TeX present in the checkout. No model or paid API is required. All questions embedded in guides are *public development self-checks*, never hidden evaluation tasks. References in HTML comments are deliberately unobtrusive evidence ledger keys; this script verifies their presence, not their human-friendly correctness.

## Iteration 12: public claim-versus-proof audit lab

New [audit_lab](audit_lab/README.md) separates theorem-claim status from validity of a particular proof. It supplies nine researcher-authored public development cards, a separate answer key, exact rational/noncommutative witnesses and 12 additional tests. Two cases intentionally contain a **bad proof step for a true local theorem**. Unknown means source high-level truth was not independently audited, NOT false or undecidable. Details: [Iteration 12 report](../reports/2026-10-11_iteration12_dual_axis_human_audit.md). No human study or automatically generalized producer is claimed.
