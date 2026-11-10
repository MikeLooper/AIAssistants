# Azure performance efficiency guidance — localized summary

- Source site: learn.microsoft.com (azure/well-architected and azure/architecture)
- Pinned pages: see the page table below (path, `ms.date`, "Last updated" and git commit at retrieval)
- Citation base: https://learn.microsoft.com/azure/
- Localized: 2026-11-08 · Elements: 53 (cap 100), of which 2 retired (AZPE-47, AZPE-48; 2026-11-09)
- Source name for `Finding.standard`: the Source name of the element's primary page (first anchor). The **Src** column gives it: **W** = `Azure Well-Architected Framework`, **A** = `Azure Architecture Center`.
- Level: every element is `REVIEW` (the pages use no normative keywords); severity is the owning check's default.
- Every element is Scope G (generic). No element depends on Azure services. Azure product names in the sources (Azure Managed Redis, Service Bus) are generalized to "distributed cache", "message queue".
- Anchor(s): `<page key>#<section anchor>`, primary first. Bullet-level guidance has no anchor of its own and cites its section anchor.
- Citation URL: citation base + page path + `#` + primary anchor, with no locale segment. Example: `https://learn.microsoft.com/azure/architecture/antipatterns/improper-instantiation/#how-to-fix-improper-instantiation-antipattern`.

| Key | Page path | Source name | ms.date | Last updated | Git commit |
|-----|-----------|-------------|---------|--------------|------------|
| pe-check | well-architected/performance-efficiency/checklist | Azure Well-Architected Framework | 2026-04-20 | 2026-05-06 | ce3921ce25f1 |
| pe-svc | well-architected/performance-efficiency/select-services | Azure Well-Architected Framework | 2023-11-15 | 2023-11-15 | 0007a4d4697c |
| pe-scale | well-architected/performance-efficiency/scale-partition | Azure Well-Architected Framework | 2023-11-15 | 2023-11-15 | 28a78d225235 |
| pe-code | well-architected/performance-efficiency/optimize-code-infrastructure | Azure Well-Architected Framework | 2023-11-15 | 2023-11-15 | 28a78d225235 |
| pe-data | well-architected/performance-efficiency/optimize-data-performance | Azure Well-Architected Framework | 2026-05-13 | 2026-05-13 | 3ff81f3a01b0 |
| pe-crit | well-architected/performance-efficiency/prioritize-critical-flows | Azure Well-Architected Framework | 2023-11-15 | 2023-11-30 | 28a78d225235 |
| pe-ops | well-architected/performance-efficiency/optimize-operational-tasks | Azure Well-Architected Framework | 2023-11-15 | 2023-11-15 | ee7c014e94f1 |
| ap | architecture/antipatterns/ | Azure Architecture Center | 2023-12-13 | 2026-02-03 | d8f79749034a |
| ap-bdb | architecture/antipatterns/busy-database/ | Azure Architecture Center | 2017-06-05 | 2026-05-07 | 52bf91783e87 |
| ap-bfe | architecture/antipatterns/busy-front-end/ | Azure Architecture Center | 2017-06-05 | 2026-10-13 | dcf29659535a |
| ap-cio | architecture/antipatterns/chatty-io/ | Azure Architecture Center | 2017-06-05 | 2022-12-16 | dcf29659535a |
| ap-ef | architecture/antipatterns/extraneous-fetching/ | Azure Architecture Center | 2022-07-25 | 2025-12-09 | dcf29659535a |
| ap-ii | architecture/antipatterns/improper-instantiation/ | Azure Architecture Center | 2017-06-05 | 2026-08-18 | d16b276a2d92 |
| ap-mp | architecture/antipatterns/monolithic-persistence/ | Azure Architecture Center | 2017-06-05 | 2025-04-25 | ac27d8de066b |
| ap-nc | architecture/antipatterns/no-caching/ | Azure Architecture Center | 2017-06-05 | 2026-03-04 | dcf29659535a |
| ap-nn | architecture/antipatterns/noisy-neighbor/noisy-neighbor | Azure Architecture Center | 2025-06-11 | — (no footer) | 853fa39cce09 |
| ap-sio | architecture/antipatterns/synchronous-io/ | Azure Architecture Center | 2017-06-05 | 2026-05-06 | a5a1441ee207 |
| bp-cache | architecture/best-practices/caching | Azure Architecture Center | 2026-03-25 | 2026-06-12 | 5ebacc7a6045 |
| pat-ca | architecture/patterns/cache-aside | Azure Architecture Center | 2025-09-11 | — (no footer) | cb69919fc6c9 |

