---
name: northwind-validation
description: Validate Northwind exercise results retrieved from the pilot MCP server against a static baseline copied from a known-good run, and produce a per-part validation percentage. Use after computing each part's exercise results and before writing the part's report under docs/.
---

# Northwind Validation

Compares the data retrieved and computed in the current run against a static
baseline, and produces a **validation percentage per part** for the report writer.

## Baseline

Static, minimized copies of the data from the reference run (2026-10-24, .NET Core
with SQL Server) live in [baseline/](baseline/). Each file holds only what
validation needs: a `Snapshot:` line with the table row counts, then one
`## <N>.<M>` section per exercise containing its result table (or, for the two
write exercises, the `Action taken` and `Verification` lines).

| Part | Baseline file |
| --- | --- |
| 1 | [part-1.md](baseline/part-1.md) |
| 2 | [part-2.md](baseline/part-2.md) |
| 3 | [part-3.md](baseline/part-3.md) |
| 4 | [part-4.md](baseline/part-4.md) |

- The baseline files are **read-only reference data**. Never edit them, never write
  to them during a run, and never copy current-run values into them.
- Refresh the baseline only when the user explicitly asks, by reducing a vetted
  report from `docs/` to the same minimal format.
- The baseline reflects the database state of the reference run: shippers 3 before
  Exercise 1.9 and 4 afterwards, and the extra "Test Cat" categories.

## When to run

After all exercises of a part are computed in memory and **before** the part's
report file is written, so the result can be embedded in that report. Validate only
the parts in scope for the run.

## Procedure

1. Read `baseline/part-<N>.md` for the part being validated.
2. **Snapshot check.** Compare each table row count in the current `Data snapshot`
   header line with the baseline's `Snapshot:` line (categories, customers, employees, orders,
   order details, products, shippers, suppliers). Ignore parenthetical remarks in the current line
   such as "(before Exercise 1.9)". Record each as match or mismatch. This is
   informational and explains downstream differences; it is not part of the
   percentage.
3. **Exercise check.** For every exercise in the part, compare the current result
   with the baseline section of the same exercise number:
   - Parse each result table into rows keyed by their full set of cell values,
     using the same column order and labels.
   - Normalize before comparing: trim whitespace; compare numbers numerically at the
     report's precision (2 decimals for money/averages); compare dates as
     `yyyy-MM-dd`; treat `(null)` as equal only to `(null)`.
   - Compare rows as an **unordered multiset**, because sort order is not data.
     Count duplicate rows individually (for example, the three identical
     "Test Cat" rows).
   - `matched` = rows present in both. `baseline rows` and `current rows` are the
     row counts on each side.
   - Exercise checks = `max(baseline rows, current rows)`. This penalizes both
     missing and unexpected rows.
   - Exercise score = `matched / checks`. When both sides have 0 rows, the score is
     100%.
   - A section missing from the current run counts as `matched = 0` against the
     baseline's rows. A section that exists only in the current run counts as a
     failure with `checks = current rows`.
4. **Write exercises** (1.9 add shipper, 2.1 rename shipper) are scored as one
   check each, compared on the business payload and verification after-state:
   - Compare `companyName` (sent payload and re-fetched state) and the full
     `get_all_shippers` after-state, **ignoring the generated `shipperId`** of the
     new shipper, which the database assigns and varies between runs.
   - Pass (1/1) only if the payload and after-state agree; otherwise 0/1.
   - If 1.9 was skipped because `Amazon` already existed, score it 0/1 and say so in
     the exercise note rather than guessing.
5. **Part score** = `sum(matched) / sum(checks)` across all exercises of the part,
   as a percentage rounded to 2 decimals. Also count exercises with an exact match
   (score 100%).
6. Describe each difference briefly (missing row, unexpected row, value changed) so
   it can be listed in the report. Limit to the first 5 differences per exercise and
   state how many more exist.

## Interpreting results

- 100% means the current data and results agree with the baseline.
- Below 100% is **not** a failure of the run: the Northwind databases are shared,
  mutable state and a deployment may legitimately differ. Report the number and
  differences; do not alter results to match the baseline and never stop the run
  because of a mismatch.
- If a mismatch is plausibly explained by a snapshot count difference, say so.
- Never invent or "correct" current values using baseline data. The report must
  contain only values from the current run; the baseline is used for comparison
  only.
- A baseline file that cannot be read is a validation failure to report, not a
  reason to guess. Report the part's percentage as `Unavailable` and continue.

## Output handed to the report writer

For each part provide:

- Part score (percentage, 2 decimals), total matched checks, total checks, and the
  number of exact-match exercises out of the exercises validated.
- The snapshot-check table.
- One row per exercise: baseline rows, current rows, matched, score, and status
  (`Match`, `Partial`, or `Mismatch`), plus any difference notes.

The [northwind-report-writing](../northwind-report-writing/SKILL.md) skill defines
how this is rendered in the report.
