# Code cleanup plan

> Use this for a repository, package or module audit. This report is analysis-only. Do not edit implementation files until the user approves the work.

## Scope and evidence
- Repository, revision and inspected paths:
- Excluded or inaccessible paths:
- Commands and tools actually run:
- Tests and scientific reference outputs currently available:
- What could not be verified:

## Existing implementation approach
Describe the observed architectural or programming principles and cite files or project decisions that support this reading. Mark uncertain inferences.

## Findings

| Priority | Location | Finding and evidence | Confidence | Suggested action | Behaviour/science risk | Tests and checks | Effort |
| --- | --- | --- | --- | --- | --- | --- | --- |
| High / Medium / Low | `path:line` | What is duplicated, unused or needlessly complex; how it was checked | Confirmed / Probable / Uncertain | Smallest appropriate change | API, numerical, external-caller and other risks | Existing test and any needed new regression | S / M / L |

## Recommended stages
1. **Baseline:** record test commands, reference outputs, supported public callers and relevant tolerances.
2. **Low-risk cleanup:** candidates with clear evidence and focused tests.
3. **Local simplification:** refactor independent functions or modules with before/after checks.
4. **Structural work:** only after separately reviewing interfaces, dependencies and scientific assumptions.

For each stage, list the files, verification commands, dependencies and rollback route. Distinguish proposed work from work that has actually been completed.

## Decisions needed
- Which candidates are approved?
- Are any public interfaces or numerical results allowed to change?
- What additional data, tests or references are needed before proceeding?
