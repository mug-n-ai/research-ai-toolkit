# Research AI Toolkit

[![Licence: MIT](docs/badges/licence.svg)](LICENSE)
[![Agent Skills: Catalogue](docs/badges/skills.svg)](skills/README.md)
[![Contributions welcome](docs/badges/contributing.svg)](CONTRIBUTING.md)

Use this toolkit when you want an AI assistant to help with your own research, from checking the evidence behind a draft to rerunning an analysis. The department shares the repository, and contributors from different research groups can add workflows that others can use in their own projects.

## Choose your tool

| Tool | How to use the toolkit |
| --- | --- |
| Chat interfaces | Use the prompt below in any chat that can open public links, or share the files directly. |
| Claude Code | Use one local clone for all your projects, or copy the files into a single project. [Claude Code setup](INSTALL.md#claude-code-from-the-clone) |
| OpenCode | Point OpenCode at the same clone, or copy the files into a single project. [OpenCode setup](INSTALL.md#opencode-from-the-clone) |

## Use the toolkit in a chat

Paste this prompt into ChatGPT, Claude, or any other assistant that can open public links. Replace the last line with your task. The assistant can then read the rules and choose a relevant workflow for that conversation.

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

If the assistant cannot open the links, paste or attach [`AGENTS.md`](AGENTS.md), the relevant `SKILL.md` and any supporting files it needs. For a project that already uses the toolkit, share its own instruction file for project-specific details.

## What is a skill?

A skill is a folder of instructions for a task you expect to do again. If you check a simulation's convergence every time you change the grid, a skill can tell the assistant which runs to compare, what to report and when to flag a discrepancy. `AGENTS.md` holds the rules that apply across the project. The skill holds the steps for this particular check.

### How the assistant chooses a skill

Once a skill is installed and available in the current project or workspace, the assistant can pick it up from a normal request. For example, “Check what evidence supports this paragraph” can bring in `literature-review` if its description matches the task. The assistant can use the name and description to decide what fits and then load the instructions in `SKILL.md`. You can name the skill if you want a particular workflow or if the assistant misses it.

Claude Code, Codex, OpenCode and ChatGPT workspaces with Skills enabled support automatic selection for eligible skills. Request any skill marked **By request** by name. Your client settings also affect which skills are available and which can be picked automatically. [Claude Code skills](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) · [ChatGPT and Codex skills](https://learn.chatgpt.com/docs/build-skills) · [OpenCode skills](https://opencode.ai/docs/skills/#loading)

If you are using the public toolkit without installing it, paste the [chat prompt above](#use-the-toolkit-in-a-chat) to give the assistant the catalogue for that conversation. If a specific workflow matters, give it the link to that skill's `SKILL.md`.

### Create a skill

1. Pick a task you do more than once. Write down the inputs, the expected output and how you check the result.
2. Create `skills/<skill-name>/SKILL.md` in the toolkit. Start with a YAML header containing `name` and `description`, then write the workflow in Markdown. Use a lowercase, hyphenated name that matches the folder. The description should say what the skill does and when to use it.
3. Keep any templates or reference files in the skill folder and link to them from `SKILL.md` with relative paths. Try the instructions on a real example and a case with missing inputs. Add the skill to the [catalogue](skills/README.md) if you are contributing it to the toolkit.

For example, save this file as `skills/check-simulation-convergence/SKILL.md`.

```markdown
---
name: check-simulation-convergence
description: Compare results across grid resolutions. Use after a simulation grid changes or when checking convergence.
---

# Check simulation convergence

1. Take the run outputs, the quantity to compare and the tolerance.
   Ask for any input that is missing.
2. Check that the runs use the same physical setup and report in the same units.
   Compare the quantity between successive resolutions.
3. Return a table with the resolutions, values and differences. State which
   comparisons meet the tolerance and which still need checking.
```

### Ask Claude or ChatGPT to write it

Copy this prompt and replace the examples in brackets with details from your project.

```text
Create a reusable Agent Skill for [task we repeat].
It should take [inputs] and produce [output].
Here is an example of how we do it now [paste an example or link to it].
The result is ready when [checks].

Write a SKILL.md with a name and a description that says when to use it.
Include the steps, the checks and what to do if an input is missing.
Add supporting files only if the workflow needs them and link them by
relative path. Show how to try the skill on the example above.
```

In **Claude Code**, ask it to write the folder under `.claude/skills/` in your project, then try `/<skill-name>`. For **OpenCode**, use `.opencode/skills/`. If you are contributing to this toolkit, keep the source under `skills/` and follow the [installation guide](INSTALL.md#copying-skills) to try it in a project.

In **ChatGPT or Claude in a browser**, ask for the complete `SKILL.md` and any supporting files. You can attach them or paste the instructions into a new chat and ask the assistant to apply them. If your ChatGPT workspace has a **Skills** menu, you can also create or upload skills there under **Create**. [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)

## Original toolkit contributions

### Literature review

Use `literature-review` when you need to find papers for a new question, check what supports a claim in a draft, or pick up a reading list over several sessions.

- **Rule.** Read each source used as evidence in full and inspect the figures in the original paper. For each substantive claim, point to the passage that supports it. Carry the study's assumptions and limits into the result. [Research practice](AGENTS.md#research-practice)
- **Skill.** Compare what the papers support and use that evidence to decide what belongs in the text. The optional review record keeps track of the sources, the claims they support and how you decided to use the figures. [Literature review skill](skills/literature-review/SKILL.md)

### Reproduce an analysis

Use `reproduce-analysis` when you have a figure, table or number and want to find out whether you can get it again. Trace it to the inputs, code revision, environment, configuration and random seeds. Rerun the workflow in a separate output directory and record what matches, what differs and what you could not check. [Reproduce analysis skill](skills/reproduce-analysis/SKILL.md)

### Rules for research software

| Rule | What to do |
| --- | --- |
| [Branches and pull requests](AGENTS.md#git-branches-and-pull-requests) | Work on a separate branch. With `develop`, open a PR into it and a separate PR when promoting the changes to `main`. In a `main`-only project, open the PR there. Get explicit approval for any direct commit or push to either branch and for each merge. |
| [Branch cleanup](AGENTS.md#git-branches-and-pull-requests) | Delete the temporary working branch after merge, unless the user asks to keep it or another open PR depends on it. |
| [Versioning](AGENTS.md#versioning-on-main) | Before each update to `main`, recommend no bump, a patch, a minor or a major release and give the reason. Follow the project's release policy and flag any effect on compatibility or existing scientific results. |
| [Docstrings](AGENTS.md#code-documentation-and-physics) | When adding or changing code, document its use cases, an example, the inputs and outputs, and the errors callers may encounter. |
| [Physics in code](AGENTS.md#code-documentation-and-physics) | Explain the model, equations, units, assumptions and limits in the docstring. Use comments beside the calculations to explain the physical reasoning. |
| [Signatures and attribution](AGENTS.md#attribution-and-signatures) | Use the user's authorised identity for commits and signatures. Keep any AI-use disclosure required by the project or publisher. |

## Third-party skills for research work

- **Review a draft.** No AI Slop flags vague attributions, stock phrases and inflated wording. It can report the passages to check or make a light edit that preserves the author's voice. [No AI Slop](skills/README.md#writing)
- **Plan and check research software.** Matt Pocock's skills help you work through a design before writing code, trace answers to primary sources, reproduce bugs and test changes in small steps. [Matt Pocock's skills](skills/README.md#matt-pococks-skills)
- **Check data, calculations and plots.** Use K-Dense's skills to inspect missing data and outliers, check units and propagate uncertainty, or prepare a figure that shows the data clearly. [Scientific analysis skills](skills/README.md#scientific-analysis)

## Keep a local knowledge base

If you ask an assistant why a parameter was fixed in an analysis, the answer should point you to the code, the methods notes or the paper that explains the choice. A plausible answer can still get the reason wrong. Keep the sources your project relies on in a local repository or folder so the assistant has somewhere specific to look.

Start with the papers you have checked, the versions of the code used in the analysis, and your notes on how decisions were made. Keep the DOI or original link for each paper and record the relevant version or commit where you can. Ask the assistant to cite the file and the relevant passage for each claim that matters. Check that the passage supports the claim, especially before using it in a paper or analysis. If the sources leave a question open, ask the assistant to say what evidence is missing.

### Search the sources with Carsen

Carsen is one example of a tool you can use to search a local knowledge base. You can use another search tool or work directly with the files in your repository.

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

## Contributing

See the [contribution guide](CONTRIBUTING.md) to propose a rule, add a skill or improve the documentation.

## Licence

The original material in this toolkit is available under the [MIT Licence](LICENSE). This includes the project templates, shared rules, documentation and the `literature-review` skill. Imported skills carry their own licence and copyright notices. [Third-party sources and licences](skills/README.md#sources-and-licences)

## How this repository was made

This entire repository was put together using ChatGPT through its web chat, including the documentation, project templates and integration of the third-party skills. The [skill catalogue](skills/README.md#sources-and-licences) credits the original authors and links to their licences.
