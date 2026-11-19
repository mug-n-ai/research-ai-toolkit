"""Check which skill Claude Code loads first for each request in evals/routing.json.

The README promises that users can describe a task without naming a skill.
This script tests that promise against the skills installed for the current
user: for each case it starts a fresh, non-interactive Claude Code session in
an empty temporary directory, allows only the Skill tool, and records the
first skill the assistant loads.

    python3 scripts/run_routing_evals.py
    python3 scripts/run_routing_evals.py --jobs 4 --model sonnet

It needs an authenticated 'claude' on PATH and uses the account's normal
usage, so it is not run in CI. Install the toolkit revision you want to test
first (see INSTALL.md): the session sees whatever is in ~/.claude/skills,
including skills from other sources, which is the realistic setting.
Exit status is 0 when every case passes, 1 otherwise.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/routing.json"
TIMEOUT = 300


def load_cases(path=CASES):
    """Return the list of {prompt, expect} cases from a routing file.

    'expect' is a skill name, or null when no skill should be loaded.
    Raise ValueError for a malformed file, naming the bad case.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{path}: expected a non-empty 'cases' list")
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError(f"{path}: case {index} needs a non-empty 'prompt'")
        if "expect" not in case or not (case["expect"] is None or isinstance(case["expect"], str)):
            raise ValueError(f"{path}: case {index} needs 'expect' as a skill name or null")
    return cases


def build_command(prompt, model=None):
    """Return the claude command line for one case.

    Only the Skill tool is enabled and MCP servers are skipped, so the session
    cannot change files or reach external services, and no session is saved.
    """
    command = [
        "claude", "-p", prompt,
        "--output-format", "stream-json", "--verbose",
        "--tools", "Skill",
        "--strict-mcp-config",
        "--no-session-persistence",
    ]
    if model:
        command += ["--model", model]
    return command


def first_skill(stream):
    """Return the name of the first skill loaded in a stream-json transcript, or None.

    'stream' is an iterable of JSON lines as printed by
    'claude -p --output-format stream-json'. Lines that are not JSON, and
    tool calls other than Skill, are ignored.
    """
    for line in stream:
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(event, dict) or event.get("type") != "assistant":
            continue
        for block in event.get("message", {}).get("content", []):
            if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                return block.get("input", {}).get("skill")
    return None


def run_claude(command):
    """Run one claude command in an empty temporary directory and return its stdout lines.

    A timeout or a non-zero exit raises the subprocess error.
    """
    with tempfile.TemporaryDirectory(prefix="routing-eval-") as directory:
        result = subprocess.run(
            command, cwd=directory, check=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, timeout=TIMEOUT,
        )
    return result.stdout.splitlines()


def run_case(case, model=None, runner=run_claude):
    """Return the case with the skill that was loaded and whether it matched.

    'runner' takes a command list and returns output lines; tests pass a fake.
    A failed run is reported as an error instead of raising.
    """
    try:
        selected = first_skill(runner(build_command(case["prompt"], model)))
    except (subprocess.SubprocessError, OSError) as exc:
        return {**case, "selected": None, "passed": False, "error": str(exc)}
    return {**case, "selected": selected, "passed": selected == case["expect"]}


def report(results):
    """Return the text report and the number of passing cases."""
    lines = []
    for result in results:
        mark = "PASS" if result["passed"] else "FAIL"
        got = result.get("error") or result["selected"] or "no skill"
        lines.append(f"{mark}  expected {result['expect'] or 'no skill'}, got {got}: {result['prompt'][:70]}")
    passed = sum(result["passed"] for result in results)
    lines.append(f"{passed}/{len(results)} cases passed")
    return "\n".join(lines), passed


def main(argv=None, runner=run_claude):
    """Run every case and print the report; return 0 if all pass, else 1."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cases", type=Path, default=CASES, help="routing file (default: evals/routing.json)")
    parser.add_argument("--model", help="model alias or ID passed to claude --model")
    parser.add_argument("--jobs", type=int, default=1, help="cases to run in parallel")
    args = parser.parse_args(argv)
    cases = load_cases(args.cases)
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        results = list(pool.map(lambda case: run_case(case, args.model, runner), cases))
    text, passed = report(results)
    print(text)
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
