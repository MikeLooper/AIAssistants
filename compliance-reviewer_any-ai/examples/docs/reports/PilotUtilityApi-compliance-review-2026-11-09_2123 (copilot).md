# PilotUtilityApi — Compliance Review

_Generated 2026-11-09T21:41:01-07:00 · Run `2026-11-09_2123-PilotUtilityApi`_

## 1. Summary

**Overall score: 53.36/100 — Poor**

| Subject | Score | Band |
|---------|-------|------|
| Software Quality | 70.97/100 | Fair |
| Software Lifecycle | 65.00/100 | Fair |
| Twelve-Factor | 90.91/100 | Excellent |
| API Design | 29.27/100 | Poor |
| Security / Identity & Access | 0.00/100 | Poor |
| Security | 51.39/100 | Poor |
| Testing | 68.00/100 | Fair |
| Observability | 56.25/100 | Poor |
| Implementation | 64.29/100 | Fair |
| Operations / Reliability | 45.45/100 | Poor |
| Operations / Performance | 60.00/100 | Fair |
| Maintainability | 9.09/100 | Poor |

**Findings by severity:** Error: 20 · Warning: 30 · Information: 13

### Top 5 Risks

1. **[Error] Spec documents /testing/reset but the controller route is /v{version}/testing/reset** — API Design / Spec ↔ Implementation (docs/PilotUtilityApi_v1.json (+1 more)). Regenerate the committed spec from the running app (or fix the route) so the documented path matches the implemented route exactly. [OpenAPI Specification — OAS-38](https://spec.openapis.org/oas/v3.1.2.html#paths-object)
1. **[Error] show-details is [BindRequired] in code but optional with a default in the spec** — API Design / Spec ↔ Implementation (src/PilotUtiltyApi.Web/Controllers/SystemController.cs (+1 more)). Decide whether the parameter is optional; either drop [BindRequired] (keeping the default) or mark it required: true in the spec without a default. [OpenAPI Specification — OAS-39](https://spec.openapis.org/oas/v3.1.2.html#parameter-object)
1. **[Error] AboutResponse.ApplicationConfiguration is returned but absent from the spec schema** — API Design / Spec ↔ Implementation (src/PilotUtiltyApi.Domain/Models/Responses/AboutResponse.cs (+1 more)). Add the applicationConfiguration property (with its schema) to AboutResponse in the spec, or stop returning it. [OpenAPI Specification — OAS-40](https://spec.openapis.org/oas/v3.1.2.html#schema-object)
1. **[Error] 500 ProblemDetails responses from the exception middleware are not documented** — API Design / Spec ↔ Implementation (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs (+1 more)). Document the error responses every operation can return (e.g. a `default` response with the error schema). [OpenAPI Specification — OAS-41](https://spec.openapis.org/oas/v3.1.2.html#responses-object)
1. **[Error] Error responses carry no x-ms-error-code header** — API Design / Status Codes & Errors (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs). Set an `x-ms-error-code` header on every error response, matching `error.code` in the body. [Microsoft Azure REST API Guidelines — AZ-044](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#rest-error-code-header)

## 2. Things Done Well

### Software Quality

- [Coding Standards] XML documentation on all public types and members, with GenerateDocumentationFile enabled — src/PilotUtiltyApi.Web/PilotUtilityApi.Web.csproj
- [Architecture Patterns] Error-to-ProblemDetails mapping centralized in one middleware instead of per controller — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs
- [Architecture Patterns] Clean downward layering: controller → service → repository, no data access in controllers — src/PilotUtiltyApi.Web/Controllers/TestingController.cs

### Software Lifecycle

- [Continuous Integration] CI builds every pull request to main on hosted GitHub Actions from a pipeline defined in the repository — .github/workflows/dotnet.yml
- [Versioning] A single, valid SemVer version is declared centrally in Directory.Build.props — Directory.Build.props
- [Workflow Security] Workflow uses only push and pull_request triggers and interpolates no untrusted context into scripts — .github/workflows/dotnet.yml

### Twelve-Factor

- [IV. Backing services] Database provider and handle are selected purely by config (DataSourceType + Active flag) and validated at startup — src/PilotUtiltyApi.Web/appsettings.json
- [II. Dependencies] All dependencies declared through central package management and project references; CI restores and builds deterministically — Directory.Packages.props
- [IX. Disposability] Self-hosted Generic Host/Kestrel app with lean startup and log flush on shutdown — src/PilotUtiltyApi.Web/Program.cs

### API Design

- [OpenAPI Spec] Committed OAS 3.1 spec is structurally valid, with 3.1-style nullability and resolving $refs — docs/PilotUtilityApi_v1.json
- [Method Semantics] About details redact sensitive configuration values before returning them — src/PilotUtiltyApi.Web/Controllers/SystemController.cs
- [URLs] Route tokens are lowercased consistently via a route token transformer — src/PilotUtiltyApi.Shared/Api/Transformers/LowercaseParameterTransformer.cs

### Security

- [Input & Injection] Reset SQL is a compile-time constant selected by a fixed switch; no request data reaches SQL text — src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs
- [Input & Injection] Only input is a strongly typed, required bool query parameter on an [ApiController] (automatic 400 on invalid model state) — src/PilotUtiltyApi.Web/Controllers/SystemController.cs
- [Web & API] No CORS policy is configured, so the Same Origin Policy applies — src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs
- [Web & API] Actions declare explicit HTTP methods and take no credentials in URLs — src/PilotUtiltyApi.Web/Controllers/TestingController.cs
- [Operational] Global exception middleware logs the exception and returns a generic ProblemDetails with only a correlation ID — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs
- [Operational] Data-source configuration redacts the password in ToString and copy-with-suppression — src/PilotUtiltyApi.Shared/Configuration/Models/DataSourceConfiguration.cs
- [Operational] File log sink is size-capped, rolled daily with bounded retention and structured JSON output — src/PilotUtiltyApi.Web/appsettings.json

### Testing

- [CI Execution] CI runs the full test suite on every push and pull request to main, failing the build on test failure — .github/workflows/dotnet.yml
- [Isolation & Determinism] Unit tests build their own state per test, with no shared setup, sleeps, clock reads or ordering — test/PilotUtiltyApi.Services.Tests/Services/TestingServiceTests.cs
- [Test Code Quality] Consistent Unit_Scenario_Expected naming and clear arrange/act/assert, with thorough validation-path tests — test/PilotUtiltyApi.Shared.Tests/Configuration/ApplicationConfigurationTests.cs

### Observability

- [Structured Logging] Serilog configured from appsettings with compact JSON file sink, request logging and bridging to OpenTelemetry logs — src/PilotUtiltyApi.Shared/Logging/Extensions/LoggingExtensions.cs
- [Distributed Tracing] OpenTelemetry SDK instruments ASP.NET Core, HttpClient, Npgsql and SqlClient for traces and metrics, exported via OTLP to a collector — src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs
- [Error Recording] Global middleware logs unhandled exceptions once at Error with the exception object; host failures logged at Fatal — src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs

### Implementation

- [Dependency Management] Central Package Management with exact versions for every package; no floating versions — Directory.Packages.props
- [Dependency Management] All projects target .NET 10 (LTS, supported to 2028-11-14) and .NET-versioned packages are aligned at 10.0.13 — Directory.Build.props
- [Dependency Management] Test-only packages (NUnit, Moq, coverlet) are confined to test projects; production projects reference only runtime packages — test/PilotUtiltyApi.TestingShared/PilotUtilityApi.TestingShared.csproj

### Operations / Reliability

- [Reliability] Explicit, configurable connect timeout on the database connection — src/PilotUtiltyApi.Web/appsettings.json

### Operations / Performance

- [Performance] Async controller → service → repository chain with CancellationToken passed to the Dapper query; no blocking on task results — src/PilotUtiltyApi.Web/Controllers/TestingController.cs

### Maintainability

- [Architecture Docs] README architecture section names each layer, its responsibility and its dependencies — README.md
- [License & Conduct] Root MIT LICENSE, linked from README, and a Contributor Covenant code of conduct in CONTRIBUTING — LICENSE
- [Prerequisites & Configuration] Data source keys documented in a table; sample settings use placeholders for secrets — README.md

## 3. Recommended Improvements

### Errors

- **Spec documents /testing/reset but the controller route is /v{version}/testing/reset** — API Design / Spec ↔ Implementation (docs/PilotUtilityApi_v1.json (+1 more), lines 81-82). Regenerate the committed spec from the running app (or fix the route) so the documented path matches the implemented route exactly. [OpenAPI Specification — OAS-38](https://spec.openapis.org/oas/v3.1.2.html#paths-object)
- **show-details is [BindRequired] in code but optional with a default in the spec** — API Design / Spec ↔ Implementation (src/PilotUtiltyApi.Web/Controllers/SystemController.cs (+1 more), lines 64-64). Decide whether the parameter is optional; either drop [BindRequired] (keeping the default) or mark it required: true in the spec without a default. [OpenAPI Specification — OAS-39](https://spec.openapis.org/oas/v3.1.2.html#parameter-object)
- **AboutResponse.ApplicationConfiguration is returned but absent from the spec schema** — API Design / Spec ↔ Implementation (src/PilotUtiltyApi.Domain/Models/Responses/AboutResponse.cs (+1 more), lines 20-21). Add the applicationConfiguration property (with its schema) to AboutResponse in the spec, or stop returning it. [OpenAPI Specification — OAS-40](https://spec.openapis.org/oas/v3.1.2.html#schema-object)
- **500 ProblemDetails responses from the exception middleware are not documented** — API Design / Spec ↔ Implementation (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs (+1 more), lines 83-92). Document the error responses every operation can return (e.g. a `default` response with the error schema). [OpenAPI Specification — OAS-41](https://spec.openapis.org/oas/v3.1.2.html#responses-object)
- **Error bodies do not use the standard { error: { code, message } } structure** — API Design / Status Codes & Errors (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs (+1 more), lines 59-65). Return one error body shape everywhere with `error.code` and `error.message` (extra fields allowed), and put the message in the body rather than a Warning header. [Microsoft Azure REST API Guidelines — AZ-046](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#rest-error-response-body-structure)
- **Error responses carry no x-ms-error-code header** — API Design / Status Codes & Errors (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs, lines 91-94). Set an `x-ms-error-code` header on every error response, matching `error.code` in the body. [Microsoft Azure REST API Guidelines — AZ-044](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#rest-error-code-header)
- **Synchronous POST action returns 204 instead of 200 with a body** — API Design / Status Codes & Errors (src/PilotUtiltyApi.Web/Controllers/TestingController.cs, lines 61-63). Always return 200 with a JSON object body (e.g. `{ "deletedCount": 0 }`) from the reset action. [Microsoft Azure REST API Guidelines — AZ-017](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#http-post-action-returns-200)
- **Service-side reset failures are reported as 400 with an empty body** — API Design / Status Codes & Errors (src/PilotUtiltyApi.Web/Controllers/TestingController.cs, lines 55-58). Return a 5xx for failures the caller cannot fix (400 only for invalid requests), with a diagnosable error body. [Microsoft Azure REST API Guidelines — AZ-031](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#rest-use-standard-status-codes)
- **API version is placed in the URL path** — API Design / Versioning (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 17-17). Remove the `v{version}` path segment and the URL-segment reader; carry the version in the `api-version` query parameter. [Microsoft Azure REST API Guidelines — AZ-088](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#versioning-no-version-in-path)
- **api-version is not required on every operation** — API Design / Versioning (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs (+1 more), lines 35-35). Require the `api-version` query parameter on all operations and document it in the spec. [Microsoft Azure REST API Guidelines — AZ-085](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#versioning-api-version-query-param)
- **Missing api-version silently falls back to a default instead of returning 400** — API Design / Versioning (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 35-36). Set AssumeDefaultVersionWhenUnspecified to false and return 400 with code `MissingApiVersionParameter` / `UnsupportedApiVersionValue`. [Microsoft Azure REST API Guidelines — AZ-087](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#versioning-api-version-missing)
- **API versions are numeric (1.0) rather than date-based** — API Design / Versioning (src/PilotUtiltyApi.Web/Controllers/TestingController.cs, lines 16-16). Use `YYYY-MM-DD` version values (with `-preview` for previews). [Microsoft Azure REST API Guidelines — AZ-086](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#versioning-date-based-versioning)
- **Query parameter show-details is kebab-case, not camelCase** — API Design / Query Parameters & Headers (src/PilotUtiltyApi.Web/Controllers/SystemController.cs, lines 64-64). Rename the query parameter to `showDetails` (and update the spec). [Microsoft Azure REST API Guidelines — AZ-020](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#http-query-names-casing)
- **AboutResponse can serialize null-valued fields** — API Design / JSON Representation (src/PilotUtiltyApi.Domain/Models/Responses/AboutResponse.cs (+2 more), lines 33-33). Omit null fields from responses (e.g. JsonIgnoreCondition.WhenWritingNull on the DTO or globally). [Microsoft Azure REST API Guidelines — AZ-054](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#json-null-response-values)
- **deployDate is an unformatted string passed through from an environment variable** — API Design / JSON Representation (src/PilotUtiltyApi.Web/Controllers/SystemController.cs (+1 more), lines 86-86). Parse the deploy date and emit it as an RFC 3339 date-time (`format: date-time` in the spec). [Microsoft Azure REST API Guidelines — AZ-058](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#json-date-time-is-rfc3339)
- **No x-ms-request-id is generated or returned, including on error responses** — API Design / Correlation & Telemetry (src/PilotUtiltyApi.Shared/Api/Middleware/UnhandledExceptionMiddleware.cs (+1 more), lines 75-76). Generate an opaque request ID per request, return it in an `x-ms-request-id` response header (documented in the spec) and include it in error logs. [Microsoft Azure REST API Guidelines — AZ-027](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#http-header-request-id)
- **No authentication or authorization configured; every controller is explicitly [AllowAnonymous] (no deny-by-default)** — Security / Identity & Access / Identity & Access (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs (+2 more), lines 79-85). Add an authentication scheme and AddAuthorization with a FallbackPolicy requiring authenticated users, call UseAuthentication/UseAuthorization, and keep [AllowAnonymous] only on truly public endpoints such as healthcheck (ATZ-02, T10-01). [OWASP .NET Security Cheat Sheet — ASP-09](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html#authorization)
- **Destructive POST /v1/testing/reset and configuration details on /about?show-details=true are callable anonymously** — Security / Identity & Access / Identity & Access (src/PilotUtiltyApi.Web/Controllers/TestingController.cs (+1 more), lines 46-53). Protect the reset and configuration-detail operations with a named policy or role (e.g. [Authorize(Policy = "TestAdmin")]) and, for reset, also restrict it to non-production environments (T10-04). [OWASP .NET Security Cheat Sheet — ASP-10](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html#authorization)
- **HTTPS redirection is enabled only in Development; production pipeline has no HTTPS enforcement** — Security / Web & API (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 72-75). Invert the condition so production calls UseHttpsRedirection (DNW-02) and, for API endpoints, configure Kestrel to listen on HTTPS only or reject HTTP with 400 (DNW-01, TLS-04, RST-01); if a reverse proxy enforces HTTPS, record that in the repository. [OWASP Transport Layer Security Cheat Sheet — TLS-03](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html#use-tls-for-all-pages)
- **SQL Server connection string disables server-certificate validation while sending database credentials** — Security / Operational (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs, lines 140-145). Remove TrustServerCertificate=True (or make it a development-only setting) and require encrypted connections with certificate validation for both SQL Server and PostgreSQL credential exchanges. [OWASP Secrets Management Cheat Sheet — SMG-11](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html#28-transport-layer-security-tls-everywhere)

### Warnings

- **Same switch on DataSourceType repeated in 3 repository methods (plus a 4th branch in SystemController) [ISO 25010:2023 Maintainability › Modifiability, ISO-30]** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+2 more), lines 138-138). Introduce one per-provider abstraction (e.g. an IDataSourceProvider with SqlServer/PostgreSQL implementations supplying connection string, connection and reset script) selected once. Apply Replace Conditional with Polymorphism (FRC-06, https://refactoring.com/catalog/replaceConditionalWithPolymorphism.html). [Compliance Reviewer Software Quality Rubric — SQR-07](../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-07)
- **Repository catches System.Exception without a filter (twice) and drops the original exception [ISO 25010:2023 Maintainability › Analysability, ISO-29]** — Software Quality / Software Quality (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+1 more), lines 92-103). Catch the provider exceptions you can handle (DbException, ConfigurationException) or add an exception filter, and pass the caught exception as InnerException of UserException; let the UnhandledExceptionMiddleware boundary handle the rest. [Microsoft C# conventions — MSC-09](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions#language-guidelines)
- **Connection and transaction managed with try/finally Close() instead of using declarations; transaction never disposed** — Software Quality / Coding Standards (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+1 more), lines 73-79). Use 'using var connection = ...' and 'using var transaction = ...' (the .editorconfig already prefers csharp_prefer_simple_using_statement) and drop the Close() finally block. [Microsoft C# conventions — MSC-16](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions#try-catch-and-using-statements-in-exception-handling)
- **Nullable annotations are used but key nullable warnings are downgraded to suggestions** — Software Quality / Coding Standards (.editorconfig (+1 more), lines 256-260). Restore CS8602/CS8604 to warning (or error) and fix the flagged dereferences, e.g. DataSources?.Find vs DataSources.FirstOrDefault usage. [Compliance Reviewer Software Quality Rubric — SQR-36](../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-36)
- **Private fields use camelCase without the _ prefix and no .editorconfig naming rule documents this convention** — Software Quality / Coding Standards (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+2 more), lines 24-24). Either rename private fields to _camelCase or add a dotnet_naming_rule for private fields in .editorconfig that documents the this.camelCase convention. [Microsoft C# conventions — MSC-03](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/identifier-names#camel-case)
- **No CODEOWNERS file on a GitHub repository, so pipeline and build files have no required code-owner review** — Software Lifecycle / Branch Protection (.github/workflows/dotnet.yml, lines 4-10). Add .github/CODEOWNERS with a '*' rule (or at least rules for .github/workflows/ and Directory.Build.props) naming the maintainers, and require code-owner review on main. [OpenSSF Scorecard v5.6.0 — OSC-04](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#branch-protection)
- **Workflow declares no permissions block, so the GITHUB_TOKEN inherits the repository default scopes** — Software Lifecycle / Pipeline Hardening (.github/workflows/dotnet.yml, lines 6-15). Add a top-level 'permissions: contents: read' (or 'permissions: {}') and grant any write scopes only on the jobs that need them. [OpenSSF Scorecard v5.6.0 — OSC-09](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#token-permissions)
- **Actions are pinned to mutable tags (@v4) rather than full commit SHAs** — Software Lifecycle / Pipeline Hardening (.github/workflows/dotnet.yml, lines 20-22). Pin each action to its full 40-character commit SHA with a version comment (e.g. actions/checkout@<sha> # v4.x.y) and let an update bot keep the pins current. [OpenSSF Scorecard v5.6.0 — OSC-11](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#pinned-dependencies)
- **No SAST tool runs in CI on pull requests or pushes** — Software Lifecycle / Static Analysis (.github/workflows/dotnet.yml, lines 25-30). Add a CodeQL workflow (github/codeql-action init + analyze for csharp) on pull_request and push to main, uploading SARIF results, with a defined severity threshold that blocks merge. [OpenSSF Scorecard v5.6.0 — OSC-14](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#sast)
- **Compiler warnings are not treated as errors in the shared build configuration** — Software Lifecycle / Static Analysis (Directory.Build.props, lines 2-9). Set <TreatWarningsAsErrors>true</TreatWarningsAsErrors> (at least for CI builds, e.g. via ContinuousIntegrationBuild) and an explicit <AnalysisLevel> in Directory.Build.props. [NIST SSDF 1.1 — SSDF-04](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf#page=23)
- **Production config writes rolling log files via the Serilog File sink** — Twelve-Factor / XI. Logs (src/PilotUtiltyApi.Web/appsettings.json (+2 more), lines 58-66). Remove the File sink (path, rolling and retention settings) from the base appsettings.json and keep only the Console sink and OTLP exporter; if file logging is wanted locally, move it into appsettings.Development.json. [Compliance Reviewer Twelve-Factor Rubric — TFR-19](../../compliance-reviewer/skills/review-twelve-factor/references/standards/twelve-factor-rubric.md#tfr-19)
- **Reset action uses a path segment instead of the :action pattern** — API Design / URLs (src/PilotUtiltyApi.Web/Controllers/TestingController.cs, lines 46-47). Expose the action as `POST /<collection>:reset` (e.g. `/testing-data:reset`) rather than a `/reset` sub-path. [Microsoft Azure REST API Guidelines — AZ-069](https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md#actions-url-pattern-for-resource-action)
- **HSTS is never enabled (no UseHsts/AddHsts) while production has no HTTPS enforcement** — Security / Web & API (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs, lines 72-75). Call app.UseHsts() outside Development with AddHsts(o => { o.MaxAge = TimeSpan.FromSeconds(63072000); o.IncludeSubDomains = true; }) (DNW-03), or serve the API over HTTPS only (DNW-04); if a proxy adds HSTS, record that in the repository. [OWASP HTTP Security Response Headers Cheat Sheet — HDR-07](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#strict-transport-security-hsts)
- **Swagger UI / Scalar pages have no framing protection (frame-ancestors or X-Frame-Options)** — Security / Web & API (src/PilotUtiltyApi.Shared/OpenApi/Extensions/OpenApiExtensions.cs (+1 more), lines 144-144). Send Content-Security-Policy: frame-ancestors 'none' (CSP-11) plus X-Frame-Options: DENY on HTML responses; if a reverse proxy adds these, record that in the repository. [OWASP HTTP Security Response Headers Cheat Sheet — HDR-01](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-frame-options)
- **OpenAPI document, Scalar and Swagger UI are exposed in all environments despite an acknowledged production gate** — Security / Web & API (src/PilotUtiltyApi.Shared/OpenApi/Extensions/OpenApiExtensions.cs (+1 more), lines 137-141). Wrap MapOpenApi, MapScalarApiReference and UseSwaggerUI in an IsDevelopment() (or explicit configuration flag) check so unnecessary documentation endpoints are disabled in production. [OWASP Top 10:2025 A02 — A02-03](https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/#description)
- **CI workflow runs no secret-detection scan before merge** — Security / Operational (.github/workflows/dotnet.yml, lines 17-28). Add a secret-scanning step (e.g. gitleaks or GitHub secret scanning/push protection) to the pull_request workflow and a matching pre-commit hook. [OWASP Secrets Management Cheat Sheet — SMG-05](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html#81-general-detection-approaches)
- **Base appsettings.json (all environments) carries development data-source values** — Security / Operational (src/PilotUtiltyApi.Web/appsettings.json, lines 10-13). Keep development host/user values only in appsettings.Development.json and leave the base file with empty or environment-supplied values so production cannot silently inherit development settings. [OWASP Secure Code Review Cheat Sheet — SCR-02](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html#configuration-deployment)
- **coverlet.collector is referenced but CI never collects or publishes coverage** — Testing / Coverage (test/PilotUtiltyApi.Web.Tests/PilotUtilityApi.Web.Tests.csproj (+1 more), lines 9-9). Run `dotnet test --collect:"XPlat Code Coverage"` in CI and publish the result (reportgenerator step, coverage artifact or Codecov upload) so untested code is visible; no percentage gate is required. [Compliance Reviewer Testing Rubric — TSR-04](../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-04)
- **Placeholder Assert.Pass test and tests whose arrange contradicts their name cannot catch the defects they claim to cover (3 tests)** — Testing / Assertion Quality (test/PilotUtiltyApi.Domain.Tests/ExampleTest.cs (+2 more), lines 9-14). Remove the Assert.Pass placeholder (or replace it with a real test), stub a null ErrorMessage and assert the default Warning value, and either build a null-result response or rename the null-result test. [Compliance Reviewer Testing Rubric — TSR-07](../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-07)
- **Repository data access is never tested against a real database engine** — Testing / Integration Tests (test/PilotUtiltyApi.Repositories.Tests/Repositories/TestingRepositoryTests.cs (+1 more), lines 17-17). Add an integration test project that runs TestingRepository.ResetTestingAsync against a containerized SQL Server/PostgreSQL (e.g. Testcontainers) with a fresh database per run. [Compliance Reviewer Testing Rubric — TSR-18](../../compliance-reviewer/skills/review-testing/references/standards/testing-rubric.md#tsr-18)
- **Error correlation ID is a fresh random GUID unrelated to the trace ID and only embedded in message text** — Observability / Correlation & Context Propagation (src/PilotUtiltyApi.Shared/Logging/Models/LoggingCorrelation.cs (+1 more), lines 15-15). Derive the correlation ID from Activity.Current.TraceId (fall back to a GUID only when no activity exists) and log it as its own template property (e.g. {CorrelationId}) so the user-facing ID links directly to the trace and logs. [Azure Well-Architected Framework — WAFO-05](https://learn.microsoft.com/azure/well-architected/operational-excellence/observability#correlate-data-for-end-to-end-insights)
- **Only health endpoint returns a constant 200 and never reflects the required database dependency** — Observability / Health Endpoints (src/PilotUtiltyApi.Web/Controllers/SystemController.cs (+1 more), lines 43-48). Register AddHealthChecks() with a timed, read-only SQL Server/PostgreSQL check tagged "ready", and map separate shallow liveness and readiness endpoints that return 503 when the active data source is unreachable. [Azure Well-Architected Framework — WAFO-16](https://learn.microsoft.com/azure/well-architected/design-guides/health-modeling#use-health-probes)
- **.NET SDK version is not pinned (no global.json); build tooling floats to whatever SDK is installed** — Implementation / Dependency Management (Directory.Build.props (+1 more), lines 4-4). Add a global.json at the repository root pinning the .NET 10 SDK version (with an explicit rollForward policy such as latestPatch) so builds use a known toolchain. [OWASP Software Supply Chain Security Cheat Sheet — OCS-15](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html#inventory-build-tools)
- **Database calls in the request path have no transient-fault retry** — Operations / Reliability / Reliability (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs, lines 73-89). Add a bounded retry with exponential back-off and jitter for transient DB errors only (e.g. SqlClient configurable retry logic / Npgsql retry, or a Polly pipeline registered once in DI), wrapping the whole transaction. [Azure Architecture Center — AZRL-05](https://learn.microsoft.com/azure/architecture/best-practices/transient-faults#check-whether-a-built-in-retry-mechanism-exists)
- **No circuit breaker around the synchronous database dependency on the request path** — Operations / Reliability / Reliability (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs, lines 89-89). Register a shared resilience pipeline (retry inside a circuit breaker) once in DI for the active data source and handle BrokenCircuitException with a clear 503-style error. [Azure Architecture Center — AZRL-21](https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker#solution)
- **README does not link CONTRIBUTING.md or the docs/ content** — Maintainability / README & Onboarding (README.md (+1 more), lines 5-20). Add a 'Contributing' and 'Further documentation' section linking CONTRIBUTING.md, docs/PilotUtilityApi_v1.json and the architecture instructions. [Compliance Reviewer Maintainability Rubric — MR-06](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-06)
- **No local database setup steps or local stack for the required SQL Server/PostgreSQL** — Maintainability / Prerequisites & Configuration (README.md, lines 84-86). Add steps (or a docker-compose file) to create the NorthWind database, schema, DevUser login and test tables the reset script expects. [Compliance Reviewer Maintainability Rubric — MR-16](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-16)
- **README run/config paths point to src/PilotUtilityApi.Web, which does not exist** — Maintainability / Docs in Sync (README.md (+2 more), lines 116-116). Change the README paths to src/PilotUtiltyApi.Web (or rename the folder), and align the inconsistent example ports (58701, 58401, 7000) with launch settings. [Compliance Reviewer Maintainability Rubric — MR-33](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-33)
- **Versions in docs disagree with the project version (0.1.1 / 1.0.0 vs 1.0.1)** — Maintainability / Docs in Sync (README.md (+2 more), lines 183-183). Update the README example and regenerate docs/PilotUtilityApi_v1.json so both show 1.0.1, matching Directory.Build.props and appsettings.json. [Compliance Reviewer Maintainability Rubric — MR-35](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-35)
- **CONTRIBUTING links a README anchor (#copilot-customization) that does not exist** — Maintainability / Docs in Sync (CONTRIBUTING.md, lines 14-14). Add a 'Copilot Customization' section to the README describing .github/copilot-instructions.md and instructions/, or remove the link. [Compliance Reviewer Maintainability Rubric — MR-36](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-36)

### Information

- **TestingService is a pass-through Middle Man that only forwards to the repository [ISO 25010:2023 Maintainability › Analysability, ISO-29]** — Software Quality / Design Patterns (src/PilotUtiltyApi.Services/Services/TestingService.cs, lines 49-52). Either give the service real responsibility (e.g. environment guard for the reset, result mapping) or document the deliberate closed-layer choice; otherwise apply Remove Middle Man (FRC-19, https://refactoring.com/catalog/removeMiddleMan.html). [Compliance Reviewer Software Quality Rubric — SQR-23](../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-23)
- **Misleading names: a delete result typed as RetrieveResponse, and 'PilotUtilty' folder names inconsistent with 'PilotUtility' projects** — Software Quality / Coding Standards (src/PilotUtiltyApi.Repositories/Repositories/TestingRepository.cs (+2 more), lines 57-57). Use an intention-revealing result type for write operations (e.g. OperationResponse<T>) and fix the 'PilotUtilty' spelling so folder and project names agree. Apply Rename (FRC-22, https://refactoring.com/catalog/changeFunctionDeclaration.html). [Compliance Reviewer Software Quality Rubric — SQR-32](../../compliance-reviewer/skills/review-software-quality/references/standards/software-quality-rubric.md#sqr-32)
- **No SECURITY.md security policy in the root, .github/ or docs/** — Software Lifecycle / Security Policy (.github/workflows/dotnet.yml, lines 4-4). Add a SECURITY.md giving a private reporting channel (email or GitHub private vulnerability reporting), the handling process and disclosure timelines, and supported versions. [OpenSSF Scorecard v5.6.0 — OSC-15](https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md#security-policy)
- **API responses carry no Cache-Control: no-store or frame-ancestors 'none' headers** — Security / Web & API (src/PilotUtiltyApi.Shared/Api/Extensions/ApiExtensions.cs (+1 more), lines 84-84). Add middleware setting Cache-Control: no-store and Content-Security-Policy: frame-ancestors 'none' (RST-08) on API responses, at least for configuration-detail responses such as /about?show-details=true. [OWASP REST Security Cheat Sheet — RST-07](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#security-headers)
- **Deployable Web API has no automated load or performance tests** — Testing / Load Tests (.github/workflows/dotnet.yml, lines 27-28). Add a scripted load test (k6, NBomber or similar) for the API's critical endpoints with pass/fail thresholds, run on a schedule or in the pipeline. [Azure Well-Architected Framework — AZT-01](https://learn.microsoft.com/azure/well-architected/performance-efficiency/performance-test#apply-multiple-performance-test-types)
- **OTLP exporter scheme and protocol are hard-coded, overriding OTEL_EXPORTER_OTLP_* configuration** — Observability / Telemetry Export (src/PilotUtiltyApi.Shared/OpenTelemetry/Extensions/OpenTelemetryExtensions.cs (+1 more), lines 52-52). Take the full endpoint (including scheme) and protocol from configuration, or leave Endpoint unset when OTEL_EXPORTER_OTLP_ENDPOINT is provided, so TLS and protocol can change per environment without a code change. [OpenTelemetry — OTO-29](https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/#endpoint-configuration)
- **No SLOs or SLIs documented for the service** — Observability / SLOs & SLIs (README.md, lines 38-38). Document availability and p95 latency SLOs for the API with their SLIs (e.g. based on http.server.request.duration) and an observation window. [Azure Well-Architected Framework — WAFO-19](https://learn.microsoft.com/azure/well-architected/reliability/metrics#define-composite-slo-targets)
- **Documented project structure uses folder names that do not exist (PilotUtilityApi.* vs actual PilotUtiltyApi.*)** — Maintainability / Repository Layout (README.md (+1 more), lines 49-64). Rename the src/ and test/ folders to PilotUtilityApi.* (updating the .sln paths), or correct the README tree to the actual folder names. [Compliance Reviewer Maintainability Rubric — MR-10](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-10)
- **Project folder names are misspelled and inconsistent with their project names** — Maintainability / Repository Layout (PilotUtilityApi.sln, lines 20-30). Make every project folder name match its project/assembly name (PilotUtilityApi.*) so the one-project-per-folder convention is applied consistently. [Compliance Reviewer Maintainability Rubric — MR-07](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-07)
- **CONTRIBUTING does not say how to build, format or test before submitting** — Maintainability / Contributing Guide (CONTRIBUTING.md, lines 8-18). Add a pre-submit step listing `dotnet build`, `dotnet format --verify-no-changes` and `dotnet test`, and drop the unrelated container-layer boilerplate. [Compliance Reviewer Maintainability Rubric — MR-25](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-25)
- **CONTRIBUTING does not state coding conventions or point to .editorconfig** — Maintainability / Contributing Guide (CONTRIBUTING.md, lines 1-18). Add a 'Coding conventions' section pointing to .editorconfig and .github/instructions/architecture.instructions.md. [Compliance Reviewer Maintainability Rubric — MR-26](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-26)
- **Versioned API has no CHANGELOG or release notes** — Maintainability / Change History (Directory.Build.props (+1 more), lines 3-3). Add a root CHANGELOG.md with dated per-version entries (starting at 1.0.1) and link it from the README. [Compliance Reviewer Maintainability Rubric — MR-27](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-27)
- **Significant decisions (Dapper, multi-database, layering) are not recorded with context and consequences** — Maintainability / Architecture Docs (.github/instructions/architecture.instructions.md, lines 33-35). Add docs/adr/ with short ADRs (context, decision, consequences) for Dapper, SQL Server/PostgreSQL switching and the layer structure. [Compliance Reviewer Maintainability Rubric — MR-31](../../compliance-reviewer/skills/review-maintainability/references/standards/maintainability-rubric.md#mr-31)

## 4. Full Results

### Software Quality

#### Software Quality

| Check | Result | Evidence |
|-------|--------|----------|
| SQ-01 | pass |  |
| SQ-02 | pass |  |
| SQ-03 | fail | The same DataSourceType switch is repeated in 3 repository methods (SQR-07). |
| SQ-04 | pass |  |
| SQ-05 | pass |  |
| SQ-06 | fail | Repository catches System.Exception without a filter below the request boundary (MSC-09). |
| SQ-08 | pass |  |

#### Design Patterns

| Check | Result | Evidence |
|-------|--------|----------|
| DP-01 | pass |  |
| DP-02 | N/A | No project-defined class hierarchies in the reviewed files. |
| DP-04 | fail | TestingService only forwards to the repository (SQR-23). |
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
| AP-07 | N/A | Only one deployable unit (the Web API) in the reviewed files. |

#### Coding Standards

| Check | Result | Evidence |
|-------|--------|----------|
| CS-01 | fail | RetrieveResponse names a delete result and 'PilotUtilty' folders misspell the project name (SQR-32). |
| CS-02 | pass |  |
| CS-03 | fail | duplicate evidence of OBS-06#1, see Observability/Health Endpoints |
| CS-04 | pass |  |
| CS-05 | fail | No using for IDisposable connection/transaction (MSC-16), nullable warnings downgraded (SQR-36), undocumented private field naming (MSC-03). |

### Software Lifecycle

#### Continuous Integration

| Check | Result | Evidence |
|-------|--------|----------|
| SL-01 | pass |  |

#### Release Automation

| Check | Result | Evidence |
|-------|--------|----------|
| SL-02 | N/A | Repo publishes no versioned artifacts: no release, packaging or deploy pipeline in the reviewed files. |

#### Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| SL-03 | pass |  |

#### Branch Protection

| Check | Result | Evidence |
|-------|--------|----------|
| SL-04 | fail | No CODEOWNERS on a GitHub repository (OSC-04, SSDF-10); other setting elements skipped as repository settings are not visible in files. |

#### Provenance & Signing

| Check | Result | Evidence |
|-------|--------|----------|
| SL-05 | N/A | Repo publishes no versioned artifacts. |

#### Security Policy

| Check | Result | Evidence |
|-------|--------|----------|
| SL-07 | fail | No SECURITY.md exists in the repository. |

#### Workflow Security

| Check | Result | Evidence |
|-------|--------|----------|
| SL-09 | pass |  |

#### Pipeline Hardening

| Check | Result | Evidence |
|-------|--------|----------|
| SL-10 | fail | Workflow has no permissions block and actions are pinned to mutable @v4 tags. |

#### Static Analysis

| Check | Result | Evidence |
|-------|--------|----------|
| SL-11 | fail | No SAST in CI and warnings are not treated as errors in build config. |

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
| TF-05 | N/A | No Dockerfile, deployment manifest or deploy step visible; CI only builds and tests. |

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
| TF-10 | N/A | Production backing-service definition not visible (no IaC/compose/manifests; only localhost config). |

#### XI. Logs

| Check | Result | Evidence |
|-------|--------|----------|
| TF-11 | fail | Base appsettings.json configures a Serilog rolling File sink with retention, and runtime log files exist under logs/. |

#### XII. Admin processes

| Check | Result | Evidence |
|-------|--------|----------|
| TF-12 | N/A | No admin or migration tasks visible in the reviewed files. |

### API Design

#### OpenAPI Spec

| Check | Result | Evidence |
|-------|--------|----------|
| API-01 | pass |  |
| API-02 | pass |  |

#### Spec ↔ Implementation

| Check | Result | Evidence |
|-------|--------|----------|
| API-03 | fail | Spec path, parameter required-ness, response schema and error status codes drift from the implementation. |

#### URLs

| Check | Result | Evidence |
|-------|--------|----------|
| API-04 | fail | The reset action uses a /reset sub-path instead of the :action URL pattern. |

#### Status Codes & Errors

| Check | Result | Evidence |
|-------|--------|----------|
| API-05 | fail | Non-standard error body and header, 204 from a POST action, and 400 for service-side failures. |

#### Pagination

| Check | Result | Evidence |
|-------|--------|----------|
| API-06 | N/A | No collection/list endpoints in scope. |

#### Versioning

| Check | Result | Evidence |
|-------|--------|----------|
| API-07 | fail | Version is in the path, not required, defaults silently and is not date-based. |

#### Filtering & Sorting

| Check | Result | Evidence |
|-------|--------|----------|
| API-08 | N/A | No collection query options are offered. |

#### Method Semantics

| Check | Result | Evidence |
|-------|--------|----------|
| API-09 | pass |  |

#### Query Parameters & Headers

| Check | Result | Evidence |
|-------|--------|----------|
| API-10 | fail | Query parameter name show-details is not camelCase. |

#### JSON Representation

| Check | Result | Evidence |
|-------|--------|----------|
| API-11 | fail | Null fields can be serialized and deployDate has no RFC 3339 contract. |

#### Enums & Polymorphism

| Check | Result | Evidence |
|-------|--------|----------|
| API-12 | N/A | No enums or polymorphic types in the API contract. |

#### Long-Running Operations

| Check | Result | Evidence |
|-------|--------|----------|
| API-13 | N/A | No long-running operations exist. |

#### Conditional Requests

| Check | Result | Evidence |
|-------|--------|----------|
| API-14 | N/A | No resource read/update operations (only health, about and a reset action). |

#### Correlation & Telemetry

| Check | Result | Evidence |
|-------|--------|----------|
| API-15 | fail | No x-ms-request-id is generated, returned or documented. |

### Security / Identity & Access

#### Identity & Access

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-IA-01 | fail | No fallback/deny-by-default policy; no authentication configured (ASP-09, ATZ-02). |
| SEC-IA-02 | fail | Privileged write and config-detail endpoints have no role or policy (ASP-10, T10-04). |
| SEC-IA-03 | N/A | No JWTs issued or validated in the reviewed files. |
| SEC-IA-04 | N/A | No OAuth 2.0/OIDC in use. |
| SEC-IA-05 | N/A | No sessions or cookie authentication in use. |
| SEC-IA-06 | N/A | The target stores no user passwords. |
| SEC-IA-07 | N/A | No custom authentication, session or credential-hashing code in the reviewed files. |
| SEC-IA-08 | N/A | No service-to-service auth, roles, scopes or accounts in the reviewed files. |
| SEC-IA-09 | N/A | No login flow or access-control decisions exist to fail. |
| SEC-IA-10 | N/A | No user password policy or application user credentials in scope. |
| SEC-IA-11 | N/A | No client-side token handling or credential endpoints. |

### Security

#### Input & Injection

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-II-01 | pass |  |
| SEC-II-02 | pass |  |
| SEC-II-03 | pass |  |
| SEC-II-04 | N/A | No OS command, script engine, LDAP, XPath, NoSQL or other interpreter use in the subject files. |
| SEC-II-05 | N/A | No XML is parsed in the subject files. |
| SEC-II-06 | N/A | No file upload handling in the subject files. |
| SEC-II-07 | N/A | No file upload storage or serving in the subject files. |
| SEC-II-08 | N/A | JSON API only; nothing is rendered to HTML, JavaScript, CSS or URL contexts. |
| SEC-II-09 | N/A | Nothing is deserialized beyond plain JSON into DTOs; no native or polymorphic serializers. |
| SEC-II-10 | N/A | No outbound request uses a URL, host or IP derived from untrusted data. |

#### Web & API

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-WA-01 | fail | duplicate evidence of SEC-IA-01#1, see Security / Identity & Access/Identity & Access |
| SEC-WA-02 | fail | No UseHsts/AddHsts and HTTPS is not enforced outside Development. |
| SEC-WA-03 | fail | duplicate evidence of SEC-IA-01#1, see Security / Identity & Access/Identity & Access |
| SEC-WA-04 | fail | HTML pages have no frame-ancestors or X-Frame-Options protection. |
| SEC-WA-05 | pass |  |
| SEC-WA-06 | fail | UseHttpsRedirection runs only in Development, leaving production without HTTPS enforcement. |
| SEC-WA-07 | pass |  |
| SEC-WA-08 | fail | API responses lack Cache-Control: no-store and frame-ancestors 'none' (SHOULD elements). |
| SEC-WA-09 | fail | OpenAPI/Scalar/Swagger UI endpoints are enabled in production (unnecessary features). |
| SEC-WA-10 | pass |  |
| SEC-WA-11 | fail | duplicate evidence of SEC-IA-01#1, see Security / Identity & Access/Identity & Access |

#### Operational

| Check | Result | Evidence |
|-------|--------|----------|
| SEC-OP-01 | pass |  |
| SEC-OP-02 | pass |  |
| SEC-OP-03 | pass |  |
| SEC-OP-04 | pass |  |
| SEC-OP-05 | fail | No literal secrets (passwords are placeholders), but the CI workflow has no secret-detection step (SMG-05). |
| SEC-OP-06 | fail | SQL Server credentials are sent over a connection with TrustServerCertificate=True (SMG-11). |
| SEC-OP-07 | fail | duplicate evidence of API-03#1, see API Design/Spec ↔ Implementation |
| SEC-OP-08 | fail | duplicate evidence of SQ-06#1, see Software Quality/Software Quality |
| SEC-OP-09 | pass |  |
| SEC-OP-10 | fail | duplicate evidence of CS-05#1, see Software Quality/Coding Standards |

### Testing

#### Test Pyramid

| Check | Result | Evidence |
|-------|--------|----------|
| TST-01 | pass |  |

#### Coverage

| Check | Result | Evidence |
|-------|--------|----------|
| TST-02 | fail | Coverage collector is referenced but no collection or report runs in CI or a documented command. |

#### Assertion Quality

| Check | Result | Evidence |
|-------|--------|----------|
| TST-03 | fail | An Assert.Pass placeholder and two tests whose arrange contradicts their names cannot catch the claimed defects. |

#### Test Doubles

| Check | Result | Evidence |
|-------|--------|----------|
| TST-04 | pass |  |

#### Isolation & Determinism

| Check | Result | Evidence |
|-------|--------|----------|
| TST-05 | pass |  |

#### CI Execution

| Check | Result | Evidence |
|-------|--------|----------|
| TST-06 | pass |  |

#### Module Coverage

| Check | Result | Evidence |
|-------|--------|----------|
| TST-07 | pass |  |

#### Test Code Quality

| Check | Result | Evidence |
|-------|--------|----------|
| TST-08 | pass |  |

#### Integration Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-09 | fail | Repository data access exists but no test runs it against a real database engine. |

#### Security Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-10 | pass |  |

#### Fuzz & DAST

| Check | Result | Evidence |
|-------|--------|----------|
| TST-11 | fail | duplicate evidence of SEC-OP-05#1, see Security/Operational |

#### Load Tests

| Check | Result | Evidence |
|-------|--------|----------|
| TST-12 | fail | Deployable Web API has no load or performance tests (signals.loadTests false). |

#### Resilience Tests

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
| OBS-02 | fail | Error correlation ID is a random GUID disconnected from the trace ID and not logged as its own attribute. |

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
| OBS-05 | fail | OTLP export goes to a collector, but scheme and protocol are hard-coded and override standard OTEL_EXPORTER_OTLP_* settings. |

#### Health Endpoints

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-06 | fail | Single anonymous constant-200 health endpoint with no readiness check for the required database; probe wiring (WAFO-15) not judged since IaC is out of scope. |

#### SLOs & SLIs

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-07 | fail | README documents no SLO targets or SLIs for the deployable API. |

#### Telemetry Identity

| Check | Result | Evidence |
|-------|--------|----------|
| OBS-08 | fail | duplicate evidence of MAINT-09#2, see Maintainability/Docs in Sync |

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
| DEP-01 | fail | Package versions are exact, but the .NET SDK (build tooling) is not pinned: no global.json exists. |
| DEP-02 | fail | duplicate evidence of SL-11#2, see Software Lifecycle/Static Analysis |
| DEP-03 | N/A | no vulnerability analyzer output for this run |
| DEP-04 | pass |  |
| DEP-05 | fail | duplicate evidence of SL-11#2, see Software Lifecycle/Static Analysis |
| DEP-07 | N/A | No dependency-update or scanning config (Dependabot/Renovate, NuGetAudit, suppressions) is in the subject's file list. |
| DEP-08 | pass |  |
| DEP-09 | pass |  |

### Operations / Reliability

#### Reliability

| Check | Result | Evidence |
|-------|--------|----------|
| REL-01 | pass |  |
| REL-02 | fail | Remote DB calls in the request path have no retry (AZRL-05). |
| REL-03 | N/A | No retry logic or redelivery in scope. |
| REL-04 | fail | Synchronous DB calls in the request path have no circuit breaker (AZRL-21). |
| REL-05 | N/A | No deployment config in scope. |
| REL-06 | fail | duplicate evidence of SEC-IA-01#1, see Security / Identity & Access/Identity & Access |
| REL-07 | N/A | No message consumers or background jobs in scope. |
| REL-08 | N/A | No deployment config in scope (IaC not reviewed, advanced usage off). |

### Operations / Performance

#### Performance

| Check | Result | Evidence |
|-------|--------|----------|
| PERF-01 | N/A | No repeated reads or cache in request paths; the only data endpoint is a write (reset). |
| PERF-02 | fail | duplicate evidence of CS-05#1, see Software Quality/Coding Standards |
| PERF-03 | fail | duplicate evidence of CS-05#1, see Software Quality/Coding Standards |
| PERF-04 | pass |  |
| PERF-05 | N/A | No hot-path loops over unbounded data in the reviewed files. |
| PERF-06 | pass |  |
| PERF-07 | pass |  |
| PERF-08 | N/A | No hosting/scaling config in scope; no static assets or processing pipelines (AZPE-49…53 not applicable). |

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
| MAINT-02 | fail | Documented structure and project names don't match the misspelled PilotUtiltyApi.* folders (MR-07, MR-10). |

#### Prerequisites & Configuration

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-03 | fail | duplicate evidence of API-11#1, see API Design/JSON Representation |

#### Technical Debt

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-04 | N/A | No debt markers or warning suppressions in the 3 reviewed source files. |

#### Deprecation

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-05 | N/A | No deprecated, legacy-named or versioned-copy code in the reviewed files or listing. |

#### Contributing Guide

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-06 | fail | CONTRIBUTING covers PR review but not pre-submit commands or coding conventions (MR-25, MR-26). |

#### Change History

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-07 | fail | Versioned API (1.0.1, SemVer) has no CHANGELOG or release notes (MR-27). |

#### Architecture Docs

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-08 | fail | Architecture overview exists but no decisions/ADRs are recorded (MR-31). |

#### Docs in Sync

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-09 | fail | Docs reference non-existent paths, stale versions and a missing anchor (MR-33, MR-35, MR-36). |

#### License & Conduct

| Check | Result | Evidence |
|-------|--------|----------|
| MAINT-10 | pass |  |

## 5. Appendix

- **Run:** `2026-11-09_2123-PilotUtilityApi` · Target: `C:\Working\Storage\Dev\GitHub\PilotUtilityApi` · Git HEAD: `59fedaa36172568260fd667103313ee95af13a16`
- **Started:** 2026-11-09T21:23:03-07:00 · **Completed:** 2026-11-09T21:41:01-07:00
- **Run flags:** advanced off (IaC and CLI analyzers not run)
- **Subjects skipped:** review-disaster-recovery (advanced usage off (IaC not reviewed)); review-monitoring (advanced usage off (IaC not reviewed)); review-cost-sustainability (advanced usage off (IaC not reviewed))
- **URLs fetched:** none
- **Link approvals:** none
