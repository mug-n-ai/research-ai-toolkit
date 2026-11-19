"""Regression tests for the skill metadata rules in scripts/check_toolkit.py.

Run with 'python -m unittest discover -s scripts' (needs PyYAML).
"""

from pathlib import Path
import tempfile
import unittest
from unittest import mock

import check_toolkit


LONG = "Check a thing in a specific situation. Use when the user asks for that check on their data or code."


def make_skill(root, name="demo", description=LONG, licence="MIT", by_request=False):
    """Write a skill folder with an MIT LICENSE and return its SKILL.md path.

    A by-request skill also gets the matching Codex policy sidecar.
    """
    folder = Path(root) / "skills" / name
    folder.mkdir(parents=True)
    extra = ""
    if by_request:
        extra = "disable-model-invocation: true\n"
        (folder / "agents").mkdir()
        (folder / "agents/openai.yaml").write_text("policy:\n  allow_implicit_invocation: false\n")
    (folder / "LICENSE").write_text("MIT License\n\nCopyright (c) 2026 Someone\n")
    licence_line = f"license: {licence}\n" if licence else ""
    path = folder / "SKILL.md"
    path.write_text(f"---\nname: {name}\ndescription: {description}\n{licence_line}{extra}---\n\n# Demo\n")
    return path


class SkillMetadataTest(unittest.TestCase):
    def diagnostics(self, **kwargs):
        with tempfile.TemporaryDirectory() as directory:
            path = make_skill(directory, **kwargs)
            catalogue = Path(directory) / "skills/README.md"
            catalogue.write_text(f"[{path.parent.name}]({path.parent.name}/SKILL.md)\n")
            with mock.patch.object(check_toolkit, "ROOT", Path(directory)), \
                    mock.patch.object(check_toolkit, "CATALOGUE", catalogue):
                return list(check_toolkit.check_skills([path]))

    def test_valid_skill_has_no_diagnostics(self):
        self.assertEqual(self.diagnostics(), [])

    def test_missing_or_mismatched_licence_field_is_reported(self):
        self.assertIn("license field", self.diagnostics(licence=None)[0])
        self.assertIn("license field", self.diagnostics(licence="Apache-2.0")[0])

    def test_short_or_long_description_is_reported_for_automatic_skills(self):
        self.assertIn("80 to 600", self.diagnostics(description="Use when writing a PR body.")[0])
        self.assertIn("80 to 600", self.diagnostics(description="word " * 130)[0])

    def test_by_request_skill_may_have_a_short_description(self):
        self.assertEqual(self.diagnostics(description="Run a retro.", by_request=True), [])

if __name__ == "__main__":
    unittest.main()
