import json,tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from generate_197 import (
    FREEZE_BLOB_SHA,FREEZE_COMMIT,CONDITIONS,TRACKS,
    load_frozen,build,write_data,exact_direct,independent_oracle,git_blob,mul
)

class Frozen197ConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[5]
        cls.doc=load_frozen(cls.root)

    def test_frozen_blob_and_semantic_coverage(self):
        self.assertEqual(len(FREEZE_COMMIT),40)
        self.assertEqual(len(FREEZE_BLOB_SHA),40)
        self.assertFalse(self.doc["is_automatically_extracted"])
        sem=self.doc["semantic_contract"]
        self.assertTrue(sem["no_silent_repair"])
        self.assertEqual(sem["external_lean_kernel_build"],"not_run")
        self.assertEqual(sem["exact_formal_theorem_correspondence"],"unknown")

    def test_all_small_f2s3_operator_oracles_agree(self):
        for a in range(64):
            for b in range(64):
                for h in range(6):
                    for track in TRACKS:
                        self.assertEqual(exact_direct(a,b,h,track),
                                         independent_oracle(a,b,h,track))

    def test_noncommutativity_is_not_ignored(self):
        self.assertTrue(any(mul(a,b)!=mul(b,a) for a in range(64) for b in range(64)))

    def test_post_freeze_paired_data_and_no_gold_in_prompts(self):
        d=build(self.root,12)
        self.assertEqual(len(d["gold"]),36)
        self.assertEqual(len(d["prompts"]),144)
        self.assertEqual(len({row["id"] for row in d["gold"]}),36)
        self.assertEqual(d["metadata"]["freeze_commit"],FREEZE_COMMIT)
        self.assertGreaterEqual(min(d["oracle_diagnostics"]["unique_masks"].values()),5)
        for row in d["prompts"]:
            self.assertNotIn("answer",row)
            self.assertNotIn("oracle",row)
            self.assertIn("Return JSON only",row["prompt"])
        art=[x for x in d["prompts"] if x["condition"]=="artifact"]
        excerpt=[x for x in d["prompts"] if x["condition"]=="source_excerpt"]
        self.assertTrue(all("Mechanism right_homomorphism" in x["prompt"] for x in art))
        self.assertTrue(all("Mechanism right_homomorphism" not in x["prompt"] for x in excerpt))

    def test_public_reproducibility_and_manifest(self):
        a=build(self.root,4)
        self.assertEqual(a,build(self.root,4))
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)
            write_data(a,p)
            self.assertEqual(len((p/"prompts.jsonl").read_text().splitlines()),48)
            self.assertEqual(json.loads((p/"metadata.json").read_text())["freeze_commit"],FREEZE_COMMIT)

    def test_git_blob_changes_if_tampered(self):
        self.assertNotEqual(git_blob(b"not the artifact"),FREEZE_BLOB_SHA)

    def test_invalid_base_counts(self):
        with self.assertRaises(ValueError):build(self.root,0)
        with self.assertRaises(ValueError):build(self.root,81)

if __name__=="__main__":unittest.main()
