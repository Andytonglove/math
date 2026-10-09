"""Post-freeze development tasks for source-deprived understanding of family 197.

The source-derived artifact was committed first. Its Git blob ID is fixed.
This is a public deterministic developer pilot, not a blind benchmark.
"""
from __future__ import annotations
from collections import Counter
from hashlib import sha1,sha256
from itertools import permutations
from pathlib import Path
from random import Random
import argparse,json,sys

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts"))
from s3_operator_transfer import G,mul,act

FREEZE_COMMIT="04fef27eed6f3a10e529f728f3f478cb459f0821"
FREEZE_BLOB_SHA="a603b3877de63eaf90f336867fdd6f5b70467209"
ARTIFACT="research/proof_understanding/design_v1/frozen/197_operator_artifact_v1.json"
SOURCE=("preprints/A-Counterexample-to-Kaplanskys-Direct-Finiteness-Conjecture-in-"
        "Characteristic-Two-September-23-2026/build/sections/06-cellular-automata.tex")
TRACKS=("right","left","mixed")
CONDITIONS=("background","summary","artifact","source_excerpt")
PERMS=",".join("".join(map(str,p)) for p in G)

def git_blob(data:bytes)->str:
    return sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()

def load_frozen(root:Path)->dict:
    raw=(root/ARTIFACT).read_bytes()
    if git_blob(raw)!=FREEZE_BLOB_SHA:
        raise ValueError("Frozen artifact content differs from committed Git blob")
    doc=json.loads(raw)
    if doc.get("artifact_id")!="frozen-197-operator-mechanism-v1":
        raise ValueError("incorrect frozen artifact ID")
    sem=doc["semantic_contract"]
    if sem.get("external_lean_kernel_build")!="not_run" or \
            not str(sem.get("exact_formal_theorem_correspondence","")).startswith("unknown"):
        raise ValueError("unsupported semantic certification in artifact")
    if not sem.get("no_silent_repair"):
        raise ValueError("no-silent-repair policy missing")
    return doc

def artifact_text(doc:dict)->str:
    sem=doc["semantic_contract"]
    parts=["Evidence-carrying mathematical-understanding artifact (manually prepared).",
           sem["mathematical_objects"],sem["multiplication"],
           sem["right_neighbor_definition"],sem["left_neighbor_definition"]]
    for m in doc["mechanisms"]:
        parts.append("Mechanism "+m["id"]+": "+m["conclusion"]+
                     ". Conditions: "+"; ".join(m["premises"])+". Proof: "+m["proof"])
    unknown=[o["claim"] for o in doc["proof_obligations"] if o["state"].startswith("unresolved")]
    parts.append("Unverified/unresolved: "+"; ".join(unknown))
    parts.extend(doc["limits"])
    return "\n".join(parts)

def manuscript_excerpt(root:Path)->str:
    source=(root/SOURCE).read_text(encoding="utf8")
    lo=source.index(r"\subsection{The group algebra acting on all configurations}")
    hi=source.index(r"\subsection{Transport to a group of type",lo)
    return source[lo:hi]

SUMMARY=(
    "Group algebra elements are finitely supported, so their actions are "
    "defined on all configurations. Right-neighbor action T_c uses x(g*u) "
    "and composition T_c T_d = T_(c*d). Left-neighbor action S_c uses "
    "x(u*g) and composition S_c S_d = S_(d*c). The reversed order matters "
    "when the group is noncommutative. Coefficients can be recovered with "
    "point-indicator configurations. If a*b=1 then T_b is injective, and "
    "the image is the fixed set of T_(b*a); non-surjectivity additionally "
    "needs b*a!=1. This is conditional, not a verified exotic example."
)

COMMON=(
    "Use F_2[S_3], the group algebra over the field of 2 elements. "
    "The six permutations of {0,1,2} have indices 0..5 in lexicographic "
    "one-line notation: "+PERMS+". Multiplication p*q means function "
    "composition (p*q)(i)=p(q(i)). Each six-bit integer mask c has "
    "coefficient 1 at permutation index i iff bit i is 1. A configuration "
    "x also has six bits, with bit g giving x(g). delta_h has only bit h=1. "
    "Define T_c(x)(g)=XOR over indices u with c[u]=1 of x(g*u). "
    "Define S_c(x)(g)=XOR over indices u with c[u]=1 of x(u*g). "
    "All sums are over F_2. Your answer is a 6-bit output mask as an "
    'integer 0..63. Return JSON only: {"mask":N}.'
)

def exact_direct(a:int,b:int,h:int,track:str)->int:
    x=1<<h
    if track=="right":
        return act(a,act(b,x,left=False),left=False)
    if track=="left":
        return act(a,act(b,x,left=True),left=True)
    if track=="mixed":
        return act(a,act(b,x,left=True),left=False)
    raise ValueError("unknown operator track")

