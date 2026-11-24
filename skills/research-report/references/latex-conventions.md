# Portable LaTeX conventions

Use an established report template or document class already present in the research project. For a new self-contained report the bundled default is `scrartcl` from KOMA-Script, with `mathtools`, `amssymb`, `siunitx`, `graphicx`, `booktabs`, `tabularx`, `listings`, `natbib`, `hyperref` and `cleveref`. These are common packages on full TeX distributions and Overleaf. Use `pdflatex` via `latexmk` by default. Choose a different engine or package only when the material requires it, and document why.

Put `main.tex` in the root of the exportable `overleaf/` subtree. Put substantive sections in `sections/`, figure assets in `figures/`, small report tables in `tables/` when appropriate and checked bibliographic records in `references.bib`. Use file references relative to `main.tex`, with explicit paths such as `\input{sections/workflow}` and `\includegraphics{figures/pipeline.pdf}`. Prefer PDF, PNG or JPEG assets and avoid needing external commands or shell escape during compilation. A custom class, plugin, font or nonstandard package must be bundled or otherwise verified available in the target TeX environment.

Write a coherent symbol and unit convention; use `\label` and `\cref` for cross-references. Explain derivations in prose adjacent to their equations. Prefer `booktabs` rules and aligned columns for tables. Use `listings` only for necessary code excerpts, not entire source trees. A code sample imported with `\lstinputlisting` is a dependency that must be included and checked. Add citations only for sources actually read or verified; never invent DOI or bibliography records. Enable the template's bibliography commands once real references are present.

The helper's output structure is:

```
reports/<name>/
  overleaf/
    main.tex
    sections/
    figures/
    tables/
    references.bib
  artifacts/            # Local PDF and build files, excluded from export
  report-overleaf.zip   # Archive of overleaf/ contents, main.tex at ZIP root
```

Run the helper's `package` command after edits and inspect its output. This performs limited checks on literal local file references, not complete TeX dependency analysis. Compiling and reviewing the PDF remain required where tools are available. Do not claim cloud-side compatibility until it has actually been tested. When Overleaf imports the ZIP, confirm the detected main document is `main.tex`.

Do not upload secret tokens, unpublished materials or restricted datasets to an unapproved cloud service. An Overleaf-ready archive is only a packaging format; the user decides whether the project's data may be uploaded.

