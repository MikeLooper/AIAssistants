# Agent Instructions

## Compliance review

When the user asks to review, audit or assess a codebase for architecture, coding standards, security or compliance (OWASP, ISO/IEC 25010, Twelve-Factor, REST API guidelines, MCP server best practices), or to resume a previous compliance review run:

1. Read `compliance-reviewer/ORCHESTRATOR.md` and follow it exactly. It is tool-neutral and includes a capability mapping and a no-subagent fallback.
2. The worker procedure is `compliance-reviewer/WORKER.md`; subject checklists live under `compliance-reviewer/skills/`.
3. Never modify the target codebase. Write only to `transitions/`, `docs/reports/` and a caller-supplied `--out-file`.
4. Pass any operational flags (`--subjects`, `--advanced`, `--analyzers`, `--programmatic`, `--output`, `--out-file`, `--readme`) through to the orchestrator unchanged.

## Standards refresh (maintainers)

When the user asks to refresh, update, re-pin or drift-check the review skills' localized standards, or to collect `localized-standard-gap` notes, read `compliance-reviewer/REFRESH.md` and follow it exactly. This is maintenance, never part of a review; it may fetch only the pages listed in `approved-sources.md`.

The provider-neutral Compliance Reviewer documentation (Claude Code, GitHub Copilot, ChatGPT/Codex, others) is in [compliance-reviewer/README.md](./compliance-reviewer/README.md).
