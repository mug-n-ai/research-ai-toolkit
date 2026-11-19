# Skill routing checks

The README says you can describe a task without naming a skill. [`routing.json`](routing.json) lists requests and the skill an assistant should load first for each one, including pairs that are easy to confuse, such as `research` and `literature-review` or `simulation-provenance` and `reproduce-analysis`.

Run the checks after changing a skill description or adding a skill:

```sh
python3 scripts/install.py --client claude   # link the revision you want to test
python3 scripts/run_routing_evals.py --jobs 4
```

Each case starts a fresh Claude Code session in an empty temporary directory. Only the Skill tool is enabled and MCP servers are skipped, so a case cannot change files or reach other services. The script reports the first skill each session loads and exits with status 1 if any case fails.

The checks use your Claude Code account and count towards its usage, so they do not run in CI. They see every skill installed in `~/.claude/skills`, including skills from other sources, which is the setting users will have. Record the toolkit revision, the client version and the model when you report results, since all three affect the choice.

When you add a skill that the assistant can select by itself, add at least one case for it, and one for any skill it could be confused with.
