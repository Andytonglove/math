# Iteration 11 — Recenter on HUMAN understanding of AI-generated proofs

Date: 2026-10-10, Singapore/China local time. Branch: research/proof-understanding-pilot. Start SHA: 76cb44a3fca139e011f39818b862b0e784e64a50.

## 1. Primary scientific correction

The user clarified the original problem: the ultimate beneficiary must be a HUMAN mathematician facing an unfamiliar, potentially extremely long and error-prone AI-generated research proof. We previously overemphasized the ability of a second model to answer unseen math questions. Machine mathematical transfer is an informative **instrument** for checking what a representation retains, but it does not establish that people can understand the proof.

**Revised central question:** Can an evidence-carrying, mathematically scoped explanation of a machine-generated proof help a human reader (i) grasp its key construction and necessary assumptions, (ii) independently check a nontrivial local step, (iii) find an invalid implication or overgeneralization, and (iv) recognize an honestly unresolved high-level claim—better or more efficiently than the original source and strong, token-matched natural-language competitors?

The project does **not** infer a generator model's private reasoning process, equate feeling of clarity with true understanding, certify every underlying OpenAI manuscript, or claim general user-study results from AI-to-AI proxies. Graph is a candidate interface only.

## 2. Actual delivered files and what they accomplish

- human_reader/197_READER_GUIDE.md: human-readable conditional group-algebra/operator proof, including the right-neighbor word order guv, the left-inverse injection argument, image as a fixed-point set, explicit delta_h exclusion, and GROUP-versus-MONOID scope. Five references link prose steps to recognized conditional producer claims. **The original GROUP existence theorem is UNKNOWN to this project.**
- human_reader/017_READER_GUIDE.md: intuitive feasible-gap ratio and sharp source auxiliary threshold nu>2, then the weighted convex-polynomial extension under a GLOBAL tangent identity. A concrete nonconvex counterexample prevents invalid inference from endpoint derivative alone. Three evidence markers link to O1–O3 exact local derivations. **The original advanced pi proof has NOT been independently verified, nor generalized.**
- human_reader/HUMAN_EVAL_PROTOCOL.md: four information-budget-aware human-reader controls, objective proof comprehension/audit/transfer rubrics, calibrated UNKNOWN and confidence, reading effort and participant/expertise/source-family controls. This is a **design**, not a completed experiment.
- human_reader/check_guides.py: standard-library fail-closed *provenance and disclosure* gate. Checks 197 producer status, 197 source SHA-256 against the unchanged original TeX when supplied, five 197 claim references, 017 independently-derived O1/O2/O3, O4 unverified, six section/disclosure obligations per guide, and explicit unresolved matters.
- human_reader/tests/test_guides.py: 11 unittest cases, including rejection of blocked source, missing claims, missing disclosures, unsupported proof references, promoted unverified 017 claims, lost evidence tier and corrupted original source SHA.
- .github/workflows/proof-understanding-human-reader.yml: sparse checkout of these files and the **actual** original 197 TeX; runs 11 Python tests and the require-original audit. No hosted paid model call.
- Updated CORE_RESEARCH_CHARTER.md, MANUSCRIPT.md, PROTOCOL.md and MASTER_PLAN.md to state human mathematical understanding/auditing as the *primary* target. Prior mathematical material remains as carefully scoped infrastructure.

The two explanatory guides are HAND-AUTHORED research development examples. The earlier deterministic 197 TeX recognizer is unchanged and does not automatically produce these guides. Creating a general and mathematically faithful explanation producer is still an open research milestone.

## 3. Exact mathematics actually used

**197:** For finitely supported c, (T_c x)(g)=sum_u c_u x(gu). Associative index multiplication and finite regrouping yield T_c T_d = T_(cd). Under **conditional** hypotheses ab=1 and ba!=1, T_a T_b=I; hence T_b injective. P=T_b T_a is an idempotent with image(T_b)=Fix(P). For a coefficient h where (ba-1)_h !=0, (P-I)delta_h evaluated at the identity is nonzero, so delta_h is excluded from the image; T_b is not surjective. This *does not* provide a group-algebra witness a,b satisfying those hypotheses. In a MONOID the same conditional mechanism works, but existence of a MONOID counterexample does not imply existence of the original GROUP witness. Original Lean semantics remain unreviewed.

