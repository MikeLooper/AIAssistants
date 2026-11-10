# Maintenance — Testing localized standards

**Maintainers only. Workers never load this file.** Background and design decisions:
`docs/plan_localize-review-testing.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1). martinfowler.com is also used by `review-software-quality`;
learn.microsoft.com, the OWASP sites, nist.gov and github.com are used by several localized skills. Each skill has its
own budget. nvlpubs.nist.gov counts as nist.gov.

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| martinfowler.com | martinfowler-testing.md | 40 | 100 | 5 pages (ptp, tc, nd, mas, ci) |
| learn.microsoft.com | microsoft-unit-testing.md, azure-waf-testing.md | 25 (16 + 9) | 100 | `dotnet/core/testing/unit-testing-best-practices`; WAF PE:06, RE:08 and AAC transient faults (AZT, 2026-11-09) |
| cheatsheetseries.owasp.org | security-testing.md | 5 | 100 | Authorization (3), Logging `#verification` (2) |
| top10.owasp.org | security-testing.md | 2 | 100 | A01:2025, A05:2025 |
| nist.gov | security-testing.md | 5 | 100 | SP 800-218 SSDF 1.1, PW.8 (PDF page 24) |
| github.com | security-testing.md | 2 | 100 | ossf/scorecard `docs/checks.md` @ v5.6.0 (Fuzzing, CI-Tests) |
| — (local) | testing-rubric.md | 23 | n/a | Compliance Reviewer Testing Rubric v1.0 |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID.
- Primary anchor first; list every absorbed anchor so coverage stays auditable. martinfowler.com anchors are
  **case-sensitive** table-of-contents ids; check them against the raw HTML (`id = '…'`, single-quoted, with spaces).
- Every MFT, MSU, STS, TSR and AZT ID must be listed by exactly one check in `../checklist.md`.
- `security-testing.md` mixes four publishers: give the source name per row and count each website separately.
- SSDF rows name their task and example numbers and cite the **physical** PDF page (`#page=N`).
- Levels are informational; severity is always the check's default (plan DEC-7).
- Keep rows to one line (≈ 200 characters where possible).

## Rubric thresholds and signals (plan DEC-9, DEC-12)

A threshold or signal change is a rubric edit: no source refresh, but log it below with a date and reason, and add a
README note if the change would shift scores.

| Measure | Value | Reason |
|---|---|---|
| Pyramid shape (TSR-02) | E2E/UI ≥ unit, or unit < 50 % of classified tests | Lenient: only an unmistakably inverted suite fails; counts come from name/reference greps. |
| Assertion-free tests (TSR-06) | ≥ 2 sampled, or > 10 % of sampled methods | One accidental smoke test shouldn't fail the check. |
| Test doubles per unit test (TSR-08) | > 5 | Beyond five doubles a unit test usually tests wiring, not behavior; confirm by reading. |
| Skipped tests (TSR-12) | any skip without reason/tracking, or > 5 % skipped | Quarantine is acceptable when it is visible and bounded (MFT-23). |
| Test length (TSR-16) | > 40 logical lines | Above the production-code feel of a readable test; large expected-object builders are exempt by confirmation. |
| Copied arrange block (TSR-17) | > 10 lines in ≥ 3 tests | Two copies are tolerable (readability over DRY, MFT-18); three signal a missing builder. |

The signal table in `testing-rubric.md` is a lookup table: extend it when run notes log
`unknown test framework <name>` (no source refresh needed).

## Pins and watch items

- **martinfowler.com:** each page's "Significant Revisions" list (no change feed). Pins: ptp 2018-02-26, tc 2012-04-17,
  nd 2011-04-14, mas 2007-01-02, ci 2024-01-18. Confirm the TOC ids still exist.
- **Learn:** `ms.date` 2026-11-05, `git_commit_id` 3733dc918e2e037a94c719296e4d964cd460acf1 (`updated_at`
  2026-11-06). Drift: `https://api.github.com/repos/dotnet/docs/commits`.
