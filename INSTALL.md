# Install the toolkit

Clone the toolkit once to use the same instructions and skills across your own projects. The examples use Git and a shell such as Bash or Zsh. You can also [copy files into one project](#shared-project-instructions) if it needs its own snapshot.

```sh
mkdir -p "$HOME/.local/share"
git clone https://github.com/mug-n-ai/research-ai-toolkit.git "$HOME/.local/share/research-ai-toolkit"
toolkit_dir="$HOME/.local/share/research-ai-toolkit"
```

Use the same `toolkit_dir` in the rest of this guide. If you cloned the repository somewhere else, substitute that path.

## Choose a version

Use the default clone to follow `main`. To update it, run:

```sh
git -C "$toolkit_dir" pull --ff-only origin main
```

For a project that needs a fixed version, clone a [release tag](https://github.com/mug-n-ai/research-ai-toolkit/releases) into its own directory. Use that clone as `toolkit_dir` before following the rest of this guide.

```sh
version="v0.4.1"
mkdir -p "$HOME/.local/share"
toolkit_dir="$HOME/.local/share/research-ai-toolkit-$version"
git clone --branch "$version" --single-branch https://github.com/mug-n-ai/research-ai-toolkit.git "$toolkit_dir"
```

To move the project to another version, use a new clone for that tag and update the paths or copies the project uses. Record the toolkit revision and client version alongside the workflow you want to rerun.

## Install with the script

From the clone, run the installer for the clients you use. It links the skills, loads the rules in every session and reports anything it leaves for you to do. Python 3.9 or newer is enough.

```sh
python3 "$toolkit_dir/scripts/install.py" --client claude --client opencode
```

Add `--client codex` for Codex. Use `--dry-run` first to see the changes without making them. `--skills literature-review reproduce-analysis` links only those skills, and `--rules research-practice testing` loads only those [rule modules](rules) in every session. `--uninstall` removes what the script added.

The script keeps your existing configuration. It does not touch a skill folder of the same name that did not come from the toolkit, an import you added by hand or an OpenCode file with comments. It reports these instead. Before it edits a file, it saves a copy with the suffix `.research-ai-toolkit.bak`. Run it again after each `git pull` to link new skills and remove links to skills that no longer exist.

Claude Code and OpenCode share one set of links: OpenCode v2 also reads skills from `~/.claude/skills`. The sections below describe the same setup by hand, for each client.

## Ask an assistant to set it up

Paste this into an assistant session with terminal access on the machine where you run your tools. For a remote machine, run it in a session that can access that machine.

```text
Install Research AI Toolkit for [Codex, Claude Code, OpenCode, or several].
Use it [across my projects or only in this project].
Install [all skills or the following skills and their required companions].
Read https://raw.githubusercontent.com/mug-n-ai/research-ai-toolkit/main/INSTALL.md.

Check my OS, installed client versions and current configuration. Choose a
supported setup for each client. Reuse an existing clone if available. For a
setup across my projects, prefer scripts/install.py and run it with --dry-run
first.
Keep my existing instructions, settings and skills. Report any name clashes.
Verify that the toolkit rules and a skill I selected are discoverable in the
requested scope. Use literature-review if I selected all skills. Tell me what
you changed and how to update the toolkit.
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

To load only some of the rules in every session, import the modules you want from `rules/` instead, one line each, for example `@/path/to/research-ai-toolkit/rules/research-practice.md`. You can then copy [`templates/AGENTS.md`](templates/AGENTS.md) into the projects where you want the full set.

Claude Code discovers skills through its personal directory. Run the [linking commands below](#link-skills-from-the-clone) with `skill_root="$HOME/.claude/skills"`. Start Claude Code from one of your research projects. Check the instructions with `/memory` and look for `/literature-review`.

### Link skills from the clone

Set `skill_root` for your client. Leave `skill_selection` empty to link the whole catalogue, or set it to the skill names you want, separated by spaces. The loop keeps any existing skills in place.

```sh
skill_root="$HOME/.claude/skills"  # Use "$HOME/.agents/skills" for Codex.
skill_selection=""  # For example: "literature-review reproduce-analysis"
mkdir -p "$skill_root"
for skill_file in "$toolkit_dir"/skills/*/SKILL.md; do
    [ -f "$skill_file" ] || continue
    skill_dir=${skill_file%/SKILL.md}
    skill_name=${skill_dir##*/}
    if [ -n "$skill_selection" ]; then
        case " $skill_selection " in
            *" $skill_name "*) ;;
            *) continue ;;
        esac
    fi
    skill_target="$skill_root/$skill_name"
    if [ -e "$skill_target" ] || [ -L "$skill_target" ]; then
        printf 'Keeping existing skill %s\n' "$skill_name"
        continue
    fi
    ln -s "$skill_dir" "$skill_target"
