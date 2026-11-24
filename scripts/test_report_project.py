"""Fast standard-library tests for the optional research-report packager."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "skills/research-report/scripts/report_project.py"
spec = importlib.util.spec_from_file_location("report_project", SCRIPT)
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


class ReportProjectTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "reports" / "example"
        report.create_report(self.project)

    def test_create_has_portable_main_file_and_does_not_overwrite(self):
        self.assertTrue((self.project / "overleaf/main.tex").is_file())
        self.assertTrue((self.project / "overleaf/sections/model.tex").is_file())
        self.assertTrue((self.project / "artifacts").is_dir())
        with self.assertRaises(FileExistsError):
            report.create_report(self.project)

    def test_package_has_main_at_root_and_omits_artifacts(self):
        (self.project / "artifacts/report.pdf").write_bytes(b"generated build output")
        archive = report.package_report(self.project)
        with zipfile.ZipFile(archive) as zipped:
            names = set(zipped.namelist())
            self.assertIn("main.tex", names)
            self.assertIn("sections/model.tex", names)
            self.assertIn("references.bib", names)
            self.assertIn("figures/", names)
            self.assertIn("tables/", names)
            self.assertNotIn("artifacts/report.pdf", names)
            self.assertNotIn("report-overleaf.zip", names)

    def test_existing_figure_is_packaged_and_missing_figure_is_rejected(self):
        main = self.project / "overleaf/main.tex"
        main.write_text(main.read_text() + "\n\\includegraphics{figures/plot.pdf}\n")
        with self.assertRaisesRegex(ValueError, "missing local file"):
            report.package_report(self.project)
        (self.project / "overleaf/figures/plot.pdf").write_bytes(b"PDF placeholder")
        archive = report.package_report(self.project)
        with zipfile.ZipFile(archive) as zipped:
            self.assertIn("figures/plot.pdf", zipped.namelist())

    def test_rejects_absolute_parent_paths_and_symlinks(self):
        main = self.project / "overleaf/main.tex"
        original = main.read_text()
        for unsafe in ("../secrets.tex", "/tmp/secrets.tex"):
            with self.subTest(unsafe=unsafe):
                main.write_text(original + f"\n\\input{{{unsafe}}}\n")
                with self.assertRaisesRegex(ValueError, "non-portable|leaves the project"):
                    report.package_report(self.project)
        main.write_text(original)
        (self.project / "overleaf/sections/outside.tex").symlink_to(main)
        with self.assertRaisesRegex(ValueError, "symlink"):
            report.package_report(self.project)

    def test_rejects_hidden_and_unexpected_files(self):
        hidden = self.project / "overleaf/.env"
        hidden.write_text("SECRET=sample")
        with self.assertRaisesRegex(ValueError, "hidden file"):
            report.package_report(self.project)
        hidden.unlink()
        bad = self.project / "overleaf/main.log"
        bad.write_text("temporary output")
        with self.assertRaisesRegex(ValueError, "unexpected or generated"):
            report.package_report(self.project)

    def test_ignores_commented_references_and_checks_bibliography(self):
        main = self.project / "overleaf/main.tex"
        main.write_text(main.read_text() + "\n% \\input{does-not-exist}\n")
        report.package_report(self.project)
        main.write_text(main.read_text() + "\n\\bibliography{missing-source}\n")
        with self.assertRaisesRegex(ValueError, "missing local file"):
            report.package_report(self.project)


if __name__ == "__main__":
    unittest.main()

