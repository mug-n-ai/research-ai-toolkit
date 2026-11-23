---
name: research
description: Investigate a technical question about software, such as library or API behaviour, tool documentation, specifications or source code, against primary sources and capture the findings as a Markdown file in the repo. Use when the user wants docs or API facts gathered or reading legwork delegated to a background agent. For scholarly papers, published results or scientific claims, use literature-review instead.
license: MIT
---

Spin up a **background agent** to do the research, so you keep working while it reads. Start it with a fresh context window.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. When comparing dependencies or implementations, check the options against the project's requirements and supported versions. For numerical methods, check their assumptions and valid regime. Recommend whether to reuse, adapt or implement the method and explain why.
3. Write the findings to a single Markdown file, citing each claim's source.
4. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
