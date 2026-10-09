# Understanding AI-Generated Mathematical Proofs through Evidence-Carrying Abstractions

**Working manuscript v0.2, updated 10 October 2026.** Research-design paper, not a positive model-results paper. Original AI-generated high-level mathematical claims are NOT independently certified by this project.

## Abstract
As AI systems increasingly generate research-level mathematical arguments, proof availability does not by itself guarantee that a theorem's operative ideas can be checked, transferred, or incorporated into subsequent mathematical reasoning. We study the problem of recovering an *evidence-carrying mathematical abstraction* from a completed proof. Such an artifact identifies a theorem's claim contract, mathematical mechanism, explicit proof obligations, validity boundaries, reusable lemmas, supporting evidence and unresolved issues. We argue that fluent summarization and theorem-answer accuracy alone cannot establish mathematical understanding. Our proposed evaluation freezes the artifact before downstream tasks are instantiated and asks an independent consumer, deprived of the original proof, to solve mathematically verified interventions and transfer problems. Graph structure is a falsifiable encoding hypothesis, not a required output. We demonstrate this framing through two carefully scoped source-inspired examples: a sharp rational feasibility barrier with an explicit nonconvex counterexample to a common overgeneralization, and a conditional noncommutative action with composition-direction obligations. Exact local checks yield 23 public development questions and finite-algebra diagnostics; no model-based artifact-only improvement has yet been measured. We outline what would constitute evidence for knowledge transfer rather than proof paraphrase.

## 1. Introduction
Machine theorem proving, verification, and mathematical discovery are related but distinct from mathematically understanding a completed argument. A full formal certificate may establish a precise proposition without communicating the construction's role. Conversely, a compact explanation can be persuasive yet omit assumptions essential to correctness. The research problem is not to infer inaccessible private discovery traces of the source model. It is to recover a mathematical knowledge object from the available research product.

This project is motivated by the large OpenAI mathematical manuscript repository, but its public texts are research-source documents, not automatic ground truth. We define the relevant unit as a bounded argument with explicit imported lemmas; we do not assume every published main theorem in the corpus is correct.

The primary question is: **Given an unfamiliar machine-generated proof, can a producer construct a faithful, verifiable abstraction that enables an independent mathematical reader to solve new, checkable problems after the source proof is removed?**

## 2. Objects of study
Let X=(T,P,K,F,V) denote an exact theorem statement T, proof or proof component P, shared mathematical background K, optional formal objects F, and version/provenance V. An artifact A=G(X) consists of:
- C: typed claim contract (objects, hypotheses, conventions, quantifiers, conclusion).
- M: explanatory mechanism (construction, invariant, inequalities, proof-by-cases structure).
- O: proof obligations, including bridges hidden by compression.
- D: validity boundaries and counterfactual failure analysis.
- R: reusable, independently stated consequences or methods.
- E: evidence anchors, derivations, checked certificates and explicit dependencies.
- U: unresolved claims and calibrated unknowns.

Every claim receives a status: verbatim source, exact re-derivation, checked consequence, proposed but unverified mechanism, or unknown. An artifact can be long; the compression budget is explicit and never allowed to silently erase needed assumptions.

We call an artifact **faithful** only when it retains the necessary mathematical conditions; **useful** only when it improves independent reasoning or reduces justified communication cost; and **reusable** only when a new application admits independent mathematical verification. A dependency graph can represent aspects of M and O, but graph centrality and source citation counts do not establish these criteria.

## 3. Evaluation protocol
A producer reads X and a declared communication budget, but not the realized evaluation queries or gold solutions. The artifact is frozen and hashed before evaluation-set instantiation. The reader is freshly initialized with shared background and query, but NO ability to retrieve P in the main replacement track. All conditions use the same task specification and checking infrastructure. A separate augmentation track may provide source plus artifact, but does not test replacement.

Strong comparisons include: shared background; theorem statement alone; source argument; token-matched source extract; ordinary natural-language summary; evidence-carrying prose artifact; and, only where useful, graph encoding of exactly the same claims. Track producer cost separately from consumer reading cost. Compare both effectiveness and amortized cost across reuse count m: build cost plus m times read cost.

