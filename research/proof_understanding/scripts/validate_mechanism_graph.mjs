// Validate provenance and graph shape; cannot prove semantic graph correctness.
import {readFileSync} from 'node:fs';
import {resolve,join} from 'node:path';

export function validateMechanismGraph(graph, getSource){
  const errors=[];
  if(graph.graph_type!=='manually_curated_proof_mechanism_hypothesis')errors.push('unexpected graph type');
  const seen=new Set();
  for(const n of graph.nodes ?? []){
    if(seen.has(n.id))errors.push('duplicate node '+n.id);
    seen.add(n.id);
    if(!n.source?.startsWith('preprints/') || n.source.split('/').includes('..')){errors.push('invalid source path '+n.id);continue;}
    let file;
    try{file=getSource(n.source);}catch{errors.push('missing source '+n.id);continue;}
    if(!file.includes('\\label{'+n.tex_label+'}'))errors.push('unresolved source label '+n.id+':'+n.tex_label);
  }
  const edges=new Set();
  for(const e of graph.edges ?? []){
    if(!seen.has(e.source)||!seen.has(e.target))errors.push('dangling edge '+e.source+' -> '+e.target);
    if(!e.relation)errors.push('untyped edge '+e.source+' -> '+e.target);
    const id=e.source+'|'+e.target+'|'+e.relation;
    if(edges.has(id))errors.push('duplicate edge '+id);
    edges.add(id);
  }
  return {ok:errors.length===0,errors,nodes:seen.size,edges:edges.size};
}

if(process.argv[1]&&import.meta.url.endsWith('/'+process.argv[1].split('/').pop())){
  const root=resolve(process.argv[2]??'.');
  const file=join(root,'research/proof_understanding/data/017_mechanism_graph.json');
  const graph=JSON.parse(readFileSync(file,'utf8'));
  const result=validateMechanismGraph(graph,p=>readFileSync(join(root,p),'utf8'));
  console.log(JSON.stringify(result,null,2));if(!result.ok)process.exitCode=1;
}
