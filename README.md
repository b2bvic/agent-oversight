# agent-oversight

Check agent work from outside the agent. Seven small tools score Claude Code and Codex CLI responses against your writing rules, show which sessions run and what they consumed, bind code review receipts to file hashes, and hold REST writes in dry-run until a human turns execution on.
Each tool runs on its own, keeps its tests in its folder, and reports what it checked instead of claiming the task is done.

[Project page](https://scalewithsearch.com/code/agent-oversight)

A hosted-model agent can write fluent text about work it did not finish, and a second agent that reviews the first inherits the same blind spots.
These components came from one operator running several Claude Code and Codex sessions at once. They check evidence: the response text, the process table, the file digest, the HTTP payload.

## Quick start

Clone once. Python 3.11 or newer runs the hub fixtures and five components. observer-daemon needs Rust 1.88 or newer; observer-protocol needs Node.js 22 or 24.

```bash
git clone https://github.com/b2bvic/agent-oversight.git
cd agent-oversight
python3 -m unittest discover -s tests -v
```

The four hub tests read the synthetic transcripts in `examples/` and contain no personal session data.

Score one response with observer-daemon, with ledger paths kept inside the checkout:

```bash
cd components/observer-daemon
mkdir -p .demo
sed 's|~/.observer/|./.demo/|g' spec.toml.example > .demo/spec.toml
cargo run --locked -- --config .demo/spec.toml --validate "The file is ready."
```

Expected output: `Class: generic`, `Score: 100/100`, `No violations.`

Refuse an unauthorized action with effect-gate-template, offline:

```bash
cd components/effect-gate-template
python3 examples/demo.py
```

The fixture prints a `denied` receipt for a request without authorization, then `authorized` and `completed` receipts for a matching synthetic authorization against an in-memory stub.

## Components

| Component | Purpose | Runtime |
|---|---|---|
| [observer-daemon](#observer-daemon) | Score responses against configured writing rules. | Rust |
| [agent-monitor](#agent-monitor) | Report local Claude and Codex processes and recorded token usage. | Python standard library |
| [observer-protocol](#observer-protocol) | Capture Markdown intake, corrections, and local draft status. | Node.js |
| [swarm-contract](#swarm-contract) | Check packet ownership and file-bound review receipts. | Python standard library |
| [effect-gate-template](#effect-gate-template) | Check structured authorization before an adapter runs. | Python standard library |
| [safe-api](#safe-api) | Apply dry-run, scope, and breaker controls to REST writes. | Python standard library |
| [skills](#skills) | Eight Claude Code skills for session search, context selection, and artifact checks. | Claude Code and Python |

Every command below starts from the repository root.

<a id="observer-daemon"></a>

## observer-daemon

Scores a response against the writing rules in a TOML spec and records violations in a JSONL ledger.
In daemon mode it watches Claude Code and Codex JSONL transcript paths you configure.
A writing score does not verify facts, completed work, or permission to act. [Source and instructions](components/observer-daemon/README.md)

```bash
cd components/observer-daemon
cargo test --locked
```

<a id="agent-monitor"></a>

## agent-monitor

Lists running Claude and Codex processes and sums recorded token usage from local project and session directories, with coverage warnings when a source is missing.
A live process does not prove task completion, and recorded tokens are not a billing total. [Source and instructions](components/agent-monitor/README.md)

```bash
cd components/agent-monitor
python3 -m unittest discover -s tests -v
```

<a id="observer-protocol"></a>

## observer-protocol

Stores intake as Markdown, corrections as JSONL, and loop drafts as YAML, and runs heuristic pattern analysis over recent files.
Approving a draft changes its local status. Publishing needs a separate action service that checks authorization. [Source and instructions](components/observer-protocol/README.md)

```bash
cd components/observer-protocol
npm ci
npm test
```

<a id="swarm-contract"></a>

## swarm-contract

Validates a packet manifest for disjoint file ownership and checks review receipts whose fingerprint covers SHA-256 hashes of the listed files.
Changed content invalidates the receipt. The reviewer must differ from the worker, and test and lint status must both be `pass`.
The checker cannot authenticate the reviewer or confirm that tests ran. [Source and instructions](components/swarm-contract/README.md)

```bash
cd components/swarm-contract
python3 -m unittest discover -s tests -v
```

<a id="effect-gate-template"></a>

## effect-gate-template

Binds authorization to a digest of the action, account, target, and payload, and refuses to call the adapter when the digest does not match.
You supply trusted authorization. An `approved_by` string does not authenticate a human, and direct adapter calls bypass the gate. [Source and instructions](components/effect-gate-template/README.md)

```bash
cd components/effect-gate-template
python3 -m unittest discover -s tests -v
```

<a id="safe-api"></a>

## safe-api

Wraps `post`, `put`, `patch`, and `delete` with an endpoint allowlist, an optional duplicate callback, a failure and rate circuit breaker, and JSONL logs.
`execute=False` records the intended write and sends nothing. `execute=True` sends one urllib request per call, and that setting is not evidence of human approval. [Source and instructions](components/safe-api/README.md)

```bash
cd components/safe-api
python3 -m unittest discover -s tests -v
```

<a id="skills"></a>

## skills

Installs eight Claude Code skills: `/ledger-search`, `/agent-status`, `/gate-check`, `/completion-check`, `/vault-route`, `/vault-context`, `/vault-log`, and `/vault-handoff`.
`install.py` copies the folders into `~/.claude/skills/` and refuses to overwrite an existing name. Skill text guides the model; it enforces nothing.
`/ledger-search` needs `ledger` from [owned-record](https://github.com/b2bvic/owned-record/tree/main/components/session-ledger). [Source and instructions](components/skills/README.md)

```bash
cd components/skills
python3 -m unittest discover -s tests -v
```

## What these tools do not do

- No component reads your private transcripts until you configure its paths. The shipped fixtures and demos are synthetic.
- No component authorizes an action. Scores, receipts, and dry-run logs are evidence for your approval step, which runs in the executing service.
- The repository holds no measured team deployment or model benchmark. [EVALUATION.md](EVALUATION.md) describes how to record one.
- The skills installer targets Claude Code. There is no Codex CLI hook adapter.

For transcript archives and owned context files, see [owned-record](https://github.com/b2bvic/owned-record).

## How this was built

This README was written with model assistance in 2026. The code and tests in this repository are the evidence; read them to judge the tool.
The agent-monitor, observer-daemon, and safe-api component READMEs carry the same disclosure.
Component histories were imported with Git subtree merges without squashing.

## License

[MIT](LICENSE). Every component keeps its MIT license in its own folder.
