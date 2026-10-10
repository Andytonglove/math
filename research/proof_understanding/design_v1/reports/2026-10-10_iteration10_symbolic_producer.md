# Iteration 10 — Source-grounded automatic producer (restricted) and a finite-dimensional transfer boundary

Date: 2026-10-10, Asia/Shanghai. Branch: research/proof-understanding-pilot. Starting head: f2a9146d89ad4f0dbfa8d4aef6d82b5744331347. Code commit: b315d02471f0b6216b04a6c7089582629a2f8b4e.

## 1. Scientific decision and exact scope

The previous manually frozen 197 artifact, 36 finite group-algebra developer tasks, and the incomplete 10/24 Qwen2.5-1.5B CPU run do NOT establish automated source understanding or any reader benefit. Rather than pay for another weak model to compute long 6-bit convolution answers, this iteration makes a small genuinely executable producer that reads the unmodified original source TeX. It exercises mathematical assumption boundaries and accurate UNKNOWN handling without claiming research-level source correctness.

This is a **restricted deterministic source-template recognizer**, not an LLM and not an automatic mathematics discovery system. It cannot transfer unassisted to novel papers or certify faithful natural-language/Lean correspondence. It is a concrete instrumented negative-control baseline for future producers, not a scientific demonstration of AI reading research mathematics.

## 2. What was actually implemented

Files under design_v1/producer/:
- source197_producer.py: reads the original 197 LaTeX section; locates 5 labeled equations, the original representation lemma and transfer proposition; checks their source-scoped premises, right-neighbor ordering, coefficient recovery, image formula, left-inverse claim, and two explicit proof-step strings. Records SHA-256 of the source and equation bodies and 1-based source line locations. Emits a structured JSON contract with five conditional mathematical claims, proof-scope labels, missing assurances, and a candidate monoid transfer.
- finite_boundary.py: builds the full transformation monoid on a two-point set, enumerates the 16 elements of its algebra over F2, exhausts 256 coefficient pairs for one-sided inverses, and emits six human-authored epistemic test cards (YES/NO/UNKNOWN). No model responses appear in these cards.
- tests/: checks explicit source mutation classes, symbolic monoid index-word normalization, finite algebra associativity and units, and the actual manuscript when checked out. A new GitHub Actions workflow runs the tests and generates original machine-readable output, without modifying the source or main.

The successful output is **not a faithful reconstruction of an arbitrary proof**: its rules and eligible source anchors were manually predeclared. The producer extracts and checks a narrowly known argument; it does not synthesize new general-purpose proof mechanisms. The transition to monoids is a separately justified conditional mathematical extension, not a statement quoted from the source.

## 3. Exact mathematical argument: monoid operator lemma

Let M be any unital associative monoid, K any field, K[M] its finite-support monoid algebra, and K^M all functions from M to K. For finitely supported c, define

    (T_c x)(g) = sum_{u in M} c_u x(gu).

Because the sum is finite, T_c is well-defined on all configurations even if x has infinite support. Associativity gives

    (T_c T_d x)(g) = sum_{u,v} c_u d_v x((gu)v)
                   = sum_{u,v} c_u d_v x(g(uv))
                   = (T_(cd) x)(g).

The identity acts as I. For every h in M, using delta_h and monoid identity e,

    (T_c delta_h)(e) = c_h,

so c -> T_c is faithful. No inverses in M are used anywhere in these statements.

Assume a,b in K[M] have ab=1. Then T_a T_b=I, hence T_b is injective. Put P=T_b T_a=T_(ba); it is idempotent and

    im(T_b) = Fix(P).

If ba!=1, some coefficient (ba-1)_h is nonzero. The delta configuration delta_h is not fixed by P because ((P-I)delta_h)(e)=(ba-1)_h != 0. Therefore it is not in the image of T_b and T_b is not surjective.

**This generalizes only the conditional operator transfer** from the source's group setting to a monoid. The original high-difficulty claim of group-ring elements satisfying ab=1, ba!=1 is neither proved nor disproved here. Neither this derivation nor CI verifies the author's proposed group existence result, the claimed nonsurjunctivity corollary, or corresponding Lean objects.

Finite K is required in the source to describe the operator as a cellular automaton over a *finite alphabet*; arbitrary K suffices for the algebraic identities on K^M. Treating these premises as interchangeable would be a semantic error.

## 4. New structural boundary: finite-dimensionality, not groupness

**Theorem (elementary).** If A is a finite-dimensional unital algebra over a field and a,b in A satisfy ab=1, then ba=1.

Proof. Consider left multiplication L_a and L_b acting linearly on the finite-dimensional vector space A. Since L_a composed with L_b is the identity, L_b is injective and hence bijective. Consequently its inverse is L_a, so L_b composed with L_a is also the identity. Evaluating at 1 gives ba=1. QED.

