# Maintenance — Observability localized standards

**Maintainers only. Workers never load this file.** Background and design decisions: `docs/plan_localize-review-observability.md`.

Cross-skill strategy, cadence overview and AI-tool usage: `compliance-reviewer/STANDARDS-MAINTENANCE.md`.

## Element budget per website

The cap is counted per skill per website (plan DEC-1).

| Website | Local file | Elements | Cap | Note |
|---|---|---|---|---|
| opentelemetry.io | opentelemetry-observability.md | 46 | 100 | 22 pages (concepts, SDK config, Collector, security, 8 semconv pages, Logs Data Model); `concepts/semantic-conventions/` cited page-level |
| learn.microsoft.com (azure/well-architected + 1 Architecture Center page) | azure-well-architected-observability.md | 37 | 100 | 6 content pages + 2 checklist pages (traceability) |

`../languages/*.md` are local lookup tables, not source summaries. They aren't counted against any budget and aren't refreshed from these sources.

## Rules for editing elements

- IDs are stable forever. Retire an element by marking its row `(retired)`; never reuse the ID. Prefixes are skill-specific (`OTO-`, `WAFO-`; plan DEC-7) so they can't be confused with `review-api-design`'s `SDK-`, or the WAF prefixes `WAF-` (cost), `WAFR-` (DR) and `WAFM-` (monitoring).
- Level (OpenTelemetry): the strongest RFC 2119 keyword in the summarized sentences; lower-case "should" / "we recommend" on concept pages counts as `SHOULD`; otherwise `REVIEW`. WAF elements are `REVIEW`. The level never changes severity (plan DEC-9; `SKILL.md` step 9).
- Stab. (OpenTelemetry): keep in sync with the pinned semconv/spec version. `D` = the summarized section is Development status. Stability promotions on refresh change `D` → `S`.
- Primary anchor first; list every absorbed anchor so coverage stays auditable. Concept pages without section anchors (`c-zero`, `c-semconv`) are cited page-level (bare key).
- Keep rows to one line (≈ 200 characters where possible). Rows are summaries in our own words (OpenTelemetry docs are CC BY 4.0).
- Every OTO and WAFO ID must be listed by exactly one check in `../checklist.md`, and each standards file's `## OBS-xx` section must agree with it.
- Don't add elements for alerting, dashboards, external probes, probe thresholds or telemetry retention (`review-monitoring`), for secrets/PII in log *messages*, log injection or security-event logging (security skills), or for API-contract headers (`review-api-design` API-15). See plan §4.4 and §10.

## Refresh procedure

1. **Cadence:** quarterly; on each Semantic Conventions minor release that changes HTTP, database, messaging, exception or resource conventions; or when run notes contain ≥ 3 `localized-standard-gap` entries for this skill.
2. **Detect drift:**
   - OpenTelemetry: compare the current semconv version (title of `https://opentelemetry.io/docs/specs/semconv/` or the semantic-conventions releases API) with the pinned v1.45.0 and read the changelog for the localized domains. Check stability promotions (messaging, recording errors, exception severity, `deployment.environment.name`), since they change the Stab. column. Compare the Specification version (title of `/docs/specs/otel/`) with v1.62.0. For concept, SDK, Collector and security pages, compare each page's "Last modified" commit with the page table in `opentelemetry-observability.md`, or list opentelemetry.io commits touching `content/en/docs/concepts/**`, `languages/sdk-configuration/**`, `collector/_index.md` and `security/**` since the pinned commits; diff the changed pages' anchors and text.
   - WAF: re-fetch each pinned page (locale `en-us`), follow redirects, and compare the final URL and the `ms.date` meta value with the header table. A changed date means diffing that page's section text and anchor list. Check `https://learn.microsoft.com/azure/well-architected/toc.json` for added, removed or renamed observability, health-modeling or reliability-target pages. The Health Endpoint Monitoring pattern page isn't in the WAF TOC: compare its `ms.date` and `git_commit_id` meta values directly.
