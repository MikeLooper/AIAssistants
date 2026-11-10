# Azure reliability and resiliency guidance — localized summary

- Source site: learn.microsoft.com (azure/well-architected and azure/architecture)
- Pinned pages: see the page table below (path, `ms.date`, "Last updated" and git commit at retrieval)
- Citation base: https://learn.microsoft.com/azure/
- Localized: 2026-11-08 · Elements: 52 (cap 100)
- Source name for `Finding.standard`: the Source name of the element's primary page (first anchor). The **Src** column gives it: **W** = `Azure Well-Architected Framework`, **A** = `Azure Architecture Center`.
- Level: every element is `REVIEW` (the pages use no normative keywords); severity is the owning check's default.
- Every element is Scope G (generic). No element depends on Azure services. Azure product names in the sources (Service Bus, Front Door, API Management, Chaos Studio) are generalized to "message broker", "gateway", "fault injection". Platform-specific settings live in `../reliability-config-signals.md`.
- Anchor(s): `<page key>#<section anchor>`, primary first. Bullet-level guidance has no anchor of its own and cites its section anchor.
- Citation URL: citation base + page path + `#` + primary anchor, with no locale segment. Examples: `https://learn.microsoft.com/azure/architecture/best-practices/transient-faults#avoid-antipatterns`, `https://learn.microsoft.com/azure/well-architected/reliability/self-preservation#implement-a-graceful-degradation-mode`.

| Key | Page path | Source name | ms.date | Last updated | Git commit |
|-----|-----------|-------------|---------|--------------|------------|
| re-check | well-architected/reliability/checklist | Azure Well-Architected Framework | 2023-11-15 | 2026-05-29 | 687e8febe6dd |
| re-prin | well-architected/reliability/principles | Azure Well-Architected Framework | 2025-09-30 | 2025-09-30 | e565e8c63950 |
| re-red | well-architected/reliability/redundancy | Azure Well-Architected Framework | 2025-08-13 | 2025-09-09 | 84b9446eb8fc |
| re-scale | well-architected/reliability/scaling | Azure Well-Architected Framework | 2025-05-29 | 2025-05-29 | 28a78d225235 |
| re-sp | well-architected/reliability/self-preservation | Azure Well-Architected Framework | 2026-06-20 | 2026-08-21 | ced3ebc11c89 |
| re-fma | well-architected/reliability/failure-mode-analysis | Azure Well-Architected Framework | 2026-07-14 | 2026-08-21 | ddb1377836ee |
| bp-tf | architecture/best-practices/transient-faults | Azure Architecture Center | 2026-02-26 | 2026-02-26 | d6ef15167b11 |
| bp-bg | architecture/best-practices/background-jobs | Azure Architecture Center | 2026-03-30 | 2026-03-31 | 03e41c0834ab |
| pat-retry | architecture/patterns/retry | Azure Architecture Center | 2024-07-18 | — (no footer) | cb69919fc6c9 |
| pat-cb | architecture/patterns/circuit-breaker | Azure Architecture Center | 2025-02-05 | 2025-03-21 | 9fdb775034a2 |
| pat-bh | architecture/patterns/bulkhead | Azure Architecture Center | 2026-03-19 | 2026-03-19 | 02e4881cd2c9 |
| pat-thr | architecture/patterns/throttling | Azure Architecture Center | 2026-05-29 | 2026-05-30 | 8ba9a37b0455 |
| pat-rl | architecture/patterns/rate-limiting-pattern | Azure Architecture Center | 2026-06-08 | 2026-06-15 | 15cfa4cb8710 |
| pat-qbll | architecture/patterns/queue-based-load-leveling | Azure Architecture Center | 2026-06-09 | 2026-06-12 | d73cd1632ffa |
| pat-cc | architecture/patterns/competing-consumers | Azure Architecture Center | 2026-04-02 | 2026-04-03 | 282a7f99b9f7 |
| pat-ic | architecture/patterns/idempotent-consumer | Azure Architecture Center | 2026-08-13 | 2026-09-05 | dcf29659535a |
| pat-ct | architecture/patterns/compensating-transaction | Azure Architecture Center | 2026-04-16 | 2026-04-20 | 0244238b6c53 |
| ap-rs | architecture/antipatterns/retry-storm/ | Azure Architecture Center | 2025-07-16 | 2025-08-11 | 91bbd0ff1799 |

