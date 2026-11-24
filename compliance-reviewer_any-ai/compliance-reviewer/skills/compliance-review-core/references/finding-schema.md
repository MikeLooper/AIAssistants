# Finding, Strength and Check-Result Schemas

`schemaVersion: 2` for everything a worker writes. Workers write only what the report script can't work out for itself. The script takes labels and check severities from the skill's `checklist.md`, and builds citations from the element ID. (Older `schemaVersion: 1` files, with labels, `severityIfFailed`, `standard`/`url` and a `checkResults` array, are still read.)

## Finding

```json
{
  "id": "API-05#1",
  "checkId": "API-05",
  "element": "AZ-031",
  "severity": "Error | Warning | Information",
  "title": "short one-line summary",
  "evidence": [
    { "file": "relative/path/from/target/root", "lineStart": 1, "lineEnd": 10, "excerpt": "short verbatim snippet, trimmed" }
  ],
  "recommendation": "concrete, actionable fix",
  "confidence": "High | Medium | Low",
  "effort": "Small | Medium | Large"
}
```

- `checkId` must be an active id in the skill's `checklist.md`. An unknown id blocks `validate`; a retired id only warns and is dropped from scoring.
- `element` is the ID of the failed standards element (the ID column of the skill's `references/standards/*.md`, as shown in its review pack). The report script turns it into `standard` (`"<source name> — <element ID>"`) and `url` (citation base + page + primary anchor). Don't write `standard` or `url`.
  - Give each distinct element violation its own finding: two findings of one check merge only when they cite the same element.
  - `page` (optional): only for an element whose source has one page per version, such as the OpenAPI Specification. Give the spec's version line (`3.0.x`, `3.1.x`, `3.2.x`, `2.0`).
  - When no element fits, leave `element` out. Then give `standard` (and optionally `url`) yourself; this is rare. A `url` with no scheme is a repo path relative to `docs/reports/`.
- Don't write `subject` or `subSubject`; the script takes them from the checklist (by skill and `checkId`).
- `evidence` may have more than one entry after aggregation collapses duplicate findings across files.
- `id` is `<checkId>#<sequence>`, stable across a re-run of the same step.

## Repository contents

In every check, *committed*, *in the repository*, *checked in* and *tracked* mean *present in the target's working files*. Judge only files on disk. Never run Git commands or read `.git/` to find tracked, ignored, staged or historical content. Read `.gitignore` as a plain file when a skill needs it (e.g. SL-12). The orchestrator's single `git -C <target> rev-parse HEAD` call (run by the report script's `init`, for `targetGitHead`) is the only Git command in a review.

## Strength

```json
{ "id": "API-09#s1", "checkId": "API-09", "title": "short one-line summary", "evidence": [ { "file": "...", "lineStart": 1, "lineEnd": 10, "excerpt": "..." } ], "element": "AZ-009" }
```

`checkId` and `element` are optional.

## Check results (`checks`)

Every active checklist item appears exactly once, under one of three keys:

```json
"checks": {
  "pass": ["API-01", "API-02", "API-04"],
  "fail": { "API-05": { "findingIds": ["API-05#1"], "reason": "optional one sentence" } },
  "na":   { "API-13": "no long-running operations" }
}
```

- `pass`: a list of check ids.
- `fail`: check id → `findingIds` (required) and an optional `reason`. When `reason` is left out, the report shows the first finding's title.
- `na`: check id → the reason (one sentence, required).
- The script adds each check's label and default severity (`severityIfFailed`) from `checklist.md`, and scores from these results.
- A cross-subject duplicate is handled only at aggregation (step 90): a suppressed finding's check stays `fail` in its own subject, and the report points at the other subject's finding. Workers don't do this themselves.

## Output Size Caps

Every token a worker writes is paid for, so keep results compact:

- Write the file as compact JSON (no indentation).
- At most **3 strengths** per subject skill (pick the most significant).
- `excerpt`: one or two lines, at most about 200 characters. `evidence` lists at most 3 locations per finding (the aggregator can still merge more).
- `reason`: one sentence, for `na` and, only when the finding titles don't explain the failure, for `fail`.
- `recommendation`: one or two sentences.

## Subject Transition File (written by the worker)

The worker writes one file per subject it was given, to the `out` path in its dispatch payload (`transitions/<runId>/<stepId>.json`), as one JSON object: the payload's `header` values plus `stepId`, `status: "completed"` and `completedAt`, followed by the subject content.

```json
{
  "schemaVersion": 2,
  "runId": "...",
  "stepId": "13-review-api-design",
  "status": "completed",
  "startedAt": "ISO-8601",
  "completedAt": "ISO-8601",
  "targetPath": "...",
  "targetGitHead": null,
  "inputsHash": "...",
  "batchId": "batch-1",
  "skill": "review-api-design",
  "findings": [],
  "strengths": [],
  "checks": { "pass": [], "fail": {}, "na": {} },
  "notes": "optional short string"
}
```

- Each file is self-contained, so a malformed file only costs a single-subject retry.
- `validate` checks that every active check id appears exactly once and that every `fail` names its findings.

## Worker Status Reply

The worker returns only this short JSON object (no prose, no fences). It does not echo findings back; the orchestrator never needs them in context.

```json
{
  "batchId": "batch-1",
  "written": [
    { "skill": "review-api-design", "path": "transitions/<runId>/13-review-api-design.json", "findings": 2, "strengths": 1, "checks": 15 }
  ],
  "failed": [
    { "skill": "review-security-web-api", "reason": "short reason" }
  ]
}
```
