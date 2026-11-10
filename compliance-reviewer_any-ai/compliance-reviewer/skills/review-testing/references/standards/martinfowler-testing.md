# Martin Fowler (martinfowler.com) — testing, localized summary

- Source site: martinfowler.com · Version: articles as dated below (each page's "Significant Revisions" list)
- Citation base: https://martinfowler.com/
- Localized: 2026-11-09 (retrieved 2026-11-09) · Elements: 40 (cap 100)
- Source name for `Finding.standard`: Martin Fowler (martinfowler.com)
- Level: informational only; severity is the owning check's default.
- Anchors are the pages' table-of-contents ids and are **case-sensitive** (e.g. `#TheImportanceOftestAutomation`,
  `#End-to-endTests`, `#build-fast`). `tc` has no section anchors: cite the page URL.
- Citation: `Finding.url` = citation base + page path + `#` + primary anchor, e.g.
  `https://martinfowler.com/articles/nonDeterminism.html#LackOfIsolation`.

| Key | Page path | Pin |
|-----|-----------|-----|
| ptp | `articles/practical-test-pyramid.html` | 2018-02-26 (Ham Vocke; installments 2018-02-14 … 2018-02-26) |
| tc | `bliki/TestCoverage.html` | 2012-04-17 (no section anchors) |
| nd | `articles/nonDeterminism.html` | 2011-04-14 |
| mas | `articles/mocksArentStubs.html` | 2007-01-02 (first published 2004-07-08) |
| ci | `articles/continuousIntegration.html` | 2024-01-18 |

