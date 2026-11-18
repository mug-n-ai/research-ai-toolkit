# Project instructions

## Project context

<!-- Add a short description of the project and point to any files that explain its structure. -->

## Shared research group rules

<!-- Add the group's agreed guidance here. -->

- **Literature review.** Read each source used as evidence in full and inspect its figures directly in the original paper. Record what you were able to read and see. Trace substantive claims to specific passages in the original sources and carry their assumptions and limitations into the synthesis. Use `literature-review` for the full workflow.
- When reviewing a draft, preserve its scientific claims, citations, units and degree of certainty. Use `no-ai-slop` for style feedback or a light edit when requested.
- Use a task-specific skill when it fits the work. In a browser-only chat, the public skill files provide the workflow directly. The [skill catalogue](https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/refs/heads/main/skills/README.md) explains when to use each one.

### Git branches and pull requests

- Start code changes on a working branch. Get the user's explicit approval before committing or pushing directly to `develop` or `main`.
- When the project uses `develop`, open a pull request from the working branch into `develop`. To promote the changes into `main`, open a separate pull request from `develop` into `main`. In a project that uses `main` as its integration branch, open the pull request from the working branch into `main`.
- For each pull request, share its link and ask the user to confirm the merge before running it. Approval to open the pull request or merge into `develop` does not approve a merge into `main`. Enable auto-merge only with explicit approval for that pull request.

- After a pull request merges, delete its temporary working branch by default. Keep it if the user asks or another open pull request still depends on it. Keep long-lived branches such as `develop` and `main`.

### Attribution and signatures

- Use the user's authorised identity for commits and sign-offs made on their behalf. If a document or message needs a signature, use the user's name. Omit AI signatures, bylines and `Co-authored-by` trailers that credit an AI tool.
- Use the identity already configured for the user or supplied by them. If it is unavailable, ask for it. Keep any AI-use disclosure required by the project, institution or publisher.

## Project workflow

<!-- Add project-specific conventions and the commands used to set up, run and check the work. -->
