"""Exercise the gate with an in-memory stub and stdout receipts."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from effect_gate import digest, execute  # noqa: E402

request = {
    "action": "send",
    "account": "demo-account",
    "target": "demo-recipient",
    "payload": "Local fixture only.",
}


def record(event):
    print(json.dumps(event, sort_keys=True))


def stub(item):
    return {"adapter": "local-stub", "target": item["target"]}


try:
    execute(request, None, stub, record)
except PermissionError:
    print("Missing authorization refused before the stub ran.")
approval = {"digest": digest(request), "approved_by": "fixture-human"}
print(json.dumps(execute(request, approval, stub, record)))
