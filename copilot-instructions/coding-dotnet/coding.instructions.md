---
description: Source code creation standards for C#/.NET applications in this repository.
applyTo: "src/**/*.cs"
---

# Coding Instructions: C# / .NET

## Purpose and Scope
These instructions define how GitHub Copilot should create and maintain production source code for C#/.NET applications in this repository.

Scope restriction:
- These instructions apply to creating and maintaining application source code, configuration, and supporting project files.
- Unit test work is governed by `unit-tests.instructions.md`; follow that file when the task is test-related.

Hard constraints:
- Target the latest LTS .NET release used by the solution (do not change the target framework unless asked).
- Enable nullable reference types (`<Nullable>enable</Nullable>`) and treat warnings as errors in new projects.
- Every file must contain only one top-level type.
- Never hard-code secrets, connection strings, or environment-specific values.
- Every operation that touches a database, HTTP endpoint, message broker, cache, or file system must be logged and traced, and every log entry must carry a `CorrelationId`.

## How This Instructions File Is Used
When a request involves creating or changing application source code, Copilot must:
1. Follow this file as the primary standard for structure, naming, design, and cross-cutting concerns.
2. Match existing conventions in the solution where they do not conflict with these rules.
3. Build the solution and resolve all compiler errors and warnings introduced by the change.
4. Keep changes scoped to the task; do not refactor unrelated code.

## Project Structure
Rules:
- Use a solution (`.sln` or `.slnx`) at the repository root with production projects under `src/` and test projects under `test/`.
- Name projects `<Product>.<Layer>` (for example, `PilotApi.Api`, `PilotApi.Services`, `PilotApi.Domain`, `PilotApi.Repositories`).
- Organize folders inside a project by feature first, then by technical role (for example, `Orders/Commands`, `Orders/Queries`, `Orders/Models`).
- Folder structure must match namespaces; use file-scoped namespaces.
- Centralize build settings in `Directory.Build.props` and package versions in `Directory.Packages.props`.
- Keep `Program.cs` thin: register services through extension methods such as `services.AddOrdersFeature()`.
- Place configuration in `appsettings.json` with environment overrides (`appsettings.{Environment}.json`); never commit secrets to these files.

Example layout:
```
src/
  PilotApi.Api/               # Controllers or minimal API endpoints, middleware, Program.cs
  PilotApi.Services/       # Use cases, commands/queries, validators, interfaces (ports)
  PilotApi.Domain/            # Entities, value objects, domain events, domain services
  PilotApi.Repositories/    # EF Core, HTTP clients, messaging, external adapters
test/
  PilotApi.Services.Tests/
```

## Architecture
Rules:
- Follow Clean Architecture / Hexagonal principles: dependencies point inward (`Api` -> `Services` -> `Domain`; `Repositories` implements `Services` interfaces).
- The `Domain` project has no dependency on frameworks, EF Core, or ASP.NET Core.
- Use dependency injection via `Microsoft.Extensions.DependencyInjection`; prefer constructor injection (primary constructors are acceptable).
- Choose service lifetimes deliberately: `DbContext` and unit-of-work types are scoped; stateless services may be singletons; never inject a scoped service into a singleton.
- Apply SOLID principles; favor composition over inheritance.
- Use the Options pattern (`IOptions<T>`, `IOptionsMonitor<T>`) with `ValidateDataAnnotations()` and `ValidateOnStart()` for configuration.
- Use `async`/`await` end to end for I/O; never block with `.Result` or `.Wait()`.
- Pass `CancellationToken` through every async call chain.
- Use records for immutable DTOs and value objects.
- Use the Result pattern or domain-specific exceptions for expected failures; do not use exceptions for control flow.

## Naming Conventions
| Artifact | Convention | Example |
|---|---|---|
| Namespace | PascalCase, matches folder | `PilotApi.Services.Orders` |
| Class / Record / Struct | PascalCase noun | `OrderService`, `OrderSummary` |
| Interface | `I` + PascalCase | `IOrderRepository` |
| Method | PascalCase verb | `CalculateTotal` |
| Async method | Suffix `Async` | `GetOrderAsync` |
| Property / Event | PascalCase | `CreatedAt`, `OrderPlaced` |
| Private field | `_camelCase` | `_orderRepository` |
| Local / parameter | camelCase | `orderId` |
| Constant | PascalCase | `MaxRetryCount` |
| Enum type / member | PascalCase singular (plural for `[Flags]`) | `OrderStatus.Shipped` |
| Generic type parameter | `T` + PascalCase | `TEntity` |
| Attribute | Suffix `Attribute` | `AuditedAttribute` |
| Exception | Suffix `Exception` | `OrderNotFoundException` |
| Options class | Suffix `Options` | `PaymentGatewayOptions` |
| DTO | Suffix `Request` / `Response` | `CreateOrderRequest` |

Rules:
- File names match the type name (`OrderService.cs`).
- Avoid abbreviations and Hungarian notation; prefer descriptive names.
- Boolean members read as predicates (`IsActive`, `HasItems`, `CanShip`).

