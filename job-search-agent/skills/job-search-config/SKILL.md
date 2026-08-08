---
name: job-search-config
description: "Use when the job-search agent needs to load and parse settings/urls.txt, settings/attributes.txt, settings/targets.txt, settings/programminglanguages.txt, or settings/tools.txt. Defines file formats, comment/ordering rules, and the match_pct threshold default."
---

# Job Search Config Skill

## Objective
Load and normalize the workspace configuration files that drive the job-search workflow, and hand back structured, ordered data for the other skills to consume.

## Required Inputs
- `settings/urls.txt`: one search URL per line, allow comments beginning with `#`.
- `settings/attributes.txt`: attribute names to extract (one per line).
- `settings/targets.txt`: matching rules (one rule per line, allow comments with `#`).
- `settings/programminglanguages.txt`: programming-language discovery terms and canonical values (one per line).
- `settings/tools.txt`: tool discovery terms and canonical values (one per line). If a line contains a colon, the left side is used for discovery and the right side is used for reporting.
- Optional threshold from user: `match_pct` in range 0-100, default `75`.

## Parsing Rules
- Ignore empty lines.
- Ignore comment lines that start with `#` after trimming whitespace.
- Preserve user ordering from each file.
- Read `settings/programminglanguages.txt` and `settings/tools.txt` the same way as other config files, storing values in memory for extraction and reporting.
- For `programminglanguages.txt` and `tools.txt`: if a line contains a colon, the part before the colon is the discovery term and the part after the colon is the reporting value. If no colon is present, the value is both the discovery term and the reporting value.

## Attribute Ordering Rules
- Preserve `attributes.txt` ordering for parsing and extraction requests.
- For report output, render known attributes in this canonical order when present:
  1. `Job Title`
  2. `Programming Language`
  3. `Tools`
  4. `Salary Range`
- Append any additional attributes after the canonical set, preserving their original `attributes.txt` order.

## Output Contract
Return these structured objects for downstream skills:
- `urls`: ordered list of search URLs.
- `attributes`: ordered list of attribute names to extract.
- `targets`: ordered list of raw target rule strings.
- `programming_languages`: ordered list of `{ discovery_term, reporting_value }` pairs.
- `tools`: ordered list of `{ discovery_term, reporting_value }` pairs.
- `match_pct`: resolved threshold (user override or default `75`).

## Failure Handling
- If a required file is missing, the current runtime raises an error and stops the run.
- If a file exists but contains no active lines after comment filtering, the resulting input list is empty.
