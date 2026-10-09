import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from analyze_model_197 import analyze,CONDS

class AnalysisTests(unittest.TestCase):
    def make_result(self):
        records=[]
        for idx in range(3):
            gold=idx
            for cond in CONDS:
                ans=(gold if cond in ("artifact","source_excerpt") else
                     gold+1 if idx!=0 else gold)
                records.append({
                    "id":f"task{idx}","base_index":idx//2,"track":"right",
                    "condition":cond,"gold":gold,"parsed":ans,"correct":ans==gold,
                    "input_tokens":100 if cond=="background" else 200,
                    "latency_seconds":1.0,
                })
        return {"model":"fixture","frozen_commit":"freeze123","records":records}

    def test_correct_pairs_and_cluster_reporting(self):
        a=analyze(self.make_result())
        self.assertEqual(a["evaluated_distinct_tasks"],3)
        self.assertEqual(a["base_case_clusters"],2)
        self.assertEqual(a["per_condition"]["artifact"]["correct"],3)
        self.assertEqual(a["per_condition"]["background"]["correct"],1)
        self.assertEqual(a["paired_differences"]["artifact_vs_background"]["wins"],2)
        self.assertEqual(a["paired_differences"]["artifact_vs_background"]["losses"],0)
        self.assertEqual(a["p_values"],"NOT_ESTIMATED_small_correlated_and_unmatched_pilot")

    def test_reject_missing_condition(self):
        r=self.make_result()
        r["records"].pop()
        with self.assertRaisesRegex(ValueError,"incomplete paired"):
            analyze(r)

    def test_reject_duplicate_condition(self):
        r=self.make_result()
        r["records"].append(dict(r["records"][0]))
        with self.assertRaisesRegex(ValueError,"duplicate"):
            analyze(r)

    def test_tracks_format_and_token_cost_without_replacing_gold(self):
        r=self.make_result()
        r["records"][1]["parsed"]=None
        a=analyze(r)
        self.assertEqual(a["per_condition"]["summary"]["schema_valid"],2)
        self.assertEqual(a["per_condition"]["artifact"]["mean_input_tokens"],200)
        self.assertFalse(a["source_advanced_theorem_validated"])

if __name__=="__main__":unittest.main()
