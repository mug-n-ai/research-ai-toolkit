# Skill catalogue

Each link opens a `SKILL.md`. An assistant can [pick an available skill from its description](../README.md#how-the-assistant-chooses-a-skill). In a chat that can open public links, paste the [toolkit prompt](../README.md#use-the-toolkit-in-a-chat) or ask the assistant to read a specific skill and its references. For Codex, Claude Code and OpenCode, use the [installation guide](../INSTALL.md). **By request** marks skills to invoke by name. A workflow that runs code or uses an issue tracker needs a client with those capabilities.

## Original toolkit skills

[Literature review](literature-review/SKILL.md) helps you find and read papers, work out what each study supports and decide which results belong in the synthesis. You can use it for an exploratory search, to revise a draft or to carry out a review with a formal protocol. When you compare studies, record where their evidence agrees and what its limits allow you to conclude.

[Reproduce analysis](reproduce-analysis/SKILL.md) traces a reported result to its inputs and run settings, reruns the workflow and compares the new output with the reference. It includes an optional [reproduction record](reproduce-analysis/reproduction-record.md).

[Run provenance](run-provenance/SKILL.md) records the code revision, configuration, inputs, environment and seeds of each computational run before it starts, such as a simulation, a model training, a data-processing pipeline or a batch analysis, so every figure and number can be traced to the run that made it. It includes an optional [run record](run-provenance/run-record.md). Use `reproduce-analysis` when you later need to rerun a reported result and compare it with the reference.

[Code cleanup](code-cleanup/SKILL.md) checks for dead code, avoidable complexity, duplication and inconsistencies with the project's design choices. For a named function it performs and tests a targeted refactor; for a repository it delivers a prioritised [cleanup plan](code-cleanup/cleanup-plan-template.md) without modifying the code. It complements `codebase-design` and `code-review`, rather than replacing either.

## Scientific analysis

| Skill | When to use it |
| --- | --- |
| [Exploratory data analysis](exploratory-data-analysis/SKILL.md) | Check the structure of local data, missing values, outliers and sensitivity to transformations before fitting a model. The core tools handle CSV, TSV and JSON. See the skill's capability matrix for other formats. |
| [Uncertainty and units](uncertainty-and-units/SKILL.md) | Check dimensions and orders of magnitude, propagate correlated uncertainties and report what an uncertainty interval means. |
| [Scientific visualisation](scientific-visualization/SKILL.md) | Build or audit figures from your data. Check how the plot shows uncertainty, missing data and comparisons, then choose a suitable export format. |

The three skills in this section come from K-Dense. They include optional local Python tools. Check the requirements in each skill for the workflow you need.

## Writing

[No AI Slop](no-ai-slop/SKILL.md), by [Peter Yang](https://github.com/petergyang/no-ai-slop), spots stock phrases, vague attributions and emphasis that adds little to a draft. Ask for a list of passages to revisit, or ask for an edit and a short account of what changed. For abstracts, reports and outreach copy, use it after you are happy with the substance. Check that any edit preserves the original claims, citations and uncertainty. The [editing checks](no-ai-slop/eval.md) cover both clarity and the author's voice. A flagged phrase tells you where the prose can improve. It gives you no basis for deciding who wrote the draft.

## Matt Pocock's skills

[Matt Pocock's collection](https://github.com/mattpocock/skills) gives the assistant a workflow for decisions that often get skipped when you go straight from a prompt to code. For example, if you are changing how a pipeline treats missing measurements, use `grill-with-docs` to agree what counts as missing, then `tdd` to cover the cases you decide to support. Start with `research` if the decision turns on what a library or a paper actually says.

### Installing a selection

If you [install only some skills](../INSTALL.md#install-a-selection), start with the workflow you want to use and read its **Companions** column. When it calls another skill, include that folder and check its row too. For example, to use `grill-with-docs`, select `grill-with-docs`, `grilling` and `domain-modeling`. Add companions marked for particular tasks when you need those parts of the workflow.

### Research software

| Skill | When to use it | Companions |
| --- | --- | --- |
| [research](research/SKILL.md) | Ask a background agent to investigate a software question, such as library, API or tool behaviour, against primary sources and write a cited Markdown note. For papers and scientific claims, use `literature-review`. | |
| [grill-with-docs](grill-with-docs/SKILL.md) | Work through a design and record terms and durable decisions in a glossary and architecture decision records (ADRs). By request. | `grilling`, `domain-modeling` |
| [domain-modeling](domain-modeling/SKILL.md) | Agree what a term means in your code and capture decisions future maintainers need to understand. | |
| [prototype](prototype/SKILL.md) | Try an interface or state model in a disposable prototype before committing to a design. | |
| [to-spec](to-spec/SKILL.md) | Turn an agreed discussion into a spec on your configured tracker. By request. | `setup-matt-pocock-skills` |
| [to-tickets](to-tickets/SKILL.md) | Break an agreed plan into small, testable tickets and record what blocks each one. By request. | `setup-matt-pocock-skills` |
| [setup-matt-pocock-skills](setup-matt-pocock-skills/SKILL.md) | Set up the tracker, triage labels and location of the glossary and decision records in a project. By request. | |
| [triage](triage/SKILL.md) | Decide what each issue needs next and apply the project's triage labels. By request. | `setup-matt-pocock-skills`, plus `grilling` and `domain-modeling` as needed |
| [tdd](tdd/SKILL.md) | Change a small piece of behaviour by writing a test that fails first, implementing the change and running the test again. | `codebase-design` for interface questions |
| [diagnosing-bugs](diagnosing-bugs/SKILL.md) | Reproduce a bug or performance regression, narrow it down, test a fix and capture a regression check. | |
| [implement](implement/SKILL.md) | Carry out a spec or set of tickets on the current branch with tests and review. By request. | `tdd`, `code-review` |
| [code-review](code-review/SKILL.md) | Review a diff against both the project's coding standards and the scope of the original spec. | `setup-matt-pocock-skills` |
| [pr](pr/SKILL.md) | Write a pull request description with a clear summary, before-and-after evidence and the risks of merging. | |
| [codebase-design](codebase-design/SKILL.md) | Evaluate module boundaries and design interfaces that callers can use and test. | |
| [improve-codebase-architecture](improve-codebase-architecture/SKILL.md) | Survey the code and discuss where a different module boundary could make it easier to change or test. By request. | `codebase-design`, `grilling`, `domain-modeling` |
| [retro](retro/SKILL.md) | Use a recent coding session to find friction in the project instructions, tools or checks. By request. | `writing-for-agents` |

### Planning, handovers and learning

| Skill | When to use it | Companions |
| --- | --- | --- |
| [grilling](grilling/SKILL.md) | Work through open questions in dependency order, using the repo for facts it already answers. | |
| [handoff](handoff/SKILL.md) | Give the next session enough context to pick up work without rereading the whole conversation. By request. | |
| [writing-for-agents](writing-for-agents/SKILL.md) | Write or revise agent instructions and skills so the essential guidance is easy to find. | |

## Sources and licences

- **Literature review** is a toolkit contribution by Lorenzo V. Mugnai. See its [MIT licence](literature-review/LICENSE).
- **Reproduce analysis** is an original toolkit skill under the [MIT licence](reproduce-analysis/LICENSE).
- **Code cleanup** is an original toolkit skill under the [MIT licence](code-cleanup/LICENSE).
- **Run provenance** is an original toolkit skill under the [MIT licence](run-provenance/LICENSE).
- **Scientific analysis skills** come from [K-Dense Scientific Agent Skills at commit `ec59a29`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/ec59a29a03d5c40f73ab40878df04860bc00e876). Each imported folder includes the upstream MIT notice. The toolkit copies use the client's usual tool permissions, and the units skill's commands resolve from its own directory. To keep the main instructions short, the toolkit moves the CLI details, pinned versions and dated source lists verbatim from each `SKILL.md` into `references/cli-reference.md`, `references/version-baseline.md` or `references/sources.md`, leaving a short pointer. The units skill's description is shortened to stay within the toolkit's length limit.
- **No AI Slop** comes from [Peter Yang's repository at commit `000650b`](https://github.com/petergyang/no-ai-slop/tree/000650b156983f5159695b441477f4e63b25dc85). Its [MIT licence](no-ai-slop/LICENSE) is included with the skill.
- **Matt Pocock's collection** comes from [commit `5863806`](https://github.com/mattpocock/skills/tree/5863806dd4e15c63174bee4e7515a4256792ecfa). This toolkit includes a selection of 19 skills from that snapshot. The tracker templates omit the Wayfinder setup. The [v0.1.0 release](https://github.com/mug-n-ai/research-ai-toolkit/releases/tag/v0.1.0) includes the original collection of 27. Each directory includes the MIT licence, and [`pr`](pr/CREDITS.md) also includes the [HumanLayer MIT notice](pr/LICENSE-HUMANLAYER) for the credited `show-me` material. The toolkit replaces the one-line `pr` description with one that says what the skill produces and when to use it. The `pr` credit is a text field in the YAML for compatibility with Agent Skills metadata. The toolkit narrows the `research` description to software documentation, APIs and source code, so that questions about papers and scientific claims go to `literature-review`. The workflow itself is unchanged.

## Skill format

Give each skill its own directory under `skills/`. The main file is `skills/<skill-name>/SKILL.md`. It starts with YAML front matter containing `name`, `description` and `license`, followed by the Markdown workflow. The `license` value must match the bundled `LICENSE` file. A skill the assistant can select by itself needs a description of 80 to 600 characters, because that text is loaded into every session and decides when the skill is used. Move long reference material into files alongside `SKILL.md`. Use the same lowercase, hyphenated name for the directory and the `name` field. Write the description so someone can tell which task calls for the skill.

The workflow can state what inputs the assistant needs, what it should produce and how to check the result. Keep any references or templates alongside the skill and link to them with relative paths so the directory can be copied as a unit.

See the [Agent Skills specification](https://agentskills.io/specification) for the file format and the [setup guide](../INSTALL.md#copying-skills) for installation paths.
