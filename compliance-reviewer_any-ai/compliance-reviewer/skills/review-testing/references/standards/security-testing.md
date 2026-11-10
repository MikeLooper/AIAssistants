# Security testing sources — localized summary (testing sentences only)

- Sources: four publishers, each counted against its own website budget (see the page-key table).
- Localized: 2026-11-09 (retrieved 2026-11-09) · Elements: 14 (cheatsheetseries.owasp.org 5, top10.owasp.org 2,
  nist.gov 5, github.com 2; cap 100 each)
- Source name for `Finding.standard`: **per row** (column "Source name"), e.g.
  `OWASP Authorization Cheat Sheet — STS-01`.
- Level: informational only; severity is the owning check's default.
- Scope: only the sentences about *testing*. The rest of these pages is owned by the security skills and
  `review-software-lifecycle`.
- Citation: `Finding.url` = the key's URL + `#` + primary anchor, e.g.
  `https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#verification` or
  `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf#page=24`.

| Key | URL | Website | Pin |
|-----|-----|---------|-----|
| azc | https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | cheatsheetseries.owasp.org | `OWASP/CheatSheetSeries` `cheatsheets/Authorization_Cheat_Sheet.md` @ cfd69aabc7e6 (2026-10-09) |
| lcs | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | cheatsheetseries.owasp.org | `OWASP/CheatSheetSeries` `cheatsheets/Logging_Cheat_Sheet.md` @ f1d0311aaada (2026-10-22) |
| a01 | https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/ | top10.owasp.org | OWASP Top 10:2025 (`OWASP/Top10` @ 3a31f35346c3, 2026-09-24) |
| a05 | https://top10.owasp.org/2025/A05_2025-Injection/ | top10.owasp.org | OWASP Top 10:2025 (`OWASP/Top10` @ 3a31f35346c3, 2026-09-24) |
| ssdf | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf | nist.gov | SP 800-218, SSDF Version 1.1, February 2022; PW.8 is on physical PDF page 24 |
| sc | https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md | github.com | OpenSSF Scorecard v5.6.0 (heading slugs `#fuzzing`, `#ci-tests`) |

| ID | Source name | Requirement (summary) | Applies when | Check | Anchor(s) |
|----|-------------|-----------------------|--------------|-------|-----------|
| STS-01 | OWASP Authorization Cheat Sheet | Authorization logic has automated unit and integration tests, covering deny-by-default, safe failure when a check fails, and attribute or relationship policies. | access control present | TST-10 | azc#create-unit-and-integration-test-cases-for-authorization-logic |
| STS-02 | OWASP Authorization Cheat Sheet | Tests confirm that the designed permissions (least privilege) are actually enforced. | access control present | TST-10 | azc#enforce-least-privileges |
| STS-03 | OWASP Authorization Cheat Sheet | The handling of exceptions and authorization failures is verified by tests. | access control present | TST-10 | azc#exit-safely-when-authorization-checks-fail |
| STS-04 | OWASP Logging Cheat Sheet | Logging is part of testing: it works as specified, events are classified consistently, and the logging mechanism resists injection. | security event logging present | TST-10 | lcs#verification |
| STS-05 | OWASP Logging Cheat Sheet | The application's behavior when logging fails (no space, lost connectivity, no write permission, logger errors) is tested. | security event logging present | TST-10 | lcs#verification |
| STS-06 | OWASP Top 10:2025 | Functional access control is included in unit and integration tests. | access control present | TST-10 | a01#how-to-prevent |
| STS-07 | OWASP Top 10:2025 | Injection flaws are detected by automated testing that includes fuzzing of inputs (parameters, headers, URL, cookies, JSON/XML). | untrusted input parsed | TST-11 | a05#description |
| STS-08 | NIST SSDF 1.1 | (PW.8.1) Which kinds of executable-code testing are used is a deliberate, documented choice, for vulnerabilities not found by review or static analysis. | untrusted input parsed | TST-11 | ssdf#page=24 |
| STS-09 | NIST SSDF 1.1 | (PW.8.2 ex. 1) Security features (authentication, authorization, validation, cryptographic use) have robust functional tests. | security features present | TST-10 | ssdf#page=24 |
| STS-10 | NIST SSDF 1.1 | (PW.8.2 ex. 2) Dynamic vulnerability testing is integrated into the automated test suite. | HTTP endpoints present | TST-11 | ssdf#page=24 |
| STS-11 | NIST SSDF 1.1 | (PW.8.2 ex. 3) Previously reported vulnerabilities have regression tests so they aren't reintroduced. | a fixed vulnerability is referenced (advisory, changelog, test name) | TST-10 | ssdf#page=24 |
| STS-12 | NIST SSDF 1.1 | (PW.8.2 ex. 5) Fuzz-testing tools are used to find input-handling issues. | untrusted input parsed | TST-11 | ssdf#page=24 |
| STS-13 | OpenSSF Scorecard | The project fuzzes: OSS-Fuzz or ClusterFuzzLite integration, or fuzz or property-based test functions in a supported language. | untrusted input parsed | TST-11 | sc#fuzzing |
| STS-14 | OpenSSF Scorecard | Checked-in scripts run all of the repository's tests, and a CI platform runs them on every pull request. | CI config present | TST-06 | sc#ci-tests |
