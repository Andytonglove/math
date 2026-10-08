import unittest
from pathlib import Path
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_argument_hypergraphs import validate_graph


class HypergraphValidatorTests(unittest.TestCase):
    def test_evidence_and_shape(self):
        with tempfile.TemporaryDirectory() as folder:
            repo=Path(folder)
            (repo/'preprints').mkdir()
            (repo/'preprints/example.tex').write_text(r'\label{test}')
            graph={"representation":"candidate_typed_argument_hypergraph",
                   "family_graphs":[{"family":"001","nodes":[
                       {"id":"A","role":"assumption","source":{"file":"preprints/example.tex","anchor":r"\label{test}"}},
                       {"id":"B","role":"conclusion","source":{"file":"preprints/example.tex","anchor":r"\label{test}"}}],
                   "edges":[{"id":"x","kind":"implies","premises":["A"],"conclusion":"B",
                             "meaning":"test","semantic_review":"pending"}]}]}
            self.assertTrue(validate_graph(graph,repo)["ok"])
            graph["family_graphs"][0]["edges"][0]["conclusion"]="missing"
            self.assertFalse(validate_graph(graph,repo)["ok"])

    def test_no_semantic_verification_is_claimed(self):
        with tempfile.TemporaryDirectory() as folder:
            repo=Path(folder)
            (repo/'preprints').mkdir()
            (repo/'preprints/example.tex').write_text("A")
            graph={"representation":"candidate_typed_argument_hypergraph","family_graphs":[
                 {"family":"001","nodes":[{"id":"A","role":"claim","source":{"file":"preprints/example.tex","anchor":"A"}}],
                 "edges":[{"id":"self","kind":"implies","premises":["A"],"conclusion":"A",
                           "meaning":"test","semantic_review":"verified_by_lean"}]}]}
            self.assertFalse(validate_graph(graph,repo)["ok"])


if __name__=="__main__":unittest.main()