def independent_oracle(a:int,b:int,h:int,track:str)->int:
    """Second implementation with fresh tuple permutations, no imported act/mul."""
    perms=tuple(permutations((0,1,2)))
    ix={p:i for i,p in enumerate(perms)}
    def compose(p,q):
        return tuple(p[q[t]] for t in range(3))
    def basis_action(mask,vector,left):
        out=0
        for gi,g in enumerate(perms):
            bit=0
            for ui,u in enumerate(perms):
                if (mask>>ui)&1:
                    target=compose(u,g) if left else compose(g,u)
                    bit^=(vector>>ix[target])&1
            out|=bit<<gi
        return out
    def basis_product(x,y):
        out=0
        for ui,u in enumerate(perms):
            if (x>>ui)&1:
                for vi,v in enumerate(perms):
                    if (y>>vi)&1:
                        out^=1<<ix[compose(u,v)]
        return out
    delta=1<<h
    if track=="right":
        return basis_action(basis_product(a,b),delta,False)
    if track=="left":
        return basis_action(basis_product(b,a),delta,True)
    if track=="mixed":
        return basis_action(b,basis_action(a,delta,False),True)
    raise ValueError("unknown operator track")

def build(root:Path,bases:int=12)->dict:
    if not 1<=bases<=80:
        raise ValueError("basis count outside 1..80")
    artifact=load_frozen(root)
    source_text=manuscript_excerpt(root)
    conditions={
        "background":"",
        "summary":SUMMARY,
        "artifact":artifact_text(artifact),
        "source_excerpt":source_text,
    }
    rng=Random(int(FREEZE_COMMIT[:16],16))
    candidates=[];seen=set()
    for _ in range(200000):
        a,b,h=rng.randrange(1,64),rng.randrange(1,64),rng.randrange(6)
        if (a,b,h) in seen or mul(a,b)==mul(b,a):
            continue
        values=[exact_direct(a,b,h,t) for t in TRACKS]
        if 0 in values or len(set(values))<2:
            continue
        seen.add((a,b,h));candidates.append((a,b,h))
        if len(candidates)==bases:
            break
    if len(candidates)!=bases:
        raise RuntimeError("insufficient noncommutative examples")
    records=[];gold=[]
    commands={
        "right":"Compute (T_a composed with T_b)(delta_h).",
        "left":"Compute (S_a composed with S_b)(delta_h).",
        "mixed":"Compute (T_a composed with S_b)(delta_h).",
    }
    for group,(a,b,h) in enumerate(candidates):
        for track in TRACKS:
            answer=exact_direct(a,b,h,track)
            if answer!=independent_oracle(a,b,h,track):
                raise AssertionError("two exact independent oracles disagree")
            digest=sha256(f"{FREEZE_COMMIT}/{group}/{a}/{b}/{h}/{track}".encode()).hexdigest()[:20]
            question=f"a mask={a}, b mask={b}, h={h}. "+commands[track]
            gold.append({"id":digest,"family":"197","answer_type":"integer",
                         "answer":answer,"base_index":group,"track":track,
                         "oracle":"finite F2[S3]: basis action versus algebra product order"})
            for condition in CONDITIONS:
                records.append({"id":digest,"family":"197",
                                "condition":condition,"track":track,
                                "base_index":group,"prompt":
                                "\n\n".join(v for v in (conditions[condition],COMMON,question) if v)})
    return {
        "metadata":{
            "experiment":"197 chronologically frozen artifact consumer",
            "freeze_commit":FREEZE_COMMIT,"frozen_blob_sha":FREEZE_BLOB_SHA,
            "seed":"public first 64 bits of freeze commit",
            "artifact_producer":"manual, not automated",
            "models_evaluated_at_generation":0,
            "advanced_source_theorem_independently_verified":False,
            "data_splitting":"public development; not hidden",
            "base_cases":bases,"tasks":len(gold),"prompt_records":len(records),
            "conditions":list(CONDITIONS),
        },
        "prompts":records,"gold":gold,
        "oracle_diagnostics":{
            "counts":dict(Counter(x["track"] for x in gold)),
            "unique_masks":{t:len(set(g["answer"] for g in gold if g["track"]==t)) for t in TRACKS},
            "verified_two_way_checks":len(gold)
        },
    }

def write_data(data:dict,folder:Path):
    folder.mkdir(parents=True,exist_ok=True)
    for name,content in (
        ("metadata.json",data["metadata"]),
        ("gold.json",{"entries":data["gold"]}),
        ("oracle_diagnostics.json",data["oracle_diagnostics"])):
        (folder/name).write_text(json.dumps(content,indent=2)+"\n")
    (folder/"prompts.jsonl").write_text("".join(
        json.dumps(v,ensure_ascii=False)+"\n" for v in data["prompts"]))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo-root",default=".")
    parser.add_argument("--bases",type=int,default=12)
    parser.add_argument("--output-dir",required=True)
    args=parser.parse_args()
    data=build(Path(args.repo_root),args.bases)
    write_data(data,Path(args.output_dir))
    print(json.dumps({"metadata":data["metadata"],
                      "oracle_diagnostics":data["oracle_diagnostics"]},indent=2))

if __name__=="__main__":
    main()
