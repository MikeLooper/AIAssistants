# Approved Sources

## Link Access Policy

**No review-time fetching** since 2026-11-09 (plan: `docs/plan_localize-review-twelve-factor.md`, C-16 option (a)).

- The orchestrator, the worker and the skills never fetch a URL during a review, whether it is listed here or not. Each subject reviews against its local files: the `references/standards/` files a skill declares under `## Standards (local, authoritative)`, otherwise its `checklist.md` and `sources.md`. Citations use the URLs recorded in those files, without fetching them.
- This file is a **maintainer-only registry**. It lists the exact pages that maintainers may fetch to refresh a skill's local standards, following that skill's `references/standards/MAINTENANCE.md`. The orchestrator and the workers don't load it during a review.
- If a reviewer finds that a situation needs an external source, it doesn't fetch the source. It marks the check N/A with a reason and adds `localized-standard-gap: <description>` to `notes` for maintainers.
- A maintainer who adds a page to this registry records it under the owning subject's section, as an exact page. Site-wide prefixes aren't allowed.
- `linkApprovals` in `state.json` and `urlsFetched` in transition files stay in the schemas for compatibility with older runs. New runs leave them empty.

## API Design

**Maintenance-only** since 2026-11-07: `review-api-design` declares local standards (plan: `docs/plan_localize-review-api-design.md`). Workers don't fetch these during a review.

- https://spec.openapis.org/oas/latest.html
- https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
- Pinned versions used for localization and citations:
  - https://spec.openapis.org/oas/v3.0.4.html
  - https://spec.openapis.org/oas/v3.1.2.html
  - https://spec.openapis.org/oas/v3.2.1.html
  - https://spec.openapis.org/oas/v2.0.html
  - https://github.com/microsoft/api-guidelines/blob/15c12663c363250bea4d60aa054e81466a1f0106/azure/Guidelines.md
  - https://azure.github.io/azure-sdk/general_azurecore.html (telemetry and distributed-tracing policies only)
- Drift checks (maintainers; added 2026-11-09 for `scripts/check_source_drift.py`): https://api.github.com/repos/microsoft/api-guidelines/commits, https://api.github.com/repos/Azure/azure-sdk/commits

## Cost & Sustainability

**Maintenance-only** since 2026-11-07: `review-cost-sustainability` declares local standards (plan: `docs/plan_localize-review-cost-sustainability.md`). Workers don't fetch these during a review. Exact pages only — this entry does not allowlist other learn.microsoft.com/azure/well-architected pages.

