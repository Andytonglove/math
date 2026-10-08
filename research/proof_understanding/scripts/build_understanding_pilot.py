"""Build *mechanism-unit* probes for Understanding AI-Generated Mathematical Proofs.

All gold answers come from small independent mathematics oracles. We do NOT
claim these establish comprehension of the 017/102/197 research proofs.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction
from pathlib import Path

from parameter_oracle import construct, minimum_pairwise_collisions, collision_scaling_example, InfeasibleParameter
from understanding_oracles import (
    xor_translation_assignment, exact_unique_game_value,
    enumerate_one_sided_pairs, shift_left, shift_right, example_games
)

BASE017="preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections/"
BASE102="preprints/The-Unique-Games-Theorem-September-23-2026/build/sections/"
BASE197="preprints/A-Counterexample-to-Kaplanskys-Direct-Finiteness-Conjecture-in-Characteristic-Two-September-23-2026/build/sections/"

def entry(id, family, domain, question, answer_type, answer, anchor_file, anchor,
          oracle, math_role, notes):
    return {
        "id":id, "family":family, "domain":domain,
        "question":question, "answer_type":answer_type, "answer":answer,
        "source_provenance":{"file":anchor_file,"anchor":anchor},
        "oracle":oracle, "math_role":math_role, "notes":notes,
        "benchmark_status":"unit_probe_only",
        "requires_original_research_result_to_be_correct":False
    }


def build(root: Path) -> dict:
    root=root.resolve()
    games=example_games()
    sat_yes,_=xor_translation_assignment(4,2,games["consistent"])
    sat_no,_=xor_translation_assignment(4,2,games["one_edge_perturbed"])
    val_no=exact_unique_game_value(4,2,games["one_edge_perturbed"])
    count,violations=enumerate_one_sided_pairs(4)
    comparison=collision_scaling_example(8,1)
    try:
        construct(Fraction(2))
        boundary=False
    except InfeasibleParameter:
        boundary=True
    # construct rejecting nu <= 2 is only a test of the constructor's domain;
    # the accompanying maths note gives the genuine impossibility proof.
    assert boundary and val_no==Fraction(3,4) and sat_yes and not sat_no
    assert violations==0 and count>0
    assert comparison['normalized_quadratic_saving']=='1/4' and comparison['normalized_linear_saving']=='1/8'
    assert all(shift_left(shift_right(x))==x for x in range(256))
    assert shift_right(shift_left(1))!=1
    edge_txt=lambda edges: "; ".join(f"({u},{v},shift={s})" for u,v,s in edges)

    tasks=[
        entry("017-PARAM-BOUNDARY","017","number_theory",
            "A proof requires 0<theta<A<B<1, C>1, B<1/C, B<C*theta<1, and nu*(A-theta)>1-theta. At nu=2, can the same inequalities all hold?",
            "boolean",False,BASE017+"conclusion.tex",r"\label{par:constants}",
            "symbolic_parameter_infeasibility_and_exact_boundary_guard",
            "assumption_intervention","No: the B,C inequalities force A^2<theta, implying 2(A-theta)<1-theta. This does NOT refute the stronger theorem."),
        entry("017-COLLISION-7-3","017","number_theory",
            "Seven rows may use at most three Taylor-index groups. What is the minimum number of unordered pairs that must share a group?",
            "integer",minimum_pairwise_collisions(7,3),BASE017+"determinant.tex",r"\label{det:collision}",
            "balanced_occupancy_formula","combinatorial_mechanism","The balanced counts 3,2,2 give 5. This is not the full analytic determinant bound."),
        entry("017-COLLISION-10-3","017","number_theory",
            "Ten rows may use at most three Taylor-index groups. What is the minimum number of unordered pairs that must share a group?",
            "integer",minimum_pairwise_collisions(10,3),BASE017+"determinant.tex",r"\label{det:collision}",
            "balanced_occupancy_formula","perturbed_mathematical_transfer","The balanced counts 4,3,3 give 12; accessible without the original paper."),
        entry("017-COLLISION-SCALING","017","number_theory",
            "In a determinant argument with M rows and degree H, the low-index collision saving changes from exp(-c*sum_a n_a^2) to the weaker exp(-c*sum_a n_a), with sum_a n_a=M. After dividing log|det| by M*H and taking H->infinity, does the weaker saving still provide an H-independent strictly positive margin?",
            "boolean",False,BASE017+"determinant.tex",r"\label{det:collision}",
            "quadratic_vs_linear_normalization","proof_mechanism_ablation",
            "No. The weaker saving contributes only c/H and vanishes. A quadratic saving may persist at positive normalized scale with repeated indices; this does not independently verify the original analytic bound."),
        entry("102-XOR-CONSISTENT","102","complexity_theory",
            "In F_2^2, translation constraints x[v]=x[u] XOR shift on vertices 0..3 are: "+edge_txt(games["consistent"])+". Can all constraints be satisfied simultaneously?",
            "boolean",sat_yes,BASE102+"00-introduction.tex",r"\label{thm:ugc}",
            "xor_component_consistency","mechanism_microcase","Simple 4-cycle; does not verify the Unique Games hardness reduction."),
        entry("102-XOR-EDGE-FLIP","102","complexity_theory",
            "In F_2^2, translation constraints x[v]=x[u] XOR shift on vertices 0..3 are: "+edge_txt(games["one_edge_perturbed"])+". Can all constraints be satisfied simultaneously?",
            "boolean",sat_no,BASE102+"00-introduction.tex",r"\label{thm:ugc}",
            "xor_component_consistency","counterfactual_intervention","Single edge shift changed; nonzero XOR around the cycle is inconsistent."),
        entry("102-XOR-OPT-VALUE","102","complexity_theory",
            "In F_2^2, the four translation constraints are: "+edge_txt(games["one_edge_perturbed"])+". What is the maximum fraction of simultaneously satisfied constraints?",
            "fraction",str(val_no),BASE102+"00-introduction.tex",r"\label{thm:ugc}",
            "bruteforce_small_game_optimum","quantitative_intervention","Three of four constraints can be met; no labeling meets all four."),
        entry("197-FINITE-GROUP-OBSTRUCTION","197","algebra",
            "If G is a finite group and K any field, can there exist a,b in K[G] with ab=1 but ba!=1?",
            "boolean",False,BASE197+"01-introduction.tex","For a finite group $G$",
            "finite_dimensional_linear_algebra_proof_and_gf2_cyclic_checks",
            "assumption_intervention","No: K[G] is finite dimensional. Left multiplication by a has a right inverse and is therefore bijective; hence also ba=1. Finite cyclic GF2 cases are brute-checked."),
        entry("197-ONE-SIDED-SHIFT","197","algebra",
            "On finitely supported sequences over F_2 with basis e_0,e_1,..., define R(e_i)=e_(i+1), L(e_0)=0, L(e_(i+1))=e_i. Which composition equals identity on all vectors: LR, RL, both, or neither?",
            "choice","LR",BASE197+"01-introduction.tex","If a linear map on a finite-dimensional vector space",
            "symbolic_infinite_shift_identity_and_finite_support_checks",
            "mechanism_analogy","LR=I; RL=I-P_{e0}. This is an infinite-dimensional linear analogy, NOT the paper's group-ring construction.")
    ]
    paths={}
    for t in tasks:
        p=t["source_provenance"]["file"]
        if p not in paths:
            path=root/p
            if not path.is_file():raise FileNotFoundError(str(path))
            paths[p]=path.read_text(encoding="utf-8")
        if t["source_provenance"]["anchor"] not in paths[p]:
            raise ValueError("Missing source anchor for "+t["id"])
    if len({t["id"] for t in tasks})!=len(tasks):raise ValueError("Duplicate IDs")
    base={
        "version":"0.1.0",
        "corpus":"Andytonglove/math pinned upstream commit fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb",
        "task_count":len(tasks),
        "families":sorted(set(t["family"] for t in tasks)),
        "evaluation_warning":"These tasks have elementary independent mathematical oracles and are NOT evidence of understanding the original research proof. No model has been tested.",
        "source_oracle_warning":"Original OpenAI research manuscripts may not yet be independently validated. Unit oracles do not rely on their main theorem being true."
    }
    prompts={**base,"entries":[{k:v for k,v in t.items() if k not in ("answer","notes","oracle")} for t in tasks]}
    gold={**base,"entries":[{k:t[k] for k in ("id","family","answer_type","answer","oracle","math_role","notes")} for t in tasks]}
    return {"prompts":prompts,"gold":gold}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",default=".")
    parser.add_argument("--out-dir",required=True)
    args=parser.parse_args()
    output=build(Path(args.root))
    folder=Path(args.out_dir);folder.mkdir(parents=True,exist_ok=True)
    for name,data in output.items():
        (folder/(name+".json")).write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"count":output["prompts"]["task_count"],
                      "families":output["prompts"]["families"],
                      "oracle_labels":len(output["gold"]["entries"]),
                      "model_evaluations":0},indent=2))


if __name__=="__main__":main()
