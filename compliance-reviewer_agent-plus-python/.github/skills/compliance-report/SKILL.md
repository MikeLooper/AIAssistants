---
name: compliance-report
description: 'Aggregates transition files into merged findings and scores, then renders the final scored Markdown compliance report. Use when the compliance-reviewer orchestrator runs step 90 (aggregate) and step 99 (report) of a compliance review.'
user-invocable: false
---

# Compliance Report

Two procedures: **Aggregate** (step 90) merges every subject's transition file into scores and a deduplicated finding set; **Render** (step 99) fills the report template and writes it to `docs/reports/`.

## Aggregate Procedure

1. Read every `NN-review-*.json` (and `.part-K.json`) transition file for the run.
2. Merge exact-duplicate findings: two findings are duplicates if they share the same `checkId` and `subject`/`subSubject` and point at overlapping evidence (same file, overlapping line range). Collapse duplicates into one finding whose `evidence` array holds every location.
3. Merge cross-subject semantic duplicates: after step 2, some checklists intentionally overlap in scope across different skills (e.g. a cloud-resilience check in Software Quality's Architecture Patterns sub-subject vs. a retry/circuit-breaker check in Reliability). If two *different* findings (different `checkId` and/or `subject`) point at overlapping evidence (same file, overlapping line range), treat them as the same underlying issue:
   - Keep the higher-severity finding (Error > Warning > Information; if tied, keep the one from the subject that runs earlier in the pipeline order) as the **primary** finding in the deduplicated `findings` array.
   - Do not add the other finding to `findings` — this keeps severity counts and the top-5-risks list from double-counting one code issue.
   - In that finding's own subject's `checkResults`, still record the check as `fail`, but set `findingIds` to reference the primary finding's `id` (not a new id) and note in `reason`: `"duplicate evidence of <primary finding id>, see <primary subject>/<primary subSubject>"`. This keeps Full Results accurate per subject without inflating the finding count.
4. Compute each subject's score and band using the formula and bands in `compliance-review-core`'s `severity-and-scoring.md`. Scoring is based on `checkResults` (pass/fail/N/A), so a check suppressed as a semantic duplicate in step 3 still counts as `fail` for its own subject's score — only the top-level `findings` list (and counts derived from it) is deduplicated.
5. Compute the overall score as the weighted average of subject scores (weight = each subject's total applicable weight), then its band.
6. Count findings by severity, overall and per subject, using the deduplicated `findings` list from steps 2–3.
7. Select the top 5 risks: the highest-severity, highest-confidence findings, preferring Errors, then Warnings, ordered by effort ascending (quick wins first) as a tiebreaker.
8. Write `90-aggregate.json` with: `schemaVersion`, `runId`, subject scores/bands, overall score/band, severity counts, deduplicated `findings`, `strengths`, and the top-5-risks list (by finding id).

## Render Procedure

1. Read `90-aggregate.json` and `state.json`.
2. Fill [`assets/report-template.md`](./assets/report-template.md) with:
   - **Summary**: overall score/band, subject score table, severity counts, top 5 risks.
   - **Things Done Well**: from `strengths`, grouped by subject.
   - **Recommended Improvements**: from `findings`, grouped Errors then Warnings then Information; each item links to its `url`.
   - **Full Results**: every `checkResults` entry per subject with pass/fail/N/A and evidence.
   - **Appendix**: run metadata (`runId`, `targetPath`, `targetGitHead`, start/end times), skipped subjects and why, every URL fetched across all steps, and link approval decisions from `state.json`.
3. Write the filled report to `docs/reports/<target-name>-compliance-review-<YYYY-MM-DD_HHmm>.md`, using the same date/time as `runId` for consistency.
4. Write `99-report.json` with the report path and `status: completed`, then update `state.json`'s `reportPath` and `status`.

## Output

- `90-aggregate.json`, `99-report.json` transition files.
- The final report at `docs/reports/...`.
