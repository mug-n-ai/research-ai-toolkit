"""Install, update or remove the toolkit rules and skills for Claude Code, OpenCode and Codex.

Use this script after cloning the toolkit to make its rules and skills
available in every session of the chosen clients, without copying files:

    python3 scripts/install.py --client claude --client opencode
    python3 scripts/install.py --client codex --skills literature-review tdd
    python3 scripts/install.py --client claude --rules research-practice testing
    python3 scripts/install.py --client claude --uninstall
    python3 scripts/install.py --client claude --dry-run

Running it again after 'git pull' links new skills and removes links to
skills that no longer exist. The script never modifies or deletes anything it
did not create: existing skills with the same name, personal instruction
files and commented OpenCode configurations are reported, not overwritten.
It needs Python 3.9 or newer and no third-party packages.

What it changes for each client:

- claude: symlinks each skill into ~/.claude/skills and adds an import block
  to ~/.claude/CLAUDE.md. A manual import of the toolkit is left in place.
- opencode: adds the rules to 'instructions' in the global opencode.json.
  OpenCode also discovers ~/.claude/skills, so skills are linked into
  ~/.config/opencode/skills only when claude is not selected as well.
- codex: symlinks each skill into ~/.agents/skills and links
  $CODEX_HOME/AGENTS.md (default ~/.codex) to the toolkit rules if there is
  no personal file there yet.
"""

import argparse
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import shutil
import sys


TOOLKIT = Path(__file__).resolve().parents[1]
CLIENTS = ("claude", "opencode", "codex")
BEGIN = "<!-- research-ai-toolkit:begin -->"
END = "<!-- research-ai-toolkit:end -->"
BACKUP_SUFFIX = ".research-ai-toolkit.bak"


@dataclass
class Plan:
    """Changes to make and notes for the user, collected before anything runs.

    'changes' holds (kind, path, payload) tuples. Kinds are 'link' (payload is
    the link target), 'unlink' (payload unused) and 'write' (payload is the
    new file text). 'notes' are messages about things left for the user.
    """

    changes: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    def extend(self, other):
        """Append the changes and notes of another Plan to this one."""
        self.changes.extend(other.changes)
        self.notes.extend(other.notes)


def available_skills(toolkit=TOOLKIT):
    """Return the sorted names of skill folders that contain a SKILL.md.

    For example, 'literature-review' is in available_skills().
    """
    return sorted(path.parent.name for path in Path(toolkit).glob("skills/*/SKILL.md"))


def available_rules(toolkit=TOOLKIT):
    """Return the sorted names of rule modules in rules/, without '.md'."""
    return sorted(path.stem for path in Path(toolkit).glob("rules/*.md"))


def choose(requested, available, kind):
    """Return the requested names, or all available names when none are given.

    Raise ValueError naming any requested entry that does not exist, so a
    typo is reported instead of silently installing nothing.
    """
    if not requested:
        return list(available)
    unknown = sorted(set(requested) - set(available))
    if unknown:
        raise ValueError(f"unknown {kind}: {', '.join(unknown)}")
    return sorted(set(requested))


def skill_roots(clients, home, config_home):
    """Return the personal skill directories to manage for the chosen clients.

    For example, skill_roots(["claude", "opencode"], home, config) returns only
    home/.claude/skills because OpenCode already discovers that directory.
    """
    roots = []
    if "claude" in clients:
        roots.append(Path(home) / ".claude/skills")
    if "codex" in clients:
        roots.append(Path(home) / ".agents/skills")
    if "opencode" in clients and "claude" not in clients:
        roots.append(Path(config_home) / "opencode/skills")
    return roots


def link_target(path):
    """Return the absolute target of a symlink, whether or not it exists.

    Relative link targets are resolved against the link's directory. Return
    None for anything that is not a symlink.
    """
    if not os.path.islink(path):
        return None
    target = Path(os.readlink(path))
    if not target.is_absolute():
        target = Path(path).parent / target
    return Path(os.path.normpath(target))


def is_toolkit_link(path, toolkit=TOOLKIT):
    """Return True if path is a symlink into this toolkit's skills directory."""
    target = link_target(path)
    if target is None:
        return False
    # Resolve the directories but not the final component, so a dangling link
    # made through a symlinked clone path is still recognised.
    target = target.parent.resolve() / target.name
    skills = (Path(toolkit) / "skills").resolve()
    return skills in target.parents


