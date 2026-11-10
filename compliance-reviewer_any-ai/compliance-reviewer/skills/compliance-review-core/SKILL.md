---
name: compliance-review-core
description: 'Shared schemas, scoring rubric, language detection and transition/resume conventions for the compliance review agent pipeline, plus the maintainer-only source registry. Use when the compliance-reviewer orchestrator or the compliance-subject-reviewer worker needs the finding schema, severity rules or transition file format.'
user-invocable: false
---

# Compliance Review Core

Shared reference material for the compliance review pipeline. This skill has no procedure of its own — the orchestrator and worker agents load individual reference files as needed.

## References

- [`references/approved-sources.md`](./references/approved-sources.md) — the Link Access Policy (no review-time fetching) and the maintainer-only registry of source pages used to refresh local standards. Not loaded during a review.
- [`references/severity-and-scoring.md`](./references/severity-and-scoring.md) — wording-to-severity mapping, fallback rubric, scoring formula and rating bands.
- [`references/finding-schema.md`](./references/finding-schema.md) — JSON shapes for findings, strengths and check results.
- [`references/transition-schema.md`](./references/transition-schema.md) — transition file naming, required header fields, `state.json` layout and resume rules.
- [`references/languages.md`](./references/languages.md) — how languages are detected and the convention for loading per-language reference files.
- [`references/status-format.md`](./references/status-format.md) — the per-step status line format.

## When to Load What

- The orchestrator loads the five review-time references (all except `approved-sources.md`) once at the start of a run.
- The worker (see `compliance-reviewer/WORKER.md`) loads `finding-schema.md` (for its transition-file shape and size caps), `severity-and-scoring.md` (for severity assignment) and `languages.md` (to know which language files to load from its assigned skill).
- Nobody loads `approved-sources.md` during a review. Maintainers use it when they refresh a skill's local standards.
