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
