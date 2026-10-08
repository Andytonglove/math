# Family 017 — The irrationality exponent of π is 2

Status: **source-level case audit**, not a verification of the mathematical discovery.

## Directly inspected evidence

- `lean/docs/017.md`: selected theorem scope.
- `lean/ComparatorChallenges/PiExponent.json`: comparator points to `OAI.PiExponent.main` in `OAI.NumberTheory.PiExponent.Main`; allowed axioms listed in comparator config.
- `lean/ComparatorChallenges/PiExponent.lean`: target is a `by sorry` challenge template, NOT the claimed proof file.
- `lean/OAI/NumberTheory/PiExponent/Statement.lean`: definitions of good rational approximations, irrationality exponent and eventual lower bounds.
- `lean/OAI/NumberTheory/PiExponent/Main.lean`: high-level theorems and selected main statement.
- `lean/OAI/NumberTheory/PiExponent/Approximation/InterpolationConsequence.lean`: a bridge from global interpolation and analytic aggregate to eventual lower bounds.
- `lean/OAI/NumberTheory/PiExponent/Approximation/AdmissibleMatrixGeometry.lean`: one higher-level argument for global interpolation from eventual jet-restriction surjectivity.

## What the selected formal statement says

For every real ν > 2, there exists a threshold Q such that for all integer p and integer q >= Q,

    |π - p/q| >= q^(-ν).

The selected statement also formalizes a supremum characterization of the irrationality exponent of π as 2. The scope note is explicit.

**Do not confuse** this with the unasserted stronger boundary estimate at ν=2; nor infer an effective numerical Q. The paper also discusses Flint–Hills convergence, but `lean/docs/017.md` says it is outside the **selected comparator statement**. Separately, a theorem called `flint_hills_summable` does appear in the Lean Main module.

## Visible local proof spine

```text
OAI.PiExponent.main
  |- pi_integer_eventual_lower_bound
  |    `- pi_eventual_lower_bound
  `- pi_irrationalityExponent_eq_two
       `- pi_eventual_lower_bound
             `- piEventualLowerBound_of_globalInterpolation
                  |- AdmissibleMatrixInterpolation.globalInterpolation
                  |     `- eventually_jetRestriction_surjective (via local construction)
                  `- LiteralAnalytic.analyticAggregate
```

The graph is an **illustrative partial source invocation structure**. Some edges compress intermediate proof steps; it is NOT a complete theorem dependency graph. See `data/case017_proof_spine.json` for cited file paths.

## First useful observation

`Main.lean` looks simple because its hard work is delegated to imported modules. A short top-level proof therefore need not be an easily understood proof. Source line-count and theorem-name centrality are poor *unvalidated proxies* for mathematical insight; their actual predictive power remains an experimental question.

## Scope distinction exposed by the case

1. Paper-level reported consequence: irrationality exponent and Flint–Hills series.
2. Comparator-selected target: `OAI.PiExponent.main` with explicit rational approximation and supremum statement.
3. Additional Lean claim visible in same main module: `flint_hills_summable`.

A benchmark should not collapse these into a single binary `formalized=true` label. This is about *coverage granularity*, not a claim of an error in the release.

## What we have not done

- Not compiled the enormous Lean library, run the Comparator, or independently checked soundness of all dependencies.
- Not extracted the semantic core of the long LaTeX paper or public reasoning-summary PDF in this pass.
- Not run a model to measure understanding, nor claimed the proof contains a particular new conceptual mechanism.
- Not obtained a mathematician's independent assessment of the research result.

## Preliminary research question

Can models distinguish a theorem's true mathematical scope from prominent manuscript claims, reconstruct a meaningful part of its proof mechanism, and use that mechanism on an independent new target, without answering by lexical retrieval alone?

Benchmark candidate prompts live at `evaluation/pilot_tasks.json`; only source-grounded controls can be used at this stage.
