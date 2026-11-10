---
name: review-security-operational
description: 'Reviews error handling and fail-safe behaviour, security logging (sensitive data, log injection, security events, log protection), secrets management and production configuration, against pinned OWASP cheat sheets (Error Handling, Logging, Secrets Management, Secure Code Review), OWASP Top 10:2025 A09/A10 and pinned ASP.NET Core/.NET, Spring Boot and Django/Python guidance. Use when the compliance-reviewer orchestrator delegates the Security subject (Operational sub-subject).'
user-invocable: false
---

# Review: Security — Operational

Assesses how the target handles errors and exceptional conditions, what and how it logs, how it stores and
delivers secrets, and whether production configuration is locked down, using local, pinned summaries of OWASP and
vendor guidance.

## Inputs

Global error handlers and exception middleware, logging code and logging configuration, secrets/config loading
code and configuration files (`appsettings*.json`, `web.config`, `application*.properties|yml`, `settings*.py`,
committed `.env` files), container and orchestrator definitions, admin/audit code paths and transaction code, per
`compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/owasp-operational.md` — ERR-01…06, LOG-01…26, SMG-01…12, SCR-01…03, A09-01…08,
  A10-01…07. Always load.
- `references/standards/dotnet-operational.md` — DNO-01…16. Load when language `csharp` is detected.
- `references/standards/java-operational.md` — JVO-01…06. Load when language `java` is detected.
- `references/standards/python-operational.md` — PYO-01…09. Load when language `python` is detected.
- `references/standards/node-operational.md` — NDO-01…05. Load when language `javascript` is detected.
- Framework elements apply only when that framework is in use; runtime and library elements apply whenever the
  language is detected. Container, orchestrator and CI files are evaluated with the language-agnostic SMG and LOG
  elements whenever they are in the subject's files.
- Do **not** fetch any URL for this skill, and never use remembered defaults: an error-page, logging or
  secret-store default counts only when a localized element states it. Do not load
  `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, the standards files that apply (above), and
   `references/languages/<id>.md` for each detected language (detection signals only; they cite no standard).
2. Read as the Secure Code Review method suggests (scr#review-process, scr#data-flow-analysis): start from the
   global error handler, logging configuration and configuration loading, then trace high-risk paths (admin
   functions, data export, authorization decisions, multi-step writes) to their error paths and log calls. The
   method guides reading; it is not scored.
3. For each check SEC-OP-01…SEC-OP-10, evaluate the elements it lists against the subject's files, using the
   signal files to find evidence. Mark a check N/A with a reason when no element applies (e.g. SEC-OP-07 when no
   production configuration is in the files; SEC-OP-10 when there are no multi-step writes or security
   decisions in the files).
4. Evidence rules: fail an element only on concrete code or configuration in the files (see the evidence notes in
   `checklist.md`). A missing setting counts only when a localized element states the insecure default; for
   libraries without one, add `localized-standard-gap: <library> default for <setting> not localized` to `notes`.
   Platform-injected environment variables are acceptable secret delivery; SMG-07 and DNO-11 never fail on their
   own. Don't fail on speculation. Use confidence `medium` unless the evidence is unambiguous.
5. Ownership: management-endpoint network placement is judged here (ORS-01 under SEC-OP-07). Don't report
   authentication/authorization/session-failure logging or management-endpoint authorization (identity-access), SQL injection in log writes (input-injection), HTTP headers (web-api),
   telemetry attributes, correlation IDs, audit/diagnostic log separation or health-endpoint detail
   (observability), alerting, SIEM routing, retention or telemetry-store access (monitoring), general robustness
   outside security paths (software-quality), rate limits and quotas (reliability), library versions
   (dependency-management) or error-response format (api-design). Logging rejected input verbatim is judged here.
6. Severity: MUST/REVIEW elements take the check's default from `checklist.md`; SHOULD elements one level lower
   (Error → Warning, Warning → Information). Always Error, whatever the check's default: production debug mode,
   developer exception page or stack-trace/message exposure (PYO-01 `DEBUG = True` in production settings; DNO-06
   `UseDeveloperExceptionPage()` not gated on Development; JVO-01 `include-stacktrace`/`include-message` =
   `always`), and Actuator `env`/`configprops` exposed over HTTP with `show-values: always` (JVO-03). When several
   elements fail on the same evidence, write one finding at the highest severity. `checkResults.severityIfFailed`
   is the check's default.
7. Citations: prefer a vendor element, then a cheat-sheet element, then an A09/A10 element (cite A09/A10 only
   when nothing more specific fits; otherwise name the Top 10 ID in the recommendation). For an element marked
   (Default), cite the OWASP element it supports and name the vendor element in the recommendation. Where vendor
   guidance is weaker than an OWASP element, the OWASP element decides. `standard` = "<source name> — <element
   ID>" (source name from the standards file header); `url` = citation base + "#" + primary anchor (first anchor
   listed). `urlsFetched` stays empty.
8. If the reference date (date part of `startedAt`) is more than 9 months after a standards file's "Localized"
   date, add `localized-standard-stale: <file> localized <date>` to `notes`.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
