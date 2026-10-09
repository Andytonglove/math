# Mathematical result from the frozen 197 mechanism: commuting left and right actions

**Status:** independently derived elementary algebraic consequence, source-inspired. Not a new research-level theorem or validation of Kaplansky's conjecture.

Let K be a commutative field, G any group and c,d finite-support elements of K[G]. On all x:G→K, let

    (T_c x)(g) = ∑_{u∈G} c_u x(gu),     (S_d x)(g) = ∑_{v∈G} d_v x(vg).

Every sum is finite because c,d are finitely supported. From the original right-neighbor representation, T_c T_d = T_cd. The left-neighbor variant satisfies S_c S_d = S_dc: the order is reversed. However, **left and right actions commute with one another**:

    (T_c S_d x)(g) = ∑_u c_u ∑_v d_v x(vgu)
                     = ∑_v d_v ∑_u c_u x(vgu)
                     = (S_d T_c x)(g).

Only group associativity, finite support and commutativity of scalar multiplication in K are used. Thus the image of the right group algebra action commutes with the left group algebra action; this is a basic bimodule phenomenon.

## Why the mathematical mechanism matters

The key transferable insight is not just that the paper invokes a lemma about cellular automata. It is the relationship between **operator convention** and **multiplication direction**. A model that changes x(gu) to x(ug) but retains the same composition law silently changes the proof mechanism. In a noncommutative group the resulting theorem statement is in general wrong.

An exact finite counterexample to order confusion is available in F₂[S₃], with permutations indexed lexicographically as in scripts/s3_operator_transfer.py. Take a=2 (singleton index 1, 021), b=4 (singleton index 2, 102) and delta at group identity h=0. Then ab has coefficient-mask 16 while ba has mask 8. With the right-neighbor convention (T_a T_b)(delta_e) is mask 8, but the incorrectly reversed product produces mask 16. With the left-neighbor convention the correct output is 16, and the unreversed product incorrectly gives 8. These outputs can be checked by direct evaluation of six basis coordinates.

## Exactly what is supported

- General T_c S_d = S_d T_c: complete short proof above, no advanced source assumption.
- T_c T_d = T_cd and S_c S_d = S_dc: complete direct finite-sum proof as given in frozen artifact.
- The finite group F₂[S₃] task oracle checks all 64² coefficient-pairs and six basis inputs for three tracks (73,728 paired direct-vs-derived comparisons in a single exhaustive test), then chooses 36 nonzero, noncommuting development tasks.
- The source's claimed exotic group G and elements a,b with ab=1 but ba≠1 are **not constructed or verified** by this note. Finite group algebras cannot provide such a witness.
- Lean theorem correspondence remains UNKNOWN; no source-claim certification is implied.

## Consequences for the real research question

We have one honest mathematics-only example of using a proof mechanism to derive a new relation about an adjacent construction. Whether the frozen explanatory artifact helps an AI reader discover or calculate such relations better than the original text, an ordinary summary or the bare definitions is an **empirical question**. Our development test controls numerical data and uses source-deprived prompts, but the producer is manual, the task generator is public, task templates are researcher-designed and input lengths are not matched.

Do not turn an exact finite-algebra oracle score into 'the model understands the 197 proof' or a claim about human comprehension. A stronger study would test genuinely withheld extension families, source/method error detection and multiple capable models with stable contexts and math expert auditing.

## Provenance

Frozen artifact commit: 04fef27eed6f3a10e529f728f3f478cb459f0821.
Source research family: 197, original section 06-cellular-automata.tex in repository commit 79b8d182b49e7184708bd22bfec1e9a9b1d41994.
Code: design_v1/consumer/generate_197.py and research/proof_understanding/scripts/s3_operator_transfer.py.