`re-check` (RE:01–RE:10) is traceability and drift only; no element cites it.

## REL-01 — Explicit timeouts on remote calls

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZRL-01 | A | Every remote call (HTTP/gRPC, DB, cache, broker, SDK) has a timeout. Explicitly disabled timeouts and clients whose library default is "none" fail; finite defaults pass with a note. | remote-call rule (SKILL.md step 2) | bp-tf#determine-an-appropriate-retry-count-and-interval, pat-cb#problems-and-considerations |
| AZRL-02 | A | Timeouts fit the calling context: an outbound timeout on a request path is shorter than the service's own inbound request timeout, so threads and connections don't pile up during outages. | inbound timeout stated in the files | bp-tf#determine-an-appropriate-retry-count-and-interval, pat-cb#problems-and-considerations, pat-retry#impact-on-performance |
| AZRL-03 | A | When calls are retried, the whole operation is bounded: an overall timeout or deadline covers all attempts and delays, and the per-attempt timeout is shorter than it. | retries on request paths | bp-tf#determine-an-appropriate-retry-count-and-interval |
| AZRL-04 | A | Steps of long-running or multi-step operations that can block, and locks or leases taken for work, have a timeout or expiry, so a stuck step or a crashed holder doesn't block the flow indefinitely. | multi-step workflows, distributed locks | pat-ct#problems-and-considerations, pat-rl#solution |

## REL-02 — Transient faults are retried safely (Retry, Retry Storm)

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZRL-05 | A | Remote calls in request/handler paths have a retry for transient faults. The client SDK's built-in retry, or a resilience library, is used instead of hand-written loops unless a stated reason exists. | missing-retry rule (SKILL.md step 4) | bp-tf#check-whether-a-built-in-retry-mechanism-exists, ap-rs#solution, pat-retry#solution |
| AZRL-06 | A | Retries are finite: a bounded attempt count and/or total duration. No `while(true)` or retry-forever loops. | retry logic present | ap-rs#solution, ap-rs#context-and-problem, bp-tf#avoid-antipatterns |
| AZRL-07 | A | Background/batch retries use growing delays (exponential or incremental back-off) with jitter; interactive paths may use a few regular-interval retries. At most one immediate retry. No fixed short interval with many attempts. | retry logic present | bp-tf#determine-an-appropriate-retry-count-and-interval, bp-tf#avoid-antipatterns, ap-rs#solution |
| AZRL-08 | A | Only transient failures are retried (timeouts, connection errors, 408/429/5xx). Most 4xx, validation and business errors aren't, and retry logic stops on non-transient errors. | retry logic present | bp-tf#check-whether-retrying-suits-the-operation, ap-rs#considerations, pat-retry#exception-type, pat-retry#when-to-use-this-pattern |
| AZRL-09 | A | A server-provided delay (`Retry-After` or equivalent) is honored and takes precedence over the client's own back-off. | HTTP/SDK calls that can be throttled | bp-tf#determine-an-appropriate-retry-count-and-interval, ap-rs#solution, pat-rl#problems-and-considerations |
| AZRL-10 | A | Retries happen at one layer only. Nested layers (SDK retry + resilience handler + outer loop) are avoided, or inner layers are set to fail fast. | ≥ 2 retry mechanisms on one call chain | bp-tf#avoid-antipatterns, pat-retry#general-guidance |
| AZRL-11 | A | High-volume services that retry against a shared dependency also cap aggregate retries (a retry budget or retry-rate limit), not only per-request attempts. | high-concurrency service + shared dependency | bp-tf#avoid-antipatterns |
| AZRL-12 | A | User-facing paths use few, short retries and then fail fast with a clear message. Long or many retries are kept for background and batch work. | retries on interactive paths | bp-tf#determine-an-appropriate-retry-count-and-interval, pat-retry#impact-on-performance |
| AZRL-13 | A | Retry settings (count, intervals, which errors) are defined centrally from configuration with sensible defaults, not hard-coded differently at many call sites. | retry logic at ≥ 3 call sites | bp-tf#manage-retry-policy-configurations |
| AZRL-14 | A | When retries are exhausted, the failure is surfaced and handled (exception, fallback, error to caller), and for queued or deferred work the input isn't lost (dead-lettered or stored for later). | retry logic present | bp-tf#determine-an-appropriate-retry-count-and-interval, pat-retry#solution, bp-tf#manage-operations-that-continually-fail |

