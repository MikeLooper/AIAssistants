---
name: northwind-report-writing
description: Conventions for Northwind exercise report files — output location, timestamped file naming (part + date/time), per-exercise section structure, and Markdown formatting rules. Use whenever producing Northwind exercise reports under docs/.
---

# Northwind Report Writing

Rules for the Markdown reports produced by the Northwind reporting exercises.

## File naming and location

- One Markdown file **per exercise part per run**, written to the `docs/` directory.
- File name: `northwind-part-<N>-report-<yyyyMMdd>-<HHmmss>.md`
  - `<N>` is the part number (1–4).
  - The timestamp is the **local** date/time when work on that part started.
  - Example: `docs/northwind-part-2-report-20260906-143210.md`
- Get the timestamp from the system clock — in this workspace, run
  `Get-Date -Format "yyyyMMdd-HHmmss"` in the terminal. Do not guess or invent it.
  Capture it once per part and use the same value in the file name and the header.
- Never overwrite an earlier report; the timestamp makes every run's output unique.

## File structure

```markdown
# Northwind Exercises — Part <N> Report

- **Generated:** <yyyy-MM-dd HH:mm:ss> local
- **Pilot API:** <deployment description> (<host:port>)
- **Data snapshot:** categories <n> · customers <n> · employees <n> · orders <n> · order details <n> · products <n> · shippers <n> · suppliers <n>
- **Data validation:** <pp.pp>% (<matched> of <checks> checks matched baseline · <x> of <y> exercises exact)

## Exercise <N>.<M> — <short title>

**Goal:** one-line restatement of the exercise
**Data used:** MCP tools called (e.g. `get_all_customers`, `get_all_orders`)
**Logic:** 1–3 sentences describing the filters, joins, and aggregation applied
**Result (<row count> rows):**

| Column | Column |
| --- | --- |
| value | value |

**Notes:** assumptions, interpretation choices, null handling, edge cases (omit if none)

## Data validation — Part <N>

**Validation score:** <pp.pp>% (<matched> of <checks> checks matched the baseline)

**Snapshot check:**

| Table | Baseline | Current | Result |
| --- | --- | --- | --- |
| categories | <n> | <n> | Match |

**Exercise check:**

| Exercise | Baseline rows | Current rows | Matched | Score | Status |
| --- | --- | --- | --- | --- | --- |
| <N>.<M> | <n> | <n> | <n> | <pp.pp>% | Match |

**Differences:** bullet per difference (missing, unexpected, or changed row), or `None`
```

- Title the section with the part and exercise number (e.g. `## Exercise 2.4 — ...`).
- For **write** exercises (add/rename shipper), replace the result table with:
  - `**Action taken:**` the tool called and the payload sent, and
  - `**Verification:**` the re-fetched after-state quoted from tool output.

## Data validation section

- Every part report ends with a `## Data validation — Part <N>` section, after the
  last exercise, and repeats the score in the `Data validation` header line.
- The results come from the [northwind-validation](../northwind-validation/SKILL.md)
  skill, which is run **before** the report is written. The percentage is that
  skill's part score; do not compute it any other way.
- The score is a percentage with 2 decimal places (for example `98.75%`).
- The `Status` column is `Match` (100%), `Partial` (above 0% and below 100%), or
  `Mismatch` (0%). The snapshot `Result` column is `Match` or `Mismatch`.
- List up to 5 differences per exercise under **Differences**, then state how many
  more exist. Write `None` when every exercise matches.
- If the baseline could not be read, write `Unavailable` for the score and explain
  why under **Differences**. Never estimate a score.
- A score below 100% is informational only; it does not change or replace the
  results reported for the exercises.

## Formatting rules

- Results are GitHub-flavored Markdown tables, one row per record.
- Always state the row count in `**Result (N rows):**` — even for single-value
  results, which render as a one-row, one-column table.
- Render nulls as `(null)`, booleans as `Yes`/`No`.
- Money, revenue, and averages: 2 decimal places. Dates: `yyyy-MM-dd`.
- Use the exact column labels an exercise prescribes (e.g. `DisplayName`).
- Sort order: follow the exercise; otherwise state the chosen sort under **Logic**.
- If a result set is empty, say so explicitly and note whether that is plausible.
- Never fabricate rows or values: every reported value must trace back to tool
  output from the current run.

## Run summary report

Every completed run also produces **one** summary report, written **after** all
requested part reports exist. It is a required deliverable, not optional.

- File name: `docs/northwind-exercise-summary-<yyyyMMdd>-<HHmmss>.md`, using a
  timestamp captured with `Get-Date -Format "yyyyMMdd-HHmmss"` when the summary is
  written. Never overwrite an earlier summary.
- Cover only the parts in scope for the run.
- Structure:

```markdown
# Northwind Exercises

- **Generated:** <yyyy-MM-dd HH:mm:ss> local
- **Requested parts:** <e.g. 1, 2, 3, 4>
- **Pilot API:** <deployment description> (<host:port>)

## Part reports

| Part | Report file | Data validation |
| --- | --- | --- |
| 1 | [<file name>](<file name>) | <pp.pp>% |

## Validations per exercise

| Part/Exercise | Status | Validation |
| --- | --- | --- | --- |
| 1.1 | <number or Unavailable> | Completed | <pp.pp>% |
```

- One row per exercise in scope, in numerical order. `Status` is `Completed`, plus a
  short parenthetical for the write exercises (for example `Completed (shipper
  added as shipperId 11038, verified)` or `Skipped (shipper already existed)`).  `Validation` is the percent correct from the data validation on the exercise.
- Link the part reports with paths relative to the summary file (same `docs/`
  folder, so just the file name).

## Failure reports

- A non-success API status code, API error message, MCP tool error, timeout, or
  malformed/unusable response stops the run immediately; do not write results for
  exercises that were not completed.
- Report the failure in chat or in a clearly marked failure section of a report
  already created. Include the timestamp, Pilot API deployment, MCP tool, logical
  endpoint/operation, safe request parameters, status code, status/description,
  complete error message or response body, request/correlation id and response
  headers when available, plus the exercise and step in progress.
- Include what completed, what was not attempted, and files already written.
  Redact secrets and credentials, and never invent
  missing response details; write `Unavailable` when a diagnostic field is not
  exposed.