## Documentation
Rules:
- Every public and protected type and member must have XML documentation comments (`<summary>`, `<param>`, `<returns>`, `<exception>` as applicable).
- Enable `<GenerateDocumentationFile>true</GenerateDocumentationFile>` so missing docs surface as warnings.
- Comments explain *why*, not *what*; do not restate the code.
- Each project includes a `README.md` describing its purpose, how to build/run it, and required configuration keys.
- Record significant design decisions as Architecture Decision Records under `docs/adr/`.
- APIs publish an OpenAPI document with summaries, descriptions, and response types for every endpoint.

## API Design
Applies when the project exposes HTTP APIs.

Rules:
- Use ASP.NET Core controllers or minimal APIs consistently within a project.
- Use resource-oriented, plural, lowercase, kebab-case routes (`/api/v1/purchase-orders/{id}`).
- Use HTTP verbs and status codes correctly (`201 Created` with `Location` header, `204 No Content`, `404 Not Found`, `409 Conflict`).
- Return errors as RFC 9457 Problem Details (`AddProblemDetails()`), including the `CorrelationId` in an extension field.
- Version APIs explicitly (URL segment or header) using `Asp.Versioning`.
- Validate all input (FluentValidation or DataAnnotations) and return `400`/`422` with field-level details.
- Paginate collection endpoints; support filtering and sorting through query parameters.
- Support idempotency for unsafe retried operations (for example, an `Idempotency-Key` header on `POST`).
- Never expose domain entities or EF Core entities directly; map to DTOs.
- Generate OpenAPI documentation (`Microsoft.AspNetCore.OpenApi`) for every endpoint.

### 12-Factor App Guidance
| Factor | .NET Practice |
|---|---|
| I. Codebase | One repository per deployable; one build produces many deploys. |
| II. Dependencies | Declare all packages in project files with central package management; no reliance on globally installed tools. |
| III. Config | Read config from environment variables via `IConfiguration`; secrets from Azure Key Vault / user secrets (dev only). |
| IV. Backing services | Treat databases, queues, and caches as attached resources addressed by configuration. |
| V. Build, release, run | Build immutable container images; inject config at release; never patch running instances. |
| VI. Processes | Keep services stateless; store session/state in a backing service (for example, Redis). |
| VII. Port binding | Self-host with Kestrel; bind to the port supplied by `ASPNETCORE_URLS` / `ASPNETCORE_HTTP_PORTS`. |
| VIII. Concurrency | Scale out by adding processes; use `BackgroundService` / worker processes for background work. |
| IX. Disposability | Start fast; handle `SIGTERM` via `IHostApplicationLifetime`; drain in-flight requests within `HostOptions.ShutdownTimeout`. |
| X. Dev/prod parity | Use the same backing services locally (Docker Compose / .NET Aspire) as in production. |
| XI. Logs | Write structured logs to stdout; let the platform route them. |
| XII. Admin processes | Run migrations and one-off tasks as separate commands using the same codebase and config. |

## UI Design
Applies when the project includes a UI (Blazor, Razor Pages, MVC, MAUI).

Rules:
- Separate presentation from logic: use components/view models; keep code-behind thin.
- Build small, reusable components with explicit parameters and `EventCallback`s.
- Meet WCAG 2.2 AA: semantic HTML, labels for all inputs, keyboard navigation, sufficient color contrast, ARIA only when native semantics are insufficient.
- Validate input on the client for usability and on the server for security.
- Show loading, empty, and error states for every asynchronous operation.
- Support localization through resource files (`IStringLocalizer`); do not hard-code user-facing strings.
- Use responsive layouts that work on mobile and desktop.
- Use anti-forgery tokens for form posts.

## Security
Rules:
- Follow the OWASP Top 10 and OWASP ASVS.
- Authenticate with OpenID Connect / OAuth 2.0 (JWT bearer for APIs); authorize with policy-based authorization (`[Authorize(Policy = ...)]`) and deny by default.
- Store secrets in a secrets manager (Azure Key Vault, AWS Secrets Manager); use managed identities where available.
- Use parameterized queries or EF Core; never build SQL by string concatenation.
- Validate and encode all untrusted input and output; rely on Razor encoding and avoid `Html.Raw` on untrusted data.
- Enforce HTTPS and HSTS; set security headers (CSP, `X-Content-Type-Options`, `Referrer-Policy`).
- Configure CORS with explicit allowed origins; never use `AllowAnyOrigin` with credentials.
- Apply rate limiting (`Microsoft.AspNetCore.RateLimiting`) to public endpoints.
- Never log secrets, tokens, passwords, or PII; redact sensitive fields (`Microsoft.Extensions.Compliance.Redaction`).
- Use `System.Security.Cryptography` primitives and ASP.NET Core Data Protection; never implement custom cryptography.
- Return generic error messages to clients; keep stack traces out of responses.