**017:** For f(A)=A^2, 0<theta<A<1 and theta>A^2 force (A-theta)/(1-theta)<A/(1+A)<1/2, so nu>2 is necessary. The limit A→1 supplies rational feasible choices for each nu>2. For positive rational mixtures sum_i w_i A^{r_i}, exact polynomial tangent-gap identity proves a different threshold nu>s/(s-1), where s=sum w_i r_i. The global inequality is essential: the separately derived nonconvex h(A)=A²-3A³(1-A)² has h'(1)=2 but at A=3/4, theta=31/64, nu=39/20 satisfies h(A)=495/1024<theta=496/1024 with nu(A-theta)-(1-theta)=3/1280>0. This is a counterexample to a DERIVATIVE-ONLY extrapolation, NOT to the source high-level pi theorem. Fractions were recomputed locally with Python Fraction this round.

## 4. Executions and evidence (not invented human gains)

A local fixture checkout was assembled only to test the new guide gate: 11/11 Python unittest methods passed, including require-original for a controlled fixture file. A separate exact Fraction script recomputed the 017 witness values quoted above.

After commits ffb58c2 (guides) and 4a61fa5 (source gate, tests and CI), GitHub Actions run **38020692302** completed successfully. Its log states "Ran 11 tests in 0.003s" and "OK"; its real-repository audit reports source197_sha_checked=true, 5 referenced producer claims, 3 derived obligations, high_level_source_theorems_verified=false and human_outcomes_measured=false. Full log: https://github.com/Andytonglove/math/actions/runs/38020692302 . Other pilot CI runs 38020692308 and 38020758538 also completed successfully, including after changes to the charter and manuscript.

Raw result fields were versioned at human_reader/evidence/iteration11_gate_audit.json. The updated status/SPRINT_STATE.json records no paid model run, zero human participants and no source-high-theorem/Lean verification. The action uses hosted CI runtime, but actual account billing or free quota was NOT audited; do not infer verified $0 infrastructure spend.

A diff from base commit 76cb44a3 to the interim update at 5a803474 touched only research documentation/new human_reader code and its new workflow. No preprint source, original frozen197 artifact or main branch was edited.

## 5. Honest scientific limitations and competing explanations

1. **No human causal evidence:** nobody read these guides as a study; no measured effect size, preference, comprehension, reading time or calibrated confidence. A human-authored explanation may be just a good summary.
2. **No general explanation generator:** existing producer recognizes predeclared 197 TeX anchors; guides were manually prepared. A script checking markers/sha/unknown text is NOT a semantic proof checker and can accept persuasive false text.
3. **Source validity unverified:** local operator identities and rational calculations do not validate the full research-level 197 group construction or 017 pi theorem; source-to-Lean correspondence remains unknown.
4. **No independent held-out human assessment:** questions embedded in guides are explicitly public self-checks. They may be answered without reading the original paper; using them as hidden test items would contaminate an experiment.
5. **No comparable summary/excerpt dataset yet:** the proposed controls and fairness constraints exist on paper, not as completed stimuli or outcomes.
6. **No paid models/GPU:** no new inference was authorized or used. Prior incomplete Qwen CPU reader (10/24 prompts completed, 0 correct among these ten) remains uninterpretable for comprehension benefit.

## 6. Research positioning and what is actually novel *if validated*

Existing work addresses multi-dimensional proof comprehension (Mejía-Ramos et al. 2012), Lean-backed tutoring (LeanTutor AAAI 2026), interactive proof blueprints (MathCoPilot 2026) and the mismatch between self-reported understanding and objective correctness. The potential contribution is not a proof diagram or AI tutor. It would be a source-anchored, mathematically faithful *research-level* explanation that communicates proof obligations and exact epistemic limits and is shown to improve HUMAN mathematical audit/understanding under fair controls. This is currently a **hypothesis**, not an achieved empirical contribution.

## 7. Next decisive questions

A. Can a non-template producer, initially on a truly unseen source family (not a recognizer prewritten for 197), generate a mathematical human reader guide preserving premises, critical proof steps, counterexamples and UNKNOWN? Evaluate faithfulness with independent mathematicians or local independently proved units before making any human-comprehension claim.

B. At matched mathematical information and reading length, do human readers actually become better at source-specific counterfactual and proof-gap detection relative to a strong plain summary or a curated source excerpt? Randomize by proof family and reader expertise, use blinded mathematical rubrics and preregister confidence/overconfidence measures; ethics/consent requirements precede human participation.

C. Can explanations help readers detect that a source itself is wrong, instead of silently repairing its argument? Explicit error localization and incorrect theorem/incorrect proof distinctions are required. Abstention must not win simply by being universal.

**Current bottom line:** A human-facing research target is now explicit, two manually derived proof guides and source-bound checks exist and CI passed. This is a bounded tangible iteration, NOT evidence that humans understand better or that AI has automatically explained difficult proofs.
