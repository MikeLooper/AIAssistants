# PilotUtilityApi — Compliance Review

_Generated 2026-09-26 22:35 · Run `2026-09-26_2225-pilotutilityapi`_

## 1. Summary

**Overall score: 59.17/100 — Poor**

| Subject | Score | Band |
|---------|-------|------|
| Software Quality | 74.19/100 | Fair |
| Software Lifecycle | 13.33/100 | Poor |
| Application Design (Twelve-Factor) | 54.17/100 | Poor |
| API Design | 79.17/100 | Good |
| Security | 43.14/100 | Poor |
| Implementation | 66.04/100 | Fair |
| Operations | 75.00/100 | Good |

**Findings by severity:** Error: 7 · Warning: 13 · Information: 6 (after cross-subject deduplication; 5 additional findings were suppressed as duplicate evidence of one of the 26 listed below)

### Top 5 Risks

1. **[Error] No authentication scheme is registered anywhere in the application** — Security (`src/PilotUtiltyApi.Web/Controllers/TestingController.cs`, `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`). Register an authentication scheme (e.g. JWT bearer or API key) and remove `[AllowAnonymous]` from state-changing endpoints. [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
2. **[Error] The destructive testing-data-reset endpoint has no authorization check** — Security (`src/PilotUtiltyApi.Web/Controllers/TestingController.cs`, lines 16-36). Require an authenticated caller with an explicit role/scope for `POST /v1/testing/reset`. [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
3. **[Error] HTTPS redirection is only enabled in Development** — Security (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 73-76). Call `UseHttpsRedirection()` unconditionally and add `UseHsts()` for non-development environments. [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
4. **[Error] No CI pipeline builds or tests the solution on push/PR** — Software Lifecycle (`.github/workflows/`, empty). Add a GitHub Actions workflow that runs `dotnet build` and `dotnet test` on every push/PR. [SLSA v1.0 build requirements](https://slsa.dev/spec/v1.0/requirements)
5. **[Error] No committed lock file for NuGet dependencies** — Application Design (`Directory.Packages.props`). Enable `RestorePackagesWithLockFile` and commit the generated `packages.lock.json` files. [Twelve-Factor App II. Dependencies](https://12factor.net/dependencies)

_Two further Error-severity findings exist (Program.cs's unhandled fatal-exception exit code, and the OpenAPI spec/implementation path mismatch) — see Recommended Improvements → Errors below. SEC-IA-01 is ranked first despite a Medium remediation effort because it is the root cause enabling SEC-IA-02 and the single highest real-world risk in this codebase._

## 2. Things Done Well

### Software Quality

- Clean layering: Web controllers call Services, Services call Repositories; no layer is skipped — `src/PilotUtiltyApi.Web/Controllers/TestingController.cs`
- Cross-cutting concerns (logging, OpenTelemetry, OpenAPI, error handling, versioning) are centralized in the Shared project rather than duplicated per module — `src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`
- Consistent, descriptive naming and thorough XML documentation comments throughout the reviewed files — `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`

### Software Lifecycle

- Version is centrally declared and follows SemVer (1.0.0) via `Directory.Build.props` — `Directory.Build.props`

### Application Design

- Backing services (SQL Server / PostgreSQL) are attached purely via configuration, with a single 'Active' flag switching providers without code changes — `src/PilotUtiltyApi.Web/appsettings.json`

### API Design

- An OpenAPI 3.1 spec is generated and checked in, backed by Scalar/Swashbuckle UI wiring in code — `docs/PilotUtilityApi_v1.json`
- The API is explicitly versioned via Asp.Versioning, with version-neutral system endpoints kept separate — `src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`

### Security

- Database access goes through Dapper's parameterized `CommandDefinition` with static, literal-only SQL scripts — no string concatenation of any input — `src/PilotUtiltyApi.Repositories/Constants/SqlConstants.cs`
- Error responses return a sanitized ProblemDetails message; no stack traces or internal details are leaked to the client — `src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs`
- Errors are logged with class/method context and a correlation ID before being translated to a safe user-facing message — `src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`
- A dedicated `UserException` type enforces that only pre-sanitized, user-safe messages ever reach the HTTP response — `src/PilotUtiltyApi.Shared/Exceptions/UserException.cs`

### Implementation

- Every public type/member across the reviewed files has XML documentation comments, and `GenerateDocumentationFile` is enabled — `src/PilotUtiltyApi.Shared/PilotUtilityApi.Shared.csproj`
- Nullable reference types are enabled solution-wide and used correctly — `Directory.Build.props`
- Tests mock only the true external boundaries (`ILoggerFactory`, `IApplicationConfiguration`) and assert concrete return values/messages — `test/PilotUtiltyApi.Repositories.Tests/Repositories/TestingRepositoryTests.cs`
- OpenTelemetry logging, metrics and tracing are all wired up with AspNetCore/HttpClient/SqlClient/Npgsql instrumentation and exported via OTLP — `src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs`
- A dedicated, version-neutral health check endpoint is exposed — `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`
- Every package version is centrally and exactly pinned via `Directory.Packages.props` (central package management); no floating/wildcard versions — `Directory.Packages.props`

### Operations

- All I/O-bound request-handling code is fully async with `CancellationToken` propagation — `src/PilotUtiltyApi.Web/Controllers/TestingController.cs`
- README.md documents prerequisites, build, run, configuration and project structure in detail, with a table of contents — `README.md`
- Folder boundaries map 1:1 to the Domain/Repositories/Services/Shared/Web architecture, both in code and in README's documented project structure — `README.md`

## 3. Recommended Improvements

### Errors

- **Fatal startup exceptions are logged but not surfaced via a non-zero process exit code** — Software Quality (`src/PilotUtiltyApi.Web/Program.cs`, lines 34-41). Set `Environment.Exit(1)` (or rethrow) in the catch block so orchestrators/process supervisors see the process as failed when startup throws. [ISO/IEC 25010 Reliability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#reliability)
- **No CI pipeline builds or tests the solution on push/PR** — Software Lifecycle (`.github/workflows/`, empty). Add a GitHub Actions workflow that runs `dotnet build` and `dotnet test` on every push and pull request. [SLSA v1.0 build requirements](https://slsa.dev/spec/v1.0/requirements)
- **No committed lock file for NuGet dependencies** — Application Design (`Directory.Packages.props`). Enable `<RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>` and commit the generated `packages.lock.json` files. [Twelve-Factor App II. Dependencies](https://12factor.net/dependencies)
- **OpenAPI spec's `/testing/reset` path omits the version segment the controller actually requires** — API Design (`docs/PilotUtilityApi_v1.json`, lines 78-79; `src/PilotUtiltyApi.Web/Controllers/TestingController.cs`, lines 16-17). Regenerate `docs/PilotUtilityApi_v1.json` from the running app (or add it to CI) so the documented path includes the required `v{version}` segment. [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- **No authentication scheme is registered anywhere in the application; every endpoint is explicitly anonymous** — Security (`src/PilotUtiltyApi.Web/Controllers/TestingController.cs`, line 19; `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`, line 18). Register an authentication scheme via `builder.Services.AddAuthentication(...)` and remove `[AllowAnonymous]` from state-changing endpoints. [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- **The destructive testing-data-reset endpoint has no authorization check** — Security (`src/PilotUtiltyApi.Web/Controllers/TestingController.cs`, lines 16-36). Require an authenticated caller with an explicit role/scope for `POST /v1/testing/reset`, since it deletes production-shaped data. [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- **HTTPS redirection is only enabled in Development; HTTP requests in other environments are never redirected or rejected** — Security (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 73-76). Call `UseHttpsRedirection()` unconditionally and add `UseHsts()` for non-development environments. [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

### Warnings

- **`TestingRepository.ResetTestingAsync` mixes connection selection, transaction control and error translation in one method** — Software Quality (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 55-130). Extract connection/transaction handling into a small helper so `ResetTestingAsync` only orchestrates the reset operation. [ISO/IEC 25010 Maintainability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability)
- **No documented branch protection or required-review policy found in the repo** — Software Lifecycle (`CONTRIBUTING.md`, lines 15-16). Document and enforce branch protection rules on the default branch. [NIST SP 800-218 (SSDF)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **No automated dependency update tool configured** — Software Lifecycle (`.github/`). Add a `.github/dependabot.yml` (or Renovate config). [NIST SP 800-218 (SSDF)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **Data source credentials live in tracked appsettings JSON files rather than environment/secret-store config** — Application Design (`src/PilotUtiltyApi.Web/appsettings.json`, lines 3-20; `src/PilotUtiltyApi.Web/appsettings.Development.json`, line 6). Remove the Password field from appsettings*.json entirely and source it from user-secrets locally and a vault/environment variable in deployed environments. [Twelve-Factor App III. Config](https://12factor.net/config)
- **Serilog writes application-managed rolling log files to a local logs/ folder in addition to stdout** — Application Design (`src/PilotUtiltyApi.Web/appsettings.json`, lines 28-37). Treat logs purely as an event stream to stdout/stderr and let the execution environment handle routing/retention. [Twelve-Factor App XI. Logs](https://12factor.net/logs)
- **Spec documents a ProblemDetails body for the 400 response, but the controller returns an empty BadRequest with only a custom header** — API Design (`src/PilotUtiltyApi.Web/Controllers/TestingController.cs`, lines 38-42). Return `BadRequest(new ProblemDetails { Detail = ... })` so the response body matches the documented schema. [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- **No security response headers (CSP, X-Content-Type-Options, X-Frame-Options, HSTS) are set anywhere in the pipeline** — Security (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 65-87). Add a middleware that sets these headers on every response. [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)
- **No vault/secret-manager integration is wired up for non-local environments** — Security (`src/PilotUtiltyApi.Web/PilotUtilityApi.Web.csproj`, line 6). Add an Azure Key Vault (or equivalent) configuration provider for staging/production. [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- **The `IDbConnection` created in `TestingRepository` is closed but never disposed via a using statement** — Implementation (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 78-118). Wrap the connection in a `using`/`await using` declaration instead of manually calling `Close()`. [C# Coding Conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **No integration test exercises the actual SQL execution success path** — Implementation (`test/PilotUtiltyApi.Repositories.Tests/Repositories/TestingRepositoryTests.cs`). Add an integration test (e.g. with Testcontainers) that runs `ResetTestingAsync` end-to-end. [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- **Error correlation IDs are freshly generated GUIDs, not tied to the OpenTelemetry trace/span ID already in use** — Implementation (`src/PilotUtiltyApi.Shared/Logging/Models/LoggingCorrelation.cs`, lines 13-16). Derive `CorrelationId` from `Activity.Current?.TraceId` instead of a new GUID. [OpenTelemetry](https://opentelemetry.io/docs/)
- **No retry-with-backoff policy wraps the database connection/query or the OTLP exporter calls** — Operations (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 78-100). Wrap the DB call with a Polly retry policy for transient errors. [Azure Well-Architected — Reliability](https://learn.microsoft.com/azure/well-architected/reliability/)
- **No circuit breaker protects calls to the database or the OpenTelemetry collector** — Operations (`src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs`, lines 51-60). Add a Polly circuit-breaker policy around the DB client. [Azure Well-Architected — Reliability](https://learn.microsoft.com/azure/well-architected/reliability/)

### Information

- **No `SECURITY.md` vulnerability-reporting policy** — Software Lifecycle. Add a `SECURITY.md`. [NIST SP 800-218 (SSDF)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **No CHANGELOG or release notes file** — Software Lifecycle. Maintain a `CHANGELOG.md`. [SemVer](https://semver.org/)
- **No `.editorconfig` or formatter/analyzer config found** — Implementation. Add a `.editorconfig` (and optionally `dotnet format` in CI). (fallback rubric)
- **No SLOs/SLIs are documented for the API** — Implementation. Document target latency/availability/error-rate SLOs in README.md or docs/. [Azure Well-Architected — Operational Excellence](https://learn.microsoft.com/azure/well-architected/operational-excellence/)
- **No SBOM or dependency license inventory is generated** — Implementation. Generate an SBOM once CI exists. (fallback rubric)
- **Tracing uses `AlwaysOnSampler`, exporting 100% of traces regardless of environment** — Operations (`src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs`, line 87). Consider a ratio-based sampler for production traffic once volume grows. [Azure Well-Architected — Performance Efficiency](https://learn.microsoft.com/azure/well-architected/performance-efficiency/)

## 4. Full Results

### Software Quality

| Check | Result | Evidence |
|-------|--------|----------|
| SQ-01 | fail | ResetTestingAsync mixes several responsibilities in one method |
| SQ-02 | pass | |
| SQ-03 | pass | |
| SQ-04 | pass | |
| SQ-05 | pass | |
| SQ-06 | fail | Program.cs swallows fatal startup exceptions without a non-zero exit code |
| SQ-07 | pass | |
| SQ-08 | pass | |
| DP-01 | pass | |
| DP-02 | pass | |
| DP-04 | pass | |
| DP-05 | pass | |
| DP-06 | N/A | no observer/event subscription patterns used |
| AP-01 | pass | |
| AP-02 | pass | |
| AP-03 | pass | |
| AP-04 | pass | |
| AP-05 | fail | duplicate evidence of REL-02#1, see Operations/Reliability |
| AP-06 | pass | |

### Software Lifecycle

| Check | Result | Evidence |
|-------|--------|----------|
| SL-01 | fail | .github/workflows is empty; no CI pipeline exists |
| SL-02 | fail | no documented tagging/publish/release process beyond the PR checklist |
| SL-03 | pass | |
| SL-04 | fail | two-reviewer rule documented but no enforced branch-protection settings visible |
| SL-05 | N/A | no build/release pipeline exists yet to assess |
| SL-06 | fail | no Dependabot/Renovate configuration found |
| SL-07 | fail | no SECURITY.md |
| SL-08 | fail | no CHANGELOG.md |

### Application Design (Twelve-Factor)

| Check | Result | Evidence |
|-------|--------|----------|
| TF-01 | pass | |
| TF-02 | fail | no packages.lock.json / nuget.config found anywhere |
| TF-03 | fail | connection credentials structured as JSON config fields committed to the repo |
| TF-04 | pass | |
| TF-05 | pass | |
| TF-06 | pass | |
| TF-07 | pass | |
| TF-08 | pass | |
| TF-09 | pass | |
| TF-10 | fail | duplicate evidence of SEC-WA-06#1, see Security/Web & API |
| TF-11 | fail | Serilog file sink manages its own rolling/retention instead of relying on stdout |
| TF-12 | pass | |

### API Design

| Check | Result | Evidence |
|-------|--------|----------|
| API-01 | pass | |
| API-02 | pass | visual inspection only; not run through a formal validator |
| API-03 | fail | documented /testing/reset path and 400 response body diverge from the actual versioned route/response |
| API-04 | pass | |
| API-05 | pass | |
| API-06 | N/A | no collection-returning endpoints exist |
| API-07 | pass | |
| API-08 | N/A | no collection-returning endpoints exist |

### Security

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-IA-01 | fail | no AddAuthentication/authentication middleware configured; both controllers [AllowAnonymous] |
| SEC-IA-02 | fail | no authorization policy guards the data-mutating reset endpoint |
| SEC-IA-03 | N/A | no JWTs issued or consumed |
| SEC-IA-04 | N/A | no OAuth2 flow implemented |
| SEC-IA-05 | N/A | no session cookies/server-side sessions used |
| SEC-IA-06 | N/A | app does not store end-user passwords |
| SEC-IA-07 | N/A | no custom cryptography/hashing code found |
| SEC-IA-08 | fail | no authentication at all means access relies on network-level trust |
| SEC-II-01 | N/A | only in-scope parameter is a trivial bool |
| SEC-II-02 | pass | |
| SEC-II-03 | pass | |
| SEC-II-04 | N/A | no shell/OS process execution code |
| SEC-II-05 | N/A | no XML parsing code |
| SEC-II-06 | N/A | no file upload endpoints |
| SEC-II-07 | N/A | no file upload endpoints |
| SEC-WA-01 | fail | no CSP header set anywhere |
| SEC-WA-02 | fail | no UseHsts() call and HTTPS redirection is dev-only |
| SEC-WA-03 | fail | no X-Content-Type-Options header set |
| SEC-WA-04 | fail | no X-Frame-Options/frame-ancestors protection set |
| SEC-WA-05 | N/A | no CORS middleware registered at all |
| SEC-WA-06 | fail | HTTPS enforced only in Development |
| SEC-WA-07 | pass | |
| SEC-OP-01 | pass | |
| SEC-OP-02 | pass | |
| SEC-OP-03 | pass | no evidence of secrets/PII in log messages |
| SEC-OP-04 | N/A | no user-controlled input currently logged |
| SEC-OP-05 | fail | duplicate evidence of TF-03#1, see Application Design/Twelve-Factor |
| SEC-OP-06 | fail | no vault/secret-manager provider configured beyond local user-secrets |
| SEC-OP-07 | pass | review prioritized auth, data access and error/secrets handling first |

### Implementation

| Check | Result | Evidence |
|-------|--------|----------|
| CS-01 | pass | |
| CS-02 | fail | no .editorconfig or enforced formatter config found |
| CS-03 | pass | |
| CS-04 | pass | |
| CS-05 | fail | see CS-CS-04 |
| CS-CS-01 | pass | |
| CS-CS-02 | pass | |
| CS-CS-03 | pass | |
| CS-CS-04 | fail | TestingRepository disposes its IDbConnection via manual Close() instead of using |
| CS-CS-05 | pass | |
| TST-01 | fail | every test project is unit-only; happy-path DB write untested at any level |
| TST-02 | pass | |
| TST-03 | pass | |
| TST-04 | pass | |
| TST-05 | pass | |
| TST-06 | fail | duplicate evidence of SL-01#1, see Software Lifecycle |
| OBS-01 | pass | |
| OBS-02 | fail | CorrelationId is a fresh GUID per error, unrelated to the OTel TraceId |
| OBS-03 | pass | |
| OBS-04 | pass | |
| OBS-05 | pass | |
| OBS-06 | pass | |
| OBS-07 | fail | no SLO/SLI documentation found |
| DEP-01 | pass | |
| DEP-02 | fail | duplicate evidence of TF-02#1, see Application Design/Twelve-Factor |
| DEP-03 | N/A | CLI analyzers not approved for this run; vulnerability status could not be verified |
| DEP-04 | pass | targets net10.0, a current LTS release under active support |
| DEP-05 | fail | no SBOM/license-inventory artifact found |
| DEP-06 | pass | MIT-licensed project; reviewed dependencies use permissive licenses |

### Operations

| Check | Result | Evidence |
|-------|--------|----------|
| REL-01 | pass | ConnectTimeout configured; drivers/OTLP exporter use provider-default timeouts |
| REL-02 | fail | no retry policy exists for DB or OTLP calls |
| REL-03 | N/A | no retry logic exists at all |
| REL-04 | fail | no circuit breaker exists for the DB or OTel collector dependency |
| REL-05 | N/A | no deployment/infrastructure configuration exists in this repository |
| PERF-01 | N/A | no expensive/repeated read operations found |
| PERF-02 | pass | |
| PERF-03 | pass | ADO.NET drivers use built-in connection pooling by default |
| PERF-04 | N/A | no loop-based/per-item data access code exists |
| PERF-05 | fail | 100% trace sampling configured with no environment-based override |
| DR-01 | N/A | no infrastructure-as-code found |
| DR-02 | N/A | no infrastructure-as-code found |
| DR-03 | N/A | no infrastructure-as-code found |
| DR-04 | N/A | no infrastructure-as-code found |
| DR-05 | N/A | no infrastructure-as-code found |
| MON-01 | N/A | no infrastructure-as-code found |
| MON-02 | N/A | no infrastructure-as-code found |
| COST-01 | N/A | no infrastructure-as-code found |
| COST-02 | N/A | no infrastructure-as-code found |
| COST-03 | N/A | no infrastructure-as-code found |
| COST-04 | N/A | no infrastructure-as-code found |
| MAINT-01 | pass | |
| MAINT-02 | pass | |
| MAINT-03 | pass | prerequisites/config documented in README, even though config is JSON-file based (see TF-03) |
| MAINT-04 | N/A | no TODO/FIXME/HACK markers found |
| MAINT-05 | pass | no deprecated/dead code paths found |

## 5. Appendix

- **Run:** `2026-09-26_2225-pilotutilityapi` · Target: `C:\Working\Storage\Dev\GitHub\PilotUtilityApi` · Git HEAD: `unavailable (user declined the read-only git rev-parse command)`
- **Started:** 2026-09-26T22:25:00-05:00 · **Completed:** 2026-09-26T23:35:00-05:00
- **Subjects skipped:** review-disaster-recovery, review-monitoring, review-cost-sustainability — all skipped because no infrastructure-as-code (`*.bicep`, `*.tf`, k8s/helm manifests, etc.) was found anywhere in the target repository
- **CLI analyzers:** not approved for this run (user selected "files only"); `DEP-03` (known-vulnerability check) is marked N/A as a result — re-run with analyzer approval for a complete dependency-vulnerability check
- **URLs fetched:** none — all citations came from the pre-approved allowlist without needing a live fetch
- **Link approvals:** none requested (no non-allowlisted URLs were needed)

## 6. Manual addendum

Model: Claude Sonnet 5
Credits: 331.1
