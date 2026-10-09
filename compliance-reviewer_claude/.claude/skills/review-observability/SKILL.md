---
name: review-observability
description: 'Reviews structured logging, tracing and metrics in code against OpenTelemetry conventions, plus health check endpoints and SLO/SLI documentation. Use when the compliance-reviewer orchestrator delegates the Implementation / Observability subject.'
user-invocable: false
---

# Review: Observability

Assesses structured logging, distributed tracing and metrics instrumentation, using OpenTelemetry as the reference model. Also covers health check endpoints and SLO/SLI documentation — the source/doc-visible half of monitoring; the IaC-only half (alerting rules, dashboards-as-code) is reviewed by `review-monitoring`.

## Inputs

Logging/tracing/metrics setup, OpenTelemetry config, health check endpoints, SLO docs, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check logging is structured (key-value/JSON) rather than free-text string concatenation, with consistent correlation/trace IDs.
3. Check distributed tracing is instrumented (OpenTelemetry SDK or equivalent) across service boundaries, if the app calls other services.
4. Check metrics are emitted for key operations (request rate, latency, error rate) and exported to a backend.
5. Note gaps such as missing correlation IDs across async/queue boundaries.
6. Check a health check or liveness/readiness endpoint exists for deployable services.
7. Check SLOs (or at least SLIs) are documented anywhere in the repo.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
