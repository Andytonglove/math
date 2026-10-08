# Family 017 — a proof-specific mathematical mechanism intervention

## Question

The submitted determinant argument uses a **quadratic collision penalty** on repeated Taylor-degree indices. Suppose we replace that analytic estimate with a hypothetical weaker penalty **linear** in the total number of rows, leaving the proof's normalization by M H unchanged.

Can the low-index case still yield a uniform nonzero saving as the polynomial degree H tends to infinity?

**Answer: no, not from that weaker estimate alone.**

## Independent scaling argument

Let M denote the determinant row count, H the polynomial degree, and n_a the number of times Taylor group label a occurs. As a counting identity, sum_a n_a = M.

A hypothetical estimate involving only a factor exp(-c sum_a n_a) provides after logarithm and normalization by M H:

    c (sum_a n_a)/(M H) = c/H -> 0.

It therefore supplies no *fixed strictly positive* normalized gap. This only diagnoses the insufficiency of that proposed replacement in the submitted proof architecture. It does not claim that the main theorem itself is false or that alternative proof methods cannot exist.

By contrast, the paper's stated collision estimate scales like exp(-c sum_a n_a^2). If a fixed fraction eta of rows lie in at most D low-index groups, elementary Cauchy-Schwarz forces sum_a n_a^2 >= (eta M)^2/D.

For an idealized example with H even, choose M=H^(m+1), D=H^m, eta=1/2. Balanced group sizes are H/2; then

    sum_a n_a^2 = D (H/2)^2 = H^(m+2)/4.

The normalized quadratic collision is exactly

    (sum_a n_a^2)/(M H) = 1/4,

independent of H. The hypothetical linear replacement tends to 0.

This is a checkable **reason for the quadratic shape of a mechanism**, rather than a lookup of a lemma name. The full manuscript has additional constants and asymptotic errors not reconstructed by this toy model.

## Executable oracle and provenance

- Submitted proof source: preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections/determinant.tex, especially the collision estimate and determinant comparison.
- Exact oracle: research/proof_understanding/scripts/parameter_oracle.py, function collision_scaling_example.
- Unit tests: research/proof_understanding/tests/test_parameter_oracle.py.
- Task generator: research/proof_understanding/scripts/build_understanding_pilot.py, probe 017-COLLISION-SCALING.

This task remains **a source-inspired mathematical-unit probe**. A strong model could derive it without reading the paper if given enough of the formulas, so it cannot itself certify proof understanding. The relevant future test is whether exposure to the paper improves the model's ability to reason about *new, less explicit* counterfactual proof mechanisms.
