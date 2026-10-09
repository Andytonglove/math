# Related work and semantic-faithfulness research boundary (2026-10-10)

## Primary theoretical criticism

Bastounis, Circelli & Hansen, arXiv:2610.08144v1, submitted October 6, 2026: https://arxiv.org/html/2610.08144v1

Theorem A.3: an explicitly defined existence-presupposition problem is Sigma^0_2-complete, strictly beyond a single ordinary halting oracle. Theorem A.4 constructs related problems arbitrarily high in the finite arithmetical hierarchy. SCI=infinity is thus an unbounded worst-case construction, NOT a claim that every concrete mathematical sentence is harder than halting. Selective/partial faithful translation with explicit assumptions is not ruled out.

Their case studies report natural-language Navier–Stokes m+4 regularity against a compared Lean estimate requiring m+5; another pressure-flux estimate has extra terms and a different proof approach. We independently inspected two related formal declarations at the pinned OpenAI commit but did not referee the entire source or show no alternate bridge exists:
- https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/SmoothFamilyTorusInverse.lean#L1059-L1080
- https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/R3/PressureFlux.lean#L576-L610

## Empirical and method comparators

| Work | Claim supported by source | What it means for our novelty |
|---|---|---|
| Beyond Compilation (2026-10-02 v3), https://arxiv.org/html/2606.31002v3 | On 227 graduate-level theorem statements, tool agent compilation 87.2%, consensus semantic faithfulness 57.7%; calibrated by human audit. | Compile-vs-fidelity gap alone is not novel. Earlier paper versions describe different benchmark sizes: use v3 if reporting exact numbers. |
| FaithformBench, https://arxiv.org/abs/2608.10916 | Eight autoformalization systems often silently correct invalid informal steps. | Invalidity-preserving translation tasks already exist. |
| Evaluating Robustness of Proof Autoformalization, https://arxiv.org/abs/2606.14867 | Local and global NL-proof perturbations; failures of translation fidelity. | Local perturbation test suite alone is insufficient novelty. |
| The Faithfulness Gap, https://arxiv.org/abs/2606.16541 | Bidirectional Provability Fingerprinting and distributional PAC/probe guarantees under the paper's assumptions; self-reported DriftBench. | Do not claim unrestricted equivalence certification or reinvent semantic probes. |
| ProofFlow, https://proceedings.iclr.cc/paper_files/paper/2026/hash/5fce5198dbf92d5ff45f74504431e2ff-Abstract-Conference.html | Structure/lemma dependency graph in proof autoformalization. | A dependency DAG is not a standalone scientific contribution. |
| LeanArchitect, https://arxiv.org/abs/2601.22554 | Lean-to-LaTeX blueprint alignment. | Do not claim first alignment of formal and informal proof graphs. |
| Trellis, https://arxiv.org/abs/2606.09674 | Incremental NL-to-Lean refinement. | Do not conflate our output with incremental Lean checking. |
| Explorable Theorems, https://arxiv.org/abs/2604.02598 | Lean-grounded proof exploration and a small user study. | An interactive proof reader alone is not novel. |

## The defensible research gap is not a universal semantic oracle

Our independent unit of evidence is an evidence-carrying mathematical abstraction, frozen before new transfer tasks, supplied to a separate reader deprived of the source proof. We test whether it preserves theorem scope, actual source argument and reusable mathematics. A Semantic Contract records missing bridges and a calibrated UNKNOWN status before source removal.

We have not yet demonstrated artifact-only transfer on unseen research-level tasks. Six local tests and five example audits from this iteration are limited diagnostics; neither establish a novel mathematical theorem nor verify all OpenAI/Navier–Stokes results.
