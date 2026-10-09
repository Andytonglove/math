# Frozen 197 Artifact → Source-Deprived Consumer (Development Pilot)

## Research objective

One evidence-carrying Mathematical Understanding Artifact was committed at Git SHA 04fef27eed6f3a10e529f728f3f478cb459f0821 **before** this task generator was added. The exact frozen artifact Git blob SHA is a603b3877de63eaf90f336867fdd6f5b70467209. The generator rejects subsequent artifact edits.

This is a **chronologically frozen but public development experiment**, not an independently designed confidential test. Both producer artifact and current task designer originate in our same research process; only the downstream model's context can be kept source-deprived.

## Mathematical object

Use the group algebra F₂[S₃] with a lexicographic permutation index, coefficients encoded as 6-bit masks, and configuration vectors encoded likewise. The original paper contains a conditional right-neighbor representation. We test three source-inspired operator tracks: right-right composition, left-left composition, and mixed right-left composition. Left-neighbor action reverses the product, and left and right group actions commute. These elementary claims are mathematically checkable independent of the **unverified advanced Kaplansky counterexample**.

The generator selects 12 noncommuting coefficient-mask pairs and one basis indicator per pair, then creates 3 related tracks (36 distinct labeled tasks, 144 prompts across 4 conditions). All tasks have exact finite F₂[S₃] gold answers verified twice: direct operator actions and separately derived algebraic product order. The source-free baseline receives complete mathematical definitions, so no information is missing from its task statement.

## Conditions and controls

| Condition | Input visible to independent model |
|---|---|
| background | Complete finite-group and operator definitions, question |
| summary | Accurate compact summary of right- and left-action properties, plus question |
| artifact | Frozen source-independent mechanism explanation, evidence obligations and unknowns, plus question |
| source_excerpt | Actual source excerpt from manuscript section 06, plus question |

Contexts differ in length; this initial test **does not** establish token-matched communication efficiency. Unlike the original proof, the artifact includes a separately derived left-action anti-homomorphism, so source/excerpt and artifact may contain different mathematical information. The accurate summary contains the same principal composition laws to mitigate this confound. Graph is not part of the primary comparison.

## Distinguishing source fidelity from mathematical utility

Even if the artifact improves finite-operator computations, this does NOT prove a general AI system understands the entire research-level 197 counterexample. A manual producer does not demonstrate automatic extraction. The original manuscript's claimed exotic group or Lean equivalence has not been independently checked. Output format and model compute are separate axes of measurement.

Crucially, the frozen artifact commits to UNKNOWN regarding full Lean semantic equivalence and exotic witness existence, and says not to silently repair errors. It is legitimate to evaluate bounded conditional mathematics while refusing to certify the larger source theorem.

## Reproduce

From repository root:

    python3 research/proof_understanding/design_v1/consumer/generate_197.py --repo-root . --bases 12 --output-dir /tmp/197-consumer
    python3 -m unittest discover -s research/proof_understanding/design_v1/consumer/tests -p test_*.py -v

Only the GitHub model runner, if separately invoked, should receive the prompts.jsonl; the gold.json is used by the offline scorer. Public task generation after artifact freeze is not equivalent to blind preregistration.
