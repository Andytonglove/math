# Human mathematical proof comprehension: pilot protocol v0.1

**Primary target:** Help a human mathematician understand, audit, and responsibly use an AI-generated proof. AI-to-AI transfer is a diagnostic secondary track, NOT a demonstrated proxy for human benefit. No human experiment has been run.

## Task and scope

Each unit is a bounded proof segment with source/version and imported assumptions. A human-facing evidence guide should answer: what is the proof trying to do, why this construction is chosen, which exact step does the work, where could it break, what may be reused, and what remains unverified? A readable but mathematically false explanation is a failure even if readers report liking it. The guide does not reconstruct the discovery model's private deliberations.

The v0.1 case studies 017 and 197 are HUMAN-AUTHORED public development materials; the source197 deterministic extraction code only verifies specific anchors. Source and artifact correctness are not established by CI alone. Treat the entire source main theorem as unverified unless independently reviewed. Do not use these two disclosed examples as blinded held-out tests.

## Distinguish three scientific targets

1. **Faithfulness and evidence** (expert/math oracle): check claims, assumptions, quantifier scopes, source provenance, exact derivations, negative counterexamples and unverified areas; a broken argument is not a false theorem.
2. **Objective human comprehension** (human reader): ask for the proof's key idea, explain a nontrivial step, predict changes under a counterfactual, locate a flawed inference and correctly answer UNKNOWN when evidence is insufficient.
3. **Communication cost and calibrated trust**: elapsed reading/response time, accessed pages, confidence versus accuracy, willingness to make an unsupported downstream claim. Self-reported clarity is only secondary, never a substitute for performance.

## Controlled comparisons and assignment

- C0: unmodified original proof segment with stated common background.
- C1: independently authored ordinary prose summary, source-faithful and **token-budget matched** to the evidence guide; no hidden answer key or oracle.
- C2: source excerpt plus glossary, budget matched (controls for simple selection of the right lines).
- C3: human-facing evidence guide: contract + causal proof mechanism + local derivation + source anchors + conditional boundaries + explicit unknowns.
- Optional C4: graph or interactive presentation with **the same mathematical claims and evidence**, not extra insights.

A participant must not see multiple presentations of the SAME proof before answering; instead balance conditions across distinct proof families and participants. Pretest baseline mathematical background and notation familiarity; stratify by expertise. Give identical task queries and permitted reference aids across arms. Preregister family-level holdouts and rubrics *after freezing outputs*, with graders blinded to condition. Avoid giving near-identical numeric variants across conditions or using public guide self-check prompts as secret test questions.

Suggested later pilot: recruit willing math-trained readers only after research ethics/consent review and a feasible independent mathematical assessment. No number of participants, effect or power claim is established by this document. If source itself may be wrong, include an independent validity audit and report source correctness separately; never score accepting a false source premise as successful comprehension.

## Proposed measures (not observed)

- Mechanism explanation: expert-coded 0/1/2 for correct construction, why it works, and where premises enter; blind double-grade a subset and adjudicate disagreements.
- Logical audit: objectively correct identification of scope changes and proof-gap localization, not simply guessing YES/NO.
- Conditional transfer: exact oracle or full solution rubric with novelty checked separately; ensure the base mathematical question is not trivially answerable without the source.
- Calibrated UNKNOWN: score correct justified abstention AND warranted confident conclusions. Track unsupported-confidence rate and coverage; do not let universal abstention achieve a high score.
- Efficiency: task time, source lookups and reading tokens/pages. Separate time to build a guide from time to read it; do not invent measured speedups.

**Main estimand:** paired or stratified difference in objective comprehension score between C3 and the strongest C1/C2 control on source-family-held-out tasks, alongside uncertainty calibration and reading cost. Pre-register minimum important effect and sample size only after a pilot variance estimate; participant and proof-family clustering is necessary.

## Why this is not a generic proof tutoring app

The scientific object is a *faithful explanation interface to a specific unfamiliar research proof*, with explicit evidence, conditional validity and epistemic limits. The project does not claim novelty in simply paraphrasing or visualizing math, nor in Lean compilation. Possible contribution requires a reproducible producer plus independent evidence that people gain correct mathematical insight or audit ability rather than misplaced confidence.

## Relevant prior work (positioning, not novelty claims)

- Mejía-Ramos et al. (2012), An Assessment Model for Proof Comprehension in Undergraduate Mathematics: proof comprehension is multidimensional, beyond step-by-step correctness. https://eric.ed.gov/?id=EJ948400
- Patel et al. (AAAI 2026), LeanTutor: Towards a Verified AI Mathematical Proof Tutor: natural-language tutoring plus formal verification is an existing line, not our invention. https://ojs.aaai.org/index.php/AAAI/article/view/41514
- Zhang et al. (2026), MathCoPilot: interactive human–AI mathematical research and living proof blueprints already exist. https://arxiv.org/abs/2607.14582
- Does understanding moderate aesthetic appraisals of proofs? (Journal of Mathematical Behavior 2026): self-reports and performance-based comprehension may diverge; motivates objective outcomes. https://www.sciencedirect.com/science/article/pii/S0732312325000483

## Evidence before any positive claim

Freeze producer and guides; independently select untouched paper families and hidden comprehension questions; mathematically audit key answers; carry out a controlled and ethically appropriate reader study; report raw anonymous outcomes, failures, attrition and time/cost. Until then report HUMAN_COMPREHENSION_EFFECT=NOT_MEASURED and PRODUCER_GENERALIZATION=NOT_MEASURED.
