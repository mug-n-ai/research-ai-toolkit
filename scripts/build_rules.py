"""Build the combined rule files from the modules in 'rules/'.

The modules under 'rules/' are the source of truth. This script writes two
generated files from them:

- 'AGENTS.md': every rule module, for a global or personal installation.
  Codex and OpenCode cannot follow Claude Code's '@' imports, so they need
  one file that already contains the rules.
- 'templates/AGENTS.md': the same rules framed by empty project sections, for
  copying into a single research project.

Run 'python scripts/build_rules.py' after editing a module, and
'python scripts/build_rules.py --check' to fail when a generated file is out
of date (the CI does this).
"""

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

# Order in which the modules appear in the combined files. Every file in
# 'rules/' must be listed, so a new module cannot be silently left out.
RULE_ORDER = (
    "research-practice",
    "code-planning",
    "git-workflow",
    "attribution",
    "testing",
    "code-documentation",
)

GENERATED_NOTE = (
    "<!-- Generated from rules/*.md by scripts/build_rules.py. "
    "Edit the modules, then rebuild. -->"
)


def read_modules(root=ROOT, order=RULE_ORDER):
    """Return the text of each rule module in the documented order.

    For example, 'read_modules()[0]' starts with '## Research practice'.
    Each module is stripped of surrounding blank lines. Raise ValueError when
    a listed module is missing or 'rules/' holds a module that is not listed,
    so the generated files cannot drift from the directory contents.
    """
    rules_dir = Path(root) / "rules"
    present = {path.stem for path in rules_dir.glob("*.md")}
    missing = [name for name in order if name not in present]
    unlisted = sorted(present - set(order))
    if missing:
        raise ValueError(f"missing rule modules: {', '.join(missing)}")
    if unlisted:
        raise ValueError(f"rule modules not listed in RULE_ORDER: {', '.join(unlisted)}")
    return [(rules_dir / f"{name}.md").read_text(encoding="utf-8").strip() for name in order]


def render_rules(modules):
    """Return the personal rule file built from a list of module texts.

    For example, 'render_rules(["## A\\n\\nRule."])' returns a document with
    a title, the generated-file note and the module. The result ends with a
    single newline. An empty list raises ValueError.
    """
    if not modules:
        raise ValueError("at least one rule module is required")
    body = "\n\n".join(modules)
    return f"# Research AI Toolkit rules\n\n{GENERATED_NOTE}\n\n{body}\n"


def render_template(modules):
    """Return the project starter: empty project sections around the rules.

    For example, copy the result to a project's 'AGENTS.md' and fill in the
    'Project context' and 'Project workflow' sections. Raise ValueError for an
    empty module list, as render_rules does.
    """
    if not modules:
        raise ValueError("at least one rule module is required")
    body = "\n\n".join(modules)
    return (
        "# Project instructions\n\n"
        "## Project context\n\n"
        "<!-- Add a short description of the project and point to any files "
        "that explain its structure. -->\n\n"
        f"{body}\n\n"
        "## Project workflow\n\n"
        "<!-- Add project-specific conventions and the commands used to set "
        "up, run and check the work. -->\n"
    )


def outputs(root=ROOT, order=RULE_ORDER):
    """Return a mapping from each generated path to its expected contents.

    For example, 'outputs()[ROOT / "AGENTS.md"]' is the combined rule file.
    Errors from read_modules propagate.
    """
    modules = read_modules(root, order)
    root = Path(root)
    return {
        root / "AGENTS.md": render_rules(modules),
        root / "templates/AGENTS.md": render_template(modules),
    }


def stale_files(expected):
    """Return the paths whose contents differ from the expected text.

    Pass the mapping from outputs(). A missing file counts as stale.
    """
    return [
        path for path, text in expected.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != text
    ]


def main(argv=None, root=ROOT):
    """Write the generated rule files, or check them with '--check'.

    Return the process exit status: 0 on success, 1 when '--check' finds a
    stale file. Each stale or written path is printed relative to 'root'.
    Module errors exit with the ValueError message.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if a generated file is out of date")
    args = parser.parse_args(argv)
    try:
        expected = outputs(root)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    stale = stale_files(expected)
    root = Path(root)
    if args.check:
        for path in stale:
            print(f"{path.relative_to(root)} is out of date; run python scripts/build_rules.py", file=sys.stderr)
        return 1 if stale else 0
    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected[path], encoding="utf-8")
        print(f"wrote {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
