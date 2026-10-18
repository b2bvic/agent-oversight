import gc
import json
import tempfile
import threading
import unittest
import urllib.parse
import warnings
from datetime import datetime
from unittest import mock
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import safe_api
from safe_api import CircuitBreakerTripped, SafeAPIClient, ScopeViolation


class FixtureHandler(BaseHTTPRequestHandler):
    requests = []
    response_status = 200

    def _respond(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length) if length else b""
        body = json.loads(raw_body.decode()) if raw_body else None
        self.__class__.requests.append(
            {"method": self.command, "path": self.path, "body": body}
        )
        self.send_response(self.__class__.response_status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"ok": self.__class__.response_status < 400, "path": self.path}
        self.wfile.write(json.dumps(response).encode())

    do_GET = _respond
    do_POST = _respond
    do_PUT = _respond
    do_PATCH = _respond
    do_DELETE = _respond

    def log_message(self, _format, *_args):
        pass


class SafeAPIContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        host, port = cls.server.server_address
        cls.base_url = f"http://{host}:{port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_dir = Path(self.temp_dir.name)
        FixtureHandler.requests = []
        FixtureHandler.response_status = 200

    def tearDown(self):
        self.temp_dir.cleanup()

    def client(self, **kwargs):
        defaults = {
            "base_url": self.base_url,
            "name": "contract-test",
            "allowed_endpoints": ["/contacts"],
            "log_dir": str(self.log_dir),
            "execute": False,
        }
        defaults.update(kwargs)
        return SafeAPIClient(**defaults)

    def test_dry_run_is_default_and_writes_a_receipt(self):
        client = self.client()
        result = client.post("/contacts", {"name": "Jane"}, reason="fixture")

        self.assertTrue(result["dry_run"])
        self.assertEqual([], FixtureHandler.requests)
        self.assertEqual("DRY_RUN", client.log_tail(1)[0]["action"])

    def test_scope_violation_prevents_request(self):
        client = self.client()
        with self.assertRaises(ScopeViolation):
            client.post("/billing", {"amount": 10})
        self.assertEqual([], FixtureHandler.requests)

    def test_duplicate_callback_prevents_request_and_logs(self):
        client = self.client(dedup_checker=lambda *_args: {"id": "existing"})
        result = client.post("/contacts", {"email": "jane@example.com"})

        self.assertTrue(result["skipped"])
        self.assertEqual([], FixtureHandler.requests)
        self.assertEqual("SKIPPED_DUPLICATE", client.log_tail(1)[0]["action"])

    def test_execute_mode_sends_one_local_request_and_logs(self):
        client = self.client(execute=True)
        result = client.post("/contacts", {"name": "Jane"})

        self.assertTrue(result["ok"])
        self.assertEqual(1, len(FixtureHandler.requests))
        self.assertEqual({"name": "Jane"}, FixtureHandler.requests[0]["body"])
        self.assertEqual("EXECUTED", client.log_tail(1)[0]["action"])

    def test_get_encodes_query_parameters(self):
        client = self.client()
        result = client.get("/contacts", {"email": "jane+test@example.com", "tag": ["a", "b"]})
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(result["path"]).query)

        self.assertEqual(["jane+test@example.com"], query["email"])
        self.assertEqual(["a", "b"], query["tag"])

    def test_rate_breaker_trips_before_second_write(self):
        client = self.client(execute=True, max_writes_per_minute=1)
        client.post("/contacts", {"id": 1})

        with self.assertRaises(CircuitBreakerTripped):
            client.post("/contacts", {"id": 2})

        self.assertEqual(1, len(FixtureHandler.requests))
        self.assertEqual(1, len(list(self.log_dir.glob("incident-*.json"))))

    def test_failure_threshold_writes_incident_and_blocks_later_write(self):
        FixtureHandler.response_status = 500
        client = self.client(execute=True, max_failures=2)

        self.assertIn("error", client.post("/contacts", {"id": 1}))
        self.assertIn("error", client.post("/contacts", {"id": 2}))
        self.assertEqual(1, len(list(self.log_dir.glob("incident-*.json"))))

        with self.assertRaises(CircuitBreakerTripped):
            client.post("/contacts", {"id": 3})
        self.assertEqual(2, len(FixtureHandler.requests))


    def test_http_error_path_emits_no_resource_warning(self):
        FixtureHandler.response_status = 500
        client = self.client(execute=True, max_failures=5)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            self.assertIn("error", client.post("/contacts", {"id": 1}))
            gc.collect()

        resource_warnings = [w for w in caught if issubclass(w.category, ResourceWarning)]
        self.assertEqual([], resource_warnings)

    def test_incidents_in_same_second_write_distinct_files(self):
        calls = iter(range(1, 100))

        class SameSecondDatetime(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime(2026, 10, 3, 12, 0, 0, next(calls), tzinfo=tz)

        with mock.patch.object(safe_api, "datetime", SameSecondDatetime):
            for _ in range(2):
                client = self.client(execute=True, max_writes_per_minute=1)
                client.post("/contacts", {"id": 1})
                with self.assertRaises(CircuitBreakerTripped):
                    client.post("/contacts", {"id": 2})

        incidents = list(self.log_dir.glob("incident-*.json"))
        self.assertEqual(2, len(incidents))
        self.assertTrue(all("-20261003-120000-" in path.name for path in incidents))

    def test_query_value_cannot_inject_another_parameter(self):
        client = self.client()
        result = client.get("/contacts", {"q": "a&admin=1"})
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(result["path"]).query)
        self.assertEqual(query, {"q": ["a&admin=1"]})

    def test_transport_failure_trips_on_the_threshold_request(self):
        client = self.client(execute=True, max_failures=1)
        with mock.patch.object(safe_api.urllib.request, "urlopen", side_effect=OSError("fixture unavailable")) as request:
            self.assertIn("error", client.post("/contacts", {}))
            self.assertTrue(client._breaker_tripped)
            self.assertEqual(len(list(self.log_dir.glob("incident-*.json"))), 1)
            with self.assertRaises(CircuitBreakerTripped):
                client.post("/contacts", {})
            self.assertEqual(request.call_count, 1)


if __name__ == "__main__":
    unittest.main()
