---
name: compliance-report
description: 'Validates subject transition files, then aggregates them into merged findings and scores and renders the final scored Markdown compliance report, using a deterministic Python script. Use when the compliance-reviewer orchestrator validates subject output or runs step 90 (aggregate) and step 99 (report) of a compliance review.'
user-invocable: false
---

# Compliance Report

Three procedures: **Validate** checks the workers' transition files; **Aggregate** (step 90) merges them into scores and a deduplicated finding set; **Render** (step 99) fills the report template and writes it to `docs/reports/`. All three are done by a deterministic script — they need no model tokens beyond the one shell call each. Use the manual fallback only when Python is unavailable.

```
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py validate  transitions/<runId>
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py aggregate transitions/<runId>
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py render    transitions/<runId> --out docs/reports/<target-name>-compliance-review-<YYYY-MM-DD_HHmm>.md [--copy-to <out-file>]
```

## Validate (after the subject steps)

`validate` prints JSON `{ok, missing, problems, warnings}` and exits non-zero if any subject file is missing, unparsable, not `status: completed`, or malformed. The orchestrator re-runs only the affected subjects (single-subject worker call) and validates again. Warnings (for example more than 3 strengths) never block the run.

It also checks each file against its skill's `references/checklist.md`:

| Condition | Result |
|---|---|
| `subject`/`subSubject` differs from the checklist | warning (aggregate normalizes it; no retry) |
| `checkId` not in the checklist and not retired | problem (single-subject retry) |
| Retired `checkId` | warning (dropped from scoring) |
| An active check has no `checkResults` entry | problem |
| Orchestrator N/A placeholder (`checkId: "N/A"`) | accepted |
| Checklist missing or unreadable | warning (labels not checked or normalized; run `labels`) |

## Labels

Subject and sub-subject labels belong to the checklists, not the model: each `checklist.md` has one `Subject:` line after its H1 and a `Sub-subject` column in its checks table (retired checks are rows whose Check cell starts with `*(retired`). `aggregate` and `render` rewrite `subject`/`subSubject` on every finding, strength and check result from the checklist, by skill and `checkId`, before deduplicating and scoring. A strength without a `checkId` gets the skill's subject and, when the skill has a single sub-subject, that one (otherwise the worker's label is kept). `90-aggregate.json` records `labelsNormalized` (changed entries per skill) so label drift stays visible. Re-aggregating an older run brings it onto the current labels.

Lint the checklists after editing one:

```
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py labels [skill ...]
```

It prints `{ok, problems}` and exits non-zero on problems: not exactly one `Subject:` line, a checks table without `id`/`Sub-subject`/`Check` columns, a check row outside the table, duplicate ids, or an active check whose sub-subject is empty or breaks the label style (Title Case except Twelve-Factor's factor titles, `&` not `and`, no ` / `, at most 36 characters). With no arguments it lints every skill in `transition-schema.md`'s step table.

## Aggregate (step 90)

`aggregate` reads every `NN-review-*.json` (and legacy `.part-K.json`) file and writes `90-aggregate.json`:

0. **Labels.** Normalize `subject`/`subSubject` from the checklists and drop retired check results (see [Labels](#labels)).
1. **Exact duplicates.** Same `checkId` + `subject`/`subSubject` + `standard` citation with overlapping evidence collapse into one finding holding every location. Findings of one check that cite different standard elements (e.g. `… — AZ-054` vs `… — AZ-058`) are distinct violations and are kept.
2. **Cross-subject semantic duplicates.** Findings from *different subject skills* (different `NN-review-*` transition files) whose evidence is at the *same location* (same real file and line ranges with intersection-over-union of at least 0.5, or both whole-file) are one issue. The highest severity wins (ties go to the subject earlier in pipeline order); the other is suppressed from `findings` and recorded in `duplicatesSuppressed` and `suppressedChecks`. Its own subject's check stays `fail`, and the Full Results row reads `duplicate evidence of <primary id>, see <primary subject> / <primary subSubject>` (the subject alone when the two are equal). Findings without a real file location never match. Different checks within one skill never suppress each other, even when they cite the same lines.
3. **Scores** per `compliance-review-core`'s `severity-and-scoring.md`, from `checkResults` (a suppressed duplicate still counts as `fail` for its own subject), grouped by `subject`, plus the weighted overall score. Subjects with no applicable checks are left out of the score table.
4. **Severity counts** over the deduplicated findings, and the **top 5 risks** ordered by severity, then confidence (High first), then effort (Small first), then pipeline order.

`90-aggregate.json` holds scores, `severityCounts`, `topRisks`, `findings`, `strengths`, `duplicatesSuppressed` and `suppressedChecks`. It does **not** embed `checkResults`; `render` reads them from the per-subject files.

## Render (step 99)

`render` fills [`assets/report-template.md`](./assets/report-template.md) (sections: Summary with subject score table, severity counts and top 5 risks; Things Done Well; Recommended Improvements by severity; Full Results grouped by subject then sub-subject, with no sub-subject heading where it equals the subject; Appendix with run metadata, run flags from `state.json` `flags`, skipped subjects, fetched URLs and link approvals), writes the report to `--out` and, when `--copy-to` is given (the orchestrator's `--out-file`), renders the same report to that path too, with local links rebased for its folder. Each finding's citation is `[standard](url)`, or plain `standard` when `url` is empty; a scheme-less `url` (a local standard, written relative to `docs/reports/`) is rebased onto the `--out` folder so the link resolves wherever the report is written. It then writes `99-report.json`, and sets `state.json` to `status: completed` with `reportPath`. It prints the overall score/band and top risks for the final message.

## Manual fallback (no Python)

Apply the same rules by hand: read the subject files, replace every `subject`/`subSubject` with the labels from the skill's `checklist.md`, merge duplicates as above, compute scores and counts, write `90-aggregate.json` without `checkResults`, then fill the template reading Full Results from the subject files. Expect this to cost far more than the script.

## Output

- `90-aggregate.json`, `99-report.json` transition files.
- The final report at `docs/reports/...` (plus the `--copy-to` copy, if requested).