| ID | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-----------------------|--------------|-------|-----------|
| MFT-01 | Tests are automated so the software can be released at any time. Regression checking doesn't depend on manual click-through. | always | TST-06 | ptp#TheImportanceOftestAutomation |
| MFT-02 | The suite is shaped like a pyramid: many small, fast unit tests, fewer coarser tests, and very few end-to-end tests (no "ice-cream cone"). | any tests | TST-01 | ptp#TheTestPyramid |
| MFT-03 | Unit tests make up the largest share and stay fast, so they don't touch databases, the filesystem or the network. | any tests | TST-01 | ptp#UnitTests |
| MFT-04 | Collaborators are replaced with doubles only when the real ones are slow or awkward. Otherwise real (sociable) collaborators are fine. | unit tests with doubles | TST-04 | ptp#SociableAndSolitary |
| MFT-05 | Test doubles replace external or slow parts. Mocks and stubs are distinguished, and the terms aren't used interchangeably. | unit tests with doubles | TST-04 | ptp#MockingAndStubbing |
| MFT-06 | Private methods aren't tested directly (no reflection or visibility hacks). Wanting to test one signals a class that should be split. | any tests | TST-03 | ptp#private-methods-sidebar |
| MFT-07 | Tests exercise the public interface and observable behavior, including non-trivial and edge paths, not implementation details or trivial accessors. | any tests | TST-03 | ptp#WhatToTest |
| MFT-08 | Each test has a clear arrange/act/assert (given/when/then) structure. | any tests | TST-08 | ptp#TestStructure |
| MFT-09 | Every point where data is serialized or deserialized (database, REST, queue, files) has an integration test. One integration point is tested at a time, against dependencies run locally, never against production. | integration points exist | TST-09 | ptp#IntegrationTests |
| MFT-10 | At least one repository or data-access integration test runs against a real engine. In-memory substitutes can behave differently from production. | data store used | TST-09 | ptp#DatabaseIntegration |
| MFT-11 | Separate services and third-party APIs are replaced by fake servers in integration tests, and those fakes are verified by contract tests. | outbound HTTP or messaging client | TST-09 | ptp#IntegrationWithSeparateServices |
| MFT-12 | Interfaces between separately deployed consumers and providers are covered by consumer-driven contract tests that the provider verifies in its pipeline. | ≥ 2 services, or a client of an in-house service | TST-09 | ptp#ContractTests, ptp#ConsumerTestourTeam, ptp#ProviderTestourTeam |
| MFT-13 | End-to-end tests cover only the most valuable user journeys. API-level end-to-end tests are preferred over browser tests where they give the same confidence. | E2E tests exist | TST-01 | ptp#End-to-endTests, ptp#RestApiEnd-to-endTest |
| MFT-14 | UI behavior (including APIs and CLIs as user interfaces) is tested with framework-level tools where possible, not only through full-stack browser tests. | UI or CLI present | TST-01 | ptp#UiTests |
| MFT-15 | Features are verified from the user's perspective by acceptance tests, which may be written at a lower level than the UI. | always | TST-07 | ptp#acceptance |
| MFT-16 | Pipeline stages are ordered by speed and scope. Fast tests run first, and narrow integration tests may run alongside unit tests. | CI config present | TST-06 | ptp#PuttingTestsIntoYourDeploymentPipeline |
| MFT-17 | Tests are pushed as low in the pyramid as possible. A higher-level test that only duplicates lower-level coverage is removed. | ≥ 2 test levels | TST-01 | ptp#AvoidTestDuplication |
| MFT-18 | Test code gets the same care as production code. Each test checks one condition, and readability is preferred over DRY. | any tests | TST-08 | ptp#WritingCleanTestCode |
| MFT-19 | Coverage is measured to find untested code. The coverage tool is run regularly and its gaps are reviewed. | always | TST-02 | tc |
| MFT-20 | Coverage isn't treated as a quality target. A mandated percentage invites gaming, up to and including assertion-free tests. | coverage threshold configured | TST-02 | tc |
| MFT-21 | Coverage figures are interpreted, not mandated: well below half signals trouble, near 100 % is suspicious, and upper 80s–90s is typical of thoughtful testing. | coverage threshold configured | TST-02 | tc |
| MFT-22 | When simple production changes need long test changes, the cause is usually duplication in the tests. | any tests | TST-08 | tc |
| MFT-23 | Non-deterministic (flaky) tests are fixed or quarantined promptly. Quarantine is limited in size and age and kept out of the main pipeline. | any tests | TST-05 | nd#WhyNon-deterministicTestsAreAProblem, nd#Quarantine |
| MFT-24 | Tests are isolated and pass in any order. Each test builds its start state from scratch (or rolls back a transaction) instead of relying on earlier tests. | any tests | TST-05 | nd#LackOfIsolation |
| MFT-25 | Shared state in statics, singletons and context (for example the logged-in user) doesn't leak between tests, and tear-down failures are loud. | any tests | TST-05 | nd#LackOfIsolation |
| MFT-26 | Asynchronous results are awaited with callbacks or short polling under a timeout, never with bare sleeps. A timeout fails with a clear message. | async code under test | TST-05 | nd#AsynchronousBehavior |
| MFT-27 | Logic is moved out of asynchronous plumbing (Humble Object) so it can be tested synchronously. | async code under test | TST-05 | nd#AsynchronousBehavior |
| MFT-28 | Functional tests don't depend on live remote systems. They use doubles for determinism. | remote dependencies | TST-05 | nd#RemoteServices |
| MFT-29 | The system clock is wrapped so tests can control time. Clock stubs are re-initialized per test, and direct clock calls can be blocked by a build check. | time-dependent code | TST-05 | nd#Time |
| MFT-30 | Leaks and hidden randomness are exposed: pooled resources are sized to 1 in tests and randomizers are stubbed to fixed values. | pooled resources or randomness | TST-05 | nd#ResourceLeaks |
| MFT-31 | Test doubles are named for their role (dummy, fake, stub, spy, mock) so a reader knows what is being verified. | unit tests with doubles | TST-04 | mas#TheDifferenceBetweenMocksAndStubs |
| MFT-32 | State verification with real objects is used where collaboration is easy. Doubles and behavior verification are used where collaboration is awkward or state can't reveal the outcome (for example caching). | unit tests with doubles | TST-04 | mas#ClassicalAndMockistTesting, mas#ChoosingBetweenTheDifferences |
| MFT-33 | Interaction-verifying tests couple to the implementation and hinder refactoring. Strict call and argument matching is used only where the interaction *is* the behavior. | mocks with verification | TST-04 | mas#CouplingTestsToImplementations |
| MFT-34 | Whatever the unit-test style, the suite also has coarser acceptance or system tests across the system. | any tests | TST-01 | mas#SoShouldIBeAClassicistOrAMockist |
| MFT-35 | The build is self-testing. A comprehensive suite runs in the build, and any failing test fails the build. | CI config present | TST-06 | ci#MakeTheBuildSelf-testing |
| MFT-36 | A change isn't complete until automated tests verify its new behavior. | always | TST-07 | ci#MakeTheBuildSelf-testing |
| MFT-37 | Every push to mainline triggers a build that runs the tests. | CI config present | TST-06 | ci#EveryPushToMainlineShouldTriggerABuild |
| MFT-38 | The commit build stays fast (about ten minutes). Slower tests move to later pipeline stages, independent tests run in parallel, and a bug caught late gets a commit-stage test. | CI config present | TST-06 | ci#build-fast |
| MFT-39 | Tests that need infrastructure run against a production-like environment (same versions, typically containers), not hand-maintained shared servers. | integration tests exist | TST-09 | ci#TestInACloneOfTheProductionEnvironment |
| MFT-40 | Contract tests against external services run on an automated schedule. | contract tests or fakes of external services | TST-09 | ci#build-fast |
