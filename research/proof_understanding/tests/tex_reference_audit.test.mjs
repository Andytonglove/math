import test from 'node:test';
import assert from 'node:assert/strict';
import {stripTexComment,auditReferences} from '../scripts/tex_reference_audit.mjs';

test('comment stripping respects escaped percent',()=>{
 assert.equal(stripTexComment('value \\% marker % invisible'),'value \\% marker ');
 assert.equal(stripTexComment('show \\label{visible} % \\label{hidden}'),'show \\label{visible} ');
});
test('resolves cross-file labels, handles comment and duplicate reporting',()=>{
 const docs={'a.tex':'\\section{Intro}\\label{sec:intro}\nReference \\ref{lem:x}. %\\ref{missing}',
             'b.tex':'\\begin{lemma}\\label{lem:x}\n\\end{lemma}'};
 const g=auditReferences(docs);
 assert.equal(g.summary.labels,2);
 assert.equal(g.summary.reference_occurrences,1);
 assert.equal(g.summary.cross_file_references,1);
 assert.equal(g.summary.duplicate_label_count,0);
 assert.equal(g.summary.unresolved_reference_count,0);
});
test('unresolved refs and duplicate labels are reported, not silently ignored',()=>{
 const g=auditReferences({'x.tex':'\\label{dup} \\ref{nope}', 'y.tex':'\\label{dup}'});
 assert.equal(g.summary.duplicate_label_count,1);
 assert.equal(g.summary.unresolved_reference_count,1);
});