3. **Update:** edit or add elements (new IDs only), mark retired ones `(retired)`, keep each site ≤ 100 elements. Update the coverage map below, the page versions/dates and retrieval date in each file header and in `../sources.md`, and the URL list in `compliance-review-core/references/approved-sources.md` if a page moves.
4. **Language files:** when a review logs a `localized-standard-gap` for an unrecognized logging, telemetry or health library, add it to the matching `../languages/<id>.md`. No source refresh is needed for that.
5. **Verify:**
   - Download the pinned sources into a scratch folder (never into the repo).
   - Script-check: element IDs are contiguous; the checklist mapping rule above holds; every listed anchor exists on its pinned page (by HTML `id`); every content heading anchor (H1–H4) on the pinned pages, minus the boilerplate listed below, appears in the coverage map with zero unaccounted; plus each `dg-mon` antipattern-table row and each `pat-hem` consideration bullet and sub-bullet.
   - Run a review against small sample repos (plan §9 step 9): (a) ASP.NET Core with the OpenTelemetry SDK, `ILogger` templates and `MapHealthChecks` with live/ready tags; (b) Spring Boot with only the Java agent in a Dockerfile and Actuator probe groups; (c) a Python library package; (d) a Flask app with f-string logging, no telemetry and an SLA figure in the README. Expect: `validate` passes; `20-review-observability.json` has `urlsFetched: []`; all 10 checks present; citations use pinned URLs and element IDs; (a) passes WAFO-32/33, and fails WAFO-32 if a single dependency-checking endpoint is the liveness probe; (b) passes OBS-03/OBS-04 framework coverage through zero-code and WAFO-32/33 via Actuator groups; (c) has OBS-05/OBS-06/OBS-07 N/A; (d) fails OBS-01 (OTO-02), OBS-03, OBS-04 and OBS-07 (confidence low, "target without SLI").
6. **Automated first pass:** `python compliance-reviewer/scripts/check_source_drift.py check review-observability` (maintainers only, never during a review) compares the pins in `pins.json` with the live sources; `lint` confirms `pins.json` matches the file headers. Diffing, anchor coverage and the sample review stay manual. Update `pins.json` whenever a pin changes.

## Localization log

### 2026-11-08 — initial localization

