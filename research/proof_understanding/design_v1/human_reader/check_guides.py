"""Fail-closed *provenance* checks for two human reading guides.

These checks validate references, local scopes and disclosures, NOT the
mathematical validity of the whole research proof or actual human learning.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

REQUIRED_HEADINGS = (
    "## 数学问题", "## 核心机制", "## 自己核查",
    "## 条件改变后", "## 不应相信什么",
)
REQUIRED_DISCLOSURES = (
    "人工编写的开发版理解材料",
    "原始论文主定理没有在本项目得到独立验证",
)
REQUIRED_197 = frozenset({
    "right_homomorphism", "faithful", "split_injective",
    "image", "non_surjective",
})
REQUIRED_017 = frozenset({"O1", "O2", "O3"})


def references(text: str, kind: str) -> set[str]:
    return set(re.findall(r"<!--\s*" + re.escape(kind) + r":\s*([A-Za-z0-9_]+)\s*-->", text))


def check_contracts(producer: dict, barrier: dict, guide197: str,
                    guide017: str, source_bytes: bytes | None = None) -> dict:
    """Check that readable prose has known anchors and explicit uncertainty.

    Absence of an original TeX file is allowed in a lightweight local clone;
    production CI MUST supply source_bytes for the original SHA-256 check.
    """
    if producer.get("gate", {}).get("status") != "PASSED_SCOPED":
        raise ValueError("197 producer gate not passed; withhold guide")
    claim_ids = {x["id"] for x in producer.get("claims", [])}
    if not REQUIRED_197 <= claim_ids:
        raise ValueError("197 source contract missing required conditional claims")
    if not producer.get("source", {}).get("required_anchors"):
        raise ValueError("197 source anchors missing")
    if not producer.get("unresolved"):
        raise ValueError("197 unknowns silently removed")
    if source_bytes is not None:
        actual_hash = hashlib.sha256(source_bytes).hexdigest()
        if actual_hash != producer["source"]["sha256"]:
            raise ValueError("197 original TeX hash mismatch")

    obligations = {x["id"]: x["status"] for x in barrier.get("proof_obligations", [])}
    if not REQUIRED_017 <= obligations.keys():
        raise ValueError("017 independent local obligations missing")
    if any(obligations[k] != "independently_derived" for k in REQUIRED_017):
        raise ValueError("017 local derivation lost its evidence tier")
    if obligations.get("O4") != "unverified_out_of_scope":
        raise ValueError("017 source high-level claim should remain unknown")
    if not barrier.get("boundaries") or not barrier.get("unknowns"):
        raise ValueError("017 boundaries or unknowns absent")
    if barrier.get("artifact_provenance", {}).get("source_advanced_theorem_verified") is not False:
        raise ValueError("017 source status is not explicitly unverified")

    for family, content in (("197", guide197), ("017", guide017)):
        for heading in REQUIRED_HEADINGS:
            if heading not in content:
                raise ValueError(f"{family} guide missing section: {heading}")
        for disclosure in REQUIRED_DISCLOSURES:
            if disclosure not in content:
                raise ValueError(f"{family} guide missing disclosure: {disclosure}")
    ref197 = references(guide197, "proof-ref")
    ref017 = references(guide017, "obligation-ref")
    if not REQUIRED_197 <= ref197:
        raise ValueError("197 guide omits source-backed reasoning links")
    if not ref197 <= claim_ids:
        raise ValueError("197 guide references an absent producer claim")
    if not REQUIRED_017 <= ref017:
        raise ValueError("017 guide omits independently derived steps")
    if not ref017 <= {k for k, state in obligations.items() if state == "independently_derived"}:
        raise ValueError("017 guide promotes an unverified obligation")
    if references(guide017, "proof-ref") or references(guide197, "obligation-ref"):
        raise ValueError("cross-family reference marker confused")
    return {
        "scope": "provenance+disclosure+source-SHA when available; NOT semantic/human validation",
        "source197_sha_checked": source_bytes is not None,
        "source197_claim_refs": sorted(ref197),
        "source017_obligation_refs": sorted(ref017),
        "high_level_source_theorems_verified": False,
        "human_outcomes_measured": False,
    }


def inspect_repo(repo: Path, require_original: bool = False) -> dict:
    root = repo / "research/proof_understanding/design_v1"
    producer = json.loads((root / "producer/data/produced_197_2026-10-10.json").read_text(encoding="utf-8"))
    barrier = json.loads((root / "artifacts/017_rational_barrier_dev_v01.json").read_text(encoding="utf-8"))
    reader = root / "human_reader"
    guide197 = (reader / "197_READER_GUIDE.md").read_text(encoding="utf-8")
    guide017 = (reader / "017_READER_GUIDE.md").read_text(encoding="utf-8")
    source = repo / producer["source"]["path"]
    if require_original and not source.is_file():
        raise ValueError("required original 197 TeX missing in CI checkout")
    return check_contracts(producer, barrier, guide197, guide017,
                           source_bytes=source.read_bytes() if source.is_file() else None)


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    cli.add_argument("--require-original", action="store_true")
    args = cli.parse_args()
    print(json.dumps(inspect_repo(args.repo_root, args.require_original),
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
