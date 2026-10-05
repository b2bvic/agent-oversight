import tempfile
import unittest
from pathlib import Path

from swarm_contract import fingerprint, validate_manifest, verify


class ContractTests(unittest.TestCase):
    def test_disjoint_paths(self):
        validate_manifest(
            [{"id": "one", "paths": ["docs"]}, {"id": "two", "paths": ["src/parser.py"]}]
        )

    def test_overlap_traversal_and_duplicate_ids_fail(self):
        for packets in (
            [{"id": "one", "paths": ["docs"]}, {"id": "two", "paths": ["docs/a.md"]}],
            [{"id": "one", "paths": ["../outside"]}],
            [{"id": "one", "paths": ["/outside"]}],
            [{"id": "one", "paths": ["src"]}, {"id": "one", "paths": ["docs"]}],
        ):
            with self.subTest(packets=packets), self.assertRaises(ValueError):
                validate_manifest(packets)

    def test_content_and_review_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "file.txt"
            path.write_text("before")
            receipt = {
                "files": ["file.txt"],
                "worker": "builder",
                "tests": "pass",
                "lint": "pass",
                "review": {
                    "reviewer": "reviewer",
                    "verdict": "pass",
                    "digest": fingerprint(root, ["file.txt"]),
                },
            }
            verify(root, receipt)
            for field in ("tests", "lint"):
                receipt[field] = "fail"
                with self.assertRaises(ValueError):
                    verify(root, receipt)
                receipt[field] = "pass"
            receipt["review"]["reviewer"] = "builder"
            with self.assertRaises(ValueError):
                verify(root, receipt)
            receipt["review"]["reviewer"] = "reviewer"
            receipt["review"]["verdict"] = "revise"
            with self.assertRaises(ValueError):
                verify(root, receipt)
            receipt["review"]["verdict"] = "pass"
            path.write_text("after")
            with self.assertRaises(ValueError):
                verify(root, receipt)

    def test_symlink_escape_and_empty_manifest_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "link").symlink_to("/etc/hosts")
            for files in ([], ["link"], ["../outside"]):
                with self.assertRaises(ValueError):
                    fingerprint(root, files)


if __name__ == "__main__":
    unittest.main()
