# PilotUtilityApi — Compliance Review Comparison

_Compares [`PilotUtilityApi-compliance-review-2026-09-26_2225.md`](PilotUtilityApi-compliance-review-2026-09-26_2225.md) (run `2026-09-26_2225-pilotutilityapi`) against [`PilotUtilityApi-compliance-review-2026-09-27_1246.md`](PilotUtilityApi-compliance-review-2026-09-27_1246.md) (run `2026-09-27_1246-pilotutilityapi`). Based solely on the two report documents — no source code or Git data was consulted._

## 1. Headline Numbers

| Metric | 09-26 2225 | 09-27 1246 | Δ |
|---|---|---|---|
| **Overall score** | 59.17/100 (Poor) | 59.91/100 (Poor) | +0.74 |
| Errors | 7 | 7 | 0 |
| Warnings | 13 | 24 | **+11** |
| Information | 6 | 7 | +1 |
| Total listed findings | 26 | 38 | +12 |
| Duplicate/suppressed findings | 5 | 3 | -2 |

The overall band is unchanged (**Poor**), and the total score barely moved, but that stability masks large, largely offsetting swings underneath: Application Design and Security improved sharply while Software Lifecycle, Implementation and Operations got materially worse, and the total number of reported Warnings nearly doubled.

## 2. Subject Score Comparison

| Subject | 09-26 2225 | 09-27 1246 | Δ | Direction |
|---|---|---|---|---|
| Software Quality | 74.19/100 (Fair) | 70.97/100 (Fair) | -3.22 | ▼ |
| Software Lifecycle | 13.33/100 (Poor) | **0.00/100 (Poor)** | -13.33 | ▼▼ |
| Application Design (Twelve-Factor) | 54.17/100 (Poor) | **73.08/100 (Fair)** | **+18.91** | ▲▲ |
| API Design | 79.17/100 (Good) | 79.17/100 (Good) | 0.00 | ▬ |
| Security | 43.14/100 (Poor) | 55.74/100 (Poor) | **+12.60** | ▲ |
| Implementation | 66.04/100 (Fair) | 56.86/100 (Poor) | -9.18 | ▼ |
| Operations | 75.00/100 (Good) | 69.57/100 (Fair) | -5.43 | ▼ |

Software Lifecycle moved from "Poor" into a hard 0, and Implementation crossed the Fair→Poor boundary in the wrong direction, while Application Design crossed Poor→Fair in the right direction.

## 3. Top 5 Risks — What Changed

| # | 09-26 2225 | 09-27 1246 |
|---|---|---|
| 1 | No authentication scheme registered | No authentication scheme registered *(same)* |
| 2 | No authorization on the testing-reset endpoint | No function-level access control (authorization) — same underlying gap, now framed separately from authentication |
| 3 | HTTPS redirection only in Development | HTTPS redirection only in Development *(same)* |
| 4 | No CI pipeline builds/tests the solution | No CI pipeline builds/tests the code *(same)* |
| 5 | No committed NuGet lock file | **New:** environment-specific backing-service config hardcoded in versioned appsettings files |

