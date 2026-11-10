# Maintenance — Security: Operational localized standards

**Maintainers only. Workers never load this file.** Background and design decisions:
`docs/plan_localize-review-security-operational.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website and per host (plan DEC-6). `review-security-identity-access` (94) and
`review-security-input-injection` (66) also use cheatsheetseries.owasp.org; those budgets are separate.

| Website | Local file(s) | Elements | Cap | Note |
|---|---|---|---|---|
| cheatsheetseries.owasp.org | owasp-operational.md (48, incl. ORS-01) + dotnet-operational.md (5) + node-operational.md (5) | **58** | 100 | Headroom 42 (Node.js sheet, 5 elements, added 2026-11-09) |
| top10.owasp.org | owasp-operational.md | 15 | 100 | A09:2025 (8), A10:2025 (7) |
| learn.microsoft.com | dotnet-operational.md | 11 | 100 | 7 pages (ASP.NET Core 10.0, .NET logging) |
| docs.spring.io | java-operational.md | 6 | 100 | Spring Boot 4.1 reference, selected sections and property rows |
| docs.djangoproject.com | python-operational.md | 5 | 100 | Django 6.1, 5 pages (selected sections/settings) |
| docs.python.org | python-operational.md | 4 | 100 | Python 3.15, 2 pages |
| expressjs.com | node-operational.md | 1 | 100 | Production Best Practices: Security (2026-11-09) |
| **Total** | | **99** | | |

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Prefixes (ERR, LOG,
  SMG, SCR, A09, A10, DNO, JVO, PYO) stay distinct from every other localized skill (plan DEC-9).
- Check IDs: SEC-OP-07 was reused once, by user decision (plan DEC-4: it changed from "the review prioritized
  high-risk areas" to the production-configuration check). Check IDs are not reused again.
- Every element ID is listed by exactly one check in `../checklist.md`, and the "Check" column of its row names that check.
- Level:
  - OWASP cheat sheets: `MUST` where the source says must/must not/never/do not/ensure, gives an unqualified
    imperative, or names a prohibited practice; Logging sheet "Where possible, always log" items are `MUST`
    ("Optionally consider" items are not localized); `SHOULD` for should/recommended/prefer/consider/"if available".
    Secure Code Review checklist items are `MUST`.
  - Top 10: `MUST` for "How to prevent" bullets, `REVIEW` for "Description" weaknesses and mapped CWEs (`REVIEW` is
    treated like `MUST`).
  - Vendor files: the level of the OWASP element the vendor element supports, or `SHOULD` when the vendor only recommends.
- **(Default)** elements state API behaviour or a default. Add one only with the version it was read from and the source
  sentence quoted in the localization log. Workers may rely on no other default (`SKILL.md` step 4).
- Vendor elements state behaviour and defaults; they never relax an OWASP element (plan DEC-8).
- SMG-07 and DNO-11 are advisory and never fail on their own (plan DEC-13, consistent with `review-twelve-factor` TF-03 / TFR-06).
- Boundary with `review-software-quality` SQ-06: SQ-06 judges exception *design* (granularity, catch-alls only at boundaries, no exceptions as control flow); swallowed or unlogged errors are SEC-OP-02 and fail-safe handling is SEC-OP-10. Don't add elements for exception granularity.
- Primary anchor first; list every absorbed anchor so coverage stays auditable. Rows ≈ 220 characters at most.
  Microsoft Learn pages carry several version blocks: use only anchors of the block that includes `aspnetcore-10.0`
  (or common content); older blocks repeat headings with `-1`/`-2` suffixes or use different ids.
- Vendor files are split **by language** (matching `compliance-review-core/references/languages.md` ids). A new vendor
  file gets a line in `SKILL.md`, a row in `../sources.md` and a row in the budget table.

## Refresh procedure

1. **Cadence:**
   - OWASP file: quarterly, or when run notes contain ≥ 3 `localized-standard-gap` or any `localized-standard-stale`
     entry for this skill. Secrets Management was committed on 2026-11-08 and Logging on 2026-10-22.
   - Top 10: when a new edition is published (check whether A09/A10 are renumbered).
   - Microsoft Learn: on each ASP.NET Core/.NET major release (November) — re-pin `view=` — and when `ms.date` changes
     on the unversioned .NET pages (`ms-log`, `ms-red`).
   - Spring Boot: within two weeks of each minor release (api.spring.io); property renames (as in 4.0, `server.error.*`
     → `spring.web.error.*`) change JVO-01.
   - Django: within two weeks of each feature release. Python: within two weeks of each feature release (October).
2. **Detect drift:**
   - OWASP cheat sheets: compare the latest commit SHA of each pinned file
     (`https://api.github.com/repos/OWASP/CheatSheetSeries/commits?path=cheatsheets/<Name>_Cheat_Sheet.md&per_page=1`)
     with the pinned SHA. If they differ, diff the text and the anchor list.
   - Top 10: `https://api.github.com/repos/OWASP/Top10/commits?path=2025/docs/en/<page>.md&per_page=1` for
     `A09_2025-Security_Logging_and_Alerting_Failures` and `A10_2025-Mishandling_of_Exceptional_Conditions`.
   - Microsoft Learn: the `ms.date` meta tag of each page and the current ASP.NET Core / .NET version.
   - Spring Boot: `https://api.spring.io/projects/spring-boot/releases` (the release with `current: true`).
   - Python: the version in the title of `https://docs.python.org/3/`. Django: the redirect target of
     `https://docs.djangoproject.com/en/stable/`.
   - On any vendor change, re-read the pinned sections and the stated defaults (DNO-06, DNO-07, DNO-10, DNO-11, DNO-12,
     DNO-14, JVO-01 … JVO-03, JVO-05, JVO-06, PYO-01, PYO-03, PYO-05, PYO-08).
3. **Update:** keep IDs stable (new IDs only, `(retired)` for removed rules). Keep every website ≤ 100 for this skill,
   and decide follow-up candidates against the remaining headroom. Update the coverage map below, the "Localized" dates
   and versions in the file headers, `../sources.md`, and the URL list in
   `compliance-review-core/references/approved-sources.md` when a version path changes (e.g. `aspnetcore-10.0` →
   `aspnetcore-11.0`, `/en/6.1/` → `/en/6.2/`, `/3.15/` → `/3.16/`).
4. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo); run any Python over them with `-I`.
   - Script-check: 93 element IDs, each in exactly one check, matching its row's "Check" column; every signal row in
     `../languages/*.md` names at least one existing element ID; every listed anchor exists as an `id` on its published
     page (Learn anchors inside the 10.0 version block or common content); every H2/H3/H4 anchor of the 5 cheat sheets
     (the .NET sheet: all headings), every A09/A10 Description / How-to-prevent bullet and every anchor of the pinned
     vendor sections appears in the coverage map below — zero unaccounted.
   - Run reviews against small sample repos (plan §9 step 10): `validate` passes,
     `17-review-security-operational.json` has `urlsFetched: []` and 10 check results, expected findings cite the
     element IDs, SHOULD elements are one level lower, always-Error cases are at Error, environment-variable secrets
     alone produce no finding.
5. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-security-operational` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Refresh due

- **ASP.NET Core / .NET 11** (November 2026): re-pin `view=aspnetcore-11.0` and re-read DNO-06, DNO-07, DNO-10,
  DNO-11, DNO-12, DNO-14 (the Learn pages already carry `aspnetcore-11.0`/`12.0` in the 10.0 version block).
- **Spring Boot 4.2** (4.2.0-RC2 on 2026-11-08): re-read JVO-01 … JVO-06 within two weeks of GA.
- **Django 6.2** (next feature release): re-pin `python-operational.md` and re-read PYO-01, PYO-03, PYO-05.
- **Python 3.16** (October 2027): re-pin `/3.16/` and re-read PYO-06 … PYO-09.

## Localization log

### 2026-11-08 — initial localization

- Snapshot taken on 2026-11-08 (planning) and re-taken the same day at implementation (plan §9 step 1), into a scratch
  folder: 5 cheat sheets (published HTML and the Markdown at each pinned SHA), the A09 and A10 pages (HTML and
  Markdown at the pinned SHAs), 19 vendor pages, the GitHub commits API, `api.spring.io`, `docs.python.org/3.15/` and
  `docs.djangoproject.com/en/stable/`. The user approved the non-allowlisted fetches for planning and again for
  implementation. Plan decisions DEC-1 … DEC-14 were all confirmed by the user on 2026-11-08.
- Pins confirmed unchanged against the plan (GitHub commits API, latest commit per file):

  | Page | Commit | Date (UTC) |
  |---|---|---|
  | Error Handling | 796eed7d0a36450702bc930050f0c4aac8e31b75 | 2026-10-04 |
  | Logging | f1d0311aaadac4c315471feb8947c9fbb3cbb32e | 2026-10-22 |
  | Secrets Management | d6474de095dedba6caf536fdf8926d6ae53f3cfc | 2026-11-08 23:09 |
  | Secure Code Review | a11444a59f93e1ab696ae9ff474b52a1d124bc4b | 2026-10-04 |
  | .NET Security | 3cfa49de48236c667ddf1d0f9dc79e13e672b56d | 2026-10-18 |
  | Java Security (not used) | f1d0311aaadac4c315471feb8947c9fbb3cbb32e | 2026-10-22 |
  | Top 10 A09:2025 | d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966 | 2025-12-24 |
  | Top 10 A10:2025 | 494be56d88168940f1f3392961f71fe2cc414e6a | 2026-01-06 |

- DEC-10 disclosures:
  - (a) Secrets Management same-day commit: `d6474de0` changes one sentence in §7.1 (keylength.com link replaced by
    NIST SP 800-57 Part 1) and nothing else in this sheet. The published HTML at implementation already shows the
    NIST link and no keylength.com link, so it matches the pinned Markdown. §7.1 is not localized (code F), so no
    element is affected. The other four sheets' published text also matches their pinned Markdown (only code blocks
    differ in extraction).
  - (b) The Application Logging Vocabulary Cheat Sheet was downloaded during planning (not allowlisted); its content
    is not used. Not re-downloaded at implementation.
  - (c) The A02:2025 page was downloaded in error during planning and deleted unread. Not re-downloaded.
- Versions: ASP.NET Core 10.0 (`view=aspnetcore-10.0`); `ms.date` — error handling 2026-10-27, environments
  2026-11-04, app secrets 2026-05-13, Key Vault 2026-05-13, HTTP logging 2025-04-25, .NET logging 2025-10-21, data
  redaction 2025-03-21 (all as planned). Spring Boot 4.1.2 is `current` on api.spring.io (4.2.0-RC2 is a prerelease).
  Python 3.15.2 (`docs.python.org/3.15/` title). Django 6.1 (`/en/stable/` redirects to `/en/6.1/`).
- Anchors: all 140 element anchor references (97 distinct) exist as `id`s on the published pages; every Learn anchor is in the 10.0 version
  block or in common content (checked against the `data-moniker` zones).
- Defaults quoted from the sources (the only defaults workers may rely on):
  - DNO-06: "ASP.NET Core apps enable the developer exception page by default when both: Running in the Development
    environment. The app was created with the current templates, that is, by using WebApplication.CreateBuilder." /
    "Don't enable the Developer Exception Page unless the app is running in the Development environment." / it can
    include "Stack trace", "Query string parameters", "Cookies", "Headers".
  - DNO-07: "If the environment isn't set, it defaults to the Production environment, which disables most debugging
    features." / "DOTNET_ENVIRONMENT, if present, is read during initial bootstrap and takes precedence over
    ASPNETCORE_ENVIRONMENT."
  - DNO-10: "Starting in .NET 10, the default behavior is to suppress emission of diagnostics such as logs and metrics
    for handled exceptions (when TryHandleAsync returns true). This differs from earlier versions (.NET 8 and 9) where
    diagnostics were always emitted regardless of whether the exception was handled."
  - DNO-11: "Environment variables are commonly stored as plain, unencrypted text. If the machine or process is
    compromised, environment variables are accessible to untrusted parties."
  - DNO-12: "Secret Manager doesn't encrypt the stored secrets and shouldn't be treated as a trusted store. It's for
    development purposes only. The keys and values are stored in a JSON configuration file in the user profile directory."
  - DNO-14: "By default, HTTP logging logs common properties such as path, status-code, and headers for requests and
    responses." / "LoggingFields defaults to RequestPropertiesAndHeaders | ResponsePropertiesAndHeaders." / "Header
    values are only logged for header names that are in these collections." / "HTTP logging can potentially log
    personally identifiable information (PII)."
  - JVO-01: properties appendix — `spring.web.error.include-stacktrace` "never", `include-message` "never",
    `include-exception` "false", `include-binding-errors` "never". Servlet page: "For machine clients, it produces a
    JSON response with details of the error, the HTTP status, and the exception message." (weaker; DEC-8 applies).
  - JVO-02: "By default, only the health endpoint is exposed over HTTP and JMX." / "Before setting the
    management.endpoints.web.exposure.include, ensure that the exposed actuators do not contain sensitive information,
    are secured by placing them behind a firewall, or are secured by something like Spring Security." / "If Spring
    Security is on the classpath and no other SecurityFilterChain bean is present, all actuators other than /health
    are secured by Spring Boot auto-configuration."
  - JVO-03: "Information returned by the /env, /configprops and /quartz endpoints can be sensitive, so by default
    values are always fully sanitized (replaced by ******)." / "always - values are shown to all users" / "By default,
    any authenticated user is authorized."; `management.endpoint.env.show-values` default "never".
  - JVO-05: "By default, Spring Boot logs only to the console and does not write log files." / "If you are using
    Logback or Log4j2, it is possible to fine-tune log rotation settings … For all other logging system, you will need
    to configure rotation settings directly yourself." / `max-history` "(defaults to 7)" for both.
  - JVO-06: "Spring Boot supports structured logging and has support for the following JSON formats out of the box:
    Elastic Common Schema (ECS), Graylog Extended Log Format (GELF), Logstash" / set `logging.structured.format.console`
    or `logging.structured.format.file`.
  - PYO-01: `DEBUG` "Default: False" / "Never deploy a site into production with DEBUG turned on." / excluded setting
    names 'API', 'KEY', 'PASS', 'SECRET', 'SIGNATURE', 'TOKEN' / "when running with DEBUG turned on, Django will
    remember every SQL query it executes" / "The default settings.py file created by django-admin startproject sets
    DEBUG = True for convenience."
  - PYO-03: "by default Django records the full traceback for the exception raised, each traceback frame's local
    variables, and the HttpRequest's attributes".
  - PYO-05: "When DEBUG is False: The django logger sends messages in the django hierarchy (except django.server) with
    ERROR or CRITICAL level to AdminEmailHandler." (console handler filtered by `require_debug_true`).
  - PYO-08: "The default value of raiseExceptions is True." / "If raiseExceptions is False (production mode), the
    event is silently dropped."
- Corrections made while checking rows:
  - **DNO-11**: the plan's anchor `ms-sec#environment-variables` sits in the 3.0–5.0 version block. In the 10.0 block
    the section is `ms-sec#work-with-environment-variables`, now the only anchor. Wording aligned with the source
    ("commonly stored as plain, unencrypted text").
  - **DNO-12**: the plan's anchors `ms-sec#secret-manager` and `ms-sec#how-the-secret-manager-tool-works` sit in the
    3.0–5.0 block. In the 10.0 block both passages are under `ms-sec#use-the-secret-manager-tool`, now the only anchor.
  - **DNO-07**: wording aligned with the source (unset → Production, "disables most debugging features").
  - **JVO-05**: the plan said other systems than Logback need their own rotation. Spring Boot 4.1 also supports Log4j2
    rotation via `logging.log4j2.rollingpolicy.*` (`max-history` 7, `max-file-size` 10MB); the row now names both.
  - **A09-05**: A09:2025 says "all transactions", not "high-value transactions" (that was the 2021 wording); the row
    now says "Transactions".
  - **PYO-01**: "local variables" replaced by "environment metadata" (the `DEBUG` setting text describes a detailed
    traceback with environment metadata and settings; local variables are PYO-03's error-report default).
  - Anchors added for coverage only (no change of meaning): LOG-04 and LOG-25 `scr#security-monitoring` (audit-trail
    and log-integrity items); SMG-10 `smg#273-revocation`; DNO-05 `dnet#data-protection`; PYO-03
    `dj-log#security-implications`.
- Level judgments: SCR-01 … SCR-03 are checklist items without RFC keywords, kept `MUST` (pass/fail review criteria,
  plan §4.2); vendor (Default) rows take the level of the OWASP element they support.
- Sample-repo review runs (plan §9 step 10) were deferred by the user on 2026-11-08; see "Open items".

### 2026-11-09 — management-endpoint network placement (afterplanning WP-12b)

- ORS-01 added under SEC-OP-07 from the OWASP REST Security Cheat Sheet `#management-endpoints` (commit
  97cb8a3c4b62104227ba52833ff7842ff1d0c850, 2026-10-14; the same pin `review-security-web-api` uses for its own RST
  elements, separate budget). Prefix `ORS-` avoids web-api's `RST-`. Closes web-api plan C-3 (placement part). Check
  count unchanged; the element's "Avoid exposing … via Internet" and "Expose … via different HTTP ports or hosts"
  sentences are imperatives, so the level is `MUST`.

### 2026-11-09 — JavaScript/TypeScript (afterplanning WP-12f phase 2)

- `node-operational.md` (NDO-01 … NDO-05) and `../languages/javascript.md` from the OWASP Node.js Security Cheat Sheet (commit
  eeaa1e474bc2ef98119a3de7bafd067f52faf35e, 2026-11-05) and the Express page (custom error handlers). Closes this skill's JavaScript follow-up (Node logging follow-up).
  Check count unchanged. Framework defaults beyond those stated in `node-operational.md` (Fastify, NestJS, Next.js, Koa, Passport,
  logger masking) stay unlocalized; workers add `localized-standard-gap` notes.

## Open items

- Plan §9 step 10: run reviews against sample repos — (a) ASP.NET Core with ungated `UseDeveloperExceptionPage`, an
  `IExceptionHandler` returning `true` without logging, `$"…"` log templates, a token in a log call, a password in
  `appsettings.json`, `ENV API_KEY=` in the Dockerfile; (b) Spring Boot with `include-stacktrace=always`,
  `exposure.include=*` without security, `show-values=always`, `log.info("user " + name)`, a datasource password in
  `application.yml`, a multi-step write without `@Transactional`; (c) Django with `DEBUG = True`, literal
  `SECRET_KEY`, no `LOGGING`/`ADMINS`, `logger.info(f"…{password}")`, a login view without
  `sensitive_post_parameters`; (d) a well-configured app with a global handler, structured logging, Key Vault/managed
  identity and environment-gated diagnostics (expect SEC-OP-01/-05/-06/-07 to pass with strengths).
- Plan §10 C-1, C-2 and C-14 were applied on 2026-11-08; C-15 done 2026-11-09. The remaining hand-offs were closed by
  `docs/plan_localize-afterplanning-changes.md` (2026-11-09): C-7 security-event alerting → `review-monitoring`
  (WAFM-41 … WAFM-44); C-10 rate limiting → `review-reliability` AZRL-32; C-11 CI/CD secrets stay here; C-12
  dependency and API parts → boundary steps in those skills, secret-store backup → `review-disaster-recovery` DR-06.
  Open: none.

## Follow-up candidates (plan §7.3)

| Candidate | Est. elements | Status |
|---|---|---|
| Application Logging Vocabulary Cheat Sheet | ≈ 8 | Open (scope; fetch approval) |
| Key Management Cheat Sheet | ≈ 6 | Open (scope) |
| CI/CD Security Cheat Sheet (secrets and build-log masking) | ≈ 5 | Stays with security-operational; lifecycle doesn't own pipeline secrets (lifecycle plan C-6, DEC-5). Scope/fetch still open |
| Cryptographic Storage Cheat Sheet | ≈ 6 | Open (scope; ownership decision) |
| Kubernetes Security Cheat Sheet (secrets) | ≈ 3 | Open (IaC scope) |
| OWASP Top 10:2025 A02 Security Misconfiguration | ≈ 5 | Not approved by the user (DEC-3) |
| ASVS v5.0 V16 and V13 | > 40 | Open (would need its own budget decision) |
| Handling secrets in memory (`smg#25-handling-secrets-in-memory`) | 1 | Open (threat-model dependent; noisy) |
| Flask debug / `PROPAGATE_EXCEPTIONS`; FastAPI exception handlers | ≈ 3 each | Open (DEC-2 scope; new websites) |
| Serilog/NLog destructuring and masking; Logback/Log4j2 masking and `JsonTemplateLayout` | ≈ 4 each | Open (new websites) |
| ASP.NET Core `DetailedErrors` (Blazor), SignalR/gRPC `EnableDetailedErrors`, host `CaptureStartupErrors`/`DetailedErrors` (`ms-err#startup-exception-handling`) | ≈ 3 | Open (scope) |
| Microsoft Learn "Best practices for exceptions" | ≈ 4 | Open (scope) |
| Spring Boot DevTools in production | 1 | Open (scope) |
| Django `django.security.*` loggers (`dj-rlog#django-security`) | 1 | Open (scope) |

## `localized-standard-gap` / `localized-standard-stale` log

| Date | Run | Note | Action |
|---|---|---|---|
| — | — | (none yet) | — |

## Coverage map

Every H2/H3/H4 anchor of the 5 pinned cheat sheets, every A09/A10 Description and How-to-prevent bullet, and every
anchor of the pinned vendor sections is listed once: mapped to element IDs, or given a reason code. Microsoft Learn
pages list only headings of the 10.0 version block and common content (older-version duplicates are out of scope;
page chrome `ms--*` is ignored). Vendor pages localized for selected sections only (`dj-set` `DEBUG`, `dj-rlog`
default configuration, the Spring Boot pages' error-handling, Actuator exposure/security/sanitization, configuration
tree/encryption and logging file/rotation/structured sections, and the `sb-props` rows used) list only those anchors;
their other sections are out of scope [M]. Snapshot 2026-11-08, script-checked: 170 cheat-sheet headings, 14 Top 10
headings, 140 Learn headings, 25 Spring Boot anchors, 59 Django anchors and 40 Python anchors (447 in all), plus the
Top 10 bullets below; 0 unaccounted.

### Reason codes

| Code | Reason for not localizing |
|---|---|
| B | background, definitions, examples, review method, test techniques or references; no testable rule |
| P | parent heading; its rules are localized through the child anchors listed as mapped |
| C | Top 10 context (background, score table, attack scenarios, references), not a requirement |
| N | secret-store, infrastructure or organizational control; not visible in application code |
| M | framework mechanics or customization, or a section outside the pinned scope; not a security rule |
| S | restates or duplicates a localized element (named in brackets) |
| D | framework behaviour that meets the OWASP element by default; nothing to fail |
| F | follow-up candidate (plan §7.3) |
| Oia | owned by `review-security-identity-access` |
| Oinj | owned by `review-security-input-injection` |
| Oweb | owned by `review-security-web-api` |
| Oobs | owned by `review-observability` |
| Omon | owned by `review-monitoring` (alerting, SIEM, retention, log infrastructure) |
| Orel | owned by `review-reliability` (rate limits, quotas) |
| Odep | owned by `review-dependency-management` |
| Oapi | owned by `review-api-design` (status codes, Problem Details format) |
| Otest | owned by `review-testing` (TST-10: STS-04, STS-05, TSR-22) |
| Olc | owned by `review-software-lifecycle` (CI/CD pipeline hardening; plan C-11) |
| Odr | owned by `review-disaster-recovery` (optional; plan C-12) |
| Oscope | out of this subject's scope (general code quality, memory safety, concurrency, crypto algorithms) |

### Top 10 bullets

| Bullet | Mapped to / reason |
|---|---|
| A09 Description 1 (auditable events — logins, failed logins, high-value transactions — not logged) | A09-01 (login part Oia), LOG-04 |
| A09 Description 2 (warnings and errors: no, inadequate or unclear log messages) | A09-08 |
| A09 Description 3 (log integrity not protected) | S [LOG-25, A09-05] |
| A09 Description 4 (logs not monitored for suspicious activity) | Omon |
| A09 Description 5 (logs only stored locally, not backed up) | Omon, Odr |
| A09 Description 6 (alerting thresholds and escalation) | Omon |
| A09 Description 7 (pen tests and DAST don't trigger alerts) | Otest, Omon |
| A09 Description 8 (can't detect or alert on active attacks in real time) | Omon |
| A09 Description 9 (sensitive information leakage via visible logging events or logged PII/PHI) | A09-07 |
| A09 Description 10 (log data not correctly encoded) | S [A09-04] |
| A09 Description 11 (errors mishandled so the system is unaware) | A09-08 |
| A09 Description 12 … 14 (alert use cases, false positives, playbooks) | Omon |
| A09 Prevent 1 (login, access-control, input-validation failures logged with context) | A09-01 |
| A09 Prevent 2 (every security control logged, success or failure) | A09-02 |
| A09 Prevent 3 (log format consumable by log management) | A09-03 |
| A09 Prevent 4 (log data encoded against injection) | A09-04 |
| A09 Prevent 5 (transactions have an audit trail with integrity controls) | A09-05 |
| A09 Prevent 6 (failed transactions rolled back; fail closed) | A09-06 |
| A09 Prevent 7 … 11 (alerts, SOC playbooks, honeytokens, behavior analysis, incident response) | Omon |
| A10 Description (exceptional conditions: failure to prevent, identify, respond) | A10-07 |
| A10 Prevent 1 (catch errors where they occur; inform, log, alert) | A10-02 |
| A10 Prevent 2 (roll back part-way transactions; fail closed) | A10-03 |
| A10 Prevent 3 (rate limiting, quotas, throttling) | Orel |
| A10 Prevent 4 (repeated identical errors as statistics) | B |
| A10 Prevent 5 (input validation; centralized handling, logging, monitoring; global exception handler) | A10-01 (input validation Oinj; monitoring/alerting Omon) |
| A10 Prevent 6 (handle exceptional conditions the same way across the organization) | A10-01 |

### Error Handling CS (`err`)

| Anchor | Mapped to / reason |
|---|---|
| `introduction` | B |
| `context` | ERR-02 |
| `objective` | ERR-01, ERR-02, ERR-03 (RFC 7807/9457 format Oapi) |
| `proposition` | ERR-01 |
| `standard-java-web-application` | ERR-05 |
| `java-springmvcspringboot-web-application` | ERR-05 |
| `asp-net-core-web-application` | ERR-04 |
| `asp-net-web-api-web-application` | ERR-04, ERR-06 |
| `sources-of-the-prototype` | B |
| `appendix-http-errors` | Oapi (status codes), Omon (5xx monitoring) |
| `references` | B |

### Logging CS (`log`)

| Anchor | Mapped to / reason |
|---|---|
| `introduction` | B |
| `purpose` | B (audit/security log separation Oobs) |
| `operational-use-cases` | B |
| `security-use-cases` | B |
| `design-implementation-and-testing` | P |
| `event-data-sources` | LOG-15 |
| `where-to-record-event-data` | LOG-22, LOG-23, LOG-24 (routing to stdout/SIEM Oobs/Omon) |
| `which-events-to-log` | LOG-01 … LOG-07 (authentication, authorization, session failures Oia; "Optionally consider" list B) |
| `event-attributes` | LOG-08, LOG-09 (interaction identifier Oobs) |
| `data-to-exclude` | LOG-10, LOG-12, LOG-13, LOG-14 |
| `customizable-logging` | LOG-19 |
| `event-collection` | LOG-11, LOG-15, LOG-16, LOG-18, LOG-20 (SQL injection in log writes Oinj; time synchronization Omon) |
| `verification` | LOG-20, LOG-21 (lockout DoS Oia; testing bullets Otest) |
| `network-architecture` | Omon |
| `deployment-and-operation` | P |
| `release` | Omon |
| `operation` | Omon |
| `protection` | LOG-24, LOG-25, LOG-26 |
| `monitoring-of-events` | Omon |
| `disposal-of-logs` | Omon |
| `attacks-on-logs` | P |
| `log-injection` | LOG-16, LOG-21 |
| `log-injection-in-java` | LOG-17 |
| `confidentiality` | LOG-12 |
| `integrity` | S [LOG-25, LOG-26] |
| `availability` | LOG-21 |
| `accountability` | S [LOG-25] |
| `references` | B |

### Secrets Management CS (`smg`)

| Anchor | Mapped to / reason |
|---|---|
| `1-introduction` | SMG-01 |
| `2-general-secrets-management` | P |
| `21-high-availability` | N |
| `22-centralize-and-standardize` | N |
| `23-access-control` | SMG-09 |
| `24-automate-secrets-management` | SMG-10 |
| `241-architectural-patterns-for-automated-rotation` | B |
| `25-handling-secrets-in-memory` | F |
| `26-auditing` | N |
| `27-secret-lifecycle` | P |
| `271-creation` | N |
| `272-rotation` | SMG-10 |
| `273-revocation` | SMG-10 |
| `274-expiration` | SMG-10 |
| `28-transport-layer-security-tls-everywhere` | SMG-11 |
| `29-downtime-break-glass-backup-and-restore` | Odr |
| `210-policies` | N |
| `211-metadata-prepare-to-move-the-secret` | N |
| `212-passwordless-authentication-and-token-security` | Oia |
| `3-continuous-integration-ci-and-continuous-deployment-cd` | P |
| `31-hardening-your-cicd-pipeline` | Olc |
| `32-where-should-a-secret-be` | P |
| `321-as-part-of-your-cicd-tooling` | SMG-12 |
| `322-storing-it-in-a-secrets-management-system` | SMG-12 |
| `323-not-touched-by-cicd-at-all` | SMG-06 |
| `33-authentication-and-authorization-of-cicd-tooling` | SMG-12 |
| `34-logging-and-accounting` | Omon |
| `35-rotation-vs-dynamic-creation` | B |
| `36-pipeline-created-secrets` | SMG-04 |
| `4-cloud-providers` | P |
| `41-choosing-a-secret-management-service` | SMG-06 |
| `411-native-cloud-provider-services` | N |
| `412-hardware-security-modules-hsms` | N |
| `413-confidential-computing-and-enclaves` | N |
| `414-other-clouds-multi-cloud-and-cloud-agnostic` | N |
| `42-envelope-client-side-encryption` | F (crypto storage) |
| `421-client-side-encryption-versus-server-side-encryption` | F |
| `422-bring-your-own-key-versus-cloud-provider-key` | N |
| `43-identity-and-access-management-iam` | SMG-09 |
| `44-api-limits` | N |
| `5-containers-orchestrators` | SMG-02 |
| `51-injection-of-secrets-file-in-memory` | SMG-02, SMG-07 |
| `52-short-lived-sidecar-containers` | F (Kubernetes) |
| `53-internal-vs-external-access` | F (Kubernetes) |
| `6-implementation-guidance` | P |
| `61-key-material-management-policies` | F (Key Management) |
| `62-dynamic-vs-static-use-cases` | B |
| `63-ensure-limitations-are-in-place` | SMG-08 |
| `64-security-event-monitoring-is-key` | Omon |
| `65-usability-and-ease-of-onboarding` | B |
| `7-encryption` | P |
| `71-encryption-types-to-use` | F (crypto storage; the only section changed by `d6474de0`) |
| `72-convergent-encryption` | F |
| `73-where-to-store-the-encryption-keys` | SMG-03 |
| `74-encryption-as-a-service-eaas` | N |
| `8-detection` | P |
| `81-general-detection-approaches` | SMG-05 |
| `82-types-of-secrets-to-be-detected` | SMG-01 |
| `83-detection-lifecycle` | LOG-12 ("never logged"; other bullets B) |
| `84-documentation-for-how-to-detect-secrets` | B |
| `9-incident-response` | B |
| `91-documentation` | B |
| `92-remediation` | B |
| `93-logging` | B (Logging Vocabulary pointer F) |
| `10-related-cheat-sheets-further-reading` | B |
| `references` | B |

### Secure Code Review CS (`scr`)

| Anchor | Mapped to / reason |
|---|---|
| `introduction` | B |
| `review-types` | B |
| `review-methodology` | P |
| `preparation` | B |
| `review-process` | B (procedure guidance in `SKILL.md` step 2) |
| `common-vulnerability-patterns` | P |
| `input-validation-vulnerabilities` | Oinj |
| `injection-vulnerabilities` | Oinj |
| `authentication-session-management-vulnerabilities` | Oia |
| `access-control-vulnerabilities` | Oia |
| `deserialization-vulnerabilities` | Oinj |
| `cryptographic-implementation-flaws` | Oscope |
| `review-techniques` | P |
| `code-pattern-analysis` | B (secret grep pattern used as an SMG-01 signal) |
| `data-flow-analysis` | B (procedure guidance in `SKILL.md` step 2) |
| `threat-based-review` | B |
| `business-logic-review` | B |
| `review-checklists` | P |
| `input-validation` | Oinj |
| `authentication-session-management` | Oia |
| `authorization` | Oia |
| `cryptography` | Oscope |
| `business-logic` | SCR-03 (resource limits Orel; workflow, race conditions, business rules Oscope) |
| `configuration-deployment` | SCR-01, SCR-02 (secrets/error/logging pointers S [SMG-01, ERR-02, LOG-12]; headers, TLS Oweb; dependencies Odep) |
| `security-monitoring` | LOG-04, LOG-25 (security events Oia; anomaly detection, alerts, incident response Omon) |
| `tools-and-techniques` | P |
| `code-editors` | B |
| `command-line-pattern-detection` | B |
| `manual-review-focus-areas` | B |
| `automated-tool-integration` | Otest |
| `documentation-templates` | B |
| `integration-with-sdlc` | B |
| `review-timing` | B |
| `baseline-review-integration` | B |
| `diff-based-review-integration` | B |
| `hybrid-approach` | B |
| `team-collaboration` | B |
| `advanced-techniques` | P |
| `race-condition-analysis` | Oscope |
| `business-logic-analysis` | B |
| `security-architecture-review` | B |
| `memory-safety` | Oscope |
| `references` | B |

### .NET Security CS (`dnet`)

| Anchor | Mapped to / reason |
|---|---|
| `introduction` | B |
| `authentication-and-authorization` | Oia |
| `account-protection` | Oia |
| `passwords` | Oia |
| `authentication-cookies` | Oia |
| `authorization` | Oia |
| `redirects` | Oia |
| `input-handling` | Oinj |
| `sql-injection` | Oinj |
| `os-command-injection` | Oinj |
| `cross-site-request-forgery` | Oia |
| `cross-site-scripting-xss` | Oinj |
| `serialization-and-xml` | Oinj |
| `data-protection` | DNO-05 |
| `encryption-for-storage` | DNO-05 (DPAPI scope, `AesGcm` usage F) |
| `encryption-for-transmission` | Oweb |
| `configuration-and-deployment` | DNO-01, DNO-02, DNO-03, DNO-04 (HTTP security headers Oweb; OS isolation N) |
| `legacy-net-framework` | Oinj |
| `aspnet-mvc-and-web-forms` | Oinj |
| `forms-authentication` | Oia |
| `windows-communication-foundation-wcf` | Oweb |
| `references` | B |

### Top 10 A09:2025 (`a09`) and A10:2025 (`a10`)

| Anchor | Mapped to / reason |
|---|---|
| `a09#background` | C |
| `a09#score-table` | C |
| `a09#description` | A09-07, A09-08 (bullets above) |
| `a09#how-to-prevent` | A09-01 … A09-06 (bullets above) |
| `a09#example-attack-scenarios` | C |
| `a09#references` | C |
| `a09#list-of-mapped-cwes` | C |
| `a10#background` | A10-05 |
| `a10#score-table` | C |
| `a10#description` | A10-07 |
| `a10#how-to-prevent` | A10-01, A10-02, A10-03 (bullets above) |
| `a10#example-attack-scenarios` | A10-03, A10-04, A10-06 |
| `a10#references` | C |
| `a10#list-of-mapped-cwes` | A10-04, A10-05, A10-06, A10-07 (CWE-234/235 Oinj; CWE-369/476/478/484 Oscope) |

### Microsoft Learn: error handling, ASP.NET Core 10.0 (`ms-err`)

| Anchor | Mapped to / reason |
|---|---|
| `developer-exception-page` | DNO-06 |
| `exception-handler-page` | DNO-08 |
| `access-the-exception-and-original-routing-details` | DNO-09 |
| `exception-handler-lambda` | DNO-09 |
| `iexceptionhandler` | DNO-08, DNO-10 |
| `configure-useexceptionhandler-when-using-iexceptionhandler` | DNO-08 |
| `suppressdiagnosticscallback` | DNO-10 |
| `usestatuscodepages` | M |
| `usestatuscodepages-with-format-string` | M |
| `usestatuscodepages-with-lambda` | M |
| `usestatuscodepageswithredirects` | M |
| `usestatuscodepageswithreexecute` | M |
| `disable-status-code-pages` | M |
| `exception-handling-code` | M |
| `response-headers` | M |
| `server-exception-handling` | M |
| `startup-exception-handling` | F (`CaptureStartupErrors`/detailed errors) |
| `database-error-page` | D (Development-only by default) |
| `exception-filters` | M |
| `model-state-errors` | M |
| `problem-details` | Oapi |
| `customize-problem-details` | Oapi |
| `customizeproblemdetails-operation` | Oapi |
| `custom-iproblemdetailswriter` | Oapi |
| `problem-details-from-middleware` | Oapi |
| `produce-a-problemdetails-payload-for-exceptions` | Oapi (detail content S [DNO-09]) |
| `related-content` | B |

### Microsoft Learn: runtime environments, ASP.NET Core 10.0 (`ms-env`)

| Anchor | Mapped to / reason |
|---|---|
| `environments` | DNO-07 |
| `logging` | B |
| `environment-variables-that-determine-the-runtime-environment` | DNO-07 |
| `control-code-execution-by-environment` | M |
| `control-rendered-content` | M |
| `set-the-environment-in-a-command-shell-when-the-app-is-run-dotnet-run` | M |
| `set-the-environment-with-the-launch-settings-file-launchsettingsjson` | M |
| `set-the-environment-with-an-environment-variable` | M |
| `azure-app-service` | M |
| `set-environment-variable-for-a-process` | M |
| `set-environment-variable-globally` | M |
| `set-the-environment-for-apps-deployed-to-iis` | M |
| `docker` | M |
| `use-a-dockerfile` | M |
| `use-docker-compose` | M |
| `use-the-docker-run-command` | M |
| `docker-environment-file` | M |
| `set-the-environment-in-the-apps-startup-code` | M |
| `load-configuration-by-environment` | M |
| `access-the-environment-from-a-startup-class` | M |
| `environment-specific-startup-class` | M |
| `environment-specific-startup-class-methods` | M |
| `related-content` | B |

### Microsoft Learn: app secrets in development, ASP.NET Core 10.0 (`ms-sec`)

| Anchor | Mapped to / reason |
|---|---|
| `work-with-environment-variables` | DNO-11 |
| `use-the-secret-manager-tool` | DNO-12 |
| `enable-secret-storage` | M |
| `use-the-cli` | M |
| `use-visual-studio` | M |
| `if-generateassemblyinfo-is-false` | M |
| `set-a-secret` | M |
| `json-structure-flattening-in-visual-studio` | M |
| `set-multiple-secrets` | M |
| `access-a-secret` | M |
| `register-the-user-secrets-configuration-source` | M |
| `read-the-secret-via-the-configuration-api` | M |
| `map-secrets-to-a-poco` | M |
| `use-string-replacement-with-secrets` | S [DNO-01] |
| `list-the-secrets` | M |
| `remove-a-single-secret` | M |
| `remove-all-secrets` | M |
| `manage-user-secrets-with-visual-studio` | M |
| `migrate-user-secrets-from-aspnet-framework-to-aspnet-core` | M |
| `work-with-user-secrets-in-non-web-applications` | M |
| `related-content` | B |

### Microsoft Learn: Azure Key Vault configuration provider, ASP.NET Core 10.0 (`ms-kv`)

| Anchor | Mapped to / reason |
|---|---|
| `packages` | M |
| `sample-app` | M |
| `secret-storage-in-the-development-environment` | S [DNO-02] |
| `secret-storage-in-the-production-environment-with-key-vault` | S [SMG-06] |
| `use-application-id-and-x509-certificate-for-non-azure-hosted-apps` | DNO-13 |
| `use-managed-identities-for-azure-resources` | DNO-13 |
| `configuration-options` | M |
| `use-a-key-name-prefix` | M |
| `bind-an-array-to-a-class` | M |
| `reload-secrets` | S [SMG-10] |
| `disabled-and-expired-secrets` | S [SMG-10] |
| `troubleshoot-configuration-load-issues` | M |
| `related-content` | B |

### Microsoft Learn: HTTP logging, ASP.NET Core 10.0 (`ms-hlog`)

| Anchor | Mapped to / reason |
|---|---|
| `enable-http-logging` | S [DNO-14] |
| `http-logging-options` | P |
| `loggingfields` | DNO-14 |
| `requestheaders-and-responseheaders` | DNO-14 |
| `mediatypeoptions` | M |
| `mediatypeoptions-methods` | M |
| `requestbodyloglimit-and-responsebodyloglimit` | M |
| `combinelogs` | M |
| `endpoint-specific-configuration` | M |
| `ihttplogginginterceptor` | M |
| `logging-configuration-order-of-precedence` | M |
| `redacting-sensitive-data` | S [DNO-15] |
| `logging-redaction-options` | M |
| `requestpathloggingmode` | M |
| `requestpathparameterredactionmode` | M |
| `requestheadersdataclasses` | M |
| `responseheadersdataclasses` | M |
| `routeparameterdataclasses` | M |
| `excludepathstartswith` | M |
| `includeunmatchedroutes` | M |

### Microsoft Learn: logging in .NET (`ms-log`)

| Anchor | Mapped to / reason |
|---|---|
| `get-started` | M |
| `logging-in-a-non-trivial-app` | M |
| `integration-with-hosts-and-dependency-injection` | M |
| `get-an-ilogger-from-di` | M |
| `host-provided-iloggerfactory` | M |
| `create-an-iloggerfactory-with-di` | M |
| `configure-logging` | M |
| `configure-logging-without-code` | M |
| `set-log-level-by-command-line-environment-variables-and-other-configuration` | M |
| `configure-logging-with-code` | M |
| `how-filtering-rules-are-applied` | M |
| `log-category` | M |
| `log-level` | M |
| `log-event-id` | M |
| `log-message-template` | DNO-16 |
| `log-message-template-formatting` | DNO-16 |
| `examples` | M |
| `log-exceptions` | M |
| `default-log-level` | M |
| `filter-function` | M |
| `log-scopes` | M |
| `create-logs-in-main` | M |
| `no-asynchronous-logger-methods` | M |
| `change-log-levels-in-a-running-app` | M (change control is LOG-19) |
| `nuget-packages` | M |
| `see-also` | B |

### Microsoft Learn: data redaction in .NET (`ms-red`)

| Anchor | Mapped to / reason |
|---|---|
| `install-redaction-package` | M |
| `available-redactors` | M |
| `usage-example` | M |
| `configure-a-redactor` | M |
| `configure-the-hmac-redactor` | M |
| `configure-a-custom-redactor` | M |
| `create-a-custom-redactor-provider` | M |
| `logging-sensitive-information` | DNO-15 |
| `steps-for-logging-sensitive-data` | M |
| `example-redacting-data-in-logs` | M |

### Spring Boot 4.1: pinned sections (`sb-web`, `sb-act`, `sb-props`, `sb-cfg`, `sb-log`)

| Anchor | Mapped to / reason |
|---|---|
| `sb-web#web.servlet.spring-mvc.error-handling` | JVO-01 |
| `sb-web#web.servlet.spring-mvc.error-handling.error-pages` | M |
| `sb-web#web.servlet.spring-mvc.error-handling.error-pages-without-spring-mvc` | M |
| `sb-web#web.servlet.spring-mvc.error-handling.in-a-war-deployment` | M |
| `sb-act#actuator.endpoints.exposing` | JVO-02 |
| `sb-act#actuator.endpoints.security` | JVO-02 (endpoint authorization Oia) |
| `sb-act#actuator.endpoints.security.csrf` | Oia |
| `sb-act#actuator.endpoints.sanitization` | JVO-03 |
| `sb-props#application-properties.web.spring.web.error.include-stacktrace` | JVO-01 |
| `sb-props#application-properties.web.spring.web.error.include-message` | S [JVO-01] |
| `sb-props#application-properties.web.spring.web.error.include-exception` | S [JVO-01] |
| `sb-props#application-properties.web.spring.web.error.include-binding-errors` | S [JVO-01] |
| `sb-props#application-properties.actuator.management.endpoint.env.show-values` | JVO-03 |
| `sb-props#application-properties.actuator.management.endpoint.configprops.show-values` | S [JVO-03] |
| `sb-cfg#features.external-config.files.configtree` | JVO-04 |
| `sb-cfg#features.external-config.encrypting` | JVO-04 |
| `sb-log#features.logging.file-output` | JVO-05 |
| `sb-log#features.logging.file-rotation` | JVO-05 |
| `sb-log#features.logging.structured` | JVO-06 |
| `sb-log#features.logging.structured.ecs` | M |
| `sb-log#features.logging.structured.gelf` | M |
| `sb-log#features.logging.structured.logstash` | M |
| `sb-log#features.logging.structured.customizing-json` | M |
| `sb-log#features.logging.structured.customizing-stack-traces` | M |
| `sb-log#features.logging.structured.other-formats` | M |

### Django 6.1: pinned pages (`dj-set`, `dj-dep`, `dj-err`, `dj-log`, `dj-rlog`)

| Anchor | Mapped to / reason |
|---|---|
| `dj-set#debug` | PYO-01 |
| `dj-dep#deployment-checklist` | P |
| `dj-dep#run-manage-py-check-deploy` | B |
| `dj-dep#switch-away-from-manage-py-runserver` | M |
| `dj-dep#critical-settings` | P |
| `dj-dep#secret-key` | PYO-02 |
| `dj-dep#debug` | PYO-01 |
| `dj-dep#environment-specific-settings` | S [SCR-02] |
| `dj-dep#allowed-hosts` | Oweb |
| `dj-dep#caches` | M |
| `dj-dep#databases` | S [SMG-01] (password storage); otherwise M |
| `dj-dep#mailers-and-related-settings` | M |
| `dj-dep#static-root-and-static-url` | M |
| `dj-dep#media-root-and-media-url` | Oinj |
| `dj-dep#https` | Oweb |
| `dj-dep#csrf-cookie-secure` | Oia |
| `dj-dep#session-cookie-secure` | Oia |
| `dj-dep#performance-optimizations` | M |
| `dj-dep#sessions` | Oia |
| `dj-dep#conn-max-age` | M |
| `dj-dep#templates` | M |
| `dj-dep#error-reporting` | P |
| `dj-dep#logging` | PYO-05 |
| `dj-dep#admins-and-managers` | S [PYO-05] |
| `dj-dep#customize-the-default-error-views` | M |
| `dj-err#how-to-manage-error-reporting` | P |
| `dj-err#email-reports` | M |
| `dj-err#server-errors` | M |
| `dj-err#errors` | M |
| `dj-err#id1` | M |
| `dj-err#id2` | M |
| `dj-err#filtering-error-reports` | PYO-04 |
| `dj-err#filtering-sensitive-information` | PYO-03 |
| `dj-err#custom-error-reports` | M |
| `dj-log#logging` | P |
| `dj-log#overview` | B |
| `dj-log#the-cast-of-players` | B |
| `dj-log#loggers` | M |
| `dj-log#topic-logging-parts-loggers` | M |
| `dj-log#handlers` | M |
| `dj-log#topic-logging-parts-handlers` | M |
| `dj-log#filters` | M |
| `dj-log#topic-logging-parts-filters` | M |
| `dj-log#formatters` | M |
| `dj-log#topic-logging-parts-formatters` | M |
| `dj-log#security-implications` | PYO-03 |
| `dj-log#logging-security-implications` | S [PYO-03] |
| `dj-log#adminemailhandler` | PYO-04 |
| `dj-log#configuring-logging` | M |
| `dj-log#examples` | M |
| `dj-log#custom-logging-configuration` | M |
| `dj-log#disabling-logging-configuration` | M |
| `dj-log#logging-explanation` | B |
| `dj-log#id1` | M |
| `dj-log#id2` | M |
| `dj-rlog#default-logging-configuration` | PYO-05 |
| `dj-rlog#django-s-default-logging-configuration` | S [PYO-05] |
| `dj-rlog#default-logging-conditions` | S [PYO-05] |
| `dj-rlog#default-logging-definition` | S [PYO-05] |

### Python 3.15: pinned pages (`py-cfg`, `py-how`)

| Anchor | Mapped to / reason |
|---|---|
| `py-cfg#module-logging.config` | P |
| `py-cfg#configuration-functions` | M |
| `py-cfg#logging.config.listen` | PYO-07 |
| `py-cfg#security-considerations` | PYO-06 |
| `py-cfg#logging-eval-security` | S [PYO-07] |
| `py-cfg#configuration-dictionary-schema` | M |
| `py-cfg#dictionary-schema-details` | M |
| `py-cfg#incremental-configuration` | M |
| `py-cfg#object-connections` | M |
| `py-cfg#user-defined-objects` | S [PYO-06] |
| `py-cfg#handler-configuration-order` | M |
| `py-cfg#access-to-external-objects` | S [PYO-06] |
| `py-cfg#access-to-internal-objects` | M |
| `py-cfg#import-resolution-and-custom-importers` | M |
| `py-cfg#configuring-queuehandler-and-queuelistener` | M |
| `py-cfg#configuration-file-format` | M |
| `py-how#logging-howto` | P |
| `py-how#basic-logging-tutorial` | M |
| `py-how#when-to-use-logging` | M |
| `py-how#a-simple-example` | M |
| `py-how#logging-to-a-file` | M |
| `py-how#logging-variable-data` | PYO-09 |
| `py-how#changing-the-format-of-displayed-messages` | M |
| `py-how#displaying-the-date-time-in-messages` | M |
| `py-how#next-steps` | M |
| `py-how#advanced-logging-tutorial` | M |
| `py-how#logging-flow` | M |
| `py-how#loggers` | M |
| `py-how#handlers` | M |
| `py-how#formatters` | M |
| `py-how#configuring-logging` | M |
| `py-how#what-happens-if-no-configuration-is-provided` | M |
| `py-how#configuring-logging-for-a-library` | M |
| `py-how#logging-levels` | M |
| `py-how#custom-levels` | M |
| `py-how#useful-handlers` | M |
| `py-how#exceptions-raised-during-logging` | PYO-08 |
| `py-how#using-arbitrary-objects-as-messages` | M |
| `py-how#optimization` | M |
| `py-how#other-resources` | B |