done
```

If the clone follows `main`, its links use the updated files after a pull. Run the loop again to pick up any new skill names you want, or use the [installer](#install-with-the-script), which also removes links to skills that no longer exist.

### Install a selection

For Codex or Claude Code, use the loop above with a list such as `skill_selection="literature-review reproduce-analysis"`. Check the [companion skills](skills/README.md#installing-a-selection) before choosing a workflow from Matt Pocock's collection. For any client, you can [copy selected skill folders into one project](#copying-skills).

For a personal selection in OpenCode v2, keep the `instructions` entry below. In the `skills` array, list the full path to each chosen folder, such as `/path/to/research-ai-toolkit/skills/literature-review`, in place of the toolkit's full `skills` directory. Keep any entries for other sources. OpenCode may also discover skills you installed through its compatibility paths. For v1, you can [copy the selected folders into the project](#copying-skills).

### Estimate the context cost

In v0.4.1, the shared rules are about 1,700 tokens. Names and descriptions for the installed skills account for about 1,100 to 1,300 more before file paths. The full initial context contributed by the toolkit is roughly 2,800 to 3,600 tokens, depending on which skills the client lists and whether it includes paths. For a smaller setup, use three rule modules and four skills, about 1,200 tokens including example paths.

```sh
python3 "$toolkit_dir/scripts/install.py" --client codex \
  --rules research-practice code-planning testing \
  --skills literature-review reproduce-analysis run-provenance tdd
```

For Codex, follow the installer's message to merge the selected modules into your Codex instructions. With `--client claude`, the installer adds imports for those modules.

These estimates count the toolkit text with OpenAI's `o200k_base` encoding. Actual context varies with the client, model and other installed skills. Full skill instructions are loaded on demand in clients such as Codex and Claude Code. A paper, tool output or sub-agent review adds its own usage. The context figures do not predict how much of a subscription allowance a task will use.

## OpenCode from the clone

In OpenCode v2, add the toolkit paths to your personal `~/.config/opencode/opencode.json` or `opencode.jsonc`. Append the values to any existing `instructions` and `skills` arrays. The example uses the default clone location. Substitute the directory of your clone if you chose a release or a different location.

```json
{
  "instructions": ["~/.local/share/research-ai-toolkit/AGENTS.md"],
  "skills": ["~/.local/share/research-ai-toolkit/skills"]
}
```

To load only some rule modules, list paths such as `~/.local/share/research-ai-toolkit/rules/research-practice.md` in `instructions` instead of `AGENTS.md`.

Start a new OpenCode session from a research project and ask it to use `@literature-review`. OpenCode reads the rules from `AGENTS.md` and discovers the skill folders under the configured path. If you follow `main`, a pull makes new and updated skills available to new sessions.

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

Use `AGENTS.md` in Codex, Claude Code and OpenCode. If your project already has one, open both files and integrate the toolkit guidance alongside the instructions that belong to the project. For a project without an `AGENTS.md`, copy the starter file from `templates/` and fill in the project sections as needed.

```sh
[ -e AGENTS.md ] || cp "$toolkit_dir/templates/AGENTS.md" ./AGENTS.md
```

The test leaves an existing file untouched. Commit the resulting `AGENTS.md` if you want those instructions versioned with the project.

## Codex

With `AGENTS.md` in place, use `.agents/skills/` as the destination when [copying skills](#copying-skills). Start a new Codex session from the project and check the skill in `/skills`.

## Claude Code

With `AGENTS.md` in place, copy `CLAUDE.md` into the root of your project.

```sh
[ -e CLAUDE.md ] || cp "$toolkit_dir/CLAUDE.md" ./CLAUDE.md
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

To update the copies, compare them with the files in the latest `main` or the release you chose. Merge the changes you want to adopt.

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

If an update to `main` removes a skill you linked from this clone, its symlink will no longer resolve. Check where it points with `ls -l` before removing the link. For OpenCode setups that list individual skill folders, remove the missing path from the configuration. To keep using a workflow from the original collection, [clone a separate copy](#choose-a-version) with `version="v0.1.0"` and install the skill with its companions. [Changelog](CHANGELOG.md)

## Verify the setup

Open a fresh session from the project you intend to use. Check that the assistant can find both the toolkit rules and an installed skill before giving it research material. Substitute a skill from your selection for `literature-review` in the checks below if needed.

| Client | What to check |
| --- | --- |
| Codex | Look for `literature-review` in `/skills`. Ask which instruction file supplies the toolkit's literature-review rule. |
| Claude Code | Check the relevant files in `/memory` and look for `/literature-review`. |
| OpenCode | Ask the client to load `literature-review` and identify the instruction file it sees. In v2 you can select the skill with `@literature-review`. |

To check the exact revision you installed, run `git -C "$toolkit_dir" rev-parse HEAD`.

## Optional AI footprint hook

To see estimated electricity, water and CO₂e after each reply in Claude Code
or Codex, follow the [hook setup and activation guide](integrations/ai-footprint/README.md).

## Official documentation

- [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code project instructions](https://code.claude.com/docs/en/memory) and [skills](https://code.claude.com/docs/en/skills)
- [OpenCode project instructions](https://opencode.ai/docs/instructions/) and [skills](https://opencode.ai/docs/skills/)
- [Searching the web with ChatGPT](https://help.openai.com/en/articles/9237897-chatgpt-search)
