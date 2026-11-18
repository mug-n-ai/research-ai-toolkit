# Install the toolkit

Clone the toolkit once to use the same instructions and skills across your own projects. The examples use Git and a shell such as Bash or Zsh. You can also [copy files into one project](#shared-project-instructions) if it needs its own snapshot.

```sh
mkdir -p "$HOME/.local/share"
git clone https://github.com/mug-n-ai/research-ai-toolkit.git "$HOME/.local/share/research-ai-toolkit"
toolkit_dir="$HOME/.local/share/research-ai-toolkit"
```

Use the same `toolkit_dir` in the rest of this guide. If you cloned the repository somewhere else, substitute that path.

## Ask an assistant to set it up

Paste this into an assistant session with terminal access on the machine where you run your tools. For a remote machine, run it in a session that can access that machine.

```text
Install Research AI Toolkit for [Codex, Claude Code, OpenCode, or several].
Use it [across my projects or only in this project].
Read https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/main/INSTALL.md.

Check my OS, installed client versions and current configuration. Choose a
supported setup for each client. Reuse an existing clone if available.
Keep my existing instructions, settings and skills. Report any name clashes.
Verify that the toolkit rules and literature-review are discoverable in the
requested scope. Tell me what you changed and how to update the toolkit.
If you cannot access the machine or start a client, tell me what remains to do.
```

## Codex from the clone

Codex loads personal instructions from its configuration directory, normally `~/.codex`. Use `CODEX_HOME` if it is set. If that directory already has a non-empty `AGENTS.override.md`, add the toolkit rules there. Otherwise use its `AGENTS.md`. Merge the rules into the existing file if there is one. If neither file exists, you can link the toolkit's `AGENTS.md` directly.

```sh
codex_config_dir="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$codex_config_dir"
if [ ! -s "$codex_config_dir/AGENTS.override.md" ] &&
   [ ! -e "$codex_config_dir/AGENTS.md" ] &&
   [ ! -L "$codex_config_dir/AGENTS.md" ]; then
    ln -s "$toolkit_dir/AGENTS.md" "$codex_config_dir/AGENTS.md"
fi
```

For the skills, run the [linking commands below](#link-skills-from-the-clone) with `skill_root="$HOME/.agents/skills"`. Start a new Codex session in the intended project and look for `literature-review` in `/skills`. Check that Codex can see the toolkit instructions too. A pull in the clone updates linked files. If you merged the rules into an existing personal file, compare that file with the updated toolkit rules.

## Claude Code from the clone

Add one import line to your personal `~/.claude/CLAUDE.md`. The command below prints the line with your full path. Paste it into the file as plain text on its own line, outside a code block. The toolkit's `CLAUDE.md` imports the `AGENTS.md` beside it.

```sh
printf '@%s/CLAUDE.md\n' "$toolkit_dir"
```

If the path includes spaces, escape each one with a backslash in the import line. Keep any instructions already in your personal file.

Claude Code discovers skills through its personal directory. Run the [linking commands below](#link-skills-from-the-clone) with `skill_root="$HOME/.claude/skills"`. Start Claude Code from one of your research projects. Check the instructions with `/memory` and look for `/literature-review`.

### Link skills from the clone

Set `skill_root` for your client in the first line, then run the loop. It leaves existing skills in place.

```sh
skill_root="$HOME/.claude/skills"  # Use "$HOME/.agents/skills" for Codex.
mkdir -p "$skill_root"
for skill_file in "$toolkit_dir"/skills/*/SKILL.md; do
    [ -f "$skill_file" ] || continue
    skill_dir=${skill_file%/SKILL.md}
    skill_name=${skill_dir##*/}
    skill_target="$skill_root/$skill_name"
    if [ -e "$skill_target" ] || [ -L "$skill_target" ]; then
        printf 'Keeping existing skill %s\n' "$skill_name"
        continue
    fi
    ln -s "$skill_dir" "$skill_target"
done
```

For updates, run `git -C "$toolkit_dir" pull --ff-only`. The existing links use the updated files. Run the loop again to pick up new skill names.

## OpenCode from the clone

In OpenCode v2, add the toolkit paths to your personal `~/.config/opencode/opencode.json` or `opencode.jsonc`. Append the values to any existing `instructions` and `skills` arrays. This example uses the default clone location above.

```json
{
  "instructions": ["~/.local/share/research-ai-toolkit/AGENTS.md"],
  "skills": ["~/.local/share/research-ai-toolkit/skills"]
}
```

Start a new OpenCode session from a research project and ask it to use `@literature-review`. OpenCode reads the rules from `AGENTS.md` and discovers the skill folders under the configured path. A pull in the clone makes new and updated skills available to new sessions.

If OpenCode v2 already discovers the toolkit skills through `~/.agents/skills/` or `~/.claude/skills/`, add only the `instructions` entry for the toolkit. [OpenCode skill locations](https://opencode.ai/docs/skills/#discovery)

On OpenCode v1, put the skill directory in `skills.paths`. Replace `/absolute/path/to/research-ai-toolkit` with the full path to your clone and merge these entries into your existing configuration. [OpenCode configuration changes from v1 to v2](https://opencode.ai/docs/migrate-v1/#skills)

```json
{
  "instructions": ["/absolute/path/to/research-ai-toolkit/AGENTS.md"],
  "skills": {
    "paths": ["/absolute/path/to/research-ai-toolkit/skills"]
  }
}
```

## Shared project instructions

Use `AGENTS.md` in Codex, Claude Code and OpenCode. If your project already has one, open both files and integrate the toolkit guidance alongside the instructions that belong to the project. For a project without an `AGENTS.md`, copy the starter file and fill in the project sections as needed.

```sh
cp -n "$toolkit_dir/AGENTS.md" ./AGENTS.md
```

The `-n` option preserves an existing file. Commit the resulting `AGENTS.md` if you want those instructions versioned with the project.

## Codex

With `AGENTS.md` in place, use `.agents/skills/` as the destination when [copying skills](#copying-skills). Start a new Codex session from the project and check the skill in `/skills`.

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
skill_destination=".claude/skills"  # Use .agents/skills for Codex or .opencode/skills for OpenCode.
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

Run `setup-matt-pocock-skills` in the research project if your chosen workflow uses an issue tracker, triage labels or the project's glossary and decision records. This setup lets you choose local Markdown for tracking work. In a chat without access to the tracker, ask for a draft of the spec or tickets in the conversation.

If you already use the upstream Matt Pocock plugin, use that installation or the toolkit copies for that agent. Both use the same skill names.

## Verify the setup

Open a fresh session from the project you intend to use. Check that the assistant can find both the toolkit rules and `literature-review` before giving it research material.

| Client | What to check |
| --- | --- |
| Codex | Look for `literature-review` in `/skills`. Ask which instruction file supplies the toolkit's literature-review rule. |
| Claude Code | Check the relevant files in `/memory` and look for `/literature-review`. |
| OpenCode | Ask the client to load `literature-review` and identify the instruction file it sees. In v2 you can select the skill with `@literature-review`. |

For a reproducible setup, record the toolkit commit from `git -C "$toolkit_dir" rev-parse HEAD` alongside the client version. To use a fixed snapshot for a project, check out that revision in a separate clone before copying the files.

## Optional AI footprint hook

To see estimated electricity, water and CO₂e after each reply in Claude Code
or Codex, follow the [hook setup and activation guide](integrations/ai-footprint/README.md).

## Official documentation

- [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code project instructions](https://code.claude.com/docs/en/memory) and [skills](https://code.claude.com/docs/en/skills)
- [OpenCode project instructions](https://opencode.ai/docs/instructions/) and [skills](https://opencode.ai/docs/skills/)
- [Searching the web with ChatGPT](https://help.openai.com/en/articles/9237897-chatgpt-search)
