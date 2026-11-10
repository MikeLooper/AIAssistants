# OpenTelemetry — Application instrumentation — localized summary

- Source site: opentelemetry.io (docs; semantic conventions; specification)
- Pinned versions: Semantic Conventions **v1.45.0**; Specification **v1.62.0**; concept, SDK-configuration, Collector and security pages pinned by the opentelemetry.io commit shown in each page's "Last modified" footer (page table below)
- Citation base: https://opentelemetry.io/docs/
- Licence: CC BY 4.0 (docs). Rows are summaries in our own words.
- Localized: 2026-11-08 · Elements: 46 (cap 100)
- Source name for `Finding.standard`: `OpenTelemetry`
- Level: the strongest RFC 2119 keyword in the summarized sentences (`MUST`, `SHOULD`; lower-case "should"/"we recommend" on concept pages counts as `SHOULD`), otherwise `REVIEW`. Severity is always the owning check's default.
- Stab. column: `S` = stable; `D` = Development status in the pinned version. A `D` element applies only when the repo already uses that convention; otherwise report it only with confidence `low` and never above the check default.
- Anchor(s): `<page key>#<section anchor>`, primary first. A bare page key (no `#`) cites a page without section anchors.
- Citation URL: citation base + page path + `#` + primary anchor (no anchor for a bare page key).

| Key | Page path | Version / status |
|-----|-----------|------------------|
| c-logs | concepts/signals/logs/ | commit c161165 (2026-08-07) |
| c-traces | concepts/signals/traces/ | commit 6bf06dd (2026-01-14) |
| c-metrics | concepts/signals/metrics/ | commit 6524d48 (2026-07-02) |
| c-prop | concepts/context-propagation/ | commit 89a269b (2026-08-10) |
| c-res | concepts/resources/ | commit 8ada5a9 (2026-02-10) |
| c-samp | concepts/sampling/ | commit 6b2e90b (2025-10-16) |
| c-inst | concepts/instrumentation/ | commit 58e6847 (2026-02-21) |
| c-code | concepts/instrumentation/code-based/ | commit 8d7aa29 (2024-03-04) |
| c-zero | concepts/instrumentation/zero-code/ | commit d1ef521 (2025-03-21); no section anchors |
| c-semconv | concepts/semantic-conventions/ | commit 6b6b228 (2026-09-28); no section anchors |
| sdk-gen | languages/sdk-configuration/general/ | commit c8d0756 (2026-02-25) |
| sdk-otlp | languages/sdk-configuration/otlp-exporter/ | commit 2cde6bd (2026-10-08) |
| col | collector/ | commit 17662c2 (2026-11-08) |
| sec | security/handling-sensitive-data/ | commit 4edfbfc (2026-01-14) |
| sc-svc | specs/semconv/registry/attributes/service/ | semconv 1.45.0, Stable |
| sc-res | specs/semconv/resource/ | semconv 1.45.0, Mixed (Environment section Development) |
| sc-http-spans | specs/semconv/http/http-spans/ | semconv 1.45.0, Stable |
| sc-http-metrics | specs/semconv/http/http-metrics/ | semconv 1.45.0, Mixed (duration histograms Stable) |
| sc-err | specs/semconv/general/recording-errors/ | semconv 1.45.0, Development |
| sc-exc-logs | specs/semconv/exceptions/exceptions-logs/ | semconv 1.45.0, Stable except When-not-to-record, Event name, Severity (Development) |
| sc-msg | specs/semconv/messaging/messaging-spans/ | semconv 1.45.0, Development |
| sc-db | specs/semconv/db/database-spans/ | semconv 1.45.0, Stable |
| spec-logdm | specs/otel/logs/data-model/ | Specification 1.62.0, Stable |

## OBS-01 — Logging is structured

