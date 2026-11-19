---
name: code-cleanup
description: Identify dead code, needless complexity, duplication and deviations from existing implementation principles. Use for clean-code audits, safe refactoring or DRY improvements. For a named function, make and verify a focused refactor; for an entire repository, report a prioritised cleanup plan without changing code.
license: MIT
metadata:
  author: Lorenzo V. Mugnai
---

# Code cleanup

Improve maintainability without changing what the software promises or the science it implements. Prefer a clear, traceable implementation over the shortest implementation. Follow the repository's rules in `AGENTS.md` and any more specific project instructions.

## Decide the scope and action

- **Function or small, explicitly named code region:** inspect its callers and tests, then perform a focused refactor in the allowed work area. Show the code change and evidence of equivalent behaviour. Do not silently expand into a repository-wide rewrite. If the function is supplied in chat with no writable repository, return both the revised function and a runnable test.
- **Whole repository:** inspect the codebase and deliver a prioritised action plan using [the cleanup plan template](cleanup-plan-template.md). This is **analysis-only**: do not delete, rewrite, format, commit or push implementation files. Ask for approval before carrying out any of the proposed stages. A request to "audit" or "review" is analysis-only even when the scope is a function.
- **Named file, package or module:** use the repository audit/report workflow by default, constrained to that scope. Only change code if the user explicitly asks to refactor or clean it.
- When in doubt, pick the least destructive interpretation. Record the scope you covered and any paths you could not inspect.

## 1. Understand the implementation before judging it

Read the relevant files, their callers and tests, project instructions, documentation, architecture decision records (ADRs), glossary, build and plugin configuration and, where useful, recent changes. Identify what the code does, its supported callers and user-facing contracts. Do not infer a design philosophy from the language or the presence of classes alone.

Describe the actual implementation approach in ordinary terms: e.g. pure functions and explicit data flow, layered interfaces, object-oriented state, numerical vectorisation, dependency injection, plugins, or deliberately explicit scientific calculations. Identify decisions that are consistent with this approach and candidates that depart from it. Separate a demonstrated inconsistency from a stylistic preference. If there is insufficient evidence, label the inferred philosophy as tentative.

## 2. Find potential dead code

Inspect unreachable branches, unused imports and variables, unused functions and methods, unused files, duplicate entry points, stale configuration and obsolete compatibility layers. Choose ecosystem-appropriate tooling **when available** (for example, Ruff and Vulture in Python, or Knip in TypeScript), and supplement it with import/call-site searches, configuration, tests and documented external usage. Do not install or run an untrusted tool without the relevant permissions.

**A static-analysis warning is a candidate, not proof.** Check dynamic imports, reflection, plugin registries, CLI and notebook entry points, callbacks, serialisation, public/library APIs and external callers. Treat absence of references in the repository as weaker evidence for exported public functions. Mark each finding as `confirmed`, `probable` or `uncertain` and give the evidence. Never delete uncertain code automatically; document its possible external role.

## 3. Examine complexity, duplication and clarity

Look for excessive nesting, large multi-purpose functions, repeated branches, redundant indirection, state that could be local, unnecessary transformations, repeated calculations, opaque naming and avoidable dependencies. Where useful, measure cyclomatic/cognitive complexity or profile a hot path, and record the tool and limitations.

Apply **DRY to duplicated knowledge or behaviour**, not merely similar syntax. Two apparently similar routines may encode different physical assumptions, algorithms, boundary conditions or validity regimes. Check these distinctions before suggesting a shared implementation. Conversely, avoid helper extraction that increases navigation cost or makes a simple operation harder to understand. Prefer the smallest useful change consistent with the project's documented design.

Consult `codebase-design` for substantial interface or module-boundary questions. Use `code-review` to review the eventual diff, `diagnosing-bugs` for suspected bugs and `tdd` when a test-first loop is appropriate. These are optional companions; do not require a tracker, extra agents or an HTML report for a small cleanup.

## 4. Establish a verification baseline

Before editing, determine which contracts must remain unchanged: public signatures, accepted inputs, outputs and shapes, error behaviour, side effects, data formats, determinism, performance requirements and backwards compatibility. Run existing tests if possible and record the baseline. For a function without tests, create a focused behaviour-based test before refactoring, following [the toolkit testing rule](../../AGENTS.md#tests-for-every-new-function).

For scientific and numerical code, also preserve the underlying physical model, equations, units, valid regimes, boundary conditions, uncertainties and scientific interpretation. Compare with independent expected results, analytic limits or recorded reference outputs. Set justified numerical tolerances before comparing. Floating-point reordering, parallel execution and vectorisation can change numerical results; a performance improvement is not proof of equivalence.

If a baseline or dependency cannot be reproduced, record the gap; do not claim the proposed change is safe merely because static checks pass.

## 5A. Function mode: refactor and verify

1. Keep the public contract and intended behaviour fixed. Make the smallest improvement supported by the evidence; avoid speculative architecture changes or changing unrelated callers.
2. Remove confirmed dead paths, simplify flow, reduce justified duplication and improve names and local structure. If a suspected defect changes expected behaviour, report it separately rather than silently mixing a bug fix into the cleanup.
3. Update docstrings and explanatory comments, including usage, parameters, results, exceptions and physical reasoning where relevant. Apply the [code documentation rule](../../AGENTS.md#code-documentation-and-physics).
4. Add or update a corresponding behavioural test for each newly created function. Use the existing test directory if present. If none exists, create a small standalone test (or return it alongside a chat-only snippet). Existing functions being refactored must retain tests that check their observed behaviour; add regression tests where coverage is missing. Include normal and meaningful edge or error cases.
5. Run focused and relevant project tests, linting and any numerical or performance checks that matter. Compare before and after. If execution is unavailable, give the runnable tests and say explicitly that they were not run.
6. Report the code changed, why it is simpler, what was removed, and the observed checks. Do not commit, push or merge without respecting the project's Git approval rules.

## 5B. Repository mode: produce an action plan only

Survey the important code paths, entry points, tests, dependencies and historical decisions. If the repository is too large to inspect fully, sample deliberately, report coverage and identify what still needs inspection. Do not claim a full audit when only some directories were read.

Use [the cleanup plan template](cleanup-plan-template.md). For each candidate state:
- file and function/line range, evidence and confidence;
- why it matters, with the relevant design principle and any DRY or complexity trade-off;
- proposed smallest change, expected benefit, compatibility/scientific risk and tests needed;
- effort and priority, favouring low-risk changes with clear verification.

Group related changes into small stages, each independently reviewable and testable. Identify baseline gaps and order the work so safe deletions and clearly redundant complexity are handled before high-risk scientific or architectural refactors. No code changes are authorised by delivery of the plan.

## Completion rules

- Do not equate fewer lines with cleaner code.
- Do not invent usage evidence, benchmark results, test outcomes or tool runs.
- Report what could and could not be inspected, and distinguish confirmed dead code from candidates.
- A new function is not finished without its associated test or an explicit execution blocker and runnable test.
- Use existing project conventions; do not impose a new architectural philosophy for appearance alone.
