# OWASP operational security guidance — localized summary

- Sources: cheatsheetseries.owasp.org @ OWASP/CheatSheetSeries (per-sheet commits below);
  top10.owasp.org (A09:2025 @ OWASP/Top10 d4d000ec89ef2b2eb87de0eb7dcfa8c05f8dd966, 2025-12-24;
  A10:2025 @ OWASP/Top10 494be56d88168940f1f3392961f71fe2cc414e6a, 2026-01-06)
- Localized: 2026-11-08 · Elements: cheatsheetseries.owasp.org 48 here (ORS-01 added 2026-11-09) + 5 in `dotnet-operational.md` = 53 (cap 100);
  top10.owasp.org 15 (cap 100)
- Level: `MUST` where the source says must/must not/never/do not/ensure, gives an unqualified imperative, or names a
  prohibited practice; items of the Logging sheet's "Where possible, always log" list are `MUST`. `SHOULD` for
  recommendations (should/recommended/prefer/consider/"if available"). Secure Code Review checklist items are `MUST`.
  Top 10 elements: `MUST` for "How to prevent" bullets, `REVIEW` for "Description" weaknesses and mapped CWEs (`REVIEW`
  is treated like `MUST`). Severity rules are in `../../SKILL.md`.
- Untrusted data: anything the application didn't create — request parameters, bodies, headers, cookies, file names,
  queue messages, partner feeds and data from other trust zones.
- Language-agnostic files (`Dockerfile`, compose files, Kubernetes manifests, Helm values, pipeline YAML) have no
  language id. Evaluate them with the SMG and LOG elements below whenever they are in the subject's file list.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.
- Citation preference: vendor element (DNO/JVO/PYO) → cheat-sheet element (ERR/LOG/SMG/SCR) → A09/A10 element (cite
  A09/A10 only when nothing more specific fits; otherwise name the Top 10 ID in the recommendation).

| Key | Citation base | Pinned commit | Source name for `Finding.standard` |
|-----|---------------|---------------|------------------------------------|
| err | https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html | 796eed7d (2026-10-04) | OWASP Error Handling Cheat Sheet |
| log | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | f1d0311a (2026-10-22) | OWASP Logging Cheat Sheet |
| smg | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | d6474de0 (2026-11-08) | OWASP Secrets Management Cheat Sheet |
| scr | https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html | a11444a5 (2026-10-04) | OWASP Secure Code Review Cheat Sheet |
| rest | https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html | 97cb8a3c (2026-10-14) | OWASP REST Security Cheat Sheet |
| a09 | https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures/ | d4d000ec (2025-12-24) | OWASP Top 10:2025 A09 |
| a10 | https://top10.owasp.org/2025/A10_2025-Mishandling_of_Exceptional_Conditions/ | 494be56d (2026-01-06) | OWASP Top 10:2025 A10 |

## Error Handling Cheat Sheet (ERR)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| ERR-01 | MUST | Configure a global error handler (runtime configuration or code) so every unexpected error is caught centrally. | no `UseExceptionHandler`, `@RestControllerAdvice`/`<error-page>`, `handler500`; per-action try/catch only | SEC-OP-01 | err#objective, err#proposition |
| ERR-02 | MUST | On unexpected errors return a generic response; no stack trace, exception message, framework/server version, SQL error or file path in the body or headers. | `ex.ToString()`/`e.getMessage()`/`str(e)`/`traceback` in responses | SEC-OP-01 | err#objective, err#context |
| ERR-03 | MUST | Log the error details server-side for investigation in the handler, instead of returning them. | handler builds a response but never logs the exception | SEC-OP-02 | err#objective |
| ERR-04 | MUST | Detailed or developer error pages are enabled only for development; other environments use the generic handler (`customErrors` `RemoteOnly`/`On`, never `Off`). | `UseDeveloperExceptionPage()` ungated; `customErrors mode="Off"` | SEC-OP-07 | err#asp-net-core-web-application, err#asp-net-web-api-web-application |
| ERR-05 | MUST | Java web apps declare a catch-all `<error-page>` for `java.lang.Exception`/`Throwable`, or a Spring `@RestControllerAdvice` with `@ExceptionHandler(Exception.class)`, returning a generic body. | no catch-all error page or advice | SEC-OP-01 | err#standard-java-web-application, err#java-springmvcspringboot-web-application |
| ERR-06 | MUST | ASP.NET Web API (.NET Framework) registers a global `IExceptionLogger` and `IExceptionHandler` that returns a generic response. | `WebApiConfig` without both services replaced | SEC-OP-01 | err#asp-net-web-api-web-application |

