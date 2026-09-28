# Transition Files and Resume Protocol

## Location and Naming

All transition files for one run live in `transitions/<runId>/`.

- `runId` format: `<YYYY-MM-DD_HHmm>-<short-target-name>`, e.g. `2026-09-26_1420-myapp`.
- Step files: `NN-<name>.json`, e.g. `00-init.json`, `01-inventory.json`, `10-review-software-quality.json`.
- Batched steps: `NN-<skill>.part-K.json` (K starting at 1), one per batch of files reviewed by the worker.
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
3. `resume run <id> from step <NN>`: move every transition file for step `NN` and all later steps (including their `.part-K` files) into `transitions/<id>/superseded/`, mark those steps `not-started` in `state.json`, then run from step `NN`.
4. Before resuming, recompute `targetGitHead` (if applicable) and `inputsHash`. If either differs from the stored value, warn the user and ask whether to continue, restart, or abort.
5. A step is only marked `completed` in `state.json` after its transition file (and all `.part-K` files, for batched steps) is written successfully.
