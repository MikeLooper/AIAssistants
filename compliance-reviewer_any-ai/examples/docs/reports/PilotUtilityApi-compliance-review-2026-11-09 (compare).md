# PilotUtilityApi — Compliance Review Comparison (Claude vs Copilot)

_Compared 2026-11-09 · Reports compared:_

- **Claude:** [PilotUtilityApi-compliance-review-2026-11-09_2044 (claude).md](<PilotUtilityApi-compliance-review-2026-11-09_2044 (claude).md>), run `2026-11-09_2035-PilotUtilityApi`
- **Copilot:** [PilotUtilityApi-compliance-review-2026-11-09_2123 (copilot).md](<PilotUtilityApi-compliance-review-2026-11-09_2123 (copilot).md>), run `2026-11-09_2123-PilotUtilityApi`

## At a glance

| | Claude (20:44) | Copilot (21:23) |
|---|---|---|
| Overall score | **54.55 — Poor** | **53.36 — Poor** |
| Findings (Error / Warning / Info) | 18 / 30 / 15 = 63 | 20 / 30 / 13 = 63 |
| Run time | about 9 min | about 18 min |
| Target, Git HEAD, flags | same (`59fedaa`, advanced off) | same |

## Differences

### 1. Copilot groups the subjects differently, so the score tables don't line up

- Copilot gave **"Security / Identity & Access"** its own row, scoring **0.00**, separate from **"Security"** at 51.39. Claude has one Security row at 62.16. The finding schema's example uses `subject: "Security"` with `subSubject: "Identity & Access"` ([finding-schema.md](../../compliance-reviewer/skills/compliance-review-core/references/finding-schema.md)). Claude follows that example. Copilot's labels produce a doubled heading: "Security / Identity & Access / Identity & Access".
- Copilot uses "Operations / Reliability" and "Operations / Performance" where Claude uses "Reliability" and "Operations".
- Many category names also differ, for example "Spec ↔ Implementation" vs "OpenAPI Specification", "Docs in Sync" vs "Docs Accuracy", and "Workflow Security" vs "Pipeline Hardening".
- **What this means:** subject and category labels aren't fixed anywhere, so the two tools fill them in differently. That makes reports hard to compare automatically. The fix would be to pin the labels, for example in the orchestrator's subject table or each checklist, and have `validate` check them.

### 2. Subject scores that differ

| Subject | Claude | Copilot | Why |
|---|---|---|---|
| Software Quality | 61.29 | 70.97 | Claude fails SQ-01 (long `ResetTestingAsync`) and SQ-05; Copilot passes both |
| Security | 62.16 | 0.00 (Identity & Access) + 51.39 | Copilot fails 8 more checks (see section 3) |
| Testing | 48.00 | 68.00 | Claude fails TST-07, TST-08 and TST-10; Copilot passes all three |
| Implementation | 50.00 | 64.29 | Claude fails DEP-08 (no `nuget.config`); Copilot passes it |

The other subjects score the same in both reports:

| Subject | Score |
|---|---|
| Software Lifecycle | 65.00 |
| Twelve-Factor | 90.91 |
| API Design | 29.27 |
| Observability | 56.25 |
| Reliability | 45.45 |
| Operations / Performance | 60.00 |
| Maintainability | 9.09 |

### 3. Check results that differ

| Check | Claude | Copilot |
|---|---|---|
| SQ-01 | fail (long method, SQR-02) | pass |
| SQ-05 | fail (duplicate of SEC-IA-02) | pass |
| SEC-WA-01, -04, -11 | N/A (API-only) | fail (Copilot found the Swagger UI and Scalar HTML pages, so browser headers apply) |
| SEC-WA-02 | pass | fail (no HSTS) |
| SEC-OP-06 | pass | fail (`TrustServerCertificate=True`) |
| SEC-OP-08 | pass | fail (duplicate of SQ-06) |
| SEC-OP-10 | N/A | fail (duplicate of CS-05) |
| TST-07 | fail (no acceptance tests; the Bruno collection has no assertions) | pass |
| TST-08 | fail (copied arrange blocks, misleading test name) | pass, and Copilot lists test naming as a strength |
| TST-10 | fail (no test for a generic error response) | pass |
| DEP-08 | fail (no `nuget.config` with `<clear/>`) | pass |

Some checks fail in both reports but point at different evidence:

| Check | Claude's evidence | Copilot's evidence |
|---|---|---|
| CS-01 | Folder names, and a namespace that doesn't match its folder | `RetrieveResponse` used for a delete result, and folder spelling |
| CS-05 | Nullable warnings downgraded; `var` used against the convention | `using` missing for disposables; nullable warnings downgraded; private field naming |
| SEC-WA-08 | Duplicate of SEC-IA-01 | No `Cache-Control: no-store` or `frame-ancestors` |
| SEC-OP-05 | Duplicate of SL-11 (SAST) | No secret scanning in CI |
| SEC-OP-07 | Duplicate of SEC-IA-02 | Duplicate of API-03 |
| TST-11 | Duplicate of SL-11 | Duplicate of SEC-OP-05 |
| OBS-02 | Duplicate of API-15 (no `x-ms-request-id`) | The error correlation ID is a random GUID that isn't tied to the trace ID (WAFO-05) |
| OBS-08 | `service.version` comes from config (OTO-32) | Duplicate of MAINT-09 (version mismatch in the docs) |
| REL-04 | Duplicate of SEC-IA-01, which looks wrong | A real circuit-breaker finding (AZRL-21) |
| PERF-02/03 | Duplicate of CS-05#2 (`var`) | Duplicate of CS-05#1 (`using` and disposal), which fits better |
| MAINT-03 | MR-14 and MR-16 | Duplicate of API-11, which looks wrong |

### 4. Findings in only one report

**Only Claude:**

- Long method `ResetTestingAsync` (SQR-02)
- `var` used against the convention in `.editorconfig` (MSC-12)
- No `nuget.config` or package source mapping (OCS-13)
- No acceptance tests (MFT-15), and no test that errors come back generic (TSR-22)
- Copied test arrange blocks (TSR-17) and a misleading test name (MSU-08)
- `/about` exposes data anonymously, as a health-endpoint issue (WAFO-37)
- `service.version` comes from config instead of the build (OTO-32)
- OpenTelemetry config keys aren't documented (MR-14)
- Runtime log files are committed in the source tree (MR-11)

**Only Copilot:**

- `TrustServerCertificate=True` while sending database credentials (SMG-11, **Error**)
- Reset failures return 400 when they should return 5xx (AZ-031, Error)
- `using` isn't used for the connection and transaction, and the transaction is never disposed (MSC-16)
- Private field naming isn't documented (MSC-03)
- No HSTS (HDR-07)
- No frame protection on the Swagger and Scalar pages (HDR-01)
- No secret scanning in CI (SMG-05)
- The base `appsettings.json` holds development values (SCR-02)
- No circuit breaker (AZRL-21)
- The correlation GUID isn't linked to the trace (WAFO-05)
- Doc versions disagree with the project: 0.1.1 and 1.0.0 vs 1.0.1 (MR-35)
- Folder names don't match project names (MR-07)
- No `Cache-Control: no-store` on responses (RST-07)

### 5. Severity and Top 5

- **HTTPS enforced only in Development** is a Warning in Claude's report and an **Error** in Copilot's.
- **Top 5 risks:** 3 are the same (OAS-40, OAS-41, AZ-044). Claude adds AZ-017 and AZ-088. Copilot adds OAS-38 and OAS-39.
- Neither report puts the anonymous destructive reset endpoint in its Top 5, even though both rate it an Error.

## Similarities

- **Same verdict.** Both score the target Poor, about 54, with the same weak spots: API Design (29.27), Maintainability (9.09) and Reliability (45.45).
- **API Design.** Every check result matches, and both report the same core errors:
  - spec drift: the reset route, `show-details`, `AboutResponse`, and undocumented 500 responses
  - POST returning 204
  - the non-standard error body, and no `x-ms-error-code`
  - the version in the path, numeric versions, and `api-version` not required and falling back silently
  - a kebab-case query parameter
  - null fields, and `deployDate` not RFC 3339
  - no request ID
- **Security basics.** Both report:
  - no authentication or deny-by-default
  - an anonymous destructive reset
  - `/about` details exposed anonymously
  - HTTPS redirect only in Development
  - Swagger exposed in production

  Both list the same strengths: constant SQL, no CORS, redacted passwords, generic ProblemDetails and bounded log files.
- **Lifecycle and Twelve-Factor.** These match nearly finding for finding: no CODEOWNERS, no `permissions:` block, actions pinned to tags instead of SHAs, no SAST, no TreatWarningsAsErrors, no SECURITY.md, and a File sink in the production config.
- **Testing, Observability and Maintainability.** Both report:
  - coverage is never collected
  - an `Assert.Pass` placeholder test
  - no integration tests against a real database
  - no load tests
  - a constant-200 health check
  - a hard-coded OTLP scheme
  - no SLOs
  - no global.json
  - no database retry
  - README path and port errors
  - a broken CONTRIBUTING anchor
  - no CHANGELOG or ADRs
- **N/A handling.** Both mark Disaster Recovery, Monitoring and Cost & Sustainability as N/A because advanced usage was off. Neither fetched any URLs.

## Takeaway

The two runs agree on the main result and on most of the API, CI and docs findings. They differ mostly in how deeply they reviewed Security and Testing.

- Copilot went deeper on transport and header security. Its `TrustServerCertificate` finding is a real one that Claude missed.
- Claude was stricter on testing and code structure.
- The subject-label mismatch is a gap in the reviewer itself, not in either run. Fixing it would make these comparisons much easier.
