# agent-monitor

Track running Claude Code processes and session token usage. Outputs a markdown dashboard.

Built by [Victor Valentine Romo](https://victorvalentineromo.com) at [Scale With Search](https://scalewithsearch.com).

## Usage

```bash
# Write dashboard to default file
agent-monitor

# Write to specific path
agent-monitor ~/Desktop/agents.md

# Run every 5 minutes via cron
*/5 * * * * ~/.local/bin/agent-monitor
```

## Output

```markdown
# Agent Monitor

## Running: 2

| PID | CPU | MEM | Uptime | Command |
|-----|-----|-----|--------|---------|
| 12345 | 3.2% | 1.1% | 01:23 | claude --project ... |

## Today: 5 sessions · 142,000 tokens (98,000 in / 44,000 out)
```

## How It Works

- Detects running `claude` processes with CPU/MEM/uptime
- Scans today's session JSONL files for token usage
- Writes formatted markdown with frontmatter (Dataview-compatible)
- Cross-platform: macOS and Linux

## Install

```bash
curl -o ~/.local/bin/agent-monitor https://raw.githubusercontent.com/b2bvic/agent-monitor/main/agent-monitor
chmod +x ~/.local/bin/agent-monitor
```

## License

MIT
