# Compliance Reviewer Testing Rubric — local standard

- Source: authored in this repository (no external source; see `../sources.md`)
- Version: 1.0 · Created: 2026-11-09 · Elements: 23 (no website, no cap)
- Source name for `Finding.standard`: `Compliance Reviewer Testing Rubric`
- Citation base (relative to `docs/reports/`): `../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md` + `#tsr-NN`
- Level: informational only; severity always comes from the owning check (SKILL.md).
- **Thresholds are triggers, not verdicts.** Fail only when the threshold is exceeded **and** reading the tests
  confirms the problem (e.g. a 50-line test that builds one large expected object is not a long test). Counts are
  reading estimates: state the counted value in the evidence excerpt and use confidence `medium` unless the value is
  at least twice the threshold. An approved analyzer output (step `02`) may support a count but is never required.
- **Counting.** Ratios (TSR-02) use the inventory's `testInventory.totals` when present; otherwise `totalMatched` with
  folder or project names; from the 12-file sample only when the imbalance is unmistakable (confidence `low`, plus
  `localized-standard-gap: pyramid judged from sample only` in `notes`).

## Signals (part of TSR-01)

Folder and project names (`*.UnitTests`, `*.IntegrationTests`, `e2e/`, `tests/integration/`) count only when the
content agrees. Unit = no infrastructure (no database, network, filesystem, container, browser or in-process web host).
Integration = a real or containerized dependency, or an in-process host. E2E/UI = a deployed or full-stack target.

| Signal | .NET | Java | Python | JS/TS | Go |
|---|---|---|---|---|---|
| Test framework | xUnit, NUnit, MSTest | JUnit 5, TestNG | pytest, unittest | Jest, Vitest, Mocha | `testing` |
| Assertion | `Assert.*`, FluentAssertions `.Should()`, Shouldly | `assert*`, AssertJ `assertThat` | `assert`, `self.assert*`, `pytest.raises` | `expect(...)`, `assert` | `t.Error*`, `t.Fatal*`, testify |
| Expected-exception test (counts as an assertion) | `Assert.Throws*`, `.Should().Throw` | `assertThrows` | `pytest.raises`, `assertRaises` | `toThrow`, `rejects` | error checks |
| Skip | `[Fact(Skip=…)]`, `[Ignore]`, `[Explicit]` | `@Disabled`, `@Ignore` | `@pytest.mark.skip`, `xfail`, `@unittest.skip` | `it.skip`, `xit`, `test.todo` | `t.Skip` |
| Order dependence | `[Order]`, `TestCaseOrderer`, `[Priority]` | `@TestMethodOrder`, `@Order`, `dependsOnMethods` | `pytest-order`, `pytest-dependency` | `--runInBand` used to hide shared state | — |
| Integration | Testcontainers, `WebApplicationFactory`, `TestServer` | Testcontainers, `@SpringBootTest`, `@DataJpaTest` | Testcontainers, DB fixtures, `TestClient` against a real app | Testcontainers, supertest against a real DB | `httptest` + real DB |
| HTTP fakes | WireMock.Net | WireMock, MockServer | `responses`, `respx`, `pytest-httpserver` | `nock`, `msw` | `httptest.Server` |
| Contract tests | PactNet | Pact JVM, Spring Cloud Contract | pact-python | pact-js | pact-go |
| E2E/UI | Playwright, Selenium | Selenium, Playwright, REST-assured (base URL) | Playwright, Selenium | Playwright, Cypress, Puppeteer | chromedp |
| Coverage | coverlet, `--collect:"XPlat Code Coverage"`, dotCover | JaCoCo | coverage.py, pytest-cov | c8, nyc/istanbul, `--coverage` | `-cover`, `-coverprofile` |
| Fuzz / property-based | SharpFuzz, FsCheck, CsCheck | Jazzer, jqwik | Hypothesis, atheris | fast-check, jsfuzz | `func FuzzXxx` |
| DAST | OWASP ZAP baseline/API scan job, Nuclei, Burp CI | (same) | (same) | (same) | (same) |
| Report published | Codecov or Coveralls upload, a coverage artifact, a PR coverage comment, a `reportgenerator` step, a documented local command | | | | |

An unknown test framework: classify by content where possible and add
`localized-standard-gap: unknown test framework <name>` to `notes` once.

**Excluded files:** snapshot files (`*.snap`, `__snapshots__/`, `*.verified.*`), recorded HTTP cassettes, test-data
fixtures, `obj/`, `target/`, `build/`, `node_modules/`, `vendor/`. Note and skip them if handed over.

## Thresholds

| Measure | Threshold | Element |
|---|---|---|
| Pyramid shape | E2E/UI tests ≥ unit tests, **or** unit tests < 50 % of classified tests | TSR-02 |
| Assertion-free tests | ≥ 2 sampled tests **or** > 10 % of sampled test methods | TSR-06 |
| Test doubles per unit test | > 5 | TSR-08 |
| Skipped tests | any skip without a reason or tracking reference, **or** > 5 % of sampled tests skipped | TSR-12 |
| Test length | > 40 logical lines | TSR-16 |
| Copied arrange block | > 10 lines repeated in ≥ 3 tests | TSR-17 |

## Elements