| ID | Level | Stab. | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| OTO-01 | REVIEW | S | Logs use a consistent structured schema with stable field names and types. Valid JSON with varying fields isn't enough. | app emits logs | c-logs#structured-logs, c-logs#semistructured-logs |
| OTO-02 | REVIEW | S | Production code paths don't emit unstructured free text built by concatenation or interpolation; they use a standard logging framework with templates or key-value pairs. | app emits logs | c-logs#unstructured-logs |
| OTO-03 | SHOULD | S | Application code logs through an established logging library bridged to OpenTelemetry by an appender/bridge; it doesn't call the Logs Bridge API (Logger, LoggerProvider) directly. | OpenTelemetry logs in use | c-logs#log-appender--bridge, c-logs#logger, c-logs#logger-provider |
| OTO-04 | SHOULD | S | Log records carry a severity mapped consistently to TRACE/DEBUG/INFO/WARN/ERROR/FATAL. Error conditions are logged at ERROR or above, not INFO. | app emits logs | spec-logdm#severity-fields |
| OTO-05 | SHOULD | S | Per-event context goes in attributes, not interpolated into the body. Well-known fields use semconv names. Event-shaped records use a stable event name. | app emits logs | spec-logdm#field-attributes, spec-logdm#field-body, spec-logdm#field-eventname |
| OTO-06 | SHOULD | S | `IsEnabled`/`Enabled` guards are used only around costly argument evaluation, guarded code has no side effects, and the result is evaluated per record, not cached. | log guards present | c-logs#checking-whether-logging-is-enabled |

## OBS-02 — Correlation and trace context propagate

| ID | Level | Stab. | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| OTO-07 | REVIEW | S | Logs emitted inside an active span carry TraceId and SpanId (through the SDK, appender or log-scope enrichment), so logs correlate with traces. | logs + tracing | c-logs#opentelemetry-logs-for-applications, spec-logdm#trace-context-fields |
| OTO-08 | REVIEW | S | Context crosses process boundaries through propagators (inject on send, extract on receive). W3C Trace Context (`traceparent`) is the default; custom header schemes need a reason. | service calls or receives remote calls | c-prop#propagation, sdk-gen#otel_propagators |
| OTO-09 | SHOULD | D | Message producers attach a creation context to each message. Consumers extract it and link to it (span links by default; parent only for single-message processing). | message broker in use | sc-msg#context-propagation, sc-msg#trace-structure |
| OTO-10 | REVIEW | S | In-process asynchronous work (threads, executors, background tasks, callbacks) carries the current context, so child spans attach to the right parent. | async or background work | c-prop#context, c-traces#context-propagation, c-traces#span-context |
| OTO-11 | REVIEW | S | When context is carried in a custom protocol or payload, the receiver extracts it and removes it before processing. | custom carrier | c-prop#custom-context-propagation |

## OBS-03 — Distributed tracing is instrumented

| ID | Level | Stab. | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| OTO-12 | REVIEW | S | Tracer, Meter and Logger providers are configured once at startup, live for the app's lifetime, and are given a Resource and exporters. They are never created per request. | code-based mode | c-traces#tracer-provider, c-metrics#meter-provider, c-logs#logger-provider, c-code#configure-the-opentelemetry-api |
| OTO-13 | SHOULD | S | Tracers and meters are obtained from the provider and named after the instrumented component or library, with a version. | code-based mode | c-code#configure-the-opentelemetry-api, c-traces#tracer, c-metrics#meter |
| OTO-14 | REVIEW | S | Inbound and outbound frameworks (HTTP server and client, database, messaging) are covered by instrumentation libraries or a zero-code agent, not left uninstrumented. | service calls or receives remote calls | c-code#create-telemetry-data, c-zero, c-inst |
| OTO-15 | SHOULD | S | Libraries depend only on the OpenTelemetry API. The SDK and exporters are wired only in the application. | library or multi-module repo | c-code#import-the-opentelemetry-api-and-sdk, c-inst#additional-opentelemetry-benefits |
| OTO-16 | REVIEW | S | Key business operations have custom spans with meaningful low-cardinality names. Every span is ended on all paths (finally/using/with) and sits under the correct parent. | custom spans present or business-critical flow | c-traces#spans |
| OTO-17 | REVIEW | S | Span kind matches direction: SERVER inbound, CLIENT outbound synchronous calls, PRODUCER/CONSUMER for queued jobs, INTERNAL for in-process work. | custom spans present | c-traces#span-kind |
| OTO-18 | MUST | S | HTTP span names are `{method} {http.route}` for servers (`{method}` or `url.template` for clients). The raw URI path is never the span name. | custom HTTP spans or naming config | sc-http-spans#name |
| OTO-19 | SHOULD | S | Custom HTTP spans carry the required attributes (method, route or path, scheme, status code; server address and port for clients). `http.route` is set at creation when known. | custom HTTP spans | sc-http-spans#http-server-span, sc-http-spans#http-client-span |
| OTO-20 | SHOULD | S | Custom DB spans use CLIENT kind and set `db.system.name` and the operation/collection. Query text is captured only parameterized or sanitized; parameter values are opt-in. | custom DB spans or DB instrumentation options | sc-db#span-definition, sc-db#sanitization-of-dbquerytext |
| OTO-21 | SHOULD | D | Custom messaging spans are named `{operation} {destination}`, use the kind defined per operation, and set `messaging.system.name` and `messaging.operation.name`. | custom messaging spans | sc-msg#span-name, sc-msg#span-kind |
| OTO-22 | REVIEW | S | Attributes are set at span start when available (for samplers) and use semconv names. Span events record timestamped occurrences; links record non-parent causal relations. | custom spans present | c-traces#attributes, c-traces#when-to-use-span-events-versus-span-attributes, c-traces#span-links |

