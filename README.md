# agent-monitor

You can lose track of agents that keep running after you leave a terminal. Use agent-monitor to see matching processes and recorded token usage in one Markdown file.

Install with Bash and curl:

```bash
mkdir -p "$HOME/.local/bin" && curl -fsSL https://raw.githubusercontent.com/b2bvic/agent-monitor/main/agent-monitor -o "$HOME/.local/bin/agent-monitor" && chmod +x "$HOME/.local/bin/agent-monitor"
```

Sample terminal output from `~/.local/bin/agent-monitor ./status.md` (illustrative counts):

```text
Agent monitor: 2 running, 5 sessions, 142000 tokens
```

You get a Markdown dashboard at `./status.md`. The script matches processes whose command contains `claude`.

Session totals use JSONL files modified during the previous 24 hours under the first project directory returned by the filesystem. You do not get calendar-day totals or a complete account usage report.

## Worked example

```bash
./agent-monitor ./status.md
```

## License

MIT.

## How this was built

This 2026 README refit used model assistance.

No claim is made about how the underlying code was authored or reviewed.

## Principles

This repository demonstrates **P10 (production means persistence, bounded autonomy, and observability)** because it assembles process counts, resource fields, session counts, and token totals in one generated document.

[Read the principles](https://victorvalentineromo.com/principles).
