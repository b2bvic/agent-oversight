# Multi-agent orchestration receipts: swarm-contract

swarm-contract checks packet ownership paths and file-bound review receipts for teams that use hosted coding agents.
It detects overlapping packet paths and rejects reviews when listed file content changes.

This is a local publication candidate extracted from a single-operator workflow. It shows patterns a team can adopt.

## Install

Use Python 3.11 or later. The runtime uses the Python standard library.
From the directory that contains this candidate, run these commands.

```sh
cd swarm-contract
python3 --version
```

## Quick start

Validate the disjoint packet manifest.

```sh
python3 swarm_contract.py examples/packets.json
```

Run the content-change fixture.

```sh
python3 examples/demo.py
```

The fixture creates a temporary file, checks its digest, changes its content, and confirms review rejection.
The fixture supplies a synthetic review. It does not perform independent review.

## How it works

The manifest assigns relative ownership paths to packets.
The checker rejects duplicate packet identifiers, empty ownership, traversal, and overlapping directory or file paths.
The receipt lists files, worker identity, test status, lint status, and review identity, verdict, and digest.
The fingerprint covers sorted file names and their SHA-256 content hashes.
Review must pass, match current content, and name a reviewer different from the worker.
Test and lint status must both be `pass`.

Use the process template in [docs/contract.md](docs/contract.md) for Git worktree setup and promotion gates.

Source evidence appears in [CLAIMS.md](CLAIMS.md).

## Limits

The checker validates supplied evidence. It cannot authenticate the reviewer or verify that tests ran.
A trusted coordinator must build the complete changed-file manifest and verify review provenance.
Unlisted files and Git commit metadata are outside the digest.
The checker does not create worktrees, dispatch agents, merge code, or enforce operating-system isolation.
The manifest states ownership. It does not monitor worker writes.
This example does not prove team deployment or successful production promotion.

## Verify

```sh
python3 -m unittest discover -s tests -v
python3 -m pip install ruff==0.16.10
ruff check .
ruff format --check .
git diff --check
```

The CI workflow contains these checks. Hosted CI has not run for this local candidate.

## Related repositories

- [agent-oversight](https://github.com/b2bvic/agent-oversight)
- [session-ledger](https://github.com/b2bvic/session-ledger)
- [safe-api](https://github.com/b2bvic/safe-api)
