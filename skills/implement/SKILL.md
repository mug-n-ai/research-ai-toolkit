---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
license: MIT
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Before adding a dependency or reimplementing an algorithm, check the project's existing utilities, tests and dependencies. Use `research` when a comparison of external options would change the plan.

Use `tdd` where practical. Follow its guidance on when the expected behaviour needs clarification.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, call the Skill tool with "code-review" to review the work.

Commit your work to the current branch.
