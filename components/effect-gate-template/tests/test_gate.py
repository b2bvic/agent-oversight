import unittest
from unittest.mock import Mock

from effect_gate import digest, execute


class GateTests(unittest.TestCase):
    def setUp(self):
        self.request = {
            "action": "send",
            "account": "demo-account",
            "target": "demo-target",
            "payload": "fixture",
        }
        self.approval = {"digest": digest(self.request), "approved_by": "human"}
        self.capability = Mock(return_value="done")
        self.events = []

    def test_missing_authorization_denies_without_call(self):
        with self.assertRaises(PermissionError):
            execute(self.request, None, self.capability, self.events.append)
        self.capability.assert_not_called()
        self.assertEqual(self.events[0]["status"], "denied")

    def test_each_request_change_invalidates_authorization(self):
        for field in self.request:
            request = {**self.request, field: "changed"}
            with self.subTest(field=field), self.assertRaises(PermissionError):
                execute(request, self.approval, self.capability, self.events.append)
        self.capability.assert_not_called()

    def test_blocked_unknown_and_malformed_requests_deny(self):
        for action in ("delete-protected-record", "unbounded-bulk-write", "unknown", ""):
            request = {**self.request, "action": action}
            approval = {"digest": digest(request), "approved_by": "human"}
            with self.subTest(action=action), self.assertRaises(PermissionError):
                execute(request, approval, self.capability, self.events.append)
        self.capability.assert_not_called()

    def test_preview_never_calls_capability(self):
        request = {**self.request, "action": "preview"}
        self.assertEqual(execute(request, None, self.capability, self.events.append), request)
        self.capability.assert_not_called()

    def test_authorization_receipt_precedes_capability(self):
        def capability(request):
            self.assertEqual(self.events[-1]["status"], "authorized")
            return "done"

        self.assertEqual(
            execute(self.request, self.approval, capability, self.events.append), "done"
        )
        self.assertEqual(self.events[-1]["status"], "completed")

    def test_receipt_failure_prevents_effect(self):
        record = Mock(side_effect=OSError("receipt unavailable"))
        with self.assertRaises(OSError):
            execute(self.request, self.approval, self.capability, record)
        self.capability.assert_not_called()

    def test_capability_failure_has_failure_receipt(self):
        self.capability.side_effect = RuntimeError("fixture failure")
        with self.assertRaises(RuntimeError):
            execute(self.request, self.approval, self.capability, self.events.append)
        self.assertEqual(self.events[-1]["status"], "failed")


if __name__ == "__main__":
    unittest.main()
