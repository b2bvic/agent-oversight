# Claim evidence

This table maps functional README claims to source lines.

The scaffold is a local candidate. Publication, hosted CI, deployment, and customer use are not claimed.

| Claim | Source evidence |
|---|---|
| Ownership paths stay relative and traversal is refused | [swarm_contract.py:11](swarm_contract.py#L11): `if not value or path.is_absolute() or ".." in path.parts or path == PurePosixPath("."):` |
| Packet identifiers must be unique and ownership cannot be empty | [swarm_contract.py:20](swarm_contract.py#L20): `if not packet["id"] or packet["id"] in identifiers or not packet["paths"]:` |
| Overlapping file or directory ownership is refused | [swarm_contract.py:26](swarm_contract.py#L26): `if path == previous or path in previous.parents or previous in path.parents:` |
| Listed names and content hashes define the SHA-256 fingerprint | [swarm_contract.py:41](swarm_contract.py#L41): `rows.append([name, hashlib.sha256(path.read_bytes()).hexdigest()])` |
| Symlink files and files escaping the root are refused | [swarm_contract.py:39](swarm_contract.py#L39): `if path.is_symlink() or not path.resolve().is_relative_to(root):` |
| Both supplied test and lint status must pass | [swarm_contract.py:47](swarm_contract.py#L47): `if receipt["tests"] != "pass" or receipt["lint"] != "pass":` |
| Review must pass and approve the current listed content digest | [swarm_contract.py:50](swarm_contract.py#L50): `if review["verdict"] != "pass" or review["digest"] != digest:` |
| The reviewer name must differ from the worker name | [swarm_contract.py:52](swarm_contract.py#L52): `if not review["reviewer"] or review["reviewer"] == receipt["worker"]:` |
| The demo checks a temporary fixture then refuses changed content | [examples/demo.py:26](examples/demo.py#L26): `(root / "example.txt").write_text("changed after review\n")` |
| The demo review is synthetic, not independently performed | [examples/demo.py:19](examples/demo.py#L19): `"reviewer": "fixture-reviewer",` |
| Unlisted files and Git metadata are outside the fingerprint | [swarm_contract.py:37](swarm_contract.py#L37): `for name in sorted(files):` |
| Review names and status fields are supplied, not authenticated | [swarm_contract.py:49](swarm_contract.py#L49): `review = receipt["review"]` |
| CLI only reads and checks manifests; it does not dispatch, merge, or create worktrees | [swarm_contract.py:57](swarm_contract.py#L57): `def main():` |
| Runtime imports use only the standard library | [swarm_contract.py:3](swarm_contract.py#L3): `import argparse` |
| Worktree lifecycle and promotion gates are a process template | [docs/contract.md:12](docs/contract.md#L12): `git worktree add -b packet/example ../packet-example BASE_COMMIT` |
| CI contains unittest, Ruff lint, Ruff format, and diff checks | [.github/workflows/ci.yml:14](.github/workflows/ci.yml#L14): `- run: python -m unittest discover -s tests -v` |
