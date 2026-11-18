# Contributing to Research AI Toolkit

If a rule or skill gets in the way of a research task, tell us what you were trying to do, which tool you used and what happened. If you are proposing a new workflow, include a short example that shows when you would use it. You can [open an issue](https://github.com/mug-n-ai/research-ai-toolkit/issues) or submit a pull request with the change.

## Where changes belong

- Use [`AGENTS.md`](AGENTS.md) for shared rules that apply across tasks. Put the details of a specific workflow in its skill.
- Add a skill under `skills/<skill-name>/` with a `SKILL.md` that says what it does and when to use it. Keep any templates or references in the same directory. Add it to the [skill catalogue](skills/README.md) and update the README if the change affects how people discover or use the toolkit.
- When importing a skill, record its source repository and revision, keep its copyright and licence notices, and explain any changes made for this toolkit. Toolkit contributions use the [MIT Licence](LICENSE).

## Create a skill

1. Pick a task you do more than once. Write down the inputs, the expected output and how you check the result.
2. Create `skills/<skill-name>/SKILL.md` in the toolkit. Start with a YAML header containing `name` and `description`, then write the workflow in Markdown. Use a lowercase, hyphenated name that matches the folder. The description should say what the skill does and when to use it.
3. Keep any templates or reference files in the skill folder and link to them from `SKILL.md` with relative paths. Try the instructions on a real example and a case with missing inputs. Add the skill to the [catalogue](skills/README.md) if you are contributing it to the toolkit.

For example, save this file as `skills/check-simulation-convergence/SKILL.md`.

```markdown
---
name: check-simulation-convergence
description: Compare results across grid resolutions. Use after a simulation grid changes or when checking convergence.
---

# Check simulation convergence

1. Take the run outputs, the quantity to compare and the tolerance.
   Ask for any input that is missing.
2. Check that the runs use the same physical setup and report in the same units.
   Compare the quantity between successive resolutions.
3. Return a table with the resolutions, values and differences. State which
   comparisons meet the tolerance and which still need checking.
```

### Ask Claude or ChatGPT to write it

Copy this prompt and replace the examples in brackets with details from your project.

```text
Create a reusable Agent Skill for [task we repeat].
It should take [inputs] and produce [output].
Here is an example of how we do it now [paste an example or link to it].
The result is ready when [checks].

Write a SKILL.md with a name and a description that says when to use it.
Include the steps, the checks and what to do if an input is missing.
Add supporting files only if the workflow needs them and link them by
relative path. Show how to try the skill on the example above.
```

To try the skill locally, use `.agents/skills/` for Codex, `.claude/skills/` for Claude Code or `.opencode/skills/` for OpenCode. Open a new session and ask the client to load the skill by name. If you are contributing to this toolkit, keep the source under `skills/` and follow the [installation guide](INSTALL.md#copying-skills) to try it in a project.

In **ChatGPT or Claude in a browser**, ask for the complete `SKILL.md` and any supporting files. You can attach them or paste the instructions into a new chat and ask the assistant to apply them. If your ChatGPT workspace has a **Skills** menu, you can also create or upload skills there under **Create**. [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)

## Check the change

Try the rule or skill on a representative task and describe what you verified. Check that links open and that any referenced files are available. If you change installation instructions, check the steps in the relevant tool. For changes to a scientific workflow, check that the instructions preserve the evidence, assumptions and limits that affect the result.

From the repository root, run the automated checks with Python 3.11 or newer and Bash.

```sh
python -m pip install PyYAML==6.0.3
python scripts/check_toolkit.py
python -m unittest discover -s integrations/ai-footprint
```

The setup checks exercise the documented file layout in a temporary home and project. To check discovery in a running client, follow [Verify the setup](INSTALL.md#verify-the-setup).

## Open a pull request

Create a working branch and open a pull request into `main`. In the description, explain the problem, what changed and how you checked it. State whether the update needs a version bump under the project's release policy. Ask for explicit approval before merging. After the merge, delete the working branch unless it was requested to be kept or another open pull request depends on it. See the [full project rules](AGENTS.md).