- **OWASP cheat sheets:** Authorization @ cfd69aabc7e6090867afdc440f838b3a97cca21b (2026-10-09), Logging @
  f1d0311aaadac4c315471feb8947c9fbb3cbb32e (2026-10-22) — the last commits touching each sheet's `.md` on 2026-11-09.
  Drift: `https://api.github.com/repos/OWASP/CheatSheetSeries/commits?path=cheatsheets/<Sheet>.md`.
- **OWASP Top 10:** 2025 edition, `OWASP/Top10` @ 3a31f35346c3 (2026-09-24). A new edition means re-pinning A01/A05
  together with the security skills.
- **SSDF:** v1.1. SP 800-218 Rev. 1 (SSDF 1.2) is in draft; `review-software-lifecycle` watches it too. Re-check the PW.8
  page and example numbering on re-pin.
- **Scorecard:** v5.6.0. Drift: `https://api.github.com/repos/ossf/scorecard/releases/latest`; diff `#fuzzing` and
  `#ci-tests`.

## Refresh procedure

1. **Cadence:** every twelve months. Refresh earlier on any trigger above, or when run notes contain ≥ 3
   `localized-standard-gap` entries for this skill. "Pyramid judged from sample only" entries don't count toward the
   refresh; they are evidence for the inventory's `testInventory` (plan C-2).
2. **Drift checks:** as listed under "Pins and watch items".
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep each website ≤ 100 elements.
   Update the coverage map, the header pins and retrieval dates, `../sources.md`, and the URL list in
   `compliance-review-core/references/approved-sources.md` (section Testing) if a page moves.
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo).
   - Script-check: every element ID is in exactly one check of `../checklist.md` and the per-check counts match; every
     listed anchor exists on its pinned page; every heading on the 6 pages and every testing sentence on the security
     pages appears in the coverage map below — zero unaccounted.
   - Run a review against small sample repos (plan §12 step 8): `validate` passes, `19-review-testing.json` has
     `urlsFetched: []`, 11 checks are present, citations use pinned URLs or `#tsr-NN` paths and element IDs.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-testing` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Localization log

### 2026-11-09 — initial localization

- Implementation re-snapshot (plan §12 step 1) taken on 2026-11-09 into a scratch folder: the 5 martinfowler.com pages
  (raw HTML), the Learn page, both cheat sheets, A01/A05, the SSDF PDF and Scorecard `checks.md` @ v5.6.0. All pins
  matched the planning snapshot. **All 58 distinct cited section anchors** (MFT, MSU, STS rows; `tc` and `ssdf`
  excluded) were found on their pinned pages by script; no differences to log.
- SSDF PW.8 confirmed on **physical PDF page 24** (PW.7.2 on page 23, PW.9.1 on page 25). PW.8.1 has two examples
  (sandboxed testing policy; methods by software stage); PW.8.2 has nine. Neither PW.8.1 example is localized
  separately: STS-08 summarizes the task.
- Cheat-sheet pins: the plan left the commit open ("recorded at step 1"); pinned to the last commit touching each
  sheet's source file (more precise than the repository HEAD pins other skills use).
- Defect 1 of the plan fixed: TST-02 now cites `tc` (TestCoverage) and TST-05 cites `nd` (nonDeterminism) instead of
  the test-pyramid article, which covers neither topic.
- Martin Fowler anchors are case-sensitive (e.g. `#TheImportanceOftestAutomation`, `#ConsumerTestourTeam`,
  `#build-fast`).
- Checklist mapping checked by script on 2026-11-09: 93 element IDs (40 MFT, 16 MSU, 14 STS, 23 TSR), each in exactly
  one check; per-check counts match plan §9.
