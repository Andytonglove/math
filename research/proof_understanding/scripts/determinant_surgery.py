"""Exact algebraic proof-surgery tasks from the limiting two-case determinant bound.
This checks a local certificate, not the correctness of the pi theorem.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
from random import Random
import argparse, hashlib, json

SOURCE = "preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections/determinant.tex"
PIN = "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb"
MODES = ("minimal","theorem","proof","syntax","hypergraph","prose","distractor")

@dataclass(frozen=True)
class Bound:
    nu:F
    A:F
    eta:F
    b:F
    Ea:F
    En:F
    C:F

def normalized_bounds(x:Bound):
    return (-(1-x.b)-x.Ea, x.En-x.C, x.En-x.nu*(x.A*(1-x.eta)-x.b))

def classify(x:Bound):
    lower,upper_collision,upper_approx=normalized_bounds(x)
    yes_collision=upper_collision < lower
    yes_approx=upper_approx < lower
    return ("BOTH" if yes_collision and yes_approx else
            "ONLY_COLLISION" if yes_collision else
            "ONLY_APPROX" if yes_approx else "NEITHER")

def independent_oracle(x:Bound):
    """Independently rearranged exact inequalities, not copied comparison."""
    req=1-x.b+x.Ea+x.En
    c=x.C>req
    a=x.nu*(x.A*(1-x.eta)-x.b)>req
    return ("BOTH" if c and a else
            "ONLY_COLLISION" if c else "ONLY_APPROX" if a else "NEITHER")

def random_base(seed):
    r=Random(seed)
    x=Bound(F(r.randint(3,5)),F(r.randint(32,36),40),
            F(r.randint(1,3),20),F(r.randint(4,12),40),
            F(r.randint(1,3),80),F(r.randint(1,3),80),F(0))
    threshold=1-x.b+x.Ea+x.En
    x=replace(x,C=threshold+F(1,10))
    if classify(x)!="BOTH":raise AssertionError("generation domain")
    return x

def surgeries(x):
    threshold=1-x.b+x.Ea+x.En
    eta_tie=1-(x.b+threshold/x.nu)/x.A
    if not x.eta<eta_tie<1:raise AssertionError("eta tie not interior")
    eta_bad=(eta_tie+1)/2
    low_bad=threshold-F(1,10)
    if low_bad<=0:raise AssertionError("collision penalty nonpositive")
    return {
        "unmodified":x,
        "weaken_collision":replace(x,C=low_bad),
        "weaken_approx":replace(x,eta=eta_bad),
        "weaken_both":replace(x,C=low_bad,eta=eta_bad),
        "tie_collision":replace(x,C=threshold),
        "tie_approx":replace(x,eta=eta_tie),
    }

TASK=("An arithmetic LOWER bound is L=-(1-b)-Ea. There are two exhaustive "
      "alternative analytic UPPER bounds: Uc=En-C in the collision case, "
      "and Ua=En-nu*(A*(1-eta)-b) in the approximation case. "
      "Each branch is a strict contradiction precisely when its upper bound "
      "is LESS THAN L. Determine which branches contradict. Return only JSON: "
      '{"branch_status":"BOTH|ONLY_COLLISION|ONLY_APPROX|NEITHER"} '
      "using exactly one of these four values. All numbers are exact fractions.")
CONTEXT={
    "minimal":"",
    "theorem":"The reported source theorem concerns irrationality exponent 2 of pi, for nu>2. This task concerns only a simplified determinant certificate.",
    "proof":"Source mechanism: interpolation produces a nonzero determinant with an arithmetic lower bound. For each term in its analytic expansion, either many low-weight indices create quadratic collision savings, or enough high-weight indices create rational approximation savings. Both cases must be bounded strictly below the same arithmetic lower bound; equality does not close the argument.",
    "syntax":"Source reference labels: det:lower, det:arithmetic, det:translation, det:collision, det:comparison, det:upper. Citation presence does not establish logical necessity.",
    "hypergraph":"Typed candidate structure: LOWER=L; COLLISION=Uc<L; APPROX=Ua<L. Both COLLISION and APPROX are exhaustive case certificates. AND-hyperedge (COLLISION, APPROX) implies proof-by-cases closes. Equality is failure.",
    "prose":"A proof by cases can only reach a contradiction if each possible case contradicts the arithmetic lower bound. Check the collision upper bound and the approximation upper bound separately. Even one unsuccessful case makes the overall two-case certificate insufficient. A tie does not count.",
    "distractor":"A finite group algebra is finite-dimensional. Consequently, one-sided inverses in it are two-sided. This elementary point appears in a different mathematical manuscript, unrelated to determinant savings."
}

def q(x):
    return str(x)

def make_dataset(seed=26008,bases=12):
    if not 1<=bases<=1000:raise ValueError("bases must be between 1 and 1000")
    rng=Random(seed ^ 0x51AF)
    items=[];gold=[];counts=Counter()
    for i in range(bases):
        for name,x in surgeries(random_base(seed+10007*i)).items():
            truth=classify(x)
            if truth!=independent_oracle(x):raise AssertionError("independent oracle mismatch")
            opaque=hashlib.sha256(f"v1/{seed}/{i}/{name}".encode()).hexdigest()[:20]
            params=", ".join(f"{k}={q(getattr(x,k))}" for k in x.__dataclass_fields__)
            items.append((opaque,params))
            gold.append({"id":opaque,"family":"017","answer_type":"choice",
                         "answer":truth,"surgery":name,
                         "bounds":[q(z) for z in normalized_bounds(x)],
                         "oracle":"exact Fraction, direct and independent rearrangement"})
            counts[truth]+=1
    rng.shuffle(items);rng.shuffle(gold)
    prompts=[{"id":i,"condition":mode,"family":"017",
              "prompt":"\n\n".join(z for z in [CONTEXT[mode],TASK,params] if z)}
             for mode in MODES for i,params in items]
    return {"meta":{"schema_version":"0.1","source_commit":PIN,"source":SOURCE,
                    "seed":seed,"base_instances":bases,"tasks":len(items),
                    "conditions":list(MODES),"model_runs":0,
                    "warning":"Limiting algebraic skeleton; not full source proof."},
            "prompts":prompts,"gold":gold,"distribution":dict(counts)}

def sanity_baselines(gold):
    actual={r["id"]:r["answer"] for r in gold}
    correct_AND=sum(v==actual[k] for k,v in actual.items())
    wrong_OR=sum(("BOTH" if v!="NEITHER" else "NEITHER")==v
                 for v in actual.values())
    return {"exact_AND":{"correct":correct_AND,"total":len(actual)},
            "invalid_OR_shortcut":{"correct":wrong_OR,"total":len(actual)},
            "notice":"Deterministic checks, NOT language model evaluations."}

def write_data(data,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    (folder/"metadata.json").write_text(json.dumps(data["meta"],indent=2)+"\n")
    (folder/"prompts.jsonl").write_text("".join(
        json.dumps(r,ensure_ascii=False)+"\n" for r in data["prompts"]))
    (folder/"gold.json").write_text(json.dumps({"entries":data["gold"]},indent=2)+"\n")
    (folder/"sanity.json").write_text(json.dumps(sanity_baselines(data["gold"]),indent=2)+"\n")

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--source-root",default=".")
    a.add_argument("--seed",type=int,default=26008)
    a.add_argument("--bases",type=int,default=12)
    a.add_argument("--out-dir",required=True)
    p=a.parse_args()
    source=(Path(p.source_root)/SOURCE).read_text(encoding="utf-8")
    for marker in (r"\label{det:lower}",r"\label{det:comparison}",r"\label{det:upper}"):
        if marker not in source:raise ValueError("Missing source anchor "+marker)
    d=make_dataset(p.seed,p.bases);write_data(d,p.out_dir)
    print(json.dumps({"tasks":d["meta"]["tasks"],"prompts":len(d["prompts"]),
          "distribution":d["distribution"],"sanity":sanity_baselines(d["gold"]),
          "model_runs":0},indent=2))

if __name__=="__main__":main()
