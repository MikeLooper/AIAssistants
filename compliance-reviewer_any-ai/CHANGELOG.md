# Changelog

All notable changes to the Compliance Reviewer are recorded here. The tool follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html); the current version is in [VERSION](VERSION). See [Versioning](compliance-reviewer/README.md#versioning) for what counts as a major, minor or patch change.

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
