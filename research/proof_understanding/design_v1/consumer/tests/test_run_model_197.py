import json,tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run_model_197 import parse_mask,choose,aggregate
from generate_197 import build,write_data,FREEZE_COMMIT

class FrozenReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[5]

    def test_strict_and_fenced_json(self):
        self.assertEqual(parse_mask('{"mask":25}'),(25,"raw_json"))
        fence=chr(96)*3
        self.assertEqual(parse_mask(fence+'json\n{"mask":12}\n'+fence),(12,"fenced_json"))
        for bad in ('{"mask":true}','{"mask":64}','{"mask":"12"}',
                    '{"mask":4,"explanation":"extra"}','the answer is 12'):
            self.assertIsNone(parse_mask(bad)[0])

    def test_paired_selection(self):
        data=build(self.root,12)
        with tempfile.TemporaryDirectory() as d:
            write_data(data,Path(d))
            sample=choose(Path(d),examples_per_track=2)
            self.assertEqual(len(sample),24)
            self.assertEqual(len({x["id"] for x in sample}),6)
            self.assertEqual({x["condition"] for x in sample},
                             {"background","summary","artifact","source_excerpt"})
            self.assertTrue(all(0<=x["gold"]<64 for x in sample))
            with self.assertRaises(ValueError):choose(Path(d),13)

    def test_aggregation_preserves_format_failures_and_costs(self):
        rows=[
            {"track":"right","condition":"summary","correct":True,"parsed":8,
             "input_tokens":100,"latency_seconds":1.0},
            {"track":"right","condition":"summary","correct":False,"parsed":None,
             "input_tokens":300,"latency_seconds":3.0},
        ]
        x=aggregate(rows)["right/summary"]
        self.assertEqual(x["tasks"],2)
        self.assertEqual(x["correct"],1)
        self.assertEqual(x["valid"],1)
        self.assertEqual(x["mean_input_tokens"],200)
        self.assertEqual(x["mean_latency_seconds"],2)

    def test_selection_refuses_wrong_freeze_commit(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"metadata.json").write_text(json.dumps({"freeze_commit":"bad"}))
            with self.assertRaises(ValueError):choose(root,2)

if __name__=="__main__":unittest.main()
