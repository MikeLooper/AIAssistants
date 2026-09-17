---
name: unit-test-coverage-test-mapping
description: 'Discovers source files and pairs them with associated unit test suites in the workspace or an external target directory. Use when starting a unit test coverage review, mapping tests to source, or finding untested source files. Builds the Source Unit ↔ Test Unit(s) Target Mapping table using multi-language naming conventions (*.Tests.cs, *Test.java, *.test.ts, *.spec.ts, test_*.py, *_test.go), and separates unit tests from integration/E2E suites. Strictly read-only: never modifies target files.'
---

# Unit Test Coverage — Test Mapping

First stage of the Unit Test Coverage Reviewer pipeline. Produces the **Target Mapping table** consumed by the control-flow-extraction and test-assertion-audit stages.

## Inputs

- `targetRoot`: workspace-relative path or absolute external directory path (e.g., `C:/Working/OtherProject` or `/path/to/repo`).
- `runId`: the run's shared `YYYYMMDD-HHmmss` timestamp, supplied by the orchestrating agent; used to name the persisted artifact.
- Optional user-supplied include/exclude patterns.

## Guardrails

- **READ-ONLY**: never write to, rename, move, or delete files in the target root — including external directories.
- Accept absolute external paths verbatim; do not attempt to normalize them into the workspace.

## Procedure

1. **Enumerate source files** under `targetRoot`, skipping build/dependency artifacts: `bin/`, `obj/`, `node_modules/`, `dist/`, `build/`, `out/`, `target/`, `vendor/`, `.git/`, and generated-code folders.
2. **Enumerate candidate test files** using multi-language conventions:
   - **.NET**: `*.Tests.cs`, `*.Test.cs`, `*Tests.fs`, `*Tests.vb`
   - **Java/JVM**: `*Test.java`, `*Tests.java`, `*Test.kt`, `*Spec.groovy`, `*Test.scala`
   - **TypeScript/JavaScript**: `*.test.ts`, `*.test.tsx`, `*.spec.ts`, `*.spec.js`, `*.test.js`, `__tests__/**`
   - **Python**: `test_*.py`, `*_test.py`, `tests/**`
   - **Go**: `*_test.go`
   - **Rust**: `#[cfg(test)]` inline modules, `tests/**`
3. **Classify each test suite as unit vs integration/E2E.** Set aside (exclude from mapping, but count) files showing integration/E2E signals:
   - Naming: `*IntegrationTest*`, `*IT.java`, `*.e2e.*`, `*.ui.*`, `*.system.*`
   - Tooling: Playwright/Cypress specs, Testcontainers fixtures, Selenium, supertest against live servers
   - Dependencies: live HTTP clients, real database connections, message brokers, file-system fixtures
4. **Pair each source unit with its test unit(s)** using, in priority order:
   1. File-name stem match (`OrderService.cs` ↔ `OrderServiceTests.cs`, `order_service.py` ↔ `test_order_service.py`).
   2. Namespace/package correspondence plus import/using/from statements in the test file.
   3. Direct symbol references (class/function names) exercised inside test bodies.
   Record one-to-many mappings when multiple suites target one source unit.
5. **Flag gaps**:
   - *Unmapped source units* — no test suite found (these become automatic coverage gaps downstream).
   - *Orphan test suites* — no matching source unit (note them; they may be stale or utility tests).

## Output

Produce a Target Mapping table:

| # | Source Unit | Test Unit(s) | Mapping Basis | Notes |
|---|-------------|--------------|---------------|-------|
| 1 | path/to/source.ext | path/to/test.ext | name-stem + import | — |
| 2 | path/to/unmapped.ext | — | — | No test suite found |

Close with summary counts: total source units, mapped units, unmapped units, orphan test suites, and excluded integration/E2E suites.

## Artifact Persistence

- Before the next stage begins, write the complete output to `transitions/01-test-mapping-<runId>.md` in the **current workspace** (create `transitions/` if absent) — never into an external target directory.
- The artifact must be **self-contained** so a later session can resume from the file alone: run ID, target root, generation timestamp, the full Target Mapping table, summary counts, and the list of excluded integration/E2E suites.
- If invoked in a context without write capability, emit the full artifact markdown in the response and state that the invoking agent must persist it.