`pe-check` (PE:01–PE:12) and `ap` (antipattern catalog) are traceability and drift only; no element cites them.

## PERF-01 — Caching of expensive or repeated reads

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZPE-01 | A | Data that's read often and changes rarely, or is expensive to fetch (reference data, repeated query results, remote lookups), is cached instead of fetched from the source on every request. | repeated reads of the same data in request paths | ap-nc#how-to-fix-the-no-caching-antipattern, bp-cache#decide-when-to-cache-data, pe-data#use-caching, pe-data#optimize-database-queries |
| AZPE-02 | A | Cached entries expire. An absolute or sliding TTL is set per cache or per entry and matches the data's volatility and the staleness callers can accept. Data that must be current bypasses the cache. | cache present | bp-cache#manage-data-expiration-in-a-cache, bp-cache#caching-and-eventual-consistency, pat-ca#problems-and-considerations, ap-nc#considerations-for-caching-strategy |
| AZPE-03 | A | Caches are bounded. In-process caches have a size limit or eviction policy. Caches without built-in expiry are swept so they can't grow without limit. | in-process cache | bp-cache#manage-data-expiration-in-a-cache, ap-nc#considerations-for-caching-strategy, pat-ca#problems-and-considerations |
| AZPE-04 | A | Writes keep the cache consistent: the source is updated and the entry invalidated (cache-aside), or both are updated in one write (write-through) where read-after-write freshness is needed. | app writes data it also caches | bp-cache#keep-the-cache-consistent-on-writes, pat-ca#solution, ap-nc#how-to-fix-the-no-caching-antipattern |
| AZPE-05 | A | The cache is not the system of record: important changes are persisted to the data store, not held only in the cache. | app writes to the cache | bp-cache#decide-when-to-cache-data, bp-cache#implement-high-availability-and-scalability-and-improve-performance |
| AZPE-06 | A | If the cache is unavailable, the request doesn't fail: the app falls back to the source and protects it from a sudden surge. General circuit breakers belong to reliability. | shared/distributed cache | ap-nc#considerations-for-caching-strategy, bp-cache#implement-high-availability-and-scalability-and-improve-performance |
| AZPE-07 | A | With several instances, mutable shared data isn't kept only in per-instance memory caches: a shared cache is used, or private caches use short expiry (or a local + shared two-level cache). | multi-instance rule + in-process cache of mutable data | bp-cache#private-caching, bp-cache#shared-caching, pat-ca#problems-and-considerations |
| AZPE-08 | A | Concurrent updates to shared cached values use atomic operations or optimistic concurrency, not a separate read-then-write. | shared cache updated by several instances | bp-cache#manage-concurrency-in-a-cache, bp-cache#perform-atomic-and-batch-operations |
| AZPE-09 | A | Reads and writes of several cache keys are batched (multi-get/multi-set, pipelining), not one round trip per key in a loop. | several keys per operation | bp-cache#perform-atomic-and-batch-operations, bp-cache#implement-high-availability-and-scalability-and-improve-performance |
| AZPE-10 | A | Static reference data that fits in the cache is primed at startup; very large seeding that would overload the source at startup is avoided. | reference data cached | bp-cache#determine-how-to-cache-data-effectively, pat-ca#problems-and-considerations, ap-nc#considerations-for-caching-strategy |
| AZPE-11 | A | Cacheable web pages and static assets send caching headers (Cache-Control/ETag), and static asset URIs are versioned so clients pick up changes. HTTP APIs: skipped (review-api-design). Never recommend caching authenticated, per-user or sensitive responses (`no-store`: review-security-web-api SEC-WA-08). | web app serving pages or static assets | ap-nc#considerations-for-caching-strategy, bp-cache#invalidate-data-in-a-client-side-cache |
| AZPE-12 | A | User- or tenant-specific data in a shared cache uses keys that include the user/tenant scope. Sensitive data is read from the primary source, not cached in a shared cache. | shared cache holding per-user data | pat-ca#when-to-use-this-pattern, pat-ca#problems-and-considerations, bp-cache#protect-cached-data |

