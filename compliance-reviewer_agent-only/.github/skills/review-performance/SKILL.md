---
name: review-performance
description: 'Reviews caching, async I/O usage and resource efficiency. Use when the compliance-reviewer orchestrator delegates the Operations / Performance subject.'
user-invocable: false
---

# Review: Performance

Assesses caching strategy, use of async I/O, and general resource efficiency.

## Inputs

Caching code/config, async I/O usage, connection pool config, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check caching is used for expensive/repeated reads (in-memory or distributed cache) with a sane invalidation/expiry strategy.
3. Check I/O-bound operations (HTTP, DB, file) use async/non-blocking APIs where the language/framework supports it, especially in request-handling paths.
4. Check connection pooling is used for DB/HTTP clients rather than creating a new connection per call.
5. Flag obvious N+1 query patterns or repeated work inside loops that could be hoisted or batched.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
