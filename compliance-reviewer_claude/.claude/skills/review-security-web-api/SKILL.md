---
name: review-security-web-api
description: 'Reviews Content Security Policy, HTTP security response headers and REST security practices. Use when the compliance-reviewer orchestrator delegates the Security / Web & API subject.'
user-invocable: false
---

# Review: Security — Web & API

Assesses Content Security Policy, HTTP security response headers, CORS and REST API security practices.

## Inputs

HTTP middleware/response header config, CORS config, REST controllers, per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check for a Content-Security-Policy header and that it avoids `unsafe-inline`/`unsafe-eval` where practical.
3. Check standard security headers are set: `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`/frame-ancestors, `Referrer-Policy`.
4. Check CORS is scoped to specific origins, not `*` combined with credentials.
5. Check REST endpoints enforce HTTPS, use safe HTTP methods correctly (idempotency of GET/PUT/DELETE), and don't leak stack traces or internal details in error responses.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