- Snapshot: planning snapshot (plan DEC-3) and implementation snapshot both 2026-11-08. All 8 WAF/Architecture Center `ms.date` values match the plan; the pattern page's `git_commit_id` is `9fdb775034a2…` as planned. `devops/monitor-instrument` still redirects to `operational-excellence/observability` (identical content and commit).
- OpenTelemetry versions: semconv **1.45.0** (page title), Specification **1.62.0** (page title). Concept/SDK/Collector/security pages carry a per-page "Last modified" date and commit instead of one site-wide commit, so the page table pins each page's commit (plan §4.2 assumed a single site SHA).
- Script verification: 83 IDs (46 OTO + 37 WAFO), contiguous, each listed by exactly one check and in the matching `## OBS-xx` section; every element anchor exists as an HTML `id` on its pinned page. Coverage map below accounts for all 363 H1–H4 content anchors on the 22 OpenTelemetry pages and the 8 WAF/Architecture Center pages (zero unaccounted), plus the 10 `dg-mon` antipattern rows and the `pat-hem` consideration bullets (9 bullets + 3 security sub-bullets; plan §4.5 counted 10).
- Anchor corrections (the plan's slugified concept anchors were all correct; these replace page-level or approximate citations):
  - Page-level `c-code` → `c-code#configure-the-opentelemetry-api` (OTO-12, OTO-13), `#create-telemetry-data` (OTO-14), `#import-the-opentelemetry-api-and-sdk` (OTO-15), `#configure-the-opentelemetry-sdk` (OTO-29), `#export-data` (OTO-30). Page-level `c-inst` for OTO-15 → `c-inst#additional-opentelemetry-benefits`.
  - `sdk-gen (OTEL_PROPAGATORS)` → `sdk-gen#otel_propagators` (OTO-08); `sdk-gen` → `sdk-gen#otel_traces_sampler` (OTO-44); added `sdk-gen#otel_service_name` to OTO-31.
  - `sdk-otlp` → its four `*-configuration` section anchors (OTO-29). `col` → `col#when-to-use-a-collector` (OTO-30). `sec` → `sec#data-minimization`, `sec#protecting-sensitive-data` (OTO-45). `sc-svc` → `sc-svc#service-attributes` (OTO-31, OTO-32, OTO-34).
  - `sc-exc-logs` → `#recording-an-exception` (OTO-40), `#severity` + `#event-name` (OTO-41), `#when-not-to-record-exceptions` (OTO-43). `sc-res` → `sc-res#service` (OTO-32), `sc-res#environment` (OTO-33). `sc-http-metrics` → `sc-http-metrics#http-server` (OTO-36).
  - OTO-07 primary anchor → `c-logs#opentelemetry-logs-for-applications` (automatic log–trace correlation); OTO-09 added `sc-msg#trace-structure` (span links); OTO-10 primary → `c-prop#context` ("service, or execution unit").
- Wording, Level and Stab. corrections while checking rows against the pinned text (these take precedence over the plan's §5–§6 inventories; severity is unaffected):
  - OTO-03 → `SHOULD` ("the Logs Bridge API should not be called by you directly"); also absorbs `c-logs#logger-provider`.
  - OTO-06 → `SHOULD`; added "evaluated per record, not cached" (source: "should be evaluated per log record and not cached").
  - OTO-07 → `REVIEW` (TraceId/SpanId are optional fields; the only SHOULD is "TraceId present if SpanId present").
  - OTO-13 → `SHOULD` ("you should name it after your library"; version "recommended"). OTO-30 → `SHOULD` ("we recommend using a collector"); "redaction" → "encryption and filtering" (the source's list).
  - OTO-34 → `MUST` (`service.instance.id` MUST be unique per instance). OTO-38 → `MUST` (4xx on server spans MUST be left unset). OTO-45 → `MUST` (`url.full` MUST NOT contain credentials).
  - OTO-40 → Stab. `S` (the "Recording an exception" section is Stable; only "When not to record", "Event name" and "Severity" are Development) and Level `MUST` (exception events MUST be associated with the span context).
  - OTO-20: "parameter values aren't captured by default" → "parameter values are opt-in" (`db.query.parameter.<key>` is Opt-In).
  - OTO-44: added the source's ≈ 1000 traces/s threshold as the high-volume indicator.
  - OTO-46: added "incoming context from untrusted sources is ignored or sanitized" (`c-prop#external-services`); "Applies when" widened to "baggage used or external calls".
  - WAFO-25: "UTC in a standard format" → "universal format (UTC)" (source: "timestamps in universal format").
  - WAFO-35: added `pat-hem#endpoint-behavior` ("bound each dependency check with a timeout"); "full integration tests" kept via `#when-to-use-this-pattern`.
- Language files (plan step 4, user decision 2026-11-08: write from maintainer knowledge, fetch only uncertain names): checked against opentelemetry.io zero-code pages for .NET (`OTEL_DOTNET_AUTO_HOME`, `OTEL_DOTNET_AUTO_{TRACES,METRICS,LOGS}_ENABLED`, `CORECLR_ENABLE_PROFILING`, `DOTNET_STARTUP_HOOKS`, `instrument.sh`), Java agent (`-javaagent`, `JAVA_TOOL_OPTIONS`) and Python (`opentelemetry-instrument`, `opentelemetry-bootstrap`); the OpenTelemetry registry for Python Kafka instrumentations (corrected the plan's `opentelemetry-instrumentation-kafka` → `kafka-python`, `confluent-kafka`); Spring Boot Actuator endpoints docs (`management.endpoint.health.probes.enabled`, `/actuator/health/liveness|readiness`, health groups, `show-details`); ASP.NET Core health-checks docs (`MapHealthChecks` with `Predicate`, `ResponseWriter`). Not fetched (maintainer knowledge; re-check on the first refresh): SLF4J 2 `addKeyValue`, Log4j2 `JsonTemplateLayout`, Spring Boot `logging.structured.format.*` (3.4+), `Context.taskWrapping`, .NET `Activity.AddException` (.NET 9+), `HealthCheckRegistration.Timeout`, python-json-logger, structlog, loguru, `django-health-check`, vendor SDK names.
- Step 9 (sample-repo validation runs) **not yet run** (user decision 2026-11-08: deferred). Run it per refresh step 5 before relying on the new checks, and record the result here.

## Open items

- Plan §10 follow-ups (changes outside this skill): reviewed and closed by `docs/plan_localize-afterplanning-changes.md` on 2026-11-09 (see its Appendix A). Open hand-offs: none.

## `localized-standard-gap` log

_No entries yet._ Record each gap reported in run notes here (date, run ID, description, action taken).

## Coverage map

Reason codes for "not localized":
- **MON**: alerting, dashboards, external probes and probe tuning, diagnostic routing, telemetry storage/retention, health-model tooling. Owned by `review-monitoring` (WAFM-xx, MON-01 … MON-06).
- **DR**: recovery metrics and recoverability. Owned by `review-disaster-recovery`.
- **SEC**: Collector/endpoint security hardening, security-event monitoring, log-message secrets. Owned by the security skills.
- **COST**: telemetry or probe cost. Owned by `review-cost-sustainability`.
- **COL**: Collector configuration and processors (infrastructure). Telemetry-pipeline wiring is `review-monitoring` (MON-06).
- **LIB**: set by the SDK or instrumentation library, or guidance for SDK/library authors; not verifiable as application pass/fail.
- **DOMAIN**: semconv detail beyond the required/conditionally-required attributes localized (optional metrics, per-attribute tables, server-address resolution, examples).
- **ARCH**: architecture or technology choice not verifiable as a pass/fail check.
- **ORG**: organizational practice; not visible in a repo.
- **TOOL**: optional tooling advice, product lists, language-support or status tables.
- **AZ**: Azure-service-specific implementation detail (not generic).
- **BG**: background, definitions, examples or case studies.
- **PARENT**: page title or parent heading whose substance is in its subsections (mapped separately).
- **TRACE**: traceability only (checklist rows).

### OpenTelemetry — section anchors (22 pages)

Excluded as boilerplate: headings without an `id` (page title on some pages, "Feedback", Collector release-list H5s).

**c-logs** (16)
- `opentelemetry-logs` → BG
- `opentelemetry-logs-in-the-opentelemetry-collector` → COL
- `opentelemetry-logs-for-applications` → OTO-07
- `language-support` → TOOL
- `structured-unstructured-and-semistructured-logs` → PARENT
- `structured-logs` → OTO-01
- `unstructured-logs` → OTO-02
- `semistructured-logs` → OTO-01
- `checking-whether-logging-is-enabled` → OTO-06
- `opentelemetry-logging-components` → PARENT
- `log-appender--bridge` → OTO-03
- `logger-provider` → OTO-03, OTO-12
- `logger` → OTO-03
- `log-record-exporter` → OTO-28
- `log-record` → LIB
- `specification` → BG

**c-traces** (18)
- `tracer-provider` → OTO-12
- `tracer` → OTO-13
- `trace-exporters` → OTO-28
- `context-propagation` → OTO-10
- `spans` → OTO-16
- `span-context` → OTO-10
- `attributes` → OTO-22
- `span-events` → OTO-22 (via `when-to-use-span-events-versus-span-attributes`)
- `when-to-use-span-events-versus-span-attributes` → OTO-22
- `span-links` → OTO-22
- `span-status` → OTO-37
- `span-kind` → OTO-17
- `client` → OTO-17
- `server` → OTO-17
- `internal` → OTO-17
- `producer` → OTO-17
- `consumer` → OTO-17
- `specification` → BG

**c-metrics** (11)
- `meter-provider` → OTO-12
- `meter` → OTO-13
- `metric-exporter` → OTO-28
- `metric-instruments` → OTO-24
- `aggregation` → OTO-27
- `views` → OTO-27
- `cardinality-limits` → OTO-25
- `what-the-limit-does-not-apply-to` → OTO-26
- `temporality-and-cardinality-limits` → LIB (temporality tuning)
- `language-support` → TOOL
- `specification` → BG

**c-prop** (12)
- `context` → OTO-10
- `propagation` → OTO-08
- `example` → BG
- `traces` → BG
- `logs` → BG
- `metrics` → BG
- `custom-context-propagation` → OTO-11
- `security-best-practices` → PARENT
- `external-services` → OTO-46
- `baggage` → OTO-46
- `support-in-language-sdks` → TOOL
- `specification` → BG

**c-res** (4)
- `introduction` → BG
- `semantic-attributes-with-sdk-provided-default-value` → OTO-31
- `resource-detectors` → OTO-35
- `custom-resources` → OTO-33

**c-samp** (10)
- `terminology` → BG
- `why-sampling` → PARENT
- `when-to-sample` → OTO-44
- `when-not-to-sample` → OTO-44 (cost trade-offs: COST)
- `head-sampling` → OTO-44
- `tail-sampling` → OTO-44
- `support` → TOOL
- `collector` → COL
- `language-sdks` → TOOL
- `vendors` → TOOL

**c-inst** (1; page cited by OTO-14)
- `additional-opentelemetry-benefits` → OTO-15

**c-code** (5)
- `import-the-opentelemetry-api-and-sdk` → OTO-15
- `configure-the-opentelemetry-api` → OTO-12, OTO-13
- `configure-the-opentelemetry-sdk` → OTO-29
- `create-telemetry-data` → OTO-14
- `export-data` → OTO-30

**c-zero** (0 section anchors; page cited by OTO-14; bytecode/eBPF mechanism detail: LIB)

**c-semconv** (0 section anchors; page cited by OTO-36)

**sdk-gen** (8)
- `otel_service_name` → OTO-31
- `otel_resource_attributes` → OTO-32, OTO-33 (mechanism for setting resource attributes)
- `otel_traces_sampler` → OTO-44
- `otel_traces_sampler_arg` → OTO-44
- `otel_propagators` → OTO-08
- `otel_traces_exporter` → OTO-28
- `otel_metrics_exporter` → OTO-28
- `otel_logs_exporter` → OTO-28

**sdk-otlp** (27)
- `endpoint-configuration` → OTO-29 (and its H3s: `otel_exporter_otlp_endpoint`, `otel_exporter_otlp_traces_endpoint`, `otel_exporter_otlp_metrics_endpoint`, `otel_exporter_otlp_logs_endpoint`, `otel_exporter_otlp_profiles_endpoint` → OTO-29)
- `header-configuration` → OTO-29 (and its H3s: `otel_exporter_otlp_headers`, `otel_exporter_otlp_traces_headers`, `otel_exporter_otlp_metrics_headers`, `otel_exporter_otlp_logs_headers`, `otel_exporter_otlp_profiles_headers` → OTO-29)
- `timeout-configuration` → OTO-29 (and its H3s: `otel_exporter_otlp_timeout`, `otel_exporter_otlp_traces_timeout`, `otel_exporter_otlp_metrics_timeout`, `otel_exporter_otlp_logs_timeout`, `otel_exporter_otlp_profiles_timeout` → OTO-29)
- `protocol-configuration` → OTO-29 (and its H3s: `otel_exporter_otlp_protocol`, `otel_exporter_otlp_traces_protocol`, `otel_exporter_otlp_metrics_protocol`, `otel_exporter_otlp_logs_protocol`, `otel_exporter_otlp_profiles_protocol` → OTO-29)
- `metrics-specific-configuration` → LIB (and its H3s: `otel_exporter_otlp_metrics_temporality_preference`, `otel_exporter_otlp_metrics_default_histogram_aggregation` → LIB, backend-specific tuning)

**col** (6)
- `introduction` → BG
- `objectives` → BG
- `when-to-use-a-collector` → OTO-30
- `collector-security` → SEC
- `status` → TOOL
- `releases` → TOOL

**sec** (8)
- `your-responsibility` → OTO-45
- `sensitive-data-considerations` → OTO-45
- `data-minimization` → OTO-45
- `protecting-sensitive-data` → OTO-45
- `deleting-and-hashing-user-information` → COL (Collector processor example; hashing idea in OTO-45)
- `replacing-userid-with-userhash` → COL
- `truncating-ip-addresses` → COL
- `delete-attributes-with-redaction-processor` → COL

**sc-svc** (2)
- `service-attributes` → OTO-31, OTO-32, OTO-34
- `service-attributes-for-peer-services` → DOMAIN

**sc-res** (13)
- `todos` → BG
- `document-conventions` → BG
- `attributes-with-special-handling` → PARENT
- `semantic-attributes-with-dedicated-environment-variable` → OTO-31 (`OTEL_SERVICE_NAME`)
- `semantic-attributes-with-sdk-provided-default-value` → OTO-31
- `service` → OTO-32
- `telemetry-sdk` → LIB
- `telemetry-distro` → LIB
- `compute-unit` → OTO-35 (detector-provided)
- `compute-instance` → OTO-35 (detector-provided)
- `environment` → OTO-33
- `version-attributes` → BG
- `cloud-provider-specific-attributes` → OTO-35 (detector-provided)

**sc-http-spans** (19)
- `name` → OTO-18
- `status` → OTO-38
- `http-client-span` → OTO-19, OTO-45
- `http-client-span-duration` → LIB
- `http-request-retries-and-redirects` → LIB
- `http-server` → PARENT
- `http-server-definitions` → DOMAIN
- `setting-serveraddress-and-serverport-attributes` → DOMAIN
- `simple-clientserver-example` → BG
- `clientserver-example-with-reverse-proxy` → BG
- `http-server-span` → OTO-19
- `examples` → BG (and its H3s: `http-client-server-example`, `http-client-retries-examples`, `http-client-authorization-retry-examples`, `http-client-redirects-examples`, `http-client-call-dns-error`, `http-client-call-internal-server-error`, `http-server-call-connection-dropped-before-response-body-was-sent` → BG)

**sc-http-metrics** (12)
- `http-server` → OTO-25, OTO-36
- `metric-httpserverrequestduration` → OTO-23, OTO-27
- `metric-httpserveractive_requests` → DOMAIN
- `metric-httpserverrequestbodysize` → DOMAIN
- `metric-httpserverresponsebodysize` → DOMAIN
- `http-client` → PARENT
- `metric-httpclientrequestduration` → OTO-23
- `metric-httpclientrequestbodysize` → DOMAIN
- `metric-httpclientresponsebodysize` → DOMAIN
- `metric-httpclientopen_connections` → DOMAIN
- `metric-httpclientconnectionduration` → DOMAIN
- `metric-httpclientactive_requests` → DOMAIN

**sc-err** (4)
- `what-constitutes-an-error` → OTO-39
- `recording-errors-on-spans` → OTO-37
- `recording-errors-on-metrics` → OTO-42
- `recording-exceptions` → OTO-39

**sc-exc-logs** (12)
- `recording-an-exception` → OTO-40
- `when-not-to-record-exceptions` → OTO-43
- `event-name` → OTO-41
- `severity` → OTO-41 (and its H4s: `fatal-severity`, `error-severity`, `warn-severity`, `info-severity`, `debug-severity`, `trace-severity` → OTO-41)
- `attributes` → LIB (set by the SDK when the exception object is passed; OTO-40)
- `stacktrace-representation` → LIB

**sc-msg** (33)
- `definitions` → BG (and its H3/H4s: `message`, `producer`, `consumer`, `intermediary`, `destinations`, `message-consumption`, `consumer-groups`, `subscriptions`, `conversations`, `temporary-and-anonymous-destinations` → BG)
- `conventions` → PARENT
- `context-propagation` → OTO-09
- `span-name` → OTO-21
- `operation-types` → OTO-21
- `span-kind` → OTO-21
- `span-status` → OTO-37 (general error recording)
- `trace-structure` → OTO-09 (and its H4s: `producer-spans`, `consumer-spans` → OTO-09)
- `messaging-spans` → DOMAIN (and its H3s: `create-span`, `send-span-producer`, `send-span-client`, `receive-span`, `process-span`, `settle-span`, `recording-per-message-attributes-on-batch-operations` → DOMAIN)
- `examples` → BG (and its H3s: `topic-with-multiple-consumers`, `batch-receiving`, `batch-publishing-with-create-spans`, `batch-publishing-without-create-spans` → BG)

**sc-db** (12)
- `name` → OTO-20
- `database-server-address` → DOMAIN (and its H3s: `database-server-endpoints`, `service-discovery` → DOMAIN)
- `span-definition` → OTO-20
- `notes-and-well-known-identifiers-for-dbsystemname` → DOMAIN
- `database-client-span-duration` → LIB
- `sanitization-of-dbquerytext` → OTO-20
- `generating-a-summary-of-the-query` → LIB
- `context-propagation` → DOMAIN (and its H3: `sql-commenter` → DOMAIN)
- `semantic-conventions-for-specific-database-technologies` → DOMAIN

**spec-logdm** (28)
- `design-notes` → BG (and its H3s: `requirements`, `events`, `field-kinds` → BG)
- `log-and-event-record-definition` → PARENT
- `field-timestamp` → LIB
- `field-observedtimestamp` → LIB
- `trace-context-fields` → OTO-07 (and its H4s: `field-traceid`, `field-spanid`, `field-traceflags` → OTO-07)
- `severity-fields` → OTO-04 (and its H4s: `field-severitytext`, `field-severitynumber`, `mapping-of-severitynumber`, `reverse-mapping`, `error-semantics`, `displaying-severity`, `comparing-severity` → OTO-04)
- `field-body` → OTO-05
- `field-resource` → OTO-26 (Resource carries constant context)
- `field-instrumentationscope` → LIB
- `field-attributes` → OTO-05 (and its H4: `errors-and-exceptions` → OTO-40)
- `field-eventname` → OTO-05
- `example-log-records` → BG
- `example-mappings` → BG
- `references` → BG

### WAF and Architecture Center — section anchors (8 pages)

Excluded as boilerplate on every page: `ms--in-this-article`, `ms--feedback`, `ms--additional-resources-mobile-heading`, `next-step`, `next-steps`, `related-links`, `related-resources`, `operational-excellence-checklist`, `reliability-checklist`. Monitoring's coverage map (`review-monitoring/references/standards/MAINTENANCE.md`) shows the other side of every shared page.

**oe-check** (2)
- `design-review-checklist-for-operational-excellence` → PARENT
- `checklist` → TRACE (OE:07 row; other OE rows owned by other skills or ORG)

**re-check** (2)
- `design-review-checklist-for-reliability` → PARENT
- `checklist` → TRACE (RE:04 → WAFO-19 … WAFO-23; RE:10 → WAFO-14 … WAFO-18; other rows owned by `review-reliability` / `review-disaster-recovery`)

**oe-obs** (13)
- `architecture-strategies-for-designing-a-monitoring-system` → PARENT
- `align-telemetry-with-health-and-kpi-models` → WAFO-08, WAFO-23
- `emit-telemetry-from-workload-components` → WAFO-01, WAFO-06, WAFO-26, WAFO-27, WAFO-28, WAFO-29, WAFO-30, WAFO-31 (profiling note, AI notes: TOOL)
- `collect-telemetry-across-the-workload` → ARCH (push vs pull)
- `standardize-data-consolidation` → WAFO-13
- `tailor-storage-and-retention-for-usage-patterns` → MON
- `correlate-data-for-end-to-end-insights` → WAFO-05, WAFO-07
- `analyze-and-visualize-to-support-actionable-decisions` → MON
- `define-alerts-around-meaningful-operational-conditions` → MON
- `design-scalable-durable-telemetry-pipelines` → MON
- `use-observability-to-support-continuous-improvement` → ORG
- `watch-out-for-antipatterns` → BG (pointer to dg-mon antipatterns, mapped below)
- `azure-facilitation` → TOOL

**dg-mon** (20)
- `how-to-build-a-monitoring-system-for-azure-workloads` → PARENT
- `terminology` → BG
- `phase-1---instrumentation` → WAFO-03, WAFO-08, WAFO-12, WAFO-26
- `best-practices-for-instrumentation` → WAFO-02, WAFO-04, WAFO-06, WAFO-24, WAFO-25, WAFO-27
- `example-instrumentation` → BG
- `phase-2---telemetry-data-collection-and-storage` → PARENT
- `telemetry-data-storage-decision` → ARCH
- `telemetry-performance-and-reliability-considerations` → MON
- `telemetry-data-lifecycle-management` → MON
- `telemetry-data-security` → WAFO-31 (encryption, access: MON / SEC)
- `phase-3---correlation-aggregation-analysis` → PARENT
- `correlation` → WAFO-05, WAFO-25
- `supporting-hot-warm-and-cold-analysis` → ARCH
- `best-practices-for-alerts` → MON
- `example-correlation-aggregation-analysis` → BG
- `phase-4---visualization` → MON
- `best-practices-for-visualization` → MON
- `example-visualization` → BG
- `monitoring-antipatterns-and-how-to-avoid-them` → rows below
- `azure-facilitation` → TOOL

**dg-mon antipattern rows** (10 rows; keyed by row name)
- Logging too little, or too much → WAFO-27
- Missing correlation across services → WAFO-04
- Ignoring business context → WAFO-08, WAFO-23
- Unconfigured or mismanaged telemetry → WAFO-30 (diagnostic settings, routing: MON)
- Poor data governance → WAFO-31 (retention: MON)
- Ignoring monitoring costs → COST
- Inconsistent and fragmented telemetry → WAFO-01, WAFO-24
- Poorly designed dashboards → MON
- Alert fatigue → MON
- No trend analysis or forecasting → MON

**dg-hm** (25)
- `health-modeling-for-workloads` → PARENT
- `terminology` → BG
- `what-is-health-health-modeling-and-a-health-model` → WAFO-16
- `health-model-schema` → MON
- `build-a-health-model` → PARENT
- `evaluate-your-workload-design` → ARCH
- `contextualize-using-business-requirements` → WAFO-23
- `map-to-reliability-metrics` → WAFO-19, WAFO-23
- `identify-health-signals` → WAFO-11
- `use-platform-metrics-and-logs` → WAFO-17 (diagnostic settings: MON)
- `add-application-logs` → WAFO-02, WAFO-03, WAFO-28, WAFO-30
- `implement-distributed-tracing` → WAFO-07
- `use-health-probes` → WAFO-14, WAFO-15, WAFO-16 (probe configuration: MON, WAFM-32)
- `adopt-structural-and-functional-monitoring-techniques` → MON
- `model-the-design` → WAFO-17 (propagation rules: ARCH)
- `set-actionable-alerts` → MON
- `visualize-the-model` → MON
- `adopt-your-health-model` → PARENT
- `applicability-to-various-roles` → ORG
- `continuous-validation` → MON
- `organizational-health` → ORG
- `health-trends-and-ai-for-it-operations` → TOOL
- `maintain-your-health-model` → MON
- `azure-facilitation` → TOOL
- `implement-with-azure-monitor-health-models` → TOOL

**re-met** (16)
- `architecture-strategies-for-defining-reliability-targets` → PARENT
- `set-availability-objectives` → WAFO-21
- `consider-common-slos-and-influencing-factors` → WAFO-20
- `determine-the-slo-scope` → WAFO-19, WAFO-22
- `define-composite-slo-targets` → WAFO-19, WAFO-21
- `assess-the-impact-of-microsoft-slas` → WAFO-21
- `implement-multiregion-targets` → WAFO-22 (trade-offs: ARCH)
- `define-recovery-metrics` → DR
- `monitor-and-visualize-the-targets` → MON
- `azure-facilitation` → TOOL
- `example` → BG (and its H3s: `components`, `calculate-a-composite-slo`, `determine-the-overall-composite-slo-result`, `set-the-workload-sla`, `set-the-correctness-slo` → BG)

**re-mon** (14)
- `architecture-strategies-for-monitoring-workload-reliability` → PARENT
- `monitor-workload-functionality` → WAFO-10
- `monitor-user-experience` → WAFO-09
- `track-availability-targets` → MON (target definition: WAFO-19)
- `track-recoverability-targets` → DR
- `make-alerts-actionable-with-a-health-model` → MON
- `monitor-all-layers-of-the-system` → WAFO-15, WAFO-28 (data and network layers: MON)
- `monitor-administrative-dashboards-and-status-apis` → WAFO-18
- `define-and-monitor-stamp-capacity` → MON
- `monitor-load-distribution-across-redundant-instances` → MON
- `detect-failure-modes` → WAFO-12 (malicious activity: SEC)
- `be-informed-about-platform-reliability-status` → MON
- `azure-facilitation` → TOOL
- `example` → BG

**pat-hem** (10)
- `health-endpoint-monitoring-pattern` → PARENT
- `context-and-problem` → BG
- `solution` → WAFO-32, WAFO-33, WAFO-34 (external checks, alerting, remediation: MON; failover capacity: DR)
- `problems-and-considerations` → bullets below
- `when-to-use-this-pattern` → WAFO-35
- `workload-design` → BG (pillar mapping)
- `example` → PARENT
- `endpoint-behavior` → WAFO-32, WAFO-33, WAFO-35
- `app-service-integration` → AZ
- `other-implementation-options` → AZ

**pat-hem consideration bullets** (9 bullets + 3 security sub-bullets; keyed by bullet name)
- Response validation → WAFO-16
- Number of endpoints → WAFO-34
- Shared versus dedicated endpoints → WAFO-36
- Type of information to collect → WAFO-35 (includes the excessive-processing and deep-check-overhead paragraphs)
- Cascading failure from deep probes → WAFO-35
- Caching the endpoint status → WAFO-35
- Probe frequency and cost → COST / MON
- Security for monitoring endpoints → WAFO-37
  - Require authentication → WAFO-37 (probe credential handling: SEC)
  - Restrict network access → WAFO-37 ("a nonstandard port or hard-to-guess path isn't access control"; network rules: SEC)
  - Use a separate endpoint for basic tests → WAFO-37
- Monitoring agent correctness → MON
