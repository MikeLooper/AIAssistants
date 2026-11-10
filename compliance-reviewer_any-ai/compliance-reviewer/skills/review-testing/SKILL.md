---
name: review-testing
description: 'Reviews automated tests for pyramid balance, coverage measurement, assertion quality, use of test doubles, isolation and determinism, CI execution and gating, tests for every production module, clean test code, integration and contract tests, security-focused tests (authorization, error and logging paths, fuzzing), and load/performance and resilience tests, against local summaries of Martin Fowler''s testing articles, Microsoft''s unit-testing best practices, Azure Well-Architected PE:06/RE:08 testing guidance, OWASP, NIST SSDF PW.8, OpenSSF Scorecard and a local Testing Rubric. Use when the compliance-reviewer orchestrator delegates the Testing subject.'
user-invocable: false
---

# Review: Testing

Assesses the automated test suite: its shape (test pyramid), whether coverage is measured, whether tests can
actually fail, how test doubles are used, isolation and determinism, CI execution, coverage of production modules,
test-code quality, integration and contract tests, security-focused tests, and load/performance and resilience
tests.

## Inputs

The capped, sampled list of test files, test configuration and CI test steps assigned by `compliance-inventory`,
plus the inventory's `testInventory` summary (test totals by category, production project roots and signals, when
present), and any authorization or integration-client file it lists for this subject. Review only those files.

## Standards (local, authoritative)

- `references/standards/testing-rubric.md`: TSR-01…TSR-23, the signal table and thresholds. Always load.
- `references/standards/martinfowler-testing.md`: MFT-01…MFT-40. Always load.
- `references/standards/microsoft-unit-testing.md`: MSU-01…MSU-16 (language-neutral). Always load.
- `references/standards/security-testing.md`: STS-01…STS-14. Always load.
- `references/standards/azure-waf-testing.md`: AZT-01…AZT-09 (load and resilience tests). Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation, apply the closest element if it clearly fits. Otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md` and the five standards files.
2. Skip snapshot, recorded-cassette, fixture-data, generated and vendored files; note any skipped.
3. Classify tests as unit, integration or E2E/UI using the TSR-01 signal table. Names count only when the content
   agrees. Use the inventory's per-category totals for ratios; if only the sample is available, judge TST-01 only
   when the imbalance is unmistakable, with confidence `low`, and add
   `localized-standard-gap: pyramid judged from sample only` to `notes`. For an unknown test framework add
   `localized-standard-gap: unknown test framework <name>` once.
4. Evidence rule: a rubric threshold is a trigger, not a verdict. Fail only when the threshold is exceeded **and**
   reading the tests confirms the problem. State the counted value in the evidence excerpt; confidence `medium`
   unless the value is at least twice the threshold.
5. If the repository has no automated tests: fail TST-01, TST-02, TST-06 and TST-07; mark TST-03, TST-04, TST-05,
   TST-08 and TST-09 N/A ("no tests"); evaluate TST-10 … TST-13 if they apply.
6. For each check TST-01…TST-13, evaluate only the elements it lists whose "Applies when" condition holds; if none
   apply, mark the check N/A with that reason. TST-09 needs integration points (a data store, an outbound HTTP or
   messaging client, or ≥ 2 services), TST-10 access control (N/A for libraries and CLIs without it), and TST-11
   untrusted-input parsing. TST-07 needs production roots; without them judge it only from test-project names that
   obviously mirror production projects, with confidence `low`. TST-02 never fails on a coverage percentage: record
   TSR-05 observations in `notes` only. TST-04 never fails for a mocking style or library, only for the
   TSR-08/TSR-09 signals.
   TST-12 (load tests) applies to a deployable service with request or message endpoints; it is N/A for libraries,
   CLIs and static front ends. Load-test signals: `*.k6.js`/k6 scripts (`import http from 'k6/http'`), `*.jmx`,
   `locustfile.py`, Gatling simulations, NBomber projects, Artillery YAML, hosted load-test configs; use
   `testInventory.signals.loadTests` when the sample has none. No load tests at all fails AZT-01 (confidence
   `medium`); AZT-02 … AZT-05 are judged only when load tests exist. Never fail for a missing stated target: without
   one, AZT-02 passes when any threshold is set.
   TST-13 (resilience tests) applies when the code makes remote calls (`testInventory.signals.integrationPoints`).
   Resilience signals: tests that make a fake, mock server or HTTP fault handler return errors, delays or timeouts and
   assert retry, breaker or fallback behaviour (WireMock/MockServer fault responses, `HttpMessageHandler` stubs,
   Polly/Resilience4j test setups, `responses`/`respx` errors), Toxiproxy config, Chaos Mesh/Litmus manifests, hosted
   chaos experiments; use `testInventory.signals.faultInjection` when the sample has none. Fail AZT-06/AZT-07 only
   when retry, timeout or breaker logic is visible in the files and no test exercises its failure path. AZT-09 is
   judged only when fault-injection or chaos definitions exist; their absence alone is never a failure.
7. Boundaries: don't fail for whether CI builds every change (review-software-lifecycle SL-01), SAST or analyzer
   gating (SL-11), branch protection (SL-04), README test instructions (review-maintainability MAINT-01),
   production-code design or testability smells (review-software-quality), production-code correctness of
   authorization, input handling, errors or logging (security skills), API contract documentation
   (review-api-design), restore tests or DR drills (review-disaster-recovery), alert testing (review-monitoring),
   or test-only packages in production scope (review-dependency-management). Load, performance, resilience and
   chaos tests are judged here (TST-12/TST-13; decision D-3, 2026-11-09); the code's own retry, timeout and breaker
   logic is review-reliability's, and its performance is review-performance's.
8. Severity: every Finding takes the check's default severity from `checklist.md`;
   `checkResults.severityIfFailed` is always that default.
9. Citations: `standard` = "<source name> — <element ID>" of the failed element (source names in each standards
   file header, or per row in `security-testing.md`); `url` = citation base + page path + "#" + primary anchor, or
   for rubric elements the `docs/reports/`-relative path + `#tsr-NN`. `urlsFetched` stays empty.
10. Note strengths where the suite is clearly well shaped, coverage is published, tests are deterministic and
    readable, contract tests guard service boundaries, authorization has thorough negative tests, or load and
    fault-injection tests gate the pipeline.

## Output

Emit every finding, strength and check result with `subject: "Testing"`. Follow `compliance-review-core`'s
`finding-schema.md`.
