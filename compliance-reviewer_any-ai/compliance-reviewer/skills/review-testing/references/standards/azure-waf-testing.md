# Azure Well-Architected and Architecture Center testing guidance — localized summary

- Source site: learn.microsoft.com (azure/well-architected and azure/architecture)
- Pinned pages: see the page table below (path, `ms.date` and `git_commit_id` at retrieval, 2026-11-09)
- Citation base: https://learn.microsoft.com/azure/
- Localized: 2026-11-09 · Elements: 9 (testing's learn.microsoft.com budget: 16 + 9 = 25 of 100)
- Source name for `Finding.standard`: the Source name of the element's primary page (page table).
- Level: every element is `REVIEW` (the pages use no normative keywords); severity is the owning check's default.
- Scope: generic. Azure product names in the sources (Azure Load Testing, Chaos Studio) are generalized ("load-test
  tool", "fault-injection tool"). Tool names a reviewer can look for are in `../SKILL.md` step 6.
- Citation: `Finding.url` = citation base + page path + `#` + primary (first) anchor, with no locale segment.
  Example: `https://learn.microsoft.com/azure/well-architected/performance-efficiency/performance-test#start-early-and-test-continuously`.

| Key | Page path | Source name | ms.date | Git commit |
|-----|-----------|-------------|---------|------------|
| pe-test | `well-architected/performance-efficiency/performance-test` (PE:06) | Azure Well-Architected Framework | 2026-06-24 | c96d7decedaf65e86add6d4c063c6b380c1535ef |
| re-test | `well-architected/reliability/reliability-test` (RE:08) | Azure Well-Architected Framework | 2026-05-27 | c96d7decedaf65e86add6d4c063c6b380c1535ef |
| bp-tf | `architecture/best-practices/transient-faults` | Azure Architecture Center | 2026-02-26 | d6ef15167b11bdd59c441e3af2068b5e86369155 |

## TST-12 — Load and performance tests

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| AZT-01 | REVIEW | Automated load tests exist for the service's critical flows, scripted as synthetic transactions with realistic data and usage patterns; load testing comes first, stress, spike and soak tests as risk grows. | deployable service with request or message endpoints | TST-12 | pe-test#apply-multiple-performance-test-types, pe-test#use-real-world-usage-patterns-and-data-characteristics |
| AZT-02 | REVIEW | Load tests have acceptance criteria with explicit pass/fail thresholds per metric (for example p95 latency, error rate, throughput), derived from the stated performance targets. | load tests exist | TST-12 | pe-test#set-measurable-goals-for-your-performance-tests |
| AZT-03 | REVIEW | Performance tests run in the deployment pipeline or on a recorded automated schedule, so regressions and drift are caught before production. | load tests exist | TST-12 | pe-test#start-early-and-test-continuously |
| AZT-04 | REVIEW | Load tests target a production-like environment (matching compute, autoscaling and caching settings, or a deliberately scaled-down copy for non-critical workloads), never a developer machine as the only target. | load-test config names a target environment | TST-12 | pe-test#mirror-your-production-environment |
| AZT-05 | REVIEW | Results are compared with a recorded baseline (stored results, baseline file or run comparison), so regressions are visible. | load tests run in CI or on a schedule | TST-12 | pe-test#use-test-results-to-guide-design-decisions |

## TST-13 — Resilience tests

| ID | Level | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------|-----------------------|--------------|-------|-----------|
| AZT-06 | REVIEW | Transient-fault handling is tested: retry policies, timeouts and circuit-breaker thresholds are exercised under failure, including exhaustion (all retries fail, breaker open) and the switch to fallback or degradation. | code makes remote calls with retry, timeout or breaker logic | TST-13 | re-test#transient-faults |
| AZT-07 | REVIEW | Retry behaviour is tested deterministically: a mock or fake returns the range of errors the retry strategy detects, or an HTTP fault library in automated tests changes status codes, headers or latency. | code makes remote calls with retry logic | TST-13 | bp-tf#test-your-retry-strategy-and-implementation |
| AZT-08 | REVIEW | Critical dependency failures are tested: each fallback activates, partial failures (added latency, intermittent errors) are covered, and one failing dependency doesn't break unrelated functionality. | code calls remote dependencies on critical flows | TST-13 | re-test#dependency-failures |
| AZT-09 | REVIEW | Fault-injection or chaos experiments have a stated hypothesis and a contained blast radius, start in non-production environments, run on a regular cadence or in the pipeline, and may be combined with load tests. | fault-injection or chaos definitions in scope | TST-13 | re-test#use-fault-injection-and-chaos-engineering, re-test#combine-different-types-of-tests, bp-tf#test-your-retry-strategy-and-implementation |
