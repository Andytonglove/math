# Understanding AI-Generated Mathematical Proofs — Research Charter (v0.2)

**Project identity:** Understanding AI-Generated Mathematical Proofs.
**Focus:** Mathematical understanding in AI systems, NOT a graph visualization product and NOT primarily an HCI teaching system.

## Core scientific question

Can a model recover the mathematical mechanisms in another AI system's unfamiliar research proof, manipulate them under changed conditions, and transfer them to independently checkable new mathematical problems?

Understanding is defined operationally by falsifiable performance, not by fluent paraphrase. We cannot reconstruct the original discovery model's private thinking from its published paper.

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

## First go/no-go criterion

Find at least one nontrivial, truly source-conditioned **held-out intervention** per selected family, with independent mathematical oracle, such that providing the proof significantly changes the model's ability to solve it relative to B0 and B1. Test B2 before building more graphs. If the effect is absent, revise the scientific question or dataset rather than growing the architecture.

This project may eventually become a series in the style of Physics of Language Models, but not before reproducible scientific phenomena justify that structure.
