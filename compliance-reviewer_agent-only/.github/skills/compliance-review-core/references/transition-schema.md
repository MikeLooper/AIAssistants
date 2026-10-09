# Transition Files and Resume Protocol

## Location and Naming

All transition files for one run live in `transitions/<runId>/`.

- `runId` format: `<YYYY-MM-DD_HHmm>-<short-target-name>`, e.g. `2026-09-26_1420-myapp`.
- Step files: `NN-<name>.json`, e.g. `00-init.json`, `01-inventory.json`, `10-review-software-quality.json`.
- A worker call covers one `fileBatches` entry and writes one `NN-<skill>.json` file per subject in that batch. Each subject is in exactly one batch, so there are no `.part-K` files. (Older runs may contain `NN-<skill>.part-K.json` files; the aggregation script still merges them.) Each file carries the originating `batchId`.
- Workers write their own subject files; the orchestrator writes only `00`, `01`, `02`, the N/A subject files and `state.json`; the report script writes `90` and `99`.
- Step numbers (fixed; `18` is retired):

| Step | Skill | Step | Skill |
|------|-------|------|-------|
| 10 | review-software-quality | 20 | review-observability |
| 11 | review-software-lifecycle | 21 | review-dependency-management |
| 12 | review-twelve-factor | 22 | review-reliability |
| 13 | review-api-design | 23 | review-performance |
| 14 | review-security-identity-access | 24 | review-disaster-recovery |
| 15 | review-security-input-injection | 25 | review-monitoring |
| 16 | review-security-web-api | 26 | review-cost-sustainability |
| 17 | review-security-operational | 27 | review-maintainability |
| 19 | review-testing | | |
- Superseded files (from a `resume ... from step NN`) move to `transitions/<runId>/superseded/` keeping their original names.
- `state.json` lives at `transitions/<runId>/state.json`.

## Required Header Fields

Every step file (00–99) starts with this header, followed by step-specific content:

```json
{
  "schemaVersion": 1,
  "runId": "2026-09-26_1420-myapp",
  "stepId": "10-review-software-quality",
  "status": "started | completed | failed",
  "startedAt": "ISO-8601 timestamp",
  "completedAt": "ISO-8601 timestamp or null",
  "targetPath": "path supplied by the user",
  "targetGitHead": "commit sha, or null if the target isn't a git repo",
  "inputsHash": "hash of {targetPath, targetGitHead, chosen subjects, analyzer approvals}"
}
```

## `state.json` Layout

```json
{
  "schemaVersion": 1,
  "runId": "string",
  "targetPath": "string",
  "targetGitHead": "string | null",
  "inputsHash": "string",
  "startedAt": "ISO-8601",
  "updatedAt": "ISO-8601",
  "status": "in-progress | completed | failed",
  "subjects": ["chosen subject names"],
  "analyzerApproval": "none | approved-list of analyzer names",
  "linkApprovals": { "https://example.com/x": "approved | denied" },
  "steps": {
    "00-init": "completed",
    "01-inventory": "completed",
    "10-review-software-quality": "completed",
    "...": "not-started | started | completed | failed"
  },
  "reportPath": "docs/reports/... or null until step 99 completes"
}
```

## Resume Rules

1. On startup, list subdirectories of `transitions/` whose `state.json` has `status != completed` and offer to resume the most recent one.
2. `resume run <id>`: read `state.json`, find the first step that is not `completed`, and continue from there. Steps already `completed` are not re-run.
3. `resume run <id> from step <NN>`: move every transition file for step `NN` and all later steps (including their `.part-K` files) into `transitions/<id>/superseded/`, mark those steps `not-started` in `state.json`, then run from step `NN`. Since one batch call writes several subjects' files together, identify every subject transition file with the same `batchId` as a call being superseded and supersede them together, even if a sibling subject's step number is earlier than `NN`; mark all those sibling subject steps `not-started` as well. Re-running that batch call must not leave stale sibling-subject results in place.
4. Before resuming, recompute `targetGitHead` (if applicable) and `inputsHash`. If either differs from the stored value, warn the user and ask whether to continue, restart, or abort.
5. A subject step is only marked `completed` in `state.json` after its transition file exists with `status: "completed"` and passes the report script's `validate` command.