## REL-03 — Retries don't repeat non-idempotent side effects

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZRL-15 | A | Non-idempotent operations (creating resources, payments, increments, sending messages or e-mail) are retried automatically only when protected by an idempotency or deduplication key. Otherwise retry is off for them. | retries cover non-idempotent calls | pat-retry#idempotency, bp-tf#other-considerations |
| AZRL-16 | A | Operations are made naturally idempotent where possible: upserts keyed on a business ID, absolute values instead of increments, PUT to a resource ID. | write operations that are retried or redelivered | pat-ic#problems-and-considerations |
| AZRL-17 | A | An idempotency key identifies the logical operation: created once before the first attempt (not per attempt or from timestamps), and passed on to downstream calls. | idempotency keys used | pat-ic#choose-a-stable-deduplication-key, pat-ic#problems-and-considerations |
| AZRL-18 | A | The retry scope doesn't re-run steps that already succeeded with side effects. Either the scope is narrowed to the failing step, or every step in it is idempotent. | one retry wraps several operations | bp-tf#other-considerations |
| AZRL-19 | A | Multi-step operations across services or stores that can't share a transaction compensate completed steps when a later step fails. Compensation steps are idempotent, and irreversible steps run last. | distributed multi-step workflows | pat-ct#problems-and-considerations, pat-ct#solution, bp-bg#coordination |
| AZRL-20 | A | Operations inside a transaction are retried as a whole transaction unit (for example, an execution strategy around the transaction), not one statement mid-transaction. | retries + explicit transactions | pat-retry#transaction-consistency |

## REL-04 — Circuit breakers protect against persistently failing dependencies

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZRL-21 | A | Synchronous calls to remote dependencies that can fail for long periods go through a circuit breaker (library, resilience pipeline, mesh or gateway policy), so repeated failures fail fast instead of tying up threads. | circuit-breaker rule (SKILL.md step 5) | pat-cb#solution, pat-cb#when-to-use-this-pattern, bp-tf#manage-operations-that-continually-fail, ap-rs#solution |
| AZRL-22 | A | Retry and circuit breaker are composed so retries stop when the circuit is open; the open-circuit exception isn't treated as transient. | both retry and breaker present | pat-cb#solution |
| AZRL-23 | A | Breakers trip on failures within a time window (count or ratio), stay open for a set break duration, and allow limited trial calls (half-open) before closing. | breaker present | pat-cb#solution, pat-cb#problems-and-considerations |
| AZRL-24 | A | Callers handle the open-circuit outcome with a fallback, a degraded response or a clear error, not an unhandled exception. | breaker present | pat-cb#problems-and-considerations |
| AZRL-25 | A | Breakers are scoped per independent resource (per downstream service, endpoint, shard or region), not one breaker shared by independent providers. | breaker over several independent resources | pat-cb#problems-and-considerations |
| AZRL-26 | A | A breaker's state is shared by all calls to its dependency (one long-lived, thread-safe instance), not a new breaker per request, which would never trip. | breaker present | pat-cb#problems-and-considerations |

