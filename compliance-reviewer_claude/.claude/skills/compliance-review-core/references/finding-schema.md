# Finding, Strength and Check-Result Schemas

`schemaVersion: 1` for all shapes below.

## Finding

```json
{
  "id": "string, e.g. SEC-IA-003#1",
  "subject": "string, e.g. Security",
  "subSubject": "string, e.g. Identity & Access",
  "checkId": "string, matches an id in the skill's checklist.md",
  "severity": "Error | Warning | Information",
  "title": "short one-line summary",
  "evidence": [
    { "file": "relative/path/from/target/root", "lineStart": 1, "lineEnd": 10, "excerpt": "short verbatim snippet, trimmed" }
  ],
  "standard": "name of the standard or guideline, e.g. OWASP Authentication Cheat Sheet",
  "url": "https://... including a #anchor when possible",
  "recommendation": "concrete, actionable fix",
  "confidence": "High | Medium | Low",
  "effort": "Small | Medium | Large"
}
```

- `evidence` may have more than one entry after aggregation collapses duplicate findings across files.
- `id` should be stable across a re-run of the same step so the aggregator can detect duplicates: `<skill-prefix>-<checkId>#<sequence>`.

## Strength

```json
{
  "id": "string",
  "subject": "string",
  "subSubject": "string",
  "checkId": "string, optional — a checklist item done well",
  "title": "short one-line summary",
  "evidence": [ { "file": "...", "lineStart": 1, "lineEnd": 10, "excerpt": "..." } ],
  "standard": "optional",
  "url": "optional"
}
```

## Check Result

One entry per checklist item, regardless of outcome, so `compliance-report` can render Full Results.

```json
{
  "checkId": "string",
  "subject": "string",
  "subSubject": "string",
  "severityIfFailed": "Error | Warning | Information",
  "result": "pass | fail | N/A",
  "reason": "short explanation, required when result is fail or N/A",
  "findingIds": ["ids of findings raised by this check, if any"]
}
```

- When `compliance-report`'s aggregate step (step 90) identifies a cross-subject semantic duplicate — a different `checkId`/`subject` whose evidence overlaps an existing finding's file+line range — the *suppressed* check still reports `result: fail` here with its own `reason`, but `findingIds` points at the other subject's finding id instead of creating a new one. This keeps every subject's Full Results accurate while the deduplicated `findings` array (and severity counts, top-5 risks) only lists the issue once. Worker subagents don't need to do this themselves; it happens only at aggregation, across all subjects' transition files.

## Output Size Caps

Every token a worker writes is paid for, so keep results compact:

- At most **3 strengths** per subject skill (pick the most significant).
- `excerpt`: one or two lines, at most about 200 characters. `evidence` lists at most 3 locations per finding (the aggregator can still merge more).
- `reason` only for `fail` and `N/A` check results; omit it for `pass`. Keep it to one sentence.
- `recommendation`: one or two sentences.

## Subject Transition File (written by the worker)

The worker writes one file per subject it was given, directly to `transitions/<runId>/<stepId>.json`, as a single JSON object: the required header fields from `transition-schema.md` (with `status: "completed"`) followed by the subject content below. The orchestrator supplies the header values and the `stepId` for each skill.

```json
{
  "schemaVersion": 1,
  "runId": "...",
  "stepId": "10-review-software-quality",
  "status": "completed",
  "startedAt": "ISO-8601",
  "completedAt": "ISO-8601",
  "targetPath": "...",
  "targetGitHead": null,
  "inputsHash": "...",
  "batchId": "batch-1",
  "skill": "review-<name>",
  "subject": "string",
  "findings": [ /* Finding[] */ ],
  "strengths": [ /* Strength[] */ ],
  "checkResults": [ /* CheckResult[] */ ],
  "urlsFetched": ["https://..."],
  "notes": "optional short string"
}
```

- Finding ids are `<checkId>#<sequence>` (no batch suffix; a subject runs in exactly one batch).
- Every checklist item gets one `checkResults` entry; every `fail` result names its `findingIds`.
- Each file is self-contained, so a malformed file only costs a single-subject retry.

## Worker Status Reply

The worker returns only this short JSON object (no prose, no fences). It does not echo findings back; the orchestrator never needs them in context.

```json
{
  "batchId": "batch-1",
  "written": [
    { "skill": "review-api-design", "path": "transitions/<runId>/13-review-api-design.json", "findings": 2, "strengths": 1, "checks": 8 }
  ],
  "failed": [
    { "skill": "review-security-web-api", "reason": "short reason" }
  ]
}
```
