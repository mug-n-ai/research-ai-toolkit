# Research AI Toolkit

*Reusable AI skills and guidelines for scientific research.*

[![Latest release](https://img.shields.io/github/v/release/mug-n-ai/research-ai-toolkit?label=release&color=315588)](https://github.com/mug-n-ai/research-ai-toolkit/releases/latest)
[![Toolkit checks](https://github.com/mug-n-ai/research-ai-toolkit/actions/workflows/check.yml/badge.svg?branch=main)](https://github.com/mug-n-ai/research-ai-toolkit/actions/workflows/check.yml)
[![Skill count](https://img.shields.io/github/directory-file-count/mug-n-ai/research-ai-toolkit/skills?type=dir&label=skills&color=315588)](skills/README.md)
[![Licence: MIT](docs/badges/licence.svg)](LICENSE)
[![Contributions welcome](docs/badges/contributing.svg)](CONTRIBUTING.md)

**Works with:** [![Claude Code](https://img.shields.io/badge/Claude_Code-353B45?logo=anthropic&logoColor=white)](INSTALL.md#claude-code-from-the-clone) [![Codex](https://img.shields.io/badge/Codex-353B45?logo=openai&logoColor=white)](INSTALL.md#codex-from-the-clone) [![OpenCode](https://img.shields.io/badge/OpenCode-353B45?logo=opencode&logoColor=white)](INSTALL.md#opencode-from-the-clone) [![ChatGPT](https://img.shields.io/badge/ChatGPT-353B45?logo=openai&logoColor=white)](#use-the-toolkit-in-a-chat) and other chat interfaces that can read public links.

Use this toolkit when you want an AI assistant to help with your own research, from checking the evidence behind a draft to rerunning an analysis.

**Core principles:** Verify sources · Reproduce results · Reuse workflows

**You do not need to choose a skill yourself.** Once the toolkit is installed in a client that can discover its skills, just describe what you want to do. The assistant can match your request to an available skill and follow its instructions when relevant. For example, asking “Does this paragraph agree with the published evidence?” can bring in `literature-review` automatically. You do not need to say “use literature-review” or know the names of the skills.

Some workflows are marked **By request** and need to be invoked explicitly. In a web chat without installed skills, start with the [chat prompt](#use-the-toolkit-in-a-chat) so the assistant knows where to find the catalogue. Automatic selection also depends on the client and which skills it can access.

## Contents

- [Quick start](#quick-start) · [Use the toolkit](#use-the-toolkit) · [Research workflows](#research-workflows)
- [Project rules and knowledge bases](#project-rules-and-knowledge-bases) · [What is a skill?](#what-is-a-skill)
- [Optional tools](#optional-tools) · [Contributing](#contributing) · [Licence](#licence) · [How this repository was made](#how-this-repository-was-made)

## Quick start

[Use the chat prompt](#use-the-toolkit-in-a-chat) or [install the toolkit](INSTALL.md), then give the assistant a task and the material it needs. Here are four requests to adapt.

> [!TIP]
> **You can ask an AI assistant to install the toolkit.** Give Claude Code, Codex or OpenCode the [setup prompt](INSTALL.md#ask-an-assistant-to-set-it-up). It should check your existing configuration, preserve your settings and verify the installation.

- “Check which papers support each claim in this paragraph. Read the full sources and inspect their original figures. Point me to the relevant passages and flag any claim you could not verify.” [Literature review](skills/literature-review/SKILL.md)
- “Reproduce this figure using the data and code revision I supplied. Record the settings and seeds, save the new plot separately and report what differs.” [Reproduce analysis](skills/reproduce-analysis/SKILL.md)
- “Check the units in this calculation and propagate the reported uncertainties. Tell me what correlation information you need and state what the final interval represents.” [Uncertainty and units](skills/uncertainty-and-units/SKILL.md)
- “Audit this repository for dead code, unnecessary complexity and duplication. Follow the existing design decisions and give me a prioritised plan without changing files.” [Code cleanup](skills/code-cleanup/SKILL.md)

## Use the toolkit

### Choose your tool

| Tool | How to use the toolkit |
| --- | --- |
| Chat interfaces | Use the prompt below in any chat that can open public links, or share the files directly. |
| Codex | Use one local clone across your projects, or install the rules and skills in a single project. [Codex setup](INSTALL.md#codex-from-the-clone) |
| Claude Code | Use one local clone for all your projects, or copy the files into a single project. [Claude Code setup](INSTALL.md#claude-code-from-the-clone) |
| OpenCode | Point OpenCode at the same clone, or copy the files into a single project. [OpenCode setup](INSTALL.md#opencode-from-the-clone) |

### Install it with an assistant

An assistant with terminal access on the machine where you run Codex, Claude Code or OpenCode can install the toolkit for you. Tell it which tools and scope you want. It can check your existing setup, choose how to make the rules and skills available, and verify the result. [Copy the setup prompt](INSTALL.md#ask-an-assistant-to-set-it-up)

### Use the toolkit in a chat

Paste this prompt into ChatGPT, Claude, or any other assistant that can open public links. Replace the last line with your task. The assistant can then read the rules and choose a relevant workflow for that conversation.

<details>
<summary>Show the prompt for a web chat</summary>

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

</details>

If the assistant cannot open the links, paste or attach [`AGENTS.md`](AGENTS.md), the relevant `SKILL.md` and any supporting files it needs. For a project that already uses the toolkit, share its own instruction file for project-specific details.

## Research workflows

The workflows below show what the toolkit can help with, not commands you have to memorise. When a matching skill is available, the assistant can choose it from the task you describe. The links let you inspect the instructions and examples.

### Literature review

The `literature-review` skill can find papers, check a claim or continue a reading list. Read each source used as evidence in full and inspect its figures in the original paper. Record which passage supports the claim and the conditions that limit what you can conclude. [Skill instructions](skills/literature-review/SKILL.md) · [Example: sodium in HD 209458 b](examples/literature-review/README.md)

### Reproduce an analysis

The `reproduce-analysis` skill traces a figure, table or number to its inputs, code and run settings. Rerun it in a separate output directory and record what matches, what differs and what you could not check. [Skill instructions](skills/reproduce-analysis/SKILL.md) · [Example: Anscombe's quartet](examples/reproduce-analysis/README.md)

### Clean up code

The `code-cleanup` skill can find dead code, remove unnecessary complexity, reduce duplication or check whether an implementation still follows the project's design. **For a single function**, it makes a targeted refactor and tests the behaviour. **For a whole repository**, it identifies candidates and writes a prioritised plan without changing the implementation. Static-analysis findings are leads, not proof that code is safe to remove. [Skill instructions](skills/code-cleanup/SKILL.md) · [Cleanup plan template](skills/code-cleanup/cleanup-plan-template.md)

### Third-party skills for research work

Use No AI Slop to review a draft, Matt Pocock's skills to plan and test software, or K-Dense's workflows to inspect data, check units and prepare figures. The [skill catalogue](skills/README.md) explains when to use each one and lists its source, licence and companions.

## Project rules and knowledge bases

### What the files do

| File | When to use it |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Shared project instructions. Codex and OpenCode read it from the project. Add context and rules that apply across your tasks. |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code's instruction file. This template imports the neighbouring `AGENTS.md` with `@AGENTS.md`. Put Claude-specific instructions below the import. |

### Rules for research software

| Rule | What to do |
| --- | --- |
| [Branches and pull requests](AGENTS.md#git-branches-and-pull-requests) | Work on a separate branch. With `develop`, open a PR into it and a separate PR when promoting the changes to `main`. In a `main`-only project, open the PR there. Get explicit approval for any direct commit or push to either branch and for each merge. |
| [Branch cleanup](AGENTS.md#git-branches-and-pull-requests) | Delete the temporary working branch after merge, unless the user asks to keep it or another open PR depends on it. |
| [Versioning](AGENTS.md#versioning-on-main) | Before each update to `main`, recommend no bump, a patch, a minor or a major release and give the reason. Follow the project's release policy and flag any effect on compatibility or existing scientific results. |
| [Tests for every new function](AGENTS.md#tests-for-every-new-function) | Add a behaviour-based test when creating a function or method. Use the existing test suite if available; otherwise write a small independent test. Run it and report the command and result, or state why execution is pending. |
| [Docstrings](AGENTS.md#code-documentation-and-physics) | When adding or changing code, document its use cases, an example, the inputs and outputs, and the errors callers may encounter. |
| [Physics in code](AGENTS.md#code-documentation-and-physics) | Explain the model, equations, units, assumptions and limits in the docstring. Use comments beside the calculations to explain the physical reasoning. |
| [Signatures and attribution](AGENTS.md#attribution-and-signatures) | Use the user's authorised identity for commits and signatures. Keep any AI-use disclosure required by the project or publisher. |

Even a short script or a function written directly in chat needs a test. You do not need to introduce an entire testing framework for a one-off function, but you should still check a normal case and meaningful edge cases, and distinguish a test you ran from one you only supplied.

### Keep a local knowledge base

> [!IMPORTANT]
> **Keep scientific work traceable.** Check AI-generated claims and citations against the original sources, and verify calculations and numerical results before relying on them. Use only approved tools and environments for unpublished manuscripts and restricted research data.

Keep checked papers, code revisions and methods notes where the assistant can read them. Record the DOI or original link for each paper and ask the assistant to cite the passage behind each substantive claim. Before sharing unpublished work or restricted data, check which tools and providers can access it. [Research practice](AGENTS.md#research-practice)

[Carsen](https://github.com/LorenzoMugnai/Carsen) is one example. It indexes local files and returns passages with their file paths and line ranges through MCP. You can ask an assistant with terminal access to install it, configure it to index your folders and test a search. [Carsen setup guide for AI agents](https://github.com/LorenzoMugnai/Carsen/blob/main/docs/agent-setup.md)

## What is a skill?

A skill is a folder of instructions for a task you expect to repeat. Its `SKILL.md` tells the assistant when to use it and what steps to follow. Keep any scripts, references or templates the workflow needs in the same folder.

### How the assistant chooses a skill

In clients that support skill discovery, the assistant reads the descriptions of available skills and chooses a relevant workflow for the task. You can also name a skill if you want a specific one. Skills marked **By request** are deliberately not selected automatically: ask for them by name. If a skill is missing, check its installation and the client's settings. Without installed skills, the [chat prompt](#use-the-toolkit-in-a-chat) tells the assistant where to find the public catalogue.

To create your own skill, follow the [instructions in CONTRIBUTING.md](CONTRIBUTING.md#create-a-skill). They include an example `SKILL.md` and a prompt you can give an assistant.

### How the pieces fit together

The project rules and task-specific skills do different jobs. `AGENTS.md` provides guidance shared across research tasks. The assistant can select a matching `SKILL.md` when a task needs one; you do not have to pick it in advance. Claude Code can import the shared rules through `CLAUDE.md`. In a web chat, the prompt above asks the assistant to fetch the same files.

```mermaid
flowchart LR
    TASK["Research task"] --> AI["AI assistant"]
    RULES["AGENTS.md: shared rules"] --> AI
    CLAUDE["CLAUDE.md: Claude Code import"] --> RULES
    AI --> CHOOSE["Check available skills"]
    CHOOSE -->|Relevant skill| SKILL["Matching SKILL.md"]
    CHOOSE -->|No skill needed| WORK["Carry out task"]
    SKILL --> WORK
    WORK --> RESULT["Evidence, tests and reported limits"]
```

Which skills and checks can actually run depends on the client and its available tools. The [installation guide](INSTALL.md) explains how each client finds the rules and skills.

## Optional tools

Claude Code and Codex can show the estimated electricity, water and CO₂e for each reply. The hook uses local token counts and is off by default. Once you have installed it, start the client with `RESEARCH_AI_FOOTPRINT=1 claude` or `RESEARCH_AI_FOOTPRINT=1 codex`. The figures depend on the infrastructure scenario you choose. [AI Footprint setup and methodology](integrations/ai-footprint/README.md)

## Contributing

See the [contribution guide](CONTRIBUTING.md) to propose a rule, add a skill or improve the documentation.

See the [changelog](CHANGELOG.md) for changes or [choose a version](INSTALL.md#choose-a-version) for your installation.

## Licence

The original material in this toolkit is available under the [MIT Licence](LICENSE). This includes the project templates, shared rules, documentation and the `literature-review` skill. Imported skills carry their own licence and copyright notices. [Third-party sources and licences](skills/README.md#sources-and-licences)

## How this repository was made

This entire repository was put together using ChatGPT through its web chat, including the documentation, project templates and integration of the third-party skills. The [skill catalogue](skills/README.md#sources-and-licences) credits the original authors and links to their licences.
