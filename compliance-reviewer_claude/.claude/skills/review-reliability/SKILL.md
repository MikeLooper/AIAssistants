---
name: review-reliability
description: 'Reviews retries, timeouts, circuit breakers and redundancy. Use when the compliance-reviewer orchestrator delegates the Operations / Reliability subject.'
user-invocable: false
---

# Review: Reliability

Assesses resilience patterns: retries, timeouts, circuit breakers and redundancy.

## Inputs

HTTP client config, retry/circuit-breaker code, health check registration, IaC redundancy settings, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check outbound calls (HTTP, DB, queue) have explicit timeouts — no indefinite waits.
3. Check transient failures are retried with backoff (not naive infinite/no-backoff loops), and non-idempotent operations aren't retried unsafely.
4. Check a circuit breaker (or equivalent) protects against cascading failures to a degraded dependency.
5. Check redundancy: more than one instance/replica configured where the target is a deployable service, per IaC.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
