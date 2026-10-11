"""Public development answer keys; source-level claims remain unreviewed."""
def gold_labels() -> dict[str, dict]:
    return {
        "017_strict_threshold": {"claim": "LOCALLY_ESTABLISHED", "proof": "VALID_LOCAL", "tier": "HUMAN_PROOF_WITH_ALGEBRAIC_INEQUALITY"},
        "017_true_claim_bad_step": {"claim": "LOCALLY_ESTABLISHED", "proof": "INVALID_STEP", "tier": "EXACT_RATIONAL_STEP_COUNTEREXAMPLE_AND_INDEPENDENT_PROOF"},
        "017_false_slope_extension": {"claim": "EXACTLY_REFUTED", "proof": "INVALID_STEP", "tier": "EXACT_RATIONAL_COUNTEREXAMPLE"},
        "017_source_main_unknown": {"claim": "NOT_INDEPENDENTLY_AUDITED", "proof": "NOT_AUDITED", "tier": "SCOPE_ONLY"},
        "197_mixed_commuting": {"claim": "LOCALLY_ESTABLISHED", "proof": "VALID_LOCAL", "tier": "HUMAN_ASSOCIATIVITY_PROOF_FINITE_SANITY"},
        "197_true_claim_bad_step": {"claim": "LOCALLY_ESTABLISHED", "proof": "INVALID_STEP", "tier": "NONCOMMUTATIVE_STEP_COUNTEREXAMPLE_AND_INDEPENDENT_PROOF"},
        "197_missing_second_inverse_condition": {"claim": "EXACTLY_REFUTED", "proof": "INVALID_STEP", "tier": "ALGEBRAIC_IDENTITY_COUNTEREXAMPLE"},
        "197_monoid_witness": {"claim": "LOCALLY_ESTABLISHED", "proof": "VALID_LOCAL", "tier": "ELEMENTARY_SYMBOLIC_IDENTITY_PREFIX_SANITY"},
        "197_group_existence_unknown": {"claim": "NOT_INDEPENDENTLY_AUDITED", "proof": "NOT_AUDITED", "tier": "SCOPE_ONLY"},
    }

