# Synthetic transcript examples

These files contain invented text and identifiers. They contain no personal session data.
Both providers use the same source session identifier to exercise provider isolation.
The Codex example records one assistant answer in two event forms. Search should return the answer once.
It also records a function call and its matching output.

Use isolated input roots and a temporary database when you run these fixtures.
Do not copy them into your live Claude or Codex history directories.
The text reports a local file result. That statement alone does not verify that the file exists.

Expected recorded usage:

| Provider | Input | Output | Cache read | Cache creation |
|---|---:|---:|---:|---:|
| Claude | 100 | 12 | 20 | 0 |
| Codex | 80 | 10 | 20 | Not reported |

Codex cached input is a subset of input. Reasoning output is a subset of output.
Do not add those subsets to the input/output total again.
Claude cache input fields are separate from uncached input. Preserve that distinction when comparing providers.
These values describe the fixture records, not account usage or billing.
