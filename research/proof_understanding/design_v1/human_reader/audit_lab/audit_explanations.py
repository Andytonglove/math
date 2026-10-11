"""Public development answer keys; source-level claims remain unreviewed."""
def explanation_records() -> dict[str, str]:
    return {
        "017_strict_threshold": "theta>A^2 implies (A-theta)/(1-theta)<(A-A^2)/(1-A^2)=A/(1+A)<1/2. All inequalities are strict.",
        "017_true_claim_bad_step": "The inequality direction is reversed: theta>A^2 means A-theta<A-A^2. At A=3/4, theta=5/8 the incorrect step asserts 1/8>3/16. The true nu>2 necessity follows from the *correct* upper bound, independently of the flawed step.",
        "017_false_slope_extension": "For h(A)=A^2-3A^3(1-A)^2, h(1)=1 and h'(1)=2. Yet A=3/4, theta=31/64, nu=39/20 gives h(A)=495/1024<496/1024 and strict second-inequality slack 3/1280>0. Endpoint slope does not imply the global tangent bound.",
        "017_source_main_unknown": "A checked local auxiliary feasibility lemma neither certifies nor refutes the source's high-level pi theorem. Independent whole-proof and NL/Lean correspondence reviews are absent; NOT_INDEPENDENTLY_AUDITED is epistemic, not a claim that truth is undecidable.",
        "197_mixed_commuting": "T_u S_v x(g)=S_v x(gu)=x(v(gu))=x((vg)u)=S_v T_u x(g), by associativity. A finite S3 check is supplemental only.",
        "197_true_claim_bad_step": "S3 transpositions u=(1,0,2), v=(0,2,1) and g=e violate ugv=vgu, because uv!=vu. The theorem is nonetheless valid by reassociating v(gu)=(vg)u without swapping u,v.",
        "197_missing_second_inverse_condition": "a=b=1 yields ab=1 but T_b=I, which is surjective. Having a left inverse gives injectivity, not nonsurjectivity; the source conditional argument also requires ba!=1.",
        "197_monoid_witness": "L(R(n))=max(n+1-1,0)=n for every natural n, whereas R(L(0))=1. In the free K-module basis of monoid algebra, the two distinct transformations yield [L][R]=[1] and [R][L]!=[1]. These maps do not constitute a group.",
        "197_group_existence_unknown": "A monoid witness does not instantiate the original GROUP assumptions. The conditional operator mechanism cannot establish existence of elements satisfying its hypotheses in the particular proposed group. No independent high-level group proof review is recorded.",
    }

