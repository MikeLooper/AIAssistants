# Checklist — Security: Operational

Each check is evaluated through the elements it lists; every element belongs to exactly one check. Element
definitions, anchors and citation bases are in `standards/`. Severity rules (SHOULD elements one level lower; the
always-Error list) are in `../SKILL.md`.

| id | Check | Default severity | Elements | Source |
|----|-------|------------------|----------|--------|
| SEC-OP-01 | Unexpected errors are caught by a global handler and clients get a generic response: no stack traces, exception messages, SQL errors, paths or version details | Warning | ERR-01, ERR-02, ERR-05, ERR-06, DNO-04, DNO-08, DNO-09, JVO-01, A10-01, A10-04, NDO-03 | ERR, DNO, JVO, A10, NDO |
| SEC-OP-02 | Errors are logged server-side with enough context to diagnose; none are silently swallowed or left unchecked | Warning | ERR-03, LOG-02, DNO-10, PYO-05, A09-08, A10-07, NDO-02 | ERR, LOG, DNO, PYO, A09, A10, NDO |
| SEC-OP-03 | Logs and error reports don't contain secrets (passwords, tokens, session IDs, keys, connection strings) or sensitive personal or payment data; other personal data is minimized | Error | LOG-12, LOG-13, LOG-14, DNO-14, DNO-15, PYO-03, PYO-04, A09-07 | LOG, DNO, PYO, A09 |
| SEC-OP-04 | Untrusted data written to logs can't forge or corrupt entries: constant templates with parameters, CR/LF/delimiter neutralization or structured encoding, output-safe encoding | Warning | LOG-15, LOG-16, LOG-17, LOG-18, DNO-16, JVO-06, PYO-09, A09-04 | LOG, DNO, JVO, PYO, A09 |
| SEC-OP-05 | No hardcoded secrets in source, configuration, container definitions or manifests in the repository files | Error | SMG-01, SMG-02, SMG-03, SMG-04, SMG-05, DNO-01, PYO-02 | SMG, DNO, PYO |
| SEC-OP-06 | Secrets are delivered at runtime from a secret manager or platform injection with least-privilege, environment-separated access, never in plaintext transit; development-only stores aren't used in production | Error | SMG-06…12, DNO-02, DNO-05, DNO-11, DNO-12, DNO-13, JVO-04 | SMG, DNO, JVO |
| SEC-OP-07 | Production configuration uses secure defaults: debug/developer modes, detailed error pages and diagnostic endpoints are off or restricted outside development, and environments are separated | Warning | ERR-04, SCR-01, SCR-02, ORS-01, DNO-03, DNO-06, DNO-07, JVO-02, JVO-03, PYO-01, NDO-05 | ERR, SCR, ORS, DNO, JVO, PYO, NDO |
| SEC-OP-08 | Security-relevant events (validation failures, high-risk functions, startup/shutdown, deserialization and connection failures, suspicious business activity) are logged through the logging framework with when/where/who/what | Warning | LOG-01, LOG-03…11, A09-01, A09-02, A09-03, NDO-04 | LOG, A09, NDO |
| SEC-OP-09 | Logs and the logging mechanism are protected and resilient: not web-accessible, restricted and tamper-resistant, securely transported, bounded in size, not fully disableable, and logging failures or configuration loading can't break or compromise the app | Warning | LOG-19…26, JVO-05, PYO-06, PYO-07, PYO-08, A09-05 | LOG, JVO, PYO, A09 |
| SEC-OP-10 | Exceptional conditions fail safe: errors are handled where they occur, security decisions fail closed, part-way transactions roll back and resources are released on exception paths | Warning | A10-02, A10-03, A10-05, A10-06, A09-06, SCR-03, NDO-01 | A10, A09, SCR, NDO |

Totals: 48 OWASP cheat-sheet + 15 Top 10 + 16 DNO + 6 JVO + 9 PYO + 5 NDO = 99 elements across 10 checks.

## Evidence notes

- **SEC-OP-01 / SEC-OP-07:** fail on code or configuration that returns exception messages, stack traces, SQL errors
  or paths to clients, or that enables detailed error output for production. Configuration gated on a development
  environment or profile passes.
- **SEC-OP-07 (ORS-01):** fail only when the files show management or diagnostic endpoints (Actuator, admin, metrics,
  debug routes) served on the public listener with no separate port or host and no network restriction (ingress
  allowlist, firewall rule, bind address) in the files in scope; confidence `low` when the deployment network isn't in
  scope. Their authorization stays with identity-access.
- **SEC-OP-02:** fail on catch blocks that neither log, rethrow nor translate the exception (empty or comment-only
  catch, bare `except: pass`), or on a handler that marks an exception handled without logging where a localized
  default says nothing else logs it (DNO-10, PYO-05).
- **SEC-OP-03:** fail when a log call or logging configuration writes a value that is a secret or sensitive personal
  data (variables or properties named like password/secret/token/apiKey/connectionString/cardNumber,
  `Authorization`/`Cookie` headers, whole request or entity objects known to contain them), or enables body/header
  logging of such data.
- **SEC-OP-05:** fail on literal credential values in source or configuration files in the repository: keys named like
  password/secret/api_key/token/connectionString with a non-placeholder value; private-key blocks; recognizable cloud
  key formats; `.env` files with values present in the repository; plain Kubernetes `Secret` manifests with data. Placeholders (`${…}`,
  `<secret>`, `changeme`-style samples clearly marked as such), password-less local development connection strings and
  files outside the subject's list don't fail. Use confidence `medium` unless the value is unambiguous.
- **SEC-OP-06:** secrets injected as environment variables by the platform or orchestrator at deploy time pass.
  SMG-07 and DNO-11 never fail on their own; name them in recommendations only. Environment-variable values hardcoded
  in container or compose definitions in the repository fail SMG-02 (SEC-OP-05).
- **SEC-OP-08:** fail only when the subject's files contain the security-relevant operation itself (e.g. a
  user-administration endpoint, a data export, a deserializer, a startup routine) and no logging call covers it, or
  when security-relevant code writes events with `print`/`Console.WriteLine`/`System.out` instead of the logging
  framework. Authentication, authorization and session-failure logging is not evaluated here.
- **SEC-OP-09:** evaluate only what application code and configuration show (log paths, file appenders,
  rotation/size settings, log endpoints, transport URLs, logging-config loading). Log storage access control in IaC
  belongs to `review-monitoring`.
- **SEC-OP-10:** fail on catch blocks in authorization, authentication, validation or limit checks that allow or
  continue (fail open); multi-step writes without a transaction or rollback on exception; streams, connections or
  locks not released on exception paths (no `using`/try-with-resources/`with`/`finally`).
