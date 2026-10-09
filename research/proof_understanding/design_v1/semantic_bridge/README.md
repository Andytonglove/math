# Semantic Contract and Translation-Risk Audit — 2026-10-10

**Research purpose:** support *Understanding AI-Generated Mathematical Proofs* with a bounded **faithfulness gate**. The original paper may be wrong, the Lean statement may be valid but not correspond, and an extracted explanation may preserve a different argument. We must track these three questions separately.

This is an adversarial local diagnostic, not a universal natural-language-to-Lean semantic equivalence checker.

## New primary source
Alexander Bastounis, Fabian Circelli, Anders C. Hansen, *Navier–Stokes lost in translation: Why Lean verification of AI autoformalisation does not guarantee correct natural language proofs*, arXiv:2610.08144v1, submitted 2026-10-06. https://arxiv.org/html/2610.08144v1

Theorem A.3 identifies a **particular** presupposition-existence problem that is Sigma^0_2-complete, which is strictly beyond a single halting oracle. Theorem A.4 constructs instances at arbitrarily high finite arithmetical hierarchy levels. Interpret SCI=∞ in this precise *unbounded-level worst-case* sense; it does not mean each mathematical sentence is harder than halting, nor prove that selective/conditional translations are impossible. An algorithm may refuse to certify undecidable or underspecified cases.

The paper offers source/Lean mismatches in Navier-Stokes:
- NL m+4 versus a compared Lean estimate using m+5 input derivatives (Section 3.1). Independently inspected Lean theorem source at pinned commit; did not independently audit the entire NL or recover a bridge theorem.
- Pressure-flux estimate contains extra A_R in Lean (Section 3.2), and quantification changes from almost-everywhere to everywhere for t, though whole propositions also have different assumptions and RHS, so no unqualified global implication should be claimed.
- Example 2.1 shows a valid theorem with a **false natural-language factorization** silently repaired by an alternative correct Lean proof.
- Example 4.3 illustrates a least-natural-number presupposition where Nat.sInf(empty)=0 replaces an undefined mathematical object.

The exact local tests and machine-readable cards are in cases_v0.json, contract_audit.py, and tests/. They detect these **restricted discrepancies**, with explicit evidence-tier caveats. A passing test certifies only the local arithmetic/symbolic check, not the research-grade Navier-Stokes proof or original author's intended semantics.

## How this changes the core project's output
Every Evidence-Carrying Mathematical Understanding Artifact now needs a **Semantic Contract**:
1. Original mathematical claim and its definitions/domains/hypotheses/quantifier order/regularity/conventions.
2. Exact formal statement, axioms and verification scope when Lean is provided.
3. Scoped correspondence links: matched, formal-weaker, formal-stronger, incomparable, proof-method-different, or unresolved.
4. Distinct evidence for *statement faithfulness* and *proof mechanism faithfulness*.
5. Unresolved bridge obligations (e.g. how to derive an m+4 estimate from available m+5 inputs); do not declare their absence a proof that the original theorem is false.
6. A no-silent-repair policy: if the source argument is incorrect, flag that; offer a corrected proof only as a separately labelled new artifact.
7. Selective abstention: undecidable preconditions or missing mathematical semantics remain UNKNOWN with precise missing information.

This becomes a gate **before** artifact freeze and independent transfer. A source-mismatched artifact can solve downstream problems about a changed theorem; that performance must not be counted as understanding the original theorem.

## Tests
From repo root:

```bash
python3 -m unittest discover -s research/proof_understanding/design_v1/semantic_bridge/tests -p 'test_*.py' -v
python3 research/proof_understanding/design_v1/semantic_bridge/contract_audit.py \
  --input research/proof_understanding/design_v1/semantic_bridge/cases_v0.json \
  --output /tmp/semantic_contract_audit.json
```

No paid model inference. No complete Lean build. Five source-linked cases and six tests are **development diagnostics**, not headline accuracy or new undecidability proofs.
