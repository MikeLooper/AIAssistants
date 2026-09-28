---
name: unit-test-coverage-test-assertion-audit
description: 'Audits unit test cases against the cataloged logical paths to verify whether branches are truly tested. Use after control-flow-extraction, or when asked to check assertion quality, mock bypass risks, or whether tests really verify behavior. Maps test fixture inputs and parameters to specific paths (P-01, P-02), flags Mock Bypass False Positives where mocked objects skip intermediate branch logic, evaluates Assertion Strength (execution without verification vs true state/exception assertion), and classifies paths as Covered, Partially Covered, or Uncovered. Strictly read-only.'
---

# Unit Test Coverage — Test Assertion Audit

Third stage of the Unit Test Coverage Reviewer pipeline. Consumes the Target Mapping table (test-mapping) and the logical path catalog (control-flow-extraction), and produces the **per-path coverage classifications** consumed by `unit-test-coverage-reporting`.

## Inputs

- Target Mapping table (source ↔ test suites) — from in-context state, or from `transitions/01-test-mapping-<runId>.md` when resuming.
- Logical path catalog (`P-01`, `P-02`, … per method) — from in-context state, or from `transitions/02-control-flow-<runId>.md` when resuming.
- `runId`: the run's shared `YYYYMMDD-HHmmss` timestamp, supplied by the orchestrating agent.

## Guardrails

- **READ-ONLY**: never edit test files, even to "improve" them. All remediation is deferred to the reporting stage as markdown snippets.

## Procedure

For each source unit and its mapped test suite(s):

1. **Map test cases to paths**
   - Correlate each test's fixture inputs, parameterized cases (e.g., `[Theory]`/`InlineData`, `@ParameterizedTest`, `pytest.mark.parametrize`, table-driven Go tests), and stubbed return values with the specific path IDs they drive execution through.
   - One test may cover multiple paths; one path may require multiple tests. Record the mapping explicitly.
2. **Flag Mock Bypass False Positives**
   - Detect cases where a mocked collaborator's canned response skips intermediate branch logic in the unit under test (e.g., the mock returns a pre-computed result so the `if/else` that would normally derive it never executes).
   - Also flag mocks configured to match any input (`It.IsAny`, `any()`, `mock.Anything`) when input-dependent branches exist downstream.
3. **Evaluate Assertion Strength**
   - *Strong*: asserts returned state, mutated state, exact exception type, or specific emitted values.
   - *Weak*: asserts only non-null, mock interaction counts (`Verify`/`toHaveBeenCalled`) without state checks, or snapshot-only without semantic review.
   - *Absent*: test executes the path with no assertion at all ("execution without verification") — treat as Uncovered regardless of execution.
4. **Classify each path**
   - **Covered**: a test drives the path AND asserts its expected outcome strongly.
   - **Partially Covered**: the path executes but assertions are weak, or only some sub-conditions of a compound branch are exercised, or a Mock Bypass risk exists.
   - **Uncovered**: no test drives the path, or execution occurs with no meaningful assertion.

## Output

A per-unit audit table:

### `<source unit>` vs `<test unit(s)>`

| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---------|-----------|--------------|--------------------|----------------|-------|
| P-01 | input is null | `Ctor_NullInput_Throws` | Strong (exception type) | Covered | — |
| P-02 | list is empty | — | — | Uncovered | No test found |
| P-03 | flag == true | `Process_FlagTrue_Runs` | Weak (verify-only) | Partially Covered | Mock bypass risk on dependency |

Close with tally counts: Covered, Partially Covered, Uncovered, and Mock Bypass risk count — the inputs to the reporting stage's metrics.

## Artifact Persistence

- Write the complete audit (all per-unit tables plus tallies) to `transitions/03-assertion-audit-<runId>.md` in the current workspace before the reporting stage begins.
- The artifact must be **self-contained** for resume: run ID, target root, generation timestamp, every audit table, and the tally counts (Covered / Partially Covered / Uncovered / Mock Bypass risks).
- If invoked in a context without write capability, emit the full artifact markdown in the response and state that the invoking agent must persist it.
