# Project instructions

## Project context

<!-- Add a short description of the project and point to any files that explain its structure. -->

## Research practice

<!-- Add any guidance that applies to your research projects. -->

- **Literature review.** Read each source used as evidence in full and inspect its figures directly in the original paper. Record what you were able to read and see. Trace substantive claims to specific passages in the original sources and carry their assumptions and limitations into the synthesis. Use `literature-review` for the full workflow.
- When reviewing a draft, preserve its scientific claims, citations, units and degree of certainty. Use `no-ai-slop` for style feedback or a light edit when requested.
- Use a task-specific skill when it fits the work. In a chat without installed skills, read the public skill files or use the copies provided by the user. The [skill catalogue](https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/refs/heads/main/skills/README.md) explains when to use each one.

### Git branches and pull requests

- Start code changes on a working branch. Get the user's explicit approval before committing or pushing directly to `develop` or `main`.
- When the project uses `develop`, open a pull request from the working branch into `develop`. To promote the changes into `main`, open a separate pull request from `develop` into `main`. In a project that uses `main` as its integration branch, open the pull request from the working branch into `main`.
- For each pull request, share its link and ask the user to confirm the merge before running it. Approval to open the pull request or merge into `develop` does not approve a merge into `main`. Enable auto-merge only with explicit approval for that pull request.

- After a pull request merges, delete its temporary working branch by default. Keep it if the user asks or another open pull request still depends on it. Keep long-lived branches such as `develop` and `main`.

### Attribution and signatures

- Use the user's authorised identity for commits and sign-offs made on their behalf. If a document or message needs a signature, use the user's name. Omit AI signatures, bylines and `Co-authored-by` trailers that credit an AI tool.
- Use the identity already configured for the user or supplied by them. If it is unavailable, ask for it. Keep any AI-use disclosure required by the project, institution or publisher.

### Versioning on main

Before each commit or push that updates `main`, including a pull request merge, recommend a version bump or explain why a bump is unnecessary, unless the user says otherwise. Put the recommendation in the pull request or share it before an approved direct update. Check the project's release policy, current version and changes since its last release. Use the project's scheme where one exists. For projects using [Semantic Versioning](https://semver.org/), apply these criteria.

| Recommendation | When to use it |
| --- | --- |
| No bump | The update needs no new release. Examples include an internal refactor or a change to tests, comments or contributor notes that leaves the released product and its commitments intact. If the project has no version scheme, say so and suggest one only if the project needs a release. |
| Patch | The release corrects existing behaviour and preserves the supported interfaces. A scientific bug fix can change numerical results while keeping the same inputs and outputs. Identify affected calculations and explain whether existing results need to be regenerated. |
| Minor | The release adds a backwards-compatible capability, such as an opt-in model or a new supported workflow, or deprecates a public interface. |
| Major | The release breaks a public contract, such as removing a supported option or changing an output format incompatibly. Flag the effect on existing callers and the migration they need. For pre-1.0 projects, follow the project's stated compatibility policy. |

State the current and proposed versions when they are known, the reason for the recommendation and any compatibility or reproducibility impact. A recommendation alone does not change a version file, create a tag or publish a release. When the user requests a bump, use the project's existing release process.

### Code documentation and physics

- Whenever you add or change code, write or update docstrings for the modules, classes, functions and methods you touch. Use the project's usual format or the language's equivalent. Describe what the code does and when to use it. Give a representative usage example. Specify inputs and outputs, including defaults and units where relevant. Explain expected errors or exceptions, what causes them and how invalid inputs are handled. If a routine has no inputs or return value, describe any effects on state or files.
- When the code implements physics, explain the physical model in the docstring. Name the equations or approximations it uses, define the quantities and units, and state the assumptions, valid regime and limits that affect the result. Add comments alongside the relevant calculations to explain the physical reasoning behind choices such as a sign convention, a boundary condition or a numerical approximation. Update the docstrings and comments when the model changes.

## Project workflow

<!-- Add project-specific conventions and the commands used to set up, run and check the work. -->
