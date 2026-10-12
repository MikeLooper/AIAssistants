---
name: compliance-report
description: 'Validates subject transition files, then aggregates them into merged findings and scores and renders the final scored Markdown compliance report, using a deterministic Python script. Use when the compliance-reviewer orchestrator validates subject output or runs step 90 (aggregate) and step 99 (report) of a compliance review.'
user-invocable: false
---

# Compliance Report

Three procedures: **Validate** checks the workers' transition files; **Aggregate** (step 90) merges them into scores and a deduplicated finding set; **Render** (step 99) fills the report template and writes it to `docs/reports/`. All three are done by a deterministic script — they need no model tokens beyond the one `execute` call each. Use the manual fallback only when Python is unavailable.

```
python .github/skills/compliance-report/scripts/compliance_report.py validate  transitions/<runId>
python .github/skills/compliance-report/scripts/compliance_report.py aggregate transitions/<runId>
python .github/skills/compliance-report/scripts/compliance_report.py render    transitions/<runId> --out docs/reports/<target-name>-compliance-review-<YYYY-MM-DD_HHmm>.md
```

## Validate (after the subject steps)

`validate` prints JSON `{ok, missing, problems, warnings}` and exits non-zero if any subject file is missing, unparsable, not `status: completed`, or malformed. The orchestrator re-runs only the affected subjects (single-subject worker call) and validates again. Warnings (for example more than 3 strengths) never block the run.

## Aggregate (step 90)

`aggregate` reads every `NN-review-*.json` (and legacy `.part-K.json`) file and writes `90-aggregate.json`:

1. **Exact duplicates.** Same `checkId` + `subject`/`subSubject` with overlapping evidence collapse into one finding holding every location.
2. **Cross-subject semantic duplicates.** Findings with a different `checkId`/`subject` whose evidence is at the *same location* (same real file and line ranges with intersection-over-union of at least 0.5, or both whole-file) are one issue. The highest severity wins (ties go to the subject earlier in pipeline order); the other is suppressed from `findings` and recorded in `duplicatesSuppressed` and `suppressedChecks`. Its own subject's check stays `fail`, and the Full Results row reads `duplicate evidence of <primary id>, see <primary subject>/<primary subSubject>`. Findings without a real file location never match.
3. **Scores** per `compliance-review-core`'s `severity-and-scoring.md`, from `checkResults` (a suppressed duplicate still counts as `fail` for its own subject), grouped by `subject`, plus the weighted overall score. Subjects with no applicable checks are left out of the score table.
4. **Severity counts** over the deduplicated findings, and the **top 5 risks** ordered by severity, then confidence (High first), then effort (Small first), then pipeline order.

`90-aggregate.json` holds scores, `severityCounts`, `topRisks`, `findings`, `strengths`, `duplicatesSuppressed` and `suppressedChecks`. It does **not** embed `checkResults`; `render` reads them from the per-subject files.

## Render (step 99)

`render` fills [`assets/report-template.md`](./assets/report-template.md) (sections: Summary with subject score table, severity counts and top 5 risks; Things Done Well; Recommended Improvements by severity; Full Results grouped by subject then sub-subject; Appendix with run metadata, skipped subjects, fetched URLs and link approvals), writes the report to `--out`, writes `99-report.json`, and sets `state.json` to `status: completed` with `reportPath`. It prints the overall score/band and top risks for the final message.

## Manual fallback (no Python)

Apply the same rules by hand: read the subject files, merge duplicates as above, compute scores and counts, write `90-aggregate.json` without `checkResults`, then fill the template reading Full Results from the subject files. Expect this to cost far more than the script.

## Output

- `90-aggregate.json`, `99-report.json` transition files.
- The final report at `docs/reports/...`.