# Checklist — Performance

Each check is evaluated against the local standards elements it lists (see `standards/`). Every element belongs to exactly one check.
Source: AZPE = `standards/azure-performance-efficiency.md`.

| id | Check | Default severity | Elements | Source |
|----|-------|-------------------|----------|--------|
| PERF-01 | Expensive or repeated reads are cached with bounded size, expiry matched to volatility, invalidation on write, graceful fallback, and multi-instance-safe, user-scoped keys | Warning | AZPE-01–AZPE-12 | AZPE |
| PERF-02 | I/O in request paths doesn't block: async APIs on async-first stacks, no blocking on async results, independent calls concurrent, and fan-out bounded | Warning | AZPE-13–AZPE-18 | AZPE |
| PERF-03 | Shareable clients (HTTP, messaging, DB/SDK, cache) and expensive objects are created once and reused; connections are pooled, released promptly and sized explicitly | Warning | AZPE-19–AZPE-24 | AZPE |
| PERF-04 | No N+1 query patterns or chatty I/O: related data loaded eagerly or in batches, writes batched, coarse-grained remote calls, buffered file I/O, bounded batches | Warning | AZPE-25–AZPE-29 | AZPE |
| PERF-05 | No repeated expensive work in hot paths: invariants hoisted, fitting data structures, low allocation, memoized computations, limited logging in loops | Information | AZPE-30–AZPE-34 | AZPE |
| PERF-06 | Data retrieval is efficient: projection, filtering and aggregation in the store, bounded queries, no business logic in the DB, separate stores for logs and queues, indexes, optimistic concurrency | Warning | AZPE-35–AZPE-41 | AZPE |
| PERF-07 | Long-running and resource-intensive work is offloaded from request paths to managed, independently scaled workers, scheduled or prioritized appropriately | Warning | AZPE-42–AZPE-46 | AZPE |
| PERF-08 | The app is ready to scale out and serves efficiently: sound autoscale triggers, resource limits, compression/HTTP/2, CDN for static content, no singleton bottleneck (statelessness and sticky sessions: review-twelve-factor TF-06) | Information | AZPE-49–AZPE-53 | AZPE |

Totals: 53 AZPE elements across 8 checks.

Retries, timeouts and circuit breakers are reviewed by `review-reliability`; the HTTP API contract (caching headers, pagination, long-running operations) by `review-api-design`; instrumentation and telemetry volume by `review-observability`.
