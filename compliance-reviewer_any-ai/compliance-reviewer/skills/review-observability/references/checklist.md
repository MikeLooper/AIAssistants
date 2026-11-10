# Checklist — Observability

Subject: Observability

Each check is evaluated against the local standards elements it lists (see `standards/`). Every element belongs to exactly one check.
Sources: OTO = `standards/opentelemetry-observability.md`; WAFO = `standards/azure-well-architected-observability.md`.

| id | Sub-subject | Check | Default severity | Elements | Source |
|----|-------------|-------|-------------------|----------|--------|
| OBS-01 | Structured Logging | Logging is structured (consistent schema, templates or key-value pairs, proper severity, shared framework), not free-text concatenation | Warning | OTO-01–OTO-06, WAFO-01–WAFO-03 | OTO, WAFO |
| OBS-02 | Correlation & Context Propagation | Correlation and trace context propagate across requests, async work and message boundaries, and logs carry trace IDs | Warning | OTO-07–OTO-11, WAFO-04–WAFO-05 | OTO, WAFO |
| OBS-03 | Distributed Tracing | Distributed tracing (OpenTelemetry SDK, zero-code agent or equivalent) covers inbound/outbound calls with correct span names, kinds and attributes | Warning | OTO-12–OTO-22, WAFO-06–WAFO-07 | OTO, WAFO |
| OBS-04 | Metrics | Metrics cover request rate, latency (histograms) and errors on key operations, plus business, job and async signals, with bounded cardinality | Warning | OTO-23–OTO-27, WAFO-08–WAFO-12 | OTO, WAFO |
| OBS-05 | Telemetry Export | Metrics, traces and logs are exported to a backend or collector through external configuration, not only to the local console | Information | OTO-28–OTO-30, WAFO-13 | OTO, WAFO |
| OBS-06 | Health Endpoints | Long-running services expose health endpoints wired to probes: shallow liveness, readiness that reflects required dependencies, cheap read-only checks, no anonymous diagnostic detail | Warning | WAFO-14–WAFO-18, WAFO-32–WAFO-37 | WAFO |
| OBS-07 | SLOs & SLIs | SLOs with measurable SLIs are documented for the service and its critical flows | Information | WAFO-19–WAFO-23 | WAFO |
| OBS-08 | Telemetry Identity & Naming | Telemetry identifies its source (`service.name`, version, environment, instance) and follows semantic-convention naming and UTC timestamps | Information | OTO-31–OTO-36, WAFO-24–WAFO-25 | OTO, WAFO |
| OBS-09 | Error Recording | Errors and exceptions are recorded correctly: span status and `error.type`, exception object logged once at an impact-based severity | Warning | OTO-37–OTO-43, WAFO-26 | OTO, WAFO |
| OBS-10 | Telemetry Volume & Safety | Telemetry volume and safety are controlled: configurable verbosity, deliberate sampling, non-blocking and failure-isolated instrumentation, no sensitive data in telemetry attributes or baggage | Information | OTO-44–OTO-46, WAFO-27–WAFO-31 | OTO, WAFO |

Totals: 46 OTO + 37 WAFO = 83 elements across 10 checks.

Alert rules, dashboards-as-code, external probes and telemetry-store settings are reviewed by `review-monitoring` (MON-01 … MON-06), which is N/A without IaC.
