import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from paper_claim_graph import audit, graph_from_lines, strip_comments, expand_sources


class PaperClaimGraphTests(unittest.TestCase):
    def test_comments_and_escaped_percent(self):
        self.assertEqual(strip_comments(r'price \% label % ignore'),'price \\% label ')
        self.assertEqual(strip_comments(r'\label{abc} % \ref{invisible}'),r'\label{abc} ')

    def test_nested_inputs_and_provenance(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'sections').mkdir()
            (root/'main.tex').write_text(r'\section{Intro}\label{sec:intro}'+'\n'+r'\input{sections/child}'+'\n')
            (root/'sections/child.tex').write_text(r'\begin{lemma}\label{lem:key}'+'\n'+r'\end{lemma}'+'\n'+r'See \ref{sec:intro}.'+'\n')
            g=audit(root,'main.tex')
            self.assertEqual(g['summary']['source_files'],2)
            self.assertEqual(g['summary']['labels'],2)
            self.assertEqual(g['labels']['lem:key']['role'],'statement')
            self.assertEqual(g['summary']['cross_file_references'],1)
            self.assertEqual(g['summary']['missing_reference_targets'],0)


    def test_project_root_relative_input_from_section(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'sections').mkdir();(root/'figures').mkdir()
            (root/'main.tex').write_text(r'\\input{sections/chapter}')
            (root/'sections/chapter.tex').write_text(r'\\input{figures/overview}')
            (root/'figures/overview.tex').write_text(r'\\begin{figure}\\label{fig:overview}\\end{figure}')
            result=audit(root,'main.tex')
            self.assertEqual(result['summary']['source_files'],3)
            self.assertIn('fig:overview',result['labels'])

    def test_ambiguous_root_and_child_include_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'sections').mkdir()
            (root/'main.tex').write_text(r'\\input{sections/chapter}')
            (root/'sections/chapter.tex').write_text(r'\\input{other}')
            (root/'other.tex').write_text('root')
            (root/'sections/other.tex').write_text('child')
            with self.assertRaisesRegex(ValueError,'Ambiguous'):
                audit(root,'main.tex')

    def test_cycle_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'main.tex').write_text(r'\input{main}')
            with self.assertRaisesRegex(ValueError,'cycle'):expand_sources(root,'main.tex')

    def test_missing_and_duplicate_reported(self):
        g=graph_from_lines([('a.tex',1,r'\label{dup} \ref{lost}'),
                            ('b.tex',1,r'\label{dup}')])
        self.assertEqual(g['summary']['missing_reference_targets'],1)
        self.assertEqual(g['summary']['duplicate_labels'],1)

    def test_no_spurious_dependency_claim(self):
        g=graph_from_lines([('a.tex',1,r'\section{Case}'),
                            ('a.tex',2,r'\begin{proof} \ref{lem:x} \end{proof}'),
                            ('b.tex',1,r'\begin{lemma}\label{lem:x}\end{lemma}')])
        self.assertTrue(g['not_a_proof_dependency_graph'])
        self.assertEqual(g['references'][0]['context_environments'],['proof'])


if __name__=='__main__':unittest.main()
