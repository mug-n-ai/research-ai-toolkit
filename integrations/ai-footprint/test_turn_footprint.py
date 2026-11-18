"""Regression tests for opt-in reporting and per-turn token accounting."""

import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from turn_footprint import claude_turn, codex_turn


class TurnFootprintTests(unittest.TestCase):
    """Exercise representative transcript records and the hook entry point."""

    def test_claude_counts_only_current_main_turn(self):
        """Keep tool steps and streamed usage while excluding earlier prompts."""
        prompt = {"type": "user", "message": {"content": [{"type": "text", "text": "Hi"}]}}

        def assistant(call_id, output, **fields):
            """Build a Claude fixture with one usage snapshot."""
            return {
                "type": "assistant",
                "message": {
                    "id": call_id,
                    "model": "claude-sonnet-4",
                    "usage": {"input_tokens": 10, "output_tokens": output},
                },
                **fields,
            }

        rows = [
            prompt,
            assistant("earlier", 1000),
            prompt,
            assistant("first", 1),
            assistant("first", 20),
            {"type": "user", "message": {"content": [{"type": "tool_result", "content": "OK"}]}},
            assistant("subagent", 900, isSidechain=True),
            assistant("second", 30),
        ]
        calls = claude_turn(rows)
        self.assertEqual([tokens["output"] for _, tokens in calls], [20, 30])
        self.assertEqual(sum(tokens["input"] for _, tokens in calls), 20)
        self.assertEqual(claude_turn(rows + [prompt]), [])

    def test_codex_prefers_response_records(self):
        """Deduplicate response IDs and count cached and written input once."""
        usage = {
            "input_tokens": 100, "cached_input_tokens": 30,
            "cache_write_input_tokens": 20, "output_tokens": 24,
            "reasoning_output_tokens": 9,
        }
        earlier = {
            "type": "token_usage_record",
            "payload": {"turn_id": "old", "response_id": "first", "usage": usage},
        }
        current = {
            "type": "token_usage_record",
            "payload": {"turn_id": "new", "response_id": "second", "usage": usage},
        }
        self.assertEqual(
            codex_turn([earlier, current, current], "new", "gpt-5"),
            [("gpt-5", {"input": 50, "cache_creation": 20, "cache_read": 30, "output": 24})],
        )

    def test_codex_legacy_counters_are_differenced(self):
        """Ignore repeated cumulative snapshots and later turns."""
        def event(event_type, **fields):
            """Build a legacy Codex event record."""
            return {"type": "event_msg", "payload": {"type": event_type, **fields}}

        def count(input_tokens, output_tokens, last=None):
            """Build a cumulative usage event."""
            info = {"total_token_usage": {
                "input_tokens": input_tokens, "output_tokens": output_tokens,
            }}
            if last is not None:
                info["last_token_usage"] = dict(zip(("input_tokens", "output_tokens"), last))
            return event("token_count", info=info)

        rows = [
            count(100, 20),
            event("task_started", turn_id="target"),
            count(120, 25),
            count(120, 25),
            count(160, 33),
            event("task_complete", turn_id="target"),
            event("task_started", turn_id="later"),
            count(700, 400),
        ]
        calls = codex_turn(rows, "target", "gpt-5")
        self.assertEqual([(c["input"], c["output"]) for _, c in calls], [(20, 5), (40, 8)])
        self.assertEqual(codex_turn(rows, "missing", "gpt-5"), [])
        compacted = rows[:5] + [count(8, 2, last=(8, 2))]
        calls = codex_turn(compacted, "target", "gpt-5")
        self.assertEqual([(c["input"], c["output"]) for _, c in calls], [(20, 5), (40, 8), (8, 2)])
        self.assertEqual(codex_turn(rows[:5] + [count(8, 2)], "target", "gpt-5"), [])

    def test_hook_is_opt_in_and_missing_data_is_reported(self):
        """Ensure disabled hooks are silent and missing logs yield no numbers."""
        script = Path(__file__).with_name("turn_footprint.py")
        with TemporaryDirectory() as temporary:
            payload = json.dumps({
                "hook_event_name": "Stop",
                "transcript_path": str(Path(temporary) / "missing.jsonl"),
            })
            for flag in ("0", "1"):
                result = subprocess.run(
                    [sys.executable, str(script), "claude"],
                    input=payload, text=True, capture_output=True, check=True,
                    env={**os.environ, "RESEARCH_AI_FOOTPRINT": flag},
                )
                if flag == "0":
                    self.assertEqual(result.stdout, "")
                else:
                    self.assertIn("AI footprint unavailable", json.loads(result.stdout)["systemMessage"])


if __name__ == "__main__":
    unittest.main()
