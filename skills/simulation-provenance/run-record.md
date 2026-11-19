# Run record

Copy this file into the run directory and fill it in before the run starts. Add the end time, status and outputs when it finishes.

| Item | Record |
| --- | --- |
| Run identifier | [Timestamp plus short code hash, unique within the project] |
| Purpose | [Why this run exists and which run or result it should be compared with] |
| Code | [Repository, commit, uncommitted changes (saved diff path) and versions of external simulation codes] |
| Configuration | [Copied configuration files, resolved configuration if available, full command line] |
| Inputs | [Path, size and checksum of each input; version or source of reference data] |
| Environment | [Interpreter and package versions, lockfile or container digest, machine or partition, threads or processes, relevant environment variables] |
| Randomness and numerics | [Every seed and the generator it feeds; settings that can change results between runs] |
| Execution | [Start and end time, exit status, log paths] |
| Outputs | [Output files or directory and the main values] |
| Gaps | [Anything not recorded, why, and what would close the gap] |
