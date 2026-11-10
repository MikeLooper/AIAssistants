---
name: review-security-identity-access
description: 'Reviews authentication enforcement, authorization (function- and object-level), JWT validation, OAuth 2.0/OIDC flows, session management and CSRF for cookie auth, password storage and policy, authentication failure handling, client-side token handling and Zero Trust posture, against pinned OWASP cheat sheets, OWASP Top 10:2025 A01/A07 and pinned ASP.NET Core, Spring Security and Django guidance. Use when the compliance-reviewer orchestrator delegates the Security / Identity & Access subject.'
user-invocable: false
---

# Review: Security — Identity & Access

Assesses how the target authenticates users and services, authorizes actions, issues and validates tokens,
manages sessions and stores credentials, using local, pinned summaries of OWASP and framework guidance.

## Inputs

Auth middleware/filters, security configuration (e.g. `SecurityFilterChain`, `Program.cs` auth setup,
`settings.py`), login/registration/password-reset/logout code, token issuing and validation code, session and
cookie config, identity-provider/OAuth client config, user and role seed data, and front-end code that stores
tokens, per `compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/owasp-identity-access.md` — ATN-01…18, ATZ-01…08, JWT-01…11, OAU-01…11, SES-01…17,
  PWS-01…10, ZTA-01…05, T10-01…16. Always load.
- `references/standards/aspnetcore-identity.md` — ASP-01…14. Load when language `csharp` is detected.
- `references/standards/spring-security.md` — SPS-01…13. Load when language `java` is detected.
- `references/standards/django-auth.md` — DJ-01…11. Load when language `python` is detected.
- `references/standards/node-identity-access.md` — NDA-01…05. Load when language `javascript` is detected.
- Framework elements apply only when that framework is in use; otherwise they don't apply.
- Do **not** fetch any URL for this skill, and never use remembered framework defaults: a default counts only when
  a localized element states it. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, the standards files that apply (above), and
   `references/languages/<id>.md` for each detected language (detection signals only; they cite no standard).
2. For each check SEC-IA-01…SEC-IA-11, evaluate the elements it lists against the subject's files, using the
   signal files to find evidence. Mark the check N/A with a reason when no element applies (e.g. SEC-IA-04 when
   no OAuth/OIDC is used; SEC-IA-06/-10 when the target stores no passwords; SEC-IA-03 when no JWTs are handled).
3. Evidence rule: fail an element only on concrete evidence in the files. Explicit insecure settings always count;
   a missing setting counts only when a localized element states the insecure default. For frameworks without a
   localized file (Flask, FastAPI, Express, Quarkus, …), a missing setting is not a finding: add
   `localized-standard-gap: <framework> default for <setting> not localized` to `notes`. When the files can't show
   whether an element is met, it doesn't apply. Don't fail on speculation. Use confidence `medium` unless the
   evidence is unambiguous. Legacy framework APIs (`WebSecurityConfigurerAdapter`, `authorizeRequests`,
   `@EnableGlobalMethodSecurity`, `System.Web` Forms auth) are judged against the same elements; whether the
   framework version is supported belongs to `review-dependency-management`.
4. Ownership: don't report security headers, CORS or site-wide HTTPS (web-api), secrets in logs or hardcoded
   secrets (operational), input validation (input-injection), general API rate limiting (reliability), missing
   tests (testing) or out-of-order workflow execution (review-software-quality SQR-37 under AP-02; per-step
   authorization stays here under SEC-IA-02). CSRF for cookie-authenticated state changes is reported here under SEC-IA-05. JWT-08 still
   flags a weak or password-derived HMAC secret.
5. Severity: MUST/REVIEW elements take the check's default from `checklist.md`; SHOULD elements one level lower
   (Error → Warning, Warning → Information). Exceptions, always Error: default credentials shipped (T10-08);
   passwords, session IDs or tokens over plain `http://` (ATN-09, OAU-11); JWT signature not verified (JWT-01).
   When several elements fail on the same evidence, write one finding at the highest severity.
   `checkResults.severityIfFailed` is the check's default.
6. Citations: prefer a framework element, then a cheat-sheet element, then a T10 element (cite T10 only when
   nothing more specific fits; otherwise name it in the recommendation). `standard` = "<source name> — <element ID>"
   (source name from the standards file header); `url` = citation base + "#" + primary anchor (first anchor listed).
   `urlsFetched` stays empty.
7. If the reference date (date part of `startedAt`) is more than 9 months after a standards file's "Localized"
   date, add `localized-standard-stale: <file> localized <date>` to `notes`.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
