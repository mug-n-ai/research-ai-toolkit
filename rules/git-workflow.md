## Git branches and pull requests

- Start code changes on a working branch. Get the user's explicit approval before committing or pushing directly to `develop` or `main`.
- When the project uses `develop`, open a pull request from the working branch into `develop`. To promote the changes into `main`, open a separate pull request from `develop` into `main`. In a project that uses `main` as its integration branch, open the pull request from the working branch into `main`.
- For each pull request, share its link and ask the user to confirm the merge before running it. Approval to open the pull request or merge into `develop` does not approve a merge into `main`. Enable auto-merge only with explicit approval for that pull request.
- After a pull request merges, delete its temporary working branch by default. Keep it if the user asks or another open pull request still depends on it. Keep long-lived branches such as `develop` and `main`.

## Versioning on main

Before each commit or push that updates `main`, including a pull request merge, recommend a version bump or explain why a bump is unnecessary, unless the user says otherwise. Put the recommendation in the pull request or share it before an approved direct update. Check the project's release policy, current version and changes since its last release. Use the project's scheme where one exists. For projects using [Semantic Versioning](https://semver.org/), apply these criteria.

| Recommendation | When to use it |
| --- | --- |
| No bump | The update needs no new release. Examples include an internal refactor or a change to tests, comments or contributor notes that leaves the released product and its commitments intact. If the project has no version scheme, say so and suggest one only if the project needs a release. |
| Patch | The release corrects existing behaviour and preserves the supported interfaces. A scientific bug fix can change numerical results while keeping the same inputs and outputs. Identify affected calculations and explain whether existing results need to be regenerated. |
| Minor | The release adds a backwards-compatible capability, such as an opt-in model or a new supported workflow, or deprecates a public interface. |
| Major | The release breaks a public contract, such as removing a supported option or changing an output format incompatibly. Flag the effect on existing callers and the migration they need. For pre-1.0 projects, follow the project's stated compatibility policy. |

State the current and proposed versions when they are known, the reason for the recommendation and any compatibility or reproducibility impact. A recommendation alone does not change a version file, create a tag or publish a release. When the user requests a bump, use the project's existing release process.
