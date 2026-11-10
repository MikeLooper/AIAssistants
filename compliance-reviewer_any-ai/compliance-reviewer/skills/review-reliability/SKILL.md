---
name: review-reliability
description: 'Reviews timeouts, transient-fault retries (including retry storms), idempotency of retried operations, circuit breakers, instance redundancy, fault isolation and load protection, reliable message and background-job processing, and in-region high-availability configuration, against Azure Well-Architected Reliability and Azure Architecture Center resiliency patterns. Use when the compliance-reviewer orchestrator delegates the Operations / Reliability subject.'
user-invocable: false
---

# Review: Reliability

Assesses resilience that is visible in code and configuration: timeouts, retries, idempotency, circuit breakers,
bulkheads, degradation and load protection, message and background-job reliability, and in-region redundancy. It uses
a local, pinned summary of Azure Well-Architected Reliability and Azure Architecture Center guidance. Cross-region
recovery, runtime fault injection and load testing are out of scope.

## Inputs

HTTP, gRPC, DB, cache and broker client setup; DI/startup registration of resilience pipelines; retry, timeout,
circuit-breaker and rate-limit code and config; message consumers, queue triggers, scheduled jobs and background
workers; service-mesh, gateway and broker config; and hosting/IaC/Kubernetes config for instances, zones, probes and
autoscaling, per `compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/azure-reliability-resiliency.md` — AZRL-01…AZRL-52. Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, `references/reliability-config-signals.md`, the
   standards file and, for each language id in `01-inventory.json`, `references/languages/<id>.md` if it exists.
2. Remote calls: REL-01…REL-04 apply to calls that leave the process (HTTP/gRPC, DB, cache, broker, SDK). If a
   sidecar or mesh in the files applies its own timeout/retry/breaker to a call, judge that policy instead.
3. Timeouts: AZRL-01 fails only when no timeout applies (disabled, or a library default of "none" per the language
   file). A finite default passes; note `relies on library default <n>`. Judge AZRL-02 only when the service's own
   inbound timeout is in the files ("no inbound timeout in scope" otherwise).
4. Retries: if remote calls in request or handler paths have no retry and the SDK doesn't retry by default, fail
   AZRL-05 (confidence `medium`). Judge AZRL-06…AZRL-14 only where retry logic exists.
5. Circuit breakers: apply REL-04 to synchronous remote calls in request paths. Skip message-driven flows with
   dead-lettering, dependencies with a mesh/gateway breaker in the files, and local resources, with that reason.
6. Messaging: judge REL-07 only when message consumers, queue/event triggers, scheduled jobs or background workers
   are in the files; otherwise N/A ("no message consumers or background jobs in scope").
7. Deployment config: judge REL-05 and REL-08 only when hosting, IaC or Kubernetes config for a deployable service
   is in the files; otherwise N/A ("no deployment config in scope" or "not a deployable service").
8. Boundaries: API rate limiting and `429` for request endpoints, including per-client or per-API-key limits and
   download limits, are judged here under AZRL-32 (the four security skills send rate limits here); login
   throttling stays with review-security-identity-access SEC-IA-09. Don't fail for client reuse, pool sizing, total
   concurrency bounds, offloading, autoscale metrics/thresholds or resource limits (review-performance);
   statelessness, session state and sticky sessions (review-twelve-factor TF-06); the 429/503/Retry-After response
   shape or error contract of the repo's own APIs (review-api-design); health-endpoint implementation or
   retry/breaker telemetry (review-observability); alerts (review-monitoring); cross-region redundancy, backups or
   delete protection (review-disaster-recovery); over-provisioning or autoscale maximums
   (review-cost-sustainability); resilience tests (review-testing TST-13); staged rollouts and rollback paths
   (review-software-lifecycle SDP-01). Edge DDoS and WAF rules aren't judged by
   any subject (known coverage gap, README).
9. For each check (REL-01…REL-08), evaluate only the elements it lists whose "Applies when" condition holds. If
   none apply, mark the check N/A with that reason.
10. Evidence rule: fail only on concrete evidence in the files (see the lookup files' fail signals, e.g.
    `requests.get(url)` with no `timeout=`, `while (true)` around an HTTP call, `WaitAndRetryForever`, a breaker
    created inside the request method, Kafka `enable.auto.commit=true` with side effects, `replicas: 1`). Use
    confidence `medium` unless the evidence is unambiguous.
11. Severity: every Finding takes the check's default severity from `checklist.md`;
    `checkResults.severityIfFailed` is always that default.
12. Citations: `standard` = "<source name> — <element ID>", where the source name is that of the element's
    primary page in the standards file (Src column: W = Azure Well-Architected Framework, A = Azure Architecture
    Center); `url` = citation base + page path + "#" + primary anchor. Never cite the language or config-signals
    files. `urlsFetched` stays empty.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
