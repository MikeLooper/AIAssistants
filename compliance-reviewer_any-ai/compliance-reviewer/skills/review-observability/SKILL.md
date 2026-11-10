---
name: review-observability
description: 'Reviews structured logging, trace-context propagation, distributed tracing, metrics, telemetry export and identity, error recording and telemetry safety in code, plus health check endpoints and SLO/SLI documentation, against OpenTelemetry and the Azure Well-Architected Framework. Use when the compliance-reviewer orchestrator delegates the Observability subject.'
user-invocable: false
---

# Review: Observability

Assesses the telemetry that application code and app configuration emit (logs, traces, metrics, resource identity,
error recording), the health endpoints the app exposes, and SLO/SLI documentation. It uses local, pinned summaries
of OpenTelemetry and the Azure Well-Architected Framework. Alert rules, dashboards, external probes and telemetry
routing in IaC are reviewed by `review-monitoring`.

## Inputs

Logging, tracing and metrics setup, OpenTelemetry or APM SDK configuration and agent settings, exception handling
middleware, health check endpoints and probe manifests, SLO docs, per `compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/opentelemetry-observability.md` — OTO-01…OTO-46. Always load.
- `references/standards/azure-well-architected-observability.md` — WAFO-01…WAFO-37. Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, both standards files, and
   `references/languages/<id>.md` for each detected language.
2. Service type: classify the target (web/API service, worker/consumer, library, CLI/batch, front-end only). OBS-06
   applies only to long-running deployable services. Cross-service parts of OBS-02/OBS-03 apply only when the code
   calls or receives calls from other services, databases or brokers. For a library, judge only OTO-13, OTO-15 and
   the absence of SDK/exporter setup, and mark OBS-05 N/A.
3. Instrumentation mode (language file signals): zero-code agent, code-based SDK, vendor APM SDK, or none.
   Zero-code configured for the service passes framework tracing and HTTP metrics (OTO-14, OTO-23); custom spans and
   business metrics (OTO-16, WAFO-08) are still judged on code. A vendor SDK is "equivalent" for OBS-03…OBS-05; skip
   OpenTelemetry naming elements (OTO-18…OTO-21, OTO-31…OTO-36) unless it uses OpenTelemetry conventions, with reason
   "vendor SDK; OpenTelemetry naming not applicable".
4. For each check (OBS-01…OBS-10), evaluate only the elements it lists whose "Applies when" condition holds. If none
   apply, mark the check N/A with that reason.
5. Development-status elements (Stab. `D`): apply when the repo already uses that convention; otherwise report only
   as confidence `low`.
6. Boundaries: don't report alert rules, dashboards, external probes, probe thresholds or telemetry retention
   (review-monitoring); routing and restart probe configuration (review-reliability AZRL-49/50); secrets/PII in log messages, log injection or security-event logging (security skills; if
   both could fire on the same line, don't report it here); API header documentation (review-api-design).
   OBS-10 covers only telemetry attributes, baggage and captured headers/bodies. OBS-07 is the only place a missing
   SLO is reported.
7. OBS-06: the endpoint must exist and be wired to the host's probe mechanism when manifests are in scope. A
   constant-200 handler passes WAFO-14 but fails WAFO-16 when the service has critical dependencies (confidence
   `medium`). A liveness check must not call dependencies (WAFO-32); readiness must cover required dependencies only
   and return non-2xx on failure (WAFO-33). A single combined endpoint passes WAFO-34 when only one probe consumer is
   configured and startup is fast. Detailed diagnostics on an anonymous health route fail WAFO-37.
   OBS-07: SLOs count as documented when a target and its SLI are stated (README/docs, ADRs, OpenSLO/Sloth specs,
   SLO resources in IaC). A target without an SLI (e.g. only an SLA figure) fails with confidence `low` ("target
   without SLI"). Never fail OBS-07 for a library or CLI.
8. Evidence rule: fail only on concrete evidence in the files (e.g. an interpolated log message, an uninstrumented
   HTTP client in an instrumented app, a span with no end path, a metric attribute from a user ID, a console-only
   exporter in production config). Use confidence `medium` unless unambiguous; absence-only failures use `high` only
   if the language file's signals were searched across the whole file list.
9. Severity: every Finding takes the check's default severity from `checklist.md` regardless of element level;
   `checkResults.severityIfFailed` is always that default.
10. Citations: `standard` = "<source name> — <element ID>" (source name from the standards file header);
    `url` = citation base + page path + "#" + primary anchor (first listed; `pat-hem` uses its full path from
    https://learn.microsoft.com/). `urlsFetched` stays empty.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
