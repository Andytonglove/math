# Iteration 03 — Full-worktree infrastructure and collaboration preparation

**Project:** Understanding AI-Generated Mathematical Proofs  
**Branch:** `research/proof-understanding-pilot`  
**Date:** 2026-10-08

## Motivation

The user requested that the entire fork be cloned to the assistant's server and associated with a shared group, with ongoing reproducible research.
A direct clone into the current assistant container was attempted but DNS access to `github.com` failed. The container is temporary; it cannot honestly be presented as a permanent SSH research machine. The actual fork remains reachable through the GitHub connector.

## Implemented

- A new **full GitHub Actions checkout workflow** (fetch-depth 0, no sparse paths) to validate real remote workspace availability.
- A standard-library Python inventory tool recording commit, tree SHA, tracked file counts, directory size distribution, extension counts, and missing worktree entries.
- Three offline synthetic repository tests, including explicit rejection of sparse or incomplete checkouts.
- Clear collaboration and server onboarding instructions. Do not associate with a guessed group identity.
- Artifacts are uploaded from the runner for inspection; this task does not persist a clone on an always-on server.

## Verification tier

- Locally executed three fixture tests (all pass in the current container) before commit.
- Full repository checkout, runtime and inventory counts will be recorded only after the GitHub Actions job finishes; no premature success claim.
- No model inference or full Lean theorem verification in this infrastructure iteration.

## Next research gate

Once full checkout passes: examine selected source families and create new independently verified held-out mathematical interventions and baselines. Continue keeping original mathematical source files and main unchanged.

## Verified execution update — full source checkout

GitHub Actions run [37773543681](https://github.com/Andytonglove/math/actions/runs/37773543681) completed **SUCCESS** at commit fb4f55b36560676c1d0c6825d1f8500dda0e2781. It checked out the complete Git history and full worktree (no sparse checkout) and uploaded an inventory artifact.

The actual artifact, independently opened after the job, records:

| Metric | Value |
|---|---:|
| Tracked worktree entries | **133,982** |
| Missing tracked paths | **0** |
| Worktree bytes (tracked) | **2,214,553,648** |
| Lean files (.lean) | **122,876** |
| LaTeX files (.tex) | **8,009** |
| PDF files (.pdf) | **787** |
| Entries under lean/ | **123,565** |
| Entries under preprints/ | **10,373** |
| lean/ tracked bytes | **1,584,025,482** |
| preprints/ tracked bytes | **627,365,628** |
| Git checkout | **not sparse, not shallow** |

This is the first verified full-source-scale audit. It indicates that scanning all Lean source modules is a large task. Subsequent structural work should first traverse **case-specific import closures**, with explicit awareness that imported Mathlib packages lie outside the repository's `lean/` source tree.

The full inventory JSON is available as a workflow artifact (14-day retention), not as a permanently committed raw file. These counts correspond to the pinned commit above, not to future upstream updates.

## Next experiment: Lean import closure vs conceptual mechanism

Added an independent syntax-level import closure analyzer for `OAI.NumberTheory.PiExponent.Main`. It reports only modules physically imported under `lean/` and external dependency names; it does **not** infer mathematical proof dependencies or concept graphs. A full-worktree CI task will measure the actual closure, followed by comparisons with source references and curated mechanism edges.

## Verified second cloud execution — import graph baseline

GitHub Actions [run 37773918416](https://github.com/Andytonglove/math/actions/runs/37773918416) completed **SUCCESS** at commit `97bc38942d3c1603fa170763b503b1ad495ddba1`. Downloaded the zipped workflow artifact and independently inspected its two JSON files.

**Actual case 017 syntactic import-closure measurements:**

| Quantity | Measured value |
|---|---:|
| Seed | `OAI.NumberTheory.PiExponent.Main` |
| Seed's direct imports | **2** |
| Transitive in-repository Lean modules | **869** |
| In-repository syntactic import edges | **1,707** |
| Distinct unresolved-to-local-tree / external import identifiers | **215** |
| Modules with root namespace `OAI` | **869** |

The two seed imports are `AdmissibleMatrixGeometry` and `InterpolationConsequence`, not a complete picture of the mathematics. The import closure excludes external Mathlib package implementation and makes **no claim about true theorem-level dependencies**. The previously constructed LaTeX reference graph (70 labels / 92 references / 27 cross-file references) and the curated mechanism graph (10 manually interpreted nodes) represent very different views of the same claimed proof.

This supports studying **information loss and abstraction across representations**, but does not yet show that any one graph improves comprehension or transfer. No model performance comparison was conducted. Artifact retention is 14 days; key aggregate numbers are preserved in this report.
