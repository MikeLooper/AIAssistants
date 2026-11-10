# Language Signals — C#/.NET (Reliability)

Local lookup table, not a standard. Use it to classify code and configuration for REL-01 … REL-08; cite the AZRL elements, never this file. If a library isn't listed and you can't classify it, add `localized-standard-gap: unrecognized library <name>` to `notes`.

## Default timeouts (AZRL-01, SKILL.md step 3)

| Client | Default timeout | AZRL-01 |
|---|---|---|
| `HttpClient` | 100 s (`Timeout`) | pass with note; `Timeout.InfiniteTimeSpan` fails |
| Standard resilience handler (`AddStandardResilienceHandler`, Microsoft.Extensions.Http.Resilience) | total request 30 s, per attempt 10 s; retry and circuit breaker included | pass |
| ADO.NET / `SqlClient` | command 30 s, connect 15 s | pass with note; `CommandTimeout = 0` (infinite) fails |
| EF Core | provider command timeout (30 s for SQL Server) | pass with note; `SetCommandTimeout(0)` fails |
| gRPC (`Grpc.Net.Client`) | no deadline | **fail** unless a deadline is set (`deadline:` on the call, or a resilience/timeout handler on the channel) |
| Azure SDK clients (Azure.Core) | network timeout 100 s; built-in retry on (exponential, 3 retries) | pass with note |
| StackExchange.Redis | connect 5 s, sync 5 s, async = sync | pass with note |

## Signals

| Area | Pass signals | Anti-patterns / fail signals |
|---|---|---|
| Retries (REL-02) | `AddStandardResilienceHandler`; Polly v8 `AddRetry` with `BackoffType.Exponential` + `UseJitter = true`, `MaxRetryAttempts`; EF Core `EnableRetryOnFailure`; Azure SDK `RetryOptions` (`Mode = Exponential`); policies built from `IConfiguration` / `IOptions`; `ShouldHandle` limited to transient results (`HttpRequestException`, 408/429/5xx) | `while (true)` / `for (;;)` around remote calls; Polly v7 `RetryForever` / `WaitAndRetryForever`; `Handle<Exception>()` with no status filter; fixed `Task.Delay` with high attempt counts; Polly retry around an Azure SDK client that already retries (AZRL-10); ignoring `RetryAfter` |
| Idempotency (REL-03) | `options.Retry.DisableForUnsafeHttpMethods()` or `DisableFor(HttpMethod.Post, …)` on the standard handler; idempotency-key header created once per operation; EF execution strategy wrapping the whole transaction (`Database.CreateExecutionStrategy().ExecuteAsync`) | standard resilience handler on a client that POSTs non-idempotent operations without a key; `EnableRetryOnFailure` with user-initiated `BeginTransaction` outside an execution strategy |
| Circuit breakers (REL-04) | `AddCircuitBreaker` in a pipeline registered once (DI, `AddResiliencePipeline`, `AddResilienceHandler`); breaker inside the retry; `BrokenCircuitException` handled | breaker or `ResiliencePipelineBuilder` built inside the request method; one named pipeline shared by unrelated downstream services |
| Isolation and load (REL-06) | per-client `AddConcurrencyLimiter` / bulkhead; ASP.NET Core `AddRateLimiter` + `UseRateLimiter` early in the pipeline, limits from config; fallback strategy (`AddFallback`) for optional dependencies | catching a downstream 429/503 and returning 500; optional-dependency exceptions bubbling to a 500 |
| Messaging and jobs (REL-07) | Service Bus processor in `PeekLock` with default `AutoCompleteMessages` (completes after the handler) or explicit `CompleteMessageAsync`; `DeadLetterMessageAsync` for permanent errors; `MaxConcurrentCalls` set; MassTransit / NServiceBus outbox or inbox; unique index on processed-message ID; `BackgroundService` honoring `stoppingToken`; `HostOptions.ShutdownTimeout` set; Quartz `[DisallowConcurrentExecution]` + clustered job store; Hangfire `DisableConcurrentExecution` | `ServiceBusReceiveMode.ReceiveAndDelete` for work that must not be lost; catch-all that completes failed messages; `Channel<T>` / `ConcurrentQueue` as the only buffer for must-not-lose work; ignoring `stoppingToken`; `Timer`-based jobs on several instances without a lock |