## PERF-02 — Non-blocking I/O in request paths

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZPE-13 | A | On async-first stacks, I/O in request paths (DB, HTTP, queue, storage, file) uses the library's async API where one exists. Short, low-contention local I/O (e.g. small files read at startup) is exempt. | async-first stack | ap-sio#how-to-fix-the-problem, ap-sio#considerations, pe-code#use-concurrency-and-parallelism |
| AZPE-14 | A | Async operations aren't blocked on synchronously in request or handler code (waiting on a task, future or promise result); one blocking call blocks the whole call chain. | any stack using async APIs | ap-sio#problem-description, ap-sio#how-to-fix-the-problem |
| AZPE-15 | A | Synchronous I/O isn't wrapped in a thread-offload "async" wrapper as a fix in server code; a native async API is used, because wrappers add threads and overhead. | async-first stack | ap-sio#how-to-fix-the-problem |
| AZPE-16 | A | Service interfaces and client libraries that the repo exposes offer async versions of I/O-bound operations, so callers can stay non-blocking. | repo exposes an I/O-bound service or client library | ap-sio#how-to-fix-the-problem |
| AZPE-17 | W | Independent I/O calls in one operation run concurrently (e.g. awaited together) rather than one after another, when order doesn't matter. | ≥ 2 independent remote calls in one handler | pe-code#use-concurrency-and-parallelism |
| AZPE-18 | A | Concurrency against shared resources is bounded (semaphore, bounded executor or parallelism, pool size), so unblocked work doesn't starve or throttle downstream resources. | parallel or concurrent fan-out | ap-sio#considerations, pe-code#use-concurrency-and-parallelism |

## PERF-03 — Client, connection and expensive-object reuse

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZPE-19 | A | Shareable, thread-safe broker clients (HTTP, messaging, database/document SDK, cache connection) are created once and reused for the app's lifetime (singleton, DI or factory), not per request or call. | such clients used | ap-ii#problem-description, ap-ii#how-to-fix-improper-instantiation-antipattern, bp-cache#connect-and-configure-client-applications |
| AZPE-20 | A | Long-lived HTTP clients also handle connection lifetime and DNS changes, through a client factory or a pooled-connection lifetime setting. | long-lived HTTP client | ap-ii#how-to-fix-improper-instantiation-antipattern |
| AZPE-21 | A | Per-request settings (e.g. default headers) aren't changed on shared client instances; they're set once at startup or put on the individual request. | shared clients | ap-ii#considerations |
| AZPE-22 | W | Database connections come from a pool and are released promptly after each unit of work; scarce connections aren't held open across requests or idle periods. | DB access | pe-code#use-connection-pooling, ap-ii#considerations |
| AZPE-23 | W | Pool sizes are set explicitly for the concurrency each instance must support and stay within the service's connection limits. Defaults that run out under load are avoided, and pooling isn't disabled. | pool config present, or high-concurrency service | pe-code#use-connection-pooling |
| AZPE-24 | A | Objects that are expensive to create are reused (pooling, or lazy creation of one shared instance) instead of being created and destroyed repeatedly. | expensive objects in hot paths | ap-ii#problem-description, ap-ii#considerations, pe-code#optimize-memory-management |

