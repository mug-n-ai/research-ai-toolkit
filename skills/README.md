# Skill catalogue

There are no published skills yet. Each entry here will give the skill's name, describe when to use it and link to its `SKILL.md`.

## Skill format

Give each skill its own directory under `skills/`. The main file is `skills/<skill-name>/SKILL.md`. It starts with YAML front matter containing `name` and `description`, followed by the Markdown workflow. Use the same lowercase, hyphenated name for the directory and the `name` field. Write the description so someone can tell which task calls for the skill.

The workflow can state what inputs the assistant needs, what it should produce and how to check the result. Keep any references or templates alongside the skill and link to them with relative paths so the directory can be copied as a unit.

See the [Agent Skills specification](https://agentskills.io/specification) for the file format and the [setup guide](../INSTALL.md#copying-skills) for installation paths.
