# Changelog

## Unreleased

- Curate the Matt Pocock selection from 27 to 19 skills. Remove `ask-matt`, `grill-me`, `implement-spec`, `teach`, `to-questionnaire`, `wait-what`, `wayfinder` and `wizard`, and trim the tracker templates to match. The [v0.1.0 release](https://github.com/mug-n-ai/research-ai-toolkit/releases/tag/v0.1.0) still contains all 27.
- Replace the introductory exercises with a claim check on [Charbonneau et al. (2002)](examples/literature-review/README.md) and a numerical reproduction of [Anscombe's 1973 quartet](examples/reproduce-analysis/README.md).

## 0.1.0

- Shared research instructions for Codex, Claude Code, OpenCode and chat interfaces that can read public links. The rules cover source verification, confidential materials and research software.
- A catalogue of 33 skills, including the toolkit's literature-review and analysis-reproduction workflows and imported skills for writing, coding and scientific analysis.
- Setup from a shared clone or within one project, with a choice of release or `main` and support for installing selected skills. Automated checks cover catalogue links, skill metadata, supporting files and installation steps.
- Worked examples for checking a claim against a full source and investigating a figure that could only be partly reproduced.
- An opt-in hook for Claude Code and Codex that estimates electricity, water and emissions per reply using local token counts.
