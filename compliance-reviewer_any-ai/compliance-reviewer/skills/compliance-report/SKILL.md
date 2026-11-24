---
name: compliance-report
description: 'Runs the deterministic steps of a compliance review with one Python script: run init (step 00), the scripted inventory (step 01), N/A subject files, worker dispatch payloads, state updates and resume, validation of the workers'' transition files, aggregation into merged findings and scores (step 90) and rendering of the final scored Markdown report (step 99); also builds and checks the review packs. Use when the compliance-reviewer orchestrator runs any of those steps.'
user-invocable: false
---

# Compliance Report

One deterministic script, `scripts/compliance_report.py` (standard library only), runs every mechanical step of a review, so those steps cost no model tokens beyond one shell call each. **Validate** checks the workers' transition files; **Aggregate** (step 90) merges them into scores and a deduplicated finding set; **Render** (step 99) fills the report template and writes it to `docs/reports/`. The [run steps](#run-steps) create the run, build the inventory, write N/A subjects, print worker payloads and keep `state.json` current. Use the manual fallback only when Python is unavailable.

```
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py init      <target> [--subjects all|a,b] [--advanced on|off] [--analyzers auto|none|a,b] [--out-file <path>]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py inventory transitions/<runId> [--picks <picks.json>]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py na        transitions/<runId>
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py dispatch  transitions/<runId> [--only <skill>]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py step      transitions/<runId> <stepId> <status> [--approval a,b]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py resume    transitions/<runId> [--from <NN>]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py validate  transitions/<runId> [--mark]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py aggregate transitions/<runId>
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py render    transitions/<runId> --out docs/reports/<target-name>-compliance-review-<YYYY-MM-DD_HHmm>.md [--copy-to <out-file>]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py labels    [skill ...]
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py packs     build|check [skill ...]
```

## Run steps

| Command | Does |
|---|---|
| `init` | Step 00. Checks the target folder and `--out-file` (never inside the target), resolves `--subjects`/`--advanced`/`--analyzers`, runs `git -C <target> rev-parse HEAD`, computes `runId` (`<YYYY-MM-DD_HHmm>-<target-name>`, suffixed `-2`, `-3` … if taken) and `inputsHash`, and writes `00-init.json` and `state.json` with every chosen step listed. Prints `{ok, runId, runDir, targetGitHead, inputsHash, …}`. |
| `inventory` | Step 01, per `compliance-inventory`. Writes `01-inventory.json` (including the value-free `secretCandidates`, `piiCandidates` and `personalDataFound`), marks step 01 completed and step 02 skipped when advanced usage is off. Prints a summary with the batches, skipped subjects and, for each capped subject, its default `sample` and `candidates`. `--picks` replaces those subjects' lists and re-batches. |
| `na` | Writes the minimal N/A file (`checks: {"na": {"N/A": <reason>}}`) for every chosen subject in `skippedSubjects` and marks it completed. |
| `dispatch` | Prints one worker payload per `fileBatches` entry (JSON lines; see `WORKER.md`) and marks those subject steps started. `review-security-operational` gets `secretCandidates` (merged with a `02-analyzer-gitleaks.raw.json` report when present, one per file and line); `review-data-protection` gets `piiCandidates` and `personalDataSignals`. `--only <skill>` prints a single-subject payload for a retry. |
| `step` | Sets one step's status in `state.json`; `--approval` records the analyzers that ran (step 02). |
| `resume` | Recomputes `targetGitHead` and `inputsHash`, reports whether either changed and names the next pending step. `--from <NN>` first moves step `NN` and later (and every subject file sharing a `batchId` with a moved one) into `superseded/` and resets those steps. |

## Validate (after the subject steps)

`validate` prints JSON `{ok, missing, problems, warnings}` and exits non-zero if any subject file is missing, unparsable, not `status: completed`, or malformed. With `--mark` it also records each subject's step as `completed` or `failed` in `state.json`. The orchestrator re-runs only the affected subjects (single-subject worker call) and validates again. Warnings (for example more than 3 strengths) never block the run.

It also checks each file against its skill's `references/checklist.md`:

| Condition | Result |
|---|---|
| `subject`/`subSubject` differs from the checklist (schemaVersion 1 files) | warning (aggregate normalizes it; no retry) |
| `checkId` not in the checklist and not retired | problem (single-subject retry) |
| Retired `checkId` | warning (dropped from scoring) |
| An active check has no result (missing from `checks`, or from `checkResults` in schemaVersion 1) | problem |
| A check listed under more than one of `pass`/`fail`/`na`, or an unknown key in `checks` | problem |
| A finding's `element` isn't in the skill's standards | warning (cited as plain text) |
| Orchestrator N/A placeholder (`checkId: "N/A"`) | accepted |
| An evidence `excerpt` that contains a secret value or personal data (shared patterns in `compliance-inventory/references/secret-patterns.json`) | problem (single-subject retry; the worker writes `<redacted:kind>` instead) |
| Checklist missing or unreadable | warning for schemaVersion 1 (labels not checked or normalized); problem for schemaVersion 2 (severities unknown). Run `labels`. |

## Compact worker files (schemaVersion 2)

Workers write only what the script can't derive (`compliance-review-core`'s `finding-schema.md`). Before validating, aggregating or rendering, the script expands each file:

- `checks` (`pass` list, `fail` and `na` maps) becomes one check result per check, with `severityIfFailed` from the checklist's **Default severity** column (its first word; a parenthetical only qualifies Finding severity).
- `subject`/`subSubject` come from the checklist, as in [Labels](#labels).
- Each finding's `element` becomes `standard` and `url` through the skill's `references/standards/*.md` (`scripts/standards.py`): the source name from the header line "Source name for `Finding.standard`", the page-key table, the `Src` or per-row `Source name` column, or a PEP-style ID range; the URL from the citation base, page key or path, primary anchor, `PDF page` or rubric anchor. An optional `page` picks one of several per-version bases (OpenAPI). An explicit `standard`/`url` from the worker is kept as is. Pages without anchors get the section or item in `standard` (e.g. `… — CSA-05 (§3.6)`).

schemaVersion 1 files are still read as before, so older runs re-aggregate unchanged.

## Labels

Subject and sub-subject labels belong to the checklists, not the model: each `checklist.md` has one `Subject:` line after its H1 and a `Sub-subject` column in its checks table (retired checks are rows whose Check cell starts with `*(retired`). `aggregate` and `render` rewrite `subject`/`subSubject` on every finding, strength and check result from the checklist, by skill and `checkId`, before deduplicating and scoring. A strength without a `checkId` gets the skill's subject and, when the skill has a single sub-subject, that one (otherwise the worker's label is kept). `90-aggregate.json` records `labelsNormalized` (changed entries per skill) so label drift stays visible. Re-aggregating an older run brings it onto the current labels.

Lint the checklists after editing one:

```
python compliance-reviewer/skills/compliance-report/scripts/compliance_report.py labels [skill ...]
```

It prints `{ok, problems}` and exits non-zero on problems: not exactly one `Subject:` line, a checks table without `id`/`Sub-subject`/`Check`/`Default severity` columns, an active check whose default severity doesn't start with Error, Warning or Information, a check row outside the table, duplicate ids, or an active check whose sub-subject is empty or breaks the label style (Title Case except Twelve-Factor's factor titles, `&` not `and`, no ` / `, at most 36 characters). With no arguments it lints every skill in `transition-schema.md`'s step table.

The same command also flags, for the skills it lints:

