# Azure Well-Architected Framework — Observability, health and reliability targets — localized summary

- Source site: learn.microsoft.com (azure/well-architected, plus one Azure Architecture Center pattern page)
- Pinned pages: see the page table below (path + `ms.date` at retrieval)
- Citation base: https://learn.microsoft.com/azure/well-architected/
  (page key `pat-hem` is outside this base: its URL is built from https://learn.microsoft.com/ + the full path in the table)
- Localized: 2026-11-08 · Elements: 37 (cap 100)
- Source name for `Finding.standard`: `Azure Well-Architected Framework` (also for `pat-hem` elements)
- Level: every element is `REVIEW` (the pages use no normative keywords); severity is the owning check's default.
- Every element is Scope G (generic). No element depends on Azure services.
- Anchor(s): `<page key>#<section anchor>`, primary first. Rows of the `dg-mon` antipattern table and bullets of the `pat-hem` "Problems and considerations" list have no anchors of their own, so they cite the section anchor.
- Citation URL: citation base + page path + `#` + primary anchor, with no locale segment. For `pat-hem`: `https://learn.microsoft.com/azure/architecture/patterns/health-endpoint-monitoring#<anchor>`.

| Key | Page path | ms.date |
|-----|-----------|---------|
| oe-check | operational-excellence/checklist | 2026-02-11 |
| re-check | reliability/checklist | 2023-11-15 |
| oe-obs | operational-excellence/observability | 2026-10-24 |
| dg-mon | design-guides/monitoring | 2026-02-18 |
| dg-hm | design-guides/health-modeling | 2026-02-11 |
| re-met | reliability/metrics | 2024-08-16 |
| re-mon | reliability/monitoring | 2026-10-24 |
| pat-hem | azure/architecture/patterns/health-endpoint-monitoring (full path from https://learn.microsoft.com/) | 2026-09-24 |

`oe-check` (OE:07) and `re-check` (RE:04, RE:10) are traceability only: OE:07 = design a monitoring system that captures operational telemetry; RE:04 = define reliability and recovery targets; RE:10 = measure and model the workload's health signals.

## OBS-01 — Logging is structured

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-01 | REVIEW | One configurable logging framework (or a shared logging library) is used across components, with common schemas and naming conventions. | app emits logs | oe-obs#emit-telemetry-from-workload-components, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |
| WAFO-02 | REVIEW | Telemetry is structured and both human- and machine-readable (JSON, MessagePack, Protobuf). | app emits logs | dg-mon#best-practices-for-instrumentation, dg-hm#add-application-logs |
| WAFO-03 | REVIEW | Events are logged at service boundaries: request start, duration and status, and dependency calls with duration, status, retries and errors. | service | dg-mon#phase-1---instrumentation, dg-hm#add-application-logs |

## OBS-02 — Correlation and trace context propagate

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-04 | REVIEW | A correlation (activity) ID is generated at the entry point when absent and propagated when supplied, across services, threads, queues and dependencies. | service | dg-mon#best-practices-for-instrumentation, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |
| WAFO-05 | REVIEW | Logs, metrics and traces share common identifiers across presentation, middle and data tiers. Correlation relies on IDs, not timestamps alone. | service | oe-obs#correlate-data-for-end-to-end-insights, dg-mon#correlation |

## OBS-03 — Distributed tracing is instrumented

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-06 | REVIEW | Instrumentation is vendor-neutral and language-agnostic (e.g. OpenTelemetry) and decoupled from a specific backend. | service | dg-mon#best-practices-for-instrumentation, oe-obs#emit-telemetry-from-workload-components |
| WAFO-07 | REVIEW | Distributed tracing covers the critical system flows end to end. | multi-service or dependency calls | dg-hm#implement-distributed-tracing, oe-obs#correlate-data-for-end-to-end-insights |

## OBS-04 — Metrics for request rate, latency and errors

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-08 | REVIEW | Request-level signals (rate, duration, status) are emitted, and meaningful business events or KPIs (e.g. orders placed) are instrumented alongside technical metrics. | service | dg-mon#phase-1---instrumentation, oe-obs#align-telemetry-with-health-and-kpi-models, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |
| WAFO-09 | REVIEW | Latency is measured so that percentiles (p50/p95/p99) can be derived, not only averages. | service | re-mon#monitor-user-experience |
| WAFO-10 | REVIEW | Critical scheduled or background jobs emit both execution and result-validity signals (ran on schedule; output non-empty and well-formed). | scheduled jobs in code | re-mon#monitor-workload-functionality |
| WAFO-11 | REVIEW | Flows accepted synchronously and completed asynchronously emit acceptance and completion signals (backlog or message age). Fallback paths (e.g. cache miss → database) are observable. | async processing | dg-hm#identify-health-signals |
| WAFO-12 | REVIEW | Dependency retries and transient-fault occurrences are counted or logged. | retry policies present | re-mon#detect-failure-modes, dg-mon#phase-1---instrumentation |

## OBS-05 — Telemetry is exported to a backend

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-13 | REVIEW | Telemetry leaves local silos (local files, console) through a consistent collection method into a central store. No manual retrieval from components. | deployable service | oe-obs#standardize-data-consolidation |

## OBS-06 — Health endpoint exists

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-14 | REVIEW | Each deployable long-running service exposes a health endpoint that an external probe (load balancer, orchestrator, watchdog) can call. | long-running service | dg-hm#use-health-probes |
| WAFO-15 | REVIEW | The health endpoint is wired to the host's probe mechanism (orchestrator probes, load-balancer health path, platform health-check setting) where those manifests are in scope. | deployment manifests in scope | dg-hm#use-health-probes, re-mon#monitor-all-layers-of-the-system |
| WAFO-16 | REVIEW | Health checks measure responsiveness of the app and of its critical components and dependencies, and can report degraded as well as unhealthy rather than a constant OK. | service with critical dependencies | dg-hm#use-health-probes, dg-hm#what-is-health-health-modeling-and-a-health-model |
| WAFO-17 | REVIEW | Health logic distinguishes transient from persistent faults, and a dependency with a working fallback degrades the result instead of failing it. | service with dependencies | dg-hm#use-platform-metrics-and-logs, dg-hm#model-the-design |
| WAFO-18 | REVIEW | Status APIs and admin summaries that the app exposes return fresh, accurate values. Stale cached state is detectable (e.g. a last-refreshed timestamp). | status API or admin summary in code | re-mon#monitor-administrative-dashboards-and-status-apis |
| WAFO-32 | REVIEW | Liveness is a shallow check: it reports whether the process can respond and doesn't call downstream dependencies, so a dependency outage doesn't cause restarts. | liveness endpoint or probe present | pat-hem#solution, pat-hem#endpoint-behavior |
| WAFO-33 | REVIEW | Readiness is a deep check of initialization and the dependencies required to serve requests; it returns non-2xx (e.g. 503) when a required check fails. Optional dependencies don't fail it. | service with required dependencies | pat-hem#solution, pat-hem#endpoint-behavior |
| WAFO-34 | REVIEW | Consumers that need different signals get separate endpoints or check groups (liveness vs readiness; core vs lower-priority services). Startup time is allowed for, not treated as failure. | more than one probe consumer, or slow startup | pat-hem#solution, pat-hem#problems-and-considerations |
| WAFO-35 | REVIEW | Health checks are bounded and cheap: a timeout per dependency check, degraded status or circuit breaker for unreliable dependencies, no heavy work per probe. A cached result's TTL fits the detection delay. | health checks call dependencies | pat-hem#problems-and-considerations, pat-hem#endpoint-behavior, pat-hem#when-to-use-this-pattern |
| WAFO-36 | REVIEW | Health checks are read-only: they don't change production data or trigger downstream workflows. A synthetic transaction that must write uses isolated test accounts and data. | health checks present | pat-hem#problems-and-considerations |
| WAFO-37 | REVIEW | Anonymous health responses return only the status a probe needs. Detailed diagnostics (dependency names, versions, error text) require authorization. An obscure path or port isn't access control. | health endpoint present | pat-hem#problems-and-considerations |

## OBS-07 — SLOs or SLIs are documented

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-19 | REVIEW | Reliability targets are documented: SLOs for the workload and its critical flows, each measurable through stated SLIs within a stated observability window. | deployable service | re-met#define-composite-slo-targets, re-met#determine-the-slo-scope, dg-hm#map-to-reliability-metrics |
| WAFO-20 | REVIEW | SLIs cover success rate, percentile latency and availability, plus throughput or capacity where they apply. | SLOs stated | re-met#consider-common-slos-and-influencing-factors |
| WAFO-21 | REVIEW | SLOs are kept distinct from SLAs. A platform SLA isn't adopted as an SLO without checking its coverage, and critical dependencies are included in composite targets. | SLOs or SLAs stated | re-met#set-availability-objectives, re-met#assess-the-impact-of-microsoft-slas, re-met#define-composite-slo-targets |
| WAFO-22 | REVIEW | SLO scope fits the deployment: per tenant for multitenant SaaS, per stamp for bulkhead multi-region deployments. | multitenant or multi-stamp | re-met#determine-the-slo-scope, re-met#implement-multiregion-targets |
| WAFO-23 | REVIEW | Business KPIs are defined alongside technical SLIs, and SLIs map to health states (healthy / degraded / unhealthy definitions). | SLOs stated | dg-hm#map-to-reliability-metrics, oe-obs#align-telemetry-with-health-and-kpi-models, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |

## OBS-08 — Telemetry identity and naming

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-24 | REVIEW | Telemetry consistently records source component, environment, deployment/version and operation name, plus tenant or user ID only where allowed. | telemetry present | dg-mon#best-practices-for-instrumentation, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |
| WAFO-25 | REVIEW | Timestamps are taken when the event occurs and recorded in a universal format (UTC). | telemetry present | dg-mon#best-practices-for-instrumentation, dg-mon#correlation |

## OBS-09 — Errors and exceptions are recorded

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-26 | REVIEW | Critical exceptions and failures are logged with enough detail for diagnosis (exception information, operation, dependency). | error handling present | oe-obs#emit-telemetry-from-workload-components, dg-mon#phase-1---instrumentation |

## OBS-10 — Telemetry volume, safety and configurability

| ID | Level | Requirement (summary) | Applies when | Anchor(s) |
|----|-------|-----------------------|--------------|-----------|
| WAFO-27 | REVIEW | Log verbosity is configurable per environment without a code change, levels are used properly, and high-volume components sample. | app emits logs | oe-obs#emit-telemetry-from-workload-components, dg-mon#best-practices-for-instrumentation, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |
| WAFO-28 | REVIEW | Logging is asynchronous (fire-and-forget) and kept off the request path, except where audit requires synchronous writes. | app emits logs | dg-hm#add-application-logs, re-mon#monitor-all-layers-of-the-system, oe-obs#emit-telemetry-from-workload-components |
| WAFO-29 | REVIEW | Telemetry failures (exporter or backend unavailable) don't cascade into application failures. Buffers are bounded and errors are contained. | telemetry SDK in use | oe-obs#emit-telemetry-from-workload-components |
| WAFO-30 | REVIEW | Telemetry is classified by concern (audit, security, diagnostic, performance). Audit logs are kept separate from diagnostic logs; workload data isn't written into telemetry. | app emits logs | oe-obs#emit-telemetry-from-workload-components, dg-hm#add-application-logs, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |
| WAFO-31 | REVIEW | Telemetry-specific sensitive data is scrubbed before export while diagnostic context is kept. (Secrets/PII in log messages belong to the security skills.) | telemetry present | oe-obs#emit-telemetry-from-workload-components, dg-mon#telemetry-data-security, dg-mon#monitoring-antipatterns-and-how-to-avoid-them |