## PERF-04 — N+1 and chatty I/O

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZPE-25 | W | Related data is loaded with joins, eager loading or batch fetching, not one query per item while iterating a result set (including lazy-loaded navigation used in loops or during serialization). | ORM or data-access code | pe-data#optimize-database-queries, ap-cio#reading-and-writing-individual-records-to-a-database-as-distinct-requests, ap-cio#how-to-fix-the-problem |
| AZPE-26 | A | Multiple records are written with batch or bulk operations, or committed in one unit of work, not one round trip per record in a loop. | writes in loops | ap-cio#reading-and-writing-individual-records-to-a-database-as-distinct-requests, pe-data#optimize-data-movement-and-processing |
| AZPE-27 | A | One logical operation isn't split into many small remote calls (one per property or item); coarse-grained or batch endpoints are used or offered. | remote API calls | ap-cio#implementing-a-single-logical-operation-as-a-series-of-http-requests, ap-cio#how-to-fix-the-problem, pe-code#optimize-code-logic |
| AZPE-28 | A | File and stream writes are buffered into larger operations, not repeated open/write/close cycles for small pieces. | file I/O in loops | ap-cio#reading-and-writing-to-a-file-on-disk, ap-cio#how-to-fix-the-problem |
| AZPE-29 | A | Combined requests stay bounded: a batch fetches only what the caller is likely to use, and write batches are size-limited. | batching present | ap-cio#considerations |

## PERF-05 — Efficient hot-path code

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZPE-30 | W | Calls, lookups and computations that don't change inside a loop are moved out of it; redundant calculations and repeated validations on the same path are removed. | hot-path rule | pe-code#optimize-code-logic |
| AZPE-31 | W | Data structures fit the access pattern (e.g. a hash lookup instead of repeated linear searches inside a loop). | lookups in loops | pe-code#optimize-code-logic |
| AZPE-32 | W | Allocations in hot paths are kept low: no repeated string concatenation in loops, buffers reused, large objects pooled, objects created lazily. | hot-path rule | pe-code#optimize-memory-management, pe-code#optimize-code-logic |
| AZPE-33 | A | Results of expensive, repeatable computations are reused (memoized or cached) instead of recomputed on every call. | repeated pure computation | bp-cache#determine-how-to-cache-data-effectively, ap-nc#considerations-for-caching-strategy |
| AZPE-34 | W | Logging and diagnostics inside hot loops are limited (no per-iteration info-level logging), and debug-only features (e.g. remote debugging) are off in production config. Telemetry volume: OBS-10. | hot loops with logging | pe-code#optimize-code-logic, pe-ops#optimize-monitoring-and-debugging |

