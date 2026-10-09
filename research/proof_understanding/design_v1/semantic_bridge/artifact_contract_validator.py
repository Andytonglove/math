"""Check schema and conservative verification claims in development artifacts.

Syntactic/schema gate ONLY. Does not certify mathematical semantics.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

ALLOWED={"independently_local_proved","unknown","source_reported",
         "checked_formal_statement_scope","conditional_unverified"}

def validate(data):
    errors=[]
    if data.get("frozen_for_independent_evaluation") is not False:
        errors.append("development artifacts must not be falsely frozen")
    found=set()
    for a in data.get("artifacts",[]):
        name=a.get("artifact_id")
        if name in found: errors.append("duplicate artifact id "+str(name))
        found.add(name)
        if not a.get("no_silent_repair"):
            errors.append("no_silent_repair must be true: "+str(name))
        if a.get("formal_contract",{}).get("lean_kernel_compilation")=="passed" and a["formal_contract"].get("statement_correspondence")=="unknown":
            # Lean validity is permitted even if semantic alignment is unknown:
            # do NOT report an error for this combination.
            pass
        if a.get("formal_contract",{}).get("statement_correspondence") in ("confirmed","verified") and a.get("formal_contract",{}).get("lean_kernel_compilation")=="not_run_by_this_project":
            errors.append("unreviewed formal correspondence falsely promoted: "+str(name))
        if a.get("source_contract",{}).get("advanced_theorem_status") not in (
                "not_independently_reviewed","source's existence construction not independently reviewed"):
            errors.append("advanced source incorrectly certified: "+str(name))
        if not a.get("obligations"):
            errors.append("missing obligations: "+str(name))
        if not a.get("excluded_conclusions"):
            errors.append("missing limits/exclusions: "+str(name))
        for o in a.get("obligations",[]):
            if o.get("state") not in ALLOWED:
                errors.append("unrecognized obligation status: "+str(o.get("id")))
        if not a.get("source",{}).get("path") or not a.get("source",{}).get("anchor"):
            errors.append("missing provenance for "+str(name))
        if not a.get("formal_contract",{}).get("statement_correspondence"):
            errors.append("missing statement correspondence for "+str(name))
    return {
        "ok":not errors,
        "development_artifacts_checked":len(data.get("artifacts",[])),
        "meaning_of_pass":"schema and no-false-certification invariants only",
        "complete_semantic_verification":False,
        "errors":errors
    }

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--input",required=True)
    x=p.parse_args()
    r=validate(json.loads(Path(x.input).read_text(encoding="utf-8")))
    print(json.dumps(r,indent=2))
    if not r["ok"]:raise SystemExit(1)