## REL-05 — More than one instance (no single point of failure)

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZRL-27 | W | Each compute component that serves production traffic runs ≥ 2 instances (replicas, instance count, autoscale minimum), or runs on a platform that manages instance redundancy (serverless, managed PaaS). | deployment-config rule (SKILL.md step 7) | re-red#build-redundancy-into-your-workload-with-multiple-component-instances, re-red#prefer-serverless-and-fully-managed-services-to-reduce-operational-burden, re-sp#design-for-redundancy |
| AZRL-28 | A | A component that is deliberately a singleton (scheduler, leader, single consumer) restarts automatically, and where it serves a critical flow it uses leader election or a standby. | singleton component in config or code | bp-bg#conflicts, re-red#build-redundancy-into-your-workload-with-multiple-component-instances, re-prin#design-for-resilience |
| AZRL-29 | W | Compute instances hold no data that must survive them: no business data whose only copy is on local disk, ephemeral volumes or in memory. (Session state for scale-out is judged by review-twelve-factor TF-06.) | deployment-config rule | re-red#build-redundancy-into-your-workload-with-multiple-component-instances |

## REL-06 — Fault isolation, graceful degradation and load protection

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZRL-30 | A | Calls to different dependencies use separate resource pools or concurrency limits (a bulkhead per dependency), so one slow dependency can't use up shared threads or connections. | ≥ 2 remote dependencies on shared request threads | pat-bh#solution, pat-bh#problems-and-considerations, pat-bh#when-to-use-this-pattern |
| AZRL-31 | W | When a non-critical dependency fails, the flow continues with reduced functionality (fallback, cached data, feature off, read-only mode) and tells the user, instead of failing the whole request. | optional dependency calls in request paths | re-sp#implement-a-graceful-degradation-mode, re-fma#plan-mitigation-strategies, re-prin#design-for-resilience, pat-cb#problems-and-considerations |
| AZRL-32 | A | A service limits or sheds excess load before it saturates (concurrency or rate limiter, gateway rate-limit policy, bounded queues), and rejects early in the pipeline, before expensive work. | service exposes request endpoints | pat-thr#solution, pat-thr#problems-and-considerations, ap-rs#solution |
| AZRL-33 | A | Overload from downstream is passed upstream, not masked: a downstream 429/503 isn't retried silently without limit or turned into a generic 500, so callers can back off. | service calls dependencies that can throttle | pat-thr#problems-and-considerations, ap-rs#solution |
| AZRL-34 | A | Bulk or batch work against a dependency with known throughput limits paces its calls (rate limiter, or a durable queue drained at a controlled rate), and all workstreams to that dependency share the limit. | bulk/batch calls to a throttled dependency | pat-rl#solution, pat-rl#problems-and-considerations, pat-thr#solution |
| AZRL-35 | A | Load limits are configuration that can change without a code change, and with several instances they account for instance count (a shared counter, or the limit divided across replicas). | rate or concurrency limits present | pat-thr#problems-and-considerations |

