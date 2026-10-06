"""Exercise a local review fixture. This does not perform independent review."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from swarm_contract import fingerprint, verify  # noqa: E402

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root / "example.txt").write_text("local fixture\n")
    receipt = {
        "files": ["example.txt"],
        "worker": "builder",
        "tests": "pass",
        "lint": "pass",
        "review": {
            "reviewer": "fixture-reviewer",
            "verdict": "pass",
            "digest": fingerprint(root, ["example.txt"]),
        },
    }
    verify(root, receipt)
    print("Fixture content matches its review digest.")
    (root / "example.txt").write_text("changed after review\n")
    try:
        verify(root, receipt)
    except ValueError as error:
        print(f"Changed content refused: {error}")