## PERF-06 — Efficient data retrieval and data-store use

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZPE-35 | A | Queries select only the columns or fields they need (projection), not whole entities or `SELECT *` trimmed afterwards in code. | data access | ap-ef#how-to-fix-extraneous-fetching-antipattern, ap-ef#considerations, pe-code#optimize-infrastructure-performance |
| AZPE-36 | A | Filtering, sorting and aggregation run in the data store, not after rows are loaded into memory (e.g. a query materialized before its filter, or an expression the ORM can't translate that forces client-side evaluation). | data access | ap-ef#examples-of-extraneous-fetching-antipattern, ap-ef#how-to-fix-extraneous-fetching-antipattern, ap-ef#considerations |
| AZPE-37 | A | Queries that could return unbounded results are paged or capped with a server-side maximum (record count or query time limit). Data layer only; the API pagination contract is api-design's. | list/search/export reads | ap-ef#considerations, ap-nn#actions-that-service-providers-can-take |
| AZPE-38 | A | The database isn't used as an application engine: formatting, string manipulation and complex business logic aren't pushed into stored procedures, triggers or queries. Aggregation stays in the database. | stored procedures or SQL in the repo | ap-bdb#how-to-fix-the-problem, ap-bdb#considerations, ap-bdb#problem-description |
| AZPE-39 | A | Data with different access patterns uses separate stores; logs, telemetry and queue messages aren't written to the business transactional database. | app writes logs or queues to the business DB | ap-mp#solution, ap-mp#problems-and-considerations |
| AZPE-40 | W | Columns used often in WHERE, JOIN and ORDER BY are indexed in the schema or migrations; low-cardinality and redundant indexes are avoided. | schema or migration files in scope | pe-data#optimize-index-performance |
| AZPE-41 | W | Restrictive locking is avoided (no unnecessary lock hints or long pessimistic locks); concurrent updates use optimistic concurrency (version column, rowversion, ETag). | update paths | pe-data#optimize-database-queries, pe-data#optimize-data-updates, pe-scale#design-application-to-scale, ap-cio#considerations |

## PERF-07 — Long-running and resource-intensive work is offloaded

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZPE-42 | A | CPU- or I/O-intensive or long-running work started by a request goes to a queue and a separate worker (queue-based load leveling), and the request returns promptly. The 202/status contract is api-design's. | such work in request handlers | ap-bfe#how-to-fix-the-problem, pe-scale#design-application-to-scale, pe-code#use-concurrency-and-parallelism |
| AZPE-43 | A | Request handlers don't start unmanaged threads or fire-and-forget tasks for heavy work; background work runs in managed hosted services or workers. | web front end | ap-bfe#problem-description, pe-code#optimize-background-jobs |
| AZPE-44 | A | Background workers scale independently of the front end (competing consumers; autoscaling on queue length when IaC is in scope). | queue workers present | ap-bfe#how-to-fix-the-problem, pe-scale#design-application-to-scale |
| AZPE-45 | A | Heavy work that isn't time-sensitive is scheduled off-peak or rate-limited, so it doesn't use capacity that time-sensitive flows need. | batch or scheduled jobs | ap-nn#actions-that-service-providers-can-take, pe-crit#optimize-capacity-allocation |
| AZPE-46 | W | Where flows or tenants have different priorities, critical work is prioritized (priority queues, rate limits on non-critical callers or tenants). | several flows or tenants share a queue or API | pe-crit#optimize-capacity-allocation, ap-bfe#considerations, ap-nn#actions-that-service-providers-can-take |

## PERF-08 — Scale-out readiness and efficient serving

| ID | Src | Requirement (summary) | Applies when | Anchor(s) |
|----|-----|-----------------------|--------------|-----------|
| AZPE-47 | W | (retired 2026-11-09; owned by review-twelve-factor TF-06) App instances are stateless: session and user state lives in an external shared store, not in process memory or on local disk. | — | pe-scale#design-application-to-scale, bp-cache#cache-session-state-and-html-output, pat-ca#when-to-use-this-pattern |
| AZPE-48 | W | (retired 2026-11-09; owned by review-twelve-factor TF-06) Client/session affinity (sticky sessions) is off unless justified in the files. | — | pe-scale#design-application-to-scale |
| AZPE-49 | W | Where autoscaling is configured, it uses meaningful load metrics (CPU/memory plus queue depth or HTTP queue length), keeps minimum headroom (buffer), and leaves a margin between scale-out and scale-in thresholds to prevent flapping. Max bounds: cost. | autoscale config in scope | pe-scale#configure-scaling |
| AZPE-50 | W | Compute has explicit resource requests and limits (container CPU/memory, runtime heap), so one component can't destabilize others. | container or runtime config in scope | pe-code#optimize-infrastructure-performance, pe-crit#isolate-critical-flows |
| AZPE-51 | W | Text responses are compressed, and HTTP/2 is enabled where clients support it. | HTTP server config in scope | pe-code#optimize-infrastructure-performance |
| AZPE-52 | W | Static content is served from a CDN or static hosting with caching, not produced by application compute on every request. | app serves static assets | pe-code#optimize-infrastructure-performance, pe-data#use-caching, pe-svc#evaluate-cache-requirements |
| AZPE-53 | W | The processing path has no single-instance bottleneck (one queue consumer or singleton worker for all load) where the work could be partitioned or fanned out. | processing pipelines | pe-scale#design-infrastructure-to-scale |
