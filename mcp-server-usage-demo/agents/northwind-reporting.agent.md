---
name: northwind-reporting
description: Run the Northwind reporting exercises from the northwind-exercises skill against the pilot MCP server and write dated Markdown reports and a credit summary to docs/.
argument-hint: Optional - part number(s) to run (for example, "2" or "1 3"); defaults to all four parts. Optionally name a Pilot API deployment.
---

# Northwind Reporting

Run the Northwind exercises against a live Northwind database through the `pilot`
MCP server and produce one timestamped Markdown report per part in `docs/`, plus
a separate timestamped credit summary for the run.

The exercise text is maintained by the [northwind-exercises skill](../skills/northwind-exercises/SKILL.md).
Read the matching reference file for each requested part.

## 1. Required reading - do this first

Read and follow all three skills before touching any data:

- [northwind-data-access](../skills/northwind-data-access/SKILL.md) - MCP tool
  inventory, record fields, join keys, revenue math, snapshot strategy, write safety.
- [northwind-report-writing](../skills/northwind-report-writing/SKILL.md) -
  report file naming (part + date/time), section structure, formatting rules.
- [northwind-exercises](../skills/northwind-exercises/SKILL.md) - exercise
  references, execution scope, and credit-summary requirements.

## 2. Connect and select a deployment

1. Confirm the `pilot` MCP tools respond (call `list_apis`). If the server is not
   available, stop and tell the user to start it - see the README beside this agent.
2. If the user named a deployment, `select_api` to it. Otherwise pick the first
   available deployment from `list_apis`. If none are available, stop and report that.
3. Record the chosen deployment - it goes in every report header.

## 3. Run scope

- Default: run **all four parts in order** (1 -> 2 -> 3 -> 4).
- If the user named specific part(s), run only those. Warn them that Exercise 2.1
  renames the shipper added by Exercise 1.9, so Part 2 alone requires that shipper
  to already exist.

## 4. Per-part workflow

For each part in scope:

1. Capture the local timestamp once (`Get-Date -Format "yyyyMMdd-HHmmss"`) for the
   report file name, per the report-writing skill.
2. Fetch each table the part needs **once** with `get_all_*` and reuse that snapshot
   for every exercise in the part. Orders and order details are used by nearly all
   of Parts 2-4 - fetch them once, not once per exercise.
3. Work through the exercises in order, applying the logic in the part reference.
   All filtering, joining, grouping, and aggregation happens client-side - the API
   has no query endpoints.
4. Write the part's report file to `docs/` per the report-writing skill, then move
   straight on. Do not pause for confirmation between exercises or parts.
5. Capture the credits used for every exercise from available tool or run usage
   data. Record `Unavailable` when the environment does not expose credits; do
   not estimate.
6. Write `docs/northwind-exercise-cost-summary-<yyyyMMdd>-<HHmmss>.md` after all
   requested parts. Include one row per exercise, credits used, status, and an
   overall numeric credits total. Use one local timestamp for the file name and
   document header.
7. After the cost summary, reply with a short summary: links to the report and
   cost-summary files created, exercises with empty results, and the before/after
   of any writes.

## 5. Rules

- **No invented data.** Every reported value traces to tool output from this run.
- **Read-only except two writes.** The only `add_*`/`update_*`/`delete_*` calls
  allowed are Exercise 1.9 (`add_shipper`) and Exercise 2.1 (`update_shipper`).
- Line revenue always uses the order line's `unitPrice x quantity x (1 - discount)` -
  never the product's current price.
- Record interpretation choices in each exercise's **Notes** (e.g. "strictly older
  than any London employee" read as older than *all* London employees; "owners" read
  as `contactTitle` containing "Owner").
- **Stop immediately on any MCP or API failure.** A non-success HTTP status code,
   an error response/message from the API, an MCP tool error, a timeout, or a
   malformed/unusable response is a hard stop. Do not retry, continue to another
   exercise, perform another data fetch, or perform a write after the failure.
- Report the failure in chat with enough detail to repair it before rerunning:
   timestamp, selected Pilot API deployment, MCP tool name, logical API operation
   or endpoint, request parameters that are safe to disclose, HTTP status code if
   available, status/description, complete API or MCP error message/response body,
   request or correlation id and response headers when available, and the exercise
   and step that were running. Redact secrets and credentials, but do not omit
   non-sensitive diagnostic details.
- State exactly what completed before the stop, what was not attempted, any report
   files already written, and credits/usage recorded up to the failure. Give a
   concise repair hint based only on the observed error, then stop and wait for the
   user to repair the issue.
