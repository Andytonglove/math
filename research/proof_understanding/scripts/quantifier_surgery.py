"""Finite quantifier-countermodel interventions sourced from family 102.

Logical surrogate only; does not prove the Unique Games conjecture or any
hardness reduction. Original quantifier shape: forall e exists s forall phi.
"""
from __future__ import annotations
from pathlib import Path
from random import Random
import argparse, hashlib, json

SOURCE = "preprints/The-Unique-Games-Theorem-September-23-2026/build/sections/00-introduction.tex"
CASES = ("uniform","parameter_dependent","input_dependent","missing_input")
MODES = ("minimal","theorem","proof","syntax","hypergraph","prose","distractor")

def truth(table):
    ecount=len(table)
    acount=len(table[0])
    xcount=len(table[0][0])
    strong=any(all(table[e][a][x] for e in range(ecount) for x in range(xcount))
               for a in range(acount))
    original=all(any(all(table[e][a][x] for x in range(xcount))
                     for a in range(acount)) for e in range(ecount))
    weak=all(any(table[e][a][x] for a in range(acount))
             for e in range(ecount) for x in range(xcount))
    if strong and not original or original and not weak:
        raise AssertionError("quantifier monotonicity broken")
    return ''.join('1' if v else '0' for v in (strong,original,weak))

def alternate_truth(table):
    """Independent direct set-intersection calculation of same quantified facts."""
    ecount=len(table);acount=len(table[0]);xcount=len(table[0][0])
    viable=[{a for a in range(acount) if all(table[e][a][x]
                for x in range(xcount))} for e in range(ecount)]
    pairs=[{a for a in range(acount) if table[e][a][x]}
           for e in range(ecount) for x in range(xcount)]
    s=bool(set.intersection(*viable))
    o=all(viable)
    w=all(pairs)
    return ''.join(str(int(v)) for v in (s,o,w))

def generate_case(seed,kind):
    r=Random(seed)
    ecount,acount,xcount=3,3,2
    t=[[[False for x in range(xcount)] for a in range(acount)]
       for e in range(ecount)]
    labels=list(range(acount));r.shuffle(labels)
    if kind=="uniform":
        common=labels[0]
        for e in range(ecount):
            t[e][common]=[True,True]
    elif kind=="parameter_dependent":
        for e in range(ecount):
            t[e][labels[e]]=[True,True]
    elif kind=="input_dependent":
        for e in range(ecount):
            t[e][labels[0]][0]=True
            t[e][labels[1]][1]=True
    elif kind=="missing_input":
        for e in range(ecount):
            for x in range(xcount):
                if (e,x)!=(2,1):
                    t[e][labels[(e+x)%3]][x]=True
    else:raise ValueError("unknown case")
    # Remap parameter order without changing truth, to reduce positional templates.
    eperm=list(range(ecount));r.shuffle(eperm)
    t=[t[e] for e in eperm]
    assert truth(t)==alternate_truth(t)
    return t

def to_table(t):
    return '; '.join(f"e{e}: "+' '.join(
        f"s{a}="+''.join(str(int(v)) for v in row)
        for a,row in enumerate(setting))
        for e,setting in enumerate(t))

TASK=("An unknown Boolean predicate P(e,s,phi) is given by this finite "
      "truth table. For each e row and s column, two digits give P for phi0 "
      "and phi1, respectively. Evaluate these three statements in order: "
      "STRONG: exists s forall e forall phi P; "
      "ORIGINAL: forall e exists s forall phi P; "
      "WEAK: forall e forall phi exists s P. "
      "Return ONLY JSON with key truth_bits and a three-character string "
      "with 1=true, 0=false, in the order STRONG,ORIGINAL,WEAK. ")
CONTEXT={
    "minimal":"",
    "theorem":"The cited AI mathematical manuscript claims a Unique Games hardness result in which an alphabet size can be chosen after fixed approximation errors but before the SAT input.",
    "proof":"Quantifier-level proof scope: the target error pair is fixed first, then one reduction and alphabet are selected, and their completeness/soundness claims must hold for all input formulas. A single universal alphabet independent of all error targets is a logically stronger statement.",
    "syntax":"The source includes theorem thm:ugc and reduction text. The paper labels cannot by themselves resolve the order of existential and universal quantifiers.",
    "hypergraph":"Quantifier structure: FORALL target errors e; EXISTS alphabet/reduction witness s as a function of e; FORALL input formulas phi; predicate P. Swapping EXISTS s before FORALL e demands a single global witness, which is stronger. Moving EXISTS s after FORALL phi is weaker.",
    "prose":"Read the quantifiers in their given order: the witness for s may depend on e, but in the middle statement it must work for every phi. The first statement requires one single s for every e and phi, while the third lets s change separately with both e and phi.",
    "distractor":"In determinant proofs, repeated Taylor degrees create quadratic collision savings; a different AI manuscript uses this to obtain a two-case contradiction."
}

def build(seed=10267,bases=12):
    if not 1<=bases<=1000:raise ValueError("invalid bases")
    r=Random(seed^0xBED)
    task=[];gold=[]
    for i in range(bases):
        for kind in CASES:
            t=generate_case(seed+i*991+len(kind),kind)
            label=truth(t)
            identity=hashlib.sha256(f"102/{seed}/{i}/{kind}".encode()).hexdigest()[:20]
            task.append((identity,to_table(t)))
            gold.append({"id":identity,"family":"102","answer_type":"choice",
                         "answer":label,"case_kind":kind,
                         "oracle":"explicit finite quantifier evaluation and independent set intersections"})
    r.shuffle(task);r.shuffle(gold)
    prompts=[{"id":id,"condition":mode,"family":"102",
              "prompt":"\n\n".join(k for k in (CONTEXT[mode],TASK,rows) if k)}
             for mode in MODES for id,rows in task]
    return {"meta":{"schema_version":"0.1","seed":seed,"bases":bases,"tasks":len(task),
                    "conditions":list(MODES),"source_path":SOURCE,
                    "caveat":"Finite quantifier surrogate, NOT Unique Games proof validation",
                    "model_runs":0},
            "prompts":prompts,"gold":gold}

def write_data(data,folder):
    d=Path(folder);d.mkdir(parents=True,exist_ok=True)
    (d/"metadata.json").write_text(json.dumps(data["meta"],indent=2)+"\n")
    (d/"prompts.jsonl").write_text("".join(json.dumps(x)+"\n" for x in data["prompts"]))
    (d/"gold.json").write_text(json.dumps({"entries":data["gold"]},indent=2)+"\n")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-root",default=".")
    p.add_argument("--seed",type=int,default=10267)
    p.add_argument("--bases",type=int,default=12)
    p.add_argument("--out-dir",required=True)
    a=p.parse_args()
    s=(Path(a.source_root)/SOURCE).read_text()
    if r"\label{thm:ugc}" not in s:raise ValueError("Source label absent")
    data=build(a.seed,a.bases);write_data(data,a.out_dir)
    from collections import Counter
    print(json.dumps({"tasks":len(data["gold"]),"prompts":len(data["prompts"]),
            "distribution":dict(Counter(x["answer"] for x in data["gold"])),
            "model_runs":0},indent=2))

if __name__=="__main__":main()
