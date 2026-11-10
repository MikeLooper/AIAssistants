---
name: review-performance
description: 'Reviews caching, non-blocking I/O, client and connection reuse, N+1 and chatty data access, data retrieval efficiency, offloading of long-running work, hot-path code and scale-out readiness, against Azure Well-Architected Performance Efficiency and Azure Architecture Center performance antipattern and caching guidance. Use when the compliance-reviewer orchestrator delegates the Performance subject.'
user-invocable: false
---

# Review: Performance

Assesses performance risks that are visible in code and configuration: caching, blocking I/O, client and connection
reuse, N+1 and chatty data access, extraneous fetching, offloading of heavy work, hot-path efficiency and scale-out
readiness. It uses a local, pinned summary of Azure Well-Architected Performance Efficiency and Azure Architecture
Center guidance. Runtime measurement, load testing and profiling are out of scope.

## Inputs

Data-access code (repositories, ORM queries, SQL, schema migrations), request handlers, client and DI/startup
registration, caching code and config, background-job code, web-server config, and hosting/scaling config, per
`compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/azure-performance-efficiency.md` — AZPE-01…AZPE-53. Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, `references/performance-config-signals.md`, the
   standards file and, for each language id in `01-inventory.json`, `references/languages/<id>.md` if it exists.
2. Concurrency model: classify each request-handling stack as async-first or thread-per-request using the language
   files. On thread-per-request stacks skip AZPE-13 and AZPE-15 ("thread-per-request stack; synchronous I/O is the
   model"). AZPE-14 and AZPE-18 apply to both. On async-first stacks, a blocking I/O call in a request path fails
   AZPE-13 with confidence `high` when the async alternative is used elsewhere in the codebase, otherwise `medium`.
3. Hot paths: count loop, query and allocation patterns (PERF-04, PERF-05) only in request, message, batch or
   scheduled-job paths that iterate over data that isn't evidently small and fixed (a result set, a collection from
   input, a page of records). Exclude startup code, scripts, migrations, tests and loops over constants. Use
   confidence `medium` unless the data is evidently unbounded (e.g. `findAll()`, `objects.all()`).
4. Multi-instance: apply AZPE-07 only when the files show more than one instance can run (replicas,
   autoscale, instance count, Kubernetes Deployment/HPA, serverless; see `performance-config-signals.md`).
   Otherwise skip ("no multi-instance evidence in scope").
5. Config in scope: judge AZPE-49…AZPE-51 only when hosting, ingress, autoscale or server config is in the files;
   otherwise skip ("no hosting/scaling config in scope"), which is never a failure. If PERF-08 then has no applicable
   element, mark it N/A.
6. Boundaries: don't fail for retries, backoff, timeouts or general circuit breakers (review-reliability; AZPE-06
   judges only cache fallback); API caching headers, pagination contract, long-running-operation shape or rate-limit
   responses (review-api-design; skip AZPE-11 for HTTP APIs with reason "API caching headers judged by
   review-api-design"); instrumentation, cache hit/miss metrics or telemetry volume (review-observability);
   performance alerts (review-monitoring); autoscale maximum bounds, over-provisioning or data archive/purge
   (review-cost-sustainability); cache authentication, TLS or access control (security skills; AZPE-12 judges only
   key scoping and sensitive data in shared caches); statelessness, session state and sticky sessions
   (review-twelve-factor TF-06); load and performance tests (review-testing TST-12). Never recommend caching
   authenticated, per-user or sensitive responses (`no-store`: review-security-web-api SEC-WA-08).
7. For each check (PERF-01…PERF-08), evaluate only the elements it lists whose "Applies when" condition holds. If
   none apply, mark the check N/A with that reason.
8. Evidence rule: fail only on concrete evidence in the files (see the language files' fail signals, e.g.
   `new HttpClient()` inside an action method, `.Result` on an EF Core call in a controller, `requests.get` inside
   `async def`, a loop that calls `repository.GetById`, `ToList()` before `Where`, `IMemoryCache.Set` with no
   expiration, `clientAffinityEnabled: true`). Use confidence `medium` unless the evidence is unambiguous.
9. Severity: every Finding takes the check's default severity from `checklist.md`;
   `checkResults.severityIfFailed` is always that default.
10. Citations: `standard` = "<source name> — <element ID>", where the source name is that of the element's
    primary page in the standards file (Src column: W = Azure Well-Architected Framework, A = Azure Architecture
    Center); `url` = citation base + page path + "#" + primary anchor. Never cite the language or config-signals
    files. `urlsFetched` stays empty.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
