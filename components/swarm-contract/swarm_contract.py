"""Validate disjoint packet paths and content-bound review receipts."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def relative_path(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or path == PurePosixPath("."):
        raise ValueError("packet paths must stay inside the worktree")
    return path


def validate_manifest(packets):
    paths = []
    identifiers = set()
    for packet in packets:
        if not packet["id"] or packet["id"] in identifiers or not packet["paths"]:
            raise ValueError("each packet needs a unique id and at least one path")
        identifiers.add(packet["id"])
        for value in packet["paths"]:
            path = relative_path(value)
            for previous in paths:
                if path == previous or path in previous.parents or previous in path.parents:
                    raise ValueError("packet paths overlap")
            paths.append(path)


def fingerprint(root, files):
    """Hash an explicit file manifest, including each relative path."""
    root = root.resolve()
    if not files or len(files) != len(set(files)):
        raise ValueError("provide a nonempty unique file manifest")
    rows = []
    for name in sorted(files):
        path = root / relative_path(name)
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError("file escapes the worktree")
        rows.append([name, hashlib.sha256(path.read_bytes()).hexdigest()])
    return hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()


def verify(root, receipt):
    digest = fingerprint(root, receipt["files"])
    if receipt["tests"] != "pass" or receipt["lint"] != "pass":
        raise ValueError("test and lint evidence must pass")
    review = receipt["review"]
    if review["verdict"] != "pass" or review["digest"] != digest:
        raise ValueError("review does not approve current content")
    if not review["reviewer"] or review["reviewer"] == receipt["worker"]:
        raise ValueError("reviewer must differ from worker")
    return digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    try:
        validate_manifest(json.loads(args.manifest.read_text()))
        digest = None
        if args.receipt:
            digest = verify(args.root, json.loads(args.receipt.read_text()))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(json.dumps({"manifest": "pass", "reviewed_digest": digest}))


if __name__ == "__main__":
    main()
