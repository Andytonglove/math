// Research pilot - auditable catalogue of source artifacts, NOT truth labels.

import { readFileSync, existsSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve, join, dirname } from "node:path";


export function readBraced(s,start){
  if(s[start]!=="{")throw Error("expected '{' at "+start);
  let depth=1,v="";
  for(let i=start+1;i<s.length;i++){
    const c=s[i];
    if(c==="\\"&&i+1<s.length){v+=s.slice(i,i+2);i++;continue;}
    if(c==="{"){depth++;v+=c;continue;}
    if(c==="}"){depth--;if(depth===0)return {value:v,next:i+1};v+=c;continue;}
    v+=c;
  }
  throw Error("unbalanced TeX braces");
}

export function readFamilies(tex){
  const sections=[];
  let m;
  const sectionPattern=/\\cataloguesection\{([^{}]+)\}\{\d+\}/g;
  while((m=sectionPattern.exec(tex)))sections.push({at:m.index,discipline:m[1]});
  const families=[];
  const resultPattern=/\\resultentry\{/g;
  let section=0;
  while((m=resultPattern.exec(tex))){
    let position=m.index+"\\resultentry".length;
    const fields=[];
    for(let j=0;j<4;j++){
      const parsed=readBraced(tex,position);
      fields.push(parsed.value);
      position=parsed.next;
    }
    while(section+1<sections.length&&sections[section+1].at<m.index)section++;
    const links=[...fields[3].matchAll(/\\href\{([^}]+)\}/g)].map(z=>z[1]);
    families.push({id:fields[0],discipline:sections[section]?.discipline??"unknown",title:fields[1],summary:fields[2],manuscript_links:links});
    resultPattern.lastIndex=position;
  }
  return families;
}

export function readTraces(readme){
  return [...readme.matchAll(/^\|\s*(\d{3})\s*\|\s*\[[^\]]+\]\(([^)]+)\)/gm)]
    .map(m=>({id:m[1],path:m[2]}));
}

export function makeIndex(families,traces,scopeIds,commit){
  const traceMap=new Map(traces.map(t=>[t.id,t.path]));
  const seen=new Set();
  const items=families.map(f=>{
    if(seen.has(f.id))throw Error("duplicate family id "+f.id);
    seen.add(f.id);
    return {
      id:f.id,
      discipline:f.discipline,
      title:f.title,
      manuscripts:f.manuscript_links.map(u=>u.replace(/^https:\/\/github\.com\/openai\/math\/blob\/main\//,"")),
      lean_scope_doc:scopeIds.has(f.id)?`lean/docs/${f.id}.md`:null,
      reasoning_summary:traceMap.get(f.id)??null
    };
  });
  const histogram={};
  for(const f of items)histogram[f.discipline]=(histogram[f.discipline]??0)+1;
  return {
    schema_version:"0.1",
    provenance:{repository:"Andytonglove/math",base_commit:commit,inputs:["overview.tex","README.md","lean/docs/"]},
    caveats:[
      "A scope note is metadata, not independent validation of a Lean theorem.",
      "A listed manuscript is not independently certified correct by this index.",
      "A reasoning summary is abridged and is not a complete model discovery trace."
    ],
    summary:{
      families:items.length,
      disciplines:Object.keys(histogram).length,
      manuscript_links:items.reduce((a,f)=>a+f.manuscripts.length,0),
      families_with_scope_note:items.filter(f=>f.lean_scope_doc).length,
      families_with_reasoning_summary:items.filter(f=>f.reasoning_summary).length,
      by_discipline:histogram
    },
    families:items
  };
}

const isDirectRun = process.argv[1] && import.meta.url.endsWith("/"+process.argv[1].split("/").pop());

if (isDirectRun) {
  const root=resolve(process.argv[2]??".");
  const output=resolve(process.argv[3]??join(root,"research/proof_understanding/data/catalog_index.json"));
  const commit=process.argv[4]??"unrecorded";
  const families=readFamilies(readFileSync(join(root,"overview.tex"),"utf8"));
  const traces=readTraces(readFileSync(join(root,"README.md"),"utf8"));
  const scopes=new Set(families.filter(f=>existsSync(join(root,"lean/docs",f.id+".md"))).map(f=>f.id));
  const manifest=makeIndex(families,traces,scopes,commit);
  mkdirSync(dirname(output),{recursive:true});
  writeFileSync(output,JSON.stringify(manifest,null,2)+"\n");
  console.log(JSON.stringify(manifest.summary,null,2));
}
