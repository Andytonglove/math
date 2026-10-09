"""Exact finite S3 conditional proof-operator sanity check."""
from itertools import permutations
import json
G=tuple(permutations(range(3)))
ix={p:i for i,p in enumerate(G)}
identity=ix[(0,1,2)]
mult=[[ix[tuple(a[b[t]] for t in range(3))] for b in G] for a in G]

def mul(a,b):
    out=0
    for i in range(6):
        if (a//(2**i))%2:
            for j in range(6):
                if (b//(2**j))%2:out^=2**mult[i][j]
    return out

def act(c,x,left=False):
    result=0
    for g in range(6):
        bit=0
        for u in range(6):
            if (c//(2**u))%2:
                h=mult[u][g] if left else mult[g][u]
                bit^=(x//(2**h))%2
        result+=bit*(2**g)
    return result

def audit():
    equations=0;inverse_pairs=0;first_wrong=None
    for a in range(64):
        for b in range(64):
            ab=mul(a,b);ba=mul(b,a)
            if ab==2**identity:
                inverse_pairs+=1
                assert ba==2**identity
            for h in range(6):
                delta=2**h
                assert act(a,act(b,delta))==act(ab,delta)
                actual=act(a,act(b,delta,True),True)
                assert actual==act(ba,delta,True)
                equations+=2
                bad=act(ab,delta,True)
                if first_wrong is None and actual!=bad:
                    first_wrong={"a":a,"b":b,"delta":delta,
                                 "observed":actual,"wrong_orientation":bad}
    for a in range(64):
        for h in range(6):
            assert (act(a,2**h)//(2**identity))%2==(a//(2**h))%2
    assert first_wrong is not None
    return {"pair_count":4096,"operator_basis_equations":equations,
            "coefficient_recovery_equations":384,"invertible_pairs":inverse_pairs,
            "one_sided_only_pairs":0,"wrong_orientation_example":first_wrong,
            "scope":"finite model only; does not prove original paper"}
if __name__=="__main__":print(json.dumps(audit(),indent=2))
