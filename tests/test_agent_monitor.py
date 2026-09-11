#!/usr/bin/env python3
"""Isolated synthetic tests for agent-monitor 0.2.0. Does not read live telemetry."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from importlib.machinery import SourceFileLoader
from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "agent-monitor"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
NOW = "2026-01-15T18:00:00Z"
UTC = timezone.utc


def load_monitor():
    loader = SourceFileLoader("agent_monitor", str(SCRIPT))
    spec = importlib.util.spec_from_loader("agent_monitor", loader)
    if spec is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["agent_monitor"] = module
    loader.exec_module(module)
    return module


MONITOR = load_monitor()


def python_bin() -> str:
    return os.environ.get("AGENT_MONITOR_PYTHON", sys.executable)


class AgentMonitorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.out_dir = Path(self.tmpdir.name)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def observe(
        self,
        fixture: str,
        *,
        claude_root: Path | None = None,
        codex_root: Path | None = None,
        output_name: str = "status.md",
        json_name: str = "status.json",
        ps_file: Path | None = None,
        hours: str = "24",
        now: str = NOW,
    ) -> tuple[dict, str, str]:
        base = FIXTURES / fixture
        if claude_root is None:
            claude_root = base / "claude" / "projects"
        if codex_root is None:
            candidate = base / "codex"
            codex_root = candidate if candidate.exists() else self.out_dir / "missing-codex"
        output = self.out_dir / output_name
        json_output = self.out_dir / json_name
        snapshot = ps_file if ps_file is not None else FIXTURES / "processes" / "empty.jsonl"
        args = MONITOR.build_parser().parse_args([
            "--now",
            now,
            "--hours",
            hours,
            "--claude-root",
            str(claude_root),
            "--codex-root",
            str(codex_root),
            "--ps-file",
            str(snapshot),
            "--json-output",
            str(json_output),
            str(output),
        ])
        report = MONITOR.observe(args)
        markdown = MONITOR.render_markdown(report)
        payload = report.as_dict()
        json_text = json.dumps(payload, indent=2) + "\n"
        MONITOR.atomic_write_text(output, markdown)
        MONITOR.atomic_write_text(json_output, json_text)
        summary = MONITOR.summary_line(report)
        return payload, markdown, summary

    def test_spacing_in_json(self) -> None:
        payload, markdown, _ = self.observe("spacing")
        claude = payload["usage"]["claude"]
        self.assertTrue(claude["observed"])
        self.assertEqual(claude["input_tokens"], 11)
        self.assertEqual(claude["output_tokens"], 4)
        self.assertEqual(claude["cache_creation_input_tokens"], 2)
        self.assertEqual(claude["cache_read_input_tokens"], 8)
        self.assertNotIn("cost", json.dumps(payload))
        self.assertIn("cache create 2", markdown)

    def test_old_event_recently_modified(self) -> None:
        work = self.out_dir / "old_event"
        shutil.copytree(FIXTURES / "old_event", work)
        session = work / "claude" / "projects" / "p1" / "session.jsonl"
        now = datetime.now(UTC).timestamp()
        os.utime(session, (now, now))
        payload, markdown, _ = self.observe(
            "old_event",
            claude_root=work / "claude" / "projects",
            codex_root=self.out_dir / "missing-codex-old-event",
        )
        claude = payload["usage"]["claude"]
        self.assertTrue(claude["observed"])
        self.assertEqual(claude["sessions"], 0)
        self.assertEqual(claude["input_tokens"], 0)
        self.assertEqual(payload["coverage"]["claude"]["status"], "complete")
        self.assertNotIn("999", markdown.split("## Usage", 1)[-1])

    def test_new_event_in_old_file(self) -> None:
        work = self.out_dir / "new_event_old_file"
        shutil.copytree(FIXTURES / "new_event_old_file", work)
        session = work / "claude" / "projects" / "p1" / "session.jsonl"
        os.utime(session, (1_000_000_000, 1_000_000_000))
        payload, _, _ = self.observe(
            "new_event_old_file",
            claude_root=work / "claude" / "projects",
            codex_root=self.out_dir / "missing-codex-old-file",
        )
        claude = payload["usage"]["claude"]
        self.assertTrue(claude["observed"])
        self.assertEqual(claude["input_tokens"], 21)
        self.assertEqual(claude["output_tokens"], 3)

    def test_duplicates_use_last_snapshot(self) -> None:
        payload, _, _ = self.observe("duplicates")
        claude = payload["usage"]["claude"]
        self.assertEqual(claude["sessions"], 1)
        self.assertEqual(claude["input_tokens"], 10)
        self.assertEqual(claude["output_tokens"], 7)

    def test_codex_resume_cumulative_deltas(self) -> None:
        payload, _, summary = self.observe(
            "codex_resume",
            claude_root=self.out_dir / "missing-claude-resume",
            codex_root=FIXTURES / "codex_resume" / "codex",
        )
        codex = payload["usage"]["codex"]
        self.assertTrue(codex["observed"])
        self.assertEqual(codex["input_tokens"], 240)
        self.assertEqual(codex["output_tokens"], 35)
        self.assertEqual(codex["cached_input_tokens"], 95)
        self.assertNotEqual(codex["input_tokens"], 380)
        self.assertNotIn("cost", summary)

    def test_multiple_projects_and_codex_locations(self) -> None:
        payload, _, _ = self.observe(
            "multiple_projects",
            claude_root=FIXTURES / "multiple_projects" / "claude" / "projects",
            codex_root=FIXTURES / "multiple_projects" / "codex",
        )
        claude = payload["usage"]["claude"]
        codex = payload["usage"]["codex"]
        self.assertEqual(claude["sessions"], 2)
        self.assertEqual(claude["input_tokens"], 30)
        self.assertEqual(codex["sessions"], 2)
        self.assertEqual(codex["input_tokens"], 55)
        self.assertEqual(codex["cached_input_tokens"], 7)
        self.assertEqual(codex["reasoning_output_tokens"], 1)
        self.assertEqual(payload["coverage"]["claude"]["status"], "complete")
        self.assertEqual(payload["coverage"]["codex"]["status"], "partial")

    def test_missing_root_is_unknown_not_zero(self) -> None:
        missing_claude = self.out_dir / "no-such-claude"
        missing_codex = self.out_dir / "no-such-codex"
        payload, markdown, summary = self.observe(
            "spacing",
            claude_root=missing_claude,
            codex_root=missing_codex,
        )
        self.assertFalse(payload["usage"]["claude"]["observed"])
        self.assertFalse(payload["usage"]["codex"]["observed"])
        self.assertEqual(payload["coverage"]["claude"]["status"], "unknown")
        self.assertEqual(payload["coverage"]["codex"]["status"], "unknown")
        self.assertNotIn("input_tokens", payload["usage"]["claude"])
        self.assertIn("unknown, not zero", markdown)
        self.assertIn("usage unknown", summary)
        kinds = {item["kind"] for item in payload["errors"]}
        self.assertIn("missing_root", kinds)

    def test_malformed_row_is_partial(self) -> None:
        payload, markdown, summary = self.observe("malformed")
        claude = payload["usage"]["claude"]
        self.assertTrue(claude["observed"])
        self.assertEqual(claude["input_tokens"], 7)
        self.assertEqual(payload["coverage"]["claude"]["status"], "partial")
        kinds = {item["kind"] for item in payload["errors"]}
        self.assertIn("malformed_record", kinds)
        self.assertIn("malformed", markdown.lower())
        self.assertIn("warning", summary)

    def test_path_spaces(self) -> None:
        output_dir = self.out_dir / "out dir"
        payload, markdown, _ = self.observe(
            "path_spaces",
            claude_root=FIXTURES / "path_spaces" / "claude" / "projects",
            output_name=str(Path("out dir") / "status file.md"),
            json_name=str(Path("out dir") / "status file.json"),
        )
        self.assertEqual(payload["usage"]["claude"]["input_tokens"], 9)
        self.assertTrue((output_dir / "status file.md").is_file())
        self.assertTrue((output_dir / "status file.json").is_file())
        spaced_session = (
            FIXTURES / "path_spaces" / "claude" / "projects" / "my project" / "session 1.jsonl"
        )
        self.assertTrue(spaced_session.is_file())
        self.assertIn("Agent Monitor", markdown)

    def test_false_process_matches(self) -> None:
        payload, markdown, _ = self.observe(
            "spacing",
            ps_file=FIXTURES / "processes" / "snapshot.jsonl",
        )
        pids = {row["pid"] for row in payload["processes"]}
        self.assertEqual(pids, {15, 16, 17})
        providers = {row["pid"]: row["provider"] for row in payload["processes"]}
        self.assertEqual(providers[15], "claude")
        self.assertEqual(providers[16], "claude")
        self.assertEqual(providers[17], "codex")
        self.assertNotIn("grep claude", markdown)
        self.assertNotIn("bash -c claude", markdown)
        self.assertIn("are running now", markdown)
        self.assertIn("not treated as completion", markdown)

    def test_missing_timestamp_and_unknown_schema(self) -> None:
        payload, _, _ = self.observe("missing_timestamp")
        kinds = {item["kind"] for item in payload["errors"]}
        self.assertIn("missing_timestamp", kinds)
        self.assertEqual(payload["usage"]["claude"]["input_tokens"], 8)
        self.assertEqual(payload["coverage"]["claude"]["status"], "partial")

        payload, _, _ = self.observe("unknown_schema")
        kinds = {item["kind"] for item in payload["errors"]}
        self.assertIn("unknown_schema", kinds)
        self.assertEqual(payload["usage"]["claude"]["input_tokens"], 4)
        self.assertEqual(payload["coverage"]["claude"]["status"], "partial")

    def test_json_report_shape_and_no_cost(self) -> None:
        payload, _, _ = self.observe(
            "multiple_projects",
            claude_root=FIXTURES / "multiple_projects" / "claude" / "projects",
            codex_root=FIXTURES / "multiple_projects" / "codex",
        )
        self.assertEqual(payload["version"], "0.2.0")
        self.assertEqual(payload["observed_at"], "2026-01-15T18:00:00+00:00")
        self.assertIn("claude", payload["roots"])
        self.assertIn("codex", payload["roots"])
        self.assertIn("coverage", payload)
        self.assertIn("errors", payload)
        self.assertIn("usage", payload)
        dumped = json.dumps(payload)
        for forbidden in ("cost", "usd", "price", "dollar"):
            self.assertNotIn(forbidden, dumped.casefold())
        self.assertEqual(payload["hours"], 24.0)

    def test_atomic_replace_existing_output(self) -> None:
        output = self.out_dir / "status.md"
        output.write_text("stale\n", encoding="utf-8")
        _, markdown, _ = self.observe("spacing", output_name="status.md")
        self.assertTrue(markdown.startswith("type:: agents"))
        self.assertNotIn("stale", markdown)
        leftovers = list(self.out_dir.glob(".agent-monitor.*.tmp"))
        self.assertEqual(leftovers, [])

    def test_cache_not_added_to_input(self) -> None:
        payload, _, _ = self.observe("spacing")
        claude = payload["usage"]["claude"]
        self.assertEqual(claude["input_tokens"], 11)
        self.assertNotEqual(claude["input_tokens"], 11 + 8)

    def test_cli_python_version_gate(self) -> None:
        proc = subprocess.run(
            [python_bin(), str(SCRIPT), "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        if sys.version_info < (3, 11) and "AGENT_MONITOR_PYTHON" not in os.environ:
            self.assertEqual(proc.returncode, 2)
            self.assertIn("Python 3.11+", proc.stderr)
        else:
            self.assertEqual(proc.returncode, 0)
            self.assertIn("0.2.0", proc.stdout)

    def test_cli_main_json_and_spaced_output(self) -> None:
        original = MONITOR.require_python
        MONITOR.require_python = lambda: None
        try:
            out_dir = self.out_dir / "cli out"
            md = out_dir / "status file.md"
            js = out_dir / "status file.json"
            argv = [
                "--now",
                NOW,
                "--hours",
                "24",
                "--claude-root",
                str(FIXTURES / "path_spaces" / "claude" / "projects"),
                "--codex-root",
                str(self.out_dir / "missing-codex-cli"),
                "--ps-file",
                str(FIXTURES / "processes" / "empty.jsonl"),
                "--json",
                "--json-output",
                str(js),
                str(md),
            ]
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = MONITOR.main(argv)
            self.assertEqual(code, 0)
            self.assertTrue(md.is_file())
            payload = json.loads(js.read_text(encoding="utf-8"))
            printed = json.loads(stdout.getvalue())
            self.assertEqual(payload["usage"]["claude"]["input_tokens"], 9)
            self.assertEqual(payload["version"], "0.2.0")
            self.assertEqual(printed["usage"]["claude"]["input_tokens"], 9)
        finally:
            MONITOR.require_python = original

    def native_event(self, timestamp, total, last=None):
        info = {"total_token_usage": {"input_tokens": total, "output_tokens": 0}}
        if last is not None:
            info["last_token_usage"] = {"input_tokens": last, "output_tokens": 0}
        return {"timestamp": timestamp, "type": "event_msg", "payload": {"type": "token_count", "info": info}}

    def custom_codex(self, rows):
        root = self.out_dir / "codex"
        (root / "sessions").mkdir(parents=True)
        (root / "archived_sessions").mkdir()
        (root / "sessions/native.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        return self.observe("spacing", codex_root=root)[0]

    def test_pre_window_cumulative_baseline_is_retained(self):
        data = self.custom_codex([
            self.native_event("2026-01-14T17:00:00Z", 100000),
            self.native_event("2026-01-15T12:00:00Z", 101000),
        ])
        self.assertEqual(data["usage"]["codex"]["input_tokens"], 1000)

    def test_repeated_last_usage_with_same_total_counts_once(self):
        data = self.custom_codex([
            self.native_event("2026-01-15T12:00:00Z", 100, 100),
            self.native_event("2026-01-15T12:00:01Z", 100, 100),
        ])
        self.assertEqual(data["usage"]["codex"]["input_tokens"], 100)

    def test_claude_message_copied_across_files_counts_once(self):
        root = self.out_dir / "claude"
        (root / "a").mkdir(parents=True)
        (root / "b").mkdir()
        source = FIXTURES / "spacing/claude/projects/p1/session.jsonl"
        for folder in ("a", "b"):
            shutil.copy(source, root / folder / "session.jsonl")
        data, _, _ = self.observe("spacing", claude_root=root)
        self.assertEqual(data["usage"]["claude"]["input_tokens"], 11)

    def test_empty_directory_does_not_establish_coverage(self):
        root = self.out_dir / "empty"
        root.mkdir()
        data, _, _ = self.observe("spacing", claude_root=root)
        self.assertEqual(data["coverage"]["claude"]["status"], "unknown")
        self.assertFalse(data["usage"]["claude"]["observed"])

    def test_invalid_window_is_controlled_error(self):
        for value in ("nan", "inf", "1e100"):
            args = MONITOR.build_parser().parse_args(["--hours", value])
            with self.assertRaisesRegex(SystemExit, "error:"):
                MONITOR.observe(args)


class ProcessMatchUnitTests(unittest.TestCase):
    def test_executable_boundaries(self) -> None:
        match = MONITOR.match_agent_process
        self.assertEqual(match("claude", "/usr/local/bin/claude --project x"), "claude")
        self.assertEqual(match("codex", "/usr/local/bin/codex"), "codex")
        self.assertEqual(
            match(
                "node",
                "node /usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js",
            ),
            "claude",
        )
        self.assertIsNone(match("grep", "grep claude"))
        self.assertIsNone(match("bash", "bash -c claude"))
        self.assertEqual(match("bash", "bash /usr/local/bin/claude"), "claude")
        self.assertIsNone(match("cat", "cat /tmp/claude.jsonl"))
        self.assertIsNone(match("claude-agent", "/usr/local/bin/claude-agent"))
        self.assertIsNone(match("python3", "python3 /tmp/claude_helper.py"))
        self.assertIsNone(match("node", "node /tmp/my-claude-tool.js"))
        self.assertIsNone(match("agent-monitor", "python3 ./agent-monitor ./status.md"))

    def test_codex_cumulative_accumulator(self) -> None:
        usage = MONITOR.TokenUsage
        events = [
            ("cumulative", usage(input_tokens=100, output_tokens=10, cached_input_tokens=50)),
            ("cumulative", usage(input_tokens=150, output_tokens=20, cached_input_tokens=70)),
            ("cumulative", usage(input_tokens=40, output_tokens=5, cached_input_tokens=10)),
            ("cumulative", usage(input_tokens=90, output_tokens=15, cached_input_tokens=25)),
        ]
        total = MONITOR.accumulate_codex_events(events)
        self.assertEqual(total.input_tokens, 240)
        self.assertEqual(total.output_tokens, 35)
        self.assertEqual(total.cached_input_tokens, 95)


if __name__ == "__main__":
    unittest.main()
