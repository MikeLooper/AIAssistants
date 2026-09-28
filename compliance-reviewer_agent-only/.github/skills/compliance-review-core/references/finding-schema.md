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

## Worker Output Envelope

The worker subagent returns exactly one JSON object (no prose) with this shape; the orchestrator writes it to the transition file:

```json
{
  "schemaVersion": 1,
  "skill": "review-<name>",
  "subject": "string",
  "batchIndex": 0,
  "findings": [ /* Finding[] */ ],
  "strengths": [ /* Strength[] */ ],
  "checkResults": [ /* CheckResult[] */ ],
  "urlsFetched": ["https://..."],
  "notes": "optional short string, e.g. why a subject is N/A"
}
```
