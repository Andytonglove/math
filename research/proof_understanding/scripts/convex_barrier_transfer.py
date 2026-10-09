"""Exact local 017 proof-mechanism transfer; NO claim about irrationality of pi.
All generated examples are public development material, not blind model tests.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json, random

FAMILIES = (
    ("square", ((2,F(1)),)),
    ("cube", ((3,F(1)),)),
    ("mixed24", ((2,F(1,2)), (4,F(1,2)))),
    ("mixed25", ((2,F(2,3)), (5,F(1,3)))),
    ("mixed27", ((2,F(3,4)), (7,F(1,4)))),
    ("mixed35", ((3,F(1,2)), (5,F(1,2)))),
    ("mixed248", ((2,F(1,2)), (4,F(1,4)), (8,F(1,4)))),
)
def value(terms,x):
    if not terms or any(r<2 or w<=0 for r,w in terms) or sum((w for _,w in terms),F(0))!=1:
        raise ValueError("mixture requires positive weights summing to one and degrees >=2")
    return sum((w*F(x)**r for r,w in terms),F(0))

def slope(terms):
    value(terms,F(1,2))
    return sum((r*w for r,w in terms),F(0))

def critical(terms):
    s=slope(terms)
    return s/(s-1)

def certificate(terms):
    """f(x)-s*x+s-1=(1-x)^2*sum(coeff[k]*x**k), all coeff >=0."""
    slope(terms)
    out=[F(0)]*(max(r for r,_ in terms)-1)
    for r,w in terms:
        for k in range(r-1):out[k]+=w*(r-1-k)
    return out

def valid(f,nu,a,t):
    return 0<t<a<1 and f<t and nu*(a-t)>1-t

def witness(terms,nu,limit=120):
    if nu<=critical(terms):return None
    for k in range(2,limit+1):
        a=1-F(1,2**k)
        low=max(F(0),value(terms,a))
        high=min(a,(nu*a-1)/(nu-1))
        if low<high:
            t=(low+high)/2
            if valid(value(terms,a),nu,a,t):return a,t
    raise RuntimeError("witness search limit: raise limit")

def nonconvex(x):
    return x*x-3*x**3*(1-x)**2

def controlled_counterexample():
    a,t,nu=F(3,4),F(31,64),F(39,20)
    assert nonconvex(a)==F(495,1024)
    assert valid(nonconvex(a),nu,a,t)
    assert nu*(a-t)-(1-t)==F(3,1280)
    return {"f":"x^2-3*x^3*(1-x)^2","slope_at_1":"2","nu":str(nu),
            "A":str(a),"theta":str(t),"f(A)":"495/1024","gap":"3/1280"}

def generate(seed=26009):
    rows=[]
    for name,terms in FAMILIES:
        b=critical(terms)
        for d in (-F(1,20),F(0),F(1,20)):
            nu=b+d
            w=witness(terms,nu)
            assert (w is not None)==(nu>b)
            tag=hashlib.sha256(f"{seed}:{name}:{nu}".encode()).hexdigest()[:16]
            rows.append(({"id":tag,"kind":"mixture",
                "question":f"f(x)={'+'.join(str(c)+'*x^'+str(r) for r,c in terms)}; nu={nu}. Are there rational 0<theta<A<1 with f(A)<theta and nu*(A-theta)>1-theta? Give rigorous evidence."},
                {"id":tag,"answer":nu>b,"slope":str(slope(terms)),"threshold":str(b),
                 "certificate":list(map(str,certificate(terms))),"witness":None if w is None else list(map(str,w))}))
    for nu in (F(39,20),F(2)):
        tag=hashlib.sha256(f"{seed}:nonconvex:{nu}".encode()).hexdigest()[:16]
        a,t=F(3,4),F(31,64)
        assert valid(nonconvex(a),nu,a,t)
        rows.append(({"id":tag,"kind":"nonconvex","question":f"f(x)=x^2-3*x^3*(1-x)^2; nu={nu}. Are there rational 0<theta<A<1 with f(A)<theta and nu*(A-theta)>1-theta? Give rigorous evidence."},
                    {"id":tag,"answer":True,"slope":"2","witness":[str(a),str(t)],"gap":str(nu*(a-t)-(1-t))}))
    random.Random(seed).shuffle(rows)
    return {"tasks":[x for x,_ in rows],"gold":[y for _,y in rows],
            "meta":{"seed":seed,"count":len(rows),"positives":sum(int(y["answer"]) for _,y in rows),
                    "scope":"public development examples; no LLM inference"}}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out-dir",required=True)
    p.add_argument("--seed",type=int,default=26009)
    args=p.parse_args();d=generate(args.seed)
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    (out/"questions.jsonl").write_text("".join(json.dumps(t)+"\n" for t in d["tasks"]))
    (out/"gold.json").write_text(json.dumps(d["gold"],indent=2)+"\n")
    (out/"meta.json").write_text(json.dumps(d["meta"],indent=2)+"\n")
    print(json.dumps({**d["meta"],"nonconvex_control":controlled_counterexample()},indent=2))
