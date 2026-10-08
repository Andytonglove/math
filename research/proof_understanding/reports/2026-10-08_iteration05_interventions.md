# Iteration 05 — Proof Surgery and First Open-Model Evidence

**Date:** 2026-10-08  
**Branch:** research/proof-understanding-pilot  
**Core project:** Understanding AI-Generated Mathematical Proofs

## Research objective

Study whether machine systems preserve and can operate the mechanisms of AI-generated mathematical arguments under **counterfactual interventions**. The Graph is only a proposed representation. Source-level parsing, algebraic sanity checks and measured model behavior must never be conflated.

We deliberately began with mathematically checkable *subroutine* abstractions of two OpenAI/math manuscripts. The original deep theorems remain **unverified by our independent project**.

## Family 017 — two-case determinant bound surgery

Source anchors: determinant.tex det:lower, det:comparison, det:upper.

The source proposes a lower bound L=-(1-b)-Ea and two alternative upper bounds:
- collision: Uc=En-C;
- approximation: Ua=En-nu*(A*(1-eta)-b).

Under the abstract limiting certificate, a two-case proof closes only if **Uc<L AND Ua<L**. The generator changes C or eta, creates both failure variants and strict-equality boundary variants, and uses **exact rational arithmetic**. A second, independently rearranged inequality implementation checks every answer.

Development dataset (seed 26008, 12 base instances):
- 72 distinct algebraic interventions, 504 rendered prompts across 7 information conditions.
- Oracle labels: BOTH=12, ONLY_COLLISION=24, ONLY_APPROX=24, NEITHER=12.
- Exact AND calculator: 72/72. **Deliberately invalid OR shortcut: 24/72**. These are deterministic algorithm checks, not model observations.
- 6 script tests passed in GitHub Actions. In unit tests, a range of other random seeds/perturbations was also checked.

**Important limitation:** The no-proof prompt already includes all algebraic formulas and exact values needed. This eliminates missing-information leakage but makes the task solvable without any proof access. It tests source-context utility for *executing a two-case certificate*, not deep understanding of the entire irrationality exponent proof.

## Family 102 — logical quantifier surgery

The source claims a hardness reduction with quantifier order FORALL fixed approximation errors e; EXISTS an alphabet/reduction witness s; FORALL input formulas phi.

A 3-by-3-by-2 finite Boolean predicate P(e,s,phi) gives independently enumerable countermodels for:
- STRONG: exists s forall e forall phi;
- ORIGINAL: forall e exists s forall phi;
- WEAK: forall e forall phi exists s.

Twelve randomized finite models of each of the four logically distinct patterns yield 48 tasks and 336 contextualized prompts. Oracle label distributions: 111=12, 011=12, 001=12, 000=12. Both direct enumeration and set intersection oracles agree. All 4 focused unit tests passed.

This is a test of quantified statement meaning, not a verification of the complex Unique Games hardness reduction. The predicate P is synthetic and does not assert any finite model of the claimed actual reduction.

## Total data and scope

**120 development tasks**, **840 prompt renderings**, and **two distinct independently checkable mathematical oracle families**. All test examples and answers generated for CI are **public development data**, not a contamination-safe test set.

Sources and scripts:
- scripts/determinant_surgery.py; tests/test_determinant_surgery.py
- scripts/quantifier_surgery.py; tests/test_quantifier_surgery.py
- scripts/smoke_open_model.py; tests/test_smoke_open_model.py
- evaluation/DETERMINANT_SURGERY.md; evaluation/QUANTIFIER_SURGERY.md

## Actual model pilot: Qwen2.5-0.5B-Instruct, CPU, no paid API

Completed GitHub Actions run: https://github.com/Andytonglove/math/actions/runs/37779018026

32 paired responses: 4 sampled labels from each of two families, each in minimal / proof / prose / hypergraph conditions. Greedy decoding, max_new_tokens=48. Total model download + evaluation: **150.4 seconds** on a GitHub hosted public runner.

The original strict JSON parser incorrectly treated Markdown-fenced JSON as invalid. Downloading and inspecting the full raw artifact exposed that mistake. **Corrected analysis (accept only exact raw JSON or one well-formed fenced JSON object, never coerced schemas):**

