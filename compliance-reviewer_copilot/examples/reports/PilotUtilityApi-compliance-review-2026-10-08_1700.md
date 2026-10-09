# PilotUtilityApi — Compliance Review

_Generated 2026-10-08T17:30:24-06:00 · Run `2026-10-08_1700-PilotUtilityApi`_

## 1. Summary

**Overall score: 60.92/100 — Fair**

| Subject | Score | Band |
|---------|-------|------|
| Software Quality | 62.22/100 | Fair |
| Software Lifecycle | 12.50/100 | Poor |
| Twelve-Factor App | 90.91/100 | Excellent |
| API Design | 37.50/100 | Poor |
| Security | 63.77/100 | Fair |
| Testing | 53.33/100 | Poor |
| Observability | 75.00/100 | Good |
| Implementation | 75.00/100 | Good |
| Operations | 62.50/100 | Fair |
| Maintainability | 85.71/100 | Good |

**Findings by severity:** Error: 8 · Warning: 14 · Information: 8

### Top 5 Risks

1. **[Error] No CI pipeline builds and tests changes automatically** — Software Lifecycle / CI/CD (CONTRIBUTING.md). Add a CI workflow (e.g. .github/workflows/ci.yml) that runs dotnet restore/build/test on every push and pull request, and make it a required status check before merge. [SLSA v1.0 requirements](https://slsa.dev/spec/v1.0/requirements)
1. **[Error] No authorization on sensitive actions: anonymous POST /reset deletes data and anonymous /about?show-details=true returns configuration** — Security / Identity & Access (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more)). Protect reset with [Authorize] using a role/policy (and disable it outside test environments); require authorization for /about show-details, keeping only /healthcheck anonymous. [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
1. **[Error] No CI workflow runs the test suite on every change** — Testing / Test Automation (.github/instructions/unit-tests.instructions.md). Add a CI workflow that runs 'dotnet test' (with coverlet collection) on every push and pull request, and make it a required check. [The Practical Test Pyramid (Martin Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html#the-deployment-pipeline)
1. **[Error] No server-side authentication: pipeline has no UseAuthentication/AddAuthentication and the destructive reset endpoint is explicitly [AllowAnonymous]** — Security / Identity & Access (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more)). Register authentication (e.g. JWT bearer/OIDC via a vetted IdP), call UseAuthentication/UseAuthorization, and apply a fallback policy requiring authenticated users; allow anonymous only on healthcheck. [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
1. **[Error] Checked-in OpenAPI spec is out of sync with the implemented routes and DTOs** — API Design / OpenAPI Spec (docs/PilotUtilityApi_v1.json (+2 more)). Regenerate docs/PilotUtilityApi_v1.json from the running app (or in CI) and fail the build on drift. The current file omits the v1 path prefix, the required flag on show-details, the AboutResponse.applicationConfiguration property, and the configured info title, version and contact. [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)

## 2. Things Done Well

### Software Quality

- [Coding Standards] Consistent XML documentation on public types, constructors and members across layers — src/PilotUtiltyApi.Services/Services/TestingService.cs
- [Architecture Patterns] Clean Controller -> Service -> Repository layering with interface-based DI; controllers do not touch the database — src/PilotUtiltyApi.Web/Controllers/TestingController.cs
- [Architecture Patterns] Centralized exception handling middleware with correlation ids and user-safe messages — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs

### Software Lifecycle

- [Versioning] Single central SemVer-style version, and SemVer is the documented scheme — Directory.Build.props

### Twelve-Factor App

- [Dependencies] Dependencies explicitly declared with central package management and pinned versions — Directory.Packages.props
- [Config] Configuration is bound from IConfiguration (env-overridable) and validated at startup — src/PilotUtiltyApi.Shared/Configuration/ApplicationConfiguration.cs
- [Disposability] Fail-fast startup and logs flushed on shutdown via host lifetime — src/PilotUtiltyApi.Web/Program.cs

### API Design

- [OpenAPI Spec] OpenAPI 3.1 spec is generated, checked in and served with a UI — src/PilotUtiltyApi.Shared/OpenApi/Extensions/OpenApiExtensions.cs
- [Versioning] Explicit API versioning with a default version and a per-version OpenAPI document — src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs
- [Status Codes & Errors] Actions declare their response types and status codes with ProducesResponseType — src/PilotUtiltyApi.Web/Controllers/TestingController.cs

### Security

- [Input & Injection] SQL is a compile-time constant executed through Dapper CommandDefinition; no user input reaches SQL text — src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs
- [Input & Injection] Only external input is a strongly typed, required bool query parameter; the data-changing endpoint takes no input — src/PilotUtiltyApi.Web/Controllers/SystemController.cs
- [Web & API] Global exception middleware returns generic ProblemDetails and logs details server-side — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs
- [Web & API] No CORS policy is registered, so no wildcard-with-credentials exposure exists — src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs
- [Operational] Global exception middleware logs the exception and returns a generic message with a correlation ID — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs
- [Operational] Password is redacted in ToString() and can be suppressed when configuration is copied — src/PilotUtiltyApi.Shared/Configuration/Models/DataSourceConfiguration.cs
- [Operational] Committed config contains only placeholder passwords and runtime log files are git-ignored — src/PilotUtiltyApi.Web/appsettings.json

### Testing

- [Test Pyramid] Per-project fast unit test suites mirror the source layout, with a single lightweight Bruno E2E smoke test — test/PilotUtiltyApi.Services.Tests/Services/TestingServiceTests.cs
- [Coverage] coverlet.collector is configured in the test project — test/PilotUtiltyApi.Web.Tests/PilotUtilityApi.Web.Tests.csproj
- [Test Quality] Configuration validation tests assert specific exception types and messages across edge cases — test/PilotUtiltyApi.Shared.Tests/Configuration/ApplicationConfigurationTests.cs

### Observability

- [Observability] Serilog structured logging with compact JSON file sink, message templates and enrichers — src/PilotUtiltyApi.Web/appsettings.json
- [Observability] OpenTelemetry tracing instrumented for ASP.NET Core, HttpClient, Npgsql and SqlClient — src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs
- [Observability] Logs, metrics and traces exported via OTLP to a collector; console exporter limited to Development — src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs

### Implementation

- [Dependency Management] Central package management with exact pinned versions; no floating versions — Directory.Packages.props
- [Dependency Management] All projects target net10.0 (LTS) from a single shared setting — Directory.Build.props

### Operations

- [Reliability] Connection timeout is configurable per data source (30s) and the request CancellationToken is propagated to the database command — src/PilotUtiltyApi.Web/appsettings.json
- [Performance] Async/await and CancellationToken propagated from controller through service to Dapper command — src/PilotUtiltyApi.Web/Controllers/TestingController.cs
- [Performance] Entire reset is a single batched SQL script per call, avoiding per-table round trips — src/PilotUtiltyApi.Repositories/Constants/SqlConstants.cs

### Maintainability

- [Maintainability] README covers prerequisites, build, run, configuration, test commands and architecture layers — README.md
- [Maintainability] Clear layered structure (Domain/Repositories/Services/Shared/Web) with documented dependency rules and written architecture instructions — .github/instructions/architecture.instructions.md
- [Maintainability] Configuration properties, defaults and local User Secrets example are documented; CONTRIBUTING requires README updates — README.md

## 3. Recommended Improvements

### Errors

- **No CI pipeline builds and tests changes automatically** — Software Lifecycle / CI/CD (CONTRIBUTING.md, lines 8-18). Add a CI workflow (e.g. .github/workflows/ci.yml) that runs dotnet restore/build/test on every push and pull request, and make it a required status check before merge. [SLSA v1.0 requirements](https://slsa.dev/spec/v1.0/requirements)
- **Checked-in OpenAPI spec is out of sync with the implemented routes and DTOs** — API Design / OpenAPI Spec (docs/PilotUtilityApi_v1.json (+2 more), lines 83-85). Regenerate docs/PilotUtilityApi_v1.json from the running app (or in CI) and fail the build on drift. The current file omits the v1 path prefix, the required flag on show-details, the AboutResponse.applicationConfiguration property, and the configured info title, version and contact. [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- **Inconsistent URL versioning and an RPC-style action route** — API Design / URL Structure & Versioning (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs (+2 more), lines 31-34). Choose one versioning mechanism, and a single URL convention for all endpoints. Model reset as a resource or a documented custom action (e.g. POST /v1/testing:reset) instead of an ad-hoc verb route. Alternatively, document the system endpoints as deliberately unversioned. [Microsoft Azure REST API Guidelines - URL structure / versioning](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#url-structure)
- **Reset endpoint returns an empty 400 with the error in a Warning header, and has an inconsistent success shape** — API Design / Status Codes & Errors (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 55-58). Return a structured error body (ProblemDetails or the Azure error object) with a status that matches the failure, such as 500 for service or database faults and 4xx only for client errors. Do not put the error message in the Warning header. Use one consistent success shape, e.g. 200 with a JSON object holding the count. [Microsoft Azure REST API Guidelines - HTTP status codes / error response](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#http-status-codes)
- **No server-side authentication: pipeline has no UseAuthentication/AddAuthentication and the destructive reset endpoint is explicitly [AllowAnonymous]** — Security / Identity & Access (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 15-18). Register authentication (e.g. JWT bearer/OIDC via a vetted IdP), call UseAuthentication/UseAuthorization, and apply a fallback policy requiring authenticated users; allow anonymous only on healthcheck. [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- **No authorization on sensitive actions: anonymous POST /reset deletes data and anonymous /about?show-details=true returns configuration** — Security / Identity & Access (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 46-51). Protect reset with [Authorize] using a role/policy (and disable it outside test environments); require authorization for /about show-details, keeping only /healthcheck anonymous. [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- **HTTPS redirection is enabled only in Development; no HSTS; HTTP-only launch URL** — Security / Web & API (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs (+1 more), lines 71-74). Call UseHttpsRedirection() (and UseHsts()) in all environments, or document and verify that TLS is terminated and HTTP is rejected at the ingress; add an https:// applicationUrl to launchSettings. [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#https)
- **No CI workflow runs the test suite on every change** — Testing / Test Automation (.github/instructions/unit-tests.instructions.md, lines 1-1). Add a CI workflow that runs 'dotnet test' (with coverlet collection) on every push and pull request, and make it a required check. [The Practical Test Pyramid (Martin Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html#the-deployment-pipeline)

### Warnings

- **TestingRepository.ResetTestingAsync is a ~75-line method mixing config lookup, connection, transaction and error handling (maintainability)** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs, lines 57-133). Extract data-source resolution, connection/transaction execution and error logging into small private methods (or a shared unit-of-work helper) so the method has one purpose. [ISO/IEC 25010 - Maintainability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability)
- **Duplicated blocks: same data-source-type switch repeated 3x and duplicated ProblemDetails/response blocks in middleware (maintainability)** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+1 more), lines 146-205). Introduce a per-provider strategy/factory (connection string, connection, reset script) and a private WriteProblemAsync helper in the middleware. [ISO/IEC 25010 - Maintainability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability)
- **SystemController.About embeds application-metadata and display-name logic instead of delegating to a service** — Software Quality / Architecture Patterns (src/PilotUtiltyApi.Web/Controllers/SystemController.cs, lines 64-96). Move the construction of AboutResponse into a service in the Services layer (like TestingController does) and keep the controller to HTTP mapping. [Azure Architecture Center - Cloud Design Patterns](https://learn.microsoft.com/azure/architecture/patterns/)
- **BuildServiceProvider() called during service registration creates a second container (ASP.NET Core analyzer ASP0000)** — Software Quality / Coding Standards (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 125-128). Pass the already-bound configuration or use AddOptions/IConfigureOptions (or the app-level instance) instead of building a provider mid-registration, which duplicates singletons. [ASP.NET Core analyzer ASP0000](https://learn.microsoft.com/aspnet/core/diagnostics/asp0000)
- **IDbConnection/IDbTransaction are not wrapped in using; connection leaks if BeginTransaction or Open throws** — Software Quality / Coding Standards (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+1 more), lines 73-79). Use 'using var connection' and 'using var transaction' (and OpenAsync) so disposal occurs on every path. [C# coding conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **No documented release process (tagging, changelog, publish)** — Software Lifecycle / Release Process (CONTRIBUTING.md, lines 15-16). Document how releases are cut (version bump in Directory.Build.props, git tag, release notes, publish/deploy step) and automate it with a release workflow. [Semantic Versioning 2.0.0](https://semver.org/)
- **Branching model not documented; review rule not demonstrably enforced** — Software Lifecycle / Branching & Review (CONTRIBUTING.md, lines 17-18). Document the branching model (e.g. trunk-based with short-lived feature branches) and enforce it via branch protection with required reviews and status checks on main. [NIST SP 800-218 (SSDF)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **No automated dependency update configuration** — Software Lifecycle / Supply Chain (CONTRIBUTING.md, lines 10-11). Add .github/dependabot.yml (nuget ecosystem) or Renovate config, or document a scheduled dependency review cadence. [NIST SP 800-218 (SSDF)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **App manages its own rolling log files in addition to writing to stdout** — Twelve-Factor App / Logs (src/PilotUtiltyApi.Web/appsettings.json (+1 more), lines 56-69). Make stdout (Console sink, ideally CompactJsonFormatter) the only default sink and leave routing/retention to the execution environment or the OTLP pipeline. Keep the File sink only as a Development-only override. [The Twelve-Factor App, XI. Logs](https://12factor.net/logs)
- **Implicit network trust: all endpoints anonymous and AllowedHosts is wildcard; no explicit verification of callers** — Security / Identity & Access (src/PilotUtiltyApi.Web/appsettings.json (+1 more), lines 78-78). Verify every caller explicitly (token + scoped policies), restrict AllowedHosts to known hostnames, and use least-privilege database credentials. [OWASP Zero Trust Architecture Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Zero_Trust_Architecture_Cheat_Sheet.html)
- **Placeholder and weak-assertion tests do not verify real behavior** — Testing / Test Quality (test/PilotUtiltyApi.Domain.Tests/ExampleTest.cs (+1 more), lines 14-14). Replace the Assert.Pass placeholder with real Domain tests or remove it. In the 'default warning' controller test, set up the scenario its name describes and assert the Warning header value. [The Practical Test Pyramid (Martin Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html#whattotest)
- **Error correlation ID is an ad-hoc GUID, not tied to the trace ID or logged as a structured property** — Observability / Observability (src/PilotUtiltyApi.Shared/Logging/Models/LoggingCorrelation.cs (+1 more), lines 14-17). Use Activity.Current?.TraceId as the correlation ID (or push it and any inbound X-Correlation-ID into Serilog LogContext as a separate CorrelationId property) so it is searchable and links logs to traces. Also return it for the UserException path. [OpenTelemetry documentation (context propagation / logs correlation)](https://opentelemetry.io/docs/concepts/signals/traces/#context-propagation)
- **No NuGet lock file; restore is not locked to exact transitive versions** — Implementation / Dependency Management (Directory.Packages.props (+1 more), lines 2-4). Set <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile> in Directory.Build.props, commit the generated packages.lock.json files, and use --locked-mode in CI. [NuGet package restore with lock file (fallback rubric: best-practice gap)](https://learn.microsoft.com/nuget/consume-packages/package-references-in-project-files#locking-dependencies)
- **No retry with backoff for transient database failures** — Operations / Reliability (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs, lines 73-89). Add a bounded retry with exponential backoff and jitter for transient connection errors (e.g. Polly/Microsoft.Extensions.Resilience, or provider retry options such as EnableRetryOnFailure/Npgsql retry). [Azure Well-Architected Framework - Reliability](https://learn.microsoft.com/azure/well-architected/reliability/)

### Information

- **Shared project is a grab-bag (API middleware, logging, OpenTelemetry, OpenAPI, Swagger, configuration, exceptions) with low cohesion** — Software Quality / Architecture Patterns (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 6-11). Split Shared into cohesive projects (e.g. Web infrastructure vs. core configuration/exceptions) so the Domain/Repositories layers don't depend on ASP.NET-heavy code. [fallback rubric](https://learn.microsoft.com/azure/architecture/patterns/)
- **Inconsistent naming: folders/projects spelled 'PilotUtiltyApi' vs namespaces 'PilotUtilityApi'; AboutResponse sits in Models/Responses but uses the Models.Dto namespace** — Software Quality / Coding Standards (src/PilotUtiltyApi.Domain/Models/Responses/AboutResponse.cs (+1 more), lines 4-4). Fix the 'Utilty' typo in folder/project paths and align namespaces with folder structure (Responses vs Dto). [fallback rubric](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **Copy-pasted, incorrect XML doc on HealthCheck (describes a category table DTO list)** — Software Quality / Coding Standards (src/PilotUtiltyApi.Web/Controllers/SystemController.cs, lines 41-43). Correct the <returns> text to state it returns 200 OK with "OK"; review other docs for copy/paste drift (e.g. ApiWebApplication example). [fallback rubric](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **Nullable warnings suppressed with #pragma instead of addressed (non-nullable properties left uninitialized)** — Software Quality / Coding Standards (src/PilotUtiltyApi.Shared/Configuration/Models/DataSourceConfiguration.cs, lines 11-13). Mark the properties 'required' or give them defaults/nullable types, and remove the pragma. [C# coding conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **No SECURITY.md or vulnerability-reporting process** — Software Lifecycle / Vulnerability Reporting (CONTRIBUTING.md, lines 70-72). Add a SECURITY.md describing supported versions and how to privately report vulnerabilities. [NIST SP 800-218 (SSDF)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **No CHANGELOG or release notes maintained** — Software Lifecycle / Release Notes (CONTRIBUTING.md, lines 12-16). Add a CHANGELOG.md (e.g. Keep a Changelog format) and require an entry per pull request or release. [Semantic Versioning 2.0.0](https://semver.org/)
- **No SLOs or SLIs documented** — Observability / Observability (README.md, lines 1-1). Document at least SLIs (e.g. request success rate, p95 latency from http.server.request.duration) and target SLOs in the README or docs/. [Azure Well-Architected Framework - Operational Excellence](https://learn.microsoft.com/azure/well-architected/operational-excellence/)
- **No SBOM or license inventory present** — Implementation / Dependency Management (Directory.Packages.props, lines 5-6). Generate a CycloneDX or SPDX SBOM in CI (e.g. CycloneDX for .NET) and publish it as a build artifact or commit it. [Fallback rubric (optional point)](https://learn.microsoft.com/dotnet/core/additional-tools/sbom)

## 4. Full Results

### Software Quality

#### Software Quality

| Check | Result | Evidence |
|-------|--------|----------|
| SQ-01 | fail | ResetTestingAsync is ~75 lines with several responsibilities. |
| SQ-02 | fail | duplicate evidence of SQ-01#1, see Software Quality/Software Quality |
| SQ-03 | fail | Repeated provider switch and duplicated response blocks. |
| SQ-04 | pass |  |
| SQ-05 | pass |  |
| SQ-06 | pass |  |
| SQ-07 | pass |  |
| SQ-08 | pass |  |

#### Design Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| DP-01 | pass |  |
| DP-02 | pass |  |
| DP-04 | pass |  |
| DP-05 | pass |  |
| DP-06 | N/A | No event/observer subscriptions in the reviewed files. |

#### Architecture Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| AP-01 | pass |  |
| AP-02 | fail | About action contains metadata/display logic. |
| AP-03 | pass |  |
| AP-04 | fail | Shared project mixes unrelated concerns. |
| AP-05 | fail | duplicate evidence of CS-CS-04#1, see Software Quality/Coding Standards |
| AP-06 | pass |  |

#### Coding Standards

| Check | Result | Evidence |
|-------|--------|----------|
| CS-01 | fail | Folder/namespace typo and namespace/folder mismatch. |
| CS-02 | pass |  |
| CS-03 | fail | Incorrect copy-pasted doc comment on HealthCheck. |
| CS-04 | pass |  |
| CS-05 | fail | BuildServiceProvider() used during registration (ASP0000). |
| CS-CS-01 | pass |  |
| CS-CS-02 | pass |  |
| CS-CS-03 | pass |  |
| CS-CS-04 | fail | Connection/transaction not in using blocks. |
| CS-CS-05 | fail | CS8618 suppressed with pragma rather than addressed. |

### Software Lifecycle

#### CI/CD

| Check | Result | Evidence |
|-------|--------|----------|
| SL-01 | fail | No CI/CD workflow or pipeline config exists in the target. |

#### Release Process

| Check | Result | Evidence |
|-------|--------|----------|
| SL-02 | fail | CONTRIBUTING.md mentions version bumps only; no tagging, changelog or publish steps are documented. |

#### Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| SL-03 | pass |  |

#### Branching & Review

| Check | Result | Evidence |
|-------|--------|----------|
| SL-04 | fail | No branching model documented and no evidence of enforced branch protection; only a two-reviewer sign-off is stated. |

#### Supply Chain

| Check | Result | Evidence |
|-------|--------|----------|
| SL-05 | fail | duplicate evidence of DEP-02#1, see Implementation/Dependency Management |
| SL-06 | fail | No Dependabot/Renovate config or documented update schedule found. |

#### Vulnerability Reporting

| Check | Result | Evidence |
|-------|--------|----------|
| SL-07 | fail | No SECURITY.md exists; the contact in CONTRIBUTING.md is for Code of Conduct only. |

#### Release Notes

| Check | Result | Evidence |
|-------|--------|----------|
| SL-08 | fail | No CHANGELOG or release notes file exists. |

### Twelve-Factor App

#### Codebase

| Check | Result | Evidence |
|-------|--------|----------|
| TF-01 | pass |  |

#### Dependencies

| Check | Result | Evidence |
|-------|--------|----------|
| TF-02 | pass |  |

#### Config

| Check | Result | Evidence |
|-------|--------|----------|
| TF-03 | pass |  |

#### Backing services

| Check | Result | Evidence |
|-------|--------|----------|
| TF-04 | pass |  |

#### Build, release, run

| Check | Result | Evidence |
|-------|--------|----------|
| TF-05 | N/A | No Dockerfile, CI/CD or release definition in the files in scope to evaluate stage separation. |

#### Processes

| Check | Result | Evidence |
|-------|--------|----------|
| TF-06 | pass |  |

#### Port binding

| Check | Result | Evidence |
|-------|--------|----------|
| TF-07 | pass |  |

#### Concurrency

| Check | Result | Evidence |
|-------|--------|----------|
| TF-08 | pass |  |

#### Disposability

| Check | Result | Evidence |
|-------|--------|----------|
| TF-09 | pass |  |

#### Dev/prod parity

| Check | Result | Evidence |
|-------|--------|----------|
| TF-10 | N/A | Parity depends on deployment/container artifacts that are not in the files in scope. |

#### Logs

| Check | Result | Evidence |
|-------|--------|----------|
| TF-11 | fail | Serilog File sink with rolling/retention settings makes the app manage its own log files besides stdout. |

#### Admin processes

| Check | Result | Evidence |
|-------|--------|----------|
| TF-12 | N/A | No admin/migration tasks or scripts in the files in scope. |

### API Design

#### OpenAPI Spec

| Check | Result | Evidence |
|-------|--------|----------|
| API-01 | pass |  |
| API-02 | pass |  |
| API-03 | fail | The spec paths, parameter requirements, schemas and info block differ from the controllers, DTOs and OpenAPI transformers. |

#### URL Structure & Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| API-04 | fail | Versioning is mixed (header, query and path readers; the system endpoints are version-neutral) and the reset route is verb-style. |

#### Status Codes & Errors

| Check | Result | Evidence |
|-------|--------|----------|
| API-05 | fail | Errors return an empty 400 with the message in a Warning header, and the success responses differ in shape (200 integer vs 204). |

#### Collections

| Check | Result | Evidence |
|-------|--------|----------|
| API-06 | N/A | No collection endpoints exist. |
| API-08 | N/A | No collection endpoints exist. |

#### Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| API-07 | pass |  |

### Security

#### Identity & Access

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-IA-01 | fail | No authentication configured; endpoints are anonymous. |
| SEC-IA-02 | fail | No authorization on destructive/config-disclosing actions. |
| SEC-IA-03 | N/A | No JWT handling found in the reviewed files. |
| SEC-IA-04 | N/A | No OAuth2 flows found. |
| SEC-IA-05 | N/A | No cookie/session usage found. |
| SEC-IA-06 | N/A | No user password storage in the API. |
| SEC-IA-07 | N/A | No credential hashing or custom cryptography found. |
| SEC-IA-08 | fail | Implicit trust: anonymous endpoints and wildcard AllowedHosts. |

#### Input & Injection

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-II-01 | pass |  |
| SEC-II-02 | pass |  |
| SEC-II-03 | pass |  |
| SEC-II-04 | N/A | No shell or OS process execution found in the reviewed files. |
| SEC-II-05 | N/A | No XML parsing found in the reviewed files. |
| SEC-II-06 | N/A | No file upload handling (IFormFile or similar) exists. |
| SEC-II-07 | N/A | No file uploads are stored, so there is nothing executable to assess. |

#### Web & API

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-WA-01 | fail | duplicate evidence of SEC-IA-01#1, see Security/Identity & Access |
| SEC-WA-02 | fail | duplicate evidence of SEC-WA-06#1, see Security/Web & API |
| SEC-WA-03 | fail | duplicate evidence of SEC-IA-01#1, see Security/Identity & Access |
| SEC-WA-04 | fail | duplicate evidence of SEC-IA-01#1, see Security/Identity & Access |
| SEC-WA-05 | pass |  |
| SEC-WA-06 | fail | HTTPS redirection runs only in Development and HSTS is absent, so non-Development HTTP is not redirected or rejected in code. |
| SEC-WA-07 | pass |  |

#### Operational

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-OP-01 | pass |  |
| SEC-OP-02 | pass |  |
| SEC-OP-03 | pass |  |
| SEC-OP-04 | pass |  |
| SEC-OP-05 | pass |  |
| SEC-OP-06 | pass |  |
| SEC-OP-07 | pass |  |

### Testing

#### Test Pyramid

| Check | Result | Evidence |
|-------|--------|----------|
| TST-01 | pass |  |

#### Coverage

| Check | Result | Evidence |
|-------|--------|----------|
| TST-02 | pass |  |

#### Test Quality

| Check | Result | Evidence |
|-------|--------|----------|
| TST-03 | fail | A placeholder Assert.Pass test exists and one controller test asserts less than its name claims. |
| TST-04 | pass |  |
| TST-05 | pass |  |

#### Test Automation

| Check | Result | Evidence |
|-------|--------|----------|
| TST-06 | fail | No CI workflows exist in the target, so tests are never run automatically on changes. |

### Observability

#### Observability

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-01 | pass |  |
| OBS-02 | fail | Correlation ID is a random GUID embedded in a message string, unrelated to the trace ID and not an inbound/propagated ID. |
| OBS-03 | pass |  |
| OBS-04 | pass |  |
| OBS-05 | pass |  |
| OBS-06 | pass |  |
| OBS-07 | fail | No SLO/SLI documentation found in README.md or docs/. |

### Implementation

#### Dependency Management

| Check | Result | Evidence |
|-------|--------|----------|
| DEP-01 | pass |  |
| DEP-02 | fail | No packages.lock.json and RestorePackagesWithLockFile is not enabled. |
| DEP-03 | N/A | No analyzers were approved (no vulnerability scan results) and manifest inspection alone showed no known-vulnerable pinned versions. |
| DEP-04 | pass |  |
| DEP-05 | fail | No sbom.json, *.cdx.json, *.spdx.json or license inventory found. |
| DEP-06 | pass |  |

### Operations

#### Reliability

| Check | Result | Evidence |
|-------|--------|----------|
| REL-01 | pass |  |
| REL-02 | fail | No retry/backoff logic for transient DB failures. |
| REL-03 | N/A | No retry logic exists, so nothing is retried unsafely. |
| REL-04 | fail | duplicate evidence of SQ-01#1, see Software Quality/Software Quality |
| REL-05 | N/A | No infrastructure-as-code found; replica count cannot be assessed. |

#### Performance

| Check | Result | Evidence |
|-------|--------|----------|
| PERF-01 | N/A | No expensive or repeated read operations exist; the only data operation is a destructive reset and the other endpoints return static/config values. |
| PERF-02 | fail | duplicate evidence of CS-CS-04#1, see Software Quality/Coding Standards |
| PERF-03 | pass |  |
| PERF-04 | pass |  |
| PERF-05 | pass |  |

#### Disaster Recovery

| Check | Result | Evidence |
|-------|--------|----------|
| DR-01 | N/A | no infrastructure-as-code found |
| DR-02 | N/A | no infrastructure-as-code found |
| DR-03 | N/A | no infrastructure-as-code found |
| DR-04 | N/A | no infrastructure-as-code found |
| DR-05 | N/A | no infrastructure-as-code found |

#### Monitoring

| Check | Result | Evidence |
|-------|--------|----------|
| MON-01 | N/A | no infrastructure-as-code found |
| MON-02 | N/A | no infrastructure-as-code found |

#### Cost & Sustainability

| Check | Result | Evidence |
|-------|--------|----------|
| COST-01 | N/A | no infrastructure-as-code found |
| COST-02 | N/A | no infrastructure-as-code found |
| COST-03 | N/A | no infrastructure-as-code found |
| COST-04 | N/A | no infrastructure-as-code found |

### Maintainability

#### Maintainability

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-01 | pass |  |
| MAINT-02 | fail | duplicate evidence of DEP-02#1, see Implementation/Dependency Management |
| MAINT-03 | pass |  |
| MAINT-04 | pass |  |
| MAINT-05 | pass |  |

## 5. Appendix

- **Run:** `2026-10-08_1700-PilotUtilityApi` · Target: `C:\Working\Storage\Dev\GitHub\PilotUtilityApi` · Git HEAD: `n/a`
- **Started:** 2026-10-08T17:03:00-06:00 · **Completed:** 2026-10-08T17:30:24-06:00
- **Subjects skipped:** review-disaster-recovery (no infrastructure-as-code found); review-monitoring (no infrastructure-as-code found); review-cost-sustainability (no infrastructure-as-code found)
- **URLs fetched:** none
- **Link approvals:** none

## 6. Manual addendum

Model: Claude Sonnet 5
Credits: 320.9
