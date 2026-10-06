# Worktree and receipt contract

## Packet spec

Give each packet a goal, allowed paths, forbidden effects, test commands, receipt destination, and named reader.
Assign disjoint paths before dispatch. Keep each worker inside one packet.
Keep secrets and external effects with the coordinator.

Create a bounded Git worktree from a reviewed base commit.

```sh
git worktree add -b packet/example ../packet-example BASE_COMMIT
```

Run the worker inside that directory. Do not push, merge, deploy, or edit shared policy during the packet.

## Receipt format

Store the complete file list, commit SHA, exact test and lint output, claim evidence, scrub results, and unresolved questions.
Name the reader. Record a predicted review verdict before requesting independent review.

The checker uses this receipt subset:

```json
{
  "files": ["src/parser.py", "tests/test_parser.py"],
  "worker": "builder",
  "tests": "pass",
  "lint": "pass",
  "review": {
    "reviewer": "independent-reviewer",
    "verdict": "pass",
    "digest": "SHA256_FROM_FINGERPRINT"
  }
}
```

Generate the digest from the actual changed-file manifest after tests pass.
Require a trusted independent reviewer to examine those files and command outputs.
Verify the review digest immediately before promotion.
If any covered file changes, repeat the checks and review.

## Promotion gate

An independent review pass permits the coordinator to request release authorization.
It does not authorize a push, merge, deployment, account change, or other external effect.
Keep a blocked review blocked. Record any missing evidence explicitly.
