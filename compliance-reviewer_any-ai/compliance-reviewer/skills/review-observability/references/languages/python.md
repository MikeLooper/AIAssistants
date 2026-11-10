# Language Signals — Python (Observability)

Local lookup table, not a standard. Use it to classify code and configuration for OBS-01 … OBS-10; cite the standards elements, never this file. If a library isn't listed and you can't classify it, add `localized-standard-gap: unrecognized library <name>` to `notes`.

| Area | Pass signals | Anti-patterns / fail signals |
|---|---|---|
| Structured logging (OBS-01) | `logging` with lazy `%s` args and `extra={...}` plus a JSON formatter (python-json-logger), `structlog`, loguru `bind()` / `serialize=True`, `logging.config.dictConfig` | f-strings or `.format()` / `%` strings evaluated before the call (`log.info(f"user {u}")`); `print()` for diagnostics |
| Log levels (OBS-01, OBS-10) | level from env/config (`LOG_LEVEL`, `dictConfig`, `logging.conf`) | errors logged with `info`; `logging.basicConfig(level=DEBUG)` hard-coded for production |
| OpenTelemetry setup, code-based (OBS-03, OBS-05) | `TracerProvider` / `MeterProvider` / `LoggerProvider` set once at startup (`trace.set_tracer_provider`), `opentelemetry-sdk`, `opentelemetry-distro`, `OTLPSpanExporter` configured from env | `ConsoleSpanExporter` as the only production exporter; provider created per request; endpoint hard-coded |
| Zero-code (instrumentation mode) | `opentelemetry-instrument` launcher in Dockerfile/Procfile/entrypoint, `opentelemetry-bootstrap -a install`, `OTEL_*` env vars; Operator annotation `instrumentation.opentelemetry.io/inject-python` | — |
| Instrumentation libraries (OBS-03) | `opentelemetry-instrumentation-{fastapi,flask,django,requests,httpx,sqlalchemy,psycopg,psycopg2,kafka-python,confluent-kafka,celery}` | outbound `requests`/`httpx` calls uninstrumented where the rest of the app is instrumented |
| Context propagation (OBS-02) | `contextvars`-based context (automatic across `asyncio` tasks), `opentelemetry.propagate.inject/extract` for message headers, `opentelemetry.context.attach/detach` in thread pools | work submitted to `ThreadPoolExecutor` without carrying context in code-based mode; correlation ID not forwarded |
| Metrics (OBS-04) | `meter.create_counter/create_histogram/create_up_down_counter/create_observable_gauge`; `prometheus_client` `Histogram`/`Counter` (equivalent) | labels from user IDs or raw paths |
| Identity (OBS-08) | `OTEL_SERVICE_NAME`, `Resource.create({"service.name": ..., "service.version": ...})`, `OTEL_RESOURCE_ATTRIBUTES` | no service name; version constant |
| Health checks (OBS-06) | separate FastAPI/Flask/Django routes for live and ready, `django-health-check`, Kubernetes `livenessProbe`/`readinessProbe`/`startupProbe` paths in manifests | one route doing DB checks used as liveness probe; exception text or dependency details returned on an anonymous route (WAFO-37) |
| Exception logging (OBS-09) | `logger.exception(...)` or `exc_info=True`, `span.record_exception(e)` + `span.set_status(Status(StatusCode.ERROR))`, framework error handler logging unhandled exceptions | `logger.error(str(e))` without traceback; log-and-reraise at every layer; FastAPI `HTTPException` recorded as an error exception |
| Vendor SDK (equivalent) | `azure-monitor-opentelemetry` (`configure_azure_monitor()`), `ddtrace`, `newrelic`, `elastic-apm` | — |