Metrics include theorem/assumption fidelity, checked local derivations, positive-claim validity, sound abstentions, correct case coverage, independent transfer solutions, token budget, runtime and format compliance. An empty artifact cannot achieve a high fidelity score by making no false statements: score coverage and precision together. Distinguish a broken proof after modifying an assumption from a false theorem. Evaluate statements at the same mathematical content and context window when comparing graph against prose.

Split evaluation by source family and by structural mechanism. Altering numeric constants of one template is not an independent held-out mathematical problem. Public development tasks and the researcher-designed examples below are not the hidden test set. For statistical analysis, paired runs and proof-level clusters are the unit of inference; preregister an effect size and allocation after power assessment.

## 4. Worked mathematical mechanism: the 017 parameter barrier
A section of the source manuscript uses A^2<theta and nu(A-theta)>1-theta to establish the feasibility of auxiliary parameters under nu>2. We isolate only this elementary mathematical module.

Consider f(x)=sum_i w_i x^{r_i}, where positive rational w_i sum to one and each integer r_i>=2. Let s=sum_i w_i r_i=f'(1)>1. Determine whether rational 0<theta<A<1 exist such that
f(A)<theta, and nu(A-theta)>1-theta.

**Proposition (sharp mixture threshold).** The system is feasible exactly when nu>s/(s-1).

For 0<A<1, the polynomial identity
f(A)-sA+(s-1)=(1-A)^2 sum_i w_i sum_{k=0}^{r_i-2}(r_i-1-k)A^k > 0
implies 1-f(A)<s(1-A). Since theta>f(A), the ratio (A-theta)/(1-theta) is strictly less than (A-f(A))/(1-f(A)), itself strictly below (s-1)/s. The second feasibility inequality then demands nu>s/(s-1). Conversely, as A tends rationally to 1 from below, (A-f(A))/(1-f(A)) tends to (s-1)/s. If nu exceeds the threshold, one may choose rational A sufficiently close to one and rational theta between f(A) and min(A,(nu*A-1)/(nu-1)). The strict interval is nonempty and directly verifies the constraints.

This is an independently provable local extension of the **parameter selection mechanism**, not an extension of the parent source's interpolation theorem and certainly not an independent proof concerning pi. Different polynomials can encode the same endpoint slope: (A^2+A^4)/2 and (2A^2+A^5)/3 both have s=3 and critical nu=3/2. The polynomial (3A^2+A^7)/4 has s=13/4 and critical nu=13/9.

**Boundary-aware negative control.** Replacing global convexity by the endpoint derivative is unsound. Set f(A)=A^2-3A^3(1-A)^2, for which f(1)=1, f'(1)=2, but f''(1)=-4. Choose nu=39/20, A=3/4, theta=31/64. Then f(A)=495/1024<496/1024=theta and nu(A-theta)-(1-theta)=3/1280>0. Hence a feasible rational point exists BELOW the convex formula's threshold 2. This does not show all nonconvex barriers violate the formula; it shows an extracted mechanism must record the global curvature premise.

The identity acts as a positive-polynomial proof certificate, the explicit rational tuple as a counterexample to overgeneralization, and the conditional claim as a reusable abstraction. These are considerably stronger artifacts than the bare instruction 'replace 2 by r/(r-1)'.

### Global variational view (valid even without convexity)

For a rational-valued function f on rational A in (0,1), define b(A)=max(0,f(A)) and D={A rational: 0<A<1, b(A)<A}. At a fixed A in D, there is a rational theta with 0<theta<A, f(A)<theta and nu(A-theta)>1-theta **if and only if**
nu > R_f(A):=(1-b(A))/(A-b(A)).
Indeed nu<=1 is impossible. For nu>1, the second condition becomes theta < (nu*A-1)/(nu-1). A rational theta strictly between b(A) and this upper bound exists exactly when nu(A-b(A))>1-b(A). Thus for D nonempty, global feasibility is equivalent to nu>Gamma_f, where Gamma_f=inf_{A in D} R_f(A) (Gamma_f=+infinity if D is empty). The strict boundary is always excluded even if the infimum is attained.

