# Agent oversight for Claude Code and Codex CLI

Agent-oversight collects response checks, process observations, review receipts, and action controls in one repository.
Use it with teams that run Claude Code and Codex CLI on hosted models.
You choose the components you need and connect them to your own review and approval workflow.

[Project page](https://scalewithsearch.com/code/agent-oversight)

## Install

Clone once. Each component keeps its source, tests, documentation, and license under `components/`.

```bash
git clone https://github.com/b2bvic/agent-oversight.git
cd agent-oversight
```

Use Python 3.11 or newer for the hub fixtures and Python components.
Observer-daemon needs Rust 1.88 or newer and Cargo. Observer-protocol needs Node.js 22 or 24 and npm.
Follow each component's README before you build or install it.
The skills installer targets Claude Code; it does not install a Codex CLI adapter.

## Quick start

Run the synthetic hub fixtures without reading private transcripts:

```bash
python3 -m unittest discover -s tests -v
```

Check a response with observer-daemon using isolated ledger paths:

```bash
cd components/observer-daemon
mkdir -p .demo
sed 's|~/.observer/|./.demo/|g' spec.toml.example > .demo/spec.toml
cargo run --locked -- --config .demo/spec.toml --validate "The file is ready."
```

Inspect the [synthetic transcript examples](examples/README.md).
They cover provider identity collisions, mirrored assistant text, tool correlation, and recorded token fields.
The hub checks fixture contracts. Component tests check their implementations.

## Components

| Component | Purpose | Runtime |
|---|---|---|
| [observer-daemon](#observer-daemon) | Score responses against configured writing rules. | Rust |
| [agent-monitor](#agent-monitor) | Observe local processes and recorded usage. | Python standard library |
| [observer-protocol](#observer-protocol) | Capture Markdown intake, corrections, and local draft status. | Node.js |
| [swarm-contract](#swarm-contract) | Check packet ownership and file-bound review receipts. | Python standard library |
| [effect-gate-template](#effect-gate-template) | Check structured authorization before calling an adapter. | Python standard library |
| [safe-api](#safe-api) | Apply dry-run, scope, and breaker controls to REST writes. | Python standard library |
| [skills](#skills) | Search sessions, select context, and check declared local artifacts. | Claude Code and Python |

Each component command below starts from the repository root.

<a id="observer-daemon"></a>

## observer-daemon

[Source and instructions](components/observer-daemon/README.md)

Score agent responses against configured writing rules.
The daemon reads supported Claude and Codex JSONL records and stores validation results in a local ledger.
A writing score does not verify facts, completed work, or permission to act.

```bash
cd components/observer-daemon
cargo test --locked
```

<a id="agent-monitor"></a>

## agent-monitor

[Source and instructions](components/agent-monitor/README.md)

Inspect local Claude and Codex processes and recorded usage across project and session directories.
Read coverage warnings with the counts. Process status does not prove completion or account billing totals.

```bash
cd components/agent-monitor
python3 -m unittest discover -s tests -v
```

<a id="observer-protocol"></a>

## observer-protocol

[Source and instructions](components/observer-protocol/README.md)

Capture Markdown intake, correction history, and local drafts.
Review heuristic findings against their source. Draft approval changes local status and requires a separate action service.

```bash
cd components/observer-protocol
npm ci
npm test
```

<a id="swarm-contract"></a>

## swarm-contract

[Source and instructions](components/swarm-contract/README.md)

Check disjoint packet ownership and review receipts bound to listed file hashes.
Changed content invalidates a receipt. You must verify review provenance and include every changed file.

```bash
cd components/swarm-contract
python3 -m unittest discover -s tests -v
```

<a id="effect-gate-template"></a>

## effect-gate-template

[Source and instructions](components/effect-gate-template/README.md)

Bind authorization to the action, account, target, and payload before calling a local adapter.
The template records receipts around execution. You must supply trusted authorization and protect direct adapter access.

```bash
cd components/effect-gate-template
python3 -m unittest discover -s tests -v
```

<a id="safe-api"></a>

## safe-api

[Source and instructions](components/safe-api/README.md)

Wrap REST writes with dry-run, scope, duplicate-callback, and circuit-breaker controls.
Configure the destination and allowed endpoints. Execution settings do not prove human approval.

```bash
cd components/safe-api
python3 -m unittest discover -s tests -v
```

<a id="skills"></a>

## skills

[Source and instructions](components/skills/README.md)

Install eight Claude Code skills for session search, context selection, response checks, and local artifact checks.
Use agent-monitor and observer-daemon from this repository for their corresponding helpers.
Install `ledger` from [b2bvic/owned-record](https://github.com/b2bvic/owned-record/tree/main/components/session-ledger), folder `components/session-ledger`.

```bash
cd components/skills
python3 -m unittest discover -s tests -v
```

## Review and action boundaries

The components run independently. You supply coordination, scheduling, and approval integration.
Use [Evaluate the stack](EVALUATION.md) to record inputs, revisions, failures, and missing evidence.
Verify outcomes against output artifacts or the destination before you accept a completion claim.
Enforce authorization where an external action executes.

The examples are synthetic. This repository contains no measured team deployment or comparative model benchmark.
See [owned-record](https://github.com/b2bvic/owned-record) for transcript archives and the owned memory components.

## How this was built

This README was written with model assistance in 2026. The code and tests in this repository are the evidence; read them to judge the tool.
The agent-monitor, observer-daemon, and safe-api component READMEs retain the same model-assistance disclosure.
Component histories are imported with Git subtree merges without squashing.

## License

[MIT](LICENSE). Every component retains its MIT license in its own folder.
