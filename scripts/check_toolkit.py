"""Validate toolkit files and exercise the documented setup, without client authentication.

Run 'python scripts/check_toolkit.py' from the repository root, with PyYAML
installed and Bash available. The checker reads the checkout, uses an isolated
temporary home and project, and exits non-zero if an invariant fails.
"""

import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^([~\x60]{3,})([\w-]*)[^\S\n]*\n(.*?)^\1[^\S\n]*$", re.M | re.S)
LINK = re.compile(r"\]\(([^()\s]+)\)")
SUPPORT = re.compile(r"\x60((?:assets|references|scripts)/[\w./-]+\.\w+)\x60")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
CATALOGUE = ROOT / "skills/README.md"
MIN_DESCRIPTION = 80
MAX_DESCRIPTION = 600


def front_matter(path):
    """Read YAML delimited by '---' from a SKILL.md path.

    For example, 'front_matter(path)["name"]' gets the skill name. Return a
    mapping and raise ValueError for missing delimiters or a non-mapping value.
    PyYAML reports invalid YAML.
    """
    contents = path.read_text(encoding="utf-8")
    block = re.match(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n", contents, re.S)
    if not block:
        raise ValueError(f"{path}: missing YAML front matter")
    metadata = yaml.safe_load(block[1])
    if not isinstance(metadata, dict):
        raise ValueError(f"{path}: front matter must be a mapping")
    return metadata


def anchors(path):
    """Return GitHub-style slugs for ATX headings in the given Markdown file.

    For example, a heading '## Choose your tool' produces 'choose-your-tool'.
    Fenced examples are ignored. File errors propagate to the caller.
    """
    headings = re.findall(r"^#{1,6}[ \t]+(.+)$", FENCE.sub("", path.read_text()), re.M)
    found = set()
    for heading in headings:
        slug = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        candidate = slug
        index = 1
        while candidate in found:
            candidate = f"{slug}-{index}"
            index += 1
        found.add(candidate)
    return found


def check_links(path, *, skill=False):
    """Return diagnostics for broken local links in a Markdown file.

    For example, check_links(ROOT / "README.md") checks the TOC anchors.
    In a skill, check bundled file links and code-formatted supporting paths,
    skipping examples for files the workflow creates outside the skill.
    Unreadable files and malformed URLs raise their usual exceptions.
    """
    body = FENCE.sub("", path.read_text(encoding="utf-8"))
    targets = LINK.findall(body)
    if skill:
        targets = [target for target in targets if Path(urlsplit(target).path).suffix]
        targets += SUPPORT.findall(body)
    for target in targets:
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        destination = path.parent / unquote(url.path) if url.path else path
        if not destination.exists():
            yield f"{path.relative_to(ROOT)}: missing target {target}"
        elif url.fragment and destination.suffix == ".md" and unquote(url.fragment) not in anchors(destination):
            yield f"{path.relative_to(ROOT)}: missing heading {target}"


def check_skills(skill_files):
    """Return metadata, catalogue and support-file diagnostics for SKILL.md paths.

    Pass the list from 'ROOT.glob("skills/*/SKILL.md")'. Invalid metadata is
    reported per skill. Unreadable catalogue or support files raise OSError.
    """
    catalogue = CATALOGUE.read_text(encoding="utf-8")
    paths = {str(path.relative_to(CATALOGUE.parent)) for path in skill_files}
    listed = {target for target in LINK.findall(catalogue) if target.endswith("/SKILL.md")}
    for missing in sorted(paths - listed):
        yield f"{missing}: missing catalogue entry"

    for path in skill_files:
        try:
            metadata = front_matter(path)
            name = metadata.get("name")
            description = metadata.get("description")
            if name != path.parent.name or len(name) > 64 or not SLUG.fullmatch(name):
                raise ValueError("name must match the folder and be a valid skill name")
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                raise ValueError("description must contain 1 to 1024 characters")
            if not (path.parent / "LICENSE").is_file():
                raise ValueError("missing bundled licence")
            licence = metadata.get("license")
            first_line = (path.parent / "LICENSE").read_text(encoding="utf-8").strip().splitlines()[:1]
            if not isinstance(licence, str) or not first_line or not first_line[0].startswith(licence):
                raise ValueError("license field must name the licence in the bundled LICENSE")
            manual = metadata.get("disable-model-invocation", False)
            if not isinstance(manual, bool):
                raise ValueError("disable-model-invocation must be a boolean")
            # Descriptions of skills the assistant selects by itself are loaded into
            # every session and drive the choice, so keep them informative but short.
            if not manual and not MIN_DESCRIPTION <= len(description) <= MAX_DESCRIPTION:
                raise ValueError(
                    f"description of an automatically selected skill must contain "
                    f"{MIN_DESCRIPTION} to {MAX_DESCRIPTION} characters"
                )
            sidecar = path.parent / "agents/openai.yaml"
            codex_policy = yaml.safe_load(sidecar.read_text()) if sidecar.is_file() else {}
            if codex_policy.get("policy", {}).get("allow_implicit_invocation", True) is not (not manual):
                raise ValueError("Codex and Claude Code invocation settings disagree")
        except (ValueError, AttributeError, yaml.YAMLError) as exc:
            yield f"{path.relative_to(ROOT)}: {exc}"
        yield from check_links(path, skill=True)


def smoke_setup(skill_files):
    """Exercise INSTALL.md snippets with a temporary home and project.

    Call with the same paths as check_skills. Filesystem mismatches raise
    AssertionError, and failed shell commands raise CalledProcessError.
    This checks file placement, preservation and config paths for all three
    clients without starting a model or using a live client's configuration.
    """
    blocks = FENCE.findall((ROOT / "INSTALL.md").read_text(encoding="utf-8"))
    shell = [body for _, language, body in blocks if language == "sh"]
    codex = next(body for body in shell if body.startswith("codex_config_dir="))
    claude = next(body for body in shell if body.startswith("printf '@"))
    link_skills = next(body for body in shell if body.startswith("skill_root="))
    selection = ("literature-review", "reproduce-analysis")
    assert 'skill_selection=""' in link_skills, "Missing skill selection setting"
    link_selection = link_skills.replace(
        'skill_selection=""', f'skill_selection="{" ".join(selection)}"', 1,
    )
    copy_skill = next(body for body in shell if body.startswith("skill_name="))
    project_rules = [body for body in shell if body.startswith("[ -e ")]
    assert len(project_rules) == 2, "Expected project instruction snippets for AGENTS.md and CLAUDE.md"
    assert "skill-name-from-the-catalogue" in copy_skill, "Missing skill name placeholder"
    copy_skill = copy_skill.replace("skill-name-from-the-catalogue", "literature-review")

    with tempfile.TemporaryDirectory(prefix="research-ai-toolkit-") as directory:
        home = Path(directory)
        checkout = home / ".local/share/research-ai-toolkit"
        checkout.parent.mkdir(parents=True)
        checkout.symlink_to(ROOT, target_is_directory=True)
        project = home / "project"
        project.mkdir()
        config = home / "codex-config"
        config.mkdir()
        override = config / "AGENTS.override.md"
        override.write_text("Existing override\n")
        env = {**os.environ, "HOME": str(home), "CODEX_HOME": str(config), "toolkit_dir": str(checkout)}
        assert setup_shell(codex, project, env) == ""
        assert not (config / "AGENTS.md").exists(), "Codex setup ignored an existing override"
        assert override.read_text() == "Existing override\n"
        override.unlink()
        setup_shell(codex, project, env)
        assert (config / "AGENTS.md").resolve() == ROOT / "AGENTS.md"

        claude_rules = home / ".claude/CLAUDE.md"
        claude_rules.parent.mkdir()
        claude_rules.write_text("Existing personal rules\n" + setup_shell(claude, project, env))
        assert claude_rules.read_text().splitlines()[-1] == f"@{checkout}/CLAUDE.md"
        assert (checkout / "CLAUDE.md").read_text().splitlines().count("@AGENTS.md") == 1

        for skill_root in (".claude/skills", ".agents/skills"):
            snippet = link_selection.replace(".claude/skills", skill_root, 1)
            setup_shell(snippet, project, env)
            linked = home / skill_root
            assert sorted(path.name for path in linked.iterdir()) == sorted(selection)
            for name in selection:
                assert (linked / name / "SKILL.md").resolve() == ROOT / "skills" / name / "SKILL.md"

        for skill_root in (".claude/skills", ".agents/skills"):
            snippet = link_skills.replace(".claude/skills", skill_root, 1)
            setup_shell(snippet, project, env)
            assert len(list((home / skill_root).iterdir())) == len(skill_files)
            for path in skill_files:
                assert (home / skill_root / path.parent.name / "SKILL.md").resolve() == path
            existing = home / skill_root / "literature-review"
            existing.unlink()
            existing.mkdir()
            (existing / "SKILL.md").write_text("Existing personal skill\n")
            setup_shell(snippet, project, env)
            assert (existing / "SKILL.md").read_text() == "Existing personal skill\n"

        for snippet in project_rules:
            setup_shell(snippet, project, env)
        assert (project / "AGENTS.md").read_bytes() == (ROOT / "templates/AGENTS.md").read_bytes()
        assert (project / "CLAUDE.md").read_bytes() == (ROOT / "CLAUDE.md").read_bytes()
        for name in ("AGENTS.md", "CLAUDE.md"):
            (project / name).write_text("Existing project rules\n")
        for snippet in project_rules:
            setup_shell(snippet, project, env)
        for name in ("AGENTS.md", "CLAUDE.md"):
            assert (project / name).read_text() == "Existing project rules\n", f"Project setup overwrote {name}"
        for destination in (".claude/skills", ".agents/skills", ".opencode/skills"):
            snippet = copy_skill.replace(".claude/skills", destination, 1)
            setup_shell(snippet, project, env)
            copied = project / destination / "literature-review"
            source = ROOT / "skills/literature-review"
            for path in source.iterdir():
                assert (copied / path.name).read_bytes() == path.read_bytes()
            (copied / "SKILL.md").write_text("Project copy\n")
            setup_shell(snippet, project, env)
            assert (copied / "SKILL.md").read_text() == "Project copy\n"

        installer = next(body for body in shell if "scripts/install.py" in body)
        installer_home = home / "installer-home"
        installer_home.mkdir()
        installer_env = {key: value for key, value in env.items() if key != "XDG_CONFIG_HOME"}
        setup_shell(installer, project, {**installer_env, "HOME": str(installer_home)})
        for path in skill_files:
            linked = installer_home / ".claude/skills" / path.parent.name / "SKILL.md"
            assert linked.resolve() == path, f"Installer did not link {path.parent.name}"
        assert f"@{ROOT}/CLAUDE.md" in (installer_home / ".claude/CLAUDE.md").read_text()
        installed = json.loads((installer_home / ".config/opencode/opencode.json").read_text())
        assert installed["instructions"] == [f"{ROOT}/AGENTS.md"]

        opencode = [json.loads(body) for _, language, body in blocks if language == "json"]
        v2, v1 = opencode
        assert v2["instructions"] == ["~/.local/share/research-ai-toolkit/AGENTS.md"]
        assert v2["skills"] == ["~/.local/share/research-ai-toolkit/skills"]
        assert (home / v2["instructions"][0][2:]).is_file()
        assert (home / v2["skills"][0][2:] / "literature-review/SKILL.md").is_file()
        assert v1["instructions"] == ["/absolute/path/to/research-ai-toolkit/AGENTS.md"]
        assert v1["skills"]["paths"] == ["/absolute/path/to/research-ai-toolkit/skills"]


def setup_shell(snippet, project, env):
    """Run a documented Bash snippet and return its stdout.

    For example, pass the skill-linking loop, the temporary project directory
    and its environment. A non-zero exit or timeout raises a subprocess error.
    """
    return subprocess.run(
        ["bash", "-eu", "-c", snippet], cwd=project, env=env,
        check=True, stdout=subprocess.PIPE, text=True, timeout=20,
    ).stdout


def main():
    """Run 'python scripts/check_toolkit.py' and print diagnostics to the terminal.

    Exit with status 1 for metadata, link or setup failures. On success, print
    the number of skills checked. Unexpected filesystem errors retain tracebacks.
    """
    skill_files = sorted(ROOT.glob("skills/*/SKILL.md"))
    errors = list(check_skills(skill_files))
    docs = [
        *ROOT.glob("*.md"), CATALOGUE, ROOT / "integrations/ai-footprint/README.md",
        *ROOT.glob("examples/*/*.md"), *ROOT.glob("rules/*.md"), ROOT / "templates/AGENTS.md",
    ]
    for path in docs:
        errors.extend(check_links(path))
    if errors:
        raise SystemExit("\n".join(errors))
    smoke_setup(skill_files)
    print(f"Checked {len(skill_files)} skills, documentation links and installation layout.")


if __name__ == "__main__":
    main()
