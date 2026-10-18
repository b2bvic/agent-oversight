# Profile source evidence

These links identify the source revisions inspected for the profile.
Each repository README controls installation and current integration limits.

| Profile claim | Source |
| --- | --- |
| Independent oversight tools and evaluation guidance | [agent-oversight: README.md, lines 26 to 27](https://github.com/b2bvic/agent-oversight/blob/1ff7e4c52ca120cf2efa8073d474cb3b0f75d947/README.md#L26-L27) |
| Model evaluation procedure | [agent-oversight: EVALUATION.md, lines 37 to 49](https://github.com/b2bvic/agent-oversight/blob/1ff7e4c52ca120cf2efa8073d474cb3b0f75d947/EVALUATION.md#L37-L49) |
| Claude Code and Codex session imports | [session-ledger: ledger, lines 1590 to 1607](https://github.com/b2bvic/session-ledger/blob/77fa3bf269b7ee51686b95f6a05d78f682ac17eb/ledger#L1590-L1607) |
| SQLite session storage | [session-ledger: ledger, lines 617 to 620](https://github.com/b2bvic/session-ledger/blob/77fa3bf269b7ee51686b95f6a05d78f682ac17eb/ledger#L617-L620) |
| JSON session export | [session-ledger: ledger, lines 3524 to 3542](https://github.com/b2bvic/session-ledger/blob/77fa3bf269b7ee51686b95f6a05d78f682ac17eb/ledger#L3524-L3542) |
| REST dry runs, scope checks, duplicate callbacks, and receipts | [safe-api: safe_api.py, lines 210 to 249](https://github.com/b2bvic/safe-api/blob/d5661edb899153b6a48b230f9a64e3836f45222e/safe_api.py#L210-L249) |
| Configured response checks | [observer-daemon: src/validator.rs, lines 126 to 141](https://github.com/b2bvic/observer-daemon/blob/f1a12671f1e13f72c5736a9628185393a733385e/src/validator.rs#L126-L141) |
| JSONL correction records | [observer-daemon: src/corrections.rs, lines 53 to 64](https://github.com/b2bvic/observer-daemon/blob/f1a12671f1e13f72c5736a9628185393a733385e/src/corrections.rs#L53-L64) |
| Markdown domain context and logs | [owned-record: .claude/hooks/route_domain.py, lines 122 to 129](https://github.com/b2bvic/owned-record/blob/bf831aef15439f88e94b099baa6645539ab23181/.claude/hooks/route_domain.py#L122-L129) |
| Context pointers leave file contents unloaded | [owned-record: .claude/hooks/route_domain.py, lines 20 to 28](https://github.com/b2bvic/owned-record/blob/bf831aef15439f88e94b099baa6645539ab23181/.claude/hooks/route_domain.py#L20-L28) |
| Claude Code integration | [owned-record: .claude/settings.json, lines 2 to 13](https://github.com/b2bvic/owned-record/blob/bf831aef15439f88e94b099baa6645539ab23181/.claude/settings.json#L2-L13) |
| Selected tools and retrieval hook boundary | [pretool-memory: pretool-memory.sh, lines 35 to 41](https://github.com/b2bvic/pretool-memory/blob/f8edd601e1dbd4f27cd87c5fc1be81ae15c99dca/pretool-memory.sh#L35-L41) |
| Local knowledge search | [pretool-memory: pretool-memory.sh, lines 98 to 125](https://github.com/b2bvic/pretool-memory/blob/f8edd601e1dbd4f27cd87c5fc1be81ae15c99dca/pretool-memory.sh#L98-L125) |
| A writing score does not verify facts | [agent-oversight: EVALUATION.md, lines 29 to 29](https://github.com/b2bvic/agent-oversight/blob/1ff7e4c52ca120cf2efa8073d474cb3b0f75d947/EVALUATION.md#L29-L29) |
| Human approval at the action boundary | [agent-oversight: README.md, lines 26 to 27](https://github.com/b2bvic/agent-oversight/blob/1ff7e4c52ca120cf2efa8073d474cb3b0f75d947/README.md#L26-L27) |

## Portability boundary

Owned Record stores context and logs as Markdown. Session Ledger exports records as JSON.
Move those records when changing model vendors. Configure or replace the client adapter separately.
The public hook examples do not prove compatibility with every model client.

## Provenance and adoption

The profile presents one operator's work as patterns a team can adopt.
The source provides examples and implementation boundaries. It does not measure team adoption, customer results, or search performance.

## Profile repository boundary

This repository contains documentation and Markdown validation configuration.
It does not package the linked tools or activate their hooks.
