---
name: simulation-provenance
description: Record the code revision, configuration, inputs, environment and seeds of simulation or pipeline runs as they are launched, so each output stays traceable to the run that made it. Use when setting up, launching or organising simulation runs, parameter sweeps or batch jobs. To rerun an existing reported result and compare it with the reference, use reproduce-analysis instead.
license: MIT
metadata:
  author: Lorenzo V. Mugnai
---

# Simulation provenance

Record what each run needs before it starts, so that later you can say which code, configuration and inputs produced a figure or number without guessing. This skill covers runs you are about to launch or are organising now. To rerun a result that has already been reported and compare it with the reference, use `reproduce-analysis`.

## Use what the project already has

Look for an existing convention first: run directories, a manifest, a lab notebook, or a tool such as a workflow manager or experiment tracker. Follow it and fill any gaps listed below. Introduce a new structure only when there is none, and keep it to plain files the project can read without extra software. Describe what you set up.

## Before each run

Write the record before the run starts, so a crash still leaves it behind. Use the project's format, or the [run record](run-record.md) if there is none.

1. **Code.** Record the repository, commit and whether the working tree has uncommitted changes. If it does, save the diff next to the record or ask the user whether to commit first, following the project's Git rules. Record the version of any external simulation code the run calls.
2. **Configuration.** Copy the exact configuration files into the run record instead of only pointing at them, since a referenced file can change later. Where the tool can print the fully resolved configuration with its defaults, save that too. Record the full command line.
3. **Inputs.** For each input file, record its path, size and a checksum such as SHA-256, plus the version or source of reference data. For very large files where a checksum is too slow, record the size and modification time and say that no checksum was taken.
4. **Environment.** Record the interpreter and package versions, or the lockfile or container image digest, the machine or cluster partition, the number of threads or processes, and any environment variables that change the numerics.
5. **Randomness and numerics.** Record every seed and the random generator it feeds. Note settings that can make results differ between runs even with fixed seeds, such as parallel reduction order, GPU kernels or adaptive time steps.
6. **Purpose.** Write one line on why the run exists and which run or result it should be compared with.

Do not write credentials, tokens or private paths that should not leave the machine into the record. Replace them with a placeholder and say where they come from.

## Organise the outputs

- Give each run its own directory with an identifier that sorts by time and stays unique, such as a timestamp plus a short code hash. Never write into a previous run's directory.
- Record the start time, end time, exit status and where the logs are. Mark runs that failed or were stopped, and keep them, because they show which settings were tried.
- For a parameter sweep, keep one table with a row per run: identifier, the parameters that vary, status and the main outputs. Record the values that stay fixed once for the whole sweep.

## Link results to runs

Every figure, table or number made from run outputs should name the run identifiers it used and the revision of the analysis script that made it. Put this in the figure's metadata, in a sidecar file or in the caption notes, following the project's convention. When you summarise results for the user, quote the run identifiers.

## Hand over

Report the runs you launched or recorded, where their records are, and any gap that would stop someone from rerunning them: uncommitted code, a configuration that was not copied, inputs without checksums, missing seeds or an environment without versions. Say which gaps you could not close and what is needed to close them.
