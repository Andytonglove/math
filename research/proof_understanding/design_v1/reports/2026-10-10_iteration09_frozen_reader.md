# Iteration 09 — Frozen evidence-carrying artifact → source-deprived consumer

Date: 2026-10-10 (Asia/Shanghai). Research branch: research/proof-understanding-pilot.

## Scientific objective

Implement one chronologically frozen, manually authored mathematical-understanding artifact and assess whether a fresh model without the original proof can use its conditional mathematical content. This is a **developmental mechanism-reuse pilot**, not automatic extraction or certified understanding of the source's research-level result.

## Evidence boundary and artifact freeze

Source family 197: conditional group-algebra action from 06-cellular-automata.tex. Original AI manuscript's existence claim about a finitely presented group with ab=1 but ba!=1 remains independently UNVERIFIED. Lean formal correspondence is UNKNOWN; the source-inspired elementary operator identities were rederived separately.

Artifact: design_v1/frozen/197_operator_artifact_v1.json; freeze commit 04fef27eed6f3a10e529f728f3f478cb459f0821; frozen Git blob a603b3877de63eaf90f336867fdd6f5b70467209. The task generator was created in a later commit and refuses mutated artifact content. No artifice automatically extracted this artifact: its producer was manually authored.

The artifact records the formal mathematical conventions, right-neighbor action, left-neighbor variant, proof obligations, conditional injectivity, fixed-point image description, explicit source-claim exclusions, and unresolved advanced-theorem / Lean-alignment status.

## A concrete reusable mechanism

For arbitrary group G and field K and finitely supported c,d in K[G], define T_c x(g)=sum_u c_u x(gu), S_d x(g)=sum_v d_v x(vg). The elementary algebra gives T_c T_d=T_cd and S_c S_d=S_dc. The new source-inspired transfer identity T_c S_d=S_d T_c follows directly because both sides at g equal sum_{u,v}c_u d_v x(vgu). This derivation uses only finite sums, scalar commutativity and group associativity; it does NOT depend on the source's proposed exotic counterexample.

An explicit noncommutative F2[S3] witness detects swapped composition order: a-mask 2, b-mask 4, delta at identity h=0. True right-right composition output mask 8; false reversed law produces mask 16. Left-left true output is mask 16; unreversed law would instead give 8.

## Actual implementation and reproducibility

- Frozen artifact is a stand-alone JSON mathematical knowledge object. Its construction precedes task design in the Git commit DAG.
- Generator: design_v1/consumer/generate_197.py, seeded deterministically from the **public** freeze commit; this is NOT a hidden evaluation. Source-deprived artifact and source-excerpt controls are separate prompt modes.
- 12 selected noncommuting base configurations, 3 operator tracks each, 36 gold-labeled tasks, 144 paired prompt records under background / ordinary summary / artifact / source excerpt conditions.
- All inputs explicitly define the full group law and operator actions, so a competent background-only reader can solve them without information missing from the task.
- Exact finite group-ring oracles: direct action on configurations and an independently coded permutation-tuple/product computation. Exhaustive test covers 64² coefficient pairs × 6 point indicators × 3 tracks = 73,728 paired oracle comparisons. Only 36 chosen tasks comprise the public development set.
- GitHub Actions run 37964597803: PASS, 12 Python unit tests including reader parser, schema and complete group algebra checks.
- GitHub development artifact 11632982470 was downloaded and CRC checked. ZIP contains 36 gold answers, 144 prompts and diagnostics. All 36 output masks were nonzero. There were 10 distinct right-track answers, 10 left-track answers and 8 mixed-track answers.

## Input information imbalance (important)

The average prompt character counts on the **actual archived 36-task development data** were approximately: background 705, ordinary summary 1249, frozen artifact 3193, original source excerpt 5804. These are not token-matched conditions; a reader comparison cannot establish causal superiority of graph/prose or superior sample efficiency. Record tokenizer token counts from real model runs.

## Failures logged and fixed

Initial post-freeze CI run 37963645893 failed because a validator demanded the exact string 'unknown' whereas the immutable artifact explicitly recorded 'unknown; not independently checked against Lean'. We repaired the validator to accept scoped UNKNOWN, without editing the frozen file. Later CI passed. The independent oracle was then strengthened not to share the original group multiplication implementation, and a concrete right/left order counterexample was added.

## Status at initial reporting

The bounded CPU-only Qwen2.5-1.5B model run was started at GitHub Actions run 37964028280, with up to two base instances per operator track and all four conditions. This is 24 paired responses, if fully completed. **The model result is not yet available at the time of this report version.** Do not infer a benefit or a failure before inspecting saved outputs.

## Limits and next scientific gate

