# Profile source evidence

These links identify the source revisions inspected for the profile.
Each repository README controls installation and current integration limits.

| Profile claim | Source |
| --- | --- |
| Independent oversight tools and evaluation guidance | [agent-oversight: README.md, 3 to 9](https://github.com/b2bvic/agent-oversight/blob/9f8de6d5d6a39d5b7fb96e523b4c9a8ffdc14a56/README.md#L3-L9) |
| Model evaluation procedure | [agent-oversight: EVALUATION.md, 38 to 49](https://github.com/b2bvic/agent-oversight/blob/9f8de6d5d6a39d5b7fb96e523b4c9a8ffdc14a56/EVALUATION.md#L38-L49) |
| Claude Code and Codex session imports | [owned-record: README.md, 67 to 71](https://github.com/b2bvic/owned-record/blob/0a8ad992438620c78d363b65ffa57662a24c5a41/README.md#L67-L71) |
| SQLite session storage | [owned-record: components/session-ledger/ledger, 617 to 620](https://github.com/b2bvic/owned-record/blob/0a8ad992438620c78d363b65ffa57662a24c5a41/components/session-ledger/ledger#L617-L620) |
| JSON session export | [owned-record: components/session-ledger/ledger, 3524 to 3542](https://github.com/b2bvic/owned-record/blob/0a8ad992438620c78d363b65ffa57662a24c5a41/components/session-ledger/ledger#L3524-L3542) |
| REST dry runs, scope checks, duplicate callbacks, and receipts | [agent-oversight: components/safe-api/safe_api.py, 210 to 249](https://github.com/b2bvic/agent-oversight/blob/9f8de6d5d6a39d5b7fb96e523b4c9a8ffdc14a56/components/safe-api/safe_api.py#L210-L249) |
| Configured response checks | [agent-oversight: components/observer-daemon/src/validator.rs, 126 to 146](https://github.com/b2bvic/agent-oversight/blob/9f8de6d5d6a39d5b7fb96e523b4c9a8ffdc14a56/components/observer-daemon/src/validator.rs#L126-L146) |
| JSONL correction records | [agent-oversight: components/observer-daemon/src/corrections.rs, 53 to 64](https://github.com/b2bvic/agent-oversight/blob/9f8de6d5d6a39d5b7fb96e523b4c9a8ffdc14a56/components/observer-daemon/src/corrections.rs#L53-L64) |
| Markdown domain context and logs | [owned-record: .claude/hooks/route_domain.py, 122 to 129](https://github.com/b2bvic/owned-record/blob/0a8ad992438620c78d363b65ffa57662a24c5a41/.claude/hooks/route_domain.py#L122-L129) |
| Context pointers leave file contents unloaded | [owned-record: .claude/hooks/route_domain.py, 20 to 28](https://github.com/b2bvic/owned-record/blob/0a8ad992438620c78d363b65ffa57662a24c5a41/.claude/hooks/route_domain.py#L20-L28) |
| Claude Code integration | [owned-record: .claude/settings.json, 2 to 13](https://github.com/b2bvic/owned-record/blob/0a8ad992438620c78d363b65ffa57662a24c5a41/.claude/settings.json#L2-L13) |
| Selected tools and retrieval hook boundary | [owned-record: components/pretool-memory/pretool-memory.sh, 20 to 28](https://github.com/b2bvic/owned-record/blob/0a8ad992438620c78d363b65ffa57662a24c5a41/components/pretool-memory/pretool-memory.sh#L20-L28) |
| Local knowledge search | [owned-record: components/pretool-memory/pretool-memory.sh, 88 to 124](https://github.com/b2bvic/owned-record/blob/0a8ad992438620c78d363b65ffa57662a24c5a41/components/pretool-memory/pretool-memory.sh#L88-L124) |
| A writing score does not verify facts | [agent-oversight: EVALUATION.md, 29](https://github.com/b2bvic/agent-oversight/blob/9f8de6d5d6a39d5b7fb96e523b4c9a8ffdc14a56/EVALUATION.md#L29) |
| Callers must enforce human approval for REST writes | [agent-oversight: README.md, 124 to 125](https://github.com/b2bvic/agent-oversight/blob/9f8de6d5d6a39d5b7fb96e523b4c9a8ffdc14a56/README.md#L124-L125) |

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
