"""Exact proof-mechanism transfer for a generalized parameter inequality.

Given integer r>=2 and rational nu, ask whether rational 0<theta<A<1
with A^r<theta and nu*(A-theta)>1-theta can exist.

The precise criterion is nu > r/(r-1). This is an independent elementary
algebraic result, inspired by family 017's parameter construction, NOT an
extension of its deep geometric interpolation theorem.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import argparse, json

SOURCE="preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections/conclusion.tex"

def threshold(r:int)->F:
    if type(r) is not int or r<2:raise ValueError("integer r must be >=2")
    return F(r,r-1)

def possible(r:int,nu:F)->bool:
    return F(nu)>threshold(r)

def verify_witness(r:int,nu:F,A:F,theta:F)->bool:
    return (0<theta<A<1 and A**r<theta and
            F(nu)*(A-theta)>1-theta)

def rational_witness(r:int,nu:F,max_halving:int=80)->tuple[F,F]|None:
    """Construct exact rational A,theta whenever nu exceeds threshold."""
    if not possible(r,nu):return None
    nu=F(nu)
    for k in range(2,max_halving+1):
        A=1-F(1,2**k)
        lo=A**r
        # All theta strictly below upper satisfy the positive approximation gap.
        upper=(nu*A-1)/(nu-1)
        bound=min(A,upper)
        if lo<bound:
            theta=(lo+bound)/2
            if verify_witness(r,nu,A,theta):
                return A,theta
    raise RuntimeError("exact witness search exhausted; increase halving limit")

def elementary_upper_gap_positive(r,A):
    """The exact algebraic inequality A^r-r*A+r-1>0 for rational 0<A<1."""
    if not 0<A<1:raise ValueError("A outside (0,1)")
    return A**r-r*A+r-1>0

def generate(r_min=2,r_max=12):
    tasks=[];gold=[]
    for r in range(r_min,r_max+1):
        c=threshold(r)
        for label,nu in (("below",c-F(1,10)),("equal",c),
                         ("above",c+F(1,10))):
            wid=f"r{r:02d}-{label}"
            yes=possible(r,nu)
            pair=rational_witness(r,nu)
            if yes and (pair is None or not verify_witness(r,nu,*pair)):
                raise AssertionError("witness oracle failed")
            if not yes and pair is not None:raise AssertionError("boundary oracle failed")
            tasks.append({"id":wid,"family":"017","question":
                f"For integer r={r} and nu={nu}, can rational 0<theta<A<1 "
                "satisfy A^r<theta AND nu*(A-theta)>1-theta? "
                "Return only JSON with key possible and boolean value."})
            gold.append({"id":wid,"family":"017","answer_type":"boolean",
                         "answer":yes,"critical_nu":str(c),
                         "constructive_witness":None if pair is None else
                         {"A":str(pair[0]),"theta":str(pair[1])},
                         "oracle":"exact convexity bound + rational search"})
    return {"tasks":tasks,"gold":gold,"scientific_scope":
        "elementary mechanism-transfer inequality, not pi theorem validation"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",default=".")
    p.add_argument("--out-dir",required=True)
    p.add_argument("--max-r",type=int,default=12)
    x=p.parse_args()
    src=(Path(x.root)/SOURCE).read_text()
    if "A^2<\\theta" not in src:raise RuntimeError("family 017 source not found")
    data=generate(r_max=x.max_r)
    folder=Path(x.out_dir);folder.mkdir(parents=True,exist_ok=True)
    (folder/"prompts.jsonl").write_text("".join(json.dumps(t)+"\n" for t in data["tasks"]))
    (folder/"gold.json").write_text(json.dumps({"entries":data["gold"]},indent=2)+"\n")
    print(json.dumps({"task_count":len(data["tasks"]),
                      "witnesses":sum(x["answer"] for x in data["gold"]),
                      "critical_threshold_sample":{"r=2":"2","r=3":"3/2","r=4":"4/3"},
                      "model_evaluations":0},indent=2))

if __name__=="__main__":main()
