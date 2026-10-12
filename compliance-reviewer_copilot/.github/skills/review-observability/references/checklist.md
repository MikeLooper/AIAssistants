# Checklist — Observability

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| OBS-01 | Logging is structured (key-value/JSON) rather than free-text concatenation | Warning | https://opentelemetry.io/docs/ |
| OBS-02 | Correlation/trace IDs propagate across requests and async/queue boundaries | Warning | https://opentelemetry.io/docs/ |
| OBS-03 | Distributed tracing (OpenTelemetry SDK or equivalent) is instrumented for calls to other services | Warning | https://opentelemetry.io/docs/ |
| OBS-04 | Metrics are emitted for request rate, latency and error rate on key operations | Warning | https://opentelemetry.io/docs/ |
| OBS-05 | Metrics/traces are exported to a backend/collector, not just written to local console | Information | https://opentelemetry.io/docs/ |
| OBS-06 | A health check / liveness / readiness endpoint exists | Warning | https://learn.microsoft.com/azure/well-architected/operational-excellence/ |
| OBS-07 | SLOs or SLIs are documented | Information | https://learn.microsoft.com/azure/well-architected/operational-excellence/ |
