# Claim evidence

This table maps functional README claims to source lines.

The scaffold is a local candidate. Publication, hosted CI, deployment, and customer use are not claimed.

| Claim | Source evidence |
|---|---|
| Structured requests require action, account, target, and payload | [effect_gate.py:18](effect_gate.py#L18): `required = {"action", "account", "target", "payload"}` |
| The digest binds the complete canonical JSON request | [effect_gate.py:12](effect_gate.py#L12): `json.dumps(request, sort_keys=True, separators=(",", ":")).encode()` |
| Configured hard blocks and unknown actions fail before execution | [effect_gate.py:24](effect_gate.py#L24): `if action in BLOCKED:` |
| Exact digest and a supplied approver are required for gated actions | [effect_gate.py:30](effect_gate.py#L30): `if not authorization or authorization.get("digest") != digest(request):` |
| Denied requests never reach the adapter through this entry point | [effect_gate.py:39](effect_gate.py#L39): `authorize(request, authorization)` |
| Preview returns the request without calling the adapter | [effect_gate.py:45](effect_gate.py#L45): `return request` |
| Authorization receipt precedes the adapter call | [effect_gate.py:46](effect_gate.py#L46): `record({"status": "authorized", "request_digest": digest(request)})` |
| The adapter result has completed or failed status evidence | [effect_gate.py:50](effect_gate.py#L50): `record({"status": "failed", "request_digest": digest(request)})` |
| Receipt failure before invocation prevents the effect | [tests/test_gate.py:55](tests/test_gate.py#L55): `def test_receipt_failure_prevents_effect(self):` |
| Changed action, account, target, or payload invalidates authorization | [tests/test_gate.py:25](tests/test_gate.py#L25): `def test_each_request_change_invalidates_authorization(self):` |
| Fixture uses an in-memory stub and stdout receipts without an external service | [examples/demo.py:22](examples/demo.py#L22): `def stub(item):` |
| Fixture authorization is synthetic and does not authenticate a human | [examples/demo.py:30](examples/demo.py#L30): `approval = {"digest": digest(request), "approved_by": "fixture-human"}` |
| Approval identity is supplied by the trusted caller, not authenticated by the gate | [effect_gate.py:32](effect_gate.py#L32): `if not authorization.get("approved_by"):` |
| No signatures, expiry, replay protection, or idempotency are implemented | [effect_gate.py:16](effect_gate.py#L16): `def authorize(request, authorization):` |
| Receipt storage is a caller-supplied callback; completion recording occurs after the effect | [effect_gate.py:52](effect_gate.py#L52): `record({"status": "completed", "request_digest": digest(request)})` |
| Runtime imports use only the standard library | [effect_gate.py:3](effect_gate.py#L3): `import hashlib` |
| Direct calls to other adapters are outside this gate | [effect_gate.py:48](effect_gate.py#L48): `result = capability(request)` |
| CI contains unittest, Ruff lint, Ruff format, and diff checks | [.github/workflows/ci.yml:14](.github/workflows/ci.yml#L14): `- run: python -m unittest discover -s tests -v` |
