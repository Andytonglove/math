# Iteration 12 — Human proof-audit: theorem truth is not proof validity

Date: 2026-10-11 (Asia/Shanghai). Branch: research/proof-understanding-pilot.

## Decision and beneficiary

The primary aim is to help **human mathematicians** understand, challenge, and responsibly reuse unfamiliar AI-generated research proofs. AI-to-AI quizzes are secondary diagnostics. After examining CORE_RESEARCH_CHARTER, MANUSCRIPT, PROTOCOL, MASTER_PLAN, SPRINT_STATE and iteration09/10/11 evidence, this iteration targets a concrete failure mode: **an invalid displayed proof does not imply its conclusion is false**. Equally, a correct conditional argument does not establish that a hard source-specific premise exists.

Starting branch was a3cad1a84564c33575f4ac24770e8669cb2118f9. Both earlier GitHub checks, runs 38020891550 and 38020891572, had passed. Existing human guides for 017/197 are hand-authored demonstrations, NOT automatically produced explanations or measured human benefits. The restricted source197 recognizer and the prior frozen 197 artifact remain unchanged.

## Implemented instrument

New reproducible public-development code in human_reader/audit_lab/:
- audit_cases.py with math, stimuli and answer-key submodules: nine source-inspired **researcher-authored** audit cases, a deterministic generator and label-only scoring.
- data/checks_public_dev.json: exact arithmetic and finite structural diagnostics. The generator also produces separate cards_public_dev.json and gold_public_dev.json for transparent replay; neither is a hidden evaluation set.
- tests/test_audit_exact.py and test_audit_rubric.py: 12 local unit tests, plus the earlier 11 human guide tests retained for CI.
- New documentation records evidence strength and prohibitions on silent proof repair.

A response receives TWO separate judgments:
1. Claim status: LOCALLY_ESTABLISHED, EXACTLY_REFUTED, or NOT_INDEPENDENTLY_AUDITED.
2. Proposed argument: VALID_LOCAL, INVALID_STEP, or NOT_AUDITED.

The evaluator detects unsupported promotion of UNKNOWN and the error of declaring a genuinely true conclusion false solely because the presented proof is wrong. Written mathematical reasoning CANNOT yet be graded automatically and requires blinded expert review. These categories measure evidence status IN THIS PROJECT, not theorem provability in general.

## Nine manually designed development checks

| Family | Target | Claim / argument | Actual basis |
|---|---|---|---|
| 017 | strict nu=2 exclusion for A² | established / valid | global ratio < A/(1+A)<1/2 |
| 017 | true nu>2 necessity with a reversed step | established / **invalid** | A=3/4, theta=5/8 yields 1/8<3/16 |
| 017 | derivative f'(1)=2 alone forces nu>2 | **refuted** / invalid | nonconvex rational witness, slack 3/1280 |
| 017 | source's entire pi-level theorem is correct | NOT AUDITED / not audited | local barrier lemma cannot certify parent proof |
| 197 | right and left operators commute | established / valid | v(gu)=(vg)u, associativity |
| 197 | same true theorem proved by swapping ugv=vgu | established / **invalid** | noncommuting S3 transpositions uv!=vu |
| 197 | ab=1 alone forces T_b nonsurjective | **refuted** / invalid | a=b=1 makes T_b=I, onto |
| 197 | one-sided inverse in a MONOID algebra | established / valid | L(R(n))=n, R(L(0))=1 |
| 197 | particular source GROUP algebra pair exists | NOT AUDITED / not audited | monoid witness cannot instantiate GROUP premise |

The 017/197 wrong-proof cases are **synthetic interventions**, NOT discovered actual manuscript errors. The existing high-difficulty original mathematics and Lean semantic correspondence remain unverified.

## Exact local evidence, executed

Command: python3 -m unittest discover -s human_reader/tests -p 'test_audit_*.py' -v
(paths relative to design_v1). Result: **12/12 new tests passed locally**.

- Exact Fraction computes h(A)=A²-3A³(1-A)² with h(3/4)=495/1024 < theta=496/1024; nu=39/20 gives strict second-inequality margin **3/1280**.
- True claim / wrong inference: at A=3/4, theta=5/8, A-theta=1/8 < A-A²=3/16, disproving the incorrect inequality while leaving the original necessity theorem intact.
- Positive rational feasibility sanity: A=7/8, theta=25/32, nu=5/2.
- S3 multiplication encoded as p[q[i]]. Exactly **216** triplets checked for associativity; u=(1,0,2) and v=(0,2,1) give uv=(1,2,0) but vu=(2,0,1), disproving factor swapping. This finite computation does not prove mixed-operator commutation universally; the independent displayed associativity derivation does.
- MONOID shifts: 64 finite-prefix samples checked. The universal identity L(R(n))=n follows directly from L(n)=max(n-1,0), R(n)=n+1, NOT from 64 trials; RL(0)=1 is a counterexample to two-sided inversion.

An important semantic fix was made before archiving: asking whether "our project already certified the theorem" has a definite answer NO. The UNKNOWN cards instead ask about the **underlying high-level mathematical truth** which this project has not audited. UNKNOWN is neither falsehood nor mathematical undecidability.

## Threats, cost and scientific interpretation

The stimuli and gold were selected by the same researcher; both proof families had already been studied. These cases cannot show cross-paper transfer, model-generated understanding, hidden-task generalization, or improved human comprehension. Finite computations check witnesses, not all universal source claims. Tests and GitHub CI verify code/provenance only. No human subjects, expert blind grades, model inference, paid APIs or GPU were involved. GitHub runner account billing was not inspected, so no verified monetary-cost figure is claimed.

The earlier Qwen2.5-1.5B CPU attempt remains incomplete: **10/24 planned answers actually executed**, zero mathematically correct among those ten, all ten schema-valid; 14 unexecuted. It is not a balanced experimental effect estimate.

## Next scientific gate

Independent mathematical expert audit of exact source units and public gold, followed by a non-template proof-to-explanation producer on unseen paper families. Freeze explanations BEFORE independent evaluation items are selected. For a human study, match strong summary and excerpt controls to the evidence guide in mathematical information and appropriate reading cost, then measure proof-mechanism reconstruction, invalid-step localization, appropriate UNKNOWN, unsupported confidence and elapsed reading time. Recruit/consent and pre-register after ethical and feasibility review. Graph is optional and should never receive extra information compared with prose.

Do not alter main, original OpenAI mathematics source or the previously frozen 197 artifact; do not purchase model inference without authorization.
