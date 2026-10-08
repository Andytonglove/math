from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1] / 'scripts'))
from lean_import_audit import parse_imports, inspect_import_closure, module_file


class LeanImportTests(unittest.TestCase):
    def test_parse_multiple_imports_and_dedup(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'x.lean'
            f.write_text('import OAI.Core OAI.Tools\nimport OAI.Core -- repeated\nimport Mathlib\nnamespace X\n')
            self.assertEqual(parse_imports(f),['OAI.Core','OAI.Tools','Mathlib'])

    def test_closure_tracks_only_inrepo_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for mod,source in {
                'OAI.Main':'import OAI.Core OAI.Tools\nnamespace A\n',
                'OAI.Core':'import Mathlib\n',
                'OAI.Tools':'import OAI.Core\n'
            }.items():
                f=module_file(root,mod)
                f.parent.mkdir(parents=True,exist_ok=True)
                f.write_text(source)
            r=inspect_import_closure(root,'OAI.Main')
            self.assertEqual(r['internal_import_closure_modules'],3)
            self.assertEqual(r['internal_import_edges'],3)
            self.assertEqual(r['seed_direct_imports'],['OAI.Core','OAI.Tools'])
            self.assertIn('Mathlib',r['external_imports_sample'])

    def test_missing_root_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                inspect_import_closure(Path(tmp),'OAI.DoesNotExist')

    def test_limit_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            f=module_file(root,'OAI.Main')
            f.parent.mkdir(parents=True)
            f.write_text('import OAI.Core\n')
            g=module_file(root,'OAI.Core')
            g.write_text('import Mathlib\n')
            with self.assertRaisesRegex(RuntimeError,'limit'):
                inspect_import_closure(root,'OAI.Main',limit=1)


if __name__=='__main__':
    unittest.main()
