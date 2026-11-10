# PilotUtilityApi — Compliance Review

_Generated 2026-11-09T20:44:31-07:00 · Run `2026-11-09_2035-PilotUtilityApi`_

## 1. Summary

**Overall score: 54.55/100 — Poor**

| Subject | Score | Band |
|---------|-------|------|
| Software Quality | 61.29/100 | Fair |
| Software Lifecycle | 65.00/100 | Fair |
| Twelve-Factor | 90.91/100 | Excellent |
| API Design | 29.27/100 | Poor |
| Security | 62.16/100 | Fair |
| Testing | 48.00/100 | Poor |
| Observability | 56.25/100 | Poor |
| Implementation | 50.00/100 | Poor |
| Reliability | 45.45/100 | Poor |
| Operations | 60.00/100 | Fair |
| Maintainability | 9.09/100 | Poor |

**Findings by severity:** Error: 18 · Warning: 30 · Information: 15

### Top 5 Risks

1. **[Error] AboutResponse.applicationConfiguration is returned but missing from the spec schema** — API Design / OpenAPI Specification (src/PilotUtiltyApi.Domain/Models/Responses/AboutResponse.cs (+1 more)). Document the optional applicationConfiguration property (with its schema) in AboutResponse, or stop returning it from the endpoint. [OpenAPI Specification — OAS-40](https://spec.openapis.org/oas/v3.1.2.html#schema-object)
1. **[Error] 500 Problem Details responses from the exception middleware are not documented** — API Design / OpenAPI Specification (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs (+1 more)). Add a default (or 500) error response with the error schema to every operation, e.g. via the existing GlobalOperationTransformer. [OpenAPI Specification — OAS-41](https://spec.openapis.org/oas/v3.1.2.html#responses-object)
1. **[Error] Synchronous POST action returns 204 with no body when nothing was deleted** — API Design / Status codes and errors (src/PilotUtiltyApi.Web/Controllers/TestingController.cs). Always return 200 with a JSON object body, e.g. { "deletedCount": 0 }, instead of switching to 204 or a bare integer. [Microsoft Azure REST API Guidelines — AZ-017](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#http-post-action-returns-200)
1. **[Error] Error responses carry no x-ms-error-code header or machine-readable error code** — API Design / Status codes and errors (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs). Set an x-ms-error-code header on every error response with a documented string code that matches error.code in the body. [Microsoft Azure REST API Guidelines — AZ-044](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#rest-error-code-header)
1. **[Error] API version is placed in the operation path** — API Design / Versioning (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more)). Remove the v{version} route segment and UrlSegmentApiVersionReader; select versions with the api-version query parameter. [Microsoft Azure REST API Guidelines — AZ-088](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#versioning-no-version-in-path)

## 2. Things Done Well

### Software Quality

- [Architecture Patterns] Web project references Domain, Services and Shared only; data access stays behind the services layer — src/PilotUtiltyApi.Web/PilotUtilityApi.Web.csproj
- [Coding Standards] Comprehensive root .editorconfig defines formatting, style and naming rules — .editorconfig
- [Coding Standards] XML documentation file generation enabled and public members consistently documented — src/PilotUtiltyApi.Web/PilotUtilityApi.Web.csproj

### Software Lifecycle

- [Continuous Integration] Every pull request to main is built by a pipeline defined in the repository on a hosted runner — .github/workflows/dotnet.yml
- [Versioning] A single, valid SemVer version is declared centrally for all projects — Directory.Build.props
- [Pipeline Hardening] Workflow uses the unprivileged pull_request trigger and interpolates no untrusted context into scripts — .github/workflows/dotnet.yml

### Twelve-Factor

- [IV. Backing services] Database provider and connection handle are chosen entirely from configuration — src/PilotUtiltyApi.Web/appsettings.json
- [II. Dependencies] All dependencies declared through central package management — Directory.Packages.props
- [I. Codebase] Shared code consumed through project references, not copied source — src/PilotUtiltyApi.Web/PilotUtilityApi.Web.csproj

### API Design

- [OpenAPI Specification] A structurally valid OpenAPI 3.1 spec is checked in and generated from the code — docs/PilotUtilityApi_v1.json
- [Resource design] Configuration details exposed by GET /about suppress sensitive values — src/PilotUtiltyApi.Web/Controllers/SystemController.cs
- [URLs and resources] Route tokens are consistently lower-cased via a route token transformer — src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs

### Security

- [Input & Injection] Reset SQL is fixed constant text with no interpolated values, executed via Dapper — src/PilotUtiltyApi.Repositories/Constants/SqlConstants.cs
- [Input & Injection] Controllers use [ApiController] and the only input is a typed, required boolean query parameter — src/PilotUtiltyApi.Web/Controllers/SystemController.cs
- [Web & API] No CORS policy is configured, so the Same Origin Policy applies — src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs
- [Web & API] Controllers declare explicit HTTP method attributes and no XML formatters are registered — src/PilotUtiltyApi.Web/Controllers/TestingController.cs
- [Operational] Global exception middleware logs unexpected errors and returns a generic ProblemDetails body — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs
- [Operational] Data-source password is redacted in ToString and in suppressed configuration copies — src/PilotUtiltyApi.Shared/Configuration/Models/DataSourceConfiguration.cs
- [Operational] File log sink is bounded by rolling interval, size limit and retention count, in structured JSON — src/PilotUtiltyApi.Web/appsettings.json

### Testing

- [CI execution] CI runs the full test suite on push and pull request to main with no failure suppression — .github/workflows/dotnet.yml
- [Isolation and determinism] Tests build their own state per test with no shared statics, sleeps, clock reads or skips — test/PilotUtiltyApi.TestingShared/Base/TestBase.cs
- [Assertion quality] Configuration validation has thorough negative tests asserting exception type and message — test/PilotUtiltyApi.Shared.Tests/Configuration/ApplicationConfigurationTests.cs

### Observability

- [Structured Logging] Serilog configured from appsettings with compact JSON file sink, enrichers, request logging and message templates — src/PilotUtiltyApi.Web/appsettings.json
- [Distributed Tracing] OpenTelemetry SDK instruments ASP.NET Core, HttpClient, Npgsql and SqlClient for traces and metrics, exported via OTLP to a collector — src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs
- [Error Recording] Global middleware logs unhandled exceptions once, with the exception object, at Error level — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs

### Implementation

- [Dependency Management] Central Package Management with exact versions for every package; project files carry no version strings — Directory.Packages.props
- [Dependency Management] All projects target the supported .NET 10 LTS line, with Microsoft.AspNetCore and Microsoft.Extensions packages aligned at 10.0.13 — Directory.Build.props
- [Dependency Management] Test frameworks and mocking libraries are referenced only from test projects, and analyzers and collectors use PrivateAssets=all — test/PilotUtiltyApi.Web.Tests/PilotUtilityApi.Web.Tests.csproj

### Reliability

- [Timeouts] Database connect timeout is explicit and driven from configuration for both providers — src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs
- [Timeouts] Cancellation token flows from service to the Dapper command, and the transaction rolls back on failure — src/PilotUtiltyApi.Services/Services/TestingService.cs

### Operations

- [Performance] Test-data reset runs as one batched script in a single round trip and transaction — src/PilotUtiltyApi.Repositories/Constants/SqlConstants.cs
- [Performance] Cancellation token flows from the controller through the service to the Dapper command — src/PilotUtiltyApi.Web/Controllers/TestingController.cs

### Maintainability

- [README & Onboarding] README states purpose and gives fenced, copy-pasteable restore/build/run/test commands — README.md
- [Prerequisites & Configuration] DataSources keys documented in a table; sample settings use password placeholders — src/PilotUtiltyApi.Web/appsettings.Development.json
- [License & Conduct] MIT license stated consistently (LICENSE, README, OpenApi config) with a Code of Conduct in CONTRIBUTING — LICENSE

## 3. Recommended Improvements

### Errors

- **Spec documents /testing/reset but the controller routes it under /v{version}/testing/reset** — API Design / OpenAPI Specification (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 17-17). Regenerate the checked-in spec from the current build (or align the route template) so the documented path matches the implemented URL. [OpenAPI Specification — OAS-38](https://spec.openapis.org/oas/v3.1.2.html#paths-object)
- **show-details is [BindRequired] in code but optional with a default in the spec** — API Design / OpenAPI Specification (src/PilotUtiltyApi.Web/Controllers/SystemController.cs (+1 more), lines 64-64). Decide whether the parameter is optional; remove [BindRequired] to keep the default, or mark it required: true in the spec. [OpenAPI Specification — OAS-39](https://spec.openapis.org/oas/v3.1.2.html#parameter-object)
- **AboutResponse.applicationConfiguration is returned but missing from the spec schema** — API Design / OpenAPI Specification (src/PilotUtiltyApi.Domain/Models/Responses/AboutResponse.cs (+1 more), lines 20-21). Document the optional applicationConfiguration property (with its schema) in AboutResponse, or stop returning it from the endpoint. [OpenAPI Specification — OAS-40](https://spec.openapis.org/oas/v3.1.2.html#schema-object)
- **500 Problem Details responses from the exception middleware are not documented** — API Design / OpenAPI Specification (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs (+1 more), lines 81-92). Add a default (or 500) error response with the error schema to every operation, e.g. via the existing GlobalOperationTransformer. [OpenAPI Specification — OAS-41](https://spec.openapis.org/oas/v3.1.2.html#responses-object)
- **Synchronous POST action returns 204 with no body when nothing was deleted** — API Design / Status codes and errors (src/PilotUtiltyApi.Web/Controllers/TestingController.cs, lines 61-66). Always return 200 with a JSON object body, e.g. { "deletedCount": 0 }, instead of switching to 204 or a bare integer. [Microsoft Azure REST API Guidelines — AZ-017](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#http-post-action-returns-200)
- **Errors use an empty 400 with a Warning header or ProblemDetails, not the standard error body** — API Design / Status codes and errors (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 57-58). Return one consistent error body { "error": { "code", "message", ... } } for all errors, and do not report service failures as a body-less 400 with a Warning header. [Microsoft Azure REST API Guidelines — AZ-046](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#rest-error-response-body-structure)
- **Error responses carry no x-ms-error-code header or machine-readable error code** — API Design / Status codes and errors (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs, lines 89-92). Set an x-ms-error-code header on every error response with a documented string code that matches error.code in the body. [Microsoft Azure REST API Guidelines — AZ-044](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#rest-error-code-header)
- **API version is placed in the operation path** — API Design / Versioning (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 17-17). Remove the v{version} route segment and UrlSegmentApiVersionReader; select versions with the api-version query parameter. [Microsoft Azure REST API Guidelines — AZ-088](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#versioning-no-version-in-path)
- **api-version query parameter is not required on every operation** — API Design / Versioning (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs (+1 more), lines 31-35). Read the version only from the api-version query parameter and require it on every operation. [Microsoft Azure REST API Guidelines — AZ-085](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#versioning-api-version-query-param)
- **API versions use numeric 1.0 instead of date-based YYYY-MM-DD values** — API Design / Versioning (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 16-16). Adopt date-based version values (e.g. 2026-11-01, with -preview for previews). [Microsoft Azure REST API Guidelines — AZ-086](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#versioning-date-based-versioning)
- **Missing api-version silently falls back to the default instead of returning 400** — API Design / Versioning (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 35-36). Set AssumeDefaultVersionWhenUnspecified to false and return 400 with code MissingApiVersionParameter / UnsupportedApiVersionValue. [Microsoft Azure REST API Guidelines — AZ-087](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#versioning-api-version-missing)
- **Query parameter show-details is kebab-case, not camelCase** — API Design / Query parameters and headers (src/PilotUtiltyApi.Web/Controllers/SystemController.cs, lines 64-64). Rename the query parameter to showDetails (updating the spec and callers). [Microsoft Azure REST API Guidelines — AZ-020](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#http-query-names-casing)
- **AboutResponse sends null-valued fields to clients** — API Design / JSON representation (src/PilotUtiltyApi.Domain/Models/Responses/AboutResponse.cs (+1 more), lines 33-33). Omit null fields (e.g. JsonIgnore WhenWritingNull on all properties or a global DefaultIgnoreCondition) and drop null from the response schema types. [Microsoft Azure REST API Guidelines — AZ-054](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#json-null-response-values)
- **deployDate is an unformatted string copied from an environment variable, not RFC 3339** — API Design / JSON representation (src/PilotUtiltyApi.Web/Controllers/SystemController.cs (+1 more), lines 69-69). Parse the value into a DateTimeOffset, serialize it as RFC 3339, and declare format: date-time in the schema. [Microsoft Azure REST API Guidelines — AZ-058](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#json-date-time-is-rfc3339)
- **No x-ms-request-id is generated or returned; error responses carry no request identifier** — API Design / Correlation and telemetry (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs, lines 73-74). Generate an opaque request ID per request, return it in an x-ms-request-id response header, include it in error logs, and document the header in the spec. [Microsoft Azure REST API Guidelines — AZ-027](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#http-header-request-id)
- **No authentication or authorization is configured; there is no deny-by-default policy** — Security / Identity & Access (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs (+1 more), lines 112-126). Add authentication plus AddAuthorization with a FallbackPolicy requiring an authenticated user, call UseAuthentication/UseAuthorization, and keep [AllowAnonymous] only on truly public endpoints such as healthcheck (ASP-09, T10-01). [OWASP Authorization Cheat Sheet — ATZ-02](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#deny-by-default)
- **Anonymous POST /v1/testing/reset deletes rows across eight database tables** — Security / Identity & Access (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 15-19). Remove [AllowAnonymous] and require a named admin/test policy ([Authorize(Policy = "...")]) on the reset action, or exclude the controller from non-test environments (T10-04). [OWASP .NET Security Cheat Sheet — ASP-10](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html#authorization)
- **Anonymous GET /about?show-details=true returns the application configuration, including data-source details** — Security / Identity & Access (src/PilotUtiltyApi.Web/Controllers/SystemController.cs (+1 more), lines 60-64). Require an administrative policy for the show-details variant (or move it to a separate protected endpoint) and keep the anonymous response to name and version only. [OWASP .NET Security Cheat Sheet — ASP-10](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html#authorization)

### Warnings

- **ResetTestingAsync mixes configuration lookup, connection construction, transaction handling, execution and error mapping in one body [ISO 25010:2023 Maintainability › Modifiability, ISO-30]** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs, lines 57-125). Apply Split Phase (FRC-02, https://refactoring.com/catalog/splitPhase.html): move connection creation/opening into a connection factory and keep the method to executing the script inside a transaction. [Compliance Reviewer Software Quality Rubric — SQR-02](../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-02)
- **The same switch on DataSourceType.ToLowerInvariant() is repeated in three methods [ISO 25010:2023 Maintainability › Modifiability, ISO-30]** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+2 more), lines 138-156). Apply Replace Conditional with Polymorphism (FRC-06, https://refactoring.com/catalog/replaceConditionalWithPolymorphism.html): introduce a per-provider type (SQL Server, PostgreSQL) that supplies the connection string, connection and reset script, so adding a provider touches one class. [Compliance Reviewer Software Quality Rubric — SQR-07](../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-07)
- **Nested catch (Exception) blocks without filters inside the repository [ISO 25010:2023 Reliability › Fault tolerance, ISO-19]** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+1 more), lines 92-103). Catch the provider exceptions you can handle (DbException, OperationCanceledException) or use an exception filter, and let the existing UnhandledExceptionMiddleware handle the rest; use ArgumentNullException for null arguments. [Microsoft C# conventions — MSC-09](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions#language-guidelines)
- **Nullable reference types enabled but key nullable warnings downgraded to suggestions** — Software Quality / Coding Standards (Directory.Build.props (+1 more), lines 5-5). Restore CS8602/CS8604 to warning (or error) and fix the flagged dereferences, e.g. DataSources.FirstOrDefault in TestingRepository. [Compliance Reviewer Software Quality Rubric — SQR-36](../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-36)
- **var used where the type isn't apparent, contrary to the documented explicit-type convention** — Software Quality / Coding Standards (.editorconfig (+2 more), lines 92-94). Use explicit types where the right side doesn't show the type (or change the .editorconfig preference to match practice), and stop silencing IDE0008 so the chosen rule is enforced. [Microsoft C# conventions — MSC-12](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions#implicitly-typed-local-variables)
- **No CODEOWNERS file on a GitHub repository, so pipeline and build files have no required code-owner review** — Software Lifecycle / Branch Protection (.github/workflows/dotnet.yml, lines 6-10). Add .github/CODEOWNERS with a '*' rule and an explicit rule for .github/workflows/ and Directory.Build.props, then require code-owner review on main. [OpenSSF Scorecard v5.6.0 — OSC-04](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#branch-protection)
- **Workflow declares no permissions block, so the GITHUB_TOKEN inherits the repository default scope** — Software Lifecycle / Pipeline Hardening (.github/workflows/dotnet.yml, lines 4-15). Add a top-level 'permissions: contents: read' (or 'permissions: {}') and grant any write scopes per job only where needed. [OpenSSF Scorecard v5.6.0 — OSC-09](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#token-permissions)
- **Actions are pinned to mutable major-version tags instead of full commit SHAs** — Software Lifecycle / Pipeline Hardening (.github/workflows/dotnet.yml, lines 18-20). Pin each action to a 40-character commit SHA with a version comment (e.g. actions/checkout@<sha> # v4.x.y) and let an update bot refresh the pins. [OpenSSF Scorecard v5.6.0 — OSC-11](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#pinned-dependencies)
- **No static security analysis (SAST) runs in CI on pull requests or pushes** — Software Lifecycle / Static Analysis (.github/workflows/dotnet.yml, lines 23-28). Add a CodeQL workflow (github/codeql-action init + analyze for csharp) on pull_request and push to main, uploading SARIF results, and define the severity that blocks a merge. [OpenSSF Scorecard v5.6.0 — OSC-14](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#sast)
- **Compiler warnings are not treated as errors in the shared build configuration** — Software Lifecycle / Static Analysis (Directory.Build.props, lines 2-9). Set <TreatWarningsAsErrors>true</TreatWarningsAsErrors> (at least for CI builds, e.g. conditioned on ContinuousIntegrationBuild) and an <AnalysisLevel> in Directory.Build.props so security analyzer warnings fail the build. [NIST SSDF 1.1 — SSDF-04](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf#page=23)
- **Production base config writes and rotates log files via the Serilog File sink** — Twelve-Factor / XI. Logs (src/PilotUtiltyApi.Web/appsettings.json, lines 58-65). Keep only the Console sink (and the OTLP exporter) in appsettings.json and move the File sink to appsettings.Development.json, letting the platform capture and route stdout. [Compliance Reviewer Twelve-Factor Rubric — TFR-19](../../compliance-reviewer/skills/review-twelve-factor/references/standards/twelve-factor-rubric.md#tfr-19)
- **Reset action is a plain path segment instead of the :action pattern** — API Design / URLs and resources (src/PilotUtiltyApi.Web/Controllers/TestingController.cs, lines 46-47). Expose the action as POST /<collection>:reset (e.g. /test-data:reset) so actions are distinguishable from resources. [Microsoft Azure REST API Guidelines — AZ-069](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#actions-url-pattern-for-resource-action)
- **HTTPS redirection is enabled only in Development; the production pipeline has no HTTPS enforcement** — Security / Web & API (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 73-76). Invert the condition so HTTPS is enforced outside Development; for this API prefer listening on HTTPS only or rejecting HTTP with 400 rather than redirecting (DNW-01, DNW-02, TLS-04). If a reverse proxy outside the repository enforces HTTPS, record that in the repository. [OWASP Transport Layer Security Cheat Sheet — TLS-03](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html#use-tls-for-all-pages)
- **Swagger UI is enabled in every environment, including production** — Security / Web & API (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs (+1 more), lines 80-82). Map Swagger UI (and the OpenAPI document, if not intentionally public) only in Development or behind authorization in production. [OWASP Top 10:2025 A02 — A02-03](https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/#description)
- **coverlet.collector is referenced but coverage is never collected or published in CI** — Testing / Coverage (.github/workflows/dotnet.yml (+1 more), lines 27-28). Run `dotnet test --collect:"XPlat Code Coverage"` in CI and publish the result (reportgenerator artifact, PR comment or Codecov upload) so untested code is visible. [Compliance Reviewer Testing Rubric — TSR-04](../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-04)
- **Placeholder test always passes and a controller test cannot detect the behaviour its name claims** — Testing / Assertion quality (test/PilotUtiltyApi.Domain.Tests/ExampleTest.cs (+1 more), lines 9-14). Delete the Assert.Pass placeholder or replace it with a real Domain test; make the null-message controller test stub a null ErrorMessage and assert the actual default Warning value. [Compliance Reviewer Testing Rubric — TSR-07](../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-07)
- **No automated acceptance-level tests; the Bruno collection has no assertions and is not run in CI** — Testing / Coverage of production modules (test/Bruno/PilotUtilityApi/v1/Testing/TestingReset.yml (+1 more), lines 6-9). Add acceptance tests for the reset feature, e.g. WebApplicationFactory-based API tests or Bruno requests with assertions run by the Bruno CLI in CI. [Martin Fowler (martinfowler.com) — MFT-15](https://martinfowler.com/articles/practical-test-pyramid.html#acceptance)
- **Data access is never exercised against a real database engine** — Testing / Integration and contract tests (test/PilotUtiltyApi.Repositories.Tests/Repositories/TestingRepositoryTests.cs (+1 more), lines 51-72). Add an integration test project that runs TestingRepository.ResetTestingAsync against SQL Server and PostgreSQL in containers (e.g. Testcontainers), covering the success path. [Compliance Reviewer Testing Rubric — TSR-18](../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-18)
- **No test verifies that failures become a generic error response; tests assert the raw error is echoed in a header** — Testing / Security tests (test/PilotUtiltyApi.Web.Tests/Controllers/TestingControllerTests.cs, lines 91-110). Add tests that throw from the service/repository and assert the API returns a generic error body without internal details (exception text, connection info). [Compliance Reviewer Testing Rubric — TSR-22](../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-22)
- **Health check returns a constant 200 "OK" and does not reflect the required database dependency** — Observability / Health Endpoints (src/PilotUtiltyApi.Web/Controllers/SystemController.cs, lines 43-49). Use ASP.NET Core health checks (AddHealthChecks with a SQL Server/PostgreSQL check, tagged and time-bounded) and map separate shallow liveness and dependency-aware readiness endpoints that return 503 on failure. [Azure Well-Architected Framework — WAFO-16](https://learn.microsoft.com/azure/well-architected/design-guides/health-modeling#use-health-probes)
- **Anonymous status endpoint /about returns versions, database type and, on request, application configuration** — Observability / Health Endpoints (src/PilotUtiltyApi.Web/Controllers/SystemController.cs (+1 more), lines 18-18). Require authorization for the /about endpoint (at least for show-details=true) and keep anonymous system responses limited to the status a probe needs. [Azure Well-Architected Framework — WAFO-37](https://learn.microsoft.com/azure/architecture/patterns/health-endpoint-monitoring#problems-and-considerations)
- **The .NET SDK (build tooling) isn't pinned; there's no global.json** — Implementation / Dependency Management (Directory.Build.props, lines 2-4). Add a root global.json that pins the .NET 10 SDK version, with a narrow rollForward policy such as latestPatch, so every build uses the same, inventoried toolchain. [OWASP Software Supply Chain Security Cheat Sheet — OCS-15](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html#inventory-build-tools)
- **No repository nuget.config with <clear/> or package source mapping, so the package feed setup isn't controlled by the repo** — Implementation / Dependency Management (Directory.Packages.props, lines 5-8). Add a root nuget.config that clears inherited sources, declares only the trusted HTTPS feed(s) with packageSourceMapping, and consider signatureValidationMode=require with trustedSigners. [OWASP Software Supply Chain Security Cheat Sheet — OCS-13](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html#use-private-artifact-repository)
- **Database call on the request path has no transient-fault retry** — Reliability / Transient-fault retries (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+1 more), lines 73-89). Add a retry for transient SQL/Npgsql errors (driver-level retry logic or a Polly pipeline with finite attempts, exponential back-off and jitter, configured centrally) that wraps the whole open-connection/transaction unit rather than a single statement. [Azure Architecture Center — AZRL-05](https://learn.microsoft.com/azure/architecture/best-practices/transient-faults#check-whether-a-built-in-retry-mechanism-exists)
- **README does not link to CONTRIBUTING.md or the docs/ folder** — Maintainability / README & Onboarding (README.md (+1 more), lines 5-20). Add a 'Contributing' and 'Further documentation' section to the README linking CONTRIBUTING.md and the docs/ content (OpenAPI spec, history). [Compliance Reviewer Maintainability Rubric — MR-06](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-06)
- **Application.OpenTelemetry config keys are not documented** — Maintainability / Prerequisites & Configuration (src/PilotUtiltyApi.Web/appsettings.Development.json (+1 more), lines 27-30). Document the Application.OpenTelemetry section (Server, Port: purpose, defaults, whether a collector is required locally) in the README Configuration section. [Compliance Reviewer Maintainability Rubric — MR-14](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-14)
- **No setup steps or local stack for the required SQL Server/PostgreSQL database** — Maintainability / Prerequisites & Configuration (README.md, lines 84-86). Add steps (or a docker-compose file) to create the NorthWind database, the DevUser login, the pilot schema and the tables the reset script targets. [Compliance Reviewer Maintainability Rubric — MR-16](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-16)
- **README paths use src/PilotUtilityApi.Web, but the folder is src/PilotUtiltyApi.Web** — Maintainability / Docs Accuracy (README.md (+2 more), lines 112-117). Fix the paths to src/PilotUtiltyApi.Web (or rename the folder) so the documented `cd` command and file locations work. [Compliance Reviewer Maintainability Rubric — MR-33](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-33)
- **Documented URLs/ports (58701, 58401, 7000, https) don't match launchSettings (http://localhost:58301)** — Maintainability / Docs Accuracy (README.md (+2 more), lines 121-122). Use the launch profile's URL (http://localhost:58301) consistently in all README examples. [Compliance Reviewer Maintainability Rubric — MR-33](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-33)
- **CONTRIBUTING links README.md#copilot-customization, a section that does not exist** — Maintainability / Docs Accuracy (CONTRIBUTING.md, lines 14-14). Add a 'Copilot Customization' README section describing .github/instructions, or repoint the link at .github/copilot-instructions.md. [Compliance Reviewer Maintainability Rubric — MR-36](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-36)

### Information

- **TestingService is a pass-through tier that only forwards to the repository [ISO 25010:2023 Maintainability › Analysability, ISO-29]** — Software Quality / Design Patterns (src/PilotUtiltyApi.Services/Services/TestingService.cs, lines 49-52). Either give the service real responsibility (e.g. environment guard, auditing of the reset) or apply Remove Middle Man (FRC-19, https://refactoring.com/catalog/removeMiddleMan.html); its injected logger is also unused. [Compliance Reviewer Software Quality Rubric — SQR-23](../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-23)
- **Inconsistent names: 'PilotUtiltyApi' project folders vs 'PilotUtilityApi' projects/namespaces, and a Dto namespace in a Responses folder** — Software Quality / Coding Standards (src/PilotUtiltyApi.Web/PilotUtilityApi.Web.csproj (+1 more), lines 12-14). Apply Rename (FRC-22, https://refactoring.com/catalog/renameField.html): rename the 'PilotUtilty' folders to match the project names, and align AboutResponse's namespace with its folder (the .editorconfig already sets dotnet_style_namespace_match_folder = true). [Compliance Reviewer Software Quality Rubric — SQR-32](../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-32)
- **No SECURITY.md security policy in the root, .github/ or docs/** — Software Lifecycle / Security Policy (.github/workflows/dotnet.yml, lines 4-4). Add SECURITY.md with a private reporting channel (email or GitHub private vulnerability reporting), the handling process, disclosure expectations and supported versions. [OpenSSF Scorecard v5.6.0 — OSC-15](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#security-policy)
- **DataSourceConfiguration arrange blocks (>10 lines) are copied across many tests with no builder** — Testing / Test code quality (test/PilotUtiltyApi.Shared.Tests/Configuration/ApplicationConfigurationTests.cs (+1 more), lines 44-56). Add a DataSourceConfiguration builder or factory in PilotUtilityApi.TestingShared that returns a valid default, so each test sets only the property under test. [Compliance Reviewer Testing Rubric — TSR-17](../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-17)
- **Misleading test name with unused arrange code, and a non-descriptive placeholder test name** — Testing / Test code quality (test/PilotUtiltyApi.Web.Tests/Controllers/TestingControllerTests.cs (+1 more), lines 117-121). Remove the unused expectedResult and align the test name with the scenario actually arranged; rename or remove the example test. [Microsoft .NET unit testing best practices — MSU-08](https://learn.microsoft.com/dotnet/core/testing/unit-testing-best-practices#follow-test-naming-standards)
- **The deployable web API has no automated load or performance tests** — Testing / Load and performance tests (.github/workflows/dotnet.yml, lines 12-28). Add a small k6 or NBomber script for the API endpoints with p95 latency and error-rate thresholds, run on a schedule against a production-like environment. [Azure Well-Architected Framework — AZT-01](https://learn.microsoft.com/azure/well-architected/performance-efficiency/performance-test#apply-multiple-performance-test-types)
- **OTLP exporter scheme and protocol are hard-coded in code rather than taken from configuration** — Observability / Telemetry Export (src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs (+1 more), lines 52-52). Make the full endpoint (including scheme), protocol and timeout configurable (e.g. an Endpoint/Protocol setting or the standard OTEL_EXPORTER_OTLP_* variables) so environments can switch to TLS or gRPC without a code change. [OpenTelemetry — OTO-29](https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/#endpoint-configuration)
- **No SLOs or SLIs are documented for the service** — Observability / SLOs & SLIs (README.md, lines 266-272). Document availability, success-rate and p95/p99 latency targets for the API and its reset flow, with the SLIs (e.g. http.server.request.duration) and measurement window used to evaluate them. [Azure Well-Architected Framework — WAFO-19](https://learn.microsoft.com/azure/well-architected/reliability/metrics#define-composite-slo-targets)
- **service.version comes from a hand-maintained OpenAPI config value instead of the deployed build version** — Observability / Telemetry Identity & Naming (src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs (+2 more), lines 65-69). Set serviceVersion from the assembly/build version (e.g. FileUtilities.GetApplicationVersion(), already used by /about) so telemetry identifies the actual deployed artifact. [OpenTelemetry — OTO-32](https://opentelemetry.io/docs/specs/semconv/registry/attributes/service/#service-attributes)
- **Documented structure names PilotUtilityApi.* folders but actual folders are misspelled PilotUtiltyApi.*** — Maintainability / Repository Layout (README.md (+1 more), lines 49-49). Rename the src/ and test/ folders to PilotUtilityApi.* to match the project names and the documented structure (updating the .sln paths), or correct the README tree. [Compliance Reviewer Maintainability Rubric — MR-10](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-10)
- **Runtime log output (13 files in src/PilotUtiltyApi.Web/logs/) is kept in the source tree** — Maintainability / Repository Layout (src/PilotUtiltyApi.Web/appsettings.json, lines 59-61). Delete the generated log files from the repository, ignore the logs/ folder, and point the Serilog file sink outside the project directory. [Compliance Reviewer Maintainability Rubric — MR-11](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-11)
- **CONTRIBUTING gives no pre-submit build, format or test commands** — Maintainability / Contributing Guide (CONTRIBUTING.md, lines 10-11). Replace the generic container boilerplate with the required pre-PR steps, e.g. `dotnet format --verify-no-changes`, `dotnet build` and `dotnet test`. [Compliance Reviewer Maintainability Rubric — MR-25](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-25)
- **CONTRIBUTING does not state coding conventions or point to .editorconfig** — Maintainability / Contributing Guide (CONTRIBUTING.md, lines 8-18). Add a 'Coding conventions' section referencing .editorconfig and the .github/instructions files. [Compliance Reviewer Maintainability Rubric — MR-26](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-26)
- **No CHANGELOG or release notes although the project is versioned with SemVer** — Maintainability / Change History (Directory.Build.props (+1 more), lines 3-3). Add a CHANGELOG.md with dated per-version entries (starting at 1.0.1) and link it from the README. [Compliance Reviewer Maintainability Rubric — MR-27](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-27)
- **Significant decisions (Dapper, multi-database, layering) are not recorded with context and consequences** — Maintainability / Architecture Docs (.github/instructions/architecture.instructions.md, lines 35-35). Add short ADRs under docs/adr/ for key choices (Dapper over EF, dual SQL Server/PostgreSQL support, layer split) with context and consequences. [Compliance Reviewer Maintainability Rubric — MR-31](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-31)

## 4. Full Results

### Software Quality

#### Software Quality

| Check | Result | Evidence |
|-------|--------|----------|
| SQ-01 | fail | ResetTestingAsync (~55 logical lines) interleaves connection setup, transaction control and error mapping. |
| SQ-02 | pass |  |
| SQ-03 | fail | Same data-source-type switch repeated in three methods. |
| SQ-04 | pass |  |
| SQ-05 | fail | duplicate evidence of SEC-IA-02#2, see Security/Identity & Access |
| SQ-06 | fail | Unfiltered catch (Exception) blocks nested inside the repository. |
| SQ-08 | pass |  |

#### Design Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| DP-01 | pass |  |
| DP-02 | N/A | No project-defined class hierarchies in the reviewed files (only framework base classes). |
| DP-04 | fail | TestingService only forwards calls to the repository. |
| DP-05 | pass |  |
| DP-06 | N/A | No event or observer subscriptions in the reviewed files. |

#### Architecture Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| AP-01 | pass |  |
| AP-02 | pass |  |
| AP-03 | pass |  |
| AP-04 | pass |  |
| AP-06 | pass |  |
| AP-07 | N/A | Only one deployable unit (the Web project) in the reviewed files. |

#### Coding Standards

| Check | Result | Evidence |
|-------|--------|----------|
| CS-01 | fail | Project folder names and a namespace are inconsistent with the projects and folders they belong to. |
| CS-02 | pass |  |
| CS-03 | fail | duplicate evidence of OBS-06#1, see Observability/Health Endpoints |
| CS-04 | pass |  |
| CS-05 | fail | Nullable warnings downgraded and var used against the documented convention. |

### Software Lifecycle

#### Continuous Integration

| Check | Result | Evidence |
|-------|--------|----------|
| SL-01 | pass |  |

#### Release Automation

| Check | Result | Evidence |
|-------|--------|----------|
| SL-02 | N/A | Repo publishes no versioned artifacts: no release, packaging or production deployment pipeline is in scope. |

#### Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| SL-03 | pass |  |

#### Branch Protection

| Check | Result | Evidence |
|-------|--------|----------|
| SL-04 | fail | GitHub repository has no CODEOWNERS file; settings-as-code elements skipped (repository settings not visible in files). |

#### Provenance and Signing

| Check | Result | Evidence |
|-------|--------|----------|
| SL-05 | N/A | Repo publishes no versioned artifacts. |

#### Security Policy

| Check | Result | Evidence |
|-------|--------|----------|
| SL-07 | fail | No SECURITY.md exists in the root, .github/ or docs/. |

#### Pipeline Hardening

| Check | Result | Evidence |
|-------|--------|----------|
| SL-09 | pass |  |
| SL-10 | fail | No permissions block (OSC-09) and actions pinned to mutable @v4 tags (OSC-11). |

#### Static Analysis

| Check | Result | Evidence |
|-------|--------|----------|
| SL-11 | fail | No SAST step in CI (OSC-14, SSDF-16) and warnings are not treated as errors (SSDF-04). |

#### Committed Binaries

| Check | Result | Evidence |
|-------|--------|----------|
| SL-12 | pass |  |

### Twelve-Factor

#### I. Codebase

| Check | Result | Evidence |
|-------|--------|----------|
| TF-01 | pass |  |

#### II. Dependencies

| Check | Result | Evidence |
|-------|--------|----------|
| TF-02 | pass |  |

#### III. Config

| Check | Result | Evidence |
|-------|--------|----------|
| TF-03 | pass |  |

#### IV. Backing services

| Check | Result | Evidence |
|-------|--------|----------|
| TF-04 | pass |  |

#### V. Build, release, run

| Check | Result | Evidence |
|-------|--------|----------|
| TF-05 | N/A | No Dockerfile, manifest or deploy step visible; CI only builds and tests. |

#### VI. Processes

| Check | Result | Evidence |
|-------|--------|----------|
| TF-06 | pass |  |

#### VII. Port binding

| Check | Result | Evidence |
|-------|--------|----------|
| TF-07 | pass |  |

#### VIII. Concurrency

| Check | Result | Evidence |
|-------|--------|----------|
| TF-08 | pass |  |

#### IX. Disposability

| Check | Result | Evidence |
|-------|--------|----------|
| TF-09 | pass |  |

#### X. Dev/prod parity

| Check | Result | Evidence |
|-------|--------|----------|
| TF-10 | N/A | Production backing-service definition not visible. |

#### XI. Logs

| Check | Result | Evidence |
|-------|--------|----------|
| TF-11 | fail | Serilog File sink with rotation is configured in the production base appsettings.json. |

#### XII. Admin processes

| Check | Result | Evidence |
|-------|--------|----------|
| TF-12 | N/A | No admin or migration tasks visible in the subject's files. |

### API Design

#### OpenAPI Specification

| Check | Result | Evidence |
|-------|--------|----------|
| API-01 | pass |  |
| API-02 | pass |  |
| API-03 | fail | Spec drifts from code in the reset path, show-details required-ness, AboutResponse schema and undocumented 500 responses. |

#### URLs and resources

| Check | Result | Evidence |
|-------|--------|----------|
| API-04 | fail | The reset action uses a path segment instead of the :action pattern. |

#### Status codes and errors

| Check | Result | Evidence |
|-------|--------|----------|
| API-05 | fail | POST action returns 204, errors lack the standard error body and x-ms-error-code header. |

#### Pagination

| Check | Result | Evidence |
|-------|--------|----------|
| API-06 | N/A | No collection/list endpoints exist. |

#### Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| API-07 | fail | Version is in the path, not date-based, not required and defaults when missing. |

#### Query options

| Check | Result | Evidence |
|-------|--------|----------|
| API-08 | N/A | No filtering, sorting or field selection is offered. |

#### Resource design

| Check | Result | Evidence |
|-------|--------|----------|
| API-09 | pass |  |

#### Query parameters and headers

| Check | Result | Evidence |
|-------|--------|----------|
| API-10 | fail | Query parameter show-details is not camelCase. |

#### JSON representation

| Check | Result | Evidence |
|-------|--------|----------|
| API-11 | fail | Null fields are sent and deployDate is not RFC 3339. |

#### Enums and polymorphism

| Check | Result | Evidence |
|-------|--------|----------|
| API-12 | N/A | No enums or polymorphic types in the API contract. |

#### Long-running operations

| Check | Result | Evidence |
|-------|--------|----------|
| API-13 | N/A | No long-running operations exist. |

#### Conditional requests

| Check | Result | Evidence |
|-------|--------|----------|
| API-14 | N/A | Only utility endpoints (health, about, reset); no resource representations to version with ETags. |

#### Correlation and telemetry

| Check | Result | Evidence |
|-------|--------|----------|
| API-15 | fail | No request ID is generated or returned in x-ms-request-id. |

### Security

#### Identity & Access

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-IA-01 | fail | No authentication/authorization services, middleware or fallback policy. |
| SEC-IA-02 | fail | Destructive reset and configuration-disclosure functions are anonymous. |
| SEC-IA-03 | N/A | No JWTs are handled. |
| SEC-IA-04 | N/A | No OAuth 2.0/OIDC is used. |
| SEC-IA-05 | N/A | No sessions or authentication cookies. |
| SEC-IA-06 | N/A | The target stores no user passwords. |
| SEC-IA-07 | N/A | No authentication, session or credential scheme is implemented. |
| SEC-IA-08 | N/A | No service-to-service calls, roles, scopes or tokens in the reviewed files. |
| SEC-IA-09 | N/A | No login or access-control failure paths exist. |
| SEC-IA-10 | N/A | No user credential management; appsettings.json holds only a placeholder database password. |
| SEC-IA-11 | N/A | No client-side tokens or credential paths. |

#### Input & Injection

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-II-01 | pass |  |
| SEC-II-02 | pass |  |
| SEC-II-03 | pass |  |
| SEC-II-04 | N/A | No OS command or other interpreter invocation in the reviewed files. |
| SEC-II-05 | N/A | No XML is parsed. |
| SEC-II-06 | N/A | No file uploads. |
| SEC-II-07 | N/A | No file uploads. |
| SEC-II-08 | N/A | Nothing is rendered to HTML; JSON API only. |
| SEC-II-09 | N/A | Nothing deserialized beyond plain JSON/query binding into typed values. |
| SEC-II-10 | N/A | No outbound request uses a URL or host derived from untrusted data. |

#### Web & API

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-WA-01 | N/A | API-only: browser-rendering headers not applicable (hdr#content-security-policy-csp, rst#security-headers). |
| SEC-WA-02 | pass |  |
| SEC-WA-03 | fail | duplicate evidence of SEC-IA-01#1, see Security/Identity & Access |
| SEC-WA-04 | N/A | API-only: browser-rendering headers not applicable (hdr#content-security-policy-csp, rst#security-headers). |
| SEC-WA-05 | pass |  |
| SEC-WA-06 | fail | UseHttpsRedirection runs only in Development, leaving the production pipeline without HTTPS enforcement. |
| SEC-WA-07 | pass |  |
| SEC-WA-08 | fail | duplicate evidence of SEC-IA-01#1, see Security/Identity & Access |
| SEC-WA-09 | fail | Swagger UI is exposed in all environments (unnecessary feature enabled). |
| SEC-WA-10 | pass |  |
| SEC-WA-11 | N/A | API-only: browser-rendering headers not applicable (hdr#content-security-policy-csp, rst#security-headers). |

#### Operational

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-OP-01 | pass |  |
| SEC-OP-02 | pass |  |
| SEC-OP-03 | pass |  |
| SEC-OP-04 | pass |  |
| SEC-OP-05 | fail | duplicate evidence of SL-11#1, see Software Lifecycle/Static Analysis |
| SEC-OP-06 | pass |  |
| SEC-OP-07 | fail | duplicate evidence of SEC-IA-02#1, see Security/Identity & Access |
| SEC-OP-08 | pass |  |
| SEC-OP-09 | pass |  |
| SEC-OP-10 | N/A | No multi-step writes, transactions or security decisions in the subject's files (reset logic lives in a service outside scope). |

### Testing

#### Test pyramid

| Check | Result | Evidence |
|-------|--------|----------|
| TST-01 | pass |  |

#### Coverage

| Check | Result | Evidence |
|-------|--------|----------|
| TST-02 | fail | coverlet.collector is referenced but CI never collects or publishes coverage. |

#### Assertion quality

| Check | Result | Evidence |
|-------|--------|----------|
| TST-03 | fail | An Assert.Pass placeholder test and a controller test whose arrangement cannot detect its named behaviour. |

#### Test doubles

| Check | Result | Evidence |
|-------|--------|----------|
| TST-04 | pass |  |

#### Isolation and determinism

| Check | Result | Evidence |
|-------|--------|----------|
| TST-05 | pass |  |

#### CI execution

| Check | Result | Evidence |
|-------|--------|----------|
| TST-06 | pass |  |

#### Coverage of production modules

| Check | Result | Evidence |
|-------|--------|----------|
| TST-07 | fail | Every production root has a test project, but no automated acceptance-level tests exist. |

#### Test code quality

| Check | Result | Evidence |
|-------|--------|----------|
| TST-08 | fail | Copied >10-line arrange blocks without a builder, and a misleading test name with dead arrange code. |

#### Integration and contract tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-09 | fail | A database is used but no repository test runs against a real engine (0 integration tests). |

#### Security tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-10 | fail | No access control (authorization elements N/A); no test checks that failures become a generic error response. |
| TST-11 | fail | duplicate evidence of SL-11#1, see Software Lifecycle/Static Analysis |

#### Load and performance tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-12 | fail | Deployable web API with no load-test signals in the sample or inventory. |

#### Resilience tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-13 | pass |  |

### Observability

#### Structured Logging

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-01 | pass |  |

#### Correlation & Context Propagation

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-02 | fail | duplicate evidence of API-15#1, see API Design/Correlation and telemetry |

#### Distributed Tracing

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-03 | pass |  |

#### Metrics

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-04 | pass |  |

#### Telemetry Export

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-05 | fail | OTLP scheme (http) and protocol are hard-coded; only host and port come from configuration. |

#### Health Endpoints

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-06 | fail | Health check is a constant 200 despite a required database, and the anonymous /about endpoint exposes diagnostic detail. |

#### SLOs & SLIs

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-07 | fail | README states no SLO targets or SLIs for the deployable API. |

#### Telemetry Identity & Naming

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-08 | fail | service.version is a hand-maintained config constant rather than the deployed artifact version. |

#### Error Recording

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-09 | pass |  |

#### Telemetry Volume & Safety

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-10 | pass |  |

### Implementation

#### Dependency Management

| Check | Result | Evidence |
|-------|--------|----------|
| DEP-01 | fail | All packages use exact versions, but the .NET SDK build tooling isn't pinned because there's no global.json. |
| DEP-02 | fail | duplicate evidence of SL-11#2, see Software Lifecycle/Static Analysis |
| DEP-03 | N/A | No vulnerability analyzer output for this run. |
| DEP-04 | pass |  |
| DEP-05 | fail | duplicate evidence of SL-11#2, see Software Lifecycle/Static Analysis |
| DEP-07 | N/A | No dependency-update or scanning config (Dependabot, Renovate, NuGetAudit settings, suppressions) is in the file list. |
| DEP-08 | fail | No repo-level nuget.config with <clear/> or package source mapping, so feed selection isn't enforced; no http feeds or vendored binaries found. |
| DEP-09 | pass |  |

### Reliability

#### Timeouts

| Check | Result | Evidence |
|-------|--------|----------|
| REL-01 | pass |  |

#### Transient-fault retries

| Check | Result | Evidence |
|-------|--------|----------|
| REL-02 | fail | Request-path database call has no retry and no built-in driver retry is configured (AZRL-05); AZRL-06…14 not applicable without retry logic. |

#### Idempotency

| Check | Result | Evidence |
|-------|--------|----------|
| REL-03 | N/A | No retries, redelivery or distributed multi-step workflows in scope, so no AZRL-15…20 element applies. |

#### Circuit breakers

| Check | Result | Evidence |
|-------|--------|----------|
| REL-04 | fail | duplicate evidence of SEC-IA-01#1, see Security/Identity & Access |

#### Redundancy

| Check | Result | Evidence |
|-------|--------|----------|
| REL-05 | N/A | IaC not reviewed (advanced usage off); no deployment config in scope and no singleton component in code. |

#### Load protection

| Check | Result | Evidence |
|-------|--------|----------|
| REL-06 | fail | duplicate evidence of SEC-IA-01#1, see Security/Identity & Access |

#### Messaging and background jobs

| Check | Result | Evidence |
|-------|--------|----------|
| REL-07 | N/A | No message consumers or background jobs in scope. |

#### In-region high availability

| Check | Result | Evidence |
|-------|--------|----------|
| REL-08 | N/A | IaC not reviewed (advanced usage off). |

### Operations

#### Performance

| Check | Result | Evidence |
|-------|--------|----------|
| PERF-01 | N/A | No repeated expensive reads or caches in the reviewed request paths; HTTP API caching headers judged by review-api-design. |
| PERF-02 | fail | duplicate evidence of CS-05#2, see Software Quality/Coding Standards |
| PERF-03 | fail | duplicate evidence of CS-05#2, see Software Quality/Coding Standards |
| PERF-04 | pass |  |
| PERF-05 | N/A | No loops over data in request paths in the reviewed files. |
| PERF-06 | pass |  |
| PERF-07 | pass |  |
| PERF-08 | N/A | No hosting/scaling config, static assets or processing pipelines in scope. |

### Disaster Recovery

#### Disaster Recovery

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | advanced usage off (IaC not reviewed) |

### Monitoring

#### Monitoring

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | advanced usage off (IaC not reviewed) |

### Cost & Sustainability

#### Cost & Sustainability

| Check | Result | Evidence |
|-------|--------|----------|
| N/A | N/A | advanced usage off (IaC not reviewed) |

### Maintainability

#### README & Onboarding

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-01 | fail | README covers purpose, setup, run and test but does not link CONTRIBUTING or docs (MR-06). |

#### Repository Layout

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-02 | fail | Folder names diverge from documented/project names (MR-10) and runtime logs sit in the source tree (MR-11). |

#### Prerequisites & Configuration

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-03 | fail | OpenTelemetry keys undocumented (MR-14) and no database setup steps or local stack (MR-16). |

#### Technical Debt

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-04 | N/A | No debt markers or warning suppressions in the 3 reviewed source files. |

#### Deprecated Code

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-05 | N/A | No deprecated, legacy-named or versioned copies in the reviewed files. |

#### Contributing Guide

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-06 | fail | CONTRIBUTING has a PR process but no pre-submit commands (MR-25) or conventions (MR-26). |

#### Change History

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-07 | fail | Versioned (1.0.1, SemVer) but no CHANGELOG or release notes (MR-27). |

#### Architecture Docs

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-08 | fail | README architecture overview exists, but no recorded decisions with context (MR-31). |

#### Docs Accuracy

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-09 | fail | Wrong Web project paths and ports (MR-33) and a broken README anchor link (MR-36). |

#### License & Conduct

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-10 | pass |  |

## 5. Appendix

- **Run:** `2026-11-09_2035-PilotUtilityApi` · Target: `C:\Working\Storage\Dev\GitHub\PilotUtilityApi` · Git HEAD: `59fedaa36172568260fd667103313ee95af13a16`
- **Started:** 2026-11-09T20:35:41-07:00 · **Completed:** 2026-11-09T20:44:31-07:00
- **Run flags:** advanced off (IaC and CLI analyzers not run)
- **Subjects skipped:** review-disaster-recovery (advanced usage off (IaC not reviewed)); review-monitoring (advanced usage off (IaC not reviewed)); review-cost-sustainability (advanced usage off (IaC not reviewed))
- **URLs fetched:** none
- **Link approvals:** none
