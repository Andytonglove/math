import unittest
from pathlib import Path
import tempfile,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from smoke_open_model import strict_json_reply,select,summarize

class ModelSmokeTests(unittest.TestCase):
    def test_strict_parser(self):
        self.assertEqual(strict_json_reply('{"branch_status":"BOTH"}',"017"),"BOTH")
        self.assertEqual(strict_json_reply('{"truth_bits":"011"}',"102"),"011")
        self.assertIsNone(strict_json_reply("The answer is BOTH","017"))
        self.assertIsNone(strict_json_reply('{"branch_status":"invalid"}',"017"))
        self.assertIsNone(strict_json_reply('{"truth_bits":"011","other":1}',"102"))

    def test_paired_condition_selection(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for fam,folder,answers in [
                ("017","proof_surgery_017",["BOTH","ONLY_COLLISION","ONLY_APPROX","NEITHER"]),
                ("102","quantifier_surgery_102",["111","011","001","000"])
            ]:
                d=root/folder;d.mkdir()
                gold=[{"id":f"{fam}-{i}","answer":a} for i,a in enumerate(answers)]
                (d/"gold.json").write_text(json.dumps({"entries":gold}))
                modes=("minimal","proof","prose","hypergraph")
                rows=[{"id":item["id"],"condition":mode,"prompt":"test"}
                      for item in gold for mode in modes]
                (d/"prompts.jsonl").write_text("".join(json.dumps(x)+"\n" for x in rows))
            x=select(root)
            self.assertEqual(len(x),32)
            self.assertEqual(len(set((r["family"],r["id"]) for r in x)),8)
            self.assertEqual(len({r["condition"] for r in x}),4)

    def test_summary(self):
        rows=[{"family":"017","condition":"minimal","correct":True,
              "parsed":"BOTH","input_tokens":100,"runtime_seconds":2},
              {"family":"017","condition":"minimal","correct":False,
              "parsed":None,"input_tokens":200,"runtime_seconds":4}]
        s=summarize(rows)["017/minimal"]
        self.assertEqual(s["accuracy_all"],.5)
        self.assertEqual(s["valid_json_rate"],.5)
        self.assertEqual(s["mean_input_tokens"],150)

if __name__=="__main__":unittest.main()
