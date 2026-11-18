# AI footprint after each turn

Claude Code and Codex can show a line of estimated electricity, water and
greenhouse gas emissions when they finish a reply. The hook reads the local
transcript and uses [ai-footprint](https://github.com/abreparentesis/ai-footprint)
for the calculation. It makes no network requests and adds no model calls.
The feature is off by default.

## Set up the hook

You need a local toolkit clone, Python 3 and a version of Claude Code or Codex
that supports command hooks on `Stop`. The examples use Bash or Zsh on macOS
and Linux.

Clone the estimator once. The hook uses the calculation code from this revision.

```sh
estimator_dir="$HOME/.local/share/ai-footprint"
git clone https://github.com/abreparentesis/ai-footprint.git "$estimator_dir"
git -C "$estimator_dir" checkout --detach 0becdadbabf1f91fb4cd88270162b82920099500
```

If you already have that revision in another directory, set
`RESEARCH_AI_FOOTPRINT_ESTIMATOR` to the full path to its
`scripts/estimate_footprint.py` before starting the client.

Add the following entry under `hooks.Stop` in your client's user configuration.
If you already have entries in that list, append this one.

| Client | Configuration file | Last word of the command |
| --- | --- | --- |
| Claude Code | `~/.claude/settings.json` | `claude` |
| Codex | `~/.codex/hooks.json` (or `hooks.json` in your Codex home) | `codex` |

Use the absolute path to your toolkit clone in the command if it differs from
the one shown. Codex may ask you to trust the hook through `/hooks`.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.local/share/research-ai-toolkit/integrations/ai-footprint/turn_footprint.py\" claude",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## Switch it on for a session

Start the client with the flag set, then send a short test prompt.

```sh
RESEARCH_AI_FOOTPRINT=1 claude
# or
RESEARCH_AI_FOOTPRINT=1 codex
```

The estimate appears as a hook message alongside the completed reply. Start
the client normally to switch it off again. Use `unset RESEARCH_AI_FOOTPRINT`
first if you exported it in your shell.

## What the estimate covers

The hook counts the model usage recorded for the current turn in the main
thread. This includes model calls between tool steps. Separate subagent
transcripts and the resource use of tools, training and hardware manufacturing
water are outside the estimate. The water estimate covers cooling and
electricity generation, and CO₂e includes an allowance for hardware
manufacture.

The default `us-average` scenario uses the estimator's US grid factors. Set
`RESEARCH_AI_FOOTPRINT_GRID` to `anthropic-indiana` or `openai-azure` to try one
of its infrastructure presets. These are scenarios. Your client does not
identify the actual data centre for a request. The water range describes
the spread of the upstream model's assumptions.

If the transcript has no usable token counts for the turn, the client shows
`AI footprint unavailable`. ChatGPT and Claude in the browser do not expose
their local token logs to the Toolkit prompt. This hook runs in the local
Claude Code and Codex clients.

[Upstream methodology and factors](https://github.com/abreparentesis/ai-footprint/blob/0becdadbabf1f91fb4cd88270162b82920099500/references/methodology.md) ·
[Upstream MIT licence](https://github.com/abreparentesis/ai-footprint/blob/0becdadbabf1f91fb4cd88270162b82920099500/LICENSE) ·
[Claude Code hooks](https://code.claude.com/docs/en/hooks) ·
[Codex hooks](https://developers.openai.com/codex/hooks)
