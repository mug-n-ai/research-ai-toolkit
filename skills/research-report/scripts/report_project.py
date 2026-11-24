"""Create and package self-contained LaTeX research notes for Overleaf.

Run ``python report_project.py create reports/my-analysis`` to copy the template,
then ``python report_project.py package reports/my-analysis`` after editing.
Neither operation starts a model, compiles TeX or needs third-party packages.
"""

import argparse
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import zipfile


TEMPLATE = Path(__file__).resolve().parents[1] / "templates/overleaf"
ALLOWED_SUFFIXES = frozenset({
    ".tex", ".bib", ".pdf", ".png", ".jpg", ".jpeg",
    ".sty", ".cls", ".csv", ".tsv", ".txt", ".py",
    ".r", ".jl", ".c", ".h", ".cpp", ".f90", ".sh", ".js", ".json", ".yml", ".yaml",
})
GRAPHICS_SUFFIXES = (".pdf", ".png", ".jpg", ".jpeg")
REFERENCE = re.compile(
    r"\\(input|include|includegraphics|lstinputlisting|addbibresource|bibliography)"
    r"\s*(?:\[[^\]\n]*\])?\s*\{([^{}]+)\}"
)
COMMENT = re.compile(r"(?<!\\)%[^\n]*")


def create_report(destination, template=TEMPLATE):
    """Copy a starter Overleaf project into a new report directory.

    For example, create_report(Path('reports/test')) creates
    'reports/test/overleaf/main.tex' and an empty 'artifacts/' directory.
    Raise FileExistsError if the destination already exists; never overwrite.
    """
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError(f"report already exists: {destination}")
    destination.mkdir(parents=True)
    try:
        shutil.copytree(template, destination / "overleaf")
        for dirname in ("figures", "tables"):
            (destination / "overleaf" / dirname).mkdir(exist_ok=True)
        (destination / "artifacts").mkdir()
    except Exception:
        shutil.rmtree(destination)
        raise
    return destination / "overleaf"


def _safe_target(name):
    """Return a portable relative POSIX path or reject unsafe TeX references."""
    if not name or "\\" in name or "\x00" in name:
        raise ValueError(f"non-portable LaTeX reference: {name!r}")
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in ("..", ".") for part in name.split("/")):
        raise ValueError(f"LaTeX reference leaves the project or is non-portable: {name}")
    if any(part.startswith(".") for part in path.parts):
        raise ValueError(f"hidden file in LaTeX reference: {name}")
    return path


def _project_files(overleaf):
    """Return safe files and directories under Overleaf, rejecting unsafe files."""
    if overleaf.is_symlink():
        raise ValueError(f"Overleaf source directory is a symlink: {overleaf}")
    if not (overleaf / "main.tex").is_file():
        raise ValueError(f"missing main.tex at {overleaf}")
    files, directories = [], []
    for path in sorted(overleaf.rglob("*")):
        relative = path.relative_to(overleaf)
        if path.is_symlink():
            raise ValueError(f"symlink cannot be exported: {relative}")
        if any(part.startswith(".") for part in relative.parts):
            raise ValueError(f"hidden file cannot be exported: {relative}")
        if path.is_dir():
            directories.append(relative)
        elif path.is_file():
            if path.suffix.lower() not in ALLOWED_SUFFIXES or relative.name.lower() == "main.pdf":
                raise ValueError(f"unexpected or generated file in Overleaf source: {relative}")
            files.append(relative)
        else:
            raise ValueError(f"unsupported filesystem entry: {relative}")
    return files, directories


def check_references(overleaf, files):
    """Check simple literal TeX file references; compilation remains definitive.

    For example, a missing '\\input{sections/model}' raises ValueError.
    The checker does not interpret TeX macros, conditional branches or package
    commands. All paths are relative to the root main.tex project directory.
    """
    present = {path.as_posix() for path in files}
    for relative in files:
        if relative.suffix.lower() != ".tex":
            continue
        body = COMMENT.sub("", (overleaf / relative).read_text(encoding="utf-8"))
        for command, arg in REFERENCE.findall(body):
            targets = arg.split(",") if command == "bibliography" else [arg]
            for raw in targets:
                target = _safe_target(raw.strip())
                base = target.as_posix()
                if command in ("input", "include"):
                    candidates = (base, base + ".tex") if not target.suffix else (base,)
                elif command == "includegraphics":
                    candidates = (base,) if target.suffix else tuple(base + ext for ext in GRAPHICS_SUFFIXES)
                elif command in ("bibliography", "addbibresource"):
                    candidates = (base,) if target.suffix else (base + ".bib",)
                else:
                    candidates = (base,)
                if not any(item in present for item in candidates):
                    raise ValueError(f"{relative}: missing local file for \\{command}{{{raw}}}")


def package_report(project):
    """Validate and zip the Overleaf subtree with main.tex at archive root.

    For example, package_report(Path('reports/test')) creates
    'reports/test/report-overleaf.zip'. It never includes 'artifacts/' or
    files outside 'overleaf/'. Raise ValueError for missing or unsafe files.
    """
    project = Path(project)
    overleaf = project / "overleaf"
    files, directories = _project_files(overleaf)
    check_references(overleaf, files)
    archive = project / "report-overleaf.zip"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=project, prefix=".overleaf-", suffix=".tmp", delete=False) as tmp:
            temporary = Path(tmp.name)
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as output:
            for directory in directories:
                output.writestr(directory.as_posix().rstrip("/") + "/", "")
            for relative in files:
                output.write(overleaf / relative, relative.as_posix())
        os.replace(temporary, archive)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return archive


def main(argv=None):
    """Run the create/package CLI. Returns 0 on success, 2 for invalid input."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("create", "package"):
        command = commands.add_parser(name)
        command.add_argument("project", type=Path, help="Report directory, e.g. reports/my-analysis")
    args = parser.parse_args(argv)
    try:
        result = create_report(args.project) if args.command == "create" else package_report(args.project)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