def plan_skills(root, names, toolkit=TOOLKIT, uninstall=False):
    """Plan the skill symlinks in one skill directory.

    On install, link each name that is not there yet, keep correct links and
    remove toolkit links whose skill no longer exists in the checkout. Report
    an existing entry with the same name that is not a toolkit link. On
    uninstall, remove every toolkit link and nothing else. A missing root is
    created on install by the 'link' change.
    """
    plan = Plan()
    root = Path(root)
    existing = sorted(root.iterdir()) if root.is_dir() else []
    for entry in existing:
        if is_toolkit_link(entry, toolkit) and (uninstall or not entry.exists()):
            plan.changes.append(("unlink", entry, None))
    if uninstall:
        return plan
    for name in names:
        target = root / name
        source = Path(toolkit) / "skills" / name
        if is_toolkit_link(target, toolkit) and target.resolve() == source.resolve():
            continue
        if os.path.lexists(target):
            plan.notes.append(f"kept existing {target}; it is not this toolkit's {name} skill")
            continue
        plan.changes.append(("link", target, source))
    return plan


def import_lines(toolkit, modules):
    """Return the Claude Code import lines for the whole rule set or some modules.

    'modules' is None for every rule, which imports the toolkit's CLAUDE.md.
    Spaces in the path are escaped with a backslash, as Claude Code expects.
    """
    paths = [Path(toolkit) / "CLAUDE.md"] if modules is None else [
        Path(toolkit) / "rules" / f"{name}.md" for name in modules
    ]
    return ["@" + str(path).replace(" ", "\\ ") for path in paths]


def strip_block(text):
    """Return text without the managed import block, and whether one was found.

    Only the first block between the BEGIN and END markers is removed, along
    with the blank lines around it. Raise ValueError for a BEGIN without END.
    """
    start = text.find(BEGIN)
    if start == -1:
        return text, False
    end = text.find(END, start)
    if end == -1:
        raise ValueError("found the toolkit's begin marker without its end marker")
    before = text[:start].rstrip("\n")
    after = text[end + len(END):].strip("\n")
    joined = "\n\n".join(part for part in (before, after) if part)
    return (joined + "\n" if joined else ""), True


def manual_imports(text, toolkit):
    """Return lines outside the managed block that import a file from the toolkit."""
    outside, _ = strip_block(text)
    prefix = str(toolkit).replace(" ", "\\ ") + "/"
    return [line for line in outside.splitlines() if line.strip().startswith("@" + prefix)]


def plan_claude_rules(home, modules, toolkit=TOOLKIT, uninstall=False):
    """Plan the import block in ~/.claude/CLAUDE.md.

    Add or update a block between the BEGIN and END markers. When the file
    already imports the toolkit outside that block, leave the file alone and
    add a note, so personal edits are never rewritten. On uninstall, remove
    the block and note any manual import that still needs removing.
    """
    plan = Plan()
    path = Path(home) / ".claude/CLAUDE.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    manual = manual_imports(text, toolkit)
    base, had_block = strip_block(text)
    if manual:
        verb = "remove" if uninstall else "kept"
        plan.notes.append(f"{verb} the manual toolkit import in {path}: {', '.join(manual)}")
        if not uninstall:
            return plan
    if uninstall:
        new = base
    else:
        block = "\n".join([BEGIN, *import_lines(toolkit, modules), END])
        new = (base.rstrip("\n") + "\n\n" if base.strip() else "") + block + "\n"
    if new != text and (had_block or not uninstall):
        plan.changes.append(("write", path, new))
    return plan


def opencode_config(config_home):
    """Return the global OpenCode config file to use and whether it exists.

    Prefer an existing opencode.jsonc, then opencode.json. If neither exists,
    return the path of a new opencode.json.
    """
    directory = Path(config_home) / "opencode"
    for name in ("opencode.jsonc", "opencode.json"):
        if (directory / name).is_file():
            return directory / name, True
    return directory / "opencode.json", False


def plan_opencode_rules(config_home, modules, toolkit=TOOLKIT, uninstall=False):
    """Plan the toolkit entries in the global OpenCode 'instructions' list.

    Plain JSON files are updated in place, keeping every other setting.
    A file with comments or trailing commas (JSONC) is never rewritten:
    the plan reports the entries to add or remove by hand instead.
    """
    plan = Plan()
    entries = [str(Path(toolkit) / "AGENTS.md")] if modules is None else [
        str(Path(toolkit) / "rules" / f"{name}.md") for name in modules
    ]
    path, exists = opencode_config(config_home)
    if not exists:
        if not uninstall:
            config = {"$schema": "https://opencode.ai/config.json", "instructions": entries}
            plan.changes.append(("write", path, json.dumps(config, indent=2) + "\n"))
        return plan
    text = path.read_text(encoding="utf-8")
    try:
        config = json.loads(text)
    except json.JSONDecodeError:
        config = None
    if config is None:
        pending = [entry for entry in entries if (entry in text) == uninstall]
        if pending:
            action = "remove these entries from" if uninstall else "add these entries to"
            plan.notes.append(f"{path} has comments, so {action} 'instructions' by hand: {json.dumps(pending)}")
        return plan
    current = config.get("instructions", [])
    if not isinstance(current, list):
        plan.notes.append(f"{path}: 'instructions' is not a list; update it by hand")
        return plan
    toolkit_prefix = str(Path(toolkit)) + "/"
    kept = [item for item in current if not (isinstance(item, str) and item.startswith(toolkit_prefix))]
    updated = kept if uninstall else kept + entries
    if updated != current:
        config["instructions"] = updated
        plan.changes.append(("write", path, json.dumps(config, indent=2) + "\n"))
    return plan


