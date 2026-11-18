# Research AI Toolkit

A shared starting point for using AI in research projects. The toolkit gives a research group one place to keep project instructions and reusable workflows. This first version contains the instruction templates, setup guide and skill catalogue. Group rules and skills will be added here as they are agreed.

## Choose your tool

| Tool | How to use the toolkit |
| --- | --- |
| ChatGPT | Paste the prompt below into a chat with web search available. |
| Claude Code | Copy `AGENTS.md` and `CLAUDE.md` into your project. Install any skills you need in `.claude/skills/`. [Claude Code setup](INSTALL.md#claude-code) |
| OpenCode | Copy `AGENTS.md` into your project. Install any skills you need in `.opencode/skills/`. [OpenCode setup](INSTALL.md#opencode) |

## ChatGPT

Paste this prompt and replace the last line with your task. The public files provide the context for that conversation.

```text
Use the Research AI Toolkit for this conversation.
Read the README and AGENTS.md at these URLs before starting:
https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/main/README.md
https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/main/AGENTS.md

When my task calls for a specific workflow, check the skill catalogue:
https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/main/skills/README.md
If a listed skill matches, open its SKILL.md and any supporting files it needs.
Tell me if you cannot fetch a file you need so I can paste or attach it.

My task: [describe what you want to do]
```

If web access is unavailable, paste or attach [`AGENTS.md`](AGENTS.md) and the relevant `SKILL.md` directly in the chat. For a project that already uses the toolkit, provide its own instruction file so ChatGPT can see the project-specific details.

## What the files do

| File | When it is useful |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Shared project instructions. OpenCode reads this file from the project. Put rules here when they should apply across tasks, and add the local context an assistant needs to work on the project. |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code's project instruction file. This template imports the neighbouring `AGENTS.md` with `@AGENTS.md`, so both tools can use the same shared text. Claude-specific instructions can go below the import. |
| [`SKILL.md`](skills/README.md#skill-format) | Instructions for a particular task. A skill has a name, a description that says when to use it, and a workflow. Claude Code and OpenCode can load individual skills when they are relevant. |

For installation paths and commands, see the [setup guide](INSTALL.md). The [skill catalogue](skills/README.md) links to each skill as it is added.
