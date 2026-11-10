---
name: review-security-input-injection
description: 'Reviews input validation, SQL and ORM injection, query parameterization, command and other interpreter injection, XML parser security, file upload handling, XSS output encoding, unsafe deserialization and server-side request forgery (SSRF), against pinned OWASP cheat sheets, OWASP Top 10:2025 A05 and pinned .NET, Java (Oracle, Spring Data JPA) and Python/Django guidance. Use when the compliance-reviewer orchestrator delegates the Security subject (Input & Injection sub-subject).'
user-invocable: false
---

# Review: Security — Input & Injection

Assesses how the target validates untrusted input and keeps it from being interpreted as code: SQL/ORM queries,
OS commands and other interpreters, XML parsers, file uploads, rendered output, deserializers and server-side
requests to input-derived URLs, using local,
pinned summaries of OWASP and vendor guidance.

## Inputs

Request handlers/controllers and DTOs, data access/ORM code and stored-procedure SQL, process-execution code,
XML parsing code, file upload handlers and upload/body-size configuration, templates/views and front-end code that
writes to the DOM, serialization/deserialization code and message consumers, per `compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/owasp-input-injection.md` — IV-01…09, INJ-01…06, SQL-01…07, QP-01…02, XML-01…05,
  FU-01…10, XSS-01…10, DES-01…09, A05-01…07. Always load.
- `references/standards/dotnet-input.md` — NET-01…15. Load when language `csharp` is detected.
- `references/standards/java-input.md` — JVA-01…15. Load when language `java` is detected.
- `references/standards/python-input.md` — PY-01…10. Load when language `python` is detected.
- `references/standards/node-input.md` — NDI-01…06. Load when language `javascript` is detected.
- Framework elements apply only when that framework is in use; runtime elements apply whenever the language is
  detected. Front-end code (JavaScript/TypeScript, DOM sinks) is evaluated with XSS-01…10 whenever it is in the
  subject's files.
- Do **not** fetch any URL for this skill, and never use remembered defaults: a parser, framework or serializer
  default counts only when a localized element states it. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, the standards files that apply (above), and
   `references/languages/<id>.md` for each detected language (detection signals only; they cite no standard).
2. For each check SEC-II-01…SEC-II-10, evaluate the elements it lists against the subject's files, using the
   signal files to find evidence. Mark a check N/A with a reason when no element applies (e.g. SEC-II-05 when no
   XML is parsed; SEC-II-06/-07 when there are no uploads; SEC-II-08 when nothing is rendered to HTML; SEC-II-09
   when nothing is deserialized beyond plain JSON into DTOs; SEC-II-10 when no outbound request uses a URL, host or
   IP derived from untrusted data).
3. Untrusted data is anything the application didn't create, including stored user data and messages from other
   services. Evidence rule: fail an element only when untrusted data concretely reaches the sink in the files, or
   on an explicit insecure setting. A missing setting counts only when a localized element states the insecure
   default; for libraries without one, add `localized-standard-gap: <library> default for <setting> not
   localized` to `notes`. When the files show the sink but not where the data comes from, fail at confidence `low`
   only if the value is plainly external (e.g. an action parameter); otherwise don't fail. Don't fail on
   speculation. Use confidence `medium` unless the evidence is unambiguous.
4. Ownership: don't report CSP or Trusted Types (web-api), log injection or hardcoded credentials (operational),
   upload authorization or CSRF (identity-access), outdated library versions (dependency-management), or
   download/request rate limits (reliability). Request body size limits are evaluated here (IV-04, FU-05). SSRF is
   judged here (SEC-II-10; decision D-1, 2026-11-09); network egress controls and cloud metadata settings in IaC
   aren't judged by any subject (known coverage gap).
5. Severity: MUST/REVIEW elements take the check's default from `checklist.md`; SHOULD elements one level lower
   (Error → Warning). When several elements fail on the same evidence, write one finding at the highest severity.
   `checkResults.severityIfFailed` is the check's default.
6. Citations: prefer a vendor element, then a cheat-sheet element, then an A05 element (cite A05 only when nothing
   more specific fits). For an element marked (Default), cite the OWASP element it supports and name the vendor
   element in the recommendation. Where vendor guidance is weaker than an OWASP element, the OWASP element decides.
   `standard` = "<source name> — <element ID>" (source name from the standards file header); `url` = citation base
   + "#" + primary anchor (first anchor listed; the base alone when no anchor is given). `urlsFetched` stays empty.
7. If the reference date (date part of `startedAt`) is more than 9 months after a standards file's "Localized"
   date, add `localized-standard-stale: <file> localized <date>` to `notes`.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
