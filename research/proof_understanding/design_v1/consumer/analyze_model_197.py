"""Conservative paired analysis of source-deprived 197 consumer pilot.

Development set contains correlated operator tasks. Do not report p-values or
causal source/graph advantages from this small, unmatched-input pilot.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from pathlib import Path
import argparse,json

CONDS=("background","summary","artifact","source_excerpt")
PAIRS=("background","summary","source_excerpt")

def analyze(result:dict)->dict:
    rows=result["records"]
    pairs=defaultdict(dict)
    for r in rows:
        key=(r["id"],r["base_index"],r["track"])
        if r["condition"] in pairs[key]:
            raise ValueError("duplicate (task,condition) in raw model result")
        pairs[key][r["condition"]]=r
    if not pairs:
        raise ValueError("no model result rows")
    if any(set(x)!=set(CONDS) for x in pairs.values()):
        raise ValueError("incomplete paired experiment")
    clusters=set(k[1] for k in pairs)
    delta={}
    for comparator in PAIRS:
        wins=losses=ties=0
        for labels in pairs.values():
            art=bool(labels["artifact"]["correct"])
            other=bool(labels[comparator]["correct"])
            if art and not other:wins+=1
            elif other and not art:losses+=1
            else:ties+=1
        n=len(pairs)
        delta["artifact_vs_"+comparator]={
            "wins":wins,"losses":losses,"ties":ties,
            "paired_exact_accuracy_difference":(wins-losses)/n,
            "unit_of_analysis":"paired task, but clustering by base case required"
        }
    per_condition={}
    for c in CONDS:
        curr=[r for r in rows if r["condition"]==c]
        parsed=[r["parsed"] for r in curr if r["parsed"] is not None]
        per_condition[c]={
            "tasks":len(curr),"correct":sum(bool(r["correct"]) for r in curr),
            "schema_valid":len(parsed),
            "constant_parsed_mask":parsed[0] if parsed and len(set(parsed))==1 else None,
            "mean_input_tokens":sum(r["input_tokens"] for r in curr)/len(curr),
            "mean_model_seconds":sum(r["latency_seconds"] for r in curr)/len(curr),
        }
    return {
        "model":result["model"],
        "freeze_commit":result["frozen_commit"],
        "evaluated_distinct_tasks":len(pairs),
        "base_case_clusters":len(clusters),
        "conditions":list(CONDS),
        "per_condition":per_condition,
        "paired_differences":delta,
        "p_values":"NOT_ESTIMATED_small_correlated_and_unmatched_pilot",
        "causal_conclusion":"NOT_ESTABLISHED",
        "source_advanced_theorem_validated":False,
        "notes":[
            "Task designer knew frozen artifact mathematics; development data is public.",
            "All prompts include definitions, so background can solve tasks independently.",
            "The frozen artifact is manually authored and source-deprived only in model prompt.",
            "Token budgets and added mathematical information are not perfectly matched.",
            "Original Kaplansky main theorem remains unverified by this local experiment.",
        ]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--output",required=True)
    x=p.parse_args()
    data=json.loads(Path(x.input).read_text())
    result=analyze(data)
    Path(x.output).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__":main()
