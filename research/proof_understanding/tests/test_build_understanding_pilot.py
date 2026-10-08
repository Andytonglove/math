import tempfile
import json
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_understanding_pilot import build


class UnderstandingPilotTests(unittest.TestCase):
    def test_actual_source_anchors_if_available(self):
        root=Path(__file__).resolve().parents[3]
        expected=root/'preprints/The-Unique-Games-Theorem-September-23-2026/build/sections/00-introduction.tex'
        if not expected.exists():
            self.skipTest('source-based integration requires all three papers in checkout')
        result=build(root)
        self.assertEqual(result['prompts']['task_count'],9)
        self.assertEqual(result['prompts']['families'],['017','102','197'])
        self.assertEqual(len(result['gold']['entries']),9)
        self.assertFalse(any('answer' in t for t in result['prompts']['entries']))
        self.assertTrue(all('answer' in t for t in result['gold']['entries']))
        ids={t['id'] for t in result['prompts']['entries']}
        self.assertEqual(len(ids),9)

    def test_fails_on_missing_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(FileNotFoundError):
                build(Path(temp))


if __name__=='__main__':unittest.main()