As a consequence, for ANY finite monoid M, K[M] cannot contain an ab=1, ba!=1 pair. This is stronger than a statement restricted to finite groups but makes **no claim about arbitrary infinite groups**.

Contrast the infinite transformation monoid generated by L(n)=max(n-1,0) and R(n)=n+1, with multiplication by composition. For all natural n, L(R(n))=n, whereas R(L(0))=1 !=0. The singleton algebra elements [L] and [R] satisfy [L][R]=1, [R][L]!=1. This supplies the assumption-sensitive infinite MONOID example documented in iteration09. Its existence does not establish anything about the exotic original GROUP example.

This yields a useful three-way diagnostic:
- finite-dimensional unital algebra: one-sided inverse defect impossible (independent theorem, NO);
- infinite bicyclic/transformation monoid algebra: explicit defect possible (symbolic witness, YES);
- original infinite group algebra existence construction: not independently audited in this project (epistemic UNKNOWN; neither NO nor a certified YES).

## 5. Actual executed checks and preserved raw evidence

Local standard-library test run: 14 test methods discovered, 13 passed and one source-file-dependent test skipped because the local runtime has no cloned upstream TeX. The real source was independently fetched and its expected literal anchors screened before commit. No source file was edited.

GitHub CI then checked out the **actual original 197 TeX** and ran all 14 tests without a skip: workflow 38017985317 PASSED at code commit b315d024. The existing pilot workflow 38017985270 also PASSED. These green results certify only the executable checks and expected source strings, NOT semantic correspondence or research-level theorems.

Generated source contract: source SHA-256 f24be1d93784302e0700c0223023c0f4f49a9c2e342e21be04a5627ae0492775; 7 anchored items (5 equation blocks, lemma, proposition); gate PASSED_SCOPED with no flagged mismatches; 5 emitted conditional claims. This is a producer output on a REAL research manuscript source, but with template-familiar mathematical content. The complete generated JSON is archived in CI and committed with this report.

Finite exact arithmetic: checked 64 compositions of the four transformations in the associativity unit test, 4,096 triples of the 16-element algebra in the associativity unit test, and 256 ordered algebra-element pairs for ab=1. Exactly 4 ordered pairs satisfy ab=1, and ALL 4 also satisfy ba=1. This is numerical confirmation for one finite example; the universal result is the separate linear-algebra proof above.

Six openly designed symbolic boundary cards: five definite YES/NO and one correctly calibrated epistemic UNKNOWN. These labels are authored mathematical examples, NOT a reader model's achieved scores and NOT a blinded held-out test set.

Synthetic error interventions tested: change x(gu) to x(ug); reverse T_c T_d multiplication order; insert a false gvu source proof step while retaining a true lemma statement; remove the ab=1 assumption; remove finiteness of K from the finite-alphabet proposition; remove the nonzero-defect proof step. Each corresponding gate test detected its designed mutation and withheld all reusable claims. This does not mean that a malicious or complex false proof cannot evade this very weak lexical checker. No genuine flaw in the original 197 TeX section was established.

Raw CI source contract and finite enumeration: see producer/data/produced_197_2026-10-10.json and producer/data/finite_boundary_2026-10-10.json in this commit; the unchanged source file remains at its original path. The initial reference artifact frozen at 04fef27 was NOT modified.

Costs: no paid model/API/service requested, no new language-model inference, no GPU, no user-approved stronger reader budget. GitHub public-repo workflow tests ran on hosted CPU; account billing was not independently inspected, so we do not report zero monetary cost as a verified account claim.

## 6. Limitations, falsifiers, and next milestone

The producer's positive gate is **syntactic source matching plus a limited word-order certificate**. It is deliberately not a correct general-purpose proof checker. In particular it can accept an incorrect mathematical statement placed in unrecognized sections or a sophisticated false proof that preserves the trigger strings; source references do not establish semantic edges. The six mutation cases are chosen by the implementer. They measure whether six known corruptions are caught, not source-faithfulness sensitivity. We did not evaluate any AI consumer, prove artifact-only gain, or quantify the uncertainty calibration of a model. Graph has no role in this outcome.

Next, the real methodological question is whether a producer that has NOT been given a prewritten theorem-specific template can extract the premise-sensitive mechanism and an honest semantic contract from a genuinely distinct source. A possible falsifier is that the new producer offers no advantage over simple passage retrieval and a token-matched ordinary summary after the source is removed. Preserve the generated source contract now; a separate evaluator must select structural, not merely numerical, new questions after freeze. Compare statement-only/no-proof, full source, token-matched excerpt and ordinary prose, with semantic faithfulness scored separately from task correctness and format. Any new strong model inference requires explicit user authorization.

The user-visible short conclusion should remain: **a real but deliberately narrow automatic TeX-to-contract baseline and a new exact finite-dimensional boundary were completed; general automatic mathematical-proof understanding and artifact-only transfer remain unmeasured.**
