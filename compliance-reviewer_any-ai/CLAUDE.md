# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A provider-neutral **Compliance Reviewer**: a set of Markdown instructions and skills that let an AI tool review an *external* target codebase (architecture, coding standards, security, testing, operations) and produce one scored Markdown report. It's mostly prompt content, plus the report script and a maintainer-only source-drift script. There's no build, package manager or test suite.

`AGENTS.md` is the cross-tool entry point. Full docs: [compliance-reviewer/README.md](compliance-reviewer/README.md).

## Running a review

- `/compliance-reviewer <path-to-target> [subjects | resume run <id> [from step <NN>]] [flags]` loads [.claude/skills/compliance-reviewer/SKILL.md](.claude/skills/compliance-reviewer/SKILL.md). That file sends you to [compliance-reviewer/ORCHESTRATOR.md](compliance-reviewer/ORCHESTRATOR.md); follow it exactly.
- For a target outside this workspace, use `/add-dir <path>`.
- Hard rules from the orchestrator:
  - The target is **read-only**.
  - Write only to `transitions/<runId>/`, `docs/reports/` and a caller-supplied `--out-file` (never inside the target).
  - Don't read Git data unless the user asks. The one exception is `git -C <target> rev-parse HEAD`.
  - IaC review and CLI analyzers run only with `--advanced` on (default off). Analyzers run only when approved for that run: chosen in the interview, or selected by `--analyzers` (default `auto`).
  - Never fetch URLs during a review. `compliance-review-core/references/approved-sources.md` is a maintainer-only registry of the source pages used to refresh local standards.
  - With no flags, interview the user (subjects "all" or a subset, and advanced usage). With any flag, or `--programmatic`, don't ask: use the given flags and defaults for the rest. `--programmatic` also suppresses all chat and returns only the report text or a one-line JSON status.
- Operational flags (`--subjects`, `--advanced`, `--analyzers`, `--programmatic`, `--output`, `--out-file`, `--readme`) are defined in the orchestrator's "Operational flags" section and described for users in the README. Keep the two in sync.

## Report script (Python 3, stdlib only)

```
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py validate  transitions/<runId>
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py aggregate transitions/<runId>
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py render    transitions/<runId> --out docs/reports/<target>-compliance-review-<YYYY-MM-DD_HHmm>.md [--copy-to <out-file>]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py labels    [skill ...]
python -m unittest discover -s compliance-reviewer/skills/compliance-report/scripts
```

`validate` prints `{ok, missing, problems, warnings}` and exits non-zero on failure. [.claude/settings.json](.claude/settings.json) pre-approves this script and writes to `transitions/**` and `docs/reports/**`. The only tests are the label-normalization regression tests above. The README says to check changes against a small sample repo.

**Labels are data, not model output.** Each `review-*/references/checklist.md` owns its `Subject:` line and a `Sub-subject` column; `aggregate`/`render` rewrite every worker label from it, and `validate` warns on drift and blocks unknown `checkId`s or missing check results. After editing any checklist, run `labels` (lint). Plan: [docs/plan-fix-labels.md](docs/plan-fix-labels.md).

## Architecture

- **Neutral content, thin adapters.** All real rules live once under `compliance-reviewer/`. Tool-specific files only point at the neutral files and map generic capabilities ("ask the user", "delegate to a worker", "shell", "todo list"; there is no fetch capability, because reviews never fetch URLs) to that tool's names:
  - Claude Code: `.claude/skills/…/SKILL.md`, `.claude/agents/compliance-subject-reviewer.md`
  - GitHub Copilot: `.github/prompts/…`, `.github/agents/…`
  - Codex and other tools: `AGENTS.md`
  - Paste-in chat: `compliance-reviewer/PROMPT.md`

  Keep adapters to a few lines and never copy rules into them.
- **Pipeline** (step numbers come from `compliance-review-core/references/transition-schema.md`):
  1. `00` init
  2. `01` inventory, done by the orchestrator using `compliance-inventory`. It gives each subject a capped file list (max 12) and groups subjects with overlapping lists into `fileBatches`.
  3. `02` optional analyzers
  4. `10–29` subject reviews. Step `18` is unused because coding standards fall under `review-software-quality`; step `28` is `review-mcp-server`.
  5. `90` aggregate
  6. `99` render