Publication-level claims are blocked by: manual artifact production, same-researcher task design, public predictable seed, only a local 197 conditional lemma, unequal input budgets, tiny model and only two independent base-case clusters in the reader smoke test. The central question of source-to-knowledge transfer is therefore NOT solved.

Next prioritize a capable, authorized reader model with structural held-out mathematics and rigorous fidelity gate; a stronger summary/extract matched for *mathematical information and tokens*; a truly independent evaluator; and a future automatically generated artifact whose source claims are scrutinized rather than silently repaired.


## Final actual reader execution: bounded CPU model failed to finish, no artifact-benefit claim

The bounded Qwen2.5-1.5B-Instruct run https://github.com/Andytonglove/math/actions/runs/37964028280 reached its 950-second model time cap during a four-condition paired task set. Exactly **10 of 24 planned responses** were completed before the cap; all 10 were syntactically valid raw JSON but **all 10 mathematical masks were wrong**. GitHub Actions marked the job FAILED. Specifically, the first right-neighbor instance completed all four conditions, the first left-neighbor instance completed all four conditions, and the first mixed instance completed background and summary only. The remaining planned responses did not execute.

Inference trace: right/background 17:08:56, right/summary 17:09:45, right/artifact 17:11:39, right/source 17:15:44; left/background 17:16:17, left/summary 17:17:07, left/artifact 17:19:01, left/source 17:23:05, mixed/background 17:23:39, mixed/summary 17:24:28, then the deliberate timeout. The source-excerpt inputs required about four minutes each on this tiny CPU reader. Since 14 planned responses were not produced, **do not report 0/24 or complete paired accuracy**. This is an incomplete capacity-floor diagnostic, not an effect-size estimate.

The original runner only wrote the complete results JSON after all examples; the failing run consequently lacked per-output JSON artifacts, though GitHub job logs preserve count, timing, correctness and JSON format status. A checkpoint-on-every-response patch was added subsequently for future runs. The failing run used its own pinned earlier branch commit and was not affected by later fixes.

## Independent mathematical mechanism transfer: Group → Monoid

In a transformation monoid M generated under composition by natural-number functions L(n)=max(n-1,0) and R(n)=n+1, we have L composed with R = identity for every natural n, while R composed with L is not identity (at n=0 it equals 1). Take singleton basis elements a=[L], b=[R] in K[M] over any field K. Then ab=1 while ba!=1. This is **a MONOID algebra example, not a GROUP algebra counterexample**; group invertibility was removed.

The finite-support right-neighbor action T_c x(g)=sum_u c_u x(gu) remains defined on K^M and still satisfies T_c T_d=T_cd. Hence T_b is injective. If y=T_b x, then y(1)=x(R) and y(RL)=x((RL)R)=x(R); thus the configuration delta_1 with values 1 at identity and 0 at RL is not in its image. This supplies a full elementary symbolic proof of an injective/non-surjective operator in the monoid setting. It does **not** verify the source family's unusual finitely presented group or the published high-level Kaplansky claim.

New files: consumer/bicyclic_monoid_transfer.py, consumer/tests/test_bicyclic_monoid_transfer.py, consumer/MONOID_TRANSFER_NOTE.md. This is researcher-derived, not AI-reader-discovered mathematics. It shows what a good reusable mechanism output can look like: changing the carrier class preserves the conditional operator step but changes the existence barrier.

## Final CI and scope

GitHub Actions https://github.com/Andytonglove/math/actions/runs/37965617786 completed successfully, running **21 tests**, including exact finite F2[S3] algebra via an independently coded permutation implementation, the new monoid symbolic/finite-prefix controls, model-response parser tests, freeze hash and public data integrity checks. All 36 chosen task labels agree between two computation paths; exhaustive oracle tests cover 73,728 finite coefficient-pair/input/track cases.

The model run did not invoke any paid model APIs; it used the public GitHub-hosted CPU runner. GitHub account billing was not checked, so no dollar figure is claimed. No Lean/Comparator execution, high-level mathematical peer review or human subjects experiment was performed.

## Scientific decision

Do **not** rerun the identical costly 24-task long-context protocol on another 0.5–1.5B CPU model. The main computation task is too difficult for such models and source-context length dominates runtime. First redesign the downstream test to measure *structured mathematical insight and calibrated assumption/unknown handling*, not full six-bit convolution by hand. Then use a capable, explicitly authorized reader model and a genuinely independently selected hidden structural test set.

A manual frozen artifact plus exact new mathematical consequences demonstrates feasibility of the OUTPUT OBJECT, not successful AUTOMATIC EXTRACTION or machine consumer transfer. The main hypothesis remains unconfirmed. No graph superiority is inferred.
