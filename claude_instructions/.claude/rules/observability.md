---
paths:
  - "src/PilotApi.Shared/Logging/**"
  - "src/PilotApi.Shared/OpenTelemetry/**"
  - "src/PilotApi.Shared/Api/Middleware/**"
  - "src/PilotApi.Shared/Api/Filters/**"
  - "src/PilotApi.Shared/Models/RequestSettings.cs"
  - "src/PilotApi.Shared/Constants/*Constants.cs"
  - "src/PilotApi.Web/appsettings*.json"
---

# Request context, logging and telemetry

- `RequestSettings` is a scoped object holding `RequestId`, `CorrelationId` and `CallerName`. `RequestSettingsMiddleware` fills it from the `X-Correlation-Id` and `X-Caller-Name` headers and pushes all three onto the Serilog `LogContext` for the rest of the request. It also writes the `X-Correlation-Id`/`X-Request-Id` response headers. ProblemDetails responses include the IDs as extensions.
- `UnhandledExceptionMiddleware` runs before `RequestSettingsMiddleware`, so its Serilog events don't carry the log-context properties.
- `EndpointLoggingFilter`, a global MVC resource filter, logs endpoint start/end with status code and duration. Repository calls log their own start/end (see `RepositoryBase`).
- Serilog is registered with `writeToProviders: true` so events also reach the OpenTelemetry provider. The pipeline exports over OTLP to a collector, then Loki/Tempo/Mimir, then Grafana. OTEL log records and spans get the request IDs from `EnrichLogsWithCustomRequestDataProcessor` / `EnrichActivityWithCustomRequestDataProcessor`, not from the Serilog log context.
- The server span starts before the middleware runs, so the ASP.NET Core instrumentation's `EnrichWithHttpRequest` reads the headers directly.
- Property and attribute names are in `LogContextPropertyConstants` (Serilog), `OtelLogRecordAttributesConstants` and `OtelActivityTagsConstants`. The Serilog and OTEL request-ID names differ: `RequestId` vs `Request.Id`.
- The Serilog Console `outputTemplate` in `appsettings.json` prints CorrelationId, RequestId and CallerName.