def plan_codex_rules(codex_home, modules, toolkit=TOOLKIT, uninstall=False):
    """Plan the link from Codex's personal AGENTS.md to the toolkit rules.

    Codex reads one personal file and has no imports, so only the full rule
    set can be linked. With a module selection, an existing personal file or a
    non-empty AGENTS.override.md, the plan only adds a note about merging the
    rules by hand.
    """
    plan = Plan()
    codex_home = Path(codex_home)
    target = codex_home / "AGENTS.md"
    source = Path(toolkit) / "AGENTS.md"
    linked = target.is_symlink() and target.resolve() == source.resolve()
    if uninstall:
        if linked:
            plan.changes.append(("unlink", target, None))
        return plan
    if linked:
        return plan
    override = codex_home / "AGENTS.override.md"
    if modules is not None:
        plan.notes.append(f"Codex has no imports: merge the selected modules from {Path(toolkit) / 'rules'} into {target}")
    elif override.is_file() and override.stat().st_size:
        plan.notes.append(f"{override} takes precedence: merge {source} into it by hand")
    elif os.path.lexists(target):
        plan.notes.append(f"kept {target}; merge {source} into it by hand")
    else:
        plan.changes.append(("link", target, source))
    return plan


def build_plan(clients, skills, modules, env, toolkit=TOOLKIT, uninstall=False):
    """Return the complete Plan for the chosen clients.

    'env' supplies HOME, and optionally XDG_CONFIG_HOME and CODEX_HOME, so
    the plan can be built for a temporary home in tests.
    """
    home = Path(env["HOME"])
    config_home = Path(env.get("XDG_CONFIG_HOME") or home / ".config")
    plan = Plan()
    for root in skill_roots(clients, home, config_home):
        plan.extend(plan_skills(root, skills, toolkit, uninstall))
    if "claude" in clients:
        plan.extend(plan_claude_rules(home, modules, toolkit, uninstall))
    if "opencode" in clients:
        plan.extend(plan_opencode_rules(config_home, modules, toolkit, uninstall))
    if "codex" in clients:
        codex_home = Path(env.get("CODEX_HOME") or home / ".codex")
        plan.extend(plan_codex_rules(codex_home, modules, toolkit, uninstall))
    return plan


def describe(change):
    """Return a one-line description of a planned change."""
    kind, path, payload = change
    if kind == "link":
        return f"link {path} -> {payload}"
    if kind == "unlink":
        return f"remove link {path}"
    return f"update {path}"


def apply(plan, dry_run=False, out=print):
    """Carry out the plan's changes, or only print them with dry_run.

    Before overwriting an existing file, copy it next to itself with the
    BACKUP_SUFFIX. Every change and note is reported through 'out'.
    Filesystem errors propagate.
    """
    prefix = "would " if dry_run else ""
    for change in plan.changes:
        out(prefix + describe(change))
        if dry_run:
            continue
        kind, path, payload = change
        if kind == "unlink":
            path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if kind == "link":
            path.symlink_to(payload, target_is_directory=payload.is_dir())
        else:
            if path.is_file():
                shutil.copy2(path, path.with_name(path.name + BACKUP_SUFFIX))
            path.write_text(payload, encoding="utf-8")
    for note in plan.notes:
        out("note: " + note)
    if not plan.changes:
        out("nothing to change")


def parse_args(argv):
    """Parse the command line; see the module docstring for examples."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--client", action="append", choices=CLIENTS, required=True,
                        help="client to configure; repeat for several")
    parser.add_argument("--skills", nargs="+", metavar="NAME", help="skills to link (default: all)")
    parser.add_argument("--rules", nargs="+", metavar="MODULE",
                        help="rule modules to load in every session (default: all, via AGENTS.md)")
    parser.add_argument("--uninstall", action="store_true", help="remove what this script installed")
    parser.add_argument("--dry-run", action="store_true", help="print the changes without making them")
    return parser.parse_args(argv)


def main(argv=None, env=None, toolkit=TOOLKIT, out=print):
    """Run the installer and return the exit status (0 on success, 2 on bad input)."""
    args = parse_args(argv)
    env = os.environ if env is None else env
    try:
        skills = choose(args.skills, available_skills(toolkit), "skills")
        modules = None if not args.rules else choose(args.rules, available_rules(toolkit), "rule modules")
        plan = build_plan(set(args.client), skills, modules, env, toolkit, args.uninstall)
    except ValueError as exc:
        out(f"error: {exc}")
        return 2
    apply(plan, args.dry_run, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