## Observability
Rules:
- Instrument with OpenTelemetry (`OpenTelemetry.Extensions.Hosting`) for traces, metrics, and logs; export via OTLP.
- Set `service.name`, `service.version`, and `deployment.environment` resource attributes.
- Enable instrumentation for every component:
  - HTTP server: `OpenTelemetry.Instrumentation.AspNetCore`.
  - HTTP client: `OpenTelemetry.Instrumentation.Http`.
  - Database: `OpenTelemetry.Instrumentation.EntityFrameworkCore` / `SqlClient`.
  - Messaging: the broker's OpenTelemetry instrumentation (for example, Azure Service Bus, MassTransit, Confluent Kafka) with context propagation through message headers.
  - Cache: `OpenTelemetry.Instrumentation.StackExchangeRedis`.
- Use `ILogger<T>` with structured message templates; prefer source-generated `[LoggerMessage]` methods for hot paths.
- Log each action against a database, HTTP endpoint, message broker, cache, or external component with: operation name, target, outcome, and duration.
- Create custom `ActivitySource` spans for significant business operations and custom `Meter` instruments for business metrics.

### CorrelationId
Rules:
- Every log entry must include a `CorrelationId`.
- Middleware reads `X-Correlation-Id` from the inbound request, or generates one if absent, and returns it in the response header.
- Push the `CorrelationId` into the logging scope (`logger.BeginScope`) and add it as an `Activity` tag/baggage so it flows across HTTP calls and messages.
- Propagate `X-Correlation-Id` on all outbound HTTP calls (via a `DelegatingHandler`) and as a header on all published messages.
- Consumers restore the `CorrelationId` from message headers before processing.

Example:
```csharp
public sealed class CorrelationIdMiddleware(RequestDelegate next, ILogger<CorrelationIdMiddleware> logger)
{
    private const string HeaderName = "X-Correlation-Id";

    public async Task InvokeAsync(HttpContext context)
    {
        var correlationId = context.Request.Headers.TryGetValue(HeaderName, out var value) && !string.IsNullOrWhiteSpace(value)
            ? value.ToString()
            : Guid.NewGuid().ToString();

        context.Response.Headers[HeaderName] = correlationId;
        Activity.Current?.SetTag("correlation.id", correlationId);
        Activity.Current?.SetBaggage("correlation.id", correlationId);

        using (logger.BeginScope(new Dictionary<string, object> { ["CorrelationId"] = correlationId }))
        {
            await next(context);
        }
    }
}
```

## Scalability, Reliability, and Maintainability
Rules:
- Design services to be stateless and horizontally scalable.
- Use `IHttpClientFactory` with typed clients; never instantiate `HttpClient` per request.
- Apply resilience with `Microsoft.Extensions.Http.Resilience` (Polly): timeouts, retries with exponential backoff and jitter, and circuit breakers.
- Make message handlers idempotent; use the outbox pattern for reliable event publishing.
- Expose health checks (`/health/live`, `/health/ready`) covering every backing service.
- Implement graceful shutdown and honor cancellation tokens.
- Keep methods small and cohesive; keep cyclomatic complexity low.
- Enable .NET analyzers (`<AnalysisLevel>latest-recommended</AnalysisLevel>`) and enforce style with `.editorconfig`.
- Use EF Core migrations for schema changes; migrations must be backward compatible for rolling deployments.

## Dependency Management
Rules:
- Use Central Package Management (`Directory.Packages.props`) for all NuGet versions.
- Prefer first-party `Microsoft.Extensions.*` packages before adding third-party libraries.
- Add a dependency only when it provides clear value; justify new dependencies in the pull request.
- Pin exact versions; enable lock files (`RestorePackagesWithLockFile`) for reproducible restores.
- Scan for vulnerabilities (`dotnet list package --vulnerable`, Dependabot) and keep packages current.
- Verify licenses are compatible with the project.
- Never reference packages from untrusted feeds; configure sources in `nuget.config`.

## Performance
Rules:
- Use async I/O everywhere; avoid sync-over-async.
- Use `AsNoTracking()` for read-only EF Core queries; project to DTOs with `Select`; avoid N+1 queries.
- Paginate and stream large result sets (`IAsyncEnumerable<T>`).
- Cache with `HybridCache` / `IDistributedCache` where data is read-heavy; define explicit expiration.
- Minimize allocations in hot paths (`Span<T>`, `ArrayPool<T>`, `StringBuilder`); avoid LINQ in tight loops.
- Use `System.Text.Json` with source generation for high-throughput serialization.
- Enable response compression and output caching where appropriate.
- Measure before optimizing: use BenchmarkDotNet and profiling; track latency with OpenTelemetry metrics.
- Dispose `IDisposable`/`IAsyncDisposable` resources with `using` / `await using`.

## Validation Workflow
Before completing a code change, Copilot must:
1. Run `dotnet build` with zero errors and no new warnings.
2. Run `dotnet test` and confirm existing tests pass.
3. Confirm new public members are documented and new I/O paths are logged, traced, and carry the `CorrelationId`.
