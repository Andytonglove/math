# Understanding AI-Generated Mathematical Proofs — Research Charter (v0.3)

**Project identity:** Understanding AI-Generated Mathematical Proofs.
**Focus:** Human mathematicians' faithful understanding and auditing of AI-generated mathematical proofs. Machine extraction and AI-to-AI transfer are supporting instruments, not the end goal. This is math-native research, not a generic tutoring UI or graph-visualization product.

## Core scientific question

Can an evidence-grounded explanation of an unfamiliar AI-generated research proof help a human mathematician recover its mechanism, check crucial proof steps, diagnose assumption-dependent failures and correctly recognize unresolved claims—more accurately or efficiently than reading the source or a strong plain-language summary?

Source-to-artifact recovery by a model, machine-side transfer and exact mathematical oracles are **means** to achieve this human outcome. Human proof comprehension must ultimately be evaluated through objective reader tasks and trust calibration. Fluent explanation and self-reported clarity are insufficient. We cannot reconstruct the original discovery model's private thinking from its published paper.

## Human-facing outcome hierarchy (2026-10-10 clarification)

H0 Provenance: can a reader locate the source step and see exactly what is claimed and what is NOT verified?
H1 Mechanism: can they explain why an essential construction or invariant was chosen, rather than simply paraphrase the theorem?
H2 Critical reading: can they correctly identify a missing premise, a reversed argument or an unjustified jump without confusing an invalid proof with a false theorem?
H3 Controlled reuse: can they apply the mechanism under changed assumptions and justify correct UNKNOWN judgments?
H4 Measured human benefit: compared with source, token-matched summary and selected excerpt, do humans gain accuracy, calibrated trust or reading efficiency? **Not measured.**

The technical levels below remain useful to validate the mathematical interface and automatic producer. Machine-reader gains do NOT establish H4.

## Levels of evidence

| Ability | Test | Distinction |
|---|---|---|
| L0 Statement fidelity | quantifiers, assumptions, proof scope | Not proof understanding |
| L1 Proof reconstruction | fill missing arguments with independent checker | May be memorization or local reasoning |
| L2 Mechanism intervention | remove/change an assumption and predict implications | Failure of a proof is NOT falsehood of theorem |
| L3 Novel transfer | solve independently verified related targets | Must show improvement relative to no-proof condition |
| L4 Cross-paper synthesis (future) | derive verified connections between discoveries | Not yet implemented |

## Why Graph is subordinate

- Lean import graph = loaded modules, NOT used lemmas.
- TeX reference graph = source citations, NOT proof entailment.
- Curated argument hypergraph = **hypothesized** mechanisms, using conjunctive requirements, quantifier structure and proof-by-cases motifs.
- Hypergraph edges have pending semantic review; a real source label does not validate the meaning assigned to an edge.

Three different motifs motivate testing: 017 proves by determinant contradiction, needing BOTH low-index collision and high-index approximation-error arguments; 102's quantified complexity reduction needs completeness AND soundness; 197's counterexample needs certificates of ab=1 AND ba!=1. These are interpretations of manuscripts, not independent correctness verdicts.

## Matched model conditions

B0 task and needed background, without source proof.
B1 theorem statement only.
B2 source proof.
B3 source proof plus syntactic graph.
B4 source proof plus typed argument hypergraph.
B5 source proof plus **token-matched natural-language mechanism explanation**.

Hold the model, budget, task prompts and output format fixed. Do not feed the gold oracle to prompts. Split by paper family to avoid leakage among related manuscripts. Use independent mathematics oracles rather than another LLM judge. Track incorrect, correct, abstained and missing separately, and report inference costs.

**Crucial confound:** all current nine toy interventions may be solvable without reading the original mathematical paper. If B0 is already at ceiling, do not claim to have tested proof understanding; redesign the tasks. Correct structured answers alone also do not validate explanations.

## Falsifiable hypotheses

H1. Accurate restatement does not guarantee counterfactual competence.
H2. Source access improves independently verifiable, genuinely source-specific new tasks.
H3. Typed mechanism representation improves L2/L3 beyond B2, and beyond a length-matched prose mechanism explanation B5.
H4. Calibrated models should explicitly recognize when source evidence does not justify a claim.

H3 can be false. If Graph does not help, change or abandon that representation.

## Current concrete work

- Families 017, 102, 197 source audits and provenance checks.
- Nine independent **small mechanism-unit tasks**, prompts and exact gold generated as separate JSON.
- Small math oracle code: rational feasibility and collisions, F2 translation games, finite group algebra, unilateral shifts.
- Three *manually authored* typed argument hypergraphs, not extracted semantic truths.
- CI validates source anchor integrity, toy oracle arithmetic and parser correctness.

Nothing here validates the entire high-difficulty source papers, and no language-model baseline, independent Lean comparator verification or human experiment has been run.

## Revised go/no-go criteria

**Technical readiness:** Produce faithful and bounded reading guides from novel proof units (preferably via a producer not hardcoded to the source family), with independent local mathematical evidence, conditional failure analysis and honest unknowns. Generic fluent summaries or a source-anchor match alone do not pass.

**Primary scientific outcome:** Run an ethically appropriate and independently graded human-reader comparison against source-only, token-matched summary and token-matched excerpt, scoring proof mechanism, audit/transfer tasks, warranted abstention, overconfidence and time. No study, power claim or benefit exists yet. Public 017/197 guides are demonstrations, not blinded evaluation stimuli.

AI-to-AI transfer and Graph remain optional technical diagnostics. Negative human comprehension results or overconfidence harms require method revision rather than hiding behind machine accuracy.

This project may eventually become a series in the style of Physics of Language Models, but not before reproducible scientific phenomena justify that structure.
