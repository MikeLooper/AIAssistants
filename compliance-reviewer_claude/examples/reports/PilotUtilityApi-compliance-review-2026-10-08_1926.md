# PilotUtilityApi — Compliance Review

_Generated 2026-10-08T19:31:26-06:00 · Run `2026-10-08_1926-pilotutilityapi`_

## 1. Summary

**Overall score: 54.13/100 — Poor**

| Subject | Score | Band |
|---------|-------|------|
| Software Quality | 64.86/100 | Fair |
| Software Lifecycle | 0.00/100 | Poor |
| Application Design | 50.00/100 | Poor |
| API Design | 37.50/100 | Poor |
| Security | 59.46/100 | Poor |
| Implementation | 62.96/100 | Fair |
| Observability | 75.00/100 | Good |
| Operations | 57.14/100 | Poor |

**Findings by severity:** Error: 11 · Warning: 17 · Information: 10

### Top 5 Risks

1. **[Error] Functional suitability: reset commits only when 0 rows deleted and rolls back otherwise, yet reports success** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs). Commit the transaction on successful execution regardless of the deleted-row count (roll back only on exception), and add a test asserting deletes persist. [ISO/IEC 25010 - Functional suitability / Reliability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#reliability)
1. **[Error] No CI pipeline builds and tests every push/PR; build and test are manual only** — Software Lifecycle / CI/CD (README.md (+1 more)). Add a CI workflow (e.g. .github/workflows/ci.yml) that runs dotnet restore, build and test on every push and pull request, and make it a required status check on main. [SLSA v1.0 Requirements (scripted build on a hosted build platform)](https://slsa.dev/spec/v1.0/requirements)
1. **[Error] NuGet dependencies are declared centrally but not locked (no packages.lock.json)** — Application Design / Twelve-Factor (Directory.Packages.props). Set <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile> in Directory.Build.props, commit the generated packages.lock.json files, and restore with --locked-mode in builds. [The Twelve-Factor App - II. Dependencies](https://12factor.net/dependencies)
1. **[Error] Committed OpenAPI spec does not match implemented routes and DTOs** — API Design / OpenAPI Specification (docs/PilotUtilityApi_v1.json (+2 more)). Regenerate docs/PilotUtilityApi_v1.json from the running app (or at build time) so the path is /v1/testing/reset, the show-details parameter reflects [BindRequired], and AboutResponse includes the optional applicationConfiguration property; add a CI diff check to keep it in sync. [OpenAPI Specification 3.1](https://spec.openapis.org/oas/latest.html#paths-object)
1. **[Error] Server-side failures returned as 400 with error text in deprecated Warning header instead of a structured error body** — API Design / Azure API Guidelines (src/PilotUtiltyApi.Web/Controllers/TestingController.cs). Return 5xx for service/data-store failures (4xx only for client errors) and put a consistent error object (code + message, e.g. ProblemDetails) in the body with an error-code header, rather than using the deprecated Warning header. [Microsoft Azure REST API Guidelines - HTTP status codes / error handling (DO)](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#http-status-codes)

## 2. Things Done Well

### Software Quality

- [Architecture Patterns] Clean controller -> service -> repository layering via interfaces and DI — src/PilotUtiltyApi.Services/Extensions/ServicesInjectionExtensions.cs
- [Software Quality] Configuration is validated fail-fast at startup with explicit messages — src/PilotUtiltyApi.Shared/Configuration/ApplicationConfiguration.cs
- [Coding Standards] Public types and members consistently carry XML documentation comments — src/PilotUtiltyApi.Domain/Models/Responses/RetrieveResponse.cs

### Software Lifecycle

- [Branching Model] Contributing guide requires sign-off from two other developers before merge — CONTRIBUTING.md
- [Versioning] SemVer adopted explicitly and assembly version centralised in Directory.Build.props — CONTRIBUTING.md
- [Documentation] README documents prerequisites, build, run and test steps clearly — README.md

### Application Design

- [Twelve-Factor] Database and OTEL collector are attached resources selected purely by configuration — src/PilotUtiltyApi.Web/appsettings.json
- [Twelve-Factor] Generic host handles SIGTERM and logs are flushed on shutdown — src/PilotUtiltyApi.Web/Program.cs
- [Twelve-Factor] Self-contained Kestrel host exports HTTP via port binding — src/PilotUtiltyApi.Web/Program.cs

### API Design

- [OpenAPI Specification] OpenAPI 3.1 spec is generated and a copy is committed under docs/ — docs/PilotUtilityApi_v1.json
- [Azure API Guidelines] Explicit API versioning via Asp.Versioning with supported versions reported — src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs
- [Azure API Guidelines] Route tokens forced to lowercase for consistent URL casing — src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs

### Security

- [Input & Injection] SQL is fixed compile-time constants selected by configured provider; no request input reaches SQL — src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs
- [Input & Injection] Only strongly typed input is accepted ([ApiController] model binding of a bool query parameter) — src/PilotUtiltyApi.Web/Controllers/SystemController.cs
- [Web & API] Global exception middleware returns a ProblemDetails body with only a generic user message; stack traces are logged on the server and never returned — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs
- [Web & API] No permissive CORS policy is registered, so browsers keep the default same-origin restriction — src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs
- [Operational] Global exception middleware returns generic ProblemDetails with a correlation ID instead of exception details — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs
- [Operational] Data source password is redacted in ToString and can be suppressed when copying configuration — src/PilotUtiltyApi.Shared/Configuration/Models/DataSourceConfiguration.cs
- [Operational] Structured Serilog logging with a compact JSON formatter encodes logged values — src/PilotUtiltyApi.Web/appsettings.json

### Implementation

- [Testing] Healthy pyramid: fast NUnit unit tests per layer with a single Bruno API smoke test — test/PilotUtiltyApi.Services.Tests/Services/TestingServiceTests.cs
- [Testing] Controller and configuration tests assert concrete status codes, headers and validation messages across edge cases — test/PilotUtiltyApi.Web.Tests/Controllers/TestingControllerTests.cs
- [Testing] Documented test standards (AAA, naming, mirrored structure, determinism, avoid unnecessary mocking) — .github/instructions/unit-tests.instructions.md
- [Observability] Full OpenTelemetry tracing, metrics and logging pipeline with ASP.NET Core, HttpClient, Npgsql and SqlClient instrumentation — src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs
- [Observability] Structured logging through Serilog with a compact JSON file formatter, LogContext enrichment and forwarding to the OTel provider — src/PilotUtiltyApi.Web/appsettings.json
- [Observability] All three signals are exported over OTLP to a collector, and console exporters are limited to Development — src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs
- [Dependency Management] Central Package Management with exact pinned versions for all packages — Directory.Packages.props
- [Dependency Management] Solution-wide target of supported LTS runtime net10.0 — Directory.Build.props
- [Dependency Management] Test-only and analyzer packages marked PrivateAssets=all so they do not flow to consumers — test/PilotUtiltyApi.Web.Tests/PilotUtilityApi.Web.Tests.csproj

### Operations

- [Reliability] Database connect timeout is explicitly configured and applied to connection strings — src/PilotUtiltyApi.Web/appsettings.json
- [Reliability] Configuration is validated at startup so misconfiguration fails fast — src/PilotUtiltyApi.Services/Extensions/ServicesInjectionExtensions.cs
- [Reliability] Destructive reset runs inside a transaction with rollback on exception — src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs
- [Performance] Async end-to-end controller/service/query path with CancellationToken propagated — src/PilotUtiltyApi.Web/Controllers/TestingController.cs
- [Performance] Reset runs as a single batched script in one round trip — src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs
- [Maintainability] README documents layered architecture with explicit inter-layer dependency rules — README.md
- [Maintainability] Comprehensive .editorconfig and written architecture guardrails enforce consistent style and layering — .editorconfig
- [Maintainability] Thin composition root with no TODO/FIXME/HACK markers in reviewed code — src/PilotUtiltyApi.Web/Program.cs

## 3. Recommended Improvements

### Errors

- **Functional suitability: reset commits only when 0 rows deleted and rolls back otherwise, yet reports success** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs, lines 89-98). Commit the transaction on successful execution regardless of the deleted-row count (roll back only on exception), and add a test asserting deletes persist. [ISO/IEC 25010 - Functional suitability / Reliability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#reliability)
- **No CI pipeline builds and tests every push/PR; build and test are manual only** — Software Lifecycle / CI/CD (README.md (+1 more), lines 105-108). Add a CI workflow (e.g. .github/workflows/ci.yml) that runs dotnet restore, build and test on every push and pull request, and make it a required status check on main. [SLSA v1.0 Requirements (scripted build on a hosted build platform)](https://slsa.dev/spec/v1.0/requirements)
- **NuGet dependencies are declared centrally but not locked (no packages.lock.json)** — Application Design / Twelve-Factor (Directory.Packages.props, lines 2-4). Set <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile> in Directory.Build.props, commit the generated packages.lock.json files, and restore with --locked-mode in builds. [The Twelve-Factor App - II. Dependencies](https://12factor.net/dependencies)
- **Deploy-specific config and credential fields live in committed, environment-named appsettings files** — Application Design / Twelve-Factor (src/PilotUtiltyApi.Web/appsettings.json (+2 more), lines 10-13). Remove hosts, user names and password fields from committed appsettings files and supply them per deploy via environment variables (e.g. Application__DataSources__0__Password) or a secret store; keep only non-deploy-specific defaults in appsettings.json. [The Twelve-Factor App - III. Config](https://12factor.net/config)
- **Committed OpenAPI spec does not match implemented routes and DTOs** — API Design / OpenAPI Specification (docs/PilotUtilityApi_v1.json (+2 more), lines 81-82). Regenerate docs/PilotUtilityApi_v1.json from the running app (or at build time) so the path is /v1/testing/reset, the show-details parameter reflects [BindRequired], and AboutResponse includes the optional applicationConfiguration property; add a CI diff check to keep it in sync. [OpenAPI Specification 3.1](https://spec.openapis.org/oas/latest.html#paths-object)
- **Inconsistent URL structure: URL-segment versioning mixed with unversioned routes and a verb-style action path** — API Design / Azure API Guidelines (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+2 more), lines 46-47). Pick one versioning mechanism (Azure guidelines use the api-version query parameter rather than a path segment) and model actions as resource operations (e.g. POST /testing:reset or a resource noun) instead of a verb path segment. [Microsoft Azure REST API Guidelines - URL structure (DO)](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#url-structure)
- **Server-side failures returned as 400 with error text in deprecated Warning header instead of a structured error body** — API Design / Azure API Guidelines (src/PilotUtiltyApi.Web/Controllers/TestingController.cs, lines 55-59). Return 5xx for service/data-store failures (4xx only for client errors) and put a consistent error object (code + message, e.g. ProblemDetails) in the body with an error-code header, rather than using the deprecated Warning header. [Microsoft Azure REST API Guidelines - HTTP status codes / error handling (DO)](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md#http-status-codes)
- **No authentication is configured and every controller is marked [AllowAnonymous]** — Security / Identity & Access (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+2 more), lines 15-19). Register an authentication scheme (e.g. JWT bearer via a vetted IdP, or API key for this utility API), add UseAuthentication/UseAuthorization, and remove the class-level [AllowAnonymous] from TestingController. [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- **Destructive POST /v1/testing/reset and configuration-revealing /about?show-details have no authorization** — Security / Identity & Access (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+2 more), lines 46-53). Protect the reset endpoint with [Authorize(Policy = ...)] restricted to an admin/test role (and disable it outside test environments), and require authorization for show-details=true; keep only /healthcheck anonymous. [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- **HTTPS redirection is enabled only in Development (the condition is inverted), and the launch profile listens on HTTP only** — Security / Web & API (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs (+1 more), lines 73-76). Call `UseHttpsRedirection()` (with `UseHsts()`) in every environment except Development, or reject HTTP at the edge. Also add an HTTPS URL to the launch profile. [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#https)
- **No CI pipeline runs the test suite on each change** — Implementation / Testing (.github/instructions/unit-tests.instructions.md, lines 78-84). Add a CI workflow (e.g. GitHub Actions) that runs 'dotnet test' with coverage collection on every push and pull request, and require it to pass before merge. [The Practical Test Pyramid (Martin Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html#TheImportanceOfTestAutomation)

### Warnings

- **Maintainability: provider switch on DataSourceType repeated three times and error-logging block duplicated** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+2 more), lines 146-148). Introduce a per-provider strategy (e.g. IDbProvider with BuildConnectionString/CreateConnection/ResetScript) resolved once, and collapse the two identical LogError/throw blocks into a single outer catch. [ISO/IEC 25010 - Maintainability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability)
- **Reliability: fatal startup exception is logged but the process exits with code 0** — Software Quality / Software Quality (src/PilotUtiltyApi.Web/Program.cs, lines 34-37). Return a non-zero exit code (e.g. Environment.ExitCode = 1 or rethrow) after logging so hosts/orchestrators detect the failed start. [ISO/IEC 25010 - Reliability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#reliability)
- **IDisposable connection and transaction are not wrapped in using (CS-CS-04)** — Software Quality / Coding Standards (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs, lines 73-79). Use 'await using' declarations for the DbConnection and DbTransaction (and OpenAsync/BeginTransactionAsync) so they are disposed even if an exception occurs before the inner try. [C# coding conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **BuildServiceProvider called during service registration (ASP0000), creating a second container** — Software Quality / Coding Standards (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 124-126). Read IApplicationConfiguration from builder.Configuration (or use IOptions/IConfigureOptions) instead of building an intermediate service provider. [C# coding conventions / ASP.NET Core analyzers](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **No documented release process (tagging, changelog, publish step)** — Software Lifecycle / Release Process (CONTRIBUTING.md (+1 more), lines 15-16). Document a release procedure (version bump in Directory.Build.props, Git tag vX.Y.Z, changelog entry, build/publish step) and replace the boilerplate container-layer step in CONTRIBUTING.md, which does not apply to this repo. [Semantic Versioning 2.0.0](https://semver.org/)
- **Inconsistent version sources: assembly version 1.0.0 vs documented API version 0.1.1** — Software Lifecycle / Versioning (Directory.Build.props (+1 more), lines 3-3). Keep a single source of truth for the version (Directory.Build.props) and derive the OpenAPI/documented version from it so bumps are consistent and meaningful. [Semantic Versioning 2.0.0](https://semver.org/#semantic-versioning-specification-semver)
- **Branching model not documented; review rule exists only as text with no visible enforcement** — Software Lifecycle / Branching Model (CONTRIBUTING.md, lines 17-18). Document the branching model (e.g. trunk-based with short-lived feature branches into protected main) and enforce it with branch protection/rulesets requiring reviews and passing CI. [NIST SP 800-218 SSDF](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **No automated or scheduled dependency updates (no Dependabot/Renovate config)** — Software Lifecycle / Supply Chain (.github/copilot-instructions.md, lines 1-4). Add .github/dependabot.yml with the nuget ecosystem (and github-actions once CI exists) on a weekly schedule. [NIST SP 800-218 SSDF](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **App writes and manages its own rolling log files instead of only streaming to stdout** — Application Design / Twelve-Factor (src/PilotUtiltyApi.Web/appsettings.json, lines 58-65). Drop the Serilog File sink (or enable it only in a local-dev override) and rely on the Console/OTLP streams, leaving routing and retention to the execution environment; also remove the committed files under src/PilotUtiltyApi.Web/logs/ from the repository. [The Twelve-Factor App - XI. Logs](https://12factor.net/logs)
- **No Content-Security-Policy header is set; the pipeline also serves Swagger UI and Scalar HTML pages** — Security / Web & API (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 78-86). Add security-header middleware (for example NetEscapades.AspNetCore.SecurityHeaders or a small custom middleware) that sets `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'` on API responses. Use a looser policy only for the Swagger/Scalar UI routes. [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- **X-Content-Type-Options: nosniff is not set** — Security / Web & API (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 65-87). Add `X-Content-Type-Options: nosniff` to every response from the same security-header middleware. [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-content-type-options)
- **No clickjacking protection (no X-Frame-Options or CSP frame-ancestors)** — Security / Web & API (src/PilotUtiltyApi.Shared/Swagger/Extensions/SwaggerExtensions.cs (+1 more), lines 38-41). Send `X-Frame-Options: DENY` and/or the CSP directive `frame-ancestors 'none'` on all responses, including the Swagger and Scalar UI pages. [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-frame-options)
- **Placeholder and mis-arranged tests pass without asserting the behavior they name** — Implementation / Testing (test/PilotUtiltyApi.Domain.Tests/ExampleTest.cs (+2 more), lines 9-14). Remove the Assert.Pass placeholder or replace it with real Domain model tests, fix the null-message controller test to actually return a null ErrorMessage and assert the default Warning header value, and replace 'DoesNotThrow' constructor tests with assertions on observable behavior. [The Practical Test Pyramid (Martin Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html#WritingYourFirstUnitTest)
- **User-facing correlation ID is a random GUID that is not linked to the OpenTelemetry trace ID** — Implementation / Observability (src/PilotUtiltyApi.Shared/Logging/Models/LoggingCorrelation.cs (+1 more), lines 13-16). Derive the correlation ID from Activity.Current?.TraceId (falling back to HttpContext.TraceIdentifier), so the ID shown to callers can be used to find the trace in Tempo and the related logs in Loki. [OpenTelemetry documentation (context propagation / log-trace correlation)](https://opentelemetry.io/docs/)
- **No retry with backoff for transient database failures** — Operations / Reliability (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+1 more), lines 73-89). Add a bounded exponential-backoff retry for transient connection errors (e.g. a Polly resilience pipeline, SqlRetryLogicProvider, or Npgsql retry), applied to the connect step and the idempotent reset. [Azure Well-Architected Framework - Reliability](https://learn.microsoft.com/azure/well-architected/reliability/)
- **No circuit breaker protecting calls to the database dependency** — Operations / Reliability (src/PilotUtiltyApi.Services/Extensions/ServicesInjectionExtensions.cs, lines 71-73). Add a circuit breaker (e.g. Polly CircuitBreaker strategy in a shared resilience pipeline) around database access so a degraded DB fails fast instead of tying up requests for the full connect timeout. [Azure Well-Architected Framework - Reliability](https://learn.microsoft.com/azure/well-architected/reliability/)
- **Database provisioning and secret/environment configuration steps are not documented** — Operations / Maintainability (README.md (+1 more), lines 84-86). Document how to create the NorthWind/northwind database and the test tables/schema, give the `dotnet user-secrets set` commands, and show environment-variable overrides (e.g. Application__DataSources__0__Password) instead of editing appsettings.json. [Maintainability fallback rubric (onboarding prerequisites and environment documentation)]()

### Information

- **Unused Logger property created in TestingService** — Software Quality / Software Quality (src/PilotUtiltyApi.Services/Services/TestingService.cs, lines 30-37). Remove the unused logger dependency or use it to log service-level outcomes. [ISO/IEC 25010 - Maintainability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010#maintainability)
- **Project folders misspelled 'PilotUtiltyApi' while namespaces/projects use 'PilotUtilityApi'** — Software Quality / Coding Standards (src/PilotUtiltyApi.Services/Services/TestingService.cs (+1 more), lines 8-8). Rename the src/test folders to PilotUtilityApi.* to match namespaces and project names, and fix the 'Instatiate' typos. [C# coding conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **Several XML doc comments are inaccurate (copy-paste returns text, wrong usage examples)** — Software Quality / Coding Standards (src/PilotUtiltyApi.Web/Controllers/SystemController.cs (+2 more), lines 40-42). Correct the HealthCheck <returns> text and the <example> snippets so they match the real extension targets (WebApplicationBuilder/WebApplication). [C# coding conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **No build provenance, signing or reproducible-build settings** — Software Lifecycle / Supply Chain (Directory.Build.props, lines 2-9). Once CI exists, generate build provenance attestations (e.g. actions/attest-build-provenance) and enable deterministic builds (ContinuousIntegrationBuild, RestorePackagesWithLockFile). [SLSA v1.0 Requirements (provenance)](https://slsa.dev/spec/v1.0/requirements)
- **No SECURITY.md or vulnerability-reporting process** — Software Lifecycle / Vulnerability Disclosure (CONTRIBUTING.md, lines 73-74). Add a SECURITY.md describing supported versions and a private reporting channel (e.g. GitHub private vulnerability reporting); the only contact today is for Code of Conduct issues. [NIST SP 800-218 SSDF (RV.1)](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development)
- **No changelog or release notes** — Software Lifecycle / Documentation (CONTRIBUTING.md, lines 12-13). Add a CHANGELOG.md (Keep a Changelog format) and require an entry per PR in CONTRIBUTING.md. [Semantic Versioning 2.0.0](https://semver.org/)
- **No SLOs or SLIs are documented in the repository** — Implementation / Observability (src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs, lines 78-86). Document target SLIs, such as availability and p95 latency from http.server.request.duration, along with SLO thresholds (for example in docs/ or the README), so the exported metrics can be alerted on. [Azure Well-Architected Framework - Operational Excellence](https://learn.microsoft.com/azure/well-architected/operational-excellence/)
- **No SBOM or third-party license inventory present** — Implementation / Dependency Management (Directory.Packages.props, lines 5-40). Generate a CycloneDX or SPDX SBOM (e.g. via CycloneDX dotnet tool or Microsoft sbom-tool) as part of the build and publish it with releases. [fallback rubric (SBOM / license inventory)](https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props)
- **Project folder names misspelled (PilotUtiltyApi.*) and inconsistent with csproj names, namespaces and README structure** — Operations / Maintainability (PilotUtilityApi.sln (+2 more), lines 19-27). Rename the src/ and test/ folders to PilotUtilityApi.* to match project names and namespaces (dotnet_style_namespace_match_folder is enabled), then update the .sln paths and README. [Maintainability fallback rubric (consistent module/folder boundaries)]()
- **Stale references: solution lists a missing .runsettings file and CONTRIBUTING links a non-existent README section** — Operations / Maintainability (PilotUtilityApi.sln (+1 more), lines 9-9). Add the .runsettings file or remove it from Solution Items, and either add a 'Copilot Customization' README section or point CONTRIBUTING at .github/copilot-instructions.md. [Maintainability fallback rubric (remove stale artifacts)]()

## 4. Full Results

### Software Quality

#### Software Quality

| Check | Result | Evidence |
|-------|--------|----------|
| SQ-01 | pass |  |
| SQ-02 | pass |  |
| SQ-03 | fail | Provider switch repeated three times and LogError block duplicated in TestingRepository. |
| SQ-04 | pass |  |
| SQ-05 | pass |  |
| SQ-06 | fail | Reset rolls back successful deletes while reporting success; fatal startup exits with code 0. |
| SQ-07 | pass |  |
| SQ-08 | fail | Unused Logger in TestingService. |

#### Design Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| DP-01 | pass |  |
| DP-02 | pass |  |
| DP-04 | pass |  |
| DP-05 | pass |  |
| DP-06 | N/A | No observer/event subscriptions in the reviewed files. |

#### Architecture Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| AP-01 | pass |  |
| AP-02 | pass |  |
| AP-03 | pass |  |
| AP-04 | pass |  |
| AP-05 | fail | duplicate evidence of REL-02#1, see Operations/Reliability |
| AP-06 | pass |  |

#### Coding Standards

| Check | Result | Evidence |
|-------|--------|----------|
| CS-01 | fail | Folder names misspelled 'PilotUtiltyApi' vs 'PilotUtilityApi' namespaces; 'Instatiate' typos. |
| CS-02 | pass |  |
| CS-03 | fail | Inaccurate copy-paste doc comments and usage examples. |
| CS-04 | pass |  |
| CS-05 | fail | Undisposed IDisposable DB resources and BuildServiceProvider during registration. |

### Software Lifecycle

#### CI/CD

| Check | Result | Evidence |
|-------|--------|----------|
| SL-01 | fail | No CI configuration (.github/workflows, azure-pipelines.yml, Jenkinsfile) exists. |

#### Release Process

| Check | Result | Evidence |
|-------|--------|----------|
| SL-02 | fail | Only a manual README version bump is described; no tagging, changelog or publish step. |

#### Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| SL-03 | fail | SemVer format is used but assembly (1.0.0) and documented API (0.1.1) versions disagree. |

#### Branching Model

| Check | Result | Evidence |
|-------|--------|----------|
| SL-04 | fail | No branching model documented and no enforcement visible; only a two-reviewer rule in text. |

#### Supply Chain

| Check | Result | Evidence |
|-------|--------|----------|
| SL-05 | fail | No provenance, signing or deterministic-build configuration. |
| SL-06 | fail | No Dependabot or Renovate configuration exists. |

#### Vulnerability Disclosure

| Check | Result | Evidence |
|-------|--------|----------|
| SL-07 | fail | No SECURITY.md or equivalent vulnerability-reporting process. |

#### Documentation

| Check | Result | Evidence |
|-------|--------|----------|
| SL-08 | fail | No CHANGELOG or release notes exist. |

### Application Design

#### Twelve-Factor

| Check | Result | Evidence |
|-------|--------|----------|
| TF-01 | pass |  |
| TF-02 | fail | Central package versions are declared but no NuGet lock files exist or are enabled. |
| TF-03 | fail | Hosts and credential fields are kept in committed, environment-named appsettings files rather than supplied via environment variables. |
| TF-04 | pass |  |
| TF-05 | N/A | No CI/CD, Dockerfile or release tooling exists in scope to evaluate build/release/run separation. |
| TF-06 | pass |  |
| TF-07 | pass |  |
| TF-08 | pass |  |
| TF-09 | pass |  |
| TF-10 | pass |  |
| TF-11 | fail | Serilog File sink with app-managed rolling and retention is configured alongside Console. |
| TF-12 | N/A | No admin, migration or one-off process tooling found in scope. |

### API Design

#### OpenAPI Specification

| Check | Result | Evidence |
|-------|--------|----------|
| API-01 | pass |  |
| API-02 | pass |  |
| API-03 | fail | Spec lists /testing/reset while code serves /v1/testing/reset, omits required flag on show-details and the applicationConfiguration property. |

#### Azure API Guidelines

| Check | Result | Evidence |
|-------|--------|----------|
| API-04 | fail | Mixed URL-segment/header/query versioning, unversioned system routes and a verb-style /reset path. |
| API-05 | fail | Service errors return 400 with no error body and a deprecated Warning header. |
| API-06 | N/A | No collection endpoints exist in the reviewed controllers. |
| API-07 | pass |  |
| API-08 | N/A | No collection endpoints exist in the reviewed controllers. |

### Security

#### Identity & Access

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-IA-01 | fail | No authentication configured; controllers are [AllowAnonymous]. |
| SEC-IA-02 | fail | Destructive reset and config-details endpoints lack authorization. |
| SEC-IA-03 | N/A | No JWT handling in the reviewed files. |
| SEC-IA-04 | N/A | No OAuth2 flows implemented. |
| SEC-IA-05 | N/A | No session/cookie management; stateless API. |
| SEC-IA-06 | N/A | No user password storage in the application. |
| SEC-IA-07 | N/A | No credential hashing or cryptography code present. |
| SEC-IA-08 | fail | duplicate evidence of SEC-WA-06#1, see Security/Web & API |

#### Input & Injection

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-II-01 | pass |  |
| SEC-II-02 | pass |  |
| SEC-II-03 | pass |  |
| SEC-II-04 | N/A | No shell/OS process execution in the reviewed files. |
| SEC-II-05 | pass |  |
| SEC-II-06 | N/A | No file upload endpoints found. |
| SEC-II-07 | N/A | No file upload storage found. |

#### Web & API

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-WA-01 | fail | No Content-Security-Policy header is configured anywhere in the pipeline. |
| SEC-WA-02 | fail | duplicate evidence of SEC-WA-06#1, see Security/Web & API |
| SEC-WA-03 | fail | No X-Content-Type-Options header is set. |
| SEC-WA-04 | fail | Neither X-Frame-Options nor CSP frame-ancestors is set. |
| SEC-WA-05 | pass |  |
| SEC-WA-06 | fail | HTTPS redirection runs only in Development and the launch profile is HTTP-only. |
| SEC-WA-07 | pass |  |

#### Operational

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-OP-01 | pass |  |
| SEC-OP-02 | pass |  |
| SEC-OP-03 | pass |  |
| SEC-OP-04 | pass |  |
| SEC-OP-05 | pass |  |
| SEC-OP-06 | fail | duplicate evidence of TF-03#1, see Application Design/Twelve-Factor |
| SEC-OP-07 | pass |  |

### Implementation

#### Testing

| Check | Result | Evidence |
|-------|--------|----------|
| TST-01 | pass |  |
| TST-02 | pass |  |
| TST-03 | fail | A placeholder Assert.Pass test, a test whose arrange does not match its named scenario, and DoesNotThrow-only constructor tests do not assert real behavior. |
| TST-04 | pass |  |
| TST-05 | pass |  |
| TST-06 | fail | No CI/CD pipeline files exist, so tests are never run automatically on change. |

#### Dependency Management

| Check | Result | Evidence |
|-------|--------|----------|
| DEP-01 | pass |  |
| DEP-02 | fail | duplicate evidence of TF-02#1, see Application Design/Twelve-Factor |
| DEP-03 | N/A | No vulnerability analyzer was approved for this run; manifest inspection alone cannot confirm advisory status of the pinned versions. |
| DEP-04 | pass |  |
| DEP-05 | fail | No SBOM or third-party license inventory found in the repository. |
| DEP-06 | pass |  |

### Observability

#### Observability

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-01 | pass |  |
| OBS-02 | fail | W3C trace context propagates through the OTel instrumentation, but the app's own correlation ID is an unrelated random GUID. |
| OBS-03 | pass |  |
| OBS-04 | pass |  |
| OBS-05 | pass |  |
| OBS-06 | pass |  |
| OBS-07 | fail | No SLO/SLI documentation was found anywhere in the repository. |

### Operations

#### Reliability

| Check | Result | Evidence |
|-------|--------|----------|
| REL-01 | pass |  |
| REL-02 | fail | No retry/backoff for transient DB errors. |
| REL-03 | pass |  |
| REL-04 | fail | No circuit breaker around the database dependency. |
| REL-05 | N/A | No IaC, Dockerfile or deployment manifests found to assess replica count. |

#### Performance

| Check | Result | Evidence |
|-------|--------|----------|
| PERF-01 | N/A | No expensive or repeated reads in the reviewed files; the only DB operation is a destructive reset that must not be cached. |
| PERF-02 | fail | duplicate evidence of CS-05#1, see Software Quality/Coding Standards |
| PERF-03 | pass |  |
| PERF-04 | pass |  |
| PERF-05 | pass |  |

#### Disaster Recovery

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | No infrastructure-as-code found in the target repository. |

#### Monitoring

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | No infrastructure-as-code found in the target repository. |

#### Cost & Sustainability

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | No infrastructure-as-code found in the target repository. |

#### Maintainability

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-01 | fail | duplicate evidence of SEC-WA-06#1, see Security/Web & API |
| MAINT-02 | fail | Layering is clear, but folder names (PilotUtiltyApi.*) diverge from project names, namespaces and README. |
| MAINT-03 | fail | Tooling prerequisites are listed, but database provisioning, user-secrets setup and env-var overrides are undocumented. |
| MAINT-04 | pass |  |
| MAINT-05 | fail | Stale references remain: missing .runsettings in the solution and a dead README anchor in CONTRIBUTING. |

## 5. Appendix

- **Run:** `2026-10-08_1926-pilotutilityapi` · Target: `C:\Working\Storage\Dev\GitHub\PilotUtilityApi` · Git HEAD: `929741f5c04d8218a6852d5d6eb33cbeb2f1d20b`
- **Started:** 2026-10-09T01:26:05Z · **Completed:** 2026-10-08T19:31:26-06:00
- **Subjects skipped:** review-disaster-recovery (no infrastructure-as-code found); review-monitoring (no infrastructure-as-code found); review-cost-sustainability (no infrastructure-as-code found)
- **URLs fetched:** none
- **Link approvals:** none
