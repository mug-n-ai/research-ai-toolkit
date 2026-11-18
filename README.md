# Research AI Toolkit

A shared starting point for using AI in research projects. The toolkit gives a research group one place to keep project instructions and reusable workflows, from checking a draft to testing a change in an analysis pipeline.

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
https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/refs/heads/main/README.md
https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/refs/heads/main/AGENTS.md

When my task calls for a specific workflow, check the skill catalogue:
https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/refs/heads/main/skills/README.md
If a listed skill matches, open its SKILL.md and any supporting files it needs.
Use skills marked "By request" only when I name them. Resolve catalogue links
relative to the catalogue URL above. Tell me when a step needs a tool you lack.
Tell me if you cannot fetch a file you need so I can paste or attach it.

My task: [describe what you want to do]
```

If web access is unavailable, paste or attach [`AGENTS.md`](AGENTS.md) and the relevant `SKILL.md` directly in the chat. For a project that already uses the toolkit, provide its own instruction file so ChatGPT can see the project-specific details.

## Skills for research work

- **Review a draft.** No AI Slop flags vague attributions, stock phrases and inflated wording. It can report the passages to check or make a light edit that preserves the author's voice. [No AI Slop](skills/README.md#writing)
- **Plan and check research software.** Matt Pocock's skills help you work through a design before writing code, trace answers to primary sources, reproduce bugs and test changes in small steps. [Matt Pocock's skills](skills/README.md#matt-pococks-skills)

## Keep a local knowledge base

If you ask an assistant why a parameter was fixed in an analysis, the answer should point you to the code, the methods notes or the paper that explains the choice. A plausible answer can still get the reason wrong. Keep the sources your project relies on in a local repository or folder so the assistant has somewhere specific to look.

Start with the papers the group has checked, the versions of the code used in the analysis, and the notes that record how decisions were made. Keep the DOI or original link for each paper and record the relevant version or commit where you can. Ask the assistant to cite the file and the relevant passage for each claim that matters. Check that the passage supports the claim, especially before using it in a paper or analysis. If the sources leave a question open, ask the assistant to say what evidence is missing.

### Search the sources with Carsen

[Carsen](https://github.com/LorenzoMugnai/Carsen) indexes selected code and document folders locally. An assistant can query that index through the Model Context Protocol (MCP) and get back passages with source paths and line ranges. This gives you a place to check where an answer came from.

You can ask a coding assistant with terminal access to install Carsen, configure it for your project and test it. Give it the paths to the folders you want to index and point it to the [Carsen setup guide for AI agents](https://github.com/LorenzoMugnai/Carsen/blob/main/docs/agent-setup.md).

```text
Install and configure Carsen for this project. Follow the setup guide at
https://github.com/LorenzoMugnai/Carsen/blob/main/docs/agent-setup.md

Index the code in [path to code] and the documents in [path to documents].
Connect the resulting knowledge base to my MCP client [name of client].
Test it by searching for [a phrase known to be in the sources] and show
me the file and line range returned by the search.
```

## What the files do

| File | When it is useful |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Shared project instructions. OpenCode reads this file from the project. Put rules here when they should apply across tasks, and add the local context an assistant needs to work on the project. |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code's project instruction file. This template imports the neighbouring `AGENTS.md` with `@AGENTS.md`, so both tools can use the same shared text. Claude-specific instructions can go below the import. |
| [`SKILL.md`](skills/README.md#skill-format) | Instructions for a particular task. A skill has a name, a description that says when to use it, and a workflow. Claude Code and OpenCode can load individual skills when they are relevant. |

For installation paths and commands, see the [setup guide](INSTALL.md). The [skill catalogue](skills/README.md) links to each skill as it is added.
