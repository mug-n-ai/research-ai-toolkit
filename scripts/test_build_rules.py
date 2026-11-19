"""Tests for scripts/build_rules.py.

Run with 'python -m unittest discover -s scripts' from the repository root.
"""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import build_rules


ORDER = ("first", "second")


def make_root(directory, modules):
    """Create a fake toolkit root with the given {name: text} rule modules."""
    root = Path(directory)
    (root / "rules").mkdir()
    for name, text in modules.items():
        (root / "rules" / f"{name}.md").write_text(text, encoding="utf-8")
    return root


class ReadModulesTest(unittest.TestCase):
    def test_returns_modules_in_listed_order_without_outer_blank_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            root = make_root(directory, {"second": "## B\n\nTwo.\n\n", "first": "\n## A\n\nOne.\n"})
            self.assertEqual(build_rules.read_modules(root, ORDER), ["## A\n\nOne.", "## B\n\nTwo."])

    def test_missing_module_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = make_root(directory, {"first": "## A"})
            with self.assertRaisesRegex(ValueError, "missing rule modules: second"):
                build_rules.read_modules(root, ORDER)

    def test_unlisted_module_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = make_root(directory, {"first": "## A", "second": "## B", "extra": "## C"})
            with self.assertRaisesRegex(ValueError, "not listed in RULE_ORDER: extra"):
                build_rules.read_modules(root, ORDER)


class RenderTest(unittest.TestCase):
    def test_rules_file_has_title_note_and_modules(self):
        text = build_rules.render_rules(["## A\n\nOne.", "## B\n\nTwo."])
        self.assertTrue(text.startswith("# Research AI Toolkit rules\n"))
        self.assertIn(build_rules.GENERATED_NOTE, text)
        self.assertLess(text.index("## A"), text.index("## B"))
        self.assertTrue(text.endswith("Two.\n") and not text.endswith("\n\n"))

    def test_template_wraps_rules_in_project_sections(self):
        text = build_rules.render_template(["## A\n\nOne."])
        self.assertLess(text.index("## Project context"), text.index("## A"))
        self.assertLess(text.index("## A"), text.index("## Project workflow"))
        self.assertNotIn(build_rules.GENERATED_NOTE, text)

    def test_empty_module_list_is_rejected(self):
        for render in (build_rules.render_rules, build_rules.render_template):
            with self.assertRaises(ValueError):
                render([])


class MainTest(unittest.TestCase):
    def run_main(self, root, *argv):
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            status = build_rules.main(list(argv), root=root)
        return status, err.getvalue()

    def test_build_then_check_passes_and_edit_makes_check_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = make_root(directory, {name: f"## {name}\n" for name in build_rules.RULE_ORDER})
            self.assertEqual(self.run_main(root, "--check")[0], 1)  # nothing generated yet
            self.assertEqual(self.run_main(root)[0], 0)
            self.assertTrue((root / "templates/AGENTS.md").is_file())
            self.assertEqual(self.run_main(root, "--check")[0], 0)
            (root / "rules/testing.md").write_text("## testing\n\nChanged.\n")
            status, err = self.run_main(root, "--check")
            self.assertEqual(status, 1)
            self.assertIn("AGENTS.md is out of date", err)

    def test_repository_files_are_up_to_date(self):
        self.assertEqual(build_rules.stale_files(build_rules.outputs()), [])


if __name__ == "__main__":
    unittest.main()
