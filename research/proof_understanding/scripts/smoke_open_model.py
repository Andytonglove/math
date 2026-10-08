"""CPU-only open-weight model smoke test on proof-mechanism interventions.

No paid API; explicitly small model, deterministic decoding and strict JSON
grading. Model inference is separate from exact math oracle generation.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
import argparse, json, os, re, time

ALLOWED={"017":{"BOTH","ONLY_COLLISION","ONLY_APPROX","NEITHER"},
         "102":{"111","011","001","000"}}
OUTPUT_KEY={"017":"branch_status","102":"truth_bits"}

def load_pairs(root:Path,family:str):
    folder=root/("proof_surgery_017" if family=="017" else "quantifier_surgery_102")
    gold=json.loads((folder/"gold.json").read_text())["entries"]
    items=[json.loads(line) for line in (folder/"prompts.jsonl").read_text().splitlines() if line.strip()]
    return gold,items

def select(root:Path,conditions=("minimal","proof","prose","hypergraph")):
    records=[]
    for family in ("017","102"):
        gold,items=load_pairs(root,family)
        gold_map={r["id"]:r for r in gold}
        chosen={}
        for row in sorted(gold,key=lambda g:g["id"]):
            chosen.setdefault(row["answer"],row["id"])
        if set(chosen)!=ALLOWED[family]:
            raise ValueError("Missing category: "+family)
        prompt_by={(r["id"],r["condition"]):r for r in items}
        for label in sorted(chosen):
            pid=chosen[label]
            for condition in conditions:
                row=prompt_by[(pid,condition)]
                records.append({"family":family,"id":pid,"condition":condition,
                                "prompt":row["prompt"],"gold":gold_map[pid]["answer"]})
    # Keep same mathematical example paired across all 4 conditions.
    return records

def strict_json_reply(text:str,family:str):
    try:
        value=json.loads(text.strip())
    except (ValueError,TypeError):
        return None
    key=OUTPUT_KEY[family]
    if not isinstance(value,dict) or set(value)!={key}:
        return None
    answer=value[key]
    return answer if isinstance(answer,str) and answer in ALLOWED[family] else None

def response_content_and_format(text:str,family:str):
    """Accept raw JSON or one fenced block; do not repair invalid schemas."""
    answer=strict_json_reply(text,family)
    if answer is not None:
        return answer,"raw_json"
    matched=re.fullmatch(r"\x60{3}(?:json)?[ \t]*\n(.*?)\n\x60{3}",
                         text.strip(), flags=re.DOTALL|re.IGNORECASE)
    if matched:
        inner=strict_json_reply(matched.group(1),family)
        if inner is not None:
            return inner,"fenced_json"
    return None,"schema_or_format_invalid"


def summarize(records):
    grouped=defaultdict(list)
    for r in records:
        grouped[(r["family"],r["condition"])].append(r)
    result={}
    for (family,condition),rows in sorted(grouped.items()):
        count=sum(r["correct"] for r in rows)
        valid=sum(r["parsed"] is not None for r in rows)
        strict=sum(r.get("strict_schema_compliant",False) for r in rows)
        result[f"{family}/{condition}"]={
            "correct":count,"total":len(rows),"parsed":valid,"strict_schema":strict,
            "accuracy_all":count/len(rows),"valid_schema_rate_including_fences":valid/len(rows),
            "strict_schema_rate":strict/len(rows),
            "mean_input_tokens":sum(r["input_tokens"] for r in rows)/len(rows),
            "mean_runtime_seconds":sum(r["runtime_seconds"] for r in rows)/len(rows)
        }
    return result

def run(args):
    import torch
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(min(4,os.cpu_count() or 2))
    torch.manual_seed(0)
    started=time.monotonic()
    tokenizer=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=getattr(torch,args.dtype),trust_remote_code=False)
    model.eval()
    data=select(Path(args.input_root))
    results=[]
    for i,task in enumerate(data):
        if time.monotonic()-started>args.wall_seconds:
            raise RuntimeError("Smoke test exceeded allowed wall time; results incomplete")
        start=time.monotonic()
        message=[{"role":"system","content":"Return only the requested valid JSON object."},
                 {"role":"user","content":task["prompt"]}]
        chat=tokenizer.apply_chat_template(message,tokenize=False,add_generation_prompt=True)
        tokens=tokenizer(chat,return_tensors="pt")
        with torch.inference_mode():
            output=model.generate(**tokens,max_new_tokens=args.max_new_tokens,
                                  do_sample=False,pad_token_id=tokenizer.eos_token_id)
        continuation=output[0][tokens["input_ids"].shape[1]:]
        response=tokenizer.decode(continuation,skip_special_tokens=True).strip()
        parsed,format_type=response_content_and_format(response,task["family"])
        results.append({
            "family":task["family"],"id":task["id"],"condition":task["condition"],
            "gold":task["gold"],"parsed":parsed,"correct":parsed==task["gold"],
            "response_format":format_type,
            "strict_schema_compliant":format_type=="raw_json",
            "raw":response[:500],
            "input_tokens":int(tokens["input_ids"].shape[1]),
            "output_tokens":int(continuation.shape[0]),
            "runtime_seconds":round(time.monotonic()-start,3)
        })
        print(f'{i+1}/{len(data)} {task["family"]}/{task["condition"]}: '+
              ("correct" if parsed==task["gold"] else "incorrect/invalid"),
              flush=True)
    result={"model":args.model,"dtype":args.dtype,"run_type":"bounded_public_open_weight_CPU_smoke",
            "head_commit":os.environ.get("GITHUB_SHA","unknown"),
            "inputs":len(data),"completed":len(results),
            "model_download_and_inference_seconds":round(time.monotonic()-started,1),
            "summary":summarize(results),"records":results,
            "caveats":["Tiny model smoke test, not frontier model benchmark",
                       "Four examples per family; no statistical significance",
                       "Contexts not exact-token-matched; input tokens recorded",
                       "Answer correctness not sufficient evidence of proof comprehension",
                       "No paid API was used"]}
    Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"model":args.model,"completed":len(results),
          "seconds":result["model_download_and_inference_seconds"],
          "summary":result["summary"]},indent=2))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input-root",required=True)
    p.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    p.add_argument("--dtype",choices=("float32","bfloat16"),default="float32")
    p.add_argument("--max-new-tokens",type=int,default=48)
    p.add_argument("--wall-seconds",type=int,default=1100)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    run(args)

if __name__=="__main__":main()
