---
name: unit-test-coverage-reporting
description: 'Compiles logical path coverage metrics, presents an executive problem summary in chat, and writes the persistent coverage audit report. Use as the final stage of a unit test coverage review, or when asked to compute coverage gaps, problem percentages, severity breakdowns, or generate a coverage-review report. Computes total logical paths, total problems (uncovered + partially covered + mock bypass risks), problem percentage, and severity breakdown (Critical/High/Medium/Low); emits a formatted chat summary table and generates docs/coverage-review-YYYYMMDD-HHmmss.md with Given/When/Then remediation test skeletons. Never alters any source or test file.'
---

# Unit Test Coverage — Reporting

Final stage of the Unit Test Coverage Reviewer pipeline. Consumes the audit classifications from `unit-test-coverage-test-assertion-audit` and produces the chat summary plus the persistent timestamped report.

## Inputs

- Target Mapping table, logical path catalog, and per-path classifications from the prior stages — from in-context state, or loaded from `transitions/01-test-mapping-<runId>.md`, `02-control-flow-<runId>.md`, and `03-assertion-audit-<runId>.md` when resuming an interrupted run at this stage.
- `targetRoot` actually analyzed (workspace subfolder or external directory).
- `runId`: the run's shared `YYYYMMDD-HHmmss` timestamp, supplied by the orchestrating agent.

## Metrics

Compute:

- **Total Logical Paths Analyzed**: $N_{\text{total}}$
- **Total Problems Identified**: $N_{\text{problems}} = \text{Uncovered} + \text{Partially Covered} + \text{Mock Bypass Risks}$
- **Problem Percentage**: $\dfrac{N_{\text{problems}}}{N_{\text{total}}} \times 100\%$ (report `0%` when $N_{\text{total}} = 0$ and note that nothing was analyzed)
- **Severity Breakdown**:
  - **Critical** — unhandled error/panic paths (exceptions, Result/Option unwraps, non-zero return checks with no test)
  - **High** — untested core decision branches (if/else arms, switch cases)
  - **Medium** — untested boundary/edge cases (empty collections, boundary integers, null checks)
  - **Low** — superficial assertions on otherwise-executed paths

## Chat Summary

Present an executive summary table in chat:

| Metric | Value |
|--------|-------|
| Target root | `<targetRoot>` |
| Source units analyzed | n |
| Test suites mapped | n |
| Total logical paths ($N_{\text{total}}$) | n |
| Total problems ($N_{\text{problems}}$) | n |
| Problem percentage | n% |
| Critical / High / Medium / Low | n / n / n / n |

Follow with the top findings (highest severity first) using markdown file links.

## Persistent Report

Write the full report to `docs/coverage-review-<runId>.md` in the **current workspace** (never inside an external target directory), using the run's shared `YYYYMMDD-HHmmss` Run ID as the timestamp — this keeps the report correlated with its `transitions/` artifacts from the same run.

### Report Structure

1. **Header** — title, timestamp, target root, tool chain (the four skills).
2. **Executive Summary** — the metrics table above.
3. **Target Mapping** — Source Unit ↔ Test Unit(s) table, including unmapped units and orphan suites.
4. **Coverage Matrix** — per source unit: every path ID with its condition, classification (Covered / Partially Covered / Uncovered), mapped test case(s), assertion strength, and markdown links to source and test locations.
5. **Problem Register** — all problems grouped by severity with file/line links.
6. **Remediation Suggestions** — for each Uncovered or Partially Covered path, a **Given/When/Then** test skeleton as a markdown code snippet, e.g.:

    ```gherkin
    Given an empty order list
    When GetTotals is called
    Then it returns zero totals without throwing
    ```

    Skeletons are suggestions for developer review — they are NEVER applied to any file by this pipeline.
7. **Excluded Suites** — integration/E2E suites set aside during mapping, with the reason for exclusion.

## Guardrails

- The report file is the ONLY file this stage may write, and only into the workspace `docs/` folder.
- If report persistence is unavailable in the current context (e.g., a read-only agent invoked this skill), emit the complete report markdown in chat so the invoking agent or user can save it — state this explicitly.