- Coverage map below built from a heading dump of the snapshot (Fowler and Learn) and from the testing sentences of
  the security pages. Script check on 2026-11-09: every h2/h3 heading on the four sectioned martinfowler.com pages
  and the Learn page appears in the map (zero unaccounted); `tc` items and the security sentences were checked by
  hand.

### 2026-11-09 — load and resilience tests adopted (afterplanning WP-8, decision D-3)

- Follow-ups F-1 (load/performance tests) and F-2 (resilience tests) adopted 2026-11-09 (D-3 in
  `docs/plan_localize-afterplanning-changes.md`); this reverses the testing plan's DEC-3 for these two topics.
- New file `azure-waf-testing.md` (prefix `AZT-`, 9 elements) from three learn.microsoft.com pages fetched
  2026-11-09: WAF PE:06 `performance-efficiency/performance-test` (ms.date 2026-06-24, commit c96d7deceda…), WAF RE:08
  `reliability/reliability-test` (ms.date 2026-05-27, commit c96d7deceda…; the old path `reliability/testing-strategy`
  redirects here) and AAC `best-practices/transient-faults` (ms.date 2026-02-26, commit d6ef15167b11…). The plan's
  `handle-transient-faults` (WAF design guide) has the same retry-testing guidance; the AAC page is pinned because it
  carries the `#test-your-retry-strategy-and-implementation` section. `review-reliability` pins the same AAC page
  under its own budget.
- New checks TST-12 (load and performance tests, Information) and TST-13 (resilience tests, Information). Testing grew
  from 11 to 13 checks; scores before and after aren't directly comparable (README).
- Anchors were taken from the heading text of the fetched pages (Learn heading slugs); confirm them against the HTML
  `id` values on the first refresh. `re-test#use-fault-injection-and-chaos-engineering` is confirmed by a link on the
  transient-faults page.
- `testInventory.signals` gained `loadTests` and `faultInjection` (compliance-inventory step 6), so a 12-file sample
  that drops these files doesn't hide them.

## Open items

- Plan §10 follow-ups (changes outside this skill): reviewed and closed by `docs/plan_localize-afterplanning-changes.md` on 2026-11-09 (see its Appendix A). Open hand-offs: none.
1. Run the plan §12 step 8 sample-repo reviews (three variants: C# Web API, Python package, Java Maven). Skipped by
   user decision on 2026-11-09.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken).

## Coverage map

Reason codes for "not localized":
- **CTX** — background, motivation, tutorial or sample-app walkthrough; no rule a repository can pass or fail.
- **ORG** — organizational or process practice; not visible in a repository.
- **GIT** — needs Git or CI history (not read by the reviewer).
- **OWN-<subject>** — owned by another subject skill (SL software lifecycle, DEP dependency management, SEC security
  skills, SQ software quality, PERF performance, REL reliability).
- **STYLE** — classicist/mockist style discussion; the skill stays neutral (plan DEC-13).
- **FU** — follow-up candidate (plan §14).

### martinfowler.com — ptp (`articles/practical-test-pyramid.html`)

