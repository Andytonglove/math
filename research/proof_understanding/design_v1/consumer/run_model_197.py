"""Bounded open-weight consumer of *already frozen* 197 mathematical artifact.

Development smoke test on public deterministic tasks; not a proof-understanding
benchmark or a mathematically verified source theorem.
"""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import argparse,json,re,os,time,sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from generate_197 import CONDITIONS,TRACKS,FREEZE_COMMIT

def parse_mask(response:str)->tuple[int|None,str]:
    value=response.strip()
    kind="raw_json"
    match=re.fullmatch(r"\x60{3}(?:json)?[ \t]*\n(.*?)\n\x60{3}",value,
                       flags=re.DOTALL|re.IGNORECASE)
    if match:
        value=match.group(1).strip()
        kind="fenced_json"
    try:
        data=json.loads(value)
    except (ValueError,TypeError):
        return None,"invalid_response"
    if type(data) is dict and set(data)=={"mask"} and type(data["mask"]) is int and 0<=data["mask"]<64:
        return data["mask"],kind
    return None,"invalid_schema"

def choose(folder:Path,examples_per_track:int)->list[dict]:
    if not 1<=examples_per_track<=12:
        raise ValueError("examples_per_track must be 1..12")
    metadata=json.loads((folder/"metadata.json").read_text())
    if metadata["freeze_commit"]!=FREEZE_COMMIT:
        raise ValueError("frozen source commit mismatch")
    prompts=[json.loads(v) for v in (folder/"prompts.jsonl").read_text().splitlines() if v.strip()]
    gold=json.loads((folder/"gold.json").read_text())["entries"]
    records={(p["id"],p["condition"]):p for p in prompts}
    tasks=[]
    selected=[x for x in gold if x["base_index"] < examples_per_track]
    for g in selected:
        for condition in CONDITIONS:
            p=records[(g["id"],condition)]
            tasks.append({"id":g["id"],"base_index":g["base_index"],
                          "track":g["track"],"condition":condition,
                          "prompt":p["prompt"],"gold":g["answer"]})
    expected=examples_per_track*len(TRACKS)*len(CONDITIONS)
    if len(tasks)!=expected or len({(x["id"],x["condition"]) for x in tasks})!=expected:
        raise AssertionError("paired conditions missing")
    return tasks

def aggregate(rows:list[dict])->dict:
    groups=defaultdict(list)
    for r in rows:
        groups[(r["track"],r["condition"])].append(r)
    result={}
    for (track,condition),items in sorted(groups.items()):
        n=len(items);correct=sum(x["correct"] for x in items)
        valid=sum(x["parsed"] is not None for x in items)
        result[f"{track}/{condition}"]={
            "tasks":n,"correct":correct,"valid":valid,
            "accuracy_all":correct/n,"format_success":valid/n,
            "mean_input_tokens":round(sum(x["input_tokens"] for x in items)/n,2),
            "mean_latency_seconds":round(sum(x["latency_seconds"] for x in items)/n,2),
        }
    return result

def run(args):
    import torch
    from transformers import AutoModelForCausalLM,AutoTokenizer
    torch.set_num_threads(min(4,os.cpu_count() or 2))
    torch.manual_seed(0)
    started=time.monotonic()
    source=Path(args.dataset_dir)
    work=choose(source,args.examples_per_track)
    tok=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,
                torch_dtype=getattr(torch,args.dtype),trust_remote_code=False)
    model.eval()
    rows=[]
    for i,task in enumerate(work,1):
        if time.monotonic()-started>args.max_elapsed_seconds:
            raise RuntimeError("time cap exceeded; no complete paired result")
        begin=time.monotonic()
        messages=[
            {"role":"system","content":"Solve exactly. Return one JSON object with one integer key mask, from 0 to 63. No explanation."},
            {"role":"user","content":task["prompt"]},
        ]
        chat=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
        ids=tok(chat,return_tensors="pt")
        n=int(ids["input_ids"].shape[1])
        if n>args.max_input_tokens:
            raise RuntimeError(f"input tokens exceeded cap for {task['id']}/{task['condition']}: {n}")
        with torch.inference_mode():
            out=model.generate(**ids,do_sample=False,max_new_tokens=args.max_new_tokens,
                               pad_token_id=tok.eos_token_id)
        raw=tok.decode(out[0][ids["input_ids"].shape[1]:],skip_special_tokens=True).strip()
        parsed,format_label=parse_mask(raw)
        item={
            "id":task["id"],"track":task["track"],"base_index":task["base_index"],
            "condition":task["condition"],"gold":task["gold"],"parsed":parsed,
            "correct":parsed==task["gold"],"format":format_label,
            "raw_response":raw,"input_tokens":n,
            "output_tokens":int(out[0].shape[0]-n),
            "latency_seconds":round(time.monotonic()-begin,3),
        }
        rows.append(item)
        print(f"{i}/{len(work)} {task['track']}/{task['condition']} "
              f"correct={item['correct']} format={format_label}",flush=True)
    result={
        "run_type":"bounded_public_development_source_deprived_consumer",
        "frozen_commit":FREEZE_COMMIT,
        "branch_head":os.environ.get("GITHUB_SHA","unknown"),
        "model":args.model,"dtype":args.dtype,
        "revision":getattr(model.config,"_commit_hash",None),
        "examples_per_track":args.examples_per_track,
        "responses":len(rows),"elapsed_seconds":round(time.monotonic()-started,2),
        "summary":aggregate(rows),"records":rows,
        "limitations":[
            "manually produced frozen artifact; model is source-deprived only by prompt context",
            "development seed is public; no independent human task-design blinding",
            "small finite S3 algebra; NOT source's advanced existence theorem",
            "context token lengths unequal; report measured tokens, no causal graph claim",
            "tiny model and small paired sample; no significance claim",
            "no paid API used"
        ]
    }
    output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"model":args.model,"responses":len(rows),
                      "elapsed_seconds":result["elapsed_seconds"],
                      "summary":result["summary"]},indent=2))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--dataset-dir",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--model",default="Qwen/Qwen2.5-1.5B-Instruct")
    p.add_argument("--dtype",choices=["float32","bfloat16"],default="bfloat16")
    p.add_argument("--examples-per-track",type=int,default=2)
    p.add_argument("--max-new-tokens",type=int,default=64)
    p.add_argument("--max-input-tokens",type=int,default=6144)
    p.add_argument("--max-elapsed-seconds",type=int,default=950)
    run(p.parse_args())

if __name__=="__main__":main()
