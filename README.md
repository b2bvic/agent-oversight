# Human-in-the-loop approval gate: effect-gate-template

effect-gate-template checks structured authorization at a local capability adapter for teams that use hosted agents.
It blocks requests without matching authorization before the adapter runs.

This is a local publication candidate extracted from a single-operator workflow. It shows patterns a team can adopt.

## Install

Use Python 3.11 or later. The runtime uses the Python standard library.
From the directory that contains this candidate, run these commands.

```sh
cd effect-gate-template
python3 --version
```

## Quick start

Run the offline fixture.

```sh
python3 examples/demo.py
```

The fixture refuses a request without authorization, then runs an in-memory stub with matching synthetic authorization.
It prints receipts to stdout. It sends no message and calls no external service.

## How it works

The request names an action, account, target, and payload.
The request digest binds authorization to those exact values.
Unknown actions and configured hard blocks fail before execution.
Preview returns the request without calling the adapter.
The gate records authorization before execution and records completion or adapter failure afterward.
If the authorization receipt fails, the adapter does not run.

Use [docs/governance.md](docs/governance.md) to define capability ownership and authorization provenance.

Source evidence appears in [CLAIMS.md](CLAIMS.md).

## Limits

The caller must supply trusted authorization. An `approved_by` string does not authenticate a human.
Do not expose authorization construction to a model or accept model-authored approval fields.
This template supplies no signatures, expiry, replay prevention, idempotency, or durable receipt storage.
The gate protects adapters invoked through `execute`. Direct calls to another adapter can bypass it.
An effect may succeed before its completion receipt fails. Reconcile that outcome before retrying.
The fixture covers a local stub. It does not prove production integrations, team deployment, or compliance.

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

- [safe-api](https://github.com/b2bvic/safe-api)
- [agent-oversight](https://github.com/b2bvic/agent-oversight)
- [owned-record](https://github.com/b2bvic/owned-record)
