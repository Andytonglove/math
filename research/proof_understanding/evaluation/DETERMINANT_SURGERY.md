# Family 017: exact proof-surgery pilot

Aim: test whether models preserve a two-case *proof mechanism* under perturbations. This is not a proof of the irrationality exponent of pi and not a model performance result.

The manuscript's limiting normalized bounds are:
- arithmetic lower L = -(1-b) - Ea;
- collision upper Uc = En - C;
- approximation upper Ua = En - nu*(A*(1-eta)-b).

The contradiction closes iff Uc < L AND Ua < L. These are abstract limiting bounds: randomized rational parameter instances do NOT assert the actual interpolation theorem or all the global parameter requirements.

For each generated base case, produce six variants: unmodified, collision weakened, approximation weakened, both weakened, collision tied to lower, and approximation tied to lower. Oracle uses exact Fraction comparisons, separately checked against algebraically rearranged inequalities.

Seven conditions (minimal, theorem, proof, syntax, hypergraph, prose, distractor) receive the SAME complete task formulas and rational numbers. Thus B0 can solve each task from mathematics alone. The proof and graph conditions supply context, not hidden numerical information.

Outputs: prompts.jsonl has opaque IDs, conditions, and questions WITHOUT answers; gold.json stores exact answers separately; metadata.json and sanity.json record provenance and deterministic non-LLM checks. GitHub Actions creates a reproducible public development set (not a private test set).

Important limits:
- Passing these tasks alone does not establish understanding of the original 017 research proof.
- The AND oracle vs a deliberately wrong OR shortcut is a designed sanity check, NOT evidence of model performance.
- The proof and prose passages are paraphrases, not full source papers; token budgets are NOT fully matched across conditions yet.
- Real evaluation should use new unreleased random seeds, adequate difficulty, matched budgets, and blind source/no-source comparisons.
- If B0 is at ceiling, this question lacks discrimination; revise instead of reporting a spurious proof-understanding gain.

Run from root:
    python3 research/proof_understanding/scripts/determinant_surgery.py --source-root . --seed 26008 --bases 12 --out-dir /tmp/proof-surgery
    python3 -m unittest discover -s research/proof_understanding/tests -p test_determinant_surgery.py -v