## OBS-04 — Metrics for request rate, latency and errors

| ID | Level | Stab. | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| OTO-23 | SHOULD | S | HTTP request duration is recorded as a histogram in seconds (`http.server.request.duration`, `http.client.request.duration`) or an equivalent RED metric; rate and errors derive from it. | HTTP service or client | sc-http-metrics#metric-httpserverrequestduration, sc-http-metrics#metric-httpclientrequestduration |
| OTO-24 | REVIEW | S | Each custom metric uses the fitting instrument: Counter (monotonic), UpDownCounter (in-flight, queue size), Histogram (durations, sizes), gauge (sampled state). Units follow semconv (`s`, `By`). | custom metrics present | c-metrics#metric-instruments |
| OTO-25 | MUST | S | Metric attributes have bounded cardinality: no user, request or session IDs and no raw paths. Use route templates; unknown HTTP methods are reported as `_OTHER`. | metrics present | c-metrics#cardinality-limits, sc-http-metrics#http-server |
| OTO-26 | REVIEW | S | Constant context (service, region, environment) is on the Resource, not repeated as an attribute on every metric. | metrics present | c-metrics#what-the-limit-does-not-apply-to |
| OTO-27 | REVIEW | S | Views that drop instruments, change aggregation or filter attributes are deliberate. Histogram buckets cover the service's latency range (semconv default 5 ms – 10 s). | views or bucket config present | c-metrics#views, c-metrics#aggregation, sc-http-metrics#metric-httpserverrequestduration |

## OBS-05 — Telemetry is exported to a backend

| ID | Level | Stab. | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| OTO-28 | REVIEW | S | Production configuration exports traces, metrics and logs over OTLP or a supported backend exporter. A console exporter is used only for development. | deployable service | c-traces#trace-exporters, c-metrics#metric-exporter, c-logs#log-record-exporter |
| OTO-29 | REVIEW | S | Exporter endpoint, protocol, headers and timeout come from configuration (`OTEL_EXPORTER_OTLP_*` or a config file), not hard-coded values; header credentials come from secret config. | exporter configured | sdk-otlp#endpoint-configuration, sdk-otlp#header-configuration, sdk-otlp#timeout-configuration, sdk-otlp#protocol-configuration, c-code#configure-the-opentelemetry-sdk |
| OTO-30 | SHOULD | S | Production deployments send telemetry through a Collector (agent, sidecar or gateway) for batching, retries, encryption and filtering. Direct export is fine for development or small setups. | deployable service | col#when-to-use-a-collector, c-code#export-data |

## OBS-08 — Telemetry identity and naming

