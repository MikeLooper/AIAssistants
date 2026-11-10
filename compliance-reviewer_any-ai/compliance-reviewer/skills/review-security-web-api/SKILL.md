---
name: review-security-web-api
description: 'Reviews Content Security Policy, HTTP security response headers, HSTS and HTTPS/TLS enforcement, CORS, and API transport hygiene (response headers, methods and content types, credentials in URLs), against pinned OWASP cheat sheets (CSP, HTTP Headers, REST Security, HTML5 CORS, HSTS, TLS), OWASP Top 10:2025 A02 and pinned ASP.NET Core, Spring Security and Django guidance. Use when the compliance-reviewer orchestrator delegates the Security subject (Web & API sub-subject).'
user-invocable: false
---

# Review: Security — Web & API

Assesses the browser-facing and transport security of HTTP applications and APIs: CSP, security response headers,
HSTS and HTTPS/TLS enforcement, CORS, API response headers, HTTP method and content-type handling, and credentials in
URLs, using local, pinned summaries of OWASP and vendor guidance.

## Inputs

HTTP pipeline and middleware setup, security/header configuration (framework config classes, `settings*.py`),
CORS configuration, web-server and proxy configuration (`web.config`, `nginx*.conf`, `.htaccess`), HTTP listener
configuration (`launchSettings.json`, `application*.properties|yml`, `Dockerfile`), REST controllers and file-download
endpoints, and HTML layout templates, per `compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/owasp-web-api.md` — CSP-01…11, HDR-01…19, RST-01…12, H5-01…05, HST-01…02, TLS-01…05,
  A02-01…05. Always load.
- `references/standards/dotnet-web-api.md` — DNW-01…10. Load when language `csharp` is detected.
- `references/standards/java-web-api.md` — JVW-01…11. Load when language `java` is detected.
- `references/standards/python-web-api.md` — PYW-01…09. Load when language `python` is detected.
- `references/standards/mdn-web-api.md` — MDN-01 (CSP Trusted Types). Always load.
- `references/standards/node-web-api.md` — NDW-01…05. Load when language `javascript` is detected.
- Framework elements apply only when that framework (and, for Django, the named middleware) is in use.
- Do **not** fetch any URL for this skill, and never use remembered defaults: a header, HTTPS or CORS default counts
  only when a localized element states it. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, the standards files that apply (above), and
   `references/languages/<id>.md` for each detected language (detection signals only; they cite no standard).
2. Classify the target from its files: HTML-serving (views, templates, static HTML or SPA host served by the app),
   API-only (endpoints returning JSON/XML, no HTML), or neither (subject N/A). For API-only targets mark SEC-WA-01,
   -04 and -11 N/A ("API-only: browser-rendering headers not applicable").
3. Find where response headers are set: application code and configuration, framework defaults stated by a
   localized (Default) element, and web-server/proxy/IaC files in the subject's list. A header set in any of them
   counts as set. A header missing everywhere fails at confidence `medium` for ASP.NET Core, Spring Security,
   Django and Express (helmet defaults, NDW-01); for other frameworks judge explicit values only and add
   `localized-standard-gap: <framework> default for <header> not localized` to `notes`.
4. For each check SEC-WA-01…SEC-WA-11, evaluate the elements it lists against the subject's files, using the
   signal files to find evidence and the evidence notes in `checklist.md`. No CORS configuration at all passes
   SEC-WA-05. An HTTPS-only API without HSTS passes SEC-WA-02. Don't fail on speculation. Use confidence `medium`
   unless the evidence is unambiguous.
5. Ownership: don't report error-response bodies or diagnostic endpoints (operational), cookie flags, CSRF,
   session IDs in URLs, JWT/API-key handling, method or management-endpoint authorization (identity-access), XSS
   encoding, request size limits or XXE (input-injection), method semantics, idempotency, status codes or error
   format (api-design), rate limits (reliability), caching of public assets (performance), or library versions
   (dependency-management). CSP is defense in depth; never report a missing CSP as an XSS vulnerability.
6. Severity: MUST/REVIEW elements take the check's default from `checklist.md`; SHOULD elements one level lower
   (Error → Warning, Warning → Information); HDR-11 is advisory and never fails on its own. When several elements
   fail on the same evidence, write one finding at the highest severity. `checkResults.severityIfFailed` is the
   check's default.
7. Citations: prefer a vendor element, then a cheat-sheet element, then an A02 element (cite A02 only when nothing
   more specific fits). For an element marked (Default), cite the OWASP element it supports and name the vendor
   element in the recommendation. Where vendor guidance is weaker than an OWASP element, the OWASP element decides.
   `standard` = "<source name> — <element ID>" (source name from the standards file header); `url` = citation base
   + "#" + primary anchor (first anchor listed). `urlsFetched` stays empty.
8. If the reference date (date part of `startedAt`) is more than 9 months after a standards file's "Localized"
   date, add `localized-standard-stale: <file> localized <date>` to `notes`.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
