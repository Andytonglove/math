# Full repository workspace: execution and collaboration

We maintain the original OpenAI mathematical artifacts and **all source files** unchanged on `main`.
All new research lives on `research/proof-understanding-pilot` under `research/proof_understanding/`.

## Two different compute environments

1. **This ChatGPT run's container** is temporary and currently cannot resolve `github.com`; `git clone` from it is not available. Files here are not a persistent research server.
2. **GitHub Actions full checkout**: `.github/workflows/full-workspace-audit.yml` checks out the complete tracked repository and full commit history on a short-lived GitHub-hosted runner. It tests that the worktree is not sparse, creates `full_math_workspace_inventory.json`, and uploads this report as a short-lived artifact. It does **not** provide a permanent SSH session or preserve local modifications after the job.

An independently managed persistent compute server is still recommended for large-scale Lean builds, storage/cache reuse, and model inference. If one is provided (via SSH setup by its owner), its initial setup can use:

```bash
git clone https://github.com/Andytonglove/math.git
cd math
git remote add upstream https://github.com/openai/math.git
git fetch origin
git checkout research/proof-understanding-pilot
git submodule status
python3 -m unittest discover -s research/proof_understanding/tests -v
node --test research/proof_understanding/tests/*.test.mjs
```

No keys, access tokens, secrets, or server addresses should be checked into the repository.

## Collaboration conventions

- Single shared research branch; work in small auditable commits.
- Every iteration must include a Markdown research report: evidence, code changes, exact commands, test results, failed/omitted checks, costs and next experiment.
- Never overwrite upstream mathematical results or claim that a partial oracle validates a full proof.
- External collaborators should review through GitHub Issues or pull requests, with source-grounded references to exact files/commits.
- **The user's referenced "group" has not yet been identified** (GitHub organization/team, ChatGPT group, research group, etc.). No membership, invitation, or group-level permissions have been changed without that information.

## Large-repository note

GitHub Actions checkout is reproducible, but repeating full history download for every quick edit wastes bandwidth. Run the full-workspace audit when workspace scripts change or manually; routine fast checks continue through `proof-understanding.yml`.
