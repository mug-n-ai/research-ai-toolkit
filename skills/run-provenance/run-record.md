# Run record

Copy this file into the run directory and fill it in before the run starts. Add the end time, status and outputs when it finishes.

| Item | Record |
| --- | --- |
| Run identifier | [Timestamp plus short code hash, unique within the project] |
| Purpose | [Why this run exists and which run or result it should be compared with] |
| Code | [Repository, commit, uncommitted changes (saved diff path) and versions of external programs or models] |
| Configuration | [Copied configuration files, resolved configuration if available, full command line] |
| Inputs | [Location, size and checksum of each input; version, release or query that produced it] |
| Environment | [Interpreter and package versions, lockfile or container digest, machine or partition, relevant hardware, threads or processes, relevant environment variables] |
| Randomness | [Every seed and the generator it feeds; anything that can change results between runs] |
| Execution | [Start and end time, exit status, log paths] |
| Outputs | [Output files or directory and the main values] |
| Gaps | [Anything not recorded, why, and what would close the gap] |
