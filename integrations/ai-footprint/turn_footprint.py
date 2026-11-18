"""Report estimated inference resources for a local Claude Code or Codex turn.

Example: RESEARCH_AI_FOOTPRINT=1 python3 turn_footprint.py claude < stop.json
The input is the client's Stop event on stdin. Stdout carries one hook message in
JSON, or is empty when disabled. An invalid or missing transcript, dependency,
or grid preset produces an unavailable message and a successful exit.

The pinned ai-footprint model weights uncached input, cached input and output
tokens by model family to estimate facility electricity. It converts that
energy into water (cooling plus electricity generation) and CO2e (electricity
plus an allowance for hardware manufacture). The results are scenarios in Wh,
mL and g CO2e. They cover recorded model calls in the main thread, with assumed
infrastructure and grid factors. See README.md for the upstream methodology.
"""

import importlib.util
import json
import os
from pathlib import Path
import sys


def transcript_rows(path):
    """Yield JSON objects from a local JSONL path, skipping malformed lines."""
    with Path(path).expanduser().open(encoding="utf-8") as transcript:
        for line in transcript:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                yield row


def claude_turn(rows):
    """Return (model, token counts) per main-thread call since the last prompt."""
    calls = {}
    saw_prompt = False
    for row in rows:
        if row.get("isSidechain"):
            continue
        message = row.get("message") or {}
        content = message.get("content")
        if (
            row.get("type") == "user"
            and not row.get("isMeta")
            and not row.get("isCompactSummary")
            and not row.get("toolUseResult")
            and (
                isinstance(content, str)
                or isinstance(content, list)
                and any(
                    isinstance(block, dict) and block.get("type") in {"text", "image", "document"}
                    for block in content
                )
            )
        ):
            saw_prompt = True
            calls.clear()

        if row.get("type") != "assistant" or not saw_prompt:
            continue
        usage = message.get("usage") or {}
        model = message.get("model")
        call_id = message.get("id") or row.get("requestId")
        if not (usage and model and call_id) or model in {"<synthetic>", "synthetic"}:
            continue
        tokens = {
            "input": usage.get("input_tokens", 0),
            "cache_creation": usage.get("cache_creation_input_tokens", 0),
            "cache_read": usage.get("cache_read_input_tokens", 0),
            "output": usage.get("output_tokens", 0),
        }
        # Streamed message fragments share a message ID. Keep the largest count
        # for each field because fragments can contain partial usage.
        _, previous = calls.get(call_id, (model, {}))
        calls[call_id] = model, {
            key: max(value or 0, previous.get(key, 0)) for key, value in tokens.items()
        }
    return list(calls.values())


def codex_counts(usage):
    """Convert one Codex usage snapshot to upstream token categories."""
    cached = usage.get("cached_input_tokens", 0)
    cache_write = usage.get("cache_write_input_tokens", 0)
    return {
        "input": usage["input_tokens"] - cached - cache_write,
        "cache_creation": cache_write,
        "cache_read": cached,
        "output": usage["output_tokens"],
    }


def codex_turn(rows, turn_id, model):
    """Return usage for one Codex turn ID from response records or counter deltas."""
    records = {}
    cumulative = dict.fromkeys(("input", "cache_creation", "cache_read", "output"), 0)
    legacy_calls = []
    legacy_complete = True
    active = False
    for row in rows:
        payload = row.get("payload") or {}
        if row.get("type") == "token_usage_record" and payload.get("turn_id") == turn_id:
            response_id = payload.get("response_id")
            if response_id and payload.get("usage"):
                records[response_id] = codex_counts(payload["usage"])
        if row.get("type") != "event_msg":
            continue

        event = payload.get("type")
        if event in {"task_started", "turn_started"}:
            active = payload.get("turn_id") == turn_id
        elif event in {"task_complete", "turn_complete", "turn_aborted"}:
            active = False
        elif event == "token_count":
            info = payload.get("info") or {}
            usage = info.get("total_token_usage")
            if usage:
                counts = codex_counts(usage)
                delta = {key: counts[key] - cumulative[key] for key in counts}
                # Compaction can reset the cumulative snapshot. Use the call's
                # own usage across a reset, and skip repeated snapshots.
                if active and counts != cumulative:
                    last = info.get("last_token_usage")
                    if last:
                        legacy_calls.append((model, codex_counts(last)))
                    elif min(delta.values()) >= 0:
                        legacy_calls.append((model, delta))
                    else:
                        legacy_complete = False
                cumulative = counts

    if records:
        return [(model, counts) for counts in records.values()]
    return legacy_calls if legacy_complete else []


def load_estimator():
    """Load the separately installed upstream model without writing bytecode."""
    default = Path.home() / ".local/share/ai-footprint/scripts/estimate_footprint.py"
    path = Path(os.environ.get("RESEARCH_AI_FOOTPRINT_ESTIMATOR", default)).expanduser()
    spec = importlib.util.spec_from_file_location("ai_footprint_estimator", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load estimator from {path}")
    estimator = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(estimator)
    return estimator


def estimate_message(provider, calls, grid):
    """Return one line of Wh, mL water and g CO2e from the recorded token counts."""
    if not any(sum(tokens.values()) > 0 for _, tokens in calls):
        return "AI footprint unavailable: no token usage for this turn."

    estimator = load_estimator()
    config = estimator.PROVIDERS[provider]
    family_of = estimator.family_of if provider == "claude" else estimator.codex_family_of
    totals = {}
    for model, tokens in calls:
        family = family_of(model)
        if family is None:
            continue
        bucket = totals.setdefault(family, dict.fromkeys((*tokens, "msgs"), 0))
        for key, value in tokens.items():
            bucket[key] += value
        bucket["msgs"] += 1

    result = estimator.compute(totals, grid, config["energy"], config["pue"])
    energy = result["energy_kwh"] * 1000
    water = result["water_total_L"] * 1000
    carbon = result["co2_total_kg"] * 1000
    low = result["water_total_L_low"] * 1000
    high = result["water_total_L_high"] * 1000
    return (
        f"AI footprint (estimated, main thread, {grid} scenario): "
        f"{energy:.2g} Wh | {water:.2g} mL water ({low:.2g}–{high:.2g}) | "
        f"{carbon:.2g} g CO₂e"
    )


def main():
    """Read a Stop payload and emit JSON feedback without requesting another turn."""
    if os.environ.get("RESEARCH_AI_FOOTPRINT") != "1":
        return

    try:
        provider = sys.argv[1]
        event = json.load(sys.stdin)
        if event.get("hook_event_name") != "Stop":
            return
        path = event.get("transcript_path")
        calls = []
        if path and provider == "claude":
            calls = claude_turn(transcript_rows(path))
        elif path and provider == "codex" and event.get("turn_id"):
            calls = codex_turn(transcript_rows(path), event["turn_id"], event.get("model"))
        grid = os.environ.get("RESEARCH_AI_FOOTPRINT_GRID", "us-average")
        message = estimate_message(provider, calls, grid)
    except (AttributeError, ImportError, IndexError, KeyError, OSError, TypeError, ValueError):
        message = "AI footprint unavailable: check the transcript, estimator path and grid preset."

    print(json.dumps({"systemMessage": message}))


if __name__ == "__main__":
    main()
