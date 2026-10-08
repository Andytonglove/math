import test from "node:test";
import assert from "node:assert/strict";
import {readBraced,readFamilies,readTraces,makeIndex} from "../scripts/catalog_audit.mjs";
import {readFileSync,existsSync} from "node:fs";
import {resolve,join} from "node:path";
test("nested TeX braces and linked manuscript",()=>{
  const sample="\\cataloguesection{Test}{1}\n\\resultentry{001}{A $x^{2}$ theorem}{Nested $\\frac{a}{b}$}{\\href{preprints/example.pdf}{Proof}}";
  const f=readFamilies(sample);
  assert.equal(f.length,1);assert.equal(f[0].id,"001");
  assert.equal(f[0].manuscript_links[0],"preprints/example.pdf");
  assert.match(f[0].summary,/frac/);
});
test("abridged reasoning summary inventory",()=>{
  const sample="| 017 | [pi](reasoning_traces/pi.pdf) |\n| 102 | [Games](reasoning_traces/games.pdf) |";
  assert.deepEqual(readTraces(sample).map(x=>x.id),["017","102"]);
});
test("live catalogue has unique family IDs and resolvable manuscript references",()=>{
  const root=resolve(".");
  assert.ok(existsSync(join(root,"overview.tex")),"Run from repo root with the sources checked out");
  const rows=readFamilies(readFileSync(join(root,"overview.tex"),"utf8"));
  const traces=readTraces(readFileSync(join(root,"README.md"),"utf8"));
  const scopes=new Set(rows.filter(f=>existsSync(join(root,"lean/docs",f.id+".md"))).map(f=>f.id));
  const index=makeIndex(rows,traces,scopes,"test");
  assert.equal(new Set(rows.map(f=>f.id)).size,rows.length);
  assert.ok(rows.length>=300);
  assert.ok(index.summary.manuscript_links>=600);
  assert.equal(index.summary.manuscript_links,rows.reduce((a,r)=>a+r.manuscript_links.length,0));
  for(const f of index.families)for(const link of f.manuscripts)assert.ok(link.startsWith("preprints/"),link);
  assert.ok(index.families.some(f=>f.id==="017"&&f.lean_scope_doc&&f.reasoning_summary));
});
