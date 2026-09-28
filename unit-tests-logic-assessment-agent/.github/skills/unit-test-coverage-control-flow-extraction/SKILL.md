---
name: unit-test-coverage-control-flow-extraction
description: 'Statically catalogs all distinct logical execution paths in target source code for a coverage review. Use after test-mapping, or when asked to extract branches, decision points, or edge cases from source. Extracts decision trees (if/else-if/else, switch/case, ternary), guard clauses and early returns, error/exception branches (try/catch/finally, Result/Option unwraps, non-zero return checks), and boundary conditions (empty or single-item collections, boundary integer values, null/undefined checks), assigning unique path IDs (P-01, P-02, ...) per method. Strictly read-only analysis.'
---

# Unit Test Coverage — Control Flow Extraction

Second stage of the Unit Test Coverage Reviewer pipeline. Consumes the Target Mapping table from `unit-test-coverage-test-mapping` and produces the **logical path catalog** consumed by `unit-test-coverage-test-assertion-audit`.

## Inputs

- Target Mapping table (source units to analyze) — either from in-context pipeline state, or loaded from `transitions/01-test-mapping-<runId>.md` when resuming an interrupted run.
- `targetRoot` for resolving file locations.
- `runId`: the run's shared `YYYYMMDD-HHmmss` timestamp, supplied by the orchestrating agent.

## Guardrails

- **READ-ONLY**: analysis is purely static. Never modify source files, and never execute target code to "discover" paths.

## Procedure

For each mapped source unit, walk every method/function and catalog the following structures:

1. **Decision trees**
   - `if` / `else if` / `else` chains — one path per branch arm, plus the fall-through path when no `else` exists.
   - `switch`/`match` statements — one path per `case`, plus `default`; note fall-through cases.
   - Ternary expressions and short-circuit boolean operators (`&&`, `||`, `??`, `?.`) — each operand outcome is a branch.
2. **Guard clauses & early returns**
   - Validation checks, precondition failures, and early `return`/`break`/`continue` statements that short-circuit the method.
3. **Error & exception branches**
   - `try` / `catch` / `finally` — one path per distinct `catch` clause plus the happy path.
   - Language idioms: `Result`/`Option` unwraps (Rust), `err != nil` checks (Go), `Either` folds (JVM), non-zero/null return-code checks (C-style APIs).
   - Thrown/raised exceptions — both deliberate validation throws and propagating calls.
4. **Boundary conditions**
   - Empty collections vs single-item vs multi-item iterations.
   - Boundary integer values (0, -1, `MAX_VALUE`, loop start/end off-by-one).
   - Null/undefined/None checks and optional chaining.
   - String edge cases (empty, whitespace, very long) where logic depends on them.

## Path Identification

- Assign unique identifiers per method: `P-01`, `P-02`, …, restarting per method.
- Record for each path: the triggering condition, the expected outcome (return value, state change, or exception), and the source location (file + line range).
- Merge dominated/duplicate conditions; skip trivially unreachable code but note it as a finding.

## Output

A logical path catalog per source unit:

### Method: `<signature>` — `path/to/source.ext` (lines X–Y)

| Path ID | Condition / Branch | Expected Outcome | Category |
|---------|--------------------|------------------|----------|
| P-01 | input is null | throws ArgumentNullException | Error branch |
| P-02 | list is empty | returns empty result | Boundary |
| P-03 | flag == true | takes `if` arm | Decision tree |

End with a per-unit path count and the run total ($N_{\text{total}}$) for the reporting stage.

## Artifact Persistence

- Write the complete logical path catalog to `transitions/02-control-flow-<runId>.md` in the current workspace before the audit stage begins.
- The artifact must be **self-contained** for resume: run ID, target root, generation timestamp, every method's path table (path IDs, conditions, expected outcomes, categories, source locations), per-unit counts, and the run total $N_{\text{total}}$.
- If invoked in a context without write capability, emit the full artifact markdown in the response and state that the invoking agent must persist it.
