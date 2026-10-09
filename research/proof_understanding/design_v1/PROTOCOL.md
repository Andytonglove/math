# Producer–artifact–consumer protocol v0.1

A source unit is a bounded complete argument with explicit imported assumptions. The producer sees source, background, intended audience and communication budget, but not realized evaluation queries or gold answers. Development queries are allowed and disclosed.

The producer freezes a versioned/hash-identified artifact containing claim contract, mechanism, proof obligations, boundaries, reusable statements, evidence and unresolved matters. The consumer starts in a fresh session with artifact, common background and new query. In the primary track it cannot fetch the original proof or a renamed equivalent. Retrieval/augmentation is secondary and logs every call and token.

## Baselines

Background; Statement; full selected Source; budget-matched Extract; ordinary Summary; evidence-carrying Artifact-Prose; same-mathematical-content Artifact-Graph; optional Source+Artifact. Main comparison is artifact versus summary/extract and source-retention/cost; graph is a second-level ablation.

## Validity controls

- Equal query definitions and explicit permitted background, without target answer/theorem wrappers hidden in the background.
- Artifacts frozen before realized test query selection; structural and source-family holdout, not only changed random numbers.
- Opaque IDs, independent exact or mathematically justified oracle, no gold in prompts or retrieval.
- Public development examples cannot be reused as secret tests. Deduplicate exact and structural tasks.
- Separate source location, independent derivation, finite enumeration, formal checking, semantic correspondence and expert review.
- A failed proof search means unknown, not false. A disabled script does not establish necessity of an assumption.
- Mathematical correctness, unsupported statements, explanation coverage, parser compliance, abstention and cost are separate outputs.
- Empty artifacts cannot earn high faithfulness without coverage; a graph with extra useful claims must not beat prose by information imbalance.
- Correlated perturbations clustered by original proof/base construction; small pilot scores are descriptive only.
- AI origin recorded, not inferred from style. Match human-source controls where feasible.

## Success and limitations

A useful artifact may retain source-level utility at lower reading cost instead of beating an unlimited source reader. Report construction and amortized reuse costs separately. No human benefit is inferred from machine consumer results.

The old 0.5B/1.5B experiment is not a test of this protocol: contexts were manually prepared paraphrases and not independently frozen; all math task definitions were in the prompt; no true artifact-only reuse effect was isolated. The present two samples are manual development artifacts, not automatic-method results.


## 2026-10-10 semantic contract gate (mandatory before artifact freeze)

Record the original natural-language theorem as stated, with mathematical domains, definitions, hypotheses, quantifier order, regularity requirements and conventions. Where Lean artifacts exist, record their exact formal statement, trusted axioms and evidence scope; do not equate compilation of a different theorem with source verification.

Separate *statement correspondence* from *proof-method correspondence*: a valid alternative proof of a true theorem may be unfaithful to a false natural-language argument. The correct response to false source reasoning is to document the failure; a repaired proof must be a separately flagged contribution rather than a covert replacement.

Allow multiple simultaneously valid findings: different quantifier scope, extra RHS dependency, stronger input premise, different proof technique, or undefined source term. A simple surface mismatch does NOT always order full statements logically. Unresolved semantic bridges remain UNKNOWN with source anchors and explicit evidence tier. Do not turn a failed proof search into a theorem counterexample.

The A.3/A.4 hierarchy in arXiv:2610.08144 is an unrestricted definedness obstacle, not a prohibition on partial scoped checking. We do not promise a complete semantics-preserving NL/Lean translator. Evaluate selective accuracy jointly with useful coverage, and compare artifact-only reuse against information-budget matched prose and source snippets.

Add negative controls with invalid natural-language reasoning but true conclusions, source/formal derivative mismatch, unproven minimum-existence presupposition and different proof methods. The local instrument in semantic_bridge/ supports only five specific cases. A clean CI run is NOT a certificate that a whole research source or extracted mathematical mechanism is correct. The independent-reader transfer experiment is still outstanding.


## Pilot lessons: frozen-v1 chronology and limited reader evaluation

The 197 local operator artifact was pinned to Git commit 04fef27 before development tests were introduced in later commits; immutable content is checked via Git blob hash. This establishes chronological freezing **only**. Tests are deterministically derived from a public seed; model task designer and artifact author are not blinded to each other's mathematics. No contamination-proof research benchmark claim is permitted.

Two independent finite F2[S3] algebra implementations agree on 36 selected public tasks, and exhaustive regression checks pass. The frozen artifact-only model prompt does not provide the original paper, while the source excerpt appears in a separate control. But context information and token counts are not matched; a shorter correct summary already carries much of the same operator law information.

The Qwen2.5-1.5B CPU attempt at 24 prompts ended by timeout after 10, all correct-schema JSON but all incorrect masks. No complete paired result was produced; the first runner only wrote final JSON at experiment completion, so raw responses were not archived in this failed run. Checkpointing is now added for future executions. Do not infer an effect from the incomplete tiny-model outputs.

Prioritize symbolic mathematical statement/intervention analysis and source-specific novel transfer over bit-mask arithmetic, distinguish task design from ability validation, require a sufficiently capable and authorized reader, and separately score cost, schema and mathematical correctness.
