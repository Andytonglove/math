// Validate source-grounded pilot prompts against actual repository files.
// This is provenance testing, NOT a Lean proof checker or benchmark evaluation.
import {readFileSync,existsSync} from "node:fs";
import {resolve,join} from "node:path";
export function validateTasks(root,items){
  const allowed=new Set(["source_grounded","oracle_pending"]);
  const ids=new Set(),errors=[];
  for(const item of items){
    if(ids.has(item.id))errors.push("duplicate task id "+item.id);ids.add(item.id);
    if(!allowed.has(item.status))errors.push("invalid status "+item.id);
    if(item.status==="oracle_pending"&&item.oracle_label!==null)errors.push("unscored task with oracle "+item.id);
    if(!Array.isArray(item.evidence)||item.evidence.length===0)errors.push("missing evidence "+item.id);
    for(const e of (item.evidence??[])){
      if(e.file.startsWith("/")||e.file.split("/").includes("..")){errors.push("unsafe path "+item.id);continue;}
      const path=join(root,e.file);
      if(!existsSync(path)){errors.push("missing source "+path);continue;}
      if(!readFileSync(path,"utf8").includes(e.anchor))errors.push("missing anchor "+item.id+" "+e.anchor);
    }
  }
  return {ok:errors.length===0,errors,total:items.length,source_grounded:items.filter(t=>t.status==="source_grounded").length,oracle_pending:items.filter(t=>t.status==="oracle_pending").length};
}
const isDirectRun=process.argv[1]&&import.meta.url.endsWith("/"+process.argv[1].split("/").pop());
if(isDirectRun){
  const root=resolve(process.argv[2]??".");
  const items=JSON.parse(readFileSync(join(root,"research/proof_understanding/evaluation/pilot_tasks.json"),"utf8"));
  const result=validateTasks(root,items);
  console.log(JSON.stringify(result,null,2));if(!result.ok)process.exitCode=1;
}
