# Claude Code and Codex process monitor: agent-monitor

Agent-monitor reports local Claude Code and Codex CLI processes and recorded usage for operators who use hosted models.
It helps you inspect running sessions without treating process counts as completed work.

[Project page](https://scalewithsearch.com/code/agent-monitor)

## Install

Use Python 3.11 or newer and Git. The runtime uses the Python standard library.

```bash
git clone https://github.com/b2bvic/agent-monitor.git
cd agent-monitor
```

For a source installation after review:

```bash
mkdir -p "$HOME/.local/bin"
install -m 755 agent-monitor "$HOME/.local/bin/agent-monitor"
```

## Quick start

Generate an AI agent monitoring report from synthetic fixtures:

```bash
python3 ./agent-monitor \
  --claude-root tests/fixtures/multiple_projects/claude/projects \
  --codex-root tests/fixtures/multiple_projects/codex \
  --ps-file tests/fixtures/processes/empty.jsonl \
  --now 2026-01-15T13:00:00Z \
  --json-output ./status.json ./status.md
```

The example uses an empty process snapshot and writes Markdown and JSON reports.
Read the coverage warnings alongside the agent token usage dashboard.

To inspect your own local records and processes:

```bash
python3 ./agent-monitor --hours 24 --json-output ./status.json ./status.md
```

## How it works

The monitor matches executable names and interpreter script paths for Claude and Codex.
It discovers Claude projects plus Codex `sessions/` and `archived_sessions/` directories.
It selects usage by event timestamps and separates provider cache fields.
Claude message identities remove duplicate records. Codex cumulative observations use a baseline rather than summing every snapshot.
JSON reports include observation time, configured roots, coverage, errors, process rows, and provider usage.
Use this Codex CLI observability pattern when a team needs to inspect local session evidence.

Run the synthetic regressions:

```bash
python3 -m unittest discover -s tests -v
```

## Limits

- Process matching covers the implemented Claude and Codex executable patterns. It does not discover every agent framework.
- Missing sources produce unknown coverage. Unreadable or unsupported usage records can produce partial coverage.
- Cumulative resets or missing baselines can produce an upper bound. Per-turn snapshots can remain ambiguous.
- Codex cached input and reasoning output are subsets of its input and output totals.
- Claude cache input fields remain separate. The combined input/output figure excludes those extra cache fields.
- The report provides recorded observations. It provides no account billing totals, cost estimate, or remaining subscription allowance.
- Source version 0.2.0 uses Python. Compare an installed binary’s version with this checkout before an upgrade.

See [Build a macOS release](RELEASING.md) before packaging a source change.

## Related repositories

- [agent-oversight](https://github.com/b2bvic/agent-oversight): orchestration cluster and evaluation guide.
- [session-ledger](https://github.com/b2bvic/session-ledger): searchable transcript archive.
- [observer-daemon](https://github.com/b2bvic/observer-daemon): configured response checks.
- [skills](https://github.com/b2bvic/skills): local oversight helpers.

## License

[MIT](LICENSE).