- a standards element whose citation can't be resolved (no source name, no URL, or a URL with spaces), and an element ID defined twice in one skill;
- a review pack that is missing or out of date with its sources (see [Review packs](#review-packs));
- with no arguments, problems in `compliance-inventory/references/subject-file-map.json` (bad regex or glob, unknown pattern reference, a subject with no entry).

## Review packs

A worker reads one generated file per skill, `compliance-reviewer/packs/<skill>.md`, plus `compliance-reviewer/packs/<skill>.<language>.md` for each detected language that has language-specific content. It doesn't open the four to seven source files separately. A pack holds:

- `SKILL.md` without front matter, `references/checklist.md` and the skill's other reference files (signal tables);
- each standards file with its load rule, minus citation metadata. Left out are the header pin, citation and source-name bullets, the page-key tables, the `Anchor(s)`/`Page`/`Src`/`Source name`/`PDF page` columns and retired rows. Element rows, levels, applicability and every other legend or rule stay.

`sources.md` and `references/standards/MAINTENANCE.md` are maintainer material and are left out. The full files stay the source of truth: after editing a skill, its checklist or a standards file, run `packs build` (all skills, or name some) and commit the result. `packs check`, and `labels`, fail when a pack no longer matches what `build` would produce.

## Aggregate (step 90)

`aggregate` reads every `NN-review-*.json` (and legacy `.part-K.json`) file and writes `90-aggregate.json`:

0. **Labels.** Normalize `subject`/`subSubject` from the checklists and drop retired check results (see [Labels](#labels)).
1. **Exact duplicates.** Same `checkId` + `subject`/`subSubject` + `standard` citation with overlapping evidence collapse into one finding holding every location. Findings of one check that cite different standard elements (e.g. `… — AZ-054` vs `… — AZ-058`) are distinct violations and are kept.
2. **Cross-subject semantic duplicates.** Findings from *different subject skills* (different `NN-review-*` transition files) whose evidence is at the *same location* (same real file and line ranges with intersection-over-union of at least 0.5, or both whole-file) are one issue. The highest severity wins (ties go to the subject earlier in pipeline order); the other is suppressed from `findings` and recorded in `duplicatesSuppressed` and `suppressedChecks`. Its own subject's check stays `fail`, and the Full Results row reads `duplicate evidence of <primary id>, see <primary subject> / <primary subSubject>` (the subject alone when the two are equal). Findings without a real file location never match. Different checks within one skill never suppress each other, even when they cite the same lines.
3. **Scores** per `compliance-review-core`'s `severity-and-scoring.md`, from `checkResults` (a suppressed duplicate still counts as `fail` for its own subject), grouped by `subject`, plus the weighted overall score. Subjects with no applicable checks (N/A subjects) carry no score, add nothing to the overall score and appear in the report's score table as `N/A`.
4. **Severity counts** over the deduplicated findings, and the **top 5 risks** ordered by severity, then confidence (High first), then effort (Small first), then pipeline order.

`90-aggregate.json` holds scores, `severityCounts`, `topRisks`, `findings`, `strengths`, `duplicatesSuppressed` and `suppressedChecks`. Every string in it passes through the same secret and personal-data masking as the report (`<redacted:kind>`), so no value that slipped past a worker is stored. It does **not** embed `checkResults`; `render` reads them from the per-subject files.

## Render (step 99)

`render` fills [`assets/report-template.md`](./assets/report-template.md) (sections: Summary with subject score table, which lists N/A subjects with score `N/A`, severity counts and top 5 risks; Things Done Well; Recommended Improvements by severity; Full Results grouped by subject then sub-subject, with no sub-subject heading where it equals the subject; Appendix with run metadata, run flags from `state.json` `flags`, skipped subjects, fetched URLs and link approvals), writes the report to `--out` and, when `--copy-to` is given (the orchestrator's `--out-file`), renders the same report to that path too, with local links rebased for its folder. Each finding's citation is `[standard](url)`, or plain `standard` when `url` is empty; a scheme-less `url` (a local standard, written relative to `docs/reports/`) is rebased onto the `--out` folder so the link resolves wherever the report is written. The finished report is masked with the shared secret and personal-data patterns before it is written, so no value reaches `docs/reports/` or `--out-file`. It then writes `99-report.json`, and sets `state.json` to `status: completed` with `reportPath`. It prints the overall score/band and top risks for the final message.

## Manual fallback (no Python)

Apply the same rules by hand: read the subject files, expand compact `checks` into one result per check with the checklist's default severity, resolve each `element` to `standard`/`url` from its standards file header and row, replace every `subject`/`subSubject` with the labels from the skill's `checklist.md`, merge duplicates as above, compute scores and counts, write `90-aggregate.json` without `checkResults`, then fill the template reading Full Results from the subject files. Expect this to cost far more than the script.

## Output

- `90-aggregate.json`, `99-report.json` transition files.
- The final report at `docs/reports/...` (plus the `--copy-to` copy, if requested).