- **Orchestrator / worker split.** The orchestrator makes one worker call per `fileBatches` entry, using the `compliance-subject-reviewer` subagent, which follows [compliance-reviewer/WORKER.md](compliance-reviewer/WORKER.md). The worker writes its own `transitions/<runId>/NN-review-<subject>.json` files and returns only a short `written`/`failed` status, so the orchestrator never handles the findings itself. Without subagents, the orchestrator runs WORKER.md in-session, one batch at a time.
- **N/A subjects.** `review-api-design` is marked N/A when no API is found. `review-mcp-server` is N/A when no MCP server is found; for a stdio-only MCP server (no HTTP surface), `review-api-design` and `review-security-web-api` are N/A. Disaster recovery, monitoring and cost/sustainability are marked N/A when `iacFound` is false, which is always the case with `--advanced` off (the inventory then skips IaC and excludes IaC files from every subject). For these, the orchestrator writes a minimal transition file itself instead of calling a worker.
- **Resumability.** `transitions/<runId>/state.json` tracks step status. `resume run <id> from step <NN>` moves later files into `superseded/`.
- **Aggregation logic** is in the script, not in prompts: dedup by evidence-location IoU ≥ 0.5 (same check + same `standard` within a subject, or across different subject skills; different checks in one skill never merge), scoring from `severity-and-scoring.md`, and top-5 risk ordering. If you change the scoring or dedup rules, update the script and `compliance-report/SKILL.md` together.
- **Schemas** live in `compliance-review-core/references/` (`finding-schema.md`, `transition-schema.md`). Bump `schemaVersion` on breaking changes. Keep the script's `FILE_RE` and `HEADER_KEYS` in sync with them.

## Extending

- **New subject:**
  1. Add `compliance-reviewer/skills/review-<name>/` containing `SKILL.md`, `references/checklist.md` and `references/sources.md`.
  2. Register it in the subject table in `ORCHESTRATOR.md`, the step table in `transition-schema.md`, `compliance-inventory/references/subject-file-map.md` and `approved-sources.md`.
  3. Gate IaC-only subjects on `iacFound`, and check for overlap with existing subjects first.
- **Localized standards:** summarize external sources into `references/standards/<source>.md` (pinned version, at most 100 elements per skill per website unless an exception is recorded, an anchor per element) and declare them in `SKILL.md` under `## Standards (local, authoritative)`. List the exact source pages as maintenance-only entries in `approved-sources.md`. Put maintainer-only refresh notes in `references/standards/MAINTENANCE.md`. The refresh strategy (cadence, triggers, steps, AI-tool usage) is centralized in [compliance-reviewer/STANDARDS-MAINTENANCE.md](compliance-reviewer/STANDARDS-MAINTENANCE.md); refreshing is the only time fetching approved pages is allowed, and never during a review. Run it with `/refresh-standards [<skill>... | all] [check | gaps | full]` (procedure: [compliance-reviewer/REFRESH.md](compliance-reviewer/REFRESH.md)). Each localized skill keeps its source pins in `references/standards/pins.json`; `python compliance-reviewer/scripts/check_source_drift.py lint|check [skill]` validates them against the headers and the live sources. Keep `pins.json` in step with header pins. See [compliance-reviewer/README.md](compliance-reviewer/README.md); for a worked example, see [compliance-reviewer/skills/review-api-design/](compliance-reviewer/skills/review-api-design/).
- **New language:** add `references/languages/<id>.md` to the skills that need it, and add a detection signal in `compliance-review-core/references/languages.md`. The C#, Java, Python and JavaScript/TypeScript files already exist in the security skills.

## Environment notes (from `.github/copilot-instructions.md`)

- Windows with PowerShell (`pwsh`).
- The `pilot` MCP server is a local .NET project. [.mcp.json](.mcp.json) and [.vscode/mcp.json](.vscode/mcp.json) point at different project paths. If a pilot MCP call returns an error or non-success status, stop automated processing and report the status code, description and endpoint.
- Keep documentation in `docs/` current when adding build systems, prerequisites, environment variables or workflows.