For the nonconvex control at A=3/4, f(A)=495/1024, this fixed-A threshold is (529/1024)/(273/1024)=529/273<39/20<2. The endpoint derivative rule fails because it confuses an endpoint limit with a **global supremum of feasible secant gaps**. Convexity is a sufficient geometric reason that the endpoint controls the full interval. This identifies a general, proof-carrying transfer mechanism: use the variational expression for arbitrary barriers; specialize to the endpoint derivative only after certifying a global tangent inequality.

## 5. Second source-inspired mechanism: the 197 action contract
For a field K, group G and finitely supported c=sum_u c_u*u in K[G], let (T_c x)(g)=sum_u c_u x(gu) on all configurations x:G->K. Finite support makes the operator well-defined. A direct regrouping gives T_c composed with T_d equals T_cd, and the delta configurations recover the coefficients, so c->T_c is faithful. Conditional on ab=1, T_a T_b=I makes T_b injective. Its image is exactly the fixed-point set of T_ba; if ba is not 1 then faithfulness exposes a delta configuration not in the image.

The order is sensitive to convention: with left neighbors x(ug), the representation is an anti-homomorphism. This mechanism transfer is conditional on the algebraic assumptions; it does not independently produce or certify any particular source counterexample. A finite F2[S3] sanity check exercises algebra order but cannot produce a one-sided inverse failing to be two-sided in this finite-dimensional algebra.

## 6. Current evidence: positive mathematical checks, negative model diagnostic
Archive iteration05 generated 72 rational two-case interventions and 48 quantifier examples, and a 33-task power-threshold family. These are source-inspired development exercises, not full-theorem verification. In two CPU smoke runs on Qwen2.5-0.5B/1.5B, each condition contained only four examples per family; the 017 model outputs were constant-label, and no proof/graph context benefit appeared. Output-format parsing and unmatched token budgets further limit interpretation. This is evidence for *experiment design revision*, not evidence about capable models' ability to understand research proofs.

In the current iteration, an exact rational generator created 23 public development tasks across seven convex polynomial families and two nonconvex controls; nine had feasible answers with constructive witnesses. A local equivalent implementation passed seven unit tests. The numerical checks support reproducibility, not the mathematical theorem's universal quantification; that follows from the derivation above. A separate local finite F2[S3] enumeration checked 49,152 operator basis equalities and 384 coefficient-recovery equalities without proving the high-level 197 result.

**There is no observed benefit for automated artifact construction or independent artifact-only mathematical transfer as of this manuscript version.** The sample artifact is hand-derived and the developer knows the exercises; any general effect size is unmeasured.

## 7. Relation to prior work
ProofFlow (ICLR 2026) already uses a proof dependency DAG and lemma-level faithful autoformalization. LeanArchitect (ITP 2026) synchronizes informal blueprints with formal declarations. Explorable Theorems (2026) links written proofs and Lean executions to support comprehension. Controlled reasoning studies in Physics of Language Models (ICLR 2025) emphasize perturbable synthetic families and latent dependencies. Counterexample generation and hypothesis mutation are active neighboring research directions. Therefore our novelty cannot be 'using graphs', 'making proof explanations', 'dropping assumptions' or 'connecting mathematics to Lean' in isolation. The proposed combination must be validated by replacing source proofs with independently reusable, evidence-carrying abstractions and by measuring the retained mathematical utility under hostile assumption changes.

Primary sources: ProofFlow https://proceedings.iclr.cc/paper_files/paper/2026/hash/5fce5198dbf92d5ff45f74504431e2ff-Abstract-Conference.html ; LeanArchitect https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2026.25 ; Explorable Theorems https://arxiv.org/abs/2604.02598 ; Physics of Language Models https://physics.allen-zhu.com/part-2-grade-school-math/part-2-1 .

## 8. Threats, falsifiers and next decisions
A larger reader may solve the task directly without source help; strong background and statement-only controls are essential. A shorter document may reduce cost without preserving any uniquely source-conditioned mathematical idea. Artifacts created after exposure to evaluation queries create an unacceptable leak. Multiple perturbations of one polynomial inflate sample size. Evidence labels assigned by another language model are not mathematical certificates. Long mathematical texts with unverified imported lemmas require explicit assumptions, not false certainty.

