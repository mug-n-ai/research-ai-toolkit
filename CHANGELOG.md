# Changelog

## 0.4.1

- Follow the project's design, error-handling and testing conventions when extending code. Use existing tests and interfaces for TDD when the expected behaviour is clear, check for reusable implementations before adding dependencies or algorithms, and verify affected scientific outputs during review. Link relevant run records in session handoffs.
- Ask assistants to share what they found, what they would change and how they would check it before editing code for a feature, a substantial change or an issue that needs investigation. Quick fixes and work covered by an approved plan can proceed directly.
- Write or extend a focused test before implementing a new behaviour or fixing a bug when practical. Check that it fails for the expected reason before the change and passes afterwards.
- Document the estimated context cost and show how to install a smaller selection of rules and skills.

## 0.4.0

- Split the shared rules into modules under `rules/`. `AGENTS.md` now holds only the rules, generated from the modules, and the project starter with empty context and workflow sections moves to `templates/AGENTS.md`. You can import single modules to load only the rules you want in every session. CI fails if a generated file is out of date.
- Add `scripts/install.py`, an installer for Claude Code, OpenCode and Codex. It links skills, loads the rules, supports skill and rule selection, `--dry-run` and `--uninstall`, and removes links to skills that no longer exist. It leaves personal skills, manual imports and commented OpenCode configurations untouched and reports them.
- Add `run-provenance`, an original skill that records the code revision, configuration, inputs, environment and seeds of each computational run (simulation, model training, pipeline or batch analysis) before it starts.
- Narrow the `research` description to software documentation, APIs and source code, so that questions about papers go to `literature-review`.
- Add skill routing checks in `evals/` with a script that runs them in Claude Code.
- Require a `license` field in every `SKILL.md` that matches its `LICENSE`, and an 80 to 600 character description for skills the assistant selects by itself. Expand the `pr` description and shorten the `uncertainty-and-units` one.
- Move the CLI details, version pins and source lists of the three K-Dense skills verbatim into reference files to shorten their `SKILL.md`.
- Replace the non-portable `cp -n` in the project setup with an explicit check for an existing file.

- Explain near the start that assistants can select relevant installed skills from a task description without the user naming them. Clarify opt-in skills and web-chat limitations, and make the workflow examples and diagram reflect automatic selection.
- Refine the README with a short project description, live release, CI and skill-count badges, and a linked row of supported clients.
- Add two GitHub alerts for installation and responsible research use, make the web-chat prompt collapsible, and explain how shared rules and selected skills fit together in a Mermaid diagram.
- Keep the existing table of contents, with no logo or extra navigation block.

## 0.3.0

- Add `code-cleanup` to analyse dead code, unnecessary complexity, duplication and design consistency. It refactors and tests a named function, or prepares a prioritised action plan for an entire repository without changing the implementation.
- Require a behaviour-based test whenever a new function or method is written, including standalone research scripts or one-off snippets without a test suite. Document how to run the test and report actual results or execution limits.
- Add skill discovery, usage examples and testing guidance to the README and skill catalogue.

## 0.2.0

- Curate the Matt Pocock selection from 27 to 19 skills. Remove `ask-matt`, `grill-me`, `implement-spec`, `teach`, `to-questionnaire`, `wait-what`, `wayfinder` and `wizard`, and trim the tracker templates to match. The [v0.1.0 release](https://github.com/mug-n-ai/research-ai-toolkit/releases/tag/v0.1.0) still contains all 27.
- Replace the introductory exercises with a claim check on [Charbonneau et al. (2002)](examples/literature-review/README.md) and a numerical reproduction of [Anscombe's 1973 quartet](examples/reproduce-analysis/README.md).

## 0.1.0

- Shared research instructions for Codex, Claude Code, OpenCode and chat interfaces that can read public links. The rules cover source verification, confidential materials and research software.
- A catalogue of 33 skills, including the toolkit's literature-review and analysis-reproduction workflows and imported skills for writing, coding and scientific analysis.
- Setup from a shared clone or within one project, with a choice of release or `main` and support for installing selected skills. Automated checks cover catalogue links, skill metadata, supporting files and installation steps.
- Worked examples for checking a claim against a full source and investigating a figure that could only be partly reproduced.
- An opt-in hook for Claude Code and Codex that estimates electricity, water and emissions per reply using local token counts.
