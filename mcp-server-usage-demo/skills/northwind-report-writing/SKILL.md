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

## Exercise <N>.<M> — <short title>

**Goal:** one-line restatement of the exercise
**Data used:** MCP tools called (e.g. `get_all_customers`, `get_all_orders`)
**Logic:** 1–3 sentences describing the filters, joins, and aggregation applied
**Result (<row count> rows):**

| Column | Column |
| --- | --- |
| value | value |

**Notes:** assumptions, interpretation choices, null handling, edge cases (omit if none)
```

- Title the section with the part and exercise number (e.g. `## Exercise 2.4 — ...`).
- For **write** exercises (add/rename shipper), replace the result table with:
  - `**Action taken:**` the tool called and the payload sent, and
  - `**Verification:**` the re-fetched after-state quoted from tool output.

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

## Failure reports

- A non-success API status code, API error message, MCP tool error, timeout, or
  malformed/unusable response stops the run immediately; do not write results for
  exercises that were not completed.
- Report the failure in chat or in a clearly marked failure section of a report
  already created. Include the timestamp, Pilot API deployment, MCP tool, logical
  endpoint/operation, safe request parameters, status code, status/description,
  complete error message or response body, request/correlation id and response
  headers when available, plus the exercise and step in progress.
- Include what completed, what was not attempted, files already written, and
  recorded credits/usage. Redact secrets and credentials, and never invent
  missing response details; write `Unavailable` when a diagnostic field is not
  exposed.

## Credit summary

- Write a separate cost summary after all requested parts finish:
  `docs/northwind-exercise-cost-summary-<yyyyMMdd>-<HHmmss>.md`.
- Include one row per exercise with its part/exercise number, credits used, and
  status, followed by an overall credits total.
- Use the actual tool or run usage data. If credits are unavailable, write
  `Unavailable`; never estimate or treat unavailable values as zero.
