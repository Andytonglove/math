"""Inventory a FULL checked-out Git worktree using stdlib. Not a math verifier."""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
import argparse
import json
import os
from pathlib import Path
import subprocess


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def tracked_paths(root: Path) -> list[str]:
    raw = git(root, "ls-files", "-z")
    return sorted(os.fsdecode(part) for part in raw.split(b"\0") if part)


def build_inventory(root: Path) -> dict:
    root = root.resolve()
    repo_top = Path(os.fsdecode(git(root, "rev-parse", "--show-toplevel").strip())).resolve()
    if repo_top != root:
        raise ValueError("Audit must run from the Git working-tree root")
    shallow = git(root, "rev-parse", "--is-shallow-repository").strip() == b"true"
    config = subprocess.run(["git", "-C", str(root), "config", "--bool", "core.sparseCheckout"],
                            capture_output=True, check=False)
    if config.stdout.strip() == b"true":
        raise ValueError("Sparse checkout detected. Full worktree required")
    paths = tracked_paths(root)
    if not paths:
        raise ValueError("No tracked files found")

    ext_counts, ext_bytes, dir_counts, dir_bytes = Counter(), Counter(), Counter(), Counter()
    absent, largest, total = [], [], 0
    for rel in paths:
        file = root / rel
        if not file.exists() and not file.is_symlink():
            absent.append(rel)
            continue
        n = file.lstat().st_size
        total += n
        suffix = file.suffix.lower() or "[no extension]"
        first = rel.split("/", 1)[0] if "/" in rel else "[root]"
        ext_counts[suffix] += 1
        ext_bytes[suffix] += n
        dir_counts[first] += 1
        dir_bytes[first] += n
        largest.append((n, rel))
    if absent:
        raise ValueError(f"{len(absent)} tracked entries absent in full checkout; first={absent[:5]}")
    return {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git(root, "rev-parse", "HEAD").decode().strip(),
        "git_tree": git(root, "rev-parse", "HEAD^{tree}").decode().strip(),
        "git_is_shallow": shallow,
        "git_is_sparse": False,
        "tracked_files": len(paths),
        "missing_tracked_files": 0,
        "total_tracked_worktree_bytes": total,
        "extension_counts": dict(ext_counts.most_common()),
        "extension_bytes": dict(ext_bytes.most_common()),
        "top_level_counts": dict(dir_counts.most_common()),
        "top_level_bytes": dict(dir_bytes.most_common()),
        "largest_files": [{"bytes": n, "path": p} for n, p in sorted(largest, reverse=True)[:20]],
        "caveats": [
            "This inventories tracked worktree entries, not mathematical correctness.",
            "GitHub hosted runners are ephemeral; output JSON must be uploaded to persist.",
            "This does not build Lean dependencies or verify theorems.",
            "Full worktree checkout and full Git history are separate properties."
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = build_inventory(Path(args.root))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("git_commit","git_is_shallow","git_is_sparse",
                     "tracked_files","missing_tracked_files","total_tracked_worktree_bytes")}, indent=2))


if __name__ == "__main__":
    main()
