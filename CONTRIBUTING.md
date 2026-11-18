# Contributing to Research AI Toolkit

If a rule or skill gets in the way of a research task, tell us what you were trying to do, which tool you used and what happened. If you are proposing a new workflow, include a short example that shows when you would use it. You can [open an issue](https://github.com/mug-n-ai/research-ai-toolkit/issues) or submit a pull request with the change.

## Where changes belong

- Use [`AGENTS.md`](AGENTS.md) for shared rules that apply across tasks. Put the details of a specific workflow in its skill.
- Add a skill under `skills/<skill-name>/` with a `SKILL.md` that says what it does and when to use it. Keep any templates or references in the same directory. Add it to the [skill catalogue](skills/README.md) and update the README if the change affects how people discover or use the toolkit.
- When importing a skill, record its source repository and revision, keep its copyright and licence notices, and explain any changes made for this toolkit. Toolkit contributions use the [MIT Licence](LICENSE).

## Check the change

Try the rule or skill on a representative task and describe what you verified. Check that links open and that any referenced files are available. If you change installation instructions, check the steps in the relevant tool. For changes to a scientific workflow, check that the instructions preserve the evidence, assumptions and limits that affect the result.

## Open a pull request

Create a working branch and open a pull request into `main`. In the description, explain the problem, what changed and how you checked it. State whether the update needs a version bump under the project's release policy. Ask for explicit approval before merging. After the merge, delete the working branch unless it was requested to be kept or another open pull request depends on it. See the [full project rules](AGENTS.md).