The next pre-registered milestone is one fully frozen automatically produced source-grounded artifact, independent hidden structural tasks, strong token-matched summary/extract controls and an independently checked downstream reading study using authorized compute. If source proof access, artifact construction and graph structure do not change performance beyond controls, the core hypothesis needs revision. If the artifact preserves correct assumptions and reduces reading cost at equal mathematical utility, that is a meaningful result even without a graph advantage or human experiment.

## 9. Conclusion
The fundamental research object is not a graph, and a generated explanation is not evidence of comprehension. It is an operationally inspectable transfer of mathematical mechanisms, obligations and validity boundaries. We currently have a mathematically nontrivial demonstration of why this distinction matters, but not a demonstrated machine-learning method. The manuscript should remain explicitly preliminary until controlled source-removed tests establish an effect.


## 10. The semantic-fidelity boundary and its consequences (October 2026)

A critical limit on mathematical understanding from machine-generated proofs has been sharpened by Bastounis, Circelli and Hansen (2026), [Navier–Stokes Lost in Translation](https://arxiv.org/html/2610.08144v1). Their central distinction is between checking a given Lean statement/proof and establishing that it represents the natural-language mathematical claim and argument from which it allegedly originated. A correct formal proof of a different claim does not certify the source claim; a correct proof of the same claim using different reasoning does not certify the source argument.

The theoretical claim needs careful quantifiers. Their Theorem A.3 constructs a source-defined existence-presupposition problem, D = { e : exists n for all natural x_1,...,x_k, p_e(n,x_1,...,x_k) != 0 }, that is Sigma^0_2-complete when k >= 9. Consequently, a uniform decision procedure cannot resolve this class using only an ordinary halting oracle. Theorem A.4 constructs related tasks at every fixed finite level of the arithmetical hierarchy. The SCI=infinity headline means that **arbitrarily high finite levels arise across this unrestricted family**. It does not establish that every individual mathematical statement is harder than halting, nor rule out a sound partial method restricted to an explicit mathematical language. Our proposed system is not a universal semantic decision procedure.

The paper reports a specific translation discrepancy in OpenAI's published Navier–Stokes work. A natural-language inverse estimate refers to m+4 additional input derivatives; the compared Lean declaration uses input jets at w.length+5. We independently examined the Lean signature in openai/NavierStokesAndEuler at commit f9e8bc5b38b6e212696e8a30e3e91517af887bbd. A separate pressure-flux bound in Lean carries an additional dissipation/gradient-dependent term and its proof uses different analytic tools. These observations establish a *candidate correspondence gap* in those local statements, not the falsity of the Navier–Stokes theorem. We have not checked every possible bridging lemma or the complete PDE arguments.

A central example is a correct proposition with an incorrect informal proof. The polynomial p(x)=x^3-x^2-x+1 really factors as (x-1)^2(x+1), so it is nonnegative when x >= -1. An alleged source argument instead uses (x-1)(x+1)^2, which differs already at x=0. Replacing the false factorization by the correct one produces a valid proof of a true theorem, but **silently repairs rather than faithfully represents** the given source proof. Another example encodes an ostensibly defined least natural number whose defining predicate has no instances: totalizing an undefined minimum by Nat.sInf of the empty set silently changes the meaning. The additional condition matters even when the final algebraic identity is trivial.

### 10.1 Four semantic interfaces rather than one proof checker

An evidence-carrying artifact must now distinguish four objects:
- Original claimed mathematical proposition: precise definitions, domains, assumptions, quantifiers and conventions.
- Formal encoded proposition: what is actually provable in the formal system, including extra hypotheses and admitted axioms.
- Original proof mechanism: the author's stated mathematical construction, estimates, invariants, case splits and proof obligations.
- Exported understanding abstraction: the reusable mathematics we propose to communicate, together with unresolved obligations and provenance.

These four interfaces can align or differ in independent ways. Statement-level agreement does not imply that two proofs use the same argument. An extra regularity assumption may weaken one part of a formal statement, while a stronger all-times quantifier strengthens another; the complete propositions can be incomparable. A source-derived graph cannot certify such alignment by itself. An intuitive explanation cannot either.

We therefore attach a **Semantic Contract** to the existing artifact fields C, M, O, D, R, E and U. Each major claim has a provenance anchor, scope, typed evidence status and a bridge obligation where correspondence remains unproved. Possible relations include statement_aligned, stronger_premise, weaker_conclusion, extra_symbolic_dependency, changed_quantifier, different_argument, undefined_presupposition and unresolved. Labels may coexist. A formal proof accepted by a trusted kernel provides evidence about that encoded theorem only. It does not silently promote unverified correspondence to established faithfulness.

The output policy is *no silent repair*. When a mathematical source is wrong, a faithful artifact identifies the offending step and, if possible, creates a separately labeled proposed correction. When an assumption is not known to hold, the system may give a conditional statement or UNKNOWN. That is informative, but blank abstention everywhere has no mathematical utility: coverage and supported mathematical content must be measured jointly.

### 10.2 Why this modifies, rather than replaces, our research problem

Recent works have already studied much of basic semantic fidelity. [Beyond Compilation](https://arxiv.org/html/2606.31002v3), latest v3 released Oct 2, reports that a tool-augmented statement-formalization system compiled 87.2% of 227 graduate-level statements but met its cross-judge semantic-fidelity criterion on 57.7%; human audits support the criterion as a useful but imperfect proxy. [FaithformBench](https://arxiv.org/abs/2608.10916) tests whether incorrect natural-language steps are preserved rather than silently corrected. [Robustness of Proof Autoformalization](https://arxiv.org/abs/2606.14867) tests local semantic perturbations. [The Faithfulness Gap](https://arxiv.org/abs/2606.16541) studies bidirectional provability fingerprints and conditional distributional guarantees. [ProofFlow](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5fce5198dbf92d5ff45f74504431e2ff-Abstract-Conference.html) and [LeanArchitect](https://arxiv.org/abs/2601.22554) address structural alignment. We cannot plausibly claim novelty for detecting some NL/Lean mismatches or drawing an argument graph.

Our proposed research remains **proof-to-understanding**, with evidence-carrying *mathematical reusability* as the endpoint. The new Semantic Contract is an upstream validity gate. A downstream model may excel at tasks concerning a silently altered theorem; that apparent transfer must not be counted as understanding the intended original result.

The main scientific protocol thus separates producer, frozen artifact, and an independent consumer deprived of the original source. Before freezing, require a scoped semantic audit and explicit unresolved bridges. Downstream experiments must score mathematical transfer, false certification risk, fidelity coverage and selective UNKNOWN. Strong baselines include original proof, ordinary summary, token-matched excerpt, and artifact with/without the Semantic Contract. Graph is only a representation ablation, and not automatically a stronger explanation.

### 10.3 Reproduced diagnostics and limits

We implemented a restricted five-case development instrument in design_v1/semantic_bridge/ with exact coefficient arithmetic, a symbolic existence counterexample, constrained norm-order diagnostics, time-quantifier comparison and extra right-hand-side symbol detection. Six unit tests and the five checks completed successfully in [GitHub Actions run 37958200358](https://github.com/Andytonglove/math/actions/runs/37958200358).

The generic high-frequency derivative example demonstrates why a uniform C^(m+5) estimate for arbitrary differential operators does not automatically imply the analogous C^(m+4) estimate. **It is not a counterexample to the specific inverse Navier–Stokes operator.** Likewise, locating a new RHS symbol or a time-quantifier change is an audit finding, not a complete proof of implication or non-implication between two different PDE theorems. Our result explicitly reports that full NL/Lean semantic equivalence is NOT ESTABLISHED.

No new trained extractor, artifact-only reader advantage, full Lean compilation, mathematical referee assessment of the PDE claims, or human-comprehension experiment has been performed. This work revises the research design and provides a tested diagnostic component. A defensible main result still requires frozen artifacts, held-out source-conditioned transfer tasks, sufficiently capable independent consumers and separately checked mathematical answers.