The lock-file risk (#5 in the first report) dropped out of the Top 5 entirely — `TF-02` flips from fail to pass in the second report (see §5) even though the corresponding Implementation check `DEP-02` still fails in both reports. A new API Design error (missing `AboutResponse` schema property) also enters the second report's "further errors" callout, replacing the first report's "400 response body doesn't match schema" error.

## 4. Things Done Well — Notable Differences

- The second report adds several new positive callouts not present in the first: immutable configuration singleton, one-directional project references, redaction of the `Password` field in `DataSourceConfiguration.ToString()`, a repo-root `.editorconfig`, structured Serilog logging, and README's Clean Architecture description.
- The first report's "Version is centrally declared and follows SemVer" callout (Software Lifecycle) is **dropped** in the second report — consistent with the new `SL-03` fail (conflicting version numbers, see §5).
- The first report's "OpenAPI 3.1 spec is generated and checked in" callout is **dropped**; the second report keeps only the versioning and XML-comment-transformer callouts for API Design.

## 5. Check-Level Flips Between Runs

Checks that changed result (`pass ↔ fail ↔ N/A`) between the two reports, by subject. Checks not listed were identical in both runs.

### Software Quality (net: more fails)

| Check | 09-26 2225 | 09-27 1246 | Note |
|---|---|---|---|
| SQ-02 | pass | **fail** | Nested try/catch/finally now flagged as excess branching |
| SQ-03 | pass | **fail** | Duplicated data-source switch/case now flagged |
| SQ-06 | fail | **pass** | Startup fatal-exception exit-code issue no longer flagged |
| SQ-07 | pass | **fail** | Namespace/folder naming mismatch now flagged |
| DP-04 | pass | **fail** | `BuildServiceProvider()` called before container finalized (ASP0000) now flagged |

### Software Lifecycle (net: all fail)

| Check | 09-26 2225 | 09-27 1246 | Note |
|---|---|---|---|
| SL-03 | pass | **fail** | New: `Directory.Build.props` (1.0.0) vs. README/appsettings (0.1.1) version mismatch |
| SL-05 | N/A | **fail** | No CI/CD pipeline exists to assess → now scored fail instead of N/A |

### Application Design / Twelve-Factor (net: more passes)

| Check | 09-26 2225 | 09-27 1246 | Note |
|---|---|---|---|
| TF-02 | **fail** | **pass** | First report: "no lock file found" → fail. Second report: "dependencies explicitly declared with centrally pinned exact versions" → pass. Same underlying fact (no lock file) is graded on a different criterion; the Implementation subject's `DEP-02` (lock file specifically) still fails in both reports. |
| TF-10 | fail (dup of SEC-WA-06) | **pass** | Duplicate-evidence fail no longer applied |
| TF-12 | pass | **N/A** | Re-scoped as "no admin/migration scripts present" instead of a pass |

### API Design (no score change, evidence changed)

| Check | 09-26 2225 | 09-27 1246 | Note |
|---|---|---|---|
| API-03 | fail — path + 400-body mismatch | fail — path mismatch + **`AboutResponse` schema omission** (new finding) | Same fail result, different underlying evidence |

### Security (net: more passes)

| Check | 09-26 2225 | 09-27 1246 | Note |
|---|---|---|---|
| SEC-II-01 | N/A | **pass** | The `show-details` parameter now credited for strong typing via model binding |
| SEC-OP-04 | N/A | **pass** | Logging now credited for parameterized message templates |
| SEC-OP-05 | fail (dup of TF-03) | **pass** | Re-assessed: committed password is "a literal placeholder, not a functional credential" |

### Implementation (net: more fails)

| Check | 09-26 2225 | 09-27 1246 | Note |
|---|---|---|---|
| CS-02 | fail | **pass** | `.editorconfig` now found/credited |
| CS-CS-02 | pass | **fail** | New: `var` used where type isn't apparent, contradicting the repo's own `.editorconfig` |
| TST-02 | pass | **fail** | New: coverage tool referenced but never configured/reported |
| TST-03 | pass | **fail** | New: Domain test project's only test is a non-asserting placeholder |
| DEP-06 | pass | **N/A** | Re-scoped: no SBOM/license inventory exists to cross-reference license compatibility |

### Operations (net: more fails, but also more passes)

| Check | 09-26 2225 | 09-27 1246 | Note |
|---|---|---|---|
| PERF-02 | pass | **fail** | New: synchronous `connection.Open()`/`Commit()`/`Rollback()` inside an async method |
| PERF-04 | N/A | **pass** | Re-scoped: single fixed query, no per-item loop, now credited |
| PERF-05 | fail (100% trace sampling) | **pass** | Re-scoped to "no hot loops with repeated expensive work"; the sampling concern moves out of scoring (still called out as an Information-level improvement in the first report only) |
| MAINT-02 | pass | **fail** | New: on-disk folder names (`PilotUtiltyApi.*`) don't match `.csproj`/namespace spelling or README's structure diagram |
| MAINT-04 | N/A | **pass** | Re-scoped: absence of TODO/FIXME/HACK markers now explicitly credited |

## 6. Findings That Appeared, Disappeared, or Changed Severity

**New in 09-27 1246 (not present in 09-26 2225):**
- No function-level access control / Zero Trust violation (Security) — elevated from being folded into the authorization finding to two distinct Error+Warning findings
- Two conflicting version numbers (Software Lifecycle)
- `BuildServiceProvider()` called before the container is finalized — DI anti-pattern (Software Quality / Design Patterns)
- Nested try/catch/finally branch-count issue (Software Quality)
- Duplicated data-source switch/case (Software Quality)
- Namespace/folder naming inconsistency for `AboutResponse` (Software Quality / Information)
- `var` usage contradicting `.editorconfig` (Implementation / Coding Standards)
- Coverage tool referenced but not configured/reported (Implementation / Testing)
- Placeholder non-asserting test in Domain test project (Implementation / Testing)
- No NuGet lock file — now a Warning under Implementation/Dependency Management (previously an Error under Application Design)
- Synchronous `Open()`/`Commit()`/`Rollback()` blocking calls in an async path (Operations / Performance)
- Folder names diverge from namespaces/README structure (Operations / Maintainability)
- `AboutResponse` schema omits a returnable property (API Design — new Error)
- Build provenance/signing/reproducible-build gap called out explicitly as Information (Software Lifecycle)

**Present in 09-26 2225 but no longer called out as a finding in 09-27 1246:**
- Fatal startup exceptions not exiting with a non-zero code (Software Quality) — check now passes
- No lock file, framed as Error under Application Design — demoted to a Warning under Implementation in the second report
- 400 response body not matching documented ProblemDetails schema (API Design) — replaced by the `AboutResponse` schema finding
- 100% trace sampling via `AlwaysOnSampler` (Operations, Information-level) — no longer mentioned

## 7. Consistency Observations

- **Same underlying fact, different verdicts:** the missing NuGet lock file is graded as a hard Application-Design **Error** in the first report (`TF-02` fail) but as a passing `TF-02` plus a separate, lower-severity Implementation **Warning** (`DEP-02` fail) in the second — the total signal is similar, but its subject placement and severity differ materially between runs.
- **Same underlying fact, opposite verdicts:** the appsettings-committed database password is scored as a failing, duplicate-flagged Security check (`SEC-OP-05` fail, "duplicate evidence of TF-03") in the first report, but as a passing Security check (`SEC-OP-05` pass, "literal placeholder, not a functional credential") in the second, even though `TF-03` itself fails in both reports for the same file.
- **Re-scoping from N/A to a definitive pass/fail** occurred repeatedly (`TF-12`, `SL-05`, `PERF-04`, `PERF-05`, `MAINT-04`, `SEC-II-01`, `SEC-OP-04`), which is the main driver of the large Warning-count increase — several checks that previously contributed no signal now contribute either a pass (raising a subject's score) or a fail (adding a new Warning finding).
- **Appendix note in the second report** states that its Software Quality, Software Lifecycle and Twelve-Factor sections (steps 10–12) were carried over unchanged from an earlier session on the same repo state, distinct from both this comparison's two runs' own inventory/analysis steps — meaning some of the score movement documented above may reflect a difference in reviewer judgment between sessions rather than a change in the underlying repository.

## 8. Run Metadata Differences

| | 09-26 2225 | 09-27 1246 |
|---|---|---|
| Git HEAD | `unavailable (user declined the read-only git rev-parse command)` | `null` (declined; repo confirmed as a git repo via `.git/`) |
| Analyzer approval | not approved ("files only") | none given |
| Subjects skipped | Disaster Recovery, Monitoring, Cost & Sustainability (no IaC found) | same three subjects, same reason |
| Resume behavior | full fresh run | resumed from step 13 (`review-api-design`) onward; steps 00–12 carried over from an earlier same-day session |
| Credits (manual addendum) | 331.1 | 306.6 |

## 9. Summary

The overall score is essentially flat, but this hides substantial churn: Application Design and Security both improved by re-scoping several previously N/A or duplicate-flagged checks into passes, while Software Lifecycle collapsed to zero on a new version-mismatch finding and a re-scored CI/CD check, and Implementation/Operations picked up several genuinely new findings (coverage gaps, a placeholder test, blocking sync calls in async code, naming inconsistencies, a DI anti-pattern). The two Application-Design/Security scoring reversals on the lock-file and placeholder-password findings, plus the note that early subjects in the second report were carried over from a separate session, suggest at least part of the movement reflects reviewer judgment variance rather than a change in the codebase itself.
