# Changelog

All notable changes to the Compliance Reviewer are recorded here. The tool follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html); the current version is in [VERSION](VERSION). See [Versioning](compliance-reviewer/README.md#versioning) for what counts as a major, minor or patch change.

## [2.0.0] - 2026-11-20

Implements recommendations 2, 3 and 4 of [docs/ai/improvements-review_2026-11-20.md](docs/ai/improvements-review_2026-11-20.md) to lower the AI cost of a run. Major version because the worker output schema changed (`schemaVersion` 2).

- **Compact worker output (`schemaVersion` 2).** Workers no longer write `subject`, `subSubject`, `severityIfFailed`, `standard`, `url` or `urlsFetched`. They write check results as `checks: {pass: [...], fail: {id: {findingIds, reason?}}, na: {id: reason}}`, cite standards by `element` ID (plus `page` for per-version OpenAPI links), and write compact JSON. The report script derives labels and default severities from each checklist and citations from the standards files (`scripts/standards.py`). `validate` checks that each active check appears exactly once. schemaVersion 1 files are still read; re-aggregating recorded runs gives identical results, and converting them to the new schema reproduced their scores, top risks and duplicates exactly.
- **Scripted run steps.** `compliance_report.py` gained `init` (step 00: run id, `targetGitHead`, `inputsHash`, `--out-file` check), `inventory` (step 01, deterministic, driven by the new `compliance-inventory/references/subject-file-map.json` and `scripts/inventory.py`, with `--picks` for capped subjects), `na` (N/A subject files), `dispatch` (one worker payload per batch, `--only` for retries), `step`, `resume` (hash check and `--from` supersede, batch siblings included) and `validate --mark` (records subject steps in `state.json`). The orchestrator now only runs these commands, reviews capped samples, delegates the payloads and runs analyzers; the inventory skill's prompt procedure is the no-Python fallback.
- **Review packs.** Workers read one generated file per skill (`compliance-reviewer/packs/<skill>.md`) plus one per detected language (`<skill>.<language>.md`) instead of `SKILL.md`, `checklist.md`, `sources.md` and the standards files separately. Packs omit citation columns, header pin metadata, page-key tables, retired rows and `sources.md`. They are built with `compliance_report.py packs build`; `packs check` and `labels` flag a pack that is out of date.
- **Lint.** `labels` also checks that every checklist row has a `Default severity`, that every active standards element resolves to a citation, that packs are current, and that the inventory map is valid.
- Each review skill's "Citations" step now asks for `element` only; the four skills that told workers to copy labels now say the script adds them.
- The default inventory sample can differ from the earlier model-chosen one, so per-subject findings may differ between runs before and after this release.
## [1.0.1] - 2026-11-20

- Claude Code: the worker subagent (`.claude/agents/compliance-subject-reviewer.md`) now runs on Sonnet (`model: sonnet`) instead of inheriting the session's model, which should roughly halve the cost of a run (recommendation 1 of [docs/ai/improvements-review_2026-11-20.md](docs/ai/improvements-review_2026-11-20.md)). `--model` in `run_review.py`, the testers and the API now sets only the orchestrator's model.
- Test harness: `<app>-result.json` and `<app>-result.md` record the Claude cost per model (`costByModel`), so orchestrator and worker cost can be compared.

## [1.0.0] - 2026-11-16

First versioned release. It establishes the baseline: everything the tool did on this date is 1.0.0.

- 18 review subjects under `compliance-reviewer/skills/review-*`, including MCP Server, with localized, pinned standards (no URL fetching during reviews).
- Provider-neutral orchestrator and worker with thin adapters for Claude Code, GitHub Copilot, Codex/`AGENTS.md` and paste-in chat (`PROMPT.md`).
- Resumable runs via transition files (`transitions/<runId>/`), finding and transition schemas at `schemaVersion` 1.
- Deterministic report script (`compliance_report.py validate | aggregate | render | labels`) and the maintainer-only drift checker (`check_source_drift.py`).
- Operational flags, programmatic mode and the headless runner `scripts/run_review.py`.
- comp-review-api (`api/`): a FastAPI HTTP API on port 12001 with a Swagger UI. It provides about and health endpoints, reviews of uploaded source zips, the nine validation testers as background jobs, per-request AI tool and model selection, and an `Environment` setting (`production` switches the tester endpoints off: absent from Swagger, 404 on a direct call). Covered by unit tests.
- comp-review-ui (`webui/`): an Angular web UI on port 12101. It uploads a zip, or a directory zipped in the browser, runs the testers, follows jobs, and shows the final report and test result. A runtime `config.json` sets `environment` (`production` hides the testers). Covered by unit tests.

Earlier, unversioned changes are described under "Maintenance" in [compliance-reviewer/README.md](compliance-reviewer/README.md#maintenance).
