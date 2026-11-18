# Skill catalogue

Each link opens a `SKILL.md`. In ChatGPT, ask to read that file and the supporting files it names. In Claude Code or OpenCode, [copy the skill directory into your project](../INSTALL.md#copying-skills). **By request** marks skills to invoke by name. A workflow that writes files, uses an issue tracker or delegates work needs a client with those capabilities.

## Original toolkit skills

[Literature review](literature-review/SKILL.md), by Lorenzo V. Mugnai, helps you find and read academic sources, check which claims each paper supports and decide what belongs in the synthesis. It works for an exploratory search, an update to an existing text or a review with a formal protocol. Use it when the outcome depends on the strength and limits of the evidence across studies.

## Writing

[No AI Slop](no-ai-slop/SKILL.md), by [Peter Yang](https://github.com/petergyang/no-ai-slop), spots stock phrases, vague attributions and emphasis that adds little to a draft. Ask for a list of passages to revisit, or ask for an edit and a short account of what changed. For abstracts, reports and outreach copy, use it after you are happy with the substance. Check that any edit preserves the original claims, citations and uncertainty. The [editing checks](no-ai-slop/eval.md) cover both clarity and the author's voice. A flagged phrase tells you where the prose can improve. It gives you no basis for deciding who wrote the draft.

## Matt Pocock's skills

[Matt Pocock's collection](https://github.com/mattpocock/skills) gives the assistant a workflow for decisions that often get skipped when you go straight from a prompt to code. For example, if you are changing how a pipeline treats missing measurements, use `grill-with-docs` to agree what counts as missing, then `tdd` to cover the cases you decide to support. Start with `research` if the decision turns on what a library or a paper actually says.

### Research software

| Skill | When to use it | Companions |
| --- | --- | --- |
| [ask-matt](ask-matt/SKILL.md) | Find a workflow for the stage you are at. By request. | Install the skills you want it to suggest. |
| [research](research/SKILL.md) | Ask a background agent to investigate a question against primary sources and write a cited Markdown note. | |
| [grill-with-docs](grill-with-docs/SKILL.md) | Work through a design and record terms and durable decisions in a glossary and architecture decision records (ADRs). By request. | `grilling`, `domain-modeling` |
| [domain-modeling](domain-modeling/SKILL.md) | Agree what a term means in your code and capture decisions future maintainers need to understand. | |
| [prototype](prototype/SKILL.md) | Try an interface or state model in a disposable prototype before committing to a design. | |
| [to-spec](to-spec/SKILL.md) | Turn an agreed discussion into a spec on your configured tracker. By request. | `setup-matt-pocock-skills` |
| [to-tickets](to-tickets/SKILL.md) | Break an agreed plan into small, testable tickets and record what blocks each one. By request. | `setup-matt-pocock-skills` |
| [wayfinder](wayfinder/SKILL.md) | Map the open decisions in a project that spans several sessions. By request. | `setup-matt-pocock-skills`, `grilling`, `domain-modeling`, plus `research` and `prototype` as needed |
| [setup-matt-pocock-skills](setup-matt-pocock-skills/SKILL.md) | Set up the tracker, triage labels and location of the glossary and decision records in a project. By request. | |
| [triage](triage/SKILL.md) | Decide what each issue needs next and apply the project's triage labels. By request. | `setup-matt-pocock-skills`, plus `grilling` and `domain-modeling` as needed |
| [tdd](tdd/SKILL.md) | Change a small piece of behaviour by writing a test that fails first, implementing the change and running the test again. | `codebase-design` for interface questions |
| [diagnosing-bugs](diagnosing-bugs/SKILL.md) | Reproduce a bug or performance regression, narrow it down, test a fix and capture a regression check. | |
| [implement](implement/SKILL.md) | Carry out a spec or set of tickets on the current branch with tests and review. By request. | `tdd`, `code-review` |
| [implement-spec](implement-spec/SKILL.md) | Implement a larger spec on an integration branch, using separate agents for tickets that can proceed in parallel. By request. | `setup-matt-pocock-skills`, `tdd`, `code-review` |
| [code-review](code-review/SKILL.md) | Review a diff against both the project's coding standards and the scope of the original spec. | `setup-matt-pocock-skills` |
| [pr](pr/SKILL.md) | Write a pull request description with a clear summary, before-and-after evidence and the risks of merging. | |
| [codebase-design](codebase-design/SKILL.md) | Evaluate module boundaries and design interfaces that callers can use and test. | |
| [improve-codebase-architecture](improve-codebase-architecture/SKILL.md) | Survey the code and discuss where a different module boundary could make it easier to change or test. By request. | `codebase-design`, `grilling`, `domain-modeling` |
| [retro](retro/SKILL.md) | Use a recent coding session to find friction in the project instructions, tools or checks. By request. | `writing-for-agents` |
| [wizard](wizard/SKILL.md) | Generate a guided shell script for setup or migration steps that need a person at the keyboard. | |

### Planning, handovers and learning

| Skill | When to use it | Companions |
| --- | --- | --- |
| [grill-me](grill-me/SKILL.md) | Test a plan or a decision through questions before acting on it. By request. | `grilling` |
| [grilling](grilling/SKILL.md) | Work through open questions in dependency order, using the repo for facts it already answers. | |
| [handoff](handoff/SKILL.md) | Give the next session enough context to pick up work without rereading the whole conversation. By request. | |
| [teach](teach/SKILL.md) | Learn a concept over several sessions with a record of progress and resources. By request. | |
| [to-questionnaire](to-questionnaire/SKILL.md) | Turn open decisions into a short Markdown questionnaire for the colleague who can answer them. By request. | |
| [wait-what](wait-what/SKILL.md) | Ask for a clearer explanation of the last answer in the terms used by the project. By request. | |
| [writing-for-agents](writing-for-agents/SKILL.md) | Write or revise agent instructions and skills so the essential guidance is easy to find. | |

## Sources and licences

- **No AI Slop** comes from [Peter Yang's repository at commit `000650b`](https://github.com/petergyang/no-ai-slop/tree/000650b156983f5159695b441477f4e63b25dc85). Its [MIT licence](no-ai-slop/LICENSE) is included with the skill.
- **Matt Pocock's collection** comes from [commit `5863806`](https://github.com/mattpocock/skills/tree/5863806dd4e15c63174bee4e7515a4256792ecfa). This snapshot contains the 27 skills in the upstream plugin manifest. Each directory includes the MIT licence, and [`pr`](pr/CREDITS.md) also includes the [HumanLayer MIT notice](pr/LICENSE-HUMANLAYER) for the credited `show-me` material. The `pr` credit is a text field in the YAML for compatibility with Agent Skills metadata.

## Skill format

Give each skill its own directory under `skills/`. The main file is `skills/<skill-name>/SKILL.md`. It starts with YAML front matter containing `name` and `description`, followed by the Markdown workflow. Use the same lowercase, hyphenated name for the directory and the `name` field. Write the description so someone can tell which task calls for the skill.

The workflow can state what inputs the assistant needs, what it should produce and how to check the result. Keep any references or templates alongside the skill and link to them with relative paths so the directory can be copied as a unit.

See the [Agent Skills specification](https://agentskills.io/specification) for the file format and the [setup guide](../INSTALL.md#copying-skills) for installation paths.
