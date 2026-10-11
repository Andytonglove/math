"""Public dual-axis proof audit corpus. Not a theorem prover or human result."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from audit_math import (F, CLAIM_LABELS, PROOF_LABELS, barrier_ok, nonconvex, permutations, mul,
    finite_operator_checks, monoid_shift_checks, exact_diagnostics, score_labels)
from audit_definitions import source_independent_cases, gold_labels, explanation_records

def build_dataset() -> tuple[dict, dict, dict]:
    rational = exact_diagnostics()
    finite = finite_operator_checks()
    shifts = monoid_shift_checks()
    cases = source_independent_cases()
    gold = gold_labels()
    explanations = explanation_records()
    ids = [x["id"] for x in cases]
    if len(set(ids)) != len(ids) or set(ids) != set(gold) or set(ids) != set(explanations):
        raise ValueError("card/gold/explanation ID mismatch or duplication")
    for item in gold.values():
        if item["claim"] not in CLAIM_LABELS or item["proof"] not in PROOF_LABELS:
            raise ValueError("unknown grading label")
    # Two independent axes: a true claim may have a demonstrably invalid proof.
    for item_id in ("017_true_claim_bad_step", "197_true_claim_bad_step"):
        assert gold[item_id]["claim"] == "LOCALLY_ESTABLISHED"
        assert gold[item_id]["proof"] == "INVALID_STEP"
    for item_id in ("017_source_main_unknown", "197_group_existence_unknown"):
        assert gold[item_id]["claim"] == "NOT_INDEPENDENTLY_AUDITED"
        assert gold[item_id]["proof"] == "NOT_AUDITED"
    public = {"purpose": "public_development_only", "human_outcomes": "NOT_MEASURED",
              "mathematical_scope": "two manually studied local source-inspired families; source high-level truth unverified",
              "cases": cases}
    answer_key = {"purpose": "public_development_answer_key_NOT_hidden", "human_outcomes": "NOT_MEASURED",
                  "labels": {id: {**gold[id], "explanation_for_expert_review": explanations[id]} for id in ids}}
    diagnostics = {"exact_rational": rational, "finite_permutations": finite,
                   "monoid_shift": shifts, "count_cards": len(ids), "human_participants": 0,
                   "verified_by_machine": "local arithmetic and counterexample checks, NOT universal source theorem verification",
                   "universal_arguments": "human-readable derivations in answer key, not machine/formal proofs"}
    return public, answer_key, diagnostics


def write_data(directory: Path) -> dict:
    cards, gold, checks = build_dataset()
    directory.mkdir(parents=True, exist_ok=True)
    for fname, obj in (("cards_public_dev.json", cards), ("gold_public_dev.json", gold), ("checks_public_dev.json", checks)):
        (directory / fname).write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return checks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "data")
    args = parser.parse_args()
    print(json.dumps(write_data(args.output), indent=2))
