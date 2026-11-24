# Documenting code, data and diagrams

A technical report should expose how a result was obtained, without becoming a code dump or a substitute for running the analysis.

## Code and data

- Explain the computational problem, algorithmic choices, assumptions, inputs, transformations, intermediate representations and outputs. Identify relevant function/module paths, repository revision, configuration, data version and run identifier. Use `run-provenance` or `reproduce-analysis` when relevant.
- Show a small code excerpt with `listings` only when an implementation detail is easier to understand from code than from an equation or explanation. Keep excerpts tied to a source path and revision. Do not copy full modules or private configurations into the Overleaf project.
- Prefer tables for precise comparisons and summary values; use actual checked data with units, definitions, uncertainties and selection criteria. Keep large or restricted input data outside the report and record how to locate it through approved channels.

## Diagrams and figures

Ask what the reader must understand. A diagram is useful for physical geometry, data flow, software architecture, sequence of transformations, dependencies or decision branches. Choose the smallest representation that clarifies that relationship. Include a caption explaining every meaningful symbol or stage; distinguish illustrative structure from measured values.

- Use **TikZ** for a small self-contained physical or mathematical schematic when its maintainability justifies adding that package to this report.
- Use **Mermaid** or an existing code-driven workflow description when the project already maintains one; export to a PDF or PNG before packaging, rather than requiring Mermaid tooling on Overleaf.
- Use **Matplotlib** or existing scientific plotting code for quantitative plots. Inspect the plotted values, axes, uncertainty, provenance and transformations; prefer vector PDF when the plot supports it. Never redraw a verified plot by guessing its data.
- Keep the full code that generated figures with the original analysis, and record that source. Include only the final figure asset in the Overleaf source directory.

Avoid diagrams that merely decorate the report, repeat nearby prose or imply stronger causal or numerical relationships than the evidence supports. Do not fabricate data, error bars or relationships to make a diagram look complete. Verify that linked images actually exist under `overleaf/` before exporting.

