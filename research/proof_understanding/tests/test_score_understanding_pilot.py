import unittest
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from score_understanding_pilot import compare,evaluate,InvalidPrediction


class ScorePilotTests(unittest.TestCase):
    def setUp(self):
        self.gold={"entries":[
          {"id":"a","family":"017","answer_type":"boolean","answer":False},
          {"id":"b","family":"102","answer_type":"fraction","answer":"3/4"},
          {"id":"c","family":"197","answer_type":"integer","answer":5},
          {"id":"d","family":"197","answer_type":"choice","answer":"LR"}
        ]}

    def test_correct_all_with_strict_types(self):
        preds=[{"id":"a","answer":False},{"id":"b","answer":"6/8"},
               {"id":"c","answer":5},{"id":"d","answer":"lr"}]
        result=evaluate(self.gold,preds)
        self.assertEqual(result["summary"]["correct"],4)
        self.assertEqual(result["accuracy_attempted"],1.0)

    def test_missing_abstain_and_wrong_are_separate(self):
        preds=[{"id":"a","answer":None},{"id":"b","answer":"1/3"},
               {"id":"c","answer":True}]
        result=evaluate(self.gold,preds)
        self.assertEqual(result["summary"],
                         {"correct":0,"incorrect":2,"abstain":1,"missing":1})
        self.assertEqual(result["accuracy_attempted"],0.0)
        self.assertEqual(result["coverage"],0.5)

    def test_reject_unknown_or_duplicate_predictions(self):
        with self.assertRaises(InvalidPrediction):
            evaluate(self.gold,[{"id":"outside","answer":False}])
        with self.assertRaises(InvalidPrediction):
            evaluate(self.gold,[{"id":"a","answer":True},{"id":"a","answer":False}])

    def test_exact_answer_is_not_proof_of_understanding(self):
        result=evaluate(self.gold,[{"id":"a","answer":False}])
        self.assertIn("proof understanding",result["not_measured"])


if __name__=='__main__':unittest.main()
