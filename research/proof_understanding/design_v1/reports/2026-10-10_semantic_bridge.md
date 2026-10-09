# Iteration 07 — Lost in Translation and the semantic-fidelity gate

Date: 2026-10-10 Asia/Shanghai
Repository: Andytonglove/math
Branch: research/proof-understanding-pilot

## New source and carefully bounded conclusion

Read arXiv:2610.08144v1, sections 2–4 and appendix A, including the A.3 Sigma^0_2-completeness result and A.4 arbitrary finite arithmetical levels. SCI=infinity concerns an unbounded hard family of existence-presupposition tasks. It does not mean each NL-to-Lean translation is independently undecidable.

Read two OpenAI NavierStokesAndEuler Lean declarations at commit f9e8bc5b38b6e212696e8a30e3e91517af887bbd: an inverse theorem explicitly uses w.length+5 input jets; a pressure-flux theorem includes gradient/dissipation dependence. The arXiv paper reports m+4 and a B_R-only estimate in the source natural-language paper. No full source-LN equivalence proof, theorem refutation, or expert PDE review has been performed.

## New implementation and actual CI

research/proof_understanding/design_v1/semantic_bridge/ now contains:
- contract_audit.py: restricted algebraic/scoped semantic discrepancy checks;
- cases_v0.json: five source-associated cases: derivative-loss shift, extra RHS symbol, a.e.-vs-all time quantifier, false factorization silently repaired, and an undefined least-number presupposition;
- tests/test_contract_audit.py: six unit tests and explicit failure for unknown case kinds;
- README.md: mathematical evidence scope, provenance, no-silent-repair policy.

GitHub Actions run https://github.com/Andytonglove/math/actions/runs/37958200358 completed successfully: 6/6 tests, 5/5 exact local assertions. Generated result explicitly says semantic_equivalence_of_full_NL_and_Lean=NOT_ESTABLISHED, model_inference_runs=0.

Polynomial example: p(x)=x^3-x^2-x+1. False factorization (x-1)(x+1)^2 has value -1 at x=0 while p(0)=1; correct factorization is (x-1)^2(x+1). Source theorem truth and proof argument correctness are separable.

Presupposition example: p(n,x1,x2)=x1+x2-n has root (n,0) for every natural n, so no least root-free n exists. Returning Nat.sInf(empty)=0 is a different totalized definition. We have a symbolic universal witness, not only a finite search.

Regularity example: derivative-order difference m+4/m+5 is visible. Generic high-frequency f_n gives a norm countermodel to arbitrary norm implication, NOT to the specific Navier–Stokes inverse operator. Additional A_R dependence and time-quantifier differences are partial contract comparisons, not a certification of global implication.

## Conceptual change to project

Understanding AI-Generated Mathematical Proofs stays the research title. Add a Semantic Contract gate between source/Lean materials and our frozen proof-to-knowledge artifact:
- compare intended theorem and actual formal proposition;
- distinguish theorem equivalence from proof-method equivalence;
- explicitly preserve quantifiers, domains, regularity and side conditions;
- never silently replace an invalid source argument with another correct proof;
- mark unproved bridging obligations UNKNOWN;
- require independently useful artifact-only downstream reasoning, not just source-aligned text generation.

## Novelty threats and next step

Beyond Compilation (latest v3), FaithformBench, Robust Proof Autoformalization, The Faithfulness Gap, ProofFlow and LeanArchitect already address semantic drift or graph fidelity in some form. An NL/Lean mismatch detector alone is not enough. No new model inference or paid APIs were used. CI passing is not PDE verification.

Next: freeze one evidence-carrying mathematical abstraction BEFORE task sampling, run an independent source-deprived reader on new mathematically checked tasks, and compare against length-controlled extracts/summaries. Include mismatch and invalid-source negative controls and report selective coverage, unwarranted certification, transfer and cost. Existing pilot is not yet that experiment.
