# Checklist — Reliability

Subject: Reliability

Each check is evaluated against the local standards elements it lists (see `standards/`). Every element belongs to exactly one check.
Source: AZRL = `standards/azure-reliability-resiliency.md`.

| id | Sub-subject | Check | Default severity | Elements | Source |
|----|-------------|-------|-------------------|----------|--------|
| REL-01 | Timeouts | Remote calls have timeouts (no infinite or disabled timeouts), shorter than the service's own inbound timeout, with retried operations bounded overall and blocking steps and locks expiring | Error | AZRL-01–AZRL-04 | AZRL |
| REL-02 | Transient-Fault Retries | Transient faults are retried safely: built-in or library retry, finite attempts, back-off with jitter, transient errors only, Retry-After honored, one retry layer, aggregate budget, short retries on user paths, central config, handled exhaustion | Warning | AZRL-05–AZRL-14 | AZRL |
| REL-03 | Idempotency | Non-idempotent operations aren't retried unsafely: idempotency keys or natural idempotency, stable keys, narrow retry scope, compensation for multi-step work, whole-transaction retries | Error | AZRL-15–AZRL-20 | AZRL |
| REL-04 | Circuit Breakers | Synchronous calls to remote dependencies are protected by correctly scoped, shared circuit breakers that compose with retries and whose open state is handled | Warning | AZRL-21–AZRL-26 | AZRL |
| REL-05 | Redundancy | More than one instance runs for each production compute component (or the platform manages redundancy); singletons self-restart; no business data lives only on an instance | Warning | AZRL-27–AZRL-29 | AZRL |
| REL-06 | Load Protection | Failures are isolated and load is controlled: bulkheads per dependency, graceful degradation, early load shedding, propagated back-pressure, paced calls to throttled dependencies, configurable instance-aware limits | Warning | AZRL-30–AZRL-35 | AZRL |
| REL-07 | Messaging & Background Jobs | Messages and background jobs are processed reliably: idempotent consumers with atomic dedup, dead-lettering, ack after processing, ordering, checkpoints, graceful shutdown, no overlapping schedules, durable queues, bounded consumer concurrency | Warning | AZRL-36–AZRL-47 | AZRL |
| REL-08 | In-Region High Availability | In-region high availability is configured: instances spread across zones or nodes, health-probe routing, automatic restart, HA tiers with failover for stateful dependencies, automated scaling | Information | AZRL-48–AZRL-52 | AZRL |

Totals: 52 AZRL elements across 8 checks.

Client reuse, pool sizing, offloading and autoscale thresholds are reviewed by `review-performance`; the HTTP contract of the repo's own APIs (429/503 shape, `Retry-After`, idempotency headers) by `review-api-design`; health-endpoint implementation and retry/breaker telemetry by `review-observability`; alerts by `review-monitoring`; cross-region redundancy and backups by `review-disaster-recovery`.
