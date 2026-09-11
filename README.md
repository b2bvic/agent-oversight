# agent-monitor

You can lose track of agents that keep running after you leave a terminal. Use agent-monitor to see matching processes and recorded token usage in one Markdown file.

Install the current source with curl. You need Python 3.11+ available as `python3`:

```bash
mkdir -p "$HOME/.local/bin" && curl -fsSL https://raw.githubusercontent.com/b2bvic/agent-monitor/main/agent-monitor -o "$HOME/.local/bin/agent-monitor" && chmod +x "$HOME/.local/bin/agent-monitor"
```

The command follows `main`. Source version 0.2.0 uses Python. Existing v0.1.0 release assets retain the previous Bash implementation.
From this checkout, run `python3 ./agent-monitor ./status.md`.

Sample terminal output from `~/.local/bin/agent-monitor ./status.md` (illustrative counts):

```text
Agent monitor: 2 running, 5 sessions, 142000 tokens
```

You get a Markdown dashboard at `./status.md`.

## Coverage and accounting

The monitor matches Claude and Codex executable names or interpreter script paths.
A listed process is an observation. It does not prove task completion.
Usage comes from event timestamps across Claude projects and Codex `sessions/` and `archived_sessions/`.
Claude message identities deduplicate records across files. Codex cumulative counts use earlier observations as the baseline before window filtering.

Cache fields stay separate. Codex cached input and reasoning output are already included in its input and output counts.
Claude cache input fields are separate from uncached input. The combined input/output figure excludes those additional Claude cache fields.
You do not get cost estimates, account totals, or remaining subscription allowance.

Missing sources and empty directories report unknown coverage. Unreadable records and unsupported usage forms report partial coverage.
A cumulative reset or missing baseline can produce an upper-bound contribution. The warning identifies it.
Per-turn Codex usage without a cumulative total cannot reliably distinguish repeated snapshots at different timestamps.
Read coverage and warnings before using any total.

Use `--claude-root`, `--codex-root`, `--now`, and `--hours` to select inputs and the time window.
Use `--json` or `--json-output` for roots, observation time, coverage, errors, and provider usage.
Run `python3 -m unittest discover -s tests -v` for synthetic regressions.

## Worked example

```bash
./agent-monitor ./status.md
```

```bash
./agent-monitor --hours 24 --json-output ./status.json ./status.md
```

## License

MIT.

## How this was built

This 2026 README refit used model assistance.

No claim is made about how the underlying code was authored or reviewed.

## Principles

This repository demonstrates **P10 (production means persistence, bounded autonomy, and observability)** because it assembles process counts, resource fields, session counts, and token totals in one generated document.

[Read the principles](https://victorvalentineromo.com/principles).
