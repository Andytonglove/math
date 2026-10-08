// Structural LaTeX reference graph; not a theorem dependency graph.
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {resolve, join, dirname} from 'node:path';

export const CASE017_SOURCE_FILES = [
  'preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/main.tex',
  'preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections/interpolation.tex',
  'preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections/determinant.tex',
  'preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections/conclusion.tex',
  'preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/sections/series.tex',
];

export function stripTexComment(line){
  for(let i=0;i<line.length;i++){
    if(line[i]!=='%')continue;
    let slashes=0;
    for(let j=i-1;j>=0&&line[j]==='\\';j--)slashes++;
    if(slashes%2===0)return line.slice(0,i);
  }
  return line;
}

export function auditReferences(files){
  const labels=new Map();
  const refs=[];
  const duplicateLabels=[];
  const fileCounts={};
  for(const [file,source] of Object.entries(files)){
    let section='(preamble)';
    let localCount=0;
    for(const [i,raw] of source.split('\n').entries()){
      const line=stripTexComment(raw);
      for(const hit of line.matchAll(/\\(?:section|subsection)\*?\{([^}]*)\}/g))section=hit[1];
      for(const hit of line.matchAll(/\\label\{([^}]+)\}/g)){
        if(labels.has(hit[1]))duplicateLabels.push({label:hit[1],old:labels.get(hit[1]),new:{file,line:i+1}});
        labels.set(hit[1],{file,line:i+1,section});
      }
      for(const hit of line.matchAll(/\\(?:eqref|ref|autoref|cref|Cref)\{([^}]+)\}/g)){
        refs.push({file,line:i+1,section,target:hit[1]});
        localCount++;
      }
    }
    fileCounts[file]=localCount;
  }
  const unresolvedReferences=refs.filter(r=>!labels.has(r.target));
  const counts=new Map();
  for(const r of refs)counts.set(r.target,(counts.get(r.target)||0)+1);
  const topReferenced=[...counts].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,25)
    .map(([label,count])=>({label,count,declared_at:labels.get(label)??null}));
  return {
    graph_type:'syntactic_latex_reference_graph',
    warning:'References to labels are NOT theorem dependencies or evidence of explanatory importance.',
    summary:{source_files:Object.keys(files).length,labels:labels.size,reference_occurrences:refs.length,
      duplicate_label_count:duplicateLabels.length,unresolved_reference_count:unresolvedReferences.length,
      cross_file_references:refs.filter(r=>labels.has(r.target)&&labels.get(r.target).file!==r.file).length,
      references_by_file:fileCounts},
    labels:Object.fromEntries(labels), references:refs,
    duplicate_labels:duplicateLabels,unresolved_references:unresolvedReferences,
    top_referenced:topReferenced
  };
}

export function auditCase017(root){
  const files={};
  for(const path of CASE017_SOURCE_FILES)files[path]=readFileSync(join(root,path),'utf8');
  return auditReferences(files);
}

if(process.argv[1] && import.meta.url.endsWith('/'+process.argv[1].split('/').pop())){
  const root=resolve(process.argv[2]??'.');
  const output=resolve(process.argv[3]??join(root,'research/proof_understanding/data/017_tex_reference_graph.json'));
  const result=auditCase017(root);
  mkdirSync(dirname(output),{recursive:true});
  writeFileSync(output,JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result.summary,null,2));
  if(result.summary.duplicate_label_count||result.summary.unresolved_reference_count)process.exitCode=1;
}