| Family | Minimal | Proof | Prose | Hypergraph |
|---|---:|---:|---:|---:|
| 017 exact answer content | 1/4 | 1/4 | 1/4 | 1/4 |
| 102 exact answer content | 0/4 | 0/4 | 0/4 | 0/4 |

On 017 the model returned **the same ONLY_COLLISION label for all 16 prompts** regardless of condition. Minimal 017 responses were strict JSON; the other three conditions were commonly Markdown-fenced JSON, so their strict-format compliance differed although mathematical responses did not.

On 102 all four conditions produced improperly shaped answers (e.g. a list of strings where one three-bit string was required, together with an unrequested extra key). They cannot be graded as correct quantifier classifications. This is a **model / output-format bottleneck**, not evidence that the original mathematical idea is unknowable.

**Conclusion:** No observed graph or proof-context benefit in this tiny, underpowered, non-statistical pilot. Do not infer that graphs are useless on stronger models, or that source-proof understanding has been measured at research level.

Further bounded 1.5B model run: launched after fixing the parser and is documented separately once completed. Do not infer results or success in advance.

## Environment validation and failure transparency

- Cross-family source graphs: Actions 37775212838 PASS.
- Both exact-surgery datasets and independent oracles: Actions 37778505378 PASS.
- Expanded 017 surgery: Actions 37778125462 PASS, six tests.
- Open-model first workflow submission 37778928279 FAILED at YAML evaluation (job-level runner context); fixed.
- Open-model 0.5B run 37779018026 PASS.
- Scorer change caused regression 37779702044 / 37779769155: a test expected a renamed summary field; fixed by updating the test; run 37779872166 PASS.
- The first 1.5B workflow run 37779800191 used the pre-fix checkout and failed at this unit test; new run triggered after the correction.

No full Lean Comparator compilation, no expert mathematical validation of OpenAI/math, and no Human Experiment. No paid inference API calls. Compute used public GitHub Actions resources; no monetary charge amount is claimed.

## Literature positioning

Related work includes ProofFlow (ICLR 2026: proof dependency graph and semantic-faithful autoformalization), T-squared (ACL 2026: theorem testing via successor proof compilation) and TheoremBench (2026: premise-rich theorem proving). We must not claim to be the first to study proof structure, premise ablation or statement fidelity.

The intended distinction is to evaluate whether **reading a newly produced research proof causally changes success on independently verified, source-specific *new mathematical interventions***. The current pilots do not yet meet this strong criterion.

## Go/no-go and next investigations

1. Upgrade model capacity with clear paid-cost controls and **hold out source-specific tasks**. Current 0.5B results are dominated by a constant-response failure and schema errors.
2. Separate **format compliance** from **mathematical content accuracy** and **reasoning explanation correctness**. Never treat a fenced JSON block as a mathematical error.
3. Add true source-conditioned proof transplants, not just formula exercises. Pre-register an explicit no-proof baseline that remains information-sufficient.
4. Match context token budgets, counterbalance prompt ordering, and use paired statistics clustered by common generated base case rather than treating all interventions as independent samples.
5. Keep Graph vs token-matched prose as an empirical comparison; abandon the Graph approach if it fails to improve independently validated transfer.
6. Never assert a major mathematical theorem is true merely because a proof manuscript or unchecked Lean file exists.

## Exact reproducibility commands

From repository root:

    python3 -m unittest discover -s research/proof_understanding/tests -p 'test_determinant_surgery.py' -v
    python3 -m unittest discover -s research/proof_understanding/tests -p 'test_quantifier_surgery.py' -v
    python3 -m unittest discover -s research/proof_understanding/tests -p 'test_smoke_open_model.py' -v
    python3 research/proof_understanding/scripts/determinant_surgery.py --source-root . --seed 26008 --bases 12 --out-dir /tmp/proof_surgery_017
    python3 research/proof_understanding/scripts/quantifier_surgery.py --source-root . --seed 10267 --bases 12 --out-dir /tmp/quantifier_surgery_102

Inference is provided in the bounded GitHub workflow; use a fixed open model, strict external resource limits and record inference logs before drawing conclusions.
