---
name: run-provenance
description: Record the code revision, configuration, inputs, environment and random seeds of computational runs as they are launched, so each output stays traceable to the run that made it. Use when setting up, launching or organising simulations, model training, data-processing pipelines, parameter sweeps or batch jobs. To rerun an existing reported result and compare it with the reference, use reproduce-analysis instead.
license: MIT
metadata:
  author: Lorenzo V. Mugnai
---

# Run provenance

Record what each run needs before it starts, so that later you can say which code, configuration and inputs produced a figure, table or number without guessing. A run is any computation whose output you may report or build on: a simulation, a model training or fit, a data-processing pipeline, a batch analysis or one member of a parameter sweep. This skill covers runs you are about to launch or are organising now. To rerun a result that has already been reported and compare it with the reference, use `reproduce-analysis`.

## Use what the project already has

Look for an existing convention first, such as run directories, a manifest, a lab notebook, a workflow manager or an experiment tracker. Follow it and fill any gaps listed below. Introduce a new structure only when there is none, and keep it to plain files the project can read without extra software. Describe what you set up.

## Before each run

Write the record before the run starts, so a crash still leaves it behind. Use the project's format, or the [run record](run-record.md) if there is none.

1. **Code.** Record the repository, commit and whether the working tree has uncommitted changes. If it does, save the diff next to the record or ask the user whether to commit first, following the project's Git rules. Record the version of any external program or model the run calls.
2. **Configuration.** Copy the exact configuration files into the run record instead of only pointing at them, since a referenced file can change later. Where the tool can print its fully resolved configuration with defaults, save that too. Record the full command line.
3. **Inputs.** For each input file or dataset, record its location, size and a checksum such as SHA-256, plus the version, release or query that produced it. When a checksum is too slow for a very large input, record the size and modification time and say that no checksum was taken.
4. **Environment.** Record the interpreter and package versions, or the lockfile or container image digest, the machine or cluster partition, the hardware the results depend on, such as the GPU model, the number of threads or processes, and any environment variables that change the results.
5. **Randomness.** Record every seed and the random generator it feeds, including those used for data splits, sampling and initialisation. Note anything that can make results differ between runs even with fixed seeds, such as multithreaded or GPU operations, or library calls documented as nondeterministic.
6. **Purpose.** Write one line on why the run exists and which run or result it should be compared with.

Keep credentials, tokens and personal or restricted data out of the record. Replace them with a placeholder and say where they come from.

## Organise the outputs

- Give each run its own directory with an identifier that sorts by time and stays unique, such as a timestamp plus a short code hash. Never write into a previous run's directory.
- Record the start time, end time, exit status and where the logs are. Mark runs that failed or were stopped, and keep them, because they show which settings were tried.
- For a sweep or a batch, keep one table with a row per run: identifier, the parameters that vary, status and the main outputs. Record the settings that stay fixed once for the whole batch.

## Link results to runs

Every figure, table or number made from run outputs should name the run identifiers it used and the revision of the analysis code that made it. Put this in the file's metadata, in a sidecar file or in the caption notes, following the project's convention. When you summarise results for the user, quote the run identifiers.

## Hand over

Report the runs you launched or recorded, where their records are, and any gap that would stop someone from rerunning them: uncommitted code, a configuration that was not copied, inputs without checksums, missing seeds or an environment without versions. Say which gaps you could not close and what is needed to close them.