| Heading (anchor) | Covered by / reason |
|---|---|
| The Importance of (Test) Automation (`TheImportanceOftestAutomation`) | MFT-01 |
| The Test Pyramid (`TheTestPyramid`) | MFT-02 |
| Tools and Libraries We'll Look at (`ToolsAndLibrariesWellLookAt`) | CTX |
| The Sample Application, Functionality, High-level Structure, Internal Architecture | CTX (the anemic-domain remark: OWN-SQ) |
| Unit tests (`UnitTests`) | MFT-03 |
| What's a Unit? (`WhatsAUnit`) | CTX (team agreement; TSR-01 makes classification deterministic) |
| Sociable and Solitary (`SociableAndSolitary`) | MFT-04 |
| Mocking and Stubbing (`MockingAndStubbing`) | MFT-05 |
| But I Really Need to Test This Private Method (`private-methods-sidebar`) | MFT-06 |
| What to Test? (`WhatToTest`) | MFT-07 |
| Test Structure (`TestStructure`) | MFT-08 |
| Specialised Test Helpers (`SpecialisedTestHelpers`), Implementing a Unit Test (`ImplementingAUnitTest`) | CTX |
| Integration Tests (`IntegrationTests`) | MFT-09 |
| Database Integration (`DatabaseIntegration`) | MFT-10 |
| Integration With Separate Services (`IntegrationWithSeparateServices`) | MFT-11 |
| Contract Tests (`ContractTests`), Consumer Test (our team), Provider Test (our team) | MFT-12 |
| Provider Test (the other team) (`ProviderTesttheOtherTeam`) | CTX (tutorial; intent covered by MFT-12) |
| UI Tests (`UiTests`) | MFT-14 |
| End-to-End Tests (`End-to-endTests`), REST API End-to-End Test (`RestApiEnd-to-endTest`) | MFT-13 |
| User Interface End-to-End Test (`UserInterfaceEnd-to-endTest`) | CTX (Selenium/headless details) |
| Acceptance Tests — Do Your Features Work Correctly? (`acceptance`) | MFT-15 |
| Exploratory Testing (`ExploratoryTesting`) | ORG (manual activity) |
| The Confusion About Testing Terminology (`TheConfusionAboutTestingTerminology`) | CTX (TSR-01) |
| Putting Tests Into Your Deployment Pipeline (`PuttingTestsIntoYourDeploymentPipeline`) | MFT-16 |
| Avoid Test Duplication (`AvoidTestDuplication`) | MFT-17 |
| Writing Clean Test Code (`WritingCleanTestCode`) | MFT-18 |
| Conclusion, Acknowledgements, Significant Revisions | CTX (the revision list is the pin) |

### martinfowler.com — tc (`bliki/TestCoverage.html`, no section anchors)

| Item | Covered by / reason |
|---|---|
| Coverage finds untested code; run it regularly | MFT-19 |
| Coverage targets invite gaming (assertion-free tests) | MFT-20 |
| Interpreting figures (low = trouble, ~100 % suspicious, upper 80s–90s typical) | MFT-21 |
| Long test changes for simple production changes signal test duplication | MFT-22 |
| "Sufficient when bugs rarely escape / developers aren't afraid to change code"; "little value to management" | ORG |
| Further Reading, Notes | CTX |

### martinfowler.com — nd (`articles/nonDeterminism.html`)

| Heading (anchor) | Covered by / reason |
|---|---|
| Why non-deterministic tests are a problem (`WhyNon-deterministicTestsAreAProblem`) | MFT-23 |
| Quarantine (`Quarantine`) | MFT-23 |
| Lack of Isolation (`LackOfIsolation`) | MFT-24, MFT-25 |
| Asynchronous Behavior (`AsynchronousBehavior`) | MFT-26, MFT-27 (completion callbacks for fire-and-forget providers: CTX) |
| Remote Services (`RemoteServices`) | MFT-28 |
| Time (`Time`) | MFT-29 (includes the regex build check; running tests around midnight/month-end: CTX) |
| Resource Leaks (`ResourceLeaks`) | MFT-30 |
| Smoke test to abort early | CTX |
| Footnotes, Acknowledgments | CTX |

### martinfowler.com — mas (`articles/mocksArentStubs.html`)

| Heading (anchor) | Covered by / reason |
|---|---|
| Regular Tests (`RegularTests`), Tests with Mock Objects (`TestsWithMockObjects`), Using EasyMock (`UsingEasymock`) | CTX |
| The Difference Between Mocks and Stubs (`TheDifferenceBetweenMocksAndStubs`) | MFT-31 |
| Classical and Mockist Testing (`ClassicalAndMockistTesting`) | MFT-32 |
| Choosing Between the Differences (`ChoosingBetweenTheDifferences`) | MFT-32 |
| Driving TDD (`DrivingTdd`), Fixture Setup (`FixtureSetup`), Test Isolation (`TestIsolation`), Design Style (`DesignStyle`) | STYLE |
| Coupling Tests to Implementations (`CouplingTestsToImplementations`) | MFT-33 |
| So should I be a classicist or a mockist? (`SoShouldIBeAClassicistOrAMockist`) | MFT-34 |
| Final Thoughts, Further Reading | CTX |