| ID | Level | Stab. | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| OTO-31 | MUST | S | `service.name` is set explicitly (`OTEL_SERVICE_NAME` or the Resource), is identical across instances of the service, and is never left as `unknown_service`. | telemetry SDK or agent in use | sc-svc#service-attributes, c-res#semantic-attributes-with-sdk-provided-default-value, sdk-gen#otel_service_name |
| OTO-32 | REVIEW | S | `service.version` is set to the deployed artifact version (semver, build number or commit), not a constant. | telemetry SDK or agent in use | sc-svc#service-attributes, sc-res#service |
| OTO-33 | REVIEW | D | `deployment.environment.name` (or the platform equivalent) is set from configuration per environment. | telemetry SDK or agent in use | c-res#custom-resources, sc-res#environment |
| OTO-34 | MUST | S | `service.namespace` groups related services where several share a name. `service.instance.id` is unique per instance (SDK or detector default is fine). | multi-service repo | sc-svc#service-attributes |
| OTO-35 | REVIEW | S | Resource detectors (host, container, Kubernetes, cloud) are enabled where available, instead of hand-coding host information into attributes. | code-based mode | c-res#resource-detectors |
| OTO-36 | REVIEW | S | Custom telemetry names follow the semantic conventions (pinned version), not ad-hoc names. Semconv upgrades (`OTEL_SEMCONV_STABILITY_OPT_IN`) are adopted deliberately. | custom telemetry present | c-semconv, sc-http-metrics#http-server |

## OBS-09 — Errors and exceptions are recorded

| ID | Level | Stab. | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| OTO-37 | MUST | D | Failed operations set span status Error and `error.type`; successful ones leave status Unset (no blanket Ok). Status description is the exception message when not sensitive. | custom spans present | sc-err#recording-errors-on-spans, c-traces#span-status |
| OTO-38 | MUST | S | HTTP status mapping: 5xx sets Error; 4xx sets Error on client spans only and stays Unset on server spans. Caller cancellation isn't an error. | custom HTTP spans or status mapping code | sc-http-spans#status |
| OTO-39 | SHOULD | D | Errors that were retried or handled aren't recorded as failures of that operation. A propagating exception is recorded once, not logged again at every layer. | error handling present | sc-err#what-constitutes-an-error, sc-err#recording-exceptions |
| OTO-40 | MUST | S | Exceptions are logged with the exception object (type, message, stack trace), not only `ex.Message`, and within the active span's context. | exception logging present | sc-exc-logs#recording-an-exception |
| OTO-41 | SHOULD | D | Exception severity reflects impact: FATAL process-ending, ERROR unhandled, WARN expected/handled, DEBUG cancellation. A global unhandled-exception handler logs at ERROR or FATAL. | exception logging present | sc-exc-logs#severity, sc-exc-logs#event-name |
| OTO-42 | SHOULD | D | Duration metrics carry `error.type` on failure only, with the same value as the span. One metric covers success and failure (no separate failure counters). | custom metrics present | sc-err#recording-errors-on-metrics |
| OTO-43 | SHOULD | D | Framework exceptions that only carry an HTTP status (e.g. `HTTPException`, `ResponseStatusException`) aren't recorded as exceptions. | such exceptions used | sc-exc-logs#when-not-to-record-exceptions |

## OBS-10 — Telemetry volume, safety and configurability

| ID | Level | Stab. | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-------|-----------------------|--------------|-----------|
| OTO-44 | REVIEW | S | Sampling is a deliberate, configured policy (`OTEL_TRACES_SAMPLER` or code). Default parent-based always-on is fine at low volume; high volume (≈ 1000+ traces/s) uses ratio and/or tail sampling keeping errors; nothing sampled where data mustn't drop. | tracing present | c-samp#when-to-sample, c-samp#when-not-to-sample, c-samp#head-sampling, c-samp#tail-sampling, sdk-gen#otel_traces_sampler |
| OTO-45 | MUST | S | Telemetry attributes hold no credentials or unneeded personal data: `url.full` has no user info and sensitive query values are redacted, headers/bodies aren't captured by default, user IDs are minimized or hashed. | tracing or metrics present | sec#data-minimization, sec#protecting-sensitive-data, sc-http-spans#http-client-span |
| OTO-46 | REVIEW | S | Baggage carries no credentials, API keys or PII; context isn't propagated unfiltered to external services, and incoming context from untrusted sources is ignored or sanitized. | baggage used or external calls | c-prop#baggage, c-prop#external-services |
