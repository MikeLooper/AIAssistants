# Checklist — Testing

Elements are defined in `standards/` (MFT in `martinfowler-testing.md`; MSU in `microsoft-unit-testing.md`; STS in
`security-testing.md`; TSR in `testing-rubric.md`; AZT in `azure-waf-testing.md`). Every element belongs to exactly one check.

| id | Check | Default severity | Elements |
|----|-------|------------------|----------|
| TST-01 | The suite is pyramid-shaped: most tests are fast unit tests without infrastructure; integration tests are fewer; E2E/UI tests are few, cover only key journeys and don't duplicate lower-level coverage | Warning | MFT-02, MFT-03, MFT-13, MFT-14, MFT-17, MFT-34, MSU-01, MSU-07, TSR-01, TSR-02, TSR-03 |
| TST-02 | Code coverage is measured and reported (in CI or by a documented local command). It is used to find untested code; no percentage is required | Warning | MFT-19, MFT-20, MFT-21, MSU-05, TSR-04, TSR-05 |
| TST-03 | Tests can fail for real defects: they assert observable behavior and outputs through public interfaces, not just "did not throw", tautologies or private internals | Warning | MFT-06, MFT-07, MSU-04, MSU-15, TSR-06, TSR-07 |
| TST-04 | Test doubles are used judiciously: only for slow, remote or awkward collaborators, named for their role, without mocking the code under test or verifying the implementation instead of the outcome | Warning | MFT-04, MFT-05, MFT-31, MFT-32, MFT-33, MSU-06, TSR-08, TSR-09 |
| TST-05 | Tests are independent and deterministic: they pass in any order, share no mutable state, don't sleep-wait, control time and randomness, avoid live remote systems, and flaky or skipped tests are quarantined with limits | Warning | MFT-23, MFT-24, MFT-25, MFT-26, MFT-27, MFT-28, MFT-29, MFT-30, MSU-02, MSU-03, MSU-16, TSR-10, TSR-11, TSR-12 |
| TST-06 | The test suite runs automatically in CI on every push and pull request, ordered fast-first, and any failing test fails the build | Error | MFT-01, MFT-16, MFT-35, MFT-37, MFT-38, STS-14, TSR-13, TSR-14 |
| TST-07 | Every logic-bearing production project/module has automated tests, and features are verified by acceptance-level tests | Warning | MFT-15, MFT-36, TSR-15 |
| TST-08 | Test code is clean: arrange/act/assert structure, descriptive consistent names, one act and one condition per test, no logic or magic values, minimal inputs, visible setup through helpers or builders | Information | MFT-08, MFT-18, MFT-22, MSU-08, MSU-09, MSU-10, MSU-11, MSU-12, MSU-13, MSU-14, TSR-16, TSR-17 |
| TST-09 | Integration points are tested: data access against a real engine, outbound clients against fake servers, service boundaries by contract tests; never against production | Warning | MFT-09, MFT-10, MFT-11, MFT-12, MFT-39, MFT-40, TSR-18, TSR-19, TSR-20 |
| TST-10 | Security behavior is tested: authorization (deny by default, per role/owner, failure paths), security error paths, logging behavior, and regressions for fixed vulnerabilities | Warning | STS-01, STS-02, STS-03, STS-04, STS-05, STS-06, STS-09, STS-11, TSR-21, TSR-22 |
| TST-11 | Code that parses untrusted input is exercised by fuzz or property-based tests, or by dynamic security testing in the automated pipeline | Information | STS-07, STS-08, STS-10, STS-12, STS-13, TSR-23 |
| TST-12 | Deployable services have automated load or performance tests (k6, JMeter, Locust, Gatling, NBomber, Artillery or a hosted load-test config) with pass/fail thresholds, run in CI or on a recorded schedule against a production-like target | Information | AZT-01, AZT-02, AZT-03, AZT-04, AZT-05 |
| TST-13 | Resilience is tested: retry, timeout and circuit-breaker behaviour and dependency failures are exercised by tests, and any fault-injection or chaos experiments are scoped and run regularly | Information | AZT-06, AZT-07, AZT-08, AZT-09 |
