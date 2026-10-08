"""Grade structured answers to pilot probes against independent exact oracles.

Not a metric for human understanding, and exact-answer agreement alone is not
proof that a model understood the original machine-generated mathematical proof.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import argparse
import json

class InvalidPrediction(ValueError):
    pass

def compare(kind, pred, expected):
    if pred is None:
        return "abstain"
    if kind == "boolean":
        return "correct" if type(pred) is bool and pred is expected else "incorrect"
    if kind == "integer":
        return "correct" if type(pred) is int and pred == expected else "incorrect"
    if kind == "fraction":
        try:
            val=Fraction(pred)
            return "correct" if val == Fraction(expected) else "incorrect"
        except (ValueError,ZeroDivisionError,TypeError):
            return "incorrect"
    if kind == "choice":
        return "correct" if type(pred) is str and pred.upper().strip() == expected else "incorrect"
    raise InvalidPrediction("Unknown answer type: "+kind)

def evaluate(gold:dict, predictions:list[dict]) -> dict:
    gold_by_id={x["id"]:x for x in gold["entries"]}
    if len(gold_by_id)!=len(gold["entries"]):raise ValueError("duplicate gold IDs")
    prediction_by_id={}
    for p in predictions:
        pid=p.get("id")
        if pid not in gold_by_id:raise InvalidPrediction("unknown task "+str(pid))
        if pid in prediction_by_id:raise InvalidPrediction("duplicate prediction "+str(pid))
        prediction_by_id[pid]=p
    rows=[]
    for ident,t in gold_by_id.items():
        p=prediction_by_id.get(ident)
        if p is None:
            status="missing"
        else:
            status=compare(t["answer_type"],p.get("answer"),t["answer"])
        rows.append({"id":ident,"family":t["family"],"status":status})
    counts=lambda items:{status:sum(r["status"]==status for r in items)
                          for status in ("correct","incorrect","abstain","missing")}
    total=counts(rows)
    attempted=total["correct"]+total["incorrect"]
    by_family={}
    for family in sorted(set(r["family"] for r in rows)):
        subset=[r for r in rows if r["family"]==family]
        by_family[family]={"tasks":len(subset),**counts(subset)}
    return {
        "evaluation_mode":"exact_structured_answer_only",
        "not_measured":"explanation validity, originality, human comprehension, proof understanding",
        "tasks":len(rows),"submitted":len(prediction_by_id),
        "coverage":attempted/len(rows) if rows else None,
        "accuracy_attempted":total["correct"]/attempted if attempted else None,
        "exact_correct_over_total":total["correct"]/len(rows) if rows else None,
        "summary":total,"by_family":by_family,"rows":rows,
    }

def read_jsonl(path):
    items=[]
    for i,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
        if not line.strip():continue
        try:items.append(json.loads(line))
        except json.JSONDecodeError as e:raise ValueError(f"bad JSONL line {i}") from e
    return items

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--gold",required=True)
    ap.add_argument("--predictions",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    gold=json.loads(Path(args.gold).read_text(encoding="utf-8"))
    result=evaluate(gold,read_jsonl(args.predictions))
    Path(args.output).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("tasks","submitted","coverage","accuracy_attempted","summary")},indent=2))

if __name__=="__main__":main()
