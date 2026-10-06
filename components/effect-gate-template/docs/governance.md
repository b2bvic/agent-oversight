# Capability governance template

## Authority

Keep policy and authorization in a record your organization owns.
Authorize one bounded action, account, target, and exact payload.
Store the exact outbound text before authorizing transmission.
Keep authorization construction outside model-accessible tools.

## Executor contract

Run deterministic identity, eligibility, deduplication, suppression, and authorization checks before an effect.
Place the gate inside each adapter that can create an external effect.
Keep credentials in the adapter process. Use the narrowest available permission.
Refuse unknown actions and configured hard blocks.
Record authorization before execution. Reconcile ambiguous execution results before retrying.

## Release conditions

Require independent review of every adapter and alternate entry point.
Verify signatures or another trusted authorization channel before using this template with external services.
Add expiry, replay prevention, idempotency, and durable receipt storage for the integration's needs.
Test direct-call bypasses and receipt-storage failures.
Do not infer production enforcement from prompt language or this fixture.

## Owned evidence

Name the receipt reader and retention rule.
Retain the canonical policy, exact request, authorization provenance, result, and correction history.
Separate evidence of attempted execution from evidence of a completed external effect.
Keep sensitive request bodies out of public fixtures.
