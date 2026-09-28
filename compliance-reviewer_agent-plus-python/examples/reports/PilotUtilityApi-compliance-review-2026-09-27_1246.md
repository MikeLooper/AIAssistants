# PilotUtilityApi — Compliance Review

_Generated 2026-09-27 14:35 · Run `2026-09-27_1246-pilotutilityapi`_

## 1. Summary

**Overall score: 59.91/100 — Poor**

| Subject | Score | Band |
|---------|-------|------|
| Software Quality | 70.97/100 | Fair |
| Software Lifecycle | 0.00/100 | Poor |
| Application Design (Twelve-Factor) | 73.08/100 | Fair |
| API Design | 79.17/100 | Good |
| Security | 55.74/100 | Poor |
| Implementation | 56.86/100 | Poor |
| Operations | 69.57/100 | Fair |

**Findings by severity:** Error: 7 · Warning: 24 · Information: 7 (after cross-subject deduplication; 3 additional findings were suppressed as duplicate evidence of one of the 38 listed below)

### Top 5 Risks

1. **[Error] No authentication is registered anywhere in the app; a destructive endpoint is fully anonymous** — Security (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, `src/PilotUtiltyApi.Web/Controllers/TestingController.cs`). Register an authentication scheme (e.g. JWT bearer or the org's identity provider) and remove `[AllowAnonymous]` from `TestingController`. [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
2. **[Error] No function-level access control distinguishes sensitive actions from public ones** — Security (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`). Add `services.AddAuthorization()`/`UseAuthorization()` and apply `[Authorize]` to state-changing actions. [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
3. **[Error] HTTPS redirection is only enabled in Development, not Production** — Security (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 73-76). Call `UseHttpsRedirection()` unconditionally and add `UseHsts()` for non-development environments. [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#always-use-tls)
4. **[Error] No CI pipeline builds or tests the code on push/PR** — Software Lifecycle (`.github/workflows/`, empty). Add a GitHub Actions workflow that runs `dotnet restore`, `dotnet build` and `dotnet test` on every push/PR. [SLSA v1.0 build requirements](https://slsa.dev/spec/v1.0/requirements)
5. **[Error] Environment-specific backing-service config is hardcoded in versioned appsettings files instead of environment variables** — Application Design (`src/PilotUtiltyApi.Web/appsettings.json`, `src/PilotUtiltyApi.Web/appsettings.Development.json`). Remove real/placeholder host, port, username and password values from appsettings*.json and source them via environment variables, `dotnet user-secrets`, or a secret store. [Twelve-Factor App III. Config](https://12factor.net/config)

_Two further Error-severity findings exist (an OpenAPI spec/implementation path mismatch and a missing response-schema property) — see Recommended Improvements → Errors below. The three security Errors are ranked ahead of the CI and config-secrets Errors because an unauthenticated, unauthorized, HTTP-reachable destructive endpoint is the single highest real-world risk in this codebase; the appsettings values flagged in Top Risk 5 are currently only placeholders, not live credentials._

## 2. Things Done Well

### Software Quality

- Errors are consistently logged with a correlation id and never silently swallowed — `src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, `src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs`
- Application configuration singleton is immutable, read-only startup data — not shared mutable per-request state — `src/PilotUtiltyApi.Services/Extensions/ServicesInjectionExtensions.cs`
- Clean, one-directional layering: Web → Services/Domain/Shared, Services → Repositories/Domain/Shared, with no project referencing back up the stack — `src/PilotUtiltyApi.Web/PilotUtilityApi.Web.csproj`
- Cross-cutting concerns (versioning, logging, OpenTelemetry, unhandled-exception handling) are centralized in shared extension methods/middleware rather than duplicated per controller — `src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`

### Software Lifecycle

- `CONTRIBUTING.md` documents a PR process and explicitly references SemVer — `CONTRIBUTING.md`
- Central Package Management gives a single, auditable source of truth for dependency versions — `Directory.Packages.props`

### Application Design (Twelve-Factor)

- Single solution/repo tracks the whole app across all layers — `PilotUtilityApi.sln`
- Dependencies explicitly declared with centrally pinned exact versions — `Directory.Packages.props`
- Backing data sources are attached as swappable config-bound resources, not hardwired in code — `src/PilotUtiltyApi.Services/Extensions/ServicesInjectionExtensions.cs`

### API Design

- Explicit, multi-source API versioning with a sensible default (header/query/URL-segment readers) — `src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`
- OpenAPI operations are enriched from XML doc comments via a custom transformer — `src/PilotUtiltyApi.Shared/OpenApi/Transformers/ManualXmlCommentsOperationTransformer.cs`

### Security

- Database access goes through Dapper's parameterized `CommandDefinition`, never raw string-built SQL — `src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, `src/PilotUtiltyApi.Repositories/Constants/SqlConstants.cs`
- The one externally supplied value in scope is bound and type-checked via ASP.NET model binding rather than read as raw text — `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`
- Global exception handling returns a generic, correlation-ID-based message without stack traces or internal details — `src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs`
- Unhandled and repository-level exceptions are logged internally with full exception detail and a correlation ID before a sanitized message reaches the client — `src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`
- `DataSourceConfiguration.ToString()` explicitly redacts the Password field before any diagnostic string conversion — `src/PilotUtiltyApi.Shared/Configuration/Models/DataSourceConfiguration.cs`

### Implementation

- Every public type and member sampled across all five projects has XML documentation comments, with `GenerateDocumentationFile` enabled in every csproj — `src/PilotUtiltyApi.Web/Controllers/TestingController.cs`
- A repo-root `.editorconfig` enforces consistent tab indentation, brace style and dotnet/C# code-style rules across all projects — `.editorconfig`
- Nullable reference types are enabled solution-wide and used correctly — `Directory.Build.props`
- async/await is used consistently end-to-end (controller → service → repository) with no `.Result`/`.Wait()` blocking calls found in sampled files — `src/PilotUtiltyApi.Services/Services/TestingService.cs`
- Mocking is scoped to direct collaborators only, not internal logic — `test/PilotUtiltyApi.Services.Tests/Services/TestingServiceTests.cs`
- Tests are independent with no shared mutable state between cases — `test/PilotUtiltyApi.TestingShared/Base/TestBase.cs`
- Structured logging via Serilog with a compact-JSON file sink and message-template log calls — `src/PilotUtiltyApi.Web/appsettings.json`
- Distributed tracing and metrics are instrumented across HTTP, SQL Server and PostgreSQL call boundaries via the OpenTelemetry SDK, exported via OTLP — `src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs`
- A health check endpoint exists and is anonymously reachable — `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`
- Central Package Management pins every dependency to an exact version with no floating/wildcard overrides — `Directory.Packages.props`

### Operations

- Per-data-source connect timeout is explicitly configurable rather than hardcoded — `src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`
- DB connections rely on driver-managed connection pooling rather than an explicit anti-pattern — `src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`
- README provides thorough setup, configuration, run and test instructions — `README.md`
- Clear Clean Architecture layering with consistent, single-direction dependencies — `README.md`
- No TODO/FIXME/HACK markers accumulating in `src/`

## 3. Recommended Improvements

### Errors

- **No authentication is registered anywhere in the app; a destructive endpoint is fully anonymous** — Security / Identity & Access (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 105-128; `src/PilotUtiltyApi.Web/Controllers/TestingController.cs`, lines 15-51). Register an authentication scheme (e.g. JWT bearer or the org's identity provider) via `services.AddAuthentication(...)`, call `app.UseAuthentication()`/`UseAuthorization()` in the request pipeline, and remove `[AllowAnonymous]` from `TestingController` (or restrict it to an authenticated/internal-only policy) so the state-changing `/reset` action cannot be invoked by an unauthenticated caller. [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- **No function-level access control distinguishes sensitive actions from public ones** — Security / Identity & Access (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 65-87; `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`, lines 16-19). Add `services.AddAuthorization()` and `app.UseAuthorization()` to the pipeline, define policies/roles, and apply `[Authorize]` with the appropriate policy to state-changing actions so every sensitive action is checked server-side. [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- **HTTPS redirection is only enabled in Development, not Production** — Security / Web & API (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 73-76). Call `webApp.UseHttpsRedirection()` unconditionally (or at least in Production), not only when `IsDevelopment()` is true. [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#always-use-tls)
- **No CI pipeline builds or tests the code on push/PR** — Software Lifecycle (`.github/workflows/`, empty). Add a GitHub Actions workflow (e.g. `.github/workflows/ci.yml`) that runs `dotnet restore`, `dotnet build`, and `dotnet test` on every push and pull request targeting main. [SLSA Build Requirements](https://slsa.dev/spec/v1.0/requirements)
- **Environment-specific backing-service config is hardcoded in versioned appsettings files instead of environment variables** — Application Design / Twelve-Factor (`src/PilotUtiltyApi.Web/appsettings.json`, lines 4-15; `src/PilotUtiltyApi.Web/appsettings.Development.json`, lines 4-14). Remove real/placeholder host, port, username and password values from appsettings*.json and supply the actual per-deploy values via environment variables, `dotnet user-secrets` in dev, or a secret store (e.g. Azure Key Vault) in higher environments. [Twelve-Factor App III. Config](https://12factor.net/config)
- **Generated OpenAPI spec omits the version segment for TestingController's route** — API Design (`src/PilotUtiltyApi.Web/Controllers/TestingController.cs`, lines 15-46; `docs/PilotUtilityApi_v1.json`, lines 81-83). Regenerate the OpenAPI snapshot so paths reflect the actual versioned route (e.g. `/v1/testing/reset`), or confirm the version-substitution option is actually honored by the OpenAPI document generator for attribute-routed, `Asp.Versioning`-based controllers. [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- **AboutResponse schema omits the ApplicationConfiguration property that the endpoint can return** — API Design (`src/PilotUtiltyApi.Domain/Models/Responses/AboutResponse.cs`, lines 17-21; `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`, lines 81-88; `docs/PilotUtilityApi_v1.json`, lines 151-179). Expose the property via a concrete DTO/class (or an explicit schema transformer) so `GET /about?show-details=true` responses are fully documented instead of silently diverging from the published schema. [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)

### Warnings

- **`ResetTestingAsync` mixes multiple responsibilities in one method** — Software Quality (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 57-133). Extract connection/transaction lifecycle management into a small private helper or a using-based unit-of-work. [ISO/IEC 25010 Maintainability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability)
- **Nested try/catch/finally with multiple branch points increases cyclomatic complexity** — Software Quality (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 61-132). Flatten the nested try/catch by wrapping connection/transaction/command in `using`/`await using` declarations. [ISO/IEC 25010 Maintainability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability)
- **Data-source-type switch/case structure is duplicated across three private methods** — Software Quality (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 144-206). Consolidate the repeated switch into a single per-provider abstraction so adding a third database only touches one place. [ISO/IEC 25010 Maintainability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability)
- **Temporary service provider built before the container is finalized (DI anti-pattern)** — Software Quality / Design Patterns (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 122-126). Avoid calling `builder.Services.BuildServiceProvider()` before `WebApplicationBuilder.Build()`; read config directly from `builder.Configuration` instead. (fallback rubric)
- **No documented release process (tagging, changelog, publish step)** — Software Lifecycle (`CONTRIBUTING.md`, lines 1-5). Document a concrete release process: tagging, CHANGELOG updates, and artifact publishing. [Semantic Versioning](https://semver.org/)
- **Two conflicting version numbers for the same product with no single source of truth** — Software Lifecycle (`Directory.Build.props`, line 3; `README.md`, line 183). Pick a single version source of truth and bump it meaningfully with each release. [Semantic Versioning Specification](https://semver.org/#semantic-versioning-specification-semver)
- **Branching/review model is only partially documented and not technically enforced** — Software Lifecycle (`CONTRIBUTING.md`, lines 15-16). Name the branching model, add a CODEOWNERS file, and configure branch protection rules. [NIST SP 800-218 (SSDF)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **No automated or scheduled dependency updates** — Software Lifecycle (`Directory.Packages.props`, lines 1-5). Add a Dependabot or Renovate configuration for NuGet. [NIST SP 800-218 (SSDF)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **Serilog File sink manages log rotation/retention itself instead of treating logs as an event stream** — Application Design / Twelve-Factor (`src/PilotUtiltyApi.Web/appsettings.json`, lines 59-69). Write logs only to stdout and let the execution environment handle routing, rotation, and retention. [Twelve-Factor App XI. Logs](https://12factor.net/logs)
- **Zero Trust violation: every reviewed endpoint implicitly trusts any network caller** — Security / Identity & Access (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 65-87; `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`, lines 60-87). Require an authenticated/authorized caller identity for every endpoint, and gate the `showDetails=true` branch of `/about` behind a least-privilege policy. [OWASP Zero Trust Architecture Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Zero_Trust_Architecture_Cheat_Sheet.html)
- **No Content-Security-Policy header is configured** — Security / Web & API (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 66-86). Add a `Content-Security-Policy` response header, avoiding `unsafe-inline`/`unsafe-eval`. [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- **No Strict-Transport-Security (HSTS) header is configured** — Security / Web & API (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 66-86). Call `webApp.UseHsts()` for non-Development environments. [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#http-strict-transport-security)
- **No X-Content-Type-Options: nosniff header is configured** — Security / Web & API (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 66-86). Add `X-Content-Type-Options: nosniff` to every response via a small response-header middleware. [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-content-type-options)
- **No clickjacking protection header (X-Frame-Options / frame-ancestors) is configured** — Security / Web & API (`src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs`, lines 66-86). Set `X-Frame-Options: DENY` (or `SAMEORIGIN`) or a `frame-ancestors` CSP directive. [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-frame-options)
- **The IDbConnection and IDbTransaction created in TestingRepository are never wrapped in using/await using** — Implementation / Coding Standards (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 73-115). Wrap `connection` and `transaction` in `using`/`await using` declarations instead of manually calling `Close()` in a `finally` block. [C# Coding Conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **No integration/E2E tests exist; the DB-touching success path in TestingRepository is entirely untested** — Implementation / Testing (`test/PilotUtiltyApi.Repositories.Tests/Repositories/TestingRepositoryTests.cs`; `src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 61-105). Add a thin integration test layer (e.g. Testcontainers-backed SQL Server/PostgreSQL) that exercises the real `ResetTestingAsync` happy path. [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- **Coverage tool is referenced but never configured with a threshold or reported anywhere** — Implementation / Testing (`Directory.Packages.props`, line 7; `.github/workflows/`, empty). Add a coverage collection step, a minimum threshold, and publish/report the result in CI. [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- **Placeholder test asserts nothing meaningful** — Implementation / Testing (`test/PilotUtiltyApi.Domain.Tests/ExampleTest.cs`, lines 8-15). Replace the scaffold-generated example test with real tests for Domain classes. [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- **Correlation/trace IDs are not propagated into structured logs across the request lifecycle** — Implementation / Observability (`src/PilotUtiltyApi.Web/appsettings.json`, lines 70-76; `src/PilotUtiltyApi.Shared/Logging/Models/LoggingCorrelation.cs`, lines 13-16). Enrich Serilog output with the active OpenTelemetry trace/span IDs so every log line carries the same correlation identifier as the corresponding distributed trace. [OpenTelemetry log correlation](https://opentelemetry.io/docs/concepts/signals/traces/#log-correlation)
- **No NuGet lock file is generated or committed for any project** — Implementation / Dependency Management (`Directory.Build.props`; `Directory.Packages.props`). Set `<RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>` and commit the generated `packages.lock.json` files. (fallback rubric)
- **No retry-with-backoff policy wraps the database connection/query or the OTLP exporter calls** — Operations / Reliability (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 73-89; `src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs`, lines 58-62). Wrap the DB connection open/query call with a Polly retry policy for transient errors. [Azure Well-Architected — Reliability](https://learn.microsoft.com/azure/well-architected/reliability/)
- **No circuit breaker protects calls to the database or the OpenTelemetry collector** — Operations / Reliability (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 73-89; `src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs`, lines 58-62). Add a Polly circuit-breaker policy around the DB client. [Azure Well-Architected — Reliability](https://learn.microsoft.com/azure/well-architected/reliability/)
- **Synchronous connection.Open()/transaction.Commit()/Rollback() calls block the thread inside an otherwise async request path** — Operations / Performance (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 73-98). Use `await connection.OpenAsync(cancellationToken)` and `BeginTransactionAsync`/`CommitAsync`/`RollbackAsync`. [Azure Well-Architected — Performance Efficiency](https://learn.microsoft.com/azure/well-architected/performance-efficiency/)
- **Folder/project names diverge from namespaces and from the README's documented structure** — Operations / Maintainability (`README.md`, lines 47-54; `src/PilotUtiltyApi.Web/Program.cs`, lines 1-3). Rename the `PilotUtiltyApi.*` folders (and update project references) to match the correct `PilotUtilityApi.*` namespace spelling. (fallback rubric)

### Information

- **Namespace/folder naming is inconsistent for the Domain response model** — Software Quality (`src/PilotUtiltyApi.Domain/Models/Responses/AboutResponse.cs`, lines 1-4). Rename the namespace to match the physical folder, and align project folder names with namespace spelling. [ISO/IEC 25010 Maintainability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability)
- **No build provenance, signing, or reproducible-build process** — Software Lifecycle (`.github/workflows/`, empty). Once a CI pipeline exists, generate build provenance and sign published artifacts. [SLSA Build Requirements](https://slsa.dev/spec/v1.0/requirements)
- **No SECURITY.md vulnerability-reporting policy** — Software Lifecycle. Add a `SECURITY.md` describing how to privately report vulnerabilities. [NIST SP 800-218 (SSDF)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **No CHANGELOG or release notes** — Software Lifecycle. Add a `CHANGELOG.md` and update it with each release. [Semantic Versioning](https://semver.org/)
- **`var` is used extensively where the type is not apparent, contrary to the repo's own .editorconfig settings** — Implementation / Coding Standards (`src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs`, lines 73-79; `src/PilotUtiltyApi.Web/Controllers/SystemController.cs`, lines 68-76). Use explicit types for locals whose type isn't obvious, or relax the .editorconfig rules to match actual practice. [C# Coding Conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions#implicitly-typed-local-variables)
- **No SLOs or SLIs are documented anywhere in the repository** — Implementation / Observability (`README.md`, lines 5-19). Document target SLIs/SLOs (p95/p99 latency, error rate, availability) referencing the metrics already exported via OpenTelemetry. [Azure Well-Architected — Operational Excellence](https://learn.microsoft.com/azure/well-architected/operational-excellence/)
- **No SBOM or license inventory is present in the repository** — Implementation / Dependency Management (`Directory.Packages.props`, lines 1-35). Generate a CycloneDX or SPDX SBOM as part of CI and publish it as a build artifact. (fallback rubric)

## 4. Full Results

### Software Quality

| Check | Result | Evidence |
|-------|--------|----------|
| SQ-01 | fail | ResetTestingAsync combines data-source lookup, connection lifecycle, transaction management and SQL execution in one method |
| SQ-02 | fail | Nested try/catch/finally in ResetTestingAsync raises branch count beyond a single-purpose method |
| SQ-03 | fail | The sqlserver/postgresql switch is repeated near-identically in three private methods of TestingRepository |
| SQ-04 | pass | Controllers, services, repositories and extension classes each have a single, clearly named responsibility |
| SQ-05 | pass | Parameter lists are short; related configuration is grouped into config objects |
| SQ-06 | pass | Exceptions are caught, logged with a correlation id, and re-thrown/converted; nothing is silently swallowed |
| SQ-07 | fail | AboutResponse's namespace (Dto) doesn't match its folder (Responses); project folders are misspelled vs namespaces |
| SQ-08 | pass | No commented-out code blocks or obviously dead code found |
| DP-01 | pass | The only singleton in scope holds immutable startup configuration, not per-request mutable state |
| DP-02 | pass | Classes use composition and interfaces rather than deep inheritance chains |
| DP-04 | fail | ApiExtensions builds a second, throwaway IServiceProvider before the real container is built (ASP0000 anti-pattern) |
| DP-05 | pass | Simple internal factory methods construct provider-specific objects |
| DP-06 | N/A | No observer/event subscription pattern is present in any file in scope |
| AP-01 | pass | Web project references only Domain, Services and Shared — never Repositories |
| AP-02 | pass | Controllers only bind input, call an abstraction, and shape the HTTP response |
| AP-03 | pass | Project reference graph is acyclic |
| AP-04 | pass | Each project groups a single concern, giving high cohesion per module |
| AP-05 | fail | duplicate evidence of REL-02#1, see Operations / Reliability |
| AP-06 | pass | Versioning, logging, OpenTelemetry and error handling are centralized in shared extensions/middleware |

### Software Lifecycle

| Check | Result | Evidence |
|-------|--------|----------|
| SL-01 | fail | .github/workflows/ is empty and no other CI configuration was found anywhere in the repository |
| SL-02 | fail | No CHANGELOG, no git tags, and no documented tagging/publish step |
| SL-03 | fail | Directory.Build.props sets Version 1.0.0 while README/appsettings advertises 0.1.1 |
| SL-04 | fail | CONTRIBUTING.md states a two-reviewer policy but no branching model or CODEOWNERS/branch-protection exists |
| SL-05 | fail | No CI/CD pipeline exists to produce build provenance, signing, or reproducible builds |
| SL-06 | fail | No dependabot.yml, renovate.json, or equivalent scheduled-update configuration found |
| SL-07 | fail | No SECURITY.md file exists at the repository root |
| SL-08 | fail | No CHANGELOG* file exists at the repository root |

### Application Design (Twelve-Factor)

| Check | Result | Evidence |
|-------|--------|----------|
| TF-01 | pass | Single solution/repo tracks the whole app across all layers |
| TF-02 | pass | Dependencies explicitly declared with centrally pinned exact versions |
| TF-03 | fail | Host, port, username and password fields for both data sources are literal values committed in appsettings*.json |
| TF-04 | pass | Backing data sources are attached as swappable config-bound resources, not hardwired in code |
| TF-05 | pass | .NET SDK inherently separates build/release/run stages; CI/CD specifics covered under Software Lifecycle |
| TF-06 | pass | (per skill checklist, no failing evidence found) |
| TF-07 | pass | (per skill checklist, no failing evidence found) |
| TF-08 | pass | No in-process state or anti-patterns blocking horizontal scale-out were found |
| TF-09 | pass | (per skill checklist, no failing evidence found) |
| TF-10 | pass | (per skill checklist, no failing evidence found) |
| TF-11 | fail | Serilog is configured with a File sink performing rolling-interval and retention-count log management |
| TF-12 | N/A | No one-off admin/migration process scripts or tooling are present among the files in scope |

### API Design

| Check | Result | Evidence |
|-------|--------|----------|
| API-01 | pass | docs/PilotUtilityApi_v1.json exists and is generated per API version |
| API-02 | pass | The spec is well-formed JSON, declares openapi 3.1.1, with valid info/servers/paths/components |
| API-03 | fail | TestingController's versioned route is not reflected in the spec's path; AboutResponse schema omits a conditional property |
| API-04 | pass | Utility endpoints are version-neutral via [ApiVersionNeutral]; versioned controllers follow naming convention |
| API-05 | pass | Endpoints return 200/204/400 as appropriate; client-error handling produces a consistent ProblemDetails shape |
| API-06 | N/A | No collection-returning endpoints are present in the files in scope |
| API-07 | pass | Explicit versioning is configured via Asp.Versioning with header/query/URL-segment readers and a default version |
| API-08 | N/A | No collection endpoints are present to support field selection/filtering |

### Security

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-IA-01 | fail | No AddAuthentication/UseAuthentication is registered anywhere; TestingController.ResetTesting carries [AllowAnonymous] |
| SEC-IA-02 | fail | No AddAuthorization/UseAuthorization or [Authorize] policy exists; both controllers carry blanket [AllowAnonymous] |
| SEC-IA-03 | N/A | No JWT issuance or validation code exists in the files in scope |
| SEC-IA-04 | N/A | No OAuth2 client or server flow code is present in the files in scope |
| SEC-IA-05 | N/A | No session or cookie-based authentication is used; the API is stateless |
| SEC-IA-06 | N/A | No password or credential storage code exists in the files in scope |
| SEC-IA-07 | N/A | No custom cryptography or credential hashing code exists in the files in scope |
| SEC-IA-08 | fail | No pipeline-level authentication/authorization exists; /about can disclose full config to any anonymous caller |
| SEC-II-01 | pass | The only external input (show-details) is strongly typed via [FromQuery]/[BindRequired] model binding |
| SEC-II-02 | pass | TestingRepository executes only fixed SQL constants; no external value is concatenated into SQL text |
| SEC-II-03 | pass | Data access uses Dapper's parameterized CommandDefinition/QueryFirstOrDefaultAsync |
| SEC-II-04 | N/A | No shell/OS process execution exists in the files in scope |
| SEC-II-05 | N/A | None of the files in scope perform XML parsing |
| SEC-II-06 | N/A | None of the files in scope implement file upload handling |
| SEC-II-07 | N/A | No file upload/storage code exists in the files in scope |
| SEC-WA-01 | fail | No Content-Security-Policy header is configured anywhere in the middleware pipeline |
| SEC-WA-02 | fail | No UseHsts() call or Strict-Transport-Security header found |
| SEC-WA-03 | fail | No X-Content-Type-Options: nosniff header is set anywhere in the pipeline |
| SEC-WA-04 | fail | No X-Frame-Options header or frame-ancestors CSP directive is configured |
| SEC-WA-05 | N/A | No CORS middleware is registered anywhere in the reviewed pipeline |
| SEC-WA-06 | fail | UseHttpsRedirection() is gated behind IsDevelopment(), so HTTPS is not enforced in Production |
| SEC-WA-07 | pass | Global exception handler returns generic ProblemDetails with a correlation ID; no internal details exposed |
| SEC-OP-01 | pass | Global exception middleware returns generic, correlation-ID-based error responses |
| SEC-OP-02 | pass | Unhandled and repository-level exceptions are logged internally with full detail before a sanitized message reaches the client |
| SEC-OP-03 | pass | DataSourceConfiguration.ToString() explicitly redacts the Password field |
| SEC-OP-04 | pass | Logging uses parameterized message templates, not string-concatenated user input |
| SEC-OP-05 | pass | The committed Password value is a literal placeholder string, not a functional credential |
| SEC-OP-06 | fail | duplicate evidence of TF-03#1, see Application Design / Twelve-Factor |
| SEC-OP-07 | pass | Review prioritized exception-handling middleware, logging config, secrets-bearing appsettings, and the DB connection-string builder |

### Implementation

| Check | Result | Evidence |
|-------|--------|----------|
| CS-01 | pass | (per skill checklist, no failing evidence found) |
| CS-02 | pass | (per skill checklist, no failing evidence found) |
| CS-03 | pass | (per skill checklist, no failing evidence found) |
| CS-04 | pass | (per skill checklist, no failing evidence found) |
| CS-05 | fail | See var-usage inconsistency (CS-CS-02) and undisposed IDbConnection/IDbTransaction (CS-CS-04) |
| CS-CS-01 | pass | (per skill checklist, no failing evidence found) |
| CS-CS-02 | fail | var is used where the type is not apparent, contrary to the repo's own .editorconfig settings |
| CS-CS-03 | pass | (per skill checklist, no failing evidence found) |
| CS-CS-04 | fail | TestingRepository creates an IDbConnection/IDbTransaction never wrapped in using/await using |
| CS-CS-05 | pass | (per skill checklist, no failing evidence found) |
| TST-01 | fail | All existing tests are mocked unit tests; no integration/E2E test exercises the real DB transaction/commit path |
| TST-02 | fail | coverlet.collector is referenced but no threshold/runsettings/report step exists, and no CI runs it |
| TST-03 | fail | The Domain test project's only test is a non-asserting Assert.Pass placeholder |
| TST-04 | pass | Mocks are limited to the direct dependency being isolated, verified with explicit call-count checks |
| TST-05 | pass | TestBase carries no shared state; each test constructs its own local mocks/fixtures |
| TST-06 | fail | duplicate evidence of SL-01#1, see Software Lifecycle |
| OBS-01 | pass | Structured logging via Serilog with message-template log calls |
| OBS-02 | fail | Serilog enrichers do not attach the OpenTelemetry trace/span ID to log events |
| OBS-03 | pass | Distributed tracing instrumented across HTTP, SQL Server and PostgreSQL boundaries via OpenTelemetry SDK |
| OBS-04 | pass | ASP.NET Core, HttpClient and database metrics are collected via OpenTelemetry instrumentation |
| OBS-05 | pass | Logs, metrics and traces are exported via OTLP/HTTP to a collector, not just the local console |
| OBS-06 | pass | A health check endpoint exists and is anonymously reachable |
| OBS-07 | fail | No SLO/SLI documentation found in docs/, README.md or elsewhere |
| DEP-01 | pass | Central Package Management with every dependency pinned to an exact version |
| DEP-02 | fail | No packages.lock.json files exist and no project sets RestorePackagesWithLockFile |
| DEP-03 | N/A | No analyzer approval was given for this run; no vulnerability scan was run |
| DEP-04 | pass | All projects target net10.0, a currently supported .NET release |
| DEP-05 | fail | No SBOM or license inventory file was found anywhere in the repository |
| DEP-06 | N/A | No license inventory or SBOM exists to cross-reference dependency license compatibility |

### Operations

| Check | Result | Evidence |
|-------|--------|----------|
| REL-01 | pass | A ConnectTimeout is explicitly configured per data source for both SqlServer and PostgreSQL connection strings |
| REL-02 | fail | No retry policy exists for the DB open/query in TestingRepository or for the OTLP exporter calls |
| REL-03 | N/A | No retry logic exists anywhere in the files reviewed |
| REL-04 | fail | No circuit breaker (Polly or equivalent) wraps calls to the database or the OpenTelemetry collector |
| REL-05 | N/A | No IaC or deployment manifests exist anywhere in the target repository to assess replica/instance count |
| PERF-01 | N/A | In-scope code implements a data-reset write action, not a repeated/expensive read; no cacheable pattern exists |
| PERF-02 | fail | connection.Open() and transaction.Commit()/Rollback() are synchronous blocking calls inside an async method |
| PERF-03 | pass | CreateConnection builds a new connection per call with no Pooling=false override; default driver pooling applies |
| PERF-04 | pass | A single QueryFirstOrDefaultAsync call is issued against a fixed reset script; no per-row/per-item query loop |
| PERF-05 | pass | No hot loops with repeated expensive work were found |
| DR-01 to DR-05 | N/A | No infrastructure-as-code found anywhere in the target repo |
| MON-01 to MON-02 | N/A | No infrastructure-as-code found; health checks/SLOs covered under Observability (OBS-06/OBS-07) |
| COST-01 to COST-04 | N/A | No infrastructure-as-code found anywhere in the target repo |
| MAINT-01 | pass | README includes Table of Contents, Prerequisites, Building/Running, Configuration, API Endpoints, Testing and Architecture sections |
| MAINT-02 | fail | On-disk folder names (PilotUtiltyApi.*) don't match .csproj file names, C# namespaces, or the README's own Project Structure diagram |
| MAINT-03 | pass | Prerequisites and local-development user-secrets setup are documented; no unexplained environment variables found |
| MAINT-04 | pass | No TODO/FIXME/HACK/XXX markers found under src/** |
| MAINT-05 | pass | No [Obsolete] attributes or 'deprecated' markers found under src/**; no dead/duplicated legacy code paths observed |

## 5. Appendix

- **Run:** `2026-09-27_1246-pilotutilityapi` · Target: `C:\Working\Storage\Dev\GitHub\PilotUtilityApi` · Git HEAD: `null` (target git HEAD unavailable — user declined the git shell command for this run; repo confirmed to be a git repo via presence of `.git/`)
- **Started:** 2026-09-27T12:46:00-05:00 · **Completed:** 2026-09-27T14:35:00-05:00
- **Subjects skipped:** Disaster Recovery, Monitoring, Cost & Sustainability — no infrastructure-as-code found anywhere in the target repo (`iacFound: false` in `01-inventory.json`)
- **Analyzers:** skipped — no CLI analyzer approval was given for this run (`analyzerApproval: "none"`)
- **URLs fetched:** none (all subject reviews relied on each skill's checklist plus citations to the approved-sources allowlist without needing to fetch)
- **Link approvals:** none requested this run
- **Note:** This run (`2026-09-27_1246-pilotutilityapi`) was resumed by request from step 13 (review-api-design) onward; steps 00-init, 01-inventory, 02-analyzers (skipped), 10-review-software-quality, 11-review-software-lifecycle and 12-review-twelve-factor were completed in an earlier session on the same repo state and are included in this report's scoring and findings unchanged. A separate, stale prior run (`transitions/2026-09-26_2225-pilotutilityapi/`) was not resumed or touched.

## 6. Manual addendum

Model: Claude Sonnet 5
Credits: 306.6