- Azure Well-Architected Framework (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/checklist
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/cost-model
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/collect-review-cost-data
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/set-spending-guardrails
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/get-best-rates
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/align-usage-to-billing-increments
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/optimize-component-costs
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/optimize-environment-costs
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/optimize-flow-costs
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/optimize-data-costs
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/optimize-code-costs
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/optimize-scaling-costs
  - https://learn.microsoft.com/azure/well-architected/cost-optimization/consolidation
  - https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-cost-optimization-recommendations
  - https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-performance-efficiency-recommendations
  - https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-reliability-recommendations
  - https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-security-recommendations
  - https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-operational-excellence-recommendations
  - https://learn.microsoft.com/azure/well-architected/toc.json (drift check only)
- Green Software Foundation:
  - https://learn.greensoftware.foundation/ (principle pages: carbon-awareness, energy-efficiency, hardware-efficiency, measurement, carbon-efficiency, climate-commitments)
  - https://patterns.greensoftware.foundation/ (pattern pages and `sitemap.xml`; pages listed in the skill's MAINTENANCE.md coverage map)
- Drift checks (maintainers): https://api.github.com/repos/Green-Software-Foundation/learn/commits, https://api.github.com/repos/Green-Software-Foundation/patterns/commits

## Dependency Management

**Maintenance-only** since 2026-11-07: `review-dependency-management` declares local standards (plan: `docs/plan_localize-review-dependency-management.md`). Workers don't fetch these during a review. Vulnerability data comes only from approved analyzers, never from these or other URLs. Exact pages only — this entry does not allowlist other pages on these sites.

- OWASP:
  - https://top10.owasp.org/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html
- Runtime and framework lifecycle (vendor pages; machine-readable feeds for maintainers):
  - https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core
  - https://dotnetcli.blob.core.windows.net/dotnet/release-metadata/releases-index.json
  - https://learn.microsoft.com/lifecycle/products/microsoft-net-framework
  - https://adoptium.net/support/
  - https://spring.io/projects/spring-boot (#support), https://spring.io/projects/spring-framework (#support)
  - https://api.spring.io/projects/spring-boot/generations, https://api.spring.io/projects/spring-framework/generations
  - https://devguide.python.org/versions/
  - https://github.com/nodejs/Release (`#release-schedule`, `#end-of-life-releases`) and https://raw.githubusercontent.com/nodejs/Release/main/schedule.json (added 2026-11-09, NODE)
  - https://expressjs.com/en/advanced/best-practice-security.html (Express end-of-life section; added 2026-11-09, EXP-01; also listed under Security — Web & API)
- Drift checks (maintainers): https://api.github.com/repos/OWASP/Top10/commits, https://api.github.com/repos/OWASP/CheatSheetSeries/commits

## Disaster Recovery

**Maintenance-only** since 2026-11-08: `review-disaster-recovery` declares local standards (plan: `docs/plan_localize-review-disaster-recovery.md`). Workers don't fetch these during a review. Exact pages only — this entry does not allowlist other learn.microsoft.com/azure/well-architected pages.

- Azure Well-Architected Framework (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/azure/well-architected/reliability/checklist
  - https://learn.microsoft.com/azure/well-architected/reliability/principles
  - https://learn.microsoft.com/azure/well-architected/reliability/metrics
  - https://learn.microsoft.com/azure/well-architected/reliability/redundancy
  - https://learn.microsoft.com/azure/well-architected/reliability/reliability-test
  - https://learn.microsoft.com/azure/well-architected/reliability/disaster-recovery
  - https://learn.microsoft.com/azure/well-architected/design-guides/disaster-recovery
  - https://learn.microsoft.com/azure/well-architected/design-guides/regions-availability-zones
  - https://learn.microsoft.com/azure/well-architected/toc.json (drift check only; also listed under Cost & Sustainability)
- NIST:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final (drift check: revision or withdrawal notice)
- OWASP (added 2026-11-09, OSM-01; section 2.9 only):
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html (also listed under Security — Operational)

## Maintainability

**Localized, no external sources** since 2026-11-08: `review-maintainability` reviews only against its local rubric
(`references/standards/maintainability-rubric.md`; plan: `docs/plan_localize-review-maintainability.md`).
Workers fetch nothing for this subject, including URLs listed under other subjects. There are no maintenance URLs.

## Monitoring

**Maintenance-only** since 2026-11-08: `review-monitoring` declares local standards (plan: `docs/plan_localize-review-monitoring.md`). Workers don't fetch these during a review. Exact pages only — this entry does not allowlist other learn.microsoft.com/azure/well-architected or sre.google pages (in particular not the `operational-excellence/` landing page).

- Azure Well-Architected Framework (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/azure/well-architected/operational-excellence/checklist
  - https://learn.microsoft.com/azure/well-architected/operational-excellence/observability
  - https://learn.microsoft.com/azure/well-architected/reliability/monitoring
  - https://learn.microsoft.com/azure/well-architected/design-guides/monitoring
  - https://learn.microsoft.com/azure/well-architected/design-guides/health-modeling
  - https://learn.microsoft.com/azure/well-architected/performance-efficiency/monitoring
  - https://learn.microsoft.com/azure/well-architected/security/monitor-threats (SE:10; added 2026-11-09, WAFM-41 … WAFM-44)
  - https://learn.microsoft.com/azure/well-architected/reliability/checklist (RE:10 traceability; also listed under Disaster Recovery)
  - https://learn.microsoft.com/azure/well-architected/toc.json (drift check only; also listed under Cost & Sustainability)
- Google SRE:
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://sre.google/sre-book/practical-alerting/
  - https://sre.google/workbook/monitoring/
  - https://sre.google/workbook/alerting-on-slos/
  - https://sre.google/sre-book/table-of-contents/, https://sre.google/workbook/table-of-contents/ (drift check only)

## Observability

**Maintenance-only** since 2026-11-08: `review-observability` declares local standards (plan: `docs/plan_localize-review-observability.md`). Workers don't fetch these during a review. Exact pages only — this entry does not allowlist other opentelemetry.io or learn.microsoft.com pages (in particular not `https://opentelemetry.io/docs/` as a prefix, nor the `operational-excellence/` landing page, nor other `azure/architecture/` pages).

- OpenTelemetry (concept, SDK, Collector and security pages pinned by per-page commit; semconv pinned to v1.45.0; Specification v1.62.0):
  - https://opentelemetry.io/docs/concepts/signals/logs/
  - https://opentelemetry.io/docs/concepts/signals/traces/
  - https://opentelemetry.io/docs/concepts/signals/metrics/
  - https://opentelemetry.io/docs/concepts/context-propagation/
  - https://opentelemetry.io/docs/concepts/resources/
  - https://opentelemetry.io/docs/concepts/sampling/
  - https://opentelemetry.io/docs/concepts/instrumentation/, https://opentelemetry.io/docs/concepts/instrumentation/code-based/, https://opentelemetry.io/docs/concepts/instrumentation/zero-code/
  - https://opentelemetry.io/docs/concepts/semantic-conventions/
  - https://opentelemetry.io/docs/languages/sdk-configuration/general/
  - https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/
  - https://opentelemetry.io/docs/collector/
  - https://opentelemetry.io/docs/security/handling-sensitive-data/
  - https://opentelemetry.io/docs/specs/semconv/ (version check only), and the pages under it: registry/attributes/service/, resource/, http/http-spans/, http/http-metrics/, general/recording-errors/, exceptions/exceptions-logs/, messaging/messaging-spans/, db/database-spans/
  - https://opentelemetry.io/docs/specs/otel/ (version check only), https://opentelemetry.io/docs/specs/otel/logs/data-model/
- Azure Well-Architected Framework (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/azure/well-architected/operational-excellence/observability (also listed under Monitoring)
  - https://learn.microsoft.com/azure/well-architected/design-guides/monitoring (also listed under Monitoring)
  - https://learn.microsoft.com/azure/well-architected/design-guides/health-modeling (also listed under Monitoring)
  - https://learn.microsoft.com/azure/well-architected/reliability/metrics (also listed under Disaster Recovery)
  - https://learn.microsoft.com/azure/well-architected/reliability/monitoring (also listed under Monitoring)
  - https://learn.microsoft.com/azure/well-architected/operational-excellence/checklist (OE:07 traceability; also listed under Monitoring)
  - https://learn.microsoft.com/azure/well-architected/reliability/checklist (RE:04/RE:10 traceability; also listed under Disaster Recovery)
  - https://learn.microsoft.com/azure/well-architected/toc.json (drift check only; also listed under Cost & Sustainability)
- Azure Architecture Center (pinned page; locale-less URL):
  - https://learn.microsoft.com/azure/architecture/patterns/health-endpoint-monitoring (OBS-06 liveness/readiness)
- Drift checks (maintainers): https://api.github.com/repos/open-telemetry/opentelemetry.io/commits, https://api.github.com/repos/open-telemetry/semantic-conventions/releases

## Performance

**Maintenance-only** since 2026-11-08: `review-performance` declares local standards (plan: `docs/plan_localize-review-performance.md`). Workers don't fetch these during a review. Exact pages only — this entry does not allowlist other learn.microsoft.com/azure/well-architected or learn.microsoft.com/azure/architecture pages (in particular not the `performance-efficiency/` landing page or `antipatterns/retry-storm/`, which is owned by `review-reliability`; see `docs/plan_localize-review-reliability.md`).

- Azure Well-Architected Framework (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/azure/well-architected/performance-efficiency/checklist (traceability)
  - https://learn.microsoft.com/azure/well-architected/performance-efficiency/select-services
  - https://learn.microsoft.com/azure/well-architected/performance-efficiency/scale-partition
  - https://learn.microsoft.com/azure/well-architected/performance-efficiency/optimize-code-infrastructure
  - https://learn.microsoft.com/azure/well-architected/performance-efficiency/optimize-data-performance
  - https://learn.microsoft.com/azure/well-architected/performance-efficiency/prioritize-critical-flows
  - https://learn.microsoft.com/azure/well-architected/performance-efficiency/optimize-operational-tasks
  - https://learn.microsoft.com/azure/well-architected/toc.json (drift check only; also listed under Cost & Sustainability)
- Azure Architecture Center (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/azure/architecture/antipatterns/ (catalog; drift check)
  - https://learn.microsoft.com/azure/architecture/antipatterns/busy-database/
  - https://learn.microsoft.com/azure/architecture/antipatterns/busy-front-end/
  - https://learn.microsoft.com/azure/architecture/antipatterns/chatty-io/
  - https://learn.microsoft.com/azure/architecture/antipatterns/extraneous-fetching/
  - https://learn.microsoft.com/azure/architecture/antipatterns/improper-instantiation/
  - https://learn.microsoft.com/azure/architecture/antipatterns/monolithic-persistence/
  - https://learn.microsoft.com/azure/architecture/antipatterns/no-caching/
  - https://learn.microsoft.com/azure/architecture/antipatterns/noisy-neighbor/noisy-neighbor
  - https://learn.microsoft.com/azure/architecture/antipatterns/synchronous-io/
  - https://learn.microsoft.com/azure/architecture/best-practices/caching
  - https://learn.microsoft.com/azure/architecture/patterns/cache-aside
  - https://learn.microsoft.com/azure/architecture/toc.json (drift check only)

## Reliability

**Maintenance-only** since 2026-11-08: `review-reliability` declares local standards (plan: `docs/plan_localize-review-reliability.md`). Workers don't fetch these during a review. Exact pages only — this entry does not allowlist other learn.microsoft.com/azure/well-architected or learn.microsoft.com/azure/architecture pages (in particular not the `reliability/` landing page or the `design-guides/handle-transient-faults` and `design-guides/background-jobs` pages).

- Azure Well-Architected Framework (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/azure/well-architected/reliability/checklist (traceability; also listed under Disaster Recovery)
  - https://learn.microsoft.com/azure/well-architected/reliability/principles (also listed under Disaster Recovery)
  - https://learn.microsoft.com/azure/well-architected/reliability/redundancy (also listed under Disaster Recovery)
  - https://learn.microsoft.com/azure/well-architected/reliability/scaling
  - https://learn.microsoft.com/azure/well-architected/reliability/self-preservation
  - https://learn.microsoft.com/azure/well-architected/reliability/failure-mode-analysis
  - https://learn.microsoft.com/azure/well-architected/toc.json (drift check only; also listed under Cost & Sustainability)
- Azure Architecture Center (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/azure/architecture/best-practices/transient-faults
  - https://learn.microsoft.com/azure/architecture/best-practices/background-jobs
  - https://learn.microsoft.com/azure/architecture/patterns/retry
  - https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker
  - https://learn.microsoft.com/azure/architecture/patterns/bulkhead
  - https://learn.microsoft.com/azure/architecture/patterns/throttling
  - https://learn.microsoft.com/azure/architecture/patterns/rate-limiting-pattern
  - https://learn.microsoft.com/azure/architecture/patterns/queue-based-load-leveling
  - https://learn.microsoft.com/azure/architecture/patterns/competing-consumers
  - https://learn.microsoft.com/azure/architecture/patterns/idempotent-consumer
  - https://learn.microsoft.com/azure/architecture/patterns/compensating-transaction
  - https://learn.microsoft.com/azure/architecture/antipatterns/retry-storm/
  - https://learn.microsoft.com/azure/architecture/toc.json (drift check only; also listed under Performance)

## Security — OWASP Top 10

Exact pages only, since 2026-11-08 — this entry no longer allowlists `https://top10.owasp.org/` as a site prefix
(`https://owasp.org/Top10/` permanently redirects to that host). No unlocalized skill cites the Top 10; each page
below is also listed in the section of the subject that localizes it.

- https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/ (Security — Identity & Access; also Testing, testing sentences only)
- https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/ (Security — Web & API)
- https://top10.owasp.org/2025/A03_2025-Software_Supply_Chain_Failures/ (Dependency Management)
- https://top10.owasp.org/2025/A05_2025-Injection/ (Security — Input & Injection; also Testing, testing sentences only)
- https://top10.owasp.org/2025/A07_2025-Authentication_Failures/ (Security — Identity & Access)
- https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures/ (Security — Operational)
- https://top10.owasp.org/2025/A10_2025-Mishandling_of_Exceptional_Conditions/ (Security — Operational)

## Security — Identity & Access

**Maintenance-only** since 2026-11-08: `review-security-identity-access` declares local standards
(plan: `docs/plan_localize-review-security-identity-access.md`). Workers don't fetch these during a review.
Exact pages only — this entry does not allowlist other pages on these sites (in particular not other
docs.spring.io or docs.djangoproject.com pages or versions).

- OWASP Cheat Sheets (pinned by commit in the skill's `references/sources.md`):
  - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Zero_Trust_Architecture_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html (identity sections; also listed under Security — Operational and Security — Input & Injection)
- OWASP Top 10:2025:
  - https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/
  - https://top10.owasp.org/2025/A07_2025-Authentication_Failures/
- Spring Security reference 7.1 (versioned paths):
  - https://docs.spring.io/spring-security/reference/7.1/servlet/authorization/authorize-http-requests.html
  - https://docs.spring.io/spring-security/reference/7.1/servlet/authorization/method-security.html
  - https://docs.spring.io/spring-security/reference/7.1/servlet/authentication/session-management.html
  - https://docs.spring.io/spring-security/reference/7.1/servlet/authentication/logout.html
  - https://docs.spring.io/spring-security/reference/7.1/servlet/exploits/csrf.html
  - https://docs.spring.io/spring-security/reference/7.1/features/authentication/password-storage.html
  - https://docs.spring.io/spring-security/reference/7.1/servlet/oauth2/resource-server/jwt.html
  - https://docs.spring.io/spring-security/reference/7.1/servlet/oauth2/client/authorization-grants.html
  - https://docs.spring.io/spring-security/reference/7.1/servlet/oauth2/login/core.html
- Django 6.1 documentation (versioned paths):
  - https://docs.djangoproject.com/en/6.1/topics/auth/default/
  - https://docs.djangoproject.com/en/6.1/topics/auth/passwords/
  - https://docs.djangoproject.com/en/6.1/topics/http/sessions/
  - https://docs.djangoproject.com/en/6.1/ref/settings/ (session, CSRF-cookie and password settings only; `SECURE_*` and `X_FRAME_OPTIONS` also listed under Security — Web & API)
  - https://docs.djangoproject.com/en/6.1/ref/csrf/
  - https://docs.djangoproject.com/en/6.1/ref/middleware/ (authentication middleware only; security, clickjacking and CSP middleware listed under Security — Web & API)
  - https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/
- JavaScript/TypeScript (added 2026-11-09, NDA):
  - https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html (also listed under other security subjects)
  - https://expressjs.com/en/advanced/best-practice-security.html (also listed under other subjects)
- Drift and version checks (maintainers): https://api.github.com/repos/OWASP/CheatSheetSeries/commits,
  https://api.github.com/repos/OWASP/Top10/commits (also listed under Dependency Management),
  https://api.spring.io/projects/spring-security/releases, https://docs.djangoproject.com/en/stable/ (redirect target = current version)

## Security — Input & Injection

**Maintenance-only** since 2026-11-08: `review-security-input-injection` declares local standards
(plan: `docs/plan_localize-review-security-input-injection.md`). Workers don't fetch these during a review.
Exact pages only — this entry does not allowlist other pages on these sites (in particular not other
learn.microsoft.com, docs.oracle.com, docs.spring.io, docs.python.org or docs.djangoproject.com pages or versions).

- OWASP Cheat Sheets (pinned by commit in the skill's `references/sources.md`):
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html (added 2026-11-09, SSRF-01 … SSRF-08)
  - https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html (input-handling sections; also listed under Security — Identity & Access and Security — Operational)
  - https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html
- OWASP Top 10:2025:
  - https://top10.owasp.org/2025/A05_2025-Injection/ (also listed under Security — OWASP Top 10)
- Microsoft Learn (locale-less; version in `view=` where offered):
  - https://learn.microsoft.com/ef/core/querying/sql-queries
  - https://learn.microsoft.com/aspnet/core/mvc/models/file-uploads?view=aspnetcore-10.0
  - https://learn.microsoft.com/aspnet/core/security/cross-site-scripting?view=aspnetcore-10.0
  - https://learn.microsoft.com/aspnet/core/mvc/models/validation?view=aspnetcore-10.0
  - https://learn.microsoft.com/dotnet/api/system.xml.xmlreadersettings.dtdprocessing?view=net-10.0
  - https://learn.microsoft.com/dotnet/standard/serialization/binaryformatter-security-guide
  - https://learn.microsoft.com/dotnet/api/system.diagnostics.processstartinfo.argumentlist?view=net-10.0
- Oracle:
  - https://www.oracle.com/java/technologies/javase/seccodeguide.html (sections 1, 3, 5, 8)
  - https://docs.oracle.com/en/java/javase/25/security/java-api-xml-processing-jaxp-security-guide.html
- Spring Data JPA reference (current GA; version recorded in the skill):
  - https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html
- Python 3.15 documentation (versioned paths):
  - https://docs.python.org/3.15/library/xml.html
  - https://docs.python.org/3.15/library/subprocess.html
  - https://docs.python.org/3.15/library/pickle.html
  - https://docs.python.org/3.15/library/sqlite3.html
- Django 6.1 documentation (versioned paths):
  - https://docs.djangoproject.com/en/6.1/topics/security/ (SSL/HTTPS, CORS and CSP sections also listed under Security — Web & API)
  - https://docs.djangoproject.com/en/6.1/topics/db/sql/
  - https://docs.djangoproject.com/en/6.1/ref/models/querysets/ (`extra()` only)
  - https://docs.djangoproject.com/en/6.1/ref/settings/ (upload settings only; also listed under Security — Identity & Access for other settings)
  - https://docs.djangoproject.com/en/6.1/ref/templates/builtins/ (`autoescape`, `safe` only)
  - https://docs.djangoproject.com/en/6.1/ref/utils/ (`mark_safe` only)
- JavaScript/TypeScript (added 2026-11-09, NDI):
  - https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html (also listed under other security subjects)
  - https://expressjs.com/en/advanced/best-practice-security.html (also listed under other subjects)
- Drift and version checks (maintainers): https://api.github.com/repos/OWASP/CheatSheetSeries/commits and
  https://api.github.com/repos/OWASP/Top10/commits (both also listed under other subjects),
  https://api.spring.io/projects/spring-data-jpa/releases, https://docs.python.org/3/ (current version),
  https://docs.djangoproject.com/en/stable/ (redirect target = current version)

## Security — Operational

**Maintenance-only** since 2026-11-08: `review-security-operational` declares local standards
(plan: `docs/plan_localize-review-security-operational.md`). Workers don't fetch these during a review.
Exact pages only — this entry does not allowlist other pages on these sites (in particular not other
learn.microsoft.com, docs.spring.io, docs.djangoproject.com or docs.python.org pages or versions).

- OWASP Cheat Sheets (pinned by commit in the skill's `references/sources.md`):
  - https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html (`#management-endpoints` only; added 2026-11-09, ORS-01; also listed under Security — Web & API and Software Quality)
  - https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html (configuration, deployment and data-protection sections; also listed under Security — Identity & Access and Security — Input & Injection)
- OWASP Top 10:2025 (also listed under Security — OWASP Top 10):
  - https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures/
  - https://top10.owasp.org/2025/A10_2025-Mishandling_of_Exceptional_Conditions/
- Microsoft Learn (locale-less; version in `view=` where offered):
  - https://learn.microsoft.com/aspnet/core/fundamentals/error-handling?view=aspnetcore-10.0
  - https://learn.microsoft.com/aspnet/core/fundamentals/environments?view=aspnetcore-10.0
  - https://learn.microsoft.com/aspnet/core/security/app-secrets?view=aspnetcore-10.0
  - https://learn.microsoft.com/aspnet/core/security/key-vault-configuration?view=aspnetcore-10.0
  - https://learn.microsoft.com/aspnet/core/fundamentals/http-logging/?view=aspnetcore-10.0
  - https://learn.microsoft.com/dotnet/core/extensions/logging/overview
  - https://learn.microsoft.com/dotnet/core/extensions/data-redaction
- Spring Boot reference (current GA; version recorded in the skill):
  - https://docs.spring.io/spring-boot/reference/web/servlet.html (error handling only)
  - https://docs.spring.io/spring-boot/reference/actuator/endpoints.html (exposing, security, sanitization only)
  - https://docs.spring.io/spring-boot/appendix/application-properties/index.html (`spring.web.error.*`, `management.endpoint.*.show-values` rows only)
  - https://docs.spring.io/spring-boot/reference/features/external-config.html (configuration trees, encrypting only)
  - https://docs.spring.io/spring-boot/reference/features/logging.html (file output, rotation, structured logging only)
- Django 6.1 documentation (versioned paths):
  - https://docs.djangoproject.com/en/6.1/ref/settings/ (`DEBUG` only; also listed under other subjects for other settings)
  - https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/ (also listed under Security — Identity & Access)
  - https://docs.djangoproject.com/en/6.1/howto/error-reporting/
  - https://docs.djangoproject.com/en/6.1/topics/logging/
  - https://docs.djangoproject.com/en/6.1/ref/logging/ (default logging configuration only)
- Python 3.15 documentation (versioned paths):
  - https://docs.python.org/3.15/library/logging.config.html
  - https://docs.python.org/3.15/howto/logging.html
- JavaScript/TypeScript (added 2026-11-09, NDO):
  - https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html (also listed under other security subjects)
  - https://expressjs.com/en/advanced/best-practice-security.html (also listed under other subjects)
- Drift and version checks (maintainers): https://api.github.com/repos/OWASP/CheatSheetSeries/commits and
  https://api.github.com/repos/OWASP/Top10/commits (both also listed under other subjects),
  https://api.spring.io/projects/spring-boot/releases, https://docs.python.org/3/ (current version),
  https://docs.djangoproject.com/en/stable/ (redirect target = current version)

## Security — Web & API

**Maintenance-only** since 2026-11-09: `review-security-web-api` declares local standards
(plan: `docs/plan_localize-review-security-web-api.md`). Workers don't fetch these during a review.
Exact pages only — this entry does not allowlist other pages on these sites (in particular not other
learn.microsoft.com, docs.spring.io or docs.djangoproject.com pages or versions).

- OWASP Cheat Sheets (pinned by commit in the skill's `references/sources.md`):
  - https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html (CORS and offline sections only)
  - https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html (protocol, cipher and application sections only)
- OWASP Top 10:2025 (also listed under Security — OWASP Top 10):
  - https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/
- MDN Web Docs (added 2026-11-09, MDN-01):
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/require-trusted-types-for
- Microsoft Learn (locale-less; version in `view=`):
  - https://learn.microsoft.com/aspnet/core/security/enforcing-ssl?view=aspnetcore-10.0
  - https://learn.microsoft.com/aspnet/core/security/cors?view=aspnetcore-10.0
  - https://learn.microsoft.com/aspnet/core/web-api/advanced/formatting?view=aspnetcore-10.0
- Spring Security reference (current GA; version recorded in the skill):
  - https://docs.spring.io/spring-security/reference/features/exploits/headers.html
  - https://docs.spring.io/spring-security/reference/servlet/exploits/headers.html
  - https://docs.spring.io/spring-security/reference/servlet/exploits/http.html
  - https://docs.spring.io/spring-security/reference/servlet/integrations/cors.html
- Spring Framework reference (current GA; version recorded in the skill):
  - https://docs.spring.io/spring-framework/reference/web/webmvc-cors.html
- Django 6.1 documentation (versioned paths):
  - https://docs.djangoproject.com/en/6.1/ref/middleware/ (security, clickjacking and CSP middleware only; also listed under Security — Identity & Access)
  - https://docs.djangoproject.com/en/6.1/ref/settings/ (`SECURE_*` and `X_FRAME_OPTIONS` only; also listed under other subjects for other settings)
  - https://docs.djangoproject.com/en/6.1/ref/clickjacking/
  - https://docs.djangoproject.com/en/6.1/ref/csp/
  - https://docs.djangoproject.com/en/6.1/topics/security/ (SSL/HTTPS, CORS and CSP sections only; also listed under Security — Input & Injection)
- JavaScript/TypeScript (added 2026-11-09, NDW):
  - https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html (also listed under other security subjects)
  - https://expressjs.com/en/advanced/best-practice-security.html (also listed under other subjects)
- Drift and version checks (maintainers): https://api.github.com/repos/OWASP/CheatSheetSeries/commits and
  https://api.github.com/repos/OWASP/Top10/commits (both also listed under other subjects),
  https://api.spring.io/projects/spring-security/releases, https://api.spring.io/projects/spring-framework/releases,
  https://docs.djangoproject.com/en/stable/ (redirect target = current version)

## Software Lifecycle

**Maintenance-only** since 2026-11-09: `review-software-lifecycle` declares local standards
(plan: `docs/plan_localize-review-software-lifecycle.md`). Workers don't fetch these during a review.
Exact pages only — this entry does not allowlist other semver.org, nist.gov, slsa.dev or github.com pages.
(Replaces the former "Semantic Versioning" section.)

- Semantic Versioning:
  - https://semver.org/ (drift: still serves 2.0.0)
  - https://semver.org/spec/v2.0.0.html
- NIST SP 800-218 SSDF:
  - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf
  - https://csrc.nist.gov/pubs/sp/800/218/final (drift: supersession or withdrawal notice)
  - https://csrc.nist.gov/pubs/sp/800/218/r1/ipd and https://csrc.nist.gov/pubs/sp/800/218/r1/final (drift: Rev. 1 / v1.2 status)
- SLSA (pinned v1.2 pages):
  - https://slsa.dev/spec/v1.2/build-requirements
  - https://slsa.dev/spec/v1.2/build-track-basics
  - https://slsa.dev/spec/v1.2/source-requirements
  - https://slsa.dev/spec/v1.2/distributing-provenance
  - https://slsa.dev/spec/ (drift only: redirect target = current version)
- OpenSSF Scorecard:
  - https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md
  - https://raw.githubusercontent.com/ossf/scorecard/v5.6.0/docs/checks.md (raw text of the same file)
- Azure Well-Architected Framework (added 2026-11-09, SDP-01; locale-less URL):
  - https://learn.microsoft.com/azure/well-architected/operational-excellence/safe-deployments
- Drift checks (maintainers): https://api.github.com/repos/ossf/scorecard/releases/latest,
  https://api.github.com/repos/slsa-framework/slsa/commits, https://api.github.com/repos/semver/semver/commits

## Software Quality

**Maintenance-only** since 2026-11-09: `review-software-quality` declares local standards
(plan: `docs/plan_localize-review-software-quality.md`). Workers don't fetch these during a review.
Exact pages only — this entry does not allowlist other iso25000.com, learn.microsoft.com, google.github.io,
peps.python.org, martinfowler.com or refactoring.com pages (in particular not `/azure/architecture/patterns/`).
(Replaces the former "Coding Standards" and "Software Quality" sections.)

- ISO/IEC 25010:2023 (iso25000.com summary):
  - https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
  - https://iso25000.com/index.php/en/iso-25000-standards/iso-25010?start=5
- Azure Architecture Center (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/azure/architecture/guide/architecture-styles/
  - https://learn.microsoft.com/azure/architecture/guide/architecture-styles/n-tier
  - https://learn.microsoft.com/azure/architecture/guide/architecture-styles/web-queue-worker
  - https://learn.microsoft.com/azure/architecture/guide/architecture-styles/microservices
  - https://learn.microsoft.com/azure/architecture/guide/design-principles/design-for-evolution
  - https://learn.microsoft.com/azure/architecture/toc.json (drift check only; also listed under Performance and Reliability)
- Microsoft C# (pinned pages; locale-less URLs):
  - https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions
  - https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/identifier-names
- Google Java Style Guide:
  - https://google.github.io/styleguide/javaguide.html
- Google TypeScript Style Guide (added 2026-11-09, GTS):
  - https://google.github.io/styleguide/tsguide.html
- Python Enhancement Proposals:
  - https://peps.python.org/pep-0008/
  - https://peps.python.org/pep-0257/
- Martin Fowler:
  - https://martinfowler.com/bliki/CodeSmell.html
  - https://martinfowler.com/bliki/PresentationDomainDataLayering.html
  - https://refactoring.com/catalog/ and the pages `https://refactoring.com/catalog/<name>.html` listed in the
    skill's MAINTENANCE.md coverage map
- OWASP (reference for rubric element SQR-37 only; added 2026-11-09):
  - https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html (`#preventing-out-of-order-api-execution`; also listed under Security — Web & API and Security — Operational)
- Drift checks (maintainers): https://api.github.com/repos/MicrosoftDocs/architecture-center/commits,
  https://api.github.com/repos/dotnet/docs/commits, https://api.github.com/repos/google/styleguide/commits,
  https://api.github.com/repos/python/peps/commits

## Testing

**Maintenance-only** since 2026-11-09: `review-testing` declares local standards
(plan: `docs/plan_localize-review-testing.md`). Workers don't fetch these during a review.
Exact pages only — this entry does not allowlist other martinfowler.com, learn.microsoft.com,
cheatsheetseries.owasp.org, top10.owasp.org, nvlpubs.nist.gov or github.com pages.

- Martin Fowler:
  - https://martinfowler.com/articles/practical-test-pyramid.html
  - https://martinfowler.com/bliki/TestCoverage.html
  - https://martinfowler.com/articles/nonDeterminism.html
  - https://martinfowler.com/articles/mocksArentStubs.html
  - https://martinfowler.com/articles/continuousIntegration.html
- Microsoft Learn (locale-less URL):
  - https://learn.microsoft.com/dotnet/core/testing/unit-testing-best-practices
  - https://learn.microsoft.com/azure/well-architected/performance-efficiency/performance-test (PE:06; added 2026-11-09, AZT)
  - https://learn.microsoft.com/azure/well-architected/reliability/reliability-test (RE:08; added 2026-11-09, AZT; also listed under Disaster Recovery)
  - https://learn.microsoft.com/azure/architecture/best-practices/transient-faults (testing section only; added 2026-11-09, AZT; also listed under Reliability)
- OWASP (testing sentences only):
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html (also listed under Security — Identity & Access)
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html (also listed under Security — Operational)
  - https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/ (also listed under Security — OWASP Top 10)
  - https://top10.owasp.org/2025/A05_2025-Injection/ (also listed under Security — OWASP Top 10)
- NIST SP 800-218 SSDF (PW.8 only):
  - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf (also listed under Software Lifecycle)
- OpenSSF Scorecard (Fuzzing, CI-Tests only):
  - https://github.com/ossf/scorecard/blob/v5.6.0/docs/checks.md (also listed under Software Lifecycle)
  - https://raw.githubusercontent.com/ossf/scorecard/v5.6.0/docs/checks.md (also listed under Software Lifecycle)
- Drift checks (maintainers): https://api.github.com/repos/dotnet/docs/commits,
  https://api.github.com/repos/OWASP/CheatSheetSeries/commits, https://api.github.com/repos/OWASP/Top10/commits,
  https://api.github.com/repos/ossf/scorecard/releases/latest (all also listed under other subjects)

## Twelve-Factor App

**Maintenance-only** since 2026-11-09: `review-twelve-factor` declares local standards
(plan: `docs/plan_localize-review-twelve-factor.md`). Workers don't fetch these during a review.
Exact pages only — this entry does not allowlist other 12factor.net pages (in particular not the translations
under `/<locale>/`) or the site's GitHub repositories.

- https://12factor.net/ (introduction and factor list; applicability provenance and drift check)
- https://12factor.net/codebase
- https://12factor.net/dependencies
- https://12factor.net/config
- https://12factor.net/backing-services
- https://12factor.net/build-release-run
- https://12factor.net/processes
- https://12factor.net/port-binding
- https://12factor.net/concurrency
- https://12factor.net/disposability
- https://12factor.net/dev-prod-parity
- https://12factor.net/logs
- https://12factor.net/admin-processes
