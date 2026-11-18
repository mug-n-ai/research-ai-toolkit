# Changelog

## Unreleased

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
