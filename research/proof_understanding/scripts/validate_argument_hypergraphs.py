"""Provenance validation of typed candidate argument hypergraphs (NOT logic proof).
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

KINDS={"implies","all_of","contradicts","case_split"}
ROLES={"assumption","construction","witness","bound","transformation","case","parameter","contradiction","conclusion",
       "consequence","constraint","completeness","soundness","certificate","defect_certificate","restriction","claim"}

def validate_graph(graph:dict,repo:Path)->dict:
    errors=[];tot_nodes=0;tot_edges=0;allids=set()
    if graph.get('representation') != 'candidate_typed_argument_hypergraph':
        errors.append('incorrect representation type')
    families=set()
    for g in graph.get('family_graphs',[]):
        fid=g.get('family')
        if fid in families:errors.append(f'duplicate family {fid}')
        families.add(fid)
        ids=set()
        for n in g.get('nodes',[]):
            name=n.get('id')
            if name in ids or name in allids:errors.append(f'duplicate node {name}')
            ids.add(name);allids.add(name);tot_nodes+=1
            if n.get('role') not in ROLES:errors.append(f'unsupported node role {name}')
            info=n.get('source',{});path=info.get('file','');anchor=info.get('anchor','')
            if not path.startswith('preprints/') or '..' in path.split('/'):
                errors.append(f'invalid provenance path for {name}');continue
            try:contents=(repo/path).read_text(encoding='utf-8')
            except OSError:
                errors.append(f'missing source for {name}: {path}');continue
            if not anchor or anchor not in contents:errors.append(f'missing source anchor {name}: {anchor}')
        edgeids=set()
        for e in g.get('edges',[]):
            eid=e.get('id');tot_edges+=1
            if eid in edgeids:errors.append(f'duplicate edge {eid}')
            edgeids.add(eid)
            if e.get('kind') not in KINDS:errors.append(f'invalid edge kind {eid}')
            if e.get('kind') == 'all_of' and len(e.get('premises',[]))<2:
                errors.append(f'all_of needs multiple premises {eid}')
            if not e.get('premises'):errors.append(f'empty premise edge {eid}')
            for p in e.get('premises',[]):
                if p not in ids:errors.append(f'dangling edge premise {eid}:{p}')
            if e.get('conclusion') not in ids:errors.append(f'dangling edge target {eid}')
            if not e.get('meaning'):errors.append(f'missing semantic note {eid}')
            if e.get('semantic_review') != 'pending':
                errors.append(f'unverified review status promoted prematurely {eid}')
    return {"ok":not errors,"families":len(families),"nodes":tot_nodes,"edges":tot_edges,
            "source_checks":"source anchors only; no semantic verification","errors":errors}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',default='.')
    p.add_argument('--input',required=True)
    args=p.parse_args()
    result=validate_graph(json.loads(Path(args.input).read_text()),Path(args.root).resolve())
    print(json.dumps(result,indent=2))
    if not result["ok"]:raise SystemExit(1)


if __name__=='__main__':main()
