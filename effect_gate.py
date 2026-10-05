"""Gate a structured request at a local capability adapter."""

import hashlib
import json

GATED = {"send", "publish", "pay", "delete", "activate", "update-record"}
BLOCKED = {"delete-protected-record", "unbounded-bulk-write"}


def digest(request):
    return hashlib.sha256(
        json.dumps(request, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def authorize(request, authorization):
    """The trusted caller supplies authorization. Model text is not authority."""
    required = {"action", "account", "target", "payload"}
    if set(request) != required or any(
        not isinstance(request[key], str) or not request[key] for key in required - {"payload"}
    ):
        raise PermissionError("request needs an action, account, target, and payload")
    action = request["action"]
    if action in BLOCKED:
        raise PermissionError("action is blocked")
    if action == "preview":
        return
    if action not in GATED:
        raise PermissionError("unknown action")
    if not authorization or authorization.get("digest") != digest(request):
        raise PermissionError("authorization does not match the exact request")
    if not authorization.get("approved_by"):
        raise PermissionError("authorization needs a trusted approver")


def execute(request, authorization, capability, record):
    """Record authorization before invoking a capability, then record its result."""
    try:
        authorize(request, authorization)
    except PermissionError:
        record({"status": "denied", "request_digest": digest(request)})
        raise
    if request["action"] == "preview":
        record({"status": "preview", "request_digest": digest(request)})
        return request
    record({"status": "authorized", "request_digest": digest(request)})
    try:
        result = capability(request)
    except Exception:
        record({"status": "failed", "request_digest": digest(request)})
        raise
    record({"status": "completed", "request_digest": digest(request)})
    return result
