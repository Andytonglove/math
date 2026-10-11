# Human proof-audit development lab (Iteration 12)

**Intended beneficiary:** human mathematicians who must understand and critically audit AI-generated research proofs. These are PUBLIC RESEARCHER-AUTHORED DEVELOPMENT CASES. They do **not** measure any human benefit and do **not** certify either complete 017/197 source theorem.

## Use

From the repository root:

    python3 research/proof_understanding/design_v1/human_reader/audit_lab/audit_cases.py
    python3 -m unittest discover -s research/proof_understanding/design_v1/human_reader/tests -p 'test_*.py' -v

Only Python standard library is needed. No paid inference or human data. The generator deterministically creates:
- data/cards_public_dev.json: prompts, source-family labels and proposed proof snippets, **without answer keys**.
- data/gold_public_dev.json: the *public* two-axis answer key, scopes, expert-readable derivations and evidence tiers.
- data/checks_public_dev.json: exact Fraction witnesses and finite S3/monoid sanity checks.

The checked-in exact diagnostics record is a snapshot of the same calculations. Cards and gold are **public**: they must never be used as hidden evaluation items. Case author, oracle writer and implementer are not independent.

## Why two axes?

- Claim status: LOCALLY_ESTABLISHED / EXACTLY_REFUTED / NOT_INDEPENDENTLY_AUDITED.
- Proposed reasoning: VALID_LOCAL / INVALID_STEP / NOT_AUDITED.

An erroneous proof may accidentally conclude a true theorem. Identifying its bad step does NOT refute the underlying theorem. Similarly an audited conditional lemma does not certify an unverified source-level existence assumption. The two UNKNOWN claims concern mathematical claims not independently audited here, not the objectively false assertion that *this project already checked them*. UNKNOWN does not mean undecidable.

The label-only scorer flags (1) promoting UNKNOWN to certified and (2) incorrectly refuting a true theorem because a displayed proof step fails. It cannot grade natural-language mathematical explanations. That requires blinded expert grading.

## Exact limited checks

- Rational h(A)=A²−3A³(1−A)² counterexample: A=3/4, theta=31/64, nu=39/20, exact feasibility margin 3/1280. This refutes a derivative-only **generalization**, not the original pi theorem.
- An invalid inequality A−theta>A−A² is refuted by A=3/4, theta=5/8, while the actual nu>2 necessity stays true.
- 216 S3 associativity samples and explicit noncommuting transpositions expose a swapped-factor proof error; universal commutation of left and right operators follows from a separate algebraic derivation, not finite enumeration.
- Natural-number shifts L(R(n))=n, R(L(0))=1 demonstrate a MONOID algebra defect, never a source GROUP algebra counterexample.

See reports/2026-10-11_iteration12_dual_axis_human_audit.md for the complete scope, mathematical argument, local test evidence, limitations and proposed study gate.

**Not done:** new automatic producer, unseen-paper generalization, independent high-level theorem audit, Lean semantic equivalence, actual human-reader comparison, machine-reading benefit or any paid model call.