### martinfowler.com — ci (`articles/continuousIntegration.html`)

| Heading (anchor) | Covered by / reason |
|---|---|
| Building a Feature with Continuous Integration (`BuildingAFeatureWithContinuousIntegration`) | CTX |
| Practices of Continuous Integration (`PracticesOfContinuousIntegration`) | CTX (section intro) |
| Put everything in a version controlled mainline (`PutEverythingInAVersionControlledMainline`) | OWN-SL |
| Automate the Build (`AutomateTheBuild`) | OWN-SL (SL-01) |
| Make the Build Self-Testing (`MakeTheBuildSelf-testing`) | MFT-35, MFT-36 |
| Everyone Pushes Commits To the Mainline Every Day (`EveryonePushesCommitsToTheMainlineEveryDay`) | GIT / OWN-SL |
| Semi-Integration (`semi-integration`) | OWN-SL |
| Every Push to Mainline Should Trigger a Build (`EveryPushToMainlineShouldTriggerABuild`) | MFT-37 |
| Fix Broken Builds Immediately (`FixBrokenBuildsImmediately`) | GIT (team behavior; needs CI history) |
| Keep the Build Fast (`build-fast`) | MFT-38, MFT-40 ("check for dependency updates at least daily": OWN-DEP) |
| Hide Work-in-Progress (`HideWork-in-progress`) | OWN-SL |
| Test in a Clone of the Production Environment (`TestInACloneOfTheProductionEnvironment`) | MFT-39 |
| Infrastructure As Code (sidebar in the same section) | CTX |
| Everyone can see what's happening (`EveryoneCanSeeWhatsHappening`) | ORG |
| Automate Deployment (`AutomateDeployment`) | OWN-SL |
| Sidebars: Patterns for Managing Source Code Branches, Continuous Integration Certification, Continuous Delivery, Evolutionary Database Design | CTX |
| Styles of Integration (`StylesOfIntegration`) | CTX |
| Benefits of Continuous Integration (`BenefitsOfContinuousIntegration`): Reduced risk of delivery delays; Less time wasted in integration; Less Bugs; Enables Refactoring for sustained productivity; Release to Production is a business decision | CTX |
| When we should not use Continuous Integration (`WhenWeShouldNotUseContinuousIntegration`) | CTX |
| Introducing Continuous Integration (`introducing`) | ORG |
| Common Questions (`CommonQuestions`): Where did Continuous Integration come from? | CTX |
| What is the difference between Continuous Integration and Trunk-Based Development? (`trunk-based`) | OWN-SL |
| Can we run a CI Service on our feature branches? (`CanWeRunACiServiceOnOurFeatureBranches`) | OWN-SL |
| Can a team do both Continuous Integration and Feature Branching at the same time? (`both-ci-plus-fb`) | OWN-SL |
| What is the difference between Continuous Integration and Continuous Delivery? | CTX |
| How does Continuous Deployment fit in with all this? (`cont-deploy`) | OWN-SL |
| How do we do pull requests and code reviews? (`HowDoWeDoPullRequestsAndCodeReviews`) | OWN-SL |
| How do we handle databases? (`HowDoWeHandleDatabases`) | CTX |
| Final Thoughts, Further Reading, Acknowledgments | CTX |

### learn.microsoft.com — ut (`dotnet/core/testing/unit-testing-best-practices`)

