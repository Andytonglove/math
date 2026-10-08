import test from 'node:test';
import assert from 'node:assert/strict';
import {validateMechanismGraph} from '../scripts/validate_mechanism_graph.mjs';

const good={
  graph_type:'manually_curated_proof_mechanism_hypothesis',
  nodes:[{id:'A',source:'preprints/test.tex',tex_label:'a'},{id:'B',source:'preprints/test.tex',tex_label:'b'}],
  edges:[{source:'A',target:'B',relation:'supports'}]
};

test('curated graph source labels and typed edges are resolvable',()=>{
 const r=validateMechanismGraph(good,()=> '\\label{a} \\label{b}');
 assert.equal(r.ok,true);assert.equal(r.nodes,2);assert.equal(r.edges,1);
});
test('missing anchor, duplicate IDs and dangling edge rejected',()=>{
 const bad=structuredClone(good);
 bad.nodes.push({id:'A',source:'preprints/test.tex',tex_label:'unknown'});
 bad.edges.push({source:'A',target:'NO',relation:''});
 const r=validateMechanismGraph(bad,()=> '\\label{a} \\label{b}');
 assert.equal(r.ok,false);assert.ok(r.errors.length>=3);
});
