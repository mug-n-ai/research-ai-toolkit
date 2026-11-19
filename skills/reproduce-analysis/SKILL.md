---
name: reproduce-analysis
description: Trace a reported scientific result to its code, inputs and environment, rerun the analysis and compare with the reference. Use to reproduce a figure, table, numerical value or simulation output, or to check whether a published analysis can be rerun.
license: MIT
metadata:
  author: Lorenzo V. Mugnai
---

# Reproduce an analysis

## Identify the result

Start with the figure, table, value or file the user wants to reproduce. Find the reference output and the workflow that produced it. For a figure, look for the underlying values as well as the rendered image. If there is more than one plausible reference, state which you used and why.

Record the exact command or notebook, code revision and any local changes, input versions or checksums, configuration, software environment and random seeds. Include hardware or numerical settings when they can affect the result. Follow the project's existing records and environment files. If a detail is missing, record what you know and any assumption needed to proceed. Use the optional [reproduction record](reproduction-record.md) when there is no existing place for this information.

## Run the analysis

1. Choose how to compare the outputs before rerunning. Use exact matches for outputs that should be identical. For numerical results, specify an appropriate tolerance and its units. For stochastic results, compare the quantities the original analysis reports with a criterion that accounts for sampling variation. Record why the criterion fits the task.
2. Use the recorded code and environment where available. Run in a separate working or output directory and preserve the original data and reference outputs. Start with the smallest run that exercises the required steps if the full run is expensive. Record any substitute inputs, configurations or dependencies and which part of the result they let you check.
3. Record the commands you actually ran and where they wrote their outputs. If an input, dependency or compute resource is unavailable, report which step is blocked. In a chat without execution access, give the commands and the comparison to make, and report that the run is still pending.

## Compare and report

Compare the reference and rerun against the agreed criterion. Check units, labels, shapes and missing-value handling alongside the numerical values. If a difference matters, locate the first stage at which the results diverge where intermediate outputs are available. Keep any explanation that you have verified distinct from possible causes.

For example, to reproduce a plot from a simulation, locate the run configuration and the file behind each plotted curve. Rerun the simulation and plotting steps, compare the curve values on the same grid, then check that the figure shows those values with the expected units and labels.

Report the reference, the provenance recovered, the run and its output paths, and the measured differences. State whether the requested result matched, differed, was only partly checked or was blocked. Record the evidence for that status and the next step if a gap remains.
