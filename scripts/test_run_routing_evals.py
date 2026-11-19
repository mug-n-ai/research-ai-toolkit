"""Tests for scripts/run_routing_evals.py with a fake claude runner.

Run with 'python -m unittest discover -s scripts'. No model is called.
"""

import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import run_routing_evals as evals


def tool_use(name, **inputs):
    """Return one stream-json assistant line that calls a tool."""
    message = {"content": [{"type": "tool_use", "name": name, "input": inputs}]}
    return json.dumps({"type": "assistant", "message": message})


class LoadCasesTest(unittest.TestCase):
    def write(self, data):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(data, handle)
        handle.close()
        self.addCleanup(Path(handle.name).unlink)
        return handle.name

    def test_repository_cases_are_valid_and_name_toolkit_skills(self):
        skills = {path.parent.name for path in evals.ROOT.glob("skills/*/SKILL.md")}
        for case in evals.load_cases():
            self.assertTrue(case["expect"] is None or case["expect"] in skills, case)

    def test_malformed_cases_are_rejected(self):
        for data in ({}, {"cases": []}, {"cases": [{"prompt": ""}]}, {"cases": [{"prompt": "x"}]},
                     {"cases": [{"prompt": "x", "expect": 3}]}):
            with self.assertRaises(ValueError):
                evals.load_cases(self.write(data))


class ParsingTest(unittest.TestCase):
    def test_first_skill_ignores_noise_and_other_tools(self):
        stream = [
            "not json",
            json.dumps({"type": "system", "subtype": "init"}),
            tool_use("Read", file_path="x"),
            tool_use("Skill", skill="literature-review"),
            tool_use("Skill", skill="research"),
        ]
        self.assertEqual(evals.first_skill(stream), "literature-review")

    def test_no_skill_call_returns_none(self):
        self.assertIsNone(evals.first_skill([json.dumps({"type": "result", "result": "391"})]))

    def test_command_allows_only_the_skill_tool_and_passes_model(self):
        command = evals.build_command("hello", model="sonnet")
        self.assertEqual(command[:3], ["claude", "-p", "hello"])
        self.assertEqual(command[command.index("--tools") + 1], "Skill")
        self.assertEqual(command[-2:], ["--model", "sonnet"])
        self.assertNotIn("--model", evals.build_command("hello"))


class RunTest(unittest.TestCase):
    def test_run_case_reports_match_mismatch_and_errors(self):
        case = {"prompt": "p", "expect": "pr"}
        self.assertTrue(evals.run_case(case, runner=lambda _: [tool_use("Skill", skill="pr")])["passed"])
        miss = evals.run_case(case, runner=lambda _: [])
        self.assertEqual((miss["passed"], miss["selected"]), (False, None))

        def failing(_):
            raise subprocess.TimeoutExpired("claude", 1)

        error = evals.run_case(case, runner=failing)
        self.assertFalse(error["passed"])
        self.assertIn("timed out", error["error"])

    def test_no_skill_expected_passes_when_none_is_loaded(self):
        self.assertTrue(evals.run_case({"prompt": "p", "expect": None}, runner=lambda _: [])["passed"])

    def test_main_reports_counts_and_exit_status(self):
        def runner(command):
            return [tool_use("Skill", skill="research")] if "numpy" in command[2] else []

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = evals.main(["--jobs", "3"], runner=runner)
        self.assertEqual(status, 1)
        total = len(evals.load_cases())
        self.assertIn(f"2/{total} cases passed", out.getvalue())  # the numpy case and the no-skill case
        self.assertIn("PASS  expected research, got research", out.getvalue())


if __name__ == "__main__":
    unittest.main()