| Heading | Covered by / reason |
|---|---|
| Benefits of unit testing (Less time performing functional tests, Protection against regression, Executable documentation, Less coupled code) | CTX (motivation) |
| Characteristics of good unit tests | MSU-01 (fast), MSU-02 (isolated), MSU-03 (repeatable), MSU-04 (self-checking); "Timely": ORG |
| Code coverage and code quality | MSU-05 |
| Unit testing terminology | MSU-06 |
| Best practices | CTX (section intro) |
| Avoid infrastructure dependencies | MSU-07 |
| Follow test naming standards | MSU-08 |
| Arrange your tests | MSU-09 |
| Write minimally passing tests | MSU-10 |
| Avoid magic strings | MSU-11 |
| Avoid coding logic in unit tests | MSU-12 |
| Use helper methods instead of Setup and Teardown | MSU-13 (xUnit/MSTest lifecycle notes: CTX, framework-specific) |
| Avoid multiple Act tasks | MSU-14 |
| Validate private methods with public methods | MSU-15 |
| Handle stub static references with seams | MSU-16 |
| Related links | CTX |

### Security pages — testing sentences only

| Sentence (anchor) | Covered by / reason |
|---|---|
| azc: "Create tests that validate that the permissions mapped out in the design phase are being correctly enforced" (`enforce-least-privileges`) | STS-02 |
| azc: role growth makes testing and auditing harder | CTX |
| azc: Create Unit and Integration Test Cases for Authorization Logic (section, incl. deny by default, safe termination, ABAC enforcement) | STS-01 |
| azc: not a substitute for dedicated security or penetration testing (WSTG 4.5) | FU (F-6) |
| azc: exceptions and authorization failures handled and tested (`exit-safely-when-authorization-checks-fail`) | STS-03 |
| azc: test configuration of third-party components | CTX (folded into STS-01's intent) |
| lcs `#verification`: logging works as specified | STS-04 |
| lcs `#verification`: events classified consistently; field names, types and lengths per an agreed standard | STS-04 |
| lcs `#verification`: logging enabled during security, fuzz, penetration and performance testing | OWN-SEC / OWN-PERF |
| lcs `#verification`: mechanisms not susceptible to injection | STS-04 |
| lcs `#verification`: no unwanted side effects when logging occurs | OWN-SEC |
| lcs `#verification`: effect of lost external network connectivity on logging | STS-05 |
| lcs `#verification`: logging can't deplete system resources (DoS) | OWN-SEC |
| lcs `#verification`: effect of logging failures (DB loss, no space, no write permission, logger errors) | STS-05 |
| lcs `#verification`: access controls on event log data | OWN-SEC |
| lcs `#verification`: log-driven actions against users can't cause DoS | OWN-SEC |
| lcs: logging level verified periodically | OWN-SEC |
| a01 `#how-to-prevent`: functional access control in unit and integration tests | STS-06 |
| a05 `#description`: automated testing including fuzzing of all inputs | STS-07 |
| a05: SAST/IAST sentence | OWN-SL (SL-11) / not visible (IAST) |
| A10:2025: stress, performance and penetration testing of the final system | stress/performance: AZT-01 (TST-12, F-1 adopted) / penetration: FU (F-6) |
| ssdf PW.8.1 | STS-08 (ex. 1 sandboxing policy, ex. 2 methods by stage: ORG) |
| ssdf PW.8.2 ex. 1 | STS-09 |
| ssdf PW.8.2 ex. 2 | STS-10 |
| ssdf PW.8.2 ex. 3 | STS-11 |
| ssdf PW.8.2 ex. 4 (production stack in test plans) | ORG |
| ssdf PW.8.2 ex. 5 | STS-12 |
| ssdf PW.8.2 ex. 6 (penetration testing) | FU (F-6) |
| ssdf PW.8.2 ex. 7, 8, 9 (root causes, wiki, design records) | ORG |
| sc `#fuzzing` | STS-13 |
| sc `#ci-tests` (remediation: checked-in scripts, CI on every pull request) | STS-14 (detection via forge check runs: GIT) |
| sc: SAST and every other check | OWN-SL / OWN-DEP |

### learn.microsoft.com — pe-test (`well-architected/performance-efficiency/performance-test`, PE:06)

| Heading (anchor) | Covered by / reason |
|---|---|
| Set measurable goals for your performance tests (`set-measurable-goals-for-your-performance-tests`) | AZT-02 (budgets per layer: ORG) |
| Start early and test continuously (`start-early-and-test-continuously`) | AZT-03 (local profiling: CTX) |
| Test under real-world conditions (`test-under-real-world-conditions`) | PARENT → subsections |
| Mirror your production environment (`mirror-your-production-environment`) | AZT-04 |
| Validate performance in production (`validate-performance-in-production`) | ORG (production test scheduling and progressive traffic aren't repo-visible) |
| Validate changes with hypothesis-driven experiments (`validate-changes-with-hypothesis-driven-experiments`) | ORG |
| Apply multiple performance test types (`apply-multiple-performance-test-types`) | AZT-01 |
| Use real-world usage patterns and data characteristics (`use-real-world-usage-patterns-and-data-characteristics`) | AZT-01 (real third-party calls under load: not localized, conflicts with TST-05 determinism for automated suites) |
| Use test results to guide design decisions (`use-test-results-to-guide-design-decisions`) | AZT-05 (business correlation: ORG) |
| Azure facilitation (`azure-facilitation`) | CTX (product names) |

### learn.microsoft.com — re-test (`well-architected/reliability/reliability-test`, RE:08)

| Heading (anchor) | Covered by / reason |
|---|---|
| Define reliability testing scope based on service types (`define-reliability-testing-scope-based-on-service-types`) | ORG |
| Test against your reliability targets end-to-end (`test-against-your-reliability-targets-end-to-end`) | ORG (needs stated SLO/RTO; DR owns RTO/RPO drills) |
| Build reliability scenarios from critical flows and failure modes (`build-reliability-scenarios-from-critical-flows-and-failure-modes`) | ORG (failure mode analysis) |
| Validate your fault-tolerance and recovery mechanisms (`validate-your-fault-tolerance-and-recovery-mechanisms`) | PARENT → subsections |
| Backup and restore (`backup-and-restore`) | OWN-DR (review-disaster-recovery DR-02) |
| Transient faults (`transient-faults`) | AZT-06 |
| Load and scaling response (`load-and-scaling-response`) | AZT-01 (scale-out/in behaviour: OWN-PERF/OWN-REL) |
| Dependency failures (`dependency-failures`) | AZT-08 |
| Self-preservation and recovery (`self-preservation-and-recovery`) | OWN-REL (runbooks: OWN-DR) |
| Incidents and disaster recovery (DR) (`incidents-and-disaster-recovery-dr`) | OWN-DR (DR-09); alert detection tests: review-monitoring |
| Test and assess your plan with tabletop exercises (`test-and-assess-your-plan-with-tabletop-exercises`) | ORG |
| Take advantage of planned and unplanned outages (`take-advantage-of-planned-and-unplanned-outages`) and subsections | ORG |
| Combine different types of tests (`combine-different-types-of-tests`) | AZT-09 |
| Use fault injection and chaos engineering (`use-fault-injection-and-chaos-engineering`) | AZT-09 |
| Azure facilitation (`azure-facilitation`) | CTX |

### learn.microsoft.com — bp-tf (`architecture/best-practices/transient-faults`)

Only the testing section is localized for this skill; the rest of the page is `review-reliability`'s (AZRL).

| Heading (anchor) | Covered by / reason |
|---|---|
| Test your retry strategy and implementation (`test-your-retry-strategy-and-implementation`) | AZT-07 (mocks, HTTP fault libraries), AZT-09 (fault injection in pipelines, high-load tests) |
| All other headings | OWN-REL |
