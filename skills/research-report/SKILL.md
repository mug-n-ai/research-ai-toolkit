---
name: research-report
description: Document an existing research investigation as a technical LaTeX note with physical equations, methods, code and data provenance, checks and explanatory diagrams. Use for research notes, analysis reports, model derivations and pipeline documentation. Not for drafting journal papers or inventing scientific results.
license: MIT
metadata:
  author: Lorenzo V. Mugnai
---

# Research report

Produce a **technical record that helps a researcher understand, inspect and reproduce their work**. This skill does not draft journal manuscripts, assemble publication narratives, invent results or replace scientific judgement. If the task is a paper draft, do not repurpose this workflow; the existing `literature-review` skill can still help check claims and sources in an existing text.

## Establish the evidence and purpose

1. Identify the question, intended reader and work to document: a physical derivation, code or method, dataset, run, comparison, technical decision or verified result. Check the project for an existing report and LaTeX conventions. Preserve them where appropriate; use the starter only when no suitable structure exists.
2. Inspect the actual code, configuration, data summaries, figures, run records and cited sources relevant to the report. Track what you verified, what was supplied without independent checking and what is still missing. Ask for indispensable inputs; never fill a gap with fabricated results, references, parameter values or claims.
3. Look for author- or project-supplied writing preferences, external voice skills and style guides. Apply them to prose instead of imposing a toolkit voice. Keep scientific precision, mathematical meaning, provenance and uncertainty intact. Flag genuine instruction conflicts.

## Explain the science, not just the output

Lead with the physical question and define the model before displaying results. Explain why an equation applies, define symbols and units, and state assumptions, boundaries and approximations. Include the steps needed to understand a derivation, dimensional and limiting-case checks, and how uncertainties affect interpretation. Read [equations and physics](references/equations-and-physics.md) when working through a model or calculation.

Use headings suited to the work, for example scope and provenance, physical model, methods and computational workflow, verified checks or results, limitations and unresolved questions. **Do not impose a journal manuscript structure** or create a paper-style abstract, speculative discussion or conclusions not supported by the investigation.

When reporting on code or data, describe inputs, transformations, algorithms, outputs, environment and run identifiers. Prefer relevant short snippets and links to versioned source code over copying whole modules or raw datasets. Consider a diagram when it clarifies a physical relation, algorithm, pipeline or dependency better than prose. Figures and plots must come from checked data, equations or documented code, not illustrative numbers passed off as measurements. See [code, data and diagrams](references/code-data-and-diagrams.md) and use `scientific-visualization`, `uncertainty-and-units`, `run-provenance` or `literature-review` when their checks are relevant and available.

## Write portable LaTeX

Use existing project conventions first. For a new report, start from the bundled [LaTeX template](templates/overleaf/main.tex) and read [LaTeX conventions](references/latex-conventions.md). The default is KOMA-Script `scrartcl` with common TeX packages, not a custom document class or a journal template.

When local Python is available, create a self-contained report folder with the bundled [report project helper](scripts/report_project.py):

```sh
python3 /path/to/research-ai-toolkit/skills/research-report/scripts/report_project.py create reports/my-analysis
```

The helper creates `reports/my-analysis/overleaf/main.tex`, `sections/`, `figures/`, `tables/` and `references.bib`, with `artifacts/` beside the source for local output. Edit the new files, replacing all instructional placeholders. Use literal relative references from the root `main.tex` file, such as `\input{sections/model}` or `\includegraphics{figures/result.pdf}`. Put **only files required to compile and understand the report** in `overleaf/`; keep raw datasets, credentials, logs and unrelated code outside it. For an existing LaTeX project, adapt its structure rather than overwriting it.

If `latexmk` and a suitable TeX installation are available, compile from the `overleaf/` directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../artifacts main.tex
```

Check the log, unresolved citations and references, mathematical notation, table readability and the rendered PDF. Inspect diagrams and plots visually, including axes, units and captions. If compiling is unavailable, report that explicitly and leave the PDF as pending; do not claim Overleaf has compiled the project.

After checking the sources, package the same folder without including local build artefacts:

```sh
python3 /path/to/research-ai-toolkit/skills/research-report/scripts/report_project.py package reports/my-analysis
```

The helper checks literal `\input`, `\includegraphics`, bibliography and code-listing paths, rejects missing or unsafe resources and creates `reports/my-analysis/report-overleaf.zip` with `main.tex` **at the archive root**. These checks do not interpret arbitrary TeX macros or replace compilation. Import the ZIP using Overleaf's *New Project > Upload Project* option. No Overleaf account, shell escape, remote service or additional Python dependency is needed to create the ZIP.

## Hand over

Provide the report source directory, Overleaf ZIP path and PDF path **only if the relevant files were actually created**. State the research inputs and source revisions, important checks performed, what was not independently verified, whether local compilation succeeded and whether the file was actually tested on Overleaf. Leave authorship, scientific decisions and publication choices with the researcher.

