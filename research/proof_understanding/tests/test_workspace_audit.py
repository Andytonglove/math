"""Integration tests run offline with temporary synthetic Git repositories."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from workspace_audit import build_inventory, tracked_paths


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def fixture():
    raise RuntimeError("Use the isolated context in each test")


class WorkspaceAuditTests(unittest.TestCase):
    def make_repo(self, root):
        git(root, "init", "-q")
        (root / "preprints").mkdir()
        (root / "lean").mkdir()
        (root / "preprints" / "paper.pdf").write_bytes(b"%PDF-1.7\n")
        (root / "lean" / "proof.lean").write_text("theorem toy : True := trivial\n")
        (root / "README.md").write_text("research\n")
        git(root, "add", ".")
        git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
            "commit", "-qm", "test")

    def test_full_checkout_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            result = build_inventory(root)
            self.assertEqual(result["tracked_files"], 3)
            self.assertEqual(result["top_level_counts"]["preprints"], 1)
            self.assertEqual(result["missing_tracked_files"], 0)
            self.assertEqual(len(result["git_commit"]), 40)
            self.assertEqual(tracked_paths(root),
                             ["README.md", "lean/proof.lean", "preprints/paper.pdf"])

    def test_reject_sparse(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            git(root, "config", "core.sparseCheckout", "true")
            with self.assertRaisesRegex(ValueError, "Sparse checkout"):
                build_inventory(root)

    def test_reject_incomplete_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            (root / "README.md").unlink()
            with self.assertRaisesRegex(ValueError, "tracked entries absent"):
                build_inventory(root)


if __name__ == "__main__":
    unittest.main()
