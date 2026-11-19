"""Tests for scripts/install.py, run against a fake toolkit and a temporary home.

Run with 'python -m unittest discover -s scripts' from the repository root.
No test reads or writes the real home directory.
"""

import json
from pathlib import Path
import tempfile
import unittest

import install


class Sandbox(unittest.TestCase):
    """Create a fake toolkit with two skills and two rule modules, and an empty home."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.toolkit = base / "toolkit"
        for name in ("alpha", "beta"):
            (self.toolkit / "skills" / name).mkdir(parents=True)
            (self.toolkit / "skills" / name / "SKILL.md").write_text(f"---\nname: {name}\n---\n")
        (self.toolkit / "skills/not-a-skill").mkdir()
        (self.toolkit / "rules").mkdir()
        for name in ("one", "two"):
            (self.toolkit / "rules" / f"{name}.md").write_text(f"## {name}\n")
        (self.toolkit / "AGENTS.md").write_text("# rules\n")
        (self.toolkit / "CLAUDE.md").write_text("@AGENTS.md\n")
        self.home = base / "home"
        self.home.mkdir()
        self.env = {"HOME": str(self.home)}
        self.output = []

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, *argv, env=None):
        self.output = []
        return install.main(list(argv), env=env or self.env, toolkit=self.toolkit, out=self.output.append)


class DiscoveryTest(Sandbox):
    def test_lists_only_folders_with_skill_md_and_rule_modules(self):
        self.assertEqual(install.available_skills(self.toolkit), ["alpha", "beta"])
        self.assertEqual(install.available_rules(self.toolkit), ["one", "two"])

    def test_choose_defaults_to_all_and_rejects_unknown_names(self):
        self.assertEqual(install.choose(None, ["a", "b"], "skills"), ["a", "b"])
        self.assertEqual(install.choose(["b", "b"], ["a", "b"], "skills"), ["b"])
        with self.assertRaisesRegex(ValueError, "unknown skills: zeta"):
            install.choose(["zeta"], ["a"], "skills")

    def test_opencode_reuses_claude_skill_directory(self):
        config = self.home / ".config"
        self.assertEqual(install.skill_roots({"claude", "opencode"}, self.home, config), [self.home / ".claude/skills"])
        self.assertEqual(install.skill_roots({"opencode"}, self.home, config), [config / "opencode/skills"])
        self.assertEqual(install.skill_roots({"codex"}, self.home, config), [self.home / ".agents/skills"])


class LinkDetectionTest(Sandbox):
    def test_link_target_and_toolkit_link_recognise_relative_and_dangling_links(self):
        root = self.home / "skills"
        root.mkdir()
        relative = root / "alpha"
        relative.symlink_to(Path("../../toolkit/skills/alpha"))
        self.assertEqual(install.link_target(relative), (self.toolkit / "skills/alpha"))
        self.assertTrue(install.is_toolkit_link(relative, self.toolkit))
        dangling = root / "gone"
        dangling.symlink_to(self.toolkit / "skills/gone")
        self.assertTrue(install.is_toolkit_link(dangling, self.toolkit))
        other = root / "other"
        other.symlink_to(self.home)
        self.assertFalse(install.is_toolkit_link(other, self.toolkit))
        self.assertIsNone(install.link_target(self.home))

    def test_links_through_a_symlinked_clone_path_count_as_toolkit_links(self):
        alias = self.home / "alias"
        alias.symlink_to(self.toolkit)
        link = self.home / "beta"
        link.symlink_to(alias / "skills/beta")
        self.assertTrue(install.is_toolkit_link(link, self.toolkit))


class SkillInstallTest(Sandbox):
    def test_install_links_skills_keeps_personal_ones_and_is_idempotent(self):
        personal = self.home / ".claude/skills/beta"
        personal.mkdir(parents=True)
        (personal / "SKILL.md").write_text("mine\n")
        self.assertEqual(self.run_main("--client", "claude"), 0)
        alpha = self.home / ".claude/skills/alpha"
        self.assertEqual(alpha.resolve(), (self.toolkit / "skills/alpha").resolve())
        self.assertEqual((personal / "SKILL.md").read_text(), "mine\n")
        self.assertTrue(any("kept existing" in line and "beta" in line for line in self.output))
        self.run_main("--client", "claude")
        self.assertFalse(any(line.startswith("link") for line in self.output))

    def test_rerun_prunes_links_to_removed_skills_only(self):
        self.run_main("--client", "codex")
        unrelated = self.home / ".agents/skills/unrelated"
        unrelated.symlink_to(self.home)
        removed = self.toolkit / "skills/beta"
        (removed / "SKILL.md").unlink()
        removed.rmdir()
        self.run_main("--client", "codex")
        self.assertFalse((self.home / ".agents/skills/beta").is_symlink())
        self.assertTrue(unrelated.is_symlink())
        self.assertTrue((self.home / ".agents/skills/alpha").is_symlink())

    def test_selection_and_uninstall_remove_only_toolkit_links(self):
        self.run_main("--client", "claude", "--skills", "alpha")
        root = self.home / ".claude/skills"
        self.assertEqual(sorted(path.name for path in root.iterdir()), ["alpha"])
        (root / "personal").mkdir()
        self.run_main("--client", "claude", "--uninstall")
        self.assertEqual(sorted(path.name for path in root.iterdir()), ["personal"])

    def test_dry_run_changes_nothing(self):
        self.assertEqual(self.run_main("--client", "claude", "--client", "codex", "--dry-run"), 0)
        self.assertFalse((self.home / ".claude").exists())
        self.assertTrue(all(line.startswith(("would ", "note:")) for line in self.output))

    def test_unknown_skill_returns_error_status(self):
        self.assertEqual(self.run_main("--client", "claude", "--skills", "zeta"), 2)
        self.assertIn("error: unknown skills: zeta", self.output)


class ClaudeRulesTest(Sandbox):
    def claude_md(self):
        return self.home / ".claude/CLAUDE.md"

    def test_block_is_added_after_existing_rules_updated_and_removed(self):
        self.claude_md().parent.mkdir()
        self.claude_md().write_text("# Mine\n\nKeep this.\n")
        self.run_main("--client", "claude")
        text = self.claude_md().read_text()
        self.assertTrue(text.startswith("# Mine\n\nKeep this.\n\n" + install.BEGIN))
        self.assertIn(f"@{self.toolkit}/CLAUDE.md", text)
        self.assertTrue(Path(str(self.claude_md()) + install.BACKUP_SUFFIX).is_file())
        self.run_main("--client", "claude", "--rules", "two")
        text = self.claude_md().read_text()
        self.assertIn(f"@{self.toolkit}/rules/two.md", text)
        self.assertNotIn("CLAUDE.md\n", text.split(install.BEGIN)[1])
        self.assertEqual(text.count(install.BEGIN), 1)
        self.run_main("--client", "claude", "--uninstall")
        self.assertEqual(self.claude_md().read_text(), "# Mine\n\nKeep this.\n")

    def test_manual_import_is_left_alone(self):
        self.claude_md().parent.mkdir()
        original = f"# Mine\n\n@{self.toolkit}/CLAUDE.md\n"
        self.claude_md().write_text(original)
        self.run_main("--client", "claude")
        self.assertEqual(self.claude_md().read_text(), original)
        self.assertTrue(any("kept the manual toolkit import" in line for line in self.output))

    def test_manual_import_through_a_symlinked_path_is_recognised(self):
        alias = self.home / "alias"
        alias.symlink_to(self.toolkit)
        text = f"@{alias}/CLAUDE.md\n@relative.md\n@/elsewhere/CLAUDE.md\n"
        self.assertEqual(install.manual_imports(text, self.toolkit), [f"@{alias}/CLAUDE.md"])

    def test_import_lines_escape_spaces(self):
        lines = install.import_lines(Path("/a b/toolkit"), ["one"])
        self.assertEqual(lines, ["@/a\\ b/toolkit/rules/one.md"])

    def test_strip_block_requires_end_marker(self):
        self.assertEqual(install.strip_block("plain\n"), ("plain\n", False))
        self.assertEqual(install.strip_block(f"a\n\n{install.BEGIN}\nx\n{install.END}\n\nb\n"), ("a\n\nb\n", True))
        with self.assertRaises(ValueError):
            install.strip_block(f"{install.BEGIN}\nx\n")

    def test_manual_imports_ignore_the_managed_block(self):
        text = f"@{self.toolkit}/rules/one.md\n{install.BEGIN}\n@{self.toolkit}/CLAUDE.md\n{install.END}\n"
        self.assertEqual(install.manual_imports(text, self.toolkit), [f"@{self.toolkit}/rules/one.md"])


class OpenCodeRulesTest(Sandbox):
    def config_dir(self):
        return self.home / ".config/opencode"

    def test_creates_plain_config_then_updates_and_uninstalls_it(self):
        self.run_main("--client", "opencode")
        path = self.config_dir() / "opencode.json"
        self.assertEqual(json.loads(path.read_text())["instructions"], [str(self.toolkit / "AGENTS.md")])
        config = json.loads(path.read_text())
        config["instructions"].insert(0, "mine.md")
        config["model"] = "kept"
        path.write_text(json.dumps(config))
        self.run_main("--client", "opencode", "--rules", "one")
        config = json.loads(path.read_text())
        self.assertEqual(config["instructions"], ["mine.md", str(self.toolkit / "rules/one.md")])
        self.assertEqual(config["model"], "kept")
        self.run_main("--client", "opencode", "--uninstall")
        self.assertEqual(json.loads(path.read_text())["instructions"], ["mine.md"])

    def test_commented_config_is_reported_not_rewritten(self):
        self.config_dir().mkdir(parents=True)
        path = self.config_dir() / "opencode.jsonc"
        original = '{\n  // personal\n  "instructions": ["mine.md"],\n}\n'
        path.write_text(original)
        self.run_main("--client", "opencode")
        self.assertEqual(path.read_text(), original)
        self.assertTrue(any("by hand" in line and "AGENTS.md" in line for line in self.output))
        path.write_text(original.replace('"mine.md"', f'"mine.md", "{self.toolkit}/AGENTS.md"'))
        self.run_main("--client", "opencode")
        self.assertIn("nothing to change", self.output)

    def test_prefers_jsonc_over_json(self):
        self.config_dir().mkdir(parents=True)
        (self.config_dir() / "opencode.json").write_text("{}")
        (self.config_dir() / "opencode.jsonc").write_text("{}")
        self.assertEqual(install.opencode_config(self.home / ".config"), (self.config_dir() / "opencode.jsonc", True))

    def test_xdg_config_home_is_respected(self):
        xdg = self.home / "xdg"
        self.run_main("--client", "opencode", env={**self.env, "XDG_CONFIG_HOME": str(xdg)})
        self.assertTrue((xdg / "opencode/opencode.json").is_file())
        self.assertTrue((xdg / "opencode/skills/alpha").is_symlink())


class CodexRulesTest(Sandbox):
    def test_links_rules_when_no_personal_file_and_unlinks_on_uninstall(self):
        codex = self.home / "codex"
        env = {**self.env, "CODEX_HOME": str(codex)}
        self.run_main("--client", "codex", env=env)
        self.assertEqual((codex / "AGENTS.md").resolve(), (self.toolkit / "AGENTS.md").resolve())
        self.run_main("--client", "codex", "--uninstall", env=env)
        self.assertFalse((codex / "AGENTS.md").is_symlink())

    def test_personal_file_override_and_module_selection_are_reported(self):
        codex = self.home / ".codex"
        codex.mkdir()
        (codex / "AGENTS.md").write_text("mine\n")
        self.run_main("--client", "codex")
        self.assertEqual((codex / "AGENTS.md").read_text(), "mine\n")
        self.assertTrue(any("merge" in line for line in self.output))
        (codex / "AGENTS.md").unlink()
        (codex / "AGENTS.override.md").write_text("override\n")
        self.run_main("--client", "codex")
        self.assertFalse((codex / "AGENTS.md").exists())
        (codex / "AGENTS.override.md").write_text("")
        self.run_main("--client", "codex", "--rules", "one")
        self.assertFalse((codex / "AGENTS.md").exists())
        self.assertTrue(any("no imports" in line for line in self.output))


class DescribeTest(unittest.TestCase):
    def test_each_change_kind_has_a_description(self):
        path = Path("/x")
        self.assertEqual(install.describe(("link", path, Path("/y"))), "link /x -> /y")
        self.assertEqual(install.describe(("unlink", path, None)), "remove link /x")
        self.assertEqual(install.describe(("write", path, "text")), "update /x")


if __name__ == "__main__":
    unittest.main()
