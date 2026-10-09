# Iteration 06: mechanism transfer with assumption-breaking control (2026-10-09)

## Branch audit
Read CORE_RESEARCH_CHARTER.md and the complete iteration05 report before modifying research code. Branch head before this iteration: 79b8d182b49e7184708bd22bfec1e9a9b1d41994 (2026-10-08). GitHub Actions run 37780592551 passed at that head; the 0.5B and 1.5B model runs 37779018026 and 37779924784 passed technically but showed NO source/graph advantage on their tiny samples. Previous failures 37778928279, 37779702044/37779769155 and 37779800191 were recovered. CI passing does not prove the underlying manuscript.

## New mathematical result: a checkable abstraction of manuscript 017
The source's parameter choice uses A^2<theta and nu(A-theta)>1-theta. We generalize only this ELEMENTARY subroutine, not the geometric interpolation theorem or a result about pi.

Let f(A)=sum_i w_i A^{r_i}, with positive rational weights summing to one and integer exponents r_i>=2. Put s=sum_i w_i r_i. The rational inequalities 0<theta<A<1, f(A)<theta, nu(A-theta)>1-theta are jointly feasible iff nu>s/(s-1).

Proof: positivity of the coefficients in
f(A)-sA+(s-1)=(1-A)^2 sum_i w_i sum_{k=0}^{r_i-2}(r_i-1-k)A^k
gives 1-f(A)<s(1-A). As theta>f(A), (A-theta)/(1-theta)<(A-f(A))/(1-f(A))<(s-1)/s, so nu>(s/(s-1)). Conversely as rational A tends to one from below, (A-f(A))/(1-f(A)) tends to (s-1)/s. A rational theta in the nonempty strict interval between f(A) and min(A,(nu*A-1)/(nu-1)) gives an exact witness. Thus the derivative at one captures the threshold WITH the convexity/tangent certificate.

The equal-slope pair (A^2+A^4)/2 and (2A^2+A^5)/3 both have s=3 and threshold 3/2 despite different polynomial structures. The 3A^2/4+A^7/4 example has s=13/4, threshold 13/9.

## Crucial negative control: derivative alone is NOT sufficient
For the nonconvex f(A)=A^2-3A^3(1-A)^2, f(1)=1, f'(1)=2 and f''(1)=-4. At nu=39/20<2, take A=3/4 and theta=31/64. Then f(A)=495/1024<theta=496/1024, and nu(A-theta)-(1-theta)=3/1280>0. So the naive rule 'f'(1)=2 implies nu>2 is required' is FALSE unless the global geometric/convexity premise is checked. This produces a concrete positive case with an impossible prediction from an unwarranted transplant.

## Actual local execution
Developed a Python stdlib-only generator of 7 convex polynomial families, each at nu=threshold-1/20, exactly at threshold and threshold+1/20, plus 2 adversarial nonconvex controls: 23 public development questions, 9 true instances. Exact rational constructive witnesses and algebraic certificates accompany the answers. A local independent reference implementation executed 7/7 unit tests; the repository version includes equivalent tests, with actual GitHub Actions status to be checked after commit. This is NO language-model evaluation and NO held-out scientific claim.

An additional local F2[S3] finite-ring audit (separate working-container script) exhaustively checked 4,096 algebra pairs, 49,152 operator-on-basis equations, 384 coefficient recovery equations and 12 two-sided inverse pairs, detecting left/right action order errors. The finite algebra did not provide a one-sided-inverse counterexample; that is expected and does not validate or refute the advanced 197 claim. Include remote code and CI validation in a subsequent commit rather than presenting local-only code as committed.

## Validity and proposed next experiment
The current 23 questions were developed by the SAME researcher who formulated the mathematical abstraction, are public and potentially easy for a strong model without the manuscript; they are not blind new targets. Do not treat 23 as independent statistical samples. The source itself includes theorem statements that are unverified by this project.

Next gate: have a producer create a source-grounded mechanism artifact WITHOUT seeing realized test tasks. Freeze its bytes/hash. An independent consumer then receives the artifact but cannot retrieve the source. Compare statement/background, unabridged relevant proof, budget-matched extract, ordinary summary, mechanism prose and optional content-matched graph on genuinely new mathematical obligations, with independent correctness checking. The adversarial nonconvex example tests whether an artifact retains the global assumptions rather than simply transferring a numeric threshold. Any format errors, mathematical errors, abstentions and costs require separate reporting. Do not purchase inference resources without approval.

## Literature and positioning
ProofFlow (ICLR 2026) already uses dependency graphs and faithfulness for Lean autoformalization (https://proceedings.iclr.cc/paper_files/paper/2026/hash/5fce5198dbf92d5ff45f74504431e2ff-Abstract-Conference.html). LeanArchitect (ITP 2026) already synchronizes Lean blueprints (https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2026.25). Explorable Theorems already grounds mathematical explanation in Lean (https://arxiv.org/abs/2604.02598). These are substantive overlaps, not decorative references. Any future novel claim must be about faithful, boundary-aware abstraction enabling independently verifiable reasoning AFTER the original source is removed, with an actual controlled reader experiment.