## REL-07 — Reliable message and background-job processing

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZRL-36 | A | Message and job consumers are idempotent: they deduplicate on a stable producer or business key (not the broker's delivery ID, a correlation ID or a timestamp), or their operations are naturally idempotent. Broker duplicate detection alone isn't enough. | messaging rule (SKILL.md step 6) | pat-ic#solution, pat-ic#choose-a-stable-deduplication-key, pat-ic#problems-and-considerations, bp-bg#design-for-idempotency, pat-qbll#problems-and-considerations |
| AZRL-37 | A | The "processed" marker and the side effects are committed atomically (same transaction, inbox), and concurrent duplicates are stopped by a unique constraint or an atomic set-if-absent, not a separate check-then-set. | consumer keeps a dedup store | pat-ic#commit-the-processed-key-and-the-side-effects-atomically, pat-ic#guard-against-concurrent-duplicates |
| AZRL-38 | A | Side effects that can't join the transaction use an in-progress/completed record. Dedup records are kept longer than the broker's redelivery window. | external calls from consumers | pat-ic#handle-side-effects-that-cant-join-the-transaction, pat-ic#problems-and-considerations |
| AZRL-39 | A | A maximum delivery count and a dead-letter queue (or equivalent) are configured, so poison messages are neither requeued forever nor dropped silently. | messaging rule | pat-cc#problems-and-considerations, pat-qbll#problems-and-considerations, bp-bg#reliability-considerations, re-sp#application-design-guidance |
| AZRL-40 | A | Permanent failures (malformed payload, failed validation, missing referenced data) go to the dead-letter queue at once instead of using up retries. | messaging rule | bp-bg#reliability-considerations |
| AZRL-41 | A | A message is acknowledged or completed only after it has been processed (peek-lock, manual ack, offset commit after processing), not when it is received. | messaging rule | bp-bg#reliability-considerations, pat-cc#solution |
| AZRL-42 | A | Consumers either tolerate out-of-order delivery or enforce order (sessions or partition keys, sequence or version checks that reject stale messages). | order-dependent updates | bp-bg#reliability-considerations, pat-cc#problems-and-considerations, pat-ic#problems-and-considerations, pat-qbll#problems-and-considerations |
| AZRL-43 | W | Long-running or multi-step jobs save checkpoints to durable storage and resume from the last one after a restart, instead of starting over or losing work. | long-running jobs | re-sp#application-design-guidance, bp-bg#reliability-considerations, re-scale#adapt-scaling-strategies-to-fit-individual-components-or-flows |
| AZRL-44 | A | Workers shut down gracefully on a termination signal: stop taking new work, finish or checkpoint the current item, exit. The platform grace period is long enough for a typical item. | background workers, consumers | bp-bg#reliability-considerations, re-scale#adapt-scaling-strategies-to-fit-individual-components-or-flows |
| AZRL-45 | A | A scheduled job that can run longer than its interval, or run on several instances, is protected against overlap (a lock with lease expiry, single-instance execution, or idempotent processing). | scheduled jobs | bp-bg#design-for-idempotency, bp-bg#conflicts |
| AZRL-46 | A | Work that must not be lost goes through a durable broker or store, not an in-memory queue or buffer that a crash or restart would empty. | producers of deferred work | pat-qbll#problems-and-considerations, pat-cc#problems-and-considerations, pat-rl#solution |
| AZRL-47 | A | Consumers limit their concurrency (max concurrent calls, prefetch, max replicas), so scaling out doesn't move overload to a shared downstream dependency. | autoscaled or competing consumers | pat-qbll#problems-and-considerations, re-scale#adapt-scaling-strategies-to-fit-individual-components-or-flows |

## REL-08 — In-region high-availability configuration

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZRL-48 | W | Instances are spread across independent failure domains: availability zones where the platform offers them, otherwise separate nodes or hosts (topology spread, anti-affinity). | deployment-config rule + ≥ 2 instances | re-red#distribute-workloads-across-proximate-independent-infrastructure, re-sp#infrastructure-design-guidance-and-patterns |
| AZRL-49 | W | Traffic to multiple instances goes through a load balancer or ingress whose health probes (readiness) take unhealthy instances out of rotation. | deployment-config rule + ≥ 2 instances | re-red#build-redundancy-into-your-workload-with-multiple-component-instances, re-red#azure-facilitation, re-sp#design-for-self-healing |
| AZRL-50 | W | The platform restarts or replaces failed instances automatically (liveness probe, auto-heal, restart policy). | deployment-config rule | re-sp#infrastructure-design-guidance, re-prin#design-for-recovery |
| AZRL-51 | W | Stateful dependencies on the critical path (database, cache, broker) use an in-region highly available tier with automatic failover, and the app connects through the failover-aware endpoint. | stateful services in IaC | re-red#build-redundancy-into-your-workload-with-multiple-component-instances, re-sp#infrastructure-design-guidance |
| AZRL-52 | W | Components with variable load have scaling automated in IaC (not manual). Components that scale slowly scale ahead of expected load or are protected by throttling. | deployment-config rule | re-scale#automate-scaling, re-scale#optimize-the-scale-unit-initialization-time, re-sp#infrastructure-design-guidance-and-patterns |