## Logging Cheat Sheet (LOG)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| LOG-01 | MUST | Log input validation failures (protocol violations, bad encodings, invalid parameter names/values, values outside a discrete list) and output validation failures. | validation rejects requests with no log call | SEC-OP-08 | log#which-events-to-log |
| LOG-02 | MUST | Log application errors and system events: runtime errors, connectivity problems, third-party service errors, file system errors, upload virus detection, configuration changes. | catch of I/O/HTTP-client errors without logging | SEC-OP-02 | log#which-events-to-log |
| LOG-03 | MUST | Log application start-up and shut-down, and logging initialization (start, stop, pause). | no startup/shutdown log in host code | SEC-OP-08 | log#which-events-to-log |
| LOG-04 | MUST | Log use of higher-risk functionality: user administration and privilege changes, administrator actions, default/shared/break-glass accounts, sensitive-data access, key use/rotation, data import/export, uploads. | admin/user-management/export endpoints with no logging | SEC-OP-08 | log#which-events-to-log, scr#security-monitoring |
| LOG-05 | MUST | Log deserialization failures, network connection failures (including backend TLS and certificate-validation failures) and requests with unexpected HTTP verbs. | swallowed deserialization/TLS exceptions | SEC-OP-08 | log#which-events-to-log |
| LOG-06 | MUST | Log legal and other opt-ins: consent to personal-data use, terms of use, marketing permissions. | consent endpoints with no event logged | SEC-OP-08 | log#which-events-to-log |
| LOG-07 | MUST | Log suspicious business-logic activity: out-of-order steps, actions that make no business sense, attempts to exceed limits. | limit/state checks reject silently | SEC-OP-08 | log#which-events-to-log |
| LOG-08 | MUST | Each security event records when (timestamp, international format), where (app/version, host, service, entry point and method, code location), who (source address, user identity) and what (type, severity, description). | security log calls with message text only | SEC-OP-08 | log#event-attributes |
| LOG-09 | SHOULD | Security events also record action, object, result status and reason (and HTTP status for web apps). | "failed" with no object or reason | SEC-OP-08 | log#event-attributes |
| LOG-10 | MUST | Never exclude events from "known" users or systems (internal services, monitors, testers); flag them instead. | log filters that skip internal IPs or service accounts | SEC-OP-08 | log#data-to-exclude |
| LOG-11 | MUST | Use the framework's logging mechanism or one application-wide log handler for security events, not ad-hoc writes. | `print`, `Console.WriteLine`, `System.out` for security events | SEC-OP-08 | log#event-collection |
| LOG-12 | MUST | Don't log session IDs (hash if needed), access tokens, authentication passwords, database connection strings, encryption keys or other primary secrets; remove, mask, hash or encrypt them. | token/password/connection-string values in log arguments; whole request/header objects logged | SEC-OP-03 | log#data-to-exclude, smg#83-detection-lifecycle, log#confidentiality |
| LOG-13 | MUST | Don't log sensitive personal data (health, government IDs), bank or card-holder data, application source code, commercially sensitive data, data above the log store's classification, or data the user didn't consent to. | logging full user/payment entities | SEC-OP-03 | log#data-to-exclude |
| LOG-14 | SHOULD | Treat file paths, internal network names and addresses, and non-sensitive personal data (names, phone numbers, emails) specially: mask, pseudonymize or omit where identity isn't needed. | emails/phone numbers logged on every request | SEC-OP-03 | log#data-to-exclude |
| LOG-15 | MUST | Treat event data from other trust zones as untrusted: validate it before logging; omit or safely replace malformed fields and record the failure, without discarding the event. | partner/queue payloads logged raw | SEC-OP-04 | log#event-collection, log#event-data-sources |
| LOG-16 | MUST | Neutralize log injection: strip or encode CR, LF and delimiter characters in untrusted data, or write values through a structured (e.g. JSON) encoder that escapes them. | user input in text-format logs with no CR/LF handling | SEC-OP-04 | log#log-injection, log#event-collection |
| LOG-17 | MUST | Keep message templates constant and pass untrusted values as parameters; never concatenate them into the template (parameterization alone doesn't stop CR/LF). | `logger.warn("user " + name + " {}", x)`; interpolated templates | SEC-OP-04 | log#log-injection-in-java |
| LOG-18 | MUST | Encode logged data correctly for the log's output format (e.g. safe for HTML log viewers). | logs rendered in a web UI without encoding | SEC-OP-04 | log#event-collection |
| LOG-19 | MUST | The default log level gives enough detail; application logging, and logging of compliance-required events, can't be fully deactivated; level changes follow approved configuration or change control. | production `LogLevel: None`/`OFF` for app or security loggers; runtime toggles without control | SEC-OP-09 | log#customizable-logging |
| LOG-20 | MUST | Failures in logging don't stop the application or leak information. | logging calls that can throw into request handling | SEC-OP-09 | log#event-collection, log#verification |
| LOG-21 | MUST | Logging can't be used to exhaust resources: bound the size of user input in log messages and cap file growth (rotation, size, history). | file appenders without rotation/size caps; unbounded user strings logged | SEC-OP-09 | log#verification, log#log-injection, log#availability |
| LOG-22 | SHOULD | Logs aren't stored in web-accessible locations; if unavoidable, access is restricted and they're served as plain text. | log path under `wwwroot`/`static`/`public`; log-file endpoints | SEC-OP-09 | log#where-to-record-event-data |
| LOG-23 | SHOULD | File logs use strict directory and file permissions (ideally a separate partition); database logging uses a separate, write-only account. | world-writable log dirs (`chmod 777`); app DB account used for logs | SEC-OP-09 | log#where-to-record-event-data |
| LOG-24 | MUST | Log data sent over untrusted networks uses a secure transport. | `udp://` syslog, `http://` log collector endpoints | SEC-OP-09 | log#protection, log#where-to-record-event-data |
| LOG-25 | MUST | Logs are protected from tampering and unauthorized access, modification and deletion; read access is restricted. | app endpoints that read, edit or delete logs without authorization | SEC-OP-09 | log#protection, scr#security-monitoring |
| LOG-26 | SHOULD | Build in tamper detection and copy logs to read-only storage as soon as possible. | audit logs in mutable app tables only | SEC-OP-09 | log#protection |

## Secrets Management Cheat Sheet (SMG)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| SMG-01 | MUST | No hardcoded secrets in plaintext in source, configuration files or configuration-management tooling: API keys, database credentials, private keys, certificates, tokens. | literal credentials; committed `.env` with values; PEM blocks; start from `password\s*=\|api_key\s*=\|secret\s*=` | SEC-OP-05 | smg#1-introduction, smg#82-types-of-secrets-to-be-detected |
| SMG-02 | MUST | Secrets aren't built into container images: no secrets in Dockerfile `ENV`/`ARG` or copied secret files; the orchestrator mounts or injects them at runtime. | `ENV DB_PASSWORD=…`; `ARG API_KEY=…`; `COPY secrets.json`; literal values in compose `environment:` | SEC-OP-05 | smg#51-injection-of-secrets-file-in-memory, smg#5-containers-orchestrators |
| SMG-03 | SHOULD | Encryption keys aren't stored next to the secrets they encrypt, unless they are themselves encrypted (envelope encryption). | encrypted config value and its key in the same file | SEC-OP-05 | smg#73-where-to-store-the-encryption-keys |
| SMG-04 | SHOULD | Secrets committed to Git (GitOps) are asymmetrically encrypted with environment-specific keys (e.g. Sealed Secrets). | plain Kubernetes `kind: Secret` manifests with `data`/`stringData` | SEC-OP-05 | smg#36-pipeline-created-secrets |
| SMG-05 | SHOULD | Secret detection runs before commit or PR (pre-commit hook, IDE or CI scanner). | no secret scanner in hook/CI files in scope | SEC-OP-05 | smg#81-general-detection-approaches |
| SMG-06 | SHOULD | Use a designated secrets manager, not a general-purpose configuration store; ideally the deployed service fetches its own secrets at runtime with its platform identity, so secrets don't pass through CI/CD. | secrets in parameter/config stores; pipeline writes secrets into config | SEC-OP-06 | smg#41-choosing-a-secret-management-service, smg#323-not-touched-by-cicd-at-all |
| SMG-07 | SHOULD | Environment variables carry secrets only when file mounts or in-memory fetch aren't possible, and are set by the orchestrator, never hardcoded. **Advisory only; never fails on its own.** | — (recommendation text) | SEC-OP-06 | smg#51-injection-of-secrets-file-in-memory |
| SMG-08 | SHOULD | Production and development secrets are separate, ideally in separate secret stores with reduced access to production. | same secret values in dev and prod config | SEC-OP-06 | smg#63-ensure-limitations-are-in-place |
| SMG-09 | SHOULD | Access to secrets is least-privilege and scoped per application and environment; no account-wide access; no secrets shared across services. | one credential reused by several services; wildcard secret permissions | SEC-OP-06 | smg#23-access-control, smg#43-identity-and-access-management-iam |
| SMG-10 | SHOULD | Prefer dynamic, short-lived credentials or workload identity; static secrets support rotation, expiry and revocation, and the app verifies a secret is still active. | long-lived keys where managed identity exists; secrets read once and cached forever | SEC-OP-06 | smg#24-automate-secrets-management, smg#272-rotation, smg#274-expiration, smg#273-revocation |
| SMG-11 | MUST | Never transmit secrets in plaintext; secret-store and credential exchanges use TLS. | `http://` vault address; TLS verification disabled for the secret store | SEC-OP-06 | smg#28-transport-layer-security-tls-everywhere |
| SMG-12 | SHOULD | CI/CD tooling holds no high-value, long-lived secrets; pipelines authenticate with OIDC/workload identity federation and short-lived, least-privilege credentials. | static cloud keys in pipeline variables or YAML | SEC-OP-06 | smg#321-as-part-of-your-cicd-tooling, smg#322-storing-it-in-a-secrets-management-system, smg#33-authentication-and-authorization-of-cicd-tooling |

## Secure Code Review Cheat Sheet (SCR)

The review method (scr#review-process, scr#data-flow-analysis) is procedure guidance in `../../SKILL.md`, not scored.

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| SCR-01 | MUST | Secure defaults: shipped and default configuration is security-focused (debug off, diagnostics off, least exposure). | production config inherits development settings | SEC-OP-07 | scr#configuration-deployment |
| SCR-02 | MUST | Environment separation: configuration and settings are isolated per environment; development settings aren't deployed to production. | single settings file with dev values; dev profile active by default | SEC-OP-07 | scr#configuration-deployment |
| SCR-03 | MUST | Transaction atomicity: multi-step operations have proper rollback and consistency mechanisms. | multi-write operations without a transaction | SEC-OP-10 | scr#business-logic |

## REST Security Cheat Sheet — management endpoints (ORS)

Prefix `ORS-` (operational REST) keeps these IDs apart from `review-security-web-api`'s `RST-` elements, which cite
other sections of the same sheet under that skill's budget.

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| ORS-01 | MUST | Management and diagnostic endpoints aren't exposed to the internet: they listen on a separate port or host (preferably a restricted network) or are restricted by firewall rules or access lists; if they must be internet-facing, they require strong (multi-factor) authentication. | Actuator/admin/metrics endpoints on the public listener with no `management.server.port`/address, ingress or IP restriction in the files | SEC-OP-07 | rest#management-endpoints |

## OWASP Top 10:2025 A09 Security Logging & Alerting Failures (A09)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| A09-01 | MUST | Login, access-control and server-side input validation failures can be logged with enough user context, and kept long enough for forensics. (Login/access-control logging is judged by identity-access.) | — | SEC-OP-08 | a09#how-to-prevent |
| A09-02 | MUST | Every part of the app that contains a security control is logged, whether it succeeds or fails. | — | SEC-OP-08 | a09#how-to-prevent |
| A09-03 | MUST | Logs are generated in a format that log-management solutions can consume. | — | SEC-OP-08 | a09#how-to-prevent |
| A09-04 | MUST | Log data is encoded correctly to prevent injection into logging or monitoring systems. | — | SEC-OP-04 | a09#how-to-prevent |
| A09-05 | MUST | Transactions have an audit trail with integrity controls against tampering or deletion (append-only tables or similar). | — | SEC-OP-09 | a09#how-to-prevent |
| A09-06 | MUST | Transactions that throw an error are rolled back and started over; always fail closed. | — | SEC-OP-10 | a09#how-to-prevent |
| A09-07 | REVIEW | Sensitive information (PII, PHI) is logged, or logging/alerting events are visible to users. | — | SEC-OP-03 | a09#description |
| A09-08 | REVIEW | Warnings and errors produce no, inadequate or unclear log messages, or errors are mishandled so the system is unaware of them. | — | SEC-OP-02 | a09#description |

## OWASP Top 10:2025 A10 Mishandling of Exceptional Conditions (A10)

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| A10-01 | MUST | A global exception handler catches anything missed; exceptional conditions are handled in one place, the same way each time. | — | SEC-OP-01 | a10#how-to-prevent |
| A10-02 | MUST | Catch errors where they occur and handle them meaningfully: inform the user understandably, log the event, alert if justified. | — | SEC-OP-10 | a10#how-to-prevent |
| A10-03 | MUST | Roll back every part of a part-way transaction and start again (fail closed); don't try to recover mid-transaction. | — | SEC-OP-10 | a10#how-to-prevent, a10#example-attack-scenarios |
| A10-04 | REVIEW | Error messages or debug code expose sensitive information (CWE-209, CWE-215, CWE-550). | — | SEC-OP-01 | a10#list-of-mapped-cwes, a10#example-attack-scenarios |
| A10-05 | REVIEW | The application fails open (CWE-636) or mishandles insufficient privileges (CWE-274, CWE-280). | — | SEC-OP-10 | a10#background, a10#list-of-mapped-cwes |
| A10-06 | REVIEW | Resources aren't cleaned up when an exception is thrown (CWE-460), e.g. locked after failed uploads. | — | SEC-OP-10 | a10#example-attack-scenarios, a10#list-of-mapped-cwes |
| A10-07 | REVIEW | Errors are detected without action, return values or error conditions go unchecked, or generic catches hide failures (CWE-252, CWE-390, CWE-391, CWE-396). | — | SEC-OP-02 | a10#list-of-mapped-cwes, a10#description |
