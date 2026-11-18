# Install the toolkit

These steps install the toolkit in an existing research project. The commands use Git and a shell such as Bash or Zsh. Clone the toolkit somewhere convenient, then open the root of the research project where you want to use it.

```sh
git clone https://github.com/mug-n-ai/research-ai-toolkit.git
```

From the research project, set `toolkit_dir` to the absolute path of that clone. Use this shell for the remaining commands.

```sh
toolkit_dir="/absolute/path/to/research-ai-toolkit"
```

## Shared project instructions

Use `AGENTS.md` in both Claude Code and OpenCode. If your project already has one, open both files and integrate the toolkit guidance alongside the instructions that belong to the project. For a project without an `AGENTS.md`, copy the starter file and fill in the project sections as needed.

```sh
cp -n "$toolkit_dir/AGENTS.md" ./AGENTS.md
```

The `-n` option preserves an existing file. Commit the resulting `AGENTS.md` to your project if the team should share it.

## Claude Code

With `AGENTS.md` in place, copy `CLAUDE.md` into the root of your project.

```sh
cp -n "$toolkit_dir/CLAUDE.md" ./CLAUDE.md
```

If you already have a root `CLAUDE.md`, add `@AGENTS.md` on its own line if the import is missing. If you keep your instructions in `.claude/CLAUDE.md`, use `@../AGENTS.md` there instead of creating a second file. The path is relative to the file containing the import. Recent Claude Code versions can also read `AGENTS.md` directly, depending on their project instruction settings. The explicit import supports installations that read `CLAUDE.md`.

Use `.claude/skills/` as the destination when [copying skills](#copying-skills). Open a new Claude Code session from the project. Use `/memory` to check the project instruction files. An installed skill can be requested by typing `/<skill-name>`.

## OpenCode

OpenCode reads the project's `AGENTS.md`. Once it is in place, use `.opencode/skills/` as the destination when [copying skills](#copying-skills). Open a new OpenCode session from the project and ask it to load an installed skill by name. In OpenCode v2 you can also mention it as `@skill-name`.

## Copying skills

Choose a skill from the [catalogue](skills/README.md). Copy the whole `skills/<skill-name>/` directory, including its supporting files and licence, to the destination for your tool. The path should end in `<skill-name>/SKILL.md`. Set `skill_name` to `no-ai-slop` to install the writing skill.

```sh
skill_name="skill-name-from-the-catalogue"
skill_destination=".claude/skills"  # Use .opencode/skills for OpenCode.
skill_target="$skill_destination/$skill_name"

if [ -f "$toolkit_dir/skills/$skill_name/SKILL.md" ] &&
   [ ! -e "$skill_target" ] && [ ! -L "$skill_target" ]; then
    mkdir -p "$skill_destination" &&
        cp -R "$toolkit_dir/skills/$skill_name" "$skill_target"
else
    printf '%s\n' 'Check the skill name and review any existing installation before copying.'
fi
```

To update the toolkit, pull the latest changes in its clone. Compare the new files with the copies in your project, then merge changes you want to adopt.

### Matt Pocock's collection

The catalogue lists the companion skills each workflow calls. You can copy just the ones you need, or ask an assistant with terminal access to install the collection from this toolkit.

```text
Install Matt Pocock's skills from the Research AI Toolkit for this project.
Read https://github.com/mug-n-ai/research-ai-toolkit/blob/main/INSTALL.md
and https://github.com/mug-n-ai/research-ai-toolkit/blob/main/skills/README.md.
Clone the toolkit and copy the Matt Pocock skill directories listed in the
catalogue, including their supporting files, using the destination for [Claude
Code or OpenCode]. Keep existing skill directories and report any name clashes.
```

Run `setup-matt-pocock-skills` in the research project if your chosen workflow uses an issue tracker, triage labels or the project's glossary and decision records. This setup lets you choose local Markdown for tracking work. In browser-only ChatGPT, ask for a local draft of a spec or tickets in the chat if the tracker is unavailable.

If you already use the upstream Matt Pocock plugin, use that installation or the toolkit copies for that agent. Both use the same skill names.

## Official documentation

- [Claude Code project instructions](https://code.claude.com/docs/en/memory) and [skills](https://code.claude.com/docs/en/skills)
- [OpenCode project instructions](https://opencode.ai/docs/instructions/) and [skills](https://opencode.ai/docs/skills/)
- [Searching the web with ChatGPT](https://help.openai.com/en/articles/9237897-chatgpt-search)