| ID | Criterion (fail when …) | Applies when | Check |
|----|-------------------------|--------------|-------|
| <a id="tsr-01"></a>TSR-01 | *(Classification.)* Tests are classified unit, integration or E2E/UI by the signals above. Names count only when the content agrees, and unclassifiable tests are left out of ratios. Not failed on its own. | any tests | TST-01 |
| <a id="tsr-02"></a>TSR-02 | The pyramid is inverted per the thresholds, counted from inventory totals, or from the sample only when unmistakable (confidence `low`). | ≥ 2 test levels or E2E present | TST-01 |
| <a id="tsr-03"></a>TSR-03 | Logic-bearing production code is tested only through integration or E2E tests: there is no unit-test project, folder or file. | any tests | TST-01 |
| <a id="tsr-04"></a>TSR-04 | No coverage collection is configured anywhere (test project, build file, CI step or documented command) per the signals, or coverage is collected but never published or reported. | any tests | TST-02 |
| <a id="tsr-05"></a>TSR-05 | *(Observation; never fails.)* An enforced threshold below 50 %, or a hard gate at ≥ 95 %, is recorded in `notes` as `TST-02 observation: …`. | coverage threshold configured | TST-02 |
| <a id="tsr-06"></a>TSR-06 | Assertion-free tests reach the threshold: no assertion, verification or expected-exception check. A "smoke" test that only proves construction or startup counts unless it is named and documented as a smoke test. | any tests | TST-03 |
| <a id="tsr-07"></a>TSR-07 | Assertions are tautological or too weak to fail for a real defect: `Assert.True(true)`, asserting a stub returns what it was set up to return, or only not-null or "no exception" where a concrete value can be checked. | any tests | TST-03 |
| <a id="tsr-08"></a>TSR-08 | Over-mocking: more than 5 doubles in one unit test, the class under test is itself mocked or partially mocked, or value objects, DTOs or collections are mocked. | unit tests with doubles | TST-04 |
| <a id="tsr-09"></a>TSR-09 | Assertions only verify mock calls that restate the implementation (every call, strict order and arguments) where an observable result or state exists. | mocks with verification | TST-04 |
| <a id="tsr-10"></a>TSR-10 | Order dependence or shared state: ordering attributes used to make tests pass (signals), mutable `static` or module-level state shared between tests, or a shared database with no reset, rollback or fresh container. | any tests | TST-05 |
| <a id="tsr-11"></a>TSR-11 | Timing and non-determinism: sleeps used as waits (`Thread.Sleep`, `Task.Delay`, `time.sleep`, `setTimeout`) with no polling or timeout, unseeded randomness, or the current time read directly (`DateTime.Now`, `Instant.now()`, `datetime.now()`, `Date.now()`) in tests or in tested code with no seam. | any tests | TST-05 |
| <a id="tsr-12"></a>TSR-12 | Skipped tests reach the threshold. A skip with a reason *and* a tracking reference is a quarantined test and passes, unless it exceeds the share. | any tests | TST-05 |
| <a id="tsr-13"></a>TSR-13 | CI config in the repository has no step that runs the test suite on push to the default branch **and** on pull requests (`dotnet test`, `mvn verify`, `gradle test`, `pytest`, `npm test`, `go test`, or a script that calls them). | always | TST-06 |
| <a id="tsr-14"></a>TSR-14 | Test failures don't fail the pipeline: `continue-on-error: true` or `allow_failure: true` on the test job, `\|\| true`, `testFailureIgnore`, `-DskipTests`/`maven.test.skip`, or `--passWithNoTests` while tests exist. | CI config present | TST-06 |
| <a id="tsr-15"></a>TSR-15 | A logic-bearing production project or package has no corresponding tests (no `X.Tests`, no `tests/x`, no test source set, and no tests elsewhere that reference it). Exempt: contracts or DTO-only projects, composition roots and hosts, generated code, and migrations. | production roots known (`testInventory.productionRoots`) | TST-07 |
| <a id="tsr-16"></a>TSR-16 | A test method exceeds 40 logical lines, or contains control flow (`if`, loops, `switch`, `try/catch` other than for an expected-exception assertion), confirmed by reading. | any tests | TST-08 |
| <a id="tsr-17"></a>TSR-17 | Complex arrangement is copied instead of shared: an arrange block of > 10 lines repeated in ≥ 3 tests, with no builder, factory or helper. | any tests | TST-08 |
| <a id="tsr-18"></a>TSR-18 | A data store or outbound HTTP or messaging client exists, but no integration test exercises it: no repository test against a real engine (container or local) and no client test against a fake server. An in-memory provider alone doesn't count. | integration points exist | TST-09 |
| <a id="tsr-19"></a>TSR-19 | ≥ 2 services in the repository communicate over HTTP or messaging, or the code calls a separately deployed in-house service, and there are no contract tests or provider verification (Pact, Spring Cloud Contract, schema-based verification). | ≥ 2 services, or a client of an in-house service | TST-09 |
| <a id="tsr-20"></a>TSR-20 | Tests call production or shared external endpoints (hard-coded production URLs or connection strings, real cloud resources) instead of local or containerized dependencies. | any tests | TST-09 |
| <a id="tsr-21"></a>TSR-21 | No negative authorization tests: nothing asserts that an unauthenticated request is rejected (401) or that the wrong role or owner is refused (403/404), and custom authorization handlers or policies have no tests. | access control present | TST-10 |
| <a id="tsr-22"></a>TSR-22 | Security-relevant error paths are untested: no test checks that invalid input is rejected or that an exception becomes a generic error response without internal details. | HTTP endpoints or input validation present | TST-10 |
| <a id="tsr-23"></a>TSR-23 | Parsers, deserializers or validators of untrusted input have no fuzz or property-based tests (signals), **and** no DAST job runs in the pipeline. Either one passes the element. | untrusted input parsed | TST-11 